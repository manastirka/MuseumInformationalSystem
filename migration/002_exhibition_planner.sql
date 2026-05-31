-- ============================================================================
-- Migration 002: Exhibition Planner Enhancements
-- ============================================================================
-- Date: January 2026
-- Adds progress tracking and planning-specific fields to exhibitions table
-- ============================================================================

-- Add progress column for tracking completion percentage
ALTER TABLE exhibitions ADD COLUMN IF NOT EXISTS progress INTEGER DEFAULT 0;

-- Add planning phase column
ALTER TABLE exhibitions ADD COLUMN IF NOT EXISTS planning_phase VARCHAR(50) DEFAULT 'conceptual';

-- Add checklist data as JSONB for flexible storage
ALTER TABLE exhibitions ADD COLUMN IF NOT EXISTS checklist_data JSONB DEFAULT '{}';

-- Add responsible team members
ALTER TABLE exhibitions ADD COLUMN IF NOT EXISTS team_members JSONB DEFAULT '[]';

-- Update status values comment
COMMENT ON COLUMN exhibitions.status IS 'Status: planning, preparation, active, completed, cancelled';
COMMENT ON COLUMN exhibitions.progress IS 'Completion progress percentage (0-100)';
COMMENT ON COLUMN exhibitions.planning_phase IS 'Current planning phase: conceptual, design, technical, digital, team';
COMMENT ON COLUMN exhibitions.checklist_data IS 'JSON object storing checklist completion state';
COMMENT ON COLUMN exhibitions.team_members IS 'JSON array of team member assignments';

-- ============================================================================
-- END OF MIGRATION
-- ============================================================================
