#!/usr/bin/env python3
"""
Comprehensive Test Suite for Timesheet System Integration
Tests all routes, database operations, and approval workflows
"""

import os
import sys
import psycopg
from psycopg.rows import dict_row
from datetime import datetime

# Colors for output
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    END = '\033[0m'
    BOLD = '\033[1m'

def print_success(msg):
    print(f"{Colors.GREEN}✓{Colors.END} {msg}")

def print_error(msg):
    print(f"{Colors.RED}✗{Colors.END} {msg}")

def print_info(msg):
    print(f"{Colors.BLUE}ℹ{Colors.END} {msg}")

def print_section(msg):
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.END}")
    print(f"{Colors.BOLD}{msg}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.END}\n")

# Database connection
DATABASE_URL = os.environ.get('DATABASE_URL', 'postgresql://aleksandarlukovic@localhost/museum_system')

def test_database_schema():
    """Test 1: Verify database schema has all required columns"""
    print_section("TEST 1: Database Schema Validation")

    try:
        with psycopg.connect(DATABASE_URL) as conn:
            with conn.cursor() as cur:
                # Check timesheet_reports columns
                cur.execute("""
                    SELECT column_name FROM information_schema.columns
                    WHERE table_name = 'timesheet_reports'
                    AND column_name IN ('is_verified', 'verified_by', 'verified_at', 'is_locked')
                """)
                columns = [row[0] for row in cur.fetchall()]

                required_columns = ['is_verified', 'verified_by', 'verified_at', 'is_locked']
                missing = [col for col in required_columns if col not in columns]

                if missing:
                    print_error(f"Missing columns in timesheet_reports: {', '.join(missing)}")
                    return False
                else:
                    print_success("All verification columns exist in timesheet_reports")

                # Check timesheet_edit_requests table
                cur.execute("""
                    SELECT EXISTS (
                        SELECT FROM information_schema.tables
                        WHERE table_name = 'timesheet_edit_requests'
                    )
                """)

                if cur.fetchone()[0]:
                    print_success("timesheet_edit_requests table exists")
                else:
                    print_error("timesheet_edit_requests table does NOT exist")
                    return False

                # Check indexes
                cur.execute("""
                    SELECT indexname FROM pg_indexes
                    WHERE tablename = 'timesheet_reports'
                    AND indexname LIKE '%verified%'
                """)
                indexes = [row[0] for row in cur.fetchall()]

                if indexes:
                    print_success(f"Found {len(indexes)} verification indexes")
                else:
                    print_error("No verification indexes found")

                return True

    except Exception as e:
        print_error(f"Database schema test failed: {e}")
        return False

def test_create_sample_report():
    """Test 2: Create a sample timesheet report"""
    print_section("TEST 2: Create Sample Timesheet Report")

    try:
        with psycopg.connect(DATABASE_URL, row_factory=dict_row) as conn:
            with conn.cursor() as cur:
                # Check if test report already exists
                cur.execute("""
                    SELECT id FROM timesheet_reports
                    WHERE employee_name = 'Test Запослени'
                    AND month = 1 AND year = 2026
                """)

                existing = cur.fetchone()
                if existing:
                    print_info(f"Test report already exists (ID: {existing['id']})")
                    return existing['id']

                # Create test report
                cur.execute("""
                    INSERT INTO timesheet_reports
                    (employee_name, month, year, organization_unit, position, created_at)
                    VALUES ('Test Запослени', 1, 2026, 'Тест Одељење', 'Тест Позиција', NOW())
                    RETURNING id
                """)

                report_id = cur.fetchone()['id']

                # Add sample entries
                categories = [
                    ('rad_na_mestu', 160.0),
                    ('van_muzeja', 16.0),
                    ('godisnji_odmor', 8.0),
                    ('drzavni_praznik', 0.0),
                    ('placeno_odsustvo', 0.0),
                    ('ostalo_odsustvo', 0.0),
                    ('bolovanje_manje_30', 0.0),
                    ('bolovanje_vece_30', 0.0)
                ]

                for category, hours in categories:
                    cur.execute("""
                        INSERT INTO timesheet_entries (report_id, category, hours, created_at)
                        VALUES (%s, %s, %s, NOW())
                    """, (report_id, category, hours))

                conn.commit()

                print_success(f"Created test report (ID: {report_id}) with 8 entries")
                print_info(f"  Employee: Test Запослени")
                print_info(f"  Period: Јануар 2026")
                print_info(f"  Total hours: 184.0")

                return report_id

    except Exception as e:
        print_error(f"Failed to create sample report: {e}")
        return None

