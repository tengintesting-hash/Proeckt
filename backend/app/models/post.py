from sqlalchemy import String, DateTime, func, ForeignKey, Text, Integer, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base
from app.models.enums import PostStatus, PostCategory


class Post(Base):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(primary_key=True)
    channel_id: Mapped[int] = mapped_column(ForeignKey("channels.id"), index=True)
    text: Mapped[str] = mapped_column(Text)
    media_url: Mapped[str | None] = mapped_column(String(255), nullable=True)
    media_type: Mapped[str | None] = mapped_column(String(32), nullable=True)
    category: Mapped[PostCategory] = mapped_column(default=PostCategory.other)
    status: Mapped[PostStatus] = mapped_column(default=PostStatus.pending_ai_check)
    is_repost: Mapped[bool] = mapped_column(Boolean, default=False)
    original_post_id: Mapped[int | None] = mapped_column(ForeignKey("posts.id"), nullable=True)
    likes_count: Mapped[int] = mapped_column(Integer, default=0)
    dislikes_count: Mapped[int] = mapped_column(Integer, default=0)
    comments_count: Mapped[int] = mapped_column(Integer, default=0)
    reposts_count: Mapped[int] = mapped_column(Integer, default=0)
    nsfw_score: Mapped[float] = mapped_column(default=0.0)
    uniqueness_score: Mapped[float] = mapped_column(default=1.0)
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    channel = relationship("Channel")
    original_post = relationship("Post", remote_side=[id])
