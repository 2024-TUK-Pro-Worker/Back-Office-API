import os
from pydub import *
from typing import BinaryIO
from moviepy.editor import *
from Model.Video.Video import Video as videoModel


def getList(uuid):
    try:
        return videoModel().getVideoList(uuid)
    except:
        return None


def getDetail(uuid, videoId):
    try:
        return videoModel().getVideoInfo(uuid, videoId)
    except:
        return None


def getPreviewInfo(uuid, videoId, rangeHeader):
    try:
        videoInfo = videoModel().getVideoInfo(uuid, videoId)

        if videoInfo['uuid'] is not uuid:
            raise Exception('Invalid Request')

        videoPath = f"./Resource/Storage/{uuid}/Upload/tmp/{videoInfo['gptTitle']}.mp4"

        if not os.path.isfile(videoPath):
            videoPath = f"./Resource/Storage/{uuid}/Upload/{videoInfo['gptTitle']}.mp4"
            if not os.path.isfile(videoPath):
                raise Exception('video is not exist')

        # file Size & start end point
        fileSize = os.stat(videoPath).st_size

        try:
            h = rangeHeader.replace("bytes=", "").split("-")
            start = int(h[0]) if h[0] != "" else 0
            end = int(h[1]) if h[1] != "" else fileSize - 1
        except ValueError:
            raise Exception(f'Invalid request range (Range:{rangeHeader!r})')

        if start > end or start < 0 or end > fileSize - 1:
            raise Exception(f'Invalid request range (Range:{rangeHeader!r})')

        return {
            'result': True,
            'filePath': videoPath,
            'fileSize': fileSize,
            'startPoint': start,
            'endPoint': end
        }
    except Exception as e:
        return {
            'result': False,
            'message': e
        }

def getPreviewVideo(fileObj: BinaryIO, start: int, end: int, chunk: int = 1024*1792):
    with fileObj as f:
        f.seek(start)
        while (pos := f.tell()) <= end:
            readSize = min(chunk, end + 1 - pos)
            yield f.read(readSize)


def updateDetail(uuid, videoId, title, content, tags):
    tagToString = ','.join(tags)
    return videoModel().setVideoInfo(uuid, videoId, title, content, tagToString)


def insertIntoVideo(uuid, videoId, bgmFileName):
    try:
        videoInfo = videoModel().getVideoInfo(uuid, videoId)

        if videoInfo is None:
            raise Exception('video info is None')

        videoTmpPath = f"./Resource/Storage/{uuid}/Upload/tmp/{videoInfo['gptTitle']}.mp4"
        videoPath = f"./Resource/Storage/{uuid}/Upload/{videoInfo['gptTitle']}.mp4"
        originBgmPath = f"./Resource/Storage/{uuid}/Bgm/{bgmFileName}"
        bgmPath = f"./Resource/Storage/{uuid}/Bgm/tmp/{videoId}_{bgmFileName}"

        if not os.path.isfile(videoTmpPath):
            raise Exception('merge target video is not found')

        if not os.path.isfile(originBgmPath):
            raise Exception('merge target bgm is not found')

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
            raise Exception('video merging error')

        if os.path.isfile(videoTmpPath):
            os.remove(videoTmpPath)

        if os.path.isfile(bgmPath):
            os.remove(bgmPath)
    except Exception as e:
        return {
            'result': False,
            'message': e
        }
    finally:
        return {
            'result': True
        }
