"""Shared route implementations for access management and password manager views."""

import logging
from datetime import datetime

from flask import abort, flash, jsonify, redirect, render_template, request, session, url_for
from psycopg.rows import dict_row

import admin_system_views
import app_ui_support
import dashboard_config_support
import mail_client
from observability import add_sentry_breadcrumb, capture_observability_exception
from postgres_service import get_postgres_connection

logger = logging.getLogger(__name__)


def _server_error_response(message):
    return jsonify({'success': False, 'message': message}), 500


def _parse_user_id(value):
    if value in (None, ''):
        return None
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def _load_active_users():
    with get_postgres_connection(row_factory=dict_row) as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT
                    u.email,
                    u.full_name,
                    u.position,
                    u.is_active,
                    COALESCE(d.name, 'Природњачки музеј') as department,
                    COALESCE(r.name, 'employee') as role
                FROM users u
                LEFT JOIN departments d ON u.department_id = d.id
                LEFT JOIN roles r ON u.role_id = r.id
                WHERE u.is_active = TRUE
                ORDER BY u.full_name
                """
            )
            return [dict(row) for row in cur.fetchall()]


def _active_user_emails():
    return {
        (user.get('email') or '').strip().lower()
        for user in _load_active_users()
        if user.get('email')
    }


def render_manage_user_access(
    *,
    load_module_access,
    user_has_module_access,
    module_access,
    get_museum_employees,
):
    """Manage user module access."""
    # Render the card grid from the freshly loaded module_access, not from the
    # reference captured before this call. load_module_access() rebinds the
    # global to a new dict; with the shared-settings DB and its 60s TTL, a stale
    # reference (or another worker's stale cache) would paint cards from old
    # permissions while the access guard already sees the new ones — the card
    # then shows "+" for a module the user really has. force=True defeats the
    # TTL so the grid matches the guard.
    module_access = load_module_access(force=True)
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
    module_access = load_module_access()
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
    module_access = load_module_access()
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
    load_module_access,
    user_has_module_access,
    load_saved_elements,
    save_user_elements,
    dashboard_endpoint,
):
    """Customize dashboard element preferences for the current user."""
    user_email = session.get('user_email')
    user_role = session.get('user_role')

    module_access = load_module_access() or {}

    available_sections = [
        {
            'key': section_key,
            'name': section_info['name'],
            'description': section_info['description'],
            'icon': section_info['icon'],
        }
        for section_key, section_info in dashboard_config_support.DASHBOARD_SECTIONS.items()
    ]
    available_modules = [
        {
            'key': module_key,
            'name': module_info['name'],
            'description': module_info['description'],
            'icon': module_info['icon'],
        }
        for module_key, module_info in module_access.items()
        if user_has_module_access(user_email, user_role, module_key)
    ]
    allowed_keys = {element['key'] for element in available_sections + available_modules}

    if request.method == 'POST':
        selected_widgets = request.form.getlist('widgets')

        forbidden = [key for key in selected_widgets if key not in allowed_keys]
        if forbidden:
            logger.warning(
                "Rejected dashboard config save for %s: forbidden elements %s",
                user_email,
                forbidden,
            )
            abort(403)

        if save_user_elements(user_email, selected_widgets):
            flash('Подешавања табле су успешно сачувана!', 'success')
        else:
            flash('Грешка при чувању подешавања!', 'error')

        return redirect(url_for(dashboard_endpoint))

    legacy_preferences = load_dashboard_preferences() or {}
    current_prefs = dashboard_config_support.resolve_enabled_elements(
        user_email,
        user_role,
        allowed_keys=allowed_keys,
        saved_elements=load_saved_elements(user_email),
        legacy_enabled_widgets=legacy_preferences.get(user_email, {}).get('enabled_widgets'),
        admin_widget_users=app_ui_support.DEFAULT_ADMIN_WIDGET_USERS,
        module_keys=module_access.keys(),
    )

    return render_template(
        'customize_dashboard.html',
        available_modules=available_sections + available_modules,
        enabled_widgets=current_prefs,
    )


def render_admin_password_manager():
    """Password manager for all users."""
    return render_template('admin_password_manager.html')


def render_admin_mail_configuration():
    """Render the centralized admin mail configuration page."""
    return render_template('admin_mail_settings.html')


def api_admin_mail_settings_state():
    """Return active users, current global mail policy, and selected user settings."""
    target_email = (request.args.get('email') or '').strip().lower()
    try:
        users = []
        for user in _load_active_users():
            user_email = (user.get('email') or '').strip().lower()
            settings = mail_client.get_user_settings_safe(user_email)
            users.append(
                {
                    'email': user_email,
                    'full_name': user.get('full_name') or user_email,
                    'department': user.get('department') or '',
                    'position': user.get('position') or '',
                    'role': user.get('role') or 'employee',
                    'mail_configured': bool(settings),
                }
            )

        saved_settings = admin_system_views.load_saved_settings() or {}
        selected_settings = None
        if target_email:
            selected_settings = mail_client.get_user_settings_safe(target_email)

        return jsonify(
            {
                'success': True,
                'users': users,
                'selected_email': target_email,
                'settings': selected_settings,
                'allowed_hosts': saved_settings.get(
                    mail_client.MAIL_ALLOWED_HOSTS_KEY,
                    mail_client.get_allowed_mail_hosts(),
                ),
                'banned_hosts': saved_settings.get(
                    mail_client.MAIL_BANNED_HOSTS_KEY,
                    mail_client.get_banned_mail_hosts(),
                ),
            }
        )
    except Exception as exc:
        logger.error("Error loading admin mail settings state: %s", exc)
        return _server_error_response('Грешка при учитавању mail подешавања.')


def api_admin_mail_settings_save():
    """Save mail settings for a selected user and persist the global host policy."""
    try:
        data = request.get_json(force=True) or {}
        target_email = (data.get('target_email') or '').strip().lower()
        if not target_email:
            return jsonify({'success': False, 'message': 'Изаберите корисника.'}), 400
        if target_email not in _active_user_emails():
            return jsonify({'success': False, 'message': 'Изабрани корисник није пронађен.'}), 404

        allowed_hosts = mail_client.normalize_allowed_mail_hosts(data.get('allowed_hosts', []))
        banned_hosts = mail_client.normalize_allowed_mail_hosts(data.get('banned_hosts', []))
    except ValueError as exc:
        return jsonify({'success': False, 'message': str(exc)}), 400
    except Exception:
        logger.exception("Could not prepare admin mail settings save request")
        return jsonify({'success': False, 'message': 'Грешка при припреми mail подешавања.'}), 500

    try:
        settings = {
            'imap_server': (data.get('imap_server') or '').strip(),
            'imap_port': int(data.get('imap_port', 993)),
            'imap_ssl': bool(data.get('imap_ssl', True)),
            'smtp_server': (data.get('smtp_server') or '').strip(),
            'smtp_port': int(data.get('smtp_port', 587)),
            'smtp_starttls': bool(data.get('smtp_starttls', True)),
            'email_address': (data.get('email_address') or '').strip(),
        }
    except (TypeError, ValueError):
        return jsonify({'success': False, 'message': 'Порт мора бити број.'}), 400

    try:
        existing = mail_client.get_user_settings(target_email) or {}
        password = (data.get('password') or '').strip()
        if password:
            settings['password'] = mail_client._encrypt(password)
        elif 'password' in existing:
            settings['password'] = existing['password']
        else:
            return jsonify({'success': False, 'message': 'Лозинка је обавезна.'}), 400

        settings = mail_client.validate_mail_server_settings(
            settings,
            allowed_hosts=allowed_hosts,
            banned_hosts=banned_hosts,
        )
    except ValueError as exc:
        return jsonify({'success': False, 'message': str(exc)}), 400
    except (RuntimeError, OSError) as exc:
        logger.exception("Mail credential encryption failed for %s", target_email)
        return jsonify({'success': False, 'message': str(exc)}), 500
    except Exception:
        logger.exception("Unexpected mail credential preparation failure for %s", target_email)
        return jsonify({'success': False, 'message': 'Грешка при припреми mail лозинке.'}), 500

    try:
        saved_settings = admin_system_views.load_saved_settings() or {}
        saved_settings[mail_client.MAIL_ALLOWED_HOSTS_KEY] = allowed_hosts
        saved_settings[mail_client.MAIL_BANNED_HOSTS_KEY] = banned_hosts
        if not admin_system_views.save_settings(saved_settings):
            return jsonify({'success': False, 'message': 'Није могуће сачувати глобалну mail политику.'}), 500
        mail_client.save_user_settings(target_email, settings)
        return jsonify({'success': True, 'message': 'Mail подешавања су сачувана.'})
    except RuntimeError as exc:
        logger.exception("Mail settings save failed for %s", target_email)
        return jsonify({'success': False, 'message': str(exc)}), 500
    except Exception:
        logger.exception("Unexpected mail settings save failure for %s", target_email)
        return jsonify({'success': False, 'message': 'Грешка при чувању mail подешавања.'}), 500


def api_admin_mail_test_connection():
    """Test IMAP or SMTP using the selected user's saved or pending credentials."""
    try:
        data = request.get_json(force=True) or {}
        target_email = (data.get('target_email') or '').strip().lower()
        if not target_email:
            return jsonify({'success': False, 'message': 'Изаберите корисника.'}), 400
        if target_email not in _active_user_emails():
            return jsonify({'success': False, 'message': 'Изабрани корисник није пронађен.'}), 404

        allowed_hosts = mail_client.normalize_allowed_mail_hosts(data.get('allowed_hosts', []))
        banned_hosts = mail_client.normalize_allowed_mail_hosts(data.get('banned_hosts', []))
    except ValueError as exc:
        return jsonify({'success': False, 'message': str(exc)}), 400
    except Exception:
        logger.exception("Could not prepare admin mail connection test request")
        return jsonify({'success': False, 'message': 'Грешка при припреми mail теста.'}), 500

    try:
        conn_type = data.get('type', 'imap')
        password = (data.get('password') or '').strip()
        if not password:
            existing = mail_client.get_user_settings(target_email)
            if existing and 'password' in existing:
                try:
                    password = mail_client._decrypt(existing['password'])
                except Exception:
                    return jsonify({'success': False, 'message': 'Лозинка је потребна за тест.'}), 400
            else:
                return jsonify({'success': False, 'message': 'Лозинка је потребна за тест.'}), 400

        if conn_type == 'imap':
            result = mail_client.test_imap_connection(
                server=data.get('imap_server', ''),
                port=int(data.get('imap_port', 993)),
                ssl=bool(data.get('imap_ssl', True)),
                email_address=(data.get('email_address') or '').strip(),
                password=password,
                allowed_hosts=allowed_hosts,
                banned_hosts=banned_hosts,
            )
        else:
            result = mail_client.test_smtp_connection(
                server=data.get('smtp_server', ''),
                port=int(data.get('smtp_port', 587)),
                starttls=bool(data.get('smtp_starttls', True)),
                email_address=(data.get('email_address') or '').strip(),
                password=password,
                allowed_hosts=allowed_hosts,
                banned_hosts=banned_hosts,
            )
    except (TypeError, ValueError) as exc:
        return jsonify({'success': False, 'message': f'Погрешан параметар за тест: {exc}'}), 400
    except Exception:
        logger.exception("Unexpected mail connection test failure for %s", target_email)
        return jsonify({'success': False, 'message': 'Грешка при тестирању mail везе.'}), 500

    return jsonify(result)


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
        return _server_error_response('Грешка при учитавању корисника.')


