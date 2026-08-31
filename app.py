#!/usr/bin/env python3
"""
Museum Information System - Main Flask Application
Integrates localSQLtesting (timesheet) and PrirodnjackiMuzej (mineral database) applications
"""

import os
import sys
import json
import logging
import logging.handlers
import calendar
import time
import re
import tempfile
import requests
from functools import wraps
from copy import deepcopy
from flask import Flask, render_template, request, redirect, url_for, session, flash, current_app, send_file, send_from_directory, make_response, jsonify, g, has_request_context
from datetime import datetime
from bs4 import BeautifulSoup
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from werkzeug.middleware.proxy_fix import ProxyFix
from werkzeug.serving import run_simple
from typing import Optional, Dict
from pathlib import Path

# Load environment variables from .env file FIRST
from dotenv import load_dotenv
load_dotenv()
DEFAULT_WEATHER_CONDITION = os.environ.get('WEATHER_FALLBACK_CONDITION', 'none').strip().lower() or 'none'
FORCED_WEATHER_CONDITION = os.environ.get('WEATHER_FORCE_CONDITION', '').strip().lower()

# Use PostgreSQL version if DATABASE_URL is set, otherwise fall back to SQLite
if os.environ.get('DATABASE_URL'):
    from mineral_database_pg import get_mineral_database
    # Import Phase 3A PostgreSQL databases
    import phase3a_databases
else:
    from mineral_database import get_mineral_database

from image_storage_engine import get_image_storage
from archive_signature_blueprint import (
    APP_ROOT as ARCHIVE_SIGNATURE_APP_ROOT,
    APPROVAL_CHAINS,
    REQUEST_SUBTYPES,
    archive_signature_bp,
    can_approve_request,
    can_view_archive_request,
    resolve_signature_document_path,
)
from blueprints.projects import (
    PROJECT_AUTO_DETECTED_SPACES,
    PROJECT_AUTO_LAYOUT_VERSION,
    PROJECT_COMMON_TERMS,
    PROJECT_DEPOT_AUTO_DETECTED_SPACES,
    PROJECT_DEPOT_PLAN_AREA_ANNOTATIONS,
    PROJECT_SPACE_DEPOT_PLAN_FILE,
    PROJECT_SPACE_DEPOT_PLAN_IMAGE_SIZE,
    PROJECT_SPACE_LIBRARY,
    PROJECT_SPACE_PLAN_FILE,
    PROJECT_SPACE_PLAN_IMAGE_SIZE,
    PROJECT_SPACE_PLAN_VIEWS,
    PROJECT_SPACE_PLANNER_RELATIVE_PATH,
    projects_bp,
)
from blueprints.approval_center import approval_center_bp
from blueprints.documents import documents_bp
from blueprints.fototeka import fototeka_bp
from blueprints.kr_dosije import kr_dosije_bp
from blueprints.qr import qr_bp
from blueprints.mail import MAILBOX_ADMIN_FORBIDDEN_MESSAGE, mail_bp
from blueprints.chat import chat_bp
from blueprints.vehicles import vehicles_bp
from blueprints.science import science_bp
from blueprints.maps import maps_bp
from blueprints.content import content_bp
from blueprints.travel_finance import travel_finance_bp
from blueprints.timesheet import timesheet_bp
from blueprints.admin import admin_bp
from blueprints.collections import collections_bp
from blueprints.media import media_bp
from blueprints.mineral_science import mineral_science_bp
from blueprints.core import core_bp
import bird_ringing_database
import scientific_papers_database
import importlib.util
import admin_system_views
import admin_user_management_views
import app_access_support
import app_background_support
import app_blueprint_support
import app_collection_support
import app_core_support
import app_data_support
import app_request_support
import app_runtime_support
import app_ui_support
import bird_ringing_views
import fallback_auth_support
import module_access_support
import museum_staff_support
import vehicle_data_support
import collection_management_views
import collection_statistics_views
import collection_bootstrap_support
import core_app_views
import chat_views
import collection_access_support
import dashboard_config_support
import dashboard_integration_views
import depot_science_views
import employee_admin_views
import exhibition_planner_views
import mail_views
import maps_biodiversity_views
import maps_field_data_views
import maps_layer_views
import maps_geo_zone_views
import maps_profile_views
import maps_profile_support
import maps_terrain_support
import maps_terrain_views
import mineral_science_views
import museum_content_support
import museum_content_views
import museum_overview_views
import nhm_portal_views
import notification_views
import vehicle_depot_views
import collection_media_views
import dashboard_data_support
from postgres_service import get_postgres_connection
import qr_label_views
import qr_management_views
import project_views
import scientific_paper_views
import timesheet_admin_views
import timesheet_employee_views
import travel_finance_views
from timesheet_repository import TimesheetRepository
from science_news_updater import update_science_news_background
import map_feature_paper_enricher
from runtime_lock_utils import try_acquire_process_lock
from observability import init_observability

# Security imports
from config import get_config
from security_utils import (
    PasswordValidator,
    PasswordHasher,
    login_tracker,
    init_login_tracker,
    login_required,
    admin_required,
    module_access_required,
    log_security_event,
    get_client_ip,
    validate_session_auth_version,
)
from flask_wtf.csrf import CSRFProtect
from rate_limit_ext import limiter
from flask_session import Session
from flask_babel import Babel, gettext as _, lazy_gettext as _l

try:
    import redis as redis_client_lib
    REDIS_CLIENT_AVAILABLE = True
except ImportError:
    redis_client_lib = None
    REDIS_CLIENT_AVAILABLE = False

# Security headers
try:
    from flask_talisman import Talisman
    TALISMAN_AVAILABLE = True
except ImportError:
    TALISMAN_AVAILABLE = False
    logging.warning("flask-talisman not available - security headers disabled")

LOG_DIR = os.path.abspath(os.environ.get('LOG_DIR', 'logs'))

# Create log directory before configuring file logging handlers.
os.makedirs(LOG_DIR, exist_ok=True)

def configure_root_logging():
    """Initialize process-wide logging once, even across repeated imports."""
    root_logger = logging.getLogger()
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(name)s - %(message)s')
    log_path = os.path.abspath(os.environ.get('LOG_FILE', os.path.join(LOG_DIR, 'museum_info_system.log')))

    root_logger.setLevel(logging.INFO)

    has_file_handler = any(
        isinstance(handler, logging.FileHandler)
        and getattr(handler, 'baseFilename', None) == log_path
        for handler in root_logger.handlers
    )
    if not has_file_handler:
        # Rotate so logs can't grow without bound and fill the disk.
        file_handler = logging.handlers.RotatingFileHandler(
            log_path, maxBytes=10_000_000, backupCount=5, encoding='utf-8'
        )
        file_handler.setFormatter(formatter)
        root_logger.addHandler(file_handler)

    has_stream_handler = any(
        isinstance(handler, logging.StreamHandler) and not isinstance(handler, logging.FileHandler)
        for handler in root_logger.handlers
    )
    if not has_stream_handler:
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)
        root_logger.addHandler(stream_handler)


configure_root_logging()

if (
    __name__ == '__main__'
    and str(os.environ.get('SESSION_INVALIDATE_ON_RESTART', 'False')).strip().lower() == 'true'
    and not os.environ.get('SESSION_BOOT_ID')
):
    os.environ['SESSION_BOOT_ID'] = str(time.time_ns())

# Add paths for integrated apps
current_dir = os.path.dirname(os.path.abspath(__file__))
APP_ROOT = ARCHIVE_SIGNATURE_APP_ROOT
SIGNATURE_DOCUMENT_ROOTS = (
    APP_ROOT / 'exports',
    APP_ROOT / 'storage' / 'uploads',
)
localsql_path = os.path.join(current_dir, 'localSQLtesting')
prirodnjacki_path = os.path.join(current_dir, 'PrirodnjackiMuzej')

sys.path.insert(0, localsql_path)
sys.path.insert(0, prirodnjacki_path)

# Authentication system integration
auth_available = False
db_manager = None

# Load configuration
config_name = os.environ.get('FLASK_ENV', 'production')
app_config = get_config(config_name)

