import os
from fastapi import APIRouter
from Service.Auth.GoogleOAuth import *

google = APIRouter(prefix='/auth/google')


@google.get('/login', tags=['auth'])
async def getUrl():
    return getOAuthUrl()


@google.get('/callback', tags=['auth'])
async def callback(code: str):
    jwtToken = authGoogle(code)
    response = RedirectResponse(f"https://{os.getenv('FRONT_HOST')}/")
    response.set_cookie(key="authorization", value=jwtToken, path="/", domain=f"{os.getenv('FRONT_HOST')}", secure=False, httponly=False)
    return response