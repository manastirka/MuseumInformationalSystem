#!/usr/bin/env python3
"""Тестови за модул Конзерваторско-рестаураторски досије (К-Р досије).

Три слоја, по брзини/зависностима:

1. ЧИСТИ парсери (`kr_dosije_core`) — без базе и без Flask-а (најбржи).
2. Увозник (dry-run) над стварним xlsx-ом — прескаче се ако нема података.
3. Генератор евиденционог броја + руте/права кроз Flask test client — прескаче
   се ако база или апликација нису доступне у окружењу.

Тестови су самочистећи и идемпотентни (сигурни за поновно покретање):
генератор ев. броја ради у трансакцији коју ВРАЋА (rollback), а тест руте
брише досије који је сам направио (по ухваћеном id-у).
"""

import os
from datetime import date
from pathlib import Path

import pytest

os.environ.setdefault('FLASK_ENV', 'testing')
os.environ.setdefault('SECRET_KEY', 'test-secret')
os.environ.setdefault('REDIS_URL', '')
os.environ.setdefault('SESSION_TYPE', 'filesystem')
os.environ.setdefault('SESSION_FILE_DIR', '/tmp/museum-test-flask-session')

import kr_dosije_core as core
import kr_dosije_cli as cli


# ===========================================================================
# 1) ЧИСТИ ПАРСЕРИ — без базе, без Flask-а
# ===========================================================================
class TestParsePeriod:
    def test_od_do_puna_proza(self):
        text = 'у периоду од 23.12.2022. године до 07.01.2023. године'
        assert core.parse_period(text) == (date(2022, 12, 23), date(2023, 1, 7))

    def test_dana_jedan_datum_od_jednako_do(self):
        od, do = core.parse_period('дана 06.09.2023 године')
        assert od == date(2023, 9, 6)
        assert do == date(2023, 9, 6)

    def test_prazno_i_none(self):
        assert core.parse_period('') == (None, None)
        assert core.parse_period(None) == (None, None)

    def test_neuredan_razmak(self):
        od, do = core.parse_period('01. 09.2023 ... 15.09.2025')
        assert od == date(2023, 9, 1)
        assert do == date(2025, 9, 15)


class TestParseIzvrsioci:
    known_users = [
        ('nenad.mladenovic@nhmbeo.rs', 'Ненад Младеновић'),
        ('biljana.mitrovic@nhmbeo.rs', 'Биљана Митровић'),
    ]

    def test_poklopljen_korisnik(self):
        rez = core.parse_izvrsioci(
            'Конзервацију је извршио Ненад Младеновић на предмету', self.known_users)
        assert len(rez) == 1
        assert rez[0]['user_email'] == 'nenad.mladenovic@nhmbeo.rs'

    def test_nepoznata_osoba_bez_email_ali_sa_imenom(self):
        rez = core.parse_izvrsioci(
            'Радове извршио Петар Петровић, спољни сарадник', self.known_users)
        assert len(rez) == 1
        assert rez[0]['user_email'] is None
        assert rez[0]['ime_tekst']  # непразан текст — податак се не губи


class TestNormalizeBroj:
    def test_mineral_prefiks_m(self):
        assert core.normalize_broj('М2051') == '2051'

    def test_oznaka_sl_i_m(self):
        assert core.normalize_broj('сл. м4118') == '4118'

    def test_broj_key_col_sa_prozom(self):
        assert core.broj_key_from_text('Col.898 Фосилни материјал') == '898'

    def test_kosa_crta_i_crtica_ekvivalentni(self):
        # '/' и '-' се обоје бришу → исти кључ.
        a = core.normalize_broj('Col.УШ 85/1110')
        b = core.normalize_broj('УШ 85-1110')
        assert a == b == 'УШ851110'


