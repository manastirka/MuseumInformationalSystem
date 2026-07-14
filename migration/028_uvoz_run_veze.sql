-- ============================================================================
-- Migration 028: Import run — explicit link outcome counters
-- ============================================================================
-- Date: July 2026
-- Run 71 imported 125 photos and reported "prijemni_red=0", which read as
-- "everything got linked" — while in fact NOTHING was linked to a specimen
-- (the filename numbers carried leading zeros, e.g. 'M 028' vs the stored
-- '28', so the link pointed at a specimen that does not exist). The run log
-- could not tell the difference. These counters make the outcome explicit:
-- linked-to-specimen / field-trip / NO LINK.
-- ============================================================================

ALTER TABLE fototeka_uvoz_run
    ADD COLUMN IF NOT EXISTS vezano_predmet INTEGER NOT NULL DEFAULT 0;
ALTER TABLE fototeka_uvoz_run
    ADD COLUMN IF NOT EXISTS vezano_teren INTEGER NOT NULL DEFAULT 0;
ALTER TABLE fototeka_uvoz_run
    ADD COLUMN IF NOT EXISTS bez_veze INTEGER NOT NULL DEFAULT 0;

COMMENT ON COLUMN fototeka_uvoz_run.vezano_predmet IS
    'Photos linked to an existing specimen (the number was found in the collection)';
COMMENT ON COLUMN fototeka_uvoz_run.bez_veze IS
    'Photos with no link — unrecognized name, or a number that does not exist';
