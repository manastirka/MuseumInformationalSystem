-- ============================================================================
-- Migration 039: усклађивање инвентарске књиге и физичке базе минерала
-- ============================================================================
-- Date: August 2026
--
-- Семантика (по кустосу):
--   * inventory_entries = дигитализована ШТАМПАНА инвентарска књига. Штампана
--     верзија постоји САМО до броја 3572; после тога штампане књиге нема.
--     Штампана књига је извор истине (source of truth) до 3572.
--   * minerals = ФИЗИЧКА база депоа (шта стварно стоји у музеју). Бројеви после
--     3572 постоје физички у депоу и у minerals — то је исправно и не дира се.
--
-- Ова миграција додаје САМО ознаке (без дирања података):
--   1) inventory_entries.in_printed_book — TRUE за нормализован број 1..3572.
--      Нормализација = само цифре из inventory_number (формати: голи број или
--      M-префикс). Проверено: ниједан M-запис не пада у 1..3572, па су сви
--      означени записи голи бројеви. Запис-уљез 2932317 (без raw вредности) је
--      > 3572 и природно испада из опсега (додатно се пријављује у CLI извештају).
--   2) minerals.physical_presence_confirmed — да ли је ред стварно физички у
--      депоу. Постојећи редови су физички присутни → DEFAULT TRUE. Записи касније
--      уписани из штампане књиге (кроз `flask uskladi-knjigu-depo --execute`)
--      добијају FALSE + source='printed-book': књижни, ФИЗИЧКИ НЕПОТВРЂЕНИ.
--      Тиме semantika minerals=депо остаје чиста (bool каже „да ли је у депоу").
--   3) minerals.source — порекло реда ('printed-book' за књижне увозе; NULL за
--      изворне редове депоа).
--
-- Идемпотентна (безбедна за поновно покретање).
-- ============================================================================

-- ---- 1) Инвентарска књига: ознака штампане књиге (1..3572) ------------------
ALTER TABLE inventory_entries
    ADD COLUMN IF NOT EXISTS in_printed_book BOOLEAN NOT NULL DEFAULT FALSE;

UPDATE inventory_entries
   SET in_printed_book = TRUE
 WHERE regexp_replace(inventory_number, '\D', '', 'g') ~ '^[0-9]+$'
   AND (regexp_replace(inventory_number, '\D', '', 'g'))::bigint BETWEEN 1 AND 3572
   AND in_printed_book IS DISTINCT FROM TRUE;

CREATE INDEX IF NOT EXISTS idx_inventory_entries_in_printed_book
    ON inventory_entries (in_printed_book);

-- ---- 2) minerals: физичко присуство у депоу + порекло ----------------------
ALTER TABLE minerals
    ADD COLUMN IF NOT EXISTS physical_presence_confirmed BOOLEAN NOT NULL DEFAULT TRUE;

ALTER TABLE minerals
    ADD COLUMN IF NOT EXISTS source TEXT;

CREATE INDEX IF NOT EXISTS idx_minerals_physical_presence_confirmed
    ON minerals (physical_presence_confirmed);
