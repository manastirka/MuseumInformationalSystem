-- Timesheet Schema Update for Phase 2 Migration
-- Adds missing tables required by db/promote_from_staging.sql
-- Run with: psql postgresql://aleksandarlukovic@localhost:5432/museum_system -f db/schema_timesheet_update.sql

-- Check if tables already exist
DO $$
BEGIN
    IF EXISTS (SELECT FROM pg_tables WHERE schemaname = 'public' AND tablename = 'timesheet_reports') THEN
        RAISE NOTICE 'timesheet_reports table already exists, skipping creation';
    ELSE
        RAISE NOTICE 'Creating timesheet_reports table';
    END IF;
END $$;

-- Main timesheet reports table
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
    created_at TIMESTAMPTZ DEFAULT now()
);

-- Indexes for timesheet reports
CREATE INDEX IF NOT EXISTS timesheet_reports_employee_idx ON timesheet_reports(employee_name);
CREATE INDEX IF NOT EXISTS timesheet_reports_period_idx ON timesheet_reports(year, month);
CREATE INDEX IF NOT EXISTS timesheet_reports_legacy_idx ON timesheet_reports(legacy_radna_lista_id);

-- Daily timesheet entries per report
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

-- Indexes for report days
CREATE INDEX IF NOT EXISTS timesheet_report_days_report_idx ON timesheet_report_days(report_id);

-- Staging tables for timesheet migration
CREATE TABLE IF NOT EXISTS staging_timesheet_reports (
    radna_lista_id INTEGER,
    ime_prezime TEXT,
    mesec INTEGER,
    godina INTEGER,
    organizaciona_jedinica TEXT,
    radno_mesto TEXT,
    poseban_obim_posla TEXT,
    vanredni_poslovi TEXT,
    potpis_zaposlenog TEXT,
    nalogodavac TEXT,
    potpis_sefa TEXT,
    potpis_direktora TEXT,
    povecanje_umanjenje_zarade TEXT,
    o_posao TEXT,
    created_at TEXT
);

CREATE TABLE IF NOT EXISTS staging_timesheet_days (
    radna_lista_id INTEGER,
    dan INTEGER,
    rad_na_mestu NUMERIC,
    van_muzeja NUMERIC,
    godisnji_odmor NUMERIC,
    drzavni_praznik NUMERIC,
    placeno_odsustvo NUMERIC,
    ostalo_odsustvo NUMERIC,
    bolovanje_manje_30 NUMERIC,
    bolovanje_vece_30 NUMERIC
);

-- Grant permissions (if needed)
-- GRANT ALL ON ALL TABLES IN SCHEMA public TO aleksandarlukovic;
-- GRANT ALL ON ALL SEQUENCES IN SCHEMA public TO aleksandarlukovic;

-- Display summary
DO $$
DECLARE
    report_count INTEGER;
    day_count INTEGER;
BEGIN
    SELECT COUNT(*) INTO report_count FROM timesheet_reports;
    SELECT COUNT(*) INTO day_count FROM timesheet_report_days;

    RAISE NOTICE '';
    RAISE NOTICE '=== Timesheet Schema Update Complete ===';
    RAISE NOTICE 'Tables created/verified:';
    RAISE NOTICE '  - timesheet_reports (% records)', report_count;
    RAISE NOTICE '  - timesheet_report_days (% records)', day_count;
    RAISE NOTICE '  - staging_timesheet_reports (for migration)';
    RAISE NOTICE '  - staging_timesheet_days (for migration)';
    RAISE NOTICE '';
    RAISE NOTICE 'Ready for timesheet data migration!';
END $$;
