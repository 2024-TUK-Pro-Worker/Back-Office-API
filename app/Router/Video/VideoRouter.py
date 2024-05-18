import os
from jose import jwt
from typing import Optional, Union
from Router import Model as DefaultRoutingModel
from Service.Video import Detail as DetailService
from Router.Video import VideoDto as RoutingModel
from fastapi import APIRouter, Cookie, responses, Request, status

video = APIRouter(prefix='/api/video')


@video.get('/list', tags=['video'], response_model=Union[DefaultRoutingModel.RS_common, DefaultRoutingModel.RS_fail])
async def getVideoList(authorization: Optional[str] = Cookie(None)):
    try:
        jwtData = jwt.decode(authorization, os.getenv('JWT_SALT_KEY'), algorithms="HS256")

        result = DetailService.getList(jwtData.get('uuid'))

        if result is None:
            raise Exception('video list is None')

        return {
            'result': 'success',
            'data': result
        }
    except Exception as e:
        return {
            'result': 'fail',
            'message': e.__str__()
        }


@video.get('/detail/{videoId}', tags=['video'],
           response_model=Union[DefaultRoutingModel.RS_common, DefaultRoutingModel.RS_fail])
async def getVideoDetail(videoId: int, authorization: Optional[str] = Cookie(None)):
    try:
        jwtData = jwt.decode(authorization, os.getenv('JWT_SALT_KEY'), algorithms="HS256")

        result = DetailService.getDetail(jwtData.get('uuid'), videoId)

        if result is None:
            raise Exception('video info is None')

        return {
            'result': 'success',
            'data': result
        }
    except Exception as e:
        return {
            'result': 'fail',
            'message': e.__str__()
        }


@video.get("/preview/{videoId}", tags=['video'])
async def video_endpoint(videoId: int, request: Request, authorization: Optional[str] = Cookie(None)):
    try:
        jwtData = jwt.decode(authorization, os.getenv('JWT_SALT_KEY'), algorithms="HS256")

        rangeHeader = request.headers.get("range")

        result = DetailService.getPreviewInfo(jwtData.get('uuid'), videoId, rangeHeader)

        if result['result'] is False:
            raise Exception(result['message'])

        headers = {
            'content-type': 'video/mp4',
            'accept-ranges': 'bytes',
            'content-encoding': 'identity',
            'content-length': str(result['fileSize']),
            'access-control-expose-headers': (
                'content-type, accept-ranges, content-length, '
                'content-range, content-encoding'
            ),
        }
        if rangeHeader is None:
            result['startPoint'] = 0
            result['endPoint'] = result['fileSize'] - 1
            status_code = status.HTTP_200_OK
        else:
            size = result['endPoint'] - result['startPoint'] + 1
            headers["content-length"] = str(size)
            headers["content-range"] = f"bytes {result['startPoint']}-{result['endPoint']}/{result['fileSize']}"
            status_code = status.HTTP_206_PARTIAL_CONTENT

        return responses.StreamingResponse(
            DetailService.getPreviewVideo(open(result['filePath'], mode="rb"), result['startPoint'], result['endPoint']),
            headers=headers,
            status_code=status_code,
        )
    except Exception as e:
        return {
            'result': 'fail',
            'message': e.__str__()
        }


@video.put('/detail', tags=['video'], response_model=Union[DefaultRoutingModel.RS_common, DefaultRoutingModel.RS_fail])
async def putVideoDetail(params: RoutingModel.RQ_setDetail, authorization: Optional[str] = Cookie(None)):
    try:
        jwtData = jwt.decode(authorization, os.getenv('JWT_SALT_KEY'), algorithms="HS256")

        print(params)

        result = DetailService.updateDetail(
            jwtData.get('uuid'), params.videoId, params.title,
            params.content, params.tags
        )

        if result is False:
            raise Exception('video info is None')

        return {
            'result': 'success',
            'data': {
                'uuid': jwtData.get('uuid'),
                'videoId': params.videoId
            }
        }
    except Exception as e:
        return {
            'result': 'fail',
            'message': e.__str__()
        }


@video.patch('/bgm/set', tags=['video'],
             response_model=Union[DefaultRoutingModel.RS_common, DefaultRoutingModel.RS_fail])
async def patchBgmToVideo(params: RoutingModel.RQ_appendBgmToVideo, authorization: Optional[str] = Cookie(None)):
    try:
        jwtData = jwt.decode(authorization, os.getenv('JWT_SALT_KEY'), algorithms="HS256")

        result = DetailService.insertIntoVideo(
            jwtData.get('uuid'), params.videoId, params.bgmFileName
        )

        if result['result'] is False:
            raise Exception(result['message'])

        return {
            'result': 'success',
            'data': {
                'uuid': jwtData.get('uuid'),
                'videoId': params.videoId
            }
        }
    except Exception as e:
        return {
            'result': 'fail',
            'message': e.__str__()
        }
