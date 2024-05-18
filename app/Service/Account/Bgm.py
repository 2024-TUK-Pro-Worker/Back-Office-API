import os
from typing import BinaryIO


def getBgmList(uuid: str):
    try:
        storagePath = f"./Resource/Storage/{uuid}/Bgm"
        if not os.path.isdir(storagePath):
            raise None

        bgmFileList = os.listdir(storagePath)
        bgmFileList.remove('tmp')

        return bgmFileList
    except:
        return None


def getPreviewInfo(uuid, bgmName, rangeHeader):
    try:
        bgmPath = f"./Resource/Storage/{uuid}/Bgm/{bgmName}.mp3"

        if not os.path.isfile(bgmPath):
            raise Exception('bgm file is not exist')

        # file Size & start end point
        fileSize = os.stat(bgmPath).st_size

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
            'filePath': bgmPath,
            'fileSize': fileSize,
            'startPoint': start,
            'endPoint': end
        }
    except Exception as e:
        return {
            'result': False,
            'message': e
        }


def getPreviewVideo(fileObj: BinaryIO, start: int, end: int):
    with fileObj as f:
        f.seek(start)
        while (pos := f.tell()) <= end:
            readSize = end + 1 - pos
            yield f.read(readSize)


def uploadBgmFile(uuid: str, fileList: list):
    global fileUploadResult

    try:
        fileUploadResult = {}

        for fileData in fileList:
            bgmFileName = fileData.filename
            bgmFile = fileData.file.read()

            try:
                storagePath = f"./Resource/Storage/{uuid}/Bgm"
                fileSavePath = f"{storagePath}/{bgmFileName}"
                if not os.path.isdir(storagePath):
                    os.makedirs(storagePath)

                if os.path.isfile(f"{storagePath}/{bgmFileName}"):
                    raise Exception('same file name file exist')

                with open(fileSavePath, "wb") as fp:
                    fp.write(bgmFile)
                    fp.close()

                if not os.path.isfile(f"{storagePath}/{bgmFileName}"):
                    raise Exception('file upload fail')

                fileUploadResult[bgmFileName] = {
                    'result': True
                }
            except Exception as e:
                fileUploadResult[bgmFileName] = {
                    'result': False,
                    'message': e.__str__()
                }

        return {
            'result': True,
            'uploadList': fileUploadResult
        }
    except:
        return {
            'result': False,
            'message': 'file upload fail'
        }


def deleteBgmFile(uuid: str, fileName: str):
    try:
        filePath = f"./Resource/Storage/{uuid}/Bgm/{fileName}"
        if not os.path.isfile(filePath):
            raise Exception('file is not exist')

        os.remove(filePath)

        if os.path.isfile(filePath):
            raise Exception('file delete fail')

        return {
            'result': True
        }
    except Exception as e:
        return {
            'result': False,
            'message': e
        }
