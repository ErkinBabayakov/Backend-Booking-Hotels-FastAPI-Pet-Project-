import shutil

from pathlib import Path
from fastapi import UploadFile
from src.services.base import BaseService
from src.tasks.tasks import resize_image

BASE_DIR = Path(__file__).resolve().parent.parent.parent


class ImageService(BaseService):
    def upload_image(self, file: UploadFile):
        image_path = f"{BASE_DIR}/src/static/images/{file.filename}"

        with open(f"{image_path}", "wb+") as new_file:
            shutil.copyfileobj(file.file, new_file)

        resize_image(image_path)