# Create Flask app
app = Flask(__name__)
app.config.from_object(app_config)
app_config.init_app(app)
init_observability(app)

def apply_shared_system_settings(saved_settings):
    """Apply persisted system/security settings to the current Flask process."""
    if not saved_settings:
        return

    if 'min_password_length' in saved_settings:
        app.config['PASSWORD_MIN_LENGTH'] = saved_settings['min_password_length']
        password_validator.min_length = saved_settings['min_password_length']
    if 'max_login_attempts' in saved_settings:
        app.config['MAX_LOGIN_ATTEMPTS'] = saved_settings['max_login_attempts']
    if 'lockout_duration' in saved_settings:
        app.config['ACCOUNT_LOCKOUT_DURATION'] = int(saved_settings['lockout_duration']) * 60
    if 'session_timeout' in saved_settings:
        from datetime import timedelta as _td
        app.config['PERMANENT_SESSION_LIFETIME'] = _td(minutes=int(saved_settings['session_timeout']))
    if 'require_special_chars' in saved_settings:
        app.config['PASSWORD_REQUIRE_SPECIAL'] = saved_settings['require_special_chars']
        password_validator.require_special = bool(saved_settings['require_special_chars'])


app.apply_shared_system_settings = apply_shared_system_settings


def shared_settings_db_enabled(flask_app):
    """Return True when this runtime should use PostgreSQL-backed shared settings."""
    return bool(os.environ.get('DATABASE_URL')) and not flask_app.config.get('TESTING', False)


@app.before_request
def refresh_shared_runtime_settings():
    """Refresh shared security settings from PostgreSQL-backed storage."""
    if not shared_settings_db_enabled(app):
        return
    try:
        apply_shared_system_settings(admin_system_views.load_saved_settings())
    except Exception as exc:
        logging.getLogger(__name__).warning("Could not refresh shared system settings: %s", exc)


def auth_version_check_enabled(flask_app):
    """Gejt opoziva sesija — namerno ODVOJEN od shared_settings_db_enabled,
    da testovi koji simuliraju prod za deljena podešavanja ne uvuku i
    opoziv (sintetičke sesije bez auth_version bi padale)."""
    return bool(os.environ.get('DATABASE_URL')) and not flask_app.config.get('TESTING', False)


@app.before_request
def enforce_session_auth_version():
    """Opoziv sesije: deaktivacija/promena uloge/lozinke podiže users.auth_version,
    pa sesija sa starom verzijom pada odmah umesto da živi do isteka."""
    if not auth_version_check_enabled(app):
        return None
    return validate_session_auth_version()

# Trust proxy headers from nginx (1 proxy hop)
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)


def configure_session_storage(flask_app):
    """Configure the Flask-Session backend for the selected runtime."""
    session_type = (flask_app.config.get('SESSION_TYPE') or 'filesystem').lower()
    flask_app.config['SESSION_TYPE'] = session_type

    base_prefix = str(flask_app.config.get('SESSION_KEY_PREFIX') or 'museum:')
    flask_app.config['SESSION_KEY_PREFIX_BASE'] = base_prefix
    invalidate_on_restart = str(
        flask_app.config.get(
            'SESSION_INVALIDATE_ON_RESTART',
            os.environ.get('SESSION_INVALIDATE_ON_RESTART', 'False'),
        )
    ).strip().lower() == 'true'
    flask_app.config['SESSION_INVALIDATE_ON_RESTART'] = invalidate_on_restart

    boot_id = str(flask_app.config.get('SESSION_BOOT_ID') or os.environ.get('SESSION_BOOT_ID') or '').strip()
    if invalidate_on_restart and boot_id:
        normalized_prefix = base_prefix if base_prefix.endswith(':') else f'{base_prefix}:'
        flask_app.config['SESSION_BOOT_ID'] = boot_id
        # Namespace session records per app boot so a full restart invalidates old logins.
        flask_app.config['SESSION_KEY_PREFIX'] = f'{normalized_prefix}boot:{boot_id}:'

    if session_type == 'filesystem':
        session_dir = flask_app.config.get('SESSION_FILE_DIR')
        if session_dir:
            os.makedirs(session_dir, exist_ok=True)
        return

    if session_type != 'redis':
        raise RuntimeError(f"Unsupported SESSION_TYPE: {session_type}")

    redis_url = flask_app.config.get('REDIS_URL')
    if not redis_url:
        raise RuntimeError('REDIS_URL is required when SESSION_TYPE=redis')
    if not REDIS_CLIENT_AVAILABLE:
        raise RuntimeError('redis package is required when SESSION_TYPE=redis')

    session_redis = redis_client_lib.from_url(redis_url)
    session_redis.ping()
    flask_app.config['SESSION_REDIS'] = session_redis


def initialize_shared_state(flask_app):
    """Initialize shared-state clients used by the web tier."""
    global _login_tracker_initialized

    ratelimit_storage = str(flask_app.config.get('RATELIMIT_STORAGE_URL', ''))
    redis_url = None
    if flask_app.config.get('SESSION_TYPE') == 'redis' or ratelimit_storage.startswith('redis'):
        redis_url = flask_app.config.get('REDIS_URL')
    if not redis_url:
        return login_tracker

    init_login_tracker(redis_url)
    _login_tracker_initialized = True
    return login_tracker

# Initialize security extensions
# IMPORTANT: Session must be initialized BEFORE CSRF
configure_session_storage(app)
Session(app)
csrf = CSRFProtect(app)

# Flask-Babel configuration
app.config['BABEL_DEFAULT_LOCALE'] = 'sr_Cyrl'
# English soft-removed 2026-07-08 — Serbian only (Cyrillic + Latin). A legacy
# 'en' preference falls back to Cyrillic via the .get default below.
app.config['BABEL_SUPPORTED_LOCALES'] = ['sr_Cyrl', 'sr_Latn']

def get_locale():
    """Select locale from session, cookie, or Accept-Language header."""
    # Check session first
    lang = session.get('museum_lang')
    if lang:
        locale_map = {'sr-Cyrl': 'sr_Cyrl', 'sr-Latn': 'sr_Latn'}
        return locale_map.get(lang, 'sr_Cyrl')
    # Check cookie
    lang = request.cookies.get('museum_lang')
    if lang:
        locale_map = {'sr-Cyrl': 'sr_Cyrl', 'sr-Latn': 'sr_Latn'}
        return locale_map.get(lang, 'sr_Cyrl')
    return 'sr_Cyrl'

babel = Babel(app, locale_selector=get_locale)

app.register_blueprint(archive_signature_bp)
app.register_blueprint(approval_center_bp)
app.register_blueprint(documents_bp)
app.register_blueprint(fototeka_bp)
app.register_blueprint(kr_dosije_bp)
app_blueprint_support.register_standard_blueprints(
    app,
    {
        'projects': projects_bp,
        'qr': qr_bp,
        'mail': mail_bp,
        'chat': chat_bp,
        'vehicles': vehicles_bp,
        'science': science_bp,
        'maps': maps_bp,
        'content': content_bp,
        'travel_finance': travel_finance_bp,
        'timesheet': timesheet_bp,
        'admin': admin_bp,
        'collections': collections_bp,
        'media': media_bp,
        'mineral_science': mineral_science_bp,
        'core': core_bp,
    },
)
app_blueprint_support.apply_blueprint_aliases(app)
app_blueprint_support.apply_csrf_exemptions(app, csrf)


@app.errorhandler(413)
def handle_request_entity_too_large(error):
    """A request over MAX_CONTENT_LENGTH (or nginx client_max_body_size) is
    rejected before the view runs. The Фototeka uploader posts one file at a
    time to /fototeka/upload/jedan and expects JSON, so return a clean message
    instead of the default HTML page it would surface as a generic 'server
    error'."""
    if request.path.rstrip('/').endswith('/upload/jedan') or request.path.startswith('/api/'):
        return jsonify({'ok': False, 'error': 'Датотека је превелика за отпремање.'}), 413
    flash('Датотека је превелика за отпремање.', 'danger')
    return redirect(request.referrer or url_for('dashboard'))

