-- Migration 013: add is_department_head flag to employee_profiles so a
-- department head can verify timesheets for employees in their own
-- `department`.
--
-- Context:
--   db/schema_phase3a.sql now declares this column on fresh installs, but
--   the deployed table never received it (schema drift). Any code path
--   that reads or writes is_department_head will crash with
--   `psycopg.errors.UndefinedColumn` until this migration runs.
--
-- Safe to run repeatedly (IF NOT EXISTS) and reversible (see rollback).

ALTER TABLE employee_profiles
    ADD COLUMN IF NOT EXISTS is_department_head BOOLEAN NOT NULL DEFAULT FALSE;

-- Rollback (only if you must revert):
--   ALTER TABLE employee_profiles DROP COLUMN IF EXISTS is_department_head;