def test_verify_report(report_id):
    """Test 3: Verify a report (simulate admin approval)"""
    print_section("TEST 3: Verify/Lock Report")

    try:
        with psycopg.connect(DATABASE_URL, row_factory=dict_row) as conn:
            with conn.cursor() as cur:
                # Verify and lock the report
                cur.execute("""
                    UPDATE timesheet_reports
                    SET is_verified = TRUE,
                        verified_by = 'test@admin.com',
                        verified_at = NOW(),
                        is_locked = TRUE
                    WHERE id = %s
                    RETURNING is_verified, is_locked
                """, (report_id,))

                result = cur.fetchone()
                conn.commit()

                if result and result['is_verified'] and result['is_locked']:
                    print_success(f"Report {report_id} verified and locked")
                    print_info(f"  Verified by: test@admin.com")
                    print_info(f"  Status: Locked")
                    return True
                else:
                    print_error("Failed to verify/lock report")
                    return False

    except Exception as e:
        print_error(f"Verification test failed: {e}")
        return False

def test_create_edit_request(report_id):
    """Test 4: Create an edit request"""
    print_section("TEST 4: Create Edit Request")

    try:
        with psycopg.connect(DATABASE_URL, row_factory=dict_row) as conn:
            with conn.cursor() as cur:
                # Create edit request
                cur.execute("""
                    INSERT INTO timesheet_edit_requests
                    (report_id, requester_email, reason, status, requested_at)
                    VALUES (%s, %s, %s, 'pending', NOW())
                    RETURNING id
                """, (report_id, 'test@employee.com', 'Потребно је да исправим грешку у подацима'))

                request_id = cur.fetchone()['id']
                conn.commit()

                print_success(f"Created edit request (ID: {request_id})")
                print_info(f"  Report ID: {report_id}")
                print_info(f"  Requester: test@employee.com")
                print_info(f"  Status: pending")

                return request_id

    except Exception as e:
        print_error(f"Failed to create edit request: {e}")
        return None

def test_approve_edit_request(request_id):
    """Test 5: Approve an edit request"""
    print_section("TEST 5: Approve Edit Request")

    try:
        with psycopg.connect(DATABASE_URL, row_factory=dict_row) as conn:
            with conn.cursor() as cur:
                # Approve request
                cur.execute("""
                    UPDATE timesheet_edit_requests
                    SET status = 'approved',
                        processed_at = NOW(),
                        processed_by = 'admin@test.com',
                        notes = 'Одобрено за измену'
                    WHERE id = %s
                    RETURNING status
                """, (request_id,))

                result = cur.fetchone()

                if result and result['status'] == 'approved':
                    # Unlock the associated report
                    cur.execute("""
                        UPDATE timesheet_reports tr
                        SET is_locked = FALSE
                        FROM timesheet_edit_requests ter
                        WHERE ter.id = %s AND ter.report_id = tr.id
                        RETURNING tr.id
                    """, (request_id,))

                    unlocked = cur.fetchone()
                    conn.commit()

                    if unlocked:
                        print_success(f"Edit request {request_id} approved")
                        print_success(f"Report {unlocked['id']} unlocked for editing")
                        print_info(f"  Approved by: admin@test.com")
                        return True
                else:
                    print_error("Failed to approve request")
                    return False

    except Exception as e:
        print_error(f"Approval test failed: {e}")
        return False

def test_repository_query():
    """Test 6: Verify TimesheetRepository can fetch reports with verification status"""
    print_section("TEST 6: TimesheetRepository Query")

    try:
        from timesheet_repository import TimesheetRepository

        repo = TimesheetRepository(DATABASE_URL.replace('postgresql://', 'postgresql+psycopg://'))

        if not repo.available:
            print_error("TimesheetRepository not available")
            return False

        # List reports
        reports = repo.list_reports(page=1, per_page=10)

        if reports and reports.get('reports'):
            print_success(f"Repository fetched {len(reports['reports'])} report(s)")

            for report in reports['reports']:
                print_info(f"  Report ID {report['id']}: {report['employee_name']}")
                print_info(f"    Verified: {report.get('is_verified', False)}")
                print_info(f"    Locked: {report.get('is_locked', False)}")

                if 'verified_by' not in report:
                    print_error("    WARNING: verified_by field missing from query")
                    return False

            return True
        else:
            print_error("Repository returned no reports")
            return False

    except Exception as e:
        print_error(f"Repository test failed: {e}")
        return False

