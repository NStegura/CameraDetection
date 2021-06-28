import os
from typing import List

from fastapi import APIRouter, UploadFile, File, Form, Request, BackgroundTasks, HTTPException
from starlette.responses import StreamingResponse
from starlette.templating import Jinja2Templates


from video.schemas import UploadVideo, GetVideo, Message
from models import Video, User
from video.services import write_video, save_video

video_router = APIRouter(tags=['video'])
templates = Jinja2Templates(directory='templates')


@video_router.post('/')
async def create_video(
        back_tasks: BackgroundTasks,
        title: str = Form(...),
        description: str = Form(...),
        file: UploadFile = File(...)
):
    user = await User.objects.first()
    return await save_video(user, file, title, description, back_tasks)


@video_router.get('/video/{video_pk}', responses={404: {'model': Message}})
async def get_video(video_pk: int):
    file = await Video.objects.select_related('user').get(pk=video_pk)
    file_like = open(file.dict().get('file'), mode='rb')
    return StreamingResponse(file_like, media_type="video/mp4")


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
