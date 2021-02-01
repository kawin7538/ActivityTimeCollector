from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float, Sequence
from sqlalchemy.orm import relationship

from .database import Base

ACTIVITY_ID=Sequence('activity_id_seq',start=0)

class Activity(Base):
    __tablename__ = 'activity'

    activity_id = Column(Integer,autoincrement=True,primary_key=True,index=True)
    activity_name = Column(String)
    activity_time = Column(Float,default=0)
