import requests
from fastapi.responses import RedirectResponse
from jose import jwt
from datetime import *
from app.Model.Auth.User import User as userModel
from app.Model.Auth.Login import Login as loginModel

# Replace these with your own values from the Google Developer Console
GOOGLE_CLIENT_ID = "153370030601-njfl54m574dsvuja9qdrgn58idaaco40.apps.googleusercontent.com"
GOOGLE_CLIENT_SECRET = "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"
GOOGLE_REDIRECT_URI = "http://localhost:8081/auth/google/callback"

USER_MODEL = userModel()
LOGIN_MODEL = loginModel()

def getOAuthUrl():
    return RedirectResponse(
        f"https://accounts.google.com/o/oauth2/auth?response_type=code&client_id={GOOGLE_CLIENT_ID}&redirect_uri={GOOGLE_REDIRECT_URI}&scope=openid%20profile%20email%20https://www.googleapis.com/auth/youtube.upload&access_type=offline")


def authGoogle(code: str):
    token_url = "https://accounts.google.com/o/oauth2/token"
    data = {
        "code": code,
        "client_id": GOOGLE_CLIENT_ID,
        "client_secret": GOOGLE_CLIENT_SECRET,
        "redirect_uri": GOOGLE_REDIRECT_URI,
        "grant_type": "authorization_code",
    }
    googleToken = requests.post(token_url, data=data)

    accessToken = googleToken.json().get("access_token")
    refreshToken = googleToken.json().get("refresh_token")

    user_info = requests.get("https://www.googleapis.com/oauth2/v1/userinfo",
                             headers={"Authorization": f"Bearer {accessToken}"})

    uuid = user_info.json().get("id")
    email = user_info.json().get("email")
    userName = user_info.json().get("name")
    currentDt = datetime.now()
    expireAt = currentDt + timedelta(seconds=googleToken.json().get('expires_in'))

    userInfo = USER_MODEL.getUser(uuid)

    if userInfo == None:
        USER_MODEL.insertUser('1', uuid, email, userName)
    elif userInfo[3] != email and userInfo[4] != userName:
        USER_MODEL.updateUser('1', uuid, email, userName)

    LOGIN_MODEL.updateAuth(uuid, '1', accessToken, refreshToken, expireAt)

    data = {
        "uuid": uuid,
        "name": userName,
        "email": email,
        "exp": expireAt
    }

    return jwt.encode(data, 'test', algorithm="HS256")


def checkToken(token):
    jwtInfo = jwt.decode(token, 'test', algorithms="HS256")

    diffTime = datetime.now() - timedelta(minutes=1)

    if USER_MODEL.getUser(jwtInfo.get('uuid')) is None or datetime.fromtimestamp(jwtInfo.get('exp')) < datetime.now():
        return {
            'result': 'fail'
        }

    if not datetime.fromtimestamp(jwtInfo.get('exp')) >= diffTime:
        return {
            'result': 'success',
            'status': 'alive',
            "jwtToken": token,
            "token_type": "bearer"
        }

    tokenInfo = LOGIN_MODEL.getTokens(jwtInfo.get('uuid'))
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

    LOGIN_MODEL.updateAccessToken(jwtInfo.get('uuid'), '1', newAccessToken, expireAt)

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
