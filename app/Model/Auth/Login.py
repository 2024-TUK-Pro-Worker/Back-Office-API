import pymysql


class Login:
    def __init__(self):
        # DB와 접근하는 conn, cur 객체 생성
        self.db = pymysql.connect(host="localhost", port=13306, user="root", password="root",
                                  db='backoffice', charset="utf8")
        self.cur = self.db.cursor()

    def getAuthInfo(self, uuid):
        try:
            query = session.query(LoginDto).filter(LoginDto.uuid == uuid).first()
            sql = "SELECT accessToken, refreshToken, idToken, expireAt, scope FROM login WHERE uuid = %s"
            self.cur.execute(sql, (uuid,))
            row = self.cur.fetchone()
        finally:
            self.db.close()

        return row

    def updateAuth(self, uuid, socialType, accessToken, refreshToken, idToken, expiresIn, scope, expireAt):
        try:
            sql = ("""
                   INSERT INTO login (uuid, socialType, accessToken, refreshToken, idToken, expiresIn, scope, expireAt, updatedAt) 
                   VALUES (%s, %s, %s, %s, %s, %s, %s, %s, CURRENT_TIMESTAMP)
                   ON DUPLICATE KEY UPDATE 
                   accessToken = %s,
                   idToken = %s,
                   expiresIn = %s,
                   scope = %s,
                   expireAt = %s,
                   updatedAt = CURRENT_TIMESTAMP
                   """)

            self.cur.execute(sql, (
                uuid, socialType, accessToken, refreshToken, idToken, expiresIn, scope, expireAt,
                accessToken, idToken, expiresIn, scope, expireAt
            ))

            self.db.commit()
        except:
            self.db.close()
            return False
        finally:
            self.db.close()

    def updateAccessToken(self, uuid, socialType, accessToken, expireAt):
        try:
            sql = "UPDATE login set accessToken = %s, expireAt = %s, updatedAt = CURRENT_TIMESTAMP where uuid = %s and socialType = %s"

            self.cur.execute(sql, (accessToken, expireAt, uuid, socialType))

            self.db.commit()
        except:
            self.db.close()
            return False
        finally:
            self.db.close()
