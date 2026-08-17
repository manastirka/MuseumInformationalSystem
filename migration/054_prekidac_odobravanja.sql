-- ============================================================================
-- Migration 054: рад без одобравања (два прекидача)
-- ============================================================================
-- Date: 17.08.2026
--
-- Ланац одобравања претпоставља да шефови одељења и директор редовно
-- потписују. Кад то изостане, извештаји запослених остају заглављени у
-- SUBMITTED, а документи у 'na_odobrenju'. Прекидачи у system_settings
-- (`odobravanje_izvestaja`, `odobravanje_dokumenata`) гасе тај захтев.
--
-- Ова миграција само отвара место за нова стања. НИЈЕДАН постојећи ред се не
-- мења — угашен прекидач ништа не проглашава одобреним.
--
-- ЗАШТО НОВО СТАЊЕ, А НЕ САМООДОБРЕЊЕ У 'APPROVED'
-- Миграција 040 је увела посебан траг за административно одобрење баш зато да
-- одобрење ван редовног ланца никад не изгледа као два стварна потписа. Исто
-- правило важи и овде, само јаче: извештај који НИКО није потписао не сме да
-- дели статус са оним који су потписали шеф и директор. Годину дана касније
-- нико неће памтити када је прекидач био угашен — статус мора сам да каже.
--
-- Поља потписа (head_verified_*, director_verified_*, admin_approved_*,
-- is_verified) остају ПРАЗНА за ове редове. То је цела поента.
-- ============================================================================

BEGIN;

-- 1. Радне листе: ново стање BEZ_ODOBRENJA
ALTER TABLE timesheet_reports
    DROP CONSTRAINT IF EXISTS timesheet_reports_status_check;
ALTER TABLE timesheet_reports
    ADD CONSTRAINT timesheet_reports_status_check
    CHECK (status IN ('DRAFT', 'SUBMITTED', 'APPROVED', 'REJECTED',
                      'ARHIVA', 'BEZ_ODOBRENJA'));

COMMENT ON COLUMN timesheet_reports.status IS
    'DRAFT/SUBMITTED/APPROVED/REJECTED редован ток; ARHIVA = Word увоз, није '
    'прошао процедуру; BEZ_ODOBRENJA = поднето док је одобравање искључено, '
    'извештај је завршен а поља потписа су празна';

-- 2. Документа: ново стање bez_odobrenja
ALTER TABLE document_versions
    DROP CONSTRAINT IF EXISTS document_versions_status_check;
ALTER TABLE document_versions
    ADD CONSTRAINT document_versions_status_check
    CHECK (status IN ('nacrt', 'na_odobrenju', 'odobreno', 'arhivirano',
                      'bez_odobrenja'));

COMMENT ON COLUMN document_versions.status IS
    'nacrt/na_odobrenju/odobreno/arhivirano редован ток; bez_odobrenja = '
    'верзија је постала важећа док је одобравање искључено, без рецензента';

-- 3. Индекси: оба нова стања се често филтрирају заједно са завршеним.
CREATE INDEX IF NOT EXISTS idx_timesheet_reports_status_bez
    ON timesheet_reports (status)
    WHERE status = 'BEZ_ODOBRENJA';

CREATE INDEX IF NOT EXISTS idx_document_versions_status_bez
    ON document_versions (status)
    WHERE status = 'bez_odobrenja';

COMMIT;
