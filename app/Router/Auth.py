from fastapi import APIRouter
from app.Service.Auth.GoogleOAuth import *

google = APIRouter(prefix='/auth/google')


@google.get('/login', tags=['auth'])
async def getUrl():
    return getOAuthUrl()


@google.get('/callback', tags=['auth'])
async def callback(code: str):
    jwtToken = authGoogle(code)
    response = RedirectResponse('/')
    response.set_cookie(key="authorization", value=jwtToken)
    return response