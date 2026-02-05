from pathlib import Path
from uuid import uuid4
from fastapi import UploadFile
from app.core.config import settings


async def save_upload(file: UploadFile) -> str:
    media_dir = Path(settings.media_root)
    media_dir.mkdir(parents=True, exist_ok=True)
    extension = Path(file.filename or "").suffix
    filename = f"{uuid4().hex}{extension}"
    path = media_dir / filename
    content = await file.read()
    path.write_bytes(content)
    return f"/media/{filename}"
