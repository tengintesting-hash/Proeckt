import httpx
from app.core.config import settings


async def moderate_post(text: str, media_url: str | None, media_type: str | None) -> float:
    async with httpx.AsyncClient(timeout=30) as client:
        resp = await client.post(
            f"{settings.ml_service_url}/moderate",
            json={"text": text, "media_url": media_url, "media_type": media_type},
        )
    resp.raise_for_status()
    data = resp.json()
    return float(data["score"])


async def uniqueness_score(media_url: str | None, media_type: str | None) -> float:
    async with httpx.AsyncClient(timeout=30) as client:
        resp = await client.post(
            f"{settings.ml_service_url}/uniqueness",
            json={"media_url": media_url, "media_type": media_type},
        )
    resp.raise_for_status()
    data = resp.json()
    return float(data["score"])
