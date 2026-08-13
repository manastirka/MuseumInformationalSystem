"""Reproducing tests for bugs found in the 2026-05-29 code control-check audit.

Each test is written to FAIL against the pre-fix code (reproducing the reported
bug) and PASS once the root-cause fix is applied. Tests are grouped by the audit
identifier used in BUG_AUDIT_2026-05-29.md (C# = critical, H# = high, M# = medium).
"""

import os
from contextlib import contextmanager
from unittest.mock import MagicMock, patch

os.environ.setdefault('FLASK_ENV', 'testing')
os.environ.setdefault('SECRET_KEY', 'test-secret')
os.environ.setdefault('REDIS_URL', '')
os.environ.setdefault('SESSION_TYPE', 'filesystem')
os.environ.setdefault('SESSION_FILE_DIR', '/tmp/museum-test-flask-session-bug-audit')

import flask  # noqa: E402

import app as museum_app  # noqa: E402
import mail_views  # noqa: E402
import employee_admin_views  # noqa: E402
import museum_content_views  # noqa: E402
import collection_management_views  # noqa: E402


# ---------------------------------------------------------------------------
# C2 + H11 — mail_views
# ---------------------------------------------------------------------------
class TestMailViews:
    def test_C2_api_mail_folders_does_not_reference_undefined_names(self):
        """C2: api_mail_folders had a mis-pasted breadcrumb referencing the
        undefined names `attachments`/`to`, raising NameError on every call so
        the endpoint always returned 500."""
        fake_mc = MagicMock()
        fake_mc.list_folders.return_value = [{'name': 'INBOX', 'unread': 0}]
        with patch('mail_client.MailClient', return_value=fake_mc):
            with museum_app.app.test_request_context('/api/mail/folders'):
                flask.session['user_email'] = 'tester@museum.rs'
                result = mail_views.api_mail_folders()
        # A (response, 500) tuple means the except branch fired (the bug).
        assert not isinstance(result, tuple), "api_mail_folders fell into the 500 error branch"
        data = result.get_json()
        assert data['success'] is True
        assert data['folders'] == [{'name': 'INBOX', 'unread': 0}]

    def test_H11_api_mail_init_handles_non_numeric_page(self):
        """H11: int(?page) was evaluated before the try block, so a non-numeric
        page raised an uncaught ValueError (HTTP 500 + traceback)."""
        fake_mc = MagicMock()
        fake_mc.get_init_data.return_value = {'folders': [], 'messages': [], 'total': 0}
        with patch('mail_client.MailClient', return_value=fake_mc):
            with museum_app.app.test_request_context('/api/mail/init?page=abc'):
                flask.session['user_email'] = 'tester@museum.rs'
                result = mail_views.api_mail_init()  # must not raise ValueError
        assert not isinstance(result, tuple)
        assert result.get_json()['success'] is True
        _, kwargs = fake_mc.get_init_data.call_args
        assert kwargs['page'] == 1  # malformed page falls back to 1

    def test_H11_api_mail_messages_handles_non_numeric_page(self):
        fake_mc = MagicMock()
        fake_mc.list_messages.return_value = {'messages': [], 'total': 0}
        with patch('mail_client.MailClient', return_value=fake_mc):
            with museum_app.app.test_request_context('/api/mail/messages?page=xyz'):
                flask.session['user_email'] = 'tester@museum.rs'
                result = mail_views.api_mail_messages()  # must not raise ValueError
        assert not isinstance(result, tuple)
        assert result.get_json()['success'] is True
        _, kwargs = fake_mc.list_messages.call_args
        assert kwargs['page'] == 1


