import os
from jose import jwt
from typing import Optional, Union
from Router import Model as DefaultRoutingModel
from Router.Account import AccountDto as RoutingModel
from fastapi import APIRouter, Cookie, UploadFile, responses, Request, status
from Service.Account import Prompt as PromptService, Bgm as BgmService, Scheduler as SchedulerService

prompt = APIRouter(prefix='/api/account/prompt')
scheduler = APIRouter(prefix='/api/account/scheduler')
bgm = APIRouter(prefix='/api/account/bgm')


# 프롬프트
@prompt.get('', tags=['prompt'], response_model=Union[DefaultRoutingModel.RS_common, DefaultRoutingModel.RS_fail])
async def getPromptInfo(authorization: Optional[str] = Cookie(None)):
    try:
        jwtData = jwt.decode(authorization, os.getenv('JWT_SALT_KEY'), algorithms="HS256")

        result = PromptService.getPrompt(jwtData.get('uuid'))

        if result is None:
            raise Exception('prompt info call fail')

        return {
            'result': 'success',
            'data': result
        }
    except Exception as e:
        return {
            'result': 'fail',
            'message': e.__str__()
        }


@prompt.patch('/update', tags=['prompt'],
              response_model=Union[DefaultRoutingModel.RS_common, DefaultRoutingModel.RS_fail])
async def patchPromptInfo(params: RoutingModel.RQ_patchPromptInfo, authorization: Optional[str] = Cookie(None)):
    try:
        jwtData = jwt.decode(authorization, os.getenv('JWT_SALT_KEY'), algorithms="HS256")

        result = PromptService.updatePrompt(jwtData.get('uuid'), params.content)

        if not result:
            raise Exception('prompt info update fail')

        return {
            'result': 'success',
            'data': {
                'uuid': jwtData.get('uuid')
            }
        }
    except Exception as e:
        return {
            'result': 'fail',
            'message': e.__str__()
        }


# 스케줄러
@scheduler.get('/schedule', tags=['scheduler'],
               response_model=Union[DefaultRoutingModel.RS_common, DefaultRoutingModel.RS_fail])
async def getScheduleInfo(authorization: Optional[str] = Cookie(None)):
    try:
        jwtData = jwt.decode(authorization, os.getenv('JWT_SALT_KEY'), algorithms="HS256")

        result = SchedulerService.getJobScheduleInfo(jwtData.get('uuid'))

        if result is None:
            raise Exception('schedule info call fail')

        return {
            'result': 'success',
            'data': result
        }
    except Exception as e:
        return {
            'result': 'fail',
            'message': e.__str__()
        }


@scheduler.patch('/schedule/update', tags=['scheduler'],
                 response_model=Union[DefaultRoutingModel.RS_common, DefaultRoutingModel.RS_fail])
async def patchScheduleInfo(params: RoutingModel.RQ_patchScheduleInfo, authorization: Optional[str] = Cookie(None)):
    try:
        jwtData = jwt.decode(authorization, os.getenv('JWT_SALT_KEY'), algorithms="HS256")

        result = SchedulerService.setJobScheduleInfo(jwtData.get('uuid'), params.schedule)

        if not result:
            raise Exception('schedule info update fail')

        return {
            'result': 'success',
            'data': {
                'uuid': jwtData.get('uuid')
            }
        }
    except Exception as e:
        return {
            'result': 'fail',
            'message': e.__str__()
        }


@scheduler.get('/status', tags=['scheduler'], response_model=RoutingModel.RS_getSchedulerStatus)
async def getSchedulerStatus(authorization: Optional[str] = Cookie(None)):
    try:
        jwtData = jwt.decode(authorization, os.getenv('JWT_SALT_KEY'), algorithms="HS256")

        result = SchedulerService.getSchedulerStatus(jwtData.get('uuid'))

        if result is None:
            raise Exception('scheduler is None')

        return {
            'result': 'success',
            'message': None,
            'scheduleInfo': {
                'active': True,
                'last_schedule_time': str(result.last_schedule_time) if result.last_schedule_time is not None else None,
                'last_successful_time': str(
                    result.last_successful_time) if result.last_successful_time is not None else None
            }
        }
    except Exception as e:
        return {
            'result': 'fail',
            'message': e.__str__(),
            'scheduleInfo': {
                'active': False,
                'last_schedule_time': None,
                'last_successful_time': None
            }
        }


@scheduler.post('/create', tags=['scheduler'],
                response_model=Union[DefaultRoutingModel.RS_common, DefaultRoutingModel.RS_fail])
