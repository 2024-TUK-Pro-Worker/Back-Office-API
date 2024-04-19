import pymysql
from datetime import date


class Video:
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

    def getVideoInfo(self, uuid, createdDate=date.today()):
        try:
            sql = "SELECT * FROM video WHERE uuid = %s AND createdAt BETWEEN %s AND %s"
            self.cur.execute(sql, (uuid, (createdDate + ' 00:00:00'), (createdDate + ' 23:59:59')))

            row = self.cur.fetchone()
        finally:
            self.db.close()
        return row

    def getVideoDescription(self, uuid, videoId):
        try:
            sql = "SELECT gptTitle, title, content, tags FROM video WHERE uuid = %s AND id = %s"
            self.cur.execute(sql, (uuid, videoId))

            row = self.cur.fetchone()
        finally:
            self.db.close()
        return row

    def getVideoId(self, uuid, videoId):
        try:
            sql = "SELECT id, uploadId FROM video WHERE uuid = %s AND id = %s"
            self.cur.execute(sql, (uuid, videoId))

            row = self.cur.fetchone()
        finally:
            self.db.close()
        return row

    def insertVideoInfo(self, uuid, title):
        try:
            sql = """
                  INSERT INTO video (uuid, title) VALUES (%s, %s)
                  """

            self.cur.execute(sql, (uuid, title))

            self.db.commit()
        except:
            self.db.close()
            return False
        finally:
            self.db.close()

    def updateVideoDescription(self, uuid, videoId, uploadId):
        try:
            sql = "UPDATE video set uploadId = %s, uploadAt = CURRENT_TIMESTAMP where uuid = %s and id = %s"

            self.cur.execute(sql, (uploadId, uuid, videoId))

            self.db.commit()
        except:
            self.db.close()
            return False
        finally:
            self.db.close()

    def setVideoInfo(self, uuid, videoId, title, description, tags):
        try:
            sql = "UPDATE video set title = %s, content = %s, tags = %s, uploadAt = CURRENT_TIMESTAMP where uuid = %s and id = %s"

            self.cur.execute(sql, (title, description, tags, uuid, videoId))

            self.db.commit()
        except:
            self.db.close()
            return False
        finally:
            self.db.close()

    def deleteVideo(self, uuid, videoId):
        try:
            sql = "UPDATE video set isDeleted = %s, deletedAt = CURRENT_TIMESTAMP where uuid = %s and id = %s"

            self.cur.execute(sql, ('Y', uuid, videoId))

            self.db.commit()
        except:
            self.db.close()
            return False
        finally:
            self.db.close()