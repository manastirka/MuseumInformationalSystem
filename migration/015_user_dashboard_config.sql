-- ============================================================================
-- Migration 015: Per-user dashboard element configuration
-- ============================================================================
-- Date: July 2026
-- Stores each user's selected dashboard elements (fixed sections and module
-- cards). Replaces the shared JSON blob in app_shared_settings for new saves;
-- the blob remains only as a read-only legacy fallback.
-- ============================================================================

CREATE TABLE IF NOT EXISTS user_dashboard_config (
    user_email VARCHAR(255) PRIMARY KEY,
    enabled_elements JSONB NOT NULL DEFAULT '[]'::jsonb,
    updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);

COMMENT ON TABLE user_dashboard_config IS
    'Per-user selection of dashboard elements (sections + module cards)';
