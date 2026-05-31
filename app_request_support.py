"""Request lifecycle helpers and registration hooks for the Flask app."""

import logging
import os
import sys
import time
from pathlib import Path

from flask import current_app, render_template, request, session


def register_error_handlers(flask_app) -> None:
    """Register shared 404/500 error handlers."""

    @flask_app.errorhandler(404)
    def not_found_error(error):
        return (
            render_template(
                'error.html',
                error_code=404,
                error_message="Страница није пронађена",
            ),
            404,
        )

    @flask_app.errorhandler(500)
    def internal_error(error):
        current_app.logger.error("500 Internal Server Error: %s", error)
        current_app.logger.exception("Full traceback:")
        return (
            render_template(
                'error.html',
                error_code=500,
                error_message="Интерна грешка сервера",
            ),
            500,
        )


def register_template_context(
    flask_app,
    *,
    current_dir: str,
    get_current_weather,
    default_weather_condition: str,
    user_has_module_access,
) -> None:
    """Register shared template utility helpers."""

    @flask_app.context_processor
    def utility_processor():
        def user_logged_in():
            return 'user_id' in session

        def is_admin():
            return session.get('user_role') == 'admin'

        def is_director():
            return session.get('user_role') == 'direktor'

        def is_department_head():
            return bool(session.get('is_department_head', False))

        def endpoint_exists(endpoint_name):
            return endpoint_name in current_app.view_functions

        try:
            weather_data = get_current_weather()
        except Exception:
            weather_data = {
                'condition': default_weather_condition,
                'temperature': None,
                'windspeed': None,
                'description': '',
            }

        try:
            weather_script_version = int(
                (Path(current_dir) / 'static' / 'js' / 'weather_particles.js').stat().st_mtime
            )
        except OSError:
            weather_script_version = int(time.time())

        def has_module_access(module_key):
            user_email = session.get('user_email', '')
            user_role = session.get('user_role', '')
            if not user_email and not user_role:
                return False
            return user_has_module_access(user_email, user_role, module_key)

        return dict(
            user_logged_in=user_logged_in,
            user_name=session.get('user_name', ''),
            user_role=session.get('user_role', ''),
            user_email=session.get('user_email', ''),
            is_admin=is_admin,
            is_director=is_director,
            is_department_head=is_department_head,
            endpoint_exists=endpoint_exists,
            has_module_access=has_module_access,
            weather_condition=weather_data.get('condition', default_weather_condition),
            weather_temperature=weather_data.get('temperature'),
            weather_windspeed=weather_data.get('windspeed'),
            weather_description=weather_data.get('description', ''),
            weather_particles_version=weather_script_version,
            current_lang=session.get('museum_lang', request.cookies.get('museum_lang', 'sr-Cyrl')),
        )


def create_timesheet_app_disabled(*, localsql_path: str):
    """Create and configure timesheet sub-application."""
    try:
        if localsql_path not in sys.path:
            sys.path.insert(0, localsql_path)

        import importlib.util

        spec = importlib.util.spec_from_file_location(
            "timesheet_app",
            os.path.join(localsql_path, "start_ultra_fast.py"),
        )
        timesheet_module = importlib.util.module_from_spec(spec)

        old_cwd = os.getcwd()
        os.chdir(localsql_path)

        try:
            spec.loader.exec_module(timesheet_module)
            timesheet_app = timesheet_module.app
            timesheet_app.config['APPLICATION_ROOT'] = '/timesheet'
            logging.info("✅ Timesheet app created successfully")
            return timesheet_app
        finally:
            os.chdir(old_cwd)
    except Exception as exc:
        logging.error("❌ Could not create timesheet app: %s", exc)
        return None


def create_mineral_app_disabled(*, prirodnjacki_path: str):
    """Create and configure mineral database sub-application."""
    try:
        if prirodnjacki_path not in sys.path:
            sys.path.insert(0, prirodnjacki_path)

        import importlib.util

        spec = importlib.util.spec_from_file_location(
            "mineral_app",
            os.path.join(prirodnjacki_path, "app.py"),
        )
        mineral_module = importlib.util.module_from_spec(spec)

        old_cwd = os.getcwd()
        os.chdir(prirodnjacki_path)

        try:
            spec.loader.exec_module(mineral_module)
            mineral_app = (
                mineral_module.application
                if hasattr(mineral_module, 'application')
                else mineral_module.app
            )
            mineral_app.config['APPLICATION_ROOT'] = '/mineral'
            logging.info("✅ Mineral app created successfully")
            return mineral_app
        finally:
            os.chdir(old_cwd)
    except Exception as exc:
        logging.error("❌ Could not create mineral app: %s", exc)
        return None
