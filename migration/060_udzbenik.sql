-- 060: Интерактивни уџбеник — садржај по збирци (поглавља, лекције, историја
-- верзија, напредак читаоца). Мотор (Three.js читач) долази као готов bundle у
-- static/udzbenik/ и чита искључиво API из blueprints/udzbenik.py; садржај
-- лекције је JSONB по udzbenik/schema/lekcija.schema.json (валидација на
-- упису — scripts/udzbenik_uvoz.py). Кључ збирке је исти као у QR систему
-- (museum_qr.normalizuj_zbirku).
--
-- Нема BEGIN/COMMIT: трансакцију води deploy/run_migrations.py.

CREATE TABLE udzbenik (
    id            SERIAL PRIMARY KEY,
    zbirka        TEXT NOT NULL UNIQUE,              -- kanonski ključ kao u QR sistemu
    naslov        TEXT NOT NULL,
    opis          TEXT,
    status        TEXT NOT NULL DEFAULT 'nacrt' CHECK (status IN ('nacrt', 'objavljen')),
    javno         BOOLEAN NOT NULL DEFAULT FALSE,    -- posetioci bez prijave (kasnije)
    autor_email   TEXT,
    created_at    TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at    TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE udzbenik_poglavlje (
    id            SERIAL PRIMARY KEY,
    udzbenik_id   INTEGER NOT NULL REFERENCES udzbenik(id) ON DELETE CASCADE,
    redosled      INTEGER NOT NULL,
    slug          TEXT NOT NULL CHECK (slug ~ '^[a-z0-9][a-z0-9-]{1,59}$'),
    naslov        TEXT NOT NULL,
    opis          TEXT,
    UNIQUE (udzbenik_id, slug),
    UNIQUE (udzbenik_id, redosled)
);

CREATE TABLE udzbenik_lekcija (
    id            SERIAL PRIMARY KEY,
    poglavlje_id  INTEGER NOT NULL REFERENCES udzbenik_poglavlje(id) ON DELETE CASCADE,
    redosled      INTEGER NOT NULL,
    slug          TEXT NOT NULL CHECK (slug ~ '^[a-z0-9][a-z0-9-]{1,59}$'),
    naslov        TEXT NOT NULL,
    sazetak       TEXT,
    sadrzaj       JSONB NOT NULL,                    -- po udzbenik/schema/lekcija.schema.json
    verzija       INTEGER NOT NULL DEFAULT 1,
    status        TEXT NOT NULL DEFAULT 'nacrt' CHECK (status IN ('nacrt', 'objavljen')),
    azurirao_email TEXT,
    created_at    TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at    TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE (poglavlje_id, slug),
    UNIQUE (poglavlje_id, redosled)
);

CREATE TABLE udzbenik_lekcija_verzija (                -- istorija, osnova za uređivač
    id            SERIAL PRIMARY KEY,
    lekcija_id    INTEGER NOT NULL REFERENCES udzbenik_lekcija(id) ON DELETE CASCADE,
    verzija       INTEGER NOT NULL,
    sadrzaj       JSONB NOT NULL,
    autor_email   TEXT,
    napomena      TEXT,                              -- npr. 'uvoz iz primer-minerali.json'
    created_at    TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE (lekcija_id, verzija)
);

CREATE TABLE udzbenik_napredak (
    user_email    TEXT NOT NULL,
    lekcija_id    INTEGER NOT NULL REFERENCES udzbenik_lekcija(id) ON DELETE CASCADE,
    zavrseno      BOOLEAN NOT NULL DEFAULT FALSE,
    rezultat      JSONB,                             -- {tacno, ukupno, odgovori}
    updated_at    TIMESTAMPTZ NOT NULL DEFAULT now(),
    PRIMARY KEY (user_email, lekcija_id)
);

CREATE INDEX udzbenik_lekcija_poglavlje_idx ON udzbenik_lekcija (poglavlje_id, redosled);
CREATE INDEX udzbenik_napredak_lekcija_idx ON udzbenik_napredak (lekcija_id);

COMMENT ON TABLE udzbenik IS 'Interaktivni udžbenik po zbirci; motor u static/udzbenik/';
