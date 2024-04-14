import pymysql


class Login:
    def __init__(self):
        # DB와 접근하는 conn, cur 객체 생성
        self.db = pymysql.connect(host="localhost", port=13306, user="root", password="root",
                                  db='backoffice', charset="utf8")
        self.cur = self.db.cursor()

    def rawSelectSql(self, sql):
        try:
            self.cur.execute(sql)
            row = self.cur.fetchone()
        finally:
            self.db.close()

        return row

    def getTokens(self, uuid):
        try:
            sql = "SELECT accessToken, refreshToken FROM login WHERE uuid = %s"
            self.cur.execute(sql, (uuid))
            row = self.cur.fetchone()
        finally:
            self.db.close()

        return row

    def updateAuth(self, uuid, socialType, accessToken, refreshToken, expireAt):
        try:
            sql = ("""
                   INSERT INTO login (uuid, socialType, accessToken, refreshToken, expireAt, updatedAt) 
                   VALUES (%s, %s, %s, %s, %s, CURRENT_TIMESTAMP)
                   ON DUPLICATE KEY UPDATE 
                   accessToken = %s,
                   refreshToken = %s,
                   expireAt = %s,
                   updatedAt = CURRENT_TIMESTAMP
                   """)

            self.cur.execute(sql,
                             (uuid, socialType, accessToken, refreshToken, expireAt, accessToken, refreshToken, expireAt))

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