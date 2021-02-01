from pydantic import BaseModel

from typing import Optional

class ActivityBase(BaseModel):
    activity_id : int
    activity_name : str
    activity_time : Optional[float] = 0

class ActivityCreate(ActivityBase):
    pass

class Activity(ActivityBase):
    class Config:
        orm_mode=True
