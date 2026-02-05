from pydantic import BaseModel
from app.models.enums import PostStatus, PostCategory


class PostCreate(BaseModel):
    channel_id: int
    text: str
    media_url: str | None = None
    media_type: str | None = None
    category: PostCategory = PostCategory.other


class PostOut(BaseModel):
    id: int
    channel_id: int
    text: str
    media_url: str | None
    media_type: str | None
    category: PostCategory
    status: PostStatus
    is_repost: bool
    original_post_id: int | None
    likes_count: int
    dislikes_count: int
    comments_count: int
    reposts_count: int
    nsfw_score: float
    uniqueness_score: float

    class Config:
        from_attributes = True
