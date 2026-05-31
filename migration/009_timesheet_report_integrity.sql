-- Migration 009: integrity constraints for monthly timesheet reports
--
-- Context (2026-05-29 monthly-report pipeline audit):
--   * timesheet_reports has no uniqueness on (employee, month, year), so
--     duplicate monthly reports can exist; save/load resolve by that key and a
--     duplicate makes the wrong row exportable.
--   * timesheet_report_days hour columns are NUMERIC(4,2) with no bound, so a
--     migration / legacy import / direct SQL can store negative or >24 values
--     that the application-level validation would otherwise reject.
--
-- Apply AFTER de-duplicating any existing rows (see the dedupe query below);
-- the unique indexes will fail to build if duplicates remain.

-- 1) Uniqueness for the (employee, month, year) lookup key.
--    Split on whether employee_email is present (the load path prefers email).
CREATE UNIQUE INDEX IF NOT EXISTS uq_timesheet_reports_email_month_year
    ON timesheet_reports (LOWER(employee_email), month, year)
    WHERE employee_email IS NOT NULL;

CREATE UNIQUE INDEX IF NOT EXISTS uq_timesheet_reports_name_month_year
    ON timesheet_reports (employee_name, month, year)
    WHERE employee_email IS NULL;

-- 2) Non-negativity / max-24 bounds on each daily hour column.
--    NOT VALID enforces the rule on new/updated rows without rejecting any
--    pre-existing out-of-range data; run VALIDATE CONSTRAINT after cleanup.
ALTER TABLE timesheet_report_days
    ADD CONSTRAINT chk_report_days_hours_range CHECK (
        work_in_museum   >= 0 AND work_in_museum   <= 24 AND
        work_outside     >= 0 AND work_outside     <= 24 AND
        vacation         >= 0 AND vacation         <= 24 AND
        public_holiday   >= 0 AND public_holiday   <= 24 AND
        paid_leave       >= 0 AND paid_leave       <= 24 AND
        other_leave      >= 0 AND other_leave      <= 24 AND
        sick_leave_lt30  >= 0 AND sick_leave_lt30  <= 24 AND
        sick_leave_gte30 >= 0 AND sick_leave_gte30 <= 24
    ) NOT VALID;

-- Helper: find duplicate monthly reports before creating the unique indexes.
--   SELECT LOWER(employee_email) AS e, month, year, COUNT(*), array_agg(id)
--   FROM timesheet_reports WHERE employee_email IS NOT NULL
--   GROUP BY 1,2,3 HAVING COUNT(*) > 1;
--
-- After cleaning out-of-range day values:
--   ALTER TABLE timesheet_report_days VALIDATE CONSTRAINT chk_report_days_hours_range;

-- Rollback:
--   DROP INDEX IF EXISTS uq_timesheet_reports_email_month_year;
--   DROP INDEX IF EXISTS uq_timesheet_reports_name_month_year;
--   ALTER TABLE timesheet_report_days DROP CONSTRAINT IF EXISTS chk_report_days_hours_range;
