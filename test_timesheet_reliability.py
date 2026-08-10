#!/usr/bin/env python3
"""Reliability test suite за timesheet систем (pytest).

Покрива: валидацију, интегритет података (save/load, тригер синхронизацију),
конкурентност (оптимистичко закључавање, паралелна чувања), ивичне случајеве
(преступна година, 31-дневни месец, празна листа, специјални карактери),
rate limiting захтева за измену и структуру error guidance одговора.

Сваки тест ПАДА кроз assert када логика откаже — нема record_pass/record_fail
бројача који гута исходе.

БЕЗБЕДНОСТ:
  - ради ИСКЉУЧИВО над базом чије име садржи '_test'
    (подразумевано museum_system_test) — никад над museum_system;
  - сви редови које тестови праве користе синтетичке адресе на
    @example.invalid домену, а чишћење брише ИСКЉУЧИВО по тим адресама
    (employee_email = ANY(...)) — никад по префиксу имена.

Покретање:
    python -m pytest test_timesheet_reliability.py -q
"""

import os
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime

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
from psycopg.rows import dict_row  # noqa: E402

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

import timesheet_postgres as tp  # noqa: E402

# ---------------------------------------------------------------------------
# Синтетички идентитети — све на @example.invalid, чишћење само по њима.
# ---------------------------------------------------------------------------
TEST_EMAIL = 'reliability.primary@example.invalid'
TEST_NAME = 'Reliability Primary'
TRIGGER_EMAIL = 'reliability.trigger@example.invalid'
OPTLOCK_EMAIL = 'reliability.optlock@example.invalid'
LOCK_EMAIL = 'reliability.lock@example.invalid'
LEAP_EMAIL = 'reliability.leap@example.invalid'
MONTH31_EMAIL = 'reliability.month31@example.invalid'
EMPTY_EMAIL = 'reliability.empty@example.invalid'
SPECIAL_EMAIL = 'reliability.special@example.invalid'
RATE_LIMIT_EMAIL = 'reliability.rate-limit@example.invalid'
CONCURRENT_EMAILS = {
    i: f'reliability.concurrent.{i}@example.invalid' for i in range(1, 7)
}
BATCH_EMAILS = [f'reliability.batch.{i}@example.invalid' for i in range(1, 4)]
BATCH_ADMIN_EMAIL = 'reliability.batch-admin@example.invalid'

ALL_TEST_EMAILS = [
    TEST_EMAIL, TRIGGER_EMAIL, OPTLOCK_EMAIL, LOCK_EMAIL, LEAP_EMAIL,
    MONTH31_EMAIL, EMPTY_EMAIL, SPECIAL_EMAIL, RATE_LIMIT_EMAIL,
    *CONCURRENT_EMAILS.values(), *BATCH_EMAILS, BATCH_ADMIN_EMAIL,
]

# ---------------------------------------------------------------------------
# Експлицитни прагови
# ---------------------------------------------------------------------------
# Сати се пореде као float — толеранција за numeric->float конверзију.
HOURS_TOLERANCE = 0.01
# Паралелна чувања: 6 радника, свих 6 МОРА да успе (упис је транзакциона
# операција за различите кориснике — делимичан успех = регресија).
CONCURRENT_SAVE_WORKERS = 6
CONCURRENT_SAVE_REQUIRED_SUCCESSES = 6
# editable_until прозор за seed-оване извештаје ван рока уноса (минута).
SEED_EDIT_WINDOW_MINUTES = 60

# save_timesheet_to_postgres дозвољава упис само за текући месец (или
# претходни до 10. у месецу) — тестови зато раде над ТЕКУЋИМ месецом, а
# периоде ван рока (преступни фебруар, 31-дневни јануар) добијају кроз
# seed-ован DRAFT са активним editable_until прозором (докуменотвани
# override рока у save слоју).
_NOW = datetime.now()
CURRENT_MONTH = _NOW.month
CURRENT_YEAR = _NOW.year


