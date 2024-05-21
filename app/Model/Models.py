from sqlalchemy import Column, Text, INT, DateTime, CHAR, VARCHAR, text
from Config.DataBase.database import Base


class Login(Base):
    __tablename__ = "login"

    uuid = Column(VARCHAR(255), primary_key=True, index=True, nullable=False)
    socialType = Column(INT, index=True, nullable=False)
    accessToken = Column(Text, nullable=False)
    refreshToken = Column(Text, nullable=False)
    idToken = Column(Text, nullable=False)
    expiresIn = Column(INT, nullable=False)
    scope = Column(Text, nullable=False)
    expireAt = Column(DateTime, index=True, nullable=False)
    updatedAt = Column(DateTime, index=True, nullable=False, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))


class User(Base):
    __tablename__ = "user"

    uuid = Column(VARCHAR(255), primary_key=True, index=True, nullable=False)
    socialType = Column(INT, index=True, nullable=False)
    email = Column(VARCHAR(255), index=True, nullable=False)
    name = Column(VARCHAR(255), nullable=False)
    trial = Column(CHAR(1), nullable=False, default='Y')
    trialCount = Column(INT, nullable=False, default='1')
    createdAt = Column(DateTime, nullable=False, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))
    updatedAt = Column(DateTime, nullable=True)


class Video(Base):
    __tablename__ = "video"

    id = Column(INT, primary_key=True, index=True, nullable=False, autoincrement=True)
    uuid = Column(VARCHAR(255), index=True, nullable=False)
    uploadId = Column(VARCHAR(255), index=True, nullable=True)
    gptTitle = Column(VARCHAR(255), index=True, nullable=False)
    title = Column(VARCHAR(255), index=True, nullable=True)
    content = Column(Text, nullable=True)
    tags = Column(Text, nullable=True)
    createdAt = Column(DateTime, index=True, nullable=False)
    uploadAt = Column(DateTime, index=True, nullable=True)
    isDeleted = Column(CHAR(1), index=True, nullable=False, default='N')
    deletedAt = Column(DateTime, nullable=True)


class Prompt(Base):
    __tablename__ = "prompt"

    uuid = Column(VARCHAR(255), primary_key=True, index=True, nullable=False)
    content = Column(Text, nullable=True)


class Schedule(Base):
    __tablename__ = "schedule"

    uuid = Column(VARCHAR(255), primary_key=True, index=True, nullable=False)
    cronSchedule = Column(VARCHAR(255), nullable=True)
