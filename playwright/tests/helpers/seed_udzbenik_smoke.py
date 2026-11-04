#!/usr/bin/env python3
"""Seed/clean тест-уџбеника ``udztest-smoke`` за Playwright smoke мотора
(udzbenik-smoke.spec.js): једна лекција са блоком ``literatura`` (на dev-у
SciSearch није повезан, па мотор мора да покаже сиви блок „недоступан“) и
faznim дијаграмом. Пише кроз scripts/udzbenik_uvoz.py (валидација шемом), не
дира прави садржај.

Usage: python seed_udzbenik_smoke.py seed|clean
"""
import importlib.util
import json
import os
import sys
import tempfile

KOREN = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
sys.path.insert(0, KOREN)

ZBIRKA = 'udztest-smoke'
POGLAVLJE = 'smoke'
LEKCIJA = 'literatura-i-dijagram'

SADRZAJ = {
    'verzija': 1,
    'udzbenik': {'zbirka': ZBIRKA, 'naslov': 'Smoke уџбеник (тест)',
                 'opis': 'Привремени садржај за Playwright smoke мотора.', 'status': 'nacrt', 'javno': False},
    'poglavlja': [{
        'slug': POGLAVLJE, 'naslov': 'Smoke', 'redosled': 1,
        'lekcije': [{
            'slug': LEKCIJA, 'naslov': 'Литература и дијаграм', 'redosled': 1, 'status': 'nacrt',
            'sazetak': 'Блок literatura и фазни дијаграм за smoke тест.',
            'sadrzaj': {'verzija': 1, 'blokovi': [
                {'id': 'uvod', 'tip': 'tekst', 'markdown': 'Smoke тест мотора уџбеника.'},
                {'id': 'lit', 'tip': 'literatura', 'upit': 'пирит', 'broj': 3, 'naslov': 'Пирит у литератури'},
                {'id': 'faze', 'tip': 'dijagram', 'dijagram': 'fazni-dijagram',
                 'parametri': {'sistem': 'SiO2', 'tacka': {'T_C': 900, 'P_GPa': 0.5}},
                 'opis_za_citac': 'Фазни дијаграм SiO2 са покретном тачком притиска и температуре.'},
            ]},
        }],
    }],
}


def _uvoz():
    spec = importlib.util.spec_from_file_location('udzbenik_uvoz', os.path.join(KOREN, 'scripts', 'udzbenik_uvoz.py'))
    modul = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modul)
    return modul


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else 'seed'
    from postgres_service import get_postgres_connection
    with get_postgres_connection() as conn:
        with conn.cursor() as cur:
            cur.execute('DELETE FROM udzbenik WHERE zbirka = %s', (ZBIRKA,))
        conn.commit()
    if mode == 'clean':
        print('CLEANED')
        return 0
    uvoz = _uvoz()
    with tempfile.NamedTemporaryFile('w', suffix='.json', delete=False, encoding='utf-8') as f:
        json.dump(SADRZAJ, f, ensure_ascii=False)
        putanja = f.name
    try:
        kod = uvoz.main(['--fajl', putanja, '--execute', uvoz.POTVRDA])
    finally:
        os.unlink(putanja)
    if kod == 0:
        print(f'SEEDED /udzbenik/{ZBIRKA}/{POGLAVLJE}/{LEKCIJA}')
    return kod


if __name__ == '__main__':
    sys.exit(main())
