import os


def getBgmList(uuid: str):
    try:
        storagePath = f"./Resource/Storage/{uuid}/Bgm"
        if not os.path.isdir(storagePath):
            raise None

        return os.listdir(storagePath)
    except:
        return None


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
