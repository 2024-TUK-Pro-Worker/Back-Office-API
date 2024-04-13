from datetime import *
from fastapi import FastAPI
import requests
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from app.Model.Auth.User import User as userModel
from app.Model.Auth.Login import Login as loginModel

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Replace these with your own values from the Google Developer Console
GOOGLE_CLIENT_ID = "153370030601-njfl54m574dsvuja9qdrgn58idaaco40.apps.googleusercontent.com"
GOOGLE_CLIENT_SECRET = "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"
GOOGLE_REDIRECT_URI = "http://localhost:8081/auth/google/callback"


def getOAuthUrl():
    return {
        "url": f"https://accounts.google.com/o/oauth2/auth?response_type=code&client_id={GOOGLE_CLIENT_ID}&redirect_uri={GOOGLE_REDIRECT_URI}&scope=openid%20profile%20email%20https://www.googleapis.com/auth/youtube.upload&access_type=offline"
    }


def authGoogle(code: str):
    token_url = "https://accounts.google.com/o/oauth2/token"
    data = {
        "code": code,
        "client_id": GOOGLE_CLIENT_ID,
        "client_secret": GOOGLE_CLIENT_SECRET,
        "redirect_uri": GOOGLE_REDIRECT_URI,
        "grant_type": "authorization_code",
    }
    response = requests.post(token_url, data=data)

    accessToken = response.json().get("access_token")
    refreshToken = response.json().get("refresh_token")

    user_info = requests.get("https://www.googleapis.com/oauth2/v1/userinfo",
                             headers={"Authorization": f"Bearer {accessToken}"})

    uuid = user_info.json().get("id")
    email = user_info.json().get("email")
    userName = user_info.json().get("name")
    currentDt = datetime.now()
    expireAt = currentDt + timedelta(seconds=response.json().get('expires_in'))

    userM = userModel()
    loginM = loginModel()

    userInfo = userM.getUser(uuid)

    if userInfo == None:
        userM.insertUser('1', uuid, email, userName)
    elif userInfo[3] != email and userInfo[4] != userName:
        userM.updateUser('1', uuid, email, userName)

    loginM.updateAuth(uuid, '1', accessToken, refreshToken, expireAt)

    del userM
    del loginM

    data = {
        "uuid": uuid,
        "name": userName,
        "email": email,
        "exp": expireAt
    }
    jwtToken = jwt.encode(data, 'test', algorithm="HS256")

    return {
        "jwtToken": jwtToken,
        "token_type": "bearer"
    }


def checkToken(token):
    userM = userModel()
    loginM = loginModel()

    jwtInfo = jwt.decode(token, 'test', algorithms="HS256")

    diffTime = datetime.now() - timedelta(minutes=5)

    if userM.getUser(jwtInfo.get('uuid')) is None:
        return {
            'result': 'fail'
        }

    if datetime.fromtimestamp(jwtInfo.get('exp')) >= diffTime:
        return {
            'result': 'success',
            'status': 'alive',
            "jwtToken": token,
            "token_type": "bearer"
        }

    tokenInfo = loginM.getTokens(jwtInfo.get('uuid'))
    beforeRefreshToken = tokenInfo[1]

    token_url = "https://accounts.google.com/o/oauth2/token"
    data = {
        "client_id": GOOGLE_CLIENT_ID,
        "client_secret": GOOGLE_CLIENT_SECRET,
        "refresh_token": beforeRefreshToken,
        "grant_type": "refresh_token",
    }
    response = requests.post(token_url, data=data)

    newAccessToken = response.json().get("access_token")
    currentDt = datetime.now()
    expireAt = currentDt + timedelta(seconds=response.json().get('expires_in'))

    loginM.updateAccessToken(jwtInfo.get('uuid'), '1', newAccessToken, expireAt)

    del loginM

    data = {
        "uuid": jwtInfo.get('uuid'),
        "name": jwtInfo.get('name'),
        "email": jwtInfo.get('email'),
        "exp": expireAt
    }
    newJwtToken = jwt.encode(data, 'test', algorithm="HS256")

    return {
        'result': 'success',
        'status': 'refresh',
        "jwtToken": newJwtToken,
        "token_type": "bearer"
    }