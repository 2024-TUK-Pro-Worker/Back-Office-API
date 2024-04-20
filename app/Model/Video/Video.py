from sqlalchemy import and_
from app.Config.database import engine, SessionLocal
from app.Model import Models

Models.Base.metadata.create_all(bind=engine)


class Video:
    def __init__(self):
        self.db = SessionLocal()

    def getVideoList(self, uuid):
        result = []
        try:
            queryResult = self.db.query(Models.Video).filter(Models.Video.uuid == uuid).all()
            for row in queryResult:
                tmp = row.__dict__
                tmp.pop('_sa_instance_state', None)
                tmp['tags'] = tmp['tags'].split(',')
                tmp['createdAt'] = str(tmp['createdAt'])
                tmp['uploadAt'] = str(tmp['uploadAt']) if tmp['uploadAt'] is not None else tmp['uploadAt']
                tmp['deletedAt'] = str(tmp['deletedAt']) if tmp['deletedAt'] is not None else tmp['deletedAt']
                result.append(tmp)
        finally:
            self.db.close()

        return result

    def getVideoInfo(self, uuid, videoId):
        try:
            queryResult = self.db.query(Models.Video).filter(
                and_(
                    Models.Video.id == videoId,
                    Models.Video.uuid == uuid
                )
            ).first()

            data = queryResult.__dict__
            data.pop('_sa_instance_state', None)
            data['tags'] = data['tags'].split(',')
            data['createdAt'] = str(data['createdAt'])
            data['uploadAt'] = str(data['uploadAt']) if data['uploadAt'] is not None else data['uploadAt']
            data['deletedAt'] = str(data['deletedAt']) if data['deletedAt'] is not None else data['deletedAt']
        finally:
            self.db.close()

        return data

    def getVideoId(self, uuid, videoId):
        result = {}
        try:
            queryResult = self.db.query(Models.Video.id, Models.Video.uploadId).filter(
                and_(Models.Video.id == videoId, Models.Video.uuid == uuid)).all()

            for row in queryResult:
                tmp = row.__dict__
                tmp.pop('_sa_instance_state', None)
                result = tmp
        finally:
            self.db.close()
        return result

    def insertVideoInfo(self, uuid, title):
        try:
            self.db.add(Models.Video(uuid=uuid, gptTitle=title))
            self.db.commit()
        except:
            self.db.close()
            return False
        finally:
            self.db.close()

    def updateVideoDescription(self, uuid, videoId, uploadId):
        try:
            self.db.query(Models.Video).filter(and_(Models.Video.id == videoId, Models.Video.uuid == uuid)).update(
                {'uploadId': uploadId, 'uploadAt': 'CURRENT_TIMESTAMP'})
            self.db.commit()
        except:
            self.db.close()
            return False
        finally:
            self.db.close()

    def setVideoInfo(self, uuid, videoId, title, description, tags):
        try:
            self.db.query(Models.Video).filter(and_(Models.Video.id == videoId, Models.Video.uuid == uuid)).update(
                {
                    'title': title,
                    'content': description,
                    'tags': tags,
                    'uploadAt': 'CURRENT_TIMESTAMP'
                })
            self.db.commit()
        except:
            self.db.close()
            return False
        finally:
            self.db.close()

    def deleteVideo(self, uuid, videoId):
        try:
            self.db.query(Models.Video).filter(and_(Models.Video.id == videoId, Models.Video.uuid == uuid)).update(
                {
                    'isDeleted': 'Y',
                    'deletedAt': 'CURRENT_TIMESTAMP'
                })
            self.db.commit()
        except:
            self.db.close()
            return False
        finally:
            self.db.close()
