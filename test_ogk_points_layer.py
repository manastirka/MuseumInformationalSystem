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
# Жетва по имену локалитета: 628 локалитета, 2203 рада. Сваки рад је стварно
# оцењен (data/ogk_radovi_ocene.json), не процењен регексом — расподела суда је
# 281 потврђен, 216 вероватан, 153 несигуран, 1553 „није“. Локалитета са бар
# једним потврђеним или вероватним радом је 198, не 628.
RADOVI_LOKALITETA = 628
RADOVI_UKUPNO = 2203
RADOVI_POTVRDJENIH = 281
RADOVI_VEROVATNIH = 216
RADOVI_NESIGURNIH = 153
RADOVI_NIJE = 1553
LOKALITETA_SA_POTVRDOM = 198
REDOSLED_OCENA = ('potvrdjen', 'verovatan', 'nesigurno', 'neoceneno', 'nije')
OCENE_PUTANJA = KOREN / 'data' / 'ogk_radovi_ocene.json'
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


@pytest.fixture(scope='module')
def ocene():
    with open(OCENE_PUTANJA, encoding='utf-8') as handle:
        return json.load(handle)


def _gradnja():
    """Увези build_ogk_radovi.py без сталног гурања у sys.path."""
    sys.path.insert(0, str(KOREN / 'scripts' / 'import_export'))
    try:
        import build_ogk_radovi
        return build_ogk_radovi
    finally:
        sys.path.pop(0)


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

def test_radovi_dry_run_ne_menja_nista_i_ispisuje_raspodelu():
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
    # Расподела суда мора да се види, иначе релевантност нема меру.
    for ocena in REDOSLED_OCENA:
        assert ocena in izlaz, 'оцена {} није исписана'.format(ocena)
    for broj in (RADOVI_LOKALITETA, RADOVI_UKUPNO, RADOVI_POTVRDJENIH,
                 RADOVI_VEROVATNIH, RADOVI_NESIGURNIH, RADOVI_NIJE,
                 LOKALITETA_SA_POTVRDOM):
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


def test_meta_nosi_raspodelu_i_broj_potvrdjenih(radovi, ocene):
    """Расподела у излазу мора да буде пресликана из фајла оцена, не измишљена."""
    assert radovi['raspodela'] == {
        'potvrdjen': RADOVI_POTVRDJENIH,
        'verovatan': RADOVI_VEROVATNIH,
        'nesigurno': RADOVI_NESIGURNIH,
        'neoceneno': 0,
        'nije': RADOVI_NIJE,
    }
    assert radovi['ukupno_potvrdjenih'] == RADOVI_POTVRDJENIH
    for ocena, broj in ocene['raspodela'].items():
        assert radovi['raspodela'][ocena] == broj, ocena
    stvarno = {}
    for spisak in radovi['radovi'].values():
        for rad in spisak:
            stvarno[rad['ocena']] = stvarno.get(rad['ocena'], 0) + 1
    assert stvarno == {k: v for k, v in radovi['raspodela'].items() if v}


def test_radovi_bez_praznih_nizova_i_bez_apstrakta(radovi):
    for ogk_id, spisak in radovi['radovi'].items():
        assert spisak, 'локалитет {} има празан низ радова'.format(ogk_id)
        for rad in spisak:
            # Апстракт се користи само при оцењивању, у излаз не иде.
            assert 'abstract' not in rad and 'apstrakt' not in rad
            # Регекс `geo` је избачен: два паралелна извора истине о истој
            # ствари су нас већ ујела.
            assert 'geo' not in rad, ogk_id
            assert rad['ocena'] in REDOSLED_OCENA, (ogk_id, rad['ocena'])
            assert isinstance(rad['razlog'], str)
            assert rad['godina'] is None or isinstance(rad['godina'], int)


def test_potvrdjen_rad_uvek_nosi_razlog(radovi):
    """Разлог је главна корист кустосу; потврђен рад без њега је празан суд.

    Модел је на 10 од 2203 рада вратио оцену без образложења (ниједан од њих
    није потврђен) — праг хвата да тај реп не нарасте у правило.
    """
    bez_razloga = [
        (ogk_id, rad['ocena'], rad['naslov'])
        for ogk_id, spisak in radovi['radovi'].items()
        for rad in spisak
        if rad['ocena'] != 'neoceneno' and not rad['razlog'].strip()
    ]
    potvrdjeni_bez = [s for s in bez_razloga if s[1] == 'potvrdjen']
    assert not potvrdjeni_bez, potvrdjeni_bez[:5]
    assert len(bez_razloga) < RADOVI_UKUPNO * 0.01, \
        '{} радова без разлога — суд престаје да значи'.format(len(bez_razloga))


