-- ============================================================================
-- Migration 033: Named blue-white theme palette (phase 1 of the new theme set)
-- ============================================================================
-- Date: July 2026
-- Adds a fifth theme axis: theme_palette — a self-contained named look that
-- overrides the classic "heritage" (parchment/museum) family. Phase 1 ships
-- five professional blue-white palettes. The new professional default is
-- 'plava-klasicna'; existing users are pinned to 'heritage' so nobody's look
-- changes on deploy (same quiet-rollout approach as migration 024). The
-- heritage family keeps its mode/accent/style axes; blue palettes are
-- self-describing (they carry their own light/dark surfaces).
-- ============================================================================

ALTER TABLE users ADD COLUMN IF NOT EXISTS theme_palette VARCHAR(24) NOT NULL DEFAULT 'plava-klasicna';

-- Existing rows predate the picker: keep them on the classic heritage look.
-- New rows created after this migration inherit the 'plava-klasicna' default.
UPDATE users SET theme_palette = 'heritage' WHERE theme_palette = 'plava-klasicna';

DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM pg_constraint WHERE conname = 'users_theme_palette_check'
    ) THEN
        ALTER TABLE users ADD CONSTRAINT users_theme_palette_check
            CHECK (theme_palette IN (
                'heritage',
                'plava-klasicna',
                'plava-windows',
                'plava-tamna',
                'plava-ledena',
                'plava-muzejska'
            ));
    END IF;
END $$;

COMMENT ON COLUMN users.theme_palette IS
    'Named theme palette: heritage (classic museum look, keeps mode/accent/style) '
    '| plava-klasicna (default) | plava-windows | plava-tamna | plava-ledena | plava-muzejska';
