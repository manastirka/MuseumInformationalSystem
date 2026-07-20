#!/usr/bin/env python3
"""Тестови за увоз радних листа из Word-а (.docx).

Слојеви по брзини/зависностима:

1. ПАРСЕР (`radna_lista_word_parser`) — без базе, без Flask-а. Гради .docx
   фикстуре у меморији (`tests/fixtures/radne_liste/make_fixtures.py`) и
   проверава оба распореда (дани-редови / дани-колоне), латиницу и одбијање
   поломљених докумената.
2. МАПИРАЊЕ имена (`timesheet_import.match_employee`) — тражи PostgreSQL;
   прескаче се ако база није доступна.
3. АРХИВСКИ и ТЕКУЋИ ток увоза (`import_archive` / `import_current`) — пишу у
   базу; самочистећи (бришу свој ред у `finally`), идемпотентни, користе
   годину 2099 / лажни е-mail да не ударе у стварне записе.

Скип на бази прати образац из `test_kr_dosije.py`.
"""

import os
import sys

import pytest

os.environ.setdefault('FLASK_ENV', 'testing')
os.environ.setdefault('SECRET_KEY', 'test-secret')
os.environ.setdefault('REDIS_URL', '')
os.environ.setdefault('SESSION_TYPE', 'filesystem')
os.environ.setdefault('SESSION_FILE_DIR', '/tmp/museum-test-flask-session')

import radna_lista_word_parser as rl

# Фикстура-генератор (није пакет — додајемо фолдер на путању).
_FIXTURES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             'tests', 'fixtures', 'radne_liste')
sys.path.insert(0, _FIXTURES_DIR)
import make_fixtures as mk  # noqa: E402


# ===========================================================================
# 1) ПАРСЕР — без базе
# ===========================================================================
class TestParserCorrectMatrix:
    def test_days_rows_osnovni_podaci(self):
        parsed = rl.parse_radna_lista(mk.build_correct_matrix_days_rows())
        assert parsed['employee_name'] == mk.EMPLOYEE_NAME
        assert parsed['month'] == 9
        assert parsed['year'] == 2025
        assert parsed['orientation'] == 'days_rows'
        assert parsed['organization_unit'] == mk.ORG_UNIT
        assert parsed['position'] == mk.POSITION

    def test_days_rows_dnevni_sati(self):
        parsed = rl.parse_radna_lista(mk.build_correct_matrix_days_rows())
        daily = parsed['daily_data']
        # Конкретни дани.
        assert daily['1'] == {'rad_na_mestu': 8.0}
        assert daily['11'] == {'van_muzeja': 8.0}
        assert daily['15'] == {'godisnji_odmor': 8.0}
        assert daily['22'] == {'drzavni_praznik': 8.0}
        # Викенд (6,7) нема унос → нема кључа.
        assert '6' not in daily
        assert '7' not in daily
        # Цела матрица једнака извору.
        assert daily == mk.expected_daily_data()

    def test_days_rows_totali(self):
        totals = rl.parse_radna_lista(mk.build_correct_matrix_days_rows())['totals']
        assert totals['radni'] == 144.0   # rad_na_mestu (128) + van_muzeja (16)
        assert totals['sve'] == 176.0     # + godisnji (24) + praznik (8)
        assert totals['po_kategoriji']['rad_na_mestu'] == 128.0
        assert totals['po_kategoriji']['van_muzeja'] == 16.0
        assert totals['po_kategoriji']['godisnji_odmor'] == 24.0
        assert totals['po_kategoriji']['drzavni_praznik'] == 8.0

    def test_transponovano_daje_iste_podatke(self):
        rows = rl.parse_radna_lista(mk.build_correct_matrix_days_rows())
        cols = rl.parse_radna_lista(mk.build_transposed_days_cols())
        assert cols['orientation'] == 'days_cols'
        # Иста матрица и исти тотали, само друга оријентација.
        assert cols['daily_data'] == rows['daily_data']
        assert cols['totals'] == rows['totals']

    def test_latinica(self):
        parsed = rl.parse_radna_lista(mk.build_latin_variant())
        assert parsed['month'] == 9
        assert parsed['year'] == 2025
        assert parsed['employee_name'] == 'Petar Petrović'
        # Латиничне ознаке се мапирају на исте канонске кодове.
        assert parsed['daily_data'] == mk.expected_daily_data()


class TestParserBroken:
    def test_bez_matrice_baca(self):
        with pytest.raises(rl.RadnaListaParseError) as exc:
            rl.parse_radna_lista(mk.build_broken_no_matrix())
        msg = str(exc.value)
        assert msg.strip()                    # порука није празна
        assert 'матриц' in msg                # објашњава разлог

    def test_bez_imena_baca(self):
        with pytest.raises(rl.RadnaListaParseError) as exc:
            rl.parse_radna_lista(mk.build_broken_no_name())
        msg = str(exc.value)
        assert msg.strip()
        assert 'име' in msg

    def test_poremecen_dokument_baca_pre_bilo_kakvog_uvoza(self):
        """Поломљен документ пада на парсирању → до import_* никад не стигне."""
        with pytest.raises(rl.RadnaListaParseError):
            # Ако би ово прошло, тек бисмо онда звали import_archive/current.
            rl.parse_radna_lista(mk.build_broken_no_matrix())


# ===========================================================================
# Заједничко за тестове са базом
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
_DB_SKIP = pytest.mark.skipif(not _DB_OK, reason='PostgreSQL није доступан')

_ADMIN_EMAIL = 'admin@nhmbeo.rs'


