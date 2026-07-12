-- ============================================================================
-- Migration 023: High-contrast theme mode
-- ============================================================================
-- Date: July 2026
-- Extends the theme_mode choices (migration 022) with 'contrast' — the
-- accessibility high-contrast variant (black on white, thick borders).
-- ============================================================================

DO $$
BEGIN
    IF EXISTS (
        SELECT 1 FROM pg_constraint
        WHERE conname = 'users_theme_mode_check'
    ) THEN
        ALTER TABLE users DROP CONSTRAINT users_theme_mode_check;
    END IF;

    ALTER TABLE users ADD CONSTRAINT users_theme_mode_check
        CHECK (theme_mode IN ('light', 'dark', 'system', 'contrast'));
END $$;

COMMENT ON COLUMN users.theme_mode IS
    'UI theme mode: light | dark | system (prefers-color-scheme) | contrast (accessibility)';
