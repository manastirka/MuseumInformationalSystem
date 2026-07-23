"""Timesheet and notification routes extracted from app.py."""

from flask import Blueprint, redirect, session, url_for

import notification_views
import timesheet_admin_views
import timesheet_employee_views
import timesheet_uvoz_views
from security_utils import admin_or_department_head_required, admin_required, login_required
from timesheet_repository import TimesheetRepository


timesheet_bp = Blueprint('timesheet', __name__)


@timesheet_bp.route('/timesheet')
@login_required
def timesheet_app():
    """Route to timesheet application."""
    import app as museum_app

    return timesheet_admin_views.render_timesheet_app(
        timesheet_repository=museum_app.timesheet_repository,
        timesheet_repository_cls=TimesheetRepository,
        user_has_module_access=museum_app.user_has_module_access,
    )


@timesheet_bp.route('/admin/timesheet')
@admin_required
def admin_timesheet_main():
    """Main timesheet administration page."""
    return timesheet_admin_views.render_admin_timesheet_main()


@timesheet_bp.route('/admin/timesheet_reports')
@admin_or_department_head_required
def admin_timesheet_reports():
    """Admin view for centralized timesheet reports."""
    import app as museum_app

    return timesheet_admin_views.render_admin_timesheet_reports(
        timesheet_repository=museum_app.timesheet_repository,
        timesheet_repository_cls=TimesheetRepository,
    )


@timesheet_bp.route('/admin/timesheet_reports/<int:report_id>')
@admin_or_department_head_required
def admin_timesheet_report_detail(report_id):
    """Detailed view of a single report."""
    import app as museum_app

    return timesheet_admin_views.render_admin_timesheet_report_detail(
        report_id=report_id,
        timesheet_repository=museum_app.timesheet_repository,
        timesheet_repository_cls=TimesheetRepository,
    )


@timesheet_bp.route('/admin/timesheet/employees')
@admin_required
def admin_timesheet_employees():
    """Admin view for managing employees in timesheet system."""
    import app as museum_app

    return timesheet_admin_views.render_admin_timesheet_employees(
        timesheet_repository=museum_app.timesheet_repository,
    )


@timesheet_bp.route('/admin/timesheet/users')
@admin_required
def admin_timesheet_users():
    """Admin view for managing timesheet system users."""
    import app as museum_app

    return timesheet_admin_views.render_admin_timesheet_users(
        timesheet_repository=museum_app.timesheet_repository,
    )


@timesheet_bp.route('/admin/timesheet/pending')
@admin_or_department_head_required
def admin_timesheet_pending():
    """Pending edit requests list.

    Admin + director + department heads are allowed (heads approve unlock
    requests for their own department, so they must see them). The per-role
    department scoping happens inside the view.
    """
    import app as museum_app

    return timesheet_admin_views.render_admin_timesheet_pending(
        timesheet_repository=museum_app.timesheet_repository,
    )


@timesheet_bp.route('/admin/timesheet/analytics')
@admin_required
def admin_timesheet_analytics():
    """Admin analytics dashboard for timesheet system."""
    import app as museum_app

    return timesheet_admin_views.render_admin_timesheet_analytics(
        timesheet_repository=museum_app.timesheet_repository,
    )


@timesheet_bp.route('/api/admin/timesheet/employee-analytics')
@admin_required
def api_admin_employee_analytics():
    """Get detailed analytics for a specific employee."""
    return timesheet_admin_views.api_admin_employee_analytics()


@timesheet_bp.route('/api/admin/timesheet/report/<int:report_id>')
@admin_or_department_head_required
def api_admin_get_timesheet_report(report_id):
    """Get single timesheet report details with daily entries."""
    import app as museum_app

    return timesheet_admin_views.api_admin_get_timesheet_report(
        report_id=report_id,
        timesheet_repository=museum_app.timesheet_repository,
    )


@timesheet_bp.route('/api/admin/timesheet/report/<int:report_id>/approve', methods=['POST'])
@admin_or_department_head_required
def api_admin_approve_timesheet_report(report_id):
    """Approve or disapprove a timesheet report."""
    import app as museum_app

    return timesheet_admin_views.api_admin_approve_timesheet_report(
        report_id=report_id,
        timesheet_repository=museum_app.timesheet_repository,
    )


@timesheet_bp.route('/api/admin/timesheet/reports/batch-approve', methods=['POST'])
@admin_or_department_head_required
def api_admin_batch_approve_timesheet_reports():
    """Batch approve or disapprove multiple timesheet reports."""
    import app as museum_app

    return timesheet_admin_views.api_admin_batch_approve_timesheet_reports(
        timesheet_repository=museum_app.timesheet_repository,
    )


@timesheet_bp.route('/api/admin/timesheet/export/<int:report_id>')
@admin_or_department_head_required
def api_admin_export_timesheet_report(report_id):
    """Export timesheet report to Word document."""
    import app as museum_app

    return timesheet_admin_views.api_admin_export_timesheet_report(
        report_id=report_id,
        timesheet_repository=museum_app.timesheet_repository,
    )


@timesheet_bp.route('/api/admin/timesheet/report/<int:report_id>', methods=['DELETE'])
@admin_required
def api_admin_delete_timesheet_report(report_id):
    """Delete a timesheet report and its entries."""
    import app as museum_app

    return timesheet_admin_views.api_admin_delete_timesheet_report(
        report_id=report_id,
        timesheet_repository=museum_app.timesheet_repository,
    )


@timesheet_bp.route('/admin/timesheet/pending/approve/<int:request_id>', methods=['POST'])
@admin_or_department_head_required
def admin_approve_edit_request(request_id):
    """Approve or reject an unlock/edit request.

    Admin + director + department heads are allowed. The per-request
    department scope is enforced inside the view (dept head only for their
    own department's requests; director for heads-less depts and heads).
    """
    import app as museum_app

    return timesheet_admin_views.admin_approve_edit_request(
        request_id=request_id,
        timesheet_repository=museum_app.timesheet_repository,
    )


