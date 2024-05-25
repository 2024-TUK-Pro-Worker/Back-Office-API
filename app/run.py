import os
import time
import uvicorn
from jose import jwt
from dotenv import load_dotenv
from Router.Auth.AuthRouter import google, account
from Router.Video.VideoRouter import video
from Router.Youtube.YoutubeRouter import youtube
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Cookie, Request, responses
from Router.Account.AccountRouter import prompt, scheduler, bgm

load_dotenv()

app = FastAPI()

# Router 추가
app.include_router(google)
app.include_router(account)
app.include_router(youtube)
app.include_router(prompt)
app.include_router(scheduler)
app.include_router(video)
app.include_router(bgm)

origins = [
    "https://api-aishortmaker.lacy.co.kr",
    "https://aishortsmaker.lacy.co.kr",
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:8081"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    try:
        if '/auth/' not in request.url.path:
            if request.cookies.get('authorization') is None and request.method != 'OPTIONS':
                return responses.JSONResponse({
                    'result': 'fail',
                    'message': '403 Forbidden'
                }, status_code=403)

            # JWT 정상 변경 가능 여부 확인
            jwtToken = request.cookies.get('authorization')
            jwt.decode(jwtToken, os.getenv('JWT_SALT_KEY'), algorithms="HS256")

        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time
        response.headers["X-Process-Time"] = str(process_time)
        return response
    except jwt.ExpiredSignatureError:
        return responses.JSONResponse({
            'result': 'fail',
            'message': 'Signature has expired. '
        }, status_code=401)
    except Exception as e:
        return responses.JSONResponse({
            'result': 'fail',
            'message': 'internal server error'
        }, status_code=500)


if __name__ == "__main__":
    uvicorn.run("run:app", host='0.0.0.0', port=int(os.getenv('SERVER_PORT')), log_level="info", reload=True)
