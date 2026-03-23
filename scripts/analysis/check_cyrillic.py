#!/usr/bin/env python3
"""
Check the actual character encoding in failing coordinates
"""

import sqlite3

DB_PATH = 'data/bird_ringing.db'

def check_cyrillic():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Get one of the failing coordinates
    cursor.execute("""
        SELECT id, coordinates
        FROM bird_ringing
        WHERE id = 36874
    """)

    record = cursor.fetchone()
    if record:
        record_id, coords = record
        print(f"ID: {record_id}")
        print(f"Coordinates: '{coords}'")
        print(f"\nCharacter analysis:")
        for i, char in enumerate(coords):
            print(f"  [{i:2d}] '{char}' -> U+{ord(char):04X} ({ord(char)}) - {char!r}")

    conn.close()

if __name__ == '__main__':
    check_cyrillic()
