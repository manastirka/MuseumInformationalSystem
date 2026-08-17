"""Shared route implementations for admin system settings and maintenance."""

import gc
import json
import logging
import os
import platform
import subprocess
from copy import deepcopy
from datetime import datetime, timedelta
from pathlib import Path

import psutil
from flask import (current_app, jsonify, render_template, request,
                   send_file, session)
from psycopg.rows import dict_row

import module_access_support
from postgres_service import get_database_url, get_postgres_connection

import audit_support
import odobravanje_prekidac
import odobravanje_razresavanje

logger = logging.getLogger(__name__)

SETTINGS_FILE = Path('data/system_settings.json')
MAIN_LOG_FILE = Path(os.environ.get('LOG_FILE', os.path.join(os.environ.get('LOG_DIR', 'logs'), 'museum_info_system.log')))
BACKUP_DIR = Path('backups')
_saved_settings_cache = {
    'data': None,
    'timestamp': None,
    'db_enabled': None,
}
_SAVED_SETTINGS_CACHE_TTL_SECONDS = float(os.environ.get('SYSTEM_SETTINGS_CACHE_TTL_SECONDS', '60'))


def load_saved_settings(force: bool = False):
    """Load shared system settings from PostgreSQL first, then file fallback."""
    db_enabled = bool(os.environ.get('DATABASE_URL'))
    if (
        not force
        and _saved_settings_cache['data'] is not None
        and _saved_settings_cache['timestamp'] is not None
        and _saved_settings_cache['db_enabled'] == db_enabled
    ):
        age = datetime.now().timestamp() - _saved_settings_cache['timestamp']
        if age < _SAVED_SETTINGS_CACHE_TTL_SECONDS:
            return deepcopy(_saved_settings_cache['data'])

    try:
        loaded = module_access_support.load_json_settings_data(
            setting_key='system_settings',
            default_value={},
            get_postgres_connection=get_postgres_connection if db_enabled else None,
            file_path=str(SETTINGS_FILE),
            current_mtime=SETTINGS_FILE.stat().st_mtime if SETTINGS_FILE.exists() else None,
        )
    except module_access_support.SharedSettingsUnavailable:
        # Baza za deljena podešavanja nedostupna, a nema last-known-good: ne rušimo
        # stranicu — služimo poslednji lokalno keširan snimak ako postoji, inače
        # prazne vrednosti; greška je već ERROR-logovana u sloju ispod.
        cached = _saved_settings_cache.get('data')
        logger.error("Sistemska podešavanja nedostupna (baza pala); koristim keš/prazno")
        return deepcopy(cached) if cached is not None else {}
    _saved_settings_cache['data'] = deepcopy(loaded)
    _saved_settings_cache['timestamp'] = datetime.now().timestamp()
    _saved_settings_cache['db_enabled'] = db_enabled
    return loaded


def save_settings(settings):
    """Persist shared system settings to PostgreSQL and file fallback."""
    db_enabled = bool(os.environ.get('DATABASE_URL'))
    saved = module_access_support.save_json_settings_data(
        setting_key='system_settings',
        payload=settings,
        get_postgres_connection=get_postgres_connection if db_enabled else None,
        file_path=str(SETTINGS_FILE),
    )
    if saved:
        _saved_settings_cache['data'] = deepcopy(settings)
        _saved_settings_cache['timestamp'] = datetime.now().timestamp()
        _saved_settings_cache['db_enabled'] = db_enabled
    return saved


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
        settings.update(load_saved_settings())
    except Exception as exc:
        logger.error("Error loading settings: %s", exc)

    try:
        odobravanje = odobravanje_prekidac.stanje()
        odobravanje['zateceno'] = odobravanje_razresavanje.prebroj_zatecene()
    except Exception as exc:
        # Страница не пада због прекидача, али ни не тврди да зна стање.
        logger.error("Stanje prekidača odobravanja nije očitano: %s", exc)
        odobravanje = None

    return render_template(
        'admin_system_settings.html',
        db_stats=db_stats,
        system_info=system_info,
        recent_logs=recent_logs,
        settings=settings,
        odobravanje=odobravanje,
    )


