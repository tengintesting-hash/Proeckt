from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from redis.asyncio import Redis
from fastapi_limiter import FastAPILimiter
from app.core.config import settings
from sqlalchemy import select
from app.api import api_router
from app.db.session import SessionLocal
from app.models.user import User
from app.models.enums import Role

app = FastAPI(title=settings.app_name)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api")
app.mount("/media", StaticFiles(directory=settings.media_root), name="media")


@app.on_event("startup")
async def startup():
    redis = Redis.from_url(settings.redis_url, encoding="utf-8", decode_responses=True)
    await FastAPILimiter.init(redis)
    if settings.admin_telegram_id:
        async with SessionLocal() as session:
            result = await session.execute(select(User).where(User.telegram_id == settings.admin_telegram_id))
            user = result.scalar_one_or_none()
            if not user:
                user = User(telegram_id=settings.admin_telegram_id, role=Role.admin)
                session.add(user)
            else:
                user.role = Role.admin
            await session.commit()
