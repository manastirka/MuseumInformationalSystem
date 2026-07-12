-- ============================================================================
-- Migration 026: Batch import log (Фототека — увоз са мрежног диска)
-- ============================================================================
-- Date: July 2026
-- Persistent record of batch import runs (UI button / systemd timer / CLI)
-- and their per-file outcomes, so scheduled imports are auditable and the
-- import screen can show recent history. Dry runs are not logged.
-- ============================================================================

CREATE TABLE IF NOT EXISTS fototeka_uvoz_run (
    id SERIAL PRIMARY KEY,
    pokrenut_at TIMESTAMP NOT NULL DEFAULT NOW(),
    zavrsen_at TIMESTAMP,
    izvor TEXT NOT NULL CHECK (izvor IN ('ui', 'timer', 'cli')),
    pokrenuo_email VARCHAR(255),
    ukupno INTEGER NOT NULL DEFAULT 0,
    uvezeno INTEGER NOT NULL DEFAULT 0,
    duplikata INTEGER NOT NULL DEFAULT 0,
    neuspesno INTEGER NOT NULL DEFAULT 0,
    u_prijemni_red INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS fototeka_uvoz_stavka (
    id SERIAL PRIMARY KEY,
    run_id INTEGER NOT NULL REFERENCES fototeka_uvoz_run(id) ON DELETE CASCADE,
    datoteka TEXT NOT NULL,
    korisnicki_folder TEXT,
    ishod TEXT NOT NULL CHECK (ishod IN ('uvezeno', 'duplikat', 'neuspesno')),
    klasa TEXT CHECK (klasa IN ('predmet', 'teren', 'prijemni_red')),
    fotografija_id INTEGER REFERENCES fotografije(id) ON DELETE SET NULL,
    poruka TEXT
);

CREATE INDEX IF NOT EXISTS idx_fototeka_uvoz_stavka_run
    ON fototeka_uvoz_stavka(run_id);

COMMENT ON TABLE fototeka_uvoz_run IS
    'Batch import runs from the shared intake folder (Samba)';
COMMENT ON TABLE fototeka_uvoz_stavka IS
    'Per-file outcome of a batch import run';
