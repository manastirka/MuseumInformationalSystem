#!/usr/bin/env python3
"""Обједињена системска страница /admin/sistem (feat/sistem-jedna-stranica).

Проверава:
  1. стара рута без embedded → 302 на /admin/sistem#таб (bookmarks не пуцају);
  2. стара рута са ?embedded=1 → 200, „bare" layout (за iframe таба);
  3. /admin/sistem рендерује хаб са сва четири таба (админ и директор);
  4. ПРАВА НЕПРОМЕЊЕНА: и админ и директор имају приступ (админ-паритет),
     запослени је одбијен на хабу И на старим рутама, и са ?embedded=1
     (embedded не заобилази проверу приступа).
"""

import os
import unittest

os.environ.setdefault('FLASK_ENV', 'testing')
os.environ.setdefault('SECRET_KEY', 'test-secret')
os.environ.setdefault('REDIS_URL', '')
os.environ.setdefault('SESSION_TYPE', 'filesystem')
os.environ.setdefault('SESSION_FILE_DIR', '/tmp/museum-test-flask-session')

import app as museum_app

OLD_ROUTES = {
    '/admin/system-settings': 'podesavanja',
    '/admin/mail-settings': 'posta',
    '/admin/reports': 'izvestaji',
    '/admin/audit-log': 'revizija',
}


class SistemHubTests(unittest.TestCase):
    def setUp(self):
        self.client = museum_app.app.test_client()
        self.base_url = 'https://localhost'

    def _login(self, *, role='admin', email='user@example.com'):
        with self.client.session_transaction() as sess:
            sess['user_id'] = 1
            sess['user_email'] = email
            sess['user_name'] = 'Test User'
            sess['user_role'] = role
            sess['is_admin'] = role == 'admin'

    # --- 1. Old routes redirect to hub tab (no embedded) ---
    def test_old_routes_redirect_to_hub_for_admin(self):
        self._login(role='admin')
        for path, tab in OLD_ROUTES.items():
            resp = self.client.get(path, base_url=self.base_url)
            self.assertEqual(resp.status_code, 302, path)
            self.assertIn('/admin/sistem', resp.headers['Location'], path)
            self.assertTrue(resp.headers['Location'].endswith('#' + tab), path)

    def test_old_routes_redirect_to_hub_for_director(self):
        self._login(role='direktor')
        for path, tab in OLD_ROUTES.items():
            resp = self.client.get(path, base_url=self.base_url)
            self.assertEqual(resp.status_code, 302, path)
            self.assertIn('/admin/sistem', resp.headers['Location'], path)

    # --- 2. Embedded renders content (bare layout) ---
    def test_embedded_renders_bare_content(self):
        self._login(role='admin')
        for path in OLD_ROUTES:
            resp = self.client.get(path + '?embedded=1', base_url=self.base_url)
            self.assertEqual(resp.status_code, 200, path)
            body = resp.get_data(as_text=True)
            self.assertIn('embedded-shell', body, path)  # bare layout marker

    # --- 3. Hub renders with all four tabs for admin and director ---
    def test_hub_renders_all_tabs_for_admin(self):
        self._login(role='admin')
        resp = self.client.get('/admin/sistem', base_url=self.base_url)
        self.assertEqual(resp.status_code, 200)
        body = resp.get_data(as_text=True)
        for tab in ('tab-podesavanja', 'tab-posta', 'tab-izvestaji', 'tab-revizija'):
            self.assertIn(tab, body)

    def test_hub_renders_all_tabs_for_director(self):
        self._login(role='direktor')
        resp = self.client.get('/admin/sistem', base_url=self.base_url)
        self.assertEqual(resp.status_code, 200)
        body = resp.get_data(as_text=True)
        # Director has admin parity → sees all four tabs (permissions unchanged)
        for tab in ('tab-podesavanja', 'tab-posta', 'tab-izvestaji', 'tab-revizija'):
            self.assertIn(tab, body)

    # --- 4. Permissions unchanged: employee denied everywhere ---
    def test_employee_denied_on_hub(self):
        self._login(role='employee')
        resp = self.client.get('/admin/sistem', base_url=self.base_url)
        self.assertEqual(resp.status_code, 302)  # page route → dashboard redirect
        self.assertIn('/dashboard', resp.headers['Location'])

    def test_employee_denied_on_old_routes_even_embedded(self):
        self._login(role='employee')
        for path in OLD_ROUTES:
            resp = self.client.get(path + '?embedded=1', base_url=self.base_url)
            self.assertEqual(resp.status_code, 302, path)
            self.assertIn('/dashboard', resp.headers['Location'], path)
            body = resp.get_data(as_text=True)
            self.assertNotIn('embedded-shell', body, path)  # no content leaked


if __name__ == '__main__':
    unittest.main()
