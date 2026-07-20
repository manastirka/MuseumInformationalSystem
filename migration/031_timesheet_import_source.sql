-- ============================================================================
-- Migration 031: провенијенција увоза радних листа из Word-а
-- ============================================================================
-- Date: July 2026
-- Радне листе се могу увести из .docx: ТЕКУЋА листа улази као да је ручно
-- унета (у ланац одобравања), а АРХИВСКЕ листе претходних година се уписују
-- као већ одобрене (историја је прошла процедуру на папиру). Ова колона бележи
-- да је ред настао увозом и којим током — за трагивост и филтрирање, без
-- мешања у постојећи status workflow.
-- ============================================================================

ALTER TABLE timesheet_reports
    ADD COLUMN IF NOT EXISTS imported_from VARCHAR(20)
        CHECK (imported_from IS NULL OR imported_from IN ('word-tekuca', 'word-arhiva'));

ALTER TABLE timesheet_reports
    ADD COLUMN IF NOT EXISTS imported_at TIMESTAMPTZ;

COMMENT ON COLUMN timesheet_reports.imported_from IS
    'Порекло увоза: word-tekuca (у ланац одобравања) или word-arhiva (одобрена архива); NULL = ручни унос';
