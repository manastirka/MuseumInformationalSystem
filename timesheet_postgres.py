#!/usr/bin/env python3
"""
Timesheet System - PostgreSQL Backend
Complete timesheet functionality integrated with main app authentication

Data Flow:
- Daily data is written to timesheet_report_days (one row per day)
- Database trigger automatically syncs aggregated totals to timesheet_entries
- This ensures data consistency between detailed and summary views
"""

import os
import logging
import calendar
import atexit
from dataclasses import dataclass
from datetime import datetime, date
from enum import Enum
from typing import Optional, Dict, List, Tuple, Union
from contextlib import contextmanager
import psycopg
from psycopg.rows import dict_row
try:
    from psycopg_pool import ConnectionPool
    POOL_AVAILABLE = True
except ImportError:
    POOL_AVAILABLE = False
    ConnectionPool = None
from serbian_holidays import SerbianHolidays

import odobravanje_prekidac

logger = logging.getLogger(__name__)

# Database URL from environment
DATABASE_URL = os.environ.get('DATABASE_URL', 'postgresql+psycopg://aleksandarlukovic@localhost:5432/museum_system')

# =============================================================================
# CONNECTION POOL
# =============================================================================

# Global connection pool (lazy initialized)
_connection_pool: Optional[ConnectionPool] = None


def _get_pg_url() -> str:
    """Convert SQLAlchemy-style URL to psycopg format"""
    return DATABASE_URL.replace('postgresql+psycopg://', 'postgresql://')


def get_connection_pool() -> Optional[ConnectionPool]:
    """Get or create the connection pool (lazy initialization)"""
    global _connection_pool
    if not POOL_AVAILABLE:
        return None
    if _connection_pool is None:
        pg_url = _get_pg_url()
        _connection_pool = ConnectionPool(
            conninfo=pg_url,
            min_size=2,      # Minimum connections to keep open
            max_size=10,     # Maximum connections allowed
            max_idle=300,    # Close idle connections after 5 minutes
            max_lifetime=3600,  # Recycle connections after 1 hour
            kwargs={'row_factory': dict_row}
        )
        logger.info("Timesheet connection pool initialized (min=2, max=10)")
    return _connection_pool


def close_connection_pool():
    """Close the connection pool (call on app shutdown)"""
    global _connection_pool
    if _connection_pool is not None:
        _connection_pool.close()
        _connection_pool = None
        logger.info("Timesheet connection pool closed")


# Register cleanup on interpreter exit
atexit.register(close_connection_pool)


@contextmanager
def get_pooled_connection():
    """Context manager for getting a connection from the pool"""
    pool = get_connection_pool()
    if pool is None:
        # Pool not available, use direct connection
        conn = psycopg.connect(_get_pg_url(), row_factory=dict_row)
        try:
            yield conn
        finally:
            conn.close()
    else:
        # Use pool's connection context manager
        with pool.connection() as conn:
            yield conn


# =============================================================================
# ERROR TYPES
# =============================================================================

class TimesheetErrorType(Enum):
    """Enumeration of possible error types for structured error handling"""
    NOT_FOUND = "not_found"
    VALIDATION_ERROR = "validation_error"
    CONCURRENT_MODIFICATION = "concurrent_modification"
    DATABASE_ERROR = "database_error"
    LOCKED = "locked"
    PERMISSION_DENIED = "permission_denied"


class TimesheetStatus(Enum):
    DRAFT = 'DRAFT'
    SUBMITTED = 'SUBMITTED'
    APPROVED = 'APPROVED'
    REJECTED = 'REJECTED'
    # Листа увезена из Word-архиве. НИЈЕ званично одобрен извештај — посебна
    # класификација да не улази у листу/статистику одобрених (види миграцију 035).
    ARHIVA = 'ARHIVA'


# Actionable guidance for each error type (defined early for use in TimesheetError)
_ERROR_GUIDANCE = {
    'not_found': {
        'title': 'Радна листа није пронађена',
        'icon': 'bi-search',
        'suggestions': [
            'Проверите да ли сте изабрали исправан месец и годину',
            'Ако је ово ваша прва радна листа за овај период, кликните "Сачувај" да је креирате',
            'Контактирајте администратора ако проблем и даље постоји'
        ]
    },
    'validation_error': {
        'title': 'Грешка у подацима',
        'icon': 'bi-exclamation-triangle',
        'suggestions': [
            'Проверите да ли су сви унесени сати исправни (0-24)',
            'Проверите да укупни дневни сати не прелазе разуман лимит',
            'Исправите означене грешке и покушајте поново'
        ]
    },
    'concurrent_modification': {
        'title': 'Подаци су измењени',
        'icon': 'bi-people',
        'suggestions': [
            'Неко други је управо изменио ову радну листу',
            'Кликните "Освежи" да учитате најновије податке',
            'Унесите своје измене поново након освежавања'
        ]
    },
    'database_error': {
        'title': 'Техничка грешка',
        'icon': 'bi-database-x',
        'suggestions': [
            'Ово је привремена техничка грешка',
            'Покушајте поново за неколико минута',
            'Ако проблем и даље постоји, контактирајте ИТ подршку'
        ]
    },
    'locked': {
        'title': 'Радна листа је закључана',
        'icon': 'bi-lock',
        'suggestions': [
            'Ова радна листа је верификована и закључана за измене',
            'Кликните "Захтевај измену" да пошаљете захтев администратору',
            'Наведите разлог за измену у захтеву'
        ]
    },
    'permission_denied': {
        'title': 'Немате дозволу',
        'icon': 'bi-shield-x',
        'suggestions': [
            'Немате дозволу за ову акцију',
            'Контактирајте свог руководиоца ако вам је потребан приступ',
            'Пријавите се са одговарајућим налогом'
        ]
    }
}

# Specific error code guidance
_ERROR_CODE_GUIDANCE = {
    'ERR_RATE_LIMIT': [
        'Достигли сте дневни лимит захтева за измене',
        'Лимит се ресетује у поноћ',
        'Ако имате хитну потребу, контактирајте администратора директно'
    ],
    'ERR_REASON_TOO_SHORT': [
        'Образложење мора имати најмање 10 карактера',
        'Опишите зашто је потребна измена (нпр. грешка у уносу, нови подаци)',
        'Детаљнији разлог убрзава одобравање захтева'
    ],
    'ERR_PENDING_EXISTS': [
        'Већ сте послали захтев за измену овог месеца',
        'Сачекајте одговор на постојећи захтев',
        'Можете контактирати администратора за статус захтева'
    ]
}


def _get_guidance_for_error(error_type_value: str, error_code: str = None) -> Dict:
    """Get guidance for an error type and optional error code."""
    base_guidance = _ERROR_GUIDANCE.get(error_type_value, {
        'title': 'Грешка',
        'icon': 'bi-exclamation-circle',
        'suggestions': ['Покушајте поново или контактирајте подршку']
    })

    specific_suggestions = _ERROR_CODE_GUIDANCE.get(error_code) if error_code else None

    return {
        **base_guidance,
        'suggestions': specific_suggestions or base_guidance['suggestions']
    }


@dataclass
class TimesheetError:
    """Structured error response with actionable guidance"""
    error_type: TimesheetErrorType
    message: str
    details: Optional[Dict] = None

    def to_dict(self) -> Dict:
        error_code = self.details.get('error_code') if self.details else None
        guidance = _get_guidance_for_error(self.error_type.value, error_code)

        result = {
            'error_type': self.error_type.value,
            'message': self.message,
            'guidance': guidance
        }
        if self.details:
            result['details'] = self.details
        return result


@dataclass
class TimesheetResult:
    """Result wrapper for timesheet operations"""
    success: bool
    data: Optional[Dict] = None
    error: Optional[TimesheetError] = None

    @classmethod
    def ok(cls, data: Dict = None) -> 'TimesheetResult':
        return cls(success=True, data=data or {})

    @classmethod
    def fail(cls, error_type: TimesheetErrorType, message: str, details: Dict = None) -> 'TimesheetResult':
        return cls(success=False, error=TimesheetError(error_type, message, details))


# =============================================================================
# VALIDATION
# =============================================================================

# Valid work categories
# Sick leave is accepted under both the canonical names and the frontend alias
# names (underscore before the number) that employee_timesheet.html actually
# submits; both are read by save_timesheet_to_postgres, so both must be
# range-checked here to keep validation and save consistent.
VALID_CATEGORIES = {
    'rad_na_mestu', 'van_muzeja', 'godisnji_odmor', 'drzavni_praznik',
    'placeno_odsustvo', 'ostalo_odsustvo', 'bolovanje_manje30', 'bolovanje_30_ili_vise',
    'bolovanje_manje_30', 'bolovanje_vece_30'
}

