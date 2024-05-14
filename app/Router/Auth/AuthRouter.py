import os
from fastapi import APIRouter
from fastapi.responses import RedirectResponse
from Service.Auth.GoogleOAuth import *

google = APIRouter(prefix='/auth/google')


@google.get('/login', tags=['auth'])
async def getUrl():
    return getOAuthUrl()


@google.get('/callback', tags=['auth'], response_class=RedirectResponse)
async def callback(code: str):
    jwtToken = authGoogle(code)
    response = RedirectResponse(url=f"{os.getenv('FRONT_HOST')}/")
    response.set_cookie(key="authorization", value=jwtToken, domain=f"{os.getenv('FRONT_HOST')}")
    response.set_cookie(key="authorization", value=jwtToken, domain=f"{os.getenv('API_HOST')}")
    return response