-- 2026-04-17: audit column for timesheet_reports.
-- Records which role signed off a verification (admin / direktor /
-- sef_odeljenja / sef_pravne_sluzbe / sef_racunovodstva). Populated by the
-- approve/unapprove endpoints; NULL when the report has never been verified
-- or the verification has been revoked.
--
-- Safe to run multiple times.
ALTER TABLE timesheet_reports
  ADD COLUMN IF NOT EXISTS verified_role VARCHAR(64);
