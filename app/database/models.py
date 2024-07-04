from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.sql import func
from database.db import Base
from datetime import datetime

class Advert(Base):
    __tablename__ = 'adverts'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    farpost_id = Column(Integer, nullable=False)
    author = Column(String, nullable=False)
    views = Column(Integer, nullable=True)
    position = Column(Integer, nullable=False)
    gathered_at = Column(DateTime(timezone=True), server_default=func.now())