-- 2026-04-17: 24-hour temporary edit window after a timesheet is rejected
-- or has its verification revoked. NULL means "no temporary window — the
-- is_locked flag alone decides whether the employee may edit".
--
-- On reject/unapprove: is_locked is set FALSE and editable_until is set
-- to NOW() + INTERVAL '24 hours'. Employee edit endpoints must refuse the
-- edit when editable_until IS NOT NULL AND NOW() >= editable_until.
--
-- Safe to run multiple times.
ALTER TABLE timesheet_reports
  ADD COLUMN IF NOT EXISTS editable_until TIMESTAMPTZ;
