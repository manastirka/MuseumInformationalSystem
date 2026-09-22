-- ============================================================================
-- Migration 059: Theme system phase 4 — 'staklo' (liquid glass) palette
-- ============================================================================
-- Date: September 2026
-- Builds on 033 (theme_palette), 037/042 (phase 2 flat palettes) and
-- 043 (phase 3 custom themes).
--
-- 'staklo' is a flat palette like the phase 1/2 ones: it carries its own
-- --pal-* values in static/css/main.css and honours the mode axis (light /
-- dark) plus the accent axis. It differs only in *effect* — translucent
-- surfaces with backdrop-filter blur over a soft gradient workspace, a
-- macOS "liquid glass" look — which lives entirely in CSS. Nothing new is
-- stored per user: the palette is just one more allowed value here.
--
-- Widens users_theme_palette_check with 'staklo' and refreshes the column
-- comment. No BEGIN/COMMIT — run_migrations.py wraps all pending files in a
-- single transaction.
-- ============================================================================

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
        'staklo',
        'custom'
    ));

COMMENT ON COLUMN users.theme_palette IS
    'Named theme palette: heritage (classic museum look) | plava-* (phase 1) '
    '| siva-poslovna | zelena-institucionalna | bordo-muzejska | crno-bela '
    '(phase 2 flat palettes) | staklo (phase 4, liquid glass: translucent '
    'surfaces + backdrop blur, honours mode/accent axes) '
    '| custom (phase 3, render active_custom_theme_id)';
