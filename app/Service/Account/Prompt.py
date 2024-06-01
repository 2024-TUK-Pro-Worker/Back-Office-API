# Python 모듈

# 소스 파일 선언
from Model.Account.Prompt import Prompt as promptModel


def getPrompt(uuid: str):
    try:
        return promptModel().getPrompt(uuid)
    except:
        return None

def updatePrompt(uuid, content):
    try:
        return promptModel().updatePrompt(uuid, content)
    except:
        return False