def _db():
    return psycopg.connect(PLAIN_URL, row_factory=dict_row)


def _cleanup_test_data():
    """Брише искључиво редове синтетичких @example.invalid идентитета."""
    with _db() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "DELETE FROM timesheet_edit_requests "
                "WHERE requester_email = ANY(%s)", (ALL_TEST_EMAILS,))
            cur.execute(
                "DELETE FROM timesheet_report_days WHERE report_id IN "
                "(SELECT id FROM timesheet_reports "
                " WHERE employee_email = ANY(%s))", (ALL_TEST_EMAILS,))
            cur.execute(
                "DELETE FROM timesheet_entries WHERE report_id IN "
                "(SELECT id FROM timesheet_reports "
                " WHERE employee_email = ANY(%s))", (ALL_TEST_EMAILS,))
            cur.execute(
                "DELETE FROM timesheet_reports "
                "WHERE employee_email = ANY(%s)", (ALL_TEST_EMAILS,))
            conn.commit()


@pytest.fixture(scope='module', autouse=True)
def _preusmeri_bazu_na_test():
    """У пуном suite-у је app можда већ увезен са DATABASE_URL из .env
    (museum_system!) и pool-ови већ везани — преусмери env и ресетуј СВЕ
    pool-ове на *_test базу док траје овај модул, па врати старо стање."""
    import postgres_service
    old_env = os.environ.get('DATABASE_URL')
    old_tp_url = tp.DATABASE_URL
    os.environ['DATABASE_URL'] = TEST_DB_URL
    postgres_service.close_connection_pools()
    tp.close_connection_pool()
    tp.DATABASE_URL = TEST_DB_URL
    _cleanup_test_data()
    yield
    _cleanup_test_data()
    postgres_service.close_connection_pools()
    tp.close_connection_pool()
    tp.DATABASE_URL = old_tp_url
    if old_env is not None:
        os.environ['DATABASE_URL'] = old_env


def _save(email, name, month=CURRENT_MONTH, year=CURRENT_YEAR, *,
          daily_data, work_description='Reliability test',
          expected_version=None):
    return tp.save_timesheet_to_postgres(
        user_email=email,
        user_name=name,
        month=month,
        year=year,
        daily_data=daily_data,
        work_description=work_description,
        organization_unit='Test Unit',
        position='Test Position',
        expected_version=expected_version,
    )


def _seed_editable_report(email, name, month, year):
    """DRAFT извештај са активним editable_until прозором — једини начин да
    save слој прими упис за месец ван рока уноса (правило 5 override)."""
    with _db() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO timesheet_reports "
                "(employee_email, employee_name, month, year, status, "
                " is_locked, version, editable_until) "
                "VALUES (%s, %s, %s, %s, 'DRAFT', FALSE, 1, "
                "        NOW() + make_interval(mins => %s)) RETURNING id",
                (email, name, month, year, SEED_EDIT_WINDOW_MINUTES))
            rid = cur.fetchone()['id']
            conn.commit()
            return rid


def _lock_report(email, month, year):
    with _db() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "UPDATE timesheet_reports SET is_locked = TRUE "
                "WHERE employee_email = %s AND month = %s AND year = %s",
                (email, month, year))
            assert cur.rowcount == 1, (
                f'Очекиван тачно 1 извештај за закључавање, '
                f'нађено {cur.rowcount}')
            conn.commit()


# =============================================================================
# VALIDATION TESTS
# =============================================================================

def test_validation_negative_hours():
    """Негативни сати морају бити одбијени са јасном поруком."""
    error = tp.validate_hours(-5.0, 'test_field')
    assert error is not None, 'validate_hours(-5.0) мора вратити грешку'
    assert 'негативна' in error, f'Порука не помиње негативну вредност: {error}'


