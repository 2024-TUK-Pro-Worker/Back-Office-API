# Python 모듈
from typing import Union
from pydantic import BaseModel

# 소스 파일 선언


class RQ_patchPromptInfo(BaseModel):
    content: str


class RQ_patchScheduleInfo(BaseModel):
    schedule: str


class RQ_deleteBgmFile(BaseModel):
    fileName: str


class RS_getSchedulerStatus(BaseModel):
    result: str
    message: Union[str, None]
    scheduleInfo: Union[dict]
