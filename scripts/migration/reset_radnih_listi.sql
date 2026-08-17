-- ============================================================================
-- Ресет радних листа — брише СВЕ месечне извештаје и све што виси о њима.
-- ============================================================================
-- НЕПОВРАТНО. Три ограде:
--
--   1. Име базе се прослеђује и мора да се поклопи са `current_database()`.
--      Без тога скрипта пуца пре него што ишта дирне.
--   2. Подразумевано је DRY RUN: све се изврши у трансакцији па се уради
--      ROLLBACK. Бројеви су прави, измене нису. Тек `-v izvrsi=on` ради COMMIT.
--   3. Све је у ЈЕДНОЈ трансакцији — или све или ништа.
--
-- Дрy run:
--   psql -d mis_db -v baza=mis_db -f reset_radnih_listi.sql
-- Стварно брисање (претходно направити pg_dump!):
--   psql -d mis_db -v baza=mis_db -v izvrsi=on -f reset_radnih_listi.sql
--
-- Шта брише:
--   timesheet_reports         родитељ
--   timesheet_report_days     ┐
--   timesheet_status_history  ├ база их брише сама (ON DELETE CASCADE)
--   timesheet_entries         │
--   timesheet_edit_requests   ┘
--   timesheet_audit_log       НЕМА страни кључ — брише се изричито, и то
--                             ПОСЛЕ извештаја (окидач га допуњава при брисању)
--   staging_timesheet_*       остаци увоза
--
-- Не дира кориснике, одељења, нити ишта ван радних листа.
-- ============================================================================

\set ON_ERROR_STOP on
\pset pager off

-- Ако `izvrsi` није прослеђен, подразумева се искључено.
\if :{?izvrsi}
\else
  \set izvrsi off
\endif

-- Ограда 1: права база.
-- Провера НЕ може да иде унутар DO $$...$$ блока — psql не замењује
-- променљиве унутар dollar-quote-а, па би `:'baza'` стигло до сервера
-- дословно и дало синтаксну грешку уместо провере.
\if :{?baza}
\else
  \echo '>>> ОДБИЈЕНО: недостаје -v baza=<име базе>'
  -- Намерна грешка: `\quit` излази са кодом 0, па би скрипта која ово зове
  -- мислила да је све прошло. Одбијање мора да се види и у излазном коду.
  DO $odbij$ BEGIN RAISE EXCEPTION 'nedostaje -v baza'; END $odbij$;
\endif

SELECT (current_database() = :'baza') AS baza_ok,
       current_database()             AS stvarna_baza \gset

\if :baza_ok
\else
  \echo ''
  \echo '>>> ОДБИЈЕНО: скрипта је покренута над базом' :stvarna_baza
  \echo '>>> а тражена је' :baza '— ништа није промењено.'
  DO $odbij$ BEGIN RAISE EXCEPTION 'pogresna baza'; END $odbij$;
\endif

BEGIN;

\echo ''
\echo '=== ПРЕ ==='
SELECT 'timesheet_reports' AS tabela, COUNT(*) FROM timesheet_reports
UNION ALL SELECT 'timesheet_report_days', COUNT(*) FROM timesheet_report_days
UNION ALL SELECT 'timesheet_status_history', COUNT(*) FROM timesheet_status_history
UNION ALL SELECT 'timesheet_entries', COUNT(*) FROM timesheet_entries
UNION ALL SELECT 'timesheet_edit_requests', COUNT(*) FROM timesheet_edit_requests
UNION ALL SELECT 'timesheet_audit_log', COUNT(*) FROM timesheet_audit_log
UNION ALL SELECT 'staging_timesheet_reports', COUNT(*) FROM staging_timesheet_reports
UNION ALL SELECT 'staging_timesheet_days', COUNT(*) FROM staging_timesheet_days
ORDER BY 1;

-- РЕДОСЛЕД ЈЕ БИТАН, и супротан од очекиваног.
-- Над `timesheet_reports` стоји окидач `timesheet_reports_audit`
-- (AFTER INSERT OR DELETE OR UPDATE) који при сваком брисању УПИСУЈЕ ред у
-- `timesheet_audit_log`. Ако се траг обрише први, брисање извештаја одмах
-- направи нови — колико извештаја, толико нових редова. Ухваћено dry-run-ом:
-- после „брисања" је у логу остало тачно 51, колико и извештаја.
-- Зато прво извештаји, па тек онда траг.
DELETE FROM timesheet_reports;
DELETE FROM timesheet_audit_log;
DELETE FROM staging_timesheet_days;
DELETE FROM staging_timesheet_reports;

\echo ''
\echo '=== ПОСЛЕ (у трансакцији) ==='
SELECT 'timesheet_reports' AS tabela, COUNT(*) FROM timesheet_reports
UNION ALL SELECT 'timesheet_report_days', COUNT(*) FROM timesheet_report_days
UNION ALL SELECT 'timesheet_status_history', COUNT(*) FROM timesheet_status_history
UNION ALL SELECT 'timesheet_entries', COUNT(*) FROM timesheet_entries
UNION ALL SELECT 'timesheet_edit_requests', COUNT(*) FROM timesheet_edit_requests
UNION ALL SELECT 'timesheet_audit_log', COUNT(*) FROM timesheet_audit_log
UNION ALL SELECT 'staging_timesheet_reports', COUNT(*) FROM staging_timesheet_reports
UNION ALL SELECT 'staging_timesheet_days', COUNT(*) FROM staging_timesheet_days
ORDER BY 1;

\if :izvrsi
    COMMIT;
    \echo ''
    \echo '>>> ИЗВРШЕНО: промене су уписане (COMMIT).'
\else
    ROLLBACK;
    \echo ''
    \echo '>>> DRY RUN: све враћено (ROLLBACK). Бројеви изнад су прави, измене нису.'
    \echo '>>> За стварно брисање додај:  -v izvrsi=on'
\endif
