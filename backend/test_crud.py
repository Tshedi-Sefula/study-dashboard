"""Testing SQLAlchemy Helper Functions"""
import pytest
from datetime import date
import crud
import models
from database import SessionRemote

# use a test date to test the min_last_changed_date
test_date = date(2025, 1, 1)

@pytest.fixture(scope="function")
def db_session():
    """Starts a database session and closes it when done"""
    session = SessionRemote()
    yield session
    session.close()


# ─────────────────────────────────────────────
# StudyGroup tests
# ─────────────────────────────────────────────

def test_get_group(db_session):
    """Tests you can get a single study group by id"""
    group = crud.get_group(db_session, group_id=1)
    assert group.id == 1

def test_get_groups(db_session):
    """Tests that the count of study groups is what is expected"""
    groups = crud.get_groups(db_session, skip=0, limit=100)
    assert len(groups) == 1  # brief specifies 1 study group in seed data

def test_get_groups_by_name(db_session):
    groups = crud.get_groups(db_session, group_name="Algebra Fundamentals")
    assert len(groups) == 1
    assert groups[0].group_name == "Algebra Fundamentals"

def test_get_groups_by_min_date(db_session):
    """Tests filtering study groups by min last changed date"""
    groups = crud.get_groups(db_session, skip=0, limit=100,
                             min_last_changed_date=test_date)
    assert len(groups) >= 0  # update count to match your seed data


# ─────────────────────────────────────────────
# Student tests
# ─────────────────────────────────────────────


def test_get_students(db_session):
    """Tests that the count of students is what is expected"""
    students = crud.get_students(db_session, skip=0, limit=100)
    assert len(students) == 5  # brief specifies 5 students in seed data

def test_get_student(db_session):
    student = crud.get_student(db_session, student_id="u10000001")
    assert student.student_id == "u10000001"

def test_get_students_by_first_name(db_session):
    students = crud.get_students(db_session, first_name="Amara")
    assert len(students) == 1
    assert students[0].fname == "Amara"

def test_get_students_by_last_name(db_session):
    students = crud.get_students(db_session, last_name="Nkosi")
    assert len(students) >= 1
    assert students[0].lname == "Nkosi"



def test_get_students_by_date(db_session):
    """Tests filtering students by min last changed date"""
    students = crud.get_students(db_session, skip=0, limit=100,
                                 min_last_changed_date=test_date)
    assert len(students) >= 0  # update count to match your seed data


# ─────────────────────────────────────────────
# Activity tests
# ─────────────────────────────────────────────

def test_get_activity(db_session):
    """Tests you can get a single activity by id"""
    activity = crud.get_activity(db_session, id=1)
    assert activity.id == 1

def test_get_activities(db_session):
    """Tests that the count of activities is what is expected"""
    activities = crud.get_activities(db_session, skip=0, limit=1000)
    assert len(activities) == 50  # brief specifies ~50 activities in seed data

def test_get_activities_by_type(db_session):
    """Tests filtering activities by type"""
    activities = crud.get_activities(db_session, skip=0, limit=1000,
                                     activity_type=models.ActivityType.quiz_attempted)
    assert len(activities) >= 1
    for activity in activities:
        assert activity.activity_type == models.ActivityType.quiz_attempted

def test_get_activities_quiz_have_scores(db_session):
    """Tests that all quiz_attempted activities have a score"""
    activities = crud.get_activities(db_session, skip=0, limit=1000,
                                     activity_type=models.ActivityType.quiz_attempted)
    for activity in activities:
        assert activity.score is not None
        assert 0 <= activity.score <= 100

def test_get_activities_non_quiz_no_scores(db_session):
    """Tests that non quiz activities have no score"""
    for activity_type in [models.ActivityType.lesson_completed,
                          models.ActivityType.note_added]:
        activities = crud.get_activities(db_session, skip=0, limit=1000,
                                         activity_type=activity_type)
        for activity in activities:
            assert activity.score is None

def test_get_activities_by_date(db_session):
    """Tests filtering activities by min last changed date"""
    activities = crud.get_activities(db_session, skip=0, limit=1000,
                                     min_last_changed_date=test_date)
    assert len(activities) >= 0  # update count to match your seed data