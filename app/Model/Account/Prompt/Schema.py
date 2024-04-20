from app.Config.database import engine, SessionLocal
from app.Model.Account.Prompt import Model

Model.Base.metadata.create_all(bind=engine)


class Prompt:
    def __init__(self):
        # DB와 접근하는 conn, cur 객체 생성
        self.db = SessionLocal()

    def getPrompt(self, uuid):
        try:
            row = self.db.query(Model.Prompt).filter(Model.Prompt.uuid == uuid).first()
        finally:
            self.db.close()
        return row

    def insertDefaultPrompt(self, uuid):
        try:
            self.db.add(Model.Prompt(uuid=uuid, content='재미있고, 흥미진진한 드라마 시나리오를 작성해줘. 시나리오는 씬별로 구분 되어해. 씬은 7개를 만들어줘. 시나리오에는 제목, 등장인물에 대한 이름, 씬별 등장인물 대사가 있어야해.'))
            self.db.commit()
        except:
            self.db.close()
            return False
        finally:
            self.db.close()

    def updatePrompt(self, uuid, content):
        try:
            self.db.query(Model.Prompt).filter(Model.Prompt.uuid == uuid).update({'content': content})
            self.db.commit()
        except:
            self.db.close()
            return False
        finally:
            self.db.close()
