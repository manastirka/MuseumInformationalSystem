#!/usr/bin/env python3
"""
Check coordinate formats in the bird ringing database
"""

import sqlite3

DB_PATH = 'data/bird_ringing.db'

def check_coordinates():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Get sample coordinates
    cursor.execute("""
        SELECT id, coordinates, location
        FROM bird_ringing
        WHERE coordinates IS NOT NULL AND coordinates != ''
        LIMIT 50
    """)

    print("Sample coordinates from database:")
    print("=" * 80)

    coordinates_samples = cursor.fetchall()

    for record_id, coords, location in coordinates_samples:
        print(f"ID: {record_id}")
        print(f"  Location: {location}")
        print(f"  Coordinates: '{coords}'")
        print()

    # Get count of records with coordinates
    cursor.execute("SELECT COUNT(*) FROM bird_ringing WHERE coordinates IS NOT NULL AND coordinates != ''")
    count = cursor.fetchone()[0]
    print(f"\nTotal records with coordinates: {count:,}")

    # Get count of total records
    cursor.execute("SELECT COUNT(*) FROM bird_ringing")
    total = cursor.fetchone()[0]
    print(f"Total records: {total:,}")
    print(f"Records without coordinates: {total - count:,}")

    conn.close()

if __name__ == '__main__':
    check_coordinates()