# CLI: flask reset-test-data (praznjenje probnih podataka pred user testiranje)
import reset_test_data as reset_test_data_cli
reset_test_data_cli.register_cli(app)

# CLI: flask cleanup-empty-july-drafts (ciscenje praznih julskih DRAFT listi)
import cleanup_empty_july_drafts as cleanup_empty_july_drafts_cli
cleanup_empty_july_drafts_cli.register_cli(app)

# CLI: flask populate-lokaliteti / export-lokaliteti (sifarnik lokaliteta)
import lokaliteti_cli
lokaliteti_cli.register_cli(app)

# CLI: flask povezi-fotografije (retroaktivno vezivanje uvezenih fotografija)
import povezi_fotografije_cli
povezi_fotografije_cli.register_cli(app)

# CLI: flask obrisi-legacy-slike (brisanje starog `images` skladista)
import obrisi_legacy_slike_cli
obrisi_legacy_slike_cli.register_cli(app)

# CLI: flask uvezi-kr-dosije <putanja> (uvoz konzervatorskog xlsx + slika)
import kr_dosije_cli
kr_dosije_cli.register_cli(app)

# CLI: flask uvezi-arhivske-liste <folder> (masovni arhivski uvoz radnih listi)
import uvezi_arhivske_liste_cli
uvezi_arhivske_liste_cli.register_cli(app)

# CLI: flask uskladi-knjigu-depo (usaglašavanje inventarske knjige i baze minerala)
import uskladi_knjiga_depo_cli
uskladi_knjiga_depo_cli.register_cli(app)

# CLI: flask ocisti-kolicine (čišćenje minerals.quantity iz originala u knjizi)
import ciscenje_kolicina_cli
ciscenje_kolicina_cli.register_cli(app)

# Preserve a few legacy module-level symbols that tests and utility code still
# reference directly, even though their routes now live in blueprints.
globals().update(
    app_blueprint_support.bind_legacy_view_symbols(
        app,
        ('get_image_by_id',),
    )
)

# Initialize rate limiter (shared instance from rate_limit_ext; blueprints
# attach @limiter.limit decorators on it without importing app).
app.config.setdefault(
    'RATELIMIT_STORAGE_URI',
    app.config.get('RATELIMIT_STORAGE_URL', 'memory://'),
)
limiter.init_app(app)

app_blueprint_support.apply_endpoint_rate_limits(app, limiter)

# Initialize logger early (needed for security initialization messages)
logger = logging.getLogger(__name__)

LazyServiceProxy = app_core_support.LazyServiceProxy


def build_auth_system():
    """Create the PostgreSQL auth backend only when first needed."""
    global auth_available

    if not os.environ.get('DATABASE_URL'):
        auth_available = False
        return None

    try:
        from postgres_auth import get_postgres_auth

        service = get_postgres_auth()
        auth_available = bool(service and service.available)
        if auth_available:
            logger.info("✓ PostgreSQL authentication backend ready")
        else:
            logger.info("ℹ️ PostgreSQL authentication unavailable, fallback auth remains active")
        return service
    except Exception as exc:
        auth_available = False
        logger.error("PostgreSQL auth initialization failed: %s", exc)
        return None


def build_timesheet_repository():
    """Create the timesheet repository only when a timesheet route needs it."""
    db_url = os.environ.get('DATABASE_URL')
    if not db_url:
        return None
    return TimesheetRepository(db_url)


# Mail cache is built on-demand when users access the mail page.
# The background sync thread (_bg_sync_worker in mail_client.py) keeps it fresh.

# Initialize security headers with Flask-Talisman
if TALISMAN_AVAILABLE:
    # Content Security Policy - configured for museum application
    csp = {
        'default-src': "'self'",
        'script-src': [
            "'self'",
            "'unsafe-inline'",  # Required for inline scripts in templates
            "'unsafe-eval'",    # Required for some JS libraries
            "cdn.jsdelivr.net",
            "cdnjs.cloudflare.com",
            "unpkg.com",
            "cdn.plot.ly",      # Plotly.js for 3D terrain
            # Facebook/SnapWidget JS SDK више се НЕ учитава на нашој страни —
            # друштвене мреже иду кроз sandbox iframe (види frame-src). Зато
            # нема facebook/snapwidget у script-src (мање напада, чистија конзола).
        ],
        'style-src': [
            "'self'",
            "'unsafe-inline'",  # Required for inline styles
            "cdn.jsdelivr.net",
            "cdnjs.cloudflare.com",
            "fonts.googleapis.com",
            "unpkg.com",
        ],
        'font-src': [
            "'self'",
            "fonts.gstatic.com",
            "cdn.jsdelivr.net",
        ],
        'img-src': [
            "'self'",
            "data:",
            "blob:",
            "*.openstreetmap.org",
            "*.tile.openstreetmap.org",
            # Једина сврха: мала слика (favicon) којом табла проверава ДОСТИЖНОСТ
            # Facebook-а пре уграђивања iframe-а (graceful fallback). Без овога би
            # блокирана провера сама била CSP-грешка на НАШЕМ origin-у. FB feed
            # слике се учитавају унутар facebook iframe-а (њихов origin), не овде.
            "www.facebook.com",
            "nhmbeo.rs",
            "*.nhmbeo.rs",
            "www.nhmbeo.rs",
        ],
        'connect-src': [
            "'self'",
            "blob:",
            "localhost:11434",  # Ollama API
            "api.open-meteo.com",
            "cdn.plot.ly",
            "cdnjs.cloudflare.com",
            "cdn.jsdelivr.net",
            "unpkg.com",
        ],
        'worker-src': [
            "'self'",
            "blob:",
        ],
        'frame-src': [
            # Једина facebook дозвола: уграђивање Facebook page plugin-а у
            # sandbox iframe на табли. Минимум потребан да iframe ради.
            "'self'",
            "www.facebook.com",
            "*.facebook.com",
        ],
        'frame-ancestors': "'self'",
        'form-action': "'self'",
    }

    # Initialize Talisman with appropriate settings
    talisman = Talisman(
        app,
        # Force HTTPS only in production
        force_https=app.config.get('SESSION_COOKIE_SECURE', False),
        # Keep session cookie flags aligned with the active Flask config.
        session_cookie_secure=app.config.get('SESSION_COOKIE_SECURE', False),
        session_cookie_http_only=app.config.get('SESSION_COOKIE_HTTPONLY', True),
        session_cookie_samesite=app.config.get('SESSION_COOKIE_SAMESITE', 'Lax'),
        # Strict Transport Security (HSTS)
        strict_transport_security=True,
        strict_transport_security_max_age=31536000,  # 1 year
        strict_transport_security_include_subdomains=True,
        # Content Security Policy
        content_security_policy=csp,
        # Note: Nonces disabled because templates use inline scripts without csp_nonce()
        # To enable nonces later, update templates to use {{ csp_nonce() }} on script tags
        content_security_policy_nonce_in=[],
        # Additional security headers
        x_content_type_options=True,
        x_xss_protection=True,
        # Allow frames for same origin (needed for some features)
        frame_options='SAMEORIGIN',
        # Referrer policy
        referrer_policy='strict-origin-when-cross-origin',
    )
    logger.debug("Flask-Talisman security headers enabled")
else:
    logger.debug("Flask-Talisman not available - security headers disabled")

# Initialize password utilities (use app_config object, not app.config dict)
password_validator = PasswordValidator(app_config)
password_hasher = PasswordHasher()

auth_system = LazyServiceProxy(build_auth_system, 'authentication service')
timesheet_repository = LazyServiceProxy(build_timesheet_repository, 'timesheet repository')
_login_tracker_initialized = False
_fallback_auth_warning_logged = False
initialize_shared_state(app)
apply_shared_system_settings(admin_system_views.load_saved_settings())

