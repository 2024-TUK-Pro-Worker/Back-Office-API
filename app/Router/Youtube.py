import os
from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from jose import jwt
from app.Service.ThirdParty.Youtube import Youtube as YoutubeService
from pydantic import BaseModel

youtube = APIRouter(prefix='/youtube')


class VideoActionParam(BaseModel):
    videoId: int


@youtube.put('/upload', tags=['youtube'])
async def upload(request: Request, videoActionParam: VideoActionParam):
    params = videoActionParam.dict()
    jwtData = jwt.decode(request.headers.get('Authorization'), os.getenv('JWT_SALT_KEY'), algorithms="HS256")

    result = YoutubeService(jwtData).uploadVideo(jwtData.get('uuid'), params['videoId'])

    if result:
        return JSONResponse({
            'result': 'success'
        }, status_code=200)
    else:
        return JSONResponse({
            'result': 'fail'
        }, status_code=200)


@youtube.delete('/delete', tags=['youtube'])
async def delete(request: Request, videoActionParam: VideoActionParam):
    params = videoActionParam.dict()
    jwtData = jwt.decode(request.headers.get('Authorization'), os.getenv('JWT_SALT_KEY'), algorithms="HS256")
    result = YoutubeService(jwtData).delVideo(jwtData.get('uuid'), params['videoId'])

    if result:
        return JSONResponse({
            'result': 'success'
        }, status_code=200)
    else:
        return JSONResponse({
            'result': 'fail'
        }, status_code=200)
