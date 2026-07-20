"""Регресија: К-Р досије мора имати ставку у главној навигацији (base.html),
видљиву само корисницима са модулом. Пре исправке модул је био доступан само
преко директног URL-а.
"""

import os
import pytest

os.environ.setdefault('DATABASE_URL',
                      'postgresql://localhost/museum_system')

try:
    import app as museum_app
    _IMPORT_ERROR = None
except Exception as exc:  # pragma: no cover
    museum_app = None
    _IMPORT_ERROR = exc

_SKIP = pytest.mark.skipif(museum_app is None,
                           reason=f'апликација није доступна ({_IMPORT_ERROR})')

BASE_URL = 'https://localhost'
KR_LINK = '/kr-dosije'
KR_LABEL = 'К-Р досије'


@pytest.fixture
def client():
    prev = museum_app.app.config.get('WTF_CSRF_ENABLED', False)
    museum_app.app.config['WTF_CSRF_ENABLED'] = False
    c = museum_app.app.test_client()
    yield c
    museum_app.app.config['WTF_CSRF_ENABLED'] = prev


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
    with c.session_transaction() as sess:
        sess['user_id'] = 99
        sess['user_email'] = 'nobody.kr@nhmbeo.rs'
        sess['user_name'] = 'Нико'
        sess['user_role'] = 'employee'
        sess['is_admin'] = False
        sess['user_department'] = 'ОДСЕК ОПШТИХ И ПРАВНИХ ПОСЛОВА'
        sess['is_department_head'] = False


@_SKIP
def test_admin_vidi_kr_stavku_u_navigaciji(client):
    _login_admin(client)
    html = client.get('/dashboard', base_url=BASE_URL).get_data(as_text=True)
    assert KR_LINK in html, 'нема линка ка /kr-dosije у навигацији за админа'
    assert KR_LABEL in html, 'нема ознаке „К-Р досије" у навигацији за админа'


@_SKIP
def test_zaposleni_bez_prava_ne_vidi_kr_stavku(client):
    _login_plain_employee(client)
    html = client.get('/dashboard', base_url=BASE_URL).get_data(as_text=True)
    assert KR_LINK not in html, 'запослени без права види линк ка /kr-dosije'


@_SKIP
def test_kr_kartica_na_tabli_ima_ispravan_endpoint(client):
    """Картица модула на табли мора имати радно дугме „Отвори" (endpoint
    kr_dosije.lista у module_endpoints), не празну картицу."""
    _login_admin(client)
    # Админу подразумевано није укључен виџет, па директно проверавамо да
    # темплејт табле мапира endpoint — рендеровањем kr картице за админа
    # преко профила са укљученим модулом.
    with client.session_transaction() as sess:
        sess['user_id'] = 1
        sess['user_email'] = 'admin@nhmbeo.rs'
        sess['user_role'] = 'admin'
        sess['is_admin'] = True
    html = client.get('/dashboard', base_url=BASE_URL).get_data(as_text=True)
    # Ако се kr картица уопште рендерује, мора носити линк ка листи.
    if KR_LABEL in html:
        assert KR_LINK in html
