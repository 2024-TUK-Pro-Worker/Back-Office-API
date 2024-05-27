# Python 모듈
from pydantic import BaseModel

# 소스 파일 선언


class RQ_postUploadToYoutube(BaseModel):
    videoId: int


class RQ_deleteYoutubeVideo(BaseModel):
    videoId: int