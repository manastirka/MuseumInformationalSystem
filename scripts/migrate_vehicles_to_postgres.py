#!/usr/bin/env python3
"""
Vehicle System Migration to PostgreSQL - Phase 3D
Migrates vehicle and reservation data from JSON files to PostgreSQL.
"""

import os
import sys
import json
import psycopg
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def load_json_file(filepath):
    """Load data from JSON file."""
    if not os.path.exists(filepath):
        print(f"⚠️  File not found: {filepath}")
        return []

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data if isinstance(data, list) else []
    except Exception as e:
        print(f"❌ Error loading {filepath}: {e}")
        return []

def migrate_vehicles(conn):
    """Migrate vehicles from museum_vehicles.json to PostgreSQL."""
    print("\n" + "="*60)
    print("PHASE 3D: VEHICLE SYSTEM MIGRATION")
    print("="*60)

    # Load vehicles from JSON
    vehicles_file = 'data/museum_vehicles.json'
    vehicles = load_json_file(vehicles_file)

    print(f"\n📋 Found {len(vehicles)} vehicles in {vehicles_file}")

    if not vehicles:
        print("⚠️  No vehicles to migrate")
        return 0

    # Migrate vehicles
    cursor = conn.cursor()
    migrated_count = 0

    for vehicle in vehicles:
        try:
            # Prepare image_ids array
            image_ids = vehicle.get('image_ids', [])
            if not image_ids:
                image_ids = None

            # Insert vehicle
            cursor.execute("""
                INSERT INTO vehicles (
                    id, name, registration, type, capacity, status,
                    year, make_model, notes, image_ids, created_at, updated_at
                ) VALUES (
                    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, now(), now()
                )
                ON CONFLICT (id) DO UPDATE SET
                    name = EXCLUDED.name,
                    registration = EXCLUDED.registration,
                    type = EXCLUDED.type,
                    capacity = EXCLUDED.capacity,
                    status = EXCLUDED.status,
                    year = EXCLUDED.year,
                    make_model = EXCLUDED.make_model,
                    notes = EXCLUDED.notes,
                    image_ids = EXCLUDED.image_ids,
                    updated_at = now()
            """, (
                vehicle.get('id'),
                vehicle.get('name'),
                vehicle.get('registration'),
                vehicle.get('type'),
                vehicle.get('capacity'),
                vehicle.get('status', 'Активно'),
                vehicle.get('year'),
                vehicle.get('make_model'),
                vehicle.get('notes'),
                image_ids
            ))

            migrated_count += 1
            print(f"  ✓ {vehicle.get('name')} ({vehicle.get('registration')})")

        except Exception as e:
            print(f"  ❌ Error migrating vehicle {vehicle.get('name')}: {e}")
            raise

    conn.commit()
    return migrated_count

def migrate_reservations(conn):
    """Migrate vehicle reservations from vehicle_reservations.json to PostgreSQL."""
    print("\n" + "-"*60)
    print("Vehicle Reservations Migration")
    print("-"*60)

    # Load reservations from JSON
    reservations_file = 'data/vehicle_reservations.json'
    reservations = load_json_file(reservations_file)

    print(f"\n📋 Found {len(reservations)} reservations in {reservations_file}")

    if not reservations:
        print("ℹ️  No reservations to migrate (file is empty)")
        return 0

    # Migrate reservations
    cursor = conn.cursor()
    migrated_count = 0

    for reservation in reservations:
        try:
            cursor.execute("""
                INSERT INTO vehicle_reservations (
                    id, vehicle_id, reserved_by, purpose,
                    start_date, end_date, start_time, end_time,
                    destination, estimated_km, driver_name, driver_license,
                    passengers, notes, status, approved_by, approved_at,
                    created_at, updated_at
                ) VALUES (
                    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                    %s, %s, %s, %s, %s, %s, %s, now(), now()
                )
                ON CONFLICT (id) DO UPDATE SET
                    vehicle_id = EXCLUDED.vehicle_id,
                    reserved_by = EXCLUDED.reserved_by,
                    purpose = EXCLUDED.purpose,
                    start_date = EXCLUDED.start_date,
                    end_date = EXCLUDED.end_date,
                    start_time = EXCLUDED.start_time,
                    end_time = EXCLUDED.end_time,
                    destination = EXCLUDED.destination,
                    estimated_km = EXCLUDED.estimated_km,
                    driver_name = EXCLUDED.driver_name,
                    driver_license = EXCLUDED.driver_license,
                    passengers = EXCLUDED.passengers,
                    notes = EXCLUDED.notes,
                    status = EXCLUDED.status,
                    approved_by = EXCLUDED.approved_by,
                    approved_at = EXCLUDED.approved_at,
                    updated_at = now()
            """, (
                reservation.get('id'),
                reservation.get('vehicle_id'),
                reservation.get('reserved_by'),
                reservation.get('purpose'),
                reservation.get('start_date'),
                reservation.get('end_date'),
                reservation.get('start_time'),
                reservation.get('end_time'),
                reservation.get('destination'),
                reservation.get('estimated_km'),
                reservation.get('driver_name'),
                reservation.get('driver_license'),
                reservation.get('passengers'),
                reservation.get('notes'),
                reservation.get('status', 'Активна'),
                reservation.get('approved_by'),
                reservation.get('approved_at')
            ))

            migrated_count += 1
            print(f"  ✓ Reservation #{reservation.get('id')} for vehicle {reservation.get('vehicle_id')}")

        except Exception as e:
            print(f"  ❌ Error migrating reservation {reservation.get('id')}: {e}")
            raise

    conn.commit()
    return migrated_count