def api_password_manager_reset(*, password_validator, password_hasher, log_security_event):
    """Reset user password."""
    data = request.get_json() or {}
    user_id = _parse_user_id(data.get('user_id'))
    email = data.get('email')
    new_password = data.get('new_password')
    force_change = data.get('force_change', True)

    if not email or not new_password:
        return jsonify({'success': False, 'message': 'Недостају параметри'}), 400

    is_valid, errors = password_validator.validate(new_password)
    if not is_valid:
        return jsonify({'success': False, 'message': ', '.join(errors)}), 400

    try:
        add_sentry_breadcrumb(
            category='password_manager',
            message='Admin password reset requested',
            data={'target_email': email, 'force_change': force_change},
        )
        password_hash, salt = password_hasher.hash_password(new_password)
        with get_postgres_connection() as conn:
            with conn.cursor() as cur:
                if user_id:
                    cur.execute(
                        """
                        UPDATE users
                        SET password_hash = %s,
                            salt = %s,
                            is_first_login = %s,
                            updated_at = %s
                        WHERE id = %s
                          AND LOWER(email) = LOWER(%s)
                        """,
                        (password_hash, salt, force_change, datetime.now(), user_id, email),
                    )
                else:
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
                if cur.rowcount != 1:
                    conn.rollback()
                    return jsonify({'success': False, 'message': 'Изабрани корисник није пронађен.'}), 404
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
        capture_observability_exception(
            exc,
            tags={'component': 'password_manager', 'operation': 'reset'},
            extra={
                'admin_email': session.get('user_email'),
                'target_email': email,
                'force_change': force_change,
            },
            user={'email': session.get('user_email')},
        )
        return _server_error_response('Грешка при ресетовању лозинке.')


