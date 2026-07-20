"""Листа К-Р досијеа: пагинација + „повратак на место" (истицање/скрол).

Клијентски део (скрол, истицање, history.back) покрива Playwright; овде се
проверава серверски уговор: пагинација чува филтере, редови носе id, а
шаблони садрже механизам за истицање/повратак.
"""

import os
import uuid
import pytest

os.environ.setdefault('DATABASE_URL', 'postgresql://localhost/museum_system')

try:
    import app as museum_app
    _ERR = None
except Exception as exc:  # pragma: no cover
    museum_app = None
    _ERR = exc

_SKIP = pytest.mark.skipif(museum_app is None, reason=f'нема апликације ({_ERR})')
BASE = 'https://localhost'
MARK = 'ПОВРАТАК-ТЕСТ'


@pytest.fixture
def client():
    prev = museum_app.app.config.get('WTF_CSRF_ENABLED', False)
    museum_app.app.config['WTF_CSRF_ENABLED'] = False
    c = museum_app.app.test_client()
    yield c
    museum_app.app.config['WTF_CSRF_ENABLED'] = prev


def _admin(c):
    with c.session_transaction() as s:
        s['user_id'] = 1
        s['user_email'] = 'admin@nhmbeo.rs'
        s['user_role'] = 'admin'
        s['is_admin'] = True
        s['user_department'] = 'Администрација'
        s['is_department_head'] = False


@pytest.fixture
def many_dossiers():
    """Направи 30 гео досијеа (2 стране) па их обриши после теста."""
    from postgres_service import get_postgres_connection
    ids = []
    with get_postgres_connection() as conn, conn.cursor() as cur:
        for _ in range(30):
            cur.execute(
                """INSERT INTO kr_dosije (evidencioni_broj, odeljenje, naziv_predmeta)
                   VALUES (%s, 'geo', %s) RETURNING id""",
                (f'КР-ГЕО-2097-{uuid.uuid4().hex[:8]}', f'{MARK} {uuid.uuid4().hex[:6]}'),
            )
            ids.append(cur.fetchone()[0])
        conn.commit()
    yield ids
    with get_postgres_connection() as conn, conn.cursor() as cur:
        cur.execute("DELETE FROM kr_dosije WHERE naziv_predmeta LIKE %s", (MARK + '%',))
        conn.commit()


@_SKIP
def test_druga_strana_i_filteri_u_linkovima(client, many_dossiers):
    _admin(client)
    html = client.get(BASE + '/kr-dosije?page=2&odeljenje=geo').get_data(as_text=True)
    assert 'pagination' in html
    # активна страна 2
    import re
    active = re.search(r'page-item active[^>]*>\s*<a[^>]*>(\d+)', html)
    assert active and active.group(1) == '2'
    # линкови страница чувају филтер одељења
    assert 'odeljenje=geo' in html
    assert 'page=1' in html and 'page=3' in html


@_SKIP
def test_redovi_nose_id_za_skrol(client, many_dossiers):
    _admin(client)
    html = client.get(BASE + '/kr-dosije').get_data(as_text=True)
    import re
    assert re.search(r'id="kr-dosije-\d+"', html)
    # линк отвара досије и памти га за истицање
    assert 'data-kr-open=' in html


@_SKIP
def test_strana_van_opsega_se_svede(client, many_dossiers):
    _admin(client)
    r = client.get(BASE + '/kr-dosije?page=9999')
    assert r.status_code == 200
    import re
    active = re.search(r'page-item active[^>]*>\s*<a[^>]*>(\d+)', r.get_data(as_text=True))
    # свело на последњу постојећу страну (не празно, не пад)
    assert active is not None


@_SKIP
def test_lista_ima_mehanizam_isticanja(client):
    _admin(client)
    html = client.get(BASE + '/kr-dosije').get_data(as_text=True)
    assert 'krLastOpened' in html      # памћење отвореног досијеа
    assert 'kr-vraceno' in html        # класа истицања
    assert 'pageshow' in html          # ради и за browser back (bfcache)
    assert 'scrollIntoView' in html    # скрол на ред


@_SKIP
def test_detalj_ima_pametan_povratak(client, many_dossiers):
    _admin(client)
    did = many_dossiers[0]
    html = client.get(BASE + f'/kr-dosije/{did}').get_data(as_text=True)
    assert 'kr-nazad' in html
    assert 'history.back' in html
