"""
Phase C LOW-severity hardening tests for timesheet_postgres.py

Finding: Sick-leave alias keys (bolovanje_manje_30 / bolovanje_vece_30 — the
underscore-before-number names the frontend actually submits) bypassed hour
validation in save_timesheet_to_postgres because they were missing from
VALID_CATEGORIES, so validate_daily_data skipped them silently while the save
path still read and INSERTed them.
"""

import os

os.environ.setdefault('FLASK_ENV', 'testing')
os.environ.setdefault('SECRET_KEY', 'test-secret')
os.environ.setdefault('REDIS_URL', '')
os.environ.setdefault('SESSION_TYPE', 'filesystem')
os.environ.setdefault('SESSION_FILE_DIR', '/tmp/museum-test-c-timesheet-postgres')

import timesheet_postgres as tp


YEAR = 2026
MONTH = 5


def test_sick_leave_alias_negative_rejected():
    """A negative value under the frontend alias bolovanje_manje_30 must be
    flagged by validate_daily_data (previously skipped silently)."""
    daily_data = {'10': {'bolovanje_manje_30': -5}}
    errors = tp.validate_daily_data(daily_data, MONTH, YEAR)
    assert any('bolovanje_manje_30' in e for e in errors), errors


def test_sick_leave_alias_over_24_rejected():
    """A >24 value under the frontend alias bolovanje_vece_30 must be flagged."""
    daily_data = {'12': {'bolovanje_vece_30': 99}}
    errors = tp.validate_daily_data(daily_data, MONTH, YEAR)
    assert any('bolovanje_vece_30' in e for e in errors), errors


def test_sick_leave_alias_non_numeric_rejected():
    """A non-numeric value under an alias key must be flagged by validation
    rather than escaping to the save layer and raising an uncaught ValueError."""
    daily_data = {'8': {'bolovanje_manje_30': 'abc'}}
    errors = tp.validate_daily_data(daily_data, MONTH, YEAR)
    assert any('bolovanje_manje_30' in e for e in errors), errors


def test_sick_leave_alias_valid_value_accepted():
    """A valid in-range value under an alias key must NOT produce an error."""
    daily_data = {'8': {'bolovanje_manje_30': 8, 'bolovanje_vece_30': 0}}
    errors = tp.validate_daily_data(daily_data, MONTH, YEAR)
    assert errors == [], errors


def test_canonical_sick_leave_keys_still_validated():
    """The canonical names must keep being validated (no regression)."""
    daily_data = {
        '8': {'bolovanje_manje30': -1},
        '9': {'bolovanje_30_ili_vise': 30},
    }
    errors = tp.validate_daily_data(daily_data, MONTH, YEAR)
    assert any('bolovanje_manje30' in e for e in errors), errors
    assert any('bolovanje_30_ili_vise' in e for e in errors), errors
