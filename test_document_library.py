#!/usr/bin/env python3
"""Tests for the document library module (складиштење, преглед и одобравање).

Covers: upload (including Cyrillic filenames), the full approval workflow
(nacrt -> na_odobrenju -> odobreno -> arhivirano, rejection back to nacrt),
role-based visibility of unapproved versions, the self-approval guard,
file serving (PDF inline, other formats as attachment) and path traversal.
"""

import io
import os
import shutil
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

os.environ.setdefault('FLASK_ENV', 'testing')
os.environ.setdefault('SECRET_KEY', 'test-secret')
os.environ.setdefault('REDIS_URL', '')
os.environ.setdefault('SESSION_TYPE', 'filesystem')
os.environ.setdefault('SESSION_FILE_DIR', '/tmp/museum-test-flask-session')

import app as museum_app
import archive_signature_blueprint
import document_library_views


GEOLOGY = 'ГЕОЛОШКО ОДЕЉЕЊЕ'
BIOLOGY = 'БИОЛОШКО ОДЕЉЕЊЕ'

EMPLOYEE = {
    'user_id': 10, 'user_email': 'radnik@nhmbeo.rs', 'user_name': 'Радник',
    'user_role': 'employee', 'is_admin': False,
    'user_department': GEOLOGY, 'is_department_head': False,
}
OTHER_EMPLOYEE = {
    'user_id': 11, 'user_email': 'drugi@nhmbeo.rs', 'user_name': 'Други',
    'user_role': 'employee', 'is_admin': False,
    'user_department': GEOLOGY, 'is_department_head': False,
}
GEOLOGY_HEAD = {
    'user_id': 20, 'user_email': 'sef.geo@nhmbeo.rs', 'user_name': 'Шеф Гео',
    'user_role': 'sef_odeljenja', 'is_admin': False,
    'user_department': GEOLOGY, 'is_department_head': True,
}
BIOLOGY_HEAD = {
    'user_id': 21, 'user_email': 'sef.bio@nhmbeo.rs', 'user_name': 'Шеф Био',
    'user_role': 'sef_odeljenja', 'is_admin': False,
    'user_department': BIOLOGY, 'is_department_head': True,
}
DIRECTOR = {
    'user_id': 30, 'user_email': 'direktor@nhmbeo.rs', 'user_name': 'Директор',
    'user_role': 'direktor', 'is_admin': False,
    'user_department': None, 'is_department_head': False,
}
ADMIN = {
    'user_id': 1, 'user_email': 'admin@nhmbeo.rs', 'user_name': 'Админ',
    'user_role': 'admin', 'is_admin': True,
    'user_department': None, 'is_department_head': False,
}


def _doc(**overrides):
    doc = {
        'id': 42, 'title': 'Молба за годишњи одмор', 'description': None,
        'category': 'obrasci_zahtevi', 'department': GEOLOGY,
        'created_by_email': EMPLOYEE['user_email'], 'is_active': True,
    }
    doc.update(overrides)
    return doc


def _version(**overrides):
    version = {
        'id': 100, 'document_id': 42, 'version_no': 1,
        'file_path': 'obrasci_zahtevi/42/v01_abcd1234_molba.pdf',
        'original_filename': 'Молба за годишњи одмор.pdf',
        'mime_type': 'application/pdf', 'file_size': 1234,
        'sha256': 'f' * 64, 'status': 'nacrt',
        'uploaded_by_email': EMPLOYEE['user_email'],
        'uploaded_at': None, 'submitted_at': None,
        'reviewed_by_email': None, 'reviewed_at': None, 'review_comment': None,
    }
    version.update(overrides)
    return version


def _joined_row(document, version):
    """Row shape returned by _fetch_version_with_document's SELECT."""
    row = dict(version)
    row.update({
        'd_id': document['id'], 'd_title': document['title'],
        'd_description': document['description'], 'd_category': document['category'],
        'd_department': document['department'],
        'd_created_by_email': document['created_by_email'],
        'd_is_active': document['is_active'],
    })
    return row


