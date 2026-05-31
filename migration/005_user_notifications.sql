-- Migration 005: User notifications system
-- Creates a table for storing user notifications (obavestenja)

CREATE TABLE IF NOT EXISTS user_notifications (
    id SERIAL PRIMARY KEY,
    user_email VARCHAR(255) NOT NULL,
    title TEXT NOT NULL,
    message TEXT NOT NULL,
    icon VARCHAR(50) DEFAULT 'bi-bell',
    type VARCHAR(20) DEFAULT 'info',
    is_read BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_notifications_user_email ON user_notifications(user_email);
CREATE INDEX IF NOT EXISTS idx_notifications_unread ON user_notifications(user_email, is_read) WHERE is_read = FALSE;
