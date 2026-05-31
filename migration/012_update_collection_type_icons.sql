-- Migration 012: switch five collection_types from Bootstrap icons to
-- custom museum icons (museum-icon-*) to match the updated UI assets.
--
-- Context:
--   db/schema_collections.sql now declares the new icon codes, but the
--   `INSERT ... ON CONFLICT (code) DO NOTHING` block in that file does not
--   update existing rows. Existing deployments therefore keep the old
--   bi-* icon names and the front-end renders the wrong glyphs.
--
-- Safe to run repeatedly (each UPDATE is idempotent against the target value).

UPDATE collection_types SET icon = 'museum-icon-fish'      WHERE code = 'ichthyology';
UPDATE collection_types SET icon = 'museum-icon-mushroom'  WHERE code = 'mycology';
UPDATE collection_types SET icon = 'museum-icon-snake'     WHERE code = 'herpetology';
UPDATE collection_types SET icon = 'museum-icon-bird'      WHERE code = 'ornithology';
UPDATE collection_types SET icon = 'museum-icon-dinosaur'  WHERE code = 'paleozoology';

-- Rollback (only if you must revert):
--   UPDATE collection_types SET icon = 'bi-water'            WHERE code = 'ichthyology';
--   UPDATE collection_types SET icon = 'bi-tree'             WHERE code = 'mycology';
--   UPDATE collection_types SET icon = 'bi-emoji-sunglasses' WHERE code = 'herpetology';
--   UPDATE collection_types SET icon = 'bi-feather'          WHERE code = 'ornithology';
--   UPDATE collection_types SET icon = 'bi-gem'              WHERE code = 'paleozoology';
