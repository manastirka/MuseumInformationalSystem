-- Migration: Vlasništvo reda namere intake-a (revizija 2026-08, krug 4, stavka 2)
-- Date: 2026-08-13
-- Purpose: Protokol namere iz migracije 047 pokriva jednokorisničku granu, ne
--   konkurenciju: dva istovremena unosa iste fotografije dele JEDAN red namere
--   (upsert po raw_putanja), pa gubitnik pri čišćenju sme da obriše RAW
--   pobednika. claim_token identifikuje proces koji je nameru upisao — samo
--   vlasnik sveže namere sme da postavlja fajl i da ga briše pri čišćenju.

ALTER TABLE fototeka_intake_pending
    ADD COLUMN IF NOT EXISTS claim_token TEXT;

COMMENT ON COLUMN fototeka_intake_pending.claim_token IS
    'Vlasnik namere (uuid procesa unosa); čišćenje sme da obriše RAW samo uz poklapanje tokena';
