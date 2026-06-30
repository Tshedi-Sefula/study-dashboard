"""
BagLearn Seed Data Populator
Run: python seed.py
Seeds: 1 study group, 5 students, ~50 activities over the last 14 days
"""

import os
import random
from datetime import date, datetime, timedelta, timezone
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, StudyGroup, Student, Activity, ActivityType

load_dotenv()

# ─────────────────────────────────────────────
# Database connection
# ─────────────────────────────────────────────
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

# ─────────────────────────────────────────────
# Seed data definitions
# ─────────────────────────────────────────────
STUDY_GROUP = {
    "group_name": "Algebra Fundamentals",
    "last_changed": date.today(),
}

STUDENTS = [
    {"student_id": "u10000001", "fname": "Amara",   "lname": "Nkosi"},
    {"student_id": "u10000002", "fname": "Sipho",   "lname": "Dlamini"},
    {"student_id": "u10000003", "fname": "Lerato",  "lname": "Mokoena"},
    {"student_id": "u10000004", "fname": "Thabo",   "lname": "Sithole"},
    {"student_id": "u10000005", "fname": "Zanele",  "lname": "Khumalo"},
]

# Weighted activity types — quizzes ~40%, lessons ~40%, notes ~20%
ACTIVITY_WEIGHTS = [
    (ActivityType.quiz_attempted,   0.40),
    (ActivityType.lesson_completed, 0.40),
    (ActivityType.note_added,       0.20),
]


def weighted_choice(choices):
    """Pick an ActivityType based on weights."""
    types, weights = zip(*choices)
    return random.choices(types, weights=weights, k=1)[0]


def random_timestamp(days_ago_max: int = 14) -> datetime:
    """Random timestamp within the last N days."""
    offset_days = random.uniform(0, days_ago_max)
    offset_hours = random.uniform(0, 23)
    return datetime.now(timezone.utc) - timedelta(days=offset_days, hours=offset_hours)


def make_activity(student_id: str) -> dict:
    """Build a single activity row."""
    activity_type = weighted_choice(ACTIVITY_WEIGHTS)
    score = None
    if activity_type == ActivityType.quiz_attempted:
        # Occasionally (10% of quizzes) leave score null to test constraint robustness
        # — remove the `if random.random() > 0.1` if you want 100% quiz coverage
        score = random.randint(30, 100)

    return {
        "student_id":   student_id,
        "activity_type": activity_type,
        "score":         score,
        "last_changed":  date.today(),
        "created_at":    random_timestamp(),
    }


# ─────────────────────────────────────────────
# Main seeder
# ─────────────────────────────────────────────
def seed():
    db = SessionLocal()
    try:
        # ── 1. Guard: don't double-seed ──────────────────
        if db.query(StudyGroup).count() > 0:
            print("Database already seeded — skipping.")
            return

        print("Seeding database...")

        # ── 2. Study group ────────────────────────────────
        group = StudyGroup(**STUDY_GROUP)
        db.add(group)
        db.flush()  # get group.id before committing
        print(f"  ✓ Study group: '{group.group_name}' (id={group.id})")

        # ── 3. Students ───────────────────────────────────
        students = []
        for s in STUDENTS:
            student = Student(
                student_id=s["student_id"],
                fname=s["fname"],
                lname=s["lname"],
                last_changed=date.today(),
                study_group_id=group.id,
            )
            db.add(student)
            students.append(student)
        db.flush()
        print(f"  ✓ {len(students)} students added")

        # ── 4. Activities (~50, distributed across students)
        target = 50
        activity_count = 0
        student_ids = [s["student_id"] for s in STUDENTS]

        # Give each student at least 5 activities, then distribute the rest randomly
        per_student = 5
        guaranteed = per_student * len(student_ids)  # 25
        remainder = target - guaranteed               # 25

        for student_id in student_ids:
            for _ in range(per_student):
                row = make_activity(student_id)
                db.add(Activity(
                    student_id=student_id,
                    activity_type=row["activity_type"],
                    score=row["score"],
                    last_changed=row["last_changed"],
                    created_at=row["created_at"],
                ))
                activity_count += 1

        for _ in range(remainder):
            student_id = random.choice(student_ids)
            row = make_activity(student_id)
            db.add(Activity(
                student_id=student_id,
                activity_type=row["activity_type"],
                score=row["score"],
                last_changed=row["last_changed"],
                created_at=row["created_at"],
            ))
            activity_count += 1

        db.commit()
        print(f"  ✓ {activity_count} activities added")
        print("\nDone. Database seeded successfully.")

    except Exception as e:
        db.rollback()
        print(f"\nError during seeding: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed()