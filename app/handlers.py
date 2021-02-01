from typing import List

from fastapi import FastAPI, Depends, HTTPException, Request, Response
from sqlalchemy.orm import Session

import logging

from . import models, schemas, crud
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app=FastAPI(title="Activity Time Collector")

@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    response = Response("Internal server error", status_code=500)
    try:
        request.state.db = SessionLocal()
        response = await call_next(request)
    finally:
        request.state.db.close()
    return response

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def main():
    return "This is the first page"

@app.post("/activities/", response_model=schemas.Activity)
def create_activity(activity: schemas.ActivityCreate, db: Session = Depends(get_db)):
    return crud.create_activity(db=db, activity=activity)

@app.get("/activities/", response_model=List[schemas.Activity])
def read_activities(db: Session = Depends(get_db)):
    activities = crud.get_activities(db)
    return activities