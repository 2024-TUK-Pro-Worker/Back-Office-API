import os
from fastapi import APIRouter, Request
from jose import jwt
from app.Service.ThirdParty.Youtube import Youtube as YoutubeService

youtube = APIRouter(prefix='/youtube')


@youtube.put('/upload', tags=['youtube'])
async def upload(request: Request):
    jwtData = jwt.decode(request.headers.get('Authorization'), os.getenv('JWT_SALT_KEY'), algorithms="HS256")
    return YoutubeService(jwtData).uploadVideo()