# Category mapping: frontend names -> database column names
FRONTEND_TO_DB_COLUMNS = {
    'rad_na_mestu': 'work_in_museum',
    'van_muzeja': 'work_outside',
    'godisnji_odmor': 'vacation',
    'drzavni_praznik': 'public_holiday',
    'placeno_odsustvo': 'paid_leave',
    'ostalo_odsustvo': 'other_leave',
    'bolovanje_manje30': 'sick_leave_lt30',
    'bolovanje_30_ili_vise': 'sick_leave_gte30'
}

# Reverse mapping: database column names -> frontend names
DB_COLUMNS_TO_FRONTEND = {v: k for k, v in FRONTEND_TO_DB_COLUMNS.items()}


def validate_hours(hours: float, field_name: str = "hours") -> Optional[str]:
    """Validate hours value. Returns error message or None if valid."""
    if hours < 0:
        return f"{field_name}: негативна вредност није дозвољена ({hours})"
    if hours > 24:
        return f"{field_name}: вредност не може бити већа од 24 ({hours})"
    return None


def validate_daily_data(daily_data: Dict, month: int, year: int) -> List[str]:
    """
    Validate daily timesheet data.
    Returns list of error messages (empty if valid).
    """
    errors = []
    days_in_month = calendar.monthrange(year, month)[1]

    for day_str, day_values in daily_data.items():
        try:
            day = int(day_str)
        except (ValueError, TypeError):
            errors.append(f"Неважећи дан: {day_str}")
            continue

        if day < 1 or day > days_in_month:
            errors.append(f"Дан {day} није валидан за месец {month}/{year}")
            continue

        if not isinstance(day_values, dict):
            errors.append(f"Дан {day}: подаци морају бити речник")
            continue

        total_hours = 0
        for category, hours in day_values.items():
            # Skip unknown categories silently (backward compatibility)
            if category not in VALID_CATEGORIES:
                continue

            try:
                hours_float = float(hours)
            except (ValueError, TypeError):
                errors.append(f"Дан {day}, {category}: неважећа вредност сати ({hours})")
                continue

            hour_error = validate_hours(hours_float, f"Дан {day}, {category}")
            if hour_error:
                errors.append(hour_error)
                continue

            total_hours += hours_float

        # Warn if total exceeds 24 (but allow it - could be multiple shifts)
        if total_hours > 24:
            logger.warning(f"Day {day}: total hours ({total_hours}) exceeds 24")

    return errors


def validate_month_year(month: int, year: int) -> Optional[str]:
    """Validate month and year values."""
    if not isinstance(month, int) or month < 1 or month > 12:
        return f"Неважећи месец: {month}"
    if not isinstance(year, int) or year < 2000 or year > 2100:
        return f"Неважећа година: {year}"
    return None


def validate_loaded_data(daily_data: Dict, month: int, year: int, report_id: int) -> List[Dict]:
    """
    Validate data integrity of loaded timesheet data.
    Returns list of warnings (empty if all valid).
    Each warning has: level (warning/error), day, category, message, value.

    This function does NOT prevent data from being returned - it only reports
    issues that might indicate data corruption or need attention.
    """
    warnings = []
    days_in_month = calendar.monthrange(year, month)[1]

    for day, day_values in daily_data.items():
        if not isinstance(day_values, dict):
            warnings.append({
                'level': 'error',
                'day': day,
                'category': None,
                'message': 'Invalid data format for day',
                'value': str(day_values)
            })
            continue

        total_hours = 0

        for category, hours in day_values.items():
            # Check for negative values (data corruption indicator)
            if hours < 0:
                warnings.append({
                    'level': 'error',
                    'day': day,
                    'category': category,
                    'message': 'Negative hours detected',
                    'value': hours
                })
                # Fix in place for display (don't propagate corrupted data)
                daily_data[day][category] = 0

            # Check for excessive hours
            elif hours > 24:
                warnings.append({
                    'level': 'warning',
                    'day': day,
                    'category': category,
                    'message': 'Hours exceed 24',
                    'value': hours
                })

            # Check for non-standard values (not multiples of 0.5)
            elif hours > 0 and (hours * 2) % 1 != 0:
                warnings.append({
                    'level': 'info',
                    'day': day,
                    'category': category,
                    'message': 'Non-standard hour value',
                    'value': hours
                })

            total_hours += hours if hours > 0 else 0

        # Check if total daily hours exceed reasonable limit
        if total_hours > 24:
            warnings.append({
                'level': 'warning',
                'day': day,
                'category': None,
                'message': f'Total daily hours ({total_hours:.1f}) exceed 24',
                'value': total_hours
            })

    # Log any errors for monitoring
    error_count = sum(1 for w in warnings if w['level'] == 'error')
    warning_count = sum(1 for w in warnings if w['level'] == 'warning')

    if error_count > 0:
        logger.error(f"Report {report_id}: {error_count} data integrity errors detected")
    if warning_count > 0:
        logger.warning(f"Report {report_id}: {warning_count} data warnings detected")

    return warnings


# =============================================================================
# DATABASE CONNECTION
# =============================================================================

def get_pg_connection():
    """
    Get PostgreSQL connection context manager.
    Uses connection pooling for better performance under load.
    Falls back to direct connection if pool is unavailable.

    Usage:
        with get_pg_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(...)
    """
    return get_pooled_connection()


# =============================================================================
# CALENDAR DATA
# =============================================================================

def get_calendar_data(month: int, year: int) -> List[Dict]:
    """Generate calendar data with weekend/holiday info"""
    serbian_holidays = SerbianHolidays()
    calendar_data = []

    days_in_month = calendar.monthrange(year, month)[1]

    for day in range(1, days_in_month + 1):
        day_date = date(year, month, day)
        weekday = day_date.weekday()  # 0=Monday, 6=Sunday

        holiday_name = serbian_holidays.is_holiday(day_date)
        day_info = {
            'day': day,
            'weekday': weekday,
            'is_weekend': weekday >= 5,  # Saturday=5, Sunday=6
            'is_holiday': holiday_name is not None,
            'holiday_name': holiday_name or '',
            'day_name': ['Пон', 'Уто', 'Сре', 'Чет', 'Пет', 'Суб', 'Нед'][weekday]
        }
        calendar_data.append(day_info)

    return calendar_data


# =============================================================================
# LOAD TIMESHEET
# =============================================================================

def load_timesheet_from_postgres(user_email: str, month: int, year: int) -> Optional[Dict]:
    """
    Load existing timesheet data from PostgreSQL.

    Returns dict with keys:
        - exists: True
        - radna_lista_id: report ID
        - ime_prezime: employee name
        - OPosao: work description
        - daily_data: dict of day -> category hours
        - is_verified: verification status
        - is_locked: lock status
        - version: current version for optimistic locking

    Returns None if not found or on error.
    """
    # Validate inputs
    validation_error = validate_month_year(month, year)
    if validation_error:
        logger.error(f"Validation error in load_timesheet: {validation_error}")
        return None

    try:
        with get_pg_connection() as conn:
            with conn.cursor() as cur:
                # Get report header - try email first, fallback to name
                cur.execute("""
                    SELECT
                        id,
                        employee_name,
                        employee_email,
                        organization_unit,
                        position,
                        special_tasks,
                        is_verified,
                        is_locked,
                        version,
                        created_at,
                        COALESCE(status, 'DRAFT') as status,
                        submitted_at,
                        rejection_note
                    FROM timesheet_reports
                    WHERE (employee_email = %s OR (employee_email IS NULL AND employee_name = %s))
                      AND month = %s
                      AND year = %s
                """, (user_email, user_email, month, year))

                report = cur.fetchone()

                if not report:
                    return None

                # Get daily data from timesheet_report_days (source of truth)
                cur.execute("""
                    SELECT
                        day,
                        work_in_museum,
                        work_outside,
                        vacation,
                        public_holiday,
                        paid_leave,
                        other_leave,
                        sick_leave_lt30,
                        sick_leave_gte30
                    FROM timesheet_report_days
                    WHERE report_id = %s
                    ORDER BY day
                """, (report['id'],))

                day_rows = cur.fetchall()

                # Initialize daily data structure
                days_in_month = calendar.monthrange(year, month)[1]
                daily_data = {}
                for day in range(1, days_in_month + 1):
                    daily_data[day] = {
                        'rad_na_mestu': 0,
                        'van_muzeja': 0,
                        'godisnji_odmor': 0,
                        'drzavni_praznik': 0,
                        'placeno_odsustvo': 0,
                        'ostalo_odsustvo': 0,
                        'bolovanje_manje30': 0,
                        'bolovanje_30_ili_vise': 0
                    }

                # Fill in actual data from database
                for row in day_rows:
                    day = row['day']
                    if day in daily_data:
                        daily_data[day]['rad_na_mestu'] = float(row['work_in_museum'] or 0)
                        daily_data[day]['van_muzeja'] = float(row['work_outside'] or 0)
                        daily_data[day]['godisnji_odmor'] = float(row['vacation'] or 0)
                        daily_data[day]['drzavni_praznik'] = float(row['public_holiday'] or 0)
                        daily_data[day]['placeno_odsustvo'] = float(row['paid_leave'] or 0)
                        daily_data[day]['ostalo_odsustvo'] = float(row['other_leave'] or 0)
                        daily_data[day]['bolovanje_manje30'] = float(row['sick_leave_lt30'] or 0)
                        daily_data[day]['bolovanje_30_ili_vise'] = float(row['sick_leave_gte30'] or 0)

                # Validate loaded data integrity
                data_warnings = validate_loaded_data(daily_data, month, year, report['id'])

                result = {
                    'exists': True,
                    'radna_lista_id': report['id'],
                    'ime_prezime': report['employee_name'],
                    'OPosao': report['special_tasks'] or '',
                    'daily_data': daily_data,
                    'is_verified': bool(report['is_verified']),
                    'is_locked': bool(report['is_locked']),
                    'version': report['version'] or 1,
                    'status': report['status'] or 'DRAFT',
                    'submitted_at': report['submitted_at'].isoformat() if report['submitted_at'] else None,
                    'rejection_note': report['rejection_note'] or ''
                }

                # Include warnings if any issues found
                if data_warnings:
                    result['data_warnings'] = data_warnings

                return result

    except psycopg.Error as e:
        logger.error(f"Database error loading timesheet: {e}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error loading timesheet: {e}")
        import traceback
        traceback.print_exc()
        return None


