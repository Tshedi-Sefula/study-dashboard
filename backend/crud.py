# SQLAlchemy Query Helpers
from sqlalchemy import Column, ForeignKey, Integer, String, Float, Date, Identity, Text, DateTime, Enum, CheckConstraint, TIMESTAMP
import enum
from sqlalchemy.orm import Session
from sqlalchemy.orm import joinedload
from datetime import date
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
    if group_name:
        query = query.filter(models.StudyGroup.id == id)
    if id:
        query = query.filter(models.StudyGroup.group_name == group_name)

    return query.offset(skip).limit(limit).all()


def get_activity(db: Session, id: int = None):
    return db.query(models.Activity).filter(
        models.Activity.id == id).first()

# note, one can get all activities in general or all Id's belonging to a student
def get_activities(db: Session, student_id: Text = None, skip: int = 0, limit: int = 100,
                    student_id:Text = None,
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

    return query.offset(skip).limit(limit).all()

# analytics queries
def get_student_count(db: Session):
   query = db.query(models.Student)
   return query.count()


def get_group_count(db: Session):
   query = db.query(models.StudyGroup)
   return query.count()


def get_activity_count(db: Session, student_id: Text=None):
   query = db.query(models.Activity
                     ).options(joinedload(models.Activity.student))
   if student_id:
        query = query.filter(models.Activity.student_id == student_id)

   return query.count()