def test_validation_excessive_hours():
    """Сати > 24 морају бити одбијени."""
    error = tp.validate_hours(25.0, 'test_field')
    assert error is not None, 'validate_hours(25.0) мора вратити грешку'
    assert '24' in error, f'Порука не помиње лимит 24: {error}'


def test_validation_valid_hours():
    """Валидне вредности (0, 4, 8, 12, 24) пролазе без грешке."""
    for hours in [0, 4, 8, 12, 24]:
        error = tp.validate_hours(float(hours))
        assert error is None, f'Валидни сати {hours} одбијени: {error}'


def test_validation_month_year():
    """Месец 13 и година 1999 падају; 2/2026 пролази."""
    assert tp.validate_month_year(13, 2026) is not None, \
        'Месец 13 мора бити одбијен'
    assert tp.validate_month_year(1, 1999) is not None, \
        'Година 1999 мора бити одбијена'
    error = tp.validate_month_year(2, 2026)
    assert error is None, f'Валидан месец/година одбијен: {error}'


def test_validation_daily_data():
    """Дан 31 у фебруару пада; валидан дан пролази."""
    errors = tp.validate_daily_data({'31': {'rad_na_mestu': 8}}, 2, 2026)
    assert errors, 'Дан 31 у фебруару мора произвести грешку валидације'

    errors = tp.validate_daily_data(
        {'1': {'rad_na_mestu': 8, 'van_muzeja': 0}}, 2, 2026)
    assert errors == [], f'Валидни дневни подаци одбијени: {errors}'


# =============================================================================
# DATA INTEGRITY TESTS
# =============================================================================

def test_save_and_load_consistency():
    """Сачувани подаци се учитавају назад идентично (28 дана)."""
    daily_data = {}
    for day in range(1, 29):
        daily_data[str(day)] = {
            'rad_na_mestu': 8 if day % 7 not in [0, 6] else 0,
            'van_muzeja': 0,
            'godisnji_odmor': 0,
            'drzavni_praznik': 0,
            'placeno_odsustvo': 0,
            'ostalo_odsustvo': 0,
            'bolovanje_manje30': 0,
            'bolovanje_30_ili_vise': 0,
        }

    result = _save(TEST_EMAIL, TEST_NAME, daily_data=daily_data,
                   work_description='Save/load consistency')
    assert result.success, f'Чување није успело: {result.error.message}'

    loaded = tp.load_timesheet_from_postgres(
        TEST_EMAIL, CURRENT_MONTH, CURRENT_YEAR)
    assert loaded is not None, 'Учитавање вратило None после успешног чувања'

    for day_str, expected in daily_data.items():
        actual = loaded['daily_data'].get(int(day_str), {})
        for category, expected_hours in expected.items():
            actual_hours = actual.get(category, 0)
            assert abs(float(expected_hours) - float(actual_hours)) <= HOURS_TOLERANCE, (
                f'Дан {day_str}, {category}: очекивано {expected_hours}, '
                f'добијено {actual_hours}')


