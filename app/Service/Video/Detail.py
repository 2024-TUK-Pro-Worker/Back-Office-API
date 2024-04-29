import os
from pydub import *
from moviepy.editor import *
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


def insertIntoVideo(uuid, videoId, bgmFileName):
    try:
        videoInfo = videoModel().getVideoInfo(uuid, videoId)

        videoTmpPath = f"./Resource/Storage/{uuid}/Upload/tmp/{videoInfo['gptTitle']}.mp4"
        videoPath = f"./Resource/Storage/{uuid}/Upload/{videoInfo['gptTitle']}.mp4"
        originBgmPath = f"./Resource/Storage/{uuid}/Bgm/{bgmFileName}"
        bgmPath = f"./Resource/Storage/{uuid}/Bgm/tmp/{videoId}_{bgmFileName}"

        if not os.path.isfile(videoTmpPath):
            raise '병합 대상 비디오가 없음'

        if not os.path.isfile(originBgmPath):
            raise '병합 대상 브금이 없음'

        video = VideoFileClip(videoTmpPath)
        videoRange = int(video.duration) * 1000

        # 영상 길이에 맞춰 브금 길이 자르기
        bgmAudio = AudioSegment.from_file(originBgmPath)
        trimmedAudio = bgmAudio[0:videoRange]
        trimmedAudio.export(bgmPath, format="mp3")

        additionalAudio = AudioFileClip(bgmPath)

        # 기존 오디오와 새 오디오의 볼륨 조정(1.0이 기존 볼륨 크기 기준)
        originalAudio = video.audio.volumex(6.0)
        additionalAudio = additionalAudio.volumex(0.3)

        # 조정된 볼륨으로 오디오 결합
        combinedAudio = CompositeAudioClip([originalAudio, additionalAudio])

        # 비디오의 오디오를 결합된 오디오로 교체
        video = video.set_audio(combinedAudio)

        # 결과 비디오 파일 저장(코덱: mp4 기준)
        video.write_videofile(videoPath)

        if not os.path.isfile(videoPath):
            raise '비디오 생성 오류'

        if os.path.isfile(videoTmpPath):
            os.remove(videoTmpPath)

        if os.path.isfile(bgmPath):
            os.remove(bgmPath)

        return True
    except:
        return False
