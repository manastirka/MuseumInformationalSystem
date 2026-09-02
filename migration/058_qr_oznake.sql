-- 058: QR ознаке — један идентитет за примерак или кутију, независан од адресе
-- сервера. Ознака се додељује при првом штампању, не унапред. QR код носи
-- https://<qr_bazna_adresa>/q/<oznaka>; резолвер у blueprints/qr.py преводи
-- ознаку у детаље (пријављен) или јавну картицу (непријављен). Кутије
-- минералошке збирке задржавају и стари облик /qr_box/minerals/<kutija>, јер су
-- налепнице са њим већ залепљене.
--
-- Нема BEGIN/COMMIT: трансакцију води deploy/run_migrations.py.

CREATE TABLE IF NOT EXISTS qr_oznake (
    oznaka              TEXT PRIMARY KEY,
    vrsta               TEXT NOT NULL CHECK (vrsta IN ('primerak', 'kutija')),
    zbirka              TEXT NOT NULL,
    objekat_id          TEXT NOT NULL,
    napravio            TEXT NOT NULL,
    napravljeno_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
    stampano_puta       INTEGER NOT NULL DEFAULT 0,
    poslednje_stampano  TIMESTAMPTZ,
    poslednje_stampao   TEXT,
    CONSTRAINT ck_qr_oznake_oblik CHECK (oznaka ~ '^[0-9A-HJKMNP-TV-Z]{8}$'),
    CONSTRAINT ux_qr_oznake_objekat UNIQUE (vrsta, zbirka, objekat_id)
);

COMMENT ON TABLE qr_oznake IS
    'QR ознаке примерака и кутија; objekat_id је id записа, за кутију storage_location';
COMMENT ON COLUMN qr_oznake.oznaka IS
    '8 знакова Crockford base32 (без I, L, O, U) — штампа се и као текст испод кода';
