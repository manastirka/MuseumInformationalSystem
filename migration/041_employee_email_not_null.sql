-- ============================================================================
-- Migration 036: timesheet_reports.employee_email -> NOT NULL
-- ============================================================================
-- Date: July 2026 (ревизија Codex/GPT — налаз #5)
--
-- РУПА: идентитет радне листе се решавао са
--   (employee_email = %s OR (employee_email IS NULL AND employee_name = %s))
-- на десетак места (save/load/submit/putни налог...). Ако постоји legacy ред са
-- employee_email IS NULL, идентификује се ПО ИМЕНУ — па два истоимена запослена
-- могу преузети/прегазити туђу листу.
--
-- ЗАТВАРАЊЕ: пошто employee_email постане NOT NULL, ниједан ред више не може
-- да падне у грану ``employee_email IS NULL`` — та грана постаје мртва, а
-- поклапање по имену немогуће. Није потребно рушити све те упите (грана је
-- безопасна кад ниједан ред не одговара).
--
-- DRY-RUN (DEV, 2026-07-28): 0 редова са NULL/празним email-ом од укупно 52.
-- Backfill доле је best-effort по имену из ``users``; ако на некој бази остану
-- нередови без email-а, миграција СТАЈЕ ГЛАСНО (RAISE EXCEPTION) уместо да
-- измишља податак — те редове треба ручно разрешити пре поновног покретања.
-- ============================================================================

-- 1) Best-effort backfill: попуни email из users по тачном имену.
UPDATE timesheet_reports tr
SET employee_email = u.email
FROM users u
WHERE (tr.employee_email IS NULL OR TRIM(tr.employee_email) = '')
  AND u.full_name = tr.employee_name
  AND u.email IS NOT NULL
  AND TRIM(u.email) <> '';

-- 2) Нормализуј празан стринг у NULL да га guard ухвати.
UPDATE timesheet_reports
SET employee_email = NULL
WHERE employee_email IS NOT NULL AND TRIM(employee_email) = '';

-- 3) Guard: ако је остало редова без email-а, стани гласно (не измишљај).
DO $$
DECLARE
    n INTEGER;
BEGIN
    SELECT COUNT(*) INTO n FROM timesheet_reports WHERE employee_email IS NULL;
    IF n > 0 THEN
        RAISE EXCEPTION 'Миграција 036: % листа без employee_email — ручно разрешити (backfill/спајање) пре NOT NULL ограничења', n;
    END IF;
    RAISE NOTICE 'Миграција 036: 0 листа без employee_email — постављам NOT NULL.';
END $$;

-- 4) Ограничење: employee_email је обавезан (идемпотентно — re-run је no-op).
ALTER TABLE timesheet_reports
    ALTER COLUMN employee_email SET NOT NULL;

COMMENT ON COLUMN timesheet_reports.employee_email IS
    'Обавезан канонски идентитет запосленог (NOT NULL од миграције 036). '
    'Идентификација листе иде ИСКЉУЧИВО по email-у; поклапање по имену је '
    'укинуто јер више не постоји ред са NULL email-ом.';
