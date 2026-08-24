#!/usr/bin/env python3
"""Тестови OGK слоја тачака (OGK SFRJ 1:100 000) — подаци, скрипта и API.

Покретање:
    python -m pytest test_ogk_points_layer.py -q
"""

import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

os.environ.setdefault('FLASK_ENV', 'testing')
os.environ.setdefault('SECRET_KEY', 'test-secret')
os.environ.setdefault('REDIS_URL', '')
os.environ.setdefault('SESSION_TYPE', 'filesystem')
os.environ.setdefault('SESSION_FILE_DIR', 'logs/qa_flask_session')
os.environ.setdefault('WTF_CSRF_ENABLED', 'False')

import pytest  # noqa: E402

import app as museum_app  # noqa: E402

museum_app.app.config['TESTING'] = True
museum_app.app.config['WTF_CSRF_ENABLED'] = False

BASE = 'https://localhost'
KOREN = Path(__file__).resolve().parent
JSON_PUTANJA = KOREN / 'data' / 'ogk_points.json'
SKRIPTA = KOREN / 'scripts' / 'import_export' / 'build_ogk_points.py'

UKUPNO = 2334
OCEKIVANE_GRUPE = {
    'rudnici': 820,
    'kamenolomi': 328,
    'busotine': 188,
    'izvori': 103,
    'fosili': 146,
    'rasedi': 297,
    'jedinice': 420,
    'ostalo': 32,
}

# Границе Србије — исте као у build_ogk_points.py.
LAT_MIN, LAT_MAX = 41.5, 46.5
LON_MIN, LON_MAX = 18.5, 23.5


@pytest.fixture(scope='module')
def podaci():
    with open(JSON_PUTANJA, encoding='utf-8') as handle:
        return json.load(handle)


def _hes(putanja):
    return hashlib.sha256(Path(putanja).read_bytes()).hexdigest()


def _klijent(prijavljen=True):
    client = museum_app.app.test_client()
    if prijavljen:
        with client.session_transaction() as sesija:
            sesija['user_id'] = 990601
            sesija['user_email'] = 'ogk.tester@example.invalid'
            sesija['user_name'] = 'ОГК Тестер'
            sesija['user_role'] = 'employee'
            sesija['user_department'] = 'Природњачки музеј'
            sesija['is_admin'] = False
    return client


# --- Скрипта -----------------------------------------------------------------

def test_dry_run_ne_menja_nista_na_disku():
    """--dry-run сме само да испише бројеве; фајл мора остати бајт-исти."""
    pre = _hes(JSON_PUTANJA)
    pre_mtime = JSON_PUTANJA.stat().st_mtime_ns
    ishod = subprocess.run(
        [sys.executable, str(SKRIPTA), '--dry-run'],
        cwd=str(KOREN), capture_output=True, text=True, timeout=300,
    )
    assert ishod.returncode == 0, ishod.stderr
    assert _hes(JSON_PUTANJA) == pre, '--dry-run је изменио data/ogk_points.json'
    # Скрипта је идемпотентна, па би упис истог садржаја прошао кроз хеш —
    # mtime хвата и такав „безазлен“ упис.
    assert JSON_PUTANJA.stat().st_mtime_ns == pre_mtime, \
        '--dry-run је уписивао у data/ogk_points.json'

    izlaz = ishod.stdout
    for grupa, broj in OCEKIVANE_GRUPE.items():
        assert grupa in izlaz, 'група {} није исписана'.format(grupa)
        assert str(broj) in izlaz, 'број за {} није исписан'.format(grupa)
    # Одбачени редови се никад не гутају тихо.
    assert 'ОДБАЧЕНО' in izlaz


# --- Подаци ------------------------------------------------------------------

def test_json_ima_tacno_2334_tacke(podaci):
    assert podaci['ukupno'] == UKUPNO
    assert len(podaci['tacke']) == UKUPNO
    assert podaci['izvor'] == 'OGK SFRJ 1:100 000'
    assert podaci['generisano']


