-- Complete Timesheet Schema for PostgreSQL Migration
-- Phase 3E: Timesheet System (Sistem Radnih Lista)
-- Run with: psql postgresql://aleksandarlukovic@localhost:5432/museum_system -f db/schema_timesheet_complete.sql

-- ============================================================================
-- MAIN TABLES
-- ============================================================================

-- Main timesheet reports table (radna_lista)
CREATE TABLE IF NOT EXISTS timesheet_reports (
    id SERIAL PRIMARY KEY,
    legacy_radna_lista_id INTEGER UNIQUE,
    employee_name TEXT NOT NULL,
    month INTEGER NOT NULL CHECK (month BETWEEN 1 AND 12),
    year INTEGER NOT NULL,
    organization_unit TEXT,
    position TEXT,
    special_scope TEXT,
    extraordinary_tasks TEXT,
    employee_signature TEXT,
    approver TEXT,
    manager_signature TEXT,
    director_signature TEXT,
    salary_adjustment TEXT,
    duties_summary TEXT,
    created_at TIMESTAMPTZ DEFAULT now(),
    updated_at TIMESTAMPTZ DEFAULT now()
);

-- Daily timesheet entries per report (radna_lista_dan)
CREATE TABLE IF NOT EXISTS timesheet_report_days (
    id SERIAL PRIMARY KEY,
    report_id INTEGER NOT NULL REFERENCES timesheet_reports(id) ON DELETE CASCADE,
    day INTEGER NOT NULL CHECK (day BETWEEN 1 AND 31),
    work_in_museum NUMERIC(4,2) DEFAULT 0,
    work_outside NUMERIC(4,2) DEFAULT 0,
    vacation NUMERIC(4,2) DEFAULT 0,
    public_holiday NUMERIC(4,2) DEFAULT 0,
    paid_leave NUMERIC(4,2) DEFAULT 0,
    other_leave NUMERIC(4,2) DEFAULT 0,
    sick_leave_lt30 NUMERIC(4,2) DEFAULT 0,
    sick_leave_gte30 NUMERIC(4,2) DEFAULT 0,
    UNIQUE(report_id, day)
);

-- Category-based entries table (for repository queries)
-- This table stores aggregated hours by category for efficient querying
CREATE TABLE IF NOT EXISTS timesheet_entries (
    id SERIAL PRIMARY KEY,
    report_id INTEGER NOT NULL REFERENCES timesheet_reports(id) ON DELETE CASCADE,
    category TEXT NOT NULL CHECK (category IN (
        'rad_na_mestu',
        'van_muzeja',
        'godisnji_odmor',
        'drzavni_praznik',
        'placeno_odsustvo',
        'ostalo_odsustvo',
        'bolovanje_manje_30',
        'bolovanje_vece_30'
    )),
    hours NUMERIC(6,2) NOT NULL DEFAULT 0,
    created_at TIMESTAMPTZ DEFAULT now(),
    UNIQUE(report_id, category)
);

-- ============================================================================
-- INDEXES
-- ============================================================================

-- Timesheet reports indexes
CREATE INDEX IF NOT EXISTS idx_timesheet_reports_employee ON timesheet_reports(employee_name);
CREATE INDEX IF NOT EXISTS idx_timesheet_reports_period ON timesheet_reports(year, month);
CREATE INDEX IF NOT EXISTS idx_timesheet_reports_period_desc ON timesheet_reports(year DESC, month DESC);
CREATE INDEX IF NOT EXISTS idx_timesheet_reports_legacy ON timesheet_reports(legacy_radna_lista_id);

-- Report days indexes
CREATE INDEX IF NOT EXISTS idx_timesheet_report_days_report ON timesheet_report_days(report_id);
CREATE INDEX IF NOT EXISTS idx_timesheet_report_days_day ON timesheet_report_days(report_id, day);

-- Entries indexes
CREATE INDEX IF NOT EXISTS idx_timesheet_entries_report ON timesheet_entries(report_id);
CREATE INDEX IF NOT EXISTS idx_timesheet_entries_category ON timesheet_entries(category);
CREATE INDEX IF NOT EXISTS idx_timesheet_entries_report_category ON timesheet_entries(report_id, category);

-- ============================================================================
-- FUNCTIONS
-- ============================================================================

