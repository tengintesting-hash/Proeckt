from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.core.deps import get_current_user
from app.schemas.post import PostOut
from app.models.enums import FeedType
from app.services.feed_service import fetch_feed

router = APIRouter()


@router.get("/{feed_type}", response_model=list[PostOut])
async def get_feed(
    feed_type: FeedType,
    limit: int = 20,
    offset: int = 0,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    posts = await fetch_feed(db, feed_type, current_user.id, limit, offset)
    return posts
