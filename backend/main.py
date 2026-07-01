''' FastAPI program '''
from fastapi import Depends, FastAPI, HTTPException, Query
from sqlalchemy.orm import Session
from datetime import date, datetime 

import crud, schemas
from database import SessionRemote

app = FastAPI() # create the object

# Dependency
def get_db():
    db = SessionRemote()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
async def root():
    return {"message": "API health check successful"}

@app.get("/groups/{group_id}/students", response_model=schemas.StudyGroup)
def read_group(group_id: int, db: Session = Depends(get_db)):
    group = crud.get_group(db, group_id=group_id)
    if group is None:
        raise HTTPException(status_code=404, detail="Unknown student/group")
    return group


@app.get("/students/{student_id}/activities", response_model=list[schemas.Activity])
def get_activities(
        student_id: str,
        skip: int = Query(default=0, alias="offset"),
        limit: int = 100,
        activity_type: schemas.ActivityType = Query(default=None, alias="type"),
        min_last_changed_date: date = None,
        max_last_changed_date: date = None,
        db: Session = Depends(get_db)
        ):
    activities = crud.get_activities(
        db,
        student_id=student_id,
        skip=skip,
        limit=limit,
        activity_type=activity_type,
        min_last_changed_date=min_last_changed_date,
        max_last_changed_date=max_last_changed_date
    )
    if student_id is None:
        raise HTTPException(status_code=404, detail="Unknown student/group")
    
    return activities

@app.get("/groups/{group_id}/stats", response_model=schemas.GroupStats)
def get_stats(group_id: int, db: Session = Depends(get_db)):
    group = crud.get_group(db, group_id=group_id)
    if group is None:
        raise HTTPException(status_code=404, detail="Unknown student/group")
    return crud.get_group_stats(db, group_id=group_id)

@app.post("/students/{student_id}/activities", response_model=schemas.Activity, status_code=201)
def post_activity(
        student_id: str,
        activity: schemas.ActivityCreate,
        db: Session = Depends(get_db)
        ):
    student = crud.get_student(db, student_id=student_id)
    if student is None:
        raise HTTPException(status_code=404, detail="Unknown student/group")
    return crud.create_activity(db, student_id=student_id, activity=activity)