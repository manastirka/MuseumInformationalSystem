-- ============================================================================
-- Migration 005: Digital Signature Management System
-- ============================================================================
-- Date: January 2026
-- Creates tables for tracking digital signatures on documents
-- Based on Serbian law requirements for Qualified Electronic Signatures (KEP)
-- ============================================================================

-- ============================================================================
-- Document Signatures Table
-- ============================================================================
CREATE TABLE IF NOT EXISTS document_signatures (
    id SERIAL PRIMARY KEY,

    -- Document reference
    document_type VARCHAR(100) NOT NULL,  -- 'zahtev_godisnji', 'zahtev_slobodan_dan', 'putni_nalog', etc.
    document_id INTEGER,  -- Reference to archive_requests or other tables
    document_title VARCHAR(500) NOT NULL,
    document_pdf_path VARCHAR(500),  -- Path to generated PDF

    -- Requester info
    requester_email VARCHAR(255) NOT NULL,
    requester_name VARCHAR(255),
    requester_department VARCHAR(255),

    -- Signature status
    status VARCHAR(50) DEFAULT 'pending_signature',
    -- pending_signature, signed_by_requester, pending_legal_verification,
    -- verified, rejected, archived

    -- Requester signature
    requester_signed_at TIMESTAMP,
    requester_signature_valid BOOLEAN DEFAULT FALSE,
    requester_certificate_info JSONB DEFAULT '{}',

    -- Legal verification (by Ana Živanović / sef_pravne_sluzbe)
    legal_verified_at TIMESTAMP,
    legal_verified_by_email VARCHAR(255),
    legal_verified_by_name VARCHAR(255),
    legal_verification_notes TEXT,
    legal_certificate_info JSONB DEFAULT '{}',

    -- Director/Approver signature (if needed)
    approver_signed_at TIMESTAMP,
    approver_email VARCHAR(255),
    approver_name VARCHAR(255),
    approver_certificate_info JSONB DEFAULT '{}',

    -- Registration (delovodni broj)
    registration_number VARCHAR(100),  -- e.g., "01-1234/2026"
    registered_at TIMESTAMP,
    registered_by_email VARCHAR(255),

    -- Metadata
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    notes TEXT,

    -- Original document data (for verification)
    document_hash VARCHAR(256),  -- SHA-256 hash of original document
    signed_document_path VARCHAR(500)  -- Path to signed PDF
);

-- ============================================================================
-- Signature Audit Log
-- ============================================================================
CREATE TABLE IF NOT EXISTS signature_audit_log (
    id SERIAL PRIMARY KEY,
    document_signature_id INTEGER REFERENCES document_signatures(id) ON DELETE CASCADE,

    action VARCHAR(100) NOT NULL,  -- 'created', 'signed', 'verified', 'rejected', 'registered'
    action_by_email VARCHAR(255) NOT NULL,
    action_by_name VARCHAR(255),
    action_details JSONB DEFAULT '{}',

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================================
-- Signature Templates (for different document types)
-- ============================================================================
CREATE TABLE IF NOT EXISTS signature_templates (
    id SERIAL PRIMARY KEY,
    document_type VARCHAR(100) UNIQUE NOT NULL,
    document_type_label VARCHAR(255) NOT NULL,  -- Serbian label

    -- Signature requirements
    requires_requester_signature BOOLEAN DEFAULT TRUE,
    requires_legal_verification BOOLEAN DEFAULT TRUE,
    requires_approver_signature BOOLEAN DEFAULT FALSE,
    approver_roles JSONB DEFAULT '[]',  -- Which roles can approve

    -- Template info
    template_path VARCHAR(500),
    instructions TEXT,  -- Instructions for signing

    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================================
-- Insert default signature templates
-- ============================================================================
INSERT INTO signature_templates (document_type, document_type_label, requires_requester_signature, requires_legal_verification, requires_approver_signature, approver_roles, instructions) VALUES
('zahtev_godisnji_odmor', 'Захтев за годишњи одмор', TRUE, TRUE, TRUE, '["sef_odeljenja", "direktor"]',
 'Документ мора бити потписан квалификованим електронским потписом (КЕП). Користите личну карту са чипом или USB токен.'),
('zahtev_slobodan_dan', 'Захтев за слободан дан', TRUE, TRUE, TRUE, '["sef_odeljenja"]',
 'Документ мора бити потписан квалификованим електронским потписом (КЕП).'),
('zahtev_bolovanje', 'Захтев за боловање', TRUE, TRUE, FALSE, '[]',
 'Уз захтев приложити медицинску документацију. Потписати КЕП-ом.'),
('putni_nalog', 'Путни налог', TRUE, TRUE, TRUE, '["sef_odeljenja", "direktor", "sef_racunovodstva"]',
 'Путни налог мора бити потписан пре поласка на службени пут.'),
('zahtev_nabavka', 'Захтев за набавку', TRUE, TRUE, TRUE, '["sef_odeljenja", "sef_racunovodstva", "direktor"]',
 'Захтев за набавку мора садржати образложење и предрачун.'),
('finansijski_dokument', 'Финансијски документ', TRUE, TRUE, TRUE, '["sef_racunovodstva", "direktor"]',
 'Финансијски документи захтевају верификацију рачуноводства.')
ON CONFLICT (document_type) DO NOTHING;

-- ============================================================================
-- Indexes
-- ============================================================================
CREATE INDEX IF NOT EXISTS idx_doc_signatures_status ON document_signatures(status);
CREATE INDEX IF NOT EXISTS idx_doc_signatures_requester ON document_signatures(requester_email);
CREATE INDEX IF NOT EXISTS idx_doc_signatures_type ON document_signatures(document_type);
CREATE INDEX IF NOT EXISTS idx_doc_signatures_created ON document_signatures(created_at);
CREATE INDEX IF NOT EXISTS idx_signature_audit_doc ON signature_audit_log(document_signature_id);

-- ============================================================================
-- Comments
-- ============================================================================
COMMENT ON TABLE document_signatures IS 'Tracks digital signatures on official documents per Serbian KEP requirements';
COMMENT ON TABLE signature_audit_log IS 'Audit trail for all signature-related actions';
COMMENT ON TABLE signature_templates IS 'Configuration for different document types requiring signatures';

COMMENT ON COLUMN document_signatures.document_hash IS 'SHA-256 hash of original document for integrity verification';
COMMENT ON COLUMN document_signatures.registration_number IS 'Official registration number (delovodni broj)';

-- ============================================================================
-- END OF MIGRATION
-- ============================================================================
