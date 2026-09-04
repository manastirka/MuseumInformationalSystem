"""Заједничко заглавље стране (макро zaglavlje): структура, бројач, радње,
и да су hero блокови из шаблона стварно замењени."""
import os
import re
import unittest
from pathlib import Path

os.environ.setdefault('FLASK_ENV', 'testing')
os.environ.setdefault('SECRET_KEY', 'test-secret')
os.environ.setdefault('REDIS_URL', '')
os.environ.setdefault('SESSION_TYPE', 'filesystem')
os.environ.setdefault('SESSION_FILE_DIR', 'logs/qa_flask_session')

import app as museum_app  # noqa: E402

KOREN = Path(__file__).resolve().parent


def _render(izvor, **ctx):
    with museum_app.app.test_request_context('/'):
        return museum_app.app.jinja_env.from_string(izvor).render(**ctx)


class ZaglavljeMakroTest(unittest.TestCase):
    def test_osnovno_zaglavlje(self):
        html = _render("{% from '_zaglavlje_strane.html' import zaglavlje %}"
                       "{{ zaglavlje('База библиотеке', 'Каталог', ikona='bi-book', brojac=598, brojac_naziv='књига') }}")
        self.assertIn('class="zaglavlje page-hero"', html)
        self.assertIn('<i class="bi bi-book"', html)
        self.assertIn('<span>База библиотеке</span>', html)
        self.assertIn('zaglavlje__podnaslov">Каталог<', html)
        self.assertIn('zaglavlje__broj">598<', html)
        self.assertNotIn('zaglavlje__radnje', html)

    def test_radnje_i_nazad(self):
        html = _render("{% from '_zaglavlje_strane.html' import zaglavlje %}"
                       "{% call zaglavlje('Наслов', nazad='/x', nazad_tekst='Назад на базе') %}"
                       "<a class=\"btn btn-light\" href=\"/dodaj\">Додај</a>{% endcall %}")
        self.assertIn('zaglavlje__radnje', html)
        self.assertLess(html.index('href="/dodaj"'), html.index('href="/x"'), 'примарна радња пре „Назад“')
        self.assertIn('btn btn-outline-light" href="/x"', html.replace('href="/x" class="btn btn-outline-light"', 'btn btn-outline-light" href="/x"'))

    def test_bez_brojaca_kad_je_none_ili_prazno(self):
        for v in ('None', "''"):
            html = _render("{% from '_zaglavlje_strane.html' import zaglavlje %}{{ zaglavlje('X', brojac=" + v + ") }}")
            self.assertNotIn('zaglavlje__brojac', html, v)

    def test_puna_klasa_ikone_i_slika(self):
        html = _render("{% from '_zaglavlje_strane.html' import zaglavlje %}"
                       "{{ zaglavlje('X', ikona='museum-icon-bird', slika='/s.png', slika_alt='Лого') }}")
        self.assertIn('<i class="museum-icon-bird"', html)
        self.assertIn('class="zaglavlje__slika" src="/s.png" alt="Лого"', html)

    def test_naslov_se_eskejpuje(self):
        html = _render("{% from '_zaglavlje_strane.html' import zaglavlje %}{{ zaglavlje(n) }}", n='<b>x</b>')
        self.assertIn('&lt;b&gt;x&lt;/b&gt;', html)


class ZaglavljePrimenaTest(unittest.TestCase):
    def test_stari_hero_blokovi_zamenjeni(self):
        # Стари образац: Bootstrap картица bg-* + db-hero/page-hero на странама база и администрације.
        stari = re.compile(r'<div class="card bg-\w+ text-\w+ (?:db-hero|page-hero)"')
        preostali = sorted(p.name for p in (KOREN / 'templates').glob('*.html')
                           if stari.search(p.read_text(encoding='utf-8', errors='ignore')))
        # Изузетака више нема: све стране иду кроз макро _zaglavlje_strane.html.
        self.assertEqual(preostali, [], preostali)

    def test_kljucne_strane_koriste_makro(self):
        for ime in ('admin_collection_database.html', 'admin_mineral_collection.html', 'admin_library_database.html',
                    'admin_employees_database.html', 'fototeka_galerija.html', 'admin_bird_ringing_database.html',
                    'admin_timesheet_reports.html', 'admin_museum_databases.html'):
            t = (KOREN / 'templates' / ime).read_text(encoding='utf-8', errors='ignore')
            if ime == 'admin_museum_databases.html':
                continue  # преглед база задржава своје заглавље са претрагом
            self.assertIn("import zaglavlje", t, ime)
            self.assertIn('zaglavlje(', t, ime)

    def test_css_makroa_u_main(self):
        css = (KOREN / 'static' / 'css' / 'main.css').read_text(encoding='utf-8')
        for sel in ('.zaglavlje {', '.zaglavlje__brojac {', '.zaglavlje__radnje {',
                    '.page-hero.zaglavlje .btn-outline-light', '.login-header {'):
            self.assertIn(sel, css, sel)

    def test_meteoriti_sazet_podrazumevani_prikaz(self):
        t = (KOREN / 'templates' / 'admin_collection_database.html').read_text(encoding='utf-8')
        blok = re.search(r"meteorite: \[(.*?)\]", t, re.S).group(1)
        kolone = re.findall(r"'([a-z_]+)'", blok)
        self.assertLessEqual(len(kolone), 8, kolone)
        self.assertIn('catalog_number', kolone)
        self.assertIn('fall_location', kolone)
        self.assertIn("meteorite: '2026-09-04-meteorite-sazeto'", t)


if __name__ == '__main__':
    unittest.main()
