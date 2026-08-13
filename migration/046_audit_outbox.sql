-- Migration: Audit outbox za fajlske radnje (revizija 2026-08, batch 6, stavka 4)
-- Date: 2026-08-11
-- Purpose: record_audit je za DB entitete dobio cursor= režim (audit red u
--   ISTOJ transakciji kao poslovna promena). Fajlske radnje nemaju transakciju
--   koja bi ih pokrila, pa ide outbox protokol (audit_support.py):
--   record_audit_intent PRE radnje (diže izuzetak → radnja bez traga se ne
--   izvršava), confirm_audit_intent posle, flush_audit_outbox prenosi
--   CONFIRMED (i zastarele PENDING) redove u audit_log, briše ABORTED.

CREATE TABLE IF NOT EXISTS audit_outbox (
    id             BIGSERIAL PRIMARY KEY,
    table_name     TEXT NOT NULL,
    record_id      BIGINT,
    record_ref     TEXT,
    action         TEXT NOT NULL,
    changed_by     TEXT NOT NULL,
    old_values     JSONB,
    new_values     JSONB,
    change_summary TEXT,
    ip_address     INET,
    user_agent     TEXT,
    status         TEXT NOT NULL DEFAULT 'PENDING'
                   CHECK (status IN ('PENDING', 'CONFIRMED', 'ABORTED')),
    created_at     TIMESTAMPTZ NOT NULL DEFAULT now(),
    flushed_at     TIMESTAMPTZ
);

CREATE INDEX IF NOT EXISTS idx_audit_outbox_unflushed
    ON audit_outbox (id) WHERE flushed_at IS NULL;

COMMENT ON TABLE audit_outbox IS
    'Outbox za audit fajlskih radnji: namera pre radnje, potvrda posle, flush u audit_log';
