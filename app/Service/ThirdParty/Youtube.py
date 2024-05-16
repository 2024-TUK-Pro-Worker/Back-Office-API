import os
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload
from google.oauth2.credentials import Credentials
from Model.Auth.Login import Login as loginModel
from Model.Video.Video import Video as videoModel


class Youtube:
    def __init__(self, jwtInfo):
        googleAuthInfo = loginModel().getAuthInfo(jwtInfo.get('uuid'))

        creds = Credentials(token=googleAuthInfo['accessToken'],
                            refresh_token=googleAuthInfo['refreshToken'],
                            id_token=googleAuthInfo['idToken'],
                            token_uri='https://accounts.google.com/o/oauth2/token',
                            client_id=os.getenv('GOOGLE_CLIENT_ID'),
                            client_secret=os.getenv('GOOGLE_CLIENT_SECRET'),
                            expiry=googleAuthInfo['expireAt'],
                            scopes=googleAuthInfo['scope'])

        self.youtubeService = build('youtube', 'v3', credentials=creds)

    def uploadVideo(self, uuid, videoId):
        try:
            videoDescription = videoModel().getVideoInfo(uuid, videoId)

            # 동영상 업로드 정보 설정
            requestBody = {
                'snippet': {
                    'title': videoDescription['title'],
                    'description': videoDescription['content'],
                    'tags': videoDescription['tags']
                },
                'status': {
                    'privacyStatus': 'public'
                }
            }

            # 동영상 업로드 요청 생성
            media = MediaFileUpload(f'Resource/Storage/{uuid}/Upload/{videoDescription["gptTitle"]}.mp4')
            insertRequest = self.youtubeService.videos().insert(
                part='snippet,status',
                body=requestBody,
                media_body=media
            )

            response = insertRequest.execute()

            if 'id' not in response:
                raise Exception('youtube upload fail')

            if not videoModel().updateVideoDescription(uuid, videoId, response['id']):
                raise Exception('youtube upload info update fail')

            return {
                'result': True,
                'uuid': uuid,
                'videoId': videoId
            }
        except Exception as e:
            return {
                'result': False,
                'message': e
            }
        except HttpError as e:
            return {
                'result': False,
                'message': e
            }

    def delVideo(self, uuid, videoId):
        try:
            videoIds = videoModel().getVideoId(uuid, videoId)

            deleteRequest = self.youtubeService.videos().delete(
                id=videoIds['uploadId']
            )

            response = deleteRequest.execute()

            if response != '':
                raise Exception('video delete fail')

            if not videoModel().deleteVideo(uuid, videoId):
                raise Exception('video delete info update fail')

            return {
                'result': True,
                'uuid': uuid,
                'videoId': videoId
            }
        except Exception as e:
            return {
                'result': False,
                'message': e
            }
        except HttpError as e:
            return {
                'result': False,
                'message': e
            }
