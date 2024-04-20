import os
import requests
from jose import jwt
from datetime import *
from dotenv import load_dotenv
from fastapi.responses import RedirectResponse
from app.Model.Auth.User import User as userModel
from app.Model.Auth.Login import Login as loginModel
from app.Model.Account.Prompt import Prompt as promptModel

load_dotenv()

# Google OAuth 관련 환경변수 상수 선언
GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')
GOOGLE_CLIENT_SECRET = os.getenv('GOOGLE_CLIENT_SECRET')
GOOGLE_REDIRECT_URI = os.getenv('GOOGLE_REDIRECT_URI')


def getOAuthUrl():
    return RedirectResponse(
        f"https://accounts.google.com/o/oauth2/auth?response_type=code&client_id={GOOGLE_CLIENT_ID}&redirect_uri={GOOGLE_REDIRECT_URI}&scope=openid%20profile%20email%20https://www.googleapis.com/auth/youtube&access_type=offline")


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
    idToken = googleToken.json().get("id_token")
    expiresIn = googleToken.json().get("expires_in")
    scope = googleToken.json().get("scope")

    user_info = requests.get("https://www.googleapis.com/oauth2/v1/userinfo",
                             headers={"Authorization": f"Bearer {accessToken}"})

    uuid = user_info.json().get("id")
    email = user_info.json().get("email")
    userName = user_info.json().get("name")
    currentDt = datetime.now()
    expireAt = currentDt + timedelta(seconds=googleToken.json().get('expires_in'))

    userInfo = userModel().getUser(uuid)

    if userInfo == None:
        userModel().insertUser('1', uuid, email, userName)
        promptModel().insertDefaultPrompt(uuid)
    elif userInfo[3] != email and userInfo[4] != userName:
        userModel().updateUser('1', uuid, email, userName)

    if refreshToken == None:
        refreshToken = loginModel().getAuthInfo(uuid)[1]

    loginModel().updateAuth(uuid, '1', accessToken, refreshToken, idToken, expiresIn, scope, expireAt)

    data = {
        "uuid": uuid,
        "name": userName,
        "email": email,
        "exp": expireAt
    }

    return jwt.encode(data, os.getenv('JWT_SALT_KEY'), algorithm="HS256")