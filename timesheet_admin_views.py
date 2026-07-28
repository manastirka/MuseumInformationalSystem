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
import audit_support

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


def _session_is_admin(session_data) -> bool:
    return session_data.get('user_role') == 'admin'


def _session_is_director(session_data) -> bool:
    return session_data.get('user_role') == 'direktor'


def _session_is_department_head(session_data) -> bool:
    return bool(session_data.get('is_department_head', False))


def _norm_dept(name) -> str:
    """Normalize a department name for comparisons (trim + casefold).

    `departments.name` and `employee_profiles.department` are maintained by
    hand and can drift in case/whitespace; policy checks must not depend on
    that.
    """
    return (name or '').strip().casefold()


def _get_department_heads(cursor) -> dict:
    """Return `{normalized_department_name: head_email}` for all departments
    whose head is an active user with a leadership role (keys are normalized
    via `_norm_dept`). Used to decide whether the director should verify a
    given report: if the report's department has a head, the head verifies
    regular employees there; the director only verifies the head's own report
    (and reports from heads-less departments).
    """
    from core_app_views import DEPARTMENT_HEAD_ROLES
    cursor.execute(
        """
        SELECT COALESCE(d.name, ep.department) AS department, u.email AS head_email
        FROM users u
        JOIN roles r ON u.role_id = r.id
        LEFT JOIN departments d ON u.department_id = d.id
        LEFT JOIN employee_profiles ep ON LOWER(ep.email) = LOWER(u.email)
        WHERE u.is_active = TRUE
          AND r.name = ANY(%s)
        """,
        (list(DEPARTMENT_HEAD_ROLES),),
    )
    heads = {}
    for row in cursor.fetchall():
        if isinstance(row, dict):
            dept = (row.get('department') or '').strip()
            email = (row.get('head_email') or '').strip()
        else:
            dept = (row[0] or '').strip()
            email = (row[1] or '').strip()
        if dept:
            heads[_norm_dept(dept)] = email.lower()
    return heads


def can_user_view_report_for_department(session_data, target_department) -> bool:
    """Return True if the session user may VIEW (read) a report in the given
    department. Less restrictive than verification: directors see every
    report across departments; department heads see only their own.
    """
    if _session_is_admin(session_data) or _session_is_director(session_data):
        return True
    if not _session_is_department_head(session_data):
        return False
    user_dept = _norm_dept(session_data.get('user_department'))
    target = _norm_dept(target_department)
    return bool(user_dept) and bool(target) and user_dept == target


def can_user_verify_report_for_department(
    session_data,
    target_department,
    target_employee_email: Optional[str] = None,
    department_heads: Optional[dict] = None,
) -> bool:
    """Return True if the session user may view/verify a report belonging to
    an employee in `target_department`.

    Rules:
    - Admin: always (system administrator).
    - Department head (sef_odeljenja / sef_pravne_sluzbe / sef_racunovodstva):
      only reports in their own department, AND never their own report
      (self-approval is forbidden — the director verifies head reports).
    - Director: reports in departments WITHOUT a designated head (Edu,
      Gallery), AND reports submitted by a department head (so heads get
      their own timesheets approved by the director). For regular employees
      in departments that have a head, the director does NOT verify — the
      head does.
    - Everyone else: never.

    `target_employee_email` and `department_heads` are required for non-admin
    verification. Missing context is denied so a route cannot accidentally
    bypass the head-vs-employee split or self-approval guards.
    """
    if _session_is_admin(session_data):
        return True

    target = _norm_dept(target_department)
    target_email_lc = (target_employee_email or '').strip().lower()
    if not target:
        return False

    # Normalize the heads-map keys so lookups survive case/whitespace drift
    # between departments.name and employee_profiles.department.
    heads_by_dept = None
    if department_heads is not None:
        heads_by_dept = {
            _norm_dept(dept): (email or '').strip().lower()
            for dept, email in department_heads.items()
        }

    if _session_is_director(session_data):
        # Self-approval guard: director cannot verify their own timesheet.
        # The admin signs off the director's report.
        user_email_lc = (session_data.get('user_email') or '').strip().lower()
        if user_email_lc and target_email_lc and user_email_lc == target_email_lc:
            return False

        if heads_by_dept is None:
            return False
        head_email = heads_by_dept.get(target)
        if not head_email:
            # Department has no head (Edu, Gallery, Director) — director
            # approves reports there, except their own (caught above).
            return True
        # Department has a head — director only verifies the head's own report.
        return bool(target_email_lc) and target_email_lc == head_email

    if not _session_is_department_head(session_data):
        return False
    user_dept = _norm_dept(session_data.get('user_department'))
    if not user_dept or not target or user_dept != target:
        return False

    # Department heads may not verify their own timesheet. The director
    # handles head reports. Three complementary guards:
    #   (a) direct email match (session.user_email == target_employee_email)
    #   (b) target is the registered head of this department (via heads map)
    #       — blocks even when session.user_email is absent (stale session)
    #   (c) session user IS the head but target email is unknown (NULL in DB)
    #       — refuse rather than silently self-approve.
    user_email_lc = (session_data.get('user_email') or '').strip().lower()

    # (a)
    if user_email_lc and target_email_lc and user_email_lc == target_email_lc:
        return False

    if heads_by_dept is not None:
        head_email = heads_by_dept.get(target)
        if head_email:
            # (b): target IS the head — only director approves head reports.
            if target_email_lc and target_email_lc == head_email:
                return False
            # (c): target email unknown but current user IS the head.
            if not target_email_lc and user_email_lc == head_email:
                return False
    elif not target_email_lc:
        return False
    return True