class _FakeCursor:
    """Returns canned dict rows matched by SQL substring, records executes."""

    def __init__(self, canned=None):
        self.canned = dict(canned or {})
        self._pending = None
        self.executed = []

    def execute(self, sql, params=None):
        self.executed.append((' '.join(sql.split()), params))
        for needle, row in self.canned.items():
            if needle in sql:
                self._pending = row
                return
        self._pending = None

    def fetchone(self):
        value = self._pending
        if isinstance(value, list):
            return value[0] if value else None
        return value

    def fetchall(self):
        value = self._pending
        if isinstance(value, list):
            return value
        return [value] if value else []

    def __enter__(self):
        return self

    def __exit__(self, *_):
        return False


class _FakeConnection:
    def __init__(self, cursor):
        self._cursor = cursor
        self.commits = 0

    def cursor(self):
        return self._cursor

    def commit(self):
        self.commits += 1

    def __enter__(self):
        return self

    def __exit__(self, *_):
        self.commit()
        return False


class DocumentPermissionTests(unittest.TestCase):
    """Pure policy tests for visibility and approval rules."""

    def test_approved_version_visible_to_everyone(self):
        version = _version(status='odobreno')
        for who in (EMPLOYEE, OTHER_EMPLOYEE, GEOLOGY_HEAD, BIOLOGY_HEAD, DIRECTOR, ADMIN):
            self.assertTrue(
                document_library_views.can_view_document_version(who, _doc(), version)
            )

    def test_draft_hidden_from_other_employees(self):
        version = _version(status='nacrt')
        self.assertFalse(
            document_library_views.can_view_document_version(OTHER_EMPLOYEE, _doc(), version)
        )

    def test_draft_visible_to_author_admin_director_and_own_head(self):
        version = _version(status='nacrt')
        for who in (EMPLOYEE, ADMIN, DIRECTOR, GEOLOGY_HEAD):
            self.assertTrue(
                document_library_views.can_view_document_version(who, _doc(), version)
            )

    def test_draft_hidden_from_head_of_other_department(self):
        version = _version(status='nacrt')
        self.assertFalse(
            document_library_views.can_view_document_version(BIOLOGY_HEAD, _doc(), version)
        )

    def test_head_approves_own_department_only(self):
        version = _version(status='na_odobrenju')
        self.assertTrue(
            document_library_views.can_approve_document_version(GEOLOGY_HEAD, _doc(), version)
        )
        self.assertFalse(
            document_library_views.can_approve_document_version(BIOLOGY_HEAD, _doc(), version)
        )

    def test_director_and_admin_approve_any_department(self):
        version = _version(status='na_odobrenju')
        for who in (DIRECTOR, ADMIN):
            self.assertTrue(
                document_library_views.can_approve_document_version(who, _doc(), version)
            )

    def test_self_approval_forbidden_for_everyone(self):
        for who in (GEOLOGY_HEAD, DIRECTOR, ADMIN):
            version = _version(status='na_odobrenju', uploaded_by_email=who['user_email'])
            self.assertFalse(
                document_library_views.can_approve_document_version(who, _doc(), version),
                who['user_role'],
            )

    def test_regular_employee_never_approves(self):
        version = _version(status='na_odobrenju', uploaded_by_email=OTHER_EMPLOYEE['user_email'])
        self.assertFalse(
            document_library_views.can_approve_document_version(EMPLOYEE, _doc(), version)
        )

    def test_document_without_department_needs_director_or_admin(self):
        version = _version(status='na_odobrenju')
        doc = _doc(department=None)
        self.assertFalse(
            document_library_views.can_approve_document_version(GEOLOGY_HEAD, doc, version)
        )
        self.assertTrue(
            document_library_views.can_approve_document_version(DIRECTOR, doc, version)
        )

    def test_department_name_drift_tolerated(self):
        version = _version(status='na_odobrenju')
        head = dict(GEOLOGY_HEAD, user_department='  геолошко одељење ')
        self.assertTrue(
            document_library_views.can_approve_document_version(head, _doc(), version)
        )

    def test_cyrillic_filename_keeps_extension(self):
        safe = document_library_views._safe_document_filename('Молба за годишњи.docx')
        self.assertTrue(safe.endswith('.docx'))
        self.assertNotEqual(safe, '.docx')


