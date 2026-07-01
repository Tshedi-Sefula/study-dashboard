"""Testing FastAPI endpoints"""
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


# ─────────────────────────────────────────────
# Health check
# ─────────────────────────────────────────────

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "API health check successful"}


# ─────────────────────────────────────────────
# /groups/{group_id}/students
# ─────────────────────────────────────────────

def test_read_group():
    response = client.get("/groups/1/students")
    assert response.status_code == 200
    assert response.json().get("id") == 1
    assert response.json().get("group_name") == "Algebra Fundamentals"

def test_read_group_students():
    response = client.get("/groups/1/students")
    assert response.status_code == 200
    assert len(response.json().get("students")) == 5  # seed has 5 students

def test_read_group_not_found():
    response = client.get("/groups/9999/students")
    assert response.status_code == 404
    assert response.json().get("detail") == "Unknown student/group"


# ─────────────────────────────────────────────
# /students/{student_id}/activities
# ─────────────────────────────────────────────

def test_read_activities():
    response = client.get("/students/u10000001/activities")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_read_activities_newest_first():
    response = client.get("/students/u10000001/activities")
    assert response.status_code == 200
    activities = response.json()
    if len(activities) > 1:
        # verify descending order by created_at
        assert activities[0]["created_at"] >= activities[1]["created_at"]

def test_read_activities_pagination():
    response = client.get("/students/u10000001/activities?offset=0&limit=2")
    assert response.status_code == 200
    assert len(response.json()) <= 2

def test_read_activities_type_filter():
    response = client.get("/students/u10000001/activities?type=quiz_attempted")
    assert response.status_code == 200
    activities = response.json()
    for activity in activities:
        assert activity.get("activity_type") == "quiz_attempted"

def test_read_activities_quiz_have_scores():
    response = client.get("/students/u10000001/activities?type=quiz_attempted")
    assert response.status_code == 200
    for activity in response.json():
        assert activity.get("score") is not None
        assert 0 <= activity.get("score") <= 100

def test_read_activities_student_not_found():
    response = client.get("/students/u99999999/activities")
    assert response.status_code == 200
    assert response.json() == []  # returns empty list, not 404


# ─────────────────────────────────────────────
# /groups/{group_id}/stats
# ─────────────────────────────────────────────

def test_read_stats():
    response = client.get("/groups/1/stats")
    assert response.status_code == 200
    data = response.json()
    assert data.get("group_id") == 1
    assert data.get("total_activities") >= 50  # use >= since POST tests add activities
    assert data.get("average_quiz_score") is not None

def test_read_stats_score_range():
    response = client.get("/groups/1/stats")
    assert response.status_code == 200
    avg = response.json().get("average_quiz_score")
    if avg is not None:
        assert 0 <= avg <= 100

def test_read_stats_not_found():
    response = client.get("/groups/9999/stats")
    assert response.status_code == 404
    assert response.json().get("detail") == "Unknown student/group"


# ─────────────────────────────────────────────
# POST /students/{student_id}/activities
# ─────────────────────────────────────────────

def test_post_activity():
    from datetime import date
    payload = {
        "activity_type": "lesson_completed",
        "score": None,
        "last_changed": str(date.today())
    }
    response = client.post("/students/u10000001/activities", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data.get("activity_type") == "lesson_completed"
    assert data.get("student_id") == "u10000001"
    assert data.get("score") is None

def test_post_quiz_activity_with_score():
    from datetime import date
    payload = {
        "activity_type": "quiz_attempted",
        "score": 85,
        "last_changed": str(date.today())
    }
    response = client.post("/students/u10000001/activities", json=payload)
    assert response.status_code == 201
    assert response.json().get("score") == 85

def test_post_activity_student_not_found():
    from datetime import date
    payload = {
        "activity_type": "note_added",
        "score": None,
        "last_changed": str(date.today())
    }
    response = client.post("/students/u99999999/activities", json=payload)
    assert response.status_code == 404