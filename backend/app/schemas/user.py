from pydantic import BaseModel
from app.models.enums import Role


class UserOut(BaseModel):
    id: int
    telegram_id: int
    username: str | None
    avatar_url: str | None
    bio: str | None
    role: Role

    class Config:
        from_attributes = True
