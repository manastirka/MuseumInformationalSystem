-- Biological Collections Schema
-- Phase 3C: Unified collection management for all biological specimens
-- Supports: Botany, Ichthyology, Entomology, Mycology, Herpetology,
--           Ornithology, Paleozoology, Paleobotany, Petrology

-- Collection Types Reference Table
CREATE TABLE IF NOT EXISTS collection_types (
    id SERIAL PRIMARY KEY,
    code TEXT UNIQUE NOT NULL,  -- 'botany', 'ichthyology', etc.
    name_sr TEXT NOT NULL,      -- 'Ботаничка збирка'
    name_en TEXT,
    icon TEXT,                  -- Bootstrap icon class
    description_sr TEXT,
    description_en TEXT,
    created_at TIMESTAMPTZ DEFAULT now()
);

-- Main Collection Specimens Table
CREATE TABLE IF NOT EXISTS collection_specimens (
    id SERIAL PRIMARY KEY,
    catalog_number TEXT UNIQUE NOT NULL,
    collection_type TEXT NOT NULL REFERENCES collection_types(code),

    -- Taxonomy
    scientific_name TEXT NOT NULL,
    common_name_sr TEXT,
    common_name_en TEXT,
    family TEXT,
    order_name TEXT,
    class_name TEXT,
    phylum TEXT,
    kingdom TEXT,

    -- Collection Information
    location_found TEXT,
    locality_details TEXT,
    habitat TEXT,
    altitude TEXT,
    coordinates GEOGRAPHY(Point, 4326),  -- PostGIS support

    -- Collection Event
    date_collected DATE,
    collector TEXT,
    collection_method TEXT,

    -- Specimen Details
    age TEXT,
    sex TEXT,
    condition TEXT,
    preparation_type TEXT,

    -- Measurements (stored as JSONB for flexibility)
    measurements JSONB,  -- e.g., {"length_cm": 120, "weight_kg": 18, "wing_span": 45}

    -- Conservation Status
    endemic_status TEXT,
    conservation_status TEXT,
    iucn_status TEXT,

    -- Storage
    storage_location TEXT,
    herbarium_number TEXT,
    accession_number TEXT,

    -- Administrative
    curator TEXT,
    description TEXT,
    notes TEXT,

    -- Media
    images TEXT[],  -- Array of image URLs/paths

    -- Metadata
    status TEXT DEFAULT 'active',  -- 'active', 'on_display', 'in_storage', 'on_loan'
    created_at TIMESTAMPTZ DEFAULT now(),
    updated_at TIMESTAMPTZ DEFAULT now()
);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_specimens_collection_type ON collection_specimens(collection_type);
CREATE INDEX IF NOT EXISTS idx_specimens_catalog_number ON collection_specimens(catalog_number);
CREATE INDEX IF NOT EXISTS idx_specimens_scientific_name ON collection_specimens(scientific_name);
CREATE INDEX IF NOT EXISTS idx_specimens_family ON collection_specimens(family);
CREATE INDEX IF NOT EXISTS idx_specimens_collector ON collection_specimens(collector);
CREATE INDEX IF NOT EXISTS idx_specimens_status ON collection_specimens(status);
CREATE INDEX IF NOT EXISTS idx_specimens_coordinates ON collection_specimens USING GIST(coordinates);

-- Full-text search indexes for Serbian Cyrillic
CREATE INDEX IF NOT EXISTS idx_specimens_scientific_search
    ON collection_specimens USING gin(to_tsvector('simple', scientific_name));
CREATE INDEX IF NOT EXISTS idx_specimens_common_search
    ON collection_specimens USING gin(to_tsvector('simple', common_name_sr));
CREATE INDEX IF NOT EXISTS idx_specimens_description_search
    ON collection_specimens USING gin(to_tsvector('simple', description));

-- Collection Statistics View
CREATE OR REPLACE VIEW collection_statistics AS
SELECT
    ct.code,
    ct.name_sr,
    COUNT(cs.id) as total_specimens,
    COUNT(cs.id) FILTER (WHERE cs.endemic_status IS NOT NULL AND cs.endemic_status != '') as endemic_species,
    COUNT(cs.id) FILTER (WHERE cs.conservation_status LIKE '%угрожен%' OR cs.conservation_status LIKE '%endangered%') as threatened_species,
    COUNT(cs.id) FILTER (WHERE cs.status = 'on_display') as on_display,
    COUNT(DISTINCT cs.family) as families_count,
    MIN(cs.date_collected) as earliest_specimen,
    MAX(cs.date_collected) as latest_specimen
FROM collection_types ct
LEFT JOIN collection_specimens cs ON ct.code = cs.collection_type
GROUP BY ct.code, ct.name_sr;

-- Insert collection types
INSERT INTO collection_types (code, name_sr, name_en, icon, description_sr) VALUES
    ('botany', 'Ботаничка збирка', 'Botanical Collection', 'bi-flower1', 'Херباријум и ботанички примерци'),
    ('ichthyology', 'Ихтиолошка збирка', 'Ichthyology Collection', 'museum-icon-fish', 'Рибе и водоземци'),
    ('entomology', 'Ентомолошка збирка', 'Entomology Collection', 'bi-bug', 'Инсекти и зглавкари'),
    ('mycology', 'Миколошка збирка', 'Mycology Collection', 'museum-icon-mushroom', 'Гљиве и лишајеви'),
    ('herpetology', 'Херпетолошка збирка', 'Herpetology Collection', 'museum-icon-snake', 'Гмизавци и водоземци'),
    ('ornithology', 'Орнитолошка збирка', 'Ornithology Collection', 'museum-icon-bird', 'Птице'),
    ('paleozoology', 'Палеозоолошка збирка', 'Paleozoology Collection', 'museum-icon-dinosaur', 'Фосилни животињски остаци'),
    ('paleobotany', 'Палеботаничка збирка', 'Paleobotany Collection', 'bi-tree-fill', 'Фосилни биљни остаци'),
    ('petrology', 'Петролошка збирка', 'Petrology Collection', 'bi-layers', 'Стене и минерали')
ON CONFLICT (code) DO NOTHING;

COMMENT ON TABLE collection_specimens IS 'Phase 3C: Unified biological collection specimens';
COMMENT ON TABLE collection_types IS 'Collection type definitions for biological collections';
COMMENT ON VIEW collection_statistics IS 'Real-time statistics for each collection type';
