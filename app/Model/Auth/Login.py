# Python 모듈
from sqlalchemy import func
from sqlalchemy.dialects.mysql import insert

# 소스 파일 선언
from Model import Models
from Config.DataBase.database import engine, SessionLocal

Models.Base.metadata.create_all(bind=engine)


class Login:
    def __init__(self):
        self.db = SessionLocal()

    def getAuthInfo(self, uuid):
        try:
            data = self.db.query(Models.Login).filter(Models.Login.uuid == uuid).first()
            data = data.__dict__
            data.pop('_sa_instance_state', None)
            return data
        except:
            return None
        finally:
            self.db.close()

    def updateAuth(self, uuid, socialType, accessToken, refreshToken, idToken, expiresIn, scope, expireAt):
        try:
            sql = (
                insert(Models.Login)
                .values({
                    Models.Login.uuid: uuid,
                    Models.Login.socialType: socialType,
                    Models.Login.accessToken: accessToken,
                    Models.Login.refreshToken: refreshToken,
                    Models.Login.idToken: idToken,
                    Models.Login.expiresIn: expiresIn,
                    Models.Login.scope: scope,
                    Models.Login.expireAt: expireAt,
                    Models.Login.updatedAt: func.now()
                })
                .on_duplicate_key_update(
                    accessToken=accessToken,
                    idToken=idToken,
                    expiresIn=expiresIn,
                    scope=scope,
                    expireAt=expireAt,
                    updatedAt=func.now()
                )
            )
            self.db.execute(sql)

            self.db.commit()
            return True
        except:
            return False
        finally:
            self.db.close()
