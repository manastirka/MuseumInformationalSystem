-- Migration: Zabrana preklapanja rezervacija vozila
--            (revizija 2026-08, batch 6, stavka 9)
-- Date: 2026-08-11
-- Purpose: vehicle_reservations ima samo CHECK (end_date >= start_date) —
--   dvoje zaposlenih rezerviše isto vozilo za isti period i oboje vide uspeh.
--   EXCLUDE USING gist garantuje na nivou baze da se AKTIVNE rezervacije
--   istog vozila ne preklapaju (uklj. granične dane — '[]' zatvoren opseg);
--   otkazane/završene ne blokiraju nove.
--
-- NAPOMENA: ako u bazi VEĆ postoje preklopljene aktivne rezervacije, ALTER
--   pada — namerno vidljivo: operater rešava konflikt (otkaže jednu od njih)
--   pa ponovi migraciju. Ništa se ne otkazuje tiho.

CREATE EXTENSION IF NOT EXISTS btree_gist;

ALTER TABLE vehicle_reservations
    DROP CONSTRAINT IF EXISTS excl_vehicle_rezervacije_preklapanje;
ALTER TABLE vehicle_reservations
    ADD CONSTRAINT excl_vehicle_rezervacije_preklapanje
    EXCLUDE USING gist (
        vehicle_id WITH =,
        daterange(start_date, end_date, '[]') WITH &&
    ) WHERE (status = 'Активна');

COMMENT ON CONSTRAINT excl_vehicle_rezervacije_preklapanje
    ON vehicle_reservations IS
    'Aktivne rezervacije istog vozila ne smeju da se preklapaju po datumu (btree_gist)';
