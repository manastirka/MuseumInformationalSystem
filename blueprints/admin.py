"""Admin and access-management routes extracted from app.py."""

from flask import Blueprint, redirect, render_template, request, url_for

import admin_system_views
import admin_user_management_views
import audit_log_views
import collection_statistics_views
import core_app_views
import employee_admin_views
from security_utils import (
    admin_only,
    admin_or_director_required,
    admin_required,
    login_required,
    module_access_required,
)


admin_bp = Blueprint('admin', __name__)


@admin_bp.route('/admin')
@admin_or_director_required
def admin_panel():
    """Admin panel. Director sees a trimmed view (technical cards hidden via template)."""
    return core_app_views.render_admin_panel()


@admin_bp.route('/admin/sistem')
@admin_or_director_required
def admin_system_hub():
    """Обједињена системска страница са табовима: Подешавања / Пошта / Извештаји /
    Ревизиони траг. Сваки таб је iframe ка постојећој рути са ?embedded=1, која
    задржава СВОЈУ проверу приступа (права се не мењају). Шаблон приказује таб само
    ако корисник сме да га види (is_admin/is_director)."""
    return render_template('admin_sistem.html')


@admin_bp.route('/admin/system-settings')
@admin_only
def admin_system_settings():
    """System settings page. Standalone URL redirects to the unified hub tab;
    ?embedded=1 renders the content bare for the hub iframe (bookmarks keep working)."""
    if not request.args.get('embedded'):
        return redirect(url_for('admin.admin_system_hub') + '#podesavanja')
    return admin_system_views.render_admin_system_settings()


@admin_bp.route('/admin/audit-log')
@admin_or_director_required
def admin_audit_log():
    """Global audit trail viewer ('ko je ovo obrisao/promenio?'). Standalone URL
    redirects to the hub tab; ?embedded=1 renders bare content for the iframe."""
    if not request.args.get('embedded'):
        return redirect(url_for('admin.admin_system_hub') + '#revizija')
    return audit_log_views.render_audit_log()


@admin_bp.route('/api/admin/settings/general', methods=['POST'])
@admin_only
def api_save_general_settings():
    """Save general settings."""
    return admin_system_views.api_save_general_settings()


@admin_bp.route('/api/admin/settings/security', methods=['POST'])
@admin_only
def api_save_security_settings():
    """Save security settings."""
    return admin_system_views.api_save_security_settings()


@admin_bp.route('/api/admin/database/backup', methods=['POST'])
@admin_only
def api_database_backup():
    """Create database backup."""
    return admin_system_views.api_database_backup()


@admin_bp.route('/api/admin/database/table-stats')
@admin_only
def api_table_stats():
    """Get table statistics."""
    return admin_system_views.api_table_stats()


@admin_bp.route('/api/admin/database/vacuum', methods=['POST'])
@admin_only
def api_vacuum_database():
    """Run VACUUM ANALYZE on database."""
    return admin_system_views.api_vacuum_database()


@admin_bp.route('/api/admin/logs')
@admin_only
def api_get_logs():
    """Get system logs."""
    return admin_system_views.api_get_logs()


@admin_bp.route('/api/admin/logs/download')
@admin_only
def api_download_logs():
    """Download log file."""
    return admin_system_views.api_download_logs()


@admin_bp.route('/api/admin/cache/clear', methods=['POST'])
@admin_only
def api_clear_cache():
    """Clear system cache."""
    return admin_system_views.api_clear_cache()


@admin_bp.route('/admin/statistics')
@admin_or_director_required
def admin_statistics():
    """Collection statistics dashboard."""
    import app as museum_app

    return collection_statistics_views.render_admin_statistics(
        get_mineral_database=museum_app.get_mineral_database,
        get_meteorite_collection_database=museum_app.get_meteorite_collection_database,
        botany_collection_database=museum_app.BOTANY_COLLECTION_DATABASE,
        paleozoology_collection_database=museum_app.PALEOZOOLOGY_COLLECTION_DATABASE,
        paleobotany_collection_database=museum_app.PALEOBOTANY_COLLECTION_DATABASE,
        petrology_collection_database=museum_app.PETROLOGY_COLLECTION_DATABASE,
        get_cultural_heritage_database=museum_app.get_cultural_heritage_database,
        get_image_storage=museum_app.get_image_storage,
    )


@admin_bp.route('/admin/manage_access')
@admin_or_director_required
def manage_user_access():
    """Manage user module access."""
    import app as museum_app

    return admin_user_management_views.render_manage_user_access(
        load_module_access=museum_app.load_module_access,
        user_has_module_access=museum_app.user_has_module_access,
        module_access=museum_app.MODULE_ACCESS,
        get_museum_employees=museum_app.get_museum_employees,
    )


