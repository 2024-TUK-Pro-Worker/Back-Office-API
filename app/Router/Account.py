import os
from jose import jwt
from pydantic import BaseModel
from fastapi import APIRouter, Request, UploadFile
from fastapi.responses import JSONResponse
from app.Service.Account.Prompt import getPrompt, updatePrompt
from app.Service.Account.Bgm import getBgmList, uploadBgmFile, deleteBgmFile
from app.Service.Account.Scheduler import getJobScheduleInfo, setJobScheduleInfo, getSchedulerStatus, createScheduler, \
    deleteScheduler

prompt = APIRouter(prefix='/api/account/prompt')
scheduler = APIRouter(prefix='/api/account/scheduler')
bgm = APIRouter(prefix='/api/account/bgm')


class promptParam(BaseModel):
    content: str


class scheduleUpdateParam(BaseModel):
    schedule: str


class bgmDeleteParam(BaseModel):
    fileName: str


# 프롬프트
@prompt.get('/', tags=['prompt'])
async def promptGet(request: Request):
    jwtData = jwt.decode(request.headers.get('Authorization'), os.getenv('JWT_SALT_KEY'), algorithms="HS256")
    result = getPrompt(jwtData.get('uuid'))
    if result != '':
        return JSONResponse({
            'result': 'success',
            'data': {
                'content': result['content']
            }
        }, status_code=200)
    else:
        return JSONResponse({
            'result': 'fail'
        }, status_code=200)


@prompt.patch('/update', tags=['prompt'])
async def promptUpdate(request: Request, promptParam: promptParam):
    jwtData = jwt.decode(request.headers.get('Authorization'), os.getenv('JWT_SALT_KEY'), algorithms="HS256")
    result = updatePrompt(jwtData.get('uuid'), promptParam.content)
    if result:
        return JSONResponse({
            'result': 'success'
        }, status_code=200)
    else:
        return JSONResponse({
            'result': 'fail'
        }, status_code=200)


# 스케줄러
@scheduler.get('/schedule', tags=['scheduler'])
async def scheduleInfo(request: Request):
    jwtData = jwt.decode(request.headers.get('Authorization'), os.getenv('JWT_SALT_KEY'), algorithms="HS256")
    result = getJobScheduleInfo(jwtData.get('uuid'))

    return JSONResponse({
        'result': 'success',
        'data': {
            'schedule': result['cron_schedule']
        }
    }, status_code=200)


@scheduler.patch('/schedule/update', tags=['scheduler'])
async def scheduleUpdate(request: Request, scheduleUpdateParam: scheduleUpdateParam):
    jwtData = jwt.decode(request.headers.get('Authorization'), os.getenv('JWT_SALT_KEY'), algorithms="HS256")
    result = setJobScheduleInfo(jwtData.get('uuid'), scheduleUpdateParam.schedule)

    if result:
        return JSONResponse({
            'result': 'success'
        }, status_code=200)
    else:
        return JSONResponse({
            'result': 'fail'
        }, status_code=200)


@scheduler.get('/status', tags=['scheduler'])
async def schedulerStatus(request: Request):
    jwtData = jwt.decode(request.headers.get('Authorization'), os.getenv('JWT_SALT_KEY'), algorithms="HS256")
    try:
        result = getSchedulerStatus(jwtData.get('uuid'))

        if result is None:
            raise ('Scheduler is Null')

        return JSONResponse({
            'result': 'success',
            'scheduleInfo': {
                'active': True,
                'last_schedule_time': str(result.last_schedule_time) if result.last_schedule_time is not None else None,
                'last_successful_time': str(
                    result.last_successful_time) if result.last_successful_time is not None else None
            }
        }, status_code=200)
    except:
        return JSONResponse({
            'result': 'fail',
            'scheduleInfo': {
                'active': False,
                'last_schedule_time': None,
                'last_successful_time': None
            }
        }, status_code=200)


@scheduler.post('/create', tags=['scheduler'])
async def schedulerCreate(request: Request):
    jwtData = jwt.decode(request.headers.get('Authorization'), os.getenv('JWT_SALT_KEY'), algorithms="HS256")
    result = createScheduler(jwtData.get('uuid'))

    if result:
        return JSONResponse({
            'result': 'success'
        }, status_code=200)
    else:
        return JSONResponse({
            'result': 'fail'
        }, status_code=200)


@scheduler.delete('/delete', tags=['scheduler'])
async def schedulerCreate(request: Request):
    jwtData = jwt.decode(request.headers.get('Authorization'), os.getenv('JWT_SALT_KEY'), algorithms="HS256")
    result = deleteScheduler(jwtData.get('uuid'))

    if result:
        return JSONResponse({
            'result': 'success'
        }, status_code=200)
    else:
        return JSONResponse({
            'result': 'fail'
        }, status_code=200)


@bgm.get('/', tags=['bgm'])
async def getBgm(request: Request):
    jwtData = jwt.decode(request.headers.get('Authorization'), os.getenv('JWT_SALT_KEY'), algorithms="HS256")
    result = getBgmList(jwtData.get('uuid'))

    if result:
        return JSONResponse({
            'result': 'success',
            'data': {
                'bgmList': result
            }
        }, status_code=200)
    else:
        return JSONResponse({
            'result': 'fail'
        }, status_code=200)


@bgm.post('/insert', tags=['bgm'])
async def uploadBgm(request: Request, file: UploadFile):
    jwtData = jwt.decode(request.headers.get('Authorization'), os.getenv('JWT_SALT_KEY'), algorithms="HS256")

    bgmFileName = file.filename
    bgmFile = await file.read()

    result = uploadBgmFile(jwtData.get('uuid'), bgmFileName, bgmFile)

    if result:
        return JSONResponse({
            'result': 'success',
            'data': {
                'fileName': bgmFileName
            }
        }, status_code=200)
    else:
        return JSONResponse({
            'result': 'fail'
        }, status_code=200)


@bgm.delete('/remove', tags=['bgm'])
async def uploadBgm(request: Request, bgmDeleteParam: bgmDeleteParam):
    try :
        allowExtention = {'mp3'}
        if not ('.' in bgmDeleteParam.fileName and bgmDeleteParam.fileName.rsplit('.', 1)[1].lower() in allowExtention):
            raise '확장자가 일치 하지 않음'

        jwtData = jwt.decode(request.headers.get('Authorization'), os.getenv('JWT_SALT_KEY'), algorithms="HS256")
        result = deleteBgmFile(jwtData.get('uuid'), bgmDeleteParam.fileName)

        if not result:
            raise '결과가 올바르지 않음'

        return JSONResponse({
            'result': 'success'
        }, status_code=200)
    except:
        return JSONResponse({
            'result': 'fail'
        }, status_code=200)