def test_svaki_ogk_id_iz_zetve_ima_svoju_tacku(podaci, radovi):
    poznati = {tacka['id'] for tacka in podaci['tacke']}
    sirocici = sorted(set(radovi['radovi']) - poznati)
    assert not sirocici, 'радови висе на непостојећим тачкама: {}'.format(sirocici[:10])


def test_radovi_idu_redom_ocena_pa_godina(radovi):
    """Сортирање: potvrdjen → verovatan → nesigurno → neoceneno → nije,
    унутар групе новије горе, рад без године на крај своје групе."""
    rang = {ocena: i for i, ocena in enumerate(REDOSLED_OCENA)}
    sa_vise_grupa = 0
    for ogk_id, spisak in radovi['radovi'].items():
        rangovi = [rang[rad['ocena']] for rad in spisak]
        assert rangovi == sorted(rangovi), \
            'локалитет {} меша оцене: {}'.format(ogk_id, rangovi)
        if len(set(rangovi)) > 1:
            sa_vise_grupa += 1
        for ocena in REDOSLED_OCENA:
            godine = [rad['godina'] for rad in spisak if rad['ocena'] == ocena]
            bez_godine = [i for i, g in enumerate(godine) if g is None]
            sa_godinom = [g for g in godine if g is not None]
            assert sa_godinom == sorted(sa_godinom, reverse=True), \
                'локалитет {} није по години опадајуће'.format(ogk_id)
            if bez_godine:
                # Радови без године иду на крај своје групе.
                assert min(bez_godine) >= len(sa_godinom), ogk_id
    assert sa_vise_grupa > 0, 'ниједан локалитет нема две групе — тест не доказује ништа'


def test_potvrdjeni_su_uvek_pre_verovatnih_gde_ima_oba(radovi):
    """Барем један локалитет мора да носи и потврђен и вероватан рад."""
    oba = [ogk_id for ogk_id, spisak in radovi['radovi'].items()
           if {'potvrdjen', 'verovatan'} <= {rad['ocena'] for rad in spisak}]
    assert oba, 'ниједан локалитет нема обе групе'
    for ogk_id in oba:
        spisak = radovi['radovi'][ogk_id]
        poslednji_potvrdjen = max(i for i, rad in enumerate(spisak)
                                  if rad['ocena'] == 'potvrdjen')
        prvi_verovatan = min(i for i, rad in enumerate(spisak)
                             if rad['ocena'] == 'verovatan')
        assert poslednji_potvrdjen < prvi_verovatan, ogk_id


# --- Радови: спајање оцене са жетвом -----------------------------------------

def _lazna_zetva(koren, radovi_dosijea, ogk_id='K34-99-0001'):
    """Направи минималан dosije.json какав скрипта чита са CIFS-а."""
    lokalitet = koren / 'lokaliteti' / ogk_id
    lokalitet.mkdir(parents=True)
    (lokalitet / 'dosije.json').write_text(
        json.dumps({'ogk_id': ogk_id, 'radovi': radovi_dosijea},
                   ensure_ascii=False),
        encoding='utf-8')
    return ogk_id


def test_rad_bez_ocene_dobija_neoceneno_a_ne_nije(tmp_path, monkeypatch):
    """Следећа жетва донеће радове које суд још није видео — они нису „nije“."""
    gradnja = _gradnja()
    ogk_id = _lazna_zetva(tmp_path, [
        {'title': 'Оцењен рад', 'year': 2020},
        {'title': 'Нов рад, још неоцењен', 'year': 2021},
    ])
    monkeypatch.setattr(gradnja, 'LOKALITETI_DIR', str(tmp_path / 'lokaliteti'))

    radovi, ukupno, brojac = gradnja.izgradi_radove({
        ogk_id: [{'br': 1, 'naslov': 'Оцењен рад', 'ocena': 'potvrdjen',
                  'razlog': 'разлог'}],
    })

    assert ukupno == 2
    assert brojac['neoceneno'] == 1
    assert brojac['nije'] == 0
    po_naslovu = {rad['naslov']: rad for rad in radovi[ogk_id]}
    assert po_naslovu['Нов рад, још неоцењен']['ocena'] == 'neoceneno'
    assert po_naslovu['Нов рад, још неоцењен']['razlog'] == ''
    # Неоцењен стоји испод оцењених, али изнад „nije“ — редослед то чува.
    assert [rad['ocena'] for rad in radovi[ogk_id]] == ['potvrdjen', 'neoceneno']


