#!/usr/bin/env python3
"""
Migrate News/Exhibitions articles from news.json to PostgreSQL
Phase 3B Migration - News and Events Database
"""

import json
import os
import sys
import psycopg
from datetime import datetime
from dotenv import load_dotenv

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Load environment variables
load_dotenv()

DATABASE_URL = os.environ.get('DATABASE_URL')
if not DATABASE_URL:
    print("ERROR: DATABASE_URL environment variable not set")
    sys.exit(1)

# Convert SQLAlchemy-style URL to psycopg format
DB_URL = DATABASE_URL.replace('postgresql+psycopg://', 'postgresql://')

def migrate_news_articles():
    """Migrate news articles from JSON to PostgreSQL."""

    print("=" * 80)
    print("NEWS/EXHIBITIONS ARTICLES MIGRATION TO POSTGRESQL")
    print("=" * 80)

    # Load news.json
    news_file = 'data/news.json'
    print(f"\n1. Loading data from {news_file}...")

    try:
        with open(news_file, 'r', encoding='utf-8') as f:
            articles = json.load(f)
        print(f"   ✓ Loaded {len(articles)} articles")
    except FileNotFoundError:
        print(f"   ✗ ERROR: {news_file} not found")
        return False
    except json.JSONDecodeError as e:
        print(f"   ✗ ERROR: Invalid JSON - {e}")
        return False

    # Connect to PostgreSQL
    print(f"\n2. Connecting to PostgreSQL...")
    try:
        conn = psycopg.connect(DB_URL)
        cur = conn.cursor()
        print(f"   ✓ Connected to database")
    except Exception as e:
        print(f"   ✗ ERROR: Failed to connect - {e}")
        return False

    # Check if table exists
    print(f"\n3. Checking news_articles table...")
    try:
        cur.execute("""
            SELECT COUNT(*) FROM news_articles
        """)
        existing_count = cur.fetchone()[0]
        print(f"   ✓ Table exists with {existing_count} existing records")

        if existing_count > 0:
            response = input(f"\n   WARNING: Table has {existing_count} records. Delete and re-import? (yes/no): ")
            if response.lower() == 'yes':
                cur.execute("DELETE FROM news_articles")
                conn.commit()
                print(f"   ✓ Deleted {existing_count} existing records")
            else:
                print(f"   → Skipping migration (table not empty)")
                conn.close()
                return True
    except Exception as e:
        print(f"   ✗ ERROR: Table check failed - {e}")
        conn.close()
        return False

    # Migrate articles
    print(f"\n4. Migrating {len(articles)} articles...")

    migrated = 0
    errors = 0

    insert_sql = """
        INSERT INTO news_articles (
            original_id, title, title_en, type, status, category,
            start_date, end_date, location, curator, co_curator,
            specimens_count, species_count, boxes_count,
            illustrations_count, visitor_count,
            description, description_en, target_audience,
            educational_programs, guided_tours, catalog_available,
            keywords, source_link
        ) VALUES (
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
        )
    """

    for article in articles:
        try:
            # Parse dates
            start_date = article.get('start_date') if article.get('start_date') else None
            end_date = article.get('end_date') if article.get('end_date') else None

            # Handle integer fields
            specimens_count = article.get('specimens_count') or 0
            species_count = article.get('species_count') or 0
            boxes_count = article.get('boxes_count') or 0
            illustrations_count = article.get('illustrations_count') or 0
            visitor_count = article.get('visitor_count') or 0

            # Convert empty strings to None
            def clean_value(val):
                if val == '' or val is None:
                    return None
                return val

            cur.execute(insert_sql, (
                article.get('id'),
                article.get('title'),
                clean_value(article.get('title_en')),
                clean_value(article.get('type')),
                clean_value(article.get('status')),
                clean_value(article.get('category')),
                start_date,
                end_date,
                clean_value(article.get('location')),
                clean_value(article.get('curator')),
                clean_value(article.get('co_curator')),
                specimens_count,
                species_count,
                boxes_count,
                illustrations_count,
                visitor_count,
                clean_value(article.get('description')),
                clean_value(article.get('description_en')),
                clean_value(article.get('target_audience')),
                clean_value(article.get('educational_programs')),
                clean_value(article.get('guided_tours')),
                clean_value(article.get('catalog_available')),
                clean_value(article.get('keywords')),
                clean_value(article.get('source_link'))
            ))

            migrated += 1

            if migrated % 10 == 0:
                print(f"   → Migrated {migrated}/{len(articles)} articles...")

        except Exception as e:
            errors += 1
            print(f"   ✗ ERROR migrating article ID {article.get('id')}: {e}")
            continue

    # Commit transaction
    try:
        conn.commit()
        print(f"\n   ✓ Committed {migrated} articles to database")
    except Exception as e:
        print(f"   ✗ ERROR: Commit failed - {e}")
        conn.rollback()
        conn.close()
        return False

    # Verify migration
    print(f"\n5. Verifying migration...")
    cur.execute("SELECT COUNT(*) FROM news_articles")
    final_count = cur.fetchone()[0]
    print(f"   ✓ PostgreSQL count: {final_count}")
    print(f"   ✓ JSON count: {len(articles)}")

    if final_count == len(articles):
        print(f"   ✓ SUCCESS: All articles migrated correctly!")
    else:
        print(f"   ⚠ WARNING: Count mismatch - {final_count} in DB vs {len(articles)} in JSON")

    # Get statistics
    print(f"\n6. Migration statistics...")

    cur.execute("SELECT type, COUNT(*) FROM news_articles GROUP BY type ORDER BY COUNT(*) DESC")
    types = cur.fetchall()
    print(f"\n   Articles by type:")
    for type_name, count in types:
        print(f"     - {type_name or '(none)'}: {count}")

    cur.execute("SELECT status, COUNT(*) FROM news_articles GROUP BY status ORDER BY COUNT(*) DESC")
    statuses = cur.fetchall()
    print(f"\n   Articles by status:")
    for status_name, count in statuses:
        print(f"     - {status_name or '(none)'}: {count}")

    cur.execute("""
        SELECT EXTRACT(YEAR FROM start_date) as year, COUNT(*)
        FROM news_articles
        WHERE start_date IS NOT NULL
        GROUP BY year
        ORDER BY year DESC
        LIMIT 5
    """)
    years = cur.fetchall()
    print(f"\n   Recent years:")
    for year, count in years:
        print(f"     - {int(year)}: {count} articles")

    # Close connection
    cur.close()
    conn.close()

    print("\n" + "=" * 80)
    print(f"MIGRATION COMPLETE")
    print(f"  Total articles: {len(articles)}")
    print(f"  Migrated: {migrated}")
    print(f"  Errors: {errors}")
    print(f"  Success rate: {(migrated/len(articles)*100):.1f}%")
    print("=" * 80)

    return errors == 0


if __name__ == '__main__':
    success = migrate_news_articles()
    sys.exit(0 if success else 1)
