"""Shared route implementations for the timesheet admin surface."""

import calendar
import logging
import os
from typing import Optional
from urllib.parse import quote

from flask import (
    flash,
    jsonify,
    make_response,
    redirect,
    render_template,
    request,
    send_file,
    session,
    url_for,
)
from psycopg.rows import dict_row

from postgres_service import get_postgres_connection

logger = logging.getLogger(__name__)

REPOSITORY_UNAVAILABLE_MESSAGE = (
    'Централизовани подаци о радним листама нису доступни '
    '(проверите PostgreSQL миграцију).'
)
SERBIAN_MONTHS = [
    'Јануар',
    'Фебруар',
    'Март',
    'Април',
    'Мај',
    'Јун',
    'Јул',
    'Август',
    'Септембар',
    'Октобар',
    'Новембар',
    'Децембар',
]
SERBIAN_MONTHS_LOWER = [month.lower() for month in SERBIAN_MONTHS]


def _parse_int(value: Optional[str]) -> Optional[int]:
    try:
        if value is None or value == '':
            return None
        return int(value)
    except (TypeError, ValueError):
        return None


def _month_options():
    return [(idx, calendar.month_name[idx]) for idx in range(1, 13)]


def _timesheet_repository_available(timesheet_repository):
    return timesheet_repository is not None and timesheet_repository.available


def _timesheet_repository_redirect(timesheet_repository, endpoint):
    if _timesheet_repository_available(timesheet_repository):
        return None
    flash(REPOSITORY_UNAVAILABLE_MESSAGE, 'error')
    return redirect(url_for(endpoint))


def render_timesheet_app(timesheet_repository, timesheet_repository_cls, user_has_module_access):
    """Route implementation for the timesheet landing page."""
    user_email = session.get('user_email')
    user_role = session.get('user_role')

    if not user_has_module_access(user_email, user_role, 'timesheet'):
        flash('Немате дозволу за приступ систему радних листи.', 'error')
        return redirect(url_for('dashboard'))

    timesheet_data = None
    timesheet_labels = {}
    if _timesheet_repository_available(timesheet_repository):
        timesheet_labels = timesheet_repository_cls.CATEGORY_LABELS
        month_summary = timesheet_repository.get_month_summary()
        overall_summary = timesheet_repository.get_overall_summary()
        recent_reports = timesheet_repository.list_reports(page=1, per_page=5)
        timesheet_data = {
            'month_summary': month_summary,
            'overall': overall_summary,
            'recent_reports': recent_reports.get('reports', []),
        }

    return render_template(
        'timesheet_integration.html',
        timesheet_data=timesheet_data,
        timesheet_labels=timesheet_labels,
        user_role=user_role,
        user_name=session.get('user_name'),
        user_email=user_email,
    )


def render_admin_timesheet_main():
    """Main timesheet administration page."""
    return render_template('admin_timesheet_admin.html')


def render_admin_timesheet_reports(timesheet_repository, timesheet_repository_cls):
    """Admin view for centralized timesheet reports."""
    unavailable = _timesheet_repository_redirect(timesheet_repository, 'timesheet_app')
    if unavailable is not None:
        return unavailable

    month = _parse_int(request.args.get('month'))
    year = _parse_int(request.args.get('year'))
    search = request.args.get('search', '').strip() or None
    page = _parse_int(request.args.get('page')) or 1

    reports = timesheet_repository.list_reports(
        page=page,
        per_page=25,
        month=month,
        year=year,
        search=search,
    )
    month_summary = timesheet_repository.get_month_summary(month=month, year=year)
    overall_summary = timesheet_repository.get_overall_summary()

    return render_template(
        'admin_timesheet_reports.html',
        reports=reports,
        month_summary=month_summary,
        overall_summary=overall_summary,
        month=month,
        year=year,
        search=search or '',
        month_options=_month_options(),
        category_labels=timesheet_repository_cls.CATEGORY_LABELS,
        calendar=calendar,
    )


