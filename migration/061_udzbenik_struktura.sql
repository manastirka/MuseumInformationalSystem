-- 061: Кристалне структуре за уџбеник — један извор истине је БАЗА, не фајлови.
-- GET /api/udzbenik/struktura/<mineral> је враћао 503 на DEV-у и PROD-у јер
-- cif_strukture() чита локални RRUFF_data/ којег нема ни на једној машини; свих
-- 30 блокова `scena: kristalna-struktura` падало је на резервну слику.
-- Пуни се скриптом scripts/udzbenik_strukture_cod.py (Crystallography Open
-- Database, CIF проширен у P1 — облик који мотор очекује). RRUFF остаје само
-- као резервни извор кад директоријум постоји.
--
-- Нема BEGIN/COMMIT: трансакцију води deploy/run_migrations.py.

CREATE TABLE udzbenik_struktura (
    id            SERIAL PRIMARY KEY,
    mineral       TEXT NOT NULL UNIQUE CHECK (mineral ~ '^[a-z0-9][a-z0-9-]{1,59}$'),  -- slug као у scena.parametri.mineral
    naziv_en      TEXT NOT NULL,                      -- енглески назив (упит мотора може бити и енглески)
    izvor         TEXT NOT NULL DEFAULT 'COD' CHECK (izvor IN ('COD')),
    cod_id        INTEGER NOT NULL CHECK (cod_id > 0),
    cif_izvorni   TEXT NOT NULL,                      -- CIF како је преузет (навод, оператори, асиметрична јединица)
    cif_p1        TEXT NOT NULL,                      -- проширено у P1 — ово служи API
    citat         JSONB NOT NULL DEFAULT '{}'::jsonb, -- autori[], godina, casopis, tom, strane, doi, naslov, amcsd
    uslovi        JSONB NOT NULL DEFAULT '{}'::jsonb, -- temperatura_k, pritisak_kpa (null = није наведено = амбијент)
    uvezeno_at    TIMESTAMPTZ NOT NULL DEFAULT now(),
    uvezao        TEXT
);

COMMENT ON TABLE udzbenik_struktura IS
    'Кристалне структуре (COD → P1 CIF) за scena: kristalna-struktura у уџбенику; пуни scripts/udzbenik_strukture_cod.py';
