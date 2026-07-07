-- ============================================================================
-- Migration 017: Document library (складиштење, преглед и одобравање докумената)
-- ============================================================================
-- Date: July 2026
-- Central registry for classic museum documents (обрасци, упутства,
-- правилници...). Files live on disk under DOCUMENTS_STORAGE_PATH
-- (production: /data/mis/dokumenti); the database stores only the relative
-- path, metadata and a sha256 checksum. Every upload is a new version with
-- an approval workflow: nacrt -> na_odobrenju -> odobreno -> arhivirano
-- (rejection returns the version to nacrt with a review comment).
-- Safe to run repeatedly (IF NOT EXISTS everywhere).
-- ============================================================================

CREATE TABLE IF NOT EXISTS documents (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    category TEXT NOT NULL CHECK (category IN (
        'obrasci_zahtevi', 'uputstva', 'pravilnici', 'finansije',
        'izvestaji', 'organizacija', 'ostalo'
    )),
    department TEXT,
    created_by_email TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    is_active BOOLEAN NOT NULL DEFAULT TRUE
);

COMMENT ON TABLE documents IS
    'Logical museum documents; the actual files are per-version rows in document_versions';

CREATE TABLE IF NOT EXISTS document_versions (
    id SERIAL PRIMARY KEY,
    document_id INTEGER NOT NULL REFERENCES documents(id) ON DELETE CASCADE,
    version_no INTEGER NOT NULL,
    file_path TEXT NOT NULL,
    original_filename TEXT NOT NULL,
    mime_type TEXT,
    file_size BIGINT,
    sha256 CHAR(64),
    status TEXT NOT NULL DEFAULT 'nacrt' CHECK (status IN (
        'nacrt', 'na_odobrenju', 'odobreno', 'arhivirano'
    )),
    uploaded_by_email TEXT NOT NULL,
    uploaded_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    submitted_at TIMESTAMPTZ,
    reviewed_by_email TEXT,
    reviewed_at TIMESTAMPTZ,
    review_comment TEXT,
    UNIQUE (document_id, version_no)
);

COMMENT ON TABLE document_versions IS
    'One row per uploaded file version; file_path is relative to DOCUMENTS_STORAGE_PATH';

CREATE TABLE IF NOT EXISTS document_audit_log (
    id SERIAL PRIMARY KEY,
    document_id INTEGER NOT NULL REFERENCES documents(id) ON DELETE CASCADE,
    version_id INTEGER REFERENCES document_versions(id) ON DELETE SET NULL,
    action TEXT NOT NULL,
    actor_email TEXT NOT NULL,
    note TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

COMMENT ON TABLE document_audit_log IS
    'Who did what and when across the document approval workflow';

CREATE INDEX IF NOT EXISTS idx_documents_category ON documents (category);
CREATE INDEX IF NOT EXISTS idx_document_versions_document_id ON document_versions (document_id);
CREATE INDEX IF NOT EXISTS idx_document_versions_status ON document_versions (status);
CREATE INDEX IF NOT EXISTS idx_document_audit_log_document_id ON document_audit_log (document_id);

-- Rollback:
-- DROP TABLE IF EXISTS document_audit_log;
-- DROP TABLE IF EXISTS document_versions;
-- DROP TABLE IF EXISTS documents;
