# SQLAlchemy Query Helpers
from sqlalchemy import Column, ForeignKey, Integer, String, Float, Date, Identity, Text, DateTime, Enum, CheckConstraint, TIMESTAMP
import enum
from sqlalchemy.orm import Session
from sqlalchemy.orm import joinedload
from datetime import date
from sqlalchemy import func
import models


def get_student(db: Session, student_id: Text):
    return db.query(models.Student).filter(
        models.Student.student_id == student_id).first()


def get_students(db: Session, skip: int = 0, limit: int = 100,
                 min_last_changed_date: date = None,
                 max_last_changed_date: date = None,
                 last_name: Text = None, first_name: Text = None):
    query = db.query(models.Student)
    if min_last_changed_date:
        query = query.filter(models.Student.last_changed >= min_last_changed_date)
    if max_last_changed_date:
        query = query.filter(models.Student.last_changed <= max_last_changed_date)
    if first_name:
        query = query.filter(models.Student.fname == first_name)
    if last_name:
        query = query.filter(models.Student.lname == last_name)

    return query.offset(skip).limit(limit).all()


def get_group(db: Session, group_id: int = None):
    return db.query(models.StudyGroup).filter(
        models.StudyGroup.id == group_id).first()


def get_groups(db: Session, skip: int = 0, limit: int = 100,
               min_last_changed_date: date = None,
               max_last_changed_date: date = None,
               group_name: Text = None,
               id: int=None
               ):
    query = db.query(models.StudyGroup
                     ).options(joinedload(models.StudyGroup.students))
    if min_last_changed_date:
        query = query.filter(models.StudyGroup.last_changed >= min_last_changed_date)
    if max_last_changed_date:
        query = query.filter(models.StudyGroup.last_changed <= max_last_changed_date)
    if id is not None:
        query = query.filter(models.StudyGroup.id == id)
    if group_name:
        query = query.filter(models.StudyGroup.group_name == group_name)

    return query.offset(skip).limit(limit).all()


def get_activity(db: Session, id: int = None):
    return db.query(models.Activity).filter(
        models.Activity.id == id).first()

# note, one can get all activities in general or all Id's belonging to a student
def get_activities(db: Session, student_id: Text = None, skip: int = 0, limit: int = 100,
                   min_last_changed_date: date = None,
                   max_last_changed_date: date = None,
                   score: int = None,
                   created_at: date = None,
                   activity_type: models.ActivityType = None):
    query = db.query(models.Activity
                     ).options(joinedload(models.Activity.student))
    if min_last_changed_date:
        query = query.filter(models.Activity.last_changed >= min_last_changed_date)
    if max_last_changed_date:
        query = query.filter(models.Activity.last_changed <= max_last_changed_date)
    if created_at:
        query = query.filter(models.Activity.created_at == created_at)
    if activity_type:
        query = query.filter(models.Activity.activity_type == activity_type)
    if student_id:
        query = query.filter(models.Activity.student_id == student_id)

    return query.order_by(models.Activity.created_at.desc()).offset(skip).limit(limit).all()


# analytics queries
def get_student_count(db: Session):
   query = db.query(models.Student)
   return query.count()


def get_group_count(db: Session):
   query = db.query(models.StudyGroup)
   return query.count()


def get_activity_count(db: Session, student_id: Text=None, activity: models.ActivityType=None):
   query = db.query(models.Activity
                     ).options(joinedload(models.Activity.student))
   if student_id:
        query = query.filter(models.Activity.student_id == student_id, )
   if activity:
        query = query.filter(models.Activity.activity_type==activity,)

   return query.count()
   

def get_average_score(db: Session, student_id: str = None):
    query = db.query(func.avg(models.Activity.score)).filter(
        models.Activity.activity_type == ActivityType.quiz_attempted
    )
    if student_id:
        query = query.filter(models.Activity.student_id == student_id)
    
    result = query.scalar()  # scalar() returns a single value, not a list
    return round(result, 2) if result is not None else None

def get_group_stats(db: Session, group_id: int):
    total = db.query(func.count(models.Activity.id))\
        .join(models.Student)\
        .filter(models.Student.study_group_id == group_id)\
        .scalar()

    avg = db.query(func.avg(models.Activity.score))\
        .join(models.Student)\
        .filter(
            models.Student.study_group_id == group_id,
            models.Activity.activity_type == models.ActivityType.quiz_attempted
        ).scalar()

    return {
        "group_id": group_id,
        "total_activities": total or 0,
        "average_quiz_score": round(avg, 2) if avg else None
    }

def create_activity(db: Session, student_id: str, activity: schemas.ActivityCreate):
    db_activity = models.Activity(
        student_id=student_id,
        activity_type=activity.activity_type,
        score=activity.score,
        last_changed=activity.last_changed,
    )
    db.add(db_activity)
    db.commit()
    db.refresh(db_activity)
    return db_activity


def get_student_stats_by_group(db: Session, group_id: int):
    students = (
        db.query(models.Student)
        .filter(models.Student.study_group_id == group_id)
        .all()
    )

    results = []

    for s in students:
        total = get_activity_count(db, student_id=s.student_id)

        avg = get_average_score(db, student_id=s.student_id)

        last = (
            db.query(func.max(models.Activity.last_changed))
            .filter(models.Activity.student_id == s.student_id)
            .scalar()
        )

        results.append({
            "student_id": s.student_id,
            "fname": s.fname,
            "lname": s.lname,
            "total_activities": total,
            "avg_quiz_score": avg,
            "last_active": last,
        })

    return results