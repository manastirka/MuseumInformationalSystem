"""Тестови за `flask uvezi-arhivske-liste` — масовни архивски CLI увоз.

Мини фолдер фикстура: 2 године, дупликат истог месеца, годишњи извештај (није
месечна листа). Проверава dry-run план (OK/прескочен+разлог, дедупликација) и
стваран упис (APPROVED/word-arhiva). Само-чисти; прескаче се без базе.
"""

import os
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'tests', 'fixtures', 'radne_liste'))

import make_fixtures as mk
import uvezi_arhivske_liste_cli as cli

try:
    from postgres_service import get_postgres_connection
    _DB_OK = True
except Exception as exc:  # pragma: no cover
    _DB_OK = False
    _DB_ERR = exc

_DB = pytest.mark.skipif(not _DB_OK, reason='нема базе')
_EMPLOYEE = 'Милош Мрваљевић'   # постојећи корисник (мапира се поуздано)
_EMAIL = 'milos.mrvaljevic@nhmbeo.rs'


@pytest.fixture
def arhiva(tmp_path):
    """Фолдер: 2098/maj.docx, 2098/godisnji.docx, 2099/jun.docx, 2099/jun_dup.docx."""
    (tmp_path / '2098').mkdir()
    (tmp_path / '2099').mkdir()
    def w(rel, buf):
        (tmp_path / rel).write_bytes(buf.getvalue() if hasattr(buf, 'getvalue') else buf.read())
    w('2098/maj.docx', mk.build_correct_matrix_days_rows(name=_EMPLOYEE, month=5, year=2098))
    w('2098/godisnji_izvestaj.docx', mk.build_broken_no_matrix())
    w('2099/jun.docx', mk.build_correct_matrix_days_rows(name=_EMPLOYEE, month=6, year=2099))
    w('2099/jun_dup.docx', mk.build_correct_matrix_days_rows(name=_EMPLOYEE, month=6, year=2099))
    return str(tmp_path)


# --- unit: _resolve_owner (без базе) ---
def test_resolve_owner_ime_mapira():
    m = {'confident': True, 'email': 'a@x.rs'}
    owner, warn = cli._resolve_owner(m, None)
    assert owner == 'a@x.rs' and warn is None


def test_resolve_owner_upozori_na_drugog_korisnika():
    m = {'confident': True, 'email': 'a@x.rs'}
    owner, warn = cli._resolve_owner(m, 'b@x.rs')
    assert owner == 'a@x.rs' and warn and 'a@x.rs' in warn and 'b@x.rs' in warn


def test_resolve_owner_fallback_na_korisnika():
    m = {'confident': False, 'email': None}
    assert cli._resolve_owner(m, 'b@x.rs') == ('b@x.rs', None)
    assert cli._resolve_owner(m, None) == (None, None)


# --- план (dry-run): дедупликација + прескакање годишњег ---
@_DB
def test_plan_dry_run(arhiva):
    with get_postgres_connection() as conn, conn.cursor() as cur:
        results = cli.plan_import(arhiva, None, cur)
    by_file = {r['file']: r for r in results}
    assert len(results) == 4
    assert by_file['2098/maj.docx']['ok'] and by_file['2098/maj.docx']['owner'] == _EMAIL
    assert by_file['2099/jun.docx']['ok']
    # дупликат истог месеца (у истом покретању) — прескочен
    dup = by_file['2099/jun_dup.docx']
    assert not dup['ok'] and 'дупликат' in dup['razlog']
    # годишњи извештај — није месечна листа
    god = by_file['2098/godisnji_izvestaj.docx']
    assert not god['ok'] and 'није месечна листа' in god['razlog']
    assert sum(1 for r in results if r['ok']) == 2


# --- стваран упис + чишћење ---
@_DB
def test_execute_upisuje_arhiva(arhiva):
    try:
        with get_postgres_connection() as conn, conn.cursor() as cur:
            results = cli.plan_import(arhiva, None, cur)
        for r in [x for x in results if x['ok']]:
            import timesheet_import as ti
            ok, _m, _id = ti.import_archive(r['parsed'], r['owner'], r['ime'], 'test@x.rs')
            assert ok
        with get_postgres_connection() as conn, conn.cursor() as cur:
            cur.execute(
                "SELECT month, year, status, imported_from FROM timesheet_reports "
                "WHERE employee_email=%s AND year IN (2098, 2099) ORDER BY year",
                (_EMAIL,),
            )
            rows = cur.fetchall()
        assert len(rows) == 2
        # Ревизија ланца: архива се уписује као класификација 'ARHIVA', не APPROVED.
        for _m, _y, status, src in rows:
            assert status == 'ARHIVA' and src == 'word-arhiva'
    finally:
        with get_postgres_connection() as conn, conn.cursor() as cur:
            cur.execute("DELETE FROM timesheet_reports WHERE employee_email=%s "
                        "AND year IN (2098, 2099)", (_EMAIL,))
            conn.commit()
