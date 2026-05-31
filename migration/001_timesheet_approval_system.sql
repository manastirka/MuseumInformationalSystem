-- Migration: Add Approval System to Timesheet
-- Date: 2026-01-09
-- Purpose: Add approval workflow, verification, and edit request tracking

-- ============================================================================
-- 1. ADD COLUMNS TO timesheet_reports
-- ============================================================================

-- Add verification/approval columns
ALTER TABLE timesheet_reports
ADD COLUMN IF NOT EXISTS is_verified BOOLEAN DEFAULT FALSE;

ALTER TABLE timesheet_reports
ADD COLUMN IF NOT EXISTS verified_by VARCHAR(255);

ALTER TABLE timesheet_reports
ADD COLUMN IF NOT EXISTS verified_at TIMESTAMP;

ALTER TABLE timesheet_reports
ADD COLUMN IF NOT EXISTS is_locked BOOLEAN DEFAULT FALSE;

-- Add work description fields (if not exist)
ALTER TABLE timesheet_reports
ADD COLUMN IF NOT EXISTS extraordinary_tasks TEXT;

ALTER TABLE timesheet_reports
ADD COLUMN IF NOT EXISTS duties_summary TEXT;

-- Add signature fields
ALTER TABLE timesheet_reports
ADD COLUMN IF NOT EXISTS employee_signature VARCHAR(255);

ALTER TABLE timesheet_reports
ADD COLUMN IF NOT EXISTS supervisor_signature VARCHAR(255);

ALTER TABLE timesheet_reports
ADD COLUMN IF NOT EXISTS director_signature VARCHAR(255);

-- Add legacy compatibility
ALTER TABLE timesheet_reports
ADD COLUMN IF NOT EXISTS legacy_radna_lista_id INTEGER;

COMMENT ON COLUMN timesheet_reports.is_verified IS 'Whether the report has been verified/approved by admin';
COMMENT ON COLUMN timesheet_reports.verified_by IS 'Email of admin who verified the report';
COMMENT ON COLUMN timesheet_reports.verified_at IS 'Timestamp when report was verified';
COMMENT ON COLUMN timesheet_reports.is_locked IS 'Whether the report is locked for editing';

-- ============================================================================
-- 2. CREATE timesheet_edit_requests TABLE
-- ============================================================================

CREATE TABLE IF NOT EXISTS timesheet_edit_requests (
    id SERIAL PRIMARY KEY,
    report_id INTEGER NOT NULL REFERENCES timesheet_reports(id) ON DELETE CASCADE,
    requester_email VARCHAR(255) NOT NULL,
    reason TEXT NOT NULL,
    status VARCHAR(20) DEFAULT 'pending',
    requested_at TIMESTAMP DEFAULT NOW(),
    processed_at TIMESTAMP,
    processed_by VARCHAR(255),
    notes TEXT,

    CONSTRAINT valid_status CHECK (status IN ('pending', 'approved', 'rejected'))
);

CREATE INDEX IF NOT EXISTS idx_edit_requests_report
ON timesheet_edit_requests(report_id);

CREATE INDEX IF NOT EXISTS idx_edit_requests_status
ON timesheet_edit_requests(status);

CREATE INDEX IF NOT EXISTS idx_edit_requests_requester
ON timesheet_edit_requests(requester_email);

COMMENT ON TABLE timesheet_edit_requests IS 'Tracks edit requests for locked/verified timesheets';
COMMENT ON COLUMN timesheet_edit_requests.status IS 'Request status: pending, approved, or rejected';

-- ============================================================================
-- 3. ADD INDEXES FOR PERFORMANCE
-- ============================================================================

CREATE INDEX IF NOT EXISTS idx_timesheet_reports_verified
ON timesheet_reports(is_verified);

CREATE INDEX IF NOT EXISTS idx_timesheet_reports_locked
ON timesheet_reports(is_locked);

CREATE INDEX IF NOT EXISTS idx_timesheet_reports_verified_by
ON timesheet_reports(verified_by);

-- ============================================================================
-- 4. UPDATE EXISTING DATA
-- ============================================================================

-- Set default values for existing reports
UPDATE timesheet_reports
SET is_verified = FALSE, is_locked = FALSE
WHERE is_verified IS NULL OR is_locked IS NULL;

-- ============================================================================
-- 5. VERIFICATION
-- ============================================================================

-- Check that columns exist
DO $$
BEGIN
    IF EXISTS (
        SELECT 1 FROM information_schema.columns
        WHERE table_name = 'timesheet_reports'
        AND column_name = 'is_verified'
    ) THEN
        RAISE NOTICE '✓ is_verified column added successfully';
    END IF;

    IF EXISTS (
        SELECT 1 FROM information_schema.tables
        WHERE table_name = 'timesheet_edit_requests'
    ) THEN
        RAISE NOTICE '✓ timesheet_edit_requests table created successfully';
    END IF;
END $$;

-- ============================================================================
-- MIGRATION COMPLETE
-- ============================================================================

SELECT '========================================' as message
UNION ALL
SELECT 'Timesheet Approval System Migration Complete!'
UNION ALL
SELECT '========================================'
UNION ALL
SELECT 'New columns added to timesheet_reports:'
UNION ALL
SELECT '  - is_verified, verified_by, verified_at, is_locked'
UNION ALL
SELECT '  - extraordinary_tasks, duties_summary'
UNION ALL
SELECT '  - employee_signature, supervisor_signature, director_signature'
UNION ALL
SELECT ''
UNION ALL
SELECT 'New table created:'
UNION ALL
SELECT '  - timesheet_edit_requests'
UNION ALL
SELECT ''
UNION ALL
SELECT 'Indexes created for performance'
UNION ALL
SELECT '========================================';