def _signature_plan(session_data, target_department, target_employee_email,
                    department_heads):
    """Одреди план двостепеног потписа за дату листу и тренутног корисника.

    Враћа dict: ``{allowed, slot, head_required, head_email}`` где је
    ``slot`` ∈ {'head', 'director', 'both', None}.

    Правила (задржавају постојеће понашање за изузетке):
    - Регуларан запослени у одељењу СА шефом → траже се ОБА потписа: шеф ('head')
      и директор ('director').
    - Листа самог шефа (одељење има шефа, а листа је баш његова) → head се не
      тражи, потписује директор ('director').
    - Одељење/шеф НИЈЕ поуздано разрешен (нема шефа у мапи — одељења још нису сва
      формирана) → редован ланац НЕ може да се комплетира, па нема тихог редовног
      одобрења: једини пут напред је АДМИНИСТРАТИВНО одобрење (админ увек;
      директор такође, али обележено као административно, никад као редован
      ланац). Остали немају овлашћење → deny (обичан forbidden).
    - Админ → АДМИНИСТРАТИВНО одобрење (посебан траг, не изгледа као два потписа).
    - Иста особа = шеф И директор овог одељења → њен потпис попуњава оба ('both').
    - Нико не потписује сопствену листу (ту улогу преузима надлежни изнад/админ).

    Кључеви повратног dict-а: ``allowed``, ``slot``, ``head_required``,
    ``head_email`` и ``administrative`` (True → одобри административно, слот се
    игнорише).
    """
    target = _norm_dept(target_department)
    target_email = (target_employee_email or '').strip().lower()
    heads_by_dept = {}
    if department_heads:
        heads_by_dept = {
            _norm_dept(dept): (email or '').strip().lower()
            for dept, email in department_heads.items()
        }
    head_email = heads_by_dept.get(target) or None
    is_employee_head = bool(head_email) and target_email == head_email
    head_required = bool(head_email) and not is_employee_head

    user_email = (session_data.get('user_email') or '').strip().lower()

    def _deny():
        return {'allowed': False, 'slot': None, 'administrative': False,
                'head_required': head_required, 'head_email': head_email}

    def _allow(slot, administrative=False):
        return {'allowed': True, 'slot': slot, 'administrative': administrative,
                'head_required': head_required, 'head_email': head_email}

    # Админ: пуно овлашћење — али као АДМИНИСТРАТИВНО одобрење (посебан траг),
    # не као лажни двостепени ланац.
    if _session_is_admin(session_data):
        return _allow(None, administrative=True)

    is_director = _session_is_director(session_data)
    is_head_here = (
        _session_is_department_head(session_data)
        and bool(target)
        and _norm_dept(session_data.get('user_department')) == target
    )
    signs_own = bool(user_email) and bool(target_email) and user_email == target_email

    # Одељење/шеф НИЈЕ поуздано разрешен (нема шефа у мапи — одељења још нису сва
    # формирана). Не смемо тихо да прескочимо шефа и прогласимо листу редовно
    # одобреном. Директор (као и админ горе) може да одобри АДМИНИСТРАТИВНО
    # (обележено, са трагом — резултат јасно каже „административно"), никад као
    # редован двостепени ланац. Остали немају овлашћење → обичан forbidden.
    if head_email is None:
        if is_director and not signs_own:
            return _allow(None, administrative=True)
        return _deny()

    # Иста особа је и шеф овог одељења и директор → један потпис = оба слота.
    if head_required and head_email and user_email == head_email and is_director:
        return _allow('both')

    if is_director:
        # Директор не потписује сопствену листу — то ради админ.
        return _deny() if signs_own else _allow('director')

    # Шеф одељења потписује 'head' слот регуларних запослених свог одељења.
    if is_head_here and head_required and not signs_own:
        return _allow('head')

    return _deny()


