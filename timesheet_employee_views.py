"""Shared route implementations for employee timesheet workflows."""

import calendar
import logging
from datetime import date, datetime

from flask import jsonify, make_response, render_template, request, session
from psycopg.rows import dict_row

from postgres_service import get_postgres_connection
from serbian_holidays import SerbianHolidays

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
    current_year = datetime.now().year
    return list(range(current_year - 2, current_year + 3))


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
    current_date = datetime.now()
    if current_date.day <= 7:
        if current_date.month == 1:
            return 12, current_date.year - 1
        return current_date.month - 1, current_date.year
    return current_date.month, current_date.year


def _load_report_header(employee_name, month, year, header_fields):
    query = (
        f"SELECT {header_fields} FROM timesheet_reports "
        "WHERE employee_name = %s AND month = %s AND year = %s "
        "ORDER BY id DESC LIMIT 1"
    )
    # Fallback tolerates ONLY whitespace/case differences in the stored name —
    # never a substring match, which could otherwise return a DIFFERENT
    # employee whose name merely contains this one. Deterministic ordering.
    fallback_query = (
        f"SELECT {header_fields} FROM timesheet_reports "
        "WHERE LOWER(TRIM(employee_name)) = LOWER(TRIM(%s)) AND month = %s AND year = %s "
        "ORDER BY id DESC LIMIT 1"
    )

    with get_postgres_connection(row_factory=dict_row) as conn:
        with conn.cursor() as cur:
            cur.execute(query, (employee_name, month, year))
            header = cur.fetchone()
            if not header:
                cur.execute(fallback_query, (employee_name, month, year))
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
        "submitted_at, rejection_note"
    )
    header = _load_report_header(user_full_name, month, year, header_fields)
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
        'report_id': header['id'],
    }


