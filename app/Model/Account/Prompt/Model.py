from sqlalchemy import Column, String, Text
from app.Config.database import Base

class Prompt(Base):
    __tablename__ = "prompt"

    uuid = Column(String(255), primary_key=True, index=True)
    content = Column(Text)
