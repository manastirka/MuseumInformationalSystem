#!/usr/bin/env python3
"""
Create Sample Timesheet Data for Testing
Phase 3E: Timesheet System Migration

Creates sample timesheet reports with realistic data for testing the system.
"""

import os
import sys
from datetime import datetime
import psycopg

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Sample employee data
SAMPLE_EMPLOYEES = [
    {
        'name': 'Марко Марковић',
        'organization_unit': 'Одељење за археологију',
        'position': 'Виши кустос'
    },
    {
        'name': 'Јелена Петровић',
        'organization_unit': 'Одељење за природњачке колекције',
        'position': 'Кустос'
    },
    {
        'name': 'Немања Ђорђевић',
        'organization_unit': 'Одељење за конзервацију',
        'position': 'Конзерватор'
    }
]

def create_sample_report(conn, employee, month, year):
    """Create a sample timesheet report for an employee."""
    cursor = conn.cursor()

    # Create report
    cursor.execute("""
        INSERT INTO timesheet_reports (
            employee_name, month, year, organization_unit, position,
            approver, created_at
        ) VALUES (%s, %s, %s, %s, %s, %s, now())
        RETURNING id
    """, (
        employee['name'],
        month,
        year,
        employee['organization_unit'],
        employee['position'],
        'Др Ана Николић, директор'
    ))

    report_id = cursor.fetchone()[0]
    print(f"  ✓ Created report #{report_id} for {employee['name']} ({month}/{year})")

    # Determine number of days in month
    if month == 2:
        days_in_month = 28 if year % 4 != 0 else 29
    elif month in [4, 6, 9, 11]:
        days_in_month = 30
    else:
        days_in_month = 31

    # Create daily entries with realistic patterns
    for day in range(1, days_in_month + 1):
        # Weekday pattern (approximate)
        day_of_week = (day + (month * 2) + year) % 7

        work_in_museum = 0.0
        work_outside = 0.0
        vacation = 0.0
        public_holiday = 0.0

        # Weekend (Saturday/Sunday)
        if day_of_week >= 5:
            # Weekend - no work
            pass
        # First day of month (possible public holiday)
        elif day == 1 and month in [1, 5]:
            public_holiday = 8.0
        # Regular workday with occasional fieldwork
        else:
            if day % 7 == 0:  # Occasional fieldwork
                work_outside = 8.0
            elif day == 15 and employee['name'] == 'Јелена Петровић':  # Vacation example
                vacation = 8.0
            else:
                work_in_museum = 8.0

        # Insert daily data
        cursor.execute("""
            INSERT INTO timesheet_report_days (
                report_id, day,
                work_in_museum, work_outside, vacation, public_holiday
            ) VALUES (%s, %s, %s, %s, %s, %s)
        """, (
            report_id,
            day,
            work_in_museum,
            work_outside,
            vacation,
            public_holiday
        ))

    print(f"    • Added {days_in_month} daily entries")

    # Sync to timesheet_entries (trigger handles this automatically)
    cursor.close()
    return report_id

def main():
    """Main function to create sample data."""
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
        print("✓ Connected successfully\n")

        # Create sample data for recent months
        print("="*60)
        print("CREATING SAMPLE TIMESHEET DATA")
        print("="*60)

        current_year = 2025
        months = [10, 11, 12]  # October, November, December 2025

        total_reports = 0
        for month in months:
            print(f"\n📅 Month {month}/{current_year}:")
            for employee in SAMPLE_EMPLOYEES:
                create_sample_report(conn, employee, month, current_year)
                total_reports += 1

        # Commit all changes
        conn.commit()

        # Verify data
        print("\n" + "-"*60)
        print("DATA VERIFICATION")
        print("-"*60)

        cursor = conn.cursor()

        # Count reports
        cursor.execute("SELECT COUNT(*) FROM timesheet_reports")
        report_count = cursor.fetchone()[0]
        print(f"\n✓ Total reports created: {report_count}")

        # Count daily entries
        cursor.execute("SELECT COUNT(*) FROM timesheet_report_days")
        day_count = cursor.fetchone()[0]
        print(f"✓ Total daily entries: {day_count}")

        # Count category entries (auto-synced by trigger)
        cursor.execute("SELECT COUNT(*) FROM timesheet_entries")
        entry_count = cursor.fetchone()[0]
        print(f"✓ Total category entries (auto-synced): {entry_count}")

        # Show category breakdown
        cursor.execute("""
            SELECT category, SUM(hours) as total_hours
            FROM timesheet_entries
            GROUP BY category
            ORDER BY total_hours DESC
        """)

        print("\n📊 Hours by Category:")
        category_labels = {
            'rad_na_mestu': 'Рад у музеју',
            'van_muzeja': 'Рад ван музеја',
            'godisnji_odmor': 'Годишњи одмор',
            'drzavni_praznik': 'Државни празник',
            'placeno_odsustvo': 'Плаћено одсуство',
            'ostalo_odsustvo': 'Остало одсуство',
            'bolovanje_manje_30': 'Боловање < 30 дана',
            'bolovanje_vece_30': 'Боловање ≥ 30 дана'
        }

        for row in cursor.fetchall():
            category, hours = row
            label = category_labels.get(category, category)
            print(f"  • {label}: {hours:.1f} h")

        # Summary
        print("\n" + "="*60)
        print("SAMPLE DATA CREATION COMPLETE")
        print("="*60)
        print(f"✓ Created {report_count} timesheet reports")
        print(f"✓ Created {day_count} daily entries")
        print(f"✓ Auto-synced {entry_count} category entries")
        print("\n✅ Sample timesheet data ready for testing!\n")

        cursor.close()
        conn.close()
        return 0

    except Exception as e:
        print(f"\n❌ Error creating sample data: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == '__main__':
    sys.exit(main())
