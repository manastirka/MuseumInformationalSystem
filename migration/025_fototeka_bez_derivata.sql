-- ============================================================================
-- Migration 020: Фototeka — status 'bez_derivata'
-- ============================================================================
-- Date: July 2026
-- Some archival originals (camera RAW: CR2/NEF/ARW/DNG..., and BMP) cannot be
-- decoded by the bundled libvips, so no derivative can be generated. Such a
-- photo is fully valid and archived; it just gets status 'bez_derivata'
-- (a curator may later attach a JPG preview, which flips it to 'spremna').
-- This distinguishes "no derivative possible" from 'greska' (a real failure).
-- Safe to run repeatedly.
-- ============================================================================

ALTER TABLE fotografije DROP CONSTRAINT IF EXISTS fotografije_status_check;

ALTER TABLE fotografije ADD CONSTRAINT fotografije_status_check
    CHECK (status IN ('primljena', 'obrada', 'spremna', 'greska', 'bez_derivata'));

-- Rollback:
-- Only possible if no rows use 'bez_derivata':
-- ALTER TABLE fotografije DROP CONSTRAINT IF EXISTS fotografije_status_check;
-- ALTER TABLE fotografije ADD CONSTRAINT fotografije_status_check
--     CHECK (status IN ('primljena', 'obrada', 'spremna', 'greska'));
