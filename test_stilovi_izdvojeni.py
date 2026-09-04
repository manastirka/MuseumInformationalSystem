#!/usr/bin/env python3
"""Издвојени CSS и фонтови: шаблони не носе велике <style> блокове тамо где
је стил већ у static/css/, а страна учитава само фонтове свог стила."""
import glob
import os
import re
import unittest

os.environ.setdefault('FLASK_ENV', 'testing')
os.environ.setdefault('SECRET_KEY', 'test-secret')
os.environ.setdefault('REDIS_URL', '')
os.environ.setdefault('SESSION_TYPE', 'filesystem')
os.environ.setdefault('SESSION_FILE_DIR', 'logs/qa_flask_session')

import app as museum_app  # noqa: E402
import statika  # noqa: E402

IZDVOJENI = ('templates/base.html', 'templates/_odobravanje_style.html',
             'templates/podesavanja_izgled.html', 'templates/admin_nhm_data_portal.html',
             'templates/fototeka_galerija.html')
CSS_FAJLOVI = ('static/css/base.css', 'static/css/strane/odobravanje.css',
               'static/css/strane/podesavanja_izgled.css', 'static/css/strane/nhm_data_portal.css',
               'static/css/strane/fototeka_galerija.css')


def _tekst(p):
    return open(p, encoding='utf-8').read()


class IzdvajanjeTest(unittest.TestCase):
    def test_css_fajlovi_postoje_i_nisu_prazni(self):
        for p in CSS_FAJLOVI:
            self.assertGreater(len(_tekst(p).splitlines()), 40, p)

    def test_sabloni_vise_nemaju_velike_stilove(self):
        for p in IZDVOJENI:
            for blok in re.findall(r'<style[^>]*>(.*?)</style>', _tekst(p), re.S):
                self.assertLess(len(blok.splitlines()), 40, '%s још има велики <style>' % p)

    def test_link_na_izdvojeni_css_sa_verzijom(self):
        for p in IZDVOJENI:
            t = _tekst(p)
            self.assertIn('css/base.css' if p.endswith('base.html') else 'css/strane/', t)
            self.assertIn('v_statike(', t, p)

    def test_verzija_statike_je_mtime(self):
        self.assertIsInstance(statika.verzija_statike('css/main.css'), int)
        self.assertGreater(statika.verzija_statike('css/main.css'), 0)
        self.assertGreater(statika.verzija_statike('css/nema-ovoga.css'), 0)


class SviSabloniTest(unittest.TestCase):
    """Правило за убудуће: велики CSS иде у static/css/, не у шаблон."""

    def test_nijedan_sablon_nema_veliki_stil_bez_jinja(self):
        krivci = []
        for p in sorted(glob.glob('templates/*.html')):
            for blok in re.findall(r'<style[^>]*>(.*?)</style>', _tekst(p), re.S):
                if len(blok.splitlines()) >= 40 and '{{' not in blok and '{%' not in blok:
                    krivci.append(p)
        self.assertEqual(krivci, [], 'CSS блок дужи од 40 линија премести у static/css/strane/')

    def test_svaki_link_pokazuje_na_postojeci_fajl(self):
        veze = 0
        for p in sorted(glob.glob('templates/*.html')):
            for ime in re.findall(r"filename='css/strane/([\w.-]+\.css)'", _tekst(p)):
                veze += 1
                self.assertTrue(os.path.exists('static/css/strane/' + ime), '%s: нема %s' % (p, ime))
        self.assertGreater(veze, 40, 'очекујемо десетине издвојених страна')

    def test_link_ne_zavrsava_u_skripti_ili_komentaru(self):
        for p in sorted(glob.glob('templates/*.html')):
            t = _tekst(p)
            opsezi = [(m.start(), m.end()) for m in re.finditer(r'<script\b.*?</script>', t, re.S)]
            opsezi += [(m.start(), m.end()) for m in re.finditer(r'<!--.*?-->', t, re.S)]
            opsezi += [(m.start(), m.end()) for m in re.finditer(r'\{#.*?#\}', t, re.S)]
            for m in re.finditer(r"filename='css/strane/[\w.-]+\.css'", t):
                self.assertFalse(any(a <= m.start() < b for a, b in opsezi),
                                 '%s: <link> унутар скрипте или коментара' % p)


class FontoviTest(unittest.TestCase):
    def setUp(self):
        self.client = museum_app.app.test_client()

    def _strana(self):
        with self.client.session_transaction() as sess:
            sess.update({'user_id': 1, 'user_email': 'fontovi@example.invalid',
                         'user_role': 'admin', 'is_admin': True})
        return self.client.get('/login', base_url='https://localhost').get_data(as_text=True)

    def test_ucitava_se_najvise_dve_porodice(self):
        html = self._strana()
        veze = re.findall(r'fonts\.googleapis\.com/css2\?([^"]+)', html)
        self.assertEqual(len(veze), 1, 'тачно једна веза ка Google Fonts')
        self.assertLessEqual(veze[0].count('family='), 2, 'највише две породице по страни')
        self.assertIn('Inter', veze[0])

    def test_nijedan_sablon_ne_ucitava_fontove_mimo_ukljucka(self):
        for p in glob.glob('templates/*.html'):
            if p.endswith('_fontovi.html'):
                continue
            self.assertNotIn('fonts.googleapis.com', _tekst(p), p)

    def test_ukljucak_pokriva_sve_stilove(self):
        t = _tekst('templates/_fontovi.html')
        for stil in ('institucionalna', 'moderna', 'arhivska', 'terenska'):
            self.assertIn("'%s'" % stil, t)


if __name__ == '__main__':
    unittest.main()
