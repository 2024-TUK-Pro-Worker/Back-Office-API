def appendBgm():
    global title
    global resourcePath

    bgmList = os.listdir(f"{resourcePath}/{uuid}/Bgm")
    bgm = random.choice(bgmList)

    # 비디오 파일과 새 오디오 파일 불러오기
    video = VideoFileClip(f"{resourcePath}/{uuid}/Upload/tmp/{title}.mp4")
    videoRange = int(video.duration) * 1000

    # 영상 길이에 맞춰 브금 길이 자르기
    bgmAudio = AudioSegment.from_file(f"{resourcePath}/{uuid}/Bgm/{bgm}")
    trimmedAudio = bgmAudio[0:videoRange]
    trimmedAudio.export(f"{resourcePath}/{uuid}/Audio/{title}/bgm.mp3", format="mp3")

    additionalAudio = AudioFileClip(f"{resourcePath}/{uuid}/Audio/{title}/bgm.mp3")

    # 기존 오디오와 새 오디오의 볼륨 조정(1.0이 기존 볼륨 크기 기준)
    originalAudio = video.audio.volumex(6.0)
    additionalAudio = additionalAudio.volumex(0.3)

    # 조정된 볼륨으로 오디오 결합
    combinedAudio = CompositeAudioClip([originalAudio, additionalAudio])

    # 비디오의 오디오를 결합된 오디오로 교체
    video = video.set_audio(combinedAudio)

    # 결과 비디오 파일 저장(코덱: mp4 기준)
    video.write_videofile(f"{resourcePath}/{uuid}/Upload/{title}.mp4")