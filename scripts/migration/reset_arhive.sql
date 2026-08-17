-- ============================================================================
-- Ресет архиве захтева — брише СВЕ захтеве и потписе, чува подешавања.
-- ============================================================================
-- НЕПОВРАТНО. Исте три ограде као `reset_radnih_listi.sql`:
--   1. име базе се прослеђује и мора да се поклопи са `current_database()`;
--   2. подразумевано DRY RUN (све се изврши па ROLLBACK);
--   3. све у једној трансакцији.
--
-- Дry run:
--   psql -d mis_db -v baza=mis_db -f reset_arhive.sql
-- Стварно:
--   psql -d mis_db -v baza=mis_db -v izvrsi=on -f reset_arhive.sql
--
-- ШТА БРИШЕ
--   archive_requests      захтеви (родитељ)
--   approval_signatures   ┐
--   request_history       ├ CASCADE, брише их база сама
--   request_comments      ┘
--   document_signatures   засебан ток дигиталних потписа
--   signature_audit_log   траг тог тока
--
-- ШТА НЕ ДИРА — и то је важно
--   signature_templates   ПОДЕШАВАЊЕ, не подаци. Шест редова уписаних
--                         15.01.2026. дефинишу који тип документа тражи
--                         који потпис и коју верификацију. Брисање би
--                         однело конфигурацију модула, не тест податке.
--   procurement_requests  показује на archive_requests без CASCADE
--                         (NO ACTION). Провeрено: 0 редова, па нема шта да
--                         блокира. Ако их икад буде, брисање ће пући —
--                         и треба да пукне, уместо да остави висеће везе.
-- ============================================================================

\set ON_ERROR_STOP on
\pset pager off

\if :{?izvrsi}
\else
  \set izvrsi off
\endif

\if :{?baza}
\else
  \echo '>>> ОДБИЈЕНО: недостаје -v baza=<име базе>'
  DO $odbij$ BEGIN RAISE EXCEPTION 'nedostaje -v baza'; END $odbij$;
\endif

SELECT (current_database() = :'baza') AS baza_ok,
       current_database()             AS stvarna_baza \gset

\if :baza_ok
\else
  \echo ''
  \echo '>>> ОДБИЈЕНО: покренуто над базом' :stvarna_baza
  \echo '>>> а тражена је' :baza '— ништа није промењено.'
  DO $odbij$ BEGIN RAISE EXCEPTION 'pogresna baza'; END $odbij$;
\endif

BEGIN;

\echo ''
\echo '=== ПРЕ ==='
SELECT 'archive_requests' AS tabela, COUNT(*) FROM archive_requests
UNION ALL SELECT 'approval_signatures', COUNT(*) FROM approval_signatures
UNION ALL SELECT 'request_history', COUNT(*) FROM request_history
UNION ALL SELECT 'request_comments', COUNT(*) FROM request_comments
UNION ALL SELECT 'document_signatures', COUNT(*) FROM document_signatures
UNION ALL SELECT 'signature_audit_log', COUNT(*) FROM signature_audit_log
UNION ALL SELECT 'signature_templates (НЕ дира се)', COUNT(*) FROM signature_templates
ORDER BY 1;

DELETE FROM signature_audit_log;
DELETE FROM document_signatures;
DELETE FROM archive_requests;

\echo ''
\echo '=== ПОСЛЕ (у трансакцији) ==='
SELECT 'archive_requests' AS tabela, COUNT(*) FROM archive_requests
UNION ALL SELECT 'approval_signatures', COUNT(*) FROM approval_signatures
UNION ALL SELECT 'request_history', COUNT(*) FROM request_history
UNION ALL SELECT 'request_comments', COUNT(*) FROM request_comments
UNION ALL SELECT 'document_signatures', COUNT(*) FROM document_signatures
UNION ALL SELECT 'signature_audit_log', COUNT(*) FROM signature_audit_log
UNION ALL SELECT 'signature_templates (НЕ дира се)', COUNT(*) FROM signature_templates
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
