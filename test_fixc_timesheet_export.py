import os
import sys
from contextlib import contextmanager
from unittest.mock import MagicMock, patch

os.environ.setdefault('FLASK_ENV', 'testing')
os.environ.setdefault('SECRET_KEY', 'test-secret')
os.environ.setdefault('REDIS_URL', '')
os.environ.setdefault('SESSION_TYPE', 'filesystem')
os.environ.setdefault('SESSION_FILE_DIR', '/tmp/museum-test-c-timesheet-export')

import pytest

import timesheet_word_export


def _make_header(employee_name):
    return {
        'id': 1,
        'employee_name': employee_name,
        'month': 5,
        'year': 2026,
        'organization_unit': None,
        'position': None,
        'special_tasks': None,
        'extraordinary_tasks': None,
        'duties_summary': None,
        'created_at': None,
    }


@contextmanager
def _fake_connect(header, daily_rows):
    """Build a fake psycopg connection whose cursor returns the given header/rows."""
    cur = MagicMock()
    cur.fetchone.return_value = header
    cur.fetchall.return_value = daily_rows

    @contextmanager
    def cursor_cm(*args, **kwargs):
        yield cur

    conn = MagicMock()
    conn.cursor.side_effect = cursor_cm

    @contextmanager
    def connect_cm(*args, **kwargs):
        yield conn

    yield connect_cm


def _run_with_header(tmp_path, header, daily_rows=None):
    daily_rows = daily_rows or []
    # Redirect the export directory (real one is owned by nginx, read-only here)
    # by making os.path.dirname(__file__) resolve to a writable temp dir.
    real_dirname = os.path.dirname

    def fake_dirname(path):
        if path == timesheet_word_export.__file__:
            return str(tmp_path)
        return real_dirname(path)

    with _fake_connect(header, daily_rows) as connect_cm:
        with patch.object(timesheet_word_export.psycopg, 'connect', connect_cm), \
                patch.object(timesheet_word_export.os.path, 'dirname', fake_dirname):
            return timesheet_word_export.generate_word_document(
                1, 'postgresql://user@localhost/db'
            )


@pytest.mark.skipif(not timesheet_word_export.DOCX_AVAILABLE, reason="python-docx not installed")
def test_export_with_null_employee_name_does_not_crash(tmp_path):
    """Finding 1: employee_name NULL must not raise AttributeError during export."""
    header = _make_header(None)
    output_path = _run_with_header(tmp_path, header)
    assert output_path
    assert os.path.exists(output_path)
    # Filename must be built without crashing even though name was None.
    assert output_path.endswith('.docx')
    os.remove(output_path)


@pytest.mark.skipif(not timesheet_word_export.DOCX_AVAILABLE, reason="python-docx not installed")
def test_export_with_single_word_name(tmp_path):
    """Single-word name path (len<=1) must still produce a valid document."""
    header = _make_header('Петар')
    output_path = _run_with_header(tmp_path, header)
    assert output_path
    assert os.path.exists(output_path)
    os.remove(output_path)


@pytest.mark.skipif(not timesheet_word_export.DOCX_AVAILABLE, reason="python-docx not installed")
def test_export_with_normal_name(tmp_path):
    """Normal two-word name keeps working (no regression)."""
    header = _make_header('Петар Петровић')
    output_path = _run_with_header(tmp_path, header)
    assert output_path
    assert os.path.exists(output_path)
    assert 'Петар_Петровић' in os.path.basename(output_path)
    os.remove(output_path)
