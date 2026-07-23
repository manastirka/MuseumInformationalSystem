#!/usr/bin/env python3
"""Увоз радних листа из Word-а је ИСКЉУЧИВО админ функција (обједињено у Администрацији).

Захтеви (одлука корисника, fix/uvoz-word-admin):
  1. Запослени не види улаз/дугме за увоз у свом прегледу радне листе.
  2. СЕРВЕРСКА заштита: не-админ бива одбијен и на директан URL (не само
     сакривено дугме) — на свим рутама увоза (појединачни + архивски + стара
     путања). Одбијање прати конвенцију апликације (`admin_required`):
     HTML руте → редирект (302) са порукама; није 200.
  3. Админ (и директор, по паритету) виде обједињену страницу са ОБА тока.
  4. Оба тока раде за админа (појединачни са избором запосленог, архивски);
     делови који пишу у базу се прескачу ако PostgreSQL није доступан.

Образац теста прати `test_document_library.py` (test client + искључен CSRF).
"""

import io
import os
import sys
import unittest
from unittest.mock import patch

os.environ.setdefault('FLASK_ENV', 'testing')
os.environ.setdefault('SECRET_KEY', 'test-secret')
os.environ.setdefault('REDIS_URL', '')
os.environ.setdefault('SESSION_TYPE', 'filesystem')
os.environ.setdefault('SESSION_FILE_DIR', 'logs/qa_flask_session')

import app as museum_app

# Фикстура-генератор (није пакет — додајемо фолдер на путању).
_FIXTURES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             'tests', 'fixtures', 'radne_liste')
sys.path.insert(0, _FIXTURES_DIR)
import make_fixtures as mk  # noqa: E402


# Руте увоза које морају бити админ-заштићене.
_GET_ROUTES = ['/admin/timesheet/uvoz', '/timesheet/uvoz', '/admin/timesheet/uvoz-arhiva']
_POST_ROUTES = ['/timesheet/uvoz/pregled', '/timesheet/uvoz/potvrdi',
                '/admin/timesheet/uvoz-arhiva/pregled', '/admin/timesheet/uvoz-arhiva/potvrdi']


def _db_available():
    try:
        from postgres_service import get_postgres_connection
        with get_postgres_connection() as conn, conn.cursor() as cur:
            cur.execute('SELECT 1')
            cur.fetchone()
        return True
    except Exception:
        return False


_DB_OK = _db_available()


class _ClientTestCase(unittest.TestCase):
    def setUp(self):
        museum_app.app.config['TESTING'] = True
        csrf_was_enabled = museum_app.app.config.get('WTF_CSRF_ENABLED', False)
        museum_app.app.config['WTF_CSRF_ENABLED'] = False
        self.addCleanup(
            museum_app.app.config.__setitem__, 'WTF_CSRF_ENABLED', csrf_was_enabled
        )
        module_patch = patch.object(
            museum_app.app, 'user_has_module_access', lambda *a, **k: True
        )
        module_patch.start()
        self.addCleanup(module_patch.stop)
        self.client = museum_app.app.test_client()

    def get(self, *a, **k):
        k.setdefault('base_url', 'https://localhost')
        return self.client.get(*a, **k)

    def post(self, *a, **k):
        k.setdefault('base_url', 'https://localhost')
        return self.client.post(*a, **k)

    def login(self, *, email='user@example.com', role='employee', **extra):
        with self.client.session_transaction() as sess:
            sess['user_id'] = 1
            sess['user_email'] = email
            sess['user_name'] = 'Тест Корисник'
            sess['user_role'] = role
            sess['is_admin'] = role in ('admin', 'direktor')
            for key, value in extra.items():
                sess[key] = value


