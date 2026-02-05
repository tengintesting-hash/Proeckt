from sqlalchemy import DateTime, func, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base
from app.models.enums import ReactionType


class Reaction(Base):
    __tablename__ = "reactions"
    __table_args__ = (UniqueConstraint("post_id", "user_id", name="uix_post_user"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    post_id: Mapped[int] = mapped_column(ForeignKey("posts.id"), index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    reaction: Mapped[ReactionType] = mapped_column()
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