class _ClientTestCase(unittest.TestCase):
    """Shared plumbing: test client, disabled CSRF, temp storage, fake DB."""

    def setUp(self):
        museum_app.app.config['TESTING'] = True
        csrf_was_enabled = museum_app.app.config.get('WTF_CSRF_ENABLED', False)
        museum_app.app.config['WTF_CSRF_ENABLED'] = False
        self.addCleanup(
            museum_app.app.config.__setitem__, 'WTF_CSRF_ENABLED', csrf_was_enabled
        )

        module_patch = patch.object(
            museum_app.app, 'user_has_module_access', lambda *args, **kwargs: True
        )
        module_patch.start()
        self.addCleanup(module_patch.stop)

        self.storage_dir = tempfile.mkdtemp(prefix='dokumenti-test-')
        self.addCleanup(shutil.rmtree, self.storage_dir, True)
        env_patch = patch.dict(os.environ, {'DOCUMENTS_STORAGE_PATH': self.storage_dir})
        env_patch.start()
        self.addCleanup(env_patch.stop)

        self.client = museum_app.app.test_client()

    def get(self, *args, **kwargs):
        kwargs.setdefault('base_url', 'https://localhost')
        return self.client.get(*args, **kwargs)

    def post(self, *args, **kwargs):
        kwargs.setdefault('base_url', 'https://localhost')
        return self.client.post(*args, **kwargs)

    def login(self, who):
        with self.client.session_transaction() as sess:
            for key, value in who.items():
                sess[key] = value

    def use_db(self, canned):
        cursor = _FakeCursor(canned)
        connection = _FakeConnection(cursor)
        db_patch = patch.object(
            document_library_views, 'get_postgres_connection', lambda **kwargs: connection
        )
        db_patch.start()
        self.addCleanup(db_patch.stop)
        # The unified approval center also queries operational requests; keep
        # those queries hermetic (and empty) as well.
        requests_connection = _FakeConnection(_FakeCursor({}))
        requests_patch = patch.object(
            archive_signature_blueprint, 'get_postgres_connection',
            lambda **kwargs: requests_connection,
        )
        requests_patch.start()
        self.addCleanup(requests_patch.stop)
        return cursor


def _plain_db_url():
    return os.environ.get('DATABASE_URL', '').replace('postgresql+psycopg://', 'postgresql://')


