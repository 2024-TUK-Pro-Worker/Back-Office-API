# Python 모듈
import os
from jose import jwt
from typing import Union, Optional
from fastapi import APIRouter, Cookie

# 소스 파일 선언
from Router import Model as DefaultRoutingModel
from Router.Youtube import YoutubeDto as RoutingModel
from Service.ThirdParty.Youtube import Youtube as YoutubeService

youtube = APIRouter(prefix='/api/youtube')


@youtube.post('/upload', tags=['youtube'],
              response_model=Union[DefaultRoutingModel.RS_common, DefaultRoutingModel.RS_fail])
async def postUploadToYoutube(params: RoutingModel.RQ_postUploadToYoutube, authorization: Optional[str] = Cookie(None)):
    try:
        params = params.dict()

        jwtData = jwt.decode(authorization, os.getenv('JWT_SALT_KEY'), algorithms="HS256")

        result = YoutubeService(jwtData).uploadVideo(jwtData.get('uuid'), params['videoId'])

        if result['result'] is False:
            raise Exception(result['message'])

        return {
            'result': 'success',
            'data': {
                'uuid': jwtData.get('uuid'),
                'videoId': params['videoId']
            }
        }
    except Exception as e:
        return {
            'result': 'fail',
            'message': e.__str__()
        }


@youtube.delete('/delete', tags=['youtube'],
                response_model=Union[DefaultRoutingModel.RS_common, DefaultRoutingModel.RS_fail])
async def deleteYoutubeVideo(params: RoutingModel.RQ_deleteYoutubeVideo, authorization: Optional[str] = Cookie(None)):
    try:
        params = params.dict()

        jwtData = jwt.decode(authorization, os.getenv('JWT_SALT_KEY'), algorithms="HS256")

        result = YoutubeService(jwtData).delVideo(jwtData.get('uuid'), params['videoId'])

        if result['result'] is False:
            raise Exception(result['message'])

        return {
            'result': 'success',
            'data': {
                'uuid': jwtData.get('uuid'),
                'videoId': params['videoId']
            }
        }
    except Exception as e:
        return {
            'result': 'fail',
            'message': e.__str__()
        }
