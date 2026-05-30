-- Sanja Paleogene/Neogene large-mammal collection (moved off the flat JSON file
-- Sanja/sanja_paleogene_neogene_mammals.json into PostgreSQL).
--
-- Each specimen carries ~35 loosely-typed fields (28 text + 7 numeric, see
-- _SANJA_TEXT_FIELDS / _SANJA_NUMBER_FIELDS in collection_management_views.py).
-- The full specimen dict is stored losslessly in a JSONB column; the stable id
-- and source_row are promoted to real columns for the primary key and ordering.

CREATE TABLE IF NOT EXISTS sanja_paleogene_neogene_mammals (
    id          INTEGER PRIMARY KEY,
    source_row  INTEGER,
    specimen    JSONB NOT NULL,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at  TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- Help the most common display lookups (by taxon / locality).
CREATE INDEX IF NOT EXISTS ix_sanja_specimen_name
    ON sanja_paleogene_neogene_mammals ((specimen->>'specimen_name'));
CREATE INDEX IF NOT EXISTS ix_sanja_location_found
    ON sanja_paleogene_neogene_mammals ((specimen->>'location_found'));
