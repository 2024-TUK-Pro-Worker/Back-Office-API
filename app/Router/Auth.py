from fastapi import APIRouter
from ..Service.Google.OAuth import *

auth = APIRouter(prefix='/auth/google')

@auth.get('/login', tags=['auth'])
async def getUrl():
    return getOAuthUrl()

@auth.get('/callback', tags=['auth'])
async def callback(code: str):
    return authGoogle(code)

@auth.get('/token', tags=['auth'])
async def getToken(token: str = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1dWlkIjoiMTEwMjMwNTk0OTc5MzY2MDc3NzgyIiwibmFtZSI6Ilx1YzgxNVx1YjJlNFx1YzZiNCIsImVtYWlsIjoid2pkZWtkbnMxMDIzQGdtYWlsLmNvbSIsImV4cCI6MTcxMzA1NTQxNn0.pFmIm-GIwy_TpJSWAkdShmswlFT5e664isedOBFB3aw'):
    return checkToken(token)