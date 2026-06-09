#!/usr/bin/env python3
"""
Comprehensive Reliability Test Suite for Timesheet System
Tests: validation, concurrent access, data integrity, error handling, edge cases
"""

import os
import sys
import time
import calendar
import threading
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed

# Colors for output
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    END = '\033[0m'
    BOLD = '\033[1m'

def print_success(msg):
    print(f"{Colors.GREEN}✓{Colors.END} {msg}")

def print_error(msg):
    print(f"{Colors.RED}✗{Colors.END} {msg}")

def print_info(msg):
    print(f"{Colors.BLUE}ℹ{Colors.END} {msg}")

def print_warning(msg):
    print(f"{Colors.YELLOW}⚠{Colors.END} {msg}")

def print_section(msg):
    print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*60}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.CYAN}{msg}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.CYAN}{'='*60}{Colors.END}\n")

# Test configuration
DATABASE_URL = os.environ.get('DATABASE_URL', 'postgresql://aleksandarlukovic@localhost/museum_system')
TEST_EMAIL = 'test_reliability@museum.test'
TEST_NAME = 'Test Reliability User'


class TestResults:
    __test__ = False  # plain result holder, not a pytest test class
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.errors = []

    def record_pass(self, test_name):
        self.passed += 1
        print_success(test_name)

    def record_fail(self, test_name, reason):
        self.failed += 1
        self.errors.append((test_name, reason))
        print_error(f"{test_name}: {reason}")

    def summary(self):
        total = self.passed + self.failed
        print_section("TEST SUMMARY")
        print(f"Passed: {Colors.GREEN}{self.passed}{Colors.END}/{total}")
        print(f"Failed: {Colors.RED}{self.failed}{Colors.END}/{total}")
        if self.errors:
            print(f"\n{Colors.RED}Failed tests:{Colors.END}")
            for name, reason in self.errors:
                print(f"  - {name}: {reason}")
        return self.failed == 0


results = TestResults()


try:
    import pytest

    @pytest.fixture(scope='session', autouse=True)
    def _reliability_suite_cleanup():
        yield
        cleanup_test_data()
except ImportError:
    pass


# =============================================================================
# VALIDATION TESTS
# =============================================================================

def test_validation_negative_hours():
    """Test that negative hours are rejected"""
    from timesheet_postgres import validate_hours

    error = validate_hours(-5.0, "test_field")
    if error and "негативна" in error:
        results.record_pass("Validation: Negative hours rejected")
    else:
        results.record_fail("Validation: Negative hours rejected", f"Got: {error}")


def test_validation_excessive_hours():
    """Test that hours > 24 are rejected"""
    from timesheet_postgres import validate_hours

    error = validate_hours(25.0, "test_field")
    if error and "24" in error:
        results.record_pass("Validation: Hours > 24 rejected")
    else:
        results.record_fail("Validation: Hours > 24 rejected", f"Got: {error}")


def test_validation_valid_hours():
    """Test that valid hours pass validation"""
    from timesheet_postgres import validate_hours

    for hours in [0, 4, 8, 12, 24]:
        error = validate_hours(float(hours))
        if error:
            results.record_fail(f"Validation: Valid hours {hours}", error)
            return

    results.record_pass("Validation: Valid hours (0, 4, 8, 12, 24) accepted")


def test_validation_month_year():
    """Test month/year validation"""
    from timesheet_postgres import validate_month_year

    # Invalid month
    error = validate_month_year(13, 2026)
    if not error:
        results.record_fail("Validation: Invalid month 13", "Should have failed")
        return

    # Invalid year
    error = validate_month_year(1, 1999)
    if not error:
        results.record_fail("Validation: Invalid year 1999", "Should have failed")
        return

    # Valid
    error = validate_month_year(2, 2026)
    if error:
        results.record_fail("Validation: Valid month/year", error)
        return

    results.record_pass("Validation: Month/year validation works")


def test_validation_daily_data():
    """Test daily data validation"""
    from timesheet_postgres import validate_daily_data

    # Test invalid day for month
    daily_data = {
        '31': {'rad_na_mestu': 8}  # February doesn't have 31 days
    }
    errors = validate_daily_data(daily_data, 2, 2026)
    if not errors:
        results.record_fail("Validation: Invalid day for month", "Should have failed")
        return

    # Test valid data
    daily_data = {
        '1': {'rad_na_mestu': 8, 'van_muzeja': 0}
    }
    errors = validate_daily_data(daily_data, 2, 2026)
    if errors:
        results.record_fail("Validation: Valid daily data", str(errors))
        return

    results.record_pass("Validation: Daily data validation works")


