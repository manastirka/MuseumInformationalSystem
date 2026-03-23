#!/usr/bin/env python3
"""
Migrate RRUFF scientific mineral data from SQLite to PostgreSQL
Migrates 5,997 RRUFF minerals with chemistry, localities, and references
"""

import sys
import os
import sqlite3
from dotenv import load_dotenv

# Load environment
load_dotenv('PrirodnjackiMuzej/.env')

try:
    import psycopg
    from psycopg.rows import dict_row
except ImportError:
    print("ERROR: psycopg driver not installed")
    print("Install with: pip install 'psycopg[binary]>=3.1.0'")
    sys.exit(1)

SQLITE_DB = 'PrirodnjackiMuzej/prirodnjacki_muzej.sqlite'
DATABASE_URL = os.environ.get('DATABASE_URL', 'postgresql://aleksandarlukovic@localhost:5432/museum_system')

def migrate_rruff_minerals(sqlite_conn, pg_conn):
    """Migrate rruff_minerals table."""
    print("\n📦 Migrating RRUFF minerals...")
    
    # Get SQLite data
    sqlite_conn.row_factory = sqlite3.Row
    cursor = sqlite_conn.cursor()
    cursor.execute("""
        SELECT 
            id, rruff_id, name, name_plain,
            formula_rruff, formula_ima, formula_concise, formula_html,
            ideal_chemistry, chemistry_elements, valence_elements,
            ima_number, ima_status, ima_mineral, ima_mineral_symbol,
            year_first_published, structural_groupname, fleischers_groupname,
            fleischers_glossary, crystal_system, crystal_systems,
            space_group, space_groups, country_type_locality,
            crystal_morphology, oldest_known_age_ma, paragenetic_modes,
            status_notes, rruff_ids, database_id, created_at
        FROM rruff_minerals
        ORDER BY id
    """)
    
    rows = cursor.fetchall()
    total = len(rows)
    print(f"  Found {total} RRUFF minerals in SQLite")
    
    # Batch insert to PostgreSQL
    batch_size = 100
    inserted = 0
    
    with pg_conn.cursor() as pg_cur:
        for i in range(0, total, batch_size):
            batch = rows[i:i + batch_size]
            
            # Build INSERT query
            values_list = []
            params = []
            
            for row in batch:
                values_list.append("""(
                    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
                )""")
                params.extend([
                    row['id'], row['rruff_id'], row['name'], row['name_plain'],
                    row['formula_rruff'], row['formula_ima'], row['formula_concise'], row['formula_html'],
                    row['ideal_chemistry'], row['chemistry_elements'], row['valence_elements'],
                    row['ima_number'], row['ima_status'], row['ima_mineral'], row['ima_mineral_symbol'],
                    row['year_first_published'], row['structural_groupname'], row['fleischers_groupname'],
                    row['fleischers_glossary'], row['crystal_system'], row['crystal_systems'],
                    row['space_group'], row['space_groups'], row['country_type_locality'],
                    row['crystal_morphology'], row['oldest_known_age_ma'], row['paragenetic_modes'],
                    row['status_notes'], row['rruff_ids'], row['database_id'], row['created_at']
                ])
            
            query = f"""
                INSERT INTO rruff_minerals (
                    id, rruff_id, name, name_plain,
                    formula_rruff, formula_ima, formula_concise, formula_html,
                    ideal_chemistry, chemistry_elements, valence_elements,
                    ima_number, ima_status, ima_mineral, ima_mineral_symbol,
                    year_first_published, structural_groupname, fleischers_groupname,
                    fleischers_glossary, crystal_system, crystal_systems,
                    space_group, space_groups, country_type_locality,
                    crystal_morphology, oldest_known_age_ma, paragenetic_modes,
                    status_notes, rruff_ids, database_id, created_at
                ) VALUES {', '.join(values_list)}
            """
            
            pg_cur.execute(query, params)
            inserted += len(batch)
            print(f"  Progress: {inserted}/{total} ({inserted/total*100:.1f}%)")
        
        # Update sequence
        pg_cur.execute("SELECT setval('rruff_minerals_id_seq', (SELECT MAX(id) FROM rruff_minerals))")
        
    pg_conn.commit()
    print(f"  ✅ Migrated {inserted} RRUFF minerals")
    return inserted


