-- Migration: Naučne vesti u PostgreSQL (revizija 2026-08, krug 4, stavka 5)
-- Date: 2026-08-13
-- Purpose: data/science_news.json je bio izvor istine za kurirane naučne
--   vesti (ručne + RSS auto-fetch) — van backup-a baze, podložan gubitku i
--   konkurentnim prepisivanjima. Isti obrazac kao Sanja/Bilja (batch 6):
--   tabela + row-level CRUD, bez tihog fallback-a; JSON ostaje samo kao
--   razvojno/pre-migraciono stanje i uvozi se jednokratno alatom
--   scripts/migration/import_science_news_json.py.

CREATE TABLE IF NOT EXISTS science_news (
    id           TEXT PRIMARY KEY,
    datum        TEXT NOT NULL DEFAULT '',
    auto_fetched BOOLEAN NOT NULL DEFAULT FALSE,
    item         JSONB NOT NULL,
    created_at   TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS ix_science_news_datum
    ON science_news (datum DESC);

COMMENT ON TABLE science_news IS
    'Kurirane naučne vesti (ručne + RSS); item nosi ceo JSON zapis, datum/auto_fetched su radi sortiranja i orezivanja';
