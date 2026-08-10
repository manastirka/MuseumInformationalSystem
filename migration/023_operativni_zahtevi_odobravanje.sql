-- 018_operativni_zahtevi_odobravanje.sql
--
-- Jedinstveni okvir odobravanja za operativne module (zahtevi, nabavka,
-- službeni put) nad postojećim archive_requests engine-om (migracija 004).
--
-- 1. procurement_requests dobija vezu ka archive_requests: status nabavke
--    od sada živi u okviru odobravanja, a red nabavke ostaje nosilac
--    sadržaja (stavke, iznosi, Word export).
-- 2. Backfill created_by_department iz employee_profiles: department
--    scoping šefova odeljenja zahteva popunjeno odeljenje podnosioca
--    (postojeći redovi su ga imali prazno jer je dolazilo iz klijenta).
-- 3. Indeksi za red odobravanja i filtere arhive (tip, godina, odeljenje).
--
-- Idempotentno: bezbedno za ponovno pokretanje.

ALTER TABLE procurement_requests
    ADD COLUMN IF NOT EXISTS archive_request_id INTEGER REFERENCES archive_requests(id);

UPDATE archive_requests ar
SET created_by_department = ep.department
FROM employee_profiles ep
WHERE (ar.created_by_department IS NULL OR ar.created_by_department = '')
  AND ep.department IS NOT NULL
  AND ep.department <> ''
  AND LOWER(ep.email::text) = LOWER(ar.created_by_email);

CREATE INDEX IF NOT EXISTS idx_archive_requests_type_status
    ON archive_requests(request_type, status);
CREATE INDEX IF NOT EXISTS idx_archive_requests_archive_year
    ON archive_requests(archive_year);
CREATE INDEX IF NOT EXISTS idx_archive_requests_created_by_department
    ON archive_requests(created_by_department);
CREATE INDEX IF NOT EXISTS idx_archive_requests_created_by_email
    ON archive_requests(created_by_email);
CREATE INDEX IF NOT EXISTS idx_procurement_requests_archive_request_id
    ON procurement_requests(archive_request_id);

-- Rollback:
--   ALTER TABLE procurement_requests DROP COLUMN IF EXISTS archive_request_id;
--   DROP INDEX IF EXISTS idx_archive_requests_type_status;
--   DROP INDEX IF EXISTS idx_archive_requests_archive_year;
--   DROP INDEX IF EXISTS idx_archive_requests_created_by_department;
--   DROP INDEX IF EXISTS idx_archive_requests_created_by_email;
--   DROP INDEX IF EXISTS idx_procurement_requests_archive_request_id;
--   (backfill created_by_department se ne vraća — kolona je i ranije postojala)