class EmployeeDeniedTests(_ClientTestCase):
    """Захтеви 1 и 2: запослени нема улаз ни приступ рутама."""

    def test_employee_timesheet_page_has_no_word_import_link(self):
        # Дугме за увоз из Word-а не сме постојати у корисничком приказу.
        if not _DB_OK:
            self.skipTest('PostgreSQL није доступан за рендер корисничке стране')
        self.login(role='employee')
        resp = self.get('/timesheet')
        self.assertEqual(resp.status_code, 200)
        body = resp.get_data(as_text=True)
        self.assertNotIn('Увези из Word', body)
        self.assertNotIn('/timesheet/uvoz', body)

    def test_employee_denied_on_get_routes(self):
        self.login(role='employee')
        for route in _GET_ROUTES:
            resp = self.get(route)
            self.assertNotEqual(resp.status_code, 200,
                                f'{route} не сме бити доступан запосленом')
            self.assertIn(resp.status_code, (302, 303, 403),
                          f'{route}: очекивано одбијање, добијено {resp.status_code}')

    def test_employee_denied_on_post_routes(self):
        self.login(role='employee')
        for route in _POST_ROUTES:
            resp = self.post(route, data={})
            self.assertNotEqual(resp.status_code, 200,
                                f'{route} не сме прихватити POST од запосленог')
            self.assertIn(resp.status_code, (302, 303, 403),
                          f'{route}: очекивано одбијање, добијено {resp.status_code}')

    def test_department_head_denied_on_archive(self):
        # Шеф одељења ГУБИ приступ архивском увозу (сада само админ/директор).
        self.login(role='employee', is_department_head=True)
        resp = self.get('/admin/timesheet/uvoz-arhiva')
        self.assertNotEqual(resp.status_code, 200)
        self.assertIn(resp.status_code, (302, 303, 403))

    def test_anonymous_denied(self):
        for route in _GET_ROUTES:
            resp = self.get(route)
            self.assertNotEqual(resp.status_code, 200)


class AdminAllowedTests(_ClientTestCase):
    """Захтеви 3 и 4: админ/директор виде обједињену страницу и оба тока раде."""

    def test_admin_sees_unified_hub_with_both_flows(self):
        self.login(email='admin@nhmbeo.rs', role='admin')
        resp = self.get('/admin/timesheet/uvoz')
        self.assertEqual(resp.status_code, 200)
        body = resp.get_data(as_text=True)
        # Оба тока присутна на једној страници.
        self.assertIn('/timesheet/uvoz/pregled', body)          # појединачни
        self.assertIn('/admin/timesheet/uvoz-arhiva/pregled', body)  # архивски

    def test_director_sees_unified_hub(self):
        self.login(email='direktor@nhmbeo.rs', role='direktor')
        resp = self.get('/admin/timesheet/uvoz')
        self.assertEqual(resp.status_code, 200)

    def test_legacy_path_redirects_to_hub_for_admin(self):
        self.login(email='admin@nhmbeo.rs', role='admin')
        resp = self.get('/timesheet/uvoz')
        self.assertIn(resp.status_code, (301, 302, 303))
        self.assertIn('/admin/timesheet/uvoz', resp.headers.get('Location', ''))

    @unittest.skipUnless(_DB_OK, 'PostgreSQL није доступан')
    def test_admin_individual_flow_shows_employee_selection(self):
        # Појединачни ток: преглед нуди избор запосленог (мапирање по имену).
        self.login(email='admin@nhmbeo.rs', role='admin')
        docx = mk.build_correct_matrix_days_rows()
        resp = self.post(
            '/timesheet/uvoz/pregled',
            data={'docx': (io.BytesIO(docx.getvalue()), 'lista.docx')},
            content_type='multipart/form-data',
        )
        self.assertEqual(resp.status_code, 200)
        body = resp.get_data(as_text=True)
        self.assertIn('employee_email', body)  # dropdown за избор запосленог
        self.assertIn(str(mk.YEAR), body)

    @unittest.skipUnless(_DB_OK, 'PostgreSQL није доступан')
    def test_admin_archive_flow_dry_run(self):
        # Архивски ток: dry-run извештај без уписа.
        self.login(email='admin@nhmbeo.rs', role='admin')
        docx = mk.build_correct_matrix_days_rows(name='Тест Архива Админ', year=2099)
        resp = self.post(
            '/admin/timesheet/uvoz-arhiva/pregled',
            data={'docx': (io.BytesIO(docx.getvalue()), 'arhiva.docx')},
            content_type='multipart/form-data',
        )
        self.assertEqual(resp.status_code, 200)
        body = resp.get_data(as_text=True)
        self.assertIn('arhiva.docx', body)


if __name__ == '__main__':
    unittest.main()
