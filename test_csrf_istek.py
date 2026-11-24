#!/usr/bin/env python3
"""Истекао CSRF токен (прод лог 23.11.2026: „The CSRF token has expired“).

Подразумевано токен важи колико и сесија (WTF_CSRF_TIME_LIMIT=None); ако је
рок ипак задат и токен истекне: HTML образац → флеш + повратак на исту страну
без губитка сесије, AJAX → 400 {error: csrf_expired, csrf_token: нови}, а
поновљени захтев са новим токеном уписује у базу.
"""
import os
import subprocess
import sys
import time
from pathlib import Path
from unittest import mock

from flask import session
from flask_wtf.csrf import generate_csrf
from itsdangerous import TimestampSigner

from test_udzbenik import BAZA, EMAIL, _Osnova, _upit, _uvezi_primer
import app as museum_app

KOREN = Path(__file__).resolve().parent
SIROVI = 'f' * 40
TELO = {'zbirka': 'minerali', 'poglavlje': 'kristalografija', 'lekcija': 'kristalni-sistemi',
        'zavrseno': True, 'rezultat': None}


def _token(starost_s=0):
    with museum_app.app.test_request_context():
        session['csrf_token'] = SIROVI
        with mock.patch.object(TimestampSigner, 'get_timestamp', return_value=int(time.time()) - starost_s):
            return generate_csrf()


def _rok_u_podesavanjima(vrednost):
    """Config.WTF_CSRF_TIME_LIMIT za zadatu .env vrednost (None = nije zadato)."""
    env = {k: v for k, v in os.environ.items() if k != 'WTF_CSRF_TIME_LIMIT'}
    if vrednost is not None:
        env['WTF_CSRF_TIME_LIMIT'] = vrednost
    r = subprocess.run([sys.executable, '-c', 'import config; print(repr(config.Config.WTF_CSRF_TIME_LIMIT))'],
                       cwd=KOREN, env=env, capture_output=True, text=True, check=True)
    return r.stdout.strip()


class PodesavanjeTest(_Osnova):
    def test_podrazumevano_bez_roka(self):
        self.assertEqual(_rok_u_podesavanjima(None), 'None')
        self.assertEqual(_rok_u_podesavanjima(''), 'None')

    def test_rok_i_dalje_kroz_env(self):
        self.assertEqual(_rok_u_podesavanjima('7200'), '7200')
        self.assertEqual(_rok_u_podesavanjima('3600  # 1 hour'), '3600')

    def test_env_example_ne_zadaje_rok(self):
        redovi = (KOREN / '.env.example').read_text(encoding='utf-8').splitlines()
        self.assertFalse([r for r in redovi if r.startswith('WTF_CSRF_TIME_LIMIT=')])


class IstekTest(_Osnova):
    def setUp(self):
        super().setUp()
        _uvezi_primer()
        self._prijava()
        with self.client.session_transaction() as sess:
            sess['csrf_token'] = SIROVI
        cfg = museum_app.app.config
        for kljuc, vrednost in (('WTF_CSRF_ENABLED', True), ('WTF_CSRF_TIME_LIMIT', 3600)):
            self.addCleanup(cfg.__setitem__, kljuc, cfg.get(kljuc))
            cfg[kljuc] = vrednost

    def _redovi(self):
        return _upit("""SELECT n.user_email, l.slug, n.zavrseno FROM udzbenik_napredak n
                        JOIN udzbenik_lekcija l ON l.id = n.lekcija_id WHERE n.user_email = %s""", (EMAIL,))

    def _ajax(self, token):
        return self.post_json('/api/udzbenik/napredak', TELO, headers={'X-CSRFToken': token, 'Referer': BAZA + '/udzbenik'})

    def test_bez_roka_star_token_vazi(self):
        museum_app.app.config['WTF_CSRF_TIME_LIMIT'] = None
        r = self._ajax(_token(starost_s=6 * 3600))
        self.assertEqual(r.status_code, 200, r.get_data(as_text=True))
        self.assertEqual(self._redovi(), [(EMAIL, 'kristalni-sistemi', True)])

    def test_ajax_istekao_pa_ponovljen_sa_novim_upisuje(self):
        r = self._ajax(_token(starost_s=2 * 3600))
        self.assertEqual(r.status_code, 400)
        d = r.get_json()
        self.assertEqual(d['error'], 'csrf_expired')
        self.assertTrue(d['csrf_token'])
        self.assertEqual(self._redovi(), [])
        r2 = self._ajax(d['csrf_token'])
        self.assertEqual(r2.status_code, 200, r2.get_data(as_text=True))
        self.assertEqual(self._redovi(), [(EMAIL, 'kristalni-sistemi', True)])

    def test_ajax_pogresan_token_csrf_invalid(self):
        r = self._ajax('nije-token')
        self.assertEqual(r.status_code, 400)
        self.assertEqual(r.get_json()['error'], 'csrf_invalid')
        self.assertEqual(self._redovi(), [])

    def test_html_istekao_redirekt_flesh_sesija_ostaje(self):
        povratak = BAZA + '/udzbenik'
        r = self.client.post('/set_theme', base_url=BAZA, data={'csrf_token': _token(starost_s=2 * 3600)},
                             headers={'Referer': povratak, 'Accept': 'text/html,application/xhtml+xml'})
        self.assertEqual(r.status_code, 302)
        self.assertEqual(r.headers['Location'], povratak)
        with self.client.session_transaction() as sess:
            self.assertEqual(sess.get('user_email'), EMAIL)
            poruke = [p for _, p in sess.get('_flashes', [])]
        self.assertIn('Страница је била предуго отворена, освежена је – пошаљите поново.', poruke)
        self.assertEqual(self.get('/udzbenik').status_code, 200)

    def test_html_tudj_referrer_ne_vodi_napolje(self):
        r = self.client.post('/set_theme', base_url=BAZA, data={'csrf_token': _token(starost_s=2 * 3600)},
                             headers={'Referer': 'https://zlo.example/x', 'Accept': 'text/html'})
        self.assertEqual(r.status_code, 302)
        self.assertNotIn('zlo.example', r.headers['Location'])


class SablonTest(_Osnova):
    def test_base_ucitava_obnovu_i_token_je_promenljiv(self):
        for ime in ('base.html', 'base_embedded.html'):
            tekst = (KOREN / 'templates' / ime).read_text(encoding='utf-8')
            self.assertIn("js/csrf_obnova.js", tekst, ime)
            self.assertLess(tekst.index('csrf_obnova.js'), tekst.index('</head>'), ime)
            self.assertIn('let CSRF_TOKEN', tekst, ime)
