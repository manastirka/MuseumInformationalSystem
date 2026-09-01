-- Migration 006: Timesheet Status Workflow
-- Adds status workflow columns to timesheet_reports and creates status history table.

-- (BEGIN/COMMIT uklonjeni 2026-09-01: transakciju vodi deploy/run_migrations.py,
--  koji sve pending fajlove primenjuje u jednoj transakciji; sadržaj nepromenjen)

-- 1. Add status workflow columns to timesheet_reports
ALTER TABLE timesheet_reports
    ADD COLUMN IF NOT EXISTS status VARCHAR(20) DEFAULT 'DRAFT'
        CHECK (status IN ('DRAFT', 'SUBMITTED', 'APPROVED', 'REJECTED'));

ALTER TABLE timesheet_reports
    ADD COLUMN IF NOT EXISTS submitted_at TIMESTAMPTZ;

ALTER TABLE timesheet_reports
    ADD COLUMN IF NOT EXISTS reviewed_at TIMESTAMPTZ;

ALTER TABLE timesheet_reports
    ADD COLUMN IF NOT EXISTS reviewed_by_email VARCHAR(255);

ALTER TABLE timesheet_reports
    ADD COLUMN IF NOT EXISTS rejection_note TEXT;

-- 2. Create timesheet_status_history table
CREATE TABLE IF NOT EXISTS timesheet_status_history (
    id SERIAL PRIMARY KEY,
    report_id INTEGER REFERENCES timesheet_reports(id) ON DELETE CASCADE,
    old_status VARCHAR(20),
    new_status VARCHAR(20) NOT NULL,
    changed_by VARCHAR(255) NOT NULL,
    changed_at TIMESTAMPTZ DEFAULT NOW(),
    note TEXT
);

-- 3. Backfill existing data
UPDATE timesheet_reports
SET status = 'APPROVED'
WHERE is_verified = TRUE AND is_locked = TRUE AND status = 'DRAFT';

UPDATE timesheet_reports
SET status = 'SUBMITTED'
WHERE is_locked = TRUE AND is_verified = FALSE AND status = 'DRAFT';

-- 4. Add index on status column
CREATE INDEX IF NOT EXISTS idx_timesheet_reports_status
    ON timesheet_reports(status);

-- 5. Add index on timesheet_status_history(report_id)
CREATE INDEX IF NOT EXISTS idx_timesheet_status_history_report_id
    ON timesheet_status_history(report_id);