# =============================================================================
# SAVE TIMESHEET
# =============================================================================

def save_timesheet_to_postgres(
    user_email: str,
    user_name: str,
    month: int,
    year: int,
    daily_data: Dict,
    work_description: str,
    organization_unit: str,
    position: str,
    expected_version: Optional[int] = None
) -> TimesheetResult:
    """
    Save timesheet data to PostgreSQL.

    Uses optimistic locking: if expected_version is provided, the update will
    fail if the current version doesn't match (concurrent modification detected).

    Data is written to timesheet_report_days table. A database trigger
    automatically syncs aggregated totals to timesheet_entries.

    Args:
        user_email: Employee email
        user_name: Employee full name
        month: Month (1-12)
        year: Year
        daily_data: Dict of day -> {category: hours}
        work_description: Special tasks description
        organization_unit: Department/unit name
        position: Job position
        expected_version: If provided, used for optimistic locking

    Returns:
        TimesheetResult with success status and data or error
    """
    # Validate inputs
    validation_error = validate_month_year(month, year)
    if validation_error:
        return TimesheetResult.fail(
            TimesheetErrorType.VALIDATION_ERROR,
            validation_error
        )

    data_errors = validate_daily_data(daily_data, month, year)
    if data_errors:
        return TimesheetResult.fail(
            TimesheetErrorType.VALIDATION_ERROR,
            "Грешке у валидацији података",
            {'errors': data_errors}
        )

    try:
        with get_pg_connection() as conn:
            with conn.cursor() as cur:
                # Check if report exists and get current state
                cur.execute("""
                    SELECT id, version, is_locked, is_verified,
                           COALESCE(status, 'DRAFT') as status,
                           editable_until,
                           (editable_until IS NOT NULL AND NOW() >= editable_until) AS edit_window_expired
                    FROM timesheet_reports
                    WHERE (employee_email = %s OR (employee_email IS NULL AND employee_name = %s))
                      AND month = %s
                      AND year = %s
                    FOR UPDATE
                """, (user_email, user_name, month, year))

                existing = cur.fetchone()

                if existing:
                    report_id = existing['id']
                    current_version = existing['version'] or 1

                    # Check if locked
                    if existing['is_locked']:
                        return TimesheetResult.fail(
                            TimesheetErrorType.LOCKED,
                            "Радна листа је закључана. Потребно је одобрење администратора за измене."
                        )

                    # 24 h temporary-edit window enforced after reject / revoke.
                    # When editable_until has passed, auto-relock the report
                    # and force the user to request a new unlock from the head.
                    if existing.get('edit_window_expired'):
                        cur.execute("""
                            UPDATE timesheet_reports
                            SET is_locked = TRUE,
                                editable_until = NULL
                            WHERE id = %s
                        """, (report_id,))
                        conn.commit()
                        return TimesheetResult.fail(
                            TimesheetErrorType.LOCKED,
                            "Истекло је време за измене (24 часа). Морате затражити поновно "
                            "откључавање од шефа одељења."
                        )

                    # Предато или завршено се не мења. BEZ_ODOBRENJA је
                    # завршено стање исто колико и APPROVED — разлика је само
                    # у томе да ли је неко потписао.
                    if existing['status'] in odobravanje_prekidac.IZVESTAJ_NEIZMENJIV:
                        return TimesheetResult.fail(
                            TimesheetErrorType.LOCKED,
                            "Радна листа је поднета/одобрена и не може се мењати."
                        )

                    # Deadline (rule 1) — skipped while a 24 h post-reject
                    # window is active: that window overrides the deadline
                    # for this report only (rule 5).
                    window_active = (existing.get('editable_until') is not None
                                     and not existing.get('edit_window_expired'))
                    if not window_active:
                        can_edit, edit_message = can_edit_timesheet_by_status(
                            month, year, existing['status'])
                        if not can_edit:
                            return TimesheetResult.fail(
                                TimesheetErrorType.LOCKED,
                                edit_message
                            )

                    # Optimistic locking check
                    if expected_version is not None and expected_version != current_version:
                        return TimesheetResult.fail(
                            TimesheetErrorType.CONCURRENT_MODIFICATION,
                            "Подаци су измењени од стране другог корисника. Молимо освежите страницу.",
                            {
                                'expected_version': expected_version,
                                'current_version': current_version
                            }
                        )

                    # Update existing report (version is auto-incremented by trigger)
                    cur.execute("""
                        UPDATE timesheet_reports
                        SET employee_name = %s,
                            employee_email = %s,
                            special_tasks = %s,
                            organization_unit = %s,
                            position = %s
                        WHERE id = %s
                        RETURNING version
                    """, (user_name, user_email, work_description, organization_unit, position, report_id))

                    updated_row = cur.fetchone()
                    if updated_row is None:
                        return TimesheetResult.fail(
                            TimesheetErrorType.CONCURRENT_MODIFICATION,
                            "Извештај је у међувремену измењен или обрисан. "
                            "Освежите страницу и покушајте поново."
                        )
                    new_version = updated_row['version']

                    # Заштита од ТИХОГ брисања: ако долазна матрица нема ниједан
                    # унет сат, а листа већ садржи дане, скоро сигурно је реч о
                    # грешци (форма се отворила празна) — не бриши тихо, врати
                    # јасну грешку уместо да прикажеш „успешно сачувано".
                    def _positive(value):
                        try:
                            return float(value) > 0
                        except (TypeError, ValueError):
                            return False
                    incoming_has_data = any(
                        _positive(v)
                        for dv in (daily_data or {}).values()
                        if isinstance(dv, dict)
                        for v in dv.values()
                    )
                    if not incoming_has_data:
                        cur.execute(
                            "SELECT COUNT(*) AS n FROM timesheet_report_days "
                            "WHERE report_id = %s", (report_id,))
                        existing_days = cur.fetchone()['n']
                        if existing_days > 0:
                            return TimesheetResult.fail(
                                TimesheetErrorType.VALIDATION_ERROR,
                                "Форма нема унетих сати, а листа већ садржи "
                                "податке. Освежите страницу (Ctrl+F5) и покушајте "
                                "поново — чување празне форме би избрисало већ "
                                "унете дане."
                            )

                    # Delete old daily entries
                    cur.execute("""
                        DELETE FROM timesheet_report_days
                        WHERE report_id = %s
                    """, (report_id,))

                else:
                    # Deadline (rule 1): a new report has no edit window,
                    # so the date check always applies.
                    can_edit, edit_message = can_edit_timesheet_by_status(
                        month, year, 'DRAFT')
                    if not can_edit:
                        return TimesheetResult.fail(
                            TimesheetErrorType.LOCKED,
                            edit_message
                        )

                    # Create new report
                    cur.execute("""
                        INSERT INTO timesheet_reports (
                            employee_email,
                            employee_name,
                            month,
                            year,
                            organization_unit,
                            position,
                            special_tasks,
                            version
                        ) VALUES (%s, %s, %s, %s, %s, %s, %s, 1)
                        RETURNING id, version
                    """, (user_email, user_name, month, year, organization_unit, position, work_description))

                    result = cur.fetchone()
                    report_id = result['id']
                    new_version = result['version']

                # Insert daily entries into timesheet_report_days
                # The trigger will sync aggregated totals to timesheet_entries
                days_in_month = calendar.monthrange(year, month)[1]

                for day in range(1, days_in_month + 1):
                    day_str = str(day)
                    day_data = daily_data.get(day_str, daily_data.get(day, {}))

                    # Get hours for each category
                    work_in_museum = float(day_data.get('rad_na_mestu', 0))
                    work_outside = float(day_data.get('van_muzeja', 0))
                    vacation = float(day_data.get('godisnji_odmor', 0))
                    public_holiday = float(day_data.get('drzavni_praznik', 0))
                    paid_leave = float(day_data.get('placeno_odsustvo', 0))
                    other_leave = float(day_data.get('ostalo_odsustvo', 0))
                    # Support both old and new field names for sick leave
                    sick_lt30 = float(day_data.get('bolovanje_manje_30', day_data.get('bolovanje_manje30', 0)))
                    sick_gte30 = float(day_data.get('bolovanje_vece_30', day_data.get('bolovanje_30_ili_vise', 0)))

                    # Only insert if there's any data for this day
                    total = work_in_museum + work_outside + vacation + public_holiday + \
                            paid_leave + other_leave + sick_lt30 + sick_gte30

                    if total > 0:
                        cur.execute("""
                            INSERT INTO timesheet_report_days (
                                report_id,
                                day,
                                work_in_museum,
                                work_outside,
                                vacation,
                                public_holiday,
                                paid_leave,
                                other_leave,
                                sick_leave_lt30,
                                sick_leave_gte30
                            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                        """, (report_id, day, work_in_museum, work_outside, vacation,
                              public_holiday, paid_leave, other_leave, sick_lt30, sick_gte30))

                conn.commit()

                return TimesheetResult.ok({
                    'report_id': report_id,
                    'version': new_version,
                    'message': 'Радна листа је успешно сачувана'
                })

    except psycopg.Error as e:
        logger.error(f"Database error saving timesheet: {e}")
        return TimesheetResult.fail(
            TimesheetErrorType.DATABASE_ERROR,
            f"Грешка базе података: {str(e)}"
        )
    except Exception as e:
        logger.error(f"Unexpected error saving timesheet: {e}")
        import traceback
        traceback.print_exc()
        return TimesheetResult.fail(
            TimesheetErrorType.DATABASE_ERROR,
            f"Неочекивана грешка: {str(e)}"
        )


