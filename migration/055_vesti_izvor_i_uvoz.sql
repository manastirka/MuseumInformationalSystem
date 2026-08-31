-- Migration: Izvor vesti i automatski uvoz sa sajta muzeja
-- Date: 2026-08-31
-- Purpose: news_articles je do sada bio samo rucni unos, a prikaz je citao
--   NEWS_DATABASE (LazyLoadedDict) — kes u procesu, pa je pod gunicorn-om sa
--   vise radnika svaki radnik video svoje stanje. Ova migracija dodaje polja
--   koja razlikuju rucni unos od uvoza sa nhmbeo.rs (WordPress REST API) i
--   tabelu za trag svakog uvoza, da otkaz uvoza nikad ne prodje tiho.
--
--   izvor='rucni'  — unos kroz aplikaciju, kustos ga menja i brise
--   izvor='nhmbeo' — uvezeno sa sajta; upsert po (izvor, spoljni_id), rucna
--                    izmena nije dozvoljena jer bi je sledeci uvoz pregazio

ALTER TABLE news_articles
    ADD COLUMN IF NOT EXISTS izvor             TEXT NOT NULL DEFAULT 'rucni',
    ADD COLUMN IF NOT EXISTS spoljni_id        TEXT,
    ADD COLUMN IF NOT EXISTS slika_url         TEXT,
    ADD COLUMN IF NOT EXISTS autor             TEXT,
    ADD COLUMN IF NOT EXISTS sadrzaj_tekst     TEXT,
    ADD COLUMN IF NOT EXISTS spoljni_izmenjen  TIMESTAMPTZ,
    ADD COLUMN IF NOT EXISTS uvezeno_at        TIMESTAMPTZ;

-- Postojecih 115 zapisa su svi rucni; DEFAULT ih vec pokriva, ovo je samo
-- eksplicitna potvrda za slucaj da je kolona ranije dodata bez default-a.
UPDATE news_articles SET izvor = 'rucni' WHERE izvor IS NULL OR izvor = '';

DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM pg_constraint WHERE conname = 'news_articles_izvor_chk'
    ) THEN
        ALTER TABLE news_articles
            ADD CONSTRAINT news_articles_izvor_chk
            CHECK (izvor IN ('rucni', 'nhmbeo'));
    END IF;
END
$$;

-- Jedan red po spoljnoj objavi: uvoz radi ON CONFLICT nad ovim indeksom.
CREATE UNIQUE INDEX IF NOT EXISTS ux_news_articles_spoljni
    ON news_articles (izvor, spoljni_id)
    WHERE spoljni_id IS NOT NULL;

CREATE INDEX IF NOT EXISTS ix_news_articles_izvor
    ON news_articles (izvor);

COMMENT ON COLUMN news_articles.izvor IS
    'rucni = unos kroz aplikaciju; nhmbeo = uvezeno sa nhmbeo.rs, ne menja se rucno';
COMMENT ON COLUMN news_articles.spoljni_id IS
    'ID objave u izvornom sistemu (WordPress post id za nhmbeo)';
COMMENT ON COLUMN news_articles.spoljni_izmenjen IS
    'WordPress modified — po njemu uvoz zna da li je objava promenjena';

-- Trag svakog pokretanja uvoza. Bez ovoga tihi otkaz mrezne veze izgleda
-- isto kao "nema novih vesti", pa korisnik gleda zastarelu stranu bez znaka.
CREATE TABLE IF NOT EXISTS news_import_log (
    id            BIGSERIAL PRIMARY KEY,
    izvor         TEXT        NOT NULL,
    pokrenuto_at  TIMESTAMPTZ NOT NULL DEFAULT now(),
    zavrseno_at   TIMESTAMPTZ,
    status        TEXT        NOT NULL DEFAULT 'u_toku',
    novih         INTEGER     NOT NULL DEFAULT 0,
    azuriranih    INTEGER     NOT NULL DEFAULT 0,
    pregledano    INTEGER     NOT NULL DEFAULT 0,
    poruka        TEXT,
    pokrenuo      TEXT,
    CONSTRAINT news_import_log_status_chk
        CHECK (status IN ('u_toku', 'uspeh', 'delimicno', 'greska'))
);

CREATE INDEX IF NOT EXISTS ix_news_import_log_pokrenuto
    ON news_import_log (izvor, pokrenuto_at DESC);

COMMENT ON TABLE news_import_log IS
    'Trag svakog uvoza vesti — strana prikazuje vreme i ishod poslednjeg pokretanja';