def api_odobravanje():
    """Укључи/искључи одобравање за један ток.

    Подразумевано је ПРЕГЛЕД: врати шта би се променило и колико редова би
    се затворило, без иједне измене. Стварна промена тражи `izvrsi: true` —
    исто правило као `--execute` у скриптама, јер гашење затвара и оно што
    већ чека и то се не поништава само од себе.
    """
    TOKOVI = {
        'izvestaji': odobravanje_prekidac.KLJUC_IZVESTAJI,
        'dokumenti': odobravanje_prekidac.KLJUC_DOKUMENTI,
        # Рок и верификација немају ред који чека — гашење не разрешава
        # ништа уназад, само мења правило од сада надаље.
        'rok': odobravanje_prekidac.KLJUC_ROK,
        'verifikacija': odobravanje_prekidac.KLJUC_VERIFIKACIJA,
    }
    try:
        data = request.get_json() or {}
        tok = data.get('tok')
        if tok not in TOKOVI:
            return jsonify({'success': False,
                            'error': 'Непознат ток одобравања'}), 400
        if not isinstance(data.get('ukljuceno'), bool):
            return jsonify({'success': False,
                            'error': 'Недостаје вредност прекидача'}), 400
        ukljuceno = data['ukljuceno']
        izvrsi = bool(data.get('izvrsi'))
        kljuc = TOKOVI[tok]

        razresi = {
            'izvestaji': odobravanje_razresavanje.razresi_izvestaje,
            'dokumenti': odobravanje_razresavanje.razresi_dokumente,
        }.get(tok)

        if not izvrsi:
            pregled = {} if (ukljuceno or razresi is None) else razresi('pregled', izvrsi=False)
            return jsonify({'success': True, 'pregled': pregled})

        podesavanja = load_saved_settings(force=True) or {}
        podesavanja[kljuc] = ukljuceno
        if not save_settings(podesavanja):
            # Ако упис падне, корисник види грешку — не поруку о успеху.
            raise RuntimeError('Prekidač odobravanja nije upisan')

        ko = session.get('user_email') or 'admin'
        # Прекидач је ОД САДА уписан. Разрешавање затечених иде у засебној
        # трансакцији и може да падне независно — рецензија мерџа a507044
        # је нашла да је тада враћана порука „Прекидач није промењен", што
        # је неистина: база каже искључено, а панел је приказивао укључено.
        # Делимичан неуспех се зато пријављује КАО делимичан.
        try:
            primenjeno = ({} if (ukljuceno or razresi is None)
                          else razresi(ko, izvrsi=True))
        except Exception as exc:
            logger.error("Прекидач %s УПИСАН, разрешавање затечених пало: %s",
                         kljuc, exc)
            audit_support.record_audit(
                action=audit_support.ACTION_UPDATE,
                entity_type='system_settings', entity_id=kljuc,
                summary=f'Прекидач {kljuc} постављен на {ukljuceno}, '
                        f'разрешавање затечених НИЈЕ прошло',
                # Текст изузетка НЕ иде овде: `test_admin_system_views_ne_curi_izuzetke`
                # брани цео фајл од сировог текста грешке — и то дословно, па
                # чак ни коментар не сме да га помене. Правило је добро:
                # једном ослабљено, важило би и за одговоре ка кориснику.
                # Детаљ већ стоји у `logger.error` изнад, са временом.
                new_values={kljuc: ukljuceno, 'razresavanje_proslo': False},
            )
            return jsonify({
                'success': False,
                'prekidac_upisan': True,
                'error': ('Прекидач ЈЕСТЕ промењен, али затечене ставке нису '
                          'затворене. Оне и даље чекају одобрење. Заврши то '
                          'командом: python3 scripts/odobravanje.py '
                          f'iskljuci {tok} --execute'),
            }), 500

        audit_support.record_audit(
            action=audit_support.ACTION_UPDATE,
            entity_type='system_settings', entity_id=kljuc,
            summary=('Одобравање укључено' if ukljuceno else 'Одобравање искључено')
                    + f' — {tok}',
            new_values={kljuc: ukljuceno, 'razreseno': primenjeno},
        )
        logger.warning("Прекидач %s постављен на %s (%s)", kljuc, ukljuceno, ko)
        return jsonify({'success': True, 'primenjeno': primenjeno})
    except Exception as exc:
        logger.error("Greška pri promeni prekidača odobravanja: %s", exc)
        return jsonify({'success': False,
                        'error': 'Прекидач одобравања није промењен.'}), 500


