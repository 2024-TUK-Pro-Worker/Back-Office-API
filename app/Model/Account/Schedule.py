from app.Model import Models
from app.Config.DataBase.database import engine, SessionLocal

Models.Base.metadata.create_all(bind=engine)


class Schedule:
    def __init__(self):
        self.db = SessionLocal()

    def getSchedule(self, uuid):
        try:
            data = self.db.query(Models.Schedule).filter(Models.Schedule.uuid == uuid).first()
            data = data.__dict__
            data.pop('_sa_instance_state', None)
        finally:
            self.db.close()
        return data

    def setSchedule(self, uuid, cron_schedule):
        try:
            data = self.db.query(Models.Schedule).filter(Models.Schedule.uuid == uuid).first()
            if data.__str__() == 'None':
                self.db.add(Models.Schedule(uuid=uuid, cron_schedule=cron_schedule))
            else :
                self.db.query(Models.Schedule).filter(Models.Schedule.uuid == uuid).update({'cron_schedule': cron_schedule})
            self.db.commit()
        except:
            self.db.close()
            return False
        finally:
            self.db.close()