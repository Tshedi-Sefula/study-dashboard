CREATE TABLE study_group (
    id   SERIAL  PRIMARY KEY,
    last_changed DATE   NOT NULL, -- Allows data retrieval of updated records
    group_name TEXT    NOT NULL
    
);