-- Function to sync timesheet_entries from timesheet_report_days
-- This aggregates daily hours by category for efficient querying
CREATE OR REPLACE FUNCTION sync_timesheet_entries(p_report_id INTEGER)
RETURNS VOID AS $$
BEGIN
    -- Delete existing entries for this report
    DELETE FROM timesheet_entries WHERE report_id = p_report_id;

    -- Insert aggregated categories from daily data
    INSERT INTO timesheet_entries (report_id, category, hours)
    SELECT
        p_report_id,
        'rad_na_mestu',
        COALESCE(SUM(work_in_museum), 0)
    FROM timesheet_report_days
    WHERE report_id = p_report_id AND work_in_museum > 0;

    INSERT INTO timesheet_entries (report_id, category, hours)
    SELECT
        p_report_id,
        'van_muzeja',
        COALESCE(SUM(work_outside), 0)
    FROM timesheet_report_days
    WHERE report_id = p_report_id AND work_outside > 0;

    INSERT INTO timesheet_entries (report_id, category, hours)
    SELECT
        p_report_id,
        'godisnji_odmor',
        COALESCE(SUM(vacation), 0)
    FROM timesheet_report_days
    WHERE report_id = p_report_id AND vacation > 0;

    INSERT INTO timesheet_entries (report_id, category, hours)
    SELECT
        p_report_id,
        'drzavni_praznik',
        COALESCE(SUM(public_holiday), 0)
    FROM timesheet_report_days
    WHERE report_id = p_report_id AND public_holiday > 0;

    INSERT INTO timesheet_entries (report_id, category, hours)
    SELECT
        p_report_id,
        'placeno_odsustvo',
        COALESCE(SUM(paid_leave), 0)
    FROM timesheet_report_days
    WHERE report_id = p_report_id AND paid_leave > 0;

    INSERT INTO timesheet_entries (report_id, category, hours)
    SELECT
        p_report_id,
        'ostalo_odsustvo',
        COALESCE(SUM(other_leave), 0)
    FROM timesheet_report_days
    WHERE report_id = p_report_id AND other_leave > 0;

    INSERT INTO timesheet_entries (report_id, category, hours)
    SELECT
        p_report_id,
        'bolovanje_manje_30',
        COALESCE(SUM(sick_leave_lt30), 0)
    FROM timesheet_report_days
    WHERE report_id = p_report_id AND sick_leave_lt30 > 0;

    INSERT INTO timesheet_entries (report_id, category, hours)
    SELECT
        p_report_id,
        'bolovanje_vece_30',
        COALESCE(SUM(sick_leave_gte30), 0)
    FROM timesheet_report_days
    WHERE report_id = p_report_id AND sick_leave_gte30 > 0;
END;
$$ LANGUAGE plpgsql;

-- Trigger function to automatically sync entries when days are modified
CREATE OR REPLACE FUNCTION trigger_sync_timesheet_entries()
RETURNS TRIGGER AS $$
BEGIN
    PERFORM sync_timesheet_entries(
        CASE
            WHEN TG_OP = 'DELETE' THEN OLD.report_id
            ELSE NEW.report_id
        END
    );
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Drop existing trigger if it exists
DROP TRIGGER IF EXISTS timesheet_report_days_sync ON timesheet_report_days;

-- Create trigger to auto-sync entries when daily data changes
CREATE TRIGGER timesheet_report_days_sync
    AFTER INSERT OR UPDATE OR DELETE ON timesheet_report_days
    FOR EACH ROW
    EXECUTE FUNCTION trigger_sync_timesheet_entries();

-- ============================================================================
-- VIEWS
-- ============================================================================

-- View for monthly summary statistics
CREATE OR REPLACE VIEW timesheet_monthly_summary AS
SELECT
    tr.year,
    tr.month,
    COUNT(DISTINCT tr.id) AS report_count,
    COUNT(DISTINCT tr.employee_name) AS employee_count,
    SUM(CASE WHEN te.category = 'rad_na_mestu' THEN te.hours ELSE 0 END) AS total_work_in_museum,
    SUM(CASE WHEN te.category = 'van_muzeja' THEN te.hours ELSE 0 END) AS total_work_outside,
    SUM(CASE WHEN te.category = 'godisnji_odmor' THEN te.hours ELSE 0 END) AS total_vacation,
    SUM(CASE WHEN te.category = 'drzavni_praznik' THEN te.hours ELSE 0 END) AS total_public_holiday,
    SUM(CASE WHEN te.category = 'placeno_odsustvo' THEN te.hours ELSE 0 END) AS total_paid_leave,
    SUM(CASE WHEN te.category = 'ostalo_odsustvo' THEN te.hours ELSE 0 END) AS total_other_leave,
    SUM(CASE WHEN te.category = 'bolovanje_manje_30' THEN te.hours ELSE 0 END) AS total_sick_lt30,
    SUM(CASE WHEN te.category = 'bolovanje_vece_30' THEN te.hours ELSE 0 END) AS total_sick_gte30,
    SUM(te.hours) AS total_hours
