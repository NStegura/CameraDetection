import asyncio
from fastapi import APIRouter, UploadFile, File, Form, BackgroundTasks, Depends
from aiortc import RTCPeerConnection, RTCSessionDescription
from aiortc.contrib.media import MediaPlayer, MediaRelay, MediaBlackhole
from starlette.requests import Request
from starlette.responses import HTMLResponse
from starlette.templating import Jinja2Templates

from settings.settings import MEDIA_ROOT
from video_hosting.schemas import Offer
from video_hosting.services import get_media, create_local_tracks, VideoTransformTrack


templates = Jinja2Templates(directory="./templates")
video_hosting_router = APIRouter(prefix='/video', tags=['video_hosting'])


@video_hosting_router.get("/", response_class=HTMLResponse)
async def index(request: Request):
    media_files = get_media(MEDIA_ROOT)
    return templates.TemplateResponse("index.html", {"request": request, 'media_files': media_files})


@video_hosting_router.get("/cv", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index_cv.html", {"request": request})


@video_hosting_router.post("/offer")
async def offer(params: Offer):

    offer = RTCSessionDescription(sdp=params.sdp, type=params.type)
    pc = RTCPeerConnection()
    pcs.add(pc)
    recorder = MediaBlackhole()

    @pc.on("connectionstatechange")
    async def on_connectionstatechange():
        print("Connection state is %s" % pc.connectionState)
        if pc.connectionState == "failed":
            await pc.close()
            pcs.discard(pc)

    # open media source
    try:
        audio, video = create_local_tracks(play_from=params.play_from)
    except Exception as ex:
        print(ex)
        return index

    await pc.setRemoteDescription(offer)
    for t in pc.getTransceivers():
        if t.kind == "audio" and audio:
            pc.addTrack(audio)
        elif t.kind == "video" and video:
            pc.addTrack(video)

    answer = await pc.createAnswer()
    await pc.setLocalDescription(answer)

    return {"sdp": pc.localDescription.sdp, "type": pc.localDescription.type}


@video_hosting_router.post("/offer_cv")
async def offer(params: Offer):
    offer = RTCSessionDescription(sdp=params.sdp, type=params.type)

    pc = RTCPeerConnection()
    pcs.add(pc)
    recorder = MediaBlackhole()

    relay = MediaRelay()

    @pc.on("connectionstatechange")
    async def on_connectionstatechange():
        print("Connection state is %s" % pc.connectionState)
        if pc.connectionState == "failed":
            await pc.close()
            pcs.discard(pc)

    # open media source
    # audio, video = create_local_tracks(play_from=params.play_from)

    @pc.on("track")
    def on_track(track):

        if track.kind == "video":
            pc.addTrack(
                VideoTransformTrack(relay.subscribe(track), transform=params.video_transform)
            )

        @track.on("ended")
        async def on_ended():
            await recorder.stop()

    # handle offer
    await pc.setRemoteDescription(offer)
    await recorder.start()

    # send answer
    answer = await pc.createAnswer()
    await pc.setRemoteDescription(offer)
    await pc.setLocalDescription(answer)

    return {"sdp": pc.localDescription.sdp, "type": pc.localDescription.type}


@video_hosting_router.on_event("shutdown")
async def on_shutdown():
    # close peer connections
    coros = [pc.close() for pc in pcs]
    await asyncio.gather(*coros)
    pcs.clear()

pcs = set()