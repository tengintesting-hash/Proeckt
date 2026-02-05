from sqlalchemy import String, DateTime, func, ForeignKey, Boolean, Integer
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base
from app.models.enums import AdType


class AdCampaign(Base):
    __tablename__ = "ad_campaigns"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(120))
    ad_type: Mapped[AdType] = mapped_column()
    media_url: Mapped[str | None] = mapped_column(String(255), nullable=True)
    cta_text: Mapped[str | None] = mapped_column(String(64), nullable=True)
    cta_url: Mapped[str | None] = mapped_column(String(255), nullable=True)
    emoji: Mapped[str | None] = mapped_column(String(16), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    impressions: Mapped[int] = mapped_column(Integer, default=0)
    clicks: Mapped[int] = mapped_column(Integer, default=0)
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class AdImpression(Base):
    __tablename__ = "ad_impressions"

    id: Mapped[int] = mapped_column(primary_key=True)
    campaign_id: Mapped[int] = mapped_column(ForeignKey("ad_campaigns.id"), index=True)
    user_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"), nullable=True)
    clicked: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