def can_user_sign_report_for_department(session_data, target_department,
                                        target_employee_email=None,
                                        department_heads=None):
    """Двостепено: сме ли корисник да ПОТПИШЕ ову листу — тј. да је одобри
    (свој слот) или врати на допуну. True ако _signature_plan даје неки слот
    (шеф ИЛИ директор ИЛИ админ). Замена за can_user_verify_report_for_department
    у путањама одобравања/враћања: под старим правилом директор је био блокиран
    за регуларне запослене одељења са шефом, па није имао дугме „Одобри" ни
    могућност враћања."""
    return _signature_plan(
        session_data, target_department, target_employee_email, department_heads
    )['allowed']


def _department_scope_for_session() -> Optional[str]:
    """Return the department to scope the reports list to, or None for no scope.

    Admins and directors see every department (None). Department heads are
    scoped to their own department. Other users would not reach this view (the
    route decorator stops them), so they get an explicit empty-result scope.
    """
    if _session_is_admin(session) or _session_is_director(session):
        return None
    if _session_is_department_head(session):
        return (session.get('user_department') or '').strip() or '__no_department__'
    return '__no_department__'


def _lookup_report_department(cursor, report_id):
    """Return `(department, employee_email)` for `report_id`, or `(None, None)`.

    Tuple return lets callers apply the director-specific head-vs-employee
    rule without an extra query.
    """
    cursor.execute(
        """
        SELECT ep.department AS employee_department,
               tr.employee_email AS employee_email
        FROM timesheet_reports tr
        LEFT JOIN employee_profiles ep ON LOWER(ep.email) = LOWER(tr.employee_email)
        WHERE tr.id = %s
        """,
        (report_id,),
    )
    row = cursor.fetchone()
    if not row:
        return None, None
    if isinstance(row, dict):
        return row.get('employee_department'), row.get('employee_email')
    try:
        return row[0], row[1]
    except (TypeError, IndexError):
        return None, None


def _forbidden_json(message='Немате дозволу за приступ'):
    return jsonify({'success': False, 'message': message}), 403


def _parse_int(value: Optional[str]) -> Optional[int]:
    try:
        if value is None or value == '':
            return None
        return int(value)
    except (TypeError, ValueError):
        return None


def _month_options():
    return [(idx, SERBIAN_MONTHS[idx - 1]) for idx in range(1, 13)]


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


def render_admin_timesheet_reports(timesheet_repository, timesheet_repository_cls,
                                   scope='current'):
    """Admin view for centralized timesheet reports.

    ``scope='current'`` (подразумевано) приказује само ТЕКУЋЕ листе — ручно
    унете, текуће године; увезене архивске и старије године иду у АРХИВУ
    (``scope='archive'``). Раздвајање је само приказ — ништа се не брише.
    """
    from datetime import datetime

    unavailable = _timesheet_repository_redirect(timesheet_repository, 'timesheet_app')
    if unavailable is not None:
        return unavailable

    archived = scope == 'archive'
    current_year = datetime.now().year

    month = _parse_int(request.args.get('month'))
    year = _parse_int(request.args.get('year'))
    search = request.args.get('search', '').strip() or None
    page = _parse_int(request.args.get('page')) or 1
    only_verifiable = request.args.get('only_verifiable', '').strip() in ('1', 'true', 'on')

    department_scope = _department_scope_for_session()

    # When the "only-mine-to-verify" filter is on, the SQL-level pagination
    # can't express the head-vs-employee rule (it's computed per-row in
    # Python after annotation). Fetch a larger page so the filter isn't
    # starved; the actual museum volume fits comfortably under this cap.
    per_page = 200 if only_verifiable else 25

    reports = timesheet_repository.list_reports(
        page=page,
        per_page=per_page,
        month=month,
        year=year,
        search=search,
        department=department_scope,
        scope=scope,
        current_year=current_year,
    )
    month_summary = timesheet_repository.get_month_summary(month=month, year=year)
    overall_summary = timesheet_repository.get_overall_summary()

    report_list = reports.get('reports', [])
    _annotate_reports_with_verify_flag(report_list)

    if only_verifiable:
        filtered = [r for r in report_list if r.get('can_verify')]
        reports['reports'] = filtered
        reports['filtered_total'] = len(filtered)
        reports['only_verifiable'] = True

    from timesheet_postgres import available_report_years
    return render_template(
        'admin_timesheet_reports.html',
        reports=reports,
        month_summary=month_summary,
        overall_summary=overall_summary,
        month=month,
        year=year,
        search=search or '',
        only_verifiable=only_verifiable,
        archived=archived,
        current_year=current_year,
        month_options=_month_options(),
        # Године за филтер се изводе из података (глобално, за админа/шефа) —
        # архивски увоз старих година одмах постаје доступан.
        available_years=available_report_years(),
        category_labels=timesheet_repository_cls.CATEGORY_LABELS,
        calendar=calendar,
    )


