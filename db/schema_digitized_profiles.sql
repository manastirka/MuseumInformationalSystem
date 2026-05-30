-- Digitized geological cross-section profiles (moved off the flat file
-- data/digitized_profiles.json into PostgreSQL).
--
-- A profile is a user-created record (id, endpoints, image_bounds, layers,
-- faults, digitized_by/at). The full record is stored losslessly in JSONB;
-- the id (client-supplied string) is the primary key and digitized_by is
-- promoted to a column for ownership checks.

CREATE TABLE IF NOT EXISTS digitized_profiles (
    id           TEXT PRIMARY KEY,
    digitized_by TEXT,
    profile      JSONB NOT NULL,
    created_at   TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at   TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS ix_digitized_profiles_digitized_by
    ON digitized_profiles (digitized_by);
