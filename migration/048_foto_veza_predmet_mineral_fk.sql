-- Migration: Stabilan strani ključ veze fotografija↔mineral
--            (revizija 2026-08, batch 6, stavka 7)
-- Date: 2026-08-11
-- Purpose: foto_veza_predmet cilja predmet tekstualnim parom
--   (database_name, inventarni_broj) — namerno polimorfno, ali promena ili
--   brisanje minerala ne ažurira ni ne uklanja vezu (ispravka M-123 -> M-124
--   ostavlja vezu na M-123). Za mineralošku zbirku ('mineral') dodaje se
--   nullable mineral_id FK sa eksplicitnim pravilima:
--     ON UPDATE CASCADE  — promena minerals.id prati vezu;
--     ON DELETE CASCADE  — brisanje minerala uklanja vezu (fotografija ostaje).
--   Tekstualni par ostaje za prikaz i za zbirke bez svoje tabele; aplikacija
--   (mineral_database_pg.update_mineral) sinhronizuje inventarni_broj u istoj
--   transakciji sa preimenovanjem minerala.

ALTER TABLE foto_veza_predmet ADD COLUMN IF NOT EXISTS mineral_id INTEGER;

ALTER TABLE foto_veza_predmet DROP CONSTRAINT IF EXISTS fk_foto_veza_predmet_mineral;
ALTER TABLE foto_veza_predmet ADD CONSTRAINT fk_foto_veza_predmet_mineral
    FOREIGN KEY (mineral_id) REFERENCES minerals(id)
    ON UPDATE CASCADE ON DELETE CASCADE;

CREATE INDEX IF NOT EXISTS idx_foto_veza_predmet_mineral_id
    ON foto_veza_predmet (mineral_id) WHERE mineral_id IS NOT NULL;

-- ============================================================================
-- Backfill postojećih veza mineraloške zbirke
-- ============================================================================

-- 1) Tačno poklapanje inventarnog broja.
UPDATE foto_veza_predmet v
SET mineral_id = m.id
FROM minerals m
WHERE v.mineral_id IS NULL
  AND v.database_name = 'mineral'
  AND m.inventory_number = v.inventarni_broj;

-- 2) Normalizovano poklapanje ('M 028' ~ 'M-28' ~ '28'): skini sve što nije
--    cifra i vodeće nule, upari SAMO kad je pogodak jednoznačan.
WITH kandidati AS (
    SELECT v.id AS veza_id,
           m.id AS mineral_id,
           COUNT(*) OVER (PARTITION BY v.id) AS pogodaka
    FROM foto_veza_predmet v
    JOIN minerals m
      ON NULLIF(ltrim(regexp_replace(upper(m.inventory_number), '[^0-9]', '', 'g'), '0'), '')
       = NULLIF(ltrim(regexp_replace(upper(v.inventarni_broj), '[^0-9]', '', 'g'), '0'), '')
    WHERE v.mineral_id IS NULL
      AND v.database_name = 'mineral'
)
UPDATE foto_veza_predmet v
SET mineral_id = k.mineral_id
FROM kandidati k
WHERE v.id = k.veza_id
  AND k.pogodaka = 1;

COMMENT ON COLUMN foto_veza_predmet.mineral_id IS
    'FK ka minerals za database_name=''mineral'' (ON UPDATE/DELETE CASCADE); NULL za druge zbirke i neuparene zapise';
