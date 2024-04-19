from app.Model.Account.Prompt import Prompt as promptModel

def getPrompt(uuid):
    try:
        return promptModel().getPrompt(uuid)[0]
    except:
        return ''

def updatePrompt(uuid, content):
    try:
        promptModel().updatePrompt(uuid, content)
        return True
    except:
        return False