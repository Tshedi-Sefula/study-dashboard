''' FastAPI program '''
from fastapi import Depends, FastAPI, HTTPException
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

@app.get("/groups/{group_id}/students", response_model=StudyGroup)
def read_group( db: Session = Depends(get_db), group_name: str=None, id: int=None):
    groups = crud.get_groups(db, group_name=group_name, id=group_id)
    if group is None:
        raise HTTPException(status_code=404, detail="Group not found")
    return groups

@app.get("/students/{student_id}/activities", response_model=list[schemas.Activity])
def get_activities(
    id: int=None, 
    student_id: str=None, 
    created_at: datetime=None, 
    skip: int=Query(default=0, alias="offset"),
    limit: int=100,
    activity: schemas.ActivityType=Query(default=None, alias="type"),
    min_last_changed_date: date=None,
    max_last_changed_date: date=None,
    ):
    activies = crud.get_groups(db,id=id,
         student_id=student_id,
         created_at=created_at,
         skip=skip,
         limit=limit,
         activity=activity_type)
    return activities




