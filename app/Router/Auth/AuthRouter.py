# Python 모듈
import os
from typing import Union, Optional
from fastapi import APIRouter, Cookie

# 소스 파일 선언
from Service.Auth.Account import *
from Service.Auth.GoogleOAuth import *
from Router import Model as DefaultRoutingModel

google = APIRouter(prefix='/auth/google')
account = APIRouter(prefix='/api/account')


@google.get('/login', tags=['googleAuth'])
def getUrl():
    return getOAuthUrl()


@google.get('/callback', tags=['googleAuth'])
def getCallback(code: str):
    jwtToken = authGoogle(code)
    response = RedirectResponse(f"https://{os.getenv('FRONT_HOST')}/")
    response.set_cookie(key="authorization", value=jwtToken, path="/", domain=f"{os.getenv('DOAMIN')}")
    return response


@account.patch('/trial/off', tags=['account'],
               response_model=Union[DefaultRoutingModel.RS_common, DefaultRoutingModel.RS_fail])
def patchTrialStatusOff(authorization: Optional[str] = Cookie(None)):
    try:
        jwtData = jwt.decode(authorization, os.getenv('JWT_SALT_KEY'), algorithms="HS256")

        result = trialStatusOff(jwtData.get('uuid'))

        if result['result'] is False:
            raise Exception(result['message'])

        return {
            'result': 'success',
            'data': {
                'uuid': jwtData.get('uuid')
            }
        }
    except Exception as e:
        return {
            'result': 'fail',
            'message': e.__str__()
        }