def render_admin_timesheet_report_detail(report_id, timesheet_repository, timesheet_repository_cls):
    """Detailed view of a single report."""
    unavailable = _timesheet_repository_redirect(timesheet_repository, 'timesheet_app')
    if unavailable is not None:
        return unavailable

    report = timesheet_repository.get_report(report_id)
    if not report:
        flash('Тражени извештај није пронађен.', 'error')
        return redirect(url_for('admin_timesheet_reports'))

    return render_template(
        'admin_timesheet_report_detail.html',
        report=report,
        category_labels=timesheet_repository_cls.CATEGORY_LABELS,
        month_name=calendar.month_name[int(report['header'].get('month', 1))],
    )


def render_admin_timesheet_employees(timesheet_repository):
    """Admin view for managing employees in the timesheet system."""
    unavailable = _timesheet_repository_redirect(timesheet_repository, 'admin_panel')
    if unavailable is not None:
        return unavailable

    flash('Ова функција је у развоју. Користите базу запослених за управљање.', 'info')
    return redirect(url_for('employees_database'))


def render_admin_timesheet_users(timesheet_repository):
    """Admin view for managing timesheet system users."""
    unavailable = _timesheet_repository_redirect(timesheet_repository, 'admin_panel')
    if unavailable is not None:
        return unavailable

    flash(
        'Ова функција је у развоју. Користите управљање приступом за конфигурацију корисника.',
        'info',
    )
    return redirect(url_for('manage_user_access'))


