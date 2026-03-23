"""Shared route implementations for core session, dashboard, and admin-home views."""

import logging

from flask import flash, jsonify, make_response, redirect, render_template, request, session, url_for

logger = logging.getLogger(__name__)


def set_language_preference():
    """Store the user's UI language preference in the session and cookie."""
    data = request.get_json(silent=True) or {}
    lang = data.get('language', 'sr-Cyrl')
    allowed = {'sr-Cyrl', 'sr-Latn', 'en'}
    if lang in allowed:
        session['museum_lang'] = lang
        response = jsonify({'status': 'ok', 'language': lang})
        response.set_cookie('museum_lang', lang, max_age=31536000, samesite='Lax', path='/')
        return response
    return jsonify({'status': 'error', 'message': 'Invalid language'}), 400


def render_index(*, dashboard_endpoint):
    """Render the public landing page or redirect logged-in users."""
    if 'user_id' in session:
        return redirect(url_for(dashboard_endpoint))
    return render_template('index.html')


def handle_login(
    *,
    app_config,
    auth_system,
    ensure_login_tracker_initialized,
    log_security_event,
    log_fallback_auth_warning_once,
    authenticate_fallback_user,
    change_password_endpoint,
    dashboard_endpoint,
):
    """Authenticate a user and initialize the application session."""
    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')

        if not email or not password:
            flash('Молимо унесите имејл и лозинку.', 'error')
            return render_template('login.html')

        max_attempts = app_config.get('MAX_LOGIN_ATTEMPTS', 5)
        lockout_duration = app_config.get('ACCOUNT_LOCKOUT_DURATION', 1800)

        tracker = ensure_login_tracker_initialized()
        is_locked, seconds_remaining = tracker.is_locked_out(email, max_attempts, lockout_duration)
        if is_locked:
            minutes = seconds_remaining // 60
            flash(
                f'Налог је закључан због превише неуспешних покушаја. '
                f'Покушајте поново за {minutes} минута.',
                'danger',
            )
            log_security_event(
                'account_locked',
                {
                    'email': email,
                    'remaining_seconds': seconds_remaining,
                },
            )
            return render_template('login.html')

        authenticated_user = None
        try:
            if auth_system.available:
                authenticated_user = auth_system.verify_credentials(email, password)

            if not authenticated_user and app_config.get('ENABLE_FALLBACK_AUTH', False):
                log_fallback_auth_warning_once()
                logger.warning("Using fallback auth for: %s", email)
                authenticated_user = authenticate_fallback_user(email, password)

            if (
                not authenticated_user
                and not auth_system.available
                and not app_config.get('ENABLE_FALLBACK_AUTH', False)
            ):
                flash('Систем аутентикације није доступан.', 'error')
                return render_template('login.html')
        except Exception as exc:
            logger.error("Authentication error for %s: %s", email, exc)
            flash('Грешка при пријављивању. Покушајте поново.', 'error')
            return render_template('login.html')

        if authenticated_user:
            session.clear()
            user_id = authenticated_user.get('user_id') or authenticated_user.get('id')
            session['user_id'] = user_id
            session['user_email'] = authenticated_user['email']
            session['user_name'] = authenticated_user['full_name']
            session['user_role'] = authenticated_user['role']
            session['is_admin'] = authenticated_user['role'] == 'admin'
            session['user_department'] = authenticated_user.get('department', '')
            session.permanent = True

            tracker.record_attempt(email, success=True)
            log_security_event(
                'login_success',
                {
                    'email': email,
                    'user_id': user_id,
                },
            )

            if authenticated_user.get('is_first_login', False):
                flash('Морате променити лозинку при првој пријави.', 'warning')
                return redirect(url_for(change_password_endpoint))

            flash(f'Добродошли, {authenticated_user["full_name"]}!', 'success')
            return redirect(url_for(dashboard_endpoint))

        tracker.record_attempt(email, success=False)
        remaining = tracker.get_remaining_attempts(email, max_attempts)
        flash(
            f'Неисправни подаци за пријаву. '
            f'Преостало покушаја: {remaining}',
            'danger',
        )
        log_security_event(
            'login_failed',
            {
                'email': email,
                'remaining_attempts': remaining,
            },
        )
        return render_template('login.html')

    return render_template('login.html')


def handle_logout(*, index_endpoint):
    """Clear the user session and redirect to the landing page."""
    if 'user_id' in session:
        try:
            from chat_room import clear_presence

            clear_presence(session['user_id'])
        except Exception:
            pass
    session.clear()
    return redirect(url_for(index_endpoint))


def handle_change_password(
    *,
    auth_system,
    app_config,
    password_validator,
    dashboard_endpoint,
    log_security_event,
):
    """Change the current user's password after validating the request."""
    if request.method == 'POST':
        current_password = request.form.get('current_password', '')
        new_password = request.form.get('new_password', '')
        confirm_password = request.form.get('confirm_password', '')

        if not all([current_password, new_password, confirm_password]):
            flash('Попуните сва поља.', 'error')
            return render_template('change_password.html')

        if new_password != confirm_password:
            flash('Нове лозинке се не подударају.', 'error')
            return render_template('change_password.html')

        is_valid, errors = password_validator.validate(new_password)
        if not is_valid:
            for error in errors:
                flash(error, 'error')
            return render_template('change_password.html')

        user_id = session.get('user_id')
        user_email = session.get('user_email')

        try:
            if auth_system.available:
                if auth_system.verify_credentials(user_email, current_password):
                    success = auth_system.update_password(user_email, new_password)
                else:
                    flash('Тренутна лозинка није тачна.', 'error')
                    return redirect(url_for('change_password'))
            elif app_config.get('ENABLE_FALLBACK_AUTH', False):
                flash('Промена лозинке није доступна у режиму развоја.', 'warning')
                return redirect(url_for(dashboard_endpoint))
            else:
                flash('Систем аутентикације није доступан.', 'error')
                return render_template('change_password.html')

            if success:
                log_security_event(
                    'password_changed',
                    {
                        'user_id': user_id,
                        'email': user_email,
                    },
                )
                flash('Лозинка је успешно промењена!', 'success')
                return redirect(url_for(dashboard_endpoint))

            flash('Неисправна тренутна лозинка.', 'error')
            return render_template('change_password.html')
        except Exception as exc:
            logger.error("Password change error: %s", exc)
            flash('Грешка при промени лозинке.', 'error')
            return render_template('change_password.html')

    return render_template('change_password.html')


def render_dashboard(*, get_user_modules):
    """Render the module-based user dashboard."""
    user_role = session.get('user_role')
    user_name = session.get('user_name')
    user_email = session.get('user_email')
    accessible_modules = get_user_modules(user_email, user_role)
    response = make_response(
        render_template(
            'dashboard.html',
            user_role=user_role,
            user_name=user_name,
            user_email=user_email,
            accessible_modules=accessible_modules,
        )
    )
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response


def render_mineral_database_redirect(
    *,
    user_has_module_access,
    dashboard_endpoint,
    admin_mineral_collection_endpoint,
):
    """Gate access to the mineral database and redirect to the integrated collection."""
    user_email = session.get('user_email')
    user_role = session.get('user_role')

    if not user_has_module_access(user_email, user_role, 'mineral_database'):
        flash('Немате дозволу за приступ бази минерала.', 'error')
        return redirect(url_for(dashboard_endpoint))

    return redirect(url_for(admin_mineral_collection_endpoint))


def render_admin_panel():
    """Render the basic admin landing page."""
    return render_template('admin_panel.html')
