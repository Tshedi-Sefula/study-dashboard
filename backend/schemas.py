'''Pydantic schemas'''
from pydantic import BaseModel, ConfigDict
from typing import List, Optional
from datetime import date, datetime
import enum


class ActivityType(str, enum.Enum):
    lesson_completed = "lesson_completed"
    quiz_attempted = "quiz_attempted"
    note_added = "note_added"


class ActivityBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    student_id: str
    activity_type: ActivityType
    score: Optional[int] = Field(default=None, ge=0, le=100)
    last_changed: date
    created_at: datetime


class Activity(ActivityBase):
    model_config = ConfigDict(from_attributes=True)


class StudentBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    student_id: str
    fname: str
    lname: str
    last_changed: date


class Student(StudentBase):
    model_config = ConfigDict(from_attributes=True)
    activities: List[ActivityBase] = []


class StudyGroupBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    group_name: str
    last_changed: date


class StudyGroup(StudyGroupBase):
    model_config = ConfigDict(from_attributes=True)
    students: List[StudentBase] = []

class Counts(BaseModel):
    group_count: int
    student_count: int
    activity_count: int