def render_admin_timesheet_pending(timesheet_repository):
    """Admin view for pending edit requests."""
    unavailable = _timesheet_repository_redirect(timesheet_repository, 'admin_panel')
    if unavailable is not None:
        return unavailable

    try:
        with get_postgres_connection(row_factory=dict_row) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT
                        ter.id,
                        ter.report_id,
                        ter.requester_email,
                        ter.reason,
                        ter.status,
                        ter.requested_at,
                        ter.processed_at,
                        ter.processed_by,
                        ter.notes,
                        tr.employee_name,
                        tr.month,
                        tr.year,
                        tr.is_verified,
                        tr.is_locked
                    FROM timesheet_edit_requests ter
                    JOIN timesheet_reports tr ON ter.report_id = tr.id
                    ORDER BY
                        CASE ter.status
                            WHEN 'pending' THEN 1
                            WHEN 'approved' THEN 2
                            WHEN 'rejected' THEN 3
                        END,
                        ter.requested_at DESC
                    """
                )
                pending_requests = cur.fetchall()

        for pending_request in pending_requests:
            month_idx = pending_request['month'] - 1
            if 0 <= month_idx < 12:
                pending_request['month_name'] = SERBIAN_MONTHS[month_idx]
            else:
                pending_request['month_name'] = str(pending_request['month'])

        return render_template(
            'admin_timesheet_pending.html',
            pending_requests=pending_requests,
            message=None,
        )
    except Exception as exc:
        logger.error('Error loading timesheet requests: %s', exc)
        flash('Грешка при учитавању захтева.', 'error')
        return render_template(
            'admin_timesheet_pending.html',
            pending_requests=[],
            message=f'Грешка: {str(exc)}',
        )


def render_admin_timesheet_analytics(timesheet_repository):
    """Admin analytics dashboard for the timesheet system."""
    unavailable = _timesheet_repository_redirect(timesheet_repository, 'admin_panel')
    if unavailable is not None:
        return unavailable

    raw_summary = timesheet_repository.get_overall_summary() or {}

    total_hours = 0
    unique_months = 0
    category_breakdown = {}
    employee_stats = []
    department_stats = []
    monthly_trends = []
    yearly_stats = []
    totals = {
        'report_count': 0,
        'work_in_museum': 0,
        'work_outside': 0,
        'leave_hours': 0,
        'total_hours': 0,
    }
    month_names = {idx: month for idx, month in enumerate(SERBIAN_MONTHS, start=1)}

    try:
        with get_postgres_connection(row_factory=dict_row) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT COALESCE(SUM(
                        COALESCE(work_in_museum, 0) + COALESCE(work_outside, 0) +
                        COALESCE(vacation, 0) + COALESCE(public_holiday, 0) +
                        COALESCE(paid_leave, 0) + COALESCE(other_leave, 0) +
                        COALESCE(sick_leave_lt30, 0) + COALESCE(sick_leave_gte30, 0)
                    ), 0) as total_hours
                    FROM timesheet_report_days
                    """
                )
                result = cur.fetchone()
                total_hours = float(result['total_hours']) if result else 0

                cur.execute(
                    """
                    SELECT COUNT(DISTINCT (year, month)) as unique_months
                    FROM timesheet_reports
                    """
                )
                result = cur.fetchone()
                unique_months = int(result['unique_months']) if result else 0

                cur.execute(
                    """
                    SELECT
                        COALESCE(SUM(work_in_museum), 0) as rad_na_mestu,
                        COALESCE(SUM(work_outside), 0) as van_muzeja,
                        COALESCE(SUM(vacation), 0) as godisnji_odmor,
                        COALESCE(SUM(public_holiday), 0) as drzavni_praznik,
                        COALESCE(SUM(paid_leave), 0) as placeno_odsustvo,
                        COALESCE(SUM(other_leave), 0) as ostalo_odsustvo,
                        COALESCE(SUM(sick_leave_lt30), 0) as bolovanje_manje_30,
                        COALESCE(SUM(sick_leave_gte30), 0) as bolovanje_vece_30
                    FROM timesheet_report_days
                    """
                )
                cat_result = cur.fetchone()

                if cat_result and total_hours > 0:
                    categories = {
                        'rad_na_mestu': ('Рад у музеју', float(cat_result['rad_na_mestu'])),
                        'van_muzeja': ('Рад ван музеја', float(cat_result['van_muzeja'])),
                        'godisnji_odmor': ('Годишњи одмор', float(cat_result['godisnji_odmor'])),
                        'drzavni_praznik': ('Државни празник', float(cat_result['drzavni_praznik'])),
                        'placeno_odsustvo': ('Плаћено одсуство', float(cat_result['placeno_odsustvo'])),
                        'ostalo_odsustvo': ('Остало одсуство', float(cat_result['ostalo_odsustvo'])),
                        'bolovanje_manje_30': ('Боловање < 30 дана', float(cat_result['bolovanje_manje_30'])),
                        'bolovanje_vece_30': ('Боловање >= 30 дана', float(cat_result['bolovanje_vece_30'])),
                    }

                    for key, (label, hours) in categories.items():
                        if hours > 0:
                            category_breakdown[key] = {
                                'label': label,
                                'hours': hours,
                                'percentage': (hours / total_hours * 100) if total_hours > 0 else 0,
                            }

                cur.execute(
                    """
                    SELECT
                        r.employee_name as name,
                        COALESCE(ep.department, 'Није дефинисано') as department,
                        COUNT(DISTINCT r.id) as report_count,
                        COALESCE(SUM(d.work_in_museum), 0) as work_in_museum,
                        COALESCE(SUM(d.work_outside), 0) as work_outside,
                        COALESCE(SUM(d.vacation), 0) + COALESCE(SUM(d.public_holiday), 0) +
                        COALESCE(SUM(d.paid_leave), 0) + COALESCE(SUM(d.other_leave), 0) +
                        COALESCE(SUM(d.sick_leave_lt30), 0) + COALESCE(SUM(d.sick_leave_gte30), 0) as leave_hours,
                        COALESCE(SUM(d.work_in_museum), 0) + COALESCE(SUM(d.work_outside), 0) +
                        COALESCE(SUM(d.vacation), 0) + COALESCE(SUM(d.public_holiday), 0) +
                        COALESCE(SUM(d.paid_leave), 0) + COALESCE(SUM(d.other_leave), 0) +
                        COALESCE(SUM(d.sick_leave_lt30), 0) + COALESCE(SUM(d.sick_leave_gte30), 0) as total_hours
                    FROM timesheet_reports r
                    LEFT JOIN timesheet_report_days d ON r.id = d.report_id
                    LEFT JOIN employee_profiles ep ON r.employee_name = ep.full_name
                    GROUP BY r.employee_name, ep.department
                    ORDER BY ep.department, total_hours DESC
                    """
                )
                employee_rows = cur.fetchall()

                for employee in employee_rows:
                    report_count = int(employee['report_count'])
                    employee_total = float(employee['total_hours'] or 0)
                    employee_stats.append(
                        {
                            'name': employee['name'],
                            'department': employee['department'],
                            'report_count': report_count,
                            'work_in_museum': float(employee['work_in_museum'] or 0),
                            'work_outside': float(employee['work_outside'] or 0),
                            'leave_hours': float(employee['leave_hours'] or 0),
                            'total_hours': employee_total,
                            'avg_per_month': employee_total / report_count if report_count > 0 else 0,
                        }
                    )
                    totals['report_count'] += report_count
                    totals['work_in_museum'] += float(employee['work_in_museum'] or 0)
                    totals['work_outside'] += float(employee['work_outside'] or 0)
                    totals['leave_hours'] += float(employee['leave_hours'] or 0)
                    totals['total_hours'] += employee_total

                cur.execute(
                    """
                    SELECT
                        r.year,
                        r.month,
                        COUNT(DISTINCT r.id) as report_count,
                        COALESCE(SUM(
                            COALESCE(d.work_in_museum, 0) + COALESCE(d.work_outside, 0) +
                            COALESCE(d.vacation, 0) + COALESCE(d.public_holiday, 0) +
                            COALESCE(d.paid_leave, 0) + COALESCE(d.other_leave, 0) +
                            COALESCE(d.sick_leave_lt30, 0) + COALESCE(d.sick_leave_gte30, 0)
                        ), 0) as total_hours
                    FROM timesheet_reports r
                    LEFT JOIN timesheet_report_days d ON r.id = d.report_id
                    GROUP BY r.year, r.month
                    ORDER BY r.year DESC, r.month DESC
                    LIMIT 12
                    """
                )
                trend_rows = cur.fetchall()

                for trend in trend_rows:
                    monthly_trends.append(
                        {
                            'year': trend['year'],
                            'month': trend['month'],
                            'month_name': month_names.get(trend['month'], str(trend['month'])),
                            'report_count': int(trend['report_count']),
                            'total_hours': float(trend['total_hours'] or 0),
                        }
                    )

                cur.execute(
                    """
                    SELECT
                        COALESCE(ep.department, 'Није дефинисано') as name,
                        COUNT(DISTINCT r.employee_name) as employee_count,
                        COALESCE(SUM(
                            COALESCE(d.work_in_museum, 0) + COALESCE(d.work_outside, 0) +
                            COALESCE(d.vacation, 0) + COALESCE(d.public_holiday, 0) +
                            COALESCE(d.paid_leave, 0) + COALESCE(d.other_leave, 0) +
                            COALESCE(d.sick_leave_lt30, 0) + COALESCE(d.sick_leave_gte30, 0)
                        ), 0) as total_hours
                    FROM timesheet_reports r
                    LEFT JOIN timesheet_report_days d ON r.id = d.report_id
                    LEFT JOIN employee_profiles ep ON r.employee_name = ep.full_name
                    GROUP BY ep.department
                    ORDER BY total_hours DESC
                    """
                )
                department_rows = cur.fetchall()

                max_dept_hours = max(
                    [float(department['total_hours'] or 0) for department in department_rows],
                    default=1,
                )
                for department in department_rows:
                    dept_hours = float(department['total_hours'] or 0)
                    department_stats.append(
                        {
                            'name': department['name'],
                            'employee_count': int(department['employee_count']),
                            'total_hours': dept_hours,
                            'percentage': (dept_hours / max_dept_hours * 100) if max_dept_hours > 0 else 0,
                        }
                    )

                cur.execute(
                    """
                    SELECT
                        r.year,
                        COUNT(DISTINCT r.id) as report_count,
                        COUNT(DISTINCT r.employee_name) as employee_count,
                        COALESCE(SUM(
                            COALESCE(d.work_in_museum, 0) + COALESCE(d.work_outside, 0) +
                            COALESCE(d.vacation, 0) + COALESCE(d.public_holiday, 0) +
                            COALESCE(d.paid_leave, 0) + COALESCE(d.other_leave, 0) +
                            COALESCE(d.sick_leave_lt30, 0) + COALESCE(d.sick_leave_gte30, 0)
                        ), 0) as total_hours
                    FROM timesheet_reports r
                    LEFT JOIN timesheet_report_days d ON r.id = d.report_id
                    GROUP BY r.year
                    ORDER BY r.year DESC
                    """
                )
                year_rows = cur.fetchall()

                for year in year_rows:
                    yearly_stats.append(
                        {
                            'year': year['year'],
                            'report_count': int(year['report_count']),
                            'employee_count': int(year['employee_count']),
                            'total_hours': float(year['total_hours'] or 0),
                        }
                    )
    except Exception as exc:
        logger.error('Error getting timesheet analytics: %s', exc)

    overall_summary = {
        'total_reports': raw_summary.get('reports', 0),
        'total_employees': raw_summary.get('employees', 0),
        'total_hours': total_hours,
        'unique_months': unique_months,
        'category_breakdown': category_breakdown,
    }

    return render_template(
        'admin_timesheet_analytics.html',
        overall_summary=overall_summary,
        employee_stats=employee_stats,
        department_stats=department_stats,
        monthly_trends=monthly_trends,
        yearly_stats=yearly_stats,
        totals=totals,
    )


