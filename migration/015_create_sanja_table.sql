-- Migration 010: create the Sanja Paleogene/Neogene mammal collection table.
--
-- Moves the 1,145-specimen collection off the single git-untracked flat file
-- Sanja/sanja_paleogene_neogene_mammals.json into PostgreSQL so it is backed up
-- with the rest of the system of record. Idempotent.
--
-- After applying this, load the existing JSON data with:
--   python scripts/migrate_sanja_to_postgres.py
-- The application reads/writes Postgres automatically once the table exists
-- (Postgres-preferred, JSON fallback); see collection_management_views._sanja_pg.

CREATE TABLE IF NOT EXISTS sanja_paleogene_neogene_mammals (
    id          INTEGER PRIMARY KEY,
    source_row  INTEGER,
    specimen    JSONB NOT NULL,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at  TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS ix_sanja_specimen_name
    ON sanja_paleogene_neogene_mammals ((specimen->>'specimen_name'));
CREATE INDEX IF NOT EXISTS ix_sanja_location_found
    ON sanja_paleogene_neogene_mammals ((specimen->>'location_found'));

-- Rollback:
--   DROP TABLE IF EXISTS sanja_paleogene_neogene_mammals;
