-- ============================================================================
-- Migration 024: Default theme is light (quiet rollout)
-- ============================================================================
-- Date: July 2026
-- The initial default ('system', migration 022) would flip dark-OS users to
-- the dark theme on deploy. For a quiet rollout the default becomes 'light';
-- 'system' and 'dark' remain available through the navbar picker. The UPDATE
-- only rewrites the pre-rollout default — nobody has picked 'system' yet
-- because the picker ships in the same release.
-- ============================================================================

ALTER TABLE users ALTER COLUMN theme_mode SET DEFAULT 'light';

UPDATE users SET theme_mode = 'light' WHERE theme_mode = 'system';
