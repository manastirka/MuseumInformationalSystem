#!/usr/bin/env python3
"""
Phase 3A Migration: Library Database
Migrates library_database.json to PostgreSQL
"""

import os
import sys
import json
import psycopg
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

DATABASE_URL = os.environ.get('DATABASE_URL')
if not DATABASE_URL:
    print("❌ DATABASE_URL not set in environment")
    sys.exit(1)

# Convert SQLAlchemy-style URL to psycopg format
DB_URL = DATABASE_URL.replace('postgresql+psycopg://', 'postgresql://')

LIBRARY_JSON_PATH = 'data/library_database.json'

def load_library_json():
    """Load library database from JSON file"""
    print(f"📖 Loading library data from {LIBRARY_JSON_PATH}...")

    if not os.path.exists(LIBRARY_JSON_PATH):
        print(f"❌ Library database file not found: {LIBRARY_JSON_PATH}")
        return None

    with open(LIBRARY_JSON_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)

    print(f"✓ Loaded {len(data.get('books', []))} books from JSON")
    return data

def migrate_library_books(conn, library_data):
    """Migrate library books to PostgreSQL"""
    books = library_data.get('books', [])

    if not books:
        print("⚠️  No books to migrate")
        return 0

    print(f"\n📚 Migrating {len(books)} books...")

    migrated = 0
    skipped = 0
    errors = 0

    with conn.cursor() as cur:
        for book in books:
            try:
                # Extract book data with defaults
                title = book.get('title', '').strip()
                if not title:
                    print(f"   ⚠️  Skipping book with no title")
                    skipped += 1
                    continue

                # Prepare book data
                book_data = {
                    'title': title,
                    'author': book.get('author', '').strip() or None,
                    'isbn': book.get('isbn', '').strip() or None,
                    'publisher': book.get('publisher', '').strip() or None,
                    'publication_year': book.get('publication_year') or book.get('year') or None,
                    'category': book.get('category', '').strip() or None,
                    'subcategory': book.get('subcategory', '').strip() or None,
                    'language': book.get('language', 'српски').strip(),
                    'pages': book.get('pages') or book.get('page_count') or None,
                    'format': book.get('format', '').strip() or None,
                    'location': book.get('location', '').strip() or None,
                    'shelf_number': book.get('shelf_number', '').strip() or book.get('shelf', '').strip() or None,
                    'status': book.get('status', 'доступна').strip(),
                    'acquisition_date': book.get('acquisition_date') or None,
                    'acquisition_method': book.get('acquisition_method', '').strip() or book.get('source', '').strip() or None,
                    'price': book.get('price') or None,
                    'condition': book.get('condition', '').strip() or None,
                    'description': book.get('description', '').strip() or None,
                    'notes': book.get('notes', '').strip() or None,
                    'keywords': book.get('keywords', []) or book.get('tags', []) or None
                }

                # Convert publication year to integer if it's a string
                if book_data['publication_year'] and isinstance(book_data['publication_year'], str):
                    try:
                        book_data['publication_year'] = int(book_data['publication_year'])
                    except (ValueError, TypeError):
                        book_data['publication_year'] = None

                # Convert pages to integer if it's a string
                if book_data['pages'] and isinstance(book_data['pages'], str):
                    try:
                        book_data['pages'] = int(book_data['pages'])
                    except (ValueError, TypeError):
                        book_data['pages'] = None

                # Insert book
                cur.execute("""
                    INSERT INTO library_books (
                        title, author, isbn, publisher, publication_year,
                        category, subcategory, language, pages, format,
                        location, shelf_number, status, acquisition_date,
                        acquisition_method, price, condition, description,
                        notes, keywords
                    ) VALUES (
                        %(title)s, %(author)s, %(isbn)s, %(publisher)s, %(publication_year)s,
                        %(category)s, %(subcategory)s, %(language)s, %(pages)s, %(format)s,
                        %(location)s, %(shelf_number)s, %(status)s, %(acquisition_date)s,
                        %(acquisition_method)s, %(price)s, %(condition)s, %(description)s,
                        %(notes)s, %(keywords)s
                    )
                    ON CONFLICT DO NOTHING
                    RETURNING id
                """, book_data)

                result = cur.fetchone()
                if result:
                    migrated += 1
                    if migrated % 100 == 0:
                        print(f"   ... migrated {migrated} books")
                else:
                    skipped += 1

            except Exception as e:
                errors += 1
                print(f"   ❌ Error migrating book '{title}': {e}")
                continue

        # Commit the transaction
        conn.commit()

    print(f"\n✓ Library books migration complete:")
    print(f"   • Migrated: {migrated}")
    print(f"   • Skipped: {skipped}")
    print(f"   • Errors: {errors}")

    return migrated