def _load_timesheet_view_data(user_full_name, month, year):
    header_fields = (
        "id, employee_name, special_tasks, extraordinary_tasks, duties_summary, "
        "is_verified, is_locked, verified_by, verified_at, version"
    )
    header = _load_report_header(user_full_name, month, year, header_fields)
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
    """Notify only the leadership users who can ACTUALLY verify THIS report.

    Rule (reuses `can_user_verify_report_for_department` so policy lives in
    one place):
    - Admin: always.
    - Department head: only if their own department == submitter's department
      (and they are not the submitter themselves).
    - Director: only when the submission is one the director verifies —
      i.e., the submitter's department has no designated head, OR the
      submitter IS a department head (director signs off head reports).

    The submitter is always excluded.
    """
    try:
        # Local import avoids a module-level circular dependency and keeps
        # this helper self-contained.
        from timesheet_admin_views import (
            _get_department_heads,
            can_user_verify_report_for_department,
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
                    if not can_user_verify_report_for_department(
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
    month, year = _default_entry_period()
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

    report_id = None
    status = 'DRAFT'
    rejection_note = ''

    try:
        from timesheet_postgres import ensure_draft_exists, can_edit_timesheet_by_status, can_submit_for_review

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
        if has_pending_request:
            edit_restriction_message = (
                "Захтев за измену је послат и радна листа остаје закључана "
                "док администратор не обради захтев."
            )
        else:
            edit_restriction_message = (
                "Радна листа је закључана. Потребно је одобрење администратора за измене."
            )

    if status == 'APPROVED':
        is_approved = True

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
                has_approved_request=has_approved_request,
                is_entry_page=True,
                status=status,
                show_submit_button=show_submit_button,
                can_submit=can_submit,
                submit_message=submit_message,
                rejection_note=rejection_note,
                report_id=report_id,
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
            timesheet_data = _load_timesheet_view_data(user_full_name, month, year)
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


def request_approval():
    """Create an approval request for editing a locked timesheet."""
    try:
        month = request.form.get('month')
        year = request.form.get('year')
        reason = request.form.get('reason', '').strip()

        if not month or not year or not reason:
            return jsonify({'success': False, 'message': 'Месец, година и разлог су обавезни!'})

        user_email = session.get('user_email')
        user_name = session.get('user_name', 'Unknown')
        if not user_email:
            return jsonify({'success': False, 'message': 'Корисник није пријављен'})

        with get_postgres_connection(row_factory=dict_row) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT id, is_verified, is_locked
                    FROM timesheet_reports
                    WHERE employee_name = %s
                      AND month = %s
                      AND year = %s
                    ORDER BY id DESC
                    LIMIT 1
                    """,
                    (user_name, month, year),
                )
                report = cur.fetchone()

                if not report:
                    cur.execute(
                        """
                        INSERT INTO timesheet_reports
                        (employee_name, month, year, organization_unit, position, is_verified, is_locked, created_at)
                        VALUES (%s, %s, %s, %s, %s, FALSE, FALSE, NOW())
                        RETURNING id
                        """,
                        (
                            user_name,
                            month,
                            year,
                            'Природњачки музеј',
                            session.get('user_position', session.get('position', 'Запослени')),
                        ),
                    )
                    report = cur.fetchone()
                    conn.commit()

                report_id = report['id']

                cur.execute(
                    """
                    SELECT id, status
                    FROM timesheet_edit_requests
                    WHERE report_id = %s
                      AND requester_email = %s
                      AND status = 'pending'
                    """,
                    (report_id, user_email),
                )
                existing_request = cur.fetchone()
                if existing_request:
                    return jsonify(
                        {
                            'success': False,
                            'message': 'Већ постоји захтев на чекању за овај месец',
                        }
                    )

                cur.execute(
                    """
                    INSERT INTO timesheet_edit_requests
                    (report_id, requester_email, reason, status, requested_at)
                    VALUES (%s, %s, %s, 'pending', NOW())
                    RETURNING id
                    """,
                    (report_id, user_email, reason),
                )
                request_id = cur.fetchone()['id']
                conn.commit()

        return jsonify(
            {
                'success': True,
                'message': (
                    f'Захтев је успешно послат! (ID: {request_id})\n'
                    'Бићете обавештени када администратор обради захтев.'
                ),
            }
        )
    except Exception as exc:
        logger.error("Error submitting edit request: %s", exc)
        return jsonify({'success': False, 'message': f'Грешка при слању захтева: {str(exc)}'})


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
                        SELECT status FROM timesheet_reports
                        WHERE (employee_email = %s OR employee_name = %s)
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
                    if report_row and report_row['status'] in ('SUBMITTED', 'APPROVED'):
                        status_label = (
                            'поднета на преглед'
                            if report_row['status'] == 'SUBMITTED'
                            else 'одобрена'
                        )
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
        except Exception as exc:
            logger.warning("Status check before save failed (continuing): %s", exc)

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
            if report_row and report_row['status'] == 'REJECTED':
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
                        logger.warning(
                            "Auto-resubmit after save of REJECTED report failed: %s",
                            submit_result.error.message if submit_result.error else '',
                        )
                except Exception as exc:
                    logger.warning("Auto-resubmit after save failed: %s", exc)

            message = result.data.get('message', 'Сачувано')
            if auto_resubmitted:
                message = 'Измене сачуване и извештај је поново поднет на преглед.'
            return jsonify(
                {
                    'success': True,
                    'message': message,
                    'version': result.data.get('version'),
                    'report_id': result.data.get('report_id'),
                    'auto_resubmitted': auto_resubmitted,
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


def api_timesheet_approve(report_id):
    """Admin approves a submitted timesheet."""
    from timesheet_postgres import approve_timesheet

    result = approve_timesheet(report_id, session.get('user_email'))
    if result.success:
        _notify_employee_about_review_outcome(
            report_id,
            'Радна листа одобрена',
            'bi-check-circle',
            lambda month_name, year: f'Ваша радна листа за {month_name} {year}. је одобрена.',
        )
        return jsonify({'success': True, 'message': result.data.get('message', 'Одобрено')})
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
        can_user_verify_report_for_department,
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

        if not can_user_verify_report_for_department(
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
        can_user_verify_report_for_department,
    )

    # Per-report authorization. Admin short-circuits via the decorator; we
    # still re-check here so the scope is enforced at the business layer.
    if session.get('user_role') != 'admin':
        try:
            with get_postgres_connection(row_factory=dict_row) as conn:
                with conn.cursor() as cur:
                    report_department, employee_email = _lookup_report_department(cur, report_id)
                    heads = _get_department_heads(cur)
        except Exception as exc:
            logger.error("force_edit scope lookup failed: %s", exc)
            return jsonify({'success': False, 'message': 'Грешка провере дозволе.'}), 500

        if not can_user_verify_report_for_department(
            session, report_department,
            target_employee_email=employee_email,
            department_heads=heads,
        ):
            return jsonify({'success': False, 'message': 'Немате дозволу за ову радњу.'}), 403

    result = force_edit_timesheet(report_id, session.get('user_email'))
    if result.success:
        return jsonify({'success': True, 'message': result.data.get('message', 'Враћено на измену')})
    return jsonify({'success': False, 'message': result.error.message}), 400


def render_admin_timesheet_review():
    """Admin view for timesheets pending review."""
    from timesheet_postgres import get_pending_review_timesheets

    return render_template(
        'admin_timesheet_pending.html',
        pending_reports=get_pending_review_timesheets(),
    )
