-- ============================================================================
-- Migration 027: Localities registry (samostalan šifarnik lokaliteta)
-- ============================================================================
-- Date: July 2026
-- Until now "Локалитети" was a runtime aggregate over minerals.card_locality —
-- there was no table, so a locality with no specimen (a field site, a planned
-- dig, a place known but not yet collected from) could not exist at all.
-- This registry is INDEPENDENT of specimens: rows may be seeded from the
-- collection's distinct values, but they can also be added by hand.
-- Specimens keep their free-text card_locality; no FK is introduced here
-- (linking specimens to the registry is a separate, later decision).
-- ============================================================================

CREATE TABLE IF NOT EXISTS localities (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    country TEXT,
    note TEXT,
    source TEXT NOT NULL DEFAULT 'rucno' CHECK (source IN ('rucno', 'seed')),
    created_by_email VARCHAR(255),
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_localities_name ON localities(name);

COMMENT ON TABLE localities IS
    'Standalone locality registry — independent of specimens (field sites, future finds)';
COMMENT ON COLUMN localities.source IS
    'rucno = added by a curator; seed = imported from the collection''s distinct values';
