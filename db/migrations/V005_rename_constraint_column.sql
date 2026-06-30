ALTER TABLE activity
DROP CONSTRAINT score_only_on_quiz;

ALTER TABLE activity
ADD CONSTRAINT score_only_on_quiz CHECK (
    (activity_type = 'quiz_attempted' AND score IS NOT NULL)
    OR
    (activity_type <> 'quiz_attempted' AND score IS NULL)
);