FROM timesheet_reports tr
LEFT JOIN timesheet_entries te ON te.report_id = tr.id
GROUP BY tr.year, tr.month
ORDER BY tr.year DESC, tr.month DESC;

-- View for employee timesheet summary
CREATE OR REPLACE VIEW timesheet_employee_summary AS
SELECT
    tr.employee_name,
    tr.year,
    tr.month,
    tr.organization_unit,
    tr.position,
    SUM(CASE WHEN te.category = 'rad_na_mestu' THEN te.hours ELSE 0 END) AS work_in_museum,
    SUM(CASE WHEN te.category = 'van_muzeja' THEN te.hours ELSE 0 END) AS work_outside,
    SUM(CASE WHEN te.category = 'godisnji_odmor' THEN te.hours ELSE 0 END) AS vacation,
    SUM(CASE WHEN te.category = 'drzavni_praznik' THEN te.hours ELSE 0 END) AS public_holiday,
    SUM(CASE WHEN te.category = 'placeno_odsustvo' THEN te.hours ELSE 0 END) AS paid_leave,
    SUM(CASE WHEN te.category = 'ostalo_odsustvo' THEN te.hours ELSE 0 END) AS other_leave,
    SUM(CASE WHEN te.category = 'bolovanje_manje_30' THEN te.hours ELSE 0 END) AS sick_lt30,
    SUM(CASE WHEN te.category = 'bolovanje_vece_30' THEN te.hours ELSE 0 END) AS sick_gte30,
    SUM(te.hours) AS total_hours
FROM timesheet_reports tr
LEFT JOIN timesheet_entries te ON te.report_id = tr.id
GROUP BY tr.employee_name, tr.year, tr.month, tr.organization_unit, tr.position
ORDER BY tr.year DESC, tr.month DESC, tr.employee_name;

-- View for category totals across all time
CREATE OR REPLACE VIEW timesheet_category_totals AS
SELECT
    category,
    COUNT(DISTINCT report_id) AS report_count,
    SUM(hours) AS total_hours,
    AVG(hours) AS avg_hours_per_report,
    MIN(hours) AS min_hours,
    MAX(hours) AS max_hours
FROM timesheet_entries
GROUP BY category
ORDER BY total_hours DESC;

-- ============================================================================
-- COMMENTS
-- ============================================================================

COMMENT ON TABLE timesheet_reports IS 'Employee monthly work reports (Radna Lista)';
COMMENT ON TABLE timesheet_report_days IS 'Daily breakdown of hours by category for each report';
COMMENT ON TABLE timesheet_entries IS 'Aggregated hours by category for efficient querying';

COMMENT ON VIEW timesheet_monthly_summary IS 'Monthly aggregated statistics across all employees';
COMMENT ON VIEW timesheet_employee_summary IS 'Employee-level monthly summaries';
COMMENT ON VIEW timesheet_category_totals IS 'Overall statistics by work category';

COMMENT ON FUNCTION sync_timesheet_entries(INTEGER) IS 'Synchronizes timesheet_entries from daily data for a specific report';
COMMENT ON FUNCTION trigger_sync_timesheet_entries() IS 'Trigger function to auto-sync entries when daily data changes';

-- ============================================================================
-- DISPLAY SUMMARY
-- ============================================================================

DO $$
DECLARE
    report_count INTEGER;
    day_count INTEGER;
    entry_count INTEGER;
BEGIN
    SELECT COUNT(*) INTO report_count FROM timesheet_reports;
    SELECT COUNT(*) INTO day_count FROM timesheet_report_days;
    SELECT COUNT(*) INTO entry_count FROM timesheet_entries;

    RAISE NOTICE '';
    RAISE NOTICE '=== Complete Timesheet Schema Created ===';
    RAISE NOTICE 'Tables:';
    RAISE NOTICE '  ✓ timesheet_reports (% records)', report_count;
    RAISE NOTICE '  ✓ timesheet_report_days (% records)', day_count;
    RAISE NOTICE '  ✓ timesheet_entries (% records)', entry_count;
    RAISE NOTICE '';
    RAISE NOTICE 'Views:';
    RAISE NOTICE '  ✓ timesheet_monthly_summary';
    RAISE NOTICE '  ✓ timesheet_employee_summary';
    RAISE NOTICE '  ✓ timesheet_category_totals';
    RAISE NOTICE '';
    RAISE NOTICE 'Indexes: 9 indexes created for optimal query performance';
    RAISE NOTICE 'Triggers: Auto-sync trigger for timesheet_entries';
    RAISE NOTICE '';
    RAISE NOTICE 'Ready for timesheet data!';
    RAISE NOTICE '';
END $$;
