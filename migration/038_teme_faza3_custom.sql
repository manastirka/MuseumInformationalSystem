-- ============================================================================
-- Migration 038: Theme system phase 3 — per-user custom theme creator
-- ============================================================================
-- Date: August 2026
-- Builds on migrations 033 (theme_palette) and 037 (phase 2 flat palettes).
--
-- Phase 3 lets each user build a *private* custom theme by picking individual
-- colours (base, header, sidebar, background, cards, accent, selected row,
-- buttons, text, border, links, warnings) plus shadow strength and corner
-- roundness. A custom theme is rendered through the SAME --pal-* token layer as
-- the flat palettes (no new CSS engine): the server maps the stored definition
-- to --pal-* values injected inline on <html data-palette="custom">.
--
-- 1) Widens theme_palette with the 'custom' sentinel — it means "render the
--    user's active custom theme" (see users.active_custom_theme_id).
-- 2) Adds users.active_custom_theme_id — which of the user's saved custom
--    themes is currently applied (NULL = none). It is a soft pointer, not a
--    hard FK, so deleting a theme never blocks; the app falls back to the
--    default palette when the pointer is dangling.
-- 3) Creates user_custom_themes — the saved definitions, one row per named
--    theme, owned by user_email (same key the theme-preference writes use).
--    The definition is a validated JSONB blob (the 12 colours + shadow +
--    radius); the database is the single source of truth. Custom themes are
--    PRIVATE to their owner and never enter the system palette offer.
-- ============================================================================

-- ---- theme_palette: widen the allowed set with the 'custom' sentinel ------
ALTER TABLE users DROP CONSTRAINT IF EXISTS users_theme_palette_check;
ALTER TABLE users ADD CONSTRAINT users_theme_palette_check
    CHECK (theme_palette IN (
        'heritage',
        'plava-klasicna',
        'plava-windows',
        'plava-tamna',
        'plava-ledena',
        'plava-muzejska',
        'siva-poslovna',
        'zelena-institucionalna',
        'bordo-muzejska',
        'crno-bela',
        'custom'
    ));

COMMENT ON COLUMN users.theme_palette IS
    'Named theme palette: heritage (classic museum look) | plava-* (phase 1) '
    '| siva-poslovna | zelena-institucionalna | bordo-muzejska | crno-bela '
    '(phase 2 flat palettes) | custom (phase 3, render active_custom_theme_id)';

-- ---- users.active_custom_theme_id: soft pointer to the applied custom theme
ALTER TABLE users ADD COLUMN IF NOT EXISTS active_custom_theme_id INTEGER;

COMMENT ON COLUMN users.active_custom_theme_id IS
    'Which user_custom_themes.id is applied when theme_palette = custom. '
    'Soft pointer (no FK): a dangling value falls back to the default palette.';

-- ---- user_custom_themes: the saved, private custom definitions ------------
CREATE TABLE IF NOT EXISTS user_custom_themes (
    id          SERIAL PRIMARY KEY,
    user_email  VARCHAR(255) NOT NULL,
    name        VARCHAR(80)  NOT NULL,
    definition  JSONB        NOT NULL,
    created_at  TIMESTAMPTZ  NOT NULL DEFAULT now(),
    updated_at  TIMESTAMPTZ  NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS ix_user_custom_themes_email
    ON user_custom_themes (LOWER(user_email));

COMMENT ON TABLE user_custom_themes IS
    'Phase 3 per-user custom themes. Private to the owner (user_email); shared '
    'only by explicit JSON export/import. definition = validated colours + '
    'shadow + radius, mapped to --pal-* tokens at render time.';