# Module access configuration
# NOTE: This controls dashboard widgets only. Navigation menu remains unchanged.
MODULE_ACCESS = {
    'timesheet': {
        'name': 'Систем за радне листе',
        'description': 'Унос и управљање радним листама',
        'icon': 'bi-calendar-check',
        'default_access': True,  # Everyone has access by default
        'restricted_users': []   # No restrictions
    },
    'dokumenti': {
        'name': 'Документа',
        'description': 'Складиштење, преглед и одобравање докумената',
        'icon': 'bi-folder2-open',
        'default_access': True,  # Everyone has access by default
        'restricted_users': []   # No restrictions
    },
    'fototeka': {
        'name': 'Фототека',
        'description': 'Фотографије музеја — прегледи, тагови и везе',
        'icon': 'bi-camera',
        'default_access': True,  # Everyone has access by default
        'restricted_users': []   # No restrictions
    },
    'kr_dosije': {
        'name': 'К-Р досије',
        'description': 'Конзерваторско-рестаураторски досијеи о захватима на предметима',
        'icon': 'bi-clipboard2-pulse',
        'default_access': False,  # Restricted: конзерватори + шефови + директор/админ
        'authorized_users': [
            'nenad.mladenovic@nhmbeo.rs',   # конзерватор, геолошко одељење
            'gorana.petkovski@nhmbeo.rs',   # конзерватор, биолошко одељење
        ]
    },
    'museum_databases': {
        'name': 'Музејске базе података',
        'description': 'Преглед свих музејских база података',
        'icon': 'bi-database',
        'default_access': False,  # Restricted access
        'authorized_users': [
            'aca.lukovic@nhmbeo.rs',
            'admin',
            'slavko.spasic@nhmbeo.rs',
            'biljana.mitrovic@nhmbeo.rs',
            'verica.stojanovic@nhmbeo.rs'
        ]
    },
    'mineral_database': {
        'name': 'База минерала',
        'description': 'Колекција минерала - 5.997 примерака',
        'icon': 'bi-gem',
        'default_access': False,  # Restricted access
        'authorized_users': [
            'aca.lukovic@nhmbeo.rs',
            'admin',
            'slavko.spasic@nhmbeo.rs',
            'biljana.mitrovic@nhmbeo.rs'
        ]
    },
    'botany_collection': {
        'name': 'Ботаничка збирка',
        'description': 'Специјализована ботаничка база',
        'icon': 'bi-flower1',
        'default_access': False,
        'authorized_users': ['admin']
    },
    'ichthyology_collection': {
        'name': 'Ихтиолошка збирка',
        'description': 'Специјализована ихтиолошка база',
        'icon': 'museum-icon-fish',
        'default_access': False,
        'authorized_users': ['admin']
    },
    'entomology_collection': {
        'name': 'Ентомолошка збирка',
        'description': 'Специјализована ентомолошка база',
        'icon': 'bi-bug',
        'default_access': False,
        'authorized_users': ['admin']
    },
    'mycology_collection': {
        'name': 'Миколошка збирка',
        'description': 'Специјализована миколошка база',
        'icon': 'museum-icon-mushroom',
        'default_access': False,
        'authorized_users': ['admin']
    },
    'herpetology_collection': {
        'name': 'Херпетолошка збирка',
        'description': 'Специјализована херпетолошка база',
        'icon': 'museum-icon-snake',
        'default_access': False,
        'authorized_users': ['admin']
    },
    'ornithology_collection': {
        'name': 'Орнитолошка збирка',
        'description': 'Специјализована орнитолошка база',
        'icon': 'museum-icon-bird',
        'default_access': False,
        'authorized_users': ['admin']
    },
    'paleozoology_collection': {
        'name': 'Палеозоолошка збирка',
        'description': 'Специјализована палеозоолошка база',
        'icon': 'museum-icon-dinosaur',
        'default_access': False,
        'authorized_users': ['admin']
    },
    'sanja_paleogene_neogene_mammals': {
        'name': 'Крупни сисари палеогена и неогена',
        'description': 'Санјина база крупних сисара палеогена и неогена',
        'icon': 'museum-icon-dinosaur',
        'default_access': False,
        'authorized_users': ['admin']
    },
    'paleobotany_collection': {
        'name': 'Палеоботаничка збирка',
        'description': 'Специјализована палеоботаничка база',
        'icon': 'bi-flower2',
        'default_access': False,
        'authorized_users': ['admin']
    },
    'petrology_collection': {
        'name': 'Петролошка збирка',
        'description': 'Специјализована петролошка база',
        'icon': 'bi-bricks',
        'default_access': False,
        'authorized_users': ['admin']
    },
    'meteorite_collection': {
        'name': 'Збирка метеорита',
        'description': 'Специјализована база метеорита',
        'icon': 'museum-icon-shooting-star',
        'default_access': False,
        'authorized_users': ['admin']
    },
    'employees_database': {
        'name': 'База запослених',
        'description': 'Преглед свих 42 запослених музеја',
        'icon': 'bi-people-fill',
        'default_access': False,
        'authorized_users': ['admin', 'slavko.spasic@nhmbeo.rs']
    },
    'employee_profiles': {
        'name': 'Профили запослених',
        'description': 'Детаљне биографије запослених',
        'icon': 'bi-person-badge',
        'default_access': False,
        'authorized_users': ['admin', 'slavko.spasic@nhmbeo.rs']
    },
    'library_database': {
        'name': 'База библиотеке',
        'description': 'Каталог књига - 22.000+ јединица',
        'icon': 'bi-book',
        'default_access': False,
        'authorized_users': ['admin', 'biblioteka@nhmbeo.rs']
    },
    'exhibits_database': {
        'name': 'База експоната',
        'description': 'Каталог музејских експоната и стање артефаката',
        'icon': 'bi-collection',
        'default_access': False,
        'authorized_users': ['admin', 'slavko.spasic@nhmbeo.rs']
    },
    'exhibitions_database': {
        'name': 'База изложби',
        'description': 'Историјат галеријских изложби и аналитика посета',
        'icon': 'bi-easel',
        'default_access': False,
        'authorized_users': ['admin', 'slavko.spasic@nhmbeo.rs', 'draganav@nhmbeo.rs']
    },
    'news': {
        'name': 'Музејске вести',
        'description': 'Вести и објаве о активностима музеја',
        'icon': 'bi-newspaper',
        'default_access': True,  # Everyone can view news
        'restricted_users': []
    },
    'news_edit': {
        'name': 'Уређивање музејских вести',
        'description': ('Унос и измена вести, освежавање са сајта и преглед '
                        'вести нађених на вебу. Читање вести је одвојено '
                        'право („Музејске вести") које сви имају.'),
        'icon': 'bi-pencil-square',
        'default_access': False,
        'authorized_users': ['admin']
    },
    'cultural_heritage': {
        'name': 'Заштићена културна добра',
        'description': 'Регистар културних добара под заштитом',
        'icon': 'bi-award',
        'default_access': False,
        'authorized_users': ['admin', 'slavko.spasic@nhmbeo.rs']
    },
    'curator_collections': {
        'name': 'Кустоске збирке',
        'description': '13 специјализованих збирки',
        'icon': 'bi-collection',
        'default_access': False,
        'authorized_users': [
            'admin',
            'aca.lukovic@nhmbeo.rs',
            'slavko.spasic@nhmbeo.rs',
            'biljana.mitrovic@nhmbeo.rs',
            'verica.stojanovic@nhmbeo.rs'
        ]
    },
    'user_management': {
        'name': 'Управљање корисницима',
        'description': 'Додавање и управљање корисничким налозима',
        'icon': 'bi-people',
        'default_access': False,
        'authorized_users': ['admin']
    },
    'reports_analytics': {
        'name': 'Извештаји и аналитика',
        'description': 'Статистика и извештаји система',
        'icon': 'bi-graph-up',
        'default_access': False,
        'authorized_users': ['admin', 'slavko.spasic@nhmbeo.rs']
    },
    'system_logs': {
        'name': 'Системски логови',
        'description': 'Преглед активности корисника',
        'icon': 'bi-shield-check',
        'default_access': False,
        'authorized_users': ['admin']
    },
    'bird_ringing_database': {
        'name': 'База прстеновања птица',
        'description': 'Комплетна база података о прстенованим птицама - 157.115 записа',
        'icon': 'bi-feather',
        'default_access': False,
        'authorized_users': ['admin', 'vuk.popic@nhmbeo.rs']
    },
    'nhm_data_portal': {
        'name': 'NHM London Data Portal',
        'description': 'Приступ базама Природњачког музеја у Лондону - 286 датасетова, 35+ милиона записа',
        'icon': 'bi-globe-europe-africa',
        'default_access': False,
        'authorized_users': ['admin', 'aca.lukovic@nhmbeo.rs', 'slavko.spasic@nhmbeo.rs', 'biljana.mitrovic@nhmbeo.rs']
    },
    'maps_karte': {
        'name': 'Географске карте',
        'description': 'Интерактивне географске карте Србије',
        'icon': 'bi-map',
        'default_access': False,
        'authorized_users': ['admin', 'aca.lukovic@nhmbeo.rs']
    },
    'bilja_kenozojske_invertebrate': {
        'name': 'Кенозојски инвертебрати',
        'description': 'Фосилни инвертебрати (квартар/дилувијум) — палеозоолошка збирка.',
        'icon': 'museum-icon-dinosaur',
        'default_access': False,
        'authorized_users': ['admin']
    },
    'bilja_hydrobioidea_radoman': {
        'name': 'Hydrobioidea — збирка П. Радомана',
        'description': 'Рецентни гастроподи (слатководни/бракични), тип-примерци.',
        'icon': 'museum-icon-snail',
        'default_access': False,
        'authorized_users': ['admin']
    },
    'bilja_suvozemni_puzevi_pavlovic': {
        'name': 'Сувоземни пужеви — П. С. Павловић',
        'description': 'Рецентни копнени гастроподи, збирка П. С. Павловића.',
        'icon': 'museum-icon-snail',
        'default_access': False,
        'authorized_users': ['admin']
    },
    'bilja_opsta_zbirka_mollusca': {
        'name': 'Општа збирка мекушаца',
        'description': 'Општа збирка мекушаца (Bivalvia + Gastropoda).',
        'icon': 'museum-icon-shell',
        'default_access': False,
        'authorized_users': ['admin']
    },
    'bilja_skoljke_tadic': {
        'name': 'Збирка шкољки — А. Тадић',
        'description': 'Рецентни слатководни бивалви (Unio и др.).',
        'icon': 'museum-icon-shell',
        'default_access': False,
        'authorized_users': ['admin']
    },
    'bilja_recentni_morski_mekusci': {
        'name': 'Рецентни морски мекушци',
        'description': 'Рецентни морски мекушци (Bivalvia + Gastropoda).',
        'icon': 'museum-icon-shell',
        'default_access': False,
        'authorized_users': ['admin']
    }
}
MODULE_ACCESS_DEFAULTS = deepcopy(MODULE_ACCESS)

