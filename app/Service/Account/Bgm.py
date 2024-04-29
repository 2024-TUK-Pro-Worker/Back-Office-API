import os


def getBgmList(uuid: str):
    try:
        storagePath = f"./Resource/Storage/{uuid}/Bgm"
        if not os.path.isdir(storagePath):
            raise '디렉토리 없음'

        return os.listdir(storagePath)
    except:
        return []


def uploadBgmFile(uuid: str, bgmFileName, bgmFile):
    try:
        storagePath = f"./Resource/Storage/{uuid}/Bgm"
        fileSavePath = f"{storagePath}/{bgmFileName}"
        if not os.path.isdir(storagePath):
            os.makedirs(storagePath)

        if os.path.isfile(f"{storagePath}/{bgmFileName}"):
            raise '동일 파일명 파일 존재'

        with open(fileSavePath, "wb") as fp:
            fp.write(bgmFile)
            fp.close()

        if not os.path.isfile(f"{storagePath}/{bgmFileName}"):
            raise '파일 저장 실패'

        return True
    except:
        return False


def deleteBgmFile(uuid: str, fileName: str):
    try:
        filePath = f"./Resource/Storage/{uuid}/Bgm/{fileName}"
        if not os.path.isfile(filePath):
            raise '파일이 존재하지 않음'

        os.remove(filePath)

        if os.path.isfile(filePath):
            raise '파일 삭제 실패'

        return True
    except:
        return False
