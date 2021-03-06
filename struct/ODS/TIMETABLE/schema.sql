CREATE SCHEMA ODS_TIMETABLE;

CREATE ROLE ODS_TIMETABLE_R;
CREATE ROLE ODS_TIMETABLE_W;
CREATE ROLE ODS_TIMETABLE_A;


GRANT USAGE ON SCHEMA ODS_TIMETABLE TO ODS_TIMETABLE_R, ODS_TIMETABLE_W;
GRANT CREATE, USAGE ON SCHEMA ODS_TIMETABLE TO ODS_TIMETABLE_A;

GRANT SELECT ON SCHEMA ODS_TIMETABLE TO ODS_TIMETABLE_R;
GRANT UPDATE, DELETE, TRUNCATE, INSERT ON SCHEMA ODS_TIMETABLE TO ODS_TIMETABLE_W;
GRANT CREATE, SELECT, INSERT, UPDATE, TRUNCATE, DELETE, REFERENCES ON SCHEMA ODS_TIMETABLE TO ODS_TIMETABLE_A;
GRANT ALTER, DROP ON SCHEMA ODS_TIMETABLE TO ODS_TIMETABLE_A;
