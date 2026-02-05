from pydantic import BaseModel
from app.models.enums import AdType


class AdCampaignCreate(BaseModel):
    title: str
    ad_type: AdType
    media_url: str | None = None
    cta_text: str | None = None
    cta_url: str | None = None
    emoji: str | None = None
    is_active: bool = True


class AdCampaignOut(BaseModel):
    id: int
    title: str
    ad_type: AdType
    media_url: str | None
    cta_text: str | None
    cta_url: str | None
    emoji: str | None
    is_active: bool
    impressions: int
    clicks: int

    class Config:
        from_attributes = True