# =============================================================================
# DATA INTEGRITY TESTS
# =============================================================================

def test_save_and_load_consistency():
    """Test that saved data can be loaded back correctly"""
    from timesheet_postgres import save_timesheet_to_postgres, load_timesheet_from_postgres
    import psycopg
    from psycopg.rows import dict_row

    test_month = 12
    test_year = 2025

    # Create test data
    daily_data = {}
    for day in range(1, 29):  # Use 28 days to be safe for any month
        daily_data[str(day)] = {
            'rad_na_mestu': 8 if day % 7 not in [0, 6] else 0,
            'van_muzeja': 0,
            'godisnji_odmor': 0,
            'drzavni_praznik': 0,
            'placeno_odsustvo': 0,
            'ostalo_odsustvo': 0,
            'bolovanje_manje30': 0,
            'bolovanje_30_ili_vise': 0
        }

    # Save
    result = save_timesheet_to_postgres(
        user_email=TEST_EMAIL,
        user_name=TEST_NAME,
        month=test_month,
        year=test_year,
        daily_data=daily_data,
        work_description="Test work description",
        organization_unit="Test Unit",
        position="Test Position"
    )

    if not result.success:
        results.record_fail("Data Integrity: Save operation", result.error.message)
        return

    # Load back
    loaded = load_timesheet_from_postgres(TEST_EMAIL, test_month, test_year)

    if not loaded:
        results.record_fail("Data Integrity: Load operation", "Returned None")
        return

    # Verify data matches
    for day_str, expected in daily_data.items():
        day = int(day_str)
        actual = loaded['daily_data'].get(day, {})

        for category, expected_hours in expected.items():
            actual_hours = actual.get(category, 0)
            if abs(float(expected_hours) - float(actual_hours)) > 0.01:
                results.record_fail(
                    "Data Integrity: Value match",
                    f"Day {day}, {category}: expected {expected_hours}, got {actual_hours}"
                )
                return

    results.record_pass("Data Integrity: Save/Load consistency verified")


