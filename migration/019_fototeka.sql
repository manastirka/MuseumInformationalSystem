-- ============================================================================
-- Migration 019: Фототека (самосталне фотографије, тагови, везе, ред послова)
-- ============================================================================
-- Date: July 2026
-- A photograph is a first-class object; links to collection items, field
-- trips, projects and exhibitions are optional (zero or more). Three layers:
-- RAW originals live under FOTOTEKA_ARHIVA_PATH (production: /data/arhiva,
-- write-once, the application never modifies them), derivatives (~2500px jpg
-- + ~300px thumb) under FOTOTEKA_MEDIA_PATH (production: /data/mis/media,
-- regenerable — their paths are a pure function of sha256, so they have no
-- columns here), and this schema holds metadata, tags, links and the job
-- queue consumed by the dedicated derivative worker (fototeka_worker.py).
-- Safe to run repeatedly (IF NOT EXISTS everywhere).
-- ============================================================================

CREATE TABLE IF NOT EXISTS fotografije (
    id SERIAL PRIMARY KEY,
    sha256 CHAR(64) NOT NULL UNIQUE,
    raw_putanja TEXT NOT NULL UNIQUE,
    original_ime TEXT NOT NULL,
    ekstenzija TEXT,
    velicina_bajtova BIGINT,
    width INTEGER,
    height INTEGER,
    autor_email TEXT NOT NULL,
    datum_snimanja DATE,
    exif JSONB,
    opis TEXT,
    poreklo TEXT NOT NULL CHECK (poreklo IN ('upload', 'import')),
    status TEXT NOT NULL DEFAULT 'primljena' CHECK (status IN (
        'primljena', 'obrada', 'spremna', 'greska'
    )),
    u_prijemnom_redu BOOLEAN NOT NULL DEFAULT FALSE,
    obrisana BOOLEAN NOT NULL DEFAULT FALSE,
    fixity_proveren_at TIMESTAMPTZ,
    fixity_ok BOOLEAN,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

COMMENT ON TABLE fotografije IS
    'Photo registry; raw_putanja is relative to FOTOTEKA_ARHIVA_PATH and is written once at intake — later linking never moves the RAW file';

CREATE TABLE IF NOT EXISTS fotografija_tagovi (
    id SERIAL PRIMARY KEY,
    fotografija_id INTEGER NOT NULL REFERENCES fotografije(id) ON DELETE CASCADE,
    tag TEXT NOT NULL,
    UNIQUE (fotografija_id, tag)
);

COMMENT ON TABLE fotografija_tagovi IS
    'Free-form tags; no separate tag dictionary — autocomplete works off SELECT DISTINCT';

-- Link-target registries for entities that have no table of their own yet.
CREATE TABLE IF NOT EXISTS fototeka_tereni (
    id SERIAL PRIMARY KEY,
    godina SMALLINT NOT NULL,
    naziv TEXT NOT NULL,
    created_by_email TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE (godina, naziv)
);

COMMENT ON TABLE fototeka_tereni IS
    'Field-trip registry mirroring the RAW layout teren/<godina>/<akcija>/';

CREATE TABLE IF NOT EXISTS fototeka_projekti (
    id SERIAL PRIMARY KEY,
    naziv TEXT NOT NULL UNIQUE,
    created_by_email TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

COMMENT ON TABLE fototeka_projekti IS
    'Lightweight project registry until a real project module exists in the DB';

-- Explicit per-type link tables (a deliberate choice over one polymorphic
-- table): FK integrity where the target is a real table, typed columns where
-- collection items are addressed as (database_name, inventory number) across
-- several collection tables.
CREATE TABLE IF NOT EXISTS foto_veza_predmet (
    id SERIAL PRIMARY KEY,
    fotografija_id INTEGER NOT NULL REFERENCES fotografije(id) ON DELETE CASCADE,
    database_name TEXT NOT NULL,
    inventarni_broj TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE (fotografija_id, database_name, inventarni_broj)
);

CREATE TABLE IF NOT EXISTS foto_veza_teren (
    id SERIAL PRIMARY KEY,
    fotografija_id INTEGER NOT NULL REFERENCES fotografije(id) ON DELETE CASCADE,
    teren_id INTEGER NOT NULL REFERENCES fototeka_tereni(id) ON DELETE CASCADE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE (fotografija_id, teren_id)
);

CREATE TABLE IF NOT EXISTS foto_veza_projekat (
    id SERIAL PRIMARY KEY,
    fotografija_id INTEGER NOT NULL REFERENCES fotografije(id) ON DELETE CASCADE,
    projekat_id INTEGER NOT NULL REFERENCES fototeka_projekti(id) ON DELETE CASCADE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE (fotografija_id, projekat_id)
);

CREATE TABLE IF NOT EXISTS foto_veza_izlozba (
    id SERIAL PRIMARY KEY,
    fotografija_id INTEGER NOT NULL REFERENCES fotografije(id) ON DELETE CASCADE,
    exhibition_id INTEGER NOT NULL REFERENCES exhibitions(id) ON DELETE CASCADE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE (fotografija_id, exhibition_id)
);

-- Job queue for the dedicated worker (FOR UPDATE SKIP LOCKED consumer).
CREATE TABLE IF NOT EXISTS foto_poslovi (
    id SERIAL PRIMARY KEY,
    fotografija_id INTEGER NOT NULL REFERENCES fotografije(id) ON DELETE CASCADE,
    tip TEXT NOT NULL CHECK (tip IN ('derivati', 'fixity')),
    status TEXT NOT NULL DEFAULT 'ceka' CHECK (status IN (
        'ceka', 'radi', 'uspeh', 'greska'
    )),
    pokusaji INTEGER NOT NULL DEFAULT 0,
    sledeci_pokusaj_at TIMESTAMPTZ,
    zakljucan_at TIMESTAMPTZ,
    zakljucao TEXT,
    poslednja_greska TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

COMMENT ON TABLE foto_poslovi IS
    'DB-backed job queue; a stuck ''radi'' row older than the reclaim window is returned to ''ceka'' by the worker';

CREATE INDEX IF NOT EXISTS idx_fotografije_autor_email ON fotografije (autor_email);
CREATE INDEX IF NOT EXISTS idx_fotografije_datum_snimanja ON fotografije (datum_snimanja);
CREATE INDEX IF NOT EXISTS idx_fotografije_status ON fotografije (status);
CREATE INDEX IF NOT EXISTS idx_fotografije_prijemni_red ON fotografije (u_prijemnom_redu) WHERE u_prijemnom_redu;
CREATE INDEX IF NOT EXISTS idx_fotografija_tagovi_tag ON fotografija_tagovi (lower(tag));
CREATE INDEX IF NOT EXISTS idx_foto_veza_predmet_meta ON foto_veza_predmet (database_name, inventarni_broj);
CREATE INDEX IF NOT EXISTS idx_foto_veza_teren_teren_id ON foto_veza_teren (teren_id);
CREATE INDEX IF NOT EXISTS idx_foto_veza_projekat_projekat_id ON foto_veza_projekat (projekat_id);
CREATE INDEX IF NOT EXISTS idx_foto_veza_izlozba_exhibition_id ON foto_veza_izlozba (exhibition_id);
CREATE INDEX IF NOT EXISTS idx_foto_poslovi_red ON foto_poslovi (status, sledeci_pokusaj_at);

-- Rollback:
-- DROP TABLE IF EXISTS foto_poslovi;
-- DROP TABLE IF EXISTS foto_veza_izlozba;
-- DROP TABLE IF EXISTS foto_veza_projekat;
-- DROP TABLE IF EXISTS foto_veza_teren;
-- DROP TABLE IF EXISTS foto_veza_predmet;
-- DROP TABLE IF EXISTS fototeka_projekti;
-- DROP TABLE IF EXISTS fototeka_tereni;
-- DROP TABLE IF EXISTS fotografija_tagovi;
-- DROP TABLE IF EXISTS fotografije;