# Module access persistence
MODULE_ACCESS_FILE = 'data/module_access.json'
_module_access_mtime = None
_module_access_loaded_at = None
_dashboard_prefs_loaded_at = None
_SHARED_STATE_CACHE_TTL_SECONDS = float(os.environ.get('RUNTIME_SHARED_STATE_CACHE_TTL_SECONDS', '60'))


def _get_file_mtime(path: str):
    """Return the current file mtime, or None when the file is absent."""
    return app_runtime_support.get_file_mtime(path)


def load_module_access(force: bool = False):
    """Load module access settings from JSON file."""
    global MODULE_ACCESS, _module_access_mtime, _module_access_loaded_at

    current_mtime = _get_file_mtime(MODULE_ACCESS_FILE)
    use_shared_db = shared_settings_db_enabled(app)
    now = time.time()
    if (
        use_shared_db
        and not force
        and _module_access_loaded_at is not None
        and (now - _module_access_loaded_at) < _SHARED_STATE_CACHE_TTL_SECONDS
    ):
        return MODULE_ACCESS
    MODULE_ACCESS, _module_access_mtime = app_runtime_support.load_module_access_state(
        current_state=MODULE_ACCESS,
        stored_mtime=_module_access_mtime,
        file_mtime=current_mtime,
        force=force,
        use_shared_db=use_shared_db,
        module_access_file=MODULE_ACCESS_FILE,
        module_access_defaults=MODULE_ACCESS_DEFAULTS,
        get_postgres_connection=get_postgres_connection,
        load_module_access_data=module_access_support.load_module_access_data,
    )
    _module_access_loaded_at = now if use_shared_db else None
    return MODULE_ACCESS

def save_module_access():
    """Save module access settings to JSON file."""
    global _module_access_mtime, _module_access_loaded_at
    use_shared_db = shared_settings_db_enabled(app)
    saved, updated_mtime = app_runtime_support.save_module_access_state(
        module_access_file=MODULE_ACCESS_FILE,
        module_access=MODULE_ACCESS,
        use_shared_db=use_shared_db,
        get_postgres_connection=get_postgres_connection,
        save_module_access_data=module_access_support.save_module_access_data,
        get_file_mtime_func=_get_file_mtime,
    )
    if saved:
        _module_access_mtime = updated_mtime
        _module_access_loaded_at = time.time() if use_shared_db else None
        return True
    return False

# Dashboard widget preferences (per user)
# Admins can customize which widgets appear on their dashboard
# Dashboard preferences file
DASHBOARD_PREFS_FILE = 'data/dashboard_preferences.json'

# Default dashboard preferences
_DEFAULT_DASHBOARD_PREFS = {
    'admin': {'enabled_widgets': ['museum_databases']},
    'slavko.spasic@nhmbeo.rs': {'enabled_widgets': ['museum_databases']},
    'biljana.mitrovic@nhmbeo.rs': {'enabled_widgets': ['museum_databases']},
    'verica.stojanovic@nhmbeo.rs': {'enabled_widgets': ['museum_databases']}
}

DASHBOARD_PREFERENCES = deepcopy(_DEFAULT_DASHBOARD_PREFS)
_dashboard_prefs_mtime = None


def load_dashboard_preferences(force: bool = False):
    """Load dashboard preferences from JSON file."""
    global DASHBOARD_PREFERENCES, _dashboard_prefs_mtime, _dashboard_prefs_loaded_at

    current_mtime = _get_file_mtime(DASHBOARD_PREFS_FILE)
    use_shared_db = shared_settings_db_enabled(app)
    now = time.time()
    DASHBOARD_PREFERENCES, _dashboard_prefs_mtime = (
        app_runtime_support.load_dashboard_preferences_state(
            current_state=DASHBOARD_PREFERENCES,
            stored_mtime=_dashboard_prefs_mtime,
            file_mtime=current_mtime,
            force=force,
            use_shared_db=use_shared_db,
            dashboard_prefs_file=DASHBOARD_PREFS_FILE,
            default_prefs=_DEFAULT_DASHBOARD_PREFS,
            get_postgres_connection=get_postgres_connection,
            load_dashboard_preferences_data=module_access_support.load_dashboard_preferences_data,
        )
    )
    _dashboard_prefs_loaded_at = now if use_shared_db else None
    return DASHBOARD_PREFERENCES

def save_dashboard_preferences():
    """Save dashboard preferences to JSON file."""
    global _dashboard_prefs_mtime, _dashboard_prefs_loaded_at
    use_shared_db = shared_settings_db_enabled(app)
    saved, updated_mtime = app_runtime_support.save_dashboard_preferences_state(
        dashboard_prefs_file=DASHBOARD_PREFS_FILE,
        dashboard_preferences=DASHBOARD_PREFERENCES,
        use_shared_db=use_shared_db,
        get_postgres_connection=get_postgres_connection,
        save_dashboard_preferences_data=module_access_support.save_dashboard_preferences_data,
        get_file_mtime_func=_get_file_mtime,
    )
    if saved:
        _dashboard_prefs_mtime = updated_mtime
        _dashboard_prefs_loaded_at = time.time() if use_shared_db else None
        return True
    return False