# ---------------------------------------------------------------------------
# H1 + H2 — employee_admin_views.handle_add_user
# ---------------------------------------------------------------------------
class TestAddUser:
    def test_H1_H2_add_user_persists_to_db_without_crashing_on_empty_fallback(self):
        """H1: max([]) crashed when the in-memory employee dict was empty
        (the production default). H2: the user was never persisted to PostgreSQL.
        The fix persists via PostgresAuthSystem.create_user and lets the DB
        assign the id. Since revizija 2026-08 (#5) the handler additionally
        requires the caller's role (allow-lista) and a password_validator, so
        the test acts as an admin with a policy-passing password."""
        fake_auth = MagicMock()
        fake_auth.create_user.return_value = 42
        ph = MagicMock()
        ph.hash_password.return_value = ('hash', 'salt')
        pv = MagicMock()
        pv.validate.return_value = (True, [])
        with patch('postgres_auth.get_postgres_auth', return_value=fake_auth):
            with museum_app.app.test_request_context(
                '/admin/add_user',
                method='POST',
                data={
                    'email': 'newuser@museum.rs',
                    'full_name': 'New User',
                    'department': 'Geology',
                    'position': 'Curator',
                    'role': 'employee',
                    'password': 'longenough1',
                },
            ):
                flask.session['user_role'] = 'admin'  # allow-lista: admin sme employee
                resp = employee_admin_views.handle_add_user(
                    get_museum_employees=lambda: {},   # empty fallback (production default)
                    get_employee_directory=lambda: [],
                    password_hasher=ph,
                    password_validator=pv,
                )
        pv.validate.assert_called_once_with('longenough1')
        fake_auth.create_user.assert_called_once()
        called = fake_auth.create_user.call_args.kwargs
        assert called['email'] == 'newuser@museum.rs'
        assert called['full_name'] == 'New User'
        assert called['password'] == 'longenough1'
        assert resp.status_code == 302  # redirect to employees_database

    def test_H1_add_user_reports_error_when_persistence_fails(self):
        """When create_user returns None (e.g. duplicate email / DB error), the
        handler must report failure rather than flashing a bogus success."""
        fake_auth = MagicMock()
        fake_auth.create_user.return_value = None
        pv = MagicMock()
        pv.validate.return_value = (True, [])
        with patch('postgres_auth.get_postgres_auth', return_value=fake_auth):
            with museum_app.app.test_request_context(
                '/admin/add_user',
                method='POST',
                data={
                    'email': 'dupe@museum.rs',
                    'full_name': 'Dupe User',
                    'department': 'Geology',
                    'position': 'Curator',
                    'password': 'longenough1',
                },
            ):
                flask.session['user_role'] = 'admin'  # allow-lista: admin sme employee
                resp = employee_admin_views.handle_add_user(
                    get_museum_employees=lambda: {},
                    get_employee_directory=lambda: [],
                    password_hasher=MagicMock(),
                    password_validator=pv,
                )
                flashed = flask.get_flashed_messages(category_filter=['error'])
        fake_auth.create_user.assert_called_once()
        assert resp.status_code == 302
        assert flashed, "an error must be flashed when persistence fails"


# ---------------------------------------------------------------------------
# H8 — museum_content_views.handle_add_visitor
# ---------------------------------------------------------------------------
class TestAddVisitor:
    class _RecordingCursor:
        def __init__(self):
            self.executed = []

        def execute(self, query, params=None):
            self.executed.append((query, params))

        def __enter__(self):
            return self

        def __exit__(self, *exc):
            return False

    def test_H8_blank_group_size_does_not_crash(self):
        """H8: int(request.form.get('group_size', 1)) crashed with ValueError
        when the number field was submitted blank (default only applies when the
        key is absent, not when it is an empty string). Since batch 62c9336
        (migracija 040) the record is persisted to PostgreSQL, so the fallback
        is asserted on the INSERT parameters instead of an in-memory list."""
        cur = self._RecordingCursor()
        conn = MagicMock()
        conn.cursor.return_value = cur

        @contextmanager
        def fake_get_conn(*args, **kwargs):
            yield conn

        with patch.object(museum_content_views, 'get_postgres_connection', fake_get_conn):
            with museum_app.app.test_request_context(
                '/admin/add_visitor',
                method='POST',
                data={
                    'date': '2026-05-29',
                    'visitor_type': 'individual',
                    'group_size': '',          # blank field
                    'age_category': 'adult',
                    'ticket_type': 'full',
                },
            ):
                resp = museum_content_views.handle_add_visitor()
        assert resp.status_code == 302  # success redirect, not the error re-render
        inserts = [(q, p) for q, p in cur.executed
                   if 'INSERT INTO visitor_records' in q]
        assert len(inserts) == 1
        _, params = inserts[0]
        # Column order: visit_date, visitor_type, group_size, ...
        assert params[0] == '2026-05-29'
        assert params[1] == 'individual'
        assert params[2] == 1  # blank falls back to 1
        conn.commit.assert_called_once()


