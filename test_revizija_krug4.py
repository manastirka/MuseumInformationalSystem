#!/usr/bin/env python3
"""Тестови круга 4 ревизије 2026-08 — ставка 5: научне вести и дигитализовани
профили прелазе на PostgreSQL као извор истине (образац Sanja/Bilja, батч 6).

  * science_news (мигр. 053): row-level CRUD кроз праве руте на стварној
    *_test бази; JSON фајл се НЕ чита кад је база конфигурисана.
  * Пад базе НИЈЕ тихи прелаз на JSON: GET враћа 503, никад садржај фајла.
  * Дигитализовани профили: кар проба која пукне → 503, не JSON.

БЕЗБЕДНОСТ: ради ИСКЉУЧИВО над базом чије име садржи '_test'.

Покретање:
    python -m pytest test_revizija_krug4.py -q
"""

import json
import os
from pathlib import Path
from unittest.mock import patch

import pytest

TEST_DB_URL = os.environ.get(
    'MIS_TEST_DB_URL',
    'postgresql+psycopg://aleksandarlukovic@localhost:5432/museum_system_test',
)
if '_test' not in TEST_DB_URL.rsplit('/', 1)[-1]:
    pytest.skip(
        'MIS_TEST_DB_URL не показује на *_test базу — заштита продукционе базе',
        allow_module_level=True,
    )

os.environ['DATABASE_URL'] = TEST_DB_URL
os.environ.setdefault('FLASK_ENV', 'testing')
os.environ.setdefault('SECRET_KEY', 'test-secret')
os.environ.setdefault('REDIS_URL', '')
os.environ.setdefault('SESSION_TYPE', 'filesystem')
os.environ.setdefault('SESSION_FILE_DIR', 'logs/qa_flask_session')
os.environ.setdefault('WTF_CSRF_ENABLED', 'False')
os.environ.setdefault('RATELIMIT_STORAGE_URL', 'memory://')

import psycopg  # noqa: E402

PLAIN_URL = TEST_DB_URL.replace('postgresql+psycopg://', 'postgresql://')


def _pg_available():
    try:
        with psycopg.connect(PLAIN_URL, connect_timeout=3) as conn:
            conn.execute('SELECT 1')
        return True
    except Exception:
        return False


if not _pg_available():
    pytest.skip('PostgreSQL (museum_system_test) није доступан',
                allow_module_level=True)

import app as museum_app  # noqa: E402
import science_news_store  # noqa: E402

museum_app.app.config['TESTING'] = True
museum_app.app.config['WTF_CSRF_ENABLED'] = False

BASE = 'https://localhost'


@pytest.fixture(scope='module', autouse=True)
def _preusmeri_bazu_na_test():
    import postgres_service
    old_env = os.environ.get('DATABASE_URL')
    os.environ['DATABASE_URL'] = TEST_DB_URL
    postgres_service.close_connection_pools()
    # Миграција 053 је идемпотентна — тест је сам примењује на test бази.
    sql = (Path(__file__).parent / 'migration' / '053_science_news.sql'
           ).read_text(encoding='utf-8')
    with psycopg.connect(PLAIN_URL) as conn:
        conn.execute(sql)
    yield
    postgres_service.close_connection_pools()
    if old_env is not None:
        os.environ['DATABASE_URL'] = old_env


@pytest.fixture(autouse=True)
def _ocisti_vesti():
    def _cisti():
        with psycopg.connect(PLAIN_URL) as conn:
            conn.execute("DELETE FROM science_news WHERE item->>'source' = 'KRUG4-TEST'")
    _cisti()
    yield
    _cisti()


def _login(client, *, email, role):
    with client.session_transaction() as s:
        s['user_id'] = 990401
        s['user_email'] = email
        s['user_name'] = 'Тест Круг4'
        s['user_role'] = role
        s['user_department'] = 'Природњачки музеј'
        s['is_admin'] = role in ('admin', 'direktor')
    return client


def _client():
    return museum_app.app.test_client()