def user_has_module_access(user_email, user_role, module_key):
    """Check if user has access to specific module."""
    resolved_module_access = None
    resolved_employee_directory = None
    if has_request_context():
        resolved_module_access = getattr(g, '_module_access_cache', None)
        if resolved_module_access is None:
            resolved_module_access = load_module_access()
            g._module_access_cache = resolved_module_access
        resolved_employee_directory = getattr(g, '_employee_directory_cache', None)
        if resolved_employee_directory is None:
            resolved_employee_directory = get_employee_directory()
            g._employee_directory_cache = resolved_employee_directory
    return app_access_support.user_has_module_access(
        user_email,
        user_role,
        module_key,
        load_module_access=load_module_access,
        module_access=MODULE_ACCESS,
        get_employee_directory=get_employee_directory,
        resolved_module_access=resolved_module_access,
        resolved_employee_directory=resolved_employee_directory,
    )


app.user_has_module_access = user_has_module_access


current_user_is_admin = app_core_support.current_user_is_admin
can_access_owned_record = app_core_support.can_access_owned_record


def ensure_login_tracker_initialized():
    """Initialize the shared login tracker lazily when auth routes need it."""
    global _login_tracker_initialized
    tracker, _login_tracker_initialized = app_access_support.ensure_login_tracker_initialized(
        initialized=_login_tracker_initialized,
        is_initialized=lambda: _login_tracker_initialized,
        login_tracker=login_tracker,
        flask_app=app,
        initialize_shared_state=initialize_shared_state,
        init_login_tracker=init_login_tracker,
    )
    return login_tracker


def log_fallback_auth_warning_once():
    """Log the fallback-auth warning once per process when it is actually used."""
    global _fallback_auth_warning_logged
    _fallback_auth_warning_logged = app_access_support.log_fallback_auth_warning_once(
        already_logged=_fallback_auth_warning_logged,
        app_config=app.config,
        logger=logger,
    )

def get_user_modules(user_email, user_role):
    """Get list of modules user has access to, filtered by dashboard preferences."""
    return app_ui_support.get_user_modules(
        user_email,
        user_role,
        load_module_access=load_module_access,
        load_dashboard_preferences=load_dashboard_preferences,
        dashboard_preferences=DASHBOARD_PREFERENCES,
        module_access=MODULE_ACCESS,
        user_has_module_access=user_has_module_access,
    )

def load_user_dashboard_elements(user_email):
    """Load the per-user dashboard element selection from PostgreSQL."""
    return dashboard_config_support.load_user_dashboard_elements(user_email)

def save_user_dashboard_elements(user_email, elements):
    """Save the per-user dashboard element selection to PostgreSQL."""
    return dashboard_config_support.save_user_dashboard_elements(user_email, elements)

def get_user_dashboard_view(user_email, user_role):
    """Get dashboard sections and module cards enabled for the user."""
    return app_ui_support.get_user_dashboard_view(
        user_email,
        user_role,
        load_module_access=load_module_access,
        load_dashboard_preferences=load_dashboard_preferences,
        user_has_module_access=user_has_module_access,
        load_saved_elements=load_user_dashboard_elements,
    )

def get_fallback_employees():
    """Return fallback employee data for development/testing only."""
    return fallback_auth_support.get_fallback_employees(app.config)

# Initialize fallback employees lazily
MUSEUM_EMPLOYEES = None


def get_museum_employees():
    """Return fallback employee records, loading them only when needed."""
    global MUSEUM_EMPLOYEES
    MUSEUM_EMPLOYEES = app_runtime_support.get_cached_value(
        current_value=MUSEUM_EMPLOYEES,
        force_reload=False,
        loader=get_fallback_employees,
    )
    return MUSEUM_EMPLOYEES

# Library Database - will be loaded from JSON}

# Library Database - loaded from PostgreSQL (Phase 3A)
LIBRARY_DATABASE = None
EMPLOYEE_DIRECTORY = None

def load_library_database():
    """Load library database from PostgreSQL."""
    return app_data_support.load_library_database_data(
        library_path=os.path.join('data', 'library_database.json'),
        database_url=os.environ.get('DATABASE_URL'),
        phase3a_databases=globals().get('phase3a_databases'),
        museum_staff_support=museum_staff_support,
    )

def save_library_database():
    """Save library database to JSON file."""
    global LIBRARY_DATABASE
    if LIBRARY_DATABASE is None:
        return

    app_data_support.save_library_database_data(
        library_path=os.path.join('data', 'library_database.json'),
        library_database=LIBRARY_DATABASE,
        museum_staff_support=museum_staff_support,
    )

def get_library_database():
    """Return the cached library database, loading it if needed."""
    global LIBRARY_DATABASE
    LIBRARY_DATABASE = app_runtime_support.get_cached_value(
        current_value=LIBRARY_DATABASE,
        force_reload=False,
        loader=load_library_database,
    )
    return LIBRARY_DATABASE

def load_employee_directory():
    """Load employee directory from PostgreSQL or JSON fallback."""
    return app_data_support.load_employee_directory_data(
        directory_path=os.path.join('data', 'employee_directory.json'),
        database_url=os.environ.get('DATABASE_URL'),
        phase3a_databases=globals().get('phase3a_databases'),
        museum_staff_support=museum_staff_support,
    )

def get_employee_directory():
    """Return cached employee directory."""
    global EMPLOYEE_DIRECTORY
    EMPLOYEE_DIRECTORY = app_runtime_support.get_cached_value(
        current_value=EMPLOYEE_DIRECTORY,
        force_reload=False,
        loader=load_employee_directory,
    )
    return EMPLOYEE_DIRECTORY


LazyLoadedDict = app_core_support.LazyLoadedDict

def load_exhibitions_data():
    """Load exhibitions from PostgreSQL or JSON fallback."""
    return app_data_support.load_exhibitions_data(
        database_url=os.environ.get('DATABASE_URL'),
        phase3a_databases=globals().get('phase3a_databases'),
        museum_content_support=museum_content_support,
    )


def load_news_data():
    """Load news articles from PostgreSQL or JSON fallback."""
    return app_data_support.load_news_data(
        database_url=os.environ.get('DATABASE_URL'),
        phase3a_databases=globals().get('phase3a_databases'),
        museum_content_support=museum_content_support,
    )


def build_exhibitions_database():
    """Build the exhibition cache payload on demand."""
    return app_data_support.build_exhibitions_database(
        load_exhibitions_data=load_exhibitions_data,
        museum_content_support=museum_content_support,
    )


def build_news_database():
    """Build the news cache payload on demand."""
    return app_data_support.build_news_database(
        load_news_data=load_news_data,
        museum_content_support=museum_content_support,
    )


EXHIBITS_DATABASE = museum_content_support.EXHIBITS_DATABASE

EXHIBITIONS_DATABASE = LazyLoadedDict(build_exhibitions_database, 'exhibitions database')
NEWS_DATABASE = LazyLoadedDict(build_news_database, 'news database')


def get_exhibit_statistics():
    """Aggregate exhibit metrics from the artifacts dataset."""
    return app_data_support.get_exhibit_statistics(
        exhibits_database=EXHIBITS_DATABASE,
        museum_content_support=museum_content_support,
    )


def get_exhibition_statistics():
    """Aggregate exhibition metrics for dashboard and detail views."""
    return app_data_support.get_exhibition_statistics(
        exhibitions_database=EXHIBITIONS_DATABASE,
        current_year=datetime.now().year,
        museum_content_support=museum_content_support,
    )

# Curator collection bootstrap data and loaders live in a dedicated support module.
_collection_bootstrap_support = collection_bootstrap_support.CollectionBootstrapSupport(
    lazy_loaded_dict_cls=LazyLoadedDict,
    database_url=os.environ.get('DATABASE_URL'),
    phase3a_databases=phase3a_databases if os.environ.get('DATABASE_URL') else None,
)

load_collection_database = _collection_bootstrap_support.load_collection_database
BOTANY_COLLECTION_DATABASE = _collection_bootstrap_support.botany_collection_database
ICHTHYOLOGY_COLLECTION_DATABASE = _collection_bootstrap_support.ichthyology_collection_database
ENTOMOLOGY_COLLECTION_DATABASE = _collection_bootstrap_support.entomology_collection_database
MYCOLOGY_COLLECTION_DATABASE = _collection_bootstrap_support.mycology_collection_database
HERPETOLOGY_COLLECTION_DATABASE = _collection_bootstrap_support.herpetology_collection_database
ORNITHOLOGY_COLLECTION_DATABASE = _collection_bootstrap_support.ornithology_collection_database
PALEOZOOLOGY_COLLECTION_DATABASE = _collection_bootstrap_support.paleozoology_collection_database
PALEOBOTANY_COLLECTION_DATABASE = _collection_bootstrap_support.paleobotany_collection_database
PETROLOGY_COLLECTION_DATABASE = _collection_bootstrap_support.petrology_collection_database
METEORITE_COLLECTION_DATABASE = _collection_bootstrap_support.meteorite_collection_database
CONSERVATION_BIOLOGY_DATABASE = _collection_bootstrap_support.conservation_biology_database


