import os
from jose import jwt
from pydantic import BaseModel
from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from app.Service.Account.Prompt import getPrompt, updatePrompt

prompt = APIRouter(prefix='/api/account/prompt')


class promptParam(BaseModel):
    content: str


@prompt.get('/', tags=['prompt'])
async def index(request: Request):
    jwtData = jwt.decode(request.headers.get('Authorization'), os.getenv('JWT_SALT_KEY'), algorithms="HS256")
    result = getPrompt(jwtData.get('uuid'))
    if result != '':
        return JSONResponse({
            'result': 'success',
            'data': {
                'content': result
            }
        }, status_code=200)
    else:
        return JSONResponse({
            'result': 'fail'
        }, status_code=200)


@prompt.patch('/update', tags=['prompt'])
async def update(request: Request, promptParam: promptParam):
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
