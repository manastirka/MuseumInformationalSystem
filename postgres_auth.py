#!/usr/bin/env python3
"""
PostgreSQL Authentication Module
Replaces fallback authentication with PostgreSQL-backed auth
"""
import os
import logging
from typing import Optional, Dict, Any
from datetime import datetime

try:
    import psycopg
    from psycopg.rows import dict_row
except ImportError:
    psycopg = None

from security_utils import PasswordHasher

logger = logging.getLogger(__name__)


class PostgresAuthSystem:
    """PostgreSQL-based authentication system"""

    def __init__(self, database_url: Optional[str] = None):
        self.database_url = database_url or os.environ.get('DATABASE_URL')
        self.available = False
        self.password_hasher = PasswordHasher()

        if not self.database_url:
            logger.warning("PostgresAuth: DATABASE_URL not set")
            return

        if not psycopg:
            logger.error("PostgresAuth: psycopg module not available")
            return

        # Test connection
        try:
            pg_url = self.database_url.replace('postgresql+psycopg://', 'postgresql://')
            with psycopg.connect(pg_url) as conn:
                with conn.cursor() as cur:
                    cur.execute("SELECT COUNT(*) FROM users")
                    user_count = cur.fetchone()[0]
                    logger.info(f"PostgresAuth: Connected successfully ({user_count} users)")
                    self.available = True
        except Exception as e:
            logger.error(f"PostgresAuth: Connection failed: {e}")
            self.available = False

    def verify_credentials(self, email: str, password: str) -> Optional[Dict[str, Any]]:
        """
        Verify user credentials against PostgreSQL database

        Returns:
            User dict if valid, None otherwise
        """
        if not self.available:
            return None

        try:
            pg_url = self.database_url.replace('postgresql+psycopg://', 'postgresql://')

            with psycopg.connect(pg_url, row_factory=dict_row) as conn:
                with conn.cursor() as cur:
                    # Get user with role info
                    cur.execute("""
                        SELECT
                            u.id,
                            u.email,
                            u.password_hash,
                            u.salt,
                            u.full_name,
                            u.position,
                            u.is_active,
                            u.is_first_login,
                            u.theme_mode,
                            u.theme_accent,
                            u.theme_style,
                            u.theme_density,
                            u.theme_palette,
                            u.active_custom_theme_id,
                            u.auth_version,
                            r.name as role,
                            COALESCE(d.name, ep.department) as department
                        FROM users u
                        LEFT JOIN roles r ON u.role_id = r.id
                        LEFT JOIN departments d ON u.department_id = d.id
                        LEFT JOIN employee_profiles ep ON LOWER(ep.email) = LOWER(u.email)
                        WHERE LOWER(u.email) = LOWER(%s)
                          AND u.is_active = TRUE
                    """, (email,))

                    user = cur.fetchone()

                    if not user:
                        logger.warning(f"PostgresAuth: User not found or inactive: {email}")
                        return None

                    # Verify password
                    if not self.password_hasher.verify_password(
                        password,
                        user['password_hash'],
                        user['salt']
                    ):
                        logger.warning(f"PostgresAuth: Invalid password for {email}")
                        return None

                    # Check if password needs rehashing (upgrade from SHA-512 to bcrypt)
                    if self.password_hasher.needs_rehash(user['password_hash']):
                        try:
                            new_hash, new_salt = self.password_hasher.hash_password(password)
                            cur.execute("""
                                UPDATE users
                                SET password_hash = %s, salt = %s, updated_at = %s
                                WHERE id = %s
                            """, (new_hash, new_salt, datetime.now(), user['id']))
                            logger.info(f"PostgresAuth: Password rehashed for {email} (upgraded to bcrypt)")
                        except Exception as rehash_error:
                            logger.warning(f"PostgresAuth: Failed to rehash password: {rehash_error}")

                    # Update last login
                    cur.execute("""
                        UPDATE users
                        SET last_login_at = %s
                        WHERE id = %s
                    """, (datetime.now(), user['id']))
                    conn.commit()

                    # Return user info (without sensitive data)
                    return {
                        'id': user['id'],
                        'email': user['email'],
                        'full_name': user['full_name'],
                        'role': user['role'] or 'employee',
                        'department': user['department'],
                        'position': user['position'],
                        'is_first_login': user['is_first_login'],
                        'theme_mode': user['theme_mode'],
                        'theme_accent': user['theme_accent'],
                        'theme_style': user['theme_style'],
                        'theme_density': user['theme_density'],
                        'theme_palette': user['theme_palette'],
                        'active_custom_theme_id': user.get('active_custom_theme_id'),
                        'auth_version': user.get('auth_version') or 1,
                    }

        except Exception as e:
            logger.error(f"PostgresAuth: Error verifying credentials: {e}")
            return None

    def get_user_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        """Get user information by email"""
        if not self.available:
            return None

        try:
            pg_url = self.database_url.replace('postgresql+psycopg://', 'postgresql://')

            with psycopg.connect(pg_url, row_factory=dict_row) as conn:
                with conn.cursor() as cur:
                    cur.execute("""
                        SELECT
                            u.id,
                            u.email,
                            u.full_name,
                            u.position,
                            u.is_active,
                            r.name as role,
                            d.name as department
                        FROM users u
                        LEFT JOIN roles r ON u.role_id = r.id
                        LEFT JOIN departments d ON u.department_id = d.id
                        WHERE LOWER(u.email) = LOWER(%s)
                    """, (email,))

                    user = cur.fetchone()
                    return dict(user) if user else None

        except Exception as e:
            logger.error(f"PostgresAuth: Error getting user: {e}")
            return None

    def create_user(self, email: str, password: str, full_name: str,
                   role: str = 'employee', position: str = None) -> Optional[int]:
        """Create a new user"""
        if not self.available:
            return None

        try:
            # Hash password
            password_hash, salt = self.password_hasher.hash_password(password)

            pg_url = self.database_url.replace('postgresql+psycopg://', 'postgresql://')

            with psycopg.connect(pg_url, row_factory=dict_row) as conn:
                with conn.cursor() as cur:
                    cur.execute("""
                        INSERT INTO users (
                            email, password_hash, salt, full_name,
                            role_id, position, is_active, is_first_login, created_at, updated_at
                        )
                        VALUES (
                            %s, %s, %s, %s,
                            (SELECT id FROM roles WHERE name = %s),
                            %s, TRUE, TRUE, %s, %s
                        )
                        RETURNING id
                    """, (
                        email, password_hash, salt, full_name,
                        role, position,
                        datetime.now(), datetime.now()
                    ))

                    user_id = cur.fetchone()['id']
                    conn.commit()

                    logger.info(f"PostgresAuth: Created user {email} (ID: {user_id})")
                    return user_id

        except Exception as e:
            logger.error(f"PostgresAuth: Error creating user: {e}")
            return None

    def update_password(self, email: str, new_password: str) -> bool:
        """Update user password"""
        if not self.available:
            return False

        try:
            # Hash new password
            password_hash, salt = self.password_hasher.hash_password(new_password)

            pg_url = self.database_url.replace('postgresql+psycopg://', 'postgresql://')

            with psycopg.connect(pg_url) as conn:
                with conn.cursor() as cur:
                    cur.execute("""
                        UPDATE users
                        SET password_hash = %s,
                            salt = %s,
                            is_first_login = FALSE,
                            auth_version = auth_version + 1,
                            updated_at = %s
                        WHERE LOWER(email) = LOWER(%s)
                    """, (password_hash, salt, datetime.now(), email))

                    conn.commit()
                    logger.info(f"PostgresAuth: Updated password for {email}")
                    return True

        except Exception as e:
            logger.error(f"PostgresAuth: Error updating password: {e}")
            return False

    def save_theme_preferences(self, email: str, theme_mode: str, theme_accent: str,
                               theme_style: str = 'institucionalna',
                               theme_density: str = 'komforno',
                               theme_palette: str = 'plava-klasicna',
                               active_custom_theme_id=None) -> bool:
        """Persist the user's UI theme preference (mode + accent + style + density
        + palette). active_custom_theme_id is written only when the palette is
        'custom' (else NULL) so switching away clears the pointer."""
        if not self.available:
            return False

        try:
            pg_url = self.database_url.replace('postgresql+psycopg://', 'postgresql://')

            with psycopg.connect(pg_url) as conn:
                with conn.cursor() as cur:
                    cur.execute("""
                        UPDATE users
                        SET theme_mode = %s,
                            theme_accent = %s,
                            theme_style = %s,
                            theme_density = %s,
                            theme_palette = %s,
                            active_custom_theme_id = %s,
                            updated_at = %s
                        WHERE LOWER(email) = LOWER(%s)
                    """, (theme_mode, theme_accent, theme_style, theme_density,
                          theme_palette,
                          active_custom_theme_id if theme_palette == 'custom' else None,
                          datetime.now(), email))

                    conn.commit()
                    return True

        except Exception as e:
            logger.error(f"PostgresAuth: Error saving theme preferences: {e}")
            return False

    # ---- Custom themes (phase 3) ----------------------------------------- #
    # Private per-user themes stored as validated JSONB. All reads/writes are
    # scoped by user_email so one user can never touch another's themes.

    def list_custom_themes(self, email: str) -> list:
        """Return the user's saved custom themes (id, name, definition, timestamps),
        newest first."""
        if not self.available:
            return []
        try:
            pg_url = self.database_url.replace('postgresql+psycopg://', 'postgresql://')
            with psycopg.connect(pg_url, row_factory=dict_row) as conn:
                with conn.cursor() as cur:
                    cur.execute("""
                        SELECT id, name, definition, created_at, updated_at
                        FROM user_custom_themes
                        WHERE LOWER(user_email) = LOWER(%s)
                        ORDER BY updated_at DESC, id DESC
                    """, (email,))
                    return list(cur.fetchall())
        except Exception as e:
            logger.error(f"PostgresAuth: Error listing custom themes: {e}")
            return []

    def get_custom_theme(self, email: str, theme_id: int):
        """Return one custom theme owned by the user, or None."""
        if not self.available:
            return None
        try:
            pg_url = self.database_url.replace('postgresql+psycopg://', 'postgresql://')
            with psycopg.connect(pg_url, row_factory=dict_row) as conn:
                with conn.cursor() as cur:
                    cur.execute("""
                        SELECT id, name, definition, created_at, updated_at
                        FROM user_custom_themes
                        WHERE id = %s AND LOWER(user_email) = LOWER(%s)
                    """, (theme_id, email))
                    return cur.fetchone()
        except Exception as e:
            logger.error(f"PostgresAuth: Error getting custom theme: {e}")
            return None

    def create_custom_theme(self, email: str, name: str, definition: dict):
        """Insert a new custom theme; return its new id or None on failure."""
        if not self.available:
            return None
        try:
            import json
            pg_url = self.database_url.replace('postgresql+psycopg://', 'postgresql://')
            with psycopg.connect(pg_url) as conn:
                with conn.cursor() as cur:
                    cur.execute("""
                        INSERT INTO user_custom_themes (user_email, name, definition)
                        VALUES (%s, %s, %s)
                        RETURNING id
                    """, (email, name, json.dumps(definition)))
                    new_id = cur.fetchone()[0]
                    conn.commit()
                    return new_id
        except Exception as e:
            logger.error(f"PostgresAuth: Error creating custom theme: {e}")
            return None

    def update_custom_theme(self, email: str, theme_id: int, name: str,
                            definition: dict) -> bool:
        """Update name+definition of a theme the user owns."""
        if not self.available:
            return False
        try:
            import json
            pg_url = self.database_url.replace('postgresql+psycopg://', 'postgresql://')
            with psycopg.connect(pg_url) as conn:
                with conn.cursor() as cur:
                    cur.execute("""
                        UPDATE user_custom_themes
                        SET name = %s, definition = %s, updated_at = now()
                        WHERE id = %s AND LOWER(user_email) = LOWER(%s)
                    """, (name, json.dumps(definition), theme_id, email))
                    changed = cur.rowcount
                    conn.commit()
                    return changed > 0
        except Exception as e:
            logger.error(f"PostgresAuth: Error updating custom theme: {e}")
            return False

    def rename_custom_theme(self, email: str, theme_id: int, name: str) -> bool:
        """Rename a theme the user owns (definition untouched)."""
        if not self.available:
            return False
        try:
            pg_url = self.database_url.replace('postgresql+psycopg://', 'postgresql://')
            with psycopg.connect(pg_url) as conn:
                with conn.cursor() as cur:
                    cur.execute("""
                        UPDATE user_custom_themes
                        SET name = %s, updated_at = now()
                        WHERE id = %s AND LOWER(user_email) = LOWER(%s)
                    """, (name, theme_id, email))
                    changed = cur.rowcount
                    conn.commit()
                    return changed > 0
        except Exception as e:
            logger.error(f"PostgresAuth: Error renaming custom theme: {e}")
            return False

    def delete_custom_theme(self, email: str, theme_id: int) -> bool:
        """Delete a theme the user owns and clear it from active pointer if set."""
        if not self.available:
            return False
        try:
            pg_url = self.database_url.replace('postgresql+psycopg://', 'postgresql://')
            with psycopg.connect(pg_url) as conn:
                with conn.cursor() as cur:
                    cur.execute("""
                        DELETE FROM user_custom_themes
                        WHERE id = %s AND LOWER(user_email) = LOWER(%s)
                    """, (theme_id, email))
                    changed = cur.rowcount
                    # If this theme was the applied one, drop back to the default
                    # palette so the user never renders a deleted theme.
                    cur.execute("""
                        UPDATE users
                        SET active_custom_theme_id = NULL,
                            theme_palette = 'plava-klasicna'
                        WHERE LOWER(email) = LOWER(%s)
                          AND active_custom_theme_id = %s
                    """, (email, theme_id))
                    conn.commit()
                    return changed > 0
        except Exception as e:
            logger.error(f"PostgresAuth: Error deleting custom theme: {e}")
            return False

    def set_active_custom_theme(self, email: str, theme_id) -> bool:
        """Point the user at a custom theme and switch palette to 'custom'. Pass
        theme_id=None to keep palette handling to save_theme_preferences."""
        if not self.available:
            return False
        try:
            pg_url = self.database_url.replace('postgresql+psycopg://', 'postgresql://')
            with psycopg.connect(pg_url) as conn:
                with conn.cursor() as cur:
                    cur.execute("""
                        UPDATE users
                        SET theme_palette = 'custom',
                            active_custom_theme_id = %s,
                            updated_at = %s
                        WHERE LOWER(email) = LOWER(%s)
                    """, (theme_id, datetime.now(), email))
                    conn.commit()
                    return True
        except Exception as e:
            logger.error(f"PostgresAuth: Error setting active custom theme: {e}")
            return False

    def list_users(self) -> list:
        """List all users (for admin)"""
        if not self.available:
            return []

        try:
            pg_url = self.database_url.replace('postgresql+psycopg://', 'postgresql://')

            with psycopg.connect(pg_url, row_factory=dict_row) as conn:
                with conn.cursor() as cur:
                    cur.execute("""
                        SELECT
                            u.id,
                            u.email,
                            u.full_name,
                            u.position,
                            u.is_active,
                            r.name as role,
                            d.name as department,
                            u.created_at,
                            u.last_login_at
                        FROM users u
                        LEFT JOIN roles r ON u.role_id = r.id
                        LEFT JOIN departments d ON u.department_id = d.id
                        ORDER BY u.email
                    """)

                    return [dict(row) for row in cur.fetchall()]

        except Exception as e:
            logger.error(f"PostgresAuth: Error listing users: {e}")
            return []


# Singleton instance
_postgres_auth = None


def get_postgres_auth() -> PostgresAuthSystem:
    """Get or create PostgreSQL auth system instance"""
    global _postgres_auth

    if _postgres_auth is None:
        _postgres_auth = PostgresAuthSystem()

    return _postgres_auth
