#!/usr/bin/env python3
import sqlite3

conn = sqlite3.connect('data/bird_ringing.db')
cursor = conn.cursor()

# Count standardized coordinates (format: "XX.XXXXXX, YY.YYYYYY")
cursor.execute('SELECT COUNT(*) FROM bird_ringing WHERE coordinates LIKE "%.%, %"')
standardized = cursor.fetchone()[0]

# Count total records with coordinates
cursor.execute('SELECT COUNT(*) FROM bird_ringing WHERE coordinates IS NOT NULL AND coordinates != ""')
total_with_coords = cursor.fetchone()[0]

# Count total records
cursor.execute('SELECT COUNT(*) FROM bird_ringing')
total_records = cursor.fetchone()[0]

print("=" * 60)
print("Bird Ringing Coordinate Conversion Results")
print("=" * 60)
print(f"Total records in database:     {total_records:>10,}")
print(f"Records with coordinates:      {total_with_coords:>10,}")
print(f"Standardized coordinates:      {standardized:>10,}")
print(f"Non-standard coordinates:      {total_with_coords - standardized:>10,}")
print(f"Records without coordinates:   {total_records - total_with_coords:>10,}")
print()
print(f"Success rate: {(standardized / total_with_coords * 100):.1f}%")
print("=" * 60)

# Show some examples
print("\nSample standardized coordinates:")
cursor.execute('SELECT id, species, location, coordinates FROM bird_ringing WHERE coordinates LIKE "%.%, %" LIMIT 5')
for record_id, species, location, coords in cursor.fetchall():
    print(f"  ID {record_id}: {coords}")
    print(f"    {species} at {location}")
    print()

conn.close()
