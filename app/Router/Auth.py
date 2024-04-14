from fastapi import APIRouter
from app.Service.Auth.GoogleOAuth import *

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