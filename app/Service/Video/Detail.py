from app.Model.Video.Video import Video as videoModel


def getList(uuid):
    try:
        return videoModel().getVideoList(uuid)
    except:
        return []


def getDetail(uuid, videoId):
    try:
        return videoModel().getVideoInfo(uuid, videoId)
    except:
        return []


def updateDetail(uuid, videoId, title, content, tags):
    tagToString = ','.join(tags)
    videoModel().setVideoInfo(uuid, videoId, title, content, tagToString)
    return True
