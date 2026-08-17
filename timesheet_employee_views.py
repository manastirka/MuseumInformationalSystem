"""Shared route implementations for employee timesheet workflows."""

import calendar
import logging
from datetime import date, datetime

from flask import jsonify, make_response, render_template, request, session
from psycopg.rows import dict_row

from postgres_service import get_postgres_connection
from serbian_holidays import SerbianHolidays

import odobravanje_prekidac

logger = logging.getLogger(__name__)

MONTH_NAMES = [
    "",
    "Јануар",
    "Фебруар",
    "Март",
    "Април",
    "Мај",
    "Јун",
    "Јул",
    "Август",
    "Септембар",
    "Октобар",
    "Новембар",
    "Децембар",
]
MONTH_NAMES_LOWER = [
    "",
    "јануар",
    "фебруар",
    "март",
    "април",
    "мај",
    "јун",
    "јул",
    "август",
    "септембар",
    "октобар",
    "новембар",
    "децембар",
]
DAY_NAMES = ['Пон', 'Уто', 'Сре', 'Чет', 'Пет', 'Суб', 'Нед']


def _month_choices():
    return [(idx, name) for idx, name in enumerate(MONTH_NAMES) if idx > 0]


def _year_choices():
    """Године за бирач се ИЗВОДЕ ИЗ ПОДАТАКА запосленог (од најстарије листе коју
    има до текуће), а не из хардкодованог опсега — тако архивски увоз старих
    година одмах постаје доступан."""
    from timesheet_postgres import available_report_years
    return available_report_years(session.get('user_email'))


def _no_cache_response(response):
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response


def _build_calendar_data(year, month):
    serbian_holidays = SerbianHolidays()
    calendar_data = []
    days_in_month = calendar.monthrange(year, month)[1]

    for day in range(1, days_in_month + 1):
        day_date = date(year, month, day)
        weekday = day_date.weekday()
        holiday_name = serbian_holidays.is_holiday(day_date)
        calendar_data.append(
            {
                'day': day,
                'weekday': weekday,
                'is_weekend': weekday >= 5,
                'is_holiday': holiday_name is not None,
                'holiday_name': holiday_name or '',
                'day_name': DAY_NAMES[weekday],
            }
        )

    return calendar_data


def _default_entry_period():
    # Delegates to the single source of truth in timesheet_postgres so the
    # entry default and the day-10 deadline rules can never drift apart.
    from timesheet_postgres import default_entry_period
    return default_entry_period()


def _load_report_header(employee_name, month, year, header_fields,
                        employee_email=None):
    # Email је примарни кључ: два истоимена запослена не смеју да виде туђе
    # податке. Тек ако email није познат или ред нема email, пада се на име
    # (уз толеранцију само за размак/величину слова — никад substring match,
    # који би могао вратити ДРУГОГ запосленог чије име само садржи ово).
    email_query = (
        f"SELECT {header_fields} FROM timesheet_reports "
        "WHERE LOWER(employee_email) = LOWER(%s) AND month = %s AND year = %s "
        "ORDER BY id DESC LIMIT 1"
    )
    name_query = (
        f"SELECT {header_fields} FROM timesheet_reports "
        "WHERE employee_email IS NULL AND employee_name = %s "
        "AND month = %s AND year = %s "
        "ORDER BY id DESC LIMIT 1"
    )
    name_fallback_query = (
        f"SELECT {header_fields} FROM timesheet_reports "
        "WHERE employee_email IS NULL "
        "AND LOWER(TRIM(employee_name)) = LOWER(TRIM(%s)) "
        "AND month = %s AND year = %s "
        "ORDER BY id DESC LIMIT 1"
    )

    with get_postgres_connection(row_factory=dict_row) as conn:
        with conn.cursor() as cur:
            if employee_email:
                cur.execute(email_query, (employee_email, month, year))
                header = cur.fetchone()
                if header:
                    return header
            cur.execute(name_query, (employee_name, month, year))
            header = cur.fetchone()
            if not header:
                cur.execute(name_fallback_query, (employee_name, month, year))
                header = cur.fetchone()
            return header


def _load_daily_rows(report_id):
    with get_postgres_connection(row_factory=dict_row) as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT day, work_in_museum, work_outside, vacation, public_holiday,
                       paid_leave, other_leave, sick_leave_lt30, sick_leave_gte30
                FROM timesheet_report_days
                WHERE report_id = %s
                ORDER BY day
                """,
                (report_id,),
            )
            return cur.fetchall()


def _format_daily_rows(daily_rows):
    formatted_rows = []
    for row in daily_rows:
        formatted_rows.append(
            {
                'dan': row['day'],
                'rad_na_mestu': row['work_in_museum'],
                'van_muzeja': row['work_outside'],
                'godisnji_odmor': row['vacation'],
                'drzavni_praznik': row['public_holiday'],
                'placeno_odsustvo': row['paid_leave'],
                'ostalo_odsustvo': row['other_leave'],
                'bolovanje_manje_30': row['sick_leave_lt30'],
                'bolovanje_vece_30': row['sick_leave_gte30'],
            }
        )
    return formatted_rows


def _load_latest_edit_request(report_id, requester_email):
    with get_postgres_connection(row_factory=dict_row) as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT id, status FROM timesheet_edit_requests
                WHERE report_id = %s AND requester_email = %s
                ORDER BY requested_at DESC LIMIT 1
                """,
                (report_id, requester_email),
            )
            return cur.fetchone()


