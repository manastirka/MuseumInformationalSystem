-- Migration: Fix Timesheet Schema Inconsistencies
-- Date: 2026-02-03
-- Purpose: Add missing columns, add optimistic locking, fix schema-code mismatches

-- ============================================================================
-- 1. ADD MISSING COLUMNS TO timesheet_reports
-- ============================================================================

-- Add employee_email for user lookup (code expects this)
ALTER TABLE timesheet_reports
ADD COLUMN IF NOT EXISTS employee_email VARCHAR(255);

-- Add updated_at for change tracking
ALTER TABLE timesheet_reports
ADD COLUMN IF NOT EXISTS updated_at TIMESTAMPTZ DEFAULT now();

-- Add special_tasks as alias for extraordinary_tasks if code uses it
-- (keeping extraordinary_tasks for backward compatibility)
ALTER TABLE timesheet_reports
ADD COLUMN IF NOT EXISTS special_tasks TEXT;

-- Add version column for optimistic locking (concurrent modification protection)
ALTER TABLE timesheet_reports
ADD COLUMN IF NOT EXISTS version INTEGER DEFAULT 1;

-- ============================================================================
-- 2. CREATE INDEXES FOR NEW COLUMNS
-- ============================================================================

CREATE INDEX IF NOT EXISTS idx_timesheet_reports_email
ON timesheet_reports(employee_email);

CREATE INDEX IF NOT EXISTS idx_timesheet_reports_employee_period
ON timesheet_reports(employee_email, year, month);

-- ============================================================================
-- 3. SYNC EXISTING DATA
-- ============================================================================

-- Copy extraordinary_tasks to special_tasks where null
UPDATE timesheet_reports
SET special_tasks = extraordinary_tasks
WHERE special_tasks IS NULL AND extraordinary_tasks IS NOT NULL;

-- Set default version for existing records
UPDATE timesheet_reports
SET version = 1
WHERE version IS NULL;

-- ============================================================================
-- 4. ADD FUNCTION FOR VERSION INCREMENT
-- ============================================================================

-- Function to auto-increment version on update
CREATE OR REPLACE FUNCTION timesheet_reports_version_trigger()
RETURNS TRIGGER AS $$
BEGIN
    -- Only increment if version wasn't explicitly set in the UPDATE
    IF NEW.version = OLD.version THEN
        NEW.version := OLD.version + 1;
    END IF;
    NEW.updated_at := now();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Create trigger for version auto-increment
DROP TRIGGER IF EXISTS timesheet_reports_version_update ON timesheet_reports;

CREATE TRIGGER timesheet_reports_version_update
    BEFORE UPDATE ON timesheet_reports
    FOR EACH ROW
    EXECUTE FUNCTION timesheet_reports_version_trigger();

-- ============================================================================
-- 5. ADD CONSTRAINT COMMENTS
-- ============================================================================

COMMENT ON COLUMN timesheet_reports.employee_email IS 'Employee email for user lookup';
COMMENT ON COLUMN timesheet_reports.updated_at IS 'Last modification timestamp';
COMMENT ON COLUMN timesheet_reports.special_tasks IS 'Special tasks description (alias for extraordinary_tasks)';
COMMENT ON COLUMN timesheet_reports.version IS 'Optimistic locking version - increments on each update';

-- ============================================================================
-- 6. VERIFICATION
-- ============================================================================

DO $$
DECLARE
    col_count INTEGER;
BEGIN
    SELECT COUNT(*) INTO col_count
    FROM information_schema.columns
    WHERE table_name = 'timesheet_reports'
    AND column_name IN ('employee_email', 'updated_at', 'special_tasks', 'version');

    IF col_count = 4 THEN
        RAISE NOTICE '===========================================';
        RAISE NOTICE 'Migration 002 completed successfully!';
        RAISE NOTICE '===========================================';
        RAISE NOTICE 'Added columns:';
        RAISE NOTICE '  - employee_email (user lookup)';
        RAISE NOTICE '  - updated_at (change tracking)';
        RAISE NOTICE '  - special_tasks (work description)';
        RAISE NOTICE '  - version (optimistic locking)';
        RAISE NOTICE '';
        RAISE NOTICE 'Added triggers:';
        RAISE NOTICE '  - timesheet_reports_version_update';
        RAISE NOTICE '===========================================';
    ELSE
        RAISE NOTICE 'WARNING: Some columns may not have been added. Count: %', col_count;
    END IF;
END $$;
