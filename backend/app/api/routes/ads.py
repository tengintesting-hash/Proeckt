from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.session import get_db
from app.schemas.ad import AdCampaignCreate, AdCampaignOut
from app.core.deps import get_current_user
from app.models.ad import AdCampaign, AdImpression
from app.models.enums import Role

router = APIRouter()


@router.post("/", response_model=AdCampaignOut)
async def create_campaign(
    payload: AdCampaignCreate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    if current_user.role not in {Role.admin, Role.moderator}:
        raise HTTPException(status_code=403, detail="Not allowed")
    campaign = AdCampaign(**payload.model_dump())
    db.add(campaign)
    await db.commit()
    await db.refresh(campaign)
    return campaign


@router.get("/next", response_model=AdCampaignOut)
async def get_next_ad(
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    result = await db.execute(select(AdCampaign).where(AdCampaign.is_active == True))
    campaign = result.scalars().first()
    if not campaign:
        raise HTTPException(status_code=404, detail="No ads")
    campaign.impressions += 1
    impression = AdImpression(campaign_id=campaign.id, user_id=current_user.id, clicked=False)
    db.add(impression)
    await db.commit()
    return campaign


@router.post("/{campaign_id}/click")
async def click_ad(
    campaign_id: int,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    result = await db.execute(select(AdCampaign).where(AdCampaign.id == campaign_id))
    campaign = result.scalar_one_or_none()
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")
    campaign.clicks += 1
    impression = AdImpression(campaign_id=campaign.id, user_id=current_user.id, clicked=True)
    db.add(impression)
    await db.commit()
    return {"status": "clicked"}
