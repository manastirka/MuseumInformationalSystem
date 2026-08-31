-- Migration: Red za pregled vesti nadjenih na vebu
-- Date: 2026-08-31
-- Purpose: Automatska pretraga (Google News / Bing News RSS) nalazi i vesti o
--   DRUGIM muzejima istog generickog imena — "Природњачки музеј у Свилајнцу",
--   "у срцу Каблара" i tako dalje. Nijedno bodovanje relevantnosti to ne moze
--   savrseno da odvoji, pa nadjene vesti NE ulaze pravo medju vesti muzeja
--   nego u ovaj red: kustos odobri ili odbaci, i tek odobrene postaju vest.
--
--   Odbacene ostaju u tabeli (status='odbaceno') da ih sledeca pretraga ne bi
--   ponovo nudila. Brisanje reda bi znacilo da se ista vest vraca svaki dan.

CREATE TABLE IF NOT EXISTS news_web_kandidati (
    id            BIGSERIAL PRIMARY KEY,
    kljuc         TEXT        NOT NULL,
    url           TEXT        NOT NULL,
    naslov        TEXT        NOT NULL,
    izvod         TEXT,
    izvor_naziv   TEXT,
    objavljeno    TIMESTAMPTZ,
    slika_url     TEXT,
    upit          TEXT,
    pretrazivac   TEXT        NOT NULL,
    ocena         INTEGER     NOT NULL DEFAULT 0,
    razlog        TEXT,
    status        TEXT        NOT NULL DEFAULT 'na_cekanju',
    odluku_doneo  TEXT,
    odluceno_at   TIMESTAMPTZ,
    vest_id       INTEGER     REFERENCES news_articles(id) ON DELETE SET NULL,
    nadjeno_at    TIMESTAMPTZ NOT NULL DEFAULT now(),
    CONSTRAINT news_web_kandidati_status_chk
        CHECK (status IN ('na_cekanju', 'odobreno', 'odbaceno'))
);

-- kljuc je normalizovan naslov (mala slova, bez interpunkcije, bez imena
-- medija na kraju). Isti clanak stize i preko Google-a i preko Bing-a sa
-- razlicitim URL-ovima, pa dedup ide po naslovu a ne po adresi.
CREATE UNIQUE INDEX IF NOT EXISTS ux_news_web_kandidati_kljuc
    ON news_web_kandidati (kljuc);

CREATE INDEX IF NOT EXISTS ix_news_web_kandidati_status
    ON news_web_kandidati (status, ocena DESC, objavljeno DESC);

COMMENT ON TABLE news_web_kandidati IS
    'Vesti nadjene automatskom pretragom veba — cekaju odluku kustosa';
COMMENT ON COLUMN news_web_kandidati.kljuc IS
    'Normalizovan naslov; jedinstven, sluzi za dedup izmedju pretrazivaca i pokretanja';
COMMENT ON COLUMN news_web_kandidati.razlog IS
    'Koji pojmovi su dali bodove — kustos vidi zasto mu je vest ponudjena';
COMMENT ON COLUMN news_web_kandidati.status IS
    'na_cekanju | odobreno (napravljena vest, vidi vest_id) | odbaceno (vise se ne nudi)';

-- Odobren kandidat postaje red u news_articles sa izvor='veb'. Za razliku od
-- 'nhmbeo' redova, njih nijedan automatski posao ne prepisuje, pa ih kustos
-- sme i da menja (npr. da skrati izvod).
DO $$
BEGIN
    ALTER TABLE news_articles DROP CONSTRAINT IF EXISTS news_articles_izvor_chk;
    ALTER TABLE news_articles
        ADD CONSTRAINT news_articles_izvor_chk
        CHECK (izvor IN ('rucni', 'nhmbeo', 'veb'));
END
$$;