async def postSchedulerCreate(authorization: Optional[str] = Cookie(None)):
    try:
        jwtData = jwt.decode(authorization, os.getenv('JWT_SALT_KEY'), algorithms="HS256")

        result = SchedulerService.createScheduler(jwtData.get('uuid'))

        if not result or result['result'] is False:
            raise Exception(result['message'] if result['result'] is not None else 'schedule create fail')

        return {
            'result': 'success',
            'data': {
                'uuid': jwtData.get('uuid')
            }
        }
    except Exception as e:
        return {
            'result': 'fail',
            'message': e.__str__()
        }


@scheduler.delete('/delete', tags=['scheduler'],
                  response_model=Union[DefaultRoutingModel.RS_common, DefaultRoutingModel.RS_fail])
async def deleteScheduler(authorization: Optional[str] = Cookie(None)):
    try:
        jwtData = jwt.decode(authorization, os.getenv('JWT_SALT_KEY'), algorithms="HS256")

        result = SchedulerService.deleteScheduler(jwtData.get('uuid'))

        if not result['result']:
            raise Exception(result['message'])

        return {
            'result': 'success',
            'data': {
                'uuid': jwtData.get('uuid')
            }
        }
    except Exception as e:
        return {
            'result': 'fail',
            'message': e.__str__()
        }


@bgm.get('', tags=['bgm'], response_model=Union[DefaultRoutingModel.RS_common, DefaultRoutingModel.RS_fail])
async def getBgmList(authorization: Optional[str] = Cookie(None)):
    try:
        jwtData = jwt.decode(authorization, os.getenv('JWT_SALT_KEY'), algorithms="HS256")

        result = BgmService.getBgmList(jwtData.get('uuid'))

        if result is None:
            result = []

        return {
            'result': 'success',
            'data': {
                'bgmList': result
            }
        }
    except Exception as e:
        return {
            'result': 'fail',
            'message': e.__str__()
        }


@bgm.get("/preview/{bgmName}", tags=['bgm'])
async def bgmPreview(bgmName: str, request: Request, authorization: Optional[str] = Cookie(None)):
    try:
        jwtData = jwt.decode(authorization, os.getenv('JWT_SALT_KEY'), algorithms="HS256")

        rangeHeader = request.headers.get("range")

        result = BgmService.getPreviewInfo(jwtData.get('uuid'), bgmName, rangeHeader)

        if result['result'] is False:
            raise Exception(result['message'])

        headers = {
            'content-type': 'audio/mpeg',
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
            BgmService.getPreviewVideo(open(result['filePath'], mode="rb"), result['startPoint'], result['endPoint']),
            headers=headers,
            status_code=status_code,
        )
    except Exception as e:
        return {
            'result': 'fail',
            'message': e.__str__()
        }


@bgm.post('/insert', tags=['bgm'], response_model=Union[DefaultRoutingModel.RS_common, DefaultRoutingModel.RS_fail])
async def postUploadBgm(fileList: list[UploadFile], authorization: Optional[str] = Cookie(None)):
    try:
        jwtData = jwt.decode(authorization, os.getenv('JWT_SALT_KEY'), algorithms="HS256")

        result = BgmService.uploadBgmFile(jwtData.get('uuid'), fileList)

        return {
            'result': 'success',
            'data': {
                'uuid': jwtData.get('uuid'),
                'UploadList': result['uploadList']
            }
        }
    except Exception as e:
        return {
            'result': 'fail',
            'message': e.__str__()
        }


@bgm.delete('/remove', tags=['bgm'], response_model=Union[DefaultRoutingModel.RS_common, DefaultRoutingModel.RS_fail])
async def deleteBgmFile(params: RoutingModel.RQ_deleteBgmFile, authorization: Optional[str] = Cookie(None)):
    try:
        allowExtention = {'mp3'}

        if not ('.' in params.fileName and params.fileName.rsplit('.', 1)[1].lower() in allowExtention):
            raise Exception('not allow file extention')

        jwtData = jwt.decode(authorization, os.getenv('JWT_SALT_KEY'), algorithms="HS256")

        result = BgmService.deleteBgmFile(jwtData.get('uuid'), params.fileName)

        if not result['result']:
            raise Exception(result['message'])

        return {
            'result': 'success',
            'data': {
                'uuid': jwtData.get('uuid'),
                'fileName': params.fileName
            }
        }
    except Exception as e:
        return {
            'result': 'fail',
            'message': e.__str__()
        }