class TestParseImageFilename:
    def test_v_je_posle(self):
        rez = core.parse_image_filename('сл. 771.в.jpg')
        assert rez is not None
        assert rez['faza'] == 'posle'
        assert rez['broj_norm'] == '771'

    def test_a_je_pre(self):
        rez = core.parse_image_filename('(Сл.Col.072022. a).png')
        assert rez is not None
        assert rez['faza'] == 'pre'

    def test_b_je_tokom_sa_podindeksom(self):
        rez = core.parse_image_filename('Сл.Col. 102022.1б.jpg')
        assert rez is not None
        assert rez['faza'] == 'tokom'

    def test_bez_faze_vraca_none(self):
        assert core.parse_image_filename('Доделиће се касније 1.jpg') is None

    def test_spoljni_sum_vraca_none(self):
        assert core.parse_image_filename('IMG_20240531_122901553.jpg') is None


class TestDepartmentToOdeljenje:
    def test_geolosko(self):
        assert core.department_to_odeljenje('ГЕОЛОШКО ОДЕЉЕЊЕ') == 'geo'

    def test_biolosko(self):
        assert core.department_to_odeljenje('Биолошко одељење') == 'bio'

    def test_prazno_je_none(self):
        assert core.department_to_odeljenje('') is None


# ===========================================================================
# 2) УВОЗНИК — dry-run над стварним xlsx-ом (без уписа)
# ===========================================================================
# Фолдер садржи ћирилично 'за' у имену — копирано дословно.
_IMPORT_DIR = '/home/aleksandarlukovic/Desktop/slike za k-r dnevnik'


def _import_data_present():
    p = Path(_IMPORT_DIR)
    if not p.is_dir():
        return False
    return any(f.suffix.lower() in ('.xlsx', '.xls') for f in p.iterdir())


@pytest.mark.skipif(not _import_data_present(),
                    reason='нема улазног xlsx фолдера за увоз (CI без података)')
def test_plan_import_dry_run():
    known_users = [
        ('nenad.mladenovic@nhmbeo.rs', 'Ненад Младеновић'),
        ('biljana.mitrovic@nhmbeo.rs', 'Биљана Митровић'),
    ]
    plan = cli.plan_import(_IMPORT_DIR, 'geo', known_users)

    assert len(plan['dossiers']) == 58

    m = plan['matches']
    assert len(m['exact']) == 112
    for img, idx, faza in m['exact']:
        assert isinstance(img, Path)
        assert isinstance(idx, int)
        assert faza in {'pre', 'tokom', 'posle'}

    assert isinstance(m['ambiguous'], list)
    assert isinstance(m['unmatched'], list)
    assert isinstance(m['no_phase'], list)


# ===========================================================================
# Заједничко за тестове са базом / апликацијом
# ===========================================================================
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

try:
    import app as museum_app
    _APP_IMPORT_ERROR = None
except Exception as exc:  # pragma: no cover - зависи од окружења
    museum_app = None
    _APP_IMPORT_ERROR = exc


# ===========================================================================
# 3) ГЕНЕРАТОР ЕВИДЕНЦИОНОГ БРОЈА — прави курсор, трансакција са ROLLBACK
# ===========================================================================
@pytest.mark.skipif(not _DB_OK, reason='PostgreSQL није доступан')
def test_next_evidencioni_broj_uzastopni_u_rollback():
    """Умета један ред кроз next_evidencioni_broj па поново тражи број.

    Ради у трансакцији коју на крају ВРАЋА (rollback), тако да база остаје
    нетакнута. Користи годину 2099 да не удара у постојеће записе.
    """
    from postgres_service import get_postgres_connection

    conn = get_postgres_connection()
    try:
        cur = conn.cursor()
        prvi = core.next_evidencioni_broj(cur, 'geo', 2099)
        assert prvi == 'КР-ГЕО-2099-001'
        cur.execute(
            """
            INSERT INTO kr_dosije (evidencioni_broj, odeljenje, naziv_predmeta)
            VALUES (%s, %s, %s)
            """,
            (prvi, 'geo', 'Тест предмет (rollback)'),
        )
        drugi = core.next_evidencioni_broj(cur, 'geo', 2099)
        assert drugi == 'КР-ГЕО-2099-002'
    finally:
        conn.rollback()  # ништа се не задржава у бази
        conn.close()

    # Провера да rollback заиста није оставио траг.
    with get_postgres_connection() as conn2, conn2.cursor() as cur2:
        cur2.execute(
            "SELECT count(*) FROM kr_dosije WHERE evidencioni_broj LIKE %s",
            ('КР-ГЕО-2099-%',),
        )
        assert cur2.fetchone()[0] == 0


