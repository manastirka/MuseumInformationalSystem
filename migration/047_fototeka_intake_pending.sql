-- Migration: Namera intake-a fotografije (revizija 2026-08, batch 6, stavka 5)
-- Date: 2026-08-11
-- Purpose: _intake_photo_from_path postavlja RAW fajl unutar spoljne
--   transakcije koja se commit-uje tek po izlasku iz ManagedPostgresConnection
--   konteksta. Ako commit padne, RAW ostaje bez DB reda i write-once putanja
--   je trajno "zauzeta" (ponovni upload = lažna kolizija). Protokol: namera
--   se upiše OVDE (sopstvena kratka transakcija) PRE fajla; brisanje namere
--   ide u istoj transakciji kao red fotografije. Zaostale namere čisti
--   fototeka_jobs.reconcile_intake_pending (periodično u workeru).

CREATE TABLE IF NOT EXISTS fototeka_intake_pending (
    id           BIGSERIAL PRIMARY KEY,
    sha256       TEXT NOT NULL,
    raw_putanja  TEXT NOT NULL,
    original_ime TEXT,
    created_at   TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE UNIQUE INDEX IF NOT EXISTS uq_fototeka_intake_pending_raw
    ON fototeka_intake_pending (raw_putanja);

COMMENT ON TABLE fototeka_intake_pending IS
    'Namera intake-a RAW fajla pre postavljanja; red bez fotografije = siroče propalog commit-a';
