-- Fix Meteorite Schema - Add Missing Columns
-- Date: December 25, 2025

-- Add missing columns that exist in original data but not in schema or not populated

-- Fall type as TEXT (not just boolean)
ALTER TABLE meteorite_specimens
ADD COLUMN IF NOT EXISTS fall_type TEXT;

-- Total mass of all specimens (different from individual mass)
ALTER TABLE meteorite_specimens
ADD COLUMN IF NOT EXISTS total_mass NUMERIC(10,3);

ALTER TABLE meteorite_specimens
ADD COLUMN IF NOT EXISTS total_mass_unit VARCHAR(10) DEFAULT 'kg';

-- Quantity of specimens
ALTER TABLE meteorite_specimens
ADD COLUMN IF NOT EXISTS quantity INTEGER DEFAULT 1;

-- Meteorite Bulletin number
ALTER TABLE meteorite_specimens
ADD COLUMN IF NOT EXISTS meteorite_bulletin_number VARCHAR(50);

-- Mineralogy (detailed mineral composition)
ALTER TABLE meteorite_specimens
ADD COLUMN IF NOT EXISTS mineralogy TEXT;

-- Cosmic ray exposure age
ALTER TABLE meteorite_specimens
ADD COLUMN IF NOT EXISTS cosmic_ray_exposure TEXT;

-- Widmanstätten pattern (for iron meteorites)
ALTER TABLE meteorite_specimens
ADD COLUMN IF NOT EXISTS widmanstatten_pattern TEXT;

-- Fusion crust description
ALTER TABLE meteorite_specimens
ADD COLUMN IF NOT EXISTS fusion_crust TEXT;

-- Serbian meteorite flag (important for museum)
ALTER TABLE meteorite_specimens
ADD COLUMN IF NOT EXISTS serbian_meteorite BOOLEAN DEFAULT FALSE;

-- Fall/find date as TEXT (Serbian date formats)
ALTER TABLE meteorite_specimens
ADD COLUMN IF NOT EXISTS fall_date_text TEXT;

-- Discovery/acquisition date as TEXT
ALTER TABLE meteorite_specimens
ADD COLUMN IF NOT EXISTS acquisition_date_text TEXT;

COMMENT ON COLUMN meteorite_specimens.fall_type IS 'Serbian: Тип пада (Пад посматран, Налаз, итд.)';
COMMENT ON COLUMN meteorite_specimens.total_mass IS 'Total mass of all specimens found (not just this one)';
COMMENT ON COLUMN meteorite_specimens.quantity IS 'Number of specimens in collection';
COMMENT ON COLUMN meteorite_specimens.meteorite_bulletin_number IS 'Meteoritical Bulletin catalog number';
COMMENT ON COLUMN meteorite_specimens.serbian_meteorite IS 'Serbian: Српски метеорит';
COMMENT ON COLUMN meteorite_specimens.fall_date_text IS 'Fall date in original Serbian format (e.g. 13. октобар 1877.)';
COMMENT ON COLUMN meteorite_specimens.acquisition_date_text IS 'Acquisition date in original format';

-- Create index on serbian_meteorite for filtering
CREATE INDEX IF NOT EXISTS meteorite_serbian_idx ON meteorite_specimens(serbian_meteorite) WHERE serbian_meteorite = TRUE;

-- Create index on meteorite_bulletin_number
CREATE INDEX IF NOT EXISTS meteorite_bulletin_idx ON meteorite_specimens(meteorite_bulletin_number);
