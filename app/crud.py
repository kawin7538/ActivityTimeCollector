from sqlalchemy.orm import Session

from . import models, schemas

def get_activity(db: Session, activity_id: int):
    return db.query(models.Activity).filter(models.Activity.activity_id == activity_id).first()

def get_activities(db: Session):
    return db.query(models.Activity).all()

def create_activity(db: Session, activity: schemas.ActivityCreate):
    db_activity = models.Activity(activity_name=activity.activity_name,activity_time=activity.activity_time)
    db.add(db_activity)
    db.commit()
    db.refresh(db_activity)
    return db_activity

def delete_activity(db: Session, activity_id: int):
    db.query(models.Activity).filter(models.Activity.activity_id == activity_id).delete()
    return db.commit()