# =============================================================================
# LEGACY WRAPPER (backward compatibility)
# =============================================================================

def save_timesheet_to_postgres_legacy(
    user_email: str,
    user_name: str,
    month: int,
    year: int,
    daily_data: Dict,
    work_description: str,
    organization_unit: str,
    position: str
) -> Tuple[bool, Optional[str]]:
    """
    Legacy wrapper for save_timesheet_to_postgres.
    Returns (success, error_message) tuple for backward compatibility.
    """
    result = save_timesheet_to_postgres(
        user_email, user_name, month, year, daily_data,
        work_description, organization_unit, position
    )

    if result.success:
        return True, None
    else:
        return False, result.error.message if result.error else "Unknown error"


# =============================================================================
# USER INFO
# =============================================================================

def get_user_department_and_position(user_email: str) -> Tuple[str, str]:
    """Get user's department and position.

    Most users have `users.department_id` NULL and their real department lives
    in `employee_profiles.department`. COALESCE the two so we return the
    actual department (matches the login query in postgres_auth.py:78).
    """
    try:
        with get_pg_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT COALESCE(d.name, ep.department) AS department,
                           u.position
                      FROM users u
                      LEFT JOIN departments d ON u.department_id = d.id
                      LEFT JOIN employee_profiles ep ON LOWER(ep.email) = LOWER(u.email)
                     WHERE LOWER(u.email) = LOWER(%s)
                """, (user_email,))

                result = cur.fetchone()

                if result:
                    return (
                        result['department'] or 'Није дефинисано',
                        result['position'] or 'Није дефинисано'
                    )

    except Exception as e:
        logger.error(f"Error getting user department: {e}")

    return 'Није дефинисано', 'Није дефинисано'


# =============================================================================
# EDIT PERMISSIONS
# =============================================================================

def can_edit_timesheet(month: int, year: int) -> Tuple[bool, str, bool]:
    """
    Check if user can edit timesheet for given month/year.

    Returns: (can_edit, restriction_message, needs_approval)
    """
    current_date = datetime.now()
    current_month = current_date.month
    current_year = current_date.year

    is_current_month = (month == current_month and year == current_year)
    is_previous_month = (year < current_year) or (year == current_year and month < current_month)

    # Current month: Only 1st-7th allowed without approval
    if is_current_month:
        if current_date.day <= 7:
            return True, "", False
        else:
            return False, "Време за унос података је истекло (1-7. у месецу). Потребно је одобрење администратора за измене.", True

    # Previous months: Need approval
    elif is_previous_month:
        return False, "За мењање података из претходних месеци потребно је одобрење администратора.", True

    # Future months: Always allowed
    else:
        return True, "", False


def check_timesheet_lock_status(user_email: str, month: int, year: int) -> Tuple[bool, bool]:
    """
    Check if a timesheet is locked or verified.

    Returns: (is_locked, is_verified)
    """
    try:
        with get_pg_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT is_locked, is_verified,
                           (editable_until IS NOT NULL AND NOW() >= editable_until) AS edit_window_expired
                    FROM timesheet_reports
                    WHERE (employee_email = %s OR (employee_email IS NULL AND employee_name = %s))
                      AND month = %s
                      AND year = %s
                """, (user_email, user_email, month, year))

                result = cur.fetchone()
                if result:
                    # Relocking after window expiry is lazy (done on save), so
                    # an expired window must already read as locked here.
                    return (bool(result['is_locked']) or bool(result.get('edit_window_expired')),
                            bool(result['is_verified']))

    except Exception as e:
        # Fail-closed: пад провере не сме да се чита као „није закључано,
        # није оверено" — то би отворило упис у закључану листу (ревизија #5).
        logger.error(f"Error checking lock status: {e}")
        raise

    return False, False


# =============================================================================
# REQUEST EDIT APPROVAL
# =============================================================================

def request_edit_approval(user_email: str, month: int, year: int, reason: str) -> TimesheetResult:
    """
    Create an edit approval request for a locked/verified timesheet.

    Rate limited to 3 requests per user per 24 hours.

    Args:
        user_email: Requester's email
        month: Month of the timesheet
        year: Year of the timesheet
        reason: Reason for requesting edit permission

    Returns:
        TimesheetResult with request_id on success
    """
    # Constants for rate limiting
    MAX_REQUESTS_PER_DAY = 3
    RATE_LIMIT_HOURS = 24

    if not reason or len(reason.strip()) < 10:
        return TimesheetResult.fail(
            TimesheetErrorType.VALIDATION_ERROR,
            "Молимо наведите детаљнији разлог за измену (минимум 10 карактера)",
            {'error_code': 'ERR_REASON_TOO_SHORT', 'min_length': 10}
        )

    try:
        with get_pg_connection() as conn:
            with conn.cursor() as cur:
                # Rate limiting check - count requests in last 24 hours
                cur.execute("""
                    SELECT COUNT(*) as request_count
                    FROM timesheet_edit_requests
                    WHERE requester_email = %s
                      AND requested_at > NOW() - INTERVAL '%s hours'
                """, (user_email, RATE_LIMIT_HOURS))

                rate_check = cur.fetchone()
                if rate_check and rate_check['request_count'] >= MAX_REQUESTS_PER_DAY:
                    return TimesheetResult.fail(
                        TimesheetErrorType.VALIDATION_ERROR,
                        f"Достигнут дневни лимит захтева ({MAX_REQUESTS_PER_DAY}). Покушајте поново сутра.",
                        {
                            'error_code': 'ERR_RATE_LIMIT',
                            'max_requests': MAX_REQUESTS_PER_DAY,
                            'period_hours': RATE_LIMIT_HOURS,
                            'current_count': rate_check['request_count']
                        }
                    )

                # Get report ID
                cur.execute("""
                    SELECT id FROM timesheet_reports
                    WHERE (employee_email = %s OR (employee_email IS NULL AND employee_name = %s))
                      AND month = %s
                      AND year = %s
                """, (user_email, user_email, month, year))

                report = cur.fetchone()
                if not report:
                    return TimesheetResult.fail(
                        TimesheetErrorType.NOT_FOUND,
                        "Радна листа није пронађена",
                        {'error_code': 'ERR_REPORT_NOT_FOUND', 'month': month, 'year': year}
                    )

                # Check for existing pending request for this specific report
                cur.execute("""
                    SELECT id FROM timesheet_edit_requests
                    WHERE report_id = %s
                      AND requester_email = %s
                      AND status = 'pending'
                """, (report['id'], user_email))

                if cur.fetchone():
                    return TimesheetResult.fail(
                        TimesheetErrorType.VALIDATION_ERROR,
                        "Већ постоји захтев за измену на чекању за овај месец",
                        {'error_code': 'ERR_PENDING_EXISTS', 'report_id': report['id']}
                    )

                # Create request
                cur.execute("""
                    INSERT INTO timesheet_edit_requests
                    (report_id, requester_email, reason, status)
                    VALUES (%s, %s, %s, 'pending')
                    RETURNING id
                """, (report['id'], user_email, reason.strip()))

                request_id = cur.fetchone()['id']
                conn.commit()

                return TimesheetResult.ok({
                    'request_id': request_id,
                    'message': 'Захтев за измену је успешно послат'
                })

    except psycopg.Error as e:
        logger.error(f"Database error creating edit request: {e}")
        return TimesheetResult.fail(
            TimesheetErrorType.DATABASE_ERROR,
            f"Грешка базе података: {str(e)}",
            {'error_code': 'ERR_DATABASE'}
        )


