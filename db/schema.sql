-- Museum Information System - Phase 2 PostgreSQL Schema
-- Run with: psql -f db/schema.sql postgresql://user:pass@host:port/museum_system

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS pgcrypto;
CREATE EXTENSION IF NOT EXISTS postgis;
CREATE EXTENSION IF NOT EXISTS citext;

-- Reference tables ---------------------------------------------------------

CREATE TABLE departments (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    created_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE roles (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL UNIQUE CHECK (name IN ('admin', 'employee', 'curator', 'viewer')),
    description TEXT
);

-- Core security tables -----------------------------------------------------

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email CITEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    salt TEXT NOT NULL,
    full_name TEXT NOT NULL,
    role_id INTEGER REFERENCES roles(id),
    department_id INTEGER REFERENCES departments(id),
    position TEXT,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    last_login_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE user_sessions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id INTEGER REFERENCES users(id),
    session_key TEXT NOT NULL UNIQUE,
    issued_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    expires_at TIMESTAMPTZ NOT NULL,
    ip_address INET,
    user_agent TEXT
);

-- Minerals ----------------------------------------------------------------

CREATE TABLE minerals (
    id SERIAL PRIMARY KEY,
    inventory_number VARCHAR(50) UNIQUE,
    item_name TEXT,
    acquisition_method TEXT,
    acquisition_date DATE,
    input_date TIMESTAMPTZ,
    input_by TEXT,
    donor TEXT,
    identifier TEXT,
    comments TEXT,
    description TEXT,
    storage_location TEXT,
    card_locality TEXT,
    bibliography_flag BOOLEAN,
    quantity INTEGER,
    created_at TIMESTAMPTZ DEFAULT now(),
    updated_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE mineral_references (
    id SERIAL PRIMARY KEY,
    mineral_name TEXT NOT NULL,
    mineral_name_alt TEXT,
    mineral_species TEXT,
    chemical_formula TEXT,
    crystal_system TEXT,
    hardness TEXT,
    specific_gravity TEXT,
    color TEXT,
    streak TEXT,
    luster TEXT,
    transparency TEXT,
    fracture TEXT,
    cleavage TEXT,
    occurrence TEXT,
    locality TEXT,
    created_at TIMESTAMPTZ DEFAULT now(),
    updated_at TIMESTAMPTZ DEFAULT now()
);

-- Bird ringing -------------------------------------------------------------

CREATE TABLE bird_species (
    id SERIAL PRIMARY KEY,
    species_name TEXT UNIQUE NOT NULL
);

CREATE TABLE bird_ringing_records (
    id BIGSERIAL PRIMARY KEY,
    ring_number TEXT,
    color_ring TEXT,
    species_id INTEGER REFERENCES bird_species(id),
    age TEXT,
    sex TEXT,
    location TEXT,
    coordinates GEOGRAPHY(Point, 4326),
    coordinate_accuracy TEXT,
    event_date DATE,
    event_time TIME,
    metal_ring_position INTEGER,
    plastic_ring TEXT,
    catching_method TEXT,
    bait TEXT,
    manipulation TEXT,
    status TEXT,
    clutch_size TEXT,
    pullus_age TEXT,
    wing_length TEXT,
    third_primary_feather TEXT,
    mass TEXT,
    molting TEXT,
    back_claw TEXT,
    bill_length TEXT,
    bill_measurement_method TEXT,
    head_length TEXT,
    tarsus TEXT,
    tarsus_measurement_method TEXT,
    tail_length TEXT,
    fat_deposits TEXT,
    pectoral_muscle TEXT,
    incubation_patch TEXT,
    alula TEXT,
    carpal_feathers TEXT,
    sex_determination TEXT,
    protected_areas TEXT,
    ringer TEXT,
    notes TEXT,
    raw_json JSONB,
    created_at TIMESTAMPTZ DEFAULT now()
);

CREATE INDEX bird_ringing_geo_idx ON bird_ringing_records USING GIST(coordinates);
CREATE INDEX bird_ringing_species_idx ON bird_ringing_records(species_id);
CREATE INDEX bird_ringing_date_idx ON bird_ringing_records(event_date);

-- Inventory (library / exhibits) ------------------------------------------

CREATE TABLE inventory_entries (
    id SERIAL PRIMARY KEY,
    inventory_number TEXT UNIQUE,
    inventory_number_raw TEXT,
    name TEXT,
    locality TEXT,
    quantity TEXT,
    acquisition_info TEXT,
    collector TEXT,
    notes TEXT,
    sheet TEXT,
    row_number INTEGER,
    category TEXT,
    revisited BOOLEAN DEFAULT FALSE,
    physical_location TEXT,
    revision_date DATE,
    created_at TIMESTAMPTZ DEFAULT now()
);

-- Timesheet ---------------------------------------------------------------

CREATE TABLE timesheet_reports (
    id BIGSERIAL PRIMARY KEY,
    legacy_radna_lista_id INTEGER UNIQUE,
    employee_name TEXT NOT NULL,
    month SMALLINT NOT NULL,
    year INTEGER NOT NULL,
    organization_unit TEXT,
    position TEXT,
    special_scope TEXT,
    extraordinary_tasks TEXT,
    employee_signature TEXT,
    approver TEXT,
    manager_signature TEXT,
    director_signature TEXT,
    salary_adjustment TEXT,
    duties_summary TEXT,
    created_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE timesheet_report_days (
    id BIGSERIAL PRIMARY KEY,
    report_id INTEGER REFERENCES timesheet_reports(id) ON DELETE CASCADE,
    day SMALLINT NOT NULL,
    work_in_museum NUMERIC(5,2) DEFAULT 0,
    work_outside NUMERIC(5,2) DEFAULT 0,
    vacation NUMERIC(5,2) DEFAULT 0,
    public_holiday NUMERIC(5,2) DEFAULT 0,
    paid_leave NUMERIC(5,2) DEFAULT 0,
    other_leave NUMERIC(5,2) DEFAULT 0,
    sick_leave_lt30 NUMERIC(5,2) DEFAULT 0,
    sick_leave_gte30 NUMERIC(5,2) DEFAULT 0,
    UNIQUE (report_id, day)
);

CREATE TABLE timesheet_entries (
    id BIGSERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    report_id INTEGER REFERENCES timesheet_reports(id) ON DELETE CASCADE,
    employee_name TEXT,
    work_date DATE NOT NULL,
    category TEXT,
    hours NUMERIC(5,2),
    notes TEXT,
    created_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE user_activity_log (
    id BIGSERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    action TEXT NOT NULL,
    metadata JSONB,
    created_at TIMESTAMPTZ DEFAULT now()
);

-- Audit / logging ---------------------------------------------------------

CREATE TABLE audit_log (
    id BIGSERIAL PRIMARY KEY,
    table_name TEXT NOT NULL,
    record_id BIGINT,
    action TEXT NOT NULL,
    old_values JSONB,
    new_values JSONB,
    performed_by INTEGER REFERENCES users(id),
    performed_at TIMESTAMPTZ DEFAULT now(),
    ip_address INET
);

CREATE INDEX audit_table_idx ON audit_log(table_name, record_id);

-- Scientific papers -------------------------------------------------------

CREATE TABLE scientific_papers (
    id BIGSERIAL PRIMARY KEY,
    openalex_id TEXT UNIQUE,
    doi TEXT,
    title TEXT NOT NULL,
    abstract TEXT,
    publication_year INTEGER,
    cited_by_count INTEGER DEFAULT 0,
    journal_name TEXT,
    volume TEXT,
    issue TEXT,
    authors_json TEXT,
    keywords_json TEXT,
    concepts_json TEXT,
    is_open_access BOOLEAN DEFAULT FALSE,
    oa_url TEXT,
    pdf_url TEXT,
    language TEXT,
    source_api TEXT DEFAULT 'openalex',
    search_query TEXT,
    fetch_date TEXT,
    created_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE paper_locality_links (
    id BIGSERIAL PRIMARY KEY,
    paper_id BIGINT NOT NULL REFERENCES scientific_papers(id) ON DELETE CASCADE,
    locality_name TEXT NOT NULL,
    ogk_code TEXT,
    link_type TEXT DEFAULT 'search',
    relevance_rank INTEGER DEFAULT 0,
    search_query TEXT,
    UNIQUE (paper_id, locality_name)
);

CREATE TABLE paper_feature_links (
    id BIGSERIAL PRIMARY KEY,
    paper_id BIGINT NOT NULL REFERENCES scientific_papers(id) ON DELETE CASCADE,
    feature_type TEXT NOT NULL,
    feature_name TEXT NOT NULL,
    feature_id TEXT,
    link_type TEXT DEFAULT 'search',
    relevance_rank INTEGER DEFAULT 0,
    search_query TEXT,
    UNIQUE (paper_id, feature_type, feature_name)
);

CREATE INDEX scientific_papers_doi_idx ON scientific_papers(doi);
CREATE INDEX scientific_papers_year_idx ON scientific_papers(publication_year);
CREATE INDEX scientific_papers_citations_idx ON scientific_papers(cited_by_count DESC);
CREATE INDEX scientific_papers_journal_idx ON scientific_papers(journal_name);
CREATE INDEX scientific_papers_language_idx ON scientific_papers(language);
CREATE INDEX scientific_papers_oa_idx ON scientific_papers(is_open_access);
CREATE INDEX scientific_papers_search_idx
    ON scientific_papers
    USING gin (
        to_tsvector(
            'simple',
            COALESCE(title, '') || ' ' ||
            COALESCE(abstract, '') || ' ' ||
            COALESCE(authors_json, '') || ' ' ||
            COALESCE(keywords_json, '')
        )
    );
CREATE INDEX paper_locality_links_paper_idx ON paper_locality_links(paper_id);
CREATE INDEX paper_locality_links_locality_idx ON paper_locality_links(locality_name);
CREATE INDEX paper_locality_links_ogk_idx ON paper_locality_links(ogk_code);
CREATE INDEX paper_feature_links_paper_idx ON paper_feature_links(paper_id);
CREATE INDEX paper_feature_links_type_name_idx ON paper_feature_links(feature_type, feature_name);

-- Chat --------------------------------------------------------------------

CREATE TABLE chat_messages (
    id BIGSERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    user_name TEXT NOT NULL,
    user_email CITEXT NOT NULL,
    user_department TEXT DEFAULT '',
    channel TEXT NOT NULL DEFAULT 'general',
    message TEXT NOT NULL DEFAULT '',
    file_name TEXT,
    file_path TEXT,
    file_size BIGINT,
    file_type TEXT,
    timestamp TEXT NOT NULL,
    ts_epoch DOUBLE PRECISION NOT NULL
);

CREATE TABLE chat_presence (
    user_id INTEGER PRIMARY KEY,
    user_name TEXT NOT NULL,
    user_email CITEXT NOT NULL,
    user_department TEXT DEFAULT '',
    status TEXT NOT NULL DEFAULT 'online',
    last_seen DOUBLE PRECISION NOT NULL
);

CREATE TABLE chat_unread_cursors (
    user_id INTEGER NOT NULL,
    channel TEXT NOT NULL,
    last_read_epoch DOUBLE PRECISION NOT NULL DEFAULT 0,
    PRIMARY KEY (user_id, channel)
);

CREATE INDEX chat_messages_channel_idx ON chat_messages(channel, ts_epoch DESC);
CREATE INDEX chat_messages_user_idx ON chat_messages(user_id, channel, ts_epoch DESC);

-- Mail cache --------------------------------------------------------------

CREATE TABLE mail_cache_folders (
    user_email CITEXT NOT NULL,
    name TEXT NOT NULL,
    uidvalidity BIGINT DEFAULT 0,
    highest_uid BIGINT DEFAULT 0,
    unseen INTEGER DEFAULT 0,
    PRIMARY KEY (user_email, name)
);

CREATE TABLE mail_cache_messages (
    user_email CITEXT NOT NULL,
    folder TEXT NOT NULL,
    uid BIGINT NOT NULL,
    from_name TEXT DEFAULT '',
    from_address TEXT DEFAULT '',
    reply_to_name TEXT DEFAULT '',
    reply_to_address TEXT DEFAULT '',
    subject TEXT DEFAULT '',
    date_iso TEXT DEFAULT '',
    is_read BOOLEAN DEFAULT FALSE,
    has_body BOOLEAN DEFAULT FALSE,
    text_body TEXT DEFAULT '',
    html_body TEXT DEFAULT '',
    to_json TEXT DEFAULT '[]',
    cc_json TEXT DEFAULT '[]',
    attachments_json TEXT DEFAULT '[]',
    links_json TEXT DEFAULT '[]',
    PRIMARY KEY (user_email, folder, uid)
);

CREATE TABLE mail_cache_meta (
    user_email CITEXT NOT NULL,
    key TEXT NOT NULL,
    value TEXT,
    PRIMARY KEY (user_email, key)
);

CREATE TABLE mail_cache_pending_reads (
    user_email CITEXT NOT NULL,
    folder TEXT NOT NULL,
    uid BIGINT NOT NULL,
    PRIMARY KEY (user_email, folder, uid)
);

CREATE INDEX mail_cache_messages_folder_idx ON mail_cache_messages(user_email, folder, uid DESC);
CREATE INDEX mail_cache_messages_date_idx ON mail_cache_messages(user_email, folder, date_iso DESC, uid DESC);
CREATE INDEX mail_cache_messages_sender_idx ON mail_cache_messages(user_email, folder, lower(from_name), uid DESC);
CREATE INDEX mail_cache_messages_subject_idx ON mail_cache_messages(user_email, folder, lower(subject), uid DESC);
CREATE INDEX mail_cache_messages_read_idx ON mail_cache_messages(user_email, folder, is_read, uid DESC);

-- Staging tables (for ETL) ------------------------------------------------

CREATE TABLE staging_bird_ringing (
    ring_number TEXT,
    color_ring TEXT,
    species_name TEXT,
    age TEXT,
    sex TEXT,
    location TEXT,
    coordinates_wkt TEXT,
    coordinate_accuracy TEXT,
    event_date TEXT,
    event_time TEXT,
    metal_ring_position TEXT,
    plastic_ring TEXT,
    catching_method TEXT,
    bait TEXT,
    manipulation TEXT,
    status TEXT,
    clutch_size TEXT,
    pullus_age TEXT,
    wing_length TEXT,
    third_primary_feather TEXT,
    mass TEXT,
    molting TEXT,
    back_claw TEXT,
    bill_length TEXT,
    bill_measurement_method TEXT,
    head_length TEXT,
    tarsus TEXT,
    tarsus_measurement_method TEXT,
    tail_length TEXT,
    fat_deposits TEXT,
    pectoral_muscle TEXT,
    incubation_patch TEXT,
    alula TEXT,
    carpal_feathers TEXT,
    sex_determination TEXT,
    protected_areas TEXT,
    ringer TEXT,
    notes TEXT,
    raw_json JSONB
);

CREATE TABLE staging_minerals (
    inventory_number TEXT,
    item_name TEXT,
    acquisition_method TEXT,
    acquisition_date TEXT,
    input_date TEXT,
    input_by TEXT,
    donor TEXT,
    identifier TEXT,
    comments TEXT,
    description TEXT,
    storage_location TEXT,
    card_locality TEXT,
    bibliography_flag TEXT,
    quantity TEXT
);

CREATE TABLE staging_inventory (
    inventory_number TEXT,
    inventory_number_raw TEXT,
    name TEXT,
    locality TEXT,
    quantity TEXT,
    acquisition_info TEXT,
    collector TEXT,
    notes TEXT,
    sheet TEXT,
    row_number TEXT,
    category TEXT,
    revisited TEXT,
    physical_location TEXT,
    revision_date TEXT
);

CREATE TABLE staging_timesheet_reports (
    radna_lista_id INTEGER,
    ime_prezime TEXT,
    mesec INTEGER,
    godina INTEGER,
    organizaciona_jedinica TEXT,
    radno_mesto TEXT,
    poseban_obim_posla TEXT,
    vanredni_poslovi TEXT,
    potpis_zaposlenog TEXT,
    nalogodavac TEXT,
    potpis_sefa TEXT,
    potpis_direktora TEXT,
    povecanje_umanjenje_zarade TEXT,
    o_posao TEXT,
    created_at TEXT
);

CREATE TABLE staging_timesheet_days (
    radna_lista_id INTEGER,
    dan INTEGER,
    rad_na_mestu REAL,
    van_muzeja REAL,
    godisnji_odmor REAL,
    drzavni_praznik REAL,
    placeno_odsustvo REAL,
    ostalo_odsustvo REAL,
    bolovanje_manje_30 REAL,
    bolovanje_vece_30 REAL
);
