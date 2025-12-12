-- messaging_app/db/init.sql
-- Custom database initialization if needed
SET GLOBAL sql_mode=(SELECT REPLACE(@@sql_mode,'ONLY_FULL_GROUP_BY',''));