def _load_timesheet_entry_data(user_full_name, user_email, month, year):
    header_fields = (
        "id, employee_name, special_tasks, extraordinary_tasks, duties_summary, "
        "is_verified, is_locked, verified_by, verified_at, version, status, "
        "submitted_at, rejection_note, "
        "head_verified_by, head_verified_at, director_verified_by, director_verified_at, "
        "(editable_until IS NOT NULL AND NOW() < editable_until) AS edit_window_active"
    )
    header = _load_report_header(user_full_name, month, year, header_fields,
                                 employee_email=user_email)
    if not header:
        return None

    daily_data = _format_daily_rows(_load_daily_rows(header['id']))
    edit_request = _load_latest_edit_request(header['id'], user_email)

    return {
        'exists': True,
        'daily_data': daily_data,
        'OPosao': (
            header.get('special_tasks')
            or header.get('extraordinary_tasks')
            or header.get('duties_summary')
            or ''
        ),
        'is_verified': header.get('is_verified', False),
        'is_locked': header.get('is_locked', False),
        'verified_by': header.get('verified_by'),
        'verified_at': header.get('verified_at'),
        'version': header.get('version', 1),
        'has_pending_request': bool(edit_request and edit_request['status'] == 'pending'),
        'has_approved_request': bool(edit_request and edit_request['status'] == 'approved'),
        'status': header.get('status', 'DRAFT'),
        'submitted_at': header.get('submitted_at'),
        'rejection_note': header.get('rejection_note', ''),
        'head_verified_by': header.get('head_verified_by'),
        'head_verified_at': header.get('head_verified_at'),
        'director_verified_by': header.get('director_verified_by'),
        'director_verified_at': header.get('director_verified_at'),
        'edit_window_active': bool(header.get('edit_window_active')),
        'report_id': header['id'],
    }


def _load_returned_reports(user_email, user_full_name):
    """Све листе овог власника у статусу REJECTED (враћено на допуну), од
    најновије. Служи за истакнуту навигацију ка враћеним листама из старијих
    месеци — да запослени не остане заглављен на подразумеваном месецу."""
    query = (
        "SELECT id, month, year, rejection_note, "
        "(editable_until IS NOT NULL AND NOW() < editable_until) AS edit_window_active "
        "FROM timesheet_reports "
        "WHERE COALESCE(status, 'DRAFT') = 'REJECTED' "
        "  AND (employee_email = %s "
        "       OR (employee_email IS NULL "
        "           AND LOWER(TRIM(employee_name)) = LOWER(TRIM(%s)))) "
        "ORDER BY year DESC, month DESC"
    )
    with get_postgres_connection(row_factory=dict_row) as conn:
        with conn.cursor() as cur:
            cur.execute(query, (user_email or '', user_full_name or ''))
            return cur.fetchall() or []


def _load_timesheet_view_data(user_full_name, month, year, user_email=None):
    header_fields = (
        "id, employee_name, special_tasks, extraordinary_tasks, duties_summary, "
        "is_verified, is_locked, verified_by, verified_at, version"
    )
    header = _load_report_header(user_full_name, month, year, header_fields,
                                 employee_email=user_email)
    if not header:
        return None

    daily_data = _format_daily_rows(_load_daily_rows(header['id']))
    return {
        'exists': True,
        'OPosao': (
            header.get('special_tasks')
            or header.get('extraordinary_tasks')
            or header.get('duties_summary')
            or ''
        ),
        'daily_data': daily_data,
        'is_verified': header.get('is_verified', False),
        'is_locked': header.get('is_locked', False),
        'verified_by': header.get('verified_by'),
        'verified_at': header.get('verified_at'),
        'version': header.get('version', 1),
    }


def _resolve_employee_profile(user_email, user_full_name, user_department='', user_position=''):
    resolved_department = user_department or ''
    resolved_position = user_position or ''

    try:
        with get_postgres_connection(row_factory=dict_row) as conn:
            with conn.cursor() as cur:
                if user_email:
                    cur.execute(
                        "SELECT department, position FROM employee_profiles WHERE email = %s",
                        (user_email,),
                    )
                    employee = cur.fetchone()
                    if employee:
                        resolved_department = resolved_department or employee.get('department', '')
                        resolved_position = resolved_position or employee.get('position', '')

                if (not resolved_department or not resolved_position) and user_full_name:
                    cur.execute(
                        """
                        SELECT u.position, d.name as department
                        FROM users u
                        LEFT JOIN departments d ON u.department_id = d.id
                        WHERE u.full_name = %s LIMIT 1
                        """,
                        (user_full_name,),
                    )
                    user_info = cur.fetchone()
                    if user_info:
                        resolved_department = resolved_department or user_info.get('department', '')
                        resolved_position = resolved_position or user_info.get('position', '')
    except Exception as exc:
        logger.warning("Could not load user department/position: %s", exc)

    return resolved_department, resolved_position


