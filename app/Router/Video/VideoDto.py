from typing import List, Union
from pydantic import BaseModel


class RQ_setDetail(BaseModel):
    videoId: int
    title: str
    content: str
    tags: Union[List[str], None]


class RQ_appendBgmToVideo(BaseModel):
    videoId: int
    bgmFileName: str
