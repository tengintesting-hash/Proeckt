from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.session import get_db
from app.schemas.channel import ChannelCreate, ChannelOut
from app.core.deps import get_current_user
from app.models.channel import Channel

router = APIRouter()


@router.post("/", response_model=ChannelOut)
async def create_channel(
    payload: ChannelCreate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    existing = await db.execute(select(Channel).where(Channel.handle == payload.handle))
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Handle already taken")
    channel = Channel(owner_id=current_user.id, **payload.model_dump())
    db.add(channel)
    await db.commit()
    await db.refresh(channel)
    return channel


@router.get("/{channel_id}", response_model=ChannelOut)
async def get_channel(channel_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Channel).where(Channel.id == channel_id))
    channel = result.scalar_one_or_none()
    if not channel:
        raise HTTPException(status_code=404, detail="Channel not found")
    return channel
