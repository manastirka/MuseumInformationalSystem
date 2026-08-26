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

import maps_layer_views  # noqa: E402

BASE = 'https://localhost'
KOREN = Path(__file__).resolve().parent
JSON_PUTANJA = KOREN / 'data' / 'ogk_points.json'
SKRIPTA = KOREN / 'scripts' / 'import_export' / 'build_ogk_points.py'
RADOVI_PUTANJA = KOREN / 'data' / 'ogk_radovi.json'
SKRIPTA_RADOVI = KOREN / 'scripts' / 'import_export' / 'build_ogk_radovi.py'

UKUPNO = 2334
# Жетва по имену локалитета: 628 локалитета, 2203 рада, од тога 884 са
# геолошким појмом у наслову/часопису/апстракту и 1319 пуких помена назива.
RADOVI_LOKALITETA = 628
RADOVI_UKUPNO = 2203
RADOVI_GEO = 884
RADOVI_NE_GEO = RADOVI_UKUPNO - RADOVI_GEO
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


@pytest.fixture(scope='module')
def radovi():
    with open(RADOVI_PUTANJA, encoding='utf-8') as handle:
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


# --- Радови: скрипта ---------------------------------------------------------

def test_radovi_dry_run_ne_menja_nista_i_ispisuje_odnos_geo():
    """--dry-run сме само да испише бројеве; фајл мора остати бајт-исти."""
    pre = _hes(RADOVI_PUTANJA)
    pre_mtime = RADOVI_PUTANJA.stat().st_mtime_ns
    ishod = subprocess.run(
        [sys.executable, str(SKRIPTA_RADOVI), '--dry-run'],
        cwd=str(KOREN), capture_output=True, text=True, timeout=600,
    )
    if ishod.returncode == 2:
        pytest.skip('извор жетве није монтиран: {}'.format(ishod.stderr.strip()))
    assert ishod.returncode == 0, ishod.stderr
    assert _hes(RADOVI_PUTANJA) == pre, '--dry-run је изменио data/ogk_radovi.json'
    assert RADOVI_PUTANJA.stat().st_mtime_ns == pre_mtime, \
        '--dry-run је уписивао у data/ogk_radovi.json'

    izlaz = ishod.stdout
    # Однос geo / не-geo мора да се види, иначе оцена релевантности нема меру.
    for broj in (RADOVI_LOKALITETA, RADOVI_UKUPNO, RADOVI_GEO, RADOVI_NE_GEO):
        assert str(broj) in izlaz, 'број {} није исписан'.format(broj)
    # Сирочићи (ogk_id из жетве без тачке) се не гутају тихо.
    assert 'сирочића' in izlaz or 'УПОЗОРЕЊЕ' in izlaz


# --- Радови: подаци ----------------------------------------------------------

def test_radovi_json_ima_ocekivane_brojeve(radovi):
    assert radovi['ukupno_lokaliteta'] == RADOVI_LOKALITETA
    assert radovi['ukupno_radova'] == RADOVI_UKUPNO
    assert len(radovi['radovi']) == RADOVI_LOKALITETA
    assert sum(len(spisak) for spisak in radovi['radovi'].values()) == RADOVI_UKUPNO
    assert radovi['izvor']
    assert radovi['generisano']


def test_radovi_bez_praznih_nizova_i_bez_apstrakta(radovi):
    for ogk_id, spisak in radovi['radovi'].items():
        assert spisak, 'локалитет {} има празан низ радова'.format(ogk_id)
        for rad in spisak:
            # Апстракт се користи само при оцени geo, у излаз не иде.
            assert 'abstract' not in rad and 'apstrakt' not in rad
            assert isinstance(rad['geo'], bool)
            assert rad['godina'] is None or isinstance(rad['godina'], int)


def test_svaki_ogk_id_iz_zetve_ima_svoju_tacku(podaci, radovi):
    poznati = {tacka['id'] for tacka in podaci['tacke']}
    sirocici = sorted(set(radovi['radovi']) - poznati)
    assert not sirocici, 'радови висе на непостојећим тачкама: {}'.format(sirocici[:10])


def test_geo_radovi_prethode_ostalim_pomenima(radovi):
    """Сортирање: прво geo, па новије горе, рад без године на крај групе."""
    sa_oba = 0
    for ogk_id, spisak in radovi['radovi'].items():
        zastave = [rad['geo'] for rad in spisak]
        assert zastave == sorted(zastave, reverse=True), \
            'локалитет {} меша geo и остале'.format(ogk_id)
        if any(zastave) and not all(zastave):
            sa_oba += 1
        for grupa in (True, False):
            godine = [rad['godina'] for rad in spisak if rad['geo'] is grupa]
            bez_godine = [i for i, g in enumerate(godine) if g is None]
            sa_godinom = [g for g in godine if g is not None]
            assert sa_godinom == sorted(sa_godinom, reverse=True), \
                'локалитет {} није по години опадајуће'.format(ogk_id)
            if bez_godine:
                # Радови без године иду на крај своје групе.
                assert min(bez_godine) >= len(sa_godinom), ogk_id
    assert sa_oba > 0, 'ниједан локалитет нема обе групе — тест ништа не доказује'


