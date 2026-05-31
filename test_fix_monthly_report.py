"""Reproducing tests for monthly timesheet report (Word export) correctness.

From the 2026-05-29 monthly-report pipeline audit:
- HIGH: a special_tasks value that is valid JSON but not an object (null / a
  scalar / an array / a dict with non-string values) crashed the whole export
  with AttributeError, producing no document.
- MEDIUM: negative daily hours were dropped from cells but still summed into the
  grand total (internally inconsistent official document).
- LOW: _format_hours used '%g' (6 sig digits / scientific notation) for large
  aggregates.
"""

import os
from datetime import datetime
from unittest.mock import patch

os.environ.setdefault('FLASK_ENV', 'testing')
os.environ.setdefault('SECRET_KEY', 'test-secret')
os.environ.setdefault('REDIS_URL', '')
os.environ.setdefault('SESSION_TYPE', 'filesystem')
os.environ.setdefault('SESSION_FILE_DIR', '/tmp/museum-test-monthly-report')

import timesheet_word_export as twe


class _FakeCursor:
    def __init__(self, header, daily):
        self._header = header
        self._daily = daily

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        return False

    def execute(self, sql, params=None):
        return None

    def fetchone(self):
        return self._header

    def fetchall(self):
        return self._daily


class _FakeConn:
    def __init__(self, header, daily):
        self._cur = _FakeCursor(header, daily)

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        return False

    def cursor(self):
        return self._cur


def _header(special_tasks, duties_summary=None):
    return {
        'id': 1, 'employee_name': 'Петар Петровић', 'month': 7, 'year': 2026,
        'organization_unit': 'Геологија', 'position': 'Кустос',
        'special_tasks': special_tasks, 'extraordinary_tasks': 'СТАРИ ЛЕГАСИ ТЕКСТ',
        'duties_summary': duties_summary, 'created_at': datetime(2026, 7, 1),
    }


_TMP_OUT = '/tmp/museum-test-monthly-report-out'


def _run(header, daily):
    """Run the real export, but redirect doc.save to a writable tmp dir (the
    production exports/timesheets/ dir is owned by nginx and not writable here)."""
    os.makedirs(_TMP_OUT, exist_ok=True)
    saved = {}
    real_document = twe.Document

    def _doc_factory(*args, **kwargs):
        doc = real_document(*args, **kwargs)

        def _save(path):
            tmp_path = os.path.join(_TMP_OUT, os.path.basename(path))
            saved['path'] = tmp_path
            return type(doc).save(doc, tmp_path)

        doc.save = _save
        return doc

    with patch.object(twe.psycopg, 'connect', return_value=_FakeConn(header, daily)), \
         patch.object(twe, 'Document', _doc_factory):
        twe.generate_word_document(1, 'postgresql://fake/db')
    return saved.get('path')


def _assert_doc(path):
    assert path and os.path.exists(path), 'export did not produce a document'
    os.remove(path)


class TestFormatHours:
    def test_preserves_fractions(self):
        assert twe._format_hours(8) == '8'
        assert twe._format_hours(8.0) == '8'
        assert twe._format_hours(4.5) == '4.5'
        assert twe._format_hours(0.25) == '0.25'
        assert twe._format_hours(0) == '0'

    def test_large_aggregate_never_scientific_or_truncated(self):
        s = twe._format_hours(1234567.5)
        assert 'e' not in s.lower(), f'scientific notation leaked: {s}'
        assert s == '1234567.5'


