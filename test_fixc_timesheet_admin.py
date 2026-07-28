"""Reproducing/behavior tests for the timesheet-admin cluster (Phase C LOW).

Covers four confirmed low-severity hardening fixes in timesheet_admin_views.py:

1. Serbian-Cyrillic month names in the filter dropdown (_month_options) and the
   report detail view, instead of English calendar.month_name leaking into the
   otherwise Cyrillic UI.
2. The disapprove (un-verify) UPDATEs clear reviewed_at / reviewed_by_email so
   the persisted review metadata matches the SUBMITTED state.
3. Batch-approve de-duplicates report_ids so the skipped count is not inflated
   by duplicate ids in the request body.
4. api_admin_employee_analytics wraps each day-column in COALESCE inside the
   SUMs, so a single NULL column cannot silently drop a whole day's hours.
"""

import os

os.environ.setdefault('FLASK_ENV', 'testing')
os.environ.setdefault('SECRET_KEY', 'test-secret')
os.environ.setdefault('REDIS_URL', '')
os.environ.setdefault('SESSION_TYPE', 'filesystem')
os.environ.setdefault('SESSION_FILE_DIR', '/tmp/museum-test-c-timesheet-admin')
os.environ.setdefault('DATABASE_URL', 'postgresql://test:test@localhost:5432/test')

from contextlib import contextmanager
from unittest.mock import MagicMock, patch

import flask

import timesheet_admin_views as views
import timesheet_postgres as tp


SERBIAN_MONTHS = views.SERBIAN_MONTHS


def _fake_confirm_sig(report_id, verifier_email, slot, head_required,
                      administrative=False):
    """Stub confirm_timesheet_signature (real one uses its own DB connection)."""
    if administrative:
        # Административно одобрење → одмах APPROVED (ван двостепеног ланца).
        return tp.TimesheetResult.ok({'report_id': report_id, 'approved': True,
                                      'administrative': True})
    head_done = slot in ('head', 'both')
    director_done = slot in ('director', 'both')
    approved = director_done and (head_done or not head_required)
    return tp.TimesheetResult.ok({'report_id': report_id, 'approved': approved,
                                  'status': 'APPROVED' if approved else 'SUBMITTED'})


@contextmanager
def _request_context(query=''):
    app = flask.Flask(__name__)
    app.secret_key = 'test-secret'
    with app.test_request_context('/' + query):
        yield


class _RecordingCursor:
    """Cursor that records executed SQL and replays a queue of fetch results."""

    def __init__(self, fetchone_queue=None, fetchall_queue=None):
        self.executed = []
        self._fetchone = list(fetchone_queue or [])
        self._fetchall = list(fetchall_queue or [])
        self.rowcount = 1

    def execute(self, query, params=None):
        self.executed.append((query, params))

    def executemany(self, query, seq):
        self.executed.append((query, list(seq)))

    def fetchone(self):
        return self._fetchone.pop(0) if self._fetchone else None

    def fetchall(self):
        return self._fetchall.pop(0) if self._fetchall else []

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        return False


def _conn_for(cursor):
    conn = MagicMock()
    conn.cursor.return_value = cursor

    @contextmanager
    def _cm(*args, **kwargs):
        yield conn

    return _cm


# ---------------------------------------------------------------------------
# Finding 1: Serbian month names instead of English calendar.month_name
# ---------------------------------------------------------------------------

def test_month_options_are_serbian_cyrillic():
    options = views._month_options()
    assert [label for _, label in options] == SERBIAN_MONTHS
    # The first label must be the Cyrillic 'Јануар', never the English 'January'.
    assert options[0] == (1, 'Јануар')
    assert options[4] == (5, 'Мај')
    import calendar
    assert options[0][1] != calendar.month_name[1]


def test_report_detail_passes_serbian_month_name():
    captured = {}

    def fake_render(template, **context):
        captured.update(context)
        return ''

    repo = MagicMock()
    repo.available = True
    repo.get_report.return_value = {'header': {'month': 5, 'year': 2026}}
    repo_cls = MagicMock()
    repo_cls.CATEGORY_LABELS = {}

    session_stub = {'user_role': 'admin'}

    original_render = views.render_template
    views.render_template = fake_render
    try:
        with _request_context():
            with patch.object(views, 'session', session_stub):
                views.render_admin_timesheet_report_detail(7, repo, repo_cls)
    finally:
        views.render_template = original_render

    assert captured['month_name'] == 'Мај'
    import calendar
    assert captured['month_name'] != calendar.month_name[5]


# ---------------------------------------------------------------------------
# Finding 2: disapprove clears reviewed_at / reviewed_by_email
# ---------------------------------------------------------------------------

def test_disapprove_clears_review_metadata():
    cursor = _RecordingCursor(
        fetchone_queue=[
            {
                'id': 3,
                'employee_name': 'Петар',
                'month': 5,
                'year': 2026,
                'status': 'APPROVED',
                'employee_email': 'petar@example.com',
                'employee_department': 'Геологија',
            }
        ],
        fetchall_queue=[[]],  # _get_department_heads
    )
    repo = MagicMock()
    repo.available = True
    session_stub = {'user_role': 'admin', 'user_email': 'admin@example.com'}

    with _request_context():
        with patch.object(views, 'get_postgres_connection', _conn_for(cursor)):
            with patch.object(views, 'session', session_stub):
                with patch.object(
                    views.request, 'get_json', lambda silent=False: {'approve': False}
                ):
                    response = views.api_admin_approve_timesheet_report(3, repo)

    payload = response.get_json() if hasattr(response, 'get_json') else response
    assert payload['success'] is True

    update_sql = next(
        sql for sql, _ in cursor.executed
        if 'UPDATE timesheet_reports' in sql and "status = 'SUBMITTED'" in sql
    )
    assert 'reviewed_at = NULL' in update_sql
    assert 'reviewed_by_email = NULL' in update_sql