def test_word_export(report_id):
    """Test 7: Test Word export functionality"""
    print_section("TEST 7: Word Document Export")

    try:
        # Check if python-docx is available
        try:
            import docx
            print_success("python-docx library is available")
        except ImportError:
            print_error("python-docx not installed")
            print_info("  Install with: pip install python-docx")
            return False

        from timesheet_word_export import generate_word_document

        output_path = generate_word_document(report_id, DATABASE_URL)

        if output_path and os.path.exists(output_path):
            file_size = os.path.getsize(output_path)
            print_success(f"Word document generated successfully")
            print_info(f"  Path: {output_path}")
            print_info(f"  Size: {file_size:,} bytes")

            # Clean up test file
            os.remove(output_path)
            print_info(f"  Test file removed")

            return True
        else:
            print_error("Word document generation failed")
            return False

    except Exception as e:
        print_error(f"Word export test failed: {e}")
        return False

def test_cleanup():
    """Test 8: Clean up test data"""
    print_section("TEST 8: Cleanup Test Data")

    try:
        with psycopg.connect(DATABASE_URL) as conn:
            with conn.cursor() as cur:
                # Disable triggers temporarily
                cur.execute("ALTER TABLE timesheet_entries DISABLE TRIGGER ALL")
                cur.execute("ALTER TABLE timesheet_reports DISABLE TRIGGER ALL")

                # Delete entries first (foreign key)
                cur.execute("""
                    DELETE FROM timesheet_entries
                    WHERE report_id IN (
                        SELECT id FROM timesheet_reports
                        WHERE employee_name = 'Test Запослени'
                    )
                """)
                entries_deleted = cur.rowcount

                # Delete test reports
                cur.execute("""
                    DELETE FROM timesheet_reports
                    WHERE employee_name = 'Test Запослени'
                """)
                reports_deleted = cur.rowcount

                # Re-enable triggers
                cur.execute("ALTER TABLE timesheet_entries ENABLE TRIGGER ALL")
                cur.execute("ALTER TABLE timesheet_reports ENABLE TRIGGER ALL")

                conn.commit()

                print_success(f"Deleted {reports_deleted} report(s) and {entries_deleted} entries")
                print_info("Database restored to clean state")

                return True

    except Exception as e:
        print_error(f"Cleanup failed: {e}")
        return False

def main():
    """Run all tests"""
    print(f"\n{Colors.BOLD}{'='*60}")
    print(f"TIMESHEET SYSTEM INTEGRATION TEST SUITE")
    print(f"{'='*60}{Colors.END}\n")

    print_info(f"Database: {DATABASE_URL.split('@')[1] if '@' in DATABASE_URL else DATABASE_URL}")
    print_info(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    results = {}

    # Test 1: Schema
    results['Schema'] = test_database_schema()

    # Test 2: Create report
    report_id = test_create_sample_report()
    results['Create Report'] = report_id is not None

    if report_id:
        # Test 3: Verify report
        results['Verify Report'] = test_verify_report(report_id)

        # Test 4: Create edit request
        request_id = test_create_edit_request(report_id)
        results['Create Edit Request'] = request_id is not None

        if request_id:
            # Test 5: Approve request
            results['Approve Request'] = test_approve_edit_request(request_id)

        # Test 6: Repository query
        results['Repository Query'] = test_repository_query()

        # Test 7: Word export
        results['Word Export'] = test_word_export(report_id)

        # Test 8: Cleanup
        results['Cleanup'] = test_cleanup()

    # Summary
    print_section("TEST SUMMARY")

    passed = sum(1 for v in results.values() if v)
    total = len(results)

    for test_name, passed_test in results.items():
        if passed_test:
            print_success(f"{test_name}")
        else:
            print_error(f"{test_name}")

    print(f"\n{Colors.BOLD}Result: {passed}/{total} tests passed{Colors.END}")

    if passed == total:
        print(f"{Colors.GREEN}{Colors.BOLD}✓ ALL TESTS PASSED!{Colors.END}\n")
        return 0
    else:
        print(f"{Colors.RED}{Colors.BOLD}✗ SOME TESTS FAILED{Colors.END}\n")
        return 1

if __name__ == '__main__':
    sys.exit(main())
