import os
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload
from google.oauth2.credentials import Credentials
from app.Model.Auth.Login import Login as loginModel
from app.Model.Auth.Video import Video as videoModel


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
            videoTitle = videoDescription[0]
            videoContent = videoDescription[1]
            videotags = videoDescription[2].split(',')

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
            media = MediaFileUpload(f'Resource/Upload/{videoTitle}.mp4')
            insertRequest = self.youtubeService.videos().insert(
                part='snippet,status',
                body=requestBody,
                media_body=media
            )

            # 동영상 업로드 실행
            response = insertRequest.execute()

            # 업로드 성공 시 동영상 ID 반환
            if 'id' in response:
                videoModel().updateVideoDescription(uuid, videoId, response['id'])
            else:
                raise Exception('업로드 실패')

        except HttpError as e:
            print('동영상 업로드 중 오류 발생:', e)


    def delVideo(self, uuid, videoId):
        try:
            videoIds = videoModel().getVideoId(uuid, videoId)
            uploadId = videoIds[1]

            deleteRequest = self.youtubeService.videos().delete(
                id=uploadId
            )

            # 동영상 업로드 실행
            response = deleteRequest.execute()

            # 업로드 성공 시 동영상 ID 반환
            if 'id' in response:
                videoModel().deleteVideo(uuid, videoId)
                print(response)
            else:
                print('동영상 삭제 실패.')

        except HttpError as e:
            print('동영상 삭제 중 오류 발생:', e)
