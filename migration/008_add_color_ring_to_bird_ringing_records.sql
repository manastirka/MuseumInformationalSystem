-- Migration 008: add the missing color_ring column to bird_ringing_records
--
-- Context (audit finding M08, 2026-05-29):
--   bird_ringing_database.py writes color_ring on INSERT and db/schema.sql
--   declares `color_ring TEXT` on bird_ringing_records, but the DEPLOYED table
--   never received the column (schema drift). The read path therefore had to
--   use `NULL AS color_ring` in _PG_BASE_QUERY; selecting br.color_ring crashed
--   with `psycopg.errors.UndefinedColumn: column br.color_ring does not exist`.
--
-- This migration brings the deployed schema in line with db/schema.sql so the
-- stored color_ring value can finally be surfaced on reads.
--
-- Safe to run repeatedly (IF NOT EXISTS) and reversible (see rollback below).

ALTER TABLE bird_ringing_records
    ADD COLUMN IF NOT EXISTS color_ring TEXT;

-- After applying this migration, surface the real value by changing the read
-- query in bird_ringing_database.py (_PG_BASE_QUERY):
--     NULL AS color_ring,   ->   br.color_ring,
-- and update test_fixb_bird_bilja.py accordingly.

-- Rollback (only if you must revert):
--   ALTER TABLE bird_ringing_records DROP COLUMN IF EXISTS color_ring;
