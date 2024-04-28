from sqlalchemy import Column, String, Text, INT, DateTime, CHAR
from app.Config.DataBase.database import Base


class Video(Base):
    __tablename__ = "video"

    id = Column(INT, primary_key=True, index=True, nullable=False, autoincrement=True)
    uuid = Column(String(255), index=True, nullable=False)
    uploadId = Column(String(255), index=True)
    gptTitle = Column(String(255), index=True, nullable=False)
    title = Column(String(255), index=True)
    content = Column(Text)
    tags = Column(Text)
    createdAt = Column(DateTime, index=True, nullable=False)
    uploadAt = Column(DateTime, index=True, nullable=False)
    isDeleted = Column(CHAR(1), index=True, nullable=False, default='N')
    deletedAt = Column(DateTime)


class Prompt(Base):
    __tablename__ = "prompt"

    uuid = Column(String(255), primary_key=True, index=True)
    content = Column(Text)


class Schedule(Base):
    __tablename__ = "schedule"

    uuid = Column(String(255), primary_key=True, index=True)
    cron_schedule = Column(String(255))
