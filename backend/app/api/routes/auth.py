import json
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.session import get_db
from app.schemas.auth import TelegramAuthRequest, TokenPair
from app.core.security import create_access_token, create_refresh_token
from app.utils.telegram import validate_init_data
from app.models.user import User
from app.models.enums import Role

router = APIRouter()


@router.post("/telegram", response_model=TokenPair)
async def telegram_auth(payload: TelegramAuthRequest, db: AsyncSession = Depends(get_db)):
    data = validate_init_data(payload.init_data)
    user_data = data.get("user")
    if not user_data:
        raise HTTPException(status_code=400, detail="Missing user data")
    user_info = json.loads(user_data)
    telegram_id = int(user_info.get("id"))
    username = user_info.get("username")
    result = await db.execute(select(User).where(User.telegram_id == telegram_id))
    user = result.scalar_one_or_none()
    if not user:
        user = User(telegram_id=telegram_id, username=username, role=Role.user)
        db.add(user)
        await db.commit()
        await db.refresh(user)
    access = create_access_token(str(user.id))
    refresh = create_refresh_token(str(user.id))
    return TokenPair(access_token=access, refresh_token=refresh)