@timesheet_bp.route('/api/notifications')
@login_required
def api_get_notifications():
    """Get notifications for the current user."""
    return notification_views.api_get_notifications()


@timesheet_bp.route('/api/notifications/read', methods=['POST'])
@login_required
def api_mark_notifications_read():
    """Mark notifications as read."""
    return notification_views.api_mark_notifications_read()


@timesheet_bp.route('/api/notifications/clear', methods=['POST'])
@login_required
def api_clear_notifications():
    """Clear all notifications for the current user."""
    return notification_views.api_clear_notifications()


@timesheet_bp.route('/timesheet/entry')
@login_required
def timesheet_entry():
    """Employee timesheet entry page."""
    if session.get('user_role') in ('admin', 'direktor'):
        return redirect(url_for('admin_timesheet_reports'))
    return timesheet_employee_views.render_timesheet_entry()


@timesheet_bp.route('/timesheet/view')
@login_required
def timesheet_view():
    """Read-only view of a saved/submitted report."""
    return timesheet_employee_views.render_timesheet_view()


# --- Увоз радних листа из Word-а (ИСКЉУЧИВО админ; обједињено у Администрацији) ---
@timesheet_bp.route('/admin/timesheet/uvoz')
@admin_required
def uvoz_radne():
    """Обједињена админ страница: појединачни + архивски увоз из Word-а."""
    return timesheet_uvoz_views.render_uvoz_hub()


@timesheet_bp.route('/timesheet/uvoz')
@admin_required
def uvoz_radne_legacy():
    """Стара путања појединачног увоза → обједињена админ страница."""
    return redirect(url_for('timesheet.uvoz_radne'))


@timesheet_bp.route('/timesheet/uvoz/pregled', methods=['POST'])
@admin_required
def uvoz_pregled():
    """Парсирај отпремљени .docx и прикажи преглед + избор запосленог."""
    return timesheet_uvoz_views.handle_uvoz_pregled()


@timesheet_bp.route('/timesheet/uvoz/potvrdi', methods=['POST'])
@admin_required
def uvoz_potvrdi():
    """Потврди појединачни увоз за изабраног запосленог (иде у ланац одобравања)."""
    return timesheet_uvoz_views.handle_uvoz_potvrdi()


# --- Архивски масовни увоз (иста обједињена админ страница) ---
@timesheet_bp.route('/admin/timesheet/uvoz-arhiva')
@admin_required
def uvoz_arhiva():
    """Стари улаз архивског увоза → обједињена админ страница."""
    return redirect(url_for('timesheet.uvoz_radne'))


@timesheet_bp.route('/admin/timesheet/uvoz-arhiva/pregled', methods=['POST'])
@admin_required
def uvoz_arhiva_pregled():
    """Dry-run извештај архивског увоза (поклапања/упозорења/одбијања)."""
    return timesheet_uvoz_views.handle_uvoz_arhiva_pregled()


@timesheet_bp.route('/admin/timesheet/uvoz-arhiva/potvrdi', methods=['POST'])
@admin_required
def uvoz_arhiva_potvrdi():
    """Потврди архивски увоз (уписује као одобрене)."""
    return timesheet_uvoz_views.handle_uvoz_arhiva_potvrdi()


@timesheet_bp.route('/api/timesheet/load')
@login_required
def api_load_timesheet():
    """Load timesheet data for the selected month/year."""
    return timesheet_employee_views.api_load_timesheet()


@timesheet_bp.route('/request_approval', methods=['POST'])
@login_required
def request_approval():
    """Request approval to edit a submitted report."""
    return timesheet_employee_views.request_approval()


@timesheet_bp.route('/api/timesheet/save', methods=['POST'])
@login_required
def api_save_timesheet():
    """Save a draft timesheet report."""
    return timesheet_employee_views.api_save_timesheet()


@timesheet_bp.route('/api/timesheet/<int:report_id>/submit', methods=['POST'])
@login_required
def api_timesheet_submit(report_id):
    """Submit a draft report for review."""
    return timesheet_employee_views.api_timesheet_submit(report_id)


@timesheet_bp.route('/api/timesheet/<int:report_id>/approve', methods=['POST'])
@admin_required
def api_timesheet_approve(report_id):
    """Approve a report via employee view API."""
    return timesheet_employee_views.api_timesheet_approve(report_id)


@timesheet_bp.route('/api/timesheet/<int:report_id>/reject', methods=['POST'])
@admin_or_department_head_required
def api_timesheet_reject(report_id):
    """Return a SUBMITTED report to the employee with a note explaining why.

    Admin + director + department heads are allowed. Per-report scope
    (dept head only for own dept; director for Edu/Gallery and heads) is
    enforced inside the view. The report gets a 24 h correction window.
    """
    return timesheet_employee_views.api_timesheet_reject(report_id)


@timesheet_bp.route('/api/timesheet/<int:report_id>/force-edit', methods=['POST'])
@admin_or_department_head_required
def api_timesheet_force_edit(report_id):
    """Return a report to the employee for re-entry.

    Admin always. Department heads only for reports in their own dept.
    Director for Edu/Gallery reports and dept heads' own reports. The
    per-report scope is enforced inside the view.
    """
    return timesheet_employee_views.api_timesheet_force_edit(report_id)


@timesheet_bp.route('/admin/timesheet/review')
@admin_required
def admin_timesheet_review():
    """Legacy admin timesheet review page."""
    return timesheet_employee_views.render_admin_timesheet_review()
