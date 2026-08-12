-- Migration: auth_version za trenutni opoziv sesija (revizija 2026-08, stavka 6)
-- Date: 2026-08-12
-- Purpose: deaktiviran ili degradiran korisnik je zadržavao prava u postojećoj
--   sesiji do njenog isteka. Svaka promena prava (deaktivacija, promena uloge,
--   promena/reset lozinke) podiže users.auth_version; sesija nosi verziju iz
--   trenutka prijave i proverava se pri svakom zahtevu — stara verzija ruši
--   sesiju odmah (security_utils.validate_session_auth_version).

ALTER TABLE users ADD COLUMN IF NOT EXISTS auth_version INTEGER NOT NULL DEFAULT 1;

COMMENT ON COLUMN users.auth_version IS
    'Verzija prava naloga; bump pri deaktivaciji/promeni uloge/lozinke ruši postojeće sesije';
