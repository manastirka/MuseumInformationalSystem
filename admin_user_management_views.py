"""Shared route implementations for access management and password manager views."""

import logging
from datetime import datetime

from flask import flash, jsonify, redirect, render_template, request, session, url_for
from psycopg.rows import dict_row

from postgres_service import get_postgres_connection

logger = logging.getLogger(__name__)


def render_manage_user_access(
    *,
    load_module_access,
    user_has_module_access,
    module_access,
    get_museum_employees,
):
    """Manage user module access."""
    load_module_access()
    users_with_access = []

    try:
        with get_postgres_connection(row_factory=dict_row) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT u.email, u.full_name, u.position,
                           COALESCE(d.name, 'Природњачки музеј') as department,
                           COALESCE(r.name, 'user') as role
                    FROM users u
                    LEFT JOIN departments d ON u.department_id = d.id
                    LEFT JOIN roles r ON u.role_id = r.id
                    WHERE u.is_active = TRUE
                    ORDER BY u.full_name
                    """
                )
                users = cur.fetchall()

        for user in users:
            if user['role'] == 'admin':
                continue
            user_modules = []
            for module_key in module_access.keys():
                if user_has_module_access(user['email'], user['role'], module_key):
                    user_modules.append({'key': module_key})
            users_with_access.append(
                {
                    'email': user['email'],
                    'name': user['full_name'],
                    'department': user['department'],
                    'position': user['position'],
                    'modules': user_modules,
                }
            )
    except Exception as exc:
        logger.error("Error loading users for access management: %s", exc)
        for email, user_data in get_museum_employees().items():
            if user_data.get('role') == 'admin':
                continue
            user_modules = []
            for module_key in module_access.keys():
                if user_has_module_access(email, user_data.get('role', 'user'), module_key):
                    user_modules.append({'key': module_key})
            users_with_access.append(
                {
                    'email': email,
                    'name': user_data.get('full_name', email),
                    'department': user_data.get('department', 'N/A'),
                    'modules': user_modules,
                }
            )

    return render_template(
        'admin_manage_access.html',
        users=users_with_access,
        all_modules=module_access,
        selected_user=request.args.get('selected_user', ''),
    )


def grant_module_access(*, load_module_access, save_module_access, module_access):
    """Grant module access to a user."""
    load_module_access()
    user_email = request.form.get('user_email')
    module_key = request.form.get('module_key')

    if not user_email or not module_key:
        flash('Недостају параметри за доделу приступа.', 'error')
        return redirect(url_for('manage_user_access'))
    if module_key not in module_access:
        flash('Непознат модул.', 'error')
        return redirect(url_for('manage_user_access'))

    module = module_access[module_key]
    module_name = module['name']
    changed = False

    if module.get('default_access', False):
        restricted_users = module.get('restricted_users', [])
        if user_email in restricted_users:
            restricted_users.remove(user_email)
            changed = True
            flash(f'Приступ модулу "{module_name}" је враћен кориснику.', 'success')
        else:
            flash('Корисник већ има приступ овом модулу (подразумевани приступ).', 'info')
    else:
        if user_email not in module.get('authorized_users', []):
            module.setdefault('authorized_users', []).append(user_email)
            changed = True
            flash(f'Приступ модулу "{module_name}" је дат кориснику.', 'success')
        else:
            flash('Корисник већ има приступ овом модулу.', 'info')

    if changed:
        save_module_access()

    return redirect(url_for('manage_user_access', selected_user=user_email))


def revoke_module_access(*, load_module_access, save_module_access, module_access):
    """Revoke module access from a user."""
    load_module_access()
    user_email = request.form.get('user_email')
    module_key = request.form.get('module_key')

    if not user_email or not module_key:
        flash('Недостају параметри за укидање приступа.', 'error')
        return redirect(url_for('manage_user_access'))
    if module_key not in module_access:
        flash('Непознат модул.', 'error')
        return redirect(url_for('manage_user_access'))

    module = module_access[module_key]
    module_name = module['name']
    changed = False

    if module.get('default_access', False):
        module.setdefault('restricted_users', [])
        if user_email not in module['restricted_users']:
            module['restricted_users'].append(user_email)
            changed = True
            flash(f'Приступ модулу "{module_name}" је укинут кориснику.', 'success')
        else:
            flash('Корисник већ нема приступ овом модулу.', 'info')
    else:
        authorized_users = module.get('authorized_users', [])
        if user_email in authorized_users:
            authorized_users.remove(user_email)
            changed = True
            flash(f'Приступ модулу "{module_name}" је укинут кориснику.', 'success')
        else:
            flash('Корисник није имао приступ овом модулу.', 'info')

    if changed:
        save_module_access()

    return redirect(url_for('manage_user_access', selected_user=user_email))


def customize_dashboard_preferences(
    *,
    load_dashboard_preferences,
    save_dashboard_preferences,
    dashboard_preferences,
    module_access,
    user_has_module_access,
    dashboard_endpoint,
):
    """Customize dashboard widget preferences for the current user."""
    load_dashboard_preferences()

    user_email = session.get('user_email')
    user_role = session.get('user_role')

    if request.method == 'POST':
        selected_widgets = request.form.getlist('widgets')

        if user_email not in dashboard_preferences:
            dashboard_preferences[user_email] = {}

        dashboard_preferences[user_email]['enabled_widgets'] = selected_widgets

        if save_dashboard_preferences():
            flash('Подешавања видгета успешно сачувана!', 'success')
        else:
            flash('Грешка при чувању подешавања!', 'error')

        return redirect(url_for(dashboard_endpoint))

    available_modules = []
    for module_key, module_info in module_access.items():
        if user_has_module_access(user_email, user_role, module_key):
            available_modules.append(
                {
                    'key': module_key,
                    'name': module_info['name'],
                    'description': module_info['description'],
                    'icon': module_info['icon'],
                }
            )

    current_prefs = dashboard_preferences.get(user_email, {}).get(
        'enabled_widgets',
        list(module_access.keys()),
    )

    return render_template(
        'customize_dashboard.html',
        available_modules=available_modules,
        enabled_widgets=current_prefs,
    )


def render_admin_password_manager():
    """Password manager for all users."""
    return render_template('admin_password_manager.html')


def api_password_manager_users():
    """Get all users for password manager."""
    try:
        with get_postgres_connection(row_factory=dict_row) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT
                        u.id,
                        u.email,
                        u.full_name,
                        u.position,
                        u.is_active,
                        u.is_first_login,
                        u.last_login_at,
                        u.created_at,
                        COALESCE(r.name, 'employee') as role,
                        COALESCE(d.name, 'Природњачки музеј') as department
                    FROM users u
                    LEFT JOIN roles r ON u.role_id = r.id
                    LEFT JOIN departments d ON u.department_id = d.id
                    ORDER BY u.full_name
                    """
                )
                users = [dict(row) for row in cur.fetchall()]

        for user in users:
            if user.get('last_login_at'):
                user['last_login_at'] = user['last_login_at'].isoformat()
            if user.get('created_at'):
                user['created_at'] = user['created_at'].isoformat()

        return jsonify({'success': True, 'users': users})
    except Exception as exc:
        logger.error("Error loading users for password manager: %s", exc)
        return jsonify({'success': False, 'message': str(exc)}), 500


