import os
from fastapi import APIRouter, status
from fastapi.responses import RedirectResponse
from Service.Auth.GoogleOAuth import *

google = APIRouter(prefix='/auth/google')


@google.get('/login', tags=['auth'])
async def getUrl():
    return getOAuthUrl()


@google.get('/callback', tags=['auth'], response_class=RedirectResponse)
async def callback(code: str) -> RedirectResponse:
    jwtToken = authGoogle(code)
    response = RedirectResponse(url=f"{os.getenv('FRONT_HOST')}/", status_code="302")
    response.set_cookie(key="authorization", value=jwtToken, domain=f"{os.getenv('FRONT_HOST')}/")
    return response