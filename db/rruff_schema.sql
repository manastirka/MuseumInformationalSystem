-- RRUFF Scientific Mineral Database Schema
-- Creates tables for RRUFF Project mineralogical data

-- Drop existing tables if they exist
DROP TABLE IF EXISTS rruff_localities CASCADE;
DROP TABLE IF EXISTS rruff_references CASCADE;
DROP TABLE IF EXISTS rruff_chemistry CASCADE;
DROP TABLE IF EXISTS rruff_minerals CASCADE;
DROP TABLE IF EXISTS mineral_rruff_matches CASCADE;

-- RRUFF Minerals table (scientific mineral data)
CREATE TABLE rruff_minerals (
    id SERIAL PRIMARY KEY,
    rruff_id VARCHAR(20) NOT NULL UNIQUE,
    name TEXT NOT NULL,
    name_plain TEXT,
    formula_rruff TEXT,
    formula_ima TEXT,
    formula_concise TEXT,
    formula_html TEXT,
    ideal_chemistry TEXT,
    chemistry_elements TEXT,
    valence_elements TEXT,
    ima_number TEXT,
    ima_status TEXT,
    ima_mineral VARCHAR(1),
    ima_mineral_symbol VARCHAR(20),
    year_first_published INTEGER,
    structural_groupname TEXT,
    fleischers_groupname TEXT,
    fleischers_glossary VARCHAR(1),
    crystal_system TEXT,
    crystal_systems TEXT,
    space_group TEXT,
    space_groups TEXT,
    country_type_locality TEXT,
    crystal_morphology TEXT,
    oldest_known_age_ma FLOAT,
    paragenetic_modes TEXT,
    status_notes TEXT,
    rruff_ids TEXT,
    database_id INTEGER,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Chemical composition data
CREATE TABLE rruff_chemistry (
    id SERIAL PRIMARY KEY,
    rruff_id VARCHAR(20) NOT NULL REFERENCES rruff_minerals(rruff_id) ON DELETE CASCADE,
    oxide VARCHAR(20) NOT NULL,
    weight_percent FLOAT
);

-- Locality information
CREATE TABLE rruff_localities (
    id SERIAL PRIMARY KEY,
    rruff_id VARCHAR(20) NOT NULL REFERENCES rruff_minerals(rruff_id) ON DELETE CASCADE,
    locality TEXT,
    country VARCHAR(100),
    latitude FLOAT,
    longitude FLOAT
);

-- Reference data
CREATE TABLE rruff_references (
    id SERIAL PRIMARY KEY,
    rruff_id VARCHAR(20) NOT NULL REFERENCES rruff_minerals(rruff_id) ON DELETE CASCADE,
    reference_text TEXT,
    authors TEXT,
    title TEXT,
    journal VARCHAR(200),
    year INTEGER,
    doi VARCHAR(100)
);

-- Matches between museum minerals and RRUFF database
CREATE TABLE mineral_rruff_matches (
    id SERIAL PRIMARY KEY,
    mineral_id INTEGER NOT NULL REFERENCES minerals(id) ON DELETE CASCADE,
    rruff_id VARCHAR(20) NOT NULL REFERENCES rruff_minerals(rruff_id) ON DELETE CASCADE,
    match_confidence FLOAT DEFAULT 1.0,
    matched_by VARCHAR(50),
    matched_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(mineral_id, rruff_id)
);

-- Indexes for performance
CREATE INDEX idx_rruff_minerals_name ON rruff_minerals(name);
CREATE INDEX idx_rruff_minerals_name_plain ON rruff_minerals(name_plain);
CREATE INDEX idx_rruff_minerals_crystal_system ON rruff_minerals(crystal_system);
CREATE INDEX idx_rruff_minerals_ima_status ON rruff_minerals(ima_status);
CREATE INDEX idx_rruff_chemistry_rruff_id ON rruff_chemistry(rruff_id);
CREATE INDEX idx_rruff_localities_rruff_id ON rruff_localities(rruff_id);
CREATE INDEX idx_rruff_references_rruff_id ON rruff_references(rruff_id);
CREATE INDEX idx_mineral_rruff_matches_mineral_id ON mineral_rruff_matches(mineral_id);
CREATE INDEX idx_mineral_rruff_matches_rruff_id ON mineral_rruff_matches(rruff_id);

-- Full-text search index on mineral names
CREATE INDEX idx_rruff_minerals_name_fts ON rruff_minerals USING gin(to_tsvector('english', name || ' ' || COALESCE(name_plain, '')));
