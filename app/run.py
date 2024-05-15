import os
import time
import uvicorn
from typing import Optional
from dotenv import load_dotenv
from Router.Auth.AuthRouter import google
from Router.Video.VideoRouter import video
from Router.Youtube.YoutubeRouter import youtube
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Cookie, Request, responses
from Router.Account.AccountRouter import prompt, scheduler, bgm

load_dotenv()

app = FastAPI()

# Router 추가
app.include_router(google)
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
    allow_headers=["*"],
)

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    if '/auth/' not in request.url.path and request.cookies.get('authorization') is None:
        return responses.JSONResponse({
            'result': 'fail',
            'message': '403 Forbidden'
        }, status_code=403)

    refererDomain = None
    referer = request.headers.get('referer')
    if referer is not None:
        refererDomain = referer.split('/')[2] if referer.split('/')[2] is not None else None
        refererDomain = f"http://{refererDomain}" if 'localhost' in refererDomain else f"https://{refererDomain}"

    if refererDomain is None or refererDomain not in origins:
        return responses.JSONResponse({
            'result': 'fail',
            'message': '404 NotFound'
        }, status_code=404)

    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


if __name__ == "__main__":
    uvicorn.run("run:app", host='0.0.0.0', port=int(os.getenv('SERVER_PORT')), log_level="info", reload=True)
