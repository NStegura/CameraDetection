import os
import shutil
from typing import List
from fastapi import APIRouter, UploadFile, File, Form, Request

from settings.settings import MEDIA_ROOT
from video.schemas import UploadVideo, GetVideo, Message
from models import Video, User

video_router = APIRouter(tags=['video'])


@video_router.post('/')
async def create_video(
        title: str = Form(...), description: str = Form(...), video: UploadFile = File(...)
):
    info = UploadVideo(title=title, description=description)
    with open(os.path.join(MEDIA_ROOT, video.filename), 'wb') as buffer:
        shutil.copyfileobj(video.file, buffer)
    user = await User.objects.first()
    return await Video.objects.create(file=video.filename, user=user, **info.dict())


@video_router.get('/video/{video_pk}', response_model=GetVideo, responses={404: {'model': Message}})
async def get_video(video_pk: int):
    return await Video.objects.select_related('user').get(pk=video_pk)


# @video_router.post('/info')
# async def info_set(info: UploadVideo):
#     return info


# @video_router.get('/video', response_model=GetVideo, responses={404: {'model': Message}})
# async def get_video():
#     user = {'id': 25, 'name': 'Pipec'}
#     video = {'title': 'Test', 'description': 'Description'}
#     info = GetVideo(user=user, video=video)
#     info = Message(message='Item not found')
#     # return info
#     # return JSONResponse(status_code=404, content={"message": "Item not found"})
#     return JSONResponse(status_code=404, content=info.dict())


# @video_router.get('/info')
# async def info_get2():
#     title = 'Test'
#     desc = 'Description'
#     tags = ['g', 'f']
#     return {'title': title, 'description': desc, 'tags': tags}


# @video_router.get('/test')
# async def get_test(req: Request):
#     print(req.base_url)
#     return {}


# @video_router.post('/img')
# async def upload_image(files: List[UploadFile] = File(...)):
#     for img in files:
#         with open(os.path.join(MEDIA_ROOT, img.filename), 'wb') as buffer:
#             shutil.copyfileobj(img.file, buffer)
#     return {"file_name": files}


# @video_router.post('/video')
# async def create_video(video: Video):
#     await video.save()
#     return video
