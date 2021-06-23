import os
import shutil
from typing import List
from fastapi import APIRouter, UploadFile, File
from settings.settings import MEDIA_ROOT


video_router = APIRouter(tags=['video'])


@video_router.post('/')
async def root(video: UploadFile = File(...)):
    with open(os.path.join(MEDIA_ROOT, video.filename), 'wb') as buffer:
        shutil.copyfileobj(video.file, buffer)
    return {"file_name": video.filename}


@video_router.post('/img')
async def upload_image(files: List[UploadFile] = File(...)):
    for img in files:
        with open(os.path.join(MEDIA_ROOT, img.filename), 'wb') as buffer:
            shutil.copyfileobj(img.file, buffer)
    return {"file_name": files}
