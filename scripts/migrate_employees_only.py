#!/usr/bin/env python3
"""
Migrate Employee Directory to PostgreSQL
Standalone script to migrate employee data from JSON to PostgreSQL
"""

import os
import sys
import json
import psycopg
from datetime import datetime

# Database connection
DATABASE_URL = os.environ.get('DATABASE_URL', 'postgresql://aleksandarlukovic@localhost:5432/museum_system')

def migrate_employees():
    """Migrate employee directory from JSON to PostgreSQL"""

    print("👥 EMPLOYEE DIRECTORY MIGRATION")
    print("="*70)

    # Load employee data from JSON
    employee_path = 'data/employee_directory.json'

    if not os.path.exists(employee_path):
        print(f"❌ Employee file not found: {employee_path}")
        return 0

    with open(employee_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Handle both formats
    if isinstance(data, list):
        employees = data
    else:
        employees = data.get('employees', [])

    print(f"📂 Found {len(employees)} employees in JSON file\n")

    # Connect to PostgreSQL
    conn = psycopg.connect(DATABASE_URL.replace('postgresql+psycopg://', 'postgresql://'))
    cur = conn.cursor()

    # Check current count
    cur.execute("SELECT COUNT(*) FROM employee_profiles")
    existing_count = cur.fetchone()[0]
    print(f"📊 Current employee profiles in database: {existing_count}")

    # Ask if we should delete existing
    if existing_count > 0:
        print(f"🗑️  Deleting {existing_count} existing employee profiles...")
        cur.execute("DELETE FROM employee_profiles")
        conn.commit()

    # Get existing user IDs
    cur.execute("SELECT id FROM users")
    existing_user_ids = {row[0] for row in cur.fetchall()}
    print(f"📊 Found {len(existing_user_ids)} existing users in database")

    # Migrate employees
    migrated = 0
    errors = 0

    print(f"\n⏳ Migrating {len(employees)} employees...")

    for emp in employees:
        try:
            # Use email or user_id as unique identifier
            employee_id = f"EMP-{emp.get('user_id', '0'):03d}"

            # Only set user_id if it exists in users table, otherwise NULL
            user_id = emp.get('user_id') if emp.get('user_id') in existing_user_ids else None

            cur.execute("""
                INSERT INTO employee_profiles (
                    user_id, employee_id, full_name, email, phone,
                    position, department, employment_status,
                    hire_date, biography, biography_short,
                    created_at, updated_at
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (employee_id) DO UPDATE SET
                    full_name = EXCLUDED.full_name,
                    email = EXCLUDED.email,
                    position = EXCLUDED.position,
                    department = EXCLUDED.department,
                    updated_at = EXCLUDED.updated_at
            """, (
                user_id,
                employee_id,
                emp.get('full_name'),
                emp.get('email'),
                emp.get('phone', ''),
                emp.get('position', ''),
                emp.get('department', ''),
                'активан',  # All current employees are active
                None,  # hire_date not in JSON
                emp.get('description', ''),  # biography
                emp.get('description', '')[:200] if emp.get('description') else '',  # short bio
                datetime.now(),
                datetime.now()
            ))
            migrated += 1

            if migrated % 10 == 0:
                print(f"   ✓ Migrated {migrated} employees...")

        except Exception as e:
            errors += 1
            print(f"   ❌ Error migrating {emp.get('full_name', 'Unknown')}: {e}")

    conn.commit()

    # Verify
    cur.execute("SELECT COUNT(*) FROM employee_profiles")
    final_count = cur.fetchone()[0]

    print(f"\n{'='*70}")
    print(f"✅ Migration Complete!")
    print(f"   • Employees migrated: {migrated}")
    print(f"   • Errors: {errors}")
    print(f"   • Final count in database: {final_count}")
    print(f"{'='*70}\n")

    # Show sample
    cur.execute("SELECT full_name, department, position FROM employee_profiles LIMIT 5")
    samples = cur.fetchall()
    print("Sample employees:")
    for name, dept, pos in samples:
        print(f"   • {name} - {pos} ({dept})")

    cur.close()
    conn.close()

    return migrated

if __name__ == '__main__':
    try:
        count = migrate_employees()
        sys.exit(0 if count > 0 else 1)
    except Exception as e:
        print(f"\n❌ Migration failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
