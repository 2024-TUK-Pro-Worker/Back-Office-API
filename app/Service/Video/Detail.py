from app.Model.Video.Video import Video as videoModel


def updateDetail(uuid, videoId, title, content, tags):
    tagToString = ','.join(tags)
    videoModel().setVideoInfo(uuid, videoId, title, content, tagToString)
    return True