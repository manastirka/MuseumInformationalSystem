-- ============================================================================
-- Migration 030: Конзерваторско-рестаураторски досије (K-R досије)
-- ============================================================================
-- Date: July 2026
-- Конзерватори воде званичну документацију о захватима на предметима. Досад је
-- то био Excel (геолошко одељење: 2 године, ~58 стварних записа + 172 слике).
-- Овај модул то формализује: један ДОСИЈЕ по захвату, са три описа стања
-- (пре / поступак и материјали / после), више ИЗВРШИЛАЦА, периодом рада и
-- везом на предмет из збирке ИЛИ слободним уносом (спољни предмети —
-- Музеј Југославије, мулажи, донације).
--
-- Слике иду кроз ПОСТОЈЕЋУ Фототеку (табела `fotografije`, миграција 019);
-- веза досије↔фотографија носи ФАЗУ (pre/tokom/posle = сл. а/б/в из старе
-- конвенције имена датотека). Предлошци поступака (описи се понављају) су
-- CRUD ресурс за конзераторе.
-- ============================================================================

-- ---------------------------------------------------------------------------
-- Главни досије: један ред по захвату.
-- ---------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS kr_dosije (
    id SERIAL PRIMARY KEY,
    evidencioni_broj TEXT NOT NULL UNIQUE,
    odeljenje TEXT NOT NULL CHECK (odeljenje IN ('geo', 'bio')),

    -- Предмет: веза на збирку ИЛИ слободан унос.
    predmet_tip TEXT NOT NULL DEFAULT 'zbirka'
        CHECK (predmet_tip IN ('zbirka', 'slobodan')),
    database_name TEXT,            -- кад је 'zbirka' (нпр. 'mineral')
    inventarni_broj TEXT,          -- инвентарни број музејског предмета
    kolektorski_broj TEXT,         -- колекторски број (Col.XXX); слике се вежу по њему
    naziv_predmeta TEXT NOT NULL,  -- назив (повучен из збирке или уписан ручно)
    narucilac TEXT,                -- за спољне предмете (Музеј Југославије, мулажи…)

    -- Три описа стања (колоне E/F/G старог Excel-а).
    opis_pre TEXT,                 -- опис стања пре радова
    opis_postupak TEXT,            -- детаљан опис поступка и употребљених материјала
    opis_posle TEXT,               -- опис стања након радова

    -- Период извршења: парсиране границе + оригинални текст (уноси су
    -- неуједначени: „у периоду од … до …" или „дана …").
    period_od DATE,
    period_do DATE,
    period_tekst TEXT,

    napomena TEXT,

    -- Порекло записа + оригинални еви­денциони број из Excel-а (стари бројеви
    -- нису јединствени — имали су дупликате и празнине — па модул генерише свој).
    izvor TEXT NOT NULL DEFAULT 'rucno' CHECK (izvor IN ('rucno', 'uvoz')),
    izvorni_evidencioni_broj TEXT,

    created_by_email VARCHAR(255),
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_kr_dosije_odeljenje ON kr_dosije(odeljenje);
CREATE INDEX IF NOT EXISTS idx_kr_dosije_predmet
    ON kr_dosije(database_name, inventarni_broj);
CREATE INDEX IF NOT EXISTS idx_kr_dosije_kolektorski ON kr_dosije(kolektorski_broj);

COMMENT ON TABLE kr_dosije IS
    'Конзерваторско-рестаураторски досије — један ред по захвату на предмету';
COMMENT ON COLUMN kr_dosije.evidencioni_broj IS
    'Аутоматски, по одељењу и години: КР-ГЕО-2026-001 / КР-БИО-2026-001';
COMMENT ON COLUMN kr_dosije.kolektorski_broj IS
    'Колекторски број (Col.XXX) — слике из Фототеке се вежу по овом броју';

-- ---------------------------------------------------------------------------
-- Извршиоци: више по досијеу. `user_email` кад је поклопљен корисник из
-- `users`, иначе само `ime_tekst` (историјски записи имају имена људи који
-- нису налози — нпр. „Бранко Радуловић").
-- ---------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS kr_dosije_izvrsilac (
    id SERIAL PRIMARY KEY,
    dosije_id INTEGER NOT NULL REFERENCES kr_dosije(id) ON DELETE CASCADE,
    user_email VARCHAR(255),
    ime_tekst TEXT NOT NULL,
    redosled INTEGER NOT NULL DEFAULT 0,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    UNIQUE (dosije_id, ime_tekst)
);

CREATE INDEX IF NOT EXISTS idx_kr_izvrsilac_dosije ON kr_dosije_izvrsilac(dosije_id);
CREATE INDEX IF NOT EXISTS idx_kr_izvrsilac_email ON kr_dosije_izvrsilac(user_email);

COMMENT ON TABLE kr_dosije_izvrsilac IS
    'Лица која су вршила радове на досијеу (веза на users кад постоји налог)';

-- ---------------------------------------------------------------------------
-- Предлошци поступака: описи се понављају (исти поступак конзервације на
-- десетинама предмета). Конзерватор бира предложак па дорађује текст.
-- `odeljenje` NULL = заједнички предложак за оба одељења.
-- ---------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS kr_predlozak (
    id SERIAL PRIMARY KEY,
    odeljenje TEXT CHECK (odeljenje IS NULL OR odeljenje IN ('geo', 'bio')),
    vrsta TEXT NOT NULL CHECK (vrsta IN ('pre', 'postupak', 'posle')),
    naziv TEXT NOT NULL,
    sadrzaj TEXT NOT NULL,
    created_by_email VARCHAR(255),
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_kr_predlozak_izbor ON kr_predlozak(odeljenje, vrsta);

COMMENT ON TABLE kr_predlozak IS
    'Предлошци описа/поступка за К-Р досије — бирају се па дорађују (CRUD за конзераторе)';
COMMENT ON COLUMN kr_predlozak.vrsta IS
    'Које поље описа попуњава: pre / postupak / posle';

-- ---------------------------------------------------------------------------
-- Веза досије ↔ фотографија (из Фототеке), са фазом. Иста конвенција као
-- остале foto_veza_* табеле (миграција 019), уз додатну колону `faza`.
-- Иста фотографија сме да стоји у више досијеа и/или више фаза, зато је
-- UNIQUE по (fotografija_id, dosije_id, faza).
-- ---------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS foto_veza_kr_dosije (
    id SERIAL PRIMARY KEY,
    fotografija_id INTEGER NOT NULL REFERENCES fotografije(id) ON DELETE CASCADE,
    dosije_id INTEGER NOT NULL REFERENCES kr_dosije(id) ON DELETE CASCADE,
    faza TEXT NOT NULL CHECK (faza IN ('pre', 'tokom', 'posle')),
    redosled INTEGER NOT NULL DEFAULT 0,
    created_by_email VARCHAR(255),
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    UNIQUE (fotografija_id, dosije_id, faza)
);

CREATE INDEX IF NOT EXISTS idx_foto_veza_kr_dosije ON foto_veza_kr_dosije(dosije_id);
CREATE INDEX IF NOT EXISTS idx_foto_veza_kr_foto ON foto_veza_kr_dosije(fotografija_id);

COMMENT ON TABLE foto_veza_kr_dosije IS
    'Веза К-Р досијеа и фотографије из Фототеке; faza = pre/tokom/posle (сл. а/б/в)';
