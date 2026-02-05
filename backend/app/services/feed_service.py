import httpx
from sqlalchemy import select, desc
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.config import settings
from app.models.post import Post
from app.models.enums import PostStatus, FeedType
from app.models.ai_threshold import AiThresholds


async def fetch_feed(db: AsyncSession, feed_type: FeedType, user_id: int, limit: int, offset: int) -> list[Post]:
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            resp = await client.post(
                f"{settings.ml_service_url}/feed",
                json={"user_id": user_id, "feed_type": feed_type.value, "limit": limit, "offset": offset},
            )
        resp.raise_for_status()
        ids = resp.json().get("post_ids", [])
        if ids:
            result = await db.execute(select(Post).where(Post.id.in_(ids), Post.status == PostStatus.published))
            return list(result.scalars())
    except Exception:
        pass

    threshold_result = await db.execute(select(AiThresholds))
    thresholds = threshold_result.scalar_one_or_none()
    uniqueness_threshold = thresholds.uniqueness_threshold if thresholds else 0.7

    if feed_type == FeedType.popular:
        order = desc(Post.likes_count + Post.comments_count + Post.reposts_count)
    else:
        order = desc(Post.created_at)

    result = await db.execute(
        select(Post)
        .where(Post.status == PostStatus.published)
        .where(Post.uniqueness_score >= uniqueness_threshold if feed_type == FeedType.recommended else True)
        .order_by(order)
        .limit(limit)
        .offset(offset)
    )
    return list(result.scalars())