def test_trigger_sync():
    """Тригер агрегира timesheet_report_days у timesheet_entries."""
    daily_data = {
        '1': {'rad_na_mestu': 8},
        '2': {'rad_na_mestu': 8},
        '3': {'van_muzeja': 4},
        '4': {'godisnji_odmor': 8},
    }
    result = _save(TRIGGER_EMAIL, 'Reliability Trigger',
                   daily_data=daily_data, work_description='Trigger test')
    assert result.success, f'Чување није успело: {result.error.message}'

    with _db() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT te.category, te.hours
                FROM timesheet_entries te
                JOIN timesheet_reports tr ON tr.id = te.report_id
                WHERE tr.employee_email = %s AND tr.month = %s AND tr.year = %s
            """, (TRIGGER_EMAIL, CURRENT_MONTH, CURRENT_YEAR))
            entries = {row['category']: float(row['hours'])
                       for row in cur.fetchall()}

    expected = {
        'rad_na_mestu': 16.0,
        'van_muzeja': 4.0,
        'godisnji_odmor': 8.0,
    }
    for category, expected_hours in expected.items():
        actual = entries.get(category, 0)
        assert abs(expected_hours - actual) <= HOURS_TOLERANCE, (
            f'Тригер агрегат {category}: очекивано {expected_hours}, '
            f'добијено {actual} (сви уноси: {entries})')


# =============================================================================
# CONCURRENCY TESTS
# =============================================================================

def test_optimistic_locking():
    """Друго чување са застарелом верзијом пада са CONCURRENT_MODIFICATION."""
    initial = _save(OPTLOCK_EMAIL, 'Reliability Optlock',
                    daily_data={'1': {'rad_na_mestu': 8}},
                    work_description='Initial')
    assert initial.success, f'Почетно чување није успело: {initial.error.message}'
    initial_version = initial.data['version']

    first_update = _save(OPTLOCK_EMAIL, 'Reliability Optlock',
                         daily_data={'1': {'rad_na_mestu': 4}},
                         work_description='First update',
                         expected_version=initial_version)
    assert first_update.success, (
        f'Прво ажурирање са тачном верзијом није успело: '
        f'{first_update.error.message}')

    second_update = _save(OPTLOCK_EMAIL, 'Reliability Optlock',
                          daily_data={'1': {'rad_na_mestu': 2}},
                          work_description='Second update (stale)',
                          expected_version=initial_version)
    assert not second_update.success, \
        'Чување са застарелом верзијом је МОРАЛО да падне'
    assert second_update.error.error_type == tp.TimesheetErrorType.CONCURRENT_MODIFICATION, (
        f'Очекиван CONCURRENT_MODIFICATION, добијен '
        f'{second_update.error.error_type}')


def test_lock_enforcement():
    """Закључан извештај не сме да се мења (LOCKED грешка)."""
    initial = _save(LOCK_EMAIL, 'Reliability Lock',
                    daily_data={'1': {'rad_na_mestu': 8}},
                    work_description='To be locked')
    assert initial.success, f'Почетно чување није успело: {initial.error.message}'

    _lock_report(LOCK_EMAIL, CURRENT_MONTH, CURRENT_YEAR)

    update = _save(LOCK_EMAIL, 'Reliability Lock',
                   daily_data={'1': {'rad_na_mestu': 4}},
                   work_description='Trying to update locked')
    assert not update.success, 'Чување закључаног извештаја МОРА да падне'
    assert update.error.error_type == tp.TimesheetErrorType.LOCKED, (
        f'Очекиван LOCKED, добијен {update.error.error_type}')


def test_concurrent_saves():
    """6 паралелних чувања за 6 различитих корисника — сва морају успети."""
    def save_for(idx):
        try:
            result = _save(CONCURRENT_EMAILS[idx],
                           f'Reliability Concurrent {idx}',
                           daily_data={'1': {'rad_na_mestu': 8}},
                           work_description=f'Concurrent test {idx}')
            return (idx, result.success,
                    result.error.message if result.error else None)
        except Exception as e:  # noqa: BLE001 — исход се асертује
            return (idx, False, str(e))

    successes, failures = [], []
    with ThreadPoolExecutor(max_workers=CONCURRENT_SAVE_WORKERS) as executor:
        futures = [executor.submit(save_for, i)
                   for i in CONCURRENT_EMAILS]
        for future in as_completed(futures):
            idx, ok, error = future.result()
            (successes if ok else failures).append((idx, error))

    assert len(successes) == CONCURRENT_SAVE_REQUIRED_SUCCESSES, (
        f'Успело {len(successes)}/{CONCURRENT_SAVE_REQUIRED_SUCCESSES} '
        f'паралелних чувања. Падови: {failures}')


# =============================================================================
# EDGE CASE TESTS
# =============================================================================

def test_leap_year():
    """29. фебруар преступне 2024. се чува и учитава."""
    _seed_editable_report(LEAP_EMAIL, 'Reliability Leap', 2, 2024)
    daily_data = {str(d): {'rad_na_mestu': 8} for d in range(1, 30)}

    result = _save(LEAP_EMAIL, 'Reliability Leap', 2, 2024,
                   daily_data=daily_data, work_description='Leap year test')
    assert result.success, f'Чување фебруара 2024 није успело: {result.error.message}'

    loaded = tp.load_timesheet_from_postgres(LEAP_EMAIL, 2, 2024)
    assert loaded is not None, 'Учитавање фебруара 2024 вратило None'
    day29 = loaded['daily_data'].get(29, {}).get('rad_na_mestu', 0)
    assert abs(day29 - 8) <= HOURS_TOLERANCE, (
        f'Дан 29. фебруар: очекивано 8, добијено {day29}')


def test_31_day_month():
    """31. јануар се чува и учитава."""
    _seed_editable_report(MONTH31_EMAIL, 'Reliability Month31', 1, 2025)
    daily_data = {str(d): {'rad_na_mestu': 8} for d in range(1, 32)}

    result = _save(MONTH31_EMAIL, 'Reliability Month31', 1, 2025,
                   daily_data=daily_data, work_description='31 day test')
    assert result.success, f'Чување јануара није успело: {result.error.message}'

    loaded = tp.load_timesheet_from_postgres(MONTH31_EMAIL, 1, 2025)
    assert loaded is not None, 'Учитавање јануара вратило None'
    day31 = loaded['daily_data'].get(31, {}).get('rad_na_mestu', 0)
    assert abs(day31 - 8) <= HOURS_TOLERANCE, (
        f'Дан 31: очекивано 8, добијено {day31}')


def test_empty_timesheet():
    """Празна листа (све нуле) се чува и учитава као све-нула матрица."""
    daily_data = {str(d): {
        'rad_na_mestu': 0, 'van_muzeja': 0, 'godisnji_odmor': 0,
    } for d in range(1, 29)}

    result = _save(EMPTY_EMAIL, 'Reliability Empty',
                   daily_data=daily_data, work_description='Empty test')
    assert result.success, f'Чување празне листе није успело: {result.error.message}'

    loaded = tp.load_timesheet_from_postgres(
        EMPTY_EMAIL, CURRENT_MONTH, CURRENT_YEAR)
    assert loaded is not None, 'Учитавање празне листе вратило None'
    total = sum(hours
                for day_values in loaded['daily_data'].values()
                for hours in day_values.values())
    assert total == 0, f'Празна листа има ненулте сате: укупно {total}'


def test_special_characters_in_description():
    """Ћирилица, HTML и наводници у опису преживљавају save/load нетакнути."""
    special_desc = ("Тест са специјалним карактерима: "
                    "<script>alert('xss')</script> & \"quotes\" 'apostrophe'")

    result = _save(SPECIAL_EMAIL, 'Reliability Special',
                   daily_data={'1': {'rad_na_mestu': 8}},
                   work_description=special_desc)
    assert result.success, f'Чување није успело: {result.error.message}'

    loaded = tp.load_timesheet_from_postgres(
        SPECIAL_EMAIL, CURRENT_MONTH, CURRENT_YEAR)
    assert loaded is not None, 'Учитавање вратило None'
    assert loaded['OPosao'] == special_desc, (
        f'Опис искварен: очекивано {special_desc!r}, '
        f'добијено {loaded["OPosao"]!r}')


# =============================================================================
# SECURITY TESTS
# =============================================================================

def test_rate_limiting():
    """Лимит 3 захтева/24h: бројач, pending-дупликат и одбијање 4. захтева."""
    result = _save(RATE_LIMIT_EMAIL, 'Reliability RateLimit',
                   daily_data={'1': {'rad_na_mestu': 8}},
                   work_description='Rate limit test')
    assert result.success, f'Чување није успело: {result.error.message}'
    report_id = result.data['report_id']

    _lock_report(RATE_LIMIT_EMAIL, CURRENT_MONTH, CURRENT_YEAR)

    status = tp.get_edit_request_rate_limit_status(RATE_LIMIT_EMAIL)
    assert status['remaining'] == 3, (
        f'Почетни лимит: очекивано 3 преостала, добијено {status}')

    first = tp.request_edit_approval(
        RATE_LIMIT_EMAIL, CURRENT_MONTH, CURRENT_YEAR,
        'Test request 1 - need to fix data entry error')
    assert first.success, f'Први захтев одбијен: {first.error.message}'

    status = tp.get_edit_request_rate_limit_status(RATE_LIMIT_EMAIL)
    assert status['requests_today'] == 1, (
        f'После 1. захтева: очекиван бројач 1, добијено {status}')
    assert status['remaining'] == 2, (
        f'После 1. захтева: очекивано 2 преостала, добијено {status}')

    duplicate = tp.request_edit_approval(
        RATE_LIMIT_EMAIL, CURRENT_MONTH, CURRENT_YEAR,
        'Test request 2 - duplicate while pending exists')
    assert not duplicate.success, \
        'Дупли захтев уз постојећи pending МОРА да падне'
    assert duplicate.error.details.get('error_code') == 'ERR_PENDING_EXISTS', (
        f'Очекиван ERR_PENDING_EXISTS, добијено {duplicate.error.details}')

    # Допуни бројач до лимита (3) директним уписом одбијених захтева —
    # rate limit броји СВЕ захтеве у последња 24 часа без обзира на статус.
    with _db() as conn:
        with conn.cursor() as cur:
            for i in (2, 3):
                cur.execute(
                    "INSERT INTO timesheet_edit_requests "
                    "(report_id, requester_email, reason, status) "
                    "VALUES (%s, %s, %s, 'rejected')",
                    (report_id, RATE_LIMIT_EMAIL,
                     f'Synthetic rate-limit filler {i}'))
            conn.commit()

    status = tp.get_edit_request_rate_limit_status(RATE_LIMIT_EMAIL)
    assert status['requests_today'] == 3, (
        f'На лимиту: очекиван бројач 3, добијено {status}')
    assert status['remaining'] == 0 and status['is_limited'], (
        f'На лимиту: очекивано remaining=0/is_limited, добијено {status}')

    fourth = tp.request_edit_approval(
        RATE_LIMIT_EMAIL, CURRENT_MONTH, CURRENT_YEAR,
        'Test request 4 - must hit the rate limit')
    assert not fourth.success, '4. захтев преко лимита МОРА да падне'
    assert fourth.error.details.get('error_code') == 'ERR_RATE_LIMIT', (
        f'Очекиван ERR_RATE_LIMIT, добијено {fourth.error.details}')


# =============================================================================
# API TESTS
# =============================================================================

def test_error_guidance():
    """Error одговор носи комплетан guidance блок (LOCKED → bi-lock)."""
    result = tp.TimesheetResult.fail(
        tp.TimesheetErrorType.LOCKED,
        'Test locked error',
        {'error_code': 'TEST'})
    error_dict = result.error.to_dict()

    assert 'guidance' in error_dict, (
        f'Нема guidance у error dict: {sorted(error_dict.keys())}')
    guidance = error_dict['guidance']
    for field in ('title', 'icon', 'suggestions'):
        assert field in guidance, f'Guidance нема поље {field!r}: {guidance}'
    assert guidance['icon'] == 'bi-lock', (
        f'Очекиван bi-lock, добијено {guidance["icon"]}')
    assert isinstance(guidance['suggestions'], list) and guidance['suggestions'], (
        f'Suggestions празни или нису листа: {guidance["suggestions"]}')


def test_data_integrity_validation():
    """validate_loaded_data: чисти подаци без упозорења; негативни→error са
    корекцијом на 0; >24→warning; дневни збир >24→warning."""
    valid_data = {
        1: {'rad_na_mestu': 8, 'van_muzeja': 0},
        2: {'rad_na_mestu': 4, 'van_muzeja': 4},
    }
    warnings = tp.validate_loaded_data(valid_data, 1, 2025, 999)
    assert warnings == [], f'Валидни подаци добили упозорења: {warnings}'

    invalid_data = {1: {'rad_na_mestu': -5, 'van_muzeja': 0}}
    warnings = tp.validate_loaded_data(invalid_data, 1, 2025, 999)
    assert any(w['level'] == 'error' and 'Negative' in w['message']
               for w in warnings), (
        f'Очекиван error за негативне сате, добијено: {warnings}')
    assert invalid_data[1]['rad_na_mestu'] == 0, (
        f'Негативна вредност није коригована на 0: '
        f'{invalid_data[1]["rad_na_mestu"]}')

    excessive_data = {1: {'rad_na_mestu': 30, 'van_muzeja': 0}}
    warnings = tp.validate_loaded_data(excessive_data, 1, 2025, 999)
    assert any(w['level'] == 'warning' and '24' in w['message']
               for w in warnings), (
        f'Очекиван warning за >24 сата, добијено: {warnings}')

    total_excessive = {1: {'rad_na_mestu': 20, 'van_muzeja': 10}}
    warnings = tp.validate_loaded_data(total_excessive, 1, 2025, 999)
    assert any(w['message'] and 'Total daily hours' in w['message']
               for w in warnings), (
        f'Очекиван warning за дневни збир >24, добијено: {warnings}')


def test_batch_verification():
    """Групна верификација/деверификација: 3 извештаја кроз ANY(ids)."""
    for i, email in enumerate(BATCH_EMAILS, start=1):
        result = _save(email, f'Reliability Batch {i}',
                       daily_data={'1': {'rad_na_mestu': 8}},
                       work_description=f'Batch test {i}')
        assert result.success, (
            f'Чување извештаја {i} није успело: {result.error.message}')

    with _db() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT id FROM timesheet_reports "
                "WHERE employee_email = ANY(%s) AND month = %s AND year = %s "
                "ORDER BY id",
                (BATCH_EMAILS, CURRENT_MONTH, CURRENT_YEAR))
            report_ids = [row['id'] for row in cur.fetchall()]
    assert len(report_ids) == 3, (
        f'Очекивана 3 извештаја, нађено {len(report_ids)}')

    with _db() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                UPDATE timesheet_reports
                SET is_verified = TRUE,
                    verified_by = %s,
                    verified_at = NOW(),
                    is_locked = TRUE
                WHERE id = ANY(%s)
            """, (BATCH_ADMIN_EMAIL, report_ids))
            conn.commit()
            cur.execute(
                "SELECT COUNT(*) AS cnt FROM timesheet_reports "
                "WHERE id = ANY(%s) AND is_verified = TRUE", (report_ids,))
            verified_count = cur.fetchone()['cnt']
    assert verified_count == 3, (
        f'Групна верификација: очекивано 3, верификовано {verified_count}')

    with _db() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                UPDATE timesheet_reports
                SET is_verified = FALSE,
                    verified_by = NULL,
                    verified_at = NULL,
                    is_locked = FALSE
                WHERE id = ANY(%s)
            """, (report_ids,))
            conn.commit()
            cur.execute(
                "SELECT COUNT(*) AS cnt FROM timesheet_reports "
                "WHERE id = ANY(%s) AND is_verified = FALSE", (report_ids,))
            unverified_count = cur.fetchone()['cnt']
    assert unverified_count == 3, (
        f'Групна деверификација: очекивано 3, деверификовано {unverified_count}')


if __name__ == '__main__':
    sys.exit(pytest.main([__file__, '-q']))
