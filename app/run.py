from fastapi import FastAPI
from app.Router.Auth import auth
import uvicorn

app = FastAPI()

# Sample Router
app.include_router(auth)

@app.get('/')
def home():
    return {'msg' : 'Main'}

if __name__ == "__main__":
    uvicorn.run("run:app", host='0.0.0.0', port=8081, log_level="info", reload=True)