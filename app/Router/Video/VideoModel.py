from typing import List
from pydantic import BaseModel


class RQ_setDetail(BaseModel):
    videoId: int
    title: str
    content: str
    tags: List[str]


class RQ_appendBgmToVideo(BaseModel):
    videoId: int
    bgmFileName: str