@admin_bp.route('/admin/grant_access', methods=['POST'])
@admin_required
def grant_module_access():
    """Grant module access to a user."""
    import app as museum_app

    return admin_user_management_views.grant_module_access(
        load_module_access=museum_app.load_module_access,
        save_module_access=museum_app.save_module_access,
        module_access=museum_app.MODULE_ACCESS,
    )


@admin_bp.route('/admin/revoke_access', methods=['POST'])
@admin_required
def revoke_module_access():
    """Revoke module access from a user."""
    import app as museum_app

    return admin_user_management_views.revoke_module_access(
        load_module_access=museum_app.load_module_access,
        save_module_access=museum_app.save_module_access,
        module_access=museum_app.MODULE_ACCESS,
    )


@admin_bp.route('/admin/password_manager')
@admin_only
def admin_password_manager():
    """Password manager for all users."""
    return admin_user_management_views.render_admin_password_manager()


@admin_bp.route('/admin/mail-settings')
@admin_only
def admin_mail_configuration():
    """Centralized mail configuration. Standalone URL redirects to the unified hub
    tab; ?embedded=1 renders bare content for the iframe (bookmarks keep working)."""
    if not request.args.get('embedded'):
        return redirect(url_for('admin.admin_system_hub') + '#posta')
    return admin_user_management_views.render_admin_mail_configuration()


@admin_bp.route('/api/admin/password_manager/users')
@admin_only
def api_password_manager_users():
    """Get all users for password manager."""
    return admin_user_management_views.api_password_manager_users()


@admin_bp.route('/api/admin/mail-settings/state')
@admin_only
def api_admin_mail_settings_state():
    """Return admin mail configuration state."""
    return admin_user_management_views.api_admin_mail_settings_state()


@admin_bp.route('/api/admin/mail-settings', methods=['POST'])
@admin_only
def api_admin_mail_settings_save():
    """Save mail settings for a selected user account."""
    return admin_user_management_views.api_admin_mail_settings_save()


@admin_bp.route('/api/admin/mail-settings/test', methods=['POST'])
@admin_only
def api_admin_mail_test_connection():
    """Test mail connectivity for a selected user account."""
    return admin_user_management_views.api_admin_mail_test_connection()


@admin_bp.route('/api/admin/password_manager/reset', methods=['POST'])
@admin_only
def api_password_manager_reset():
    """Reset user password."""
    import app as museum_app

    return admin_user_management_views.api_password_manager_reset(
        password_validator=museum_app.password_validator,
        password_hasher=museum_app.password_hasher,
        log_security_event=museum_app.log_security_event,
    )


@admin_bp.route('/api/admin/password_manager/force_change', methods=['POST'])
@admin_only
def api_password_manager_force_change():
    """Force user to change password on next login."""
    import app as museum_app

    return admin_user_management_views.api_password_manager_force_change(
        log_security_event=museum_app.log_security_event,
    )


@admin_bp.route('/api/admin/password_manager/toggle_status', methods=['POST'])
@admin_only
def api_password_manager_toggle_status():
    """Activate or deactivate user."""
    import app as museum_app

    return admin_user_management_views.api_password_manager_toggle_status(
        log_security_event=museum_app.log_security_event,
    )


@admin_bp.route('/api/admin/password_manager/generate')
@admin_only
def api_password_manager_generate():
    """Generate a strong random password."""
    import app as museum_app

    return admin_user_management_views.api_password_manager_generate(
        password_validator=museum_app.password_validator,
    )


@admin_bp.route('/admin/employees_database')
@module_access_required('employees_database')
def employees_database():
    """View all employee databases and information."""
    import app as museum_app

    return employee_admin_views.render_employees_database(
        get_employee_directory=museum_app.get_employee_directory,
    )


@admin_bp.route('/admin/employee_profiles_database')
@module_access_required('employee_profiles')
def employee_profiles_database():
    """Employee profiles database with detailed biographical information."""
    import app as museum_app

    return employee_admin_views.render_employee_profiles_database(
        get_employee_directory=museum_app.get_employee_directory,
    )


@admin_bp.route('/admin/add_user', methods=['GET', 'POST'])
@admin_required
def add_user():
    """Add new user to the system."""
    import app as museum_app

    return employee_admin_views.handle_add_user(
        get_museum_employees=museum_app.get_museum_employees,
        get_employee_directory=museum_app.get_employee_directory,
        password_hasher=museum_app.password_hasher,
        password_validator=museum_app.password_validator,
    )


@admin_bp.route('/dashboard/customize', methods=['GET', 'POST'])
@login_required
def customize_dashboard():
    """Customize dashboard widget preferences."""
    import app as museum_app

    return admin_user_management_views.customize_dashboard_preferences(
        load_dashboard_preferences=museum_app.load_dashboard_preferences,
        load_module_access=museum_app.load_module_access,
        user_has_module_access=museum_app.user_has_module_access,
        load_saved_elements=museum_app.load_user_dashboard_elements,
        save_user_elements=museum_app.save_user_dashboard_elements,
        dashboard_endpoint='dashboard',
    )
