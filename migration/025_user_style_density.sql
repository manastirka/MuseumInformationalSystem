-- ============================================================================
-- Migration 025: Per-user visual style + density; system mode is the default
-- ============================================================================
-- Date: July 2026
-- Adds the remaining two theme axes (visual style character and UI density)
-- and restores 'system' (prefers-color-scheme) as the default mode for NEW
-- users. Existing rows keep their current mode — a deliberate 'light' choice
-- cannot be told apart from the migration-024 default, so nobody's theme
-- flips on deploy; the picker is available to everyone.
-- ============================================================================

ALTER TABLE users ADD COLUMN IF NOT EXISTS theme_style VARCHAR(20) NOT NULL DEFAULT 'institucionalna';
ALTER TABLE users ADD COLUMN IF NOT EXISTS theme_density VARCHAR(16) NOT NULL DEFAULT 'komforno';

DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM pg_constraint WHERE conname = 'users_theme_style_check'
    ) THEN
        ALTER TABLE users ADD CONSTRAINT users_theme_style_check
            CHECK (theme_style IN ('institucionalna', 'moderna', 'arhivska', 'terenska'));
    END IF;

    IF NOT EXISTS (
        SELECT 1 FROM pg_constraint WHERE conname = 'users_theme_density_check'
    ) THEN
        ALTER TABLE users ADD CONSTRAINT users_theme_density_check
            CHECK (theme_density IN ('komforno', 'kompakt'));
    END IF;
END $$;

ALTER TABLE users ALTER COLUMN theme_mode SET DEFAULT 'system';

COMMENT ON COLUMN users.theme_style IS
    'Visual style character: institucionalna (default) | moderna | arhivska | terenska';
COMMENT ON COLUMN users.theme_density IS
    'UI density: komforno (default) | kompakt';