def migrate_rruff_chemistry(sqlite_conn, pg_conn):
    """Migrate rruff_chemistry table."""
    print("\n🧪 Migrating RRUFF chemistry data...")
    
    cursor = sqlite_conn.cursor()
    cursor.execute("""
        SELECT id, rruff_id, oxide, weight_percent
        FROM rruff_chemistry
        ORDER BY id
    """)
    
    rows = cursor.fetchall()
    total = len(rows)
    print(f"  Found {total} chemistry records in SQLite")
    
    batch_size = 500
    inserted = 0
    
    with pg_conn.cursor() as pg_cur:
        for i in range(0, total, batch_size):
            batch = rows[i:i + batch_size]
            
            values_list = []
            params = []
            
            for row in batch:
                values_list.append("(%s, %s, %s, %s)")
                params.extend([row[0], row[1], row[2], row[3]])
            
            query = f"""
                INSERT INTO rruff_chemistry (id, rruff_id, oxide, weight_percent)
                VALUES {', '.join(values_list)}
            """
            
            pg_cur.execute(query, params)
            inserted += len(batch)
            print(f"  Progress: {inserted}/{total} ({inserted/total*100:.1f}%)")
        
        pg_cur.execute("SELECT setval('rruff_chemistry_id_seq', (SELECT MAX(id) FROM rruff_chemistry))")
    
    pg_conn.commit()
    print(f"  ✅ Migrated {inserted} chemistry records")
    return inserted


def migrate_rruff_localities(sqlite_conn, pg_conn):
    """Migrate rruff_localities table."""
    print("\n🌍 Migrating RRUFF localities...")
    
    cursor = sqlite_conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='rruff_localities'")
    
    if not cursor.fetchone():
        print("  ⚠️  Table rruff_localities doesn't exist in SQLite, skipping")
        return 0
    
    cursor.execute("""
        SELECT id, rruff_id, locality, country
        FROM rruff_localities
        ORDER BY id
    """)
    
    rows = cursor.fetchall()
    total = len(rows)
    print(f"  Found {total} locality records in SQLite")
    
    if total == 0:
        print("  ℹ️  No locality data to migrate")
        return 0
    
    batch_size = 500
    inserted = 0
    
    with pg_conn.cursor() as pg_cur:
        for i in range(0, total, batch_size):
            batch = rows[i:i + batch_size]
            
            values_list = []
            params = []
            
            for row in batch:
                values_list.append("(%s, %s, %s, %s, NULL, NULL)")
                params.extend(row)
            
            query = f"""
                INSERT INTO rruff_localities (id, rruff_id, locality, country, latitude, longitude)
                VALUES {', '.join(values_list)}
            """
            
            pg_cur.execute(query, params)
            inserted += len(batch)
            print(f"  Progress: {inserted}/{total} ({inserted/total*100:.1f}%)")
        
        if inserted > 0:
            pg_cur.execute("SELECT setval('rruff_localities_id_seq', (SELECT MAX(id) FROM rruff_localities))")
    
    pg_conn.commit()
    print(f"  ✅ Migrated {inserted} locality records")
    return inserted


def migrate_rruff_references(sqlite_conn, pg_conn):
    """Migrate rruff_references table."""
    print("\n📚 Migrating RRUFF references...")
    
    cursor = sqlite_conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='rruff_references'")
    
    if not cursor.fetchone():
        print("  ⚠️  Table rruff_references doesn't exist in SQLite, skipping")
        return 0
    
    cursor.execute("""
        SELECT id, rruff_id, reference_text, year, journal, reference
        FROM rruff_references
        ORDER BY id
    """)
    
    rows = cursor.fetchall()
    total = len(rows)
    print(f"  Found {total} reference records in SQLite")
    
    if total == 0:
        print("  ℹ️  No reference data to migrate")
        return 0
    
    batch_size = 500
    inserted = 0
    
    with pg_conn.cursor() as pg_cur:
        for i in range(0, total, batch_size):
            batch = rows[i:i + batch_size]
            
            values_list = []
            params = []
            
            for row in batch:
                # row: id, rruff_id, reference_text, year, journal, reference
                values_list.append("(%s, %s, %s, NULL, NULL, %s, %s, NULL)")
                # id, rruff_id, reference_text, year, journal
                params.extend([row[0], row[1], row[2], row[4], row[3]])
            
            query = f"""
                INSERT INTO rruff_references (id, rruff_id, reference_text, authors, title, journal, year, doi)
                VALUES {', '.join(values_list)}
            """
            
            pg_cur.execute(query, params)
            inserted += len(batch)
            print(f"  Progress: {inserted}/{total} ({inserted/total*100:.1f}%)")
        
        if inserted > 0:
            pg_cur.execute("SELECT setval('rruff_references_id_seq', (SELECT MAX(id) FROM rruff_references))")
    
    pg_conn.commit()
    print(f"  ✅ Migrated {inserted} reference records")
    return inserted