def api_password_manager_reset(*, password_validator, password_hasher, log_security_event):
    """Reset user password."""
    data = request.get_json() or {}
    email = data.get('email')
    new_password = data.get('new_password')
    force_change = data.get('force_change', True)

    if not email or not new_password:
        return jsonify({'success': False, 'message': 'Недостају параметри'}), 400

    is_valid, errors = password_validator.validate(new_password)
    if not is_valid:
        return jsonify({'success': False, 'message': ', '.join(errors)}), 400

    try:
        password_hash, salt = password_hasher.hash_password(new_password)
        with get_postgres_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    UPDATE users
                    SET password_hash = %s,
                        salt = %s,
                        is_first_login = %s,
                        updated_at = %s
                    WHERE LOWER(email) = LOWER(%s)
                    """,
                    (password_hash, salt, force_change, datetime.now(), email),
                )
                conn.commit()

        log_security_event(
            'password_reset_by_admin',
            {
                'admin_email': session.get('user_email'),
                'target_email': email,
                'force_change': force_change,
            },
        )
        logger.info("Password reset by admin for user: %s", email)
        return jsonify({'success': True, 'message': 'Лозинка је ресетована'})
    except Exception as exc:
        logger.error("Error resetting password: %s", exc)
        return jsonify({'success': False, 'message': str(exc)}), 500


def api_password_manager_force_change(*, log_security_event):
    """Force user to change password on next login."""
    data = request.get_json() or {}
    email = data.get('email')
    if not email:
        return jsonify({'success': False, 'message': 'Недостају параметри'}), 400

    try:
        with get_postgres_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    UPDATE users
                    SET is_first_login = TRUE,
                        updated_at = %s
                    WHERE LOWER(email) = LOWER(%s)
                    """,
                    (datetime.now(), email),
                )
                conn.commit()

        log_security_event(
            'force_password_change',
            {'admin_email': session.get('user_email'), 'target_email': email},
        )
        logger.info("Force password change set by admin for user: %s", email)
        return jsonify({'success': True, 'message': 'Захтев за промену лозинке је постављен'})
    except Exception as exc:
        logger.error("Error setting force password change: %s", exc)
        return jsonify({'success': False, 'message': str(exc)}), 500


def api_password_manager_toggle_status(*, log_security_event):
    """Activate or deactivate user."""
    data = request.get_json() or {}
    email = data.get('email')
    is_active = data.get('is_active', True)

    if not email:
        return jsonify({'success': False, 'message': 'Недостају параметри'}), 400
    if email.lower() == session.get('user_email', '').lower() and not is_active:
        return jsonify({'success': False, 'message': 'Не можете деактивирати сопствени налог'}), 400

    try:
        with get_postgres_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    UPDATE users
                    SET is_active = %s,
                        updated_at = %s
                    WHERE LOWER(email) = LOWER(%s)
                    """,
                    (is_active, datetime.now(), email),
                )
                conn.commit()

        status_text = 'активиран' if is_active else 'деактивиран'
        log_security_event(
            'user_status_changed',
            {
                'admin_email': session.get('user_email'),
                'target_email': email,
                'is_active': is_active,
            },
        )
        logger.info("User %s %s by admin", email, status_text)
        return jsonify({'success': True, 'message': f'Корисник је {status_text}'})
    except Exception as exc:
        logger.error("Error toggling user status: %s", exc)
        return jsonify({'success': False, 'message': str(exc)}), 500


def api_password_manager_generate(*, password_validator):
    """Generate a strong random password."""
    return jsonify({'success': True, 'password': password_validator.generate_strong_password(16)})
