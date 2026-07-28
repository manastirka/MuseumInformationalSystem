-- ============================================================================
-- Migration 035: административно одобрење + класификација архиве
-- ============================================================================
-- Date: July 2026
--
-- Два одвојена трага, оба уведена да ланац одобравања не би имао тихе рупе:
--
-- 1) АДМИНИСТРАТИВНО ОДОБРЕЊЕ. Админ (или директор кад одељење/шеф није
--    поуздано разрешен) може да одобри листу сам, али то се више НЕ бележи као
--    редован двостепени ланац (шеф+директор). Уместо тога попуњавамо посебан
--    траг admin_approved_by/at, док head_verified_*/director_verified_* остају
--    NULL — да одобрење никад не изгледа као два стварна потписа. Листа јесте
--    званично одобрена (status=APPROVED, is_verified=TRUE), али UI/PDF је
--    обележавају као „ОДОБРЕНО АДМИНИСТРАТИВНО".
--
-- 2) АРХИВА НИЈЕ ОДОБРЕН ИЗВЕШТАЈ. Листе увезене из Word-архиве се више НЕ
--    воде као званично одобрене (status='APPROVED', is_verified=TRUE), него
--    добијају посебну класификацију status='ARHIVA' (is_verified=FALSE). Тако
--    не улазе у листу/статистику одобрених извештаја, а приказују се неутрално
--    („Архива", не зелено „Одобрено"). Систем је још у фази тестирања —
--    званичан унос месечних извештаја креће касније — па ниједна увезена
--    архивска листа не сме да се рачуна као прошла кроз процедуру.
-- ============================================================================

ALTER TABLE timesheet_reports
    ADD COLUMN IF NOT EXISTS admin_approved_by VARCHAR(255),
    ADD COLUMN IF NOT EXISTS admin_approved_at TIMESTAMPTZ;

-- Прошири дозвољене статусе новом класификацијом 'ARHIVA' (миграција 001/006 је
-- ограничила статус на DRAFT/SUBMITTED/APPROVED/REJECTED CHECK ограничењем).
ALTER TABLE timesheet_reports
    DROP CONSTRAINT IF EXISTS timesheet_reports_status_check;
ALTER TABLE timesheet_reports
    ADD CONSTRAINT timesheet_reports_status_check
    CHECK (status IN ('DRAFT', 'SUBMITTED', 'APPROVED', 'REJECTED', 'ARHIVA'));

COMMENT ON COLUMN timesheet_reports.admin_approved_by IS
    'Email администратора/директора који је листу одобрио АДМИНИСТРАТИВНО '
    '(ван редовног двостепеног ланца); NULL = редовно одобрење или није одобрено';
COMMENT ON COLUMN timesheet_reports.admin_approved_at IS
    'Тренутак административног одобрења; NULL ако листа није административно одобрена';

-- Рекласификуј постојеће архивске увозе: архива није званично одобрен извештај.
-- Дира ИСКЉУЧИВО редове настале Word-архивским увозом.
UPDATE timesheet_reports
   SET status = 'ARHIVA',
       is_verified = FALSE,
       verified_by = NULL,
       verified_at = NULL
 WHERE imported_from = 'word-arhiva'
   AND COALESCE(status, 'DRAFT') = 'APPROVED';
