from Model import Models
from sqlalchemy import func
from sqlalchemy.dialects.mysql import insert
from Config.DataBase.database import engine, SessionLocal

Models.Base.metadata.create_all(bind=engine)


class User:
    def __init__(self):
        self.db = SessionLocal()

    def getUser(self, uuid):
        try:
            data = self.db.query(Models.User).filter(Models.User.uuid == uuid).first()
            data = data.__dict__
            data.pop('_sa_instance_state', None)
        finally:
            self.db.close()
            return None
        return data

    def insertUser(self, socialType, uuid, email, name):
        try:
            sql = (
                insert(Models.User)
                .values({
                    Models.User.uuid: uuid,
                    Models.User.socialType: socialType,
                    Models.User.email: email,
                    Models.User.name: name,
                    Models.User.updatedAt: func.now()
                })
                .on_duplicate_key_update(
                    email=email,
                    name=name,
                    updatedAt=func.now()
                )
            )
            self.db.execute(sql)

            self.db.commit()
        except:
            self.db.close()
            return False
        finally:
            self.db.close()
        return True

    def updateUser(self, socialType, uuid, email, name):
        try:
            self.db.query(Models.User).filter(Models.User.uuid == uuid, Models.User.socialType == socialType).update({
                'email': email,
                'name': name,
                'updatedAt': func.now()
            })
            self.db.commit()
        except:
            self.db.close()
            return False
        finally:
            self.db.close()