def test_neslaganje_naslova_je_glasna_greska(tmp_path, monkeypatch):
    """Померена жетва значи да редни број показује на туђи рад — то се виче."""
    gradnja = _gradnja()
    ogk_id = _lazna_zetva(tmp_path, [
        {'title': 'Нов рад убачен на почетак', 'year': 2024},
        {'title': 'Стари рад', 'year': 2001},
    ])
    monkeypatch.setattr(gradnja, 'LOKALITETI_DIR', str(tmp_path / 'lokaliteti'))

    with pytest.raises(gradnja.NeslaganjeNaslova) as greska:
        gradnja.izgradi_radove({
            ogk_id: [{'br': 1, 'naslov': 'Стари рад', 'ocena': 'potvrdjen',
                      'razlog': 'разлог'}],
        })
    poruka = str(greska.value)
    assert ogk_id in poruka, 'грешка не каже који локалитет'
    assert 'рад 1' in poruka, 'грешка не каже који редни број'
    assert 'Стари рад' in poruka and 'Нов рад убачен на почетак' in poruka


def test_neslaganje_naslova_rusi_ceo_prolaz(tmp_path, monkeypatch, capsys):
    """main() не сме да упише полудели фајл — излази са ненултим кодом."""
    gradnja = _gradnja()
    ogk_id = _lazna_zetva(tmp_path, [{'title': 'Прави наслов', 'year': 2024}])
    monkeypatch.setattr(gradnja, 'LOKALITETI_DIR', str(tmp_path / 'lokaliteti'))
    ocene_put = tmp_path / 'ocene.json'
    ocene_put.write_text(json.dumps({'ocene': {
        ogk_id: [{'br': 1, 'naslov': 'Туђи наслов', 'ocena': 'potvrdjen',
                  'razlog': 'разлог'}],
    }}, ensure_ascii=False), encoding='utf-8')
    izlaz_put = tmp_path / 'izlaz.json'

    kod = gradnja.main(['--ocene', str(ocene_put), '--output', str(izlaz_put),
                        '--tacke', str(tmp_path / 'nema-tacaka.json')])
    assert kod == 4
    assert not izlaz_put.exists(), 'уписан је фајл упркос неслагању наслова'
    assert 'ГРЕШКА' in capsys.readouterr().err


def test_promena_strane_u_odnosu_na_stari_regeks():
    """Извештај о разлазу са регексом се рачуна из затеченог фајла са `geo`."""
    gradnja = _gradnja()
    zatecen = {'radovi': {'K34-99-0001': [
        {'naslov': 'Лажан погодак', 'geo': True},
        {'naslov': 'Промашен рад', 'geo': False},
        {'naslov': 'Поготак', 'geo': True},
    ]}}
    novi = {'K34-99-0001': [
        {'naslov': 'Поготак', 'ocena': 'potvrdjen'},
        {'naslov': 'Промашен рад', 'ocena': 'verovatan'},
        {'naslov': 'Лажан погодак', 'ocena': 'nije'},
    ]}
    assert gradnja.promena_strane(zatecen, novi) == (1, 1)
    # Кад затечени фајл више не носи `geo`, извештај се гаси — не лаже нулом.
    assert gradnja.promena_strane({'radovi': {'K34-99-0001': [
        {'naslov': 'Поготак', 'ocena': 'potvrdjen'}]}}, novi) is None