class DocumentUploadTests(_ClientTestCase):
    """Стварни PostgreSQL: dedup (sha256) i redosled verzija (MAX+1) su tačno
    tok gde fake kursor sa unapred upisanim odgovorom ne dokazuje ono što je
    stvarno upisano posle commit-a."""

    UPLOAD_EMAIL = 'upload.tok.revizija@example.invalid'
    UPLOAD_EMAIL_2 = 'upload.tok.revizija.drugi@example.invalid'

    @classmethod
    def setUpClass(cls):
        try:
            import psycopg
        except ImportError:
            raise unittest.SkipTest('psycopg nije instaliran')
        cls.psycopg = psycopg
        try:
            with psycopg.connect(_plain_db_url(), connect_timeout=3) as conn:
                conn.execute('SELECT 1')
        except Exception:
            raise unittest.SkipTest('test baza nije dostupna')
        with psycopg.connect(_plain_db_url()) as conn:
            sql = (Path(__file__).parent / 'migration' / '022_document_library.sql'
                   ).read_text(encoding='utf-8')
            conn.execute(sql)

    def setUp(self):
        super().setUp()
        self.addCleanup(self._ocisti_bazu)
        self._ocisti_bazu()

    def _ocisti_bazu(self):
        with self.psycopg.connect(_plain_db_url()) as conn:
            conn.execute(
                'DELETE FROM documents WHERE created_by_email IN (%s, %s)',
                (self.UPLOAD_EMAIL, self.UPLOAD_EMAIL_2))
            conn.commit()

    def _login_kao(self, email, department=GEOLOGY):
        self.login({
            'user_id': 10, 'user_email': email, 'user_name': 'Тест Радник',
            'user_role': 'employee', 'is_admin': False,
            'user_department': department, 'is_department_head': False,
        })

    def _dokument(self, **overrides):
        row = {
            'title': 'Постојећи документ', 'description': None,
            'category': 'obrasci_zahtevi', 'department': GEOLOGY,
            'created_by_email': self.UPLOAD_EMAIL,
        }
        row.update(overrides)
        with self.psycopg.connect(_plain_db_url()) as conn:
            cur = conn.execute(
                """
                INSERT INTO documents (title, description, category, department, created_by_email)
                VALUES (%s, %s, %s, %s, %s) RETURNING id
                """,
                (row['title'], row['description'], row['category'],
                 row['department'], row['created_by_email']))
            document_id = cur.fetchone()[0]
            conn.commit()
        return document_id

    def _verzija(self, document_id, **overrides):
        row = {
            'version_no': 1,
            'file_path': f'obrasci_zahtevi/{document_id}/v01_seed.pdf',
            'original_filename': 'seed.pdf', 'mime_type': 'application/pdf',
            'file_size': 10, 'sha256': 'a' * 64, 'status': 'nacrt',
            'uploaded_by_email': self.UPLOAD_EMAIL,
        }
        row.update(overrides)
        with self.psycopg.connect(_plain_db_url()) as conn:
            conn.execute(
                """
                INSERT INTO document_versions
                    (document_id, version_no, file_path, original_filename,
                     mime_type, file_size, sha256, uploaded_by_email)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """,
                (document_id, row['version_no'], row['file_path'],
                 row['original_filename'], row['mime_type'], row['file_size'],
                 row['sha256'], row['uploaded_by_email']))
            conn.commit()

    def _redirect_document_id(self, response):
        location = response.headers['Location']
        return int(location.rstrip('/').rsplit('/', 1)[-1])

    def test_upload_requires_login(self):
        response = self.post('/dokumenti/upload', data={})
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login', response.headers['Location'])

    def test_upload_new_document_stores_file_and_metadata(self):
        self._login_kao(self.UPLOAD_EMAIL)
        payload = 'Садржај обрасца'.encode('utf-8')
        response = self.post(
            '/dokumenti/upload',
            data={
                'title': 'Молба за годишњи одмор',
                'category': 'obrasci_zahtevi',
                'description': 'Образац',
                'file': (io.BytesIO(payload), 'Молба за годишњи одмор.pdf'),
            },
            content_type='multipart/form-data',
        )
        self.assertEqual(response.status_code, 302)
        document_id = self._redirect_document_id(response)
        self.assertIn(f'/dokumenti/{document_id}', response.headers['Location'])

        with self.psycopg.connect(_plain_db_url()) as conn:
            conn.row_factory = self.psycopg.rows.dict_row
            doc = conn.execute(
                'SELECT title, category, department, created_by_email '
                'FROM documents WHERE id = %s', (document_id,)).fetchone()
            self.assertEqual(doc['title'], 'Молба за годишњи одмор')
            self.assertEqual(doc['category'], 'obrasci_zahtevi')
            self.assertEqual(doc['department'], GEOLOGY)

            version = conn.execute(
                'SELECT document_id, version_no, file_path, original_filename, sha256 '
                'FROM document_versions WHERE document_id = %s', (document_id,)).fetchone()
            self.assertEqual(version['version_no'], 1)
            self.assertTrue(version['file_path'].startswith(f'obrasci_zahtevi/{document_id}/v01_'))
            self.assertTrue(version['file_path'].endswith('.pdf'))
            self.assertEqual(version['original_filename'], 'Молба за годишњи одмор.pdf')

            import hashlib
            self.assertEqual(version['sha256'], hashlib.sha256(payload).hexdigest())

            audit_count = conn.execute(
                'SELECT count(*) AS n FROM document_audit_log WHERE document_id = %s',
                (document_id,)).fetchone()['n']
            self.assertEqual(audit_count, 1)

        stored = os.path.join(self.storage_dir, version['file_path'])
        self.assertTrue(os.path.isfile(stored))
        with open(stored, 'rb') as handle:
            self.assertEqual(handle.read(), payload)
        self.assertFalse(os.listdir(os.path.join(self.storage_dir, 'temp')))

    def test_upload_rejects_forbidden_extension(self):
        self._login_kao(self.UPLOAD_EMAIL)
        response = self.post(
            '/dokumenti/upload',
            data={
                'title': 'Скрипта', 'category': 'ostalo',
                'file': (io.BytesIO(b'#!/bin/sh'), 'skripta.sh'),
            },
            content_type='multipart/form-data',
        )
        self.assertEqual(response.status_code, 302)
        with self.psycopg.connect(_plain_db_url()) as conn:
            count = conn.execute(
                'SELECT count(*) FROM documents WHERE created_by_email = %s',
                (self.UPLOAD_EMAIL,)).fetchone()[0]
        self.assertEqual(count, 0)

    def test_upload_rejects_oversized_file(self):
        self._login_kao(self.UPLOAD_EMAIL)
        with patch.object(document_library_views, 'MAX_DOCUMENT_SIZE', 10):
            response = self.post(
                '/dokumenti/upload',
                data={
                    'title': 'Велики', 'category': 'ostalo',
                    'file': (io.BytesIO(b'x' * 11), 'veliki.pdf'),
                },
                content_type='multipart/form-data',
            )
        self.assertEqual(response.status_code, 302)
        with self.psycopg.connect(_plain_db_url()) as conn:
            count = conn.execute(
                'SELECT count(*) FROM documents WHERE created_by_email = %s',
                (self.UPLOAD_EMAIL,)).fetchone()[0]
        self.assertEqual(count, 0)

    def test_upload_duplicate_version_rejected(self):
        payload = b'same content'
        import hashlib
        document_id = self._dokument()
        self._verzija(document_id, sha256=hashlib.sha256(payload).hexdigest())
        self._login_kao(self.UPLOAD_EMAIL)
        response = self.post(
            '/dokumenti/upload',
            data={
                'document_id': str(document_id),
                'file': (io.BytesIO(payload), 'ponovo.pdf'),
            },
            content_type='multipart/form-data',
        )
        self.assertEqual(response.status_code, 302)
        with self.psycopg.connect(_plain_db_url()) as conn:
            count = conn.execute(
                'SELECT count(*) FROM document_versions WHERE document_id = %s',
                (document_id,)).fetchone()[0]
        self.assertEqual(count, 1, 'duplikat sadržaja ne sme kreirati novu verziju')

    def test_upload_new_version_increments_number(self):
        document_id = self._dokument()
        self._verzija(document_id, version_no=3, sha256='b' * 64)
        self._login_kao(self.UPLOAD_EMAIL_2)
        response = self.post(
            '/dokumenti/upload',
            data={
                'document_id': str(document_id),
                'file': (io.BytesIO(b'nova verzija'), 'молба-в4.pdf'),
            },
            content_type='multipart/form-data',
        )
        self.assertEqual(response.status_code, 302)
        with self.psycopg.connect(_plain_db_url()) as conn:
            conn.row_factory = self.psycopg.rows.dict_row
            version = conn.execute(
                'SELECT version_no, file_path FROM document_versions '
                'WHERE document_id = %s AND version_no = 4', (document_id,)).fetchone()
        self.assertIsNotNone(version, 'nova verzija mora biti upisana kao broj 4')
        self.assertTrue(version['file_path'].startswith(f'obrasci_zahtevi/{document_id}/v04_'))