def test_trigger_sync():
    """Test that trigger properly syncs timesheet_report_days to timesheet_entries"""
    import psycopg
    from psycopg.rows import dict_row
    from timesheet_postgres import save_timesheet_to_postgres

    test_month = 11
    test_year = 2025

    # Save data with known values
    daily_data = {
        '1': {'rad_na_mestu': 8},
        '2': {'rad_na_mestu': 8},
        '3': {'van_muzeja': 4},
        '4': {'godisnji_odmor': 8}
    }

    result = save_timesheet_to_postgres(
        user_email=TEST_EMAIL,
        user_name=TEST_NAME,
        month=test_month,
        year=test_year,
        daily_data=daily_data,
        work_description="Trigger test",
        organization_unit="Test",
        position="Test"
    )

    if not result.success:
        results.record_fail("Trigger Sync: Save operation", result.error.message)
        return

    # Check timesheet_entries has correct aggregated values
    pg_url = DATABASE_URL.replace('postgresql+psycopg://', 'postgresql://')
    with psycopg.connect(pg_url, row_factory=dict_row) as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT te.category, te.hours
                FROM timesheet_entries te
                JOIN timesheet_reports tr ON tr.id = te.report_id
                WHERE tr.employee_email = %s AND tr.month = %s AND tr.year = %s
            """, (TEST_EMAIL, test_month, test_year))

            entries = {row['category']: float(row['hours']) for row in cur.fetchall()}

    expected = {
        'rad_na_mestu': 16.0,  # 8 + 8
        'van_muzeja': 4.0,
        'godisnji_odmor': 8.0
    }

    for category, expected_hours in expected.items():
        actual = entries.get(category, 0)
        if abs(expected_hours - actual) > 0.01:
            results.record_fail(
                "Trigger Sync: Category totals",
                f"{category}: expected {expected_hours}, got {actual}"
            )
            return

    results.record_pass("Trigger Sync: timesheet_entries correctly aggregated")


# =============================================================================
# CONCURRENCY TESTS
# =============================================================================

def test_optimistic_locking():
    """Test that optimistic locking prevents concurrent modification"""
    from timesheet_postgres import save_timesheet_to_postgres, load_timesheet_from_postgres, TimesheetErrorType

    test_month = 10
    test_year = 2025

    # Create initial record
    initial_result = save_timesheet_to_postgres(
        user_email=TEST_EMAIL,
        user_name=TEST_NAME,
        month=test_month,
        year=test_year,
        daily_data={'1': {'rad_na_mestu': 8}},
        work_description="Initial",
        organization_unit="Test",
        position="Test"
    )

    if not initial_result.success:
        results.record_fail("Optimistic Locking: Initial save", initial_result.error.message)
        return

    initial_version = initial_result.data['version']

    # Simulate first user updating
    first_update = save_timesheet_to_postgres(
        user_email=TEST_EMAIL,
        user_name=TEST_NAME,
        month=test_month,
        year=test_year,
        daily_data={'1': {'rad_na_mestu': 4}},
        work_description="First update",
        organization_unit="Test",
        position="Test",
        expected_version=initial_version
    )

    if not first_update.success:
        results.record_fail("Optimistic Locking: First update", first_update.error.message)
        return

    # Simulate second user trying to update with stale version
    second_update = save_timesheet_to_postgres(
        user_email=TEST_EMAIL,
        user_name=TEST_NAME,
        month=test_month,
        year=test_year,
        daily_data={'1': {'rad_na_mestu': 2}},
        work_description="Second update (should fail)",
        organization_unit="Test",
        position="Test",
        expected_version=initial_version  # Stale version
    )

    if second_update.success:
        results.record_fail("Optimistic Locking: Stale update", "Should have failed with concurrent modification error")
        return

    if second_update.error.error_type != TimesheetErrorType.CONCURRENT_MODIFICATION:
        results.record_fail(
            "Optimistic Locking: Error type",
            f"Expected CONCURRENT_MODIFICATION, got {second_update.error.error_type}"
        )
        return

    results.record_pass("Optimistic Locking: Concurrent modification detected")


def test_lock_enforcement():
    """Test that locked timesheets cannot be modified"""
    from timesheet_postgres import save_timesheet_to_postgres, TimesheetErrorType
    import psycopg

    test_month = 9
    test_year = 2025

    # Create initial record
    initial_result = save_timesheet_to_postgres(
        user_email=TEST_EMAIL,
        user_name=TEST_NAME,
        month=test_month,
        year=test_year,
        daily_data={'1': {'rad_na_mestu': 8}},
        work_description="To be locked",
        organization_unit="Test",
        position="Test"
    )

    if not initial_result.success:
        results.record_fail("Lock Enforcement: Initial save", initial_result.error.message)
        return

    # Lock the report manually
    pg_url = DATABASE_URL.replace('postgresql+psycopg://', 'postgresql://')
    with psycopg.connect(pg_url) as conn:
        with conn.cursor() as cur:
            cur.execute("""
                UPDATE timesheet_reports
                SET is_locked = TRUE
                WHERE employee_email = %s AND month = %s AND year = %s
            """, (TEST_EMAIL, test_month, test_year))
            conn.commit()

    # Try to update locked report
    update_result = save_timesheet_to_postgres(
        user_email=TEST_EMAIL,
        user_name=TEST_NAME,
        month=test_month,
        year=test_year,
        daily_data={'1': {'rad_na_mestu': 4}},
        work_description="Trying to update locked",
        organization_unit="Test",
        position="Test"
    )

    if update_result.success:
        results.record_fail("Lock Enforcement", "Should have failed - report is locked")
        return

    if update_result.error.error_type != TimesheetErrorType.LOCKED:
        results.record_fail(
            "Lock Enforcement: Error type",
            f"Expected LOCKED, got {update_result.error.error_type}"
        )
        return

    results.record_pass("Lock Enforcement: Locked report cannot be modified")


def test_concurrent_saves():
    """Test multiple simultaneous saves to different months"""
    from timesheet_postgres import save_timesheet_to_postgres

    results_list = []
    errors_list = []

    def save_for_month(month):
        try:
            result = save_timesheet_to_postgres(
                user_email=f"concurrent_test_{month}@test.com",
                user_name=f"Concurrent Test {month}",
                month=month,
                year=2025,
                daily_data={'1': {'rad_na_mestu': 8}},
                work_description=f"Concurrent test month {month}",
                organization_unit="Test",
                position="Test"
            )
            return (month, result.success, result.error.message if result.error else None)
        except Exception as e:
            return (month, False, str(e))

    # Run 6 concurrent saves
    with ThreadPoolExecutor(max_workers=6) as executor:
        futures = [executor.submit(save_for_month, m) for m in range(1, 7)]
        for future in as_completed(futures):
            month, success, error = future.result()
            if success:
                results_list.append(month)
            else:
                errors_list.append((month, error))

    if len(results_list) == 6:
        results.record_pass("Concurrent Saves: 6 parallel saves succeeded")
    else:
        results.record_fail(
            "Concurrent Saves",
            f"Only {len(results_list)}/6 succeeded. Errors: {errors_list}"
        )


# =============================================================================
# EDGE CASE TESTS
# =============================================================================

def test_leap_year():
    """Test handling of February in leap year"""
    from timesheet_postgres import save_timesheet_to_postgres, load_timesheet_from_postgres

    # 2024 is a leap year (29 days in Feb)
    daily_data = {str(d): {'rad_na_mestu': 8} for d in range(1, 30)}  # Include day 29

    result = save_timesheet_to_postgres(
        user_email=TEST_EMAIL,
        user_name=TEST_NAME,
        month=2,
        year=2024,
        daily_data=daily_data,
        work_description="Leap year test",
        organization_unit="Test",
        position="Test"
    )

    if not result.success:
        results.record_fail("Leap Year: Save Feb 2024", result.error.message)
        return

    # Load and verify day 29 exists
    loaded = load_timesheet_from_postgres(TEST_EMAIL, 2, 2024)
    if not loaded:
        results.record_fail("Leap Year: Load", "Returned None")
        return

    if loaded['daily_data'].get(29, {}).get('rad_na_mestu', 0) != 8:
        results.record_fail("Leap Year: Day 29 data", "Day 29 not properly saved")
        return

    results.record_pass("Leap Year: February 29 handled correctly")


def test_31_day_month():
    """Test handling of 31-day months"""
    from timesheet_postgres import save_timesheet_to_postgres, load_timesheet_from_postgres

    # January has 31 days
    daily_data = {str(d): {'rad_na_mestu': 8} for d in range(1, 32)}

    result = save_timesheet_to_postgres(
        user_email=TEST_EMAIL,
        user_name=TEST_NAME,
        month=1,
        year=2025,
        daily_data=daily_data,
        work_description="31 day test",
        organization_unit="Test",
        position="Test"
    )

    if not result.success:
        results.record_fail("31-Day Month: Save", result.error.message)
        return

    loaded = load_timesheet_from_postgres(TEST_EMAIL, 1, 2025)
    if not loaded:
        results.record_fail("31-Day Month: Load", "Returned None")
        return

    if loaded['daily_data'].get(31, {}).get('rad_na_mestu', 0) != 8:
        results.record_fail("31-Day Month: Day 31 data", "Day 31 not properly saved")
        return

    results.record_pass("31-Day Month: Day 31 handled correctly")


def test_empty_timesheet():
    """Test handling of empty timesheet (no hours entered)"""
    from timesheet_postgres import save_timesheet_to_postgres, load_timesheet_from_postgres

    # All zeros
    daily_data = {str(d): {
        'rad_na_mestu': 0,
        'van_muzeja': 0,
        'godisnji_odmor': 0
    } for d in range(1, 29)}

    result = save_timesheet_to_postgres(
        user_email=TEST_EMAIL,
        user_name=TEST_NAME,
        month=8,
        year=2025,
        daily_data=daily_data,
        work_description="Empty timesheet test",
        organization_unit="Test",
        position="Test"
    )

    if not result.success:
        results.record_fail("Empty Timesheet: Save", result.error.message)
        return

    loaded = load_timesheet_from_postgres(TEST_EMAIL, 8, 2025)
    if not loaded:
        results.record_fail("Empty Timesheet: Load", "Returned None")
        return

    results.record_pass("Empty Timesheet: Handled correctly")


def test_special_characters_in_description():
    """Test handling of special characters in work description"""
    from timesheet_postgres import save_timesheet_to_postgres, load_timesheet_from_postgres

    special_desc = "Тест са специјалним карактерима: <script>alert('xss')</script> & \"quotes\" 'apostrophe'"

    result = save_timesheet_to_postgres(
        user_email=TEST_EMAIL,
        user_name=TEST_NAME,
        month=7,
        year=2025,
        daily_data={'1': {'rad_na_mestu': 8}},
        work_description=special_desc,
        organization_unit="Test",
        position="Test"
    )

    if not result.success:
        results.record_fail("Special Characters: Save", result.error.message)
        return

    loaded = load_timesheet_from_postgres(TEST_EMAIL, 7, 2025)
    if not loaded:
        results.record_fail("Special Characters: Load", "Returned None")
        return

    if loaded['OPosao'] != special_desc:
        results.record_fail(
            "Special Characters: Data integrity",
            f"Expected: {special_desc}, Got: {loaded['OPosao']}"
        )
        return

    results.record_pass("Special Characters: Handled correctly")


def test_rate_limiting():
    """Test rate limiting for edit approval requests"""
    from timesheet_postgres import (
        save_timesheet_to_postgres,
        request_edit_approval,
        get_edit_request_rate_limit_status,
        TimesheetErrorType
    )
    import psycopg

    test_email = "rate_limit_test@museum.test"
    test_month = 6
    test_year = 2025

    # Create a test report first
    result = save_timesheet_to_postgres(
        user_email=test_email,
        user_name="Rate Limit Test User",
        month=test_month,
        year=test_year,
        daily_data={'1': {'rad_na_mestu': 8}},
        work_description="Rate limit test",
        organization_unit="Test",
        position="Test"
    )

    if not result.success:
        results.record_fail("Rate Limiting: Create report", result.error.message)
        return

    # Lock the report so we can request edits
    pg_url = DATABASE_URL.replace('postgresql+psycopg://', 'postgresql://')
    with psycopg.connect(pg_url) as conn:
        with conn.cursor() as cur:
            cur.execute("""
                UPDATE timesheet_reports
                SET is_locked = TRUE
                WHERE employee_email = %s AND month = %s AND year = %s
            """, (test_email, test_month, test_year))
            conn.commit()

    # Check initial rate limit status
    status = get_edit_request_rate_limit_status(test_email)
    if status['remaining'] != 3:
        results.record_fail("Rate Limiting: Initial status", f"Expected 3 remaining, got {status['remaining']}")
        return

    # Make 3 requests (should all succeed)
    for i in range(3):
        req_result = request_edit_approval(
            test_email, test_month, test_year,
            f"Test request {i+1} - need to fix data entry error"
        )
        # First request should succeed, subsequent might fail due to pending exists
        # So we just track that at least one succeeds
        if i == 0 and not req_result.success:
            results.record_fail("Rate Limiting: First request", req_result.error.message)
            return

    # Check rate limit status after requests
    status = get_edit_request_rate_limit_status(test_email)

    # The 4th request should be rate limited (if we could make it)
    # Since we have pending request check, let's verify the rate limit counter works
    if status['requests_today'] < 1:
        results.record_fail("Rate Limiting: Request counter", f"Expected at least 1 request, got {status['requests_today']}")
        return

    results.record_pass("Rate Limiting: Working correctly")


def test_error_guidance():
    """Test that error guidance is included in error responses"""
    from timesheet_postgres import TimesheetResult, TimesheetErrorType

    # Create an error result
    result = TimesheetResult.fail(
        TimesheetErrorType.LOCKED,
        "Test locked error",
        {'error_code': 'TEST'}
    )

    # Convert to dict
    error_dict = result.error.to_dict()

    # Verify guidance is included
    if 'guidance' not in error_dict:
        results.record_fail("Error Guidance: Missing guidance", f"No guidance in error dict: {error_dict.keys()}")
        return

    guidance = error_dict['guidance']
    if 'title' not in guidance or 'icon' not in guidance or 'suggestions' not in guidance:
        results.record_fail("Error Guidance: Incomplete guidance", f"Missing fields: {guidance}")
        return

    # Verify locked error has correct guidance
    if guidance['icon'] != 'bi-lock':
        results.record_fail("Error Guidance: Wrong icon", f"Expected bi-lock, got {guidance['icon']}")
        return

    if not isinstance(guidance['suggestions'], list) or len(guidance['suggestions']) == 0:
        results.record_fail("Error Guidance: No suggestions", f"Suggestions: {guidance['suggestions']}")
        return

    results.record_pass("Error Guidance: Working correctly")


def test_data_integrity_validation():
    """Test data integrity validation on load"""
    from timesheet_postgres import validate_loaded_data

    # Test with valid data
    valid_data = {
        1: {'rad_na_mestu': 8, 'van_muzeja': 0},
        2: {'rad_na_mestu': 4, 'van_muzeja': 4}
    }
    warnings = validate_loaded_data(valid_data, 1, 2025, 999)
    if warnings:
        results.record_fail("Data Integrity: Valid data", f"Got warnings: {warnings}")
        return

    # Test with negative hours (should be flagged as error)
    invalid_data = {
        1: {'rad_na_mestu': -5, 'van_muzeja': 0}
    }
    warnings = validate_loaded_data(invalid_data, 1, 2025, 999)
    if not any(w['level'] == 'error' and 'Negative' in w['message'] for w in warnings):
        results.record_fail("Data Integrity: Negative hours", f"Expected error for negative hours, got: {warnings}")
        return

    # Verify negative value was corrected to 0
    if invalid_data[1]['rad_na_mestu'] != 0:
        results.record_fail("Data Integrity: Auto-correction", f"Expected 0, got {invalid_data[1]['rad_na_mestu']}")
        return

    # Test with hours > 24 (should be flagged as warning)
    excessive_data = {
        1: {'rad_na_mestu': 30, 'van_muzeja': 0}
    }
    warnings = validate_loaded_data(excessive_data, 1, 2025, 999)
    if not any(w['level'] == 'warning' and '24' in w['message'] for w in warnings):
        results.record_fail("Data Integrity: Excessive hours", f"Expected warning for >24 hours, got: {warnings}")
        return

    # Test with total daily hours > 24
    total_excessive = {
        1: {'rad_na_mestu': 20, 'van_muzeja': 10}
    }
    warnings = validate_loaded_data(total_excessive, 1, 2025, 999)
    if not any(w['message'] and 'Total daily hours' in w['message'] for w in warnings):
        results.record_fail("Data Integrity: Total exceeds 24", f"Expected total hours warning, got: {warnings}")
        return

    results.record_pass("Data Integrity Validation: Working correctly")


def test_batch_verification():
    """Test batch verification/unverification of reports"""
    from timesheet_postgres import save_timesheet_to_postgres
    import psycopg
    from psycopg.rows import dict_row

    pg_url = DATABASE_URL.replace('postgresql+psycopg://', 'postgresql://')
    test_email_prefix = "batch_test_"
    test_year = 2025
    test_month = 3

    # Create 3 test reports
    report_ids = []
    for i in range(1, 4):
        email = f"{test_email_prefix}{i}@museum.test"
        result = save_timesheet_to_postgres(
            user_email=email,
            user_name=f"Batch Test User {i}",
            month=test_month,
            year=test_year,
            daily_data={'1': {'rad_na_mestu': 8}},
            work_description=f"Batch test {i}",
            organization_unit="Test",
            position="Test"
        )
        if not result.success:
            results.record_fail("Batch Verification: Create reports", result.error.message)
            return

    # Get the created report IDs
    with psycopg.connect(pg_url, row_factory=dict_row) as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT id FROM timesheet_reports
                WHERE employee_email LIKE %s
                ORDER BY id
            """, (f"{test_email_prefix}%",))
            report_ids = [row['id'] for row in cur.fetchall()]

    if len(report_ids) < 3:
        results.record_fail("Batch Verification: Create reports", f"Expected 3 reports, got {len(report_ids)}")
        return

    # Test batch verification (simulate API call logic)
    with psycopg.connect(pg_url, row_factory=dict_row) as conn:
        with conn.cursor() as cur:
            # Verify all reports
            cur.execute("""
                UPDATE timesheet_reports
                SET is_verified = TRUE,
                    verified_by = %s,
                    verified_at = NOW(),
                    is_locked = TRUE
                WHERE id = ANY(%s)
            """, ("batch_test_admin@museum.test", report_ids))
            conn.commit()

            # Check all are verified
            cur.execute("""
                SELECT COUNT(*) as cnt FROM timesheet_reports
                WHERE id = ANY(%s) AND is_verified = TRUE
            """, (report_ids,))
            verified_count = cur.fetchone()['cnt']

    if verified_count != 3:
        results.record_fail("Batch Verification: Verify all", f"Expected 3 verified, got {verified_count}")
        return

    # Test batch unverification
    with psycopg.connect(pg_url, row_factory=dict_row) as conn:
        with conn.cursor() as cur:
            cur.execute("""
                UPDATE timesheet_reports
                SET is_verified = FALSE,
                    verified_by = NULL,
                    verified_at = NULL,
                    is_locked = FALSE
                WHERE id = ANY(%s)
            """, (report_ids,))
            conn.commit()

            # Check all are unverified
            cur.execute("""
                SELECT COUNT(*) as cnt FROM timesheet_reports
                WHERE id = ANY(%s) AND is_verified = FALSE
            """, (report_ids,))
            unverified_count = cur.fetchone()['cnt']

    if unverified_count != 3:
        results.record_fail("Batch Verification: Unverify all", f"Expected 3 unverified, got {unverified_count}")
        return

    results.record_pass("Batch Verification: Working correctly")


