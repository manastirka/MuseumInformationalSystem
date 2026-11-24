-- 066: Контекст локалитета из Google Earth Engine (свеске 12-kontekst-lokaliteta
-- и 13-bio-stanista у /tmp/petro/colab/). Један ред по објекту: примерак
-- (minerals.id) или локалитет из шифарника (localities.id) → надморска висина,
-- нагиб, покривач земљишта (Dynamic World), лист OGK 1:100 000, а из свеске 13
-- шума 2000. и њен губитак (Hansen GFC) и удели класа Dynamic World у кругу 1 km.
-- Свеске рачунају кустос ван MIS-а; упис САМО кроз
-- scripts/kontekst_lokaliteta_uvoz.py (CSV, dry-run, --execute <име базе>).
-- Без FK: vrsta одређује табелу (као museum_qr), постојање провери увоз.
--
-- Нема BEGIN/COMMIT: трансакцију води deploy/run_migrations.py.

CREATE TABLE lokalitet_kontekst (
    id                  SERIAL PRIMARY KEY,
    vrsta               TEXT NOT NULL CHECK (vrsta IN ('mineral', 'lokalitet')),
    objekat_id          INTEGER NOT NULL CHECK (objekat_id > 0),
    lat                 DOUBLE PRECISION NOT NULL CHECK (lat BETWEEN -90 AND 90),
    lon                 DOUBLE PRECISION NOT NULL CHECK (lon BETWEEN -180 AND 180),
    -- свеска 12
    nadmorska_visina_m  REAL,
    nagib_stepeni       REAL CHECK (nagib_stepeni BETWEEN 0 AND 90),
    pokrivac_klasa      SMALLINT CHECK (pokrivac_klasa BETWEEN 0 AND 8),
    pokrivac_godina     SMALLINT,
    ogk_list            TEXT CHECK (ogk_list ~ '^[KL]34-[0-9]{2,3}$'),
    izvor               TEXT,
    datum_izracuna      DATE,
    -- свеска 13
    suma_2000_pct       REAL CHECK (suma_2000_pct BETWEEN 0 AND 100),
    gubitak_sume_ha     REAL CHECK (gubitak_sume_ha >= 0),
    gubitak_sume_pct    REAL CHECK (gubitak_sume_pct BETWEEN 0 AND 100),
    gubitak_od          SMALLINT,
    gubitak_do          SMALLINT,
    dw_udeli            JSONB,
    dw_godina           SMALLINT,
    bio_izvor           TEXT,
    bio_datum_izracuna  DATE,
    uvezao_email        TEXT,
    created_at          TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at          TIMESTAMP NOT NULL DEFAULT NOW(),
    UNIQUE (vrsta, objekat_id),
    CHECK (gubitak_od IS NULL OR gubitak_do IS NULL OR gubitak_od <= gubitak_do)
);

COMMENT ON TABLE lokalitet_kontekst IS
    'GEE context per specimen/locality (DEM, slope, Dynamic World, OGK sheet, Hansen GFC); import via scripts/kontekst_lokaliteta_uvoz.py';
COMMENT ON COLUMN lokalitet_kontekst.pokrivac_klasa IS
    'Dynamic World V1 label: 0 water, 1 trees, 2 grass, 3 flooded_vegetation, 4 crops, 5 shrub_and_scrub, 6 built, 7 bare, 8 snow_and_ice';
COMMENT ON COLUMN lokalitet_kontekst.ogk_list IS
    'OGK 1:100 000 sheet from the nominal grid (approximate within ~200 m of a sheet edge)';
COMMENT ON COLUMN lokalitet_kontekst.dw_udeli IS
    'Share (%) of Dynamic World modal classes within 1 km, keys = DW class names';
