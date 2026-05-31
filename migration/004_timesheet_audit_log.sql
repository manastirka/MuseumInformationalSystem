-- Migration: Add Audit Logging for Timesheet Changes
-- Date: 2026-02-03
-- Purpose: Track all changes to timesheets for compliance and debugging

-- ============================================================================
-- 1. CREATE AUDIT LOG TABLE
-- ============================================================================

CREATE TABLE IF NOT EXISTS timesheet_audit_log (
    id SERIAL PRIMARY KEY,
    report_id INTEGER,  -- Can be NULL if report was deleted
    action VARCHAR(20) NOT NULL CHECK (action IN ('INSERT', 'UPDATE', 'DELETE', 'VERIFY', 'LOCK', 'UNLOCK')),
    changed_by VARCHAR(255),  -- Email or system identifier
    changed_at TIMESTAMPTZ DEFAULT now(),
    old_values JSONB,  -- Previous state (for UPDATE/DELETE)
    new_values JSONB,  -- New state (for INSERT/UPDATE)
    change_summary TEXT,  -- Human-readable description
    ip_address VARCHAR(45),  -- IPv4 or IPv6
    user_agent TEXT
);

-- ============================================================================
-- 2. CREATE INDEXES
-- ============================================================================

CREATE INDEX IF NOT EXISTS idx_audit_log_report
ON timesheet_audit_log(report_id);

CREATE INDEX IF NOT EXISTS idx_audit_log_action
ON timesheet_audit_log(action);

CREATE INDEX IF NOT EXISTS idx_audit_log_changed_at
ON timesheet_audit_log(changed_at DESC);

CREATE INDEX IF NOT EXISTS idx_audit_log_changed_by
ON timesheet_audit_log(changed_by);

-- Composite index for common queries
CREATE INDEX IF NOT EXISTS idx_audit_log_report_time
ON timesheet_audit_log(report_id, changed_at DESC);

-- ============================================================================
-- 3. CREATE AUDIT TRIGGER FUNCTION
-- ============================================================================

CREATE OR REPLACE FUNCTION timesheet_audit_trigger()
RETURNS TRIGGER AS $$
DECLARE
    audit_action VARCHAR(20);
    old_json JSONB := NULL;
    new_json JSONB := NULL;
    summary TEXT;
BEGIN
    -- Determine action and prepare data
    IF TG_OP = 'INSERT' THEN
        audit_action := 'INSERT';
        new_json := to_jsonb(NEW);
        summary := format('Created timesheet for %s (%s/%s)',
                         NEW.employee_name,
                         NEW.month,
                         NEW.year);

    ELSIF TG_OP = 'UPDATE' THEN
        -- Detect specific action types
        IF OLD.is_verified = FALSE AND NEW.is_verified = TRUE THEN
            audit_action := 'VERIFY';
            summary := format('Verified by %s', COALESCE(NEW.verified_by, 'unknown'));
        ELSIF OLD.is_locked = FALSE AND NEW.is_locked = TRUE THEN
            audit_action := 'LOCK';
            summary := 'Locked for editing';
        ELSIF OLD.is_locked = TRUE AND NEW.is_locked = FALSE THEN
            audit_action := 'UNLOCK';
            summary := 'Unlocked for editing';
        ELSE
            audit_action := 'UPDATE';
            summary := format('Updated timesheet (version %s -> %s)',
                            COALESCE(OLD.version, 1),
                            COALESCE(NEW.version, 1));
        END IF;

        old_json := to_jsonb(OLD);
        new_json := to_jsonb(NEW);

    ELSIF TG_OP = 'DELETE' THEN
        audit_action := 'DELETE';
        old_json := to_jsonb(OLD);
        summary := format('Deleted timesheet for %s (%s/%s)',
                         OLD.employee_name,
                         OLD.month,
                         OLD.year);
    END IF;

    -- Insert audit record
    INSERT INTO timesheet_audit_log (
        report_id,
        action,
        changed_by,
        old_values,
        new_values,
        change_summary
    ) VALUES (
        COALESCE(NEW.id, OLD.id),
        audit_action,
        COALESCE(NEW.verified_by, NEW.employee_email, OLD.employee_email, 'system'),
        old_json,
        new_json,
        summary
    );

    -- Return appropriate value
    IF TG_OP = 'DELETE' THEN
        RETURN OLD;
    ELSE
        RETURN NEW;
    END IF;
END;
$$ LANGUAGE plpgsql;

-- ============================================================================
-- 4. CREATE TRIGGER
-- ============================================================================

DROP TRIGGER IF EXISTS timesheet_reports_audit ON timesheet_reports;

CREATE TRIGGER timesheet_reports_audit
    AFTER INSERT OR UPDATE OR DELETE ON timesheet_reports
    FOR EACH ROW
    EXECUTE FUNCTION timesheet_audit_trigger();

-- ============================================================================
-- 5. CREATE VIEW FOR COMMON QUERIES
-- ============================================================================

CREATE OR REPLACE VIEW timesheet_audit_summary AS
SELECT
    tal.id,
    tal.report_id,
    tal.action,
    tal.changed_by,
    tal.changed_at,
    tal.change_summary,
    tr.employee_name,
    tr.month,
    tr.year
FROM timesheet_audit_log tal
LEFT JOIN timesheet_reports tr ON tr.id = tal.report_id
ORDER BY tal.changed_at DESC;

-- ============================================================================
-- 6. ADD COMMENTS
-- ============================================================================

COMMENT ON TABLE timesheet_audit_log IS 'Audit trail for all timesheet changes';
COMMENT ON COLUMN timesheet_audit_log.action IS 'Type of action: INSERT, UPDATE, DELETE, VERIFY, LOCK, UNLOCK';
COMMENT ON COLUMN timesheet_audit_log.old_values IS 'Previous state as JSON (for UPDATE/DELETE)';
COMMENT ON COLUMN timesheet_audit_log.new_values IS 'New state as JSON (for INSERT/UPDATE)';
COMMENT ON VIEW timesheet_audit_summary IS 'Human-readable audit log with employee details';

-- ============================================================================
-- 7. VERIFICATION
-- ============================================================================

DO $$
DECLARE
    table_exists BOOLEAN;
    trigger_exists BOOLEAN;
BEGIN
    SELECT EXISTS (
        SELECT FROM information_schema.tables
        WHERE table_name = 'timesheet_audit_log'
    ) INTO table_exists;

    SELECT EXISTS (
        SELECT FROM pg_trigger
        WHERE tgname = 'timesheet_reports_audit'
    ) INTO trigger_exists;

    IF table_exists AND trigger_exists THEN
        RAISE NOTICE '===========================================';
        RAISE NOTICE 'Migration 004 completed successfully!';
        RAISE NOTICE '===========================================';
        RAISE NOTICE 'Created:';
        RAISE NOTICE '  - timesheet_audit_log table';
        RAISE NOTICE '  - timesheet_reports_audit trigger';
        RAISE NOTICE '  - timesheet_audit_summary view';
        RAISE NOTICE '';
        RAISE NOTICE 'All timesheet changes will now be logged.';
        RAISE NOTICE '===========================================';
    ELSE
        RAISE WARNING 'Migration may not have completed correctly';
    END IF;
END $$;