def _db_ids():
    with psycopg.connect(PLAIN_URL) as conn:
        rows = conn.execute(
            "SELECT id FROM science_news WHERE item->>'source' = 'KRUG4-TEST'"
        ).fetchall()
    return {r[0] for r in rows}


# --- Научне вести: row-level CRUD у PostgreSQL-у -----------------------------

def test_vesti_crud_ide_u_postgres_ne_u_fajl(tmp_path):
    prazan_json = tmp_path / 'science_news.json'
    prazan_json.write_text('[]', encoding='utf-8')
    client = _login(_client(), email='admin.krug4@example.invalid', role='admin')

    with patch.object(museum_app.depot_science_views, '_science_news_file',
                      return_value=str(prazan_json)):
        resp = client.post('/api/science-news', json={
            'title': 'Круг 4 тест вест',
            'summary': 'провера skladišta',
            'category': 'geology',
            'region': 'balkans',
            'source': 'KRUG4-TEST',
        }, base_url=BASE)
        assert resp.status_code == 200, resp.get_data(as_text=True)
        news_id = resp.get_json()['news']['id']

        # Ред је у бази (прави commit), НЕ у JSON фајлу.
        assert news_id in _db_ids(), 'вест није у PostgreSQL-у'
        assert json.loads(prazan_json.read_text(encoding='utf-8')) == [], \
            'вест је уписана у JSON фајл уместо у базу'

        # Листа је чита из базе.
        listed = client.get('/api/science-news', base_url=BASE)
        assert listed.status_code == 200
        assert any(n['id'] == news_id for n in listed.get_json()['news'])

        # Брисање: row-level, непостојећи id → 404.
        gone = client.delete(f'/api/science-news/{news_id}', base_url=BASE)
        assert gone.status_code == 200
        assert news_id not in _db_ids()
        missing = client.delete(f'/api/science-news/{news_id}', base_url=BASE)
        assert missing.status_code == 404


def test_vesti_pad_baze_je_503_ne_json(tmp_path):
    """Кад је DATABASE_URL подешен а база падне, одговор је 503 — никад
    тихи прелаз на садржај JSON фајла."""
    lazni_json = tmp_path / 'science_news.json'
    lazni_json.write_text(json.dumps([{
        'id': 'stari1', 'title': 'Застарела вест', 'category': 'geology',
        'region': 'world',
    }]), encoding='utf-8')
    client = _login(_client(), email='radnik.krug4@example.invalid', role='employee')

    def _boom():
        raise RuntimeError('baza pala')

    with patch.object(museum_app.depot_science_views, '_science_news_file',
                      return_value=str(lazni_json)), \
         patch.object(science_news_store, '_get_postgres_connection', _boom):
        resp = client.get('/api/science-news', base_url=BASE)
    assert resp.status_code == 503, resp.get_data(as_text=True)
    assert 'Застарела вест' not in resp.get_data(as_text=True)


# --- Ставка 6: XSS у набавци + цурење str(exc) -------------------------------

def test_nabavka_tabela_koristi_esc():
    """Опис набавке и архивска референца из базе иду у innerHTML — морају
    кроз esc() (образац из батча 7)."""
    src = (Path(__file__).parent / 'templates' / 'finansije' /
           'zahtev_nabavka.html').read_text(encoding='utf-8')
    assert 'function esc(' in src
    assert '${esc(req.opis)}' in src
    assert '${esc(req.archive_reference)}' in src
    assert '<td>${req.opis}</td>' not in src


def test_admin_system_views_ne_curi_izuzetke():
    """Сиров str(exc) не сме у JSON одговор системских рута."""
    src = (Path(__file__).parent / 'admin_system_views.py'
           ).read_text(encoding='utf-8')
    assert 'str(exc)' not in src


# --- Ставка 7: chat прилози само учесницима разговора ------------------------

