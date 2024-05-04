from pydantic import BaseModel


class RQ_postUploadToYoutube(BaseModel):
    videoId: int


class RQ_deleteYoutubeVideo(BaseModel):
    videoId: int