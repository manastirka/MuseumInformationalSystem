-- ============================================================================
-- Migration 021: Фototeka — vidljivost (javno / privatno)
-- ============================================================================
-- Date: July 2026
-- Per-photo access control. On upload the curator picks visibility:
--   'javno'    — visible to every logged-in employee (default);
--   'privatno' — visible only to the author (plus admin/director, for
--                supervision).
-- ADD COLUMN ... DEFAULT 'javno' backfills every existing row (including the
-- Phase 4 legacy-image migration) as 'javno' — they were public, unchanged.
-- Safe to run repeatedly.
-- ============================================================================

ALTER TABLE fotografije ADD COLUMN IF NOT EXISTS vidljivost TEXT NOT NULL DEFAULT 'javno';

ALTER TABLE fotografije DROP CONSTRAINT IF EXISTS fotografije_vidljivost_check;
ALTER TABLE fotografije ADD CONSTRAINT fotografije_vidljivost_check
    CHECK (vidljivost IN ('javno', 'privatno'));

CREATE INDEX IF NOT EXISTS idx_fotografije_vidljivost ON fotografije (vidljivost);

-- Rollback:
-- ALTER TABLE fotografije DROP CONSTRAINT IF EXISTS fotografije_vidljivost_check;
-- ALTER TABLE fotografije DROP COLUMN IF EXISTS vidljivost;