def _notify_verifiers_about_submission(
    user_name,
    submitter_email,
    submitter_department,
    is_resubmission: bool = False,
):
    """Notify every leadership user who can SIGN this report (two-signature).

    Rule (reuses `can_user_sign_report_for_department` so policy lives in one
    place):
    - Admin: always.
    - Department head: only their own department (not the submitter themselves).
    - Director: сваки регуларан запослени (директорски потпис) + листе шефова +
      одељења без шефа. (Раније је директор био изостављен за регуларне
      запослене одељења са шефом — па није ни знао да треба да потпише.)

    The submitter is always excluded.
    """
    try:
        # Local import avoids a module-level circular dependency and keeps
        # this helper self-contained.
        from timesheet_admin_views import (
            _get_department_heads,
            can_user_sign_report_for_department,
        )
        with get_postgres_connection(row_factory=dict_row) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT DISTINCT u.email, r.name AS role,
                           COALESCE(d.name, ep.department) AS department
                      FROM users u
                      JOIN roles r ON u.role_id = r.id
                      LEFT JOIN departments d ON u.department_id = d.id
                      LEFT JOIN employee_profiles ep ON LOWER(ep.email) = LOWER(u.email)
                     WHERE u.is_active = TRUE
                       AND r.name IN (
                           'admin',
                           'direktor',
                           'sef_odeljenja',
                           'sef_pravne_sluzbe',
                           'sef_racunovodstva'
                       )
                       AND LOWER(u.email) <> LOWER(%s)
                    """,
                    (submitter_email or '',),
                )
                candidates = cur.fetchall()

                heads = _get_department_heads(cur)
                for candidate in candidates:
                    cand_role = candidate['role']
                    cand_session = {
                        'user_role': cand_role,
                        'user_email': candidate['email'],
                        'user_department': candidate.get('department') or '',
                        'is_department_head': cand_role in (
                            'sef_odeljenja', 'sef_pravne_sluzbe', 'sef_racunovodstva'
                        ),
                    }
                    if not can_user_sign_report_for_department(
                        cand_session,
                        submitter_department,
                        target_employee_email=submitter_email,
                        department_heads=heads,
                    ):
                        continue
                    if is_resubmission:
                        title = 'Радна листа поново поднета (реевалуација)'
                        message = (
                            f'{user_name} је поново поднео/ла радну листу после '
                            f'враћања на измену — потребно је проверити поново.'
                        )
                        icon = 'bi-arrow-repeat'
                        ntype = 'warning'
                    else:
                        title = 'Нова радна листа за преглед'
                        message = f'{user_name} је поднео/ла радну листу на преглед.'
                        icon = 'bi-send-check'
                        ntype = 'info'
                    cur.execute(
                        """
                        INSERT INTO user_notifications (user_email, title, message, icon, type)
                        VALUES (%s, %s, %s, %s, %s)
                        """,
                        (candidate['email'], title, message, icon, ntype),
                    )
                conn.commit()
    except Exception as exc:
        logger.warning("Failed to notify verifiers about timesheet submission: %s", exc)




def _notify_employee_about_review_outcome(report_id, title, icon, message_template):
    try:
        with get_postgres_connection(row_factory=dict_row) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT employee_email, employee_name, month, year FROM timesheet_reports WHERE id = %s",
                    (report_id,),
                )
                report = cur.fetchone()
                if report and report['employee_email']:
                    month_name = (
                        MONTH_NAMES_LOWER[report['month']]
                        if 1 <= report['month'] <= 12
                        else str(report['month'])
                    )
                    cur.execute(
                        """
                        INSERT INTO user_notifications (user_email, title, message, icon, type)
                        VALUES (%s, %s, %s, %s, %s)
                        """,
                        (
                            report['employee_email'],
                            title,
                            message_template(month_name, report['year']),
                            icon,
                            'success' if icon == 'bi-check-circle' else 'warning',
                        ),
                    )
                    conn.commit()
    except Exception as exc:
        logger.warning("Failed to notify employee about timesheet review outcome: %s", exc)


def render_timesheet_entry():
    """Employee timesheet entry page."""
    # Подразумевано се уноси ПРЕТХОДНИ месец. Али ако admin/шеф врати старију
    # листу НА ДОПУНУ, запослени мора моћи да је отвори преко ?month=&year=
    # без обзира на старост — измена такве (REJECTED) листе је дозвољена кроз
    # активни 24 h прозор (види can_edit логику ниже). За НОРМАЛАН унос
    # (DRAFT) месечни рок и даље важи, па стара празна листа остаје незизменљива.
    default_month, default_year = _default_entry_period()
    now = datetime.now()
    month_param = request.args.get('month', '').strip()
    year_param = request.args.get('year', '').strip()
    if (month_param.isdigit() and 1 <= int(month_param) <= 12
            and year_param.isdigit() and 2000 <= int(year_param) <= now.year + 1):
        month, year = int(month_param), int(year_param)
    else:
        month, year = default_month, default_year
    explicit_period = (month, year) != (default_month, default_year)
    months = _month_choices()
    years = _year_choices()
    calendar_data = _build_calendar_data(year, month)

    timesheet_data = None
    error_message = None
    user_full_name = session.get('user_name')
    user_email = session.get('user_email', '')

    if user_full_name:
        try:
            timesheet_data = _load_timesheet_entry_data(user_full_name, user_email, month, year)
        except Exception as exc:
            error_message = f"Грешка при учитавању података: {str(exc)}"
            logger.error("Timesheet load error: %s", exc)

    try:
        returned_reports = _load_returned_reports(user_email, user_full_name)
    except Exception as exc:
        returned_reports = []
        logger.warning("Could not load returned reports: %s", exc)
    # Тренутно отворени месец се већ приказује сопственим банером — у навигацију
    # стављамо само ОСТАЛЕ враћене листе.
    returned_reports_other = [
        r for r in returned_reports
        if not (r.get('month') == month and r.get('year') == year)
    ]

    report_id = None
    status = 'DRAFT'
    rejection_note = ''

    try:
        from timesheet_postgres import ensure_draft_exists, can_edit_timesheet_by_status, can_submit_for_review

        # Празан DRAFT се аутоматски прави САМО за подразумевани месец (нормалан
        # унос). Кад је експлицитно тражен старији месец (нпр. отварање враћене
        # листе), не правимо празне листе за месеце који не постоје — само
        # учитавамо постојећу ако је има.
        if not explicit_period:
            report_id = ensure_draft_exists(
                user_email,
                user_full_name or '',
                month,
                year,
                session.get('user_department', 'Природњачки музеј'),
                session.get('user_position', 'Запослени'),
            )
    except Exception as exc:
        logger.warning("Could not ensure draft exists: %s", exc)
        can_edit_timesheet_by_status = None
        can_submit_for_review = None

    if timesheet_data and timesheet_data.get('exists'):
        status = timesheet_data.get('status', 'DRAFT')
        rejection_note = timesheet_data.get('rejection_note', '') or ''
        if not report_id:
            report_id = timesheet_data.get('radna_lista_id') or timesheet_data.get('report_id')

    can_edit = True
    edit_restriction_message = ""
    needs_approval = False
    is_approved = False
    is_bez_odobrenja = False
    has_approved_request = False
    has_pending_request = False
    show_submit_button = False
    can_submit = False
    submit_message = ''

    # Submit button shows for any pre-review state regardless of whether
    # the deadline/edit helpers imported successfully — users must always
    # have a way to submit a DRAFT/REJECTED report. The backend /submit
    # endpoint re-checks deadlines and returns a clear error if they fail.
    show_submit_button = status in ('DRAFT', 'REJECTED')
    try:
        if can_edit_timesheet_by_status and can_submit_for_review:
            can_edit, edit_restriction_message = can_edit_timesheet_by_status(month, year, status)
            can_submit, submit_message = can_submit_for_review(month, year)
    except Exception as exc:
        logger.warning("Error checking edit/submit permissions: %s", exc)
        can_edit = True
        can_submit = False

    report_locked = bool(timesheet_data and timesheet_data.get('is_locked'))
    has_pending_request = bool(
        (timesheet_data and timesheet_data.get('has_pending_request')) or status == 'SUBMITTED'
    )
    has_approved_request = bool(timesheet_data and timesheet_data.get('has_approved_request'))

    if report_locked:
        can_edit = False
        can_submit = False
        show_submit_button = False
        edit_restriction_message = (
            "Унос за овај месец је затворен. Обратите се администратору "
            "да вам откључа унос."
        )

    # Враћена радна листа (REJECTED) носи 24 h прозор за измену
    # (editable_until) који важи ЗА ТАЈ извештај и превазилази календарски
    # рок — исто правило као window_active у save_timesheet, да се приказ и
    # слој снимања слажу. Без овога запослени види сва поља и дугме „Сачувај"
    # као disabled и не може да унесе исправку коју је шеф/админ затражио.
    if (not report_locked
            and timesheet_data
            and timesheet_data.get('edit_window_active')):
        can_edit = True
        edit_restriction_message = ""
        show_submit_button = status in ('DRAFT', 'REJECTED')

    if status == 'APPROVED':
        is_approved = True
    # НЕ уписује се у is_approved: листа завршена док је одобравање искључено
    # није одобрена. Приказ мора да их разликује, зато посебна застава.
    is_bez_odobrenja = status == odobravanje_prekidac.STATUS_IZVESTAJ_BEZ

    user_department, user_position = _resolve_employee_profile(
        user_email,
        user_full_name,
        session.get('user_department', '') or '',
        session.get('user_position', '') or '',
    )
    user_department = user_department or "Није дефинисано"
    user_position = user_position or "Није дефинисано"

    if timesheet_data is None:
        timesheet_data = {'exists': False, 'is_verified': False}
    elif 'is_verified' not in timesheet_data:
        timesheet_data['is_verified'] = False

    logger.info("📊 DEBUG timesheet_data keys: %s", list(timesheet_data.keys()) if timesheet_data else 'None')
    if timesheet_data and 'OPosao' in timesheet_data:
        logger.info("📊 DEBUG OPosao value preview: %s", str(timesheet_data['OPosao'])[:100])
    else:
        logger.info("📊 DEBUG OPosao field is MISSING from timesheet_data!")

    return _no_cache_response(
        make_response(
            render_template(
                'employee_timesheet.html',
                months=months,
                years=years,
                selected_month=month,
                selected_year=year,
                calendar_data=calendar_data,
                timesheet_data=timesheet_data,
                error_message=error_message,
                user_department=user_department,
                user_position=user_position,
                can_edit=can_edit,
                edit_restriction_message=edit_restriction_message,
                needs_approval=needs_approval,
                has_pending_request=has_pending_request,
                is_approved=is_approved,
                is_bez_odobrenja=is_bez_odobrenja,
                has_approved_request=has_approved_request,
                is_entry_page=True,
                status=status,
                show_submit_button=show_submit_button,
                can_submit=can_submit,
                submit_message=submit_message,
                rejection_note=rejection_note,
                report_id=report_id,
                returned_reports_other=returned_reports_other,
            )
        )
    )


def render_timesheet_view():
    """Employee historical timesheet view page."""
    month_param = request.args.get('month', '').strip()
    year_param = request.args.get('year', '').strip()
    now = datetime.now()
    month = int(month_param) if month_param.isdigit() and 1 <= int(month_param) <= 12 else now.month
    valid_years = _year_choices()
    year = int(year_param) if year_param.isdigit() and int(year_param) in valid_years else now.year

    timesheet_data = None
    error_message = None
    user_full_name = session.get('user_name')

    if user_full_name:
        try:
            timesheet_data = _load_timesheet_view_data(
                user_full_name, month, year, user_email=session.get('user_email'))
        except Exception as exc:
            error_message = f"Грешка при учитавању података: {str(exc)}"
            logger.error("Timesheet load error: %s", exc)

    user_department = "Непознато"
    user_position = "Непознато"
    user_email = session.get('user_email')
    if user_email:
        user_department, user_position = _resolve_employee_profile(user_email, user_full_name)
        user_department = user_department or "Непознато"
        user_position = user_position or "Непознато"

    if timesheet_data is None:
        timesheet_data = {'exists': False, 'is_verified': False}
    elif 'is_verified' not in timesheet_data:
        timesheet_data['is_verified'] = False

    return _no_cache_response(
        make_response(
            render_template(
                'employee_timesheet.html',
                months=_month_choices(),
                years=_year_choices(),
                selected_month=month,
                selected_year=year,
                calendar_data=_build_calendar_data(year, month),
                timesheet_data=timesheet_data,
                error_message=error_message,
                user_department=user_department,
                user_position=user_position,
                can_edit=False,
                edit_restriction_message="Преглед ранијих радних листа (само читање)",
                needs_approval=False,
                has_pending_request=False,
                is_approved=False,
                is_bez_odobrenja=False,
                has_approved_request=False,
                is_entry_page=False,
            )
        )
    )


def api_load_timesheet():
    """API endpoint to load existing timesheet data for a given month/year."""
    from timesheet_postgres import load_timesheet_from_postgres

    try:
        month = int(request.args.get('month', 0))
        year = int(request.args.get('year', 0))
    except (ValueError, TypeError):
        return jsonify({'success': False, 'message': 'Неважећи месец или година'})

    user_email = session.get('user_email')
    user_full_name = session.get('user_name')
    if not user_email and not user_full_name:
        return jsonify({'success': False, 'message': 'Није пријављен'})

    user_identifier = user_email or user_full_name

    try:
        result = load_timesheet_from_postgres(user_identifier, month, year)
        if not result:
            return jsonify({'success': True, 'exists': False, 'daily_data': {}})

        daily_data = {str(day): values for day, values in result['daily_data'].items()}
        return jsonify(
            {
                'success': True,
                'exists': True,
                'daily_data': daily_data,
                'obavljeni_poslovi': result.get('OPosao', ''),
                'is_verified': result.get('is_verified', False),
                'is_locked': result.get('is_locked', False),
                'version': result.get('version', 1),
                'status': result.get('status', 'DRAFT'),
                'submitted_at': result.get('submitted_at', None),
                'rejection_note': result.get('rejection_note', ''),
            }
        )
    except Exception as exc:
        logger.error("API load timesheet error: %s", exc)
        return jsonify({'success': False, 'message': str(exc)})


def api_save_timesheet():
    """Save timesheet data to PostgreSQL."""
    from timesheet_postgres import (
        TimesheetErrorType,
        get_user_department_and_position,
        save_timesheet_to_postgres,
    )

    try:
        data = request.get_json()
        if not data:
            return jsonify({'success': False, 'message': 'Недостају подаци'})

        month = data.get('month')
        year = data.get('year')
        daily_data = data.get('daily_data', {})
        work_description = data.get('obavljeni_poslovi', '')
        expected_version = data.get('version')

        if not month or not year:
            return jsonify({'success': False, 'message': 'Недостају подаци за месец/годину'})

        report_row = None
        try:
            month_check = int(month)
            year_check = int(year)
            with get_postgres_connection(row_factory=dict_row) as conn:
                with conn.cursor() as cur:
                    cur.execute(
                        """
                        SELECT COALESCE(status, 'DRAFT') AS status,
                               (editable_until IS NOT NULL AND NOW() < editable_until)
                                   AS window_active
                        FROM timesheet_reports
                        WHERE (employee_email = %s
                               OR (employee_email IS NULL AND employee_name = %s))
                          AND month = %s AND year = %s
                        """,
                        (
                            session.get('user_email', ''),
                            session.get('user_name', ''),
                            month_check,
                            year_check,
                        ),
                    )
                    report_row = cur.fetchone()
                    if (report_row and report_row['status']
                            in odobravanje_prekidac.IZVESTAJ_NEIZMENJIV):
                        status_label = {
                            'SUBMITTED': 'поднета на преглед',
                            'APPROVED': 'одобрена',
                            odobravanje_prekidac.STATUS_IZVESTAJ_BEZ:
                                'завршена без одобравања',
                        }.get(report_row['status'], 'закључана')
                        return (
                            jsonify(
                                {
                                    'success': False,
                                    'message': f'Радна листа је {status_label} и не може се мењати.',
                                    'error_type': 'locked',
                                }
                            ),
                            423,
                        )

                    # Обичан запослени попуњава ПРЕТХОДНИ месец. Текући/будући
                    # месец се самоуносом не сме отварати без активног
                    # административног откључавања (editable_until у будућности)
                    # или враћене (REJECTED) листе — иначе би се радна листа
                    # предала пре краја месеца, мимо процедуре (ревизија #4).
                    # Админ/директор нису ограничени (оператерски унос).
                    now = datetime.now()
                    is_current_or_future = (
                        year_check > now.year
                        or (year_check == now.year and month_check >= now.month)
                    )
                    window_active = bool(report_row and report_row.get('window_active'))
                    is_rejected = bool(report_row and report_row['status'] == 'REJECTED')
                    if (is_current_or_future
                            and session.get('user_role') not in ('admin', 'direktor')
                            and not window_active and not is_rejected):
                        return (
                            jsonify(
                                {
                                    'success': False,
                                    'message': (
                                        'Унос радне листе за текући/будући месец није '
                                        'омогућен. Попуњава се претходни месец; за унос '
                                        'текућег затражите откључавање од администратора.'
                                    ),
                                    'error_type': 'locked',
                                }
                            ),
                            423,
                        )
        except Exception as exc:
            # Fail-closed: без провере статуса/прозора не сме да се упише —
            # наставак би дозволио измену поднете/оверене листе (ревизија #5).
            logger.error("Status check before save failed (aborting save): %s", exc)
            return (
                jsonify(
                    {
                        'success': False,
                        'message': (
                            'Провера стања радне листе није могућа — упис је '
                            'обустављен. Покушајте поново.'
                        ),
                    }
                ),
                503,
            )

        try:
            month = int(month)
            year = int(year)
        except (ValueError, TypeError):
            return jsonify({'success': False, 'message': 'Неважећи месец или година'})

        user_full_name = session.get('user_name')
        user_email = session.get('user_email')
        if not user_full_name and not user_email:
            return jsonify({'success': False, 'message': 'Није пријављен'})

        organization_unit, position = get_user_department_and_position(user_email or user_full_name)
        result = save_timesheet_to_postgres(
            user_email=user_email or user_full_name,
            user_name=user_full_name or user_email,
            month=month,
            year=year,
            daily_data=daily_data,
            work_description=work_description,
            organization_unit=organization_unit,
            position=position,
            expected_version=int(expected_version) if expected_version else None,
        )

        if result.success:
            # If the employee is fixing a report that was RETURNED (REJECTED),
            # the save is also the act of resubmitting. Flip status →
            # SUBMITTED and ping the head/director with the re-evaluation
            # notification so the return-and-fix cycle closes in one click.
            auto_resubmitted = False
            resubmit_failed = False
            resubmit_error = ''
            was_rejected = bool(report_row and report_row['status'] == 'REJECTED')
            if was_rejected:
                try:
                    from timesheet_postgres import submit_timesheet
                    submit_result = submit_timesheet(
                        result.data.get('report_id'), user_email,
                    )
                    if submit_result.success:
                        auto_resubmitted = True
                        submitter_department = organization_unit or ''
                        _notify_verifiers_about_submission(
                            user_full_name or user_email,
                            user_email,
                            submitter_department,
                            is_resubmission=True,
                        )
                    else:
                        resubmit_failed = True
                        resubmit_error = (submit_result.error.message
                                          if submit_result.error else '')
                        logger.warning(
                            "Auto-resubmit after save of REJECTED report failed: %s",
                            resubmit_error,
                        )
                except Exception as exc:
                    resubmit_failed = True
                    resubmit_error = str(exc)
                    logger.warning("Auto-resubmit after save failed: %s", exc)

            message = result.data.get('message', 'Сачувано')
            if auto_resubmitted:
                message = 'Измене сачуване и извештај је поново поднет на преглед.'
            elif resubmit_failed:
                # Не лажирај успех: сачувано ЈЕСТЕ, али листа је остала REJECTED
                # (није поново поднета). Корисник мора знати да лист НИЈЕ у току
                # одобравања и да мора ручно да поднесе.
                message = ('Измене су сачуване, али извештај НИЈЕ поново поднет на '
                           'преглед — поднесите га ручно. '
                           + (f'Разлог: {resubmit_error}' if resubmit_error else ''))
            return jsonify(
                {
                    'success': True,
                    'message': message,
                    'version': result.data.get('version'),
                    'report_id': result.data.get('report_id'),
                    'auto_resubmitted': auto_resubmitted,
                    'resubmit_failed': resubmit_failed,
                }
            )

        error = result.error
        response_data = {
            'success': False,
            'message': error.message,
            'error_type': error.error_type.value,
        }
        if error.details:
            response_data['details'] = error.details

        if error.error_type == TimesheetErrorType.CONCURRENT_MODIFICATION:
            return jsonify(response_data), 409
        if error.error_type == TimesheetErrorType.LOCKED:
            return jsonify(response_data), 423
        if error.error_type == TimesheetErrorType.VALIDATION_ERROR:
            return jsonify(response_data), 400
        return jsonify(response_data)
    except Exception as exc:
        logger.error("API save timesheet error: %s", exc)
        logger.exception("Timesheet save failed")
        return jsonify({'success': False, 'message': f'Грешка: {str(exc)}'})


def api_timesheet_submit(report_id):
    """Employee submits a timesheet for admin review."""
    from timesheet_postgres import submit_timesheet

    user_email = session.get('user_email')
    if not user_email:
        return jsonify({'success': False, 'message': 'Није пријављен'}), 401

    result = submit_timesheet(report_id, user_email)
    if result.success:
        # Look up the submitter's department so we can notify the right
        # verifiers (admin + director + that department's head).
        submitter_department = ''
        try:
            with get_postgres_connection(row_factory=dict_row) as conn:
                with conn.cursor() as cur:
                    cur.execute(
                        """
                        SELECT COALESCE(d.name, ep.department) AS department
                          FROM users u
                          LEFT JOIN departments d ON u.department_id = d.id
                          LEFT JOIN employee_profiles ep ON LOWER(ep.email) = LOWER(u.email)
                         WHERE LOWER(u.email) = LOWER(%s)
                        """,
                        (user_email,),
                    )
                    row = cur.fetchone()
                    if row:
                        submitter_department = row.get('department') or ''
        except Exception as exc:
            logger.warning("Failed to look up submitter department: %s", exc)

        _notify_verifiers_about_submission(
            session.get('user_name', user_email),
            user_email,
            submitter_department,
            is_resubmission=bool(result.data.get('was_rejected')),
        )
        return jsonify({'success': True, 'message': result.data.get('message', 'Поднето на преглед')})
    return jsonify({'success': False, 'message': result.error.message}), 400


def api_timesheet_reject(report_id):
    """Return a SUBMITTED timesheet to the employee with a note.

    Admin/director/dept head only, with per-report scope enforced. Dept
    heads may only return reports in their own department (not their own
    report). The director returns Edu/Gallery reports and heads' own
    reports. The employee gets a 24 h correction window via the reject
    path's editable_until update.
    """
    from timesheet_postgres import reject_timesheet
    from timesheet_admin_views import (
        _get_department_heads,
        _lookup_report_department,
        can_user_sign_report_for_department,
    )

    note = (request.get_json() or {}).get('note', '').strip()
    if not note:
        return jsonify({'success': False, 'message': 'Молимо унесите разлог враћања'}), 400

    if session.get('user_role') != 'admin':
        try:
            with get_postgres_connection(row_factory=dict_row) as conn:
                with conn.cursor() as cur:
                    report_department, employee_email = _lookup_report_department(cur, report_id)
                    heads = _get_department_heads(cur)
        except Exception as exc:
            logger.error("reject scope lookup failed: %s", exc)
            return jsonify({'success': False, 'message': 'Грешка провере дозволе.'}), 500

        # Двостепено: сваки потписник (шеф ИЛИ директор) сме да врати на допуну.
        if not can_user_sign_report_for_department(
            session, report_department,
            target_employee_email=employee_email,
            department_heads=heads,
        ):
            return jsonify({'success': False, 'message': 'Немате дозволу за ову радњу.'}), 403

    result = reject_timesheet(report_id, session.get('user_email'), note)
    if result.success:
        _notify_employee_about_review_outcome(
            report_id,
            'Радна листа враћена',
            'bi-x-circle',
            lambda month_name, year: (
                f'Ваша радна листа за {month_name} {year}. је враћена на допуну. Разлог: {note}'
            ),
        )
        return jsonify({'success': True, 'message': result.data.get('message', 'Враћено на допуну')})
    return jsonify({'success': False, 'message': result.error.message}), 400


def api_timesheet_force_edit(report_id):
    """Return a report to the employee for re-entry. Admin/director/dept
    head scope is enforced against the current session — dept heads may
    only return reports from their own department (not their own report);
    the director returns Edu/Gallery reports and heads' own reports."""
    from timesheet_postgres import force_edit_timesheet
    from timesheet_admin_views import (
        _get_department_heads,
        _lookup_report_department,
        can_user_sign_report_for_department,
    )

    # Per-report authorization. Admin short-circuits via the decorator; we
    # still re-check here so the scope is enforced at the business layer.
    if session.get('user_role') != 'admin':
        try:
            with get_postgres_connection(row_factory=dict_row) as conn:
                with conn.cursor() as cur:
                    report_department, employee_email = _lookup_report_department(cur, report_id)
                    heads = _get_department_heads(cur)
                    cur.execute(
                        """
                        SELECT id, COALESCE(status, 'DRAFT') AS status
                        FROM timesheet_reports
                        WHERE id = %s
                        """,
                        (report_id,),
                    )
                    status_row = cur.fetchone()
        except Exception as exc:
            logger.error("force_edit scope lookup failed: %s", exc)
            return jsonify({'success': False, 'message': 'Грешка провере дозволе.'}), 500

        # Двостепено: сваки потписник (шеф ИЛИ директор) сме да врати листу.
        if not can_user_sign_report_for_department(
            session, report_department,
            target_employee_email=employee_email,
            department_heads=heads,
        ):
            return jsonify({'success': False, 'message': 'Немате дозволу за ову радњу.'}), 403

        # An APPROVED (verified + locked) report must not be reopened by a
        # department head — that would bypass the unlock-request flow. Only
        # admin/direktor may return an approved report to entry.
        report_status = status_row.get('status') if status_row else None
        if (report_status in odobravanje_prekidac.IZVESTAJ_ZAVRSEN
                and session.get('user_role') not in ('admin', 'direktor')):
            return jsonify(
                {
                    'success': False,
                    'message': (
                        'Оверен извештај може да врати само администратор или '
                        'директор — поднесите захтев за откључавање.'
                    ),
                }
            ), 403

    # Оверену листу сме да отвори само админ/директор. Ова провера је СЕДА
    # ауторитативна унутар force_edit_timesheet (под FOR UPDATE локом) —
    # горња провера на основу застарелог status_row остаје као брза грана,
    # али коначну реч даје лок, чиме се затвара TOCTOU трка (ревизија #2).
    allow_approved_reopen = session.get('user_role') in ('admin', 'direktor')
    result = force_edit_timesheet(
        report_id, session.get('user_email'),
        allow_approved_reopen=allow_approved_reopen,
    )
    if result.success:
        # Откључавање већ ОВЕРЕНЕ листе је осетљива радња — остави траг.
        # Статус пре измене долази из закључане трансакције (FOR UPDATE),
        # па важи за све улоге — админ прескаче scope-грану изнад.
        if result.data.get('old_status') in odobravanje_prekidac.IZVESTAJ_ZAVRSEN:
            try:
                from audit_support import record_audit
                record_audit(
                    action='reopen_approved', entity_type='timesheet_report',
                    entity_id=report_id, changed_by=session.get('user_email'),
                    summary='Оверена радна листа враћена на измену (откључана)',
                )
            except Exception:
                pass
        return jsonify({'success': True, 'message': result.data.get('message', 'Враћено на измену')})
    return jsonify({'success': False, 'message': result.error.message}), 400


def render_admin_timesheet_review():
    """Admin view for timesheets pending review."""
    from timesheet_postgres import get_pending_review_timesheets

    return render_template(
        'admin_timesheet_pending.html',
        pending_reports=get_pending_review_timesheets(),
    )
