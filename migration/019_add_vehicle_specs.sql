-- Migration 014: extend `vehicles` with the specification fields needed by
-- the updated vehicle management UI (VIN, model variant, mass figures,
-- engine specs, fuel type and consumption).
--
-- Context:
--   db/schema_vehicles.sql now declares these columns on fresh installs,
--   but the deployed table is missing them. The updated vehicle_management
--   template reads/writes them, so without this migration the read path
--   crashes with `psycopg.errors.UndefinedColumn` and writes silently
--   discard the values.
--
-- All additions are nullable, so existing rows remain valid.
-- Safe to run repeatedly (IF NOT EXISTS) and reversible (see rollback).

ALTER TABLE vehicles
    ADD COLUMN IF NOT EXISTS vin                    TEXT,
    ADD COLUMN IF NOT EXISTS model_variant          TEXT,
    ADD COLUMN IF NOT EXISTS max_mass_kg            INTEGER,
    ADD COLUMN IF NOT EXISTS curb_mass_kg           INTEGER,
    ADD COLUMN IF NOT EXISTS engine_displacement_cc INTEGER,
    ADD COLUMN IF NOT EXISTS engine_power_kw        INTEGER,
    ADD COLUMN IF NOT EXISTS fuel_type              TEXT,
    ADD COLUMN IF NOT EXISTS fuel_consumption       REAL;

-- Rollback (only if you must revert):
--   ALTER TABLE vehicles
--       DROP COLUMN IF EXISTS vin,
--       DROP COLUMN IF EXISTS model_variant,
--       DROP COLUMN IF EXISTS max_mass_kg,
--       DROP COLUMN IF EXISTS curb_mass_kg,
--       DROP COLUMN IF EXISTS engine_displacement_cc,
--       DROP COLUMN IF EXISTS engine_power_kw,
--       DROP COLUMN IF EXISTS fuel_type,
--       DROP COLUMN IF EXISTS fuel_consumption;
