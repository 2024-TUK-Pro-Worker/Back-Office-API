from app.Model.Video.Video import Video as videoModel


def getList(uuid):
    try:
        videoList = videoModel().getVideoList(uuid)
        videoList = [list(videoList[x]) for x in range(len(videoList))]
        for data in videoList:
            data[6] = data[6].split(',')
            data[7] = str(data[7])
            data[8] = str(data[8])
            data[10] = str(data[10])
        return videoList
    except:
        return []

def updateDetail(uuid, videoId, title, content, tags):
    tagToString = ','.join(tags)
    videoModel().setVideoInfo(uuid, videoId, title, content, tagToString)
    return True