def get_edit_request_rate_limit_status(user_email: str) -> Dict:
    """
    Check the rate limit status for edit requests.

    Args:
        user_email: User's email address

    Returns:
        Dict with rate limit info:
        - requests_today: Number of requests in last 24 hours
        - max_requests: Maximum allowed requests
        - remaining: Requests remaining
        - reset_at: When the oldest request expires (if at limit)
    """
    MAX_REQUESTS_PER_DAY = 3
    RATE_LIMIT_HOURS = 24

    try:
        with get_pg_connection() as conn:
            with conn.cursor() as cur:
                # Get count and oldest request time
                cur.execute("""
                    SELECT
                        COUNT(*) as request_count,
                        MIN(requested_at) as oldest_request
                    FROM timesheet_edit_requests
                    WHERE requester_email = %s
                      AND requested_at > NOW() - INTERVAL '%s hours'
                """, (user_email, RATE_LIMIT_HOURS))

                result = cur.fetchone()
                request_count = result['request_count'] if result else 0
                oldest_request = result['oldest_request'] if result else None

                remaining = max(0, MAX_REQUESTS_PER_DAY - request_count)

                # Calculate when rate limit resets
                reset_at = None
                if oldest_request and request_count >= MAX_REQUESTS_PER_DAY:
                    from datetime import timedelta
                    reset_at = oldest_request + timedelta(hours=RATE_LIMIT_HOURS)

                return {
                    'requests_today': request_count,
                    'max_requests': MAX_REQUESTS_PER_DAY,
                    'remaining': remaining,
                    'reset_at': reset_at.isoformat() if reset_at else None,
                    'is_limited': remaining == 0
                }

    except Exception as e:
        logger.error(f"Error checking rate limit: {e}")
        return {
            'requests_today': 0,
            'max_requests': MAX_REQUESTS_PER_DAY,
            'remaining': MAX_REQUESTS_PER_DAY,
            'reset_at': None,
            'is_limited': False,
            'error': str(e)
        }


# =============================================================================
# TIMESHEET STATUS WORKFLOW
# =============================================================================

def available_report_years(employee_email: Optional[str] = None) -> List[int]:
    """Списак година за бирач — ИЗВЕДЕН ИЗ ПОДАТАКА, не хардкодован опсег.

    Од MIN(година) која постоји у `timesheet_reports` (скопирано на запосленог
    ако је `employee_email` дат, иначе глобално за админа/шефа) до текуће године.
    Увек укључује бар претходну и текућу годину (унос подразумевано иде за
    претходни месец), па ради и на празној табели. Растуће сортирано.

    Овим архивски увоз (нпр. листе из 2011) одмах постаје доступан у бирачу,
    без ручног ширења опсега.
    """
    current = date.today().year
    data_min = data_max = None
    try:
        with get_pooled_connection() as conn:
            with conn.cursor() as cur:
                if employee_email:
                    cur.execute(
                        'SELECT MIN(year) AS mn, MAX(year) AS mx FROM timesheet_reports '
                        'WHERE LOWER(employee_email) = LOWER(%s)',
                        (employee_email,),
                    )
                else:
                    cur.execute('SELECT MIN(year) AS mn, MAX(year) AS mx FROM timesheet_reports')
                row = cur.fetchone()
                if row:
                    data_min = row['mn'] if isinstance(row, dict) else row[0]
                    data_max = row['mx'] if isinstance(row, dict) else row[1]
    except Exception:
        logger.exception('available_report_years: упит није успео, користим фолбек опсег')

    floor = current - 1  # унос за претходни месец увек мора да буде могућ
    start = min(data_min, floor) if data_min else floor
    end = max(current, data_max) if data_max else current
    return list(range(start, end + 1))


def default_entry_period() -> Tuple[int, int]:
    """Return the (month, year) an employee enters by default right now.

    Business rule: during the current month the report for the PREVIOUS month
    is filled (deadline the 10th — see can_submit_for_review). January rolls
    back to December of the previous year. The default is purely date-driven
    and never depends on existing rows, so it stays correct on an empty table.
    """
    today = datetime.now()
    if today.month == 1:
        return 12, today.year - 1
    return today.month - 1, today.year


def can_submit_for_review(month: int, year: int) -> Tuple[bool, str]:
    """
    Check if a report for the given month can currently be submitted for review.

    Allowed during the report month itself and on days 1-10 of the following
    month (December rolls over to January of the next year). Future months
    match neither window, so they are blocked automatically.

    Returns: (can_submit, message)
    """
    today = datetime.now()

    if today.year == year and today.month == month:
        return True, ""

    # Прекидач гаси РОК, не и здрав разум: извештај за месец који још није
    # почео остаје немогућ. То није ограничење него бесмислица — запослени
    # не може да пријави рад који се још није десио.
    if not odobravanje_prekidac.rok_predaje_ukljucen():
        if (year, month) < (today.year, today.month):
            return True, ""
        return False, (
            f"Радна листа за {month}/{year} се односи на месец који још "
            f"није почео."
        )

    if month == 12:
        submit_month, submit_year = 1, year + 1
    else:
        submit_month, submit_year = month + 1, year

    if today.year == submit_year and today.month == submit_month and 1 <= today.day <= 10:
        return True, ""

    return False, (
        f"Подношење радне листе за {month}/{year} је могуће само током тог "
        f"месеца или од 1. до 10. у месецу {submit_month}/{submit_year}."
    )


def can_edit_timesheet_by_status(month: int, year: int, status: str) -> Tuple[bool, str]:
    """
    Check if a timesheet can be edited based on its status and the current date.

    SUBMITTED/APPROVED are never editable. DRAFT/REJECTED are editable during
    the report month or days 1-10 of the following month. The 24h window after
    a reject (editable_until) is enforced at the save layer and overrides this
    deadline.

    Returns: (can_edit, message)
    """
    if status in odobravanje_prekidac.IZVESTAJ_NEIZMENJIV:
        return False, "Радна листа је поднета/одобрена и не може се мењати."

    # DRAFT or REJECTED: allow editing during the report month or days 1-10 of next month
    today = datetime.now()

    # Check if today is within the report month
    if today.year == year and today.month == month:
        return True, ""

    # Исти прекидач као при подношењу — иначе би нацрт могао да се поднесе,
    # а не и да се измени, што је недоследно и збуњује запосленог.
    if not odobravanje_prekidac.rok_predaje_ukljucen():
        if (year, month) < (today.year, today.month):
            return True, ""
        return False, (
            f"Радна листа за {month}/{year} се односи на месец који још "
            f"није почео."
        )

    # Check if today is within days 1-7 of the next month
    if month == 12:
        next_month = 1
        next_year = year + 1
    else:
        next_month = month + 1
        next_year = year

    if today.year == next_year and today.month == next_month and 1 <= today.day <= 10:
        return True, ""

    return False, (
        f"Време за измену радне листе за {month}/{year} је истекло. "
        f"Измене су могуће током месеца извештаја или од 1. до 10. наредног месеца."
    )


