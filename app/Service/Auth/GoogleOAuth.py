import os
import shutil
import requests
from jose import jwt
from datetime import *
from dotenv import load_dotenv
from fastapi.responses import RedirectResponse
from Model.Auth.User import User as userModel
from Model.Auth.Login import Login as loginModel
from Model.Account.Prompt import Prompt as promptModel

load_dotenv()

# Google OAuth 관련 환경변수 상수 선언
GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')
GOOGLE_CLIENT_SECRET = os.getenv('GOOGLE_CLIENT_SECRET')
GOOGLE_REDIRECT_URI = os.getenv('GOOGLE_REDIRECT_URI')


def getOAuthUrl():
    return RedirectResponse(
        f"https://accounts.google.com/o/oauth2/auth?response_type=code&client_id={GOOGLE_CLIENT_ID}&redirect_uri={GOOGLE_REDIRECT_URI}&scope=openid%20profile%20email%20https://www.googleapis.com/auth/youtube.upload%20https://www.googleapis.com/auth/youtube&access_type=offline")


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
    elif userInfo['email'] != email and userInfo['name'] != userName:
        userModel().updateUser('1', uuid, email, userName)

    userResourcePath = f"./Resource/Storage/{uuid}"
    promptResourcePath = f"./Resource/Storage/{uuid}/Prompt"
    scenarioDir = f"{userResourcePath}/Scenario"
    audioDir = f"{userResourcePath}/Audio"
    bgmDir = f"{userResourcePath}/Bgm"
    bgmTmpDir = f"{userResourcePath}/Bgm/tmp"
    imageDir = f"{userResourcePath}/Image"
    videoDir = f"{userResourcePath}/Video"
    uploadDir = f"{userResourcePath}/Upload"
    uploadTmpDir = f"{userResourcePath}/Upload/tmp"

    if not os.path.isdir(userResourcePath):
        os.makedirs(userResourcePath)
    if not os.path.isdir(promptResourcePath):
        os.makedirs(promptResourcePath)
    if not os.path.isdir(scenarioDir):
        os.makedirs(scenarioDir)
    if not os.path.isdir(audioDir):
        os.makedirs(audioDir)
    if not os.path.isdir(bgmDir):
        os.makedirs(bgmDir)
    if not os.path.isdir(bgmTmpDir):
        os.makedirs(bgmTmpDir)
    if not os.path.isdir(imageDir):
        os.makedirs(imageDir)
    if not os.path.isdir(uploadDir):
        os.makedirs(uploadDir)
    if not os.path.isdir(videoDir):
        os.makedirs(videoDir)
    if not os.path.isdir(uploadTmpDir):
        os.makedirs(uploadTmpDir)
    if (not os.path.isfile(f'{promptResourcePath}/GPTPrompt.txt') or
            not os.path.isfile(f'{promptResourcePath}/CustomGPTPrompt.txt')):
        shutil.copytree('./Resource/Prompt', promptResourcePath, dirs_exist_ok=True)

    if refreshToken == None:
        refreshToken = loginModel().getAuthInfo(uuid)

        if refreshToken is None:
            return {
                'result': False,
                'message': 'OAuth Info Is None'
            }

        refreshToken = refreshToken['refreshToken']

    loginResult = loginModel().updateAuth(uuid, '1', accessToken, refreshToken, idToken, expiresIn, scope, expireAt)

    if not loginResult:
        return False

    data = {
        "uuid": uuid,
        "name": userName,
        "email": email,
        "exp": expireAt
    }

    return jwt.encode(data, os.getenv('JWT_SALT_KEY'), algorithm="HS256")
