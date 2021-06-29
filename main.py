from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from db import database, metadata, engine

from user.api import user_router
from video.api import video_router
from video_hosting.api import video_hosting_router


app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

metadata.create_all(engine)  # cоздать бд
app.state.database = database


@app.on_event("startup")
async def startup() -> None:
    database_ = app.state.database
    if not database_.is_connected:
        await database_.connect()


@app.on_event("shutdown")
async def shutdown() -> None:
    database_ = app.state.database
    if database_.is_connected:
        await database_.disconnect()


app.include_router(user_router)
app.include_router(video_hosting_router)
app.include_router(video_router)




