from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.session import get_db, SessionLocal
from app.schemas.post import PostCreate, PostOut
from app.core.deps import get_current_user
from app.models.post import Post
from app.models.channel import Channel
from app.models.enums import PostStatus
from app.services.ai_service import moderate_post, uniqueness_score
from app.models.repost import Repost
from app.models.ai_threshold import AiThresholds

router = APIRouter()


def channel_ready(channel: Channel) -> bool:
    return all([channel.name, channel.handle, channel.avatar_url, channel.banner_url, channel.bio])


async def run_ai_checks(post_id: int):
    async with SessionLocal() as session:
        result = await session.execute(select(Post).where(Post.id == post_id))
        post = result.scalar_one_or_none()
        if not post:
            return
        score = await moderate_post(post.text, post.media_url, post.media_type)
        unique_score = await uniqueness_score(post.media_url, post.media_type)
        threshold_result = await session.execute(select(AiThresholds))
        thresholds = threshold_result.scalar_one_or_none() or AiThresholds()
        base_threshold = max(thresholds.text_threshold, thresholds.media_threshold)
        post.nsfw_score = score
        post.uniqueness_score = unique_score
        if score < base_threshold:
            post.status = PostStatus.published
        elif score < base_threshold + 0.2:
            post.status = PostStatus.pending_review
        else:
            post.status = PostStatus.blocked
        session.add(post)
        await session.commit()


@router.post("/", response_model=PostOut)
async def create_post(
    payload: PostCreate,
    background: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    result = await db.execute(select(Channel).where(Channel.id == payload.channel_id))
    channel = result.scalar_one_or_none()
    if not channel or channel.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not allowed")
    if not channel_ready(channel):
        raise HTTPException(status_code=400, detail="Channel profile incomplete")
    post = Post(**payload.model_dump())
    db.add(post)
    await db.commit()
    await db.refresh(post)
    background.add_task(run_ai_checks, post.id)
    return post


@router.get("/{post_id}", response_model=PostOut)
async def get_post(post_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Post).where(Post.id == post_id))
    post = result.scalar_one_or_none()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post


@router.post("/{post_id}/repost")
async def repost_post(
    post_id: int,
    channel_id: int | None = None,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    result = await db.execute(select(Post).where(Post.id == post_id))
    post = result.scalar_one_or_none()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    if channel_id:
        result = await db.execute(select(Channel).where(Channel.id == channel_id))
        channel = result.scalar_one_or_none()
        if not channel or channel.owner_id != current_user.id:
            raise HTTPException(status_code=403, detail="Not allowed")
        repost = Repost(post_id=post_id, channel_id=channel_id)
    else:
        repost = Repost(post_id=post_id, user_id=current_user.id)
    post.reposts_count += 1
    db.add(repost)
    await db.commit()
    return {"status": "reposted"}