def test_brojevi_po_grupi_su_ocekivani(podaci):
    assert podaci['grupe'] == OCEKIVANE_GRUPE
    stvarno = {}
    for tacka in podaci['tacke']:
        stvarno[tacka['grupa']] = stvarno.get(tacka['grupa'], 0) + 1
    assert stvarno == OCEKIVANE_GRUPE


def test_sve_koordinate_su_brojevi_unutar_granica_srbije(podaci):
    for tacka in podaci['tacke']:
        lat = tacka['lat']
        lon = tacka['lon']
        assert lat is not None and lon is not None, tacka['id']
        assert isinstance(lat, (int, float)) and isinstance(lon, (int, float)), tacka['id']
        assert LAT_MIN <= lat <= LAT_MAX, (tacka['id'], lat)
        assert LON_MIN <= lon <= LON_MAX, (tacka['id'], lon)


def test_iskljucene_kategorije_nisu_u_izlazu(podaci):
    zabranjene = {'naselje', 'hidrografija', 'reljef'}
    nadjene = {t['kategorija'] for t in podaci['tacke']} & zabranjene
    assert not nadjene, 'OSM подлога већ даје: {}'.format(nadjene)


# --- API ---------------------------------------------------------------------

def test_api_vraca_stvarne_tacke():
    odgovor = _klijent().get('/api/map/ogk-points', base_url=BASE)
    assert odgovor.status_code == 200, odgovor.get_data(as_text=True)
    telo = odgovor.get_json()
    assert telo['success'] is True

    tacke = telo['data']['tacke']
    assert len(tacke) == UKUPNO
    assert telo['data']['ukupno'] == UKUPNO
    assert telo['data']['grupe'] == OCEKIVANE_GRUPE
    assert tacke[0]['naziv'].strip(), 'прва тачка нема назив'
    assert tacke[0]['lat'] is not None and tacke[0]['lon'] is not None


def test_api_filtrira_grupe_na_serveru():
    odgovor = _klijent().get('/api/map/ogk-points?grupe=busotine', base_url=BASE)
    assert odgovor.status_code == 200
    podaci_api = odgovor.get_json()['data']
    assert len(podaci_api['tacke']) == 188
    assert podaci_api['ukupno'] == 188
    assert {t['grupa'] for t in podaci_api['tacke']} == {'busotine'}


def test_api_nepoznata_grupa_nije_tiho_prazan_sloj():
    odgovor = _klijent().get('/api/map/ogk-points?grupe=izmisljena', base_url=BASE)
    assert odgovor.status_code == 400
    assert odgovor.get_json()['success'] is False


def test_neautentifikovan_zahtev_ne_dobija_podatke():
    odgovor = _klijent(prijavljen=False).get('/api/map/ogk-points', base_url=BASE)
    assert odgovor.status_code != 200, 'непријављен корисник је добио 200'
    telo = odgovor.get_data(as_text=True)
    assert 'tacke' not in telo
    assert 'K34-' not in telo


def test_strana_karte_nosi_prekidace_ogk_grupa():
    client = museum_app.app.test_client()
    with client.session_transaction() as sesija:
        sesija['user_id'] = 990602
        sesija['user_email'] = 'ogk.admin@example.invalid'
        sesija['user_name'] = 'ОГК Админ'
        sesija['user_role'] = 'admin'
        sesija['user_department'] = 'Природњачки музеј'
        sesija['is_admin'] = True

    odgovor = client.get('/admin/maps', base_url=BASE)
    assert odgovor.status_code == 200
    html = odgovor.get_data(as_text=True)
    for grupa, broj in OCEKIVANE_GRUPE.items():
        assert 'id="toggle-ogk-{}"'.format(grupa) in html
        # Бејџ носи стварни број тачака, отпочетка (без додатног захтева).
        assert 'data-ogk-broj="{}">{}<'.format(grupa, broj) in html


if __name__ == '__main__':
    sys.exit(pytest.main([__file__, '-q']))