def test_batch_disapprove_clears_review_metadata():
    cursor = _RecordingCursor(
        fetchall_queue=[
            [
                {
                    'id': 11,
                    'employee_name': 'Ана',
                    'month': 5,
                    'year': 2026,
                    'status': 'APPROVED',
                    'employee_email': 'ana@example.com',
                    'employee_department': 'Геологија',
                }
            ],
        ],
    )
    repo = MagicMock()
    repo.available = True
    session_stub = {'user_role': 'admin', 'user_email': 'admin@example.com'}

    with _request_context():
        with patch.object(views, 'get_postgres_connection', _conn_for(cursor)):
            with patch.object(views, 'session', session_stub):
                with patch.object(
                    views.request,
                    'get_json',
                    lambda silent=False: {'report_ids': [11], 'approve': False},
                ):
                    response = views.api_admin_batch_approve_timesheet_reports(repo)

    payload = response.get_json() if hasattr(response, 'get_json') else response
    assert payload['success'] is True

    update_sql = next(
        sql for sql, _ in cursor.executed
        if 'UPDATE timesheet_reports' in sql and "status = 'SUBMITTED'" in sql
    )
    assert 'reviewed_at = NULL' in update_sql
    assert 'reviewed_by_email = NULL' in update_sql


# ---------------------------------------------------------------------------
# Finding 3: batch-approve de-duplicates report_ids -> correct skipped count
# ---------------------------------------------------------------------------

def test_batch_approve_dedup_reports_no_false_skip():
    # Report 5 is approvable; the request contains it twice. After dedup the
    # skipped count must be 0, not 1.
    cursor = _RecordingCursor(
        fetchall_queue=[
            [
                {
                    'id': 5,
                    'employee_name': 'Мика',
                    'month': 5,
                    'year': 2026,
                    'status': 'SUBMITTED',
                    'employee_email': 'mika@example.com',
                    'employee_department': 'Геологија',
                }
            ],
        ],
    )
    repo = MagicMock()
    repo.available = True
    session_stub = {'user_role': 'admin', 'user_email': 'admin@example.com'}

    with _request_context():
        with patch.object(views, 'get_postgres_connection', _conn_for(cursor)), \
                patch.object(views, 'session', session_stub), \
                patch.object(views, '_get_department_heads', return_value={}), \
                patch.object(tp, 'confirm_timesheet_signature',
                             side_effect=_fake_confirm_sig), \
                patch.object(
                    views.request,
                    'get_json',
                    lambda silent=False: {'report_ids': [5, 5], 'approve': True},
                ):
            response = views.api_admin_batch_approve_timesheet_reports(repo)

    payload = response.get_json() if hasattr(response, 'get_json') else response
    assert payload['success'] is True
    assert payload['processed'] == 1
    assert payload['skipped'] == 0


# ---------------------------------------------------------------------------
# Finding 4: per-column COALESCE inside analytics SUMs
# ---------------------------------------------------------------------------

def test_employee_analytics_sums_use_per_column_coalesce():
    cursor = _RecordingCursor(
        fetchone_queue=[
            {
                'total_reports': 1,
                'total_hours': 8,
                'work_in_museum': 8,
                'work_outside': 0,
                'leave_hours': 0,
            },
            {'months_count': 1},
            {
                'work_in_museum': 8,
                'work_outside': 0,
                'vacation': 0,
                'public_holiday': 0,
                'paid_leave': 0,
                'other_leave': 0,
                'sick_leave_lt30': 0,
                'sick_leave_gte30': 0,
            },
        ],
        fetchall_queue=[[]],  # monthly breakdown
    )
    repo = MagicMock()
    session_stub = {'user_role': 'admin'}

    with _request_context('?name=Мика'):
        with patch.object(views, 'get_postgres_connection', _conn_for(cursor)):
            with patch.object(views, 'session', session_stub):
                response = views.api_admin_employee_analytics()

    payload = response.get_json() if hasattr(response, 'get_json') else response
    assert payload['success'] is True

    summary_sql = cursor.executed[0][0]
    monthly_sql = cursor.executed[2][0]
    for col in (
        'd.work_in_museum',
        'd.work_outside',
        'd.vacation',
        'd.public_holiday',
        'd.paid_leave',
        'd.other_leave',
        'd.sick_leave_lt30',
        'd.sick_leave_gte30',
    ):
        assert f'COALESCE({col}, 0)' in summary_sql, col
        assert f'COALESCE({col}, 0)' in monthly_sql, col
    # The bare un-coalesced summed expression must no longer be present.
    assert 'd.work_in_museum + d.work_outside + d.vacation' not in summary_sql
    assert 'd.work_in_museum + d.work_outside + d.vacation' not in monthly_sql