class DocumentWorkflowTests(_ClientTestCase):

    def test_author_submits_draft_for_approval(self):
        document, version = _doc(), _version(status='nacrt')
        cursor = self.use_db({
            'WHERE v.id = %s': _joined_row(document, version),
            "SET status = %s, submitted_at": {'id': version['id']},
        })
        self.login(EMPLOYEE)
        response = self.post(f"/dokumenti/verzija/{version['id']}/posalji")
        self.assertEqual(response.status_code, 302)
        submits = [
            params for sql, params in cursor.executed
            if 'SET status = %s, submitted_at' in sql
        ]
        self.assertEqual(len(submits), 1)
        # Са УКЉУЧЕНИМ одобравањем верзија мора да оде на одобрење, не да
        # постане важећа. Ово је тврдња о вредности, не о тексту упита.
        self.assertEqual(submits[0][0], 'na_odobrenju')

    def test_iskljuceno_odobravanje_cini_verziju_odmah_vazecom(self):
        """Прекидач угашен: верзија важи одмах, али НЕ пише „Одобрено".

        Документ и даље сме да има само једну важећу верзију, па претходна
        мора да оде у архиву — исто као при правом одобрењу.
        """
        import document_library_views as dlv
        document, version = _doc(), _version(status='nacrt')
        cursor = self.use_db({
            'WHERE v.id = %s': _joined_row(document, version),
            "SET status = %s, submitted_at": {'id': version['id']},
        })
        self.login(EMPLOYEE)
        with patch.object(dlv.odobravanje_prekidac,
                          'odobravanje_dokumenata_ukljuceno', lambda: False):
            response = self.post(f"/dokumenti/verzija/{version['id']}/posalji")
        self.assertEqual(response.status_code, 302)

        submits = [
            params for sql, params in cursor.executed
            if 'SET status = %s, submitted_at' in sql
        ]
        self.assertEqual(len(submits), 1)
        self.assertEqual(submits[0][0], 'bez_odobrenja')

        # Никад 'odobreno': то стање значи да га је неко прегледао и потписао.
        self.assertFalse(
            [sql for sql, _ in cursor.executed if "SET status = 'odobreno'" in sql],
            'верзија без рецензента не сме да добије статус одобрене')

        arhive = [
            params for sql, params in cursor.executed
            if "SET status = 'arhivirano'" in sql and 'WHERE document_id' in sql
        ]
        self.assertEqual(len(arhive), 1,
                         'претходна важећа верзија мора да оде у архиву')
        self.assertEqual(arhive[0][0], document['id'])
        self.assertEqual(sorted(arhive[0][1]), ['bez_odobrenja', 'odobreno'])

    def test_other_employee_cannot_submit_someone_elses_draft(self):
        document, version = _doc(), _version(status='nacrt')
        self.use_db({'WHERE v.id = %s': _joined_row(document, version)})
        self.login(OTHER_EMPLOYEE)
        response = self.post(f"/dokumenti/verzija/{version['id']}/posalji")
        self.assertEqual(response.status_code, 403)

    def test_head_approves_and_previous_version_is_archived(self):
        document = _doc()
        version = _version(status='na_odobrenju', version_no=2, id=101)
        cursor = self.use_db({
            'WHERE v.id = %s': _joined_row(document, version),
            "SET status = 'odobreno'": {'id': version['id']},
        })
        self.login(GEOLOGY_HEAD)
        response = self.post(f"/dokumenti/verzija/{version['id']}/odobri")
        self.assertEqual(response.status_code, 302)

        approve = next(
            params for sql, params in cursor.executed if "SET status = 'odobreno'" in sql
        )
        self.assertEqual(approve[0], GEOLOGY_HEAD['user_email'])

        archive = next(
            params for sql, params in cursor.executed
            if "SET status = 'arhivirano'" in sql and 'WHERE document_id' in sql
        )
        # Архивира се свака ПРЕТХОДНА важећа верзија — и одобрена и она
        # завршена без одобравања. Документ никад не сме имати две важеће.
        self.assertEqual(archive[0], document['id'])
        self.assertEqual(sorted(archive[1]), ['bez_odobrenja', 'odobreno'])
        self.assertEqual(archive[2], version['id'])

    def test_self_approval_returns_403(self):
        document = _doc()
        version = _version(status='na_odobrenju', uploaded_by_email=GEOLOGY_HEAD['user_email'])
        self.use_db({'WHERE v.id = %s': _joined_row(document, version)})
        self.login(GEOLOGY_HEAD)
        response = self.post(f"/dokumenti/verzija/{version['id']}/odobri")
        self.assertEqual(response.status_code, 403)

    def test_head_of_other_department_cannot_approve(self):
        document, version = _doc(), _version(status='na_odobrenju')
        self.use_db({'WHERE v.id = %s': _joined_row(document, version)})
        self.login(BIOLOGY_HEAD)
        response = self.post(f"/dokumenti/verzija/{version['id']}/odobri")
        self.assertEqual(response.status_code, 403)

    def test_regular_employee_blocked_by_route_decorator(self):
        cursor = self.use_db({})
        self.login(EMPLOYEE)
        response = self.post('/dokumenti/verzija/100/odobri')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(cursor.executed, [])

    def test_reject_requires_comment_and_returns_to_draft(self):
        document, version = _doc(), _version(status='na_odobrenju')
        cursor = self.use_db({
            'WHERE v.id = %s': _joined_row(document, version),
            "SET status = 'nacrt'": {'id': version['id']},
        })
        self.login(DIRECTOR)

        response = self.post(f"/dokumenti/verzija/{version['id']}/odbij", data={})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            [sql for sql, _ in cursor.executed if "SET status = 'nacrt'" in sql], []
        )

        response = self.post(
            f"/dokumenti/verzija/{version['id']}/odbij",
            data={'comment': 'Недостаје потпис'},
        )
        self.assertEqual(response.status_code, 302)
        reject = next(
            params for sql, params in cursor.executed if "SET status = 'nacrt'" in sql
        )
        self.assertEqual(reject[1], 'Недостаје потпис')

    def test_archive_requires_admin_or_director(self):
        document, version = _doc(), _version(status='odobreno')
        cursor = self.use_db({
            'WHERE v.id = %s': _joined_row(document, version),
            "SET status = 'arhivirano'": {'id': version['id']},
        })
        self.login(GEOLOGY_HEAD)
        response = self.post(f"/dokumenti/verzija/{version['id']}/arhiviraj")
        self.assertEqual(response.status_code, 302)
        self.assertEqual(cursor.executed, [])

        self.login(DIRECTOR)
        response = self.post(f"/dokumenti/verzija/{version['id']}/arhiviraj")
        self.assertEqual(response.status_code, 302)
        archived = [sql for sql, _ in cursor.executed if "SET status = 'arhivirano'" in sql]
        self.assertEqual(len(archived), 1)