def _fetch_one_active_user():
    """(email, full_name) једног активног корисника, или (None, None)."""
    from postgres_service import get_postgres_connection
    with get_postgres_connection() as conn, conn.cursor() as cur:
        cur.execute(
            "SELECT email, full_name FROM users "
            "WHERE is_active = TRUE AND full_name IS NOT NULL "
            "AND length(trim(full_name)) > 3 LIMIT 1"
        )
        row = cur.fetchone()
    return (row[0], row[1]) if row else (None, None)


# ===========================================================================
# 2) МАПИРАЊЕ имена → корисник
# ===========================================================================
import timesheet_import as ti  # noqa: E402


@_DB_SKIP
def test_match_employee_pouzdano_za_postojeceg():
    email, full_name = _fetch_one_active_user()
    if not email:
        pytest.skip('нема активних корисника у бази за поклапање')
    from postgres_service import get_postgres_connection
    with get_postgres_connection() as conn, conn.cursor() as cur:
        res = ti.match_employee(cur, full_name)
    assert res['email'] is not None
    assert res['confident'] is True
    assert res['score'] >= 0.82
    assert isinstance(res['candidates'], list)


@_DB_SKIP
def test_match_employee_besmisleno_ime():
    from postgres_service import get_postgres_connection
    with get_postgres_connection() as conn, conn.cursor() as cur:
        res = ti.match_employee(cur, 'Џкхзвћ Непостојећиков Кс9999')
    assert res['email'] is None
    assert res['confident'] is False
    assert isinstance(res['candidates'], list)


# ===========================================================================
# 3) АРХИВСКИ ток → директно APPROVED (самочистећи, година 2099)
# ===========================================================================
def _delete_report(report_id):
    from postgres_service import get_postgres_connection
    with get_postgres_connection() as conn, conn.cursor() as cur:
        cur.execute('DELETE FROM timesheet_report_days WHERE report_id = %s',
                    (report_id,))
        cur.execute('DELETE FROM timesheet_reports WHERE id = %s', (report_id,))
        conn.commit()


@_DB_SKIP
def test_import_archive_upisuje_approved_i_dane():
    from postgres_service import get_postgres_connection

    fake_email = 'qa.word.arhiva.2099@example.invalid'
    fake_name = 'Тест Архивски Запослени'
    parsed = rl.parse_radna_lista(
        mk.build_correct_matrix_days_rows(name=fake_name, month=9, year=2099))

    ok, msg, report_id = ti.import_archive(parsed, fake_email, fake_name, _ADMIN_EMAIL)
    assert ok is True
    assert report_id is not None

    try:
        with get_postgres_connection() as conn, conn.cursor() as cur:
            cur.execute(
                "SELECT status, is_locked, is_verified, verified_role, imported_from "
                "FROM timesheet_reports WHERE id = %s", (report_id,))
            row = cur.fetchone()
            assert row is not None
            status, is_locked, is_verified, verified_role, imported_from = row
            assert status == 'APPROVED'
            assert is_locked is True
            assert is_verified is True
            assert verified_role == 'uvoz-arhiva'
            assert imported_from == 'word-arhiva'

            cur.execute(
                "SELECT count(*) FROM timesheet_report_days WHERE report_id = %s",
                (report_id,))
            n_days = cur.fetchone()[0]
            assert n_days == len(mk.SAMPLE_DAILY)

        # Идемпотентност: поновни увоз враћа ИСТИ ред (нема дупликата).
        ok2, _msg2, report_id2 = ti.import_archive(
            parsed, fake_email, fake_name, _ADMIN_EMAIL)
        assert ok2 is True
        assert report_id2 == report_id
    finally:
        _delete_report(report_id)


# ===========================================================================
# 4) ТЕКУЋИ ток → сачувано + послато (SUBMITTED), самочистећи
# ===========================================================================
def _submittable_period():
    """(month, year) који је сигурно унутар прозора за подношење.

    Подразумевано `default_entry_period()` (претходни месец); ако тренутни
    датум није у прозору 1–10, пада на текући месец (увек подношив).
    """
    import timesheet_postgres as tp
    month, year = tp.default_entry_period()
    can, _ = tp.can_submit_for_review(month, year)
    if can:
        return month, year
    from datetime import datetime
    now = datetime.now()
    return now.month, now.year


@_DB_SKIP
def test_import_current_cuva_i_salje_submitted():
    from postgres_service import get_postgres_connection

    test_email = 'qa.word.tekuca@example.invalid'
    test_name = 'КУ Тест Текући'
    month, year = _submittable_period()
    parsed = rl.parse_radna_lista(
        mk.build_correct_matrix_days_rows(name=test_name, month=month, year=year,
                                          daily=mk.SAFE_DAILY))

    ok, msg, report_id = ti.import_current(test_email, test_name, parsed)
    assert ok is True, msg
    assert report_id is not None

    try:
        with get_postgres_connection() as conn, conn.cursor() as cur:
            cur.execute(
                "SELECT status, imported_from FROM timesheet_reports WHERE id = %s",
                (report_id,))
            status, imported_from = cur.fetchone()
        assert imported_from == 'word-tekuca'
        # Уз изабрани прозор за подношење очекујемо SUBMITTED; ако би окружење
        # ипак блокирало слање, DRAFT је прихватљив (уз ok==True и ознаку).
        assert status in ('SUBMITTED', 'DRAFT')
        assert status == 'SUBMITTED', f'очекиван SUBMITTED, добијен {status} ({msg})'
    finally:
        _delete_report(report_id)
