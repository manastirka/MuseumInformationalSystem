-- 062: Старе адресе лекција уџбеника. Кад увоз премести лекцију у друго поглавље
-- или је преименује (поље prethodni_slug у фајлу), стари пар (поглавље, slug)
-- остаје овде, па стари URL преусмерава на нови (301) — веза из белешки, обележивача
-- и претраживача не пуца, а id, верзије и напредак лекције остају исти.
--
-- Нема BEGIN/COMMIT: трансакцију води deploy/run_migrations.py.

CREATE TABLE udzbenik_lekcija_alias (
    id             SERIAL PRIMARY KEY,
    lekcija_id     INTEGER NOT NULL REFERENCES udzbenik_lekcija(id) ON DELETE CASCADE,
    poglavlje_slug TEXT NOT NULL CHECK (poglavlje_slug ~ '^[a-z0-9][a-z0-9-]{1,59}$'),
    slug           TEXT NOT NULL CHECK (slug ~ '^[a-z0-9][a-z0-9-]{1,59}$'),
    created_at     TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE (lekcija_id, poglavlje_slug, slug)
);

CREATE INDEX udzbenik_lekcija_alias_put_idx ON udzbenik_lekcija_alias (poglavlje_slug, slug);

COMMENT ON TABLE udzbenik_lekcija_alias IS
    'Стари (поглавље, slug) премештених или преименованих лекција уџбеника — стари URL преусмерава (301)';
