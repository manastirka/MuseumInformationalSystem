-- 065: Видео клипови уџбеника (блок ``video``). Једини извор истине о клипу
-- је овај ред: путања, sha256, трајање, постер, опис и ознака AI. Фајлови
-- НИСУ у git-у ни у бази — леже у FOTOTEKA_MEDIA_PATH/udzbenik-video/
-- (адресирани садржајем, ``<sha[:2]>/<sha>.mp4|.jpg``) и испоручују се истим
-- путем као деривати Фототеке (send_file са Range, или X-Accel-Redirect
-- /_zasticeno/derivati/ кад је FOTOTEKA_XACCEL укључен).
-- Упис само кроз scripts/udzbenik_uvoz.py (кључ ``videi`` у JSON-у).
--
-- Нема BEGIN/COMMIT: трансакцију води deploy/run_migrations.py.

CREATE TABLE udzbenik_video (
    id              SERIAL PRIMARY KEY,
    udzbenik_id     INTEGER NOT NULL REFERENCES udzbenik(id) ON DELETE CASCADE,
    kljuc           TEXT NOT NULL UNIQUE CHECK (kljuc ~ '^[a-z0-9]+(-[a-z0-9]+)*$' AND length(kljuc) <= 80),
    putanja         TEXT NOT NULL,                   -- релативно у FOTOTEKA_MEDIA_PATH
    sha256          CHAR(64) NOT NULL CHECK (sha256 ~ '^[0-9a-f]{64}$'),
    velicina_b      BIGINT NOT NULL CHECK (velicina_b > 0),
    mime            TEXT NOT NULL DEFAULT 'video/mp4' CHECK (mime IN ('video/mp4', 'video/webm')),
    trajanje_s      NUMERIC(8, 2) NOT NULL CHECK (trajanje_s > 0),
    sirina_px       INTEGER NOT NULL CHECK (sirina_px > 0),
    visina_px       INTEGER NOT NULL CHECK (visina_px > 0),
    zvuk            BOOLEAN NOT NULL DEFAULT false,
    poster_putanja  TEXT NOT NULL,
    poster_sha256   CHAR(64) NOT NULL CHECK (poster_sha256 ~ '^[0-9a-f]{64}$'),
    opis            TEXT NOT NULL CHECK (length(opis) BETWEEN 1 AND 500),
    ai              BOOLEAN NOT NULL DEFAULT false,
    oznaka          TEXT,
    autor           TEXT,
    licenca         TEXT,
    uvezao_email    TEXT,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
    CHECK (NOT ai OR (oznaka IS NOT NULL AND length(oznaka) > 0))
);

CREATE INDEX udzbenik_video_udzbenik_idx ON udzbenik_video (udzbenik_id);

COMMENT ON TABLE udzbenik_video IS
    'Видео клипови уџбеника (блок video): метаподаци и путања у FOTOTEKA_MEDIA_PATH/udzbenik-video; AI клип мора имати ознаку';
