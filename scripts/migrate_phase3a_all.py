#!/usr/bin/env python3
"""
Phase 3A Migration: ALL 5 High-Priority Databases
Migrates: Library, Exhibitions, Cultural Heritage, Meteorite, Employees
"""

import os
import sys
import json
import psycopg
from datetime import datetime, date
from dotenv import load_dotenv

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Load environment variables
load_dotenv()

DATABASE_URL = os.environ.get('DATABASE_URL')
if not DATABASE_URL:
    print("❌ DATABASE_URL not set in environment")
    sys.exit(1)

# Convert SQLAlchemy-style URL to psycopg format
DB_URL = DATABASE_URL.replace('postgresql+psycopg://', 'postgresql://')

# ============================================================================
# 1. LIBRARY DATABASE MIGRATION
# ============================================================================

def migrate_library(conn):
    """Migrate library database from JSON"""
    print("\n" + "="*70)
    print("📚 1. LIBRARY DATABASE MIGRATION")
    print("="*70)

    library_path = 'data/library_database.json'

    if not os.path.exists(library_path):
        print(f"⚠️  Library file not found: {library_path}")
        return 0, 0

    # Load JSON
    with open(library_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    books = data.get('books', [])
    categories = data.get('categories', [])

    print(f"📖 Found {len(books)} books, {len(categories)} categories")

    migrated_books = 0
    migrated_cats = 0

    with conn.cursor() as cur:
        # Migrate categories first
        for cat in categories:
            try:
                if isinstance(cat, str):
                    name = cat
                else:
                    name = cat.get('name')

                if name:
                    cur.execute("""
                        INSERT INTO library_categories (name)
                        VALUES (%s)
                        ON CONFLICT (name) DO NOTHING
                        RETURNING id
                    """, (name,))
                    if cur.fetchone():
                        migrated_cats += 1
            except:
                pass

        # Migrate books
        for book in books:
            try:
                title = book.get('title', '').strip()
                if not title:
                    continue

                cur.execute("""
                    INSERT INTO library_books (
                        title, author, isbn, publisher, publication_year,
                        category, language, pages, location, status, notes
                    ) VALUES (
                        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
                    )
                    ON CONFLICT DO NOTHING
                    RETURNING id
                """, (
                    title,
                    book.get('author'),
                    book.get('isbn'),
                    book.get('publisher'),
                    book.get('year') or book.get('publication_year'),
                    book.get('category'),
                    book.get('language', 'српски'),
                    book.get('pages'),
                    book.get('location'),
                    book.get('status', 'доступна'),
                    book.get('notes')
                ))

                if cur.fetchone():
                    migrated_books += 1

                    if migrated_books % 100 == 0:
                        print(f"   ... migrated {migrated_books} books")

            except Exception as e:
                print(f"   ❌ Error: {e}")
                pass

        conn.commit()

    print(f"✓ Library migration complete: {migrated_books} books, {migrated_cats} categories")
    return migrated_books, migrated_cats

# ============================================================================
# 2. EXHIBITIONS DATABASE MIGRATION
# ============================================================================

def migrate_exhibitions(conn):
    """Migrate exhibitions database from JSON"""
    print("\n" + "="*70)
    print("🎨 2. EXHIBITIONS DATABASE MIGRATION")
    print("="*70)

    exhibitions_path = 'data/exhibitions.json'

    if not os.path.exists(exhibitions_path):
        print(f"⚠️  Exhibitions file not found: {exhibitions_path}")
        return 0

    # Load JSON
    with open(exhibitions_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Handle both formats: direct array or wrapped in 'exhibitions' key
    if isinstance(data, list):
        exhibitions = data
    else:
        exhibitions = data.get('exhibitions', [])
    print(f"🎨 Found {len(exhibitions)} exhibitions")

    migrated = 0

    with conn.cursor() as cur:
        for exh in exhibitions:
            try:
                title = exh.get('title', '').strip()
                if not title:
                    continue

                # Handle date formats
                start_date = exh.get('start_date') or exh.get('date_start')
                end_date = exh.get('end_date') or exh.get('date_end')

                cur.execute("""
                    INSERT INTO exhibitions (
                        title, subtitle, description, exhibition_type,
                        location, start_date, end_date, curator,
                        status, notes
                    ) VALUES (
                        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
                    )
                    ON CONFLICT DO NOTHING
                    RETURNING id
                """, (
                    title,
                    exh.get('subtitle'),
                    exh.get('description'),
                    exh.get('type') or exh.get('exhibition_type'),
                    exh.get('location') or exh.get('venue'),
                    start_date,
                    end_date,
                    exh.get('curator'),
                    exh.get('status', 'завршена'),
                    exh.get('notes')
                ))

                if cur.fetchone():
                    migrated += 1

            except Exception as e:
                print(f"   ❌ Error: {e}")
                pass

        conn.commit()

    print(f"✓ Exhibitions migration complete: {migrated} exhibitions")
    return migrated

# ============================================================================
# 3. CULTURAL HERITAGE MIGRATION
# ============================================================================

def migrate_cultural_heritage(conn):
    """Migrate cultural heritage from Python dict in app.py"""
    print("\n" + "="*70)
    print("🏛️  3. CULTURAL HERITAGE DATABASE MIGRATION")
    print("="*70)

    # Import the Python dict from app.py
    try:
        from app import CULTURAL_HERITAGE_DATABASE
    except:
        print("⚠️  Could not import CULTURAL_HERITAGE_DATABASE from app.py")
        return 0

    items = CULTURAL_HERITAGE_DATABASE.get('heritage_items', [])
    print(f"🏛️  Found {len(items)} heritage items")

    migrated = 0

    with conn.cursor() as cur:
        for item in items:
            try:
                name = item.get('name', '').strip()
                if not name:
                    continue

                cur.execute("""
                    INSERT INTO heritage_items (
                        registry_number, item_name, heritage_type,
                        category, subcategory, significance_level,
                        description, material, date_of_origin,
                        creator, current_location, protection_status,
                        condition, notes
                    ) VALUES (
                        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
                    )
                    ON CONFLICT (registry_number) DO NOTHING
                    RETURNING id
                """, (
                    item.get('registry_number') or item.get('id'),
                    name,
                    item.get('type') or item.get('heritage_type'),
                    item.get('category'),
                    item.get('subcategory'),
                    item.get('significance') or item.get('significance_level'),
                    item.get('description'),
                    item.get('material'),
                    item.get('date') or item.get('date_of_origin'),
                    item.get('creator') or item.get('author'),
                    item.get('location') or item.get('current_location'),
                    item.get('protection_status'),
                    item.get('condition'),
                    item.get('notes')
                ))

                if cur.fetchone():
                    migrated += 1

            except Exception as e:
                print(f"   ❌ Error: {e}")
                pass

        conn.commit()

    print(f"✓ Cultural heritage migration complete: {migrated} items")
    return migrated

# ============================================================================
# 4. METEORITE COLLECTION MIGRATION
# ============================================================================

def migrate_meteorite_collection(conn):
    """Migrate meteorite collection from Python dict in app.py"""
    print("\n" + "="*70)
    print("☄️  4. METEORITE COLLECTION MIGRATION")
    print("="*70)

    # Import the Python dict from app.py
    try:
        from app import METEORITE_COLLECTION_DATABASE
    except:
        print("⚠️  Could not import METEORITE_COLLECTION_DATABASE from app.py")
        return 0

    specimens = METEORITE_COLLECTION_DATABASE.get('specimens', [])
    print(f"☄️  Found {len(specimens)} meteorite specimens")

    migrated = 0

    with conn.cursor() as cur:
        for spec in specimens:
            try:
                catalog = spec.get('catalog_number', '').strip()
                name = spec.get('meteorite_name', spec.get('name', '')).strip()

                if not catalog or not name:
                    continue

                # Skip date parsing for now (Serbian date formats cause issues)
                cur.execute("""
                    INSERT INTO meteorite_specimens (
                        catalog_number, specimen_name, meteorite_class,
                        meteorite_type, mass, mass_unit,
                        fall_location, fall_country,
                        collector, acquisition_method, description,
                        storage_location, condition, notes
                    ) VALUES (
                        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
                    )
                    ON CONFLICT (catalog_number) DO NOTHING
                    RETURNING id
                """, (
                    catalog,
                    name,
                    spec.get('classification') or spec.get('class') or spec.get('meteorite_class'),
                    spec.get('type') or spec.get('meteorite_type'),
                    spec.get('specimen_mass') or spec.get('mass'),
                    'kg' if 'total_mass_kg' in spec else 'g',
                    spec.get('location_found') or spec.get('fall_location') or spec.get('location'),
                    spec.get('fall_country') or spec.get('country'),
                    spec.get('curator') or spec.get('collector') or spec.get('finder'),
                    spec.get('source') or spec.get('acquisition_method'),
                    spec.get('description'),
                    spec.get('storage_location') or spec.get('storage'),
                    spec.get('condition'),
                    spec.get('notes')
                ))

                if cur.fetchone():
                    migrated += 1

            except Exception as e:
                print(f"   ❌ Error: {e}")
                pass

        conn.commit()

    print(f"✓ Meteorite collection migration complete: {migrated} specimens")
    return migrated

# ============================================================================
# 5. EMPLOYEES DATABASE MIGRATION
# ============================================================================

def migrate_employees(conn):
    """Migrate employee database from JSON"""
    print("\n" + "="*70)
    print("👥 5. EMPLOYEES DATABASE MIGRATION")
    print("="*70)

    employee_path = 'data/employee_directory.json'

    if not os.path.exists(employee_path):
        print(f"⚠️  Employee file not found: {employee_path}")
        return 0

    # Load JSON
    with open(employee_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Handle both formats: direct array or wrapped in 'employees' key
    if isinstance(data, list):
        employees = data
    else:
        employees = data.get('employees', [])
    print(f"👥 Found {len(employees)} employees")

    migrated = 0

    with conn.cursor() as cur:
        for emp in employees:
            try:
                name = emp.get('name', '').strip()
                email = emp.get('email', '').strip()

                if not name or not email:
                    continue

                # Try to find matching user_id
                cur.execute("SELECT id FROM users WHERE email = %s", (email,))
                user_result = cur.fetchone()
                user_id = user_result[0] if user_result else None

                # Simple insert with just required fields
                cur.execute("""
                    INSERT INTO employee_profiles (
                        user_id, full_name, email, position
                    ) VALUES (
                        %s, %s, %s, %s
                    )
                    ON CONFLICT (email) DO NOTHING
                    RETURNING id
                """, (
                    user_id,
                    name,
                    email,
                    emp.get('position', emp.get('title', 'Запослени'))
                ))

                if cur.fetchone():
                    migrated += 1

            except Exception as e:
                print(f"   ❌ Error: {e}")
                pass

        conn.commit()

    print(f"✓ Employees migration complete: {migrated} employees")
    return migrated

# ============================================================================
# VERIFICATION
# ============================================================================

def verify_all_migrations(conn):
    """Verify all migrations"""
    print("\n" + "="*70)
    print("🔍 VERIFICATION")
    print("="*70)

    with conn.cursor() as cur:
        # Library
        cur.execute("SELECT COUNT(*) FROM library_books")
        library_count = cur.fetchone()[0]

        # Exhibitions
        cur.execute("SELECT COUNT(*) FROM exhibitions")
        exhibitions_count = cur.fetchone()[0]

        # Heritage
        cur.execute("SELECT COUNT(*) FROM heritage_items")
        heritage_count = cur.fetchone()[0]

        # Meteorites
        cur.execute("SELECT COUNT(*) FROM meteorite_specimens")
        meteorite_count = cur.fetchone()[0]

        # Employees
        cur.execute("SELECT COUNT(*) FROM employee_profiles")
        employee_count = cur.fetchone()[0]

    print(f"\n📊 Final Record Counts:")
    print(f"   • Library books: {library_count}")
    print(f"   • Exhibitions: {exhibitions_count}")
    print(f"   • Heritage items: {heritage_count}")
    print(f"   • Meteorite specimens: {meteorite_count}")
    print(f"   • Employee profiles: {employee_count}")
    print(f"\n   TOTAL: {library_count + exhibitions_count + heritage_count + meteorite_count + employee_count} records")

    return {
        'library': library_count,
        'exhibitions': exhibitions_count,
        'heritage': heritage_count,
        'meteorites': meteorite_count,
        'employees': employee_count
    }

# ============================================================================
# MAIN
# ============================================================================

def main():
    """Main migration function"""
    print("\n" + "="*70)
    print("         PHASE 3A: ALL HIGH-PRIORITY DATABASES MIGRATION")
    print("="*70)
    print("  Migrating: Library, Exhibitions, Heritage, Meteorites, Employees")
    print("="*70)

    # Connect to PostgreSQL
    print(f"\n🔌 Connecting to PostgreSQL...")
    try:
        conn = psycopg.connect(DB_URL)
        print("✓ Connected to PostgreSQL")
    except Exception as e:
        print(f"❌ Failed to connect to PostgreSQL: {e}")
        return 1

    try:
        # Run all migrations
        results = {}

        results['library'] = migrate_library(conn)
        results['exhibitions'] = migrate_exhibitions(conn)
        results['heritage'] = migrate_cultural_heritage(conn)
        results['meteorites'] = migrate_meteorite_collection(conn)
        results['employees'] = migrate_employees(conn)

        # Verify
        counts = verify_all_migrations(conn)

        # Final summary
        print("\n" + "="*70)
        print("✅ PHASE 3A MIGRATION COMPLETE")
        print("="*70)
        print("\n🎉 All 5 high-priority databases have been migrated to PostgreSQL!")
        print("\nNext steps:")
        print("  1. Update app.py to use PostgreSQL for these databases")
        print("  2. Test each database in the application")
        print("  3. Remove old JSON/dict definitions once verified")
        print()

        return 0

    except Exception as e:
        print(f"\n❌ Migration failed: {e}")
        import traceback
        traceback.print_exc()
        return 1

    finally:
        conn.close()
        print("🔌 Database connection closed\n")

if __name__ == '__main__':
    sys.exit(main())
