# Python 모듈
import os

# 소스 파일 선언
from Model.Auth.User import User as userModel


def trialStatusOff(uuid):
    try:
        userInfo = userModel().getUser(uuid)

        if userInfo['trial'] == 'N':
            raise Exception('already trial status is OFF')

        chageStatusResult = userModel().updateTrialStatus(uuid, 'N')

        if not chageStatusResult:
            raise Exception('trial status change fail')

        return {
            'result': True,
            'uuid': uuid
        }
    except Exception as e:
        return {
            'result': False,
            'message': e
        }
