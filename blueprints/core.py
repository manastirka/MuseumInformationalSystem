"""Core authentication and dashboard routes extracted from app.py."""

from flask import Blueprint

import core_app_views
from security_utils import login_required


core_bp = Blueprint('core', __name__)


@core_bp.route('/healthz')
def healthz():
    """Readiness probe (unauthenticated, minimal output): reports whether the
    app can reach PostgreSQL and Redis. 200 when healthy, 503 when degraded —
    for nginx / systemd ExecStartPost / uptime monitoring."""
    import os
    from flask import jsonify

    checks = {'db': 'skipped', 'redis': 'skipped'}
    healthy = True

    if os.environ.get('DATABASE_URL'):
        try:
            from postgres_service import get_postgres_connection
            conn = get_postgres_connection()
            try:
                with conn.cursor() as cur:
                    cur.execute('SELECT 1')
                    cur.fetchone()
                checks['db'] = 'ok'
            finally:
                conn.close()
        except Exception:
            checks['db'] = 'error'
            healthy = False

    redis_url = os.environ.get('REDIS_URL')
    if redis_url:
        try:
            import redis as _redis
            _redis.from_url(redis_url, socket_connect_timeout=2).ping()
            checks['redis'] = 'ok'
        except Exception:
            checks['redis'] = 'error'
            healthy = False

    return jsonify({'status': 'ok' if healthy else 'degraded', **checks}), (200 if healthy else 503)


@core_bp.route('/set_language', methods=['POST'])
def set_language():
    """Set the user's language/script preference (UI-only, no sensitive data)."""
    return core_app_views.set_language_preference()


@core_bp.route('/set_theme', methods=['POST'])
def set_theme():
    """Set the user's UI theme preference (mode + accent + palette)."""
    return core_app_views.set_theme_preference()


@core_bp.route('/podesavanja/izgled')
@login_required
def izgled_personalizacija():
    """Izgled i personalizacija — birač imenovanih tema (faza 1: plavo-bele)."""
    from flask import render_template
    return render_template('podesavanja_izgled.html')


@core_bp.route('/')
@core_bp.route('/index')
def index():
    """Main landing page."""
    return core_app_views.render_index(
        dashboard_endpoint='dashboard',
    )


@core_bp.route('/login', methods=['GET', 'POST'])
def login():
    """User login with security enhancements."""
    import app as museum_app

    return core_app_views.handle_login(
        app_config=museum_app.app.config,
        auth_system=museum_app.auth_system,
        ensure_login_tracker_initialized=museum_app.ensure_login_tracker_initialized,
        log_security_event=museum_app.log_security_event,
        log_fallback_auth_warning_once=museum_app.log_fallback_auth_warning_once,
        authenticate_fallback_user=museum_app.authenticate_fallback_user,
        change_password_endpoint='change_password',
        dashboard_endpoint='dashboard',
    )


@core_bp.route('/logout', methods=['GET', 'POST'])
def logout():
    """User logout. Accepts both GET (for backwards compat) and POST (preferred)."""
    return core_app_views.handle_logout(
        index_endpoint='index',
    )


@core_bp.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    """Change user password with validation."""
    import app as museum_app

    return core_app_views.handle_change_password(
        auth_system=museum_app.auth_system,
        app_config=museum_app.app.config,
        password_validator=museum_app.password_validator,
        dashboard_endpoint='dashboard',
        log_security_event=museum_app.log_security_event,
        authenticate_fallback_user=museum_app.authenticate_fallback_user,
    )


@core_bp.route('/dashboard')
@login_required
def dashboard():
    """Main dashboard."""
    import app as museum_app

    return core_app_views.render_dashboard(
        get_user_dashboard_view=museum_app.get_user_dashboard_view,
    )


@core_bp.route('/dashboard-classic')
@login_required
def dashboard_classic():
    """Classic dashboard view."""
    import app as museum_app

    return core_app_views.render_dashboard(
        get_user_dashboard_view=museum_app.get_user_dashboard_view,
    )


@core_bp.route('/mineral_database')
@login_required
def mineral_database_app():
    """Route to mineral database - redirects to admin mineral collection."""
    import app as museum_app

    return core_app_views.render_mineral_database_redirect(
        user_has_module_access=museum_app.user_has_module_access,
        dashboard_endpoint='dashboard',
        admin_mineral_collection_endpoint='admin_mineral_collection',
    )
