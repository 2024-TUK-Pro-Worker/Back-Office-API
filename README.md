# AI Shorts Maker - Back Office API

## 기술 스펙

### 언어
- Python (v3.11.8)

### Framework
- FastAPI

## 프로젝트 개발 설정 방법
1. requeirements.txt를 사용하여 python packages 설치
2. 오디오 코덱 관련 프로그램 설치
    - Mac OS
      1. brew install flac
      2. brew install ffmpeg
    - Windows
      - https://doa-oh.tistory.com/170
3. 아래 명령어로 서버 구동
   - `uvicorn run:app --host 0.0.0.0 --port 8081 --reload`