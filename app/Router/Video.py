import os
from jose import jwt
from pydantic import BaseModel
from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from app.Service.Video.Detail import getList, updateDetail

video = APIRouter(prefix='/api/video')


class RQ_setDetail(BaseModel):
    videoId: int
    title: str
    content: str
    tags: list


@video.get('/list', tags=['prompt'])
async def setDetail(request: Request):
    jwtData = jwt.decode(request.headers.get('Authorization'), os.getenv('JWT_SALT_KEY'), algorithms="HS256")

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


@video.put('/detail', tags=['prompt'])
async def setDetail(request: Request, rq_setDetail: RQ_setDetail):
    jwtData = jwt.decode(request.headers.get('Authorization'), os.getenv('JWT_SALT_KEY'), algorithms="HS256")

    result = updateDetail(jwtData.get('uuid'), rq_setDetail.videoId, rq_setDetail.title, rq_setDetail.content, rq_setDetail.tags)

    if result != '':
        return JSONResponse({
            'result': 'success'
        }, status_code=200)
    else:
        return JSONResponse({
            'result': 'fail'
        }, status_code=200)

