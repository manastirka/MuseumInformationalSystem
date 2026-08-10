-- ============================================================================
-- Migration 029: Reception queue derived from state, not from a flag
-- ============================================================================
-- Date: July 2026
-- The queue listed photos by the `u_prijemnom_redu` flag. The pre-fix import
-- set that flag to FALSE for every filename that merely LOOKED like it carried
-- an inventory number ('M 028.JPG'), even when the link pointed at a specimen
-- that does not exist. After the retroactive relink (69 of 71), the two photos
-- that still have no link kept flag=FALSE — so they were invisible in the
-- queue, with no way for a curator to reach them.
--
-- From now on the queue is derived from the truth in the data: a photo with NO
-- link at all belongs in the queue. The flag can lie; the links cannot. The new
-- column records only the curator's DELIBERATE choice to take a photo off the
-- queue without linking it (it may simply belong in the free gallery).
-- ============================================================================

ALTER TABLE fotografije
    ADD COLUMN IF NOT EXISTS sklonjena_sa_reda BOOLEAN NOT NULL DEFAULT FALSE;

COMMENT ON COLUMN fotografije.sklonjena_sa_reda IS
    'Curator explicitly took this photo off the reception queue without linking it';
COMMENT ON COLUMN fotografije.u_prijemnom_redu IS
    'LEGACY flag — no longer used to build the queue (it could lie); kept for history';

CREATE INDEX IF NOT EXISTS idx_fotografije_sklonjena_sa_reda
    ON fotografije(sklonjena_sa_reda) WHERE sklonjena_sa_reda = FALSE;
