from typing import List

from fastapi import FastAPI, Depends, HTTPException, Request, Response, Form
from fastapi.responses import HTMLResponse, RedirectResponse
# from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

import logging

from . import models, schemas, crud
from .database import SessionLocal, engine
# from .schemas import as_form

models.Base.metadata.create_all(bind=engine)

app=FastAPI(title="Activity Time Collector")

templates = Jinja2Templates(directory='templates')

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
async def main():
    return "This is the first page"

@app.post("/add_activity", response_model=schemas.Activity)
async def create_activity(request: Request, activity_id: int = Form(...), activity_name: str = Form(...), activity_time: float = Form(...), db: Session = Depends(get_db)):
    # print(activity_name,activity_time)
    print(activity_id,activity_name,activity_time)
    activity=schemas.ActivityCreate(activity_id=activity_id,activity_name=activity_name,activity_time=activity_time)
    crud.create_activity(db=db, activity=activity)
    return RedirectResponse("/activities",status_code=303)

@app.get("/activities", response_model=List[schemas.Activity], response_class=HTMLResponse)
async def read_activities(request: Request,db: Session = Depends(get_db)):
    activities = crud.get_activities(db)
    data={
        'activities':activities,
        'tid':5,
    }
    # return activities
    return templates.TemplateResponse('activities.html',{"request": request,'data':data})