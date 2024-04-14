import pymysql


class User:
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

    def getUser(self, uuid=None):
        try:
            if uuid is None:
                sql = "SELECT * FROM user"
                self.cur.execute(sql)
            else:
                sql = "SELECT * FROM user WHERE uuid = %s"
                self.cur.execute(sql, (uuid))

            row = self.cur.fetchone()
        finally:
            self.db.close()
        return row

    def insertUser(self, socialType, uuid, email, name):
        try:
            sql = """
                  INSERT INTO user (socialType, uuid, email, name, updatedAt) VALUES (%s, %s, %s, %s, CURRENT_TIMESTAMP)
                  ON DUPLICATE KEY UPDATE 
                  email = %s,
                  name = %s,
                  updatedAt = CURRENT_TIMESTAMP
                  """

            self.cur.execute(sql, (socialType, uuid, email, name, email, name))

            self.db.commit()
        except:
            self.db.close()
            return False
        finally:
            self.db.close()

    def updateUser(self, socialType, uuid, email, name):
        try:
            sql = "UPDATE user set email = %s, name = %s, updatedAt = CURRENT_TIMESTAMP where uuid = %s and socialType = %s"

            self.cur.execute(sql, (email, name, uuid, socialType))

            self.db.commit()
        except:
            self.db.close()
            return False
        finally:
            self.db.close()