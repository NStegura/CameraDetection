import asyncio
import os
import platform

import cv2

from aiortc import MediaStreamTrack, RTCPeerConnection, RTCSessionDescription
from aiortc.contrib.media import MediaPlayer, MediaRelay, MediaBlackhole

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from starlette.requests import Request
from starlette.responses import HTMLResponse
from starlette.templating import Jinja2Templates

from src.schemas import Offer
from video_transform import VideoTransformTrack

ROOT = os.path.dirname(__file__)

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

relay = None
webcam = None


def create_local_tracks(play_from=None, options={"framerate": "30", "video_size": "640x480"}):

    global relay, webcam
    # play_from = './production ID_3765335.mp4'
    if play_from:
        player = MediaPlayer(play_from)
        return player.audio, player.video
    else:
        if relay is None:
            if platform.system() == "Darwin":
                webcam = MediaPlayer(
                    "default:none", format="avfoundation", options=options
                )
            elif platform.system() == "Windows":
                webcam = MediaPlayer(
                    "video=USB2.0 PC CAMERA", format="dshow", options=options
                )
            else:
                webcam = MediaPlayer("/dev/video0", format="v4l2", options=options)
            relay = MediaRelay()
        return None, relay.subscribe(webcam.video)


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/cv", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index_cv.html", {"request": request})


@app.post("/offer")
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
    audio, video = create_local_tracks()

    await pc.setRemoteDescription(offer)
    for t in pc.getTransceivers():
        if t.kind == "audio" and audio:
            pc.addTrack(audio)
        elif t.kind == "video" and video:
            pc.addTrack(video)

    answer = await pc.createAnswer()
    await pc.setLocalDescription(answer)

    return {"sdp": pc.localDescription.sdp, "type": pc.localDescription.type}


@app.post("/offer_cv")
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
    # audio, video = create_local_tracks()

    @pc.on("track")
    def on_track(track):

        # if track.kind == "audio":
        #     pc.addTrack(player.audio)
        #     recorder.addTrack(track)
        if track.kind == "video":
            pc.addTrack(
                VideoTransformTrack(relay.subscribe(track), transform=params.video_transform)
            )
            # if args.record_to:
            #     recorder.addTrack(relay.subscribe(track))

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


pcs = set()
args = ''


@app.on_event("shutdown")
async def on_shutdown():
    # close peer connections
    coros = [pc.close() for pc in pcs]
    await asyncio.gather(*coros)
    pcs.clear()

# dshow @ 00000233ce069880] real-time buffer [USB2.0 PC CAMERA] [video input] too full or near too full (101% of size: 3041280 [rtbufsize parameter])! frame
#  dropped!