def load_sanja_paleogene_neogene_mammals_database():
    """Load Sanja's Paleogene/Neogene large mammal records (PostgreSQL-preferred,
    JSON fallback until the table is created and the data migrated)."""
    database_path = Path('Sanja/sanja_paleogene_neogene_mammals.json')
    empty_database = {
        'metadata': {'name': 'Крупни сисари палеогена и неогена'},
        'specimens': [],
        'statistics': {
            'total_specimens': 0,
            'total_taxa': 0,
            'total_localities': 0,
            'identified_by_count': 0,
        },
    }

    # Postgres-preferred when configured and the table exists.
    if os.environ.get('DATABASE_URL'):
        try:
            import phase3a_databases
            if phase3a_databases.sanja_table_exists():
                specimens = phase3a_databases.get_sanja_specimens()
                return {
                    'metadata': {'name': 'Крупни сисари палеогена и неогена'},
                    'specimens': specimens,
                    'statistics': {
                        'total_specimens': len(specimens),
                        'total_taxa': len({s.get('specimen_name') for s in specimens if s.get('specimen_name')}),
                        'total_localities': len({s.get('location_found') for s in specimens if s.get('location_found')}),
                        'identified_by_count': len({s.get('identified_by') for s in specimens if s.get('identified_by')}),
                    },
                }
        except Exception as exc:
            logging.warning("Sanja PostgreSQL load failed, using JSON fallback: %s", exc)

    try:
        with database_path.open('r', encoding='utf-8') as database_file:
            return json.load(database_file)
    except (OSError, json.JSONDecodeError) as exc:
        logging.warning("Could not load %s: %s", database_path, exc)
        return empty_database


SANJA_PALEOGENE_NEOGENE_MAMMALS_DATABASE = load_sanja_paleogene_neogene_mammals_database()


# Bilja mollusc collections (PostgreSQL-backed). Loaded once at startup;
# CRUD helpers in bilja_collections_db refresh these globals after writes.
try:
    import bilja_collections_db as _bilja_db

    _bilja_loaded = _bilja_db.load_all()
    BILJA_KENOZOJSKE_INVERTEBRATE_DATABASE = _bilja_loaded['bilja_kenozojske_invertebrate']
    BILJA_HYDROBIOIDEA_RADOMAN_DATABASE = _bilja_loaded['bilja_hydrobioidea_radoman']
    BILJA_SUVOZEMNI_PUZEVI_PAVLOVIC_DATABASE = _bilja_loaded['bilja_suvozemni_puzevi_pavlovic']
    BILJA_OPSTA_ZBIRKA_MOLLUSCA_DATABASE = _bilja_loaded['bilja_opsta_zbirka_mollusca']
    BILJA_SKOLJKE_TADIC_DATABASE = _bilja_loaded['bilja_skoljke_tadic']
    BILJA_RECENTNI_MORSKI_MEKUSCI_DATABASE = _bilja_loaded['bilja_recentni_morski_mekusci']
except Exception as _bilja_exc:  # pragma: no cover
    logging.warning('Bilja collections could not be loaded: %s', _bilja_exc)
    _bilja_db = None
    _empty_bilja = {'metadata': {}, 'specimens': [], 'statistics': {}}
    BILJA_KENOZOJSKE_INVERTEBRATE_DATABASE = deepcopy(_empty_bilja)
    BILJA_HYDROBIOIDEA_RADOMAN_DATABASE = deepcopy(_empty_bilja)
    BILJA_SUVOZEMNI_PUZEVI_PAVLOVIC_DATABASE = deepcopy(_empty_bilja)
    BILJA_OPSTA_ZBIRKA_MOLLUSCA_DATABASE = deepcopy(_empty_bilja)
    BILJA_SKOLJKE_TADIC_DATABASE = deepcopy(_empty_bilja)
    BILJA_RECENTNI_MORSKI_MEKUSCI_DATABASE = deepcopy(_empty_bilja)


# Посете и истраживачки пројекти: PostgreSQL табеле visitor_records /
# research_projects (миграција 040); čitanje/upis у museum_content_views.
# Процесне листе су уклоњене — нису преживљавале рестарт ни делиле stanje
# између gunicorn радника.

# Vozila i rezervacije: PostgreSQL je jedini izvor istine (ZADATAK #3).
# Nema JSON fajl-fallback-a — pad baze se propagira kao jasna greška, a jedini
# keš je in-memory keš ispod (invalidira se force_reload-om posle svakog upisa).

def load_vehicles():
    """Load vehicles from PostgreSQL (raises on failure — no silent fallback)."""
    return app_data_support.load_vehicles_data(
        phase3a_databases=globals().get('phase3a_databases'),
        vehicle_data_support=vehicle_data_support,
    )

def load_reservations():
    """Load reservations from PostgreSQL (raises on failure — no silent fallback)."""
    return app_data_support.load_reservations_data(
        phase3a_databases=globals().get('phase3a_databases'),
        vehicle_data_support=vehicle_data_support,
    )

_MUSEUM_VEHICLES_CACHE = None
_VEHICLE_RESERVATIONS_CACHE = None


def get_museum_vehicles(force_reload: bool = False):
    """Return cached vehicle data, loading it on first use."""
    global _MUSEUM_VEHICLES_CACHE
    _MUSEUM_VEHICLES_CACHE = app_runtime_support.get_cached_value(
        current_value=_MUSEUM_VEHICLES_CACHE,
        force_reload=force_reload,
        loader=load_vehicles,
    )
    return _MUSEUM_VEHICLES_CACHE


def get_vehicle_reservations(force_reload: bool = False):
    """Return cached vehicle reservations, loading them on first use."""
    global _VEHICLE_RESERVATIONS_CACHE
    _VEHICLE_RESERVATIONS_CACHE = app_runtime_support.get_cached_value(
        current_value=_VEHICLE_RESERVATIONS_CACHE,
        force_reload=force_reload,
        loader=load_reservations,
    )
    return _VEHICLE_RESERVATIONS_CACHE

CULTURAL_HERITAGE_DATABASE = _collection_bootstrap_support.cultural_heritage_database
get_cultural_heritage_database = _collection_bootstrap_support.get_cultural_heritage_database
get_meteorite_collection_database = _collection_bootstrap_support.get_meteorite_collection_database

def authenticate_fallback_user(email, password):
    """
    Authenticate user using fallback employee database (development only).
    DO NOT USE IN PRODUCTION - set ENABLE_FALLBACK_AUTH=False in .env
    """
    return fallback_auth_support.authenticate_fallback_user(
        email,
        password,
        app_config=app.config,
        logger=logger,
    )

# Note: login_required and admin_required decorators are now imported from security_utils

globals().update(
    app_collection_support.build_collection_access_bindings(
        user_has_module_access=user_has_module_access,
        get_mineral_database=get_mineral_database,
        get_meteorite_collection_database=get_meteorite_collection_database,
        get_cultural_heritage_database=get_cultural_heritage_database,
        botany_collection_database=BOTANY_COLLECTION_DATABASE,
        ichthyology_collection_database=ICHTHYOLOGY_COLLECTION_DATABASE,
        entomology_collection_database=ENTOMOLOGY_COLLECTION_DATABASE,
        mycology_collection_database=MYCOLOGY_COLLECTION_DATABASE,
        herpetology_collection_database=HERPETOLOGY_COLLECTION_DATABASE,
        ornithology_collection_database=ORNITHOLOGY_COLLECTION_DATABASE,
        paleozoology_collection_database=PALEOZOOLOGY_COLLECTION_DATABASE,
        paleobotany_collection_database=PALEOBOTANY_COLLECTION_DATABASE,
        petrology_collection_database=PETROLOGY_COLLECTION_DATABASE,
    )
)
_collection_access_support.image_upload_config['sanja_paleogene_neogene_mammals'] = {
    'name': 'Крупни сисари палеогена и неогена',
    'prefix': 'SANJA',
    'route': 'sanja_paleogene_neogene_mammals',
    'module': 'sanja_paleogene_neogene_mammals',
    'loader': lambda: SANJA_PALEOGENE_NEOGENE_MAMMALS_DATABASE.get('specimens', []),
    'entity_type': 'sanja_paleogene_neogene_mammals',
}