def migrate_mineral_rruff_matches(sqlite_conn, pg_conn):
    """Migrate mineral_rruff_matches table."""
    print("\n🔗 Migrating mineral-RRUFF matches...")
    
    # Skip matches migration due to foreign key constraints
    # These will be regenerated when the system is used
    print("  ℹ️  Skipping matches - will be regenerated when system is used")
    return 0
    
    cursor = sqlite_conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='mineral_rruff_matches'")
    
    if not cursor.fetchone():
        print("  ⚠️  Table mineral_rruff_matches doesn't exist in SQLite, skipping")
        return 0
    
    cursor.execute("""
        SELECT id, mineral_id, rruff_id, match_confidence, match_method
        FROM mineral_rruff_matches
        ORDER BY id
    """)
    
    rows = cursor.fetchall()
    total = len(rows)
    print(f"  Found {total} match records in SQLite")
    
    if total == 0:
        print("  ℹ️  No match data to migrate")
        return 0
    
    batch_size = 500
    inserted = 0
    
    with pg_conn.cursor() as pg_cur:
        for i in range(0, total, batch_size):
            batch = rows[i:i + batch_size]
            
            values_list = []
            params = []
            
            for row in batch:
                values_list.append("(%s, %s, %s, %s, %s, NOW())")
                params.extend(row)
            
            query = f"""
                INSERT INTO mineral_rruff_matches (id, mineral_id, rruff_id, match_confidence, matched_by, matched_at)
                VALUES {', '.join(values_list)}
            """
            
            pg_cur.execute(query, params)
            inserted += len(batch)
            print(f"  Progress: {inserted}/{total} ({inserted/total*100:.1f}%)")
        
        if inserted > 0:
            pg_cur.execute("SELECT setval('mineral_rruff_matches_id_seq', (SELECT MAX(id) FROM mineral_rruff_matches))")
    
    pg_conn.commit()
    print(f"  ✅ Migrated {inserted} match records")
    return inserted


def main():
    """Main migration function."""
    print("="*70)
    print("  RRUFF Database Migration: SQLite → PostgreSQL")
    print("="*70)
    
    # Check SQLite database
    if not os.path.exists(SQLITE_DB):
        print(f"\n❌ SQLite database not found: {SQLITE_DB}")
        return 1
    
    print(f"\n📂 SQLite database: {SQLITE_DB}")
    print(f"📍 PostgreSQL URL: {DATABASE_URL}")
    
    # Connect to databases
    try:
        sqlite_conn = sqlite3.connect(SQLITE_DB)
        print("✅ Connected to SQLite")
    except Exception as e:
        print(f"❌ Failed to connect to SQLite: {e}")
        return 1
    
    try:
        # Convert sqlalchemy-style URL to psycopg format
        db_url = DATABASE_URL.replace('postgresql+psycopg://', 'postgresql://')
        pg_conn = psycopg.connect(db_url)
        print("✅ Connected to PostgreSQL")
    except Exception as e:
        print(f"❌ Failed to connect to PostgreSQL: {e}")
        return 1
    
    try:
        # Run migrations
        results = {}
        results['minerals'] = migrate_rruff_minerals(sqlite_conn, pg_conn)
        results['chemistry'] = migrate_rruff_chemistry(sqlite_conn, pg_conn)
        results['localities'] = migrate_rruff_localities(sqlite_conn, pg_conn)
        results['references'] = migrate_rruff_references(sqlite_conn, pg_conn)
        results['matches'] = migrate_mineral_rruff_matches(sqlite_conn, pg_conn)
        
        # Summary
        print("\n" + "="*70)
        print("  MIGRATION SUMMARY")
        print("="*70)
        print(f"  ✅ RRUFF Minerals: {results['minerals']:,}")
        print(f"  ✅ Chemistry Records: {results['chemistry']:,}")
        print(f"  ✅ Locality Records: {results['localities']:,}")
        print(f"  ✅ Reference Records: {results['references']:,}")
        print(f"  ✅ Match Records: {results['matches']:,}")
        print(f"\n  Total Records Migrated: {sum(results.values()):,}")
        print("\n🎉 RRUFF migration completed successfully!")
        
        return 0
        
    except Exception as e:
        print(f"\n❌ Migration failed: {e}")
        import traceback
        traceback.print_exc()
        pg_conn.rollback()
        return 1
        
    finally:
        sqlite_conn.close()
        pg_conn.close()


if __name__ == '__main__':
    sys.exit(main())
