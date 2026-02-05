from fastapi import APIRouter, Depends, UploadFile, File
from app.core.deps import get_current_user
from app.utils.media import save_upload

router = APIRouter()


@router.post("/upload")
async def upload_media(
    file: UploadFile = File(...),
    user=Depends(get_current_user),
):
    path = await save_upload(file)
    return {"url": path}
