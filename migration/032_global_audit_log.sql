-- Migration: Global audit trail (ZADATAK #4, ANALIZA-2026-07)
-- Date: 2026-07-22
-- Purpose: Jedinstven audit trag za osetljive akcije koje do sada nisu ostavljale
--   nikakav trag: brisanja u zbirkama, promene dozvola (module access), izmene
--   korisnika, i finansijski zapisi. Modelovano po uzoru na timesheet_audit_log
--   (migration/004) — iste ideje (akcija, ko, kada, old/new, IP) — ali app-level
--   i generalizovano: događaji obuhvataju više tabela I JSON skladišta, a
--   identitet aktera (Flask sesija) postoji samo na app sloju.
--
-- VAŽNO: tabela `audit_log` VEĆ POSTOJI (db/schema.sql) i već je koristi
--   fototeka batch-edit (fototeka_views.py:_audit_upisi upisuje table_name,
--   record_id, action, new_values, performed_by). Da bismo dobili JEDAN globalni
--   trag (a ne drugi paralelni), ovde se postojeća tabela PROŠIRUJE, ne pravi
--   nova. Postojeći upisi (performed_by = users.id) ostaju validni; novi app-level
--   upisi koriste changed_by (email) jer većina hendlera u sesiji ima email, ne id.

-- ============================================================================
-- 1. TABELA (create-if-missing za sveže instalacije, pa ALTER za proširenja)
-- ============================================================================

CREATE TABLE IF NOT EXISTS audit_log (
    id           BIGSERIAL PRIMARY KEY,
    table_name   TEXT NOT NULL,
    record_id    BIGINT,
    action       TEXT NOT NULL,
    old_values   JSONB,
    new_values   JSONB,
    performed_by INTEGER REFERENCES users(id),
    performed_at TIMESTAMPTZ DEFAULT now(),
    ip_address   INET
);

-- App-level proširenja (idempotentno):
ALTER TABLE audit_log ADD COLUMN IF NOT EXISTS changed_by     TEXT;  -- email aktera (kad nemamo users.id)
ALTER TABLE audit_log ADD COLUMN IF NOT EXISTS change_summary TEXT;  -- čitljiv opis akcije
ALTER TABLE audit_log ADD COLUMN IF NOT EXISTS user_agent     TEXT;  -- klijentski User-Agent
ALTER TABLE audit_log ADD COLUMN IF NOT EXISTS record_ref     TEXT;  -- tekstualni id (email, registracija, module_key)

-- ============================================================================
-- 2. INDEKSI (upiti: "šta se dešavalo skoro", "ko je dirao X", "akcije korisnika Y")
-- ============================================================================

CREATE INDEX IF NOT EXISTS idx_audit_log_performed_at
    ON audit_log(performed_at DESC);

CREATE INDEX IF NOT EXISTS idx_audit_log_table_record
    ON audit_log(table_name, record_id);

CREATE INDEX IF NOT EXISTS idx_audit_log_changed_by
    ON audit_log(changed_by);

CREATE INDEX IF NOT EXISTS idx_audit_log_action
    ON audit_log(action);

-- ============================================================================
-- 3. KOMENTARI
-- ============================================================================

COMMENT ON TABLE audit_log IS 'Globalni audit trag osetljivih akcija (piše aplikacija, best-effort)';
COMMENT ON COLUMN audit_log.table_name IS 'Tip/tabela entiteta (mineral, user, module_access, nabavka, fotografije, ...)';
COMMENT ON COLUMN audit_log.record_id IS 'Numerički id pogođenog zapisa (NULL kad id nije broj)';
COMMENT ON COLUMN audit_log.record_ref IS 'Tekstualni id pogođenog zapisa (email, registracija, module_key)';
COMMENT ON COLUMN audit_log.changed_by IS 'Email aktera (app-level upisi); za starije upise koristi performed_by → users.id';
COMMENT ON COLUMN audit_log.change_summary IS 'Čitljiv opis akcije';

-- ============================================================================
-- 4. VERIFIKACIJA
-- ============================================================================

DO $$
DECLARE
    have_changed_by BOOLEAN;
BEGIN
    SELECT EXISTS (
        SELECT FROM information_schema.columns
        WHERE table_name = 'audit_log' AND column_name = 'changed_by'
    ) INTO have_changed_by;

    IF have_changed_by THEN
        RAISE NOTICE 'Migration 032 completed: audit_log proširen (changed_by/change_summary/user_agent/record_ref).';
    ELSE
        RAISE WARNING 'Migration 032 may not have completed correctly';
    END IF;
END $$;
