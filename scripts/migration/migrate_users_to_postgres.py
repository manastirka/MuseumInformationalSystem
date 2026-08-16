#!/usr/bin/env python3
"""
Migrate users from SQLite to PostgreSQL
Part of Phase 2 database migration
"""
import os
import sqlite3
import sys
from datetime import datetime
from dotenv import load_dotenv

try:
    import psycopg
    from psycopg.rows import dict_row
except ImportError:
    print("❌ Error: psycopg module not found")
    print("   Install with: pip install psycopg[binary]")
    sys.exit(1)

load_dotenv()

# Configuration
SQLITE_PATH = 'localSQLtesting/museum_timesheet.db'
DATABASE_URL = os.environ.get('DATABASE_URL')

if not DATABASE_URL:
    print("❌ Error: DATABASE_URL not set in .env file")
    sys.exit(1)

# Convert URL format
pg_url = DATABASE_URL.replace('postgresql+psycopg://', 'postgresql://')

print("=" * 80)
print("USER MIGRATION: SQLite → PostgreSQL")
print("=" * 80)
print()

# Check if SQLite database exists
if not os.path.exists(SQLITE_PATH):
    print(f"❌ Error: SQLite database not found at {SQLITE_PATH}")
    sys.exit(1)

print(f"✓ Source: {SQLITE_PATH}")
print(f"✓ Target: {pg_url.split('@')[1] if '@' in pg_url else 'PostgreSQL'}")
print()

# Load users from SQLite
print("Step 1: Loading users from SQLite...")
sqlite_conn = sqlite3.connect(SQLITE_PATH)
sqlite_conn.row_factory = sqlite3.Row
cursor = sqlite_conn.cursor()

try:
    users = cursor.execute("""
        SELECT
            user_id,
            email,
            password_hash as password,
            salt,
            full_name,
            department,
            position,
            role,
            is_active,
            created_at,
            last_login
        FROM users
        ORDER BY user_id
    """).fetchall()

    print(f"   Found {len(users)} users in SQLite:")
    for user in users:
        print(f"   - {user['email']} ({user['role']})")
    print()

except sqlite3.OperationalError as e:
    print(f"❌ Error reading SQLite database: {e}")
    sqlite_conn.close()
    sys.exit(1)

sqlite_conn.close()

if len(users) == 0:
    print("⚠️  No users found to migrate")
    sys.exit(0)

# Connect to PostgreSQL
print("Step 2: Connecting to PostgreSQL...")
try:
    pg_conn = psycopg.connect(pg_url, row_factory=dict_row)
    print("   ✓ Connected to PostgreSQL")
    print()
except Exception as e:
    print(f"❌ Error connecting to PostgreSQL: {e}")
    sys.exit(1)

# Ensure roles exist
print("Step 3: Ensuring roles exist...")
with pg_conn.cursor() as cur:
    # Insert default roles
    roles = [
        ('admin', 'Administrator with full access'),
        ('employee', 'Regular employee'),
        ('curator', 'Curator with collection management access'),
        ('viewer', 'Read-only access')
    ]

    for role_name, description in roles:
        cur.execute("""
            INSERT INTO roles (name, description)
            VALUES (%s, %s)
            ON CONFLICT (name) DO NOTHING
        """, (role_name, description))

    pg_conn.commit()
    print("   ✓ Roles verified")
    print()

# Check for existing users
print("Step 4: Checking for existing users in PostgreSQL...")
with pg_conn.cursor() as cur:
    cur.execute("SELECT email FROM users")
    existing_emails = {row['email'] for row in cur.fetchall()}

    if existing_emails:
        print(f"   Found {len(existing_emails)} existing users:")
        for email in existing_emails:
            print(f"   - {email}")
        print()
    else:
        print("   No existing users found")
        print()

# Migrate users
print("Step 5: Migrating users to PostgreSQL...")
migrated = 0
skipped = 0
errors = 0

with pg_conn.cursor() as cur:
    for user in users:
        email = user['email']

        if email in existing_emails:
            print(f"   ⚠️  Skipping {email} (already exists)")
            skipped += 1
            continue

        try:
            # Map SQLite role to PostgreSQL role
            role = user['role'] if user['role'] in ['admin', 'employee', 'curator', 'viewer'] else 'employee'

            # Parse created_at
            created_at = user['created_at']
            if created_at and created_at != '':
                try:
                    created_dt = datetime.fromisoformat(created_at.replace(' ', 'T'))
                except:
                    created_dt = datetime.now()
            else:
                created_dt = datetime.now()

            # Insert user
            cur.execute("""
                INSERT INTO users (
                    email,
                    password_hash,
                    salt,
                    full_name,
                    role_id,
                    department_id,
                    position,
                    is_active,
                    created_at,
                    updated_at
                )
                VALUES (
                    %s,
                    %s,
                    %s,
                    %s,
                    (SELECT id FROM roles WHERE name = %s),
                    NULL,
                    %s,
                    %s,
                    %s,
                    %s
                )
                RETURNING id
            """, (
                email,
                user['password'],  # Already hashed
                user['salt'],
                user['full_name'] or email.split('@')[0],
                role,
                user['position'],
                bool(user['is_active']),
                created_dt,
                created_dt
            ))

            user_id = cur.fetchone()['id']
            print(f"   ✓ Migrated {email} (ID: {user_id}, role: {role})")
            migrated += 1

        except Exception as e:
            print(f"   ❌ Error migrating {email}: {e}")
            errors += 1
            continue

    # Commit all changes
    pg_conn.commit()

pg_conn.close()

# Summary
print()
print("=" * 80)
print("MIGRATION SUMMARY")
print("=" * 80)
print(f"Total users in SQLite: {len(users)}")
print(f"✓ Successfully migrated: {migrated}")
print(f"⚠️  Skipped (already exist): {skipped}")
print(f"❌ Errors: {errors}")
print()

if migrated > 0:
    print("✅ User migration complete!")
    print()
    print("Next steps:")
    print("1. Verify users in PostgreSQL:")
    print("   psql $DATABASE_URL -c 'SELECT email, full_name, r.name as role FROM users u JOIN roles r ON u.role_id = r.id;'")
    print()
    print("2. Test login functionality")
    print("3. Update application to use PostgreSQL authentication")
else:
    print("⚠️  No new users were migrated")
    if skipped > 0:
        print("   All users already exist in PostgreSQL")

print()
