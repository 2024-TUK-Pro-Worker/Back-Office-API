from Model import Models
from Config.DataBase.database import engine, SessionLocal

Models.Base.metadata.create_all(bind=engine)


class Prompt:
    def __init__(self):
        self.db = SessionLocal()

    def getPrompt(self, uuid):
        global data

        try:
            data = self.db.query(Models.Prompt).filter(Models.Prompt.uuid == uuid).first()
            data = data.__dict__
            data.pop('_sa_instance_state', None)
            return data
        except:
            return {
                'uuid': uuid,
                'content': '재미있고, 흥미진진한 드라마 시나리오를 작성해줘. 시나리오는 씬별로 구분 되어해. 씬은 7개를 만들어줘. 시나리오에는 제목, 등장인물에 대한 이름, 씬별 등장인물 대사가 있어야해.'
            }
        finally:
            self.db.close()

    def insertDefaultPrompt(self, uuid):
        try:
            self.db.add(Models.Prompt(uuid=uuid,
                                      content='재미있고, 흥미진진한 드라마 시나리오를 작성해줘. 시나리오는 씬별로 구분 되어해. 씬은 7개를 만들어줘. 시나리오에는 제목, 등장인물에 대한 이름, 씬별 등장인물 대사가 있어야해.'))
            self.db.commit()
            return True
        except:
            self.db.rollback()
            return False
        finally:
            self.db.close()

    def updatePrompt(self, uuid, content):
        try:
            self.db.query(Models.Prompt).filter(Models.Prompt.uuid == uuid).update({'content': content})
            self.db.commit()
            return True
        except:
            self.db.rollback()
            return False
        finally:
            self.db.close()
