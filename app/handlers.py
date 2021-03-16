from typing import List

from fastapi import FastAPI, Depends, HTTPException, Request, Response, Form, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse, RedirectResponse
# from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

import logging

from . import models, schemas, crud
from .database import SessionLocal, engine
# from ml_models.utility import split_transformer_func
# from ml_models import *
# from pythainlp import word_vector,word_tokenize
# from pythainlp.ulmfit import process_thai
from datetime import datetime
# from .schemas import as_form

models.Base.metadata.create_all(bind=engine)

app=FastAPI(title="Activity Time Collector")

templates = Jinja2Templates(directory='templates')

# model_loader=ModelLoader()

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

@app.get("/",response_class=HTMLResponse)
async def main(request: Request):
    # return "This is the first page"
    # meta_dict=model_loader.get_meta()
    meta_dict={}
    return templates.TemplateResponse('mainpage.html',{"request": request,"meta_dict":meta_dict})

@app.get('/implement',response_class=HTMLResponse)
async def implement(request: Request):
    return templates.TemplateResponse('implementation_page.html',{'request':request})

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

@app.post("/delete_activity/{activity_id}",response_model=schemas.Activity)
async def delete_activity(request: Request, activity_id:int ,db: Session = Depends(get_db)):
    crud.get_activity(db,activity_id)
    crud.delete_activity(db,activity_id)
    # return {"detail": "Question deleted", "status_code": 204}
    return RedirectResponse("/activities",status_code=303)

# @app.websocket("/ws")
# async def websocket_endpoint(websocket: WebSocket):
#     await websocket.accept()
#     try:
#         while True:
#             data = await websocket.receive_text()
#             time1=datetime.now()
#             answer = model_loader.predict(data)
#             time2=datetime.now()
#             time_diff=time2-time1
#             print(time_diff.total_seconds())
#             # await websocket.send_text(f"Message text was: {answer}")
#             await websocket.send_json({'answer':answer,"time_elapsed":time_diff.total_seconds()})
#     except WebSocketDisconnect:
#         print("Web Socket Disconnect")
