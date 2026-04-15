-- ============================================================================
-- Bilja: Paleozoology — Kenozoic Invertebrates Inventory
-- ============================================================================
-- Source:  Bilja/Copy of KENOZOJSKE INVERTEBRATE INVENTARSKA KNJIGA ... .xlsx
-- Records: 575 rows, stratigraphy: Kvartar/Diluvium
-- Category: geology / paleozoology
-- ============================================================================

CREATE TABLE IF NOT EXISTS bilja_kenozojske_invertebrate (
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
    stratigrafski_nivo TEXT,
    datum_nalaska TEXT,
    nalazac TEXT,
    odredba TEXT,
    napomena TEXT,
    dimenzije TEXT,
    broj_primeraka TEXT,
    source_file TEXT,
    created_at TIMESTAMPTZ DEFAULT now(),
    updated_at TIMESTAMPTZ DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_kenozojske_inv_inv_broj
    ON bilja_kenozojske_invertebrate(inventarski_broj);
CREATE INDEX IF NOT EXISTS idx_kenozojske_inv_klasa
    ON bilja_kenozojske_invertebrate(klasa);
CREATE INDEX IF NOT EXISTS idx_kenozojske_inv_familija
    ON bilja_kenozojske_invertebrate(familija);
CREATE INDEX IF NOT EXISTS idx_kenozojske_inv_lokalitet
    ON bilja_kenozojske_invertebrate(lokalitet);
CREATE INDEX IF NOT EXISTS idx_kenozojske_inv_stratigrafija
    ON bilja_kenozojske_invertebrate(stratigrafski_nivo);
CREATE INDEX IF NOT EXISTS idx_kenozojske_inv_vrsta_search
    ON bilja_kenozojske_invertebrate USING gin(to_tsvector('simple', coalesce(vrsta, '')));

COMMENT ON TABLE bilja_kenozojske_invertebrate IS
    'Kenozojske invertebrate inventarska knjiga — fosilni invertebrati (kvartar/diluvium). Kategorija: paleozoologija.';
