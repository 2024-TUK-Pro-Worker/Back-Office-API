import os
import uvicorn
from typing import Optional
from fastapi import FastAPI, Cookie
from Router.Auth.AuthRouter import google
from Router.Youtube.YoutubeRouter import youtube
from Router.Account.AccountRouter import prompt, scheduler, bgm
from Router.Video.VideoRouter import video
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# Router 추가
app.include_router(google)
app.include_router(youtube)
app.include_router(prompt)
app.include_router(scheduler)
app.include_router(video)
app.include_router(bgm)


@app.get('/')
def index(authorization: Optional[str] = Cookie(None)):
    return {'JWT': authorization}


if __name__ == "__main__":
    uvicorn.run("run:app", host='0.0.0.0', port=int(os.getenv('SERVER_PORT')), log_level="info", reload=True)
