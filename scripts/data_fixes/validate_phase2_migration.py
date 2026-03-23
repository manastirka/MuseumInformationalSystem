#!/usr/bin/env python3
"""
Phase 2 PostgreSQL Migration Validation Script
Validates data migration integrity and quality across all databases
"""

import os
import sys
import sqlite3
from datetime import datetime
from typing import Dict, List, Tuple
import psycopg
from psycopg.rows import dict_row
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.environ.get('DATABASE_URL')
if not DATABASE_URL:
    print("❌ DATABASE_URL not set in .env file")
    sys.exit(1)

# Color codes for output
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'

class MigrationValidator:
    def __init__(self):
        self.results = {
            'databases': {},
            'total_issues': 0,
            'timestamp': datetime.now().isoformat()
        }

    def print_header(self, title: str):
        print(f"\n{BLUE}{'='*80}{RESET}")
        print(f"{BLUE}{title.center(80)}{RESET}")
        print(f"{BLUE}{'='*80}{RESET}\n")

    def print_success(self, msg: str):
        print(f"{GREEN}✓{RESET} {msg}")

    def print_error(self, msg: str):
        print(f"{RED}✗{RESET} {msg}")
        self.results['total_issues'] += 1

    def print_warning(self, msg: str):
        print(f"{YELLOW}⚠{RESET} {msg}")

    def print_info(self, msg: str):
        print(f"  {msg}")

    def validate_bird_ringing(self):
        """Validate bird ringing database migration"""
        self.print_header("Bird Ringing Database Validation")

        sqlite_path = 'data/bird_ringing.db'
        db_result = {'name': 'Bird Ringing', 'issues': []}

        try:
            # Count records in SQLite
            sqlite_conn = sqlite3.connect(sqlite_path)
            sqlite_count = sqlite_conn.execute("SELECT COUNT(*) FROM bird_ringing").fetchone()[0]
            sqlite_conn.close()

            # Count records in PostgreSQL
            pg_url = DATABASE_URL.replace('postgresql+psycopg://', 'postgresql://')
            with psycopg.connect(pg_url, row_factory=dict_row) as conn:
                with conn.cursor() as cur:
                    cur.execute("SELECT COUNT(*) as count FROM bird_ringing_records")
                    pg_count = cur.fetchone()['count']

                    # Check species table
                    cur.execute("SELECT COUNT(*) as count FROM bird_species")
                    species_count = cur.fetchone()['count']

            self.print_info(f"SQLite records: {sqlite_count:,}")
            self.print_info(f"PostgreSQL records: {pg_count:,}")
            self.print_info(f"Bird species entries: {species_count:,}")

            if sqlite_count == pg_count:
                self.print_success(f"Record count matches: {pg_count:,} records")
            else:
                diff = sqlite_count - pg_count
                self.print_error(f"Record count mismatch: Missing {diff} records")
                db_result['issues'].append(f"Missing {diff} records")

            # Validate data quality
            with psycopg.connect(pg_url, row_factory=dict_row) as conn:
                with conn.cursor() as cur:
                    # Check for NULL required fields
                    cur.execute("""
                        SELECT COUNT(*) as count
                        FROM bird_ringing_records
                        WHERE ring_number IS NULL
                    """)
                    null_rings = cur.fetchone()['count']

                    if null_rings > 0:
                        self.print_warning(f"{null_rings} records with NULL ring numbers")
                        db_result['issues'].append(f"{null_rings} NULL ring numbers")
                    else:
                        self.print_success("No NULL ring numbers")

                    # Check coordinate conversion
                    cur.execute("""
                        SELECT COUNT(*) as count
                        FROM bird_ringing_records
                        WHERE coordinates IS NOT NULL
                    """)
                    with_coords = cur.fetchone()['count']
                    self.print_info(f"Records with coordinates: {with_coords:,}")

            db_result['sqlite_count'] = sqlite_count
            db_result['postgres_count'] = pg_count
            db_result['status'] = 'OK' if sqlite_count == pg_count else 'ISSUES'

        except Exception as e:
            self.print_error(f"Validation failed: {e}")
            db_result['status'] = 'ERROR'
            db_result['issues'].append(str(e))

        self.results['databases']['bird_ringing'] = db_result

    def validate_inventory(self):
        """Validate inventory book database migration"""
        self.print_header("Inventory Book Database Validation")

        sqlite_path = 'data/inventory_book.db'
        db_result = {'name': 'Inventory Book', 'issues': []}

        try:
            # Count records in SQLite
            sqlite_conn = sqlite3.connect(sqlite_path)
            sqlite_count = sqlite_conn.execute("SELECT COUNT(*) FROM inventory_book").fetchone()[0]
            sqlite_conn.close()

            # Count records in PostgreSQL
            pg_url = DATABASE_URL.replace('postgresql+psycopg://', 'postgresql://')
            with psycopg.connect(pg_url, row_factory=dict_row) as conn:
                with conn.cursor() as cur:
                    cur.execute("SELECT COUNT(*) as count FROM inventory_entries")
                    pg_count = cur.fetchone()['count']

            self.print_info(f"SQLite records: {sqlite_count:,}")
            self.print_info(f"PostgreSQL records: {pg_count:,}")

            if sqlite_count == pg_count:
                self.print_success(f"Record count matches: {pg_count:,} records")
            else:
                diff = sqlite_count - pg_count
                self.print_error(f"Record count mismatch: Missing {diff} records")
                db_result['issues'].append(f"Missing {diff} records")

            # Validate data quality
            with psycopg.connect(pg_url, row_factory=dict_row) as conn:
                with conn.cursor() as cur:
                    # Check for duplicate inventory numbers
                    cur.execute("""
                        SELECT inventory_number, COUNT(*) as cnt
                        FROM inventory_entries
                        WHERE inventory_number IS NOT NULL
                        GROUP BY inventory_number
                        HAVING COUNT(*) > 1
                    """)
                    duplicates = cur.fetchall()

                    if duplicates:
                        self.print_warning(f"{len(duplicates)} duplicate inventory numbers")
                        db_result['issues'].append(f"{len(duplicates)} duplicate numbers")
                    else:
                        self.print_success("No duplicate inventory numbers")

                    # Check revision status
                    cur.execute("""
                        SELECT
                            COUNT(CASE WHEN revisited THEN 1 END) as revisited,
                            COUNT(*) as total
                        FROM inventory_entries
                    """)
                    revision = cur.fetchone()
                    self.print_info(f"Revisited: {revision['revisited']:,} / {revision['total']:,}")

            db_result['sqlite_count'] = sqlite_count
            db_result['postgres_count'] = pg_count
            db_result['status'] = 'OK' if sqlite_count == pg_count else 'ISSUES'

        except Exception as e:
            self.print_error(f"Validation failed: {e}")
            db_result['status'] = 'ERROR'
            db_result['issues'].append(str(e))

        self.results['databases']['inventory'] = db_result

    def validate_minerals(self):
        """Validate mineral database migration"""
        self.print_header("Mineral Database Validation")

        sqlite_path = 'PrirodnjackiMuzej/prirodnjacki_muzej.sqlite'
        db_result = {'name': 'Minerals', 'issues': []}

        try:
            # Count records in SQLite
            sqlite_conn = sqlite3.connect(sqlite_path)
            sqlite_count = sqlite_conn.execute("SELECT COUNT(*) FROM minerali").fetchone()[0]
            sqlite_conn.close()

            # Count records in PostgreSQL
            pg_url = DATABASE_URL.replace('postgresql+psycopg://', 'postgresql://')
            with psycopg.connect(pg_url, row_factory=dict_row) as conn:
                with conn.cursor() as cur:
                    cur.execute("SELECT COUNT(*) as count FROM minerals")
                    pg_count = cur.fetchone()['count']

            self.print_info(f"SQLite records: {sqlite_count:,}")
            self.print_info(f"PostgreSQL records: {pg_count:,}")

            if sqlite_count == pg_count:
                self.print_success(f"Record count matches: {pg_count:,} records")
            else:
                diff = sqlite_count - pg_count
                self.print_error(f"Record count mismatch: Missing {diff} records")
                db_result['issues'].append(f"Missing {diff} records")

            # Validate data quality
            with psycopg.connect(pg_url, row_factory=dict_row) as conn:
                with conn.cursor() as cur:
                    # Check inventory numbers
                    cur.execute("""
                        SELECT COUNT(*) as count
                        FROM minerals
                        WHERE inventory_number IS NOT NULL
                    """)
                    with_inv = cur.fetchone()['count']
                    self.print_info(f"Records with inventory numbers: {with_inv:,}")

                    # Check acquisition methods
                    cur.execute("""
                        SELECT acquisition_method, COUNT(*) as cnt
                        FROM minerals
                        WHERE acquisition_method IS NOT NULL
                        GROUP BY acquisition_method
                        ORDER BY cnt DESC
                        LIMIT 5
                    """)
                    methods = cur.fetchall()
                    self.print_info("Top acquisition methods:")
                    for m in methods:
                        self.print_info(f"  - {m['acquisition_method']}: {m['cnt']}")

            db_result['sqlite_count'] = sqlite_count
            db_result['postgres_count'] = pg_count
            db_result['status'] = 'OK' if sqlite_count == pg_count else 'ISSUES'

        except Exception as e:
            self.print_error(f"Validation failed: {e}")
            db_result['status'] = 'ERROR'
            db_result['issues'].append(str(e))

        self.results['databases']['minerals'] = db_result

    def validate_rruff(self):
        """Validate RRUFF reference database migration"""
        self.print_header("RRUFF Reference Database Validation")

        db_result = {'name': 'RRUFF Minerals', 'issues': []}

        try:
            # Count records in PostgreSQL
            pg_url = DATABASE_URL.replace('postgresql+psycopg://', 'postgresql://')
            with psycopg.connect(pg_url, row_factory=dict_row) as conn:
                with conn.cursor() as cur:
                    cur.execute("SELECT COUNT(*) as count FROM rruff_minerals")
                    minerals_count = cur.fetchone()['count']

                    cur.execute("SELECT COUNT(*) as count FROM rruff_chemistry")
                    chemistry_count = cur.fetchone()['count']

                    cur.execute("SELECT COUNT(*) as count FROM rruff_localities")
                    localities_count = cur.fetchone()['count']

                    cur.execute("SELECT COUNT(*) as count FROM rruff_references")
                    references_count = cur.fetchone()['count']

            self.print_info(f"RRUFF minerals: {minerals_count:,}")
            self.print_info(f"Chemistry records: {chemistry_count:,}")
            self.print_info(f"Locality records: {localities_count:,}")
            self.print_info(f"Reference records: {references_count:,}")

            if minerals_count > 5000:
                self.print_success(f"RRUFF database populated with {minerals_count:,} minerals")
            else:
                self.print_warning(f"Low record count: {minerals_count:,}")

            db_result['postgres_count'] = minerals_count
            db_result['status'] = 'OK'

        except Exception as e:
            self.print_error(f"Validation failed: {e}")
            db_result['status'] = 'ERROR'
            db_result['issues'].append(str(e))

        self.results['databases']['rruff'] = db_result

    def validate_timesheet(self):
        """Validate timesheet database migration"""
        self.print_header("Timesheet Database Validation")

        sqlite_path = 'localSQLtesting/museum_timesheet.db'
        db_result = {'name': 'Timesheet', 'issues': []}

        try:
            # Count records in SQLite
            sqlite_conn = sqlite3.connect(sqlite_path)

            # Check radna_lista table
            radna_count = sqlite_conn.execute("SELECT COUNT(*) FROM radna_lista").fetchone()[0]
            user_count = sqlite_conn.execute("SELECT COUNT(*) FROM users").fetchone()[0]
            zaposleni_count = sqlite_conn.execute("SELECT COUNT(*) FROM zaposleni").fetchone()[0]

            sqlite_conn.close()

            self.print_info(f"SQLite radna_lista: {radna_count:,}")
            self.print_info(f"SQLite users: {user_count:,}")
            self.print_info(f"SQLite zaposleni: {zaposleni_count:,}")

            # Count records in PostgreSQL
            pg_url = DATABASE_URL.replace('postgresql+psycopg://', 'postgresql://')
            with psycopg.connect(pg_url, row_factory=dict_row) as conn:
                with conn.cursor() as cur:
                    cur.execute("SELECT COUNT(*) as count FROM timesheet_entries")
                    pg_timesheet = cur.fetchone()['count']

                    cur.execute("SELECT COUNT(*) as count FROM users")
                    pg_users = cur.fetchone()['count']

            self.print_info(f"PostgreSQL timesheet_entries: {pg_timesheet:,}")
            self.print_info(f"PostgreSQL users: {pg_users:,}")

            if pg_timesheet == 0:
                self.print_error("Timesheet data NOT migrated (0 records)")
                db_result['issues'].append("No timesheet data migrated")
            else:
                self.print_success(f"Timesheet data migrated: {pg_timesheet:,} entries")

            if pg_users == 0:
                self.print_error("User data NOT migrated (0 records)")
                db_result['issues'].append("No user data migrated")
            else:
                self.print_success(f"User data migrated: {pg_users:,} users")

            db_result['sqlite_count'] = radna_count
            db_result['postgres_count'] = pg_timesheet
            db_result['status'] = 'NOT_MIGRATED' if pg_timesheet == 0 else 'OK'

        except Exception as e:
            self.print_error(f"Validation failed: {e}")
            db_result['status'] = 'ERROR'
            db_result['issues'].append(str(e))

        self.results['databases']['timesheet'] = db_result

    def validate_application_config(self):
        """Validate that application is configured to use PostgreSQL"""
        self.print_header("Application Configuration Validation")

        try:
            # Check DATABASE_URL
            if DATABASE_URL:
                self.print_success(f"DATABASE_URL is set: {DATABASE_URL.split('@')[1] if '@' in DATABASE_URL else 'configured'}")
            else:
                self.print_error("DATABASE_URL not set")

            # Check PostgreSQL connection
            pg_url = DATABASE_URL.replace('postgresql+psycopg://', 'postgresql://')
            with psycopg.connect(pg_url) as conn:
                with conn.cursor() as cur:
                    cur.execute("SELECT version()")
                    version = cur.fetchone()[0]
                    self.print_success(f"PostgreSQL connected: {version.split(',')[0]}")

            # Check extensions
            with psycopg.connect(pg_url, row_factory=dict_row) as conn:
                with conn.cursor() as cur:
                    cur.execute("SELECT extname FROM pg_extension WHERE extname IN ('postgis', 'uuid-ossp', 'pgcrypto')")
                    extensions = [row['extname'] for row in cur.fetchall()]

                    for ext in ['postgis', 'uuid-ossp', 'pgcrypto']:
                        if ext in extensions:
                            self.print_success(f"Extension '{ext}' installed")
                        else:
                            self.print_warning(f"Extension '{ext}' not installed")

        except Exception as e:
            self.print_error(f"Configuration validation failed: {e}")

    def generate_summary(self):
        """Generate final summary report"""
        self.print_header("Migration Validation Summary")

        total_databases = len(self.results['databases'])
        ok_count = sum(1 for db in self.results['databases'].values() if db['status'] == 'OK')
        issues_count = sum(1 for db in self.results['databases'].values() if db['status'] == 'ISSUES')
        not_migrated = sum(1 for db in self.results['databases'].values() if db['status'] == 'NOT_MIGRATED')
        error_count = sum(1 for db in self.results['databases'].values() if db['status'] == 'ERROR')

        print(f"\n{BLUE}Database Summary:{RESET}")
        print(f"  Total databases checked: {total_databases}")
        print(f"  {GREEN}✓{RESET} Fully migrated: {ok_count}")
        print(f"  {YELLOW}⚠{RESET} With issues: {issues_count}")
        print(f"  {RED}✗{RESET} Not migrated: {not_migrated}")
        print(f"  {RED}✗{RESET} Errors: {error_count}")

        if self.results['total_issues'] == 0 and not_migrated == 0:
            print(f"\n{GREEN}{'='*80}{RESET}")
            print(f"{GREEN}Phase 2 Migration: COMPLETE AND VALIDATED{RESET}")
            print(f"{GREEN}{'='*80}{RESET}")
        elif not_migrated > 0:
            print(f"\n{YELLOW}{'='*80}{RESET}")
            print(f"{YELLOW}Phase 2 Migration: IN PROGRESS - {not_migrated} database(s) pending{RESET}")
            print(f"{YELLOW}{'='*80}{RESET}")
        else:
            print(f"\n{YELLOW}{'='*80}{RESET}")
            print(f"{YELLOW}Phase 2 Migration: COMPLETE WITH {self.results['total_issues']} ISSUES{RESET}")
            print(f"{YELLOW}{'='*80}{RESET}")

        print(f"\n{BLUE}Recommendations:{RESET}")
        for db_name, db_data in self.results['databases'].items():
            if db_data['issues']:
                print(f"\n  {YELLOW}{db_data['name']}:{RESET}")
                for issue in db_data['issues']:
                    print(f"    - {issue}")

        # Generate JSON report
        import json
        report_file = f"migration_validation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_file, 'w') as f:
            json.dump(self.results, f, indent=2)

        print(f"\n{BLUE}Detailed report saved to: {report_file}{RESET}\n")

    def run_all(self):
        """Run all validation checks"""
        print(f"\n{BLUE}{'='*80}{RESET}")
        print(f"{BLUE}PHASE 2 POSTGRESQL MIGRATION VALIDATION{RESET}")
        print(f"{BLUE}Timestamp: {self.results['timestamp']}{RESET}")
        print(f"{BLUE}{'='*80}{RESET}")

        self.validate_application_config()
        self.validate_bird_ringing()
        self.validate_inventory()
        self.validate_minerals()
        self.validate_rruff()
        self.validate_timesheet()
        self.generate_summary()


if __name__ == '__main__':
    validator = MigrationValidator()
    validator.run_all()
