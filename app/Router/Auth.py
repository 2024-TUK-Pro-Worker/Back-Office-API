from fastapi import APIRouter
from fastapi.responses import JSONResponse
from ..Service.Google.OAuth import *

auth = APIRouter(prefix='/auth')
google = APIRouter(prefix='/auth/google')


@google.get('/login', tags=['auth'])
async def getUrl():
    return getOAuthUrl()


@google.get('/callback', tags=['auth'])
async def callback(code: str):
    jwtToken = authGoogle(code)
    response = RedirectResponse('/')
    response.set_cookie(key="authorizationToken", value=jwtToken)
    return response


@auth.get('/token', tags=['auth'])
async def getToken(token: str):
    return JSONResponse(content=checkToken(token))
