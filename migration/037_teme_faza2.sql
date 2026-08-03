-- ============================================================================
-- Migration 037: Theme system phase 2 — neutral/institutional palettes + accent axis
-- ============================================================================
-- Date: August 2026
-- Builds on migration 033 (theme_palette) and 022 (theme_accent).
--
-- 1) Widens theme_palette with four new flat palettes:
--      siva-poslovna, zelena-institucionalna, bordo-muzejska, crno-bela.
-- 2) Widens theme_accent into a full standalone accent axis (9 colours) and
--    adds the 'podrazumevano' sentinel. 'podrazumevano' means "use the family
--    default" — heritage renders green (its base), a flat palette renders its
--    own identity colour — so a flat palette is never silently tinted green.
--    It becomes the new column default for freshly created users.
-- 3) Rewrites existing 'zelena' rows to 'podrazumevano'. This is a visual no-op
--    for the heritage family (both render as the default green with no
--    data-accent attribute), but for anyone on a flat palette it restores the
--    palette's own identity accent instead of forcing green.
--
-- The heritage accents 'oker'/'petrolej' are kept for existing heritage users.
-- Auto/dark for flat palettes reuses the existing theme_mode axis (system/dark)
-- via a shared dark-flat CSS layer — no new column is needed for auto.
-- ============================================================================

-- ---- theme_palette: widen the allowed set --------------------------------
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
        'crno-bela'
    ));

COMMENT ON COLUMN users.theme_palette IS
    'Named theme palette: heritage (classic museum look, keeps mode/accent/style) '
    '| plava-* (phase 1) | siva-poslovna | zelena-institucionalna | bordo-muzejska '
    '| crno-bela (phase 2 flat palettes, honour mode for auto/dark + accent axis)';

-- ---- theme_accent: widen into the full accent axis + sentinel ------------
-- Normalise the ambiguous legacy default first (must precede the new CHECK so
-- the UPDATE target value is already permitted once the constraint lands).
ALTER TABLE users DROP CONSTRAINT IF EXISTS users_theme_accent_check;
ALTER TABLE users ADD CONSTRAINT users_theme_accent_check
    CHECK (theme_accent IN (
        'podrazumevano',
        'zelena', 'bordo', 'oker', 'petrolej',
        'klasicna-plava', 'svetloplava', 'tamnoplava', 'tirkizna',
        'ljubicasta', 'narandzasta', 'grafitnosiva'
    ));

ALTER TABLE users ALTER COLUMN theme_accent SET DEFAULT 'podrazumevano';

-- Visual no-op for heritage (default green either way); restores palette
-- identity for anyone already on a flat palette.
UPDATE users SET theme_accent = 'podrazumevano' WHERE theme_accent = 'zelena';

COMMENT ON COLUMN users.theme_accent IS
    'Accent axis: podrazumevano (family default) | zelena | bordo | oker | petrolej '
    '(heritage) | klasicna-plava | svetloplava | tamnoplava | tirkizna | ljubicasta '
    '| narandzasta | grafitnosiva (phase 2, applies to flat palettes)';
