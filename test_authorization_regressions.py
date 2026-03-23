#!/usr/bin/env python3
"""Regression tests for authorization and file-path hardening."""

import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

os.environ.setdefault('FLASK_ENV', 'testing')
os.environ.setdefault('SECRET_KEY', 'test-secret')
os.environ.setdefault('REDIS_URL', '')

import app as museum_app


class FakeCursor:
    def __init__(self, fetchone_values=None, fetchall_values=None):
        self.fetchone_values = list(fetchone_values or [])
        self.fetchall_values = list(fetchall_values or [])
        self.executed = []

    def execute(self, query, params=None):
        self.executed.append((query, params))

    def fetchone(self):
        if not self.fetchone_values:
            return None
        return self.fetchone_values.pop(0)

    def fetchall(self):
        if not self.fetchall_values:
            return []
        return self.fetchall_values.pop(0)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False


class FakeConnection:
    def __init__(self, cursor):
        self._cursor = cursor

    def cursor(self):
        return self._cursor

    def commit(self):
        return None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False


class AuthorizationRegressionTests(unittest.TestCase):
    def setUp(self):
        self.client = museum_app.app.test_client()
        self.base_url = 'https://localhost'

    def _login(self, *, email='user@example.com', role='employee'):
        with self.client.session_transaction() as sess:
            sess['user_id'] = 1
            sess['user_email'] = email
            sess['user_name'] = 'Test User'
            sess['user_role'] = role
            sess['is_admin'] = role == 'admin'

    def test_current_user_is_admin_uses_role(self):
        with museum_app.app.test_request_context('/'):
            museum_app.session['user_role'] = 'admin'
            self.assertTrue(museum_app.current_user_is_admin())

    def test_resolve_signature_document_path_rejects_outside_allowed_roots(self):
        with tempfile.NamedTemporaryFile(suffix='.pdf') as tmp:
            resolved, relative, error = museum_app.resolve_signature_document_path(tmp.name)
            self.assertIsNone(resolved)
            self.assertIsNone(relative)
            self.assertEqual(error, 'Путања документа није дозвољена')

    def test_resolve_signature_document_path_allows_exports_file(self):
        exports_dir = museum_app.APP_ROOT / 'exports' / 'signature-tests'
        exports_dir.mkdir(parents=True, exist_ok=True)
        pdf_path = exports_dir / 'sample.pdf'
        pdf_path.write_bytes(b'%PDF-1.4 test')
        self.addCleanup(lambda: pdf_path.unlink(missing_ok=True))

        resolved, relative, error = museum_app.resolve_signature_document_path('exports/signature-tests/sample.pdf')
        self.assertEqual(resolved, pdf_path.resolve())
        self.assertEqual(relative, 'exports/signature-tests/sample.pdf')
        self.assertIsNone(error)

    def test_start_paper_enrichment_requires_admin(self):
        self._login(role='employee')
        response = self.client.post('/api/admin/start-paper-enrichment', base_url=self.base_url)
        self.assertEqual(response.status_code, 403)

    def test_start_paper_enrichment_allows_admin(self):
        self._login(role='admin')
        with patch.object(museum_app.map_feature_paper_enricher, 'start_enrichment_background', return_value=True):
            response = self.client.post('/api/admin/start-paper-enrichment', base_url=self.base_url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.get_json()['success'])

    def test_archive_request_detail_blocks_non_owner(self):
        self._login(email='viewer@example.com', role='employee')
        archive_row = (
            7, 'zahtev', 'godisnji_odmor', 'Title', 'Desc', {}, 'pending', 'normal',
            'owner@example.com', 'Owner', 'Dept', None, None, [], [], 0,
            None, None, None, None, None, None, None
        )
        fake_cursor = FakeCursor(fetchone_values=[archive_row])
        with patch('psycopg.connect', return_value=FakeConnection(fake_cursor)):
            response = self.client.get('/api/archive/requests/7', base_url=self.base_url)
        self.assertEqual(response.status_code, 403)

    def test_procurement_export_blocks_non_owner(self):
        self._login(email='viewer@example.com', role='employee')
        fake_cursor = FakeCursor(fetchone_values=[{
            'id': 3,
            'datum': '2026-03-01',
            'podnosilac': 'Owner',
            'items': [],
            'user_email': 'owner@example.com'
        }])
        with patch('psycopg.connect', return_value=FakeConnection(fake_cursor)):
            response = self.client.get('/api/nabavka/export-word/3', base_url=self.base_url)
        self.assertEqual(response.status_code, 403)

    def test_financial_plan_export_blocks_non_owner(self):
        self._login(email='viewer@example.com', role='employee')
        fake_cursor = FakeCursor(fetchone_values=[
            ('odeljenje', 'Odeljenje', 'Kustos', None, {}, 0, 0, 0, 0),
            ('owner@example.com',),
        ])
        with patch.object(museum_app, 'get_postgres_connection', return_value=FakeConnection(fake_cursor)):
            response = self.client.get('/api/finansijski-plan/export-word/9', base_url=self.base_url)
        self.assertEqual(response.status_code, 403)

    def test_signature_audit_blocks_other_requesters(self):
        self._login(email='viewer@example.com', role='employee')
        fake_cursor = FakeCursor(fetchone_values=[('owner@example.com',)])
        with patch('psycopg.connect', return_value=FakeConnection(fake_cursor)):
            response = self.client.get('/api/digital-signatures/5/audit', base_url=self.base_url)
        self.assertEqual(response.status_code, 403)


if __name__ == '__main__':
    unittest.main()
