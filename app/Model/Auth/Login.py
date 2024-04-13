import pymysql


class Login:
    def __init__(self):
        # DB와 접근하는 conn, cur 객체 생성
        self.db = pymysql.connect(host="localhost", port=13306, user="root", password="root",
                                  db='backoffice', charset="utf8")
        self.cur = self.db.cursor()

    def rawSelectSql(self, sql):
        self.cur.execute(sql)
        row = self.cur.fetchone()
        return row

    def getTokens(self, uuid):
        sql = "SELECT accessToken, refreshToken FROM login WHERE uuid = %s"
        self.cur.execute(sql, (uuid))
        row = self.cur.fetchone()
        return row

    def updateAuth(self, uuid, socialType, accessToken, refreshToken, expireAt):
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

    def updateAccessToken(self, uuid, socialType, accessToken, expireAt):
        sql = "UPDATE login set accessToken = %s, expireAt = %s, updatedAt = CURRENT_TIMESTAMP where uuid = %s and socialType = %s"

        self.cur.execute(sql,(accessToken, expireAt, uuid, socialType))

        self.db.commit()

    def __del__(self):
        self.db.close()
