-- Migration 011: create the digitized cross-section profiles table.
--
-- Moves data/digitized_profiles.json into PostgreSQL. Idempotent.
-- After applying, load any existing JSON profiles with:
--   python scripts/migrate_digitized_profiles_to_postgres.py
-- The maps endpoints then read/write Postgres automatically (Postgres-preferred,
-- JSON fallback); see maps_profile_views._profiles_pg.

CREATE TABLE IF NOT EXISTS digitized_profiles (
    id           TEXT PRIMARY KEY,
    digitized_by TEXT,
    profile      JSONB NOT NULL,
    created_at   TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at   TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS ix_digitized_profiles_digitized_by
    ON digitized_profiles (digitized_by);

-- Rollback:
--   DROP TABLE IF EXISTS digitized_profiles;
