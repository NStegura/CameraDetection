from typing import List

from fastapi import APIRouter, UploadFile, File, Form, Request, BackgroundTasks
from starlette.responses import StreamingResponse, HTMLResponse
from starlette.templating import Jinja2Templates


from video.schemas import GetListVideo
from video.models import Video, User
from video.services import save_video, open_file

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


# @video_router.get('/video/{video_pk}')
# async def get_video(video_pk: int):
#     file = await Video.objects.select_related('user').get(pk=video_pk)
#     file_like = open(file.file, mode='rb')
#     return StreamingResponse(file_like, media_type="video/mp4")


@video_router.get("/user/{user_pk}", response_model=List[GetListVideo])
async def get_list_video(user_pk: int):
    return await Video.objects.filter(user=user_pk).all()


@video_router.get("/index/{video_pk}", response_class=HTMLResponse)
async def get_video(request: Request, video_pk: int):
    return templates.TemplateResponse("index.html", {"request": request, "path": video_pk})


@video_router.get("/video/{video_pk}")
async def get_streaming_video(request: Request, video_pk: int) -> StreamingResponse:
    file, status_code, content_length, headers = await open_file(request, video_pk)
    response = StreamingResponse(
        file,
        media_type='video/mp4',
        status_code=status_code,
    )

    response.headers.update({
        'Accept-Ranges': 'bytes',
        'Content-Length': str(content_length),
        **headers,
    })
    return response


@video_router.get("/404", response_class=HTMLResponse)
async def error_404(request: Request):
    return templates.TemplateResponse("404.html", {"request": request})


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
