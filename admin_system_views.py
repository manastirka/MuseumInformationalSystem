"""Shared route implementations for admin system settings and maintenance."""

import gc
import json
import logging
import os
import platform
import subprocess
from datetime import datetime, timedelta
from pathlib import Path

import psutil
from flask import current_app, jsonify, render_template, request, send_file
from psycopg.rows import dict_row

from postgres_service import get_database_url, get_postgres_connection

logger = logging.getLogger(__name__)

SETTINGS_FILE = Path('data/system_settings.json')
MAIN_LOG_FILE = Path('logs/main_app.log')
BACKUP_DIR = Path('backups')


def _load_saved_settings():
    settings = {}
    if SETTINGS_FILE.exists():
        with SETTINGS_FILE.open('r', encoding='utf-8') as handle:
            settings = json.load(handle)
    return settings


def _save_settings(settings):
    SETTINGS_FILE.parent.mkdir(parents=True, exist_ok=True)
    with SETTINGS_FILE.open('w', encoding='utf-8') as handle:
        json.dump(settings, handle, ensure_ascii=False, indent=2)


def _session_timeout_minutes(value):
    if isinstance(value, timedelta):
        return int(value.total_seconds() // 60)
    if isinstance(value, (int, float)):
        return int(value // 60)
    return 60


def render_admin_system_settings():
    """Render the admin system settings page."""
    db_stats = {
        'total_tables': 0,
        'total_users': 0,
        'db_size': 'N/A',
    }

    try:
        get_database_url()
        with get_postgres_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT COUNT(*) FROM information_schema.tables
                    WHERE table_schema = 'public'
                    """
                )
                db_stats['total_tables'] = cur.fetchone()[0]

                cur.execute("SELECT COUNT(*) FROM users")
                db_stats['total_users'] = cur.fetchone()[0]

                cur.execute("SELECT pg_size_pretty(pg_database_size(current_database()))")
                db_stats['db_size'] = cur.fetchone()[0]
    except Exception as exc:
        logger.error("Error getting db stats: %s", exc)

    system_info = {
        'version': '2.0.0',
        'platform': platform.system() + ' ' + platform.release(),
        'python_version': platform.python_version(),
        'uptime': 'N/A',
        'started_at': 'N/A',
        'memory_usage': 'N/A',
        'disk_usage': 'N/A',
    }

    try:
        memory = psutil.virtual_memory()
        system_info['memory_usage'] = f"{memory.percent}%"

        disk = psutil.disk_usage('/')
        system_info['disk_usage'] = f"{disk.percent}%"

        boot_time = datetime.fromtimestamp(psutil.boot_time())
        uptime = datetime.now() - boot_time
        system_info['uptime'] = f"{uptime.days}д {uptime.seconds // 3600}ч"
        system_info['started_at'] = boot_time.strftime('%d.%m.%Y %H:%M')
    except Exception as exc:
        logger.error("Error getting system info: %s", exc)

    recent_logs = []
    try:
        if MAIN_LOG_FILE.exists():
            with MAIN_LOG_FILE.open('r', encoding='utf-8', errors='ignore') as handle:
                lines = handle.readlines()
                recent_logs = [line.strip() for line in lines[-20:] if line.strip()]
                recent_logs.reverse()
    except Exception as exc:
        logger.error("Error reading logs: %s", exc)

    settings = {
        'institution_name': 'Природњачки музеј у Београду',
        'contact_email': 'info@nhmbeo.rs',
        'min_password_length': current_app.config.get('PASSWORD_MIN_LENGTH', 12),
        'max_login_attempts': current_app.config.get('MAX_LOGIN_ATTEMPTS', 5),
        'lockout_duration': current_app.config.get('ACCOUNT_LOCKOUT_DURATION', 1800) // 60,
        'session_timeout': _session_timeout_minutes(
            current_app.config.get('PERMANENT_SESSION_LIFETIME', 3600)
        ),
        'require_special_chars': current_app.config.get('PASSWORD_REQUIRE_SPECIAL', True),
    }

    try:
        settings.update(_load_saved_settings())
    except Exception as exc:
        logger.error("Error loading settings: %s", exc)

    return render_template(
        'admin_system_settings.html',
        db_stats=db_stats,
        system_info=system_info,
        recent_logs=recent_logs,
        settings=settings,
    )


def api_save_general_settings():
    """Save general settings."""
    try:
        data = request.get_json() or {}
        settings = _load_saved_settings() if SETTINGS_FILE.exists() else {}
        settings.update(
            {
                'institution_name': data.get('institution_name'),
                'contact_email': data.get('contact_email'),
                'system_language': data.get('system_language'),
                'timezone': data.get('timezone'),
            }
        )
        _save_settings(settings)
        return jsonify({'success': True})
    except Exception as exc:
        logger.error("Error saving general settings: %s", exc)
        return jsonify({'success': False, 'error': 'Грешка при чувању општих подешавања'})


def api_save_security_settings():
    """Save security settings."""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'success': False, 'error': 'Нема података'}), 400

        min_password_length = data.get('min_password_length', 12)
        max_login_attempts = data.get('max_login_attempts', 5)
        lockout_duration = data.get('lockout_duration', 30)
        session_timeout = data.get('session_timeout', 480)
        require_special_chars = data.get('require_special_chars', True)

        if not isinstance(min_password_length, int) or not (8 <= min_password_length <= 128):
            return jsonify(
                {'success': False, 'error': 'Минимална дужина лозинке мора бити између 8 и 128'}
            ), 400
        if not isinstance(max_login_attempts, int) or not (3 <= max_login_attempts <= 20):
            return jsonify(
                {'success': False, 'error': 'Максимални покушаји пријаве морају бити између 3 и 20'}
            ), 400
        if not isinstance(lockout_duration, (int, float)) or not (1 <= lockout_duration <= 1440):
            return jsonify(
                {'success': False, 'error': 'Трајање закључавања мора бити између 1 и 1440 минута'}
            ), 400
        if not isinstance(session_timeout, (int, float)) or not (5 <= session_timeout <= 1440):
            return jsonify(
                {'success': False, 'error': 'Трајање сесије мора бити између 5 и 1440 минута'}
            ), 400
        if not isinstance(require_special_chars, bool):
            require_special_chars = bool(require_special_chars)

        settings = _load_saved_settings() if SETTINGS_FILE.exists() else {}
        settings.update(
            {
                'min_password_length': min_password_length,
                'max_login_attempts': max_login_attempts,
                'lockout_duration': lockout_duration,
                'session_timeout': session_timeout,
                'require_special_chars': require_special_chars,
            }
        )
        _save_settings(settings)

        current_app.config['PASSWORD_MIN_LENGTH'] = min_password_length
        current_app.config['MAX_LOGIN_ATTEMPTS'] = max_login_attempts
        current_app.config['ACCOUNT_LOCKOUT_DURATION'] = int(lockout_duration) * 60

        return jsonify({'success': True})
    except Exception as exc:
        logger.error("Error saving security settings: %s", exc)
        return jsonify({'success': False, 'error': 'Грешка при чувању подешавања безбедности'})


def api_database_backup():
    """Create a PostgreSQL backup with pg_dump."""
    try:
        BACKUP_DIR.mkdir(parents=True, exist_ok=True)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_file = BACKUP_DIR / f'museum_system_backup_{timestamp}.sql'

        result = subprocess.run(
            [
                'pg_dump',
                '-U',
                os.environ.get('DB_USER', 'aleksandarlukovic'),
                '-d',
                'museum_system',
                '-f',
                str(backup_file),
            ],
            capture_output=True,
            text=True,
        )

        if result.returncode != 0:
            logger.error("Database backup failed: %s", result.stderr)
            return jsonify({'success': False, 'error': 'Грешка при креирању бекапа базе података'})

        size = backup_file.stat().st_size
        size_str = f"{size / 1024 / 1024:.2f} MB" if size > 1024 * 1024 else f"{size / 1024:.2f} KB"
        logger.info("Database backup created: %s (%s)", backup_file, size_str)
        return jsonify(
            {
                'success': True,
                'message': f'Бекап успешно креиран ({size_str})',
                'size': size_str,
            }
        )
    except Exception as exc:
        logger.error("Error creating backup: %s", exc)
        return jsonify({'success': False, 'error': 'Грешка при креирању бекапа'})


def api_table_stats():
    """Return user table statistics."""
    try:
        get_database_url()
        with get_postgres_connection(row_factory=dict_row) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT
                        relname as name,
                        n_live_tup as row_count,
                        pg_size_pretty(pg_total_relation_size(relid)) as size
                    FROM pg_stat_user_tables
                    ORDER BY n_live_tup DESC
                    """
                )
                tables = [dict(row) for row in cur.fetchall()]

        return jsonify({'success': True, 'tables': tables})
    except RuntimeError:
        return jsonify({'success': False, 'error': 'Database not configured'})
    except Exception as exc:
        logger.error("Error getting table stats: %s", exc)
        return jsonify({'success': False, 'error': str(exc)})


def api_vacuum_database():
    """Run VACUUM ANALYZE on the configured database."""
    try:
        get_database_url()
        with get_postgres_connection(autocommit=True) as conn:
            with conn.cursor() as cur:
                cur.execute("VACUUM ANALYZE")
        logger.info("Database VACUUM ANALYZE completed")
        return jsonify({'success': True})
    except RuntimeError:
        return jsonify({'success': False, 'error': 'Database not configured'})
    except Exception as exc:
        logger.error("Error running vacuum: %s", exc)
        return jsonify({'success': False, 'error': str(exc)})


def api_get_logs():
    """Get recent system logs."""
    try:
        level = request.args.get('level', 'all')
        limit = int(request.args.get('limit', 50))
        logs = []

        if MAIN_LOG_FILE.exists():
            with MAIN_LOG_FILE.open('r', encoding='utf-8', errors='ignore') as handle:
                lines = reversed(handle.readlines())
                for line in lines:
                    line = line.strip()
                    if not line:
                        continue
                    if level == 'all' or level in line:
                        logs.append(line)
                        if len(logs) >= limit:
                            break

        return jsonify({'success': True, 'logs': logs})
    except Exception as exc:
        logger.error("Error reading logs: %s", exc)
        return jsonify({'success': False, 'error': str(exc)})


def api_download_logs():
    """Download the main application log file."""
    try:
        if MAIN_LOG_FILE.exists():
            return send_file(
                MAIN_LOG_FILE,
                as_attachment=True,
                download_name='museum_system_logs.log',
            )
        return jsonify({'success': False, 'error': 'Log file not found'}), 404
    except Exception as exc:
        logger.error("Error downloading logs: %s", exc)
        return jsonify({'success': False, 'error': str(exc)}), 500


def api_clear_cache():
    """Trigger basic in-process cache cleanup."""
    try:
        gc.collect()
        logger.info("System cache cleared")
        return jsonify({'success': True})
    except Exception as exc:
        logger.error("Error clearing cache: %s", exc)
        return jsonify({'success': False, 'error': str(exc)})