# ===========================================================================
# 4) РУТЕ / ПРАВА — кроз Flask test client
# ===========================================================================
_APP_SKIP = pytest.mark.skipif(
    museum_app is None or not _DB_OK,
    reason=f'апликација/база нису доступне ({_APP_IMPORT_ERROR})',
)


@pytest.fixture
def client():
    prev_csrf = museum_app.app.config.get('WTF_CSRF_ENABLED', False)
    museum_app.app.config['WTF_CSRF_ENABLED'] = False
    c = museum_app.app.test_client()
    yield c
    museum_app.app.config['WTF_CSRF_ENABLED'] = prev_csrf


def _login_admin(c):
    with c.session_transaction() as sess:
        sess['user_id'] = 1
        sess['user_email'] = 'admin@nhmbeo.rs'
        sess['user_name'] = 'Админ'
        sess['user_role'] = 'admin'
        sess['is_admin'] = True
        sess['user_department'] = 'Администрација'
        sess['is_department_head'] = False


def _login_plain_employee(c):
    # Запослени без права на kr_dosije: није у authorized_users, а одељење
    # није ни geo ни bio (правна служба нема приступ модулу).
    with c.session_transaction() as sess:
        sess['user_id'] = 99
        sess['user_email'] = 'nobody.kr@nhmbeo.rs'
        sess['user_name'] = 'Нико'
        sess['user_role'] = 'employee'
        sess['is_admin'] = False
        sess['user_department'] = 'ОДСЕК ОПШТИХ И ПРАВНИХ ПОСЛОВА'
        sess['is_department_head'] = False


BASE_URL = 'https://localhost'


@_APP_SKIP
def test_admin_moze_da_otvori_listu(client):
    _login_admin(client)
    r = client.get('/kr-dosije', base_url=BASE_URL, follow_redirects=False)
    assert r.status_code == 200


@_APP_SKIP
def test_zaposleni_bez_prava_blokiran(client):
    _login_plain_employee(client)
    r = client.get('/kr-dosije', base_url=BASE_URL, follow_redirects=False)
    # module_access_required блокира: flash-redirect (302) или 403.
    assert r.status_code in (302, 403)
    if r.status_code == 302:
        assert '/dashboard' in r.headers.get('Location', '')


@_APP_SKIP
def test_kreiranje_dosijea_i_pdf(client):
    """Направи досије као админ, потврди да се види, повуци PDF, па очисти."""
    import re
    from postgres_service import get_postgres_connection

    _login_admin(client)
    r = client.post(
        '/kr-dosije/novi', base_url=BASE_URL, follow_redirects=False,
        data={
            'odeljenje': 'geo',
            'predmet_tip': 'slobodan',
            'naziv_predmeta': 'Тест предмет',
            'opis_pre': 'Опис стања пре радова',
            'period_od': '2026-07-01',
            'period_do': '2026-07-02',
            'izvrsilac_ime': 'Тест Извршилац',
        },
    )
    assert r.status_code == 302
    loc = r.headers.get('Location', '')
    match = re.search(r'/kr-dosije/(\d+)', loc)
    assert match, f'нема id досијеа у редиректу: {loc!r}'
    dosije_id = int(match.group(1))

    try:
        # Детаљ приказује направљени досије.
        detail = client.get(f'/kr-dosije/{dosije_id}', base_url=BASE_URL)
        assert detail.status_code == 200
        assert 'Тест предмет' in detail.get_data(as_text=True)

        # PDF извоз.
        pdf = client.get(f'/kr-dosije/{dosije_id}/pdf', base_url=BASE_URL)
        assert pdf.status_code == 200
        assert pdf.headers.get('Content-Type') == 'application/pdf'
    finally:
        # Чишћење: избриши направљени ред (izvrsioci падају уз CASCADE).
        with get_postgres_connection() as conn, conn.cursor() as cur:
            cur.execute('DELETE FROM kr_dosije WHERE id = %s', (dosije_id,))
            conn.commit()
