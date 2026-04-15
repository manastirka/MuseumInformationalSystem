-- ============================================================================
-- Bilja: Biology — Recent Mollusc Collections
-- ============================================================================
-- Sources (folder Bilja/):
--   - PAVLE RADOMAN HYDROBIOIDEA PROBA.xlsx             (388 rows, 25 cols)
--   - Zbirka  suvozemnih puzeva P S Pavlovic ... .xlsx  (Sheet1:  2486 rows, 20 cols)
--   - Zbirka  suvozemnih puzeva P S Pavlovic ... .xlsx  (Opsta zbirka Mollusca: 245 rows, 20 cols)
--   - Zbirka Skoljki Ante Tadic zavrseno.xls            (168 rows, 23 cols)
--   - РЕЦЕНТНИ МОРСКИ МЕКУШЦИ.xlsx                      (246 rows, 21 cols)
-- Category: biology (recent / living specimens)
-- ============================================================================

-- ---------------------------------------------------------------------------
-- 1) Radoman Hydrobioidea (type specimens, brackish/freshwater gastropods)
-- ---------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS bilja_hydrobioidea_radoman (
    id SERIAL PRIMARY KEY,
    redni_broj INTEGER,
    inventarski_broj TEXT,
    klasa TEXT,
    red TEXT,
    familija TEXT,
    rod TEXT,
    vrsta TEXT,
    tipska_vrsta TEXT,
    sinonim TEXT,
    lokalitet TEXT,
    rasprostranjenost TEXT,
    datum_nalaska TEXT,
    broj_primeraka TEXT,
    holotip TEXT,
    paratip TEXT,
    lektotip TEXT,
    paralektotip TEXT,
    dimenzije_ljusture TEXT,
    ekoloske_osobine TEXT,
    legator TEXT,
    odredba TEXT,
    zbirka_orman_kutija TEXT,
    ugrozenost TEXT,
    napomena TEXT,
    literatura TEXT,
    source_file TEXT,
    created_at TIMESTAMPTZ DEFAULT now(),
    updated_at TIMESTAMPTZ DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_radoman_inv_broj ON bilja_hydrobioidea_radoman(inventarski_broj);
CREATE INDEX IF NOT EXISTS idx_radoman_familija ON bilja_hydrobioidea_radoman(familija);
CREATE INDEX IF NOT EXISTS idx_radoman_rod ON bilja_hydrobioidea_radoman(rod);
CREATE INDEX IF NOT EXISTS idx_radoman_lokalitet ON bilja_hydrobioidea_radoman(lokalitet);
CREATE INDEX IF NOT EXISTS idx_radoman_holotip ON bilja_hydrobioidea_radoman(holotip) WHERE holotip IS NOT NULL;

COMMENT ON TABLE bilja_hydrobioidea_radoman IS
    'Hydrobioidea zbirka Pavla Radomana — recentni gastropodi, tipski primerci. Kategorija: biologija.';

-- ---------------------------------------------------------------------------
-- 2) Pavlović — Suvozemni puževi (land snails)
-- ---------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS bilja_suvozemni_puzevi_pavlovic (
    id SERIAL PRIMARY KEY,
    redni_broj INTEGER,
    inventarski_broj TEXT,
    klasa TEXT,
    red TEXT,
    familija TEXT,
    rod TEXT,
    vrsta TEXT,
    sinonim TEXT,
    lokalitet TEXT,
    rasprostranjenost TEXT,
    datum_nalaska TEXT,
    broj_primeraka TEXT,
    dimenzije_ljusture TEXT,
    ekoloske_osobine TEXT,
    ps_pavlovic TEXT,
    odredba TEXT,
    zbirka_orman_kutija TEXT,
    ugrozenost TEXT,
    napomena TEXT,
    literatura TEXT,
    source_file TEXT,
    created_at TIMESTAMPTZ DEFAULT now(),
    updated_at TIMESTAMPTZ DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_pavlovic_inv_broj ON bilja_suvozemni_puzevi_pavlovic(inventarski_broj);
CREATE INDEX IF NOT EXISTS idx_pavlovic_familija ON bilja_suvozemni_puzevi_pavlovic(familija);
CREATE INDEX IF NOT EXISTS idx_pavlovic_rod ON bilja_suvozemni_puzevi_pavlovic(rod);
CREATE INDEX IF NOT EXISTS idx_pavlovic_lokalitet ON bilja_suvozemni_puzevi_pavlovic(lokalitet);
CREATE INDEX IF NOT EXISTS idx_pavlovic_vrsta_search
    ON bilja_suvozemni_puzevi_pavlovic USING gin(to_tsvector('simple', coalesce(vrsta, '')));

COMMENT ON TABLE bilja_suvozemni_puzevi_pavlovic IS
    'Zbirka suvozemnih puževa P. S. Pavlovića — recentni gastropodi. Kategorija: biologija.';

-- ---------------------------------------------------------------------------
-- 3) Opšta zbirka Mollusca (general mollusc collection, mixed donors)
-- ---------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS bilja_opsta_zbirka_mollusca (
    id SERIAL PRIMARY KEY,
    redni_broj INTEGER,
    inventarski_broj TEXT,
    klasa TEXT,
    red TEXT,
    familija TEXT,
    rod TEXT,
    vrsta TEXT,
    sinonim TEXT,
    lokalitet TEXT,
    rasprostranjenost TEXT,
    datum_nalaska TEXT,
    broj_primeraka TEXT,
    dimenzije_ljusture TEXT,
    ekoloske_osobine TEXT,
    ps_pavlovic TEXT,
    odredba TEXT,
    zbirka_orman_kutija TEXT,
    ugrozenost TEXT,
    napomena TEXT,
    literatura TEXT,
    source_file TEXT,
    created_at TIMESTAMPTZ DEFAULT now(),
    updated_at TIMESTAMPTZ DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_opsta_moll_inv_broj ON bilja_opsta_zbirka_mollusca(inventarski_broj);
CREATE INDEX IF NOT EXISTS idx_opsta_moll_familija ON bilja_opsta_zbirka_mollusca(familija);
CREATE INDEX IF NOT EXISTS idx_opsta_moll_klasa ON bilja_opsta_zbirka_mollusca(klasa);
CREATE INDEX IF NOT EXISTS idx_opsta_moll_lokalitet ON bilja_opsta_zbirka_mollusca(lokalitet);

COMMENT ON TABLE bilja_opsta_zbirka_mollusca IS
    'Opšta zbirka mekušaca (Bivalvia/Gastropoda, razni sakupljači). Kategorija: biologija.';

-- ---------------------------------------------------------------------------
-- 4) Ante Tadić — Zbirka školjki (bivalves, Unio etc.)
-- ---------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS bilja_skoljke_tadic (
    id SERIAL PRIMARY KEY,
    redni_broj INTEGER,
    inventarski_broj TEXT,
    klasa TEXT,
    red TEXT,
    familija TEXT,
    rod TEXT,
    vrsta TEXT,
    podvrsta TEXT,
    sinonim TEXT,
    lokalitet TEXT,
    datum_nalaska TEXT,
    broj_primeraka TEXT,
    broj_levih_kapaka TEXT,
    broj_desnih_kapaka TEXT,
    boja_ljusture_forel_ule TEXT,
    dimenzije_kapka TEXT,
    tip_brave TEXT,
    ekoloske_osobine TEXT,
    sakupljac TEXT,
    odredba TEXT,
    zbirka_orman_kutija TEXT,
    napomena TEXT,
    literatura TEXT,
    source_file TEXT,
    created_at TIMESTAMPTZ DEFAULT now(),
    updated_at TIMESTAMPTZ DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_tadic_inv_broj ON bilja_skoljke_tadic(inventarski_broj);
CREATE INDEX IF NOT EXISTS idx_tadic_familija ON bilja_skoljke_tadic(familija);
CREATE INDEX IF NOT EXISTS idx_tadic_vrsta ON bilja_skoljke_tadic(vrsta);
CREATE INDEX IF NOT EXISTS idx_tadic_lokalitet ON bilja_skoljke_tadic(lokalitet);

COMMENT ON TABLE bilja_skoljke_tadic IS
    'Zbirka školjki Ante Tadića — recentni slatkovodni bivalvi (Unio i dr.). Kategorija: biologija.';

-- ---------------------------------------------------------------------------
-- 5) Recentni morski mekušci
-- ---------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS bilja_recentni_morski_mekusci (
    id SERIAL PRIMARY KEY,
    redni_broj INTEGER,
    inventarski_broj TEXT,
    klasa TEXT,
    red TEXT,
    familija TEXT,
    rod TEXT,
    vrsta TEXT,
    sinonim TEXT,
    lokalitet TEXT,
    rasprostranjenost TEXT,
    datum_nalaska TEXT,
    broj_primeraka TEXT,
    izbrojan_broj_primeraka TEXT,
    dimenzije_ljusture TEXT,
    ekoloske_osobine TEXT,
    ps_pavlovic TEXT,
    odredba TEXT,
    zbirka_orman_kutija TEXT,
    ugrozenost TEXT,
    napomena TEXT,
    literatura TEXT,
    source_file TEXT,
    created_at TIMESTAMPTZ DEFAULT now(),
    updated_at TIMESTAMPTZ DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_morski_inv_broj ON bilja_recentni_morski_mekusci(inventarski_broj);
CREATE INDEX IF NOT EXISTS idx_morski_klasa ON bilja_recentni_morski_mekusci(klasa);
CREATE INDEX IF NOT EXISTS idx_morski_familija ON bilja_recentni_morski_mekusci(familija);
CREATE INDEX IF NOT EXISTS idx_morski_lokalitet ON bilja_recentni_morski_mekusci(lokalitet);

COMMENT ON TABLE bilja_recentni_morski_mekusci IS
    'Recentni morski mekušci (Bivalvia + Gastropoda). Kategorija: biologija.';