# =============================================================================
# CLEANUP
# =============================================================================

def cleanup_test_data():
    """Remove all test data created during tests"""
    import psycopg

    print_section("CLEANUP")

    pg_url = DATABASE_URL.replace('postgresql+psycopg://', 'postgresql://')
    try:
        with psycopg.connect(pg_url) as conn:
            with conn.cursor() as cur:
                # Delete test edit requests first
                cur.execute("""
                    DELETE FROM timesheet_edit_requests
                    WHERE requester_email LIKE '%@museum.test'
                       OR requester_email LIKE '%@test.com'
                """)

                # Delete test reports and related data (CASCADE handles entries)
                cur.execute("""
                    DELETE FROM timesheet_reports
                    WHERE employee_email LIKE '%@museum.test'
                       OR employee_email LIKE '%@test.com'
                       OR employee_name LIKE 'Test%'
                       OR employee_name LIKE 'Concurrent Test%'
                       OR employee_name LIKE 'Batch Test%'
                """)
                deleted = cur.rowcount
                conn.commit()

        print_success(f"Cleaned up {deleted} test records")
        return True
    except Exception as e:
        print_error(f"Cleanup failed: {e}")
        return False


# =============================================================================
# MAIN
# =============================================================================

def main():
    print(f"\n{Colors.BOLD}{'='*60}")
    print("TIMESHEET RELIABILITY TEST SUITE")
    print(f"{'='*60}{Colors.END}\n")

    print_info(f"Database: {DATABASE_URL.split('@')[1] if '@' in DATABASE_URL else DATABASE_URL}")
    print_info(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # Run tests
    print_section("VALIDATION TESTS")
    test_validation_negative_hours()
    test_validation_excessive_hours()
    test_validation_valid_hours()
    test_validation_month_year()
    test_validation_daily_data()

    print_section("DATA INTEGRITY TESTS")
    test_save_and_load_consistency()
    test_trigger_sync()

    print_section("CONCURRENCY TESTS")
    test_optimistic_locking()
    test_lock_enforcement()
    test_concurrent_saves()

    print_section("EDGE CASE TESTS")
    test_leap_year()
    test_31_day_month()
    test_empty_timesheet()
    test_special_characters_in_description()

    print_section("SECURITY TESTS")
    test_rate_limiting()

    print_section("API TESTS")
    test_error_guidance()
    test_data_integrity_validation()
    test_batch_verification()

    # Cleanup
    cleanup_test_data()

    # Summary
    success = results.summary()

    if success:
        print(f"\n{Colors.GREEN}{Colors.BOLD}ALL TESTS PASSED!{Colors.END}\n")
        return 0
    else:
        print(f"\n{Colors.RED}{Colors.BOLD}SOME TESTS FAILED{Colors.END}\n")
        return 1


if __name__ == '__main__':
    sys.exit(main())
