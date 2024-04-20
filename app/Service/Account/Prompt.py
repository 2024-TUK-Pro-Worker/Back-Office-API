from app.Model.Account.Prompt.Schema import Prompt as promptModel


def getPrompt(uuid: str):
    try:
        return promptModel().getPrompt(uuid)
    except:
        return ''

def updatePrompt(uuid, content):
    try:
        promptModel().updatePrompt(uuid, content)
        return True
    except:
        return False