def test_ocena_geo_hvata_geologiju_a_ne_gradsku_hroniku():
    sys.path.insert(0, str(KOREN / 'scripts' / 'import_export'))
    try:
        import build_ogk_radovi as gradnja
    finally:
        sys.path.pop(0)

    assert gradnja.je_geoloski({
        'title': 'Petrology of plagiogranite from Sjenica, Dinaridic Ophiolite Belt',
        'journal': '', 'abstract': '',
    })
    assert gradnja.je_geoloski({
        'title': 'Рудник и лежиште олова', 'journal': '', 'abstract': '',
    })
    # „ore“ сме да се хвата само на почетку речи — иначе „before“ прође.
    assert not gradnja.je_geoloski({
        'title': 'Visegrad four in Bosnia-Herzegovina. State-building before the EU',
        'journal': 'Society and Economy',
        'abstract': 'This article analyses the approximation to the European Union.',
    })


# --- Радови: API -------------------------------------------------------------

def test_tacke_nose_brojace_radova():
    odgovor = _klijent().get('/api/map/ogk-points', base_url=BASE)
    assert odgovor.status_code == 200
    podaci_api = odgovor.get_json()['data']
    assert podaci_api['radovi_izvor'] == 'ok'

    tacke = podaci_api['tacke']
    assert len(tacke) == UKUPNO
    sa_radovima = [t for t in tacke if t['n_radova'] > 0]
    assert len(sa_radovima) == RADOVI_LOKALITETA
    assert sum(t['n_radova'] for t in tacke) == RADOVI_UKUPNO
    assert sum(t['n_radova_geo'] for t in tacke) == RADOVI_GEO
    for tacka in tacke:
        assert tacka['n_radova_geo'] <= tacka['n_radova']


def test_rute_radova_za_poznatu_tacku():
    odgovor = _klijent().get('/api/map/ogk-points/K34-03-0035/radovi', base_url=BASE)
    assert odgovor.status_code == 200
    podaci_api = odgovor.get_json()['data']
    assert podaci_api['id'] == 'K34-03-0035'
    assert podaci_api['naziv'] == 'Višegrad gabro-dijabaz'
    assert podaci_api['n_radova'] == len(podaci_api['radovi']) > 0
    assert podaci_api['n_radova_geo'] >= 1
    prvi = podaci_api['radovi'][0]
    assert prvi['geo'] is True, 'релевантан рад мора да буде први'
    assert prvi['url'].startswith('https://')
    assert set(prvi) == {'naslov', 'godina', 'autori', 'casopis', 'doi',
                         'url', 'pdf_url', 'geo'}


def test_tacka_bez_radova_nije_greska():
    odgovor = _klijent().get('/api/map/ogk-points/K34-03-0025/radovi', base_url=BASE)
    assert odgovor.status_code == 200
    podaci_api = odgovor.get_json()['data']
    assert podaci_api['radovi'] == []
    assert podaci_api['n_radova'] == 0
    assert podaci_api['n_radova_geo'] == 0


def test_nepoznat_ogk_id_daje_404_a_ne_tiho_prazno():
    odgovor = _klijent().get('/api/map/ogk-points/K34-03-9999/radovi', base_url=BASE)
    assert odgovor.status_code == 404
    telo = odgovor.get_json()
    assert telo['success'] is False
    assert 'K34-03-9999' in telo['message']


@pytest.mark.parametrize('lose', ['a$b', "' OR 1=1", 'x' * 40, '.'])
def test_neispravan_oblik_id_a_ne_puca_u_500(lose):
    odgovor = _klijent().get('/api/map/ogk-points/{}/radovi'.format(lose), base_url=BASE)
    assert odgovor.status_code in (400, 404), odgovor.get_data(as_text=True)


def test_radovi_neautentifikovan_zahtev_ne_dobija_podatke():
    odgovor = _klijent(prijavljen=False).get(
        '/api/map/ogk-points/K34-03-0035/radovi', base_url=BASE)
    assert odgovor.status_code != 200
    assert 'naslov' not in odgovor.get_data(as_text=True)


def test_nedostupni_radovi_ne_gase_sloj_ali_se_vide():
    """Без data/ogk_radovi.json тачке и даље стижу, али са radovi_izvor."""
    zatecen = maps_layer_views._ogk_radovi_cache
    maps_layer_views._ogk_radovi_cache = {'radovi': {}, 'izvor': 'nedostaje'}
    try:
        odgovor = _klijent().get('/api/map/ogk-points?grupe=busotine', base_url=BASE)
        assert odgovor.status_code == 200
        podaci_api = odgovor.get_json()['data']
        assert podaci_api['radovi_izvor'] == 'nedostaje'
        assert len(podaci_api['tacke']) == OCEKIVANE_GRUPE['busotine']
        assert all(t['n_radova'] == 0 for t in podaci_api['tacke'])

        rute = _klijent().get('/api/map/ogk-points/K34-03-0035/radovi', base_url=BASE)
        assert rute.status_code == 200
        assert rute.get_json()['data']['radovi'] == []
    finally:
        maps_layer_views._ogk_radovi_cache = zatecen


def test_strana_karte_nosi_prekidac_filtera_radova():
    client = museum_app.app.test_client()
    with client.session_transaction() as sesija:
        sesija['user_id'] = 990603
        sesija['user_email'] = 'ogk.radovi@example.invalid'
        sesija['user_name'] = 'ОГК Радови'
        sesija['user_role'] = 'admin'
        sesija['user_department'] = 'Природњачки музеј'
        sesija['is_admin'] = True

    html = client.get('/admin/maps', base_url=BASE).get_data(as_text=True)
    assert 'id="toggle-ogk-samo-radovi"' in html
    assert 'data-ogk-broj="samo-radovi">{}<'.format(RADOVI_LOKALITETA) in html
    # Филтер није слој: не сме да упадне у бројач групе ни у „Угаси све слојеве“.
    assert 'id="toggle-ogk-samo-radovi" data-map-layer' not in html


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
