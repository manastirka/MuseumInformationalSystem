#!/usr/bin/env python3
"""Тестови безбедносних исправки из ревизије 2026-08 (батч 1).

Сваки тест је писан тако да ПАДА на коду пре исправке:
  1. ускладиштени XSS у модалу прегледа радних листа (escapeHtml);
  2. `admin_only` декоратор — директор нема приступ password manager-у,
     SMTP и системским рутама;
  3. ресет лозинке не сме на туђ админ налог;
  4. IDOR на К-Р предлошцима (измена/брисање ван свог одељења);
  5. add_user — allow-листа улога по позиваоцу + права политика лозинки.

БЕЗБЕДНОСТ: ради ИСКЉУЧИВО над базом чије име садржи '_test'
(подразумевано museum_system_test) — никад над museum_system.

Покретање:
    python -m pytest test_revizija_bezbednost.py -q
"""

import json
import os
import subprocess
import tempfile

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

museum_app.app.config['TESTING'] = True
museum_app.app.config['WTF_CSRF_ENABLED'] = False

BASE = 'https://localhost'


def _db():
    return psycopg.connect(PLAIN_URL)


def _login(client, *, email, role, user_id=990001,
           department='Природњачки музеј', **extra):
    with client.session_transaction() as s:
        s['user_id'] = user_id
        s['user_email'] = email
        s['user_name'] = 'Тест Ревизија'
        s['user_role'] = role
        s['user_department'] = department
        s['is_admin'] = role in ('admin', 'direktor')
        for k, v in extra.items():
            s[k] = v
    return client


def _client():
    return museum_app.app.test_client()


# ===========================================================================
# 1. Ускладиштени XSS у модалу прегледа радних листа
# ===========================================================================
XSS_PAYLOAD = '<img src=x onerror=alert(1)>'
XSS_EMAIL = 'xss.revizija@example.invalid'


def _extract_js_function(page_html, name):
    """Извуци цео `function name(...) {...}` блок бројањем заграда."""
    start = page_html.index('function ' + name)
    i = page_html.index('{', start)
    depth = 0
    for j in range(i, len(page_html)):
        if page_html[j] == '{':
            depth += 1
        elif page_html[j] == '}':
            depth -= 1
            if depth == 0:
                return page_html[start:j + 1]
    raise AssertionError(f'нисам нашао крај функције {name}')


def _try_extract_js_function(page_html, name):
    try:
        return _extract_js_function(page_html, name)
    except ValueError:
        return ''


def _render_modal_with_node(page_html, report):
    """Изврши СТВАРНИ JS из испорученог шаблона (displayReportDetails, и
    escapeHtml ако постоји) под node-ом, са минималним DOM стубом који
    верно опонаша escape преко textContent/innerHTML."""
    harness = (
        "const report = JSON.parse(process.argv[2]);\n"
        "const modalBody = { innerHTML: '' };\n"
        "global.document = {\n"
        "    getElementById: () => modalBody,\n"
        "    createElement: () => {\n"
        "        let text = '';\n"
        "        return {\n"
        "            set textContent(v) { text = v == null ? '' : String(v); },\n"
        "            get innerHTML() {\n"
        "                return text.replace(/&/g, '&amp;')\n"
        "                    .replace(/</g, '&lt;').replace(/>/g, '&gt;');\n"
        "            },\n"
        "        };\n"
        "    },\n"
        "};\n"
        + _try_extract_js_function(page_html, 'escapeHtml') + '\n'
        + _extract_js_function(page_html, 'displayReportDetails') + '\n'
        + 'displayReportDetails(report);\n'
        + 'process.stdout.write(modalBody.innerHTML);\n'
    )
    fd, path = tempfile.mkstemp(suffix='.js')
    try:
        with os.fdopen(fd, 'w') as f:
            f.write(harness)
        run = subprocess.run(['node', path, json.dumps(report)],
                             capture_output=True, text=True, timeout=30)
    finally:
        os.unlink(path)
    assert run.returncode == 0, run.stderr
    return run.stdout