def test_ocene_i_zetva_se_poklapaju_po_naslovu(radovi, ocene):
    """Спајање је стварно проверено над испорученим подацима, не на речи."""
    assert set(ocene['ocene']) == set(radovi['radovi'])
    assert ocene['ukupno_ocena'] == RADOVI_UKUPNO
    for ogk_id, spisak in ocene['ocene'].items():
        assert [stavka['br'] for stavka in spisak] == list(range(1, len(spisak) + 1))
        ocenjeni = {stavka['naslov'].strip() for stavka in spisak}
        pozeti = {rad['naslov'].strip() for rad in radovi['radovi'][ogk_id]}
        assert ocenjeni == pozeti, ogk_id


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
    assert sum(t['n_radova_potvrdjenih'] for t in tacke) == RADOVI_POTVRDJENIH
    assert sum(t['n_radova_verovatnih'] for t in tacke) == RADOVI_VEROVATNIH
    for tacka in tacke:
        assert 'n_radova_geo' not in tacka, 'стари регекс бројач је остао у API-ју'
        assert tacka['n_radova_potvrdjenih'] + tacka['n_radova_verovatnih'] \
            <= tacka['n_radova']
    # Филтер пушта тачку са бар једним потврђеним ИЛИ вероватним радом.
    sa_potvrdom = [t for t in tacke
                   if t['n_radova_potvrdjenih'] or t['n_radova_verovatnih']]
    assert len(sa_potvrdom) == LOKALITETA_SA_POTVRDOM


def test_rute_radova_za_poznatu_tacku():
    odgovor = _klijent().get('/api/map/ogk-points/K34-03-0035/radovi', base_url=BASE)
    assert odgovor.status_code == 200
    podaci_api = odgovor.get_json()['data']
    assert podaci_api['id'] == 'K34-03-0035'
    assert podaci_api['naziv'] == 'Višegrad gabro-dijabaz'
    assert podaci_api['n_radova'] == len(podaci_api['radovi']) > 0
    assert podaci_api['n_radova_potvrdjenih'] >= 1
    # Бројеви по групама стижу уз саме радове, да поповер не рачуна два пута.
    assert podaci_api['po_oceni']['potvrdjen'] == podaci_api['n_radova_potvrdjenih']
    assert podaci_api['po_oceni']['verovatan'] == podaci_api['n_radova_verovatnih']
    assert sum(podaci_api['po_oceni'].values()) == podaci_api['n_radova']
    prvi = podaci_api['radovi'][0]
    assert prvi['ocena'] == 'potvrdjen', 'потврђен рад мора да буде први'
    assert prvi['razlog'], 'рад стоји ту где стоји без иједне речи објашњења'
    assert prvi['url'].startswith('https://')
    assert set(prvi) == {'naslov', 'godina', 'autori', 'casopis', 'doi',
                         'url', 'pdf_url', 'ocena', 'razlog'}


def test_tacka_sa_radovima_ali_bez_ijednog_potvrdjenog():
    """Осам туђих радова није исто што и ниједан рад — API то мора да разликује."""
    odgovor = _klijent().get('/api/map/ogk-points/K34-05-0028/radovi', base_url=BASE)
    assert odgovor.status_code == 200
    podaci_api = odgovor.get_json()['data']
    assert podaci_api['n_radova'] > 0
    assert podaci_api['n_radova_potvrdjenih'] == 0
    assert podaci_api['n_radova_verovatnih'] == 0
    assert all(rad['ocena'] in ('nesigurno', 'nije') for rad in podaci_api['radovi'])


def test_tacka_bez_radova_nije_greska():
    odgovor = _klijent().get('/api/map/ogk-points/K34-03-0025/radovi', base_url=BASE)
    assert odgovor.status_code == 200
    podaci_api = odgovor.get_json()['data']
    assert podaci_api['radovi'] == []
    assert podaci_api['n_radova'] == 0
    assert podaci_api['n_radova_potvrdjenih'] == 0
    assert podaci_api['n_radova_verovatnih'] == 0
    assert set(podaci_api['po_oceni'].values()) == {0}


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
    # id остаје непромењен (тест чува id-еве), мења се само видљив текст.
    assert 'id="toggle-ogk-samo-radovi"' in html
    assert 'Само са потврђеним радовима' in html
    assert 'Само тачке са радовима' not in html, 'стара, нетачна ознака је остала'
    # Бројач броји локалитете са бар једним потврђеним или вероватним радом.
    assert 'data-ogk-broj="samo-radovi">{}<'.format(LOKALITETA_SA_POTVRDOM) in html
    assert 'data-ogk-broj="samo-radovi">{}<'.format(RADOVI_LOKALITETA) not in html
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
