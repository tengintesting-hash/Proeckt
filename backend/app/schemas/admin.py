from pydantic import BaseModel
from app.models.enums import PostStatus


class ModerationUpdate(BaseModel):
    status: PostStatus


class ThresholdsUpdate(BaseModel):
    text_threshold: float
    media_threshold: float
    uniqueness_threshold: float


class ThresholdsOut(BaseModel):
    text_threshold: float
    media_threshold: float
    uniqueness_threshold: float

    class Config:
        from_attributes = True