def api_password_manager_force_change(*, log_security_event):
    """Force user to change password on next login."""
    data = request.get_json() or {}
    user_id = _parse_user_id(data.get('user_id'))
    email = data.get('email')
    if not email:
        return jsonify({'success': False, 'message': 'Недостају параметри'}), 400

    try:
        add_sentry_breadcrumb(
            category='password_manager',
            message='Admin force password change requested',
            data={'target_email': email},
        )
        with get_postgres_connection() as conn:
            with conn.cursor() as cur:
                if user_id:
                    cur.execute(
                        """
                        UPDATE users
                        SET is_first_login = TRUE,
                            updated_at = %s
                        WHERE id = %s
                          AND LOWER(email) = LOWER(%s)
                        """,
                        (datetime.now(), user_id, email),
                    )
                else:
                    cur.execute(
                        """
                        UPDATE users
                        SET is_first_login = TRUE,
                            updated_at = %s
                        WHERE LOWER(email) = LOWER(%s)
                        """,
                        (datetime.now(), email),
                    )
                if cur.rowcount != 1:
                    conn.rollback()
                    return jsonify({'success': False, 'message': 'Изабрани корисник није пронађен.'}), 404
                conn.commit()

        log_security_event(
            'force_password_change',
            {'admin_email': session.get('user_email'), 'target_email': email},
        )
        logger.info("Force password change set by admin for user: %s", email)
        return jsonify({'success': True, 'message': 'Захтев за промену лозинке је постављен'})
    except Exception as exc:
        logger.error("Error setting force password change: %s", exc)
        capture_observability_exception(
            exc,
            tags={'component': 'password_manager', 'operation': 'force_change'},
            extra={'admin_email': session.get('user_email'), 'target_email': email},
            user={'email': session.get('user_email')},
        )
        return _server_error_response('Грешка при постављању обавезне промене лозинке.')


