from Model import Models
from sqlalchemy import and_, func
from Config.DataBase.database import engine, SessionLocal

Models.Base.metadata.create_all(bind=engine)


class Video:
    def __init__(self):
        self.db = SessionLocal()

    def getVideoList(self, uuid):
        global result

        try:
            result = []

            queryResult = self.db.query(Models.Video).filter(Models.Video.uuid == uuid).order_by(Models.Video.createdAt.desc()).all()

            for row in queryResult:
                tmp = row.__dict__
                tmp.pop('_sa_instance_state', None)
                tmp['tags'] = tmp['tags'].split(',') if tmp['tags'] is not None else None
                tmp['createdAt'] = str(tmp['createdAt'])
                tmp['uploadAt'] = str(tmp['uploadAt']) if tmp['uploadAt'] is not None else tmp['uploadAt']
                tmp['deletedAt'] = str(tmp['deletedAt']) if tmp['deletedAt'] is not None else tmp['deletedAt']
                result.append(tmp)

            return result
        except:
            return None
        finally:
            self.db.close()

    def getVideoInfo(self, uuid, videoId):
        global data

        try:
            queryResult = self.db.query(Models.Video).filter(
                and_(
                    Models.Video.id == videoId,
                    Models.Video.uuid == uuid
                )
            ).first()

            data = queryResult.__dict__
            data.pop('_sa_instance_state', None)
            data['tags'] = data['tags'].split(',') if data['tags'] is not None else None
            data['createdAt'] = str(data['createdAt'])
            data['uploadAt'] = str(data['uploadAt']) if data['uploadAt'] is not None else data['uploadAt']
            data['deletedAt'] = str(data['deletedAt']) if data['deletedAt'] is not None else data['deletedAt']

            return data
        except:
            return None
        finally:
            self.db.close()

    def getVideoId(self, uuid, videoId):
        global result

        try:
            result = {}

            queryResult = self.db.query(Models.Video).filter(
                and_(
                    Models.Video.id == videoId,
                    Models.Video.uuid == uuid
                )
            ).first()

            data = queryResult.__dict__
            data.pop('_sa_instance_state', None)

            return data
        except:
            return None
        finally:
            self.db.close()

    def updateVideoDescription(self, uuid, videoId, uploadId):
        try:
            self.db.query(Models.Video).filter(and_(Models.Video.id == videoId, Models.Video.uuid == uuid)).update(
                {'uploadId': uploadId, 'uploadAt': func.now()})
            self.db.commit()

            return True
        except:
            self.db.rollback()
            return False
        finally:
            self.db.close()

    def setVideoInfo(self, uuid, videoId, title, description, tags):
        try:
            self.db.query(Models.Video).filter(and_(Models.Video.id == videoId, Models.Video.uuid == uuid)).update(
                {
                    'title': title,
                    'content': description,
                    'tags': tags
                })
            self.db.commit()

            return True
        except:
            self.db.rollback()
            return False
        finally:
            self.db.close()

    def deleteVideo(self, uuid, videoId):
        try:
            self.db.query(Models.Video).filter(and_(Models.Video.id == videoId, Models.Video.uuid == uuid)).update(
                {
                    'isDeleted': 'Y',
                    'deletedAt': func.now()
                })
            self.db.commit()
            return True
        except:
            self.db.rollback()
            return False
        finally:
            self.db.close()
