from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.session import get_db
from app.core.deps import get_current_user
from app.models.enums import Role, PostStatus
from app.models.post import Post
from app.models.ai_threshold import AiThresholds
from app.schemas.admin import ModerationUpdate, ThresholdsUpdate, ThresholdsOut

router = APIRouter()


def require_admin(user):
    if user.role not in {Role.admin, Role.moderator}:
        raise HTTPException(status_code=403, detail="Not allowed")


@router.get("/posts/pending", response_model=list[int])
async def pending_posts(db: AsyncSession = Depends(get_db), current_user=Depends(get_current_user)):
    require_admin(current_user)
    result = await db.execute(select(Post.id).where(Post.status == PostStatus.pending_review))
    return list(result.scalars())


@router.post("/posts/{post_id}")
async def update_post_status(
    post_id: int,
    payload: ModerationUpdate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    require_admin(current_user)
    result = await db.execute(select(Post).where(Post.id == post_id))
    post = result.scalar_one_or_none()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    post.status = payload.status
    db.add(post)
    await db.commit()
    return {"status": "updated"}


@router.get("/ai-thresholds", response_model=ThresholdsOut)
async def get_thresholds(db: AsyncSession = Depends(get_db), current_user=Depends(get_current_user)):
    require_admin(current_user)
    result = await db.execute(select(AiThresholds))
    thresholds = result.scalar_one_or_none()
    if not thresholds:
        thresholds = AiThresholds()
        db.add(thresholds)
        await db.commit()
        await db.refresh(thresholds)
    return thresholds


@router.post("/ai-thresholds", response_model=ThresholdsOut)
async def update_thresholds(
    payload: ThresholdsUpdate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    require_admin(current_user)
    result = await db.execute(select(AiThresholds))
    thresholds = result.scalar_one_or_none()
    if not thresholds:
        thresholds = AiThresholds(**payload.model_dump())
        db.add(thresholds)
    else:
        thresholds.text_threshold = payload.text_threshold
        thresholds.media_threshold = payload.media_threshold
        thresholds.uniqueness_threshold = payload.uniqueness_threshold
    await db.commit()
    await db.refresh(thresholds)
    return thresholds