@pytest.fixture()
def _chat_prilog(tmp_path):
    """DM poruka korisnika 990411→990412 sa prilogom u tmp CHAT_FILES_DIR."""
    import chat_room
    stored_name = 'deadbeefdeadbeefdeadbeefdeadbeef.pdf'
    (tmp_path / stored_name).write_bytes(b'%PDF-1.4 test')
    with patch.object(chat_room, 'CHAT_FILES_DIR', tmp_path):
        chat_room.send_message(
            user_id=990411, user_name='Ана Тест', user_email='ana.krug4@example.invalid',
            department='Тест', message='прилог',
            channel=chat_room.make_dm_channel(990411, 990412),
            file_name='dokument.pdf', file_path=stored_name,
            file_size=13, file_type='application/pdf',
        )
        yield stored_name
    with psycopg.connect(PLAIN_URL) as conn:
        conn.execute("DELETE FROM chat_messages WHERE file_path = %s", (stored_name,))


def _chat_login(client, user_id, email):
    with client.session_transaction() as s:
        s['user_id'] = user_id
        s['user_email'] = email
        s['user_name'] = 'Тест Круг4'
        s['user_role'] = 'employee'
        s['user_department'] = 'Тест'
        s['is_admin'] = False
    return client


def test_chat_prilog_ucesnik_moze_autsajder_403(_chat_prilog, tmp_path):
    import chat_room
    stored_name = _chat_prilog
    # Servis je trenutno ugašen flagom — ranjivost važi kad je uključen.
    with patch.dict(museum_app.app.config, {'CHAT_SERVICE_ENABLED': True}), \
         patch.object(chat_room, 'CHAT_FILES_DIR', tmp_path):
        ucesnik = _chat_login(_client(), 990412, 'boban.krug4@example.invalid')
        resp = ucesnik.get(f'/api/chat/file/{stored_name}', base_url=BASE)
        assert resp.status_code == 200, resp.get_data(as_text=True)

        autsajder = _chat_login(_client(), 990413, 'uljez.krug4@example.invalid')
        resp = autsajder.get(f'/api/chat/file/{stored_name}', base_url=BASE)
        assert resp.status_code == 403, (
            'korisnik van razgovora sme da preuzme tuđ prilog: '
            + resp.get_data(as_text=True)[:200])


def test_chat_fajl_bez_poruke_se_ne_sluzi(tmp_path):
    """Fajl u skladištu koji nijedna poruka ne referencira → 404."""
    import chat_room
    stored_name = 'feedfacefeedfacefeedfacefeedface.pdf'
    (tmp_path / stored_name).write_bytes(b'%PDF-1.4 orphan')
    with patch.dict(museum_app.app.config, {'CHAT_SERVICE_ENABLED': True}), \
         patch.object(chat_room, 'CHAT_FILES_DIR', tmp_path):
        client = _chat_login(_client(), 990414, 'neko.krug4@example.invalid')
        resp = client.get(f'/api/chat/file/{stored_name}', base_url=BASE)
    assert resp.status_code == 404


# --- Дигитализовани профили: кар пробе није тихи JSON ------------------------

def test_profili_pad_probe_je_503_ne_json(tmp_path):
    profili_json = tmp_path / 'digitized_profiles.json'
    profili_json.write_text(json.dumps([{
        'id': 'stari_profil', 'sheet_folder': 'X', 'profile_id': 'AB',
    }]), encoding='utf-8')
    client = _login(_client(), email='radnik.krug4@example.invalid', role='employee')

    import phase3a_databases
    # `create=True` је овде био штетан: атрибут се зове `_DIGITIZED_PROFILES_PATH`
    # (app.py:1585, прослеђује га blueprints/maps.py:249), па је mock правио НОВ,
    # никад читан атрибут. Тврдња „нема stari_profil у одговору" гледала је
    # прави data/digitized_profiles.json, у коме тог профила ионако нема.
    # Без `create=True` тест пада гласно ако се атрибут икад преименује.
    with patch.object(museum_app, '_DIGITIZED_PROFILES_PATH', str(profili_json)), \
         patch.object(phase3a_databases, 'digitized_profiles_table_exists',
                      side_effect=RuntimeError('baza pala')):
        resp = client.get('/api/map/digitized-profiles', base_url=BASE)
    assert resp.status_code == 503, resp.get_data(as_text=True)
    assert 'stari_profil' not in resp.get_data(as_text=True)