def _annotate_reports_with_verify_flag(report_list):
    """Set `report['can_verify']` for each row based on the session's rules.

    Runs one extra query per page to fetch the employee_email + department
    for the listed report ids and the current department-head mapping. Used
    so the template can disable the approve button when the current user
    shouldn't act on that report (e.g., director on a regular employee's
    report in a department that already has a head).
    """
    if not report_list:
        return
    if _session_is_admin(session):
        for report in report_list:
            report['can_verify'] = True
        return

    report_ids = [r['id'] for r in report_list if r.get('id') is not None]
    if not report_ids:
        for report in report_list:
            report['can_verify'] = False
        return

    with get_postgres_connection(row_factory=dict_row) as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT tr.id,
                       tr.employee_email,
                       ep.department AS employee_department
                FROM timesheet_reports tr
                LEFT JOIN employee_profiles ep ON LOWER(ep.email) = LOWER(tr.employee_email)
                WHERE tr.id = ANY(%s)
                """,
                (report_ids,),
            )
            meta_by_id = {row['id']: row for row in cur.fetchall()}
            heads = _get_department_heads(cur)

    for report in report_list:
        meta = meta_by_id.get(report.get('id'), {})
        # Двостепено: дугме „Одобри" се приказује сваком ко сме да ПОТПИШЕ листу
        # (шеф ИЛИ директор). Раније је коришћена стара верификациона политика
        # која је блокирала директора за регуларне запослене → директор није
        # видео дугме ни у једном одељењу.
        report['can_verify'] = can_user_sign_report_for_department(
            session,
            meta.get('employee_department'),
            target_employee_email=meta.get('employee_email'),
            department_heads=heads,
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

    report_month = int(report['header'].get('month', 1))
    month_name = (
        SERBIAN_MONTHS[report_month - 1]
        if 1 <= report_month <= 12
        else str(report_month)
    )

    can_verify = True
    if not _session_is_admin(session):
        with get_postgres_connection(row_factory=dict_row) as conn:
            with conn.cursor() as cur:
                report_department, employee_email = _lookup_report_department(cur, report_id)
                heads = _get_department_heads(cur)
        if not can_user_view_report_for_department(session, report_department):
            flash('Немате дозволу да прегледате овај извештај.', 'danger')
            return redirect(url_for('admin_timesheet_reports'))
        can_verify = can_user_sign_report_for_department(
            session, report_department,
            target_employee_email=employee_email,
            department_heads=heads,
        )

    return render_template(
        'admin_timesheet_report_detail.html',
        report=report,
        category_labels=timesheet_repository_cls.CATEGORY_LABELS,
        month_name=month_name,
        can_verify=can_verify,
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
                    LEFT JOIN employee_profiles ep ON LOWER(r.employee_email) = LOWER(ep.email)
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
                    LEFT JOIN employee_profiles ep ON LOWER(r.employee_email) = LOWER(ep.email)
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
                            COALESCE(d.work_in_museum, 0) + COALESCE(d.work_outside, 0) +
                            COALESCE(d.vacation, 0) + COALESCE(d.public_holiday, 0) +
                            COALESCE(d.paid_leave, 0) + COALESCE(d.other_leave, 0) +
                            COALESCE(d.sick_leave_lt30, 0) + COALESCE(d.sick_leave_gte30, 0)
                        ), 0) as total_hours,
                        COALESCE(SUM(d.work_in_museum), 0) as work_in_museum,
                        COALESCE(SUM(d.work_outside), 0) as work_outside,
                        COALESCE(SUM(
                            COALESCE(d.vacation, 0) + COALESCE(d.public_holiday, 0) +
                            COALESCE(d.paid_leave, 0) + COALESCE(d.other_leave, 0) +
                            COALESCE(d.sick_leave_lt30, 0) + COALESCE(d.sick_leave_gte30, 0)
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
                            COALESCE(d.work_in_museum, 0) + COALESCE(d.work_outside, 0) +
                            COALESCE(d.vacation, 0) + COALESCE(d.public_holiday, 0) +
                            COALESCE(d.paid_leave, 0) + COALESCE(d.other_leave, 0) +
                            COALESCE(d.sick_leave_lt30, 0) + COALESCE(d.sick_leave_gte30, 0)
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

        if not _session_is_admin(session):
            with get_postgres_connection(row_factory=dict_row) as conn:
                with conn.cursor() as cur:
                    report_department, _ = _lookup_report_department(cur, report_id)
            # Reading (not verifying) is permitted for directors cross-dept
            # and for dept heads scoped to their own dept.
            if not can_user_view_report_for_department(session, report_department):
                return _forbidden_json()

        return jsonify({'success': True, 'report': report})
    except Exception as exc:
        return jsonify({'success': False, 'message': f'Грешка: {str(exc)}'})


def api_admin_approve_timesheet_report(report_id, timesheet_repository=None):
    """Approve or disapprove a timesheet report.

    The endpoint talks to PostgreSQL directly; the injected repository is
    only used as an availability hint, so callers may omit it.
    """
    try:
        if timesheet_repository is not None and not _timesheet_repository_available(
            timesheet_repository
        ):
            return jsonify({'success': False, 'message': 'База података није доступна'})

        data = request.get_json() or {}
        approve = data.get('approve', True)
        admin_email = session.get('user_email', 'Unknown Admin')

        with get_postgres_connection(row_factory=dict_row) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT tr.id, tr.employee_name, tr.month, tr.year,
                           COALESCE(tr.status, 'DRAFT') AS status,
                           tr.employee_email,
                           ep.department AS employee_department
                    FROM timesheet_reports tr
                    LEFT JOIN employee_profiles ep ON LOWER(ep.email) = LOWER(tr.employee_email)
                    WHERE tr.id = %s
                    """,
                    (report_id,),
                )
                report = cur.fetchone()
                if not report:
                    return jsonify({'success': False, 'message': 'Извештај није пронађен'})

                report_status = report.get('status') or 'SUBMITTED'
                if approve and report_status != 'SUBMITTED':
                    return jsonify({
                        'success': False,
                        'message': 'Само поднете радне листе могу бити одобрене.'
                    }), 400
                if not approve and report_status != 'APPROVED':
                    return jsonify({
                        'success': False,
                        'message': 'Повући верификацију можете само за одобрене извештаје.'
                    }), 400

                heads = _get_department_heads(cur)

                month_name = (
                    SERBIAN_MONTHS_LOWER[report['month'] - 1]
                    if 1 <= report['month'] <= 12
                    else str(report['month'])
                )
                employee_email = report.get('employee_email')

                if approve:
                    # Двостепено одобрење: одреди слот потписа (шеф/директор) и
                    # забележи га. Листа постаје APPROVED тек кад су оба потписа
                    # присутна (осим изузетака — види _signature_plan).
                    plan = _signature_plan(
                        session,
                        report.get('employee_department'),
                        employee_email,
                        heads,
                    )
                    if not plan['allowed']:
                        return _forbidden_json()

                    from timesheet_postgres import confirm_timesheet_signature
                    sig = confirm_timesheet_signature(
                        report_id, admin_email, plan['slot'], plan['head_required'],
                        administrative=plan.get('administrative', False),
                    )
                    if not sig.success:
                        return jsonify(
                            {'success': False, 'message': sig.error.message}
                        ), 400

                    approved_now = bool(sig.data.get('approved'))
                    administrative = bool(sig.data.get('administrative'))
                    if approved_now:
                        if administrative:
                            message = ('Извештај је одобрен АДМИНИСТРАТИВНО '
                                       '(ван двостепеног ланца) и закључан.')
                            notif_msg = (f"Ваша радна листа за {month_name} "
                                         f"{report['year']}. је одобрена административно.")
                        else:
                            message = 'Извештај је одобрен и закључан (оба потписа присутна).'
                            notif_msg = (f"Ваша радна листа за {month_name} "
                                         f"{report['year']}. је одобрена (шеф и директор).")
                        if employee_email:
                            cur.execute(
                                """
                                INSERT INTO user_notifications (user_email, title, message, icon, type)
                                VALUES (%s, %s, %s, 'bi-check-circle', 'success')
                                """,
                                (
                                    employee_email,
                                    'Радна листа одобрена',
                                    notif_msg,
                                ),
                            )
                    else:
                        message = ('Потпис забележен. Радна листа чека још један '
                                   'потпис пре коначног одобрења.')
                        if employee_email:
                            cur.execute(
                                """
                                INSERT INTO user_notifications (user_email, title, message, icon, type)
                                VALUES (%s, %s, %s, 'bi-hourglass-split', 'info')
                                """,
                                (
                                    employee_email,
                                    'Радна листа — потпис забележен',
                                    f"Ваша радна листа за {month_name} {report['year']}. има један потпис и чека још један.",
                                ),
                            )
                    conn.commit()
                    return jsonify({'success': True, 'message': message,
                                    'approved': approved_now})
                else:
                    if not can_user_sign_report_for_department(
                        session,
                        report.get('employee_department'),
                        target_employee_email=employee_email,
                        department_heads=heads,
                    ):
                        return _forbidden_json()
                    # The report returns to SUBMITTED, which the save path
                    # hard-blocks — so no edit window is opened and the
                    # report stays locked awaiting re-verification.
                    cur.execute(
                        """
                        UPDATE timesheet_reports
                        SET is_verified = FALSE,
                            verified_by = NULL,
                            verified_at = NULL,
                            verified_role = NULL,
                            head_verified_by = NULL,
                            head_verified_at = NULL,
                            director_verified_by = NULL,
                            director_verified_at = NULL,
                            is_locked = TRUE,
                            status = 'SUBMITTED',
                            reviewed_at = NULL,
                            reviewed_by_email = NULL,
                            editable_until = NULL
                        WHERE id = %s
                        """,
                        (report_id,),
                    )
                    cur.execute(
                        """
                        INSERT INTO timesheet_status_history
                        (report_id, old_status, new_status, changed_by, note)
                        VALUES (%s, 'APPROVED', 'SUBMITTED', %s, 'Верификација повучена')
                        """,
                        (report_id, admin_email),
                    )
                    message = 'Верификација извештаја је повучена. Извештај је враћен у статус „поднет“ и чека поновну верификацију.'

                    if employee_email:
                        cur.execute(
                            """
                            INSERT INTO user_notifications (user_email, title, message, icon, type)
                            VALUES (%s, %s, %s, 'bi-arrow-counterclockwise', 'warning')
                            """,
                            (
                                employee_email,
                                'Верификација повучена',
                                f"Верификација ваше радне листе за {month_name} {report['year']}. је повучена. "
                                f"Извештај је враћен у статус „поднет“ и чека поновну верификацију.",
                            ),
                        )

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
            report_ids = list(dict.fromkeys(int(report_id) for report_id in report_ids))
        except (ValueError, TypeError):
            return jsonify({'success': False, 'message': 'Неисправни ID-ови извештаја'}), 400

        admin_email = session.get('user_email', 'Unknown Admin')

        with get_postgres_connection(row_factory=dict_row) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT tr.id, tr.employee_name, tr.month, tr.year,
                           COALESCE(tr.status, 'DRAFT') AS status,
                           tr.employee_email,
                           ep.department AS employee_department
                    FROM timesheet_reports tr
                    LEFT JOIN employee_profiles ep ON LOWER(ep.email) = LOWER(tr.employee_email)
                    WHERE tr.id = ANY(%s)
                    """,
                    (report_ids,),
                )
                existing_reports = cur.fetchall()
                required_status = 'SUBMITTED' if approve else 'APPROVED'
                existing_reports = [
                    row for row in existing_reports
                    if (row.get('status') or 'SUBMITTED') == required_status
                ]
                heads = _get_department_heads(cur)

                def _month_name(report):
                    return (
                        SERBIAN_MONTHS_LOWER[report['month'] - 1]
                        if 1 <= report['month'] <= 12
                        else str(report['month'])
                    )

                if approve:
                    # Двостепено одобрење: свака листа иде кроз исти пут као
                    # појединачно одобрење (потпис по слоту, APPROVED тек кад су
                    # оба потписа присутна). confirm ради у сопственој трансакцији.
                    from timesheet_postgres import confirm_timesheet_signature
                    approved_ids, partial_ids = [], []
                    for report in existing_reports:
                        plan = _signature_plan(
                            session, report.get('employee_department'),
                            report.get('employee_email'), heads,
                        )
                        if not plan['allowed']:
                            continue
                        sig = confirm_timesheet_signature(
                            report['id'], admin_email, plan['slot'], plan['head_required'],
                            administrative=plan.get('administrative', False),
                        )
                        if not sig.success:
                            continue
                        fully = bool(sig.data.get('approved'))
                        (approved_ids if fully else partial_ids).append(report['id'])
                        employee_email = report.get('employee_email')
                        if employee_email:
                            if fully:
                                cur.execute(
                                    """
                                    INSERT INTO user_notifications (user_email, title, message, icon, type)
                                    VALUES (%s, %s, %s, 'bi-check-circle', 'success')
                                    """,
                                    (employee_email, 'Радна листа одобрена',
                                     f"Ваша радна листа за {_month_name(report)} {report['year']}. је одобрена (шеф и директор)."),
                                )
                            else:
                                cur.execute(
                                    """
                                    INSERT INTO user_notifications (user_email, title, message, icon, type)
                                    VALUES (%s, %s, %s, 'bi-hourglass-split', 'info')
                                    """,
                                    (employee_email, 'Радна листа — потпис забележен',
                                     f"Ваша радна листа за {_month_name(report)} {report['year']}. има један потпис и чека још један."),
                                )
                    conn.commit()
                    processed_count = len(approved_ids) + len(partial_ids)
                    skipped_count = len(report_ids) - processed_count
                    message = (f'Обрађено {processed_count}: одобрено {len(approved_ids)}, '
                               f'чека други потпис {len(partial_ids)}')
                    if skipped_count > 0:
                        message += f' (прескочено: {skipped_count})'
                    return jsonify({
                        'success': True, 'message': message,
                        'processed': processed_count, 'approved': len(approved_ids),
                        'skipped': skipped_count,
                    })

                # Повлачење верификације (групно) — само за оне које корисник сме.
                if not _session_is_admin(session):
                    existing_reports = [
                        row for row in existing_reports
                        if can_user_sign_report_for_department(
                            session, row.get('employee_department'),
                            target_employee_email=row.get('employee_email'),
                            department_heads=heads,
                        )
                    ]
                existing_ids = {row['id'] for row in existing_reports}
                if not existing_ids:
                    return jsonify(
                        {'success': False, 'message': 'Ниједан од изабраних извештаја није пронађен'}
                    )
                cur.execute(
                    """
                    UPDATE timesheet_reports
                    SET is_verified = FALSE,
                        verified_by = NULL,
                        verified_at = NULL,
                        verified_role = NULL,
                        head_verified_by = NULL,
                        head_verified_at = NULL,
                        director_verified_by = NULL,
                        director_verified_at = NULL,
                        is_locked = TRUE,
                        status = 'SUBMITTED',
                        reviewed_at = NULL,
                        reviewed_by_email = NULL,
                        editable_until = NULL
                    WHERE id = ANY(%s)
                    """,
                    (list(existing_ids),),
                )
                cur.executemany(
                    """
                    INSERT INTO timesheet_status_history
                    (report_id, old_status, new_status, changed_by, note)
                    VALUES (%s, 'APPROVED', 'SUBMITTED', %s, 'Верификација повучена (групно)')
                    """,
                    [(rid, admin_email) for rid in existing_ids],
                )
                for report in existing_reports:
                    employee_email = report.get('employee_email')
                    if employee_email:
                        cur.execute(
                            """
                            INSERT INTO user_notifications (user_email, title, message, icon, type)
                            VALUES (%s, %s, %s, 'bi-arrow-counterclockwise', 'warning')
                            """,
                            (employee_email, 'Верификација повучена',
                             f"Верификација ваше радне листе за {_month_name(report)} {report['year']}. је повучена. "
                             f"Извештај чека поновну верификацију."),
                        )
                conn.commit()

        processed_count = len(existing_ids)
        skipped_count = len(report_ids) - processed_count
        message = f'Верификација повучена: {processed_count} извештај(а)'
        if skipped_count > 0:
            message += f' (прескочено: {skipped_count})'
        return jsonify({
            'success': True, 'message': message,
            'processed': processed_count, 'skipped': skipped_count,
        })
    except Exception as exc:
        return jsonify({'success': False, 'message': f'Грешка: {str(exc)}'})


def api_admin_export_timesheet_report(report_id, timesheet_repository):
    """Export a timesheet report to a Word document."""
    try:
        if not _timesheet_repository_available(timesheet_repository):
            flash('База података није доступна', 'error')
            return redirect(url_for('admin_timesheet_reports'))

        if not _session_is_admin(session):
            with get_postgres_connection(row_factory=dict_row) as conn:
                with conn.cursor() as cur:
                    report_department, _ = _lookup_report_department(cur, report_id)
            if not can_user_view_report_for_department(session, report_department):
                flash('Немате дозволу за извоз овог извештаја.', 'danger')
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

        audit_support.record_audit(
            action=audit_support.ACTION_DELETE,
            entity_type='timesheet_report',
            entity_id=report_id,
            summary=(
                f'Обрисан радни лист #{report_id} — {report.get("employee_name")} '
                f'{report.get("month")}/{report.get("year")} '
                f'({days_deleted} дана, {entries_deleted} уноса)'
            ),
            old_values=dict(report) if isinstance(report, dict) else None,
        )
        return jsonify(
            {
                'success': True,
                'message': f'Извештај је обрисан ({days_deleted} дана, {entries_deleted} уноса)',
            }
        )
    except Exception as exc:
        return jsonify({'success': False, 'message': f'Грешка: {str(exc)}'})


# ---------------------------------------------------------------------------
# Откључавање уноса радне листе (админ/директор) — по кориснику/месецу/периоду
# Замена за уклоњени механизам „захтева за унос": админ директно откључава.
# ---------------------------------------------------------------------------
def render_admin_unlock_entry():
    """Страница: админ бира запосленог и откључава му унос за месец или период."""
    from datetime import datetime

    employees = []
    try:
        with get_postgres_connection(row_factory=dict_row) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT email, full_name FROM users "
                    "WHERE is_active AND full_name IS NOT NULL AND email IS NOT NULL "
                    "ORDER BY full_name"
                )
                employees = cur.fetchall()
    except Exception as exc:
        logger.error("Unlock page: employee load failed: %s", exc)

    now = datetime.now()
    return render_template(
        'admin_timesheet_otkljucaj.html',
        employees=employees,
        months=list(enumerate(SERBIAN_MONTHS, start=1)),
        years=list(range(now.year, now.year - 5, -1)),
        current_month=now.month,
        current_year=now.year,
    )


def handle_admin_unlock_entry():
    """POST (JSON): откључава унос за изабраног запосленог — један месец или
    период [од..до]. Само admin/direktor (гарантује декоратор руте). Свако
    откључавање се уписује у audit траг."""
    from timesheet_postgres import admin_unlock_entry

    data = request.get_json(silent=True) or request.form
    employee_email = (data.get('employee_email') or '').strip()
    admin_email = session.get('user_email', '')

    def _int(value):
        try:
            return int(value)
        except (TypeError, ValueError):
            return None

    from_month = _int(data.get('from_month') or data.get('month'))
    from_year = _int(data.get('from_year') or data.get('year'))
    to_month = _int(data.get('to_month')) or from_month
    to_year = _int(data.get('to_year')) or from_year
    expires = (data.get('expires') or '').strip()

    if not employee_email or not from_month or not from_year:
        return jsonify({'success': False,
                        'message': 'Изаберите запосленог, месец и годину.'}), 400
    if not (1 <= from_month <= 12) or not (1 <= to_month <= 12):
        return jsonify({'success': False, 'message': 'Неисправан месец.'}), 400

    start_idx = from_year * 12 + (from_month - 1)
    end_idx = to_year * 12 + (to_month - 1)
    if end_idx < start_idx:
        return jsonify({'success': False,
                        'message': 'Крај периода је пре почетка.'}), 400
    if end_idx - start_idx > 24:
        return jsonify({'success': False,
                        'message': 'Период је предугачак (макс. 24 месеца).'}), 400

    expires_at = (expires + ' 23:59:59') if expires else None

    unlocked, errors = [], []
    for idx in range(start_idx, end_idx + 1):
        year, month = idx // 12, idx % 12 + 1
        result = admin_unlock_entry(employee_email, month, year, admin_email, expires_at)
        if result.success:
            editable_until = result.data.get('editable_until')
            unlocked.append({'month': month, 'year': year,
                             'editable_until': str(editable_until)})
            audit_support.record_audit(
                action='TIMESHEET_UNLOCK',
                entity_type='timesheet_report',
                entity_id=result.data.get('report_id'),
                summary=(f'Откључан унос радне листе {month}/{year} за '
                         f'{employee_email} до {editable_until}'),
                new_values={'employee_email': employee_email, 'month': month,
                            'year': year, 'editable_until': str(editable_until)},
                changed_by=admin_email,
            )
        else:
            errors.append({'month': month, 'year': year,
                           'message': result.error.message if result.error else 'грешка'})

    ok = len(unlocked) > 0
    message = f'Откључан унос: {len(unlocked)} месец(и) за {employee_email}.'
    if errors:
        message += f' Прескочено: {len(errors)}.'
    return jsonify({'success': ok, 'message': message,
                    'unlocked': unlocked, 'errors': errors}), (200 if ok else 400)