# ---------------------------------------------------------------------------
# H6 — collection_management_views.render_cultural_heritage_database
# ---------------------------------------------------------------------------
class TestCulturalHeritage:
    def _heritage_db(self):
        items = [
            {'significance': 'Културно добро', 'category': 'Природњачко наслеђе',
             'condition': 'Одлично', 'location': 'Сала 1'},
            {'significance': 'Културно добро', 'category': 'Друго',
             'condition': 'Добро', 'location': None},   # NULL location -> crash trigger
            {'significance': 'Културно добро', 'category': 'Друго',
             'condition': 'Добро', 'location': 'Депо 2'},
        ]
        return {
            'heritage_items': items,
            'statistics': {},
            'heritage_types': [], 'categories': [], 'subcategories': [],
            'significance_levels': [], 'locations': [], 'conditions': [],
            'protection_statuses': [],
        }

    def test_H6_null_location_does_not_crash_statistics(self):
        """H6: `'Сала' in item['location']` raised TypeError when location was
        NULL (PostgreSQL current_location is nullable)."""
        captured = {}

        def fake_render(_template, **kwargs):
            captured.update(kwargs)
            return 'ok'

        with patch.object(collection_management_views, 'render_template', fake_render):
            with museum_app.app.test_request_context('/admin/cultural_heritage_database'):
                result = collection_management_views.render_cultural_heritage_database(
                    get_cultural_heritage_database=self._heritage_db,
                    prepare_collection_records_for_display=lambda key, recs: (recs, None),
                    get_qr_collection_action_url=lambda key: '/qr',
                )
        assert result == 'ok'  # reached render_template without crashing
        stats = captured['statistics']
        assert stats['displayed_items'] == 1   # only 'Сала 1'
        assert stats['storage_items'] == 1     # only 'Депо 2'


# ---------------------------------------------------------------------------
# H7 — collection_management_views.handle_add_collection_item
# ---------------------------------------------------------------------------
class TestAddCollectionItem:
    def test_H7_generic_add_does_not_falsely_report_success(self):
        """H7: the generic add-item branch built item_data then did `_ = item_data`
        and flashed success without persisting anything — silent data loss with a
        green confirmation. The fix must not report a bogus success."""
        with patch.object(collection_management_views, 'url_for', lambda *a, **k: '/dummy'), \
             patch.dict(
                 collection_management_views._COLLECTION_FORM_INFO,
                 {'petrology': {'name': 'Петрологија', 'route': 'petrology_collection'}},
             ):
            with museum_app.app.test_request_context(
                '/collection/petrology/add',
                method='POST',
                data={'catalog_number': 'X1', 'scientific_name': 'Quartz'},
            ):
                flask.session['user_email'] = 'curator@museum.rs'
                resp = collection_management_views.handle_add_collection_item('petrology')
                success = flask.get_flashed_messages(category_filter=['success'])
                errors = flask.get_flashed_messages(category_filter=['error'])
        assert not success, "must NOT flash a bogus success when nothing is persisted"
        assert errors, "must inform the curator that the item was not saved"
        assert resp.status_code == 302