def submit_timesheet(report_id: int, user_email: str) -> TimesheetResult:
    """
    Submit a timesheet for review. Changes status from DRAFT/REJECTED to SUBMITTED.

    Args:
        report_id: ID of the timesheet report
        user_email: Email of the submitting user

    Returns:
        TimesheetResult with success status
    """
    try:
        with get_pg_connection() as conn:
            with conn.cursor() as cur:
                # Get current report state
                cur.execute("""
                    SELECT id, month, year, COALESCE(status, 'DRAFT') as status, employee_email,
                           editable_until,
                           (editable_until IS NOT NULL AND NOW() < editable_until) AS window_active
                    FROM timesheet_reports
                    WHERE id = %s
                    FOR UPDATE
                """, (report_id,))

                report = cur.fetchone()
                if not report:
                    return TimesheetResult.fail(
                        TimesheetErrorType.NOT_FOUND,
                        "Радна листа није пронађена"
                    )

                report_email = (report.get('employee_email') or '').strip().lower()
                submitter_email = (user_email or '').strip().lower()
                if not report_email or report_email != submitter_email:
                    return TimesheetResult.fail(
                        TimesheetErrorType.PERMISSION_DENIED,
                        "Можете поднети само своју радну листу"
                    )

                # Validate status
                if report['status'] not in ('DRAFT', 'REJECTED'):
                    return TimesheetResult.fail(
                        TimesheetErrorType.VALIDATION_ERROR,
                        f"Радна листа не може бити поднета из статуса '{report['status']}'. "
                        f"Само листе са статусом DRAFT или REJECTED могу бити поднете."
                    )

                # Validate submission window. An active 24 h post-reject
                # window overrides the deadline for this report (rule 5),
                # so a returned report can be resubmitted past the 10th.
                if not report.get('window_active'):
                    can_submit, message = can_submit_for_review(report['month'], report['year'])
                    if not can_submit:
                        return TimesheetResult.fail(
                            TimesheetErrorType.VALIDATION_ERROR,
                            message
                        )

                # Кад је одобравање ИСКЉУЧЕНО, слање завршава посао: нема
                # кога да чека. Статус је BEZ_ODOBRENJA, НЕ APPROVED — поља
                # потписа (is_verified, head_verified_*, director_verified_*)
                # остају празна и приказ то мора да каже. Извештај који нико
                # није потписао не сме да личи на потписан.
                trazi_potpis = odobravanje_prekidac.odobravanje_izvestaja_ukljuceno()
                novi_status = ('SUBMITTED' if trazi_potpis
                               else odobravanje_prekidac.STATUS_IZVESTAJ_BEZ)

                # Update status. Clear editable_until — the report is back
                # under review, the temp window from a prior reject/revoke
                # no longer applies.
                cur.execute("""
                    UPDATE timesheet_reports
                    SET status = %s,
                        is_locked = TRUE,
                        is_verified = FALSE,
                        submitted_at = NOW(),
                        editable_until = NULL
                    WHERE id = %s
                """, (novi_status, report_id))

                if not trazi_potpis:
                    beleska = ('Поднето док је одобравање искључено — '
                               'завршено без потписа шефа и директора')
                elif report['status'] == 'REJECTED':
                    beleska = 'Поновно поднето на преглед'
                else:
                    beleska = 'Поднето на преглед'

                # Log to status history
                cur.execute("""
                    INSERT INTO timesheet_status_history
                    (report_id, old_status, new_status, changed_by, note)
                    VALUES (%s, %s, %s, %s, %s)
                """, (report_id, report['status'], novi_status, user_email,
                      beleska))

                conn.commit()

                was_rejected = report['status'] == 'REJECTED'
                if not trazi_potpis:
                    poruka = ('Радна листа је завршена. Одобравање је '
                              'искључено, па потпис шефа и директора није '
                              'тражен — листа је означена као „Без одобравања".')
                elif was_rejected:
                    poruka = 'Радна листа је поново поднета на преглед'
                else:
                    poruka = 'Радна листа је успешно поднета на преглед'

                return TimesheetResult.ok({
                    'report_id': report_id,
                    'status': novi_status,
                    'was_rejected': was_rejected,
                    'trazen_potpis': trazi_potpis,
                    'message': poruka,
                })

    except psycopg.Error as e:
        logger.error(f"Database error submitting timesheet: {e}")
        return TimesheetResult.fail(
            TimesheetErrorType.DATABASE_ERROR,
            f"Грешка базе података: {str(e)}"
        )
    except Exception as e:
        logger.error(f"Unexpected error submitting timesheet: {e}")
        import traceback
        traceback.print_exc()
        return TimesheetResult.fail(
            TimesheetErrorType.DATABASE_ERROR,
            f"Неочекивана грешка: {str(e)}"
        )


def _approve_administratively(report_id: int, verifier_email: str) -> TimesheetResult:
    """Одобри ПОДНЕТУ листу АДМИНИСТРАТИВНО (ван редовног двостепеног ланца).

    Попуњава посебан траг ``admin_approved_by/at`` и ``verified_role``, а
    head/director слотови остају NULL — да административно одобрење никад не
    изгледа као два стварна потписа. Ради само из статуса SUBMITTED.
    """
    try:
        with get_pg_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT id, COALESCE(status, 'DRAFT') AS status
                    FROM timesheet_reports
                    WHERE id = %s
                    FOR UPDATE
                """, (report_id,))
                report = cur.fetchone()
                if not report:
                    return TimesheetResult.fail(
                        TimesheetErrorType.NOT_FOUND, "Радна листа није пронађена"
                    )
                if report['status'] != 'SUBMITTED':
                    return TimesheetResult.fail(
                        TimesheetErrorType.VALIDATION_ERROR,
                        f"Само поднете радне листе могу бити одобрене. "
                        f"Тренутни статус: '{report['status']}'"
                    )
                cur.execute("""
                    UPDATE timesheet_reports
                    SET status = 'APPROVED',
                        is_verified = TRUE,
                        is_locked = TRUE,
                        verified_by = %s,
                        verified_at = NOW(),
                        verified_role = 'administrativno',
                        admin_approved_by = %s,
                        admin_approved_at = NOW(),
                        reviewed_at = NOW(),
                        reviewed_by_email = %s,
                        editable_until = NULL
                    WHERE id = %s
                """, (verifier_email, verifier_email, verifier_email, report_id))
                cur.execute("""
                    INSERT INTO timesheet_status_history
                    (report_id, old_status, new_status, changed_by, note)
                    VALUES (%s, 'SUBMITTED', 'APPROVED', %s, %s)
                """, (report_id, verifier_email,
                      'ОДОБРЕНО АДМИНИСТРАТИВНО (ван двостепеног ланца)'))
                from audit_support import record_audit
                # Audit у ИСТОЈ трансакцији (cursor=): одобрење без трага се
                # не commit-uje; грешка се пропагира уместо тихог прогутања.
                record_audit(
                    action='approve_administrative', entity_type='timesheet_report',
                    entity_id=report_id, changed_by=verifier_email,
                    summary='Радна листа одобрена административно (ван двостепеног ланца)',
                    cursor=cur,
                )
                conn.commit()
        return TimesheetResult.ok({
            'report_id': report_id,
            'approved': True,
            'administrative': True,
            'status': 'APPROVED',
            'head_verified': False,
            'director_verified': False,
        })
    except psycopg.Error as e:
        logger.error(f"Database error in administrative approval: {e}")
        return TimesheetResult.fail(
            TimesheetErrorType.DATABASE_ERROR, "Грешка при административном одобравању."
        )


def confirm_timesheet_signature(report_id: int, verifier_email: str,
                                slot: str, head_required: bool,
                                administrative: bool = False) -> TimesheetResult:
    """Забележи потпис (шеф одељења и/или директор) на ПОДНЕТОЈ листи.

    Двостепено одобрење: листа постаје APPROVED тек кад су присутни СВИ потребни
    потписи — потпис директора је увек потребан, а потпис шефа само ако
    ``head_required`` (регуларан запослени у одељењу са шефом). До тада статус
    остаје SUBMITTED (делимично потврђено, закључано).

    ``slot`` бира који слот овај потпис попуњава:
      * 'head'     — потпис шефа одељења,
      * 'director' — потпис директора,
      * 'both'     — оба (иста особа = шеф И директор овог одељења).

    Кад је ``administrative`` True, листа се одобрава АДМИНИСТРАТИВНО (админ, или
    директор кад одељење/шеф није поуздано разрешен): status постаје APPROVED,
    али се НЕ попуњавају head/director слотови — уместо тога се бележи посебан
    траг ``admin_approved_by/at`` да одобрење никад не изгледа као два стварна
    потписа. ``slot``/``head_required`` се тада игноришу.

    Идемпотентно по слоту (поновни потпис истог слота само освежи ко/када).
    Ради само из статуса SUBMITTED.
    """
    if administrative:
        return _approve_administratively(report_id, verifier_email)
    if slot not in ('head', 'director', 'both'):
        return TimesheetResult.fail(
            TimesheetErrorType.VALIDATION_ERROR, f"Неисправан слот потписа: {slot}"
        )
    set_head = slot in ('head', 'both')
    set_dir = slot in ('director', 'both')
    try:
        with get_pg_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT id, COALESCE(status, 'DRAFT') AS status,
                           head_verified_at, director_verified_at
                    FROM timesheet_reports
                    WHERE id = %s
                    FOR UPDATE
                """, (report_id,))
                report = cur.fetchone()
                if not report:
                    return TimesheetResult.fail(
                        TimesheetErrorType.NOT_FOUND, "Радна листа није пронађена"
                    )
                if report['status'] != 'SUBMITTED':
                    return TimesheetResult.fail(
                        TimesheetErrorType.VALIDATION_ERROR,
                        f"Само поднете радне листе могу бити потврђене. "
                        f"Тренутни статус: '{report['status']}'"
                    )

                # Забележи потпис(е) за тражени слот.
                sets, params = [], []
                if set_head:
                    sets.append("head_verified_by = %s")
                    sets.append("head_verified_at = NOW()")
                    params.append(verifier_email)
                if set_dir:
                    sets.append("director_verified_by = %s")
                    sets.append("director_verified_at = NOW()")
                    params.append(verifier_email)
                params.append(report_id)
                cur.execute(
                    f"UPDATE timesheet_reports SET {', '.join(sets)} WHERE id = %s "
                    "RETURNING head_verified_at, director_verified_at, "
                    "head_verified_by, director_verified_by",
                    tuple(params),
                )
                row = cur.fetchone()
                head_done = row['head_verified_at'] is not None
                director_done = row['director_verified_at'] is not None
                approved = director_done and (head_done or not head_required)

                if approved:
                    cur.execute("""
                        UPDATE timesheet_reports
                        SET status = 'APPROVED',
                            is_verified = TRUE,
                            verified_by = %s,
                            verified_at = NOW(),
                            is_locked = TRUE,
                            reviewed_at = NOW(),
                            reviewed_by_email = %s,
                            editable_until = NULL
                        WHERE id = %s
                    """, (verifier_email, verifier_email, report_id))
                    cur.execute("""
                        INSERT INTO timesheet_status_history
                        (report_id, old_status, new_status, changed_by, note)
                        VALUES (%s, 'SUBMITTED', 'APPROVED', %s, %s)
                    """, (report_id, verifier_email,
                          'Одобрено (оба потписа присутна)'))
                else:
                    note = ('Потпис шефа одељења' if set_head and not set_dir
                            else 'Потпис директора' if set_dir and not set_head
                            else 'Потпис')
                    cur.execute("""
                        INSERT INTO timesheet_status_history
                        (report_id, old_status, new_status, changed_by, note)
                        VALUES (%s, 'SUBMITTED', 'SUBMITTED', %s, %s)
                    """, (report_id, verifier_email, note + ' — чека други потпис'))

                conn.commit()
                return TimesheetResult.ok({
                    'report_id': report_id,
                    'approved': approved,
                    'status': 'APPROVED' if approved else 'SUBMITTED',
                    'head_verified': head_done,
                    'director_verified': director_done,
                    'head_verified_by': row['head_verified_by'],
                    'director_verified_by': row['director_verified_by'],
                })
    except psycopg.Error as e:
        logger.error(f"Database error confirming signature: {e}")
        return TimesheetResult.fail(
            TimesheetErrorType.DATABASE_ERROR, "Грешка при потврђивању листе."
        )