def api_admin_employee_analytics():
    """Get detailed analytics for a specific employee."""
    try:
        employee_name = request.args.get('name', '')
        if not employee_name:
            return jsonify({'success': False, 'message': 'Име запосленог није наведено'})

        with get_postgres_connection(row_factory=dict_row) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT
                        COUNT(DISTINCT r.id) as total_reports,
                        COALESCE(SUM(
                            d.work_in_museum + d.work_outside + d.vacation + d.public_holiday +
                            d.paid_leave + d.other_leave + d.sick_leave_lt30 + d.sick_leave_gte30
                        ), 0) as total_hours,
                        COALESCE(SUM(d.work_in_museum), 0) as work_in_museum,
                        COALESCE(SUM(d.work_outside), 0) as work_outside,
                        COALESCE(SUM(
                            d.vacation + d.public_holiday + d.paid_leave + d.other_leave +
                            d.sick_leave_lt30 + d.sick_leave_gte30
                        ), 0) as leave_hours
                    FROM timesheet_reports r
                    LEFT JOIN timesheet_report_days d ON r.id = d.report_id
                    WHERE r.employee_name = %s
                    """,
                    (employee_name,),
                )
                summary_row = cur.fetchone()

                cur.execute(
                    """
                    SELECT COUNT(DISTINCT (year, month)) as months_count
                    FROM timesheet_reports
                    WHERE employee_name = %s
                    """,
                    (employee_name,),
                )
                months_result = cur.fetchone()
                months_count = (
                    months_result['months_count']
                    if months_result and months_result['months_count'] > 0
                    else 1
                )

                summary = {
                    'total_reports': summary_row['total_reports'] if summary_row else 0,
                    'total_hours': float(summary_row['total_hours']) if summary_row else 0,
                    'avg_per_month': round(float(summary_row['total_hours']) / months_count, 1)
                    if summary_row
                    else 0,
                    'work_in_museum': float(summary_row['work_in_museum']) if summary_row else 0,
                    'work_outside': float(summary_row['work_outside']) if summary_row else 0,
                    'leave_hours': float(summary_row['leave_hours']) if summary_row else 0,
                }

                cur.execute(
                    """
                    SELECT
                        r.year,
                        r.month,
                        COALESCE(SUM(
                            d.work_in_museum + d.work_outside + d.vacation + d.public_holiday +
                            d.paid_leave + d.other_leave + d.sick_leave_lt30 + d.sick_leave_gte30
                        ), 0) as total_hours
                    FROM timesheet_reports r
                    LEFT JOIN timesheet_report_days d ON r.id = d.report_id
                    WHERE r.employee_name = %s
                    GROUP BY r.year, r.month
                    ORDER BY r.year DESC, r.month DESC
                    """,
                    (employee_name,),
                )
                monthly_rows = cur.fetchall()

                monthly_breakdown = []
                for row in monthly_rows:
                    monthly_breakdown.append(
                        {
                            'year': row['year'],
                            'month': row['month'],
                            'month_name': SERBIAN_MONTHS[row['month'] - 1] if 1 <= row['month'] <= 12 else '',
                            'total_hours': float(row['total_hours']),
                        }
                    )

                cur.execute(
                    """
                    SELECT
                        COALESCE(SUM(d.work_in_museum), 0) as work_in_museum,
                        COALESCE(SUM(d.work_outside), 0) as work_outside,
                        COALESCE(SUM(d.vacation), 0) as vacation,
                        COALESCE(SUM(d.public_holiday), 0) as public_holiday,
                        COALESCE(SUM(d.paid_leave), 0) as paid_leave,
                        COALESCE(SUM(d.other_leave), 0) as other_leave,
                        COALESCE(SUM(d.sick_leave_lt30), 0) as sick_leave_lt30,
                        COALESCE(SUM(d.sick_leave_gte30), 0) as sick_leave_gte30
                    FROM timesheet_reports r
                    LEFT JOIN timesheet_report_days d ON r.id = d.report_id
                    WHERE r.employee_name = %s
                    """,
                    (employee_name,),
                )
                category_row = cur.fetchone()

                category_breakdown = {
                    'work_in_museum': float(category_row['work_in_museum']) if category_row else 0,
                    'work_outside': float(category_row['work_outside']) if category_row else 0,
                    'vacation': float(category_row['vacation']) if category_row else 0,
                    'public_holiday': float(category_row['public_holiday']) if category_row else 0,
                    'paid_leave': float(category_row['paid_leave']) if category_row else 0,
                    'other_leave': float(category_row['other_leave']) if category_row else 0,
                    'sick_leave_lt30': float(category_row['sick_leave_lt30']) if category_row else 0,
                    'sick_leave_gte30': float(category_row['sick_leave_gte30']) if category_row else 0,
                }

        return jsonify(
            {
                'success': True,
                'employee_name': employee_name,
                'summary': summary,
                'monthly_breakdown': monthly_breakdown,
                'category_breakdown': category_breakdown,
            }
        )
    except Exception as exc:
        logger.exception('Error loading employee analytics')
        return jsonify({'success': False, 'message': f'Грешка: {str(exc)}'})


def api_admin_get_timesheet_report(report_id, timesheet_repository):
    """Get a single timesheet report with daily entries."""
    try:
        if not _timesheet_repository_available(timesheet_repository):
            return jsonify({'success': False, 'message': 'База података није доступна'})

        report = timesheet_repository.get_report(report_id)
        if not report:
            return jsonify({'success': False, 'message': 'Извештај није пронађен'})

        return jsonify({'success': True, 'report': report})
    except Exception as exc:
        return jsonify({'success': False, 'message': f'Грешка: {str(exc)}'})


def api_admin_approve_timesheet_report(report_id, timesheet_repository):
    """Approve or disapprove a timesheet report."""
    try:
        if not _timesheet_repository_available(timesheet_repository):
            return jsonify({'success': False, 'message': 'База података није доступна'})

        data = request.get_json() or {}
        approve = data.get('approve', True)
        admin_email = session.get('user_email', 'Unknown Admin')

        with get_postgres_connection(row_factory=dict_row) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT id, employee_name, month, year FROM timesheet_reports WHERE id = %s",
                    (report_id,),
                )
                report = cur.fetchone()
                if not report:
                    return jsonify({'success': False, 'message': 'Извештај није пронађен'})

                if approve:
                    cur.execute(
                        """
                        UPDATE timesheet_reports
                        SET is_verified = TRUE,
                            verified_by = %s,
                            verified_at = NOW(),
                            is_locked = TRUE
                        WHERE id = %s
                        """,
                        (admin_email, report_id),
                    )
                    message = 'Извештај је одобрен и закључан'

                    month_name = (
                        SERBIAN_MONTHS_LOWER[report['month'] - 1]
                        if 1 <= report['month'] <= 12
                        else str(report['month'])
                    )
                    cur.execute(
                        "SELECT email FROM users WHERE full_name = %s AND is_active = TRUE",
                        (report['employee_name'],),
                    )
                    user_row = cur.fetchone()
                    if user_row:
                        cur.execute(
                            """
                            INSERT INTO user_notifications (user_email, title, message, icon, type)
                            VALUES (%s, %s, %s, 'bi-check-circle', 'success')
                            """,
                            (
                                user_row['email'],
                                'Радна листа верификована',
                                f"Ваша радна листа за {month_name} {report['year']}. је верификована.",
                            ),
                        )
                else:
                    cur.execute(
                        """
                        UPDATE timesheet_reports
                        SET is_verified = FALSE,
                            verified_by = NULL,
                            verified_at = NULL,
                            is_locked = FALSE
                        WHERE id = %s
                        """,
                        (report_id,),
                    )
                    message = 'Верификација извештаја је повучена'

                conn.commit()

        return jsonify({'success': True, 'message': message})
    except Exception as exc:
        return jsonify({'success': False, 'message': f'Грешка: {str(exc)}'})


def api_admin_batch_approve_timesheet_reports(timesheet_repository):
    """Batch approve or disapprove multiple timesheet reports."""
    try:
        if not _timesheet_repository_available(timesheet_repository):
            return jsonify({'success': False, 'message': 'База података није доступна'})

        data = request.get_json() or {}
        report_ids = data.get('report_ids', [])
        approve = data.get('approve', True)

        if not report_ids:
            return jsonify({'success': False, 'message': 'Није изабран ниједан извештај'}), 400
        if not isinstance(report_ids, list):
            return jsonify({'success': False, 'message': 'Неисправан формат података'}), 400
        if len(report_ids) > 100:
            return jsonify({'success': False, 'message': 'Максимално 100 извештаја одједном'}), 400

        try:
            report_ids = [int(report_id) for report_id in report_ids]
        except (ValueError, TypeError):
            return jsonify({'success': False, 'message': 'Неисправни ID-ови извештаја'}), 400

        admin_email = session.get('user_email', 'Unknown Admin')

        with get_postgres_connection(row_factory=dict_row) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT id, employee_name, month, year FROM timesheet_reports WHERE id = ANY(%s)",
                    (report_ids,),
                )
                existing_reports = cur.fetchall()
                existing_ids = {row['id'] for row in existing_reports}

                if not existing_ids:
                    return jsonify(
                        {'success': False, 'message': 'Ниједан од изабраних извештаја није пронађен'}
                    )

                if approve:
                    cur.execute(
                        """
                        UPDATE timesheet_reports
                        SET is_verified = TRUE,
                            verified_by = %s,
                            verified_at = NOW(),
                            is_locked = TRUE
                        WHERE id = ANY(%s)
                        """,
                        (admin_email, list(existing_ids)),
                    )
                    action_msg = 'верификовано и закључано'

                    for report in existing_reports:
                        month_name = (
                            SERBIAN_MONTHS_LOWER[report['month'] - 1]
                            if 1 <= report['month'] <= 12
                            else str(report['month'])
                        )
                        cur.execute(
                            "SELECT email FROM users WHERE full_name = %s AND is_active = TRUE",
                            (report['employee_name'],),
                        )
                        user_row = cur.fetchone()
                        if user_row:
                            cur.execute(
                                """
                                INSERT INTO user_notifications (user_email, title, message, icon, type)
                                VALUES (%s, %s, %s, 'bi-check-circle', 'success')
                                """,
                                (
                                    user_row['email'],
                                    'Радна листа верификована',
                                    f"Ваша радна листа за {month_name} {report['year']}. је верификована.",
                                ),
                            )
                else:
                    cur.execute(
                        """
                        UPDATE timesheet_reports
                        SET is_verified = FALSE,
                            verified_by = NULL,
                            verified_at = NULL,
                            is_locked = FALSE
                        WHERE id = ANY(%s)
                        """,
                        (list(existing_ids),),
                    )
                    action_msg = 'верификација повучена'

                conn.commit()

        processed_count = len(existing_ids)
        skipped_count = len(report_ids) - processed_count
        message = f'Успешно {action_msg}: {processed_count} извештај(а)'
        if skipped_count > 0:
            message += f' (прескочено: {skipped_count})'

        return jsonify(
            {
                'success': True,
                'message': message,
                'processed': processed_count,
                'skipped': skipped_count,
            }
        )
    except Exception as exc:
        return jsonify({'success': False, 'message': f'Грешка: {str(exc)}'})


def api_admin_export_timesheet_report(report_id, timesheet_repository):
    """Export a timesheet report to a Word document."""
    try:
        if not _timesheet_repository_available(timesheet_repository):
            flash('База података није доступна', 'error')
            return redirect(url_for('admin_timesheet_reports'))

        try:
            from timesheet_word_export import generate_word_document
        except ImportError:
            flash('Word export модул није доступан. Користите PDF export.', 'warning')
            return redirect(url_for('admin_timesheet_reports'))

        output_path = generate_word_document(report_id, os.environ.get('DATABASE_URL'))
        if not output_path or not os.path.exists(output_path):
            flash('Грешка при генерисању документа', 'error')
            return redirect(url_for('admin_timesheet_reports'))

        encoded_filename = quote(os.path.basename(output_path))
        response = make_response(
            send_file(
                output_path,
                mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document',
            )
        )
        response.headers['Content-Disposition'] = f"attachment; filename*=UTF-8''{encoded_filename}"
        response.headers['Content-Type'] = (
            'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
        )
        response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '0'
        return response
    except Exception as exc:
        logger.error('Error exporting timesheet: %s', exc)
        flash('Грешка при експорту.', 'error')
        return redirect(url_for('admin_timesheet_reports'))


def api_admin_delete_timesheet_report(report_id, timesheet_repository):
    """Delete a timesheet report and its entries."""
    try:
        if not _timesheet_repository_available(timesheet_repository):
            return jsonify({'success': False, 'message': 'База података није доступна'})

        with get_postgres_connection(row_factory=dict_row) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT id, employee_name, month, year FROM timesheet_reports WHERE id = %s",
                    (report_id,),
                )
                report = cur.fetchone()
                if not report:
                    return jsonify({'success': False, 'message': 'Извештај није пронађен'})

                cur.execute("DELETE FROM timesheet_entries WHERE report_id = %s", (report_id,))
                entries_deleted = cur.rowcount

                cur.execute("DELETE FROM timesheet_report_days WHERE report_id = %s", (report_id,))
                days_deleted = cur.rowcount

                cur.execute("DELETE FROM timesheet_reports WHERE id = %s", (report_id,))
                conn.commit()

        return jsonify(
            {
                'success': True,
                'message': f'Извештај је обрисан ({days_deleted} дана, {entries_deleted} уноса)',
            }
        )
    except Exception as exc:
        return jsonify({'success': False, 'message': f'Грешка: {str(exc)}'})


def admin_approve_edit_request(request_id, timesheet_repository):
    """Approve or reject an edit request."""
    try:
        if not _timesheet_repository_available(timesheet_repository):
            return jsonify({'success': False, 'message': 'База података није доступна'})

        data = request.get_json() or request.form.to_dict()
        action = data.get('action')
        notes = data.get('notes', '').strip()

        if action not in ['approve', 'reject']:
            return jsonify({'success': False, 'message': 'Неважећа акција'})

        admin_email = session.get('user_email', 'Unknown Admin')
        status = 'approved' if action == 'approve' else 'rejected'

        with get_postgres_connection(row_factory=dict_row) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    UPDATE timesheet_edit_requests
                    SET status = %s,
                        processed_at = NOW(),
                        processed_by = %s,
                        notes = %s
                    WHERE id = %s
                    """,
                    (status, admin_email, notes, request_id),
                )

                if cur.rowcount == 0:
                    return jsonify({'success': False, 'message': 'Захтев није пронађен'})

                if action == 'approve':
                    cur.execute(
                        """
                        UPDATE timesheet_reports tr
                        SET is_locked = FALSE
                        FROM timesheet_edit_requests ter
                        WHERE ter.id = %s AND ter.report_id = tr.id
                        """,
                        (request_id,),
                    )

                conn.commit()

        message = 'Захтев је одобрен' if action == 'approve' else 'Захтев је одбијен'
        return jsonify({'success': True, 'message': message})
    except Exception as exc:
        return jsonify({'success': False, 'message': f'Грешка: {str(exc)}'})
