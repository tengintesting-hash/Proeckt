from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.session import get_db
from app.core.deps import get_current_user
from app.models.subscription import Subscription
from app.models.channel import Channel

router = APIRouter()


@router.post("/{channel_id}")
async def toggle_subscription(
    channel_id: int,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    result = await db.execute(select(Channel).where(Channel.id == channel_id))
    channel = result.scalar_one_or_none()
    if not channel:
        raise HTTPException(status_code=404, detail="Channel not found")
    result = await db.execute(
        select(Subscription).where(Subscription.channel_id == channel_id, Subscription.user_id == current_user.id)
    )
    sub = result.scalar_one_or_none()
    if sub:
        await db.delete(sub)
        channel.subscribers_count -= 1
        action = "unsubscribed"
    else:
        sub = Subscription(channel_id=channel_id, user_id=current_user.id)
        db.add(sub)
        channel.subscribers_count += 1
        action = "subscribed"
    await db.commit()
    return {"status": action, "subscribers": channel.subscribers_count}
