import asyncio
import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from auth.api import auth
from video.api import video_router

ROOT = os.path.dirname(__file__)

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")


app.include_router(auth)
app.include_router(video_router)