def approve_timesheet(report_id: int, admin_email: str,
                      verifier_role: Optional[str] = None) -> TimesheetResult:
    """Одобри поднету листу ЈЕДНИМ потезом — АДМИНИСТРАТИВНО.

    Раније је ова функција постављала APPROVED без иједног потписа (мина: сваки
    позивалац је могао да заобиђе двостепени ланац). Сада делегира на
    административно одобравање: листа се јасно бележи као ОДОБРЕНА
    АДМИНИСТРАТИВНО (``admin_approved_by/at``, ``verified_role``), а не као
    редован двостепени ланац. Редовно одобравање иде искључиво кроз
    ``confirm_timesheet_signature`` (потпис по слоту).

    ``verifier_role`` се задржава ради компатибилности потписа, али
    административно одобрење увек носи улогу 'administrativno'.
    """
    return _approve_administratively(report_id, admin_email)


def reject_timesheet(report_id: int, admin_email: str, note: str) -> TimesheetResult:
    """
    Reject a submitted timesheet. Changes status from SUBMITTED to REJECTED.

    Args:
        report_id: ID of the timesheet report
        admin_email: Email of the rejecting admin
        note: Reason for rejection (required)

    Returns:
        TimesheetResult with success status
    """
    if not (note or '').strip():
        return TimesheetResult.fail(
            TimesheetErrorType.VALIDATION_ERROR,
            "Напомена са разлогом враћања је обавезна — запослени мора да зна шта да исправи."
        )

    try:
        with get_pg_connection() as conn:
            with conn.cursor() as cur:
                # Get current report state
                cur.execute("""
                    SELECT id, COALESCE(status, 'DRAFT') as status
                    FROM timesheet_reports
                    WHERE id = %s
                    FOR UPDATE
                """, (report_id,))

                report = cur.fetchone()
                if not report:
                    return TimesheetResult.fail(
                        TimesheetErrorType.NOT_FOUND,
                        "Радна листа није пронађена"
                    )

                # Validate status
                if report['status'] != 'SUBMITTED':
                    return TimesheetResult.fail(
                        TimesheetErrorType.VALIDATION_ERROR,
                        f"Само поднете радне листе могу бити одбијене. Тренутни статус: '{report['status']}'"
                    )

                # Update status. editable_until gives the employee a 24 h
                # window to correct and resubmit; after that the report
                # auto-locks for edits and an unlock request is required.
                cur.execute("""
                    UPDATE timesheet_reports
                    SET status = 'REJECTED',
                        is_locked = FALSE,
                        is_verified = FALSE,
                        rejection_note = %s,
                        reviewed_at = NOW(),
                        reviewed_by_email = %s,
                        head_verified_by = NULL,
                        head_verified_at = NULL,
                        director_verified_by = NULL,
                        director_verified_at = NULL,
                        editable_until = NOW() + INTERVAL '24 hours'
                    WHERE id = %s
                """, (note, admin_email, report_id))

                # Log to status history
                cur.execute("""
                    INSERT INTO timesheet_status_history
                    (report_id, old_status, new_status, changed_by, note)
                    VALUES (%s, 'SUBMITTED', 'REJECTED', %s, %s)
                """, (report_id, admin_email, note))

                conn.commit()

                return TimesheetResult.ok({
                    'report_id': report_id,
                    'status': 'REJECTED',
                    'message': 'Радна листа је одбијена. Запослени може да допуни извештај у наредна 24 часа.'
                })

    except psycopg.Error as e:
        logger.error(f"Database error rejecting timesheet: {e}")
        return TimesheetResult.fail(
            TimesheetErrorType.DATABASE_ERROR,
            f"Грешка базе података: {str(e)}"
        )
    except Exception as e:
        logger.error(f"Unexpected error rejecting timesheet: {e}")
        import traceback
        traceback.print_exc()
        return TimesheetResult.fail(
            TimesheetErrorType.DATABASE_ERROR,
            f"Неочекивана грешка: {str(e)}"
        )


