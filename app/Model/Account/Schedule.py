from Model import Models
from Config.DataBase.database import engine, SessionLocal

Models.Base.metadata.create_all(bind=engine)


class Schedule:
    def __init__(self):
        self.db = SessionLocal()

    def getSchedule(self, uuid):
        global data

        try:
            data = self.db.query(Models.Schedule).filter(Models.Schedule.uuid == uuid).first()
            data = data.__dict__
            data.pop('_sa_instance_state', None)
            return data
        except:
            return {'uuid': uuid, 'cronSchedule': '*/20 * * * *'}
        finally:
            self.db.close()

    def setSchedule(self, uuid, cronSchedule):
        try:
            data = self.db.query(Models.Schedule).filter(Models.Schedule.uuid == uuid).first()
            if data.__str__() == 'None':
                self.db.add(Models.Schedule(uuid=uuid, cronSchedule=cronSchedule))
            else :
                self.db.query(Models.Schedule).filter(Models.Schedule.uuid == uuid).update({'cronSchedule': cronSchedule})
            self.db.commit()
            return True
        except:
            self.db.rollback()
            return False
        finally:
            self.db.close()
