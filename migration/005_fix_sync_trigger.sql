-- Migration: Fix Sync Trigger for DELETE operations
-- Date: 2026-02-03
-- Purpose: Handle CASCADE delete properly in sync trigger

-- ============================================================================
-- 1. UPDATE SYNC FUNCTION TO HANDLE MISSING REPORTS
-- ============================================================================

CREATE OR REPLACE FUNCTION sync_timesheet_entries(p_report_id INTEGER)
RETURNS VOID AS $$
BEGIN
    -- Check if report still exists (important for CASCADE deletes)
    IF NOT EXISTS (SELECT 1 FROM timesheet_reports WHERE id = p_report_id) THEN
        -- Report was deleted, just clean up any orphaned entries
        DELETE FROM timesheet_entries WHERE report_id = p_report_id;
        RETURN;
    END IF;

    -- Delete existing entries for this report
    DELETE FROM timesheet_entries WHERE report_id = p_report_id;

    -- Insert aggregated categories from daily data
    INSERT INTO timesheet_entries (report_id, category, hours)
    SELECT
        p_report_id,
        'rad_na_mestu',
        COALESCE(SUM(work_in_museum), 0)
    FROM timesheet_report_days
    WHERE report_id = p_report_id
    HAVING SUM(work_in_museum) > 0;

    INSERT INTO timesheet_entries (report_id, category, hours)
    SELECT
        p_report_id,
        'van_muzeja',
        COALESCE(SUM(work_outside), 0)
    FROM timesheet_report_days
    WHERE report_id = p_report_id
    HAVING SUM(work_outside) > 0;

    INSERT INTO timesheet_entries (report_id, category, hours)
    SELECT
        p_report_id,
        'godisnji_odmor',
        COALESCE(SUM(vacation), 0)
    FROM timesheet_report_days
    WHERE report_id = p_report_id
    HAVING SUM(vacation) > 0;

    INSERT INTO timesheet_entries (report_id, category, hours)
    SELECT
        p_report_id,
        'drzavni_praznik',
        COALESCE(SUM(public_holiday), 0)
    FROM timesheet_report_days
    WHERE report_id = p_report_id
    HAVING SUM(public_holiday) > 0;

    INSERT INTO timesheet_entries (report_id, category, hours)
    SELECT
        p_report_id,
        'placeno_odsustvo',
        COALESCE(SUM(paid_leave), 0)
    FROM timesheet_report_days
    WHERE report_id = p_report_id
    HAVING SUM(paid_leave) > 0;

    INSERT INTO timesheet_entries (report_id, category, hours)
    SELECT
        p_report_id,
        'ostalo_odsustvo',
        COALESCE(SUM(other_leave), 0)
    FROM timesheet_report_days
    WHERE report_id = p_report_id
    HAVING SUM(other_leave) > 0;

    INSERT INTO timesheet_entries (report_id, category, hours)
    SELECT
        p_report_id,
        'bolovanje_manje_30',
        COALESCE(SUM(sick_leave_lt30), 0)
    FROM timesheet_report_days
    WHERE report_id = p_report_id
    HAVING SUM(sick_leave_lt30) > 0;

    INSERT INTO timesheet_entries (report_id, category, hours)
    SELECT
        p_report_id,
        'bolovanje_vece_30',
        COALESCE(SUM(sick_leave_gte30), 0)
    FROM timesheet_report_days
    WHERE report_id = p_report_id
    HAVING SUM(sick_leave_gte30) > 0;
END;
$$ LANGUAGE plpgsql;

-- ============================================================================
-- 2. UPDATE TRIGGER TO SKIP SYNC ON DELETE IF CASCADE WILL HANDLE IT
-- ============================================================================

CREATE OR REPLACE FUNCTION trigger_sync_timesheet_entries()
RETURNS TRIGGER AS $$
BEGIN
    -- For DELETE operations, check if the report still exists
    -- CASCADE delete on timesheet_reports will clean up entries automatically
    IF TG_OP = 'DELETE' THEN
        -- Only sync if report still exists (not a cascade delete)
        IF EXISTS (SELECT 1 FROM timesheet_reports WHERE id = OLD.report_id) THEN
            PERFORM sync_timesheet_entries(OLD.report_id);
        END IF;
        RETURN OLD;
    ELSE
        PERFORM sync_timesheet_entries(NEW.report_id);
        RETURN NEW;
    END IF;
END;
$$ LANGUAGE plpgsql;

-- ============================================================================
-- 3. VERIFICATION
-- ============================================================================

DO $$
BEGIN
    RAISE NOTICE '===========================================';
    RAISE NOTICE 'Migration 003 completed successfully!';
    RAISE NOTICE '===========================================';
    RAISE NOTICE 'Updated sync_timesheet_entries() to handle';
    RAISE NOTICE 'CASCADE deletes properly.';
    RAISE NOTICE '===========================================';
END $$;
