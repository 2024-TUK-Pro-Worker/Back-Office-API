import uvicorn
from fastapi import FastAPI, Response
from app.Router.Auth import google
from app.Router.Youtube import youtube
from app.Router.Prompt import prompt
from app.Router.Video import video
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# Router 추가
app.include_router(google)
app.include_router(youtube)
app.include_router(prompt)
app.include_router(video)


@app.get('/')
def index(response: Response):
    response.delete_cookie('authorizationToken')
    return {'msg': 'Main'}


@app.get('/test')
def test():
    return {'msg': 'Test'}


if __name__ == "__main__":
    uvicorn.run("run:app", host='0.0.0.0', port=8081, log_level="info", reload=True)
