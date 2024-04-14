import os
from datetime import *
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload
from google.oauth2.credentials import Credentials
from app.Model.Auth.Login import Login as loginModel


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

    def uploadVideo(self):
        try:
            # 동영상 업로드 정보 설정
            requestBody = {
                'snippet': {
                    'title': 'Memory Lane',
                    'description': 'Memory Lane',
                    'tags': []
                },
                'status': {
                    'privacyStatus': 'public'  # 동영상 공개 설정 (public, private, unlisted 중 선택)
                }
            }

            # 동영상 업로드 요청 생성
            media = MediaFileUpload('../tmp/Memory Lane.mp4')
            insertRequest = self.youtubeService.videos().insert(
                part='snippet,status',
                body=requestBody,
                media_body=media
            )

            # 동영상 업로드 실행
            response = insertRequest.execute()

            # 업로드 성공 시 동영상 ID 반환
            if 'id' in response:
                print('동영상 업로드 완료. 동영상 ID:', response['id'])
            else:
                print('동영상 업로드 실패.')

        except HttpError as e:
            print('동영상 업로드 중 오류 발생:', e)
