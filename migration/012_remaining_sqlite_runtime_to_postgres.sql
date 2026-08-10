-- Remaining runtime SQLite features -> PostgreSQL
-- Adds scientific papers, chat, and mail-cache tables.

CREATE TABLE IF NOT EXISTS scientific_papers (
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

CREATE TABLE IF NOT EXISTS paper_locality_links (
    id BIGSERIAL PRIMARY KEY,
    paper_id BIGINT NOT NULL REFERENCES scientific_papers(id) ON DELETE CASCADE,
    locality_name TEXT NOT NULL,
    ogk_code TEXT,
    link_type TEXT DEFAULT 'search',
    relevance_rank INTEGER DEFAULT 0,
    search_query TEXT,
    UNIQUE (paper_id, locality_name)
);

CREATE TABLE IF NOT EXISTS paper_feature_links (
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

CREATE INDEX IF NOT EXISTS scientific_papers_doi_idx ON scientific_papers(doi);
CREATE INDEX IF NOT EXISTS scientific_papers_year_idx ON scientific_papers(publication_year);
CREATE INDEX IF NOT EXISTS scientific_papers_citations_idx ON scientific_papers(cited_by_count DESC);
CREATE INDEX IF NOT EXISTS scientific_papers_journal_idx ON scientific_papers(journal_name);
CREATE INDEX IF NOT EXISTS scientific_papers_language_idx ON scientific_papers(language);
CREATE INDEX IF NOT EXISTS scientific_papers_oa_idx ON scientific_papers(is_open_access);
CREATE INDEX IF NOT EXISTS scientific_papers_search_idx
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
CREATE INDEX IF NOT EXISTS paper_locality_links_paper_idx ON paper_locality_links(paper_id);
CREATE INDEX IF NOT EXISTS paper_locality_links_locality_idx ON paper_locality_links(locality_name);
CREATE INDEX IF NOT EXISTS paper_locality_links_ogk_idx ON paper_locality_links(ogk_code);
CREATE INDEX IF NOT EXISTS paper_feature_links_paper_idx ON paper_feature_links(paper_id);
CREATE INDEX IF NOT EXISTS paper_feature_links_type_name_idx ON paper_feature_links(feature_type, feature_name);

CREATE TABLE IF NOT EXISTS chat_messages (
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

CREATE TABLE IF NOT EXISTS chat_presence (
    user_id INTEGER PRIMARY KEY,
    user_name TEXT NOT NULL,
    user_email CITEXT NOT NULL,
    user_department TEXT DEFAULT '',
    status TEXT NOT NULL DEFAULT 'online',
    last_seen DOUBLE PRECISION NOT NULL
);

CREATE TABLE IF NOT EXISTS chat_unread_cursors (
    user_id INTEGER NOT NULL,
    channel TEXT NOT NULL,
    last_read_epoch DOUBLE PRECISION NOT NULL DEFAULT 0,
    PRIMARY KEY (user_id, channel)
);

CREATE INDEX IF NOT EXISTS chat_messages_channel_idx ON chat_messages(channel, ts_epoch DESC);
CREATE INDEX IF NOT EXISTS chat_messages_user_idx ON chat_messages(user_id, channel, ts_epoch DESC);

CREATE TABLE IF NOT EXISTS mail_cache_folders (
    user_email CITEXT NOT NULL,
    name TEXT NOT NULL,
    uidvalidity BIGINT DEFAULT 0,
    highest_uid BIGINT DEFAULT 0,
    unseen INTEGER DEFAULT 0,
    PRIMARY KEY (user_email, name)
);

CREATE TABLE IF NOT EXISTS mail_cache_messages (
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

CREATE TABLE IF NOT EXISTS mail_cache_meta (
    user_email CITEXT NOT NULL,
    key TEXT NOT NULL,
    value TEXT,
    PRIMARY KEY (user_email, key)
);

CREATE TABLE IF NOT EXISTS mail_cache_pending_reads (
    user_email CITEXT NOT NULL,
    folder TEXT NOT NULL,
    uid BIGINT NOT NULL,
    PRIMARY KEY (user_email, folder, uid)
);

CREATE INDEX IF NOT EXISTS mail_cache_messages_folder_idx
    ON mail_cache_messages(user_email, folder, uid DESC);
CREATE INDEX IF NOT EXISTS mail_cache_messages_date_idx
    ON mail_cache_messages(user_email, folder, date_iso DESC, uid DESC);
CREATE INDEX IF NOT EXISTS mail_cache_messages_sender_idx
    ON mail_cache_messages(user_email, folder, lower(from_name), uid DESC);
CREATE INDEX IF NOT EXISTS mail_cache_messages_subject_idx
    ON mail_cache_messages(user_email, folder, lower(subject), uid DESC);
CREATE INDEX IF NOT EXISTS mail_cache_messages_read_idx
    ON mail_cache_messages(user_email, folder, is_read, uid DESC);
