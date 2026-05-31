-- ============================================================================
-- Phase 3A: High Priority Database Migration Schema
-- ============================================================================
-- Date: December 25, 2025
-- Databases: Library, Exhibitions, Cultural Heritage, Meteorite, Employees
-- ============================================================================

-- Enable required extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "citext";

-- ============================================================================
-- 1. LIBRARY DATABASE
-- ============================================================================

CREATE TABLE IF NOT EXISTS library_books (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    author TEXT,
    isbn VARCHAR(20),
    publisher TEXT,
    publication_year INTEGER,
    category VARCHAR(100),
    subcategory VARCHAR(100),
    language VARCHAR(50) DEFAULT 'српски',
    pages INTEGER,
    format VARCHAR(50),
    location TEXT,
    shelf_number VARCHAR(50),
    status VARCHAR(50) DEFAULT 'доступна',
    acquisition_date DATE,
    acquisition_method VARCHAR(100),
    price NUMERIC(10,2),
    condition VARCHAR(50),
    description TEXT,
    notes TEXT,
    keywords TEXT[],
    created_at TIMESTAMPTZ DEFAULT now(),
    updated_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE IF NOT EXISTS library_categories (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL,
    description TEXT,
    parent_category VARCHAR(100),
    created_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE IF NOT EXISTS library_loans (
    id SERIAL PRIMARY KEY,
    book_id INTEGER REFERENCES library_books(id) ON DELETE CASCADE,
    borrower_name TEXT NOT NULL,
    borrower_email TEXT,
    loan_date DATE NOT NULL DEFAULT CURRENT_DATE,
    due_date DATE NOT NULL,
    return_date DATE,
    status VARCHAR(50) DEFAULT 'активна',
    notes TEXT,
    created_at TIMESTAMPTZ DEFAULT now()
);

-- Library indexes
CREATE INDEX IF NOT EXISTS library_books_title_idx ON library_books(title);
CREATE INDEX IF NOT EXISTS library_books_author_idx ON library_books(author);
CREATE INDEX IF NOT EXISTS library_books_isbn_idx ON library_books(isbn);
CREATE INDEX IF NOT EXISTS library_books_category_idx ON library_books(category);
CREATE INDEX IF NOT EXISTS library_books_status_idx ON library_books(status);
CREATE INDEX IF NOT EXISTS library_loans_book_idx ON library_loans(book_id);
CREATE INDEX IF NOT EXISTS library_loans_status_idx ON library_loans(status);

-- ============================================================================
-- 2. EXHIBITIONS DATABASE
-- ============================================================================

CREATE TABLE IF NOT EXISTS exhibitions (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    subtitle TEXT,
    description TEXT,
    exhibition_type VARCHAR(100),
    location TEXT,
    venue TEXT,
    start_date DATE,
    end_date DATE,
    opening_date DATE,
    curator TEXT,
    co_curators TEXT[],
    organizer TEXT,
    sponsors TEXT[],
    status VARCHAR(50) DEFAULT 'планирана',
    visitor_count INTEGER DEFAULT 0,
    catalog_published BOOLEAN DEFAULT FALSE,
    catalog_path TEXT,
    poster_path TEXT,
    budget NUMERIC(12,2),
    notes TEXT,
    created_at TIMESTAMPTZ DEFAULT now(),
    updated_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE IF NOT EXISTS exhibition_items (
    id SERIAL PRIMARY KEY,
    exhibition_id INTEGER REFERENCES exhibitions(id) ON DELETE CASCADE,
    item_type VARCHAR(100),
    item_name TEXT,
    item_description TEXT,
    catalog_number VARCHAR(100),
    collection_source VARCHAR(100),
    display_location TEXT,
    display_order INTEGER,
    notes TEXT,
    created_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE IF NOT EXISTS exhibition_events (
    id SERIAL PRIMARY KEY,
    exhibition_id INTEGER REFERENCES exhibitions(id) ON DELETE CASCADE,
    event_type VARCHAR(100),
    event_title TEXT NOT NULL,
    event_date DATE,
    event_time TIME,
    speaker TEXT,
    description TEXT,
    attendees INTEGER,
    created_at TIMESTAMPTZ DEFAULT now()
);

-- Exhibition indexes
CREATE INDEX IF NOT EXISTS exhibitions_type_idx ON exhibitions(exhibition_type);
CREATE INDEX IF NOT EXISTS exhibitions_dates_idx ON exhibitions(start_date, end_date);
CREATE INDEX IF NOT EXISTS exhibitions_status_idx ON exhibitions(status);
CREATE INDEX IF NOT EXISTS exhibition_items_exhibition_idx ON exhibition_items(exhibition_id);
CREATE INDEX IF NOT EXISTS exhibition_events_exhibition_idx ON exhibition_events(exhibition_id);

-- ============================================================================
-- 3. CULTURAL HERITAGE DATABASE
-- ============================================================================

CREATE TABLE IF NOT EXISTS heritage_items (
    id SERIAL PRIMARY KEY,
    registry_number VARCHAR(100) UNIQUE,
    item_name TEXT NOT NULL,
    alternative_names TEXT[],
    heritage_type VARCHAR(100),
    category VARCHAR(100),
    subcategory VARCHAR(100),
    significance_level VARCHAR(100),
    description TEXT,
    detailed_description TEXT,

    -- Physical characteristics
    dimensions_height NUMERIC(10,2),
    dimensions_width NUMERIC(10,2),
    dimensions_depth NUMERIC(10,2),
    dimensions_diameter NUMERIC(10,2),
    dimensions_unit VARCHAR(10) DEFAULT 'cm',
    weight NUMERIC(10,2),
    weight_unit VARCHAR(10) DEFAULT 'g',
    material TEXT,
    technique TEXT,
    color TEXT,

    -- Historical data
    date_of_origin TEXT,
    century VARCHAR(50),
    cultural_period TEXT,
    creator TEXT,
    creator_nationality TEXT,
    provenance TEXT,
    historical_context TEXT,

    -- Location and status
    current_location TEXT,
    storage_location TEXT,
    display_status VARCHAR(50),
    protection_status VARCHAR(100),
    protection_level VARCHAR(50),
    legal_basis TEXT,
    inscription_date DATE,

    -- Condition
    condition VARCHAR(50),
    condition_notes TEXT,
    conservation_history TEXT,
    conservation_needs TEXT,

    -- Documentation
    bibliography TEXT,
    related_items TEXT[],
    keywords TEXT[],
    notes TEXT,

    -- Images and media
    images JSONB,

    created_at TIMESTAMPTZ DEFAULT now(),
    updated_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE IF NOT EXISTS heritage_types (
    id SERIAL PRIMARY KEY,
    type_name VARCHAR(100) UNIQUE NOT NULL,
    description TEXT
);

CREATE TABLE IF NOT EXISTS heritage_categories (
    id SERIAL PRIMARY KEY,
    category_name VARCHAR(100) UNIQUE NOT NULL,
    heritage_type VARCHAR(100),
    description TEXT
);

-- Heritage indexes
CREATE INDEX IF NOT EXISTS heritage_registry_idx ON heritage_items(registry_number);
CREATE INDEX IF NOT EXISTS heritage_type_idx ON heritage_items(heritage_type);
CREATE INDEX IF NOT EXISTS heritage_category_idx ON heritage_items(category);
CREATE INDEX IF NOT EXISTS heritage_significance_idx ON heritage_items(significance_level);
CREATE INDEX IF NOT EXISTS heritage_protection_idx ON heritage_items(protection_status);
CREATE INDEX IF NOT EXISTS heritage_name_idx ON heritage_items(item_name);

-- ============================================================================
-- 4. METEORITE COLLECTION
-- ============================================================================

CREATE TABLE IF NOT EXISTS meteorite_specimens (
    id SERIAL PRIMARY KEY,
    catalog_number VARCHAR(100) UNIQUE NOT NULL,
    specimen_name TEXT NOT NULL,
    alternative_names TEXT[],

    -- Classification
    meteorite_class VARCHAR(100),
    meteorite_group VARCHAR(100),
    meteorite_type VARCHAR(100),
    classification_scheme TEXT,

    -- Physical properties
    mass NUMERIC(10,3),
    mass_unit VARCHAR(10) DEFAULT 'g',
    dimensions TEXT,
    shape TEXT,
    color TEXT,
    surface_features TEXT,

    -- Composition
    main_minerals TEXT[],
    minor_minerals TEXT[],
    chemical_composition JSONB,
    metal_content NUMERIC(5,2),
    silicate_content NUMERIC(5,2),

    -- Fall/Find data
    fall_date DATE,
    fall_location TEXT,
    fall_country VARCHAR(100),
    fall_coordinates GEOGRAPHY(POINT, 4326),
    fall_witnessed BOOLEAN DEFAULT FALSE,
    fall_description TEXT,

    -- Discovery and collection
    discovery_date DATE,
    discovery_location TEXT,
    discoverer TEXT,
    collection_date DATE,
    collector TEXT,
    collection_method TEXT,

    -- Acquisition
    acquisition_date DATE,
    acquisition_method VARCHAR(100),
    acquisition_source TEXT,
    acquisition_value NUMERIC(12,2),

    -- Scientific data
    shock_stage VARCHAR(50),
    weathering_grade VARCHAR(50),
    texture TEXT,
    petrographic_notes TEXT,
    geochemical_data JSONB,
    isotopic_data JSONB,
    age_estimation TEXT,
    parent_body TEXT,

    -- Storage and condition
    storage_location TEXT,
    storage_conditions TEXT,
    condition VARCHAR(50),
    condition_notes TEXT,

    -- Documentation
    description TEXT,
    scientific_significance TEXT,
    publications TEXT[],
    bibliography_references TEXT,
    keywords TEXT[],
    notes TEXT,

    -- Images and media
    images JSONB,

    -- Status
    status VARCHAR(50) DEFAULT 'у збирци',
    display_status VARCHAR(50),

    created_at TIMESTAMPTZ DEFAULT now(),
    updated_at TIMESTAMPTZ DEFAULT now()
);

-- Meteorite indexes
CREATE INDEX IF NOT EXISTS meteorite_catalog_idx ON meteorite_specimens(catalog_number);
CREATE INDEX IF NOT EXISTS meteorite_class_idx ON meteorite_specimens(meteorite_class);
CREATE INDEX IF NOT EXISTS meteorite_name_idx ON meteorite_specimens(specimen_name);
CREATE INDEX IF NOT EXISTS meteorite_coords_idx ON meteorite_specimens USING GIST(fall_coordinates);

-- ============================================================================
-- 5. EMPLOYEES DATABASE (Enhanced)
-- ============================================================================

CREATE TABLE IF NOT EXISTS employee_profiles (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    employee_id VARCHAR(50) UNIQUE,

    -- Personal information
    full_name TEXT NOT NULL,
    name_cyrillic TEXT,
    date_of_birth DATE,
    place_of_birth TEXT,
    nationality VARCHAR(100),

    -- Contact information
    email CITEXT UNIQUE NOT NULL,
    phone VARCHAR(50),
    mobile VARCHAR(50),
    emergency_contact TEXT,
    emergency_phone VARCHAR(50),

    -- Employment details
    position TEXT NOT NULL,
    department VARCHAR(100),
    division VARCHAR(100),
    employment_type VARCHAR(50),
    employment_status VARCHAR(50) DEFAULT 'активан',
    hire_date DATE,
    termination_date DATE,
    contract_type VARCHAR(50),

    -- Academic credentials
    academic_title VARCHAR(100),
    academic_degree VARCHAR(100),
    education_level VARCHAR(100),
    specialization TEXT,
    university TEXT,
    graduation_year INTEGER,

    -- Professional information
    expertise_areas TEXT[],
    research_interests TEXT[],
    languages_spoken TEXT[],
    certifications TEXT[],
    memberships TEXT[],

    -- Publications and research
    publications_count INTEGER DEFAULT 0,
    research_projects TEXT[],
    awards TEXT[],

    -- Biography
    biography TEXT,
    biography_short TEXT,
    professional_experience TEXT,

    -- Office and access
    office_location TEXT,
    office_phone VARCHAR(50),
    office_hours TEXT,

    -- Authorization: head of their own department can verify timesheets
    -- for employees in `department`.
    is_department_head BOOLEAN NOT NULL DEFAULT FALSE,

    -- Photo and documents
    photo_url TEXT,
    cv_url TEXT,

    -- Additional data
    notes TEXT,
    metadata JSONB,

    created_at TIMESTAMPTZ DEFAULT now(),
    updated_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE IF NOT EXISTS employee_publications (
    id SERIAL PRIMARY KEY,
    employee_id INTEGER REFERENCES employee_profiles(id) ON DELETE CASCADE,
    publication_type VARCHAR(100),
    title TEXT NOT NULL,
    authors TEXT[],
    publication_year INTEGER,
    journal TEXT,
    publisher TEXT,
    doi TEXT,
    isbn TEXT,
    url TEXT,
    citation TEXT,
    abstract TEXT,
    keywords TEXT[],
    created_at TIMESTAMPTZ DEFAULT now()
);

-- Employee indexes
CREATE INDEX IF NOT EXISTS employee_profiles_user_idx ON employee_profiles(user_id);
CREATE INDEX IF NOT EXISTS employee_profiles_email_idx ON employee_profiles(email);
CREATE INDEX IF NOT EXISTS employee_profiles_department_idx ON employee_profiles(department);
CREATE INDEX IF NOT EXISTS employee_profiles_status_idx ON employee_profiles(employment_status);
CREATE INDEX IF NOT EXISTS employee_publications_employee_idx ON employee_publications(employee_id);

-- ============================================================================
-- VIEWS FOR STATISTICS
-- ============================================================================

-- Library statistics view
CREATE OR REPLACE VIEW library_statistics AS
SELECT
    COUNT(*) as total_books,
    COUNT(*) FILTER (WHERE status = 'доступна') as available_books,
    COUNT(*) FILTER (WHERE status = 'позајмљена') as borrowed_books,
    COUNT(DISTINCT category) as total_categories,
    COUNT(DISTINCT author) as total_authors
FROM library_books;

-- Exhibition statistics view
CREATE OR REPLACE VIEW exhibition_statistics AS
SELECT
    COUNT(*) as total_exhibitions,
    COUNT(*) FILTER (WHERE status = 'активна') as active_exhibitions,
    COUNT(*) FILTER (WHERE status = 'завршена') as completed_exhibitions,
    COUNT(*) FILTER (WHERE status = 'планирана') as planned_exhibitions,
    SUM(visitor_count) as total_visitors
FROM exhibitions;

-- Heritage statistics view
CREATE OR REPLACE VIEW heritage_statistics AS
SELECT
    COUNT(*) as total_items,
    COUNT(DISTINCT heritage_type) as total_types,
    COUNT(DISTINCT category) as total_categories,
    COUNT(*) FILTER (WHERE protection_status IS NOT NULL) as protected_items
FROM heritage_items;

-- Meteorite statistics view
CREATE OR REPLACE VIEW meteorite_statistics AS
SELECT
    COUNT(*) as total_specimens,
    COUNT(DISTINCT meteorite_class) as total_classes,
    SUM(mass) as total_mass_grams,
    COUNT(*) FILTER (WHERE fall_witnessed = TRUE) as witnessed_falls,
    COUNT(*) FILTER (WHERE fall_witnessed = FALSE) as finds
FROM meteorite_specimens;

-- Employee statistics view
CREATE OR REPLACE VIEW employee_statistics AS
SELECT
    COUNT(*) as total_employees,
    COUNT(*) FILTER (WHERE employment_status = 'активан') as active_employees,
    COUNT(DISTINCT department) as total_departments,
    COUNT(DISTINCT academic_degree) as degree_types
FROM employee_profiles;

-- ============================================================================
-- GRANTS (optional - adjust based on your security needs)
-- ============================================================================

-- Grant permissions to your application user if needed
-- GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO aleksandarlukovic;
-- GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO aleksandarlukovic;

-- ============================================================================
-- COMPLETION TIMESTAMP
-- ============================================================================

COMMENT ON TABLE library_books IS 'Phase 3A: Library database - Migrated from library_database.json';
COMMENT ON TABLE exhibitions IS 'Phase 3A: Exhibitions database - Migrated from exhibitions.json';
COMMENT ON TABLE heritage_items IS 'Phase 3A: Cultural heritage database - Migrated from CULTURAL_HERITAGE_DATABASE dict';
COMMENT ON TABLE meteorite_specimens IS 'Phase 3A: Meteorite collection - Migrated from METEORITE_COLLECTION_DATABASE dict';
COMMENT ON TABLE employee_profiles IS 'Phase 3A: Employee database - Enhanced from employee_directory.json';

-- ============================================================================
-- END OF SCHEMA
-- ============================================================================