def api_save_general_settings():
    """Save general settings."""
    try:
        data = request.get_json() or {}
        settings = load_saved_settings()
        settings.update(
            {
                'institution_name': data.get('institution_name'),
                'contact_email': data.get('contact_email'),
                'system_language': data.get('system_language'),
                'timezone': data.get('timezone'),
            }
        )
        if not save_settings(settings):
            raise RuntimeError('Could not persist general settings')
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

        settings = load_saved_settings()
        settings.update(
            {
                'min_password_length': min_password_length,
                'max_login_attempts': max_login_attempts,
                'lockout_duration': lockout_duration,
                'session_timeout': session_timeout,
                'require_special_chars': require_special_chars,
            }
        )
        if not save_settings(settings):
            raise RuntimeError('Could not persist security settings')

        apply_settings = getattr(current_app, 'apply_shared_system_settings', None)
        if apply_settings is not None:
            apply_settings(settings)
        else:
            current_app.config['PASSWORD_MIN_LENGTH'] = min_password_length
            current_app.config['MAX_LOGIN_ATTEMPTS'] = max_login_attempts
            current_app.config['ACCOUNT_LOCKOUT_DURATION'] = int(lockout_duration) * 60
            current_app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=int(session_timeout))
            current_app.config['PASSWORD_REQUIRE_SPECIAL'] = require_special_chars

        return jsonify({
            'success': True,
            'warning': 'Подешавања су примењена на овај радни процес. '
                       'Рестартујте апликацију да примените на све радне процесе.'
                       if os.environ.get('GUNICORN_WORKERS', os.environ.get('WEB_CONCURRENCY', '1')) != '1'
                       else None,
        })
    except Exception as exc:
        logger.error("Error saving security settings: %s", exc)
        return jsonify({'success': False, 'error': 'Грешка при чувању подешавања безбедности'})


def api_database_backup():
    """Create a PostgreSQL backup with pg_dump."""
    try:
        BACKUP_DIR.mkdir(parents=True, exist_ok=True)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_file = BACKUP_DIR / f'museum_system_backup_{timestamp}.sql'

        database_url = get_database_url()
        # Convert SQLAlchemy URL to libpq format for pg_dump
        pg_url = database_url.replace('postgresql+psycopg://', 'postgresql://')

        result = subprocess.run(
            ['pg_dump', '-f', str(backup_file), pg_url],
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
    except Exception:
        logger.exception("Error getting table stats")
        return jsonify({'success': False,
                        'error': 'Грешка при читању статистике табела'})


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
    except Exception:
        logger.exception("Error running vacuum")
        return jsonify({'success': False, 'error': 'Грешка при VACUUM операцији'})


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
    except Exception:
        logger.exception("Error reading logs")
        return jsonify({'success': False, 'error': 'Грешка при читању логова'})


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
    except Exception:
        logger.exception("Error downloading logs")
        return jsonify({'success': False,
                        'error': 'Грешка при преузимању логова'}), 500


def api_clear_cache():
    """Trigger basic in-process cache cleanup."""
    try:
        gc.collect()
        logger.info("System cache cleared")
        return jsonify({'success': True})
    except Exception:
        logger.exception("Error clearing cache")
        return jsonify({'success': False, 'error': 'Грешка при чишћењу кеша'})
