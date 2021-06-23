from pydantic import BaseModel


class Offer(BaseModel):
    sdp: str
    type: str
    play_from: str = None
    video_transform: str = None

