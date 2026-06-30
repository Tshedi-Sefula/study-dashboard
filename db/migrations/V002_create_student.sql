CREATE TABLE student (
    student_id     TEXT     PRIMARY KEY,
    fname          TEXT     NOT NULL,
    lname          TEXT     NOT NULL,
    last_changed   DATE     NOT NULL, -- This allows my API to query most recently updated
    -- Last Changed allows me to data pipeline only data that has been changed
    study_group_id INTEGER  REFERENCES study_group(id) ON DELETE SET NULL
);