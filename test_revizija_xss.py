"""Revizija 2026-08, stavka 5: preostali XSS.

1) admin_timesheet_reports.html — ime zaposlenog je išlo sirovo u inline
   onclick JS string; HTML escape u atributu NE štiti JS string (browser
   prvo dekodira entitete), pa ime sa navodnikom beži iz stringa. Test
   renderuje PRAVU stranicu sa payload imenom i proverava izgled odgovora.
2) admin_collection_database.html — vrednosti iz baze idu u innerHTML kroz
   template literale; svaka interpolacija mora kroz esc() helper.
"""

import os
import re
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

os.environ.setdefault('FLASK_ENV', 'testing')
os.environ.setdefault('SECRET_KEY', 'test-secret')
os.environ.setdefault('REDIS_URL', '')
os.environ.setdefault('SESSION_TYPE', 'filesystem')
os.environ.setdefault('SESSION_FILE_DIR', '/tmp/museum-test-revizija-xss')

import app as museum_app

XSS_NAME = "<img src=x onerror=alert(1)>'Петровић"
BIOLOGY = 'Одељење за биологију'


class TimesheetReportsXssTests(unittest.TestCase):
    """Payload u imenu zaposlenog ne sme da se pojavi sirov u odgovoru, a
    dugmad ne smeju da nose ime u inline onclick JS stringu."""

    def setUp(self):
        self._prev_csrf = museum_app.app.config.get('WTF_CSRF_ENABLED', False)
        museum_app.app.config['WTF_CSRF_ENABLED'] = False
        self.client = museum_app.app.test_client()

    def tearDown(self):
        museum_app.app.config['WTF_CSRF_ENABLED'] = self._prev_csrf

    def test_ime_sa_payloadom_je_escapovano_u_odgovoru(self):
        fake_repo = MagicMock()
        fake_repo.available = True
        common = {
            'month': 4, 'year': 2026, 'organization_unit': '',
            'is_verified': False, 'is_locked': True, 'status': 'SUBMITTED',
            'work_in_museum': 0, 'work_outside': 0, 'vacation': 0,
            'public_holiday': 0, 'paid_leave': 0, 'other_leave': 0,
            'sick_lt30': 0, 'sick_gte30': 0, 'total_hours': 0,
        }
        fake_repo.list_reports.return_value = {
            'reports': [dict(id=801, employee_name=XSS_NAME, **common)],
            'total': 1, 'page': 1, 'total_pages': 1,
        }
        fake_repo.get_month_summary.return_value = None
        fake_repo.get_overall_summary.return_value = None

        report_meta = [
            {'id': 801, 'employee_email': 'bio@nhmbeo.rs',
             'employee_department': BIOLOGY},
        ]
        heads_rows = [{'department': BIOLOGY,
                       'head_email': 'verica.stojanovic@nhmbeo.rs'}]

        class _Cur:
            def __init__(self):
                self._pending = None

            def execute(self, sql, params=None):
                if 'FROM timesheet_reports tr' in sql:
                    self._pending = report_meta
                elif 'FROM users u' in sql:
                    self._pending = heads_rows
                else:
                    self._pending = None

            def fetchall(self):
                return self._pending or []

            def fetchone(self):
                return (self._pending or [None])[0]

            def __enter__(self):
                return self

            def __exit__(self, *a):
                return False

        class _Conn:
            def cursor(self):
                return _Cur()

            def __enter__(self):
                return self

            def __exit__(self, *a):
                return False

        with self.client.session_transaction() as sess:
            sess['user_id'] = 27
            sess['user_email'] = 'verica.stojanovic@nhmbeo.rs'
            sess['user_role'] = 'sef_odeljenja'
            sess['user_department'] = BIOLOGY
            sess['is_department_head'] = True

        with patch('timesheet_admin_views.get_postgres_connection',
                   lambda **kw: _Conn()), \
             patch.object(museum_app, 'timesheet_repository', fake_repo):
            r = self.client.get('/admin/timesheet_reports',
                                base_url='https://localhost')

        self.assertEqual(r.status_code, 200)
        body = r.get_data(as_text=True)
        # Sirov payload ne sme NIGDE u odgovoru.
        self.assertNotIn('<img src=x onerror=', body)
        # Ime se pojavljuje, ali escapovano.
        self.assertIn('&lt;img src=x onerror=', body)
        # Ime ne sme u inline onclick JS string (mehanizam bekstva).
        self.assertNotIn('onclick="deleteReport(', body)
        self.assertNotIn('onclick="returnReportToEmployee(', body)
        # Dugme nosi ime u data-atributu (auto-escape ga pokriva).
        self.assertIn('data-employee-name="&lt;img src=x onerror=', body)


class CollectionDatabaseTemplateGuardTests(unittest.TestCase):
    """innerHTML interpolacije u admin_collection_database.html moraju kroz
    esc(); ovaj test čuva da se sirova interpolacija ne vrati."""

    @classmethod
    def setUpClass(cls):
        cls.src = (Path(__file__).parent / 'templates'
                   / 'admin_collection_database.html').read_text(encoding='utf-8')

    def test_esc_helper_postoji_i_pokriva_navodnike(self):
        self.assertIn('function esc(', self.src)
        self.assertIn('&quot;', self.src)
        self.assertIn('&#39;', self.src)

    def test_detail_polja_idu_kroz_esc(self):
        raw = re.findall(r'detail-field-(?:label|value)">\$\{(?!esc\()', self.src)
        self.assertEqual(raw, [], 'detail polje interpolira vrednost bez esc()')
        self.assertIn('detail-field-value">${esc(', self.src)

    def test_celije_tabele_idu_kroz_esc_ili_textcontent(self):
        self.assertNotIn('td.innerHTML = value;', self.src)
        self.assertIn('td.textContent = value', self.src)
        raw_badge = re.findall(
            r'<span class="badge[^"]*">\$\{(?!esc\()', self.src)
        self.assertEqual(raw_badge, [], 'badge interpolira vrednost bez esc()')

    def test_slika_koristi_encodeuricomponent_i_esc(self):
        self.assertNotIn('src="${imgUrl}"', self.src)
        self.assertIn('src="${esc(imgUrl)}"', self.src)
        self.assertIn('encodeURIComponent(entityId)', self.src)


if __name__ == '__main__':
    unittest.main()
