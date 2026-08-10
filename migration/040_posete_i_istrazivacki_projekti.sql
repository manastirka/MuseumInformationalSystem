-- ============================================================================
-- Migration 040: посете и истраживачки пројекти у базу
-- ============================================================================
-- Date: August 2026
--
-- Евиденција посета и истраживачких пројеката до сада је живела у процесним
-- Python листама (app.py: VISITOR_RECORDS / RESEARCH_PROJECTS). Под gunicorn-ом
-- са више радника упис на једном раднику је невидљив на другом и нестаје при
-- рестарту — а сваки упис је приказивао поруку о успеху.
--
-- Ова миграција уводи трајне табеле; upis и читање прелазе на PostgreSQL,
-- процесне листе се уклањају (ревизија 2026-08, ставка 3).
--
-- Идемпотентна (безбедна за поновно покретање).
-- ============================================================================

CREATE TABLE IF NOT EXISTS visitor_records (
    id SERIAL PRIMARY KEY,
    visit_date DATE,
    visitor_type TEXT,
    group_size INTEGER NOT NULL DEFAULT 1,
    age_category TEXT,
    nationality TEXT,
    ticket_type TEXT,
    guided_tour BOOLEAN NOT NULL DEFAULT FALSE,
    exhibition TEXT,
    feedback_rating TEXT,
    notes TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_visitor_records_visit_date
    ON visitor_records (visit_date);

CREATE TABLE IF NOT EXISTS research_projects (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    project_code TEXT,
    principal_investigator TEXT,
    department TEXT,
    research_area TEXT,
    start_date DATE,
    end_date DATE,
    funding_source TEXT,
    budget TEXT,
    status TEXT,
    description TEXT,
    publications TEXT,
    collaborators TEXT,
    keywords TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_research_projects_start_date
    ON research_projects (start_date);
