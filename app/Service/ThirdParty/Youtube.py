import os
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload
from google.oauth2.credentials import Credentials
from app.Model.Auth.Login import Login as loginModel
from app.Model.Video.Schema import Video as videoModel


class Youtube:
    def __init__(self, jwtInfo):
        googleAuthInfo = loginModel().getAuthInfo(jwtInfo.get('uuid'))

        creds = Credentials(token=googleAuthInfo[0],
                            refresh_token=googleAuthInfo[1],
                            id_token=googleAuthInfo[2],
                            token_uri='https://accounts.google.com/o/oauth2/token',
                            client_id=os.getenv('GOOGLE_CLIENT_ID'),
                            client_secret=os.getenv('GOOGLE_CLIENT_SECRET'),
                            expiry=googleAuthInfo[3],
                            scopes=googleAuthInfo[4])

        self.youtubeService = build('youtube', 'v3', credentials=creds)

    def uploadVideo(self, uuid, videoId):
        try:
            videoDescription = videoModel().getVideoDescription(uuid, videoId)
            gptTitle = videoDescription[0]
            videoTitle = videoDescription[1]
            videoContent = videoDescription[2]
            videotags = videoDescription[3].split(',')

            # 동영상 업로드 정보 설정
            requestBody = {
                'snippet': {
                    'title': videoTitle,
                    'description': videoContent,
                    'tags': videotags
                },
                'status': {
                    'privacyStatus': 'public'
                }
            }

            # 동영상 업로드 요청 생성
            media = MediaFileUpload(f'Resource/Upload/{gptTitle}.mp4')
            insertRequest = self.youtubeService.videos().insert(
                part='snippet,status',
                body=requestBody,
                media_body=media
            )

            response = insertRequest.execute()

            if 'id' not in response:
                raise Exception('업로드 실패')

            videoModel().updateVideoDescription(uuid, videoId, response['id'])

            return {
                'result': True,
                'uuid': uuid,
                'videoId': videoId
            }

        except Exception as e:
            print('동영상 삭제 중 오류 발생:', e)

            return {
                'result': False,
                'message': e
            }
        except HttpError as e:
            print('동영상 업로드 중 오류 발생:', e)

            return {
                'result': False,
                'message': e
            }


    def delVideo(self, uuid, videoId):
        try:
            videoIds = videoModel().getVideoId(uuid, videoId)
            uploadId = videoIds[1]

            deleteRequest = self.youtubeService.videos().delete(
                id=uploadId
            )

            response = deleteRequest.execute()

            if response != '':
                raise Exception('동영상 삭제 실패.')

            videoModel().deleteVideo(uuid, videoId)

            return {
                'result': True,
                'uuid': uuid,
                'videoId': videoId
            }

        except Exception as e:
            print('동영상 삭제 중 오류 발생:', e)

            return {
                'result': False,
                'message': e
            }
        except HttpError as e:
            print('동영상 삭제 중 오류 발생:', e)

            return {
                'result': False,
                'message': e
            }
