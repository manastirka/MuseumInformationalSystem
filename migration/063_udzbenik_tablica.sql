-- 063: Референтне табеле уџбеника (UGOVOR-TABLICE.md §2). Табела је референтни
-- податак уз уџбеник (не лекција): пуни је исти scripts/udzbenik_uvoz.py из
-- кључа ``tablice`` JSON-а уџбеника; садржај (kolone, redovi, izvori, napomene)
-- је JSONB по udzbenik/schema/tablica.schema.json (валидација на упису). Upsert
-- по slug-у; промењен ``sadrzaj`` → verzija + 1 и ред у udzbenik_tablica_verzija.
-- Мотор их чита само кроз API (/api/udzbenik/<zbirka>/tablica/<slug>).
--
-- Нема BEGIN/COMMIT: трансакцију води deploy/run_migrations.py.

CREATE TABLE udzbenik_tablica (
    id             SERIAL PRIMARY KEY,
    udzbenik_id    INTEGER NOT NULL REFERENCES udzbenik(id) ON DELETE CASCADE,
    slug           TEXT NOT NULL CHECK (slug ~ '^[a-z0-9][a-z0-9-]{1,59}$'),
    redosled       INTEGER NOT NULL,
    naslov         TEXT NOT NULL,
    opis           TEXT,
    poglavlje_slug TEXT CHECK (poglavlje_slug ~ '^[a-z0-9][a-z0-9-]{1,59}$'),  -- груписање у списку; NULL = без поглавља
    status         TEXT NOT NULL DEFAULT 'nacrt' CHECK (status IN ('nacrt', 'objavljen')),
    sadrzaj        JSONB NOT NULL,                    -- po udzbenik/schema/tablica.schema.json
    verzija        INTEGER NOT NULL DEFAULT 1,
    azurirao_email TEXT,
    created_at     TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at     TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE (udzbenik_id, slug),
    UNIQUE (udzbenik_id, redosled)
);

CREATE TABLE udzbenik_tablica_verzija (               -- историја, као udzbenik_lekcija_verzija
    id             SERIAL PRIMARY KEY,
    tablica_id     INTEGER NOT NULL REFERENCES udzbenik_tablica(id) ON DELETE CASCADE,
    verzija        INTEGER NOT NULL,
    sadrzaj        JSONB NOT NULL,
    autor_email    TEXT,
    napomena       TEXT,                              -- нпр. 'uvoz: minerali.json'
    created_at     TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE (tablica_id, verzija)
);

COMMENT ON TABLE udzbenik_tablica IS
    'Референтне табеле уџбеника (просторне групе, оптичке константе…); садржај по tablica.schema.json';
COMMENT ON TABLE udzbenik_tablica_verzija IS 'Историја садржаја табела уџбеника (свака промена sadrzaj-а при увозу)';
