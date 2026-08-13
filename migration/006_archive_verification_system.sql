-- ============================================================================
-- Migration 004: Archive and Verification System
-- ============================================================================
-- Date: January 2026
-- Creates tables for comprehensive archive and multi-level approval system
-- ============================================================================

-- Add new roles for approval workflow
INSERT INTO roles (name, description)
VALUES
    ('sef_odeljenja', 'Department Head with approval authority'),
    ('sef_racunovodstva', 'Head of Accounting with financial approval authority')
ON CONFLICT (name) DO NOTHING;

-- Update roles check constraint to include new roles
ALTER TABLE roles DROP CONSTRAINT IF EXISTS roles_name_check;
ALTER TABLE roles ADD CONSTRAINT roles_name_check CHECK (
    name = ANY (ARRAY['admin', 'employee', 'curator', 'viewer', 'direktor', 'sef_odeljenja', 'sef_racunovodstva'])
);

-- ============================================================================
-- Main Archive Requests Table
-- ============================================================================
CREATE TABLE IF NOT EXISTS archive_requests (
    id SERIAL PRIMARY KEY,

    -- Request classification
    request_type VARCHAR(50) NOT NULL,  -- 'zahtev', 'finansije', 'terenska_aktivnost'
    subtype VARCHAR(100),  -- specific subtype

    -- Request content
    title VARCHAR(500) NOT NULL,
    description TEXT,
    request_data JSONB DEFAULT '{}',  -- flexible storage for type-specific data

    -- Status tracking
    status VARCHAR(50) DEFAULT 'pending',  -- pending, in_review, approved, rejected, archived
    priority VARCHAR(20) DEFAULT 'normal',  -- low, normal, high, urgent

    -- Creator info
    created_by_email VARCHAR(255) NOT NULL,
    created_by_name VARCHAR(255),
    created_by_department VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    -- Document attachments
    attachments JSONB DEFAULT '[]',

    -- Approval tracking
    approval_chain JSONB DEFAULT '[]',  -- ordered list of required approvers with roles
    current_approval_step INTEGER DEFAULT 0,

    -- Final status
    final_decision VARCHAR(50),
    final_decision_by_email VARCHAR(255),
    final_decision_by_name VARCHAR(255),
    final_decision_at TIMESTAMP,
    final_notes TEXT,

    -- Archive info
    archived_at TIMESTAMP,
    archive_reference VARCHAR(100),
    archive_year INTEGER
);

-- ============================================================================
-- Approval Signatures Table
-- ============================================================================
CREATE TABLE IF NOT EXISTS approval_signatures (
    id SERIAL PRIMARY KEY,
    request_id INTEGER REFERENCES archive_requests(id) ON DELETE CASCADE,

    -- Approver info
    approver_role VARCHAR(100) NOT NULL,  -- 'sef_odeljenja', 'sef_racunovodstva', 'direktor'
    approver_email VARCHAR(255),
    approver_name VARCHAR(255),

    -- Decision
    decision VARCHAR(20) DEFAULT 'pending',  -- 'approved', 'rejected', 'pending'
    comments TEXT,
    signed_at TIMESTAMP,

    -- Order in chain
    signature_order INTEGER NOT NULL,

    UNIQUE(request_id, approver_role)
);

-- ============================================================================
-- Request Comments Table
-- ============================================================================
CREATE TABLE IF NOT EXISTS request_comments (
    id SERIAL PRIMARY KEY,
    request_id INTEGER REFERENCES archive_requests(id) ON DELETE CASCADE,

    -- Author info
    author_email VARCHAR(255) NOT NULL,
    author_name VARCHAR(255),

    -- Comment content
    comment TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================================
-- Request History/Audit Table
-- ============================================================================
CREATE TABLE IF NOT EXISTS request_history (
    id SERIAL PRIMARY KEY,
    request_id INTEGER REFERENCES archive_requests(id) ON DELETE CASCADE,

    -- Action details
    action VARCHAR(100) NOT NULL,  -- 'created', 'updated', 'approved', 'rejected', 'commented', 'archived'
    action_by_email VARCHAR(255) NOT NULL,
    action_by_name VARCHAR(255),

    -- Changes
    old_values JSONB,
    new_values JSONB,
    notes TEXT,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================================
-- Indexes for Performance
-- ============================================================================
CREATE INDEX IF NOT EXISTS idx_archive_requests_type ON archive_requests(request_type);
CREATE INDEX IF NOT EXISTS idx_archive_requests_subtype ON archive_requests(subtype);
CREATE INDEX IF NOT EXISTS idx_archive_requests_status ON archive_requests(status);
CREATE INDEX IF NOT EXISTS idx_archive_requests_created_by ON archive_requests(created_by_email);
CREATE INDEX IF NOT EXISTS idx_archive_requests_created_at ON archive_requests(created_at);
CREATE INDEX IF NOT EXISTS idx_archive_requests_archive_year ON archive_requests(archive_year);

CREATE INDEX IF NOT EXISTS idx_approval_signatures_request ON approval_signatures(request_id);
CREATE INDEX IF NOT EXISTS idx_approval_signatures_approver ON approval_signatures(approver_email);
CREATE INDEX IF NOT EXISTS idx_approval_signatures_decision ON approval_signatures(decision);

CREATE INDEX IF NOT EXISTS idx_request_comments_request ON request_comments(request_id);
CREATE INDEX IF NOT EXISTS idx_request_history_request ON request_history(request_id);

-- ============================================================================
-- Comments on Tables and Columns
-- ============================================================================
COMMENT ON TABLE archive_requests IS 'Main table for all archive requests (zahtevi, finansije, terenska aktivnost)';
COMMENT ON TABLE approval_signatures IS 'Tracks approval decisions by each approver in the chain';
COMMENT ON TABLE request_comments IS 'Discussion comments on requests';
COMMENT ON TABLE request_history IS 'Audit trail for all request changes';

COMMENT ON COLUMN archive_requests.request_type IS 'Type: zahtev, finansije, terenska_aktivnost';
COMMENT ON COLUMN archive_requests.approval_chain IS 'JSON array: [{role, order, required}]';
COMMENT ON COLUMN archive_requests.request_data IS 'Type-specific data stored as JSON';

-- ============================================================================
-- END OF MIGRATION
-- ============================================================================