# Bilja collections image upload config — registered from the bilja registry.
for _bilja_key, _bilja_cfg in (getattr(_bilja_db, 'COLLECTIONS', {}) or {}).items():
    _collection_access_support.image_upload_config[_bilja_key] = {
        'name': _bilja_cfg['name_sr'],
        'prefix': _bilja_cfg['prefix'],
        'route': _bilja_cfg['route'],
        'module': _bilja_cfg['module_key'],
        # Loader must read the global fresh on each call so cache refreshes are visible.
        'loader': (lambda k=_bilja_key: globals()[k.upper() + '_DATABASE'].get('specimens', [])),
        'entity_type': _bilja_key,
    }
app_collection_support.bind_collection_helpers_to_app(
    app,
    get_image_upload_module_key=get_image_upload_module_key,
    user_has_module_access=user_has_module_access,
    normalize_qr_collection_type=normalize_qr_collection_type,
    ensure_qr_collection_access=ensure_qr_collection_access,
    get_qr_collection_name=get_qr_collection_name,
    get_qr_collection_url=get_qr_collection_url,
    get_qr_collection_records=get_qr_collection_records,
    get_qr_record_identifier=get_qr_record_identifier,
    get_qr_record_catalog_label=get_qr_record_catalog_label,
    get_qr_record_name=get_qr_record_name,
    get_qr_record_summary=get_qr_record_summary,
    get_qr_record_location=get_qr_record_location,
    build_collection_highlight_qr_url=build_collection_highlight_qr_url,
    get_meteorite_collection_database=get_meteorite_collection_database,
    get_mineral_database=get_mineral_database,
    botany_collection_database=BOTANY_COLLECTION_DATABASE,
    paleozoology_collection_database=PALEOZOOLOGY_COLLECTION_DATABASE,
    get_employee_directory=get_employee_directory,
)

_RHMZ_WARNING_URL = dashboard_data_support.RHMZ_WARNING_URL
get_current_weather = dashboard_data_support.get_current_weather
get_current_weather_quick = dashboard_data_support.get_current_weather_quick
get_weather_forecast = dashboard_data_support.get_weather_forecast
get_rhmz_weather_warnings = dashboard_data_support.get_rhmz_weather_warnings
fetch_website_news = dashboard_data_support.fetch_website_news


def prepare_collection_records_for_display(collection_type, records):
    """Apply QR highlight filtering for collection pages and return the active highlight."""
    return app_ui_support.prepare_collection_records_for_display(
        collection_type,
        records,
        apply_qr_highlight_filter=apply_qr_highlight_filter,
    )

def create_timesheet_app_disabled():
    """Create and configure timesheet sub-application."""
    return app_request_support.create_timesheet_app_disabled(
        localsql_path=localsql_path,
    )

def create_mineral_app_disabled():
    """Create and configure mineral database sub-application."""
    return app_request_support.create_mineral_app_disabled(
        prirodnjacki_path=prirodnjacki_path,
    )


app_request_support.register_error_handlers(app)
app_request_support.register_template_context(
    app,
    current_dir=current_dir,
    get_current_weather=get_current_weather_quick,
    default_weather_condition=DEFAULT_WEATHER_CONDITION,
    user_has_module_access=user_has_module_access,
)


# Simple app runner (complex mounting disabled for now)
_background_jobs_started = False
_background_jobs_lock_fd = None
BACKGROUND_WORKER_ROLE_ENV = app_background_support.BACKGROUND_WORKER_ROLE_ENV
BACKGROUND_JOBS_LOCK_PATH = os.path.join(
    tempfile.gettempdir(),
    'museum_info_system_background_jobs.lock',
)


def start_background_jobs():
    """Start background jobs only inside the dedicated background worker process."""
    global _background_jobs_started, _background_jobs_lock_fd
    started, _background_jobs_lock_fd = app_background_support.start_background_jobs(
        background_jobs_started=_background_jobs_started,
        background_jobs_lock_fd=_background_jobs_lock_fd,
        background_jobs_lock_path=BACKGROUND_JOBS_LOCK_PATH,
        logger=logger,
        try_acquire_process_lock=try_acquire_process_lock,
        update_science_news_background=update_science_news_background,
        map_feature_paper_enricher=map_feature_paper_enricher,
    )
    if started:
        _background_jobs_started = True
    return started


def create_app(start_background_services: bool = False):
    """Create the main application (simplified version)."""
    return app_background_support.create_app(
        app=app,
        start_background_services=start_background_services,
        logger=logger,
    )

# ============================================================
# Projekti - New Museum Building Project
# ============================================================
PROJECT_SPACE_PLANNER_FILE = Path(app.root_path) / PROJECT_SPACE_PLANNER_RELATIVE_PATH


def format_chemical_formula(formula: str) -> str:
    """Convert RRUFF formula markup to Unicode subscript/superscript characters."""
    return mineral_science_views.format_chemical_formula(formula)


# ==================== MAP / KARTE ROUTES ====================

_KMZ_PATH = maps_terrain_support.KMZ_PATH
_TILE_CACHE_DIR = maps_terrain_support.TILE_CACHE_DIR
_build_tile_index = maps_terrain_support.build_tile_index
_extract_tile_to_cache = maps_terrain_support.extract_tile_to_cache
_DEM_DIR = maps_terrain_support.DEM_DIR


# ==================== GEOLOGICAL ZONE MAPS ====================
# ==================== GEOLOGICAL CROSS-SECTION PROFILE ====================
_load_zone_map_cached = maps_profile_support.load_zone_map_cached
_haversine_py = maps_profile_support.haversine_km
_sample_tile_color_at_point = maps_profile_support.sample_tile_color_at_point
_rgb_to_hsv = maps_profile_support.rgb_to_hsv
_classify_geo_color = maps_profile_support.classify_geo_color
_sample_geology_at_point = maps_profile_support.sample_geology_at_point
_sample_elevation_at_point = maps_profile_support.sample_elevation_at_point
_batch_sample_elevations = maps_profile_support.batch_sample_elevations
_DIGITIZED_PROFILES_PATH = maps_profile_support.DIGITIZED_PROFILES_PATH
_load_digitized_profiles = maps_profile_support.load_digitized_profiles
_save_digitized_profiles = maps_profile_support.save_digitized_profiles
_interpolate_subsurface = maps_profile_support.interpolate_subsurface


# ==================== PHASE 2: DIGITIZED PROFILES CRUD ====================


# ==================== PHASE 3: SUBSURFACE INTERPOLATION ====================


# ==================== END MAP / KARTE ROUTES ====================


if __name__ == '__main__':
    import argparse
    import time
    from datetime import datetime

    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Museum Information System')
    parser.add_argument('--host', default='0.0.0.0', help='Host to bind to')
    parser.add_argument('--port', type=int, default=5000, help='Port to bind to')
    parser.add_argument('--debug', action='store_true', help='Enable debug mode')
    args = parser.parse_args()

    print("🏛️ Museum Information System")
    print("=" * 50)
    print("Integrating:")
    print("  📊 Timesheet System (localSQLtesting)")
    print("  💎 Mineral Database (PrirodnjackiMuzej)")
    print("=" * 50)
    print(f"🌐 Server: http://{args.host}:{args.port}")
    print(f"🔐 Login: Use employee credentials from localSQLtesting")
    print("=" * 50)

    # Create the application
    application = create_app()

    # Run the application
    app.run(
        host=args.host,
        port=args.port,
        debug=args.debug
    )
