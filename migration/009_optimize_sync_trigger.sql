-- Migration: Optimize Sync Trigger for Better Performance
-- Date: 2026-02-03
-- Purpose: Use statement-level trigger instead of row-level for bulk operations

-- ============================================================================
-- 1. CREATE OPTIMIZED SYNC FUNCTION
-- ============================================================================

-- This function processes all affected report_ids in a single call
CREATE OR REPLACE FUNCTION sync_timesheet_entries_batch(report_ids INTEGER[])
RETURNS VOID AS $$
DECLARE
    rid INTEGER;
BEGIN
    FOREACH rid IN ARRAY report_ids
    LOOP
        -- Skip if report doesn't exist (cascade delete scenario)
        IF NOT EXISTS (SELECT 1 FROM timesheet_reports WHERE id = rid) THEN
            DELETE FROM timesheet_entries WHERE report_id = rid;
            CONTINUE;
        END IF;

        -- Delete existing entries for this report
        DELETE FROM timesheet_entries WHERE report_id = rid;

        -- Insert aggregated categories in a single statement
        INSERT INTO timesheet_entries (report_id, category, hours)
        SELECT
            rid,
            category,
            total_hours
        FROM (
            SELECT 'rad_na_mestu'::TEXT as category, COALESCE(SUM(work_in_museum), 0) as total_hours
            FROM timesheet_report_days WHERE report_id = rid
            UNION ALL
            SELECT 'van_muzeja', COALESCE(SUM(work_outside), 0)
            FROM timesheet_report_days WHERE report_id = rid
            UNION ALL
            SELECT 'godisnji_odmor', COALESCE(SUM(vacation), 0)
            FROM timesheet_report_days WHERE report_id = rid
            UNION ALL
            SELECT 'drzavni_praznik', COALESCE(SUM(public_holiday), 0)
            FROM timesheet_report_days WHERE report_id = rid
            UNION ALL
            SELECT 'placeno_odsustvo', COALESCE(SUM(paid_leave), 0)
            FROM timesheet_report_days WHERE report_id = rid
            UNION ALL
            SELECT 'ostalo_odsustvo', COALESCE(SUM(other_leave), 0)
            FROM timesheet_report_days WHERE report_id = rid
            UNION ALL
            SELECT 'bolovanje_manje_30', COALESCE(SUM(sick_leave_lt30), 0)
            FROM timesheet_report_days WHERE report_id = rid
            UNION ALL
            SELECT 'bolovanje_vece_30', COALESCE(SUM(sick_leave_gte30), 0)
            FROM timesheet_report_days WHERE report_id = rid
        ) AS categories
        WHERE total_hours > 0;
    END LOOP;
END;
$$ LANGUAGE plpgsql;

-- ============================================================================
-- 2. CREATE STATEMENT-LEVEL TRIGGER FUNCTION
-- ============================================================================

-- Statement-level trigger that collects all affected report_ids
CREATE OR REPLACE FUNCTION trigger_sync_timesheet_entries_statement()
RETURNS TRIGGER AS $$
DECLARE
    affected_ids INTEGER[];
BEGIN
    -- Collect unique report_ids from transition tables
    IF TG_OP = 'INSERT' OR TG_OP = 'UPDATE' THEN
        SELECT ARRAY_AGG(DISTINCT report_id) INTO affected_ids
        FROM new_table;
    END IF;

    IF TG_OP = 'DELETE' OR TG_OP = 'UPDATE' THEN
        IF affected_ids IS NULL THEN
            SELECT ARRAY_AGG(DISTINCT report_id) INTO affected_ids
            FROM old_table;
        ELSE
            -- Merge with old_table report_ids for UPDATE
            SELECT ARRAY_AGG(DISTINCT rid) INTO affected_ids
            FROM (
                SELECT UNNEST(affected_ids) AS rid
                UNION
                SELECT report_id FROM old_table
            ) AS combined;
        END IF;
    END IF;

    -- Process all affected reports in batch
    IF affected_ids IS NOT NULL AND array_length(affected_ids, 1) > 0 THEN
        PERFORM sync_timesheet_entries_batch(affected_ids);
    END IF;

    RETURN NULL;  -- Statement-level triggers return NULL
END;
$$ LANGUAGE plpgsql;

-- ============================================================================
-- 3. DROP OLD ROW-LEVEL TRIGGER
-- ============================================================================

DROP TRIGGER IF EXISTS timesheet_report_days_sync ON timesheet_report_days;

-- ============================================================================
-- 4. CREATE NEW STATEMENT-LEVEL TRIGGERS
-- ============================================================================

-- Separate triggers for INSERT, UPDATE, DELETE with transition tables
CREATE TRIGGER timesheet_report_days_sync_insert
    AFTER INSERT ON timesheet_report_days
    REFERENCING NEW TABLE AS new_table
    FOR EACH STATEMENT
    EXECUTE FUNCTION trigger_sync_timesheet_entries_statement();

CREATE TRIGGER timesheet_report_days_sync_update
    AFTER UPDATE ON timesheet_report_days
    REFERENCING OLD TABLE AS old_table NEW TABLE AS new_table
    FOR EACH STATEMENT
    EXECUTE FUNCTION trigger_sync_timesheet_entries_statement();

CREATE TRIGGER timesheet_report_days_sync_delete
    AFTER DELETE ON timesheet_report_days
    REFERENCING OLD TABLE AS old_table
    FOR EACH STATEMENT
    EXECUTE FUNCTION trigger_sync_timesheet_entries_statement();

-- ============================================================================
-- 5. VERIFICATION
-- ============================================================================

DO $$
DECLARE
    trigger_count INTEGER;
BEGIN
    SELECT COUNT(*) INTO trigger_count
    FROM pg_trigger
    WHERE tgname LIKE 'timesheet_report_days_sync%';

    IF trigger_count = 3 THEN
        RAISE NOTICE '===========================================';
        RAISE NOTICE 'Migration 005 completed successfully!';
        RAISE NOTICE '===========================================';
        RAISE NOTICE 'Optimized triggers:';
        RAISE NOTICE '  - Row-level trigger replaced with 3 statement-level triggers';
        RAISE NOTICE '  - INSERT, UPDATE, DELETE handled in batches';
        RAISE NOTICE '  - Performance improved for bulk operations';
        RAISE NOTICE '===========================================';
    ELSE
        RAISE WARNING 'Expected 3 triggers, found %', trigger_count;
    END IF;
END $$;
