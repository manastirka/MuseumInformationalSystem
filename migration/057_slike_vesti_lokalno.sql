-- Migration: Lokalna kopija slike za vesti sa veba
-- Date: 2026-08-31
-- Purpose: Vesti nadjene na vebu imale su adresu slike (politika.rs, b92.net,
--   ocdn.eu…), ali ih pregledac NIJE prikazivao — CSP zaglavlje aplikacije
--   dozvoljava img-src samo za 'self', OSM plocice, Facebook i nhmbeo.rs.
--
--   Resenje NIJE rupiti CSP za svaki medij: to bi znacilo izmenu bezbednosne
--   politike pri svakom novom izvoru, citaocev pregledac bi odlazio na tudje
--   servere (curenje posete), a slika bi nestala cim je izvor obrise.
--   Umesto toga slika se preuzima jednom i cuva kod nas (static/vesti_slike/),
--   isti obrazac kao kes plocica karte — pa se servira sa 'self'.
--
--   slika_url ostaje kao poreklo (odakle je preuzeta), slika_fajl je ime
--   lokalne kopije. Prikaz koristi lokalnu; bez nje slike nema.

ALTER TABLE news_web_kandidati
    ADD COLUMN IF NOT EXISTS slika_fajl TEXT;

ALTER TABLE news_articles
    ADD COLUMN IF NOT EXISTS slika_fajl TEXT;

COMMENT ON COLUMN news_web_kandidati.slika_fajl IS
    'Ime lokalne kopije u static/vesti_slike/; slika_url ostaje poreklo';
COMMENT ON COLUMN news_articles.slika_fajl IS
    'Ime lokalne kopije u static/vesti_slike/ (vesti sa veba); NULL kad je slika sa nhmbeo.rs koji CSP dozvoljava';