def force_edit_timesheet(report_id: int, admin_email: str,
                         *, allow_approved_reopen: bool = True) -> TimesheetResult:
    """
    Force a timesheet back to DRAFT status. Any status -> DRAFT.
    Allowed for admin, director, and department heads (per-report scope
    is enforced by the route decorator + helper in timesheet_admin_views).

    Bounces the report back with a 24-hour temporary edit window so the
    employee can correct and resubmit without needing an unlock request.

    ``allow_approved_reopen``: закључавање TOCTOU трке (ревизија #2). Статус
    се чита ПОД истим ``FOR UPDATE`` локом под којим се и мења, па ако
    директор одобри листу између провере у рути и овог позива, поновна
    провера овде то види. Кад је позивалац шеф одељења (нема право да отвара
    ОВЕРЕНУ листу), проследи ``False`` — оверена листа се тада одбија уместо
    да се тихо спусти на DRAFT. Админ/директор шаљу ``True``.

    Args:
        report_id: ID of the timesheet report
        admin_email: Email of the admin/director/dept head performing the action

    Returns:
        TimesheetResult with success status
    """
    try:
        with get_pg_connection() as conn:
            with conn.cursor() as cur:
                # Get current report state
                cur.execute("""
                    SELECT id, COALESCE(status, 'DRAFT') as status
                    FROM timesheet_reports
                    WHERE id = %s
                    FOR UPDATE
                """, (report_id,))

                report = cur.fetchone()
                if not report:
                    return TimesheetResult.fail(
                        TimesheetErrorType.NOT_FOUND,
                        "Радна листа није пронађена"
                    )

                old_status = report['status']

                # Re-авторизација ПОД локом: оверену листу сме да отвори само
                # админ/директор. Ово затвара трку — статус је прочитан истом
                # трансакцијом која ради UPDATE, па директорово одобрење у
                # међувремену не може да пропусти шефов захтев.
                if (old_status in odobravanje_prekidac.IZVESTAJ_ZAVRSEN
                        and not allow_approved_reopen):
                    return TimesheetResult.fail(
                        TimesheetErrorType.PERMISSION_DENIED,
                        "Оверен извештај може да врати само администратор или "
                        "директор — поднесите захтев за откључавање."
                    )

                # Update status to DRAFT, open the 24 h edit window.
                cur.execute("""
                    UPDATE timesheet_reports
                    SET status = 'DRAFT',
                        is_locked = FALSE,
                        is_verified = FALSE,
                        verified_by = NULL,
                        verified_at = NULL,
                        verified_role = NULL,
                        head_verified_by = NULL,
                        head_verified_at = NULL,
                        director_verified_by = NULL,
                        director_verified_at = NULL,
                        editable_until = NOW() + INTERVAL '24 hours'
                    WHERE id = %s
                """, (report_id,))

                # Log to status history
                cur.execute("""
                    INSERT INTO timesheet_status_history
                    (report_id, old_status, new_status, changed_by, note)
                    VALUES (%s, %s, 'DRAFT', %s, 'Враћено запосленом на измену')
                """, (report_id, old_status, admin_email))

                conn.commit()

                return TimesheetResult.ok({
                    'report_id': report_id,
                    'status': 'DRAFT',
                    'old_status': old_status,
                    'message': 'Радна листа је враћена запосленом на измену (24 часа).'
                })

    except psycopg.Error as e:
        logger.error(f"Database error force-editing timesheet: {e}")
        return TimesheetResult.fail(
            TimesheetErrorType.DATABASE_ERROR,
            f"Грешка базе података: {str(e)}"
        )
    except Exception as e:
        logger.error(f"Unexpected error force-editing timesheet: {e}")
        import traceback
        traceback.print_exc()
        return TimesheetResult.fail(
            TimesheetErrorType.DATABASE_ERROR,
            f"Неочекивана грешка: {str(e)}"
        )


def get_pending_review_timesheets() -> List[Dict]:
    """
    Get all timesheets with SUBMITTED status pending admin review.

    Returns:
        List of dicts with employee_name, employee_email, month, year,
        organization_unit, submitted_at
    """
    try:
        with get_pg_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT
                        id,
                        employee_name,
                        employee_email,
                        month,
                        year,
                        organization_unit,
                        submitted_at
                    FROM timesheet_reports
                    WHERE COALESCE(status, 'DRAFT') = 'SUBMITTED'
                    ORDER BY submitted_at ASC
                """)

                rows = cur.fetchall()
                return [dict(row) for row in rows]

    except psycopg.Error as e:
        logger.error(f"Database error getting pending timesheets: {e}")
        return []
    except Exception as e:
        logger.error(f"Unexpected error getting pending timesheets: {e}")
        return []


def ensure_draft_exists(
    user_email: str,
    user_name: str,
    month: int,
    year: int,
    org_unit: str,
    position: str
) -> Optional[int]:
    """
    Ensure a draft timesheet report exists for the given user/month/year.
    If one already exists, return its id. Otherwise create a new one.

    Args:
        user_email: Employee email
        user_name: Employee full name
        month: Month (1-12)
        year: Year
        org_unit: Organization unit / department
        position: Job position

    Returns:
        report_id (int) or None on error
    """
    try:
        with get_pg_connection() as conn:
            with conn.cursor() as cur:
                # Check if report already exists
                cur.execute("""
                    SELECT id
                    FROM timesheet_reports
                    WHERE (employee_email = %s OR (employee_email IS NULL AND employee_name = %s))
                      AND month = %s
                      AND year = %s
                """, (user_email, user_name, month, year))

                existing = cur.fetchone()
                if existing:
                    return existing['id']

                # Create new draft report
                cur.execute("""
                    INSERT INTO timesheet_reports (
                        employee_email,
                        employee_name,
                        month,
                        year,
                        organization_unit,
                        position,
                        status,
                        is_locked,
                        is_verified,
                        version
                    ) VALUES (%s, %s, %s, %s, %s, %s, 'DRAFT', FALSE, FALSE, 1)
                    RETURNING id
                """, (user_email, user_name, month, year, org_unit, position))

                new_id = cur.fetchone()['id']
                conn.commit()

                return new_id

    except psycopg.Error as e:
        logger.error(f"Database error ensuring draft exists: {e}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error ensuring draft exists: {e}")
        return None


def admin_unlock_entry(employee_email: str, month: int, year: int,
                       admin_email: str, expires_at=None) -> TimesheetResult:
    """Админ/директор откључава УНОС радне листе конкретном запосленом за
    дати месец, кад је прошао редовни рок (унос само за претходни месец).

    Намерно поново користи ``editable_until`` — исти механизам као 24 h прозор
    после враћања: save_timesheet/submit_timesheet и приказ уноса већ поштују
    ``window_active`` и премошћују календарски рок за тај извештај. Тако
    откључавање ради кроз СВА три слоја без нове гранања логике, и само
    ИСТИЧЕ (нема потребе за посебном „затвори" акцијом).

    ``expires_at`` (datetime/ISO) → до када важи; None → подразумевано 7 дана.
    Не дира SUBMITTED/APPROVED листе (оне су већ у току одобравања).
    """
    if not employee_email:
        return TimesheetResult.fail(
            TimesheetErrorType.VALIDATION_ERROR, "Недостаје запослени."
        )
    try:
        with get_pg_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT full_name FROM users WHERE LOWER(email) = LOWER(%s)",
                    (employee_email,),
                )
                urow = cur.fetchone()
                if not urow:
                    return TimesheetResult.fail(
                        TimesheetErrorType.NOT_FOUND,
                        f"Запослени '{employee_email}' није пронађен."
                    )
                employee_name = urow['full_name']

        department, position = get_user_department_and_position(employee_email)
        report_id = ensure_draft_exists(
            employee_email, employee_name or '', month, year,
            department, position,
        )
        if not report_id:
            return TimesheetResult.fail(
                TimesheetErrorType.DATABASE_ERROR,
                "Није могуће припремити листу за откључавање."
            )

        with get_pg_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT COALESCE(status, 'DRAFT') AS status FROM timesheet_reports "
                    "WHERE id = %s FOR UPDATE",
                    (report_id,),
                )
                status = cur.fetchone()['status']
                if status in odobravanje_prekidac.IZVESTAJ_NEIZMENJIV:
                    return TimesheetResult.fail(
                        TimesheetErrorType.VALIDATION_ERROR,
                        f"Листа за {month}/{year} је већ у току одобравања "
                        f"(статус {status}) — откључавање уноса се не примењује."
                    )

                if expires_at is not None:
                    cur.execute(
                        "UPDATE timesheet_reports "
                        "SET editable_until = %s, is_locked = FALSE "
                        "WHERE id = %s RETURNING editable_until",
                        (expires_at, report_id),
                    )
                else:
                    cur.execute(
                        "UPDATE timesheet_reports "
                        "SET editable_until = NOW() + INTERVAL '7 days', is_locked = FALSE "
                        "WHERE id = %s RETURNING editable_until",
                        (report_id,),
                    )
                editable_until = cur.fetchone()['editable_until']

                cur.execute("""
                    INSERT INTO timesheet_status_history
                    (report_id, old_status, new_status, changed_by, note)
                    VALUES (%s, %s, %s, %s, %s)
                """, (report_id, status, status, admin_email,
                      f'Админ откључао унос до {editable_until}'))

                conn.commit()

        return TimesheetResult.ok({
            'report_id': report_id,
            'employee_email': employee_email,
            'employee_name': employee_name,
            'month': month,
            'year': year,
            'status': status,
            'editable_until': editable_until,
        })

    except psycopg.Error as e:
        logger.error(f"Database error unlocking entry: {e}")
        return TimesheetResult.fail(
            TimesheetErrorType.DATABASE_ERROR, "Грешка при откључавању уноса."
        )