class DocumentServingTests(_ClientTestCase):

    def _store_file(self, relative_path, payload=b'%PDF-1.4 test'):
        full_path = os.path.join(self.storage_dir, relative_path)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        with open(full_path, 'wb') as handle:
            handle.write(payload)
        return payload

    def test_approved_pdf_served_inline(self):
        document = _doc()
        version = _version(status='odobreno')
        payload = self._store_file(version['file_path'])
        self.use_db({'WHERE v.id = %s': _joined_row(document, version)})
        self.login(OTHER_EMPLOYEE)
        response = self.get(f"/dokumenti/fajl/{version['id']}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, payload)
        self.assertEqual(response.mimetype, 'application/pdf')
        self.assertIn('inline', response.headers.get('Content-Disposition', ''))

    def test_non_pdf_served_as_attachment(self):
        document = _doc()
        version = _version(
            status='odobreno',
            file_path='obrasci_zahtevi/42/v01_abcd1234_molba.docx',
            original_filename='Молба.docx',
            mime_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        )
        self._store_file(version['file_path'], b'docx-bytes')
        self.use_db({'WHERE v.id = %s': _joined_row(document, version)})
        self.login(OTHER_EMPLOYEE)
        response = self.get(f"/dokumenti/fajl/{version['id']}")
        self.assertEqual(response.status_code, 200)
        self.assertIn('attachment', response.headers.get('Content-Disposition', ''))

    def test_unapproved_version_forbidden_for_other_employee(self):
        document = _doc()
        for status in ('nacrt', 'na_odobrenju', 'arhivirano'):
            version = _version(status=status)
            self._store_file(version['file_path'])
            self.use_db({'WHERE v.id = %s': _joined_row(document, version)})
            self.login(OTHER_EMPLOYEE)
            response = self.get(f"/dokumenti/fajl/{version['id']}")
            self.assertEqual(response.status_code, 403, status)

    def test_author_downloads_own_draft(self):
        document = _doc()
        version = _version(status='nacrt')
        self._store_file(version['file_path'])
        self.use_db({'WHERE v.id = %s': _joined_row(document, version)})
        self.login(EMPLOYEE)
        response = self.get(f"/dokumenti/fajl/{version['id']}")
        self.assertEqual(response.status_code, 200)

    def test_path_traversal_in_file_path_returns_404(self):
        document = _doc()
        version = _version(status='odobreno', file_path='../../etc/passwd')
        self.use_db({'WHERE v.id = %s': _joined_row(document, version)})
        self.login(EMPLOYEE)
        response = self.get(f"/dokumenti/fajl/{version['id']}")
        self.assertEqual(response.status_code, 404)

    def test_missing_file_returns_404(self):
        document = _doc()
        version = _version(status='odobreno', file_path='obrasci_zahtevi/42/nema.pdf')
        self.use_db({'WHERE v.id = %s': _joined_row(document, version)})
        self.login(EMPLOYEE)
        response = self.get(f"/dokumenti/fajl/{version['id']}")
        self.assertEqual(response.status_code, 404)

    def test_anonymous_user_redirected_to_login(self):
        response = self.get('/dokumenti/fajl/100')
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login', response.headers['Location'])


class DocumentPageTests(_ClientTestCase):

    def test_list_page_renders_for_employee(self):
        approved = {
            'id': 42, 'title': 'Молба за годишњи одмор', 'description': None,
            'category': 'obrasci_zahtevi', 'department': GEOLOGY,
            'version_id': 100, 'version_no': 1,
            'original_filename': 'Молба.pdf', 'file_size': 1234, 'reviewed_at': None,
        }
        self.use_db({
            'DISTINCT ON (d.id)': [approved],
            'LOWER(v.uploaded_by_email)': [],
        })
        self.login(EMPLOYEE)
        response = self.get('/dokumenti')
        self.assertEqual(response.status_code, 200)
        body = response.data.decode('utf-8')
        self.assertIn('Молба за годишњи одмор', body)
        self.assertIn('Обрасци и захтеви', body)

    def test_detail_page_hides_drafts_from_other_employee(self):
        document = _doc()
        self.use_db({
            'FROM documents WHERE id = %s': document,
            'FROM document_versions v': [_version(status='nacrt')],
        })
        self.login(OTHER_EMPLOYEE)
        response = self.get('/dokumenti/42')
        self.assertEqual(response.status_code, 404)

    def test_approval_queue_scoped_to_head_department(self):
        geo_row = dict(
            _version(status='na_odobrenju'),
            document_title='Гео образац', category='obrasci_zahtevi', department=GEOLOGY,
        )
        bio_row = dict(
            _version(status='na_odobrenju', id=200, document_id=43),
            document_title='Био образац', category='obrasci_zahtevi', department=BIOLOGY,
        )
        self.use_db({"v.status = 'na_odobrenju'": [geo_row, bio_row]})
        self.login(GEOLOGY_HEAD)
        response = self.get('/odobravanje')
        self.assertEqual(response.status_code, 200)
        body = response.data.decode('utf-8')
        self.assertIn('Гео образац', body)
        self.assertNotIn('Био образац', body)

    def test_legacy_queue_url_redirects_to_center(self):
        self.use_db({})
        self.login(GEOLOGY_HEAD)
        response = self.get('/dokumenti/odobravanje')
        self.assertEqual(response.status_code, 302)
        self.assertIn('/odobravanje', response.headers['Location'])
        self.assertIn('tab=dokumenta', response.headers['Location'])

    def test_approval_queue_shows_all_to_director(self):
        geo_row = dict(
            _version(status='na_odobrenju'),
            document_title='Гео образац', category='obrasci_zahtevi', department=GEOLOGY,
        )
        bio_row = dict(
            _version(status='na_odobrenju', id=200, document_id=43),
            document_title='Био образац', category='obrasci_zahtevi', department=BIOLOGY,
        )
        self.use_db({"v.status = 'na_odobrenju'": [geo_row, bio_row]})
        self.login(DIRECTOR)
        response = self.get('/odobravanje')
        self.assertEqual(response.status_code, 200)
        body = response.data.decode('utf-8')
        self.assertIn('Гео образац', body)
        self.assertIn('Био образац', body)

    def test_approval_queue_blocked_for_regular_employee(self):
        self.use_db({})
        self.login(EMPLOYEE)
        response = self.get('/odobravanje')
        self.assertEqual(response.status_code, 302)


if __name__ == '__main__':
    unittest.main(verbosity=2)
