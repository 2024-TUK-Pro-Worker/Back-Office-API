from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse
from app.Router.Auth import google
from app.Router.Youtube import youtube
from dotenv import load_dotenv
import uvicorn
import os
from jose import jwt
from datetime import datetime

load_dotenv()

app = FastAPI()

app.include_router(google)
app.include_router(youtube)


@app.middleware("http")
async def check_jwt(request: Request, call_next):
    locationUrl = request.url.path
    jwtToken = request.headers.get('Authorization')

    exceptUrl = (
        '/auth/google'
    )

    for target in exceptUrl:
        if target in locationUrl or locationUrl == '/':
            response = await call_next(request)
            return response

    if jwtToken is None:
        return JSONResponse({
            'result': 'fail',
            'message': '403 forbidden'
        }, status_code=403)

    jwtInfo = jwt.decode(jwtToken, os.getenv('JWT_SALT_KEY'), algorithms="HS256")

    if datetime.fromtimestamp(jwtInfo.get('exp')) < datetime.now():
        return JSONResponse({
            'result': 'fail',
            'message': '403 forbidden'
        }, status_code=403)

    return await call_next(request)


@app.get('/')
def index(response: Response):
    response.delete_cookie('authorizationToken')
    return {'msg': 'Main'}


@app.get('/test')
def test():
    return {'msg': 'Test'}


if __name__ == "__main__":
    uvicorn.run("run:app", host='0.0.0.0', port=8081, log_level="info", reload=True)
