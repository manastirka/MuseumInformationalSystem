-- 064: Детаљи редова референтних табела уџбеника (UGOVOR-TABLICE-2.md, део 2):
-- страница по реду табеле (нпр. просторна група: операције, елементи
-- симетрије, Викофови положаји, стереограм). Кључ ставке = вредност колоне
-- ``kolona`` (као текст) у неком реду табеле; садржај је JSONB по шеми врсте
-- (udzbenik/schema/detalj-<vrsta>.schema.json, валидација на упису —
-- scripts/udzbenik_uvoz.py). udzbenik_tablica.sadrzaj држи само
-- {"detalji": {"vrsta", "kolona"}}, без ставки (верзионисање табеле види
-- промену врсте/колоне); ставке се при увозу замењују у целини (upsert +
-- брисање ставки којих нема у фајлу).
-- Мотор их чита само кроз API (/api/udzbenik/<zbirka>/tablica/<slug>/detalj/<kljuc>).
--
-- Нема BEGIN/COMMIT: трансакцију води deploy/run_migrations.py.

CREATE TABLE udzbenik_tablica_detalj (
    tablica_id  INTEGER NOT NULL REFERENCES udzbenik_tablica(id) ON DELETE CASCADE,
    kljuc       TEXT NOT NULL CHECK (kljuc ~ '^[A-Za-z0-9][A-Za-z0-9._-]{0,39}$'),
    sadrzaj     JSONB NOT NULL,                      -- по шеми врсте детаља
    azurirano   TIMESTAMPTZ NOT NULL DEFAULT now(),
    PRIMARY KEY (tablica_id, kljuc)
);

COMMENT ON TABLE udzbenik_tablica_detalj IS
    'Детаљи редова табела уџбеника (страница по реду, нпр. просторна група); кључ = вредност колоне детаља';
