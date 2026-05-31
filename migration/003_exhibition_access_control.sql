-- ============================================================================
-- Migration 003: Exhibition Access Control
-- ============================================================================
-- Date: January 2026
-- Adds created_by tracking and direktor role for exhibition access control
-- ============================================================================

-- Add direktor role if it doesn't exist
INSERT INTO roles (name, description)
VALUES ('direktor', 'Director with full access to all exhibitions')
ON CONFLICT (name) DO NOTHING;

-- Add created_by column to exhibitions table
ALTER TABLE exhibitions ADD COLUMN IF NOT EXISTS created_by_email VARCHAR(255);
ALTER TABLE exhibitions ADD COLUMN IF NOT EXISTS created_by_name VARCHAR(255);

-- Add index for faster filtering by creator
CREATE INDEX IF NOT EXISTS idx_exhibitions_created_by ON exhibitions(created_by_email);

-- Comment on new columns
COMMENT ON COLUMN exhibitions.created_by_email IS 'Email of user who created the exhibition';
COMMENT ON COLUMN exhibitions.created_by_name IS 'Full name of user who created the exhibition';

-- ============================================================================
-- END OF MIGRATION
-- ============================================================================