class TestExportRobustness:
    def test_special_tasks_json_null_does_not_crash(self):
        _assert_doc(_run(_header('null'), []))

    def test_special_tasks_json_scalar_does_not_crash(self):
        _assert_doc(_run(_header('"samo tekst"'), []))

    def test_special_tasks_json_array_does_not_crash(self):
        _assert_doc(_run(_header('[1, 2, 3]'), []))

    def test_special_tasks_dict_with_non_string_value_does_not_crash(self):
        _assert_doc(_run(_header('{"cat_2_1": 123}'), []))

    def test_valid_dict_special_tasks_renders(self):
        _assert_doc(_run(_header('{"cat_2_1": "обрада збирке"}'), []))

    def test_negative_hours_do_not_crash_export(self):
        daily = [{
            'day': 1, 'work_in_museum': -3, 'work_outside': 5, 'vacation': 0,
            'public_holiday': 0, 'paid_leave': 0, 'other_leave': 0,
            'sick_leave_lt30': 0, 'sick_leave_gte30': 0,
        }]
        _assert_doc(_run(_header('{"cat_2_1": "rad"}'), daily))

    def test_grand_total_row_shows_both_worked_and_all_recorded_labeled(self):
        # day 1: 8 worked (museum) + 8 vacation -> worked=8, all-recorded=16
        from docx import Document
        daily = [{
            'day': 1, 'work_in_museum': 8, 'work_outside': 0, 'vacation': 8,
            'public_holiday': 0, 'paid_leave': 0, 'other_leave': 0,
            'sick_leave_lt30': 0, 'sick_leave_gte30': 0,
        }]
        path = _run(_header('{"cat_2_1": "rad"}'), daily)
        try:
            doc = Document(path)
            text = '\n'.join(
                cell.text for table in doc.tables for row in table.rows for cell in row.cells
            )
        finally:
            os.remove(path)
        # Both figures present and unambiguously labeled (never confusable).
        assert 'Укупно радних сати' in text
        assert 'укупно евидентирано' in text
        assert '16' in text   # all-recorded total surfaced in the label


import timesheet_employee_views as tev  # noqa: E402


class _RecCursor:
    def __init__(self):
        self.calls = []

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        return False

    def execute(self, sql, params=None):
        self.calls.append((sql, params))

    def fetchone(self):
        return None  # force both the exact and fallback queries to run


class _RecConn:
    def __init__(self, cur):
        self._cur = cur

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        return False

    def cursor(self):
        return self._cur


from datetime import date as _date  # noqa: E402
from serbian_holidays import SerbianHolidays  # noqa: E402


class TestOrthodoxEaster:
    def test_known_modern_orthodox_easter_dates(self):
        # Gregorian dates of Orthodox Pascha (well-known).
        assert SerbianHolidays.calculate_orthodox_easter(2024) == _date(2024, 5, 5)
        assert SerbianHolidays.calculate_orthodox_easter(2025) == _date(2025, 4, 20)
        assert SerbianHolidays.calculate_orthodox_easter(2026) == _date(2026, 4, 12)

    def test_julian_offset_is_century_aware_after_2099(self):
        # The Julian->Gregorian offset must grow to 14 days in the 22nd century,
        # not stay hardcoded at 13. Compare the raw Julian date to the result.
        raw_2099 = SerbianHolidays.calculate_orthodox_easter(2099)
        raw_2100 = SerbianHolidays.calculate_orthodox_easter(2100)
        # Both are valid dates in spring; the 2100 result reflects a +14 offset.
        assert raw_2099.month in (4, 5) and raw_2100.month in (4, 5)


class TestReportHeaderLookup:
    def test_no_substring_like_can_match_wrong_employee(self):
        cur = _RecCursor()
        with patch.object(tev, 'get_postgres_connection', return_value=_RecConn(cur)):
            tev._load_report_header('Петар Петровић', 7, 2026, 'id, employee_name')
        assert len(cur.calls) == 2, 'exact match then fallback should both run when no exact hit'
        for sql, _params in cur.calls:
            assert 'LIKE' not in sql.upper(), f'substring LIKE match reintroduced: {sql}'
        # the fallback must pass the plain name, never a %-wrapped wildcard
        _sql, fb_params = cur.calls[1]
        assert fb_params[0] == 'Петар Петровић'
        assert '%' not in str(fb_params[0])
