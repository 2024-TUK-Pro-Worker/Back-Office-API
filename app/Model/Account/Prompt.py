import pymysql


class Prompt:
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

    def getPrompt(self, uuid):
        try:
            sql = "SELECT * FROM prompt WHERE uuid = %s"
            self.cur.execute(sql, (uuid,))

            row = self.cur.fetchone()
        finally:
            self.db.close()
        return row

    def insertDefaultPrompt(self, uuid):
        try:
            sql = """
                  INSERT INTO prompt (uuid, content) 
                  VALUES (%s, %s)
                  """

            self.cur.execute(sql, (
                uuid,
                '재미있고, 흥미진진한 드라마 시나리오를 작성해줘. 시나리오는 씬별로 구분 되어해. 씬은 7개를 만들어줘. 시나리오에는 제목, 등장인물에 대한 이름, 씬별 등장인물 대사가 있어야해.'
            ))

            self.db.commit()
        except:
            self.db.close()
            return False
        finally:
            self.db.close()

    def updatePrompt(self, socialType, uuid, email, name):
        try:
            sql = "UPDATE user set email = %s, name = %s, updatedAt = CURRENT_TIMESTAMP where uuid = %s and socialType = %s"

            self.cur.execute(sql, (email, name, uuid, socialType))

            self.db.commit()
        except:
            self.db.close()
            return False
        finally:
            self.db.close()