import os
from typing import Optional
from jose import jwt
from pydantic import BaseModel
from fastapi import APIRouter, Cookie
from fastapi.responses import JSONResponse
from Service.Video.Detail import getList, updateDetail, getDetail, insertIntoVideo

video = APIRouter(prefix='/api/video')


class RQ_setDetail(BaseModel):
    videoId: int
    title: str
    content: str
    tags: list


class RQ_appendBgmToVideo(BaseModel):
    videoId: int
    bgmFileName: str


@video.get('/list', tags=['prompt'])
async def getVideoList(authorization: Optional[str] = Cookie(None)):
    jwtData = jwt.decode(authorization, os.getenv('JWT_SALT_KEY'), algorithms="HS256")

    result = getList(jwtData.get('uuid'))

    if result is not None:
        return JSONResponse({
            'result': 'success',
            'data': result
        }, status_code=200)
    else:
        return JSONResponse({
            'result': 'fail'
        }, status_code=200)


@video.get('/detail/{videoId}', tags=['prompt'])
async def getVideoDetail(videoId: int, authorization: Optional[str] = Cookie(None)):
    jwtData = jwt.decode(authorization, os.getenv('JWT_SALT_KEY'), algorithms="HS256")

    result = getDetail(jwtData.get('uuid'), videoId)

    if result is not None:
        return JSONResponse({
            'result': 'success',
            'data': result
        }, status_code=200)
    else:
        return JSONResponse({
            'result': 'fail'
        }, status_code=200)


@video.put('/detail', tags=['prompt'])
async def setDetail(rq_setDetail: RQ_setDetail, authorization: Optional[str] = Cookie(None)):
    jwtData = jwt.decode(authorization, os.getenv('JWT_SALT_KEY'), algorithms="HS256")

    result = updateDetail(jwtData.get('uuid'), rq_setDetail.videoId, rq_setDetail.title, rq_setDetail.content,
                          rq_setDetail.tags)

    if result != '':
        return JSONResponse({
            'result': 'success'
        }, status_code=200)
    else:
        return JSONResponse({
            'result': 'fail'
        }, status_code=200)


@video.patch('/bgm/set', tags=['prompt'])
async def setBgmToVideo(rq_appendBgmToVideo: RQ_appendBgmToVideo, authorization: Optional[str] = Cookie(None)):
    jwtData = jwt.decode(authorization, os.getenv('JWT_SALT_KEY'), algorithms="HS256")

    result = insertIntoVideo(jwtData.get('uuid'), rq_appendBgmToVideo.videoId, rq_appendBgmToVideo.bgmFileName)

    if result:
        return JSONResponse({
            'result': 'success'
        }, status_code=200)
    else:
        return JSONResponse({
            'result': 'fail'
        }, status_code=200)