def verify_migration(conn):
    """Verify the migration was successful."""
    print("\n" + "-"*60)
    print("Migration Verification")
    print("-"*60)

    cursor = conn.cursor()

    # Count vehicles
    cursor.execute("SELECT COUNT(*) FROM vehicles")
    vehicle_count = cursor.fetchone()[0]
    print(f"\n✓ Vehicles in PostgreSQL: {vehicle_count}")

    # Count reservations
    cursor.execute("SELECT COUNT(*) FROM vehicle_reservations")
    reservation_count = cursor.fetchone()[0]
    print(f"✓ Reservations in PostgreSQL: {reservation_count}")

    # Show vehicle statistics by type
    cursor.execute("""
        SELECT type, COUNT(*) as count
        FROM vehicles
        GROUP BY type
        ORDER BY count DESC
    """)

    print("\n📊 Vehicles by Type:")
    for row in cursor.fetchall():
        vehicle_type = row[0] or 'Без типа'
        count = row[1]
        print(f"  • {vehicle_type}: {count}")

    # Show vehicle statistics by status
    cursor.execute("""
        SELECT status, COUNT(*) as count
        FROM vehicles
        GROUP BY status
        ORDER BY count DESC
    """)

    print("\n📊 Vehicles by Status:")
    for row in cursor.fetchall():
        status = row[0]
        count = row[1]
        print(f"  • {status}: {count}")

    return vehicle_count, reservation_count

def main():
    """Main migration function."""
    # Get database URL
    database_url = os.environ.get('DATABASE_URL')
    if not database_url:
        print("❌ DATABASE_URL environment variable not set")
        print("Please run: export DATABASE_URL='postgresql://...'")
        return 1

    try:
        # Connect to PostgreSQL
        print("🔌 Connecting to PostgreSQL...")
        conn = psycopg.connect(database_url)
        print("✓ Connected successfully")

        # Create schema if needed
        print("\n📋 Creating vehicle schema...")
        schema_file = 'db/schema_vehicles.sql'
        if os.path.exists(schema_file):
            with open(schema_file, 'r', encoding='utf-8') as f:
                schema_sql = f.read()
                conn.execute(schema_sql)
                conn.commit()
                print("✓ Schema created/updated")
        else:
            print(f"⚠️  Schema file not found: {schema_file}")

        # Migrate data
        vehicles_migrated = migrate_vehicles(conn)
        reservations_migrated = migrate_reservations(conn)

        # Verify migration
        vehicle_count, reservation_count = verify_migration(conn)

        # Summary
        print("\n" + "="*60)
        print("MIGRATION SUMMARY")
        print("="*60)
        print(f"✓ Vehicles migrated: {vehicles_migrated}")
        print(f"✓ Reservations migrated: {reservations_migrated}")
        print(f"✓ Total vehicles in database: {vehicle_count}")
        print(f"✓ Total reservations in database: {reservation_count}")

        success_rate = 100.0 if vehicles_migrated > 0 else 0
        print(f"\n🎯 Migration success rate: {success_rate:.1f}%")
        print("\n✅ Phase 3D: Vehicle System Migration Complete!")

        conn.close()
        return 0

    except Exception as e:
        print(f"\n❌ Migration failed: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == '__main__':
    sys.exit(main())
