import asyncio
import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from auth.api import auth
from video.api import video_router
from video_hosting.api import video_hosting_router


app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")


app.include_router(auth)
app.include_router(video_hosting_router)
app.include_router(video_router)




