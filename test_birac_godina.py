"""Регресија: бирач година се ИЗВОДИ ИЗ ПОДАТАКА.

После архивског увоза (листе 2011–2026) бирач је нудио само до 2024 (хардкодован
опсег tekuca-2..tekuca+2). Сада иде од најстарије листе која постоји до текуће
године — за запосленог скопирано на његове листе, за админа глобално.
"""

import os
from datetime import date

import pytest

os.environ.setdefault('DATABASE_URL', 'postgresql://localhost/museum_system')

try:
    from postgres_service import get_postgres_connection
    from timesheet_postgres import available_report_years
    _DB_OK = True
except Exception as exc:  # pragma: no cover
    _DB_OK = False
    _DB_ERR = exc

try:
    import app as museum_app
except Exception:  # pragma: no cover
    museum_app = None

_DB = pytest.mark.skipif(not _DB_OK, reason='нема базе')
_EMAIL = 'birac.godina.test@nhmbeo.rs'
_CURRENT = date.today().year


def _insert(year, month=3):
    with get_postgres_connection() as conn, conn.cursor() as cur:
        cur.execute(
            "INSERT INTO timesheet_reports (employee_email, employee_name, month, year, status) "
            "VALUES (%s, 'Бирач Тест', %s, %s, 'APPROVED') RETURNING id",
            (_EMAIL, month, year),
        )
        rid = cur.fetchone()[0]
        conn.commit()
        return rid


def _cleanup():
    with get_postgres_connection() as conn, conn.cursor() as cur:
        cur.execute("DELETE FROM timesheet_reports WHERE employee_email = %s", (_EMAIL,))
        conn.commit()


@_DB
def test_godine_izvedene_iz_podataka_scoped():
    _cleanup()
    _insert(2011)
    _insert(2015)
    try:
        years = available_report_years(_EMAIL)
        assert years[0] == 2011                      # од најстарије листе
        assert years[-1] == max(_CURRENT, 2015)      # до текуће године
        assert 2011 in years and 2015 in years and _CURRENT in years
        # непрекидан опсег
        assert years == list(range(2011, years[-1] + 1))
    finally:
        _cleanup()


@_DB
def test_godine_globalno_ukljucuju_najstariju():
    _cleanup()
    _insert(2011)
    try:
        assert 2011 in available_report_years()      # админ/шеф: глобално
    finally:
        _cleanup()


@_DB
def test_prazan_scope_daje_bar_prethodnu_i_tekucu():
    _cleanup()
    years = available_report_years('nepostoji.niko@nhmbeo.rs')
    assert _CURRENT in years and (_CURRENT - 1) in years


@pytest.mark.skipif(museum_app is None or not _DB_OK, reason='апликација/база недоступни')
def test_pregled_stranica_nudi_2011():
    _cleanup()
    _insert(2011)
    prev = museum_app.app.config.get('WTF_CSRF_ENABLED', False)
    museum_app.app.config['WTF_CSRF_ENABLED'] = False
    try:
        c = museum_app.app.test_client()
        with c.session_transaction() as s:
            s['user_id'] = 4242
            s['user_email'] = _EMAIL
            s['user_role'] = 'employee'
            s['user_name'] = 'Бирач Тест'
            s['user_department'] = 'X'
            s['user_position'] = 'p'
            s['is_department_head'] = False
        html = c.get('/timesheet/view', base_url='https://localhost').get_data(as_text=True)
        assert 'value="2011"' in html, 'бирач на прегледу не нуди 2011'
    finally:
        museum_app.app.config['WTF_CSRF_ENABLED'] = prev
        _cleanup()
