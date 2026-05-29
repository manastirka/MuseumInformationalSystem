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
                        'is_first_login': user['is_first_login']
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
                            updated_at = %s
                        WHERE LOWER(email) = LOWER(%s)
                    """, (password_hash, salt, datetime.now(), email))

                    conn.commit()
                    logger.info(f"PostgresAuth: Updated password for {email}")
                    return True

        except Exception as e:
            logger.error(f"PostgresAuth: Error updating password: {e}")
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