def migrate_library_categories(conn, library_data):
    """Migrate library categories to PostgreSQL"""
    categories = library_data.get('categories', [])

    if not categories:
        print("\n⚠️  No categories to migrate")
        return 0

    print(f"\n📂 Migrating {len(categories)} categories...")

    migrated = 0

    with conn.cursor() as cur:
        for category in categories:
            try:
                if isinstance(category, str):
                    cat_name = category
                    cat_desc = None
                    parent = None
                elif isinstance(category, dict):
                    cat_name = category.get('name', '').strip()
                    cat_desc = category.get('description', '').strip() or None
                    parent = category.get('parent', '').strip() or None
                else:
                    continue

                if not cat_name:
                    continue

                cur.execute("""
                    INSERT INTO library_categories (name, description, parent_category)
                    VALUES (%s, %s, %s)
                    ON CONFLICT (name) DO NOTHING
                    RETURNING id
                """, (cat_name, cat_desc, parent))

                result = cur.fetchone()
                if result:
                    migrated += 1

            except Exception as e:
                print(f"   ❌ Error migrating category: {e}")
                continue

        conn.commit()

    print(f"✓ Migrated {migrated} categories")
    return migrated

def verify_migration(conn):
    """Verify the migration was successful"""
    print("\n🔍 Verifying migration...")

    with conn.cursor() as cur:
        # Count books
        cur.execute("SELECT COUNT(*) FROM library_books")
        book_count = cur.fetchone()[0]

        # Count categories
        cur.execute("SELECT COUNT(*) FROM library_categories")
        category_count = cur.fetchone()[0]

        # Count by status
        cur.execute("""
            SELECT status, COUNT(*)
            FROM library_books
            GROUP BY status
            ORDER BY COUNT(*) DESC
        """)
        status_counts = cur.fetchall()

        # Get some sample titles
        cur.execute("SELECT title, author FROM library_books LIMIT 5")
        samples = cur.fetchall()

    print(f"\n📊 Migration Results:")
    print(f"   • Total books: {book_count}")
    print(f"   • Total categories: {category_count}")
    print(f"\n   Status breakdown:")
    for status, count in status_counts:
        print(f"      - {status}: {count}")

    if samples:
        print(f"\n   Sample books:")
        for title, author in samples:
            author_str = f" by {author}" if author else ""
            print(f"      - {title}{author_str}")

    return book_count

def main():
    """Main migration function"""
    print("="*70)
    print("Phase 3A Migration: Library Database")
    print("="*70)

    # Load library data
    library_data = load_library_json()
    if not library_data:
        print("❌ Failed to load library data")
        return 1

    # Connect to PostgreSQL
    print(f"\n🔌 Connecting to PostgreSQL...")
    try:
        conn = psycopg.connect(DB_URL)
        print("✓ Connected to PostgreSQL")
    except Exception as e:
        print(f"❌ Failed to connect to PostgreSQL: {e}")
        return 1

    try:
        # Migrate books
        book_count = migrate_library_books(conn, library_data)

        # Migrate categories
        cat_count = migrate_library_categories(conn, library_data)

        # Verify migration
        total_books = verify_migration(conn)

        print("\n" + "="*70)
        print("✅ Library Database Migration COMPLETE")
        print("="*70)
        print(f"   • Migrated {book_count} books")
        print(f"   • Migrated {cat_count} categories")
        print(f"   • Total in database: {total_books} books")
        print()

        return 0

    except Exception as e:
        print(f"\n❌ Migration failed: {e}")
        import traceback
        traceback.print_exc()
        return 1

    finally:
        conn.close()
        print("🔌 Database connection closed")

if __name__ == '__main__':
    sys.exit(main())