@pytest.fixture
def xss_report_id():
    with _db() as conn:
        cur = conn.execute(
            """
            INSERT INTO timesheet_reports
                (employee_name, employee_email, month, year, organization_unit,
                 position, duties_summary, special_tasks, status)
            VALUES (%s, %s, 1, 2020, %s, %s, %s, %s, 'SUBMITTED')
            RETURNING id
            """,
            (XSS_PAYLOAD, XSS_EMAIL, XSS_PAYLOAD, XSS_PAYLOAD,
             XSS_PAYLOAD, XSS_PAYLOAD),
        )
        report_id = cur.fetchone()[0]
        conn.commit()
    yield report_id
    with _db() as conn:
        conn.execute('DELETE FROM timesheet_reports WHERE employee_email = %s',
                     (XSS_EMAIL,))
        conn.commit()


def test_xss_payload_izlazi_escapovan_iz_modala(xss_report_id):
    """БАГ (ревизија 2026-08 #1): payload сачуван у радну листу мора изаћи
    escape-ован из JS-а који гради модал — не сме постати <img> елемент."""
    client = _login(_client(), email='admin.revizija@example.invalid', role='admin')

    resp = client.get(f'/api/admin/timesheet/report/{xss_report_id}', base_url=BASE)
    data = resp.get_json()
    assert data and data.get('success'), data
    header = data['report'].get('header') or {}
    assert XSS_PAYLOAD in (header.get('duties_summary') or ''), \
        'payload није round-trip-овао кроз базу — фикстура не ваља'

    page = client.get('/admin/timesheet_reports', base_url=BASE)
    assert page.status_code == 200
    rendered = _render_modal_with_node(page.get_data(as_text=True), data['report'])
    assert '<img' not in rendered, 'payload је постао живи HTML елемент (XSS!)'
    assert '&lt;img' in rendered, 'payload се уопште не приказује escape-ован'


# ===========================================================================
# 2. admin_only — директор нема приступ техничким рутама
# ===========================================================================
def test_direktor_403_na_password_manager_reset():
    """ОДЛУКА (ревизија 2026-08 #2): password manager је admin-only."""
    client = _login(_client(), email='direktor.revizija@example.invalid',
                    role='direktor')
    resp = client.post('/api/admin/password_manager/reset', json={}, base_url=BASE)
    assert resp.status_code == 403, resp.get_data(as_text=True)


def test_admin_prolazi_gejt_na_password_manager_reset():
    """Админ пролази admin_only гејт (празан захтев → 400, никад 403)."""
    client = _login(_client(), email='admin.revizija@example.invalid', role='admin')
    resp = client.post('/api/admin/password_manager/reset', json={}, base_url=BASE)
    assert resp.status_code == 400, resp.get_data(as_text=True)


def test_direktor_403_na_smtp_rute():
    client = _login(_client(), email='direktor.revizija@example.invalid',
                    role='direktor')
    resp = client.get('/api/admin/mail-settings/state', base_url=BASE)
    assert resp.status_code == 403, resp.get_data(as_text=True)


def test_admin_prolazi_na_smtp_rute():
    client = _login(_client(), email='admin.revizija@example.invalid', role='admin')
    resp = client.get('/api/admin/mail-settings/state', base_url=BASE)
    assert resp.status_code != 403, resp.get_data(as_text=True)


def test_direktor_403_na_sistemske_rute():
    client = _login(_client(), email='direktor.revizija@example.invalid',
                    role='direktor')
    resp = client.get('/api/admin/database/table-stats', base_url=BASE)
    assert resp.status_code == 403, resp.get_data(as_text=True)


def test_admin_prolazi_na_sistemske_rute():
    client = _login(_client(), email='admin.revizija@example.invalid', role='admin')
    resp = client.get('/api/admin/database/table-stats', base_url=BASE)
    assert resp.status_code == 200, resp.get_data(as_text=True)
