import os
import shutil
from fastapi import UploadFile, BackgroundTasks, HTTPException

from models import Video, User
from video.schemas import UploadVideo
from uuid import uuid4
from settings.settings import MEDIA_ROOT


async def save_video(
        user: User,
        file: UploadFile,
        title: str,
        description: str,
        back_tasks: BackgroundTasks
):
    file_name = os.path.join(MEDIA_ROOT, str(user.id), str(uuid4())+'.mp4')
    if file.content_type == 'video/mp4':
        back_tasks.add_task(write_video, file_name, file)
    else:
        raise HTTPException(status_code=418, detail="It isn't mp4")
    info = UploadVideo(title=title, description=description)
    return await Video.objects.create(file=file_name, user=user, **info.dict())


def write_video(file_name: str, file: UploadFile):
    # async with aiofiles.open(file_name, 'wb') as buffer:
    #     data = await file.read()
    #     await buffer.write(data)
    with open(file_name, 'wb') as buffer:
        shutil.copyfileobj(file.file, buffer)