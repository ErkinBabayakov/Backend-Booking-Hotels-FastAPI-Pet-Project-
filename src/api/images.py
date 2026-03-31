from fastapi import APIRouter, UploadFile
from pathlib import Path

from src.services.images import ImageService

BASE_DIR = Path(__file__).resolve().parent.parent.parent

router = APIRouter(prefix="/images", tags=["Изображения отелей"])


@router.post("", summary="Загрузить изображение")
def upload_image(file: UploadFile):
    ImageService().upload_image(file)
