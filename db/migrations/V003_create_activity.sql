CREATE TYPE activity_type AS ENUM (
    'lesson_completed',
    'quiz_attempted',
    'note_added'
);

CREATE TABLE activity (
    id         SERIAL         PRIMARY KEY,
    student_id TEXT           NOT NULL REFERENCES student(student_id) ON DELETE CASCADE,
    type       activity_type  NOT NULL,
    score      INTEGER        CHECK (score BETWEEN 0 AND 100),
    last_changed DATE NOT NULL,
    created_at TIMESTAMPTZ    NOT NULL DEFAULT now(),

    CONSTRAINT score_only_on_quiz CHECK (
        (type = 'quiz_attempted' AND score IS NOT NULL)
        OR
        (type <> 'quiz_attempted' AND score IS NULL)
    )
);