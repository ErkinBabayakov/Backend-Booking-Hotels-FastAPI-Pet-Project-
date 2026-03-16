import shutil

from fastapi import APIRouter, UploadFile
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent

from src.tasks.tasks import resize_image


router = APIRouter(prefix="/images", tags=["Изображения отелей"])

@router.post("", summary="Загрузить изображение")
def upload_image(file: UploadFile):
    image_path = f"{BASE_DIR}/src/static/images/{file.filename}"

    with open(f"{image_path}", "wb+") as new_file:
        shutil.copyfileobj(file.file, new_file)

    resize_image(image_path)