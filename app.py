#!/usr/bin/env python3
"""
Museum Information System - Main Flask Application
Integrates localSQLtesting (timesheet) and PrirodnjackiMuzej (mineral database) applications
"""

import os
import sys
import json
import logging
import calendar
import time
import re
import requests
from copy import deepcopy
from flask import Flask, render_template, request, redirect, url_for, session, flash, current_app, send_file, send_from_directory, make_response, jsonify
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
from image_api import image_api
from archive_signature_blueprint import (
    APP_ROOT as ARCHIVE_SIGNATURE_APP_ROOT,
    APPROVAL_CHAINS,
    REQUEST_SUBTYPES,
    archive_signature_bp,
    can_approve_request,
    can_view_archive_request,
    resolve_signature_document_path,
)
from batch_image_upload import get_batch_uploader
import bird_ringing_database
import scientific_papers_database
import importlib.util
import admin_system_views
import admin_user_management_views
import app_core_support
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
    get_client_ip
)
from flask_wtf.csrf import CSRFProtect
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_session import Session
from flask_babel import Babel, gettext as _, lazy_gettext as _l

# Security headers
try:
    from flask_talisman import Talisman
    TALISMAN_AVAILABLE = True
except ImportError:
    TALISMAN_AVAILABLE = False
    logging.warning("flask-talisman not available - security headers disabled")

# Create logs directory before configuring file logging handlers.
os.makedirs('logs', exist_ok=True)

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(name)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/museum_info_system.log'),
        logging.StreamHandler()
    ]
)

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

# Apply persisted admin security settings (shared across workers via JSON file)
_settings_file = Path('data/system_settings.json')
if _settings_file.exists():
    try:
        with _settings_file.open('r', encoding='utf-8') as _fh:
            _saved = json.load(_fh)
        if 'min_password_length' in _saved:
            app.config['PASSWORD_MIN_LENGTH'] = _saved['min_password_length']
        if 'max_login_attempts' in _saved:
            app.config['MAX_LOGIN_ATTEMPTS'] = _saved['max_login_attempts']
        if 'lockout_duration' in _saved:
            app.config['ACCOUNT_LOCKOUT_DURATION'] = int(_saved['lockout_duration']) * 60
        if 'session_timeout' in _saved:
            from datetime import timedelta as _td
            app.config['PERMANENT_SESSION_LIFETIME'] = _td(minutes=int(_saved['session_timeout']))
        if 'require_special_chars' in _saved:
            app.config['PASSWORD_REQUIRE_SPECIAL'] = _saved['require_special_chars']
    except Exception as _exc:
        logging.getLogger(__name__).warning("Could not load saved settings: %s", _exc)

# Trust proxy headers from nginx (1 proxy hop)
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)

# Initialize security extensions
# IMPORTANT: Session must be initialized BEFORE CSRF
Session(app)
csrf = CSRFProtect(app)

# Flask-Babel configuration
app.config['BABEL_DEFAULT_LOCALE'] = 'sr_Cyrl'
app.config['BABEL_SUPPORTED_LOCALES'] = ['sr_Cyrl', 'sr_Latn', 'en']

def get_locale():
    """Select locale from session, cookie, or Accept-Language header."""
    # Check session first
    lang = session.get('museum_lang')
    if lang:
        locale_map = {'sr-Cyrl': 'sr_Cyrl', 'sr-Latn': 'sr_Latn', 'en': 'en'}
        return locale_map.get(lang, 'sr_Cyrl')
    # Check cookie
    lang = request.cookies.get('museum_lang')
    if lang:
        locale_map = {'sr-Cyrl': 'sr_Cyrl', 'sr-Latn': 'sr_Latn', 'en': 'en'}
        return locale_map.get(lang, 'sr_Cyrl')
    return 'sr_Cyrl'

babel = Babel(app, locale_selector=get_locale)

# Register image API blueprint (auth enforced per-route in image_api.py)
# Exempt from CSRF — image uploads use multipart FormData which can't carry CSRF tokens;
# all routes are now protected by @login_required or @admin_required instead.
csrf.exempt(image_api)
app.register_blueprint(image_api)
app.register_blueprint(archive_signature_bp)

# Initialize rate limiter
limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"],
    storage_uri=app.config.get('RATELIMIT_STORAGE_URL', 'memory://')
)

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
            "www.facebook.com",
            "connect.facebook.net",
            "snapwidget.com",
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
            "*.fbcdn.net",
            "*.facebook.com",
            "*.instagram.com",
            "*.cdninstagram.com",
            "scontent.cdninstagram.com",
            "snapwidget.com",
            "nhmbeo.rs",
            "*.nhmbeo.rs",
            "www.nhmbeo.rs",
        ],
        'connect-src': [
            "'self'",
            "blob:",
            "localhost:11434",  # Ollama API
            "www.facebook.com",
            "cdn.plot.ly",
            "cdnjs.cloudflare.com",
            "cdn.jsdelivr.net",
        ],
        'worker-src': [
            "'self'",
            "blob:",
        ],
        'frame-src': [
            "'self'",
            "www.facebook.com",
            "*.facebook.com",
            "snapwidget.com",
        ],
        'frame-ancestors': "'self'",
        'form-action': "'self'",
    }

    # Initialize Talisman with appropriate settings
    talisman = Talisman(
        app,
        # Force HTTPS only in production
        force_https=app.config.get('SESSION_COOKIE_SECURE', False),
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
            'biljana.mitrovic@nhmbeo.rs',
            'verica.stojanovic@nhmbeo.rs'
        ]
    },
    'employees_database': {
        'name': 'База запослених',
        'description': 'Преглед свих 42 запослених музеја',
        'icon': 'bi-people-fill',
        'default_access': False,
        'authorized_users': ['admin']
    },
    'employee_profiles': {
        'name': 'Профили запослених',
        'description': 'Детаљне биографије запослених',
        'icon': 'bi-person-badge',
        'default_access': False,
        'authorized_users': ['admin']
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
        'authorized_users': ['admin']
    },
    'exhibitions_database': {
        'name': 'База изложби',
        'description': 'Историјат галеријских изложби и аналитика посета',
        'icon': 'bi-easel',
        'default_access': False,
        'authorized_users': ['admin', 'draganav@nhmbeo.rs']
    },
    'news': {
        'name': 'Музејске вести',
        'description': 'Вести и објаве о активностима музеја',
        'icon': 'bi-newspaper',
        'default_access': True,  # Everyone can view news
        'restricted_users': []
    },
    'cultural_heritage': {
        'name': 'Заштићена културна добра',
        'description': 'Регистар културних добара под заштитом',
        'icon': 'bi-award',
        'default_access': False,
        'authorized_users': ['admin']
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
        'authorized_users': ['admin']
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
    }
}
MODULE_ACCESS_DEFAULTS = deepcopy(MODULE_ACCESS)

# Module access persistence
MODULE_ACCESS_FILE = 'data/module_access.json'
_module_access_mtime = None


def _get_file_mtime(path: str):
    """Return the current file mtime, or None when the file is absent."""
    try:
        return os.path.getmtime(path)
    except OSError:
        return None


def load_module_access(force: bool = False):
    """Load module access settings from JSON file."""
    global MODULE_ACCESS, _module_access_mtime

    current_mtime = _get_file_mtime(MODULE_ACCESS_FILE)
    if not force and current_mtime == _module_access_mtime:
        return MODULE_ACCESS

    MODULE_ACCESS = module_access_support.load_module_access_data(
        module_access_file=MODULE_ACCESS_FILE,
        current_mtime=current_mtime,
        default_access=MODULE_ACCESS_DEFAULTS,
    )
    _module_access_mtime = current_mtime
    return MODULE_ACCESS

def save_module_access():
    """Save module access settings to JSON file."""
    global _module_access_mtime
    if module_access_support.save_module_access_data(
        module_access_file=MODULE_ACCESS_FILE,
        module_access=MODULE_ACCESS,
    ):
        _module_access_mtime = _get_file_mtime(MODULE_ACCESS_FILE)
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
    global DASHBOARD_PREFERENCES, _dashboard_prefs_mtime

    current_mtime = _get_file_mtime(DASHBOARD_PREFS_FILE)
    if not force and current_mtime == _dashboard_prefs_mtime:
        return DASHBOARD_PREFERENCES

    DASHBOARD_PREFERENCES = module_access_support.load_dashboard_preferences_data(
        dashboard_prefs_file=DASHBOARD_PREFS_FILE,
        current_mtime=current_mtime,
        default_prefs=_DEFAULT_DASHBOARD_PREFS,
    )
    _dashboard_prefs_mtime = current_mtime
    return DASHBOARD_PREFERENCES

def save_dashboard_preferences():
    """Save dashboard preferences to JSON file."""
    global _dashboard_prefs_mtime
    if module_access_support.save_dashboard_preferences_data(
        dashboard_prefs_file=DASHBOARD_PREFS_FILE,
        dashboard_preferences=DASHBOARD_PREFERENCES,
    ):
        _dashboard_prefs_mtime = _get_file_mtime(DASHBOARD_PREFS_FILE)
        return True
    return False

def user_has_module_access(user_email, user_role, module_key):
    """Check if user has access to specific module."""
    load_module_access()

    # Admin always has access to everything
    if user_role == 'admin':
        return True

    module = MODULE_ACCESS.get(module_key)
    if not module:
        return False

    # Check default access
    if module.get('default_access', False):
        # Check if user is in restricted list
        if user_email not in module.get('restricted_users', []):
            return True

    # Check if user is explicitly authorized
    if user_email in module.get('authorized_users', []):
        return True

    return False


app.user_has_module_access = user_has_module_access


current_user_is_admin = app_core_support.current_user_is_admin
can_access_owned_record = app_core_support.can_access_owned_record


def ensure_login_tracker_initialized():
    """Initialize the shared login tracker lazily when auth routes need it."""
    global _login_tracker_initialized
    if _login_tracker_initialized:
        return login_tracker

    redis_url = app.config.get('REDIS_URL')
    init_login_tracker(redis_url if redis_url else None)
    _login_tracker_initialized = True
    return login_tracker


def log_fallback_auth_warning_once():
    """Log the fallback-auth warning once per process when it is actually used."""
    global _fallback_auth_warning_logged
    if _fallback_auth_warning_logged:
        return

    if not app.config.get('ENABLE_FALLBACK_AUTH', False):
        logger.info("Fallback authentication is disabled (production mode)")
    else:
        logger.warning("⚠️ USING FALLBACK AUTHENTICATION - NOT SECURE FOR PRODUCTION")
        logger.warning("    Set ENABLE_FALLBACK_AUTH=False in .env for production")
    _fallback_auth_warning_logged = True

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

def get_fallback_employees():
    """Return fallback employee data for development/testing only."""
    return fallback_auth_support.get_fallback_employees(app.config)

# Initialize fallback employees lazily
MUSEUM_EMPLOYEES = None


def get_museum_employees():
    """Return fallback employee records, loading them only when needed."""
    global MUSEUM_EMPLOYEES
    if MUSEUM_EMPLOYEES is None:
        MUSEUM_EMPLOYEES = get_fallback_employees()
    return MUSEUM_EMPLOYEES

# Library Database - will be loaded from JSON}

# Library Database - loaded from PostgreSQL (Phase 3A)
LIBRARY_DATABASE = None
EMPLOYEE_DIRECTORY = None

def load_library_database():
    """Load library database from PostgreSQL."""
    return museum_staff_support.load_library_database(
        library_path=os.path.join('data', 'library_database.json'),
        database_url=os.environ.get('DATABASE_URL'),
        phase3a_databases=globals().get('phase3a_databases'),
    )

def save_library_database():
    """Save library database to JSON file."""
    global LIBRARY_DATABASE
    if LIBRARY_DATABASE is None:
        return

    museum_staff_support.save_library_database(
        library_path=os.path.join('data', 'library_database.json'),
        library_database=LIBRARY_DATABASE,
    )

def get_library_database():
    """Return the cached library database, loading it if needed."""
    global LIBRARY_DATABASE
    if LIBRARY_DATABASE is None:
        LIBRARY_DATABASE = load_library_database()
    return LIBRARY_DATABASE

def load_employee_directory():
    """Load employee directory from PostgreSQL or JSON fallback."""
    return museum_staff_support.load_employee_directory(
        directory_path=os.path.join('data', 'employee_directory.json'),
        database_url=os.environ.get('DATABASE_URL'),
        phase3a_databases=globals().get('phase3a_databases'),
    )

def get_employee_directory():
    """Return cached employee directory."""
    global EMPLOYEE_DIRECTORY
    if EMPLOYEE_DIRECTORY is None:
        EMPLOYEE_DIRECTORY = load_employee_directory()
    return EMPLOYEE_DIRECTORY


LazyLoadedDict = app_core_support.LazyLoadedDict

def load_exhibitions_data():
    """Load exhibitions from PostgreSQL or JSON fallback."""
    return museum_content_support.load_exhibitions_data(
        database_url=os.environ.get('DATABASE_URL'),
        phase3a_databases=globals().get('phase3a_databases'),
    )


def load_news_data():
    """Load news articles from PostgreSQL or JSON fallback."""
    return museum_content_support.load_news_data(
        database_url=os.environ.get('DATABASE_URL'),
        phase3a_databases=globals().get('phase3a_databases'),
    )


def build_exhibitions_database():
    """Build the exhibition cache payload on demand."""
    return museum_content_support.build_exhibitions_database(
        load_exhibitions_data=load_exhibitions_data,
    )


def build_news_database():
    """Build the news cache payload on demand."""
    return museum_content_support.build_news_database(
        load_news_data=load_news_data,
    )


EXHIBITS_DATABASE = museum_content_support.EXHIBITS_DATABASE

EXHIBITIONS_DATABASE = LazyLoadedDict(build_exhibitions_database, 'exhibitions database')
NEWS_DATABASE = LazyLoadedDict(build_news_database, 'news database')


def get_exhibit_statistics():
    """Aggregate exhibit metrics from the artifacts dataset."""
    return museum_content_support.get_exhibit_statistics(
        exhibits_database=EXHIBITS_DATABASE,
    )


def get_exhibition_statistics():
    """Aggregate exhibition metrics for dashboard and detail views."""
    return museum_content_support.get_exhibition_statistics(
        exhibitions_database=EXHIBITIONS_DATABASE,
        current_year=datetime.now().year,
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

# Visitor Records Database
VISITOR_RECORDS = []

# Research Projects Database
RESEARCH_PROJECTS = []

# Vehicle data files (fallback for legacy mode)
VEHICLES_FILE = 'data/museum_vehicles.json'
RESERVATIONS_FILE = 'data/vehicle_reservations.json'

def load_vehicles():
    """Load vehicles from PostgreSQL or JSON file (fallback)."""
    return vehicle_data_support.load_vehicles(
        vehicles_file=VEHICLES_FILE,
        database_url=os.environ.get('DATABASE_URL'),
        phase3a_databases=globals().get('phase3a_databases'),
    )

def save_vehicles():
    """Save vehicles to JSON file (fallback only)."""
    return vehicle_data_support.save_vehicles(
        vehicles_file=VEHICLES_FILE,
        vehicles=get_museum_vehicles(),
    )

def load_reservations():
    """Load reservations from PostgreSQL or JSON file (fallback)."""
    return vehicle_data_support.load_reservations(
        reservations_file=RESERVATIONS_FILE,
        database_url=os.environ.get('DATABASE_URL'),
        phase3a_databases=globals().get('phase3a_databases'),
    )

def save_reservations():
    """Save reservations to JSON file (fallback only)."""
    return vehicle_data_support.save_reservations(
        reservations_file=RESERVATIONS_FILE,
        reservations=get_vehicle_reservations(),
    )

_MUSEUM_VEHICLES_CACHE = None
_VEHICLE_RESERVATIONS_CACHE = None


def get_museum_vehicles(force_reload: bool = False):
    """Return cached vehicle data, loading it on first use."""
    global _MUSEUM_VEHICLES_CACHE
    if force_reload or _MUSEUM_VEHICLES_CACHE is None:
        _MUSEUM_VEHICLES_CACHE = load_vehicles()
    return _MUSEUM_VEHICLES_CACHE


def get_vehicle_reservations(force_reload: bool = False):
    """Return cached vehicle reservations, loading them on first use."""
    global _VEHICLE_RESERVATIONS_CACHE
    if force_reload or _VEHICLE_RESERVATIONS_CACHE is None:
        _VEHICLE_RESERVATIONS_CACHE = load_reservations()
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

@app.route('/set_language', methods=['POST'])
@csrf.exempt
def set_language():
    """Set the user's language/script preference (UI-only, no sensitive data)."""
    return core_app_views.set_language_preference()

@app.route('/')
@app.route('/index')
def index():
    """Main landing page."""
    return core_app_views.render_index(
        dashboard_endpoint='dashboard',
    )

@app.route('/login', methods=['GET', 'POST'])
@limiter.limit("5 per minute")
def login():
    """User login with security enhancements."""
    return core_app_views.handle_login(
        app_config=app.config,
        auth_system=auth_system,
        ensure_login_tracker_initialized=ensure_login_tracker_initialized,
        log_security_event=log_security_event,
        log_fallback_auth_warning_once=log_fallback_auth_warning_once,
        authenticate_fallback_user=authenticate_fallback_user,
        change_password_endpoint='change_password',
        dashboard_endpoint='dashboard',
    )

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    """User logout. Accepts both GET (for backwards compat) and POST (preferred)."""
    return core_app_views.handle_logout(
        index_endpoint='index',
    )

@app.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    """Change user password with validation."""
    return core_app_views.handle_change_password(
        auth_system=auth_system,
        app_config=app.config,
        password_validator=password_validator,
        dashboard_endpoint='dashboard',
        log_security_event=log_security_event,
    )

@app.route('/dashboard')
@login_required
def dashboard():
    """Main dashboard."""
    return core_app_views.render_dashboard(
        get_user_modules=get_user_modules,
    )


@app.route('/dashboard-classic')
@login_required
def dashboard_classic():
    """Classic dashboard view."""
    return core_app_views.render_dashboard(
        get_user_modules=get_user_modules,
    )

@app.route('/timesheet')
@login_required
def timesheet_app():
    """Route to timesheet application."""
    return timesheet_admin_views.render_timesheet_app(
        timesheet_repository=timesheet_repository,
        timesheet_repository_cls=TimesheetRepository,
        user_has_module_access=user_has_module_access,
    )


@app.route('/admin/timesheet')
@admin_required
def admin_timesheet_main():
    """Main timesheet administration page."""
    return timesheet_admin_views.render_admin_timesheet_main()


@app.route('/admin/timesheet_reports')
@admin_required
def admin_timesheet_reports():
    """Admin view for centralized timesheet reports (PostgreSQL)."""
    return timesheet_admin_views.render_admin_timesheet_reports(
        timesheet_repository=timesheet_repository,
        timesheet_repository_cls=TimesheetRepository,
    )


@app.route('/admin/timesheet_reports/<int:report_id>')
@admin_required
def admin_timesheet_report_detail(report_id):
    """Detailed view of a single report."""
    return timesheet_admin_views.render_admin_timesheet_report_detail(
        report_id=report_id,
        timesheet_repository=timesheet_repository,
        timesheet_repository_cls=TimesheetRepository,
    )


@app.route('/admin/timesheet/employees')
@admin_required
def admin_timesheet_employees():
    """Admin view for managing employees in timesheet system."""
    return timesheet_admin_views.render_admin_timesheet_employees(
        timesheet_repository=timesheet_repository,
    )


@app.route('/admin/timesheet/users')
@admin_required
def admin_timesheet_users():
    """Admin view for managing timesheet system users."""
    return timesheet_admin_views.render_admin_timesheet_users(
        timesheet_repository=timesheet_repository,
    )


@app.route('/admin/timesheet/pending')
@admin_required
def admin_timesheet_pending():
    """Admin view for pending edit requests."""
    return timesheet_admin_views.render_admin_timesheet_pending(
        timesheet_repository=timesheet_repository,
    )


@app.route('/admin/timesheet/analytics')
@admin_required
def admin_timesheet_analytics():
    """Admin analytics dashboard for timesheet system."""
    return timesheet_admin_views.render_admin_timesheet_analytics(
        timesheet_repository=timesheet_repository,
    )


# ============================================================================
# ADMIN TIMESHEET API ENDPOINTS (PostgreSQL)
# ============================================================================

@app.route('/api/admin/timesheet/employee-analytics')
@admin_required
def api_admin_employee_analytics():
    """Get detailed analytics for a specific employee."""
    return timesheet_admin_views.api_admin_employee_analytics()


@app.route('/api/admin/timesheet/report/<int:report_id>')
@admin_required
def api_admin_get_timesheet_report(report_id):
    """Get single timesheet report details with daily entries."""
    return timesheet_admin_views.api_admin_get_timesheet_report(
        report_id=report_id,
        timesheet_repository=timesheet_repository,
    )


@app.route('/api/admin/timesheet/report/<int:report_id>/approve', methods=['POST'])
@admin_required
def api_admin_approve_timesheet_report(report_id):
    """Approve or disapprove a timesheet report."""
    return timesheet_admin_views.api_admin_approve_timesheet_report(
        report_id=report_id,
        timesheet_repository=timesheet_repository,
    )


@app.route('/api/admin/timesheet/reports/batch-approve', methods=['POST'])
@admin_required
def api_admin_batch_approve_timesheet_reports():
    """Batch approve or disapprove multiple timesheet reports."""
    return timesheet_admin_views.api_admin_batch_approve_timesheet_reports(
        timesheet_repository=timesheet_repository,
    )


@app.route('/api/admin/timesheet/export/<int:report_id>')
@admin_required
def api_admin_export_timesheet_report(report_id):
    """Export timesheet report to Word document."""
    return timesheet_admin_views.api_admin_export_timesheet_report(
        report_id=report_id,
        timesheet_repository=timesheet_repository,
    )


@app.route('/api/admin/timesheet/report/<int:report_id>', methods=['DELETE'])
@admin_required
def api_admin_delete_timesheet_report(report_id):
    """Delete a timesheet report and its entries."""
    return timesheet_admin_views.api_admin_delete_timesheet_report(
        report_id=report_id,
        timesheet_repository=timesheet_repository,
    )


@app.route('/admin/timesheet/pending/approve/<int:request_id>', methods=['POST'])
@admin_required
def admin_approve_edit_request(request_id):
    """Approve or reject an edit request."""
    return timesheet_admin_views.admin_approve_edit_request(
        request_id=request_id,
        timesheet_repository=timesheet_repository,
    )


# ============================================================================
# USER NOTIFICATIONS (Обавештења)
# ============================================================================

@app.route('/api/notifications')
@login_required
def api_get_notifications():
    """Get notifications for the logged-in user."""
    return notification_views.api_get_notifications()


@app.route('/api/notifications/read', methods=['POST'])
@login_required
def api_mark_notifications_read():
    """Mark notifications as read."""
    return notification_views.api_mark_notifications_read()


@app.route('/api/notifications/clear', methods=['POST'])
@login_required
def api_clear_notifications():
    """Clear all notifications for the logged-in user."""
    return notification_views.api_clear_notifications()


# ============================================================================
# EMPLOYEE TIMESHEET ENTRY SYSTEM (PostgreSQL Integration)
# ============================================================================

@app.route('/timesheet/entry')
@login_required
def timesheet_entry():
    """Employee timesheet entry page."""
    return timesheet_employee_views.render_timesheet_entry()


@app.route('/timesheet/view')
@login_required
def timesheet_view():
    """Employee timesheet view page - read-only history."""
    return timesheet_employee_views.render_timesheet_view()


@app.route('/api/timesheet/load')
@login_required
def api_load_timesheet():
    """API endpoint to load existing timesheet data for a given month/year."""
    return timesheet_employee_views.api_load_timesheet()


@app.route('/request_approval', methods=['POST'])
@login_required
def request_approval():
    """Create an employee edit approval request."""
    return timesheet_employee_views.request_approval()


@app.route('/api/timesheet/save', methods=['POST'])
@login_required
def api_save_timesheet():
    """API endpoint to save timesheet data to PostgreSQL."""
    return timesheet_employee_views.api_save_timesheet()


# =============================================================================
# TIMESHEET STATUS WORKFLOW API
# =============================================================================

@app.route('/api/timesheet/<int:report_id>/submit', methods=['POST'])
@login_required
def api_timesheet_submit(report_id):
    """Employee submits timesheet for admin review."""
    return timesheet_employee_views.api_timesheet_submit(report_id)


@app.route('/api/timesheet/<int:report_id>/approve', methods=['POST'])
@admin_required
def api_timesheet_approve(report_id):
    """Admin approves a submitted timesheet."""
    return timesheet_employee_views.api_timesheet_approve(report_id)


@app.route('/api/timesheet/<int:report_id>/reject', methods=['POST'])
@admin_required
def api_timesheet_reject(report_id):
    """Admin rejects a submitted timesheet with a note."""
    return timesheet_employee_views.api_timesheet_reject(report_id)


@app.route('/api/timesheet/<int:report_id>/force-edit', methods=['POST'])
@admin_required
def api_timesheet_force_edit(report_id):
    """Admin forces a timesheet back to DRAFT for editing."""
    return timesheet_employee_views.api_timesheet_force_edit(report_id)


@app.route('/admin/timesheet/review')
@admin_required
def admin_timesheet_review():
    """Admin view for timesheets pending review (status=SUBMITTED)."""
    return timesheet_employee_views.render_admin_timesheet_review()


@app.route('/mineral_database')
@login_required
def mineral_database_app():
    """Route to mineral database - redirects to admin mineral collection."""
    return core_app_views.render_mineral_database_redirect(
        user_has_module_access=user_has_module_access,
        dashboard_endpoint='dashboard',
        admin_mineral_collection_endpoint='admin_mineral_collection',
    )

@app.route('/admin')
@admin_required
def admin_panel():
    """Admin panel."""
    return core_app_views.render_admin_panel()

# ============================================
# SYSTEM SETTINGS ROUTES
# ============================================

@app.route('/admin/system-settings')
@admin_required
def admin_system_settings():
    """System settings page with full functionality."""
    return admin_system_views.render_admin_system_settings()

@app.route('/api/admin/settings/general', methods=['POST'])
@admin_required
def api_save_general_settings():
    """Save general settings."""
    return admin_system_views.api_save_general_settings()

@app.route('/api/admin/settings/security', methods=['POST'])
@admin_required
def api_save_security_settings():
    """Save security settings."""
    return admin_system_views.api_save_security_settings()

@app.route('/api/admin/database/backup', methods=['POST'])
@admin_required
def api_database_backup():
    """Create database backup."""
    return admin_system_views.api_database_backup()

@app.route('/api/admin/database/table-stats')
@admin_required
def api_table_stats():
    """Get table statistics."""
    return admin_system_views.api_table_stats()

@app.route('/api/admin/database/vacuum', methods=['POST'])
@admin_required
def api_vacuum_database():
    """Run VACUUM ANALYZE on database."""
    return admin_system_views.api_vacuum_database()

@app.route('/api/admin/logs')
@admin_required
def api_get_logs():
    """Get system logs."""
    return admin_system_views.api_get_logs()

@app.route('/api/admin/logs/download')
@admin_required
def api_download_logs():
    """Download log file."""
    return admin_system_views.api_download_logs()

@app.route('/api/admin/cache/clear', methods=['POST'])
@admin_required
def api_clear_cache():
    """Clear system cache."""
    return admin_system_views.api_clear_cache()

# END SYSTEM SETTINGS ROUTES
# ============================================

@app.route('/admin/statistics')
@admin_required
def admin_statistics():
    """Collection statistics dashboard."""
    return collection_statistics_views.render_admin_statistics(
        get_mineral_database=get_mineral_database,
        get_meteorite_collection_database=get_meteorite_collection_database,
        botany_collection_database=BOTANY_COLLECTION_DATABASE,
        paleozoology_collection_database=PALEOZOOLOGY_COLLECTION_DATABASE,
        paleobotany_collection_database=PALEOBOTANY_COLLECTION_DATABASE,
        petrology_collection_database=PETROLOGY_COLLECTION_DATABASE,
        get_cultural_heritage_database=get_cultural_heritage_database,
        get_image_storage=get_image_storage,
    )

_collection_access_support = collection_access_support.CollectionAccessSupport(
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
QR_COLLECTION_ALIASES = _collection_access_support.qr_collection_aliases
QR_FIELD_LABELS = _collection_access_support.qr_field_labels
QR_COLLECTION_CONFIG = _collection_access_support.qr_collection_config
IMAGE_UPLOAD_ALIASES = _collection_access_support.image_upload_aliases
IMAGE_UPLOAD_CONFIG = _collection_access_support.image_upload_config
normalize_qr_collection_type = _collection_access_support.normalize_qr_collection_type
get_qr_collection_config = _collection_access_support.get_qr_collection_config
get_qr_collection_name = _collection_access_support.get_qr_collection_name
get_qr_collection_module_key = _collection_access_support.get_qr_collection_module_key
get_qr_collection_url = _collection_access_support.get_qr_collection_url
get_qr_collection_action_url = _collection_access_support.get_qr_collection_action_url
get_qr_collection_records = _collection_access_support.get_qr_collection_records
get_qr_record_identifier = _collection_access_support.get_qr_record_identifier
get_qr_record_catalog_label = _collection_access_support.get_qr_record_catalog_label
get_qr_record_name = _collection_access_support.get_qr_record_name
get_qr_record_summary = _collection_access_support.get_qr_record_summary
get_qr_record_location = _collection_access_support.get_qr_record_location
build_collection_highlight_qr_url = _collection_access_support.build_collection_highlight_qr_url
apply_qr_highlight_filter = _collection_access_support.apply_qr_highlight_filter
ensure_qr_collection_access = _collection_access_support.ensure_qr_collection_access
load_all_mineral_records_for_image_upload = _collection_access_support.load_all_mineral_records_for_image_upload
normalize_image_upload_database = _collection_access_support.normalize_image_upload_database
get_image_upload_config = _collection_access_support.get_image_upload_config
get_image_upload_module_key = _collection_access_support.get_image_upload_module_key
get_image_upload_collection_url = _collection_access_support.get_image_upload_collection_url
get_image_upload_action_url = _collection_access_support.get_image_upload_action_url
get_image_upload_display_name = _collection_access_support.get_image_upload_display_name
get_accessible_image_upload_databases = _collection_access_support.get_accessible_image_upload_databases
normalize_image_upload_record = _collection_access_support.normalize_image_upload_record
get_image_upload_records = _collection_access_support.get_image_upload_records
ensure_image_upload_access = _collection_access_support.ensure_image_upload_access

@app.route('/admin/qr_generator')
@login_required
def admin_qr_generator():
    """Legacy QR generator entry point kept as a redirect to scoped collection pages."""
    return qr_management_views.render_admin_qr_generator(
        user_has_module_access=user_has_module_access,
    )

@app.route('/admin/qr_field_selection/<collection_type>', methods=['GET'])
@login_required
def admin_qr_field_selection(collection_type):
    """Field selection interface for QR code generation."""
    return qr_management_views.render_admin_qr_field_selection(
        collection_type,
        normalize_qr_collection_type=normalize_qr_collection_type,
        ensure_qr_collection_access=ensure_qr_collection_access,
    )

@app.route('/admin/qr_labels_with_fields/<collection_type>', methods=['POST'])
@login_required
def admin_qr_labels_with_fields(collection_type):
    """Generate QR codes with custom field selection."""
    return qr_management_views.handle_admin_qr_labels_with_fields(
        collection_type,
        normalize_qr_collection_type=normalize_qr_collection_type,
        ensure_qr_collection_access=ensure_qr_collection_access,
        get_meteorite_collection_database=get_meteorite_collection_database,
        botany_collection_database=BOTANY_COLLECTION_DATABASE,
        paleozoology_collection_database=PALEOZOOLOGY_COLLECTION_DATABASE,
    )

# Box-based QR Code System for Minerals
@app.route('/admin/qr_boxes/minerals', methods=['GET'])
@login_required
def admin_qr_mineral_boxes():
    """Select mineral storage boxes for QR code generation."""
    return qr_management_views.render_admin_qr_mineral_boxes(
        ensure_qr_collection_access=ensure_qr_collection_access,
        get_mineral_database=get_mineral_database,
    )

@app.route('/admin/qr_boxes/minerals/generate', methods=['POST'])
@login_required
def admin_generate_box_qr_codes():
    """Generate QR codes for selected mineral boxes."""
    return qr_management_views.handle_admin_generate_box_qr_codes(
        ensure_qr_collection_access=ensure_qr_collection_access,
    )


# Public route for box contents (no auth required)
@app.route('/qr_box/minerals/<box_number>')
@limiter.limit("30 per minute")
def qr_view_mineral_box(box_number):
    """Public mobile-optimized view for mineral box contents."""
    return collection_media_views.render_qr_view_mineral_box(
        box_number,
        get_mineral_database=get_mineral_database,
    )

@app.route('/admin/qr_select/<collection_type>', methods=['GET'])
@login_required
def admin_qr_select_specimens(collection_type):
    """Specimen selection interface with filters."""
    return qr_label_views.render_admin_qr_select_specimens(
        collection_type,
        normalize_qr_collection_type=normalize_qr_collection_type,
        ensure_qr_collection_access=ensure_qr_collection_access,
        get_qr_collection_name=get_qr_collection_name,
        get_qr_collection_url=get_qr_collection_url,
        get_mineral_database=get_mineral_database,
        get_qr_collection_records=get_qr_collection_records,
        get_qr_record_identifier=get_qr_record_identifier,
        get_qr_record_catalog_label=get_qr_record_catalog_label,
        get_qr_record_name=get_qr_record_name,
        get_qr_record_summary=get_qr_record_summary,
        get_qr_record_location=get_qr_record_location,
    )

@app.route('/admin/qr_labels_selected/<collection_type>', methods=['POST'])
@login_required
def admin_qr_labels_selected(collection_type):
    """Generate QR codes for selected specimens only."""
    return qr_label_views.handle_admin_qr_labels_selected(
        collection_type,
        normalize_qr_collection_type=normalize_qr_collection_type,
        ensure_qr_collection_access=ensure_qr_collection_access,
        get_mineral_database=get_mineral_database,
        get_qr_collection_records=get_qr_collection_records,
        get_qr_record_identifier=get_qr_record_identifier,
        get_qr_record_catalog_label=get_qr_record_catalog_label,
        get_qr_record_name=get_qr_record_name,
        build_collection_highlight_qr_url=build_collection_highlight_qr_url,
        get_qr_collection_name=get_qr_collection_name,
    )

@app.route('/admin/qr_label_format/<collection_type>')
@login_required
def admin_qr_label_format(collection_type):
    """Show label format selection for QR code generation."""
    return qr_label_views.render_admin_qr_label_format(
        collection_type,
        normalize_qr_collection_type=normalize_qr_collection_type,
        ensure_qr_collection_access=ensure_qr_collection_access,
        get_qr_collection_name=get_qr_collection_name,
        get_qr_collection_url=get_qr_collection_url,
    )

@app.route('/admin/qr_labels_with_format/<collection_type>', methods=['POST'])
@login_required
def admin_qr_labels_with_format(collection_type):
    """Generate QR codes with selected label format."""
    return qr_label_views.handle_admin_qr_labels_with_format(
        collection_type,
        normalize_qr_collection_type=normalize_qr_collection_type,
        ensure_qr_collection_access=ensure_qr_collection_access,
        get_qr_collection_url=get_qr_collection_url,
    )

@app.route('/admin/qr_labels/<collection_type>')
@login_required
def admin_qr_labels(collection_type):
    """Generate printable QR code labels for a collection."""
    return qr_label_views.render_admin_qr_labels(
        collection_type,
        normalize_qr_collection_type=normalize_qr_collection_type,
        ensure_qr_collection_access=ensure_qr_collection_access,
        get_mineral_database=get_mineral_database,
        get_qr_collection_records=get_qr_collection_records,
        get_qr_record_identifier=get_qr_record_identifier,
        get_qr_record_catalog_label=get_qr_record_catalog_label,
        get_qr_record_name=get_qr_record_name,
        build_collection_highlight_qr_url=build_collection_highlight_qr_url,
        get_qr_collection_name=get_qr_collection_name,
        get_qr_collection_url=get_qr_collection_url,
    )

@app.route('/admin/batch_image_upload', methods=['GET', 'POST'])
@login_required
def batch_image_upload():
    """Batch image upload interface for museum collections."""
    return collection_media_views.handle_batch_image_upload(
        get_accessible_image_upload_databases=get_accessible_image_upload_databases,
        normalize_image_upload_database=normalize_image_upload_database,
        ensure_image_upload_access=ensure_image_upload_access,
        user_has_module_access=user_has_module_access,
        get_image_upload_config=get_image_upload_config,
        get_batch_uploader=get_batch_uploader,
        get_image_upload_records=get_image_upload_records,
        get_image_upload_collection_url=get_image_upload_collection_url,
        get_image_upload_display_name=get_image_upload_display_name,
    )

@app.route('/static/<path:filename>')
def serve_static(filename):
    """Serve static files."""
    return send_from_directory('static', filename)

@app.route('/api/specimen_image/<database>/<entity_type>/<entity_id>')
@limiter.exempt
def get_specimen_image(database, entity_type, entity_id):
    """Get specimen image or placeholder."""
    return collection_media_views.get_specimen_image(
        database,
        entity_type,
        entity_id,
        get_image_storage=get_image_storage,
    )

@app.route('/api/specimen_image_full/<database>/<entity_type>/<entity_id>')
@limiter.exempt
def get_specimen_image_full(database, entity_type, entity_id):
    """Get full-size specimen image."""
    return collection_media_views.get_specimen_image_full(
        database,
        entity_type,
        entity_id,
        get_image_storage=get_image_storage,
    )

@app.route('/api/specimen_thumbnail/<database>/<entity_type>/<entity_id>')
@limiter.exempt
def get_specimen_thumbnail(database, entity_type, entity_id):
    """Get specimen thumbnail or small placeholder."""
    return collection_media_views.get_specimen_thumbnail(
        database,
        entity_type,
        entity_id,
        get_image_storage=get_image_storage,
    )


@app.route('/api/images/<image_id>')
@login_required
@limiter.exempt
def get_image_by_id(image_id):
    """Serve an image directly by image_id."""
    return collection_media_views.get_image_by_id(
        image_id,
        get_image_storage=get_image_storage,
    )

@app.route('/admin/manage_access')
@admin_required
def manage_user_access():
    """Manage user module access."""
    return admin_user_management_views.render_manage_user_access(
        load_module_access=load_module_access,
        user_has_module_access=user_has_module_access,
        module_access=MODULE_ACCESS,
        get_museum_employees=get_museum_employees,
    )

@app.route('/admin/grant_access', methods=['POST'])
@admin_required
def grant_module_access():
    """Grant module access to a user."""
    return admin_user_management_views.grant_module_access(
        load_module_access=load_module_access,
        save_module_access=save_module_access,
        module_access=MODULE_ACCESS,
    )

@app.route('/admin/revoke_access', methods=['POST'])
@admin_required
def revoke_module_access():
    """Revoke module access from a user."""
    return admin_user_management_views.revoke_module_access(
        load_module_access=load_module_access,
        save_module_access=save_module_access,
        module_access=MODULE_ACCESS,
    )


# =============================================================================
# Password Manager Routes
# =============================================================================

@app.route('/admin/password_manager')
@admin_required
def admin_password_manager():
    """Password manager for all users."""
    return admin_user_management_views.render_admin_password_manager()


@app.route('/api/admin/password_manager/users')
@admin_required
def api_password_manager_users():
    """Get all users for password manager."""
    return admin_user_management_views.api_password_manager_users()


@app.route('/api/admin/password_manager/reset', methods=['POST'])
@admin_required
def api_password_manager_reset():
    """Reset user password."""
    return admin_user_management_views.api_password_manager_reset(
        password_validator=password_validator,
        password_hasher=password_hasher,
        log_security_event=log_security_event,
    )


@app.route('/api/admin/password_manager/force_change', methods=['POST'])
@admin_required
def api_password_manager_force_change():
    """Force user to change password on next login."""
    return admin_user_management_views.api_password_manager_force_change(
        log_security_event=log_security_event,
    )


@app.route('/api/admin/password_manager/toggle_status', methods=['POST'])
@admin_required
def api_password_manager_toggle_status():
    """Activate or deactivate user."""
    return admin_user_management_views.api_password_manager_toggle_status(
        log_security_event=log_security_event,
    )


@app.route('/api/admin/password_manager/generate')
@admin_required
def api_password_manager_generate():
    """Generate a strong random password."""
    return admin_user_management_views.api_password_manager_generate(
        password_validator=password_validator,
    )


@app.route('/admin/employees_database')
@module_access_required('employees_database')
def employees_database():
    """View all employee databases and information."""
    return employee_admin_views.render_employees_database(
        get_employee_directory=get_employee_directory,
    )

@app.route('/admin/employee_profiles_database')
@module_access_required('employee_profiles')
def employee_profiles_database():
    """Employee profiles database with detailed biographical information."""
    return employee_admin_views.render_employee_profiles_database(
        get_employee_directory=get_employee_directory,
    )

@app.route('/admin/add_user', methods=['GET', 'POST'])
@admin_required
def add_user():
    """Add new user to the system."""
    return employee_admin_views.handle_add_user(
        get_museum_employees=get_museum_employees,
        get_employee_directory=get_employee_directory,
        password_hasher=password_hasher,
    )

# Duplicate manage_access route removed - using manage_user_access instead

@app.route('/dashboard/customize', methods=['GET', 'POST'])
@login_required
def customize_dashboard():
    """Customize dashboard widget preferences."""
    return admin_user_management_views.customize_dashboard_preferences(
        load_dashboard_preferences=load_dashboard_preferences,
        save_dashboard_preferences=save_dashboard_preferences,
        dashboard_preferences=DASHBOARD_PREFERENCES,
        module_access=MODULE_ACCESS,
        user_has_module_access=user_has_module_access,
        dashboard_endpoint='dashboard',
    )

@app.route('/admin/reports')
@admin_required
def system_reports():
    """Generate system reports and analytics."""
    return museum_content_views.render_system_reports(
        get_library_database=get_library_database,
        get_employee_directory=get_employee_directory,
        get_exhibit_statistics=get_exhibit_statistics,
        user_has_module_access=user_has_module_access,
    )


@app.route('/admin/exhibits_database')
@admin_required
def exhibits_database():
    """Detailed inventory of museum artifacts and exhibits."""
    return museum_content_views.render_exhibits_database(
        exhibits_database=EXHIBITS_DATABASE,
        get_exhibit_statistics=get_exhibit_statistics,
    )


@app.route('/admin/exhibitions_database')
@module_access_required('exhibitions_database')
def exhibitions_database():
    """Timeline of gallery exhibitions with analytics."""
    return museum_content_views.render_exhibitions_database(
        exhibitions_database=EXHIBITIONS_DATABASE,
        get_exhibition_statistics=get_exhibition_statistics,
    )

@app.route('/admin/news')
@module_access_required('news')
def museum_news():
    """Museum news and announcements."""
    return museum_content_views.render_museum_news(
        news_database=NEWS_DATABASE,
    )


@app.route('/api/news/save', methods=['POST'])
@admin_required
def api_save_news():
    """Save a news article to the database."""
    return museum_content_views.api_save_news(
        news_database=NEWS_DATABASE,
    )


_RHMZ_WARNING_URL = dashboard_data_support.RHMZ_WARNING_URL
get_current_weather = dashboard_data_support.get_current_weather
get_weather_forecast = dashboard_data_support.get_weather_forecast
get_rhmz_weather_warnings = dashboard_data_support.get_rhmz_weather_warnings
fetch_website_news = dashboard_data_support.fetch_website_news


@app.route('/api/website-news')
@login_required
def api_website_news():
    """API endpoint to fetch news from museum website."""
    return dashboard_integration_views.api_website_news(
        fetch_website_news=fetch_website_news,
    )


@app.route('/api/weather/details')
@login_required
def api_weather_details():
    """Return current weather, 7-day forecast, and RHMZ warning status."""
    return dashboard_integration_views.api_weather_details(
        get_current_weather=get_current_weather,
        get_weather_forecast=get_weather_forecast,
        get_rhmz_weather_warnings=get_rhmz_weather_warnings,
        rhmz_warning_url=_RHMZ_WARNING_URL,
    )


@app.route('/admin/library_database')
@module_access_required('library_database')
def library_database():
    """Library database management system."""
    return dashboard_integration_views.render_library_database(
        get_library_database=get_library_database,
    )


# =============================================================================
# NATURAL HISTORY MUSEUM LONDON DATA PORTAL INTEGRATION
# =============================================================================

@app.route('/admin/nhm_data_portal')
@module_access_required('nhm_data_portal')
def nhm_data_portal():
    """Natural History Museum London Data Portal - browse and search 286 datasets."""
    return nhm_portal_views.render_nhm_data_portal()


@app.route('/api/nhm/search')
@login_required

def api_nhm_search():
    """API endpoint for NHM dataset search."""
    return nhm_portal_views.api_nhm_search()


@app.route('/api/nhm/dataset/<dataset_id>')
@login_required

def api_nhm_dataset(dataset_id):
    """Get detailed metadata for a NHM dataset."""
    return nhm_portal_views.api_nhm_dataset(dataset_id)


@app.route('/api/nhm/resource/<resource_id>')
@login_required

def api_nhm_resource(resource_id):
    """Get metadata for a NHM resource."""
    return nhm_portal_views.api_nhm_resource(resource_id)


@app.route('/api/nhm/datastore/<resource_id>')
@login_required

def api_nhm_datastore(resource_id):
    """Search within a NHM datastore resource."""
    return nhm_portal_views.api_nhm_datastore(resource_id)


@app.route('/api/nhm/statistics')
@login_required

def api_nhm_statistics():
    """Get NHM Data Portal statistics."""
    return nhm_portal_views.api_nhm_statistics()


# =============================================================================
# NHM LOCAL SEARCH (Downloaded Datasets)
# =============================================================================

@app.route('/api/nhm/local/search')
@login_required

def api_nhm_local_search():
    """Search through locally downloaded NHM datasets."""
    return nhm_portal_views.api_nhm_local_search()


@app.route('/api/nhm/local/dataset/<dataset_name>')
@login_required

def api_nhm_local_dataset(dataset_name):
    """Get locally stored dataset details."""
    return nhm_portal_views.api_nhm_local_dataset(dataset_name)


@app.route('/api/nhm/local/statistics')
@login_required

def api_nhm_local_statistics():
    """Get statistics about locally downloaded NHM data."""
    return nhm_portal_views.api_nhm_local_statistics()


@app.route('/api/nhm/local/tags')
@login_required

def api_nhm_local_tags():
    """Get all tags from locally downloaded datasets."""
    return nhm_portal_views.api_nhm_local_tags()


@app.route('/api/nhm/local/formats')
@login_required

def api_nhm_local_formats():
    """Get all resource formats from locally downloaded datasets."""
    return nhm_portal_views.api_nhm_local_formats()


@app.route('/api/nhm/local/authors')
@login_required

def api_nhm_local_authors():
    """Get all authors from locally downloaded datasets."""
    return nhm_portal_views.api_nhm_local_authors()


@app.route('/api/nhm/download', methods=['POST'])
@admin_required

def api_nhm_download_datasets():
    """Download/update NHM datasets (admin only)."""
    return nhm_portal_views.api_nhm_download_datasets()


# ============================================================================
# NHM DATA SEARCH ROUTES (Search both local museum and NHM data)
# ============================================================================

@app.route('/api/nhm/data/search/local')
@login_required
def api_nhm_data_search_local():
    """Search local museum databases."""
    return nhm_portal_views.api_nhm_data_search_local()


@app.route('/api/nhm/data/search/nhm')
@login_required
def api_nhm_data_search_nhm():
    """Search NHM specimen data via API."""
    return nhm_portal_views.api_nhm_data_search_nhm()


def prepare_collection_records_for_display(collection_type, records):
    """Apply QR highlight filtering for collection pages and return the active highlight."""
    return app_ui_support.prepare_collection_records_for_display(
        collection_type,
        records,
        apply_qr_highlight_filter=apply_qr_highlight_filter,
    )

@app.route('/admin/cultural_heritage_database')
@module_access_required('cultural_heritage')
def cultural_heritage_database():
    """Cultural heritage database management system (Заштићена културна добра)."""
    return collection_management_views.render_cultural_heritage_database(
        get_cultural_heritage_database=get_cultural_heritage_database,
        prepare_collection_records_for_display=prepare_collection_records_for_display,
        get_qr_collection_action_url=get_qr_collection_action_url,
        get_image_upload_action_url=get_image_upload_action_url,
    )

# Curator Collection Database Routes

@app.route('/admin/botany_collection')
@module_access_required('curator_collections')
def botany_collection():
    """Botany collection database."""
    return collection_management_views.render_standard_collection_database(
        collection_name='Ботаничка збирка',
        collection_icon='bi-flower1',
        collection_type='botany',
        records=BOTANY_COLLECTION_DATABASE['specimens'],
        statistics=BOTANY_COLLECTION_DATABASE['statistics'],
        prepare_collection_records_for_display=prepare_collection_records_for_display,
        get_qr_collection_action_url=get_qr_collection_action_url,
        get_image_upload_action_url=get_image_upload_action_url,
    )

@app.route('/admin/ichthyology_collection')
@module_access_required('curator_collections')
def ichthyology_collection():
    """Ichthyology collection database."""
    return collection_management_views.render_standard_collection_database(
        collection_name='Ихтиолошка збирка',
        collection_icon='bi-water',
        collection_type='ichthyology',
        records=ICHTHYOLOGY_COLLECTION_DATABASE['specimens'],
        statistics=ICHTHYOLOGY_COLLECTION_DATABASE['statistics'],
        prepare_collection_records_for_display=prepare_collection_records_for_display,
        get_qr_collection_action_url=get_qr_collection_action_url,
        get_image_upload_action_url=get_image_upload_action_url,
    )

@app.route('/admin/entomology_collection')
@module_access_required('curator_collections')
def entomology_collection():
    """Entomology collection database."""
    return collection_management_views.render_standard_collection_database(
        collection_name='Ентомолошка збирка',
        collection_icon='bi-bug',
        collection_type='entomology',
        records=ENTOMOLOGY_COLLECTION_DATABASE['specimens'],
        statistics=ENTOMOLOGY_COLLECTION_DATABASE['statistics'],
        prepare_collection_records_for_display=prepare_collection_records_for_display,
        get_qr_collection_action_url=get_qr_collection_action_url,
        get_image_upload_action_url=get_image_upload_action_url,
    )

@app.route('/admin/mycology_collection')
@module_access_required('curator_collections')
def mycology_collection():
    """Mycology collection database."""
    return collection_management_views.render_standard_collection_database(
        collection_name='Миколошка збирка',
        collection_icon='bi-tree',
        collection_type='mycology',
        records=MYCOLOGY_COLLECTION_DATABASE['specimens'],
        statistics=MYCOLOGY_COLLECTION_DATABASE['statistics'],
        prepare_collection_records_for_display=prepare_collection_records_for_display,
        get_qr_collection_action_url=get_qr_collection_action_url,
        get_image_upload_action_url=get_image_upload_action_url,
    )

@app.route('/admin/herpetology_collection')
@module_access_required('curator_collections')
def herpetology_collection():
    """Herpetology collection database."""
    return collection_management_views.render_standard_collection_database(
        collection_name='Херпетолошка збирка',
        collection_icon='bi-emoji-sunglasses',
        collection_type='herpetology',
        records=HERPETOLOGY_COLLECTION_DATABASE['specimens'],
        statistics=HERPETOLOGY_COLLECTION_DATABASE['statistics'],
        prepare_collection_records_for_display=prepare_collection_records_for_display,
        get_qr_collection_action_url=get_qr_collection_action_url,
        get_image_upload_action_url=get_image_upload_action_url,
    )

@app.route('/admin/ornithology_collection')
@module_access_required('curator_collections')
def ornithology_collection():
    """Ornithology collection database."""
    return collection_management_views.render_standard_collection_database(
        collection_name='Орнитолошка збирка',
        collection_icon='bi-feather',
        collection_type='ornithology',
        records=ORNITHOLOGY_COLLECTION_DATABASE['specimens'],
        statistics=ORNITHOLOGY_COLLECTION_DATABASE['statistics'],
        prepare_collection_records_for_display=prepare_collection_records_for_display,
        get_qr_collection_action_url=get_qr_collection_action_url,
        get_image_upload_action_url=get_image_upload_action_url,
    )

@app.route('/admin/paleozoology_collection')
@module_access_required('curator_collections')
def paleozoology_collection():
    """Paleozoology collection database."""
    return collection_management_views.render_standard_collection_database(
        collection_name='Палеозоолошка збирка',
        collection_icon='bi-gem',
        collection_type='paleozoology',
        records=PALEOZOOLOGY_COLLECTION_DATABASE['specimens'],
        statistics=PALEOZOOLOGY_COLLECTION_DATABASE['statistics'],
        prepare_collection_records_for_display=prepare_collection_records_for_display,
        get_qr_collection_action_url=get_qr_collection_action_url,
        get_image_upload_action_url=get_image_upload_action_url,
    )

@app.route('/admin/paleobotany_collection')
@module_access_required('curator_collections')
def paleobotany_collection():
    """Paleobotany collection database."""
    return collection_management_views.render_standard_collection_database(
        collection_name='Палеоботаничка збирка',
        collection_icon='bi-flower2',
        collection_type='paleobotany',
        records=PALEOBOTANY_COLLECTION_DATABASE['specimens'],
        statistics=PALEOBOTANY_COLLECTION_DATABASE['statistics'],
        prepare_collection_records_for_display=prepare_collection_records_for_display,
        get_qr_collection_action_url=get_qr_collection_action_url,
        get_image_upload_action_url=get_image_upload_action_url,
    )

@app.route('/admin/petrology_collection')
@module_access_required('curator_collections')
def petrology_collection():
    """Petrology collection database."""
    return collection_management_views.render_standard_collection_database(
        collection_name='Петролошка збирка',
        collection_icon='bi-mountains',
        collection_type='petrology',
        records=PETROLOGY_COLLECTION_DATABASE['specimens'],
        statistics=PETROLOGY_COLLECTION_DATABASE['statistics'],
        prepare_collection_records_for_display=prepare_collection_records_for_display,
        get_qr_collection_action_url=get_qr_collection_action_url,
        get_image_upload_action_url=get_image_upload_action_url,
    )

@app.route('/admin/meteorite_collection')
@module_access_required('curator_collections')
def meteorite_collection():
    """Meteorite collection database."""
    return collection_management_views.render_meteorite_collection(
        get_meteorite_collection_database=get_meteorite_collection_database,
        prepare_collection_records_for_display=prepare_collection_records_for_display,
        get_qr_collection_action_url=get_qr_collection_action_url,
        get_image_upload_action_url=get_image_upload_action_url,
    )

@app.route('/admin/mineral_collection')
@module_access_required('mineral_database')
def admin_mineral_collection():
    """Mineral collection database - Integrated from PrirodnjackiMuzej."""
    return collection_management_views.render_mineral_collection(
        get_mineral_database=get_mineral_database,
        get_image_upload_action_url=get_image_upload_action_url,
    )

@app.route('/admin/mineral_detail/<int:mineral_id>')
@module_access_required('mineral_database')
def admin_mineral_detail(mineral_id):
    """Mineral detail view."""
    return collection_management_views.render_mineral_detail(
        mineral_id,
        get_mineral_database=get_mineral_database,
    )

@app.route('/admin/rruff_minerals')
@module_access_required('mineral_database')
def admin_rruff_minerals():
    """Redirect to mineral collection in RRUFF mode."""
    return collection_management_views.redirect_rruff_minerals()

@app.route('/admin/rruff/detail/<int:mineral_id>')
@module_access_required('mineral_database')
def admin_rruff_detail(mineral_id):
    """RRUFF mineral detail view - shows all scientific data for a RRUFF database entry."""
    return collection_management_views.render_rruff_detail(
        mineral_id,
        get_mineral_database=get_mineral_database,
    )

@app.route('/admin/add_mineral', methods=['GET', 'POST'])
@module_access_required('mineral_database')
def add_mineral():
    """Add a new mineral to the collection."""
    return collection_management_views.handle_add_mineral(
        get_mineral_database=get_mineral_database,
    )

@app.route('/admin/edit_mineral/<int:mineral_id>', methods=['GET', 'POST'])
@module_access_required('mineral_database')
def edit_mineral(mineral_id):
    """Edit an existing mineral."""
    return collection_management_views.handle_edit_mineral(
        mineral_id,
        get_mineral_database=get_mineral_database,
        get_image_storage=get_image_storage,
    )


@app.route('/admin/edit_mineral/<int:mineral_id>/delete_image/<image_id>', methods=['POST'])
@module_access_required('mineral_database')
def delete_mineral_image(mineral_id, image_id):
    """Delete a mineral image from the edit screen."""
    return collection_management_views.handle_delete_mineral_image(
        mineral_id,
        image_id,
        get_mineral_database=get_mineral_database,
        get_image_storage=get_image_storage,
    )

@app.route('/admin/delete_mineral/<int:mineral_id>', methods=['POST'])
@module_access_required('mineral_database')
def delete_mineral(mineral_id):
    """Delete a mineral from the collection."""
    return collection_management_views.handle_delete_mineral(
        mineral_id,
        get_mineral_database=get_mineral_database,
    )

@app.route('/admin/inventory_book')
@admin_required
def inventory_book():
    """Inventory book sub-database - Physical inventory book records."""
    return collection_management_views.render_inventory_book()

@app.route('/admin/inventory_reconciliation', endpoint='inventory_reconciliation')
@admin_required
def inventory_reconciliation_view():
    """Inventory reconciliation tool - Compare book vs actual collection."""
    return collection_management_views.render_inventory_reconciliation()

@app.route('/admin/conservation_biology')
@admin_required
def conservation_biology():
    """Conservation biology records database."""
    return collection_management_views.render_conservation_biology(
        conservation_biology_database=CONSERVATION_BIOLOGY_DATABASE,
    )

# Collection PDF export route (placeholder)
@app.route('/admin/export_collection_to_pdf/<collection_type>')
@module_access_required('curator_collections')
def export_collection_to_pdf(collection_type):
    """Export collection to PDF - placeholder route."""
    return collection_management_views.export_collection_to_pdf(collection_type)

@app.route('/admin/museum_databases')
@module_access_required('museum_databases')
def museum_databases():
    """Overview of all museum databases."""
    global LIBRARY_DATABASE
    if LIBRARY_DATABASE is None:
        LIBRARY_DATABASE = load_library_database()
    return museum_overview_views.render_museum_databases(
        library_database=LIBRARY_DATABASE,
        get_employee_directory=get_employee_directory,
        get_museum_employees=get_museum_employees,
        get_mineral_database=get_mineral_database,
        get_meteorite_collection_database=get_meteorite_collection_database,
        get_cultural_heritage_database=get_cultural_heritage_database,
        get_exhibit_statistics=get_exhibit_statistics,
        get_exhibition_statistics=get_exhibition_statistics,
        bird_ringing_database=bird_ringing_database,
        scientific_papers_database=scientific_papers_database,
        botany_collection_database=BOTANY_COLLECTION_DATABASE,
        ichthyology_collection_database=ICHTHYOLOGY_COLLECTION_DATABASE,
        entomology_collection_database=ENTOMOLOGY_COLLECTION_DATABASE,
        mycology_collection_database=MYCOLOGY_COLLECTION_DATABASE,
        herpetology_collection_database=HERPETOLOGY_COLLECTION_DATABASE,
        ornithology_collection_database=ORNITHOLOGY_COLLECTION_DATABASE,
        paleozoology_collection_database=PALEOZOOLOGY_COLLECTION_DATABASE,
        paleobotany_collection_database=PALEOBOTANY_COLLECTION_DATABASE,
        petrology_collection_database=PETROLOGY_COLLECTION_DATABASE,
        conservation_biology_database=CONSERVATION_BIOLOGY_DATABASE,
        visitor_records=VISITOR_RECORDS,
        research_projects=RESEARCH_PROJECTS,
        get_qr_collection_action_url=get_qr_collection_action_url,
        get_image_upload_action_url=get_image_upload_action_url,
        get_image_upload_module_key=get_image_upload_module_key,
        user_has_module_access=user_has_module_access,
    )

# Error handlers
@app.errorhandler(404)
def not_found_error(error):
    return render_template('error.html',
                          error_code=404,
                          error_message="Страница није пронађена"), 404

@app.errorhandler(500)
def internal_error(error):
    current_app.logger.error(f"500 Internal Server Error: {error}")
    current_app.logger.exception("Full traceback:")
    return render_template('error.html',
                          error_code=500,
                          error_message="Интерна грешка сервера"), 500

# Sub-application mounting (temporarily disabled)
def create_timesheet_app_disabled():
    """Create and configure timesheet sub-application."""
    try:
        # Add timesheet path to sys.path if not already there
        if localsql_path not in sys.path:
            sys.path.insert(0, localsql_path)

        # Import the timesheet app
        spec = importlib.util.spec_from_file_location("timesheet_app",
                                                    os.path.join(localsql_path, "start_ultra_fast.py"))
        timesheet_module = importlib.util.module_from_spec(spec)

        # Save current directory and change to timesheet app directory
        old_cwd = os.getcwd()
        os.chdir(localsql_path)

        try:
            # Execute the module
            spec.loader.exec_module(timesheet_module)

            # Get the Flask app from the module
            timesheet_app = timesheet_module.app

            # Configure the app for sub-mounting
            timesheet_app.config['APPLICATION_ROOT'] = '/timesheet'

            logging.info("✅ Timesheet app created successfully")
            return timesheet_app
        finally:
            # Restore original directory
            os.chdir(old_cwd)
    except Exception as e:
        logging.error(f"❌ Could not create timesheet app: {e}")
        return None

def create_mineral_app_disabled():
    """Create and configure mineral database sub-application."""
    try:
        # Add mineral path to sys.path if not already there
        if prirodnjacki_path not in sys.path:
            sys.path.insert(0, prirodnjacki_path)

        # Import the mineral database app
        spec = importlib.util.spec_from_file_location("mineral_app",
                                                    os.path.join(prirodnjacki_path, "app.py"))
        mineral_module = importlib.util.module_from_spec(spec)

        # Save current directory and change to mineral app directory
        old_cwd = os.getcwd()
        os.chdir(prirodnjacki_path)

        try:
            spec.loader.exec_module(mineral_module)

            # Create the app using the create_app function
            mineral_app = mineral_module.application if hasattr(mineral_module, 'application') else mineral_module.app

            # Configure the app for sub-mounting
            mineral_app.config['APPLICATION_ROOT'] = '/mineral'

            logging.info("✅ Mineral app created successfully")
            return mineral_app
        finally:
            # Restore original directory
            os.chdir(old_cwd)
    except Exception as e:
        logging.error(f"❌ Could not create mineral app: {e}")
        return None

# Template context
@app.context_processor
def utility_processor():
    """Add utility functions to template context."""
    def user_logged_in():
        return 'user_id' in session

    def is_admin():
        return session.get('user_role') == 'admin'

    def endpoint_exists(endpoint_name):
        return endpoint_name in current_app.view_functions

    try:
        weather_data = get_current_weather()
    except Exception:
        weather_data = {'condition': DEFAULT_WEATHER_CONDITION, 'temperature': None, 'windspeed': None, 'description': ''}

    try:
        weather_script_version = int((Path(current_dir) / 'static' / 'js' / 'weather_particles.js').stat().st_mtime)
    except OSError:
        weather_script_version = int(time.time())

    def has_module_access(module_key):
        """Check if current user has access to a module. For use in templates."""
        _email = session.get('user_email', '')
        _role = session.get('user_role', '')
        if not _email and not _role:
            return False
        return user_has_module_access(_email, _role, module_key)

    return dict(
        user_logged_in=user_logged_in,
        user_name=session.get('user_name', ''),
        user_role=session.get('user_role', ''),
        user_email=session.get('user_email', ''),
        is_admin=is_admin,
        endpoint_exists=endpoint_exists,
        has_module_access=has_module_access,
        weather_condition=weather_data['condition'],
        weather_temperature=weather_data.get('temperature'),
        weather_windspeed=weather_data.get('windspeed'),
        weather_description=weather_data.get('description', ''),
        weather_particles_version=weather_script_version,
        current_lang=session.get('museum_lang', request.cookies.get('museum_lang', 'sr-Cyrl'))
    )


# ===== ZAHTEVI (Requests) Routes =====

@app.route('/zahtevi/finansijski')
@login_required
def finansijski_zahtevi():
    """Financial requests page."""
    return travel_finance_views.render_financial_requests_page()


@app.route('/zahtevi/slobodan-dan')
@login_required
def zahtev_slobodan_dan():
    """Day off request page."""
    return travel_finance_views.render_day_off_request_page()


@app.route('/zahtevi/godisnji-odmor')
@login_required
def zahtev_godisnji_odmor():
    """Vacation request page."""
    return travel_finance_views.render_vacation_request_page()


@app.route('/zahtevi/razno')
@login_required
def zahtev_razno():
    """Miscellaneous request page."""
    return travel_finance_views.render_misc_request_page()


# ===== FINANSIJE (Finance) Routes =====

@app.route('/finansije/plan')
@login_required
def finansijski_plan():
    """Financial plan page."""
    return travel_finance_views.render_financial_plan_page()


@app.route('/finansije/nabavka')
@app.route('/zahtevi/nabavka')
@login_required
def zahtev_nabavka():
    """Procurement request page."""
    return travel_finance_views.render_procurement_request_page()


# ===== TERENSKA AKTIVNOST (Field Activity) Route =====

@app.route('/terenska-aktivnost')
@login_required
def terenska_aktivnost():
    """Field activity page."""
    return travel_finance_views.render_field_activity_page()


@app.route('/zahtev-sluzbeni-put')
@login_required
def zahtev_sluzbeni_put():
    """Business trip request form with vehicle and timesheet integration."""
    return travel_finance_views.render_business_trip_request_page(
        get_museum_vehicles=get_museum_vehicles,
    )


@app.route('/api/field-trip/create', methods=['POST'])

@login_required
def api_field_trip_create():
    """Create field trip request with vehicle reservation and timesheet entries."""
    return travel_finance_views.api_field_trip_create(
        get_vehicle_reservations=get_vehicle_reservations,
        save_reservations=save_reservations,
    )


@app.route('/api/accommodation/search', methods=['POST'])

@login_required
def api_accommodation_search():
    """Search for accommodation options using OpenStreetMap and Google Places APIs."""
    return travel_finance_views.api_accommodation_search()


@app.route('/api/route/calculate', methods=['POST'])

@login_required
def api_route_calculate():
    """Calculate route distance and toll from static database."""
    return travel_finance_views.api_route_calculate(
        get_museum_vehicles=get_museum_vehicles,
    )


# ===== NABAVKA (Procurement) API Routes =====

@app.route('/api/nabavka/save', methods=['POST'])
@login_required
def api_nabavka_save():
    """Save procurement request to database."""
    return travel_finance_views.api_nabavka_save()


@app.route('/api/nabavka/list')
@login_required
def api_nabavka_list():
    """List procurement requests for current user."""
    return travel_finance_views.api_nabavka_list()


@app.route('/api/nabavka/export-word', methods=['POST'])
@login_required
def api_nabavka_export_word():
    """Export procurement request to Word document."""
    return travel_finance_views.api_nabavka_export_word()


@app.route('/api/nabavka/export-word/<int:request_id>')
@login_required
def api_nabavka_export_word_by_id(request_id):
    """Export saved procurement request to Word document by ID."""
    return travel_finance_views.api_nabavka_export_word_by_id(
        request_id,
        can_access_owned_record=can_access_owned_record,
    )


# ============================================
# Financial Plan API Routes
# ============================================

@app.route('/api/finansijski-plan/save', methods=['POST'])
@login_required
def api_finansijski_plan_save():
    """Save financial plan to database."""
    return travel_finance_views.api_finansijski_plan_save(
        get_postgres_connection=get_postgres_connection,
    )


@app.route('/api/finansijski-plan/list')
@login_required
def api_finansijski_plan_list():
    """List financial plans for current user."""
    return travel_finance_views.api_finansijski_plan_list(
        get_postgres_connection=get_postgres_connection,
        current_user_is_admin=current_user_is_admin,
    )


@app.route('/api/finansijski-plan/export-word', methods=['POST'])
@login_required
def api_finansijski_plan_export_word():
    """Export financial plan to Word document."""
    return travel_finance_views.api_finansijski_plan_export_word()


@app.route('/api/finansijski-plan/export-word/<int:plan_id>')
@login_required
def api_finansijski_plan_export_word_by_id(plan_id):
    """Export saved financial plan to Word document by ID."""
    return travel_finance_views.api_finansijski_plan_export_word_by_id(
        plan_id,
        get_postgres_connection=get_postgres_connection,
        can_access_owned_record=can_access_owned_record,
    )


# Simple app runner (complex mounting disabled for now)
_background_jobs_started = False


def start_background_jobs():
    """Start optional background jobs once per process."""
    global _background_jobs_started

    if _background_jobs_started:
        return False

    app_root = os.path.dirname(os.path.abspath(__file__))
    update_science_news_background(app_root)
    map_feature_paper_enricher.start_enrichment_background()
    _background_jobs_started = True
    return True


def create_app(start_background_services: bool = False):
    """Create the main application (simplified version)."""
    if start_background_services and start_background_jobs():
        logger.info("Started optional background services")

    return app

# Route handlers for input forms

@app.route('/admin/add_book', methods=['GET', 'POST'])
@admin_required
def add_book():
    """Add new book to library database."""
    global LIBRARY_DATABASE
    if LIBRARY_DATABASE is None:
        LIBRARY_DATABASE = load_library_database()
    return museum_content_views.handle_add_book(
        library_database=LIBRARY_DATABASE,
        save_library_database=save_library_database,
        phase3a_databases=globals().get('phase3a_databases'),
    )

@app.route('/admin/add_heritage_item', methods=['GET', 'POST'])
@admin_required
def add_heritage_item():
    """Add new heritage item to cultural heritage database."""
    return collection_management_views.handle_add_heritage_item(
        get_cultural_heritage_database=get_cultural_heritage_database,
    )

@app.route('/admin/add_collection_item/<collection_type>', methods=['GET', 'POST'])
@module_access_required('curator_collections')
def add_collection_item(collection_type):
    """Add new item to a curator collection."""
    return collection_management_views.handle_add_collection_item(
        collection_type,
        museum_databases_endpoint='museum_databases',
    )

@app.route('/admin/add_visitor', methods=['GET', 'POST'])
@admin_required
def add_visitor():
    """Add new visitor record."""
    return museum_content_views.handle_add_visitor(
        visitor_records=VISITOR_RECORDS,
    )

@app.route('/admin/add_research', methods=['GET', 'POST'])
@admin_required
def add_research():
    """Add new research project record."""
    return museum_content_views.handle_add_research(
        research_projects=RESEARCH_PROJECTS,
    )

@app.route('/admin/visitors_database')
@admin_required
def visitors_database():
    """View visitors database."""
    return museum_content_views.render_visitors_database(
        visitor_records=VISITOR_RECORDS,
    )

@app.route('/admin/export_visitors_to_pdf')
@admin_required
def export_visitors_to_pdf():
    """Export visitors statistics to PDF - placeholder route."""
    return museum_content_views.export_visitors_to_pdf(
        visitors_endpoint='visitors_database',
    )

@app.route('/admin/research_database')
@admin_required
def research_database():
    """View research projects database."""
    return museum_content_views.render_research_database(
        research_projects=RESEARCH_PROJECTS,
    )

# ============================================================
# Projekti - New Museum Building Project
# ============================================================

@app.route('/admin/projekti')
@login_required
def admin_projekti():
    """View the new museum building project page."""
    return project_views.render_projects_page()


@app.route('/admin/projekti/dokumentacija')
@login_required
def admin_projekti_dokumentacija():
    """Read project documentation inline inside the application."""
    return project_views.render_project_documentation(
        app_root_path=app.root_path,
    )


PROJECT_SPACE_PLANNER_FILE = Path(app.root_path) / 'data' / 'project_space_planner.json'
PROJECT_SPACE_PLAN_FILE = project_views.PROJECT_SPACE_PLAN_FILE
PROJECT_SPACE_PLAN_IMAGE_SIZE = project_views.PROJECT_SPACE_PLAN_IMAGE_SIZE
PROJECT_SPACE_DEPOT_PLAN_FILE = project_views.PROJECT_SPACE_DEPOT_PLAN_FILE
PROJECT_SPACE_DEPOT_PLAN_IMAGE_SIZE = project_views.PROJECT_SPACE_DEPOT_PLAN_IMAGE_SIZE
PROJECT_DEPOT_PLAN_AREA_ANNOTATIONS = project_views.PROJECT_DEPOT_PLAN_AREA_ANNOTATIONS
PROJECT_DEPOT_AUTO_DETECTED_SPACES = project_views.PROJECT_DEPOT_AUTO_DETECTED_SPACES
PROJECT_AUTO_LAYOUT_VERSION = project_views.PROJECT_AUTO_LAYOUT_VERSION
PROJECT_SPACE_PLAN_VIEWS = project_views.PROJECT_SPACE_PLAN_VIEWS
PROJECT_SPACE_LIBRARY = project_views.PROJECT_SPACE_LIBRARY
PROJECT_COMMON_TERMS = project_views.PROJECT_COMMON_TERMS

PROJECT_AUTO_DETECTED_SPACES = project_views.PROJECT_AUTO_DETECTED_SPACES


@app.route('/admin/projekti/space-planner')
@login_required
def admin_projekti_space_planner():
    """Interactive editor for plan -5 room specifications."""
    return project_views.render_project_space_planner()


@app.route('/api/projekti/space-planner')
@login_required
def api_projekti_space_planner_get():
    """Return stored room zones and terminology for the -5 plan editor."""
    return project_views.api_project_space_planner_get(
        planner_file=PROJECT_SPACE_PLANNER_FILE,
        auto_layout_version=PROJECT_AUTO_LAYOUT_VERSION,
        project_space_plan_views=PROJECT_SPACE_PLAN_VIEWS,
        project_space_plan_file=PROJECT_SPACE_PLAN_FILE,
        project_space_plan_image_size=PROJECT_SPACE_PLAN_IMAGE_SIZE,
        project_space_library=PROJECT_SPACE_LIBRARY,
        project_common_terms=PROJECT_COMMON_TERMS,
        project_auto_detected_spaces=PROJECT_AUTO_DETECTED_SPACES,
        project_depot_auto_detected_spaces=PROJECT_DEPOT_AUTO_DETECTED_SPACES,
    )


@app.route('/api/projekti/space-planner', methods=['POST'])
@login_required
def api_projekti_space_planner_save():
    """Persist room zones and room specifications for the -5 plan editor."""
    return project_views.api_project_space_planner_save(
        planner_file=PROJECT_SPACE_PLANNER_FILE,
        auto_layout_version=PROJECT_AUTO_LAYOUT_VERSION,
        project_space_plan_file=PROJECT_SPACE_PLAN_FILE,
        project_space_library=PROJECT_SPACE_LIBRARY,
    )


@app.route('/projekti_files/<path:filename>')
@login_required
def projekti_file(filename):
    """Serve files from the Projekti folder."""
    return project_views.serve_project_file(
        filename,
        project_directory='Projekti',
    )

# ============================================================
# Scientific Papers Database Routes
# ============================================================

@app.route('/admin/scientific_papers')
@module_access_required('scientific_papers')
def scientific_papers_view():
    """Browse scientific papers with pagination and filters."""
    return scientific_paper_views.render_scientific_papers(
        scientific_papers_database=scientific_papers_database,
        museum_databases_endpoint='museum_databases',
    )


@app.route('/admin/scientific_paper/<int:paper_id>')
@module_access_required('scientific_papers')
def scientific_paper_detail(paper_id):
    """View detailed information for a single scientific paper."""
    return scientific_paper_views.render_scientific_paper_detail(
        paper_id=paper_id,
        scientific_papers_database=scientific_papers_database,
        list_endpoint='scientific_papers_view',
    )


@app.route('/admin/scientific_papers/locality/<locality_name>')
@module_access_required('scientific_papers')
def scientific_papers_by_locality(locality_name):
    """View papers for a specific geological map sheet locality."""
    return scientific_paper_views.render_scientific_papers_by_locality(
        locality_name=locality_name,
        scientific_papers_database=scientific_papers_database,
    )


@app.route('/api/map/locality-papers/<locality_name>')
@login_required
def api_locality_papers(locality_name):
    """JSON API for locality paper summary (map popup integration)."""
    return scientific_paper_views.api_locality_papers(
        locality_name=locality_name,
        scientific_papers_database=scientific_papers_database,
    )


@app.route('/api/map/feature-papers/<feature_type>/<path:feature_name>')
@login_required
def api_feature_papers(feature_type, feature_name):
    """JSON API for feature paper summary (map popup integration)."""
    return scientific_paper_views.api_feature_papers(
        feature_type=feature_type,
        feature_name=feature_name,
        map_feature_paper_enricher=map_feature_paper_enricher,
    )


@app.route('/api/admin/start-paper-enrichment', methods=['POST'])
@admin_required
def api_start_paper_enrichment():
    """Admin trigger for background paper enrichment."""
    return scientific_paper_views.api_start_paper_enrichment(
        map_feature_paper_enricher=map_feature_paper_enricher,
    )


@app.route('/api/admin/paper-enrichment-status')
@admin_required
def api_paper_enrichment_status():
    """Progress polling for paper enrichment."""
    return scientific_paper_views.api_paper_enrichment_status(
        map_feature_paper_enricher=map_feature_paper_enricher,
    )


@app.route('/admin/bird_ringing_database')
@module_access_required('bird_ringing_database')
def bird_ringing_database_view():
    """View bird ringing database with pagination and filters."""
    return bird_ringing_views.render_bird_ringing_database(
        bird_ringing_database=bird_ringing_database,
        museum_databases_endpoint='museum_databases',
    )

@app.route('/admin/bird_ringing_record/<int:record_id>')
@module_access_required('bird_ringing_database')
def bird_ringing_record_detail(record_id):
    """View detailed information for a single bird ringing record."""
    return bird_ringing_views.render_bird_ringing_record_detail(
        record_id=record_id,
        bird_ringing_database=bird_ringing_database,
        list_endpoint='bird_ringing_database_view',
    )

@app.route('/admin/add_bird_ringing', methods=['GET', 'POST'])
@admin_required
def add_bird_ringing():
    """Add a new bird ringing record."""
    return bird_ringing_views.handle_add_bird_ringing(
        bird_ringing_database=bird_ringing_database,
        detail_endpoint='bird_ringing_record_detail',
        list_endpoint='bird_ringing_database_view',
    )

@app.route('/museum_terminology')
@login_required
def museum_terminology():
    """Display museum terminology page."""
    return exhibition_planner_views.render_museum_terminology()

@app.route('/exhibition_planner')
@login_required
def exhibition_planner():
    """Display exhibition planning tool."""
    return exhibition_planner_views.render_exhibition_planner()


# ============================================================================
# EXHIBITION PLANNER API ROUTES
# ============================================================================

@app.route('/api/exhibitions', methods=['GET'])
@login_required
def api_get_exhibitions():
    """Get exhibitions for the planner based on user role.

    - Admin and Direktor: See all exhibitions
    - Other users: See only their own exhibitions + active exhibitions
    """
    return exhibition_planner_views.api_get_exhibitions()


@app.route('/api/exhibitions', methods=['POST'])
@login_required
def api_create_exhibition():
    """Create a new exhibition."""
    return exhibition_planner_views.api_create_exhibition()


@app.route('/api/exhibitions/<int:exhibition_id>', methods=['PUT'])
@login_required
def api_update_exhibition(exhibition_id):
    """Update an existing exhibition. Only owner or admin/direktor can update."""
    return exhibition_planner_views.api_update_exhibition(exhibition_id)


@app.route('/api/exhibitions/<int:exhibition_id>', methods=['DELETE'])
@login_required
def api_delete_exhibition(exhibition_id):
    """Delete an exhibition. Only owner or admin/direktor can delete."""
    return exhibition_planner_views.api_delete_exhibition(exhibition_id)


@app.route('/api/exhibitions/<int:exhibition_id>/checklist', methods=['PUT'])
@login_required
def api_update_exhibition_checklist(exhibition_id):
    """Update exhibition checklist data."""
    return exhibition_planner_views.api_update_exhibition_checklist(exhibition_id)


@app.route('/vehicle_reservations')
@login_required
def vehicle_reservations():
    """Display vehicle reservation calendar."""
    return vehicle_depot_views.render_vehicle_reservations(
        get_museum_vehicles=get_museum_vehicles,
        get_vehicle_reservations=get_vehicle_reservations,
    )

@app.route('/add_vehicle_reservation', methods=['POST'])
@login_required
def add_vehicle_reservation():
    """Add new vehicle reservation."""
    return vehicle_depot_views.handle_add_vehicle_reservation(
        phase3a_databases=globals().get('phase3a_databases'),
        get_vehicle_reservations=get_vehicle_reservations,
        save_reservations=save_reservations,
    )

@app.route('/vehicle_management')
@admin_required
def vehicle_management():
    """Display vehicle management page."""
    return vehicle_depot_views.render_vehicle_management(
        get_museum_vehicles=get_museum_vehicles,
        get_vehicle_reservations=get_vehicle_reservations,
    )

@app.route('/add_vehicle', methods=['POST'])
@admin_required
def add_vehicle():
    """Add new vehicle."""
    return vehicle_depot_views.handle_add_vehicle(
        phase3a_databases=globals().get('phase3a_databases'),
        get_museum_vehicles=get_museum_vehicles,
        save_vehicles=save_vehicles,
    )

@app.route('/edit_vehicle', methods=['POST'])
@admin_required
def edit_vehicle():
    """Edit existing vehicle."""
    return vehicle_depot_views.handle_edit_vehicle(
        phase3a_databases=globals().get('phase3a_databases'),
        get_museum_vehicles=get_museum_vehicles,
        save_vehicles=save_vehicles,
    )

@app.route('/delete_vehicle', methods=['POST'])
@admin_required
def delete_vehicle():
    """Delete vehicle."""
    return vehicle_depot_views.handle_delete_vehicle(
        phase3a_databases=globals().get('phase3a_databases'),
        get_museum_vehicles=get_museum_vehicles,
        get_vehicle_reservations=get_vehicle_reservations,
        save_vehicles=save_vehicles,
    )

# Public QR Code View Route (No authentication required)
@app.route('/qr_view/<collection_type>/<catalog_number>')
@limiter.limit("30 per minute")
def qr_view_specimen(collection_type, catalog_number):
    """Public mobile-optimized view for QR code scanned specimens."""
    return collection_media_views.render_qr_view_specimen(
        collection_type,
        catalog_number,
        normalize_qr_collection_type=normalize_qr_collection_type,
        get_meteorite_collection_database=get_meteorite_collection_database,
        botany_collection_database=BOTANY_COLLECTION_DATABASE,
        paleozoology_collection_database=PALEOZOOLOGY_COLLECTION_DATABASE,
    )


# ============================================================================
# VIRTUAL 3D MINERAL DEPOT
# ============================================================================

@app.route('/admin/virtual_depot')
@admin_required
def virtual_depot():
    """3D Virtual Mineral Depot - Three.js visualization of mineral storage."""
    return vehicle_depot_views.render_virtual_depot()


@app.route('/api/depot/boxes', methods=['GET'])
@login_required

def api_get_depot_boxes():
    """Get all boxes with mineral counts for 3D depot."""
    return vehicle_depot_views.api_get_depot_boxes()


@app.route('/api/depot/box/<box_id>', methods=['GET'])
@login_required

def api_get_box_contents(box_id):
    """Get contents of a specific box."""
    return vehicle_depot_views.api_get_box_contents(box_id)


def format_chemical_formula(formula: str) -> str:
    """Convert RRUFF formula markup to Unicode subscript/superscript characters."""
    return mineral_science_views.format_chemical_formula(formula)


@app.route('/api/rruff/mineral/<mineral_name>', methods=['GET'])
@login_required

def api_get_rruff_data(mineral_name):
    """Get RRUFF scientific data for mineral(s) by name.
    Handles Serbian names and multiple minerals in one entry.
    """
    return mineral_science_views.api_get_rruff_data(mineral_name)


# =====================================================
# COD (Crystallography Open Database) API Endpoints
# =====================================================

@app.route('/api/cod/search/<mineral_name>', methods=['GET'])
@login_required

def api_cod_search(mineral_name):
    """Search COD for crystal structure data by mineral name.
    Handles both Serbian and English names, and combined mineral names.
    """
    return mineral_science_views.api_cod_search(mineral_name)


@app.route('/api/cod/cif/<entry_id>', methods=['GET'])
@login_required

def api_cod_get_cif(entry_id):
    """Get CIF file content for a database entry (for 3D visualization).
    Supports COD, AMCSD, and RRUFF entries.
    """
    return mineral_science_views.api_cod_get_cif(entry_id)


@app.route('/api/crystal/cif', methods=['GET'])
@login_required

def api_crystal_get_cif_by_url():
    """Get CIF file content by direct URL."""
    return mineral_science_views.api_crystal_get_cif_by_url()


@app.route('/api/crystal/local/<entry_id>', methods=['GET'])
@login_required

def api_crystal_get_local_cif(entry_id):
    """Get CIF file content from local storage or download on demand.

    Supports both RRUFF IDs (R000001) and COD IDs (1000001).
    Uses rsync for COD when HTTP fails (more reliable).
    """
    return mineral_science_views.api_crystal_get_local_cif(entry_id)


@app.route('/api/cod/structure/<mineral_name>', methods=['GET'])
@login_required

def api_cod_get_structure(mineral_name):
    """Get complete crystal structure data for a mineral including CIF.
    Handles both Serbian and English names, and combined mineral names.
    """
    return mineral_science_views.api_cod_get_structure(mineral_name)


@app.route('/api/depot/localities', methods=['GET'])
@login_required

def api_get_localities():
    """Get all unique localities from the mineral collection with counts and info."""
    return depot_science_views.api_get_localities(
        get_mineral_database=get_mineral_database,
    )


@app.route('/api/science-news', methods=['GET'])
@login_required

def api_get_science_news():
    """Get curated science news from database with optional filters."""
    return depot_science_views.api_get_science_news()


@app.route('/api/science-news', methods=['POST'])
@admin_required

def api_add_science_news():
    """Add a new science news item."""
    return depot_science_views.api_add_science_news()


@app.route('/api/science-news/<news_id>', methods=['DELETE'])
@admin_required

def api_delete_science_news(news_id):
    """Delete a science news item."""
    return depot_science_views.api_delete_science_news(news_id=news_id)


@app.route('/api/depot/locality/<path:locality_name>', methods=['GET'])
@login_required

def api_get_locality_detail(locality_name):
    """Get detailed information about a specific locality."""
    return depot_science_views.api_get_locality_detail(
        locality_name,
        get_mineral_database=get_mineral_database,
    )


# =====================================================
# EarthChem/GEOROC Geochemical Database API Endpoints
# =====================================================

@app.route('/api/geochemical/<mineral_name>', methods=['GET'])
@login_required

def api_get_geochemical_data(mineral_name):
    """Get geochemical data for a mineral from EarthChem Portal and GEOROC 2.0 databases.

    Returns major/trace element compositions, isotope ratios, and geological context.
    Handles Serbian mineral names via translation.
    """
    return mineral_science_views.api_get_geochemical_data(mineral_name)


# =====================================================
# Local RRUFF Data API Endpoints
# =====================================================

@app.route('/api/local_rruff/<mineral_name>', methods=['GET'])
@login_required

def api_get_local_rruff_data(mineral_name):
    """Get all local RRUFF data for a mineral (powder, Raman, IR, images)."""
    return mineral_science_views.api_get_local_rruff_data(mineral_name)


@app.route('/api/local_rruff/dif/<mineral_name>', methods=['GET'])
@login_required

def api_get_local_rruff_dif(mineral_name):
    """Get DIF crystal structure data for 3D visualization."""
    return mineral_science_views.api_get_local_rruff_dif(mineral_name)


@app.route('/api/local_rruff/cif/<mineral_name>', methods=['GET'])
@login_required

def api_get_local_rruff_cif(mineral_name):
    """Generate CIF file content from DIF data for 3Dmol.js visualization.

    Query parameters:
        view_mode: 'asymmetric' (default), 'unitcell', or 'supercell'
    """
    return mineral_science_views.api_get_local_rruff_cif(mineral_name)


@app.route('/api/local_rruff/spectrum/<spectrum_type>/<mineral_name>', methods=['GET'])
@login_required

def api_get_local_rruff_spectrum(spectrum_type, mineral_name):
    """Get Raman or infrared spectrum data for a mineral."""
    return mineral_science_views.api_get_local_rruff_spectrum(spectrum_type, mineral_name)


@app.route('/api/local_rruff/powder_xy/<mineral_name>', methods=['GET'])
@login_required

def api_get_local_rruff_powder_xy(mineral_name):
    """Get powder diffraction XY profile data for chart visualization."""
    return mineral_science_views.api_get_local_rruff_powder_xy(mineral_name)


@app.route('/api/local_rruff/image/<path:image_path>')
@login_required
def api_serve_local_rruff_image(image_path):
    """Serve RRUFF image files."""
    return mineral_science_views.api_serve_local_rruff_image(image_path)


@app.route('/api/local_rruff/microprobe/<mineral_name>', methods=['GET'])
@login_required
def api_get_local_rruff_microprobe(mineral_name):
    """Get microprobe data for a mineral from local RRUFF chemistry files."""
    return mineral_science_views.api_get_local_rruff_microprobe(mineral_name)


# ==================== EMAIL CLIENT ROUTES ====================

@app.route('/mail')
@login_required
def mail_client_page():
    """Render the three-pane email client."""
    return mail_views.render_mail_client_page()


@app.route('/mail/settings')
@login_required
def mail_settings_page():
    """Render the email settings configuration page."""
    return mail_views.render_mail_settings_page()


@app.route('/api/mail/contacts')
@login_required
def api_mail_contacts():
    """Return all museum employee emails as a contact list."""
    return mail_views.api_mail_contacts(
        get_employee_directory=get_employee_directory,
    )


@app.route('/api/mail/init')
@login_required
def api_mail_init():
    """Combined init: return folders + first message page in one call."""
    return mail_views.api_mail_init()


@app.route('/api/mail/folders')
@login_required
def api_mail_folders():
    """List IMAP folders with unread counts."""
    return mail_views.api_mail_folders()


@app.route('/api/mail/messages')
@login_required
def api_mail_messages():
    """Paginated message list for a folder."""
    return mail_views.api_mail_messages()


@app.route('/api/mail/message/<uid>')
@login_required
def api_mail_message(uid):
    """Fetch a single message by UID."""
    return mail_views.api_mail_message(uid)


@app.route('/api/mail/attachment/<uid>/<int:att_index>')
@login_required
def api_mail_attachment(uid, att_index):
    """Download a message attachment by UID and attachment index."""
    return mail_views.api_mail_attachment(uid, att_index)


@app.route('/api/mail/attachments-all/<uid>')
@login_required
def api_mail_attachments_all(uid):
    """Download all attachments as a ZIP file."""
    return mail_views.api_mail_attachments_all(uid)


@app.route('/api/mail/send', methods=['POST'])
@login_required
def api_mail_send():
    """Send an email via SMTP, with optional file attachments."""
    return mail_views.api_mail_send()


@app.route('/api/mail/delete', methods=['POST'])
@login_required
def api_mail_delete():
    """Delete a message."""
    return mail_views.api_mail_delete()


@app.route('/api/mail/read-state', methods=['POST'])
@login_required
def api_mail_read_state():
    """Set read/unread state for a message."""
    return mail_views.api_mail_read_state()


@app.route('/api/mail/move', methods=['POST'])
@login_required
def api_mail_move():
    """Move a message between folders."""
    return mail_views.api_mail_move()


@app.route('/api/mail/check')
@login_required
def api_mail_check():
    """Return unread count for navbar badge (from local cache — instant)."""
    return mail_views.api_mail_check()


@app.route('/api/mail/sync', methods=['POST'])
@login_required
def api_mail_sync():
    """Trigger an immediate IMAP sync (used by refresh button)."""
    return mail_views.api_mail_sync()


@app.route('/api/mail/settings', methods=['GET'])
@login_required
def api_mail_settings_get():
    """Return mail settings for the current user (password excluded)."""
    return mail_views.api_mail_settings_get()


@app.route('/api/mail/settings', methods=['POST'])
@login_required
def api_mail_settings_save():
    """Save mail settings for the current user."""
    return mail_views.api_mail_settings_save()


@app.route('/api/mail/test-connection', methods=['POST'])
@login_required
def api_mail_test_connection():
    """Test IMAP or SMTP connection."""
    return mail_views.api_mail_test_connection()


# ==================== END EMAIL CLIENT ROUTES ====================


# ==================== CHAT ROOM ROUTES ====================

@app.route('/chat')
@login_required
def chat_room_page():
    """Render the employee chat room."""
    return chat_views.render_chat_room_page()


@app.route('/api/chat/messages')
@login_required
def api_chat_messages():
    """Get chat messages. Pass ?since=epoch&channel=general for incremental polling."""
    return chat_views.api_chat_messages()


@app.route('/api/chat/send', methods=['POST'])
@login_required
def api_chat_send():
    """Send a chat message (text and/or file). Accepts JSON or multipart/form-data."""
    return chat_views.api_chat_send()


@app.route('/api/chat/status', methods=['POST'])
@login_required
def api_chat_status():
    """Set user's chat status (online/busy/offline)."""
    return chat_views.api_chat_status()


@app.route('/api/chat/file/<filename>')
@login_required
def api_chat_file(filename):
    """Serve a chat file attachment for download."""
    return chat_views.api_chat_file(filename)


@app.route('/api/chat/leave', methods=['POST'])
@csrf.exempt
@login_required
def api_chat_leave():
    """Clear presence when user leaves chat page (sendBeacon, no CSRF)."""
    return chat_views.api_chat_leave()


# ==================== END CHAT ROOM ROUTES ====================


# ==================== MAP / KARTE ROUTES ====================

_KMZ_PATH = maps_terrain_support.KMZ_PATH
_TILE_CACHE_DIR = maps_terrain_support.TILE_CACHE_DIR
_build_tile_index = maps_terrain_support.build_tile_index
_extract_tile_to_cache = maps_terrain_support.extract_tile_to_cache
_DEM_DIR = maps_terrain_support.DEM_DIR


@app.route('/admin/maps')
@module_access_required('maps_karte')
def admin_maps():
    """Interactive geological map of Serbia."""
    return maps_layer_views.render_admin_maps()


@app.route('/admin/geological-timeline')
@module_access_required('maps_karte')
def admin_geological_timeline():
    """Animated geological/tectonic timeline of the Balkans."""
    return maps_layer_views.render_admin_geological_timeline()


@app.route('/api/map/balkans-terrain')
@login_required
def api_balkans_terrain():
    """Full Serbia DEM at reduced resolution for geological timeline 3D view."""
    return maps_terrain_views.api_balkans_terrain(
        dem_dir=_DEM_DIR,
    )


@app.route('/api/map/tile-index')
@login_required
def api_map_tile_index():
    """Return JSON tile index (zoom levels + bounds)."""
    return maps_terrain_views.api_map_tile_index(
        build_tile_index=_build_tile_index,
    )


@app.route('/api/map/tile/<filename>')
@login_required
def api_map_tile(filename):
    """Serve individual tile PNG (extract from KMZ on first request, cache)."""
    return maps_terrain_views.api_map_tile(
        filename=filename,
        extract_tile_to_cache=_extract_tile_to_cache,
        tile_cache_dir=_TILE_CACHE_DIR,
    )

@app.route('/api/map/3d-terrain')
@login_required
def api_map_3d_terrain():
    """Return elevation grid + geological texture for 3D terrain rendering."""
    return maps_terrain_views.api_map_3d_terrain(
        dem_dir=_DEM_DIR,
        build_tile_index=_build_tile_index,
        extract_tile_to_cache=_extract_tile_to_cache,
    )


# ==================== GEO FIELD DATA ROUTES ====================

@app.route('/api/map/field-data', methods=['POST'])
@login_required
def api_create_field_data():
    """Create a new geological field observation."""
    return maps_field_data_views.api_create_field_data()


@app.route('/api/map/field-data', methods=['GET'])
@login_required
def api_list_field_data():
    """List all geological field observations, with optional bounding box filter."""
    return maps_field_data_views.api_list_field_data()


@app.route('/api/map/field-data/<int:item_id>', methods=['GET'])
@login_required
def api_get_field_data(item_id):
    """Get a single field observation with images."""
    return maps_field_data_views.api_get_field_data(
        item_id,
        image_storage_factory=get_image_storage,
    )


@app.route('/api/map/field-data/<int:item_id>', methods=['PUT'])
@login_required
def api_update_field_data(item_id):
    """Update a field observation (owner or admin only)."""
    return maps_field_data_views.api_update_field_data(item_id)


@app.route('/api/map/field-data/<int:item_id>', methods=['DELETE'])
@login_required
def api_delete_field_data(item_id):
    """Delete a field observation (owner or admin only)."""
    return maps_field_data_views.api_delete_field_data(
        item_id,
        image_storage_factory=get_image_storage,
    )


# ==================== ORE DEPOSITS LAYER ====================

@app.route('/api/map/ore-deposits')
@login_required
def api_ore_deposits():
    """Serve ore deposit data from JSON for the map layer."""
    return maps_layer_views.api_ore_deposits(os.path.dirname(__file__))


# ==================== STRATIGRAPHY LOCALITIES LAYER ====================

@app.route('/api/map/stratigraphy')
@login_required
def api_stratigraphy_localities():
    """Serve stratigraphy locality data from JSON for the map layer."""
    return maps_layer_views.api_stratigraphy_localities(os.path.dirname(__file__))


# ==================== PALEONTOLOGICAL LOCALITIES LAYER ====================

@app.route('/api/map/paleontology')
@login_required
def api_paleo_localities():
    """Serve paleontological locality data from JSON for the map layer."""
    return maps_layer_views.api_paleo_localities(os.path.dirname(__file__))


# ==================== MINING OPERATIONS LAYER ====================

@app.route('/api/map/mining-operations')
@login_required
def api_mining_operations():
    """Serve mining operations data from JSON for the map layer."""
    return maps_layer_views.api_mining_operations(os.path.dirname(__file__))


# ==================== EXPLORATION LICENSES LAYER ====================

@app.route('/api/map/exploration-licenses')
@login_required
def api_exploration_licenses():
    """Serve exploration license data from JSON for the map layer."""
    return maps_layer_views.api_exploration_licenses(os.path.dirname(__file__))


# ==================== GEOLOGICAL MAP SHEETS LAYER ====================

@app.route('/api/map/geological-sheets')
@login_required
def api_geological_sheets():
    """Serve geological map sheet metadata (bounds, files) for the map layer."""
    return maps_layer_views.api_geological_sheets(os.path.dirname(__file__))


@app.route('/api/map/geological-sheet-image/<folder_name>/<image_type>')
@login_required
def api_geological_sheet_image(folder_name, image_type):
    """Serve individual JPG images from OGK map sheet folders."""
    return maps_layer_views.api_geological_sheet_image(
        folder_name,
        image_type,
        os.path.dirname(__file__),
    )


@app.route('/api/map/geological-sheet-tumac/<folder_name>')
@login_required
def api_geological_sheet_tumac(folder_name):
    """Serve tumac PDF/DOC file for a geological map sheet."""
    return maps_layer_views.api_geological_sheet_tumac(
        folder_name,
        os.path.dirname(__file__),
    )


# ==================== GEOLOGICAL ZONE MAPS ====================

@app.route('/api/map/geo-zones/<folder_name>/zone-map')
@login_required
def api_geo_zone_map(folder_name):
    """Serve pre-computed zone group map PNG for a geological sheet."""
    return maps_geo_zone_views.api_geo_zone_map(
        folder_name,
        app_root=os.path.dirname(__file__),
    )


@app.route('/api/map/geo-zones/<folder_name>/metadata')
@login_required
def api_geo_zone_metadata(folder_name):
    """Serve zone groups metadata JSON for a geological sheet."""
    return maps_geo_zone_views.api_geo_zone_metadata(
        folder_name,
        app_root=os.path.dirname(__file__),
    )


@app.route('/api/map/geo-zones/<folder_name>/legend')
@login_required
def api_geo_zone_legend(folder_name):
    """Serve enhanced legend JSON for a geological sheet."""
    return maps_geo_zone_views.api_geo_zone_legend(
        folder_name,
        app_root=os.path.dirname(__file__),
    )


@app.route('/api/map/geo-zones/process', methods=['POST'])
@admin_required
def api_geo_zone_process():
    """Admin: trigger zone map processing for a sheet or all sheets."""
    return maps_geo_zone_views.api_geo_zone_process(
        app_root=os.path.dirname(__file__),
    )


@app.route('/api/map/geo-zones/<folder_name>/legend', methods=['POST'])
@admin_required
def api_geo_zone_legend_update(folder_name):
    """Admin: update enhanced legend with unit code assignments."""
    return maps_geo_zone_views.api_geo_zone_legend_update(
        folder_name,
        app_root=os.path.dirname(__file__),
    )


# --- Manual map color calibration ---

@app.route('/api/map/geo-zones/<folder_name>/calibration')
@login_required
def api_geo_manual_calibration_get(folder_name):
    """Load manual color calibration for a geological sheet."""
    return maps_geo_zone_views.api_geo_manual_calibration_get(
        folder_name,
        app_root=os.path.dirname(__file__),
    )


@app.route('/api/map/geo-zones/<folder_name>/calibration', methods=['POST'])
@admin_required
def api_geo_manual_calibration_save(folder_name):
    """Save manual color calibration for a geological sheet."""
    return maps_geo_zone_views.api_geo_manual_calibration_save(
        folder_name,
        app_root=os.path.dirname(__file__),
    )


@app.route('/api/map/geo-zones/<folder_name>/calibration/entry', methods=['PATCH'])
@admin_required
def api_geo_manual_calibration_patch_entry(folder_name):
    """Update or add a single calibration entry by color match."""
    return maps_geo_zone_views.api_geo_manual_calibration_patch_entry(
        folder_name,
        app_root=os.path.dirname(__file__),
    )


@app.route('/api/map/geo-zones/<folder_name>/calibration', methods=['DELETE'])
@admin_required
def api_geo_manual_calibration_delete(folder_name):
    """Delete manual calibration for a geological sheet (reset)."""
    return maps_geo_zone_views.api_geo_manual_calibration_delete(
        folder_name,
        app_root=os.path.dirname(__file__),
    )


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


@app.route('/api/map/elevation')
@login_required
def api_map_elevation():
    """Return terrain elevation for a single lat/lon point."""
    return maps_profile_views.api_map_elevation(
        sample_elevation_at_point=_sample_elevation_at_point,
    )


@app.route('/api/map/cross-profile')
@login_required
def api_map_cross_profile():
    """Generate a cross-section profile between two points with elevation and geology."""
    return maps_profile_views.api_map_cross_profile(
        app_root=os.path.dirname(__file__),
        haversine=_haversine_py,
        batch_sample_elevations=_batch_sample_elevations,
        interpolate_subsurface=_interpolate_subsurface,
    )


# ==================== PHASE 2: DIGITIZED PROFILES CRUD ====================


@app.route('/api/map/digitized-profiles')
@login_required
def api_digitized_profiles_list():
    """List all digitized cross-section profiles."""
    return maps_profile_views.api_digitized_profiles_list(
        profiles_path=_DIGITIZED_PROFILES_PATH,
    )


@app.route('/api/map/digitized-profiles/<profile_id>')
@login_required
def api_digitized_profile_get(profile_id):
    """Get a single digitized profile with full layer data."""
    return maps_profile_views.api_digitized_profile_get(
        profile_id,
        profiles_path=_DIGITIZED_PROFILES_PATH,
    )


@app.route('/api/map/digitized-profiles', methods=['POST'])
@login_required
def api_digitized_profile_create():
    """Create a new digitized profile."""
    return maps_profile_views.api_digitized_profile_create(
        profiles_path=_DIGITIZED_PROFILES_PATH,
    )


@app.route('/api/map/digitized-profiles/<profile_id>', methods=['PUT'])
@login_required
def api_digitized_profile_update(profile_id):
    """Update an existing digitized profile."""
    return maps_profile_views.api_digitized_profile_update(
        profile_id,
        profiles_path=_DIGITIZED_PROFILES_PATH,
    )


@app.route('/api/map/digitized-profiles/<profile_id>', methods=['DELETE'])
@login_required
def api_digitized_profile_delete(profile_id):
    """Delete a digitized profile."""
    return maps_profile_views.api_digitized_profile_delete(
        profile_id,
        profiles_path=_DIGITIZED_PROFILES_PATH,
    )


# ==================== PHASE 3: SUBSURFACE INTERPOLATION ====================


# ==================== BIODIVERSITY MAP ====================

@app.route('/admin/biodiversity-map')
@module_access_required('biodiversity_map')
def admin_biodiversity_map():
    """Interactive biodiversity map of Serbia — bird ringing localities."""
    return maps_biodiversity_views.render_admin_biodiversity_map()

@app.route('/api/map/bird-ringing-localities')
@login_required
def api_bird_ringing_localities():
    """Serve bird ringing locality data for the biodiversity map layer.

    Returns both GPS-located records and geocoded records (location name
    resolved via locality_geocache).  Geocoded entries carry ``geocoded: true``
    so the frontend can render them with a distinct style.
    """
    return maps_biodiversity_views.api_bird_ringing_localities(
        app_root=os.path.dirname(__file__),
        bird_ringing_database=bird_ringing_database,
    )


@app.route('/api/map/bird-ringing-filters')
@login_required
def api_bird_ringing_filters():
    """Return available filter values for the biodiversity map."""
    return maps_biodiversity_views.api_bird_ringing_filters(
        bird_ringing_database=bird_ringing_database,
    )


# --- Collection localities for biodiversity map ---


@app.route('/api/map/collection-localities')
@login_required
def api_collection_localities():
    """Serve collection specimen localities for the biodiversity map."""
    return maps_biodiversity_views.api_collection_localities(
        app_root=os.path.dirname(__file__),
        botany_collection_database=BOTANY_COLLECTION_DATABASE,
        ornithology_collection_database=ORNITHOLOGY_COLLECTION_DATABASE,
        ichthyology_collection_database=ICHTHYOLOGY_COLLECTION_DATABASE,
        herpetology_collection_database=HERPETOLOGY_COLLECTION_DATABASE,
        entomology_collection_database=ENTOMOLOGY_COLLECTION_DATABASE,
        mycology_collection_database=MYCOLOGY_COLLECTION_DATABASE,
    )


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
    application = create_app(start_background_services=True)

    # Run the application
    app.run(
        host=args.host,
        port=args.port,
        debug=args.debug
    )
