# SQLAlchemy models
from sqlalchemy import Column, ForeignKey, Integer, String, Float, Date, Identity, Text, DateTime, Enum, CheckConstraint
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from database import Base
import enum

class StudyGroup(Base):
    __tablename__ = "study_group"

    id = Column(Integer, primary_key=True, index=True)
    last_changed = Column(Date, nullable=False)
    group_name = Column(Text, nullable=False)

    # One to Many Relationship with Students
    students = relationship("Student", back_populates="group")

class Student(Base):
    __tablename__ = "student"

    student_id = Column(Text, primary_key=True, index=True)
    fname = Column(Text, nullable=False)
    lname = Column(Text, nullable=False)
    last_changed = Column(Date, nullable=False)

    study_group_id = Column(
        Integer,
        ForeignKey("study_group.id", ondelete="SET NULL"),
        nullable=True
        )

    # Many to One Relationship with StudyGroup
    group = relationship("StudyGroup", back_populates="students")
   
    # One to Many Relationship with Activity
    activities = relationship("Activity", back_populates="student")

class ActivityType(str, enum.Enum):
    lesson_completed = "lesson_completed"
    quiz_attempted = "quiz_attempted"
    note_added = "note_added"


class Activity(Base):
    __tablename__= "activity"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(
        Text, 
        ForeignKey("student.student_id", ondelete="CASCADE"), 
        nullable=False, 
        )
    activity_type = Column(
        Enum(ActivityType, name="activity_type", create_type=False),
        nullable=False,
    )
    score = Column(Integer, CheckConstraint("score BETWEEN 0 AND 100"))
    last_changed = Column(Date, nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())

    __table_args__ = (
        CheckConstraint(
            "(activity_type = 'quiz_attempted' AND score IS NOT NULL) OR "
            "(activity_type <> 'quiz_attempted' AND score IS NULL)",
            name="score_only_on_quiz",
        ),
    )

    # Many to One Relationship with Student
    student = relationship("Student", back_populates="activities")