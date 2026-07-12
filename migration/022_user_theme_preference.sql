-- ============================================================================
-- Migration 022: Per-user theme preference (mode + accent)
-- ============================================================================
-- Date: July 2026
-- Stores each user's UI theme choice. Mode follows the OS by default
-- ('system' -> prefers-color-scheme); accent defaults to the museum green.
-- Applied client-side via data-theme/data-accent on <html> (see base.html).
-- ============================================================================

ALTER TABLE users ADD COLUMN IF NOT EXISTS theme_mode VARCHAR(16) NOT NULL DEFAULT 'system';
ALTER TABLE users ADD COLUMN IF NOT EXISTS theme_accent VARCHAR(16) NOT NULL DEFAULT 'zelena';

DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM pg_constraint
        WHERE conname = 'users_theme_mode_check'
    ) THEN
        ALTER TABLE users ADD CONSTRAINT users_theme_mode_check
            CHECK (theme_mode IN ('light', 'dark', 'system'));
    END IF;

    IF NOT EXISTS (
        SELECT 1 FROM pg_constraint
        WHERE conname = 'users_theme_accent_check'
    ) THEN
        ALTER TABLE users ADD CONSTRAINT users_theme_accent_check
            CHECK (theme_accent IN ('zelena', 'bordo', 'oker', 'petrolej'));
    END IF;
END $$;

COMMENT ON COLUMN users.theme_mode IS
    'UI theme mode: light | dark | system (follow prefers-color-scheme)';
COMMENT ON COLUMN users.theme_accent IS
    'UI accent color: zelena (default) | bordo | oker | petrolej';
