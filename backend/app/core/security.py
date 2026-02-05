from datetime import datetime, timedelta
from jose import jwt
from app.core.config import settings


def create_token(data: dict, expires_delta: timedelta) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.jwt_secret, algorithm=settings.jwt_algorithm)


def create_access_token(subject: str) -> str:
    return create_token({"sub": subject}, timedelta(minutes=settings.jwt_access_ttl_minutes))


def create_refresh_token(subject: str) -> str:
    return create_token({"sub": subject}, timedelta(minutes=settings.jwt_refresh_ttl_minutes))
