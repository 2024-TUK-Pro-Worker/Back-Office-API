from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse
from app.Router.Auth import auth, google
import uvicorn

app = FastAPI()

app.include_router(auth)
app.include_router(google)


@app.middleware("http")
async def check_jwt(request: Request, call_next):
    authExcept = False
    locationUrl = request.url.path
    authToken = request.headers.get('Authorization')

    exceptUrl = (
        '/',  # 테스트 index
        '/auth/google',
    )
    for target in exceptUrl:
        if target in locationUrl:
            authExcept = True

    if not authExcept and authToken is None:
        return JSONResponse({
            'result': 'fail',
            'message': '403 forbidden'
        }, status_code=403)

    response = await call_next(request)
    return response


@app.get('/')
def index(response: Response):
    response.delete_cookie('authorizationToken')
    return {'msg': 'Main'}


@app.get('/test')
def test():
    return {'msg': 'Test'}


if __name__ == "__main__":
    uvicorn.run("run:app", host='0.0.0.0', port=8081, log_level="info", reload=True)