def api_password_manager_toggle_status(*, log_security_event):
    """Activate or deactivate user."""
    data = request.get_json() or {}
    user_id = _parse_user_id(data.get('user_id'))
    email = data.get('email')
    is_active = data.get('is_active', True)

    if not email:
        return jsonify({'success': False, 'message': 'Недостају параметри'}), 400
    if email.lower() == session.get('user_email', '').lower() and not is_active:
        return jsonify({'success': False, 'message': 'Не можете деактивирати сопствени налог'}), 400

    try:
        add_sentry_breadcrumb(
            category='password_manager',
            message='Admin user status change requested',
            data={'target_email': email, 'is_active': is_active},
        )
        with get_postgres_connection() as conn:
            with conn.cursor() as cur:
                if user_id:
                    cur.execute(
                        """
                        UPDATE users
                        SET is_active = %s,
                            updated_at = %s
                        WHERE id = %s
                          AND LOWER(email) = LOWER(%s)
                        """,
                        (is_active, datetime.now(), user_id, email),
                    )
                else:
                    cur.execute(
                        """
                        UPDATE users
                        SET is_active = %s,
                            updated_at = %s
                        WHERE LOWER(email) = LOWER(%s)
                        """,
                        (is_active, datetime.now(), email),
                    )
                if cur.rowcount != 1:
                    conn.rollback()
                    return jsonify({'success': False, 'message': 'Изабрани корисник није пронађен.'}), 404
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
        capture_observability_exception(
            exc,
            tags={'component': 'password_manager', 'operation': 'toggle_status'},
            extra={
                'admin_email': session.get('user_email'),
                'target_email': email,
                'is_active': is_active,
            },
            user={'email': session.get('user_email')},
        )
        return _server_error_response('Грешка при промени статуса корисника.')


def api_password_manager_generate(*, password_validator):
    """Generate a strong random password."""
    return jsonify({'success': True, 'password': password_validator.generate_strong_password(16)})
