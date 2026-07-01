'''Pydantic schemas'''
from pydantic import BaseModel, ConfigDict, Field, model_validator
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

    @model_validator(mode="after")
    def check_score_matches_type(self):
        if self.activity_type == ActivityType.quiz_attempted and self.score is None:
            raise ValueError("score is required for quiz_attempted")
        if self.activity_type != ActivityType.quiz_attempted and self.score is not None:
            raise ValueError("score must be null for non-quiz activities")
        return self


class Activity(ActivityBase):
    model_config = ConfigDict(from_attributes=True)
    
class ActivityCreate(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    activity_type: ActivityType
    score: Optional[int] = Field(default=None, ge=0, le=100)
    last_changed: date


class StudentBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    student_id: str
    fname: str
    lname: str
    last_changed: date


class Student(StudentBase):
    model_config = ConfigDict(from_attributes=True)
    activities: List[Activity] = []


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


class GroupStats(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    group_id: int
    total_activities: int
    average_quiz_score: Optional[float] = None