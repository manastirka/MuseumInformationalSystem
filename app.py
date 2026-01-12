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
from flask import Flask, render_template, request, redirect, url_for, session, flash, current_app, send_file, send_from_directory, make_response, jsonify
from datetime import datetime
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from werkzeug.serving import run_simple
from typing import Optional, Dict

# Load environment variables from .env file FIRST
from dotenv import load_dotenv
load_dotenv()

# Use PostgreSQL version if DATABASE_URL is set, otherwise fall back to SQLite
if os.environ.get('DATABASE_URL'):
    from mineral_database_pg import get_mineral_database
    print("✓ Using PostgreSQL for mineral database")
    # Import Phase 3A PostgreSQL databases
    import phase3a_databases
    print("✓ Using PostgreSQL for Phase 3A databases (Library, Exhibitions, Heritage, Meteorites)")
else:
    from mineral_database import get_mineral_database
    print("✓ Using SQLite for mineral database")

from image_storage_engine import get_image_storage
import bird_ringing_database
import importlib.util
from museum_llm_assistant import get_museum_assistant
from timesheet_repository import TimesheetRepository

# Security imports
from config import get_config
from security_utils import (
    PasswordValidator,
    PasswordHasher,
    login_tracker,
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

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(name)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/museum_info_system.log'),
        logging.StreamHandler()
    ]
)

# Create logs directory
os.makedirs('logs', exist_ok=True)

# Add paths for integrated apps
current_dir = os.path.dirname(os.path.abspath(__file__))
localsql_path = os.path.join(current_dir, 'localSQLtesting')
prirodnjacki_path = os.path.join(current_dir, 'PrirodnjackiMuzej')

sys.path.insert(0, localsql_path)
sys.path.insert(0, prirodnjacki_path)

# Authentication system integration
auth_available = False
auth_system = None
db_manager = None

print("🔍 Checking authentication system availability...")

# Try PostgreSQL authentication first
try:
    from postgres_auth import get_postgres_auth
    postgres_auth = get_postgres_auth()
    if postgres_auth.available:
        auth_system = postgres_auth
        auth_available = True
        print("✓ Using PostgreSQL authentication")
    else:
        print("⚠️  PostgreSQL authentication not available, using fallback")
except Exception as e:
    print(f"⚠️  PostgreSQL auth initialization failed: {e}")
    print("   Using fallback authentication")

# Load configuration
config_name = os.environ.get('FLASK_ENV', 'development')
app_config = get_config(config_name)

# Create Flask app
app = Flask(__name__)
app.config.from_object(app_config)

# Initialize security extensions
# IMPORTANT: Session must be initialized BEFORE CSRF
Session(app)
csrf = CSRFProtect(app)

# Initialize rate limiter
limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"],
    storage_uri=app.config.get('RATELIMIT_STORAGE_URL', 'memory://')
)

# Initialize password utilities (use app_config object, not app.config dict)
password_validator = PasswordValidator(app_config)
password_hasher = PasswordHasher()

logger = logging.getLogger(__name__)

# Optional timesheet repository (PostgreSQL only)
timesheet_repository = TimesheetRepository(os.environ.get('DATABASE_URL')) if os.environ.get('DATABASE_URL') else None

# Display auth status
if app.config.get('ENABLE_FALLBACK_AUTH', True):
    logger.warning("⚠️ Using fallback authentication (MySQL not configured)")
    logger.warning("   Login with configured admin credentials")
else:
    logger.info("✓ Production mode - fallback authentication disabled")

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
    }
}

# Module access persistence
MODULE_ACCESS_FILE = 'data/module_access.json'

def load_module_access():
    """Load module access settings from JSON file."""
    global MODULE_ACCESS
    try:
        if os.path.exists(MODULE_ACCESS_FILE):
            with open(MODULE_ACCESS_FILE, 'r', encoding='utf-8') as f:
                saved_access = json.load(f)
                # Merge saved authorized_users and restricted_users with MODULE_ACCESS
                for module_key, module_data in saved_access.items():
                    if module_key in MODULE_ACCESS:
                        if 'authorized_users' in module_data:
                            MODULE_ACCESS[module_key]['authorized_users'] = module_data['authorized_users']
                        if 'restricted_users' in module_data:
                            MODULE_ACCESS[module_key]['restricted_users'] = module_data['restricted_users']
                logger.info(f"Loaded module access settings from {MODULE_ACCESS_FILE}")
    except Exception as e:
        logger.error(f"Error loading module access: {e}")

def save_module_access():
    """Save module access settings to JSON file."""
    try:
        os.makedirs(os.path.dirname(MODULE_ACCESS_FILE), exist_ok=True)
        # Save both authorized_users and restricted_users for each module
        access_data = {}
        for module_key, module_info in MODULE_ACCESS.items():
            module_data = {}
            if 'authorized_users' in module_info and module_info['authorized_users']:
                module_data['authorized_users'] = module_info['authorized_users']
            if 'restricted_users' in module_info and module_info['restricted_users']:
                module_data['restricted_users'] = module_info['restricted_users']
            if module_data:
                access_data[module_key] = module_data
        with open(MODULE_ACCESS_FILE, 'w', encoding='utf-8') as f:
            json.dump(access_data, f, ensure_ascii=False, indent=2)
        logger.info(f"Saved module access settings to {MODULE_ACCESS_FILE}")
        return True
    except Exception as e:
        logger.error(f"Error saving module access: {e}")
        return False

# Load module access on startup
load_module_access()

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

DASHBOARD_PREFERENCES = _DEFAULT_DASHBOARD_PREFS.copy()

def load_dashboard_preferences():
    """Load dashboard preferences from JSON file."""
    global DASHBOARD_PREFERENCES
    try:
        if os.path.exists(DASHBOARD_PREFS_FILE):
            with open(DASHBOARD_PREFS_FILE, 'r', encoding='utf-8') as f:
                DASHBOARD_PREFERENCES = json.load(f)
                logger.info(f"Loaded dashboard preferences from {DASHBOARD_PREFS_FILE}")
                return DASHBOARD_PREFERENCES
    except Exception as e:
        logger.error(f"Error loading dashboard preferences: {e}")

    DASHBOARD_PREFERENCES = _DEFAULT_DASHBOARD_PREFS.copy()
    return DASHBOARD_PREFERENCES

def save_dashboard_preferences():
    """Save dashboard preferences to JSON file."""
    try:
        os.makedirs(os.path.dirname(DASHBOARD_PREFS_FILE), exist_ok=True)
        with open(DASHBOARD_PREFS_FILE, 'w', encoding='utf-8') as f:
            json.dump(DASHBOARD_PREFERENCES, f, ensure_ascii=False, indent=2)
        logger.info(f"Saved dashboard preferences to {DASHBOARD_PREFS_FILE}")
        return True
    except Exception as e:
        logger.error(f"Error saving dashboard preferences: {e}")
        return False

# Load dashboard preferences on startup
load_dashboard_preferences()

def user_has_module_access(user_email, user_role, module_key):
    """Check if user has access to specific module."""
    # Reload module access from file to get latest changes (for multi-worker support)
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

def get_user_modules(user_email, user_role):
    """Get list of modules user has access to, filtered by dashboard preferences."""
    # Reload module access and dashboard preferences from file to get latest changes
    load_module_access()
    load_dashboard_preferences()

    accessible_modules = []

    # List of admin users who should only see Museum Databases by default
    admin_users = ['admin', 'slavko.spasic@nhmbeo.rs', 'biljana.mitrovic@nhmbeo.rs', 'verica.stojanovic@nhmbeo.rs']

    # Get user's dashboard preferences
    enabled_widgets = DASHBOARD_PREFERENCES.get(user_email, {}).get('enabled_widgets', None)

    # If no preferences set, determine default based on user type
    if enabled_widgets is None:
        if user_email in admin_users or user_role == 'admin':
            # Admin users: show only Museum Databases by default
            enabled_widgets = ['museum_databases']
        else:
            # Regular users: show all accessible modules
            enabled_widgets = list(MODULE_ACCESS.keys())

    for module_key, module_info in MODULE_ACCESS.items():
        # Check if user has access AND if widget is enabled in preferences
        if user_has_module_access(user_email, user_role, module_key) and module_key in enabled_widgets:
            accessible_modules.append({
                'key': module_key,
                'name': module_info['name'],
                'description': module_info['description'],
                'icon': module_info['icon']
            })

    return accessible_modules

# Fallback employee database for when MySQL is not available
def get_fallback_employees():
    """
    Fallback employee data for development/testing ONLY.
    NEVER use in production - set ENABLE_FALLBACK_AUTH=False in .env

    Returns minimal admin account if fallback auth is enabled in config.
    """
    if not app.config.get('ENABLE_FALLBACK_AUTH', False):
        logger.info("Fallback authentication is disabled (production mode)")
        return {}

    logger.warning("⚠️ USING FALLBACK AUTHENTICATION - NOT SECURE FOR PRODUCTION")
    logger.warning("    Set ENABLE_FALLBACK_AUTH=False in .env for production")

    # Return minimal admin account only
    # Password will be hashed and validated through proper authentication flow
    return {
        app.config.get('ADMIN_EMAIL', 'admin@nhmbeo.rs'): {
            'user_id': 1,
            'email': app.config.get('ADMIN_EMAIL', 'admin@nhmbeo.rs'),
            'full_name': 'System Administrator',
            'department': 'Administration',
            'position': 'System Administrator',
            'role': 'admin',
            # Password stored in config, not hardcoded
            'requires_password_check': True,
            'description': 'Администратор информационог система музеја.'
        }
    }

# Initialize fallback employees
MUSEUM_EMPLOYEES = get_fallback_employees()

# Library Database - will be loaded from JSON}

# Library Database - loaded from PostgreSQL (Phase 3A)
LIBRARY_DATABASE = None
EMPLOYEE_DIRECTORY = None

def load_library_database():
    """Load library database from PostgreSQL."""
    if os.environ.get('DATABASE_URL'):
        # Use PostgreSQL (Phase 3A)
        return phase3a_databases.get_library_database()
    else:
        # Fallback to JSON file
        library_path = os.path.join('data', 'library_database.json')
        try:
            with open(library_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                logging.info(f"Loaded library database: {data['statistics']['total_books']} books")
                return data
        except FileNotFoundError:
            logging.warning(f"Library database file not found at {library_path}, using default data")
            return {
                'books': [],
                'categories': ['Геологија', 'Минералогија', 'Палеонтологија', 'Ботаника', 'Зоологија', 'Ентомологија', 'Ихтиологија', 'Општа научна литература', 'Монографска публикација'],
                'statistics': {
                    'total_books': 0,
                    'available_books': 0,
                    'borrowed_books': 0,
                    'total_categories': 0
                }
            }
        except json.JSONDecodeError as exc:
            logging.error(f"Error decoding library database JSON: {exc}")
            return {
                'books': [],
                'categories': ['Геологија', 'Минералогија', 'Палеонтологија', 'Ботаника', 'Зоологија', 'Ентомологија', 'Ихтиологија', 'Општа научна литература', 'Монографска публикација'],
                'statistics': {
                    'total_books': 0,
                    'available_books': 0,
                    'borrowed_books': 0,
                    'total_categories': 0
                }
            }

def save_library_database():
    """Save library database to JSON file."""
    global LIBRARY_DATABASE
    if LIBRARY_DATABASE is None:
        return

    library_path = os.path.join('data', 'library_database.json')
    try:
        os.makedirs(os.path.dirname(library_path), exist_ok=True)

        # Update statistics before saving
        LIBRARY_DATABASE['statistics'] = {
            'total_books': len(LIBRARY_DATABASE['books']),
            'available_books': len([b for b in LIBRARY_DATABASE['books'] if b.get('status') == 'доступна']),
            'borrowed_books': len([b for b in LIBRARY_DATABASE['books'] if b.get('status') == 'позајмљена']),
            'total_categories': len(LIBRARY_DATABASE.get('categories', []))
        }

        with open(library_path, 'w', encoding='utf-8') as f:
            json.dump(LIBRARY_DATABASE, f, ensure_ascii=False, indent=2)

        logging.info(f"Saved library database: {LIBRARY_DATABASE['statistics']['total_books']} books")
    except Exception as exc:
        logging.error(f"Error saving library database: {exc}")

def get_library_database():
    """Return the cached library database, loading it if needed."""
    global LIBRARY_DATABASE
    if LIBRARY_DATABASE is None:
        LIBRARY_DATABASE = load_library_database()
    return LIBRARY_DATABASE

def load_employee_directory():
    """Load employee directory from PostgreSQL or JSON fallback."""
    if os.environ.get('DATABASE_URL'):
        # Use PostgreSQL (Phase 3A)
        return phase3a_databases.load_employee_directory()
    else:
        # Fallback to JSON file
        directory_path = os.path.join('data', 'employee_directory.json')
        try:
            with open(directory_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                logger.info("Loaded employee directory with %d profiles.", len(data))
                return data
        except FileNotFoundError:
            logger.warning("Employee directory not found at %s", directory_path)
            return []
        except json.JSONDecodeError as exc:
            logger.error("Error decoding employee directory JSON: %s", exc)
            return []

def get_employee_directory():
    """Return cached employee directory."""
    global EMPLOYEE_DIRECTORY
    if EMPLOYEE_DIRECTORY is None:
        EMPLOYEE_DIRECTORY = load_employee_directory()
    return EMPLOYEE_DIRECTORY

def load_exhibitions_data():
    """Load exhibitions from PostgreSQL or JSON fallback."""
    if os.environ.get('DATABASE_URL'):
        # Use PostgreSQL (Phase 3A)
        return phase3a_databases.load_exhibitions_data()
    else:
        # Fallback to JSON file
        exhibitions_path = os.path.join('data', 'exhibitions.json')
        try:
            with open(exhibitions_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if isinstance(data, list):
                    return data
                logging.warning("Expected list in exhibitions.json, got %s", type(data))
        except FileNotFoundError:
            logging.warning("Exhibitions data file not found at %s", exhibitions_path)
        except json.JSONDecodeError as exc:
            logging.error("Unable to parse exhibitions data: %s", exc)
        return []

def load_news_data():
    """Load news articles from PostgreSQL or JSON fallback."""
    if os.environ.get('DATABASE_URL'):
        # Use PostgreSQL (Phase 3B)
        return phase3a_databases.load_news_data()
    else:
        # Fallback to JSON file
        news_path = os.path.join('data', 'news.json')
        try:
            with open(news_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if isinstance(data, list):
                    return data
                logging.warning("Expected list in news.json, got %s", type(data))
        except FileNotFoundError:
            logging.warning("News data file not found at %s", news_path)
        except json.JSONDecodeError as exc:
            logging.error("Unable to parse news data: %s", exc)
        return []


EXHIBITS_DATABASE = {
    'artifacts': [
        {
            'id': 1,
            'name': 'Скелет степског мамута',
            'category': 'Палеонтологија',
            'status': 'изложен',
            'condition': 'Одлично',
            'location': 'Галерија Калемегдан – Сала 1',
            'period': 'Плеистоцен (100.000 година)',
            'dimensions': '5.2 m x 3.7 m',
            'weight': '1.8 t',
            'origin': 'Обедска бара, Србија',
            'acquisition_date': '2013-11-08',
            'description': 'Комплетни остатак мамута приморакса пронађен током истраживања у Обедској бари. Кључни експонат изложбе "Сурлаши – дивови прошлости".'
        },
        {
            'id': 2,
            'name': 'Метеорит Сокобања',
            'category': 'Минералогија',
            'status': 'изложен',
            'condition': 'Добро',
            'location': 'Галерија Калемегдан – Витрина 4',
            'period': '4.5 милијарди година',
            'dimensions': '24 cm x 18 cm x 12 cm',
            'weight': '41 kg',
            'origin': 'Сокобања, Србија',
            'acquisition_date': '1877-05-14',
            'description': 'Највећи српски метеорит, хондрит са високим уделом никла. Представља кључни пример свемирског материјала у збирци.'
        },
        {
            'id': 3,
            'name': 'Колекција пепела са Везува',
            'category': 'Геологија',
            'status': 'у депоу',
            'condition': 'Одлично',
            'location': 'Депо А – Полица G3',
            'period': '79. година нове ере',
            'dimensions': '12 узорака у архивским кутијама',
            'weight': '6.5 kg',
            'origin': 'Везув, Италија',
            'acquisition_date': '1984-06-03',
            'description': 'Серија узорака тефре и пепела из различитих фаза ерупције Везува. Користи се у едукативним програмима и научним анализама.'
        },
        {
            'id': 4,
            'name': 'Хербаријум "Ендемске орхидеје Балкана"',
            'category': 'Ботаника',
            'status': 'изложен',
            'condition': 'Одлично',
            'location': 'Галерија Калемегдан – Витрина 7',
            'period': '19–20. век',
            'dimensions': '48 табака у заштитним рамовима',
            'weight': '8.2 kg',
            'origin': 'Планина Тара, Србија',
            'acquisition_date': '1956-04-19',
            'description': 'Ручно припремљен хербаријум са ретким и заштићеним врстама орхидеја. Рестаурирала кустос Снежана Марковић 2022. године.'
        },
        {
            'id': 5,
            'name': 'Скуп одоната "Балкан ОдоБасе"',
            'category': 'Зоологија',
            'status': 'у конзервацији',
            'condition': 'Захтева конзервацију',
            'location': 'Конзерваторска лабораторија',
            'period': '20. век',
            'dimensions': '1.200 примерака у ентомолошким кутијама',
            'weight': '15 kg',
            'origin': 'Балканско полуострво',
            'acquisition_date': '1998-09-27',
            'description': 'Референтна колекција водених вилина коју је сакупио др Милош Јовић. У току је превентивна конзервација и дигитализација.'
        }
    ],
    'categories': ['Палеонтологија', 'Минералогија', 'Геологија', 'Ботаника', 'Зоологија'],
    'statuses': ['изложен', 'у депоу', 'у конзервацији'],
    'conditions': ['Одлично', 'Добро', 'Захтева конзервацију']
}

_exhibitions_loaded = load_exhibitions_data()
EXHIBITIONS_DATABASE = {
    'exhibitions': _exhibitions_loaded,
    'types': sorted({entry.get('type', 'Изложба') for entry in _exhibitions_loaded}) or ['Изложба']
}

_news_loaded = load_news_data()
NEWS_DATABASE = {
    'articles': _news_loaded,
    'types': sorted({entry.get('type', 'Изложба') for entry in _news_loaded}) or ['Изложба']
}


def get_exhibit_statistics():
    """Aggregate exhibit metrics from the artifacts dataset."""
    artifacts = EXHIBITS_DATABASE['artifacts']
    displayed = len([a for a in artifacts if a['status'] == 'изложен'])
    storage = len([a for a in artifacts if a['status'] == 'у депоу'])
    excellent = len([a for a in artifacts if a['condition'] == 'Одлично'])
    distinct_categories = len({a['category'] for a in artifacts})

    return {
        'total_artifacts': len(artifacts),
        'displayed_artifacts': displayed,
        'storage_artifacts': storage,
        'excellent_condition': excellent,
        'total_categories': distinct_categories
    }


def get_exhibition_statistics():
    """Aggregate exhibition metrics for dashboard and detail views."""
    exhibitions = [e for e in EXHIBITIONS_DATABASE['exhibitions']
                   if e.get('category', 'gallery') != 'touring']
    active = len([e for e in exhibitions if e['status'] == 'Активна'])
    completed = len([e for e in exhibitions if e['status'] in ('Завршена', 'Историјска')])
    planned = len([e for e in exhibitions if e['status'] == 'Планирана'])
    total_visitors = sum(e['visitor_count'] for e in exhibitions)
    current_year = datetime.now().year
    annual = len([e for e in exhibitions if e['start_date'].startswith(str(current_year))])

    return {
        'total_exhibitions': len(exhibitions),
        'active_exhibitions': active,
        'completed_exhibitions': completed,
        'planned_exhibitions': planned,
        'total_visitors': total_visitors,
        'annual_exhibitions': annual
    }

# Curator Collection Databases - Loading from PostgreSQL or fallback to sample data

# Load collections from PostgreSQL if DATABASE_URL is set
def load_collection_database(collection_type: str, fallback_data: dict):
    """Load collection from PostgreSQL or use fallback data."""
    if os.environ.get('DATABASE_URL'):
        try:
            if collection_type == 'botany':
                return phase3a_databases.get_botany_collection()
            elif collection_type == 'ichthyology':
                return phase3a_databases.get_ichthyology_collection()
            elif collection_type == 'entomology':
                return phase3a_databases.get_entomology_collection()
            elif collection_type == 'mycology':
                return phase3a_databases.get_mycology_collection()
            elif collection_type == 'herpetology':
                return phase3a_databases.get_herpetology_collection()
            elif collection_type == 'ornithology':
                return phase3a_databases.get_ornithology_collection()
            elif collection_type == 'paleozoology':
                return phase3a_databases.get_paleozoology_collection()
            elif collection_type == 'paleobotany':
                return phase3a_databases.get_paleobotany_collection()
            elif collection_type == 'petrology':
                return phase3a_databases.get_petrology_collection()
        except Exception as e:
            logging.warning(f"Failed to load {collection_type} from PostgreSQL: {e}")
    return fallback_data

# Botany Collection Database (Fallback data - used only if PostgreSQL unavailable)
_BOTANY_FALLBACK = {
    'specimens': [
        {
            'catalog_number': 'BOT-2024-001',
            'scientific_name': 'Pančić Omorika (Picea omorika)',
            'common_name_sr': 'Панчићева оморика',
            'family': 'Pinaceae',
            'location_found': 'Тара, Србија',
            'altitude': '800-1600m',
            'date_collected': '2023-06-15',
            'collector': 'Др М. Никетић',
            'herbarium_number': 'BEOU-40001',
            'condition': 'Одлично',
            'endemic_status': 'Ендемична врста Србије',
            'conservation_status': 'Угрожена (EN)',
            'description': 'Ендемична четинарска врста Србије. Реликтна врста из терцијара.',
            'curator': 'mniketic@nhmbeo.rs'
        },
        {
            'catalog_number': 'BOT-2024-002',
            'scientific_name': 'Ramonda serbica',
            'common_name_sr': 'Српска рамонда (Наталијина рамонда)',
            'family': 'Gesneriaceae',
            'location_found': 'Сува планина, Србија',
            'altitude': '400-1800m',
            'date_collected': '2023-05-10',
            'collector': 'Др А. Савић',
            'herbarium_number': 'BEOU-40002',
            'condition': 'Одлично',
            'endemic_status': 'Балкански ендем',
            'conservation_status': 'Ретка',
            'description': 'Реликтна биљка способна за анабиозу. Национални симбол Србије.',
            'curator': 'aleksandra.savic@nhmbeo.rs'
        },
        {
            'catalog_number': 'BOT-2024-003',
            'scientific_name': 'Lilium bosniacum',
            'common_name_sr': 'Босански љиљан',
            'family': 'Liliaceae',
            'location_found': 'Копаоник, Србија',
            'altitude': '1200-2000m',
            'date_collected': '2022-07-20',
            'collector': 'В. Стојановић',
            'herbarium_number': 'BEOU-38547',
            'condition': 'Добро',
            'endemic_status': 'Балкански ендем',
            'conservation_status': 'Заштићена',
            'description': 'Ретка врста планинског љиљана са Балкана.',
            'curator': 'verica.stojanovic@nhmbeo.rs'
        },
        {
            'catalog_number': 'BOT-2024-004',
            'scientific_name': 'Acer heldreichii',
            'common_name_sr': 'Хелдрајхов јавор',
            'family': 'Sapindaceae',
            'location_found': 'Проклетије, Србија',
            'altitude': '1000-1800m',
            'date_collected': '2023-09-12',
            'collector': 'Др М. Несторовић',
            'herbarium_number': 'BEOU-39221',
            'condition': 'Одлично',
            'endemic_status': 'Балкански ендем',
            'conservation_status': 'Ретка',
            'description': 'Врста јавора карактеристична за Балканско полуострво.',
            'curator': 'marko.nestorovic@nhmbeo.rs'
        },
        {
            'catalog_number': 'BOT-2024-005',
            'scientific_name': 'Paeonia tenuifolia',
            'common_name_sr': 'Божур',
            'family': 'Paeoniaceae',
            'location_found': 'Фрушка гора, Србија',
            'altitude': '200-400m',
            'date_collected': '2023-04-28',
            'collector': 'Др М. Никетић',
            'herbarium_number': 'BEOU-39845',
            'condition': 'Одлично',
            'endemic_status': 'Аутохтона',
            'conservation_status': 'Строго заштићена',
            'description': 'Ретка степска биљка са црвеним цветовима.',
            'curator': 'mniketic@nhmbeo.rs'
        }
    ],
    'statistics': {
        'total_specimens': 5,
        'endemic_species': 4,
        'threatened_species': 3,
        'herbarium_size': '>40,000'
    }
}

# Ichthyology Collection Database (Fallback)
_ICHTHYOLOGY_FALLBACK = {
    'specimens': [
        {
            'catalog_number': 'ICH-2024-001',
            'scientific_name': 'Acipenser ruthenus',
            'common_name_sr': 'Кечига',
            'family': 'Acipenseridae',
            'location_found': 'Дунав, Србија',
            'habitat': 'Слатководна',
            'date_collected': '2022-08-15',
            'length_cm': 85,
            'weight_kg': 4.5,
            'age_estimated': '12 година',
            'condition': 'Одличан препарат',
            'conservation_status': 'Критично угрожена (CR)',
            'description': 'Јесетра из породице Acipenseridae. Извор кавијара. Део изложбе "Kavijar".',
            'curator': 'dubravka.vucic@nhmbeo.rs'
        },
        {
            'catalog_number': 'ICH-2024-002',
            'scientific_name': 'Hucho hucho',
            'common_name_sr': 'Младица',
            'family': 'Salmonidae',
            'location_found': 'Лим, Србија',
            'habitat': 'Брзе планинске реке',
            'date_collected': '2023-05-22',
            'length_cm': 120,
            'weight_kg': 18,
            'age_estimated': '8 година',
            'condition': 'Добар препарат',
            'conservation_status': 'Угрожена (EN)',
            'description': 'Највећа врста пастрмке у Европи. Ендемична за дунавски слив.',
            'curator': 'dubravka.vucic@nhmbeo.rs'
        },
        {
            'catalog_number': 'ICH-2024-003',
            'scientific_name': 'Zingel balcanicus',
            'common_name_sr': 'Вретенар',
            'family': 'Percidae',
            'location_found': 'Вардар, Србија',
            'habitat': 'Брзотекуће воде',
            'date_collected': '2021-09-10',
            'length_cm': 18,
            'weight_kg': 0.15,
            'age_estimated': '3 године',
            'condition': 'Одличан препарат',
            'conservation_status': 'Угрожена (EN)',
            'description': 'Балкански ендем. Карактеристичне зебрасте пруге.',
            'curator': 'dubravka.vucic@nhmbeo.rs'
        }
    ],
    'statistics': {
        'total_specimens': 3,
        'endangered_species': 3,
        'endemic_species': 2
    }
}

# Entomology Collection Database (Fallback)
_ENTOMOLOGY_FALLBACK = {
    'specimens': [
        {
            'catalog_number': 'ENT-OD-001',
            'scientific_name': 'Calopteryx virgo',
            'common_name_sr': 'Девојачка виленица',
            'order': 'Odonata',
            'family': 'Calopterygidae',
            'location_found': 'Ђердап, Србија',
            'date_collected': '2023-06-18',
            'sex': 'мужјак',
            'wingspan_mm': 65,
            'condition': 'Одличан препарат',
            'part_of_collection': 'Balkan OdoBase',
            'description': 'Модра виленица са металним сјајем. Индикатор чистих вода.',
            'curator': 'milos.jovic@nhmbeo.rs'
        },
        {
            'catalog_number': 'ENT-LEP-001',
            'scientific_name': 'Parnassius apollo',
            'common_name_sr': 'Аполонов лептир',
            'order': 'Lepidoptera',
            'family': 'Papilionidae',
            'location_found': 'Стара планина, Србија',
            'date_collected': '2022-07-05',
            'sex': 'женка',
            'wingspan_mm': 75,
            'condition': 'Одличан препарат',
            'conservation_status': 'Строго заштићена',
            'description': 'Ретка планинска врста лептира. Заштићена на нивоу Европе.',
            'curator': 'aleksandar@nhmbeo.rs'
        },
        {
            'catalog_number': 'ENT-COL-001',
            'scientific_name': 'Rosalia alpina',
            'common_name_sr': 'Алпски стрижибуба',
            'order': 'Coleoptera',
            'family': 'Cerambycidae',
            'location_found': 'Шар планина, Србија',
            'date_collected': '2023-08-14',
            'sex': 'мужјак',
            'length_mm': 38,
            'condition': 'Одличан препарат',
            'conservation_status': 'Заштићена',
            'description': 'Велика плаво-црна буба дугорог. Живи на старим буквама.',
            'curator': 'milos.jovic@nhmbeo.rs'
        },
        {
            'catalog_number': 'ENT-HYM-001',
            'scientific_name': 'Bombus terrestris',
            'common_name_sr': 'Земни бумбар',
            'order': 'Hymenoptera',
            'family': 'Apidae',
            'location_found': 'Авала, Србија',
            'date_collected': '2023-05-20',
            'sex': 'радилица',
            'length_mm': 22,
            'condition': 'Добар препарат',
            'conservation_status': 'Није угрожена',
            'description': 'Најчешћа врста бумбара у Србији. Важан опрашивач.',
            'curator': 'aleksandar@nhmbeo.rs'
        }
    ],
    'statistics': {
        'total_specimens': 4,
        'odonata_collection': 1,
        'total_species_exhibited': '1,710+'
    }
}

# Mycology Collection Database (Fallback)
_MYCOLOGY_FALLBACK = {
    'specimens': [
        {
            'catalog_number': 'MYC-2024-001',
            'scientific_name': 'Tuber petrophilum',
            'common_name_sr': 'Српски тартуф',
            'family': 'Tuberaceae',
            'location_found': 'Источна Србија',
            'habitat': 'Кречњачко тло, храстове шуме',
            'date_collected': '2014-10-12',
            'diameter_cm': 4.5,
            'weight_g': 35,
            'condition': 'Конзервиран',
            'type_status': 'Холотип',
            'description': 'Нова врста тартуфа описана од др Б. Иванчевића. Објављена у Mycotaxon 2014.',
            'curator': 'boris@nhmbeo.rs'
        },
        {
            'catalog_number': 'MYC-2024-002',
            'scientific_name': 'Amanita muscaria',
            'common_name_sr': 'Мухомор',
            'family': 'Amanitaceae',
            'location_found': 'Златибор, Србија',
            'habitat': 'Четинарске шуме',
            'date_collected': '2023-09-18',
            'diameter_cm': 12,
            'condition': 'Добар препарат',
            'toxicity': 'Отровна',
            'description': 'Класичан црвени мухомор са белим тачкама. Симбионт четинара.',
            'curator': 'boris@nhmbeo.rs'
        },
        {
            'catalog_number': 'MYC-2024-003',
            'scientific_name': 'Boletus edulis',
            'common_name_sr': 'Вргањ',
            'family': 'Boletaceae',
            'location_found': 'Голија, Србија',
            'habitat': 'Мешовите шуме',
            'date_collected': '2023-10-05',
            'diameter_cm': 18,
            'weight_g': 450,
            'condition': 'Одличан препарат',
            'edibility': 'Јестива',
            'description': 'Јестива гљива високог квалитета. Симбионт храста и четинара.',
            'curator': 'boris@nhmbeo.rs'
        }
    ],
    'statistics': {
        'total_specimens': 3,
        'new_species_described': 1,
        'research_years': '30+'
    }
}

# Herpetology Collection Database (Fallback)
_HERPETOLOGY_FALLBACK = {
    'specimens': [
        {
            'catalog_number': 'HERP-AMP-001',
            'scientific_name': 'Salamandra salamandra',
            'common_name_sr': 'Обична дaламадeрица',
            'class': 'Amphibia',
            'order': 'Caudata',
            'family': 'Salamandridae',
            'location_found': 'Фрушка гора, Србија',
            'habitat': 'Влажне листопадне шуме',
            'date_collected': '2022-04-15',
            'length_cm': 18,
            'sex': 'женка',
            'condition': 'Одличан препарат',
            'conservation_status': 'Заштићена',
            'description': 'Црно-жута саламандерица. Индикатор здравих шумских екосистема.',
            'curator': 'ana.paunovic@nhmbeo.rs'
        },
        {
            'catalog_number': 'HERP-REP-001',
            'scientific_name': 'Vipera ammodytes',
            'common_name_sr': 'Поскок',
            'class': 'Reptilia',
            'order': 'Squamata',
            'family': 'Viperidae',
            'location_found': 'Суве планине, Србија',
            'habitat': 'Камењари, сунчани терени',
            'date_collected': '2021-06-22',
            'length_cm': 72,
            'sex': 'мужјак',
            'condition': 'Одличан препарат',
            'venomous': 'Да - отровна',
            'conservation_status': 'Заштићена',
            'description': 'Најотровнија европска змија. Карактеристични рог на њушци.',
            'curator': 'ana.paunovic@nhmbeo.rs'
        },
        {
            'catalog_number': 'HERP-AMP-002',
            'scientific_name': 'Bombina variegata',
            'common_name_sr': 'Жутотрба бумбарка',
            'class': 'Amphibia',
            'order': 'Anura',
            'family': 'Bombinatoridae',
            'location_found': 'Вршачке планине, Србија',
            'habitat': 'Планинске баре и потоци',
            'date_collected': '2023-05-10',
            'length_cm': 4.5,
            'sex': 'женка',
            'condition': 'Добар препарат',
            'conservation_status': 'Осетљива',
            'description': 'Мала жаба са жутим трбухом. Живи у чистим планинским водама.',
            'curator': 'ana.paunovic@nhmbeo.rs'
        }
    ],
    'statistics': {
        'total_specimens': 3,
        'amphibians': 2,
        'reptiles': 1,
        'field_research_years': '20+'
    }
}

# Ornithology Collection Database (Fallback)
_ORNITHOLOGY_FALLBACK = {
    'specimens': [
        {
            'catalog_number': 'ORN-2024-001',
            'scientific_name': 'Aquila chrysaetos',
            'common_name_sr': 'Крсташ (Сури орао)',
            'order': 'Accipitriformes',
            'family': 'Accipitridae',
            'location_found': 'Увац, Србија',
            'habitat': 'Планинске стене',
            'date_collected': '2020-11-08',
            'wingspan_cm': 220,
            'weight_kg': 4.8,
            'sex': 'женка',
            'ring_number': 'EURING-SRB-12458',
            'condition': 'Одличан препарат',
            'conservation_status': 'Строго заштићена',
            'description': 'Највећа грабљивица Србије. Симбол планинских предела.',
            'curator': 'vuk.popic@nhmbeo.rs'
        },
        {
            'catalog_number': 'ORN-2024-002',
            'scientific_name': 'Ciconia nigra',
            'common_name_sr': 'Црна рода',
            'order': 'Ciconiiformes',
            'family': 'Ciconiidae',
            'location_found': 'Обедска бара, Србија',
            'habitat': 'Мочваре и влажне шуме',
            'date_collected': '2021-07-14',
            'wingspan_cm': 185,
            'weight_kg': 3.2,
            'sex': 'мужјак',
            'ring_number': 'EURING-SRB-13201',
            'condition': 'Добар препарат',
            'conservation_status': 'Заштићена',
            'description': 'Ретка врста роде. Гнезди у старим шумама.',
            'curator': 'vuk.popic@nhmbeo.rs'
        }
    ],
    'statistics': {
        'total_specimens': 2,
        'ringed_birds': 2,
        'euring_program': 'Активан'
    }
}

# Paleozoology Collection Database (Fallback)
_PALEOZOOLOGY_FALLBACK = {
    'specimens': [
        {
            'catalog_number': 'PALEO-DINO-001',
            'scientific_name': 'Theropoda indet.',
            'common_name_sr': 'Зуб теропода',
            'taxon_group': 'Dinosauria',
            'geological_period': 'Горња креда',
            'age_million_years': 70,
            'location_found': 'Пирот, Србија',
            'date_discovered': '2019-08-12',
            'discoverers': 'Др З. Марковић, М. Миливојевић',
            'specimen_type': 'Зуб',
            'length_cm': 4.2,
            'condition': 'Добро очуван',
            'significance': 'Први фосил диносауруса у Србији',
            'description': 'Зуб месоједног диносауруса. Историјско откриће за српску палеонтологију.',
            'publication': 'Објављен у међународном часопису 2020',
            'curator': 'zoran.markovic@nhmbeo.rs'
        },
        {
            'catalog_number': 'PALEO-PROB-001',
            'scientific_name': 'Deinotherium giganteum',
            'common_name_sr': 'Деинотеријум (праисторијски слон)',
            'taxon_group': 'Proboscidea',
            'geological_period': 'Миоцен',
            'age_million_years': 10,
            'location_found': 'Белград, Србија',
            'date_discovered': '2015-03-20',
            'discoverers': 'С. Алабурић',
            'specimen_type': 'Кљова',
            'length_cm': 95,
            'condition': 'Одлично очуван',
            'exhibition': 'Surlaši - divovi prošlosti',
            'description': 'Кљова праисторијског слона. Део изложбе о сурлашима.',
            'curator': 'sanja.pavic@nhmbeo.rs'
        },
        {
            'catalog_number': 'PALEO-MOLL-001',
            'scientific_name': 'Viviparus serbicus',
            'common_name_sr': 'Српски живороднi пуж',
            'taxon_group': 'Mollusca',
            'geological_period': 'Миоцен',
            'age_million_years': 15,
            'location_found': 'Алексинац, Србија',
            'date_discovered': '2018-09-05',
            'discoverers': 'Др Б. Митровић',
            'specimen_type': 'Љушт ура',
            'length_cm': 3.5,
            'condition': 'Одлично очуван',
            'type_status': 'Нова врста за науку',
            'description': 'Фосилни слатководни пуж из миоцена. Описан од др Б. Митровић.',
            'curator': 'biljana.mitrovic@nhmbeo.rs'
        }
    ],
    'statistics': {
        'total_specimens': 3,
        'dinosaur_fossils': 1,
        'exhibitions': 'Evolucija, Surlaši, Ledeno doba, Fosilizacija'
    }
}

# Paleobotany Collection Database (Fallback)
_PALEOBOTANY_FALLBACK = {
    'specimens': [
        {
            'catalog_number': 'PBOT-2024-001',
            'scientific_name': 'Pteridium aquilinum (fossil)',
            'common_name_sr': 'Окамењена папрат',
            'geological_period': 'Карбон',
            'age_million_years': 300,
            'location_found': 'Алексинац, Србија',
            'date_discovered': '2019-06-10',
            'specimen_type': 'Лист (отисак)',
            'length_cm': 18,
            'width_cm': 12,
            'condition': 'Одлично очуван',
            'description': 'Окамењени лист древне папрати из каменоугљеног периода.',
            'curator': 'desadjm@nhmbeo.rs'
        },
        {
            'catalog_number': 'PBOT-2024-002',
            'scientific_name': 'Quercus sp. (fossil)',
            'common_name_sr': 'Фосилни храст',
            'geological_period': 'Неоген',
            'age_million_years': 8,
            'location_found': 'Мељак, Србија',
            'date_discovered': '2020-08-22',
            'specimen_type': 'Лист и жир',
            'length_cm': 14,
            'width_cm': 8,
            'condition': 'Добро очуван',
            'description': 'Фосилни лист и жир храста из неогена. Део истраживања праисторијске вегетације.',
            'curator': 'desadjm@nhmbeo.rs'
        }
    ],
    'statistics': {
        'total_specimens': 2,
        'curator_since': 1993,
        'role': 'Профессор палеоекологије'
    }
}

# Petrology Collection Database (Fallback)
_PETROLOGY_FALLBACK = {
    'specimens': [
        {
            'catalog_number': 'PETR-2024-001',
            'rock_name': 'Гранит',
            'scientific_name': 'Granite',
            'rock_type': 'Магматска стена',
            'location_found': 'Букуља, Србија',
            'geological_age': 'Палеоген',
            'date_collected': '2021-05-18',
            'minerals_present': 'Кварц, фелдспат, слуда',
            'texture': 'Грубозрна',
            'color': 'Светло сива',
            'weight_kg': 2.5,
            'dimensions_cm': '15x12x8',
            'condition': 'Одличан узорак',
            'description': 'Типичан гранит са великим кристалима. Користи се у градњи.',
            'curator': 'tatjana.milicbabic@nhmbeo.rs'
        },
        {
            'catalog_number': 'PETR-2024-002',
            'rock_name': 'Базалт',
            'scientific_name': 'Basalt',
            'rock_type': 'Вулканска стена',
            'location_found': 'Авала, Србија',
            'geological_age': 'Неоген',
            'date_collected': '2022-09-10',
            'minerals_present': 'Пироксен, плагиоклас',
            'texture': 'Ситнозрна',
            'color': 'Тамно сива до црна',
            'weight_kg': 1.8,
            'dimensions_cm': '12x10x7',
            'condition': 'Одличан узорак',
            'description': 'Вулканска стена настала брзим хлађењем лаве.',
            'curator': 'tatjana.milicbabic@nhmbeo.rs'
        }
    ],
    'statistics': {
        'total_specimens': 2,
        'exhibitions': 'I bi svetlost, Mozaik prirode'
    }
}

# Load all collections from PostgreSQL (or use fallback if DATABASE_URL not set)
BOTANY_COLLECTION_DATABASE = load_collection_database('botany', _BOTANY_FALLBACK)
ICHTHYOLOGY_COLLECTION_DATABASE = load_collection_database('ichthyology', _ICHTHYOLOGY_FALLBACK)
ENTOMOLOGY_COLLECTION_DATABASE = load_collection_database('entomology', _ENTOMOLOGY_FALLBACK)
MYCOLOGY_COLLECTION_DATABASE = load_collection_database('mycology', _MYCOLOGY_FALLBACK)
HERPETOLOGY_COLLECTION_DATABASE = load_collection_database('herpetology', _HERPETOLOGY_FALLBACK)
ORNITHOLOGY_COLLECTION_DATABASE = load_collection_database('ornithology', _ORNITHOLOGY_FALLBACK)
PALEOZOOLOGY_COLLECTION_DATABASE = load_collection_database('paleozoology', _PALEOZOOLOGY_FALLBACK)
PALEOBOTANY_COLLECTION_DATABASE = load_collection_database('paleobotany', _PALEOBOTANY_FALLBACK)
PETROLOGY_COLLECTION_DATABASE = load_collection_database('petrology', _PETROLOGY_FALLBACK)

# Meteorite Collection Database - Real Data from Museum Records
METEORITE_COLLECTION_DATABASE = {
    'specimens': [
        {
            'catalog_number': 'MET-001',
            'meteorite_name': 'Soko-Banja (Сокобања)',
            'classification': 'LL4 (Обични хондрит, брекча)',
            'fall_type': 'Пад (посматран)',
            'fall_date': '13. октобар 1877.',
            'total_mass_kg': 80.0,
            'specimen_mass': 16.286,
            'quantity': 1,
            'location_found': 'Сокобања, Заječарски округ, Централна Србија',
            'acquisition_date': 'Историјска колекција',
            'source': 'Оригинални налаз - 10 камена (највећи 38 kg)',
            'description': 'Најзначајнији српски метеорит. Пао 13.10.1877. Укупна маса свих камена 80 kg. Полиміктна брекча са различитим нивоима шока (S3-5). Садржи честице величине до 2 mm.',
            'meteorite_bulletin_number': '23661',
            'shock_stage': 'S3-5 (варијабилан шок)',
            'weathering_grade': 'W0 (без оксидације)',
            'chemical_composition': 'Оливин Fa26-32 mol%, Fe 19-22%, метално Fe 0.3-3%',
            'mineralogy': 'Оливин, ортопироксен, албитни плагиоклас, троилит, Fe-Ni метал',
            'parent_body': 'LL астероид из главног астероидног појаса',
            'curator': 'aca.lukovic@nhmbeo.rs',
            'serbian_meteorite': True
        },
        {
            'catalog_number': 'MET-002',
            'meteorite_name': 'Jelica (Јелица)',
            'classification': 'LL6 (Обични хондрит, брекча)',
            'fall_type': 'Пад (посматран)',
            'fall_date': '1. децембар 1889.',
            'total_mass_kg': 34.0,
            'specimen_mass': 8.5,
            'quantity': 1,
            'location_found': 'Јелица (Виљуша), Чачак, Моравички округ, Централна Србија (43.83°N, 20.44°E)',
            'acquisition_date': 'Историјска колекција',
            'source': 'Оригинални налаз - подручје пада 8x5 km',
            'description': 'Српски метеорит пао код планине Јелице 1.12.1889. Укупна маса 34 kg. Садржи еухедрални тетратаенит (65x107 μm) са импакт-растопљеним клaстом. Космички експозициони век ~26.2 милиона година.',
            'meteorite_bulletin_number': '12078',
            'shock_stage': 'S3 (слаб шок, ~15-20 GPa)',
            'weathering_grade': 'W0 (минимална еволуција)',
            'chemical_composition': 'Оливин Fa32.3 mol%, Fe 19-22%, метално Fe 0.3-3%, Ni≥50% у тетратаениту, Co 30% у вaирауиту',
            'mineralogy': 'Оливин, ортопироксен, албитни плагиоклас, троилит, Fe-Ni метал (тетратаенит, вaираuit, камацит, таенит), хромит, илменит, фосфати',
            'parent_body': 'LL астероид из главног астероидног појаса',
            'cosmic_ray_exposure': '~26.2 милиона година',
            'curator': 'aca.lukovic@nhmbeo.rs',
            'serbian_meteorite': True
        },
        {
            'catalog_number': 'MET-003',
            'meteorite_name': 'Dimitrovgrad (Димитровград)',
            'classification': 'Iron IIIAB (Гвоздени метеорит, средње октаедрит)',
            'fall_type': 'Налаз',
            'fall_date': 'Пронађен 1955.',
            'total_mass_kg': 'Није доступно',
            'specimen_mass': 100.0,
            'quantity': 1,
            'location_found': 'Димитровград, Пиротски округ, Централна Србија (43°2\'47"N, 22°51\'50"E)',
            'acquisition_date': '1955',
            'source': 'Документован налаз',
            'description': 'Српски гвоздени метеорит из Димитровграда. Пронађен 1955. Средње октаедрит са Widmanstätten структуром. Садржи камацит и таенит фазе.',
            'meteorite_bulletin_number': '7644',
            'shock_stage': 'Средњи до јак шок (типично за IIIAB)',
            'weathering_grade': 'Није наведено (налаз)',
            'chemical_composition': 'Ni 7.1-10.5%, Ga 16-23 ppm, Ge 27-47 ppm, Ir 0.01-19 ppm, Co ~0.5%, P 0.1-0.5%, S 0.1-1%',
            'mineralogy': 'Камацит и таенит (Fe-Ni фазе)',
            'widmanstatten_pattern': 'Присутан, ширина камацита 0.5-1.3 mm',
            'parent_body': 'Диференцирано језгро астероида из унутрашњег Сунчевог система',
            'curator': 'aca.lukovic@nhmbeo.rs',
            'serbian_meteorite': True
        },
        {
            'catalog_number': 'MET-004',
            'meteorite_name': 'Henbury (Pe section)',
            'classification': 'Iron IIIAB (Гвоздени метеорит, средње октаедрит)',
            'fall_type': 'Налаз',
            'fall_date': 'Откривен 1931., пао пре ~4,200±1,900 година',
            'total_mass_kg': 1.0,
            'specimen_mass': 0.1595,
            'quantity': 1,
            'location_found': 'Henbury Meteorite Conservation Reserve, Northern Territory, Аустралија (24°34\'S, 133°10\'E)',
            'acquisition_date': '1964-01-01',
            'source': 'Kyaneutta Museum, Kyaneutta, South Australia',
            'description': 'Пресек гвозденог метеорита из Хенбурија. Метеорит је створио ~13 ударних кратера (највећи 130m). Део међународне размене. Укупно пронађено преко 1000 kg.',
            'meteorite_bulletin_number': '11872',
            'shock_stage': 'Средњи до јак шок',
            'weathering_grade': 'Умерено до високо (хиљаде година изложености)',
            'chemical_composition': 'Ni 7.47%, Ga 17.7 ppm, Ge 33.7 ppm, Ir 13 ppm',
            'mineralogy': 'Камацит, таенит, коенит',
            'widmanstatten_pattern': 'Присутан (ширина камацита 0.9 mm), фине ламеле камацита и таенита',
            'parent_body': 'Диференцирано метално језгро астероида',
            'fusion_crust': 'Присутна на неким фрагментима',
            'curator': 'aca.lukovic@nhmbeo.rs',
            'serbian_meteorite': False
        },
        {
            'catalog_number': 'MET-005',
            'meteorite_name': 'Silica Glass (Henbury)',
            'classification': 'Импактно стакло',
            'total_mass_g': 3.0,
            'quantity': 2,
            'location_found': 'Henbury Meteorite Craters, 1/2 mile East of main Crater',
            'acquisition_date': '1964-01-01',
            'source': 'Kyaneutta Museum, Kyaneutta, South Australia',
            'description': 'Црно силикатно стакло из кратера Хенбури. Импактно стакло настало ударом.',
            'curator': 'aca.lukovic@nhmbeo.rs',
            'serbian_meteorite': False
        },
        {
            'catalog_number': 'MET-006',
            'meteorite_name': 'Wolf Creek (Wolfe Creek)',
            'classification': 'Iron IIIAB (Гвоздени метеорит, средње октаедрит)',
            'fall_type': 'Налаз',
            'fall_date': 'Кратер откривен 1947., пао пре 120,000-137,000 година',
            'total_mass_kg': 'Није прецизно квантификовано',
            'specimen_mass': 0.692,
            'quantity': 1,
            'location_found': 'Wolfe Creek Crater, Western Australia, Аустралија (Tanami Road, 150 km јужно од Halls Creek)',
            'acquisition_date': '1964-01-01',
            'source': 'Smithsonian Museum, USA',
            'description': 'Гвоздени метеорит из другог по величини кратера на свету са пронађеним метеоритом. Веома еродиран - фрагменти претворени у "гвоздене шкриљце" масе до 250 kg. Садржи 3.5-4.5% Ni у оксидованим фрагментима.',
            'meteorite_bulletin_number': '24326',
            'shock_stage': 'Није наведено',
            'weathering_grade': 'Високо (екстензивна оксидација у гвоздене шкриљце)',
            'chemical_composition': 'Ni 3.5-4.5% у оксидованим фрагментима (типично IIIAB: Ni 7.1-10.5%, Ga 16-23 ppm, Ge 27-47 ppm)',
            'mineralogy': 'Оксидовани метеоритски фрагменти, гвожђе-оксид, неки фрагменти садрже неалтерисани метал',
            'parent_body': 'Диференцирано метално језгро астероида',
            'terrestrial_age': 'Мање од 120,000 година (касни плеистоцен)',
            'curator': 'aca.lukovic@nhmbeo.rs',
            'serbian_meteorite': False
        },
        {
            'catalog_number': 'MET-007',
            'meteorite_name': 'Dalgaranga',
            'classification': 'Mesosiderite-A (Каменито-гвоздени метеорит)',
            'fall_type': 'Налаз',
            'fall_date': 'Откривен 1921.',
            'total_mass_kg': 12.2,
            'specimen_mass': 0.1328,
            'quantity': 1,
            'location_found': 'Dalgaranga Crater, Western Australia, Аустралија (75 km NW од Mount Magnet)',
            'acquisition_date': '1964-01-01',
            'source': 'Smithsonian Museum, USA (оригинално Gerard Wellard, 1921)',
            'description': 'ЈЕДИНСТВЕН метеорит - једини кратер на свету створен месосидеритом! Месосидерит са подједнаким деловима Ni-Fe метала и силиката. Формиранударом између кора и језгра астероида Весте пре ~4,525 милиона година.',
            'meteorite_bulletin_number': '5506',
            'shock_stage': 'S1-S2 (веома слаб шок, <10 GPa)',
            'weathering_grade': 'Умерено (налаз из 1921)',
            'chemical_composition': 'Оливин Fo58-92 (Fa8-42), Пироксен Fs20-40, Плагиоклас An>80 (анортит до битовнит)',
            'mineralogy': 'Ортопироксен, калциумски плагиоклас (доминантни), пигионит, оливин, тридимит, Ni-Fe метал (камацит, таенит)',
            'parent_body': 'Астероид 4 Vesta или сличан диференциран астероид',
            'fragment_type': 'Петролошка класа A (висок садржај плагиокласа)',
            'dating_method': 'U-Pb датирање: формирање коре 4,558.5±2.1 Ma, мешање метал-силикат 4,525.39±0.85 Ma',
            'curator': 'aca.lukovic@nhmbeo.rs',
            'serbian_meteorite': False
        },
        {
            'catalog_number': 'MET-008',
            'meteorite_name': 'Plainview',
            'classification': 'H5 (Обични хондрит, високо гвожђе, брекча)',
            'fall_type': 'Налаз',
            'fall_date': 'Пронађен 1917.',
            'total_mass_kg': 700.0,
            'specimen_mass': 0.132,
            'quantity': 1,
            'location_found': 'Plainview, Hale County, Texas, USA (8 km SW од Plainview)',
            'acquisition_date': '1964-01-01',
            'source': 'Smithsonian Museum, USA',
            'description': 'ТРЕЋИ најмасивнији H5 хондрит на свету (после Јилин 4 тоне и Куња-Ургенч 1.1 тона). Полиміктна брекча са реголитним материјалом. Подручје пада 6x26 km. Преко 700 kg сакупљено захваљујући Harvey Nininger-у.',
            'meteorite_bulletin_number': '54437',
            'shock_stage': 'S3 (слаб шок, ~15-20 GPa)',
            'weathering_grade': 'W2 (мања оксидација метала и сулфида, рђа)',
            'chemical_composition': 'Оливин Fa16-20 mol%, Fe 25-31%, метално Fe 15-19%, просечна величина хондрула ~0.3 mm',
            'mineralogy': 'Оливин, пироксен, плагиоклас, троилит, Fe-Ni метал; садржи неравнотежене силикатне зрна и хондруле',
            'parent_body': 'H хондритски астероид из главног астероидног појаса',
            'fragment_type': 'Комплексна реголитна брекча формирана поновљеним ударима на површини родитељског тела',
            'curator': 'aca.lukovic@nhmbeo.rs',
            'serbian_meteorite': False
        },
        {
            'catalog_number': 'MET-009',
            'meteorite_name': 'Toluca (Xiquipilco)',
            'classification': 'Гвоздени метеорит',
            'total_mass_g': 59.0,
            'quantity': 1,
            'location_found': 'Xiquipilco, Toluca, Mexico',
            'acquisition_date': '1964-01-01',
            'source': 'Smithsonian Museum, USA',
            'description': 'Гвоздени метеорит из Мексика. Познати метеорит Толука.',
            'curator': 'aca.lukovic@nhmbeo.rs',
            'serbian_meteorite': False
        },
        {
            'catalog_number': 'MET-010',
            'meteorite_name': 'Canyon Diablo',
            'classification': 'Гвоздени метеорит',
            'total_mass_g': 231.0,
            'quantity': 2,
            'location_found': 'Canyon Diablo, Arizona, USA',
            'acquisition_date': '1964-01-01',
            'source': 'Smithsonian Museum, USA',
            'description': 'Чувени метеорит из Каниона Ђаволо, креатора Meteor Cratera у Аризони.',
            'curator': 'aca.lukovic@nhmbeo.rs',
            'serbian_meteorite': False
        },
        {
            'catalog_number': 'MET-011',
            'meteorite_name': 'Звор нички хондрит',
            'classification': 'Хондрит',
            'total_mass_g': 66.5,
            'quantity': 1,
            'location_found': 'Зворник, Завидовићи, Босна и Херцеговина',
            'acquisition_date': 'Историјска колекција',
            'source': 'Мехо Рамовић',
            'description': 'Хондрит са подручја бивше Југославије. Донација М. Рамовића.',
            'curator': 'aca.lukovic@nhmbeo.rs',
            'serbian_meteorite': False
        },
        {
            'catalog_number': 'MET-012',
            'meteorite_name': 'Влтавин - Молдавит',
            'classification': 'Тектит (импактно стакло)',
            'total_mass_g': 'N/A',
            'quantity': 8,
            'location_found': 'Врабце код Ч. Будејовица, Чехословачка',
            'acquisition_date': 'Историјска колекција',
            'source': 'F.S. Tvrdel',
            'description': 'Влтавин (молдавит) - зелено тектитно стакло из Чешке. 8 примерака.',
            'curator': 'aca.lukovic@nhmbeo.rs',
            'serbian_meteorite': False
        },
        {
            'catalog_number': 'MET-013',
            'meteorite_name': 'Тектит (Индокинит)',
            'classification': 'Тектит (импактно стакло)',
            'total_mass_g': 7.2,
            'quantity': 1,
            'location_found': 'Лева обала реке Меконг, Лаос',
            'acquisition_date': 'Историјска колекција',
            'source': 'Др Ранко Рушић',
            'description': 'Индокинитски тектит из Лаоса. Донација др Р. Рушића.',
            'curator': 'aca.lukovic@nhmbeo.rs',
            'serbian_meteorite': False
        },
        {
            'catalog_number': 'MET-014',
            'meteorite_name': 'Mundrabila',
            'classification': 'Метеорит',
            'total_mass_kg': 1.965,
            'quantity': 1,
            'location_found': 'Пруга Перт - Аделаида (30°45\'S 127°30\'E), Аустралија',
            'acquisition_date': 'Историјска колекција',
            'source': 'Paul Ramdohr',
            'description': 'Метеорит Мундрабила из западне Аустралије. Донација P. Ramdohra.',
            'curator': 'aca.lukovic@nhmbeo.rs',
            'serbian_meteorite': False
        },
        {
            'catalog_number': 'MET-015',
            'meteorite_name': 'Henbury Iron #2',
            'classification': 'Гвоздени метеорит',
            'total_mass_g': 120.5,
            'quantity': 4,
            'location_found': 'Henbury, Central Australia',
            'acquisition_date': '1964-01-01',
            'source': 'Kyaneutta Museum, Kyaneutta, South Australia',
            'description': 'Додатни узорци гвозденог метеорита из Хенбурија. 4 примерка.',
            'curator': 'aca.lukovic@nhmbeo.rs',
            'serbian_meteorite': False
        },
        {
            'catalog_number': 'MET-016',
            'meteorite_name': 'Шљакасте бомбе (Henbury)',
            'classification': 'Импактни материјал',
            'total_mass_g': 28.35,
            'quantity': 3,
            'location_found': 'Henbury главни кратер, Central Australia',
            'acquisition_date': '1964-01-01',
            'source': 'Kyaneutta Museum, Kyaneutta, South Australia',
            'description': 'Шљакасте бомбе из главног кратера Хенбури. Импактни материјал.',
            'curator': 'aca.lukovic@nhmbeo.rs',
            'serbian_meteorite': False
        },
        {
            'catalog_number': 'MET-017',
            'meteorite_name': 'Henbury Iron #3',
            'classification': 'Гвоздени метеорит',
            'total_mass_g': 191.0,
            'quantity': 3,
            'location_found': 'Henbury, Central Australia',
            'acquisition_date': '1964-01-01',
            'source': 'Kyaneutta Museum, Kyaneutta, South Australia',
            'description': 'Гвоздени метеорит из Хенбурија. 3 примерка. Део аустралијске колекције.',
            'curator': 'aca.lukovic@nhmbeo.rs',
            'serbian_meteorite': False
        },
        {
            'catalog_number': 'MET-018',
            'meteorite_name': 'Bjurbole',
            'classification': 'Хиперстен хондрит',
            'total_mass_g': 55.2,
            'quantity': 1,
            'location_found': 'Bjurbole, Borge, Finland',
            'acquisition_date': 'Историјска колекција',
            'source': 'Minerals Engineering S.A, Geneva, Швајцарска',
            'description': 'Хиперстен хондрит из Финске. Класичан L/LL хондрит, пао 1899.',
            'curator': 'aca.lukovic@nhmbeo.rs',
            'serbian_meteorite': False
        }
    ],
    'statistics': {
        'total_specimens': 18,
        'serbian_meteorites': 3,
        'international_specimens': 15,
        'iron_meteorites': 7,
        'stony_meteorites': 4,
        'tektites': 2,
        'total_mass_kg': 23.631,
        'oldest_acquisition': '1949'
    }
}

# Conservation Biology Records
CONSERVATION_BIOLOGY_DATABASE = {
    'records': [
        {
            'record_number': 'CONS-2024-001',
            'specimen_id': 'ENT-LEP-001',
            'specimen_name': 'Parnassius apollo',
            'conservation_type': 'Препарација',
            'conservator': 'Г. Петковски',
            'date_started': '2024-01-15',
            'date_completed': '2024-02-20',
            'condition_before': 'Оштећен',
            'condition_after': 'Одличан',
            'treatment_applied': 'Чишћење, стабилизација, монтирање на игли',
            'materials_used': 'Ентомолошке иглице, памук, дрво',
            'notes': 'Успешно препариран примерак за изложбу инсеката.',
            'storage_location': 'Ентомолошка збирка - фиока 12'
        },
        {
            'record_number': 'CONS-2024-002',
            'specimen_id': 'HERP-AMP-001',
            'specimen_name': 'Salamandra salamandra',
            'conservation_type': 'Конзервација',
            'conservator': 'М. Мрваљевић',
            'date_started': '2024-03-10',
            'date_completed': '2024-03-25',
            'condition_before': 'Добар',
            'condition_after': 'Одличан',
            'treatment_applied': 'Формалин конзервација, стаклена боца',
            'materials_used': 'Формалин 4%, стаклена боца',
            'notes': 'Влажна препарација за научну колекцију.',
            'storage_location': 'Херпетолошка збирка - полица А-15'
        }
    ],
    'statistics': {
        'total_records': 2,
        'conservators': 3,
        'specimens_treated_2024': 2
    }
}

# Visitor Records Database
VISITOR_RECORDS = []

# Research Projects Database
RESEARCH_PROJECTS = []

# Vehicle data files (fallback for legacy mode)
VEHICLES_FILE = 'data/museum_vehicles.json'
RESERVATIONS_FILE = 'data/vehicle_reservations.json'

def load_vehicles():
    """Load vehicles from PostgreSQL or JSON file (fallback)."""
    if os.environ.get('DATABASE_URL'):
        try:
            return phase3a_databases.get_vehicles_list()
        except Exception as e:
            logging.warning(f"Failed to load vehicles from PostgreSQL: {e}")
            # Fall through to JSON fallback

    # JSON fallback
    try:
        if os.path.exists(VEHICLES_FILE):
            with open(VEHICLES_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
    except Exception as e:
        print(f"Error loading vehicles: {e}")

    # Return default vehicles if file doesn't exist
    return [
        {
            'id': 1,
            'name': 'Комби возило',
            'registration': 'BG-1234-AB',
            'type': 'Комби',
            'capacity': '9 путника',
            'status': 'Активно'
        },
        {
            'id': 2,
            'name': 'Теренско возило',
            'registration': 'BG-5678-CD',
            'type': 'Теренац',
            'capacity': '5 путника',
            'status': 'Активно'
        }
    ]

def save_vehicles():
    """Save vehicles to JSON file (fallback only)."""
    try:
        os.makedirs(os.path.dirname(VEHICLES_FILE), exist_ok=True)
        with open(VEHICLES_FILE, 'w', encoding='utf-8') as f:
            json.dump(MUSEUM_VEHICLES, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        print(f"Error saving vehicles: {e}")
        return False

def load_reservations():
    """Load reservations from PostgreSQL or JSON file (fallback)."""
    if os.environ.get('DATABASE_URL'):
        try:
            return phase3a_databases.get_vehicle_reservations()
        except Exception as e:
            logging.warning(f"Failed to load reservations from PostgreSQL: {e}")
            # Fall through to JSON fallback

    # JSON fallback
    try:
        if os.path.exists(RESERVATIONS_FILE):
            with open(RESERVATIONS_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
    except Exception as e:
        print(f"Error loading reservations: {e}")
    return []

def save_reservations():
    """Save reservations to JSON file (fallback only)."""
    try:
        os.makedirs(os.path.dirname(RESERVATIONS_FILE), exist_ok=True)
        with open(RESERVATIONS_FILE, 'w', encoding='utf-8') as f:
            json.dump(VEHICLE_RESERVATIONS, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        print(f"Error saving reservations: {e}")
        return False

# Museum Vehicles Database - loaded once at startup
MUSEUM_VEHICLES = load_vehicles()

# Vehicle Reservations Database - loaded once at startup
VEHICLE_RESERVATIONS = load_reservations()

# Cultural Heritage Database (Заштићена културна добра)
CULTURAL_HERITAGE_DATABASE = {
    'heritage_items': [
        {
            'id': 1,
            'name': 'Скелет тираносауруса рекса',
            'registry_number': 'КД-ПМ-001/2015',
            'type': 'Покретно културно добро',
            'category': 'Природњачко наслеђе',
            'subcategory': 'Палеонтолошки узорак',
            'significance': 'Културно добро од великог значаја',
            'location': 'Сала 1 - Витрина 3',
            'condition': 'Одлично',
            'protection_date': '2015-06-20',
            'acquisition_date': '2015-03-15',
            'description': 'Комплетан скелет младог тираносауруса рекса, стар око 65 милиона година. Јединствен експонат са територије Североамеричког континента.',
            'legal_basis': 'Решење Министарства културе РС бр. 612-00-00403/2015-05',
            'cultural_value': 'Научно и едукативно наслеђе изузетне вредности',
            'period': 'Креда (65 милиона година)',
            'origin': 'Монтана, САД',
            'dimensions': '4.5m × 2.1m × 1.8m',
            'material': 'Окамењене кости',
            'weight': '450 kg',
            'protection_status': 'заштићено'
        },
        {
            'id': 2,
            'name': 'Кристал кварца са Копаоника',
            'registry_number': 'КД-ПМ-002/2018',
            'type': 'Покретно културно добро',
            'category': 'Природњачко наслеђе',
            'subcategory': 'Минералошки узорак',
            'significance': 'Културно добро',
            'location': 'Сала 2 - Витрина 1',
            'condition': 'Добро',
            'protection_date': '2018-09-15',
            'acquisition_date': '2018-07-22',
            'description': 'Велики кристал кварца са планине Копаоник, представља геолошко наслеђе Србије',
            'legal_basis': 'Решење Завода за заштиту споменика културе бр. 1247/18',
            'cultural_value': 'Геолошко наслеђе националног значаја',
            'period': 'Мезозоик',
            'origin': 'Копаоник, Србија',
            'dimensions': '45cm × 30cm × 25cm',
            'material': 'Кварц',
            'weight': '15 kg',
            'protection_status': 'заштићено'
        },
        {
            'id': 3,
            'name': 'Окамењени лист древне папрати',
            'registry_number': 'КД-ПМ-003/2020',
            'type': 'Покретно културно добро',
            'category': 'Природњачко наслеђе',
            'subcategory': 'Палеоботанички узорак',
            'significance': 'Културно добро',
            'location': 'Депо А - Полица 15',
            'condition': 'Добро',
            'protection_date': '2020-12-10',
            'acquisition_date': '2020-11-08',
            'description': 'Окамењени лист древне папрати из карбонског периода, пронађен на територији Алексинца',
            'legal_basis': 'Решење Завода за заштиту споменика културе бр. 2156/20',
            'cultural_value': 'Научно наслеђе палеоботанике',
            'period': 'Карбон (300 милиона година)',
            'origin': 'Алексинац, Србија',
            'dimensions': '20cm × 15cm × 3cm',
            'material': 'Окамењени биљни остаци',
            'weight': '2 kg',
            'protection_status': 'заштићено'
        },
        {
            'id': 4,
            'name': 'Збирка лептира Балканског полуострва',
            'registry_number': 'КД-ПМ-004/2019',
            'type': 'Покретно културно добро',
            'category': 'Природњачко наслеђе',
            'subcategory': 'Ентомолошка збирка',
            'significance': 'Културно добро од великог значаја',
            'location': 'Сала 3 - Витрина 5',
            'condition': 'Одлично',
            'protection_date': '2019-07-25',
            'acquisition_date': '2019-05-14',
            'description': 'Колекција од 120 врста лептира са Балкана, представља биодиверзитет региона',
            'legal_basis': 'Решење Министарства културе РС бр. 612-00-00891/2019-05',
            'cultural_value': 'Биолошко наслеђе Балканског полуострва',
            'period': 'Савремено (XIX-XXI век)',
            'origin': 'Балкан',
            'dimensions': '1.2m × 0.8m × 0.1m',
            'material': 'Ентомолошки препарати',
            'weight': '8 kg',
            'protection_status': 'заштићено'
        },
        {
            'id': 5,
            'name': 'Херцинит кристал из Босилеграда',
            'registry_number': 'КД-ПМ-005/2021',
            'type': 'Покретно културно добро',
            'category': 'Природњачко наслеђе',
            'subcategory': 'Минералошки узорак',
            'significance': 'Културно добро од изузетног значаја',
            'location': 'Сала 2 - Витрина 2',
            'condition': 'Одлично',
            'protection_date': '2021-10-18',
            'acquisition_date': '2021-09-03',
            'description': 'Ретки кристал херцинита са локалитета Босилеград, јединствен минералошки узорак',
            'legal_basis': 'Решење Министарства културе РС бр. 612-00-01203/2021-05',
            'cultural_value': 'Минералошко наслеђе изузетне реткости',
            'period': 'Палеозоик',
            'origin': 'Босилеград, Србија',
            'dimensions': '12cm × 8cm × 6cm',
            'material': 'Херцинит (цинк алуминијум оксид)',
            'weight': '1.5 kg',
            'protection_status': 'заштићено'
        },
        {
            'id': 6,
            'name': 'Фосил трилобита из ордовика',
            'registry_number': 'КД-ПМ-006/2017',
            'type': 'Покретно културно добро',
            'category': 'Природњачко наслеђе',
            'subcategory': 'Палеонтолошки узорак',
            'significance': 'Културно добро',
            'location': 'Сала 1 - Витрина 2',
            'condition': 'Добро',
            'protection_date': '2018-02-14',
            'acquisition_date': '2017-12-10',
            'description': 'Добро очувани фосил трилобита из ордовика, сведочи о древном животу',
            'legal_basis': 'Решење Завода за заштиту споменика културе бр. 0234/18',
            'cultural_value': 'Палеонтолошко наслеђе',
            'period': 'Ордовик (450 милиона година)',
            'origin': 'Чешка Република',
            'dimensions': '8cm × 6cm × 2cm',
            'material': 'Окамењени остаци',
            'weight': '0.3 kg',
            'protection_status': 'заштићено'
        }
    ],
    'heritage_types': ['Покретно културно добро', 'Непокретно културно добро'],
    'categories': ['Природњачко наслеђе', 'Уметничко-историјска дела', 'Архивска грађа', 'Старе и ретке књиге'],
    'subcategories': ['Палеонтолошки узорак', 'Минералошки узорак', 'Палеоботанички узорак', 'Ентомолошка збирка', 'Зоолошки узорак', 'Геолошки узорак'],
    'significance_levels': ['Културно добро', 'Културно добро од великог значаја', 'Културно добро од изузетног значаја'],
    'locations': ['Сала 1', 'Сала 2', 'Сала 3', 'Депо А', 'Депо Б', 'Привремени депо'],
    'conditions': ['Одлично', 'Добро', 'Задовољавајуће', 'Лоше', 'Захтева рестаурацију'],
    'protection_statuses': ['заштићено', 'у поступку заштите', 'предложено за заштиту', 'неевидентирано'],
    'statistics': {
        'total_heritage_items': 6,
        'exceptional_significance': 1,
        'great_significance': 2,
        'regular_significance': 3,
        'natural_heritage': 6,
        'displayed_items': 5,
        'storage_items': 1,
        'excellent_condition': 3,
        'good_condition': 3
    }
}

# Cache for Phase 3A databases loaded from PostgreSQL
_CACHED_HERITAGE_DB = None
_CACHED_METEORITE_DB = None

def get_cultural_heritage_database():
    """Get cultural heritage database from PostgreSQL or fallback to dict."""
    global _CACHED_HERITAGE_DB

    if os.environ.get('DATABASE_URL'):
        # Use PostgreSQL (Phase 3A) - cache the result
        if _CACHED_HERITAGE_DB is None:
            _CACHED_HERITAGE_DB = phase3a_databases.get_cultural_heritage_database()
        return _CACHED_HERITAGE_DB
    else:
        # Use in-memory dict
        return CULTURAL_HERITAGE_DATABASE

def get_meteorite_collection_database():
    """Get meteorite collection database from PostgreSQL or fallback to dict."""
    global _CACHED_METEORITE_DB

    if os.environ.get('DATABASE_URL'):
        # Use PostgreSQL (Phase 3A) - cache the result
        if _CACHED_METEORITE_DB is None:
            _CACHED_METEORITE_DB = phase3a_databases.get_meteorite_collection_database()
        return _CACHED_METEORITE_DB
    else:
        # Use in-memory dict
        return METEORITE_COLLECTION_DATABASE

def authenticate_fallback_user(email, password):
    """
    Authenticate user using fallback employee database (development only).
    DO NOT USE IN PRODUCTION - set ENABLE_FALLBACK_AUTH=False in .env
    """
    if not app.config.get('ENABLE_FALLBACK_AUTH', False):
        return None

    # Check if admin email matches configured admin
    admin_email = app.config.get('ADMIN_EMAIL', 'admin@nhmbeo.rs')
    admin_password = app.config.get('ADMIN_DEFAULT_PASSWORD', 'change-this-immediately')
    admin_username = app.config.get('ADMIN_USERNAME', 'admin')
    fallback_password = app.config.get('ADMIN_FALLBACK_PASSWORD', 'admin123')

    normalized_email = email.strip().lower()
    admin_aliases = {
        admin_email.lower(),
        admin_username.lower(),
        'admin'
    }

    valid_passwords = {admin_password}
    if fallback_password:
        valid_passwords.add(fallback_password)

    if normalized_email in admin_aliases and password in valid_passwords:
        stored_email = admin_email if normalized_email == admin_email.lower() else (admin_username or admin_email)
        return {
            'user_id': 1,
            'email': stored_email.lower(),
            'full_name': 'System Administrator',
            'department': 'Administration',
            'position': 'Administrator',
            'role': 'admin',
            'is_first_login': True  # Force password change
        }

    return None

# Note: login_required and admin_required decorators are now imported from security_utils

@app.route('/')
def index():
    """Main landing page."""
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
@csrf.exempt  # Temporarily exempt from CSRF for testing
@limiter.limit("5 per minute")
def login():
    """User login with security enhancements."""
    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')

        # Validate inputs
        if not email or not password:
            flash('Молимо унесите имејл и лозинку.', 'error')
            return render_template('login.html')

        # Check for account lockout
        max_attempts = app.config.get('MAX_LOGIN_ATTEMPTS', 5)
        lockout_duration = app.config.get('ACCOUNT_LOCKOUT_DURATION', 1800)

        is_locked, seconds_remaining = login_tracker.is_locked_out(
            email, max_attempts, lockout_duration
        )

        if is_locked:
            minutes = seconds_remaining // 60
            flash(
                f'Налог је закључан због превише неуспешних покушаја. '
                f'Покушајте поново за {minutes} минута.',
                'danger'
            )
            log_security_event('account_locked', {
                'email': email,
                'remaining_seconds': seconds_remaining
            })
            return render_template('login.html')

        # Try authentication
        authenticated_user = None

        try:
            if auth_available:
                # Primary: Use PostgreSQL authentication
                authenticated_user = auth_system.verify_credentials(email, password)
            elif app.config.get('ENABLE_FALLBACK_AUTH', False):
                # Fallback: Development only
                logger.warning(f"Using fallback auth for: {email}")
                authenticated_user = authenticate_fallback_user(email, password)
            else:
                flash('Систем аутентикације није доступан.', 'error')
                return render_template('login.html')

        except Exception as e:
            logger.error(f"Authentication error for {email}: {e}")
            flash('Грешка при пријављивању. Покушајте поново.', 'error')
            return render_template('login.html')

        if authenticated_user:
            # Successful login (handle both MySQL and PostgreSQL auth formats)
            user_id = authenticated_user.get('user_id') or authenticated_user.get('id')
            session['user_id'] = user_id
            session['user_email'] = authenticated_user['email']
            session['user_name'] = authenticated_user['full_name']
            session['user_role'] = authenticated_user['role']
            session['user_department'] = authenticated_user.get('department', '')
            session.permanent = True  # Use configured timeout

            # Reset login attempts
            login_tracker.record_attempt(email, success=True)

            # Log successful login
            log_security_event('login_success', {
                'email': email,
                'user_id': user_id
            })

            # Check if password change required
            if authenticated_user.get('is_first_login', False):
                flash('Морате променити лозинку при првој пријави.', 'warning')
                return redirect(url_for('change_password'))

            flash(f'Добродошли, {authenticated_user["full_name"]}!', 'success')
            return redirect(url_for('dashboard'))
        else:
            # Failed login
            login_tracker.record_attempt(email, success=False)
            remaining = login_tracker.get_remaining_attempts(email, max_attempts)

            flash(
                f'Неисправни подаци за пријаву. '
                f'Преостало покушаја: {remaining}',
                'danger'
            )

            log_security_event('login_failed', {
                'email': email,
                'remaining_attempts': remaining
            })

            return render_template('login.html')

    return render_template('login.html')

@app.route('/logout')
def logout():
    """User logout."""
    session.clear()
    flash('Успешно сте се одјавили.', 'info')
    return redirect(url_for('index'))

@app.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    """Change user password with validation."""
    if request.method == 'POST':
        current_password = request.form.get('current_password', '')
        new_password = request.form.get('new_password', '')
        confirm_password = request.form.get('confirm_password', '')

        # Validate inputs
        if not all([current_password, new_password, confirm_password]):
            flash('Попуните сва поља.', 'error')
            return render_template('change_password.html')

        if new_password != confirm_password:
            flash('Нове лозинке се не подударају.', 'error')
            return render_template('change_password.html')

        # Validate password strength
        is_valid, errors = password_validator.validate(new_password)
        if not is_valid:
            for error in errors:
                flash(error, 'error')
            return render_template('change_password.html')

        # Change password
        user_id = session.get('user_id')
        user_email = session.get('user_email')

        try:
            if auth_available:
                # Use PostgreSQL authentication system
                # First verify current password
                if auth_system.verify_credentials(user_email, current_password):
                    success = auth_system.update_password(user_email, new_password)
                else:
                    flash('Тренутна лозинка није тачна.', 'error')
                    return redirect(url_for('change_password'))
            elif app.config.get('ENABLE_FALLBACK_AUTH', False):
                # Cannot change password in fallback mode
                flash('Промена лозинке није доступна у режиму развоја.', 'warning')
                return redirect(url_for('dashboard'))
            else:
                flash('Систем аутентикације није доступан.', 'error')
                return render_template('change_password.html')

            if success:
                log_security_event('password_changed', {
                    'user_id': user_id,
                    'email': user_email
                })

                flash('Лозинка је успешно промењена!', 'success')
                return redirect(url_for('dashboard'))
            else:
                flash('Неисправна тренутна лозинка.', 'error')
                return render_template('change_password.html')

        except Exception as e:
            logger.error(f"Password change error: {e}")
            flash('Грешка при промени лозинке.', 'error')
            return render_template('change_password.html')

    return render_template('change_password.html')

@app.route('/dashboard')
@login_required
def dashboard():
    """Main dashboard."""
    user_role = session.get('user_role')
    user_name = session.get('user_name')
    user_email = session.get('user_email')

    # Get modules user has access to
    accessible_modules = get_user_modules(user_email, user_role)

    return render_template('dashboard.html',
                          user_role=user_role,
                          user_name=user_name,
                          user_email=user_email,
                          accessible_modules=accessible_modules)

@app.route('/timesheet')
@login_required
def timesheet_app():
    """Route to timesheet application."""
    user_email = session.get('user_email')
    user_role = session.get('user_role')

    if not user_has_module_access(user_email, user_role, 'timesheet'):
        flash('Немате дозволу за приступ систему радних листи.', 'error')
        return redirect(url_for('dashboard'))

    timesheet_data = None
    timesheet_labels = TimesheetRepository.CATEGORY_LABELS if timesheet_repository else {}
    if timesheet_repository and timesheet_repository.available:
        month_summary = timesheet_repository.get_month_summary()
        overall_summary = timesheet_repository.get_overall_summary()
        recent_reports = timesheet_repository.list_reports(page=1, per_page=5)
        timesheet_data = {
            'month_summary': month_summary,
            'overall': overall_summary,
            'recent_reports': recent_reports.get('reports', [])
        }

    return render_template('timesheet_integration.html',
                           timesheet_data=timesheet_data,
                           timesheet_labels=timesheet_labels,
                           user_role=user_role,
                           user_name=session.get('user_name'),
                           user_email=user_email)


def _parse_int(value: Optional[str]) -> Optional[int]:
    try:
        if value is None or value == '':
            return None
        return int(value)
    except (TypeError, ValueError):
        return None


def _month_options():
    return [(idx, calendar.month_name[idx]) for idx in range(1, 13)]


@app.route('/admin/timesheet')
@admin_required
def admin_timesheet_main():
    """Main timesheet administration page."""
    return render_template('admin_timesheet_admin.html')


@app.route('/admin/timesheet_reports')
@admin_required
def admin_timesheet_reports():
    """Admin view for centralized timesheet reports (PostgreSQL)."""
    if not timesheet_repository or not timesheet_repository.available:
        flash('Централизовани подаци о радним листама нису доступни (проверите PostgreSQL миграцију).', 'error')
        return redirect(url_for('timesheet_app'))

    month = _parse_int(request.args.get('month'))
    year = _parse_int(request.args.get('year'))
    search = request.args.get('search', '').strip() or None
    page = _parse_int(request.args.get('page')) or 1

    reports = timesheet_repository.list_reports(page=page, per_page=25, month=month, year=year, search=search)
    month_summary = timesheet_repository.get_month_summary(month=month, year=year)
    overall_summary = timesheet_repository.get_overall_summary()

    return render_template(
        'admin_timesheet_reports.html',
        reports=reports,
        month_summary=month_summary,
        overall_summary=overall_summary,
        month=month,
        year=year,
        search=search or '',
        month_options=_month_options(),
        category_labels=TimesheetRepository.CATEGORY_LABELS,
        calendar=calendar
    )


@app.route('/admin/timesheet_reports/<int:report_id>')
@admin_required
def admin_timesheet_report_detail(report_id):
    """Detailed view of a single report."""
    if not timesheet_repository or not timesheet_repository.available:
        flash('Централизовани подаци о радним листама нису доступни (проверите PostgreSQL миграцију).', 'error')
        return redirect(url_for('timesheet_app'))

    report = timesheet_repository.get_report(report_id)
    if not report:
        flash('Тражени извештај није пронађен.', 'error')
        return redirect(url_for('admin_timesheet_reports'))

    return render_template(
        'admin_timesheet_report_detail.html',
        report=report,
        category_labels=TimesheetRepository.CATEGORY_LABELS,
        month_name=calendar.month_name[int(report['header'].get('month', 1))]
    )


@app.route('/admin/timesheet/employees')
@admin_required
def admin_timesheet_employees():
    """Admin view for managing employees in timesheet system."""
    if not timesheet_repository or not timesheet_repository.available:
        flash('Централизовани подаци о радним листама нису доступни (проверите PostgreSQL миграцију).', 'error')
        return redirect(url_for('admin_panel'))

    flash('Ова функција је у развоју. Користите базу запослених за управљање.', 'info')
    return redirect(url_for('employees_database'))


@app.route('/admin/timesheet/users')
@admin_required
def admin_timesheet_users():
    """Admin view for managing timesheet system users."""
    if not timesheet_repository or not timesheet_repository.available:
        flash('Централизовани подаци о радним листама нису доступни (проверите PostgreSQL миграцију).', 'error')
        return redirect(url_for('admin_panel'))

    flash('Ова функција је у развоју. Користите управљање приступом за конфигурацију корисника.', 'info')
    return redirect(url_for('manage_access'))


@app.route('/admin/timesheet/pending')
@admin_required
def admin_timesheet_pending():
    """Admin view for pending edit requests."""
    if not timesheet_repository or not timesheet_repository.available:
        flash('Централизовани подаци о радним листама нису доступни (проверите PostgreSQL миграцију).', 'error')
        return redirect(url_for('admin_panel'))

    try:
        import psycopg
        from psycopg.rows import dict_row

        with psycopg.connect(conninfo=os.environ.get('DATABASE_URL', '').replace('postgresql+psycopg://', 'postgresql://'), row_factory=dict_row) as conn:
            with conn.cursor() as cur:
                # Get all edit requests with report details
                cur.execute("""
                    SELECT
                        ter.id,
                        ter.report_id,
                        ter.requester_email,
                        ter.reason,
                        ter.status,
                        ter.requested_at,
                        ter.processed_at,
                        ter.processed_by,
                        ter.notes,
                        tr.employee_name,
                        tr.month,
                        tr.year,
                        tr.is_verified,
                        tr.is_locked
                    FROM timesheet_edit_requests ter
                    JOIN timesheet_reports tr ON ter.report_id = tr.id
                    ORDER BY
                        CASE ter.status
                            WHEN 'pending' THEN 1
                            WHEN 'approved' THEN 2
                            WHEN 'rejected' THEN 3
                        END,
                        ter.requested_at DESC
                """)

                requests = cur.fetchall()

        # Add Serbian month names
        serbian_months = [
            "Јануар", "Фебруар", "Март", "Април", "Мај", "Јун",
            "Јул", "Август", "Септембар", "Октобар", "Новембар", "Децембар"
        ]

        for req in requests:
            month_idx = req['month'] - 1
            if 0 <= month_idx < 12:
                req['month_name'] = serbian_months[month_idx]
            else:
                req['month_name'] = str(req['month'])

        return render_template(
            'admin_timesheet_pending.html',
            pending_requests=requests,
            message=None
        )

    except Exception as e:
        flash(f'Грешка при учитавању захтева: {str(e)}', 'error')
        return render_template(
            'admin_timesheet_pending.html',
            pending_requests=[],
            message=f'Грешка: {str(e)}'
        )


@app.route('/admin/timesheet/analytics')
@admin_required
def admin_timesheet_analytics():
    """Admin analytics dashboard for timesheet system."""
    if not timesheet_repository or not timesheet_repository.available:
        flash('Централизовани подаци о радним листама нису доступни (проверите PostgreSQL миграцију).', 'error')
        return redirect(url_for('admin_panel'))

    # Get basic statistics for now
    overall_summary = timesheet_repository.get_overall_summary()

    return render_template(
        'admin_timesheet_analytics.html',
        overall_summary=overall_summary,
        message='Напредна аналитика је у развоју.'
    )


# ============================================================================
# ADMIN TIMESHEET API ENDPOINTS (PostgreSQL)
# ============================================================================

@app.route('/api/admin/timesheet/report/<int:report_id>')
@admin_required
def api_admin_get_timesheet_report(report_id):
    """Get single timesheet report details with daily entries."""
    try:
        if not timesheet_repository or not timesheet_repository.available:
            return jsonify({'success': False, 'message': 'База података није доступна'})

        report = timesheet_repository.get_report(report_id)
        if not report:
            return jsonify({'success': False, 'message': 'Извештај није пронађен'})

        return jsonify({'success': True, 'report': report})

    except Exception as e:
        return jsonify({'success': False, 'message': f'Грешка: {str(e)}'})


@app.route('/api/admin/timesheet/report/<int:report_id>/approve', methods=['POST'])
@admin_required
def api_admin_approve_timesheet_report(report_id):
    """Approve or disapprove a timesheet report."""
    try:
        if not timesheet_repository or not timesheet_repository.available:
            return jsonify({'success': False, 'message': 'База података није доступна'})

        data = request.get_json() or {}
        approve = data.get('approve', True)

        # Get admin info from session
        admin_email = session.get('email', 'Unknown Admin')

        import psycopg
        from psycopg.rows import dict_row

        with psycopg.connect(conninfo=os.environ.get('DATABASE_URL', '').replace('postgresql+psycopg://', 'postgresql://'), row_factory=dict_row) as conn:
            with conn.cursor() as cur:
                # Check if report exists
                cur.execute("SELECT id FROM timesheet_reports WHERE id = %s", (report_id,))
                if not cur.fetchone():
                    return jsonify({'success': False, 'message': 'Извештај није пронађен'})

                # Update verification status
                if approve:
                    cur.execute("""
                        UPDATE timesheet_reports
                        SET is_verified = TRUE,
                            verified_by = %s,
                            verified_at = NOW(),
                            is_locked = TRUE
                        WHERE id = %s
                    """, (admin_email, report_id))
                    message = 'Извештај је одобрен и закључан'
                else:
                    cur.execute("""
                        UPDATE timesheet_reports
                        SET is_verified = FALSE,
                            verified_by = NULL,
                            verified_at = NULL,
                            is_locked = FALSE
                        WHERE id = %s
                    """, (report_id,))
                    message = 'Верификација извештаја је повучена'

                conn.commit()

        return jsonify({'success': True, 'message': message})

    except Exception as e:
        return jsonify({'success': False, 'message': f'Грешка: {str(e)}'})


@app.route('/api/admin/timesheet/export/<int:report_id>')
@admin_required
def api_admin_export_timesheet_report(report_id):
    """Export timesheet report to Word document."""
    try:
        if not timesheet_repository or not timesheet_repository.available:
            flash('База података није доступна', 'error')
            return redirect(url_for('admin_timesheet_reports'))

        # Check if word export module exists
        try:
            from timesheet_word_export import generate_word_document
        except ImportError:
            flash('Word export модул није доступан. Користите PDF export.', 'warning')
            return redirect(url_for('admin_timesheet_reports'))

        # Generate Word document
        output_path = generate_word_document(report_id, os.environ.get('DATABASE_URL'))

        if not output_path or not os.path.exists(output_path):
            flash('Грешка при генерисању документа', 'error')
            return redirect(url_for('admin_timesheet_reports'))

        # Return file for download with proper headers
        from urllib.parse import quote

        filename = os.path.basename(output_path)
        # URL-encode the filename for Content-Disposition header
        encoded_filename = quote(filename)

        response = make_response(send_file(
            output_path,
            mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
        ))
        response.headers['Content-Disposition'] = f"attachment; filename*=UTF-8''{encoded_filename}"
        response.headers['Content-Type'] = 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
        response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '0'
        return response

    except Exception as e:
        flash(f'Грешка при експорту: {str(e)}', 'error')
        return redirect(url_for('admin_timesheet_reports'))


@app.route('/api/admin/timesheet/report/<int:report_id>', methods=['DELETE'])
@admin_required
def api_admin_delete_timesheet_report(report_id):
    """Delete a timesheet report and its entries."""
    try:
        if not timesheet_repository or not timesheet_repository.available:
            return jsonify({'success': False, 'message': 'База података није доступна'})

        import psycopg
        from psycopg.rows import dict_row

        with psycopg.connect(conninfo=os.environ.get('DATABASE_URL', '').replace('postgresql+psycopg://', 'postgresql://'), row_factory=dict_row) as conn:
            with conn.cursor() as cur:
                # Check if report exists
                cur.execute("SELECT id, employee_name, month, year FROM timesheet_reports WHERE id = %s", (report_id,))
                report = cur.fetchone()

                if not report:
                    return jsonify({'success': False, 'message': 'Извештај није пронађен'})

                # Delete related records first (foreign key constraints)
                cur.execute("DELETE FROM timesheet_entries WHERE report_id = %s", (report_id,))
                entries_deleted = cur.rowcount

                cur.execute("DELETE FROM timesheet_report_days WHERE report_id = %s", (report_id,))
                days_deleted = cur.rowcount

                # Delete report
                cur.execute("DELETE FROM timesheet_reports WHERE id = %s", (report_id,))

                conn.commit()

        return jsonify({
            'success': True,
            'message': f'Извештај је обрисан ({days_deleted} дана, {entries_deleted} уноса)'
        })

    except Exception as e:
        return jsonify({'success': False, 'message': f'Грешка: {str(e)}'})


@app.route('/admin/timesheet/pending/approve/<int:request_id>', methods=['POST'])
@admin_required
def admin_approve_edit_request(request_id):
    """Approve or reject an edit request."""
    try:
        if not timesheet_repository or not timesheet_repository.available:
            return jsonify({'success': False, 'message': 'База података није доступна'})

        data = request.get_json() or request.form.to_dict()
        action = data.get('action')  # 'approve' or 'reject'
        notes = data.get('notes', '').strip()

        if action not in ['approve', 'reject']:
            return jsonify({'success': False, 'message': 'Неважећа акција'})

        admin_email = session.get('email', 'Unknown Admin')
        status = 'approved' if action == 'approve' else 'rejected'

        import psycopg
        from psycopg.rows import dict_row

        with psycopg.connect(conninfo=os.environ.get('DATABASE_URL', '').replace('postgresql+psycopg://', 'postgresql://'), row_factory=dict_row) as conn:
            with conn.cursor() as cur:
                # Update request status
                cur.execute("""
                    UPDATE timesheet_edit_requests
                    SET status = %s,
                        processed_at = NOW(),
                        processed_by = %s,
                        notes = %s
                    WHERE id = %s
                """, (status, admin_email, notes, request_id))

                if cur.rowcount == 0:
                    return jsonify({'success': False, 'message': 'Захтев није пронађен'})

                # If approved, unlock the associated report
                if action == 'approve':
                    cur.execute("""
                        UPDATE timesheet_reports tr
                        SET is_locked = FALSE
                        FROM timesheet_edit_requests ter
                        WHERE ter.id = %s AND ter.report_id = tr.id
                    """, (request_id,))

                conn.commit()

        message = 'Захтев је одобрен' if action == 'approve' else 'Захтев је одбијен'
        return jsonify({'success': True, 'message': message})

    except Exception as e:
        return jsonify({'success': False, 'message': f'Грешка: {str(e)}'})


# ============================================================================
# EMPLOYEE TIMESHEET ENTRY SYSTEM (PostgreSQL Integration)
# ============================================================================

@app.route('/timesheet/entry')
@login_required
def timesheet_entry():
    """
    Employee timesheet entry page - Full working system integrated from localSQLtesting
    Converted from MySQL to PostgreSQL with complete functionality preservation
    """
    import psycopg
    from psycopg.rows import dict_row
    from serbian_holidays import SerbianHolidays
    from datetime import date

    user_role = session.get('user_role')

    # ALWAYS use current month and year for entry (no parameters)
    month = datetime.now().month
    year = datetime.now().year

    months = [(i, m) for i, m in enumerate([
        "", "Јануар", "Фебруар", "Март", "Април", "Мај", "Јун",
        "Јул", "Август", "Септембар", "Октобар", "Новембар", "Децембар"
    ], 0) if i > 0]

    current_year = datetime.now().year
    years = list(range(current_year - 2, current_year + 3))

    # Generate calendar data with weekend/holiday info
    serbian_holidays = SerbianHolidays()
    calendar_data = []

    # Get number of days in the month
    days_in_month = calendar.monthrange(year, month)[1]

    for day in range(1, days_in_month + 1):
        day_date = date(year, month, day)
        weekday = day_date.weekday()  # 0=Monday, 6=Sunday

        holiday_name = serbian_holidays.is_holiday(day_date)
        day_info = {
            'day': day,
            'weekday': weekday,
            'is_weekend': weekday >= 5,  # Saturday=5, Sunday=6
            'is_holiday': holiday_name is not None,
            'holiday_name': holiday_name or '',
            'day_name': ['Пон', 'Уто', 'Сре', 'Чет', 'Пет', 'Суб', 'Нед'][weekday]
        }
        calendar_data.append(day_info)

    # Try to load existing timesheet data for this month/year
    timesheet_data = None
    error_message = None

    user_full_name = session.get('user_name')  # Matches login session variable
    if user_full_name:
        try:
            pg_url = os.environ.get('DATABASE_URL', '').replace('postgresql+psycopg://', 'postgresql://')

            with psycopg.connect(pg_url, row_factory=dict_row) as conn:
                with conn.cursor() as cur:
                    # Get header data (try exact match first, then partial match)
                    cur.execute(
                        "SELECT id, employee_name, extraordinary_tasks, duties_summary, is_verified, is_locked, verified_by, verified_at FROM timesheet_reports WHERE employee_name = %s AND month = %s AND year = %s",
                        (user_full_name, month, year)
                    )
                    header = cur.fetchone()

                    # If exact match fails, try partial match (handle academic titles)
                    if not header:
                        cur.execute(
                            "SELECT id, employee_name, extraordinary_tasks, duties_summary, is_verified, is_locked, verified_by, verified_at FROM timesheet_reports WHERE employee_name LIKE %s AND month = %s AND year = %s",
                            (f"%{user_full_name}%", month, year)
                        )
                        header = cur.fetchone()

                    if header:
                        # Get daily data from timesheet_report_days table
                        cur.execute(
                            """SELECT day, work_in_museum, work_outside, vacation, public_holiday,
                                      paid_leave, other_leave, sick_leave_lt30, sick_leave_gte30
                               FROM timesheet_report_days WHERE report_id = %s ORDER BY day""",
                            (header['id'],)
                        )
                        daily_results = cur.fetchall()

                        # Format for template
                        daily_data = []
                        for row in daily_results:
                            daily_data.append({
                                'dan': row['day'],
                                'rad_na_mestu': row['work_in_museum'],
                                'van_muzeja': row['work_outside'],
                                'godisnji_odmor': row['vacation'],
                                'drzavni_praznik': row['public_holiday'],
                                'placeno_odsustvo': row['paid_leave'],
                                'ostalo_odsustvo': row['other_leave'],
                                'bolovanje_manje_30': row['sick_leave_lt30'],
                                'bolovanje_vece_30': row['sick_leave_gte30']
                            })

                        # Check for pending edit requests
                        report_id = header['id']
                        user_email = session.get('email', '')

                        cur.execute("""
                            SELECT id, status FROM timesheet_edit_requests
                            WHERE report_id = %s AND requester_email = %s
                            ORDER BY requested_at DESC LIMIT 1
                        """, (report_id, user_email))

                        edit_request = cur.fetchone()
                        has_pending_request_for_report = False
                        has_approved_request_for_report = False

                        if edit_request:
                            if edit_request['status'] == 'pending':
                                has_pending_request_for_report = True
                            elif edit_request['status'] == 'approved':
                                has_approved_request_for_report = True

                        timesheet_data = {
                            'exists': True,
                            'daily_data': daily_data,
                            'OPosao': (header.get('extraordinary_tasks') or header.get('duties_summary') or ''),
                            'is_verified': header.get('is_verified', False),
                            'is_locked': header.get('is_locked', False),
                            'verified_by': header.get('verified_by'),
                            'verified_at': header.get('verified_at'),
                            'has_pending_request': has_pending_request_for_report,
                            'has_approved_request': has_approved_request_for_report
                        }

        except Exception as e:
            error_message = f"Грешка при учитавању података: {str(e)}"
            logger.error(f"Timesheet load error: {e}")

    # Check if user can edit timesheet - Enhanced logic with approval status
    # TEMPORARILY DISABLED FOR TESTING - ALL RESTRICTIONS BYPASSED
    current_date = datetime.now()
    can_edit = True  # TESTING: Always allow editing
    edit_restriction_message = "⚠️ ТЕСТНИ РЕЖИМ: Сва временска ограничења су искључена"
    needs_approval = False
    is_approved = False
    has_approved_request = False
    has_pending_request = False

    # Get request status from timesheet_data if it exists
    if timesheet_data and timesheet_data.get('exists'):
        has_pending_request = timesheet_data.get('has_pending_request', False)
        has_approved_request = timesheet_data.get('has_approved_request', False)

    # Check if the timesheet is already verified
    if timesheet_data and timesheet_data.get('exists') and timesheet_data.get('is_verified'):
        is_approved = True

    # ORIGINAL LOGIC COMMENTED OUT FOR TESTING
    # Determine if this is current month or previous month
    # current_month = current_date.month
    # current_year = current_date.year
    # is_current_month = (month == current_month and year == current_year)
    # is_previous_month = (year < current_year) or (year == current_year and month < current_month)

    # # NEW LOGIC: If report is verified AND locked, it's locked (unless approved for edit)
    # if timesheet_data and timesheet_data.get('exists'):
    #     if timesheet_data.get('is_verified') and timesheet_data.get('is_locked'):
    #         if has_approved_request:
    #             # Admin approved edit request - allow editing
    #             can_edit = True
    #             needs_approval = False
    #             edit_restriction_message = "✅ Захтев за измену је одобрен - можете мењати податке"
    #         else:
    #             # Locked and no approval
    #             can_edit = False
    #             needs_approval = True
    #             edit_restriction_message = "🔒 Радна листа је верификована и закључана. Пошаљите захтев за измену."
    #     elif is_current_month:
    #         # Current month: Follow 1st-7th rule
    #         if current_date.day > 7:
    #             if has_approved_request:
    #                 can_edit = True
    #                 edit_restriction_message = "✅ Захтев за измену је одобрен"
    #             else:
    #                 can_edit = False
    #                 needs_approval = True
    #                 edit_restriction_message = f"Време за унос података је истекло (1-7. у месецу). Потребно је одобрење администратора за измене."
    #         else:
    #             can_edit = True
    #             edit_restriction_message = ""
    #     elif is_previous_month:
    #         # Previous month: Requires approval
    #         if has_approved_request:
    #             can_edit = True
    #             edit_restriction_message = "✅ Захтев за измену је одобрен"
    #         else:
    #             can_edit = False
    #             needs_approval = True
    #             edit_restriction_message = f"За мењање података из претходних месеци потребно је одобрење администратора."
    #     else:
    #         # Future month: Always allow editing
    #         can_edit = True
    # elif is_current_month:
    #     # No existing report, current month - follow 1st-7th rule
    #     if current_date.day > 7:
    #         can_edit = False
    #         needs_approval = True
    #         edit_restriction_message = f"Време за унос података је истекло (1-7. у месецу)"
    #     else:
    #         can_edit = True
    # elif is_previous_month:
    #     # No existing report, previous month - need approval
    #     can_edit = False
    #     needs_approval = True
    #     edit_restriction_message = f"За унос података из претходних месеци потребно је одобрење администратора"
    # else:
    #     # Future month - always allow
    #     can_edit = True

    # Get user department and position from PostgreSQL
    user_department = "Није дефинисано"
    user_position = "Није дефинисано"

    if user_full_name:
        try:
            pg_url = os.environ.get('DATABASE_URL', '').replace('postgresql+psycopg://', 'postgresql://')

            with psycopg.connect(pg_url, row_factory=dict_row) as conn:
                with conn.cursor() as cur:
                    # Get user info from users table with department join
                    cur.execute(
                        """SELECT u.position, d.name as department
                           FROM users u
                           LEFT JOIN departments d ON u.department_id = d.id
                           WHERE u.full_name = %s LIMIT 1""",
                        (user_full_name,)
                    )
                    user_info = cur.fetchone()

                    if user_info:
                        user_department = user_info['department'] or "Није дефинисано"
                        user_position = user_info['position'] or "Није дефинисано"

        except Exception as e:
            logger.warning(f"Could not load user department/position: {e}")

    # Ensure timesheet_data always has is_verified field
    if timesheet_data is None:
        timesheet_data = {'exists': False, 'is_verified': False}
    elif 'is_verified' not in timesheet_data:
        timesheet_data['is_verified'] = False

    # DEBUG: Log what's being passed to template
    logger.info(f"📊 DEBUG timesheet_data keys: {list(timesheet_data.keys()) if timesheet_data else 'None'}")
    if timesheet_data and 'OPosao' in timesheet_data:
        logger.info(f"📊 DEBUG OPosao value preview: {str(timesheet_data['OPosao'])[:100]}")
    else:
        logger.info(f"📊 DEBUG OPosao field is MISSING from timesheet_data!")

    response = make_response(render_template('employee_timesheet.html',
                          months=months, years=years,
                          selected_month=month, selected_year=year,
                          calendar_data=calendar_data,
                          timesheet_data=timesheet_data,
                          error_message=error_message,
                          user_department=user_department,
                          user_position=user_position,
                          can_edit=can_edit,
                          edit_restriction_message=edit_restriction_message,
                          needs_approval=needs_approval,
                          has_pending_request=has_pending_request,
                          is_approved=is_approved,
                          has_approved_request=has_approved_request,
                          is_entry_page=True))
    # Force browser to reload fresh content (for testing)
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response


@app.route('/timesheet/view')
@login_required
def timesheet_view():
    """
    Employee timesheet view page - View historical timesheet reports (read-only)
    """
    import psycopg
    from psycopg.rows import dict_row
    from serbian_holidays import SerbianHolidays
    from datetime import date

    user_role = session.get('user_role')

    # Handle month parameter - allow selection of any month
    month_param = request.args.get('month', '').strip()
    if month_param and month_param.isdigit():
        month = int(month_param)
    else:
        month = datetime.now().month

    # Handle year parameter - allow selection of any year
    year_param = request.args.get('year', '').strip()
    if year_param and year_param.isdigit():
        year = int(year_param)
    else:
        year = datetime.now().year

    months = [(i, m) for i, m in enumerate([
        "", "Јануар", "Фебруар", "Март", "Април", "Мај", "Јун",
        "Јул", "Август", "Септембар", "Октобар", "Новембар", "Децембар"
    ], 0) if i > 0]

    current_year = datetime.now().year
    years = list(range(current_year - 2, current_year + 3))

    # Generate calendar data with weekend/holiday info
    serbian_holidays = SerbianHolidays()
    calendar_data = []

    # Get number of days in the month
    days_in_month = calendar.monthrange(year, month)[1]

    for day in range(1, days_in_month + 1):
        day_date = date(year, month, day)
        weekday = day_date.weekday()  # 0=Monday, 6=Sunday

        holiday_name = serbian_holidays.is_holiday(day_date)
        day_info = {
            'day': day,
            'weekday': weekday,
            'is_weekend': weekday >= 5,  # Saturday=5, Sunday=6
            'is_holiday': holiday_name is not None,
            'holiday_name': holiday_name or '',
            'day_name': ['Пон', 'Уто', 'Сре', 'Чет', 'Пет', 'Суб', 'Нед'][weekday]
        }
        calendar_data.append(day_info)

    # Try to load existing timesheet data for this month/year
    timesheet_data = None
    error_message = None

    user_full_name = session.get('user_name')
    if user_full_name:
        try:
            pg_url = os.environ.get('DATABASE_URL', '').replace('postgresql+psycopg://', 'postgresql://')

            with psycopg.connect(pg_url, row_factory=dict_row) as conn:
                with conn.cursor() as cur:
                    # Get header data
                    cur.execute(
                        "SELECT id, employee_name, extraordinary_tasks, duties_summary, is_verified, is_locked, verified_by, verified_at FROM timesheet_reports WHERE employee_name = %s AND month = %s AND year = %s",
                        (user_full_name, month, year)
                    )
                    header = cur.fetchone()

                    # If exact match fails, try partial match
                    if not header:
                        cur.execute(
                            "SELECT id, employee_name, extraordinary_tasks, duties_summary, is_verified, is_locked, verified_by, verified_at FROM timesheet_reports WHERE employee_name LIKE %s AND month = %s AND year = %s",
                            (f"%{user_full_name}%", month, year)
                        )
                        header = cur.fetchone()

                    if header:
                        # Get daily data
                        cur.execute(
                            """SELECT day, work_in_museum, work_outside, vacation, public_holiday,
                                      paid_leave, other_leave, sick_leave_lt30, sick_leave_gte30
                               FROM timesheet_report_days WHERE report_id = %s ORDER BY day""",
                            (header['id'],)
                        )
                        daily_results = cur.fetchall()

                        # Format for template
                        daily_data = []
                        for row in daily_results:
                            daily_data.append({
                                'dan': row['day'],
                                'rad_na_mestu': row['work_in_museum'],
                                'van_muzeja': row['work_outside'],
                                'godisnji_odmor': row['vacation'],
                                'drzavni_praznik': row['public_holiday'],
                                'placeno_odsustvo': row['paid_leave'],
                                'ostalo_odsustvo': row['other_leave'],
                                'bolovanje_manje_30': row['sick_leave_lt30'],
                                'bolovanje_vece_30': row['sick_leave_gte30']
                            })

                        timesheet_data = {
                            'exists': True,
                            'OPosao': (header.get('extraordinary_tasks') or header.get('duties_summary') or ''),
                            'daily_data': daily_data,
                            'is_verified': header.get('is_verified', False),
                            'is_locked': header.get('is_locked', False),
                            'verified_by': header.get('verified_by'),
                            'verified_at': header.get('verified_at')
                        }
        except Exception as e:
            error_message = f"Грешка при учитавању података: {str(e)}"
            logger.error(f"Timesheet load error: {e}")

    # Get employee info
    user_department = "Непознато"
    user_position = "Непознато"
    user_email = session.get('user_email')
    if user_email:
        try:
            pg_url = os.environ.get('DATABASE_URL', '').replace('postgresql+psycopg://', 'postgresql://')
            with psycopg.connect(pg_url, row_factory=dict_row) as conn:
                with conn.cursor() as cur:
                    cur.execute("SELECT department, position FROM employee_profiles WHERE email = %s", (user_email,))
                    emp = cur.fetchone()
                    if emp:
                        user_department = emp.get('department', 'Непознато')
                        user_position = emp.get('position', 'Непознато')
        except Exception as e:
            logger.error(f"Error fetching employee info: {e}")

    # VIEW MODE - Always read-only
    can_edit = False
    edit_restriction_message = "Преглед ранијих радних листа (само читање)"

    if timesheet_data is None:
        timesheet_data = {'exists': False, 'is_verified': False}
    elif 'is_verified' not in timesheet_data:
        timesheet_data['is_verified'] = False

    response = make_response(render_template('employee_timesheet.html',
                          months=months, years=years,
                          selected_month=month, selected_year=year,
                          calendar_data=calendar_data,
                          timesheet_data=timesheet_data,
                          error_message=error_message,
                          user_department=user_department,
                          user_position=user_position,
                          can_edit=can_edit,
                          edit_restriction_message=edit_restriction_message,
                          needs_approval=False,
                          has_pending_request=False,
                          is_approved=False,
                          has_approved_request=False,
                          is_entry_page=False))
    # Force browser to reload fresh content
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response


@app.route('/api/timesheet/load')
@login_required
def api_load_timesheet():
    """
    API endpoint to load existing timesheet data for a given month/year
    Returns JSON with daily timesheet data
    """
    import psycopg
    from psycopg.rows import dict_row

    month = int(request.args.get('month', 0))
    year = int(request.args.get('year', 0))
    user_full_name = session.get('user_name')

    if not user_full_name:
        return jsonify({'success': False, 'message': 'Није пријављен'})

    try:
        pg_url = os.environ.get('DATABASE_URL', '').replace('postgresql+psycopg://', 'postgresql://')

        with psycopg.connect(pg_url, row_factory=dict_row) as conn:
            with conn.cursor() as cur:
                # Get header
                cur.execute(
                    "SELECT id, extraordinary_tasks, duties_summary FROM timesheet_reports WHERE employee_name = %s AND month = %s AND year = %s",
                    (user_full_name, month, year)
                )
                header = cur.fetchone()

                if not header:
                    return jsonify({'success': True, 'exists': False, 'daily_data': {}})

                # Get daily data from timesheet_report_days
                cur.execute(
                    """SELECT day, work_in_museum, work_outside, vacation, public_holiday,
                              paid_leave, other_leave, sick_leave_lt30, sick_leave_gte30
                       FROM timesheet_report_days WHERE report_id = %s ORDER BY day""",
                    (header['id'],)
                )
                daily_results = cur.fetchall()

                # Format daily data
                daily_data = {}
                for row in daily_results:
                    daily_data[str(row['day'])] = {
                        'rad_na_mestu': float(row['work_in_museum'] or 0),
                        'van_muzeja': float(row['work_outside'] or 0),
                        'godisnji_odmor': float(row['vacation'] or 0),
                        'drzavni_praznik': float(row['public_holiday'] or 0),
                        'placeno_odsustvo': float(row['paid_leave'] or 0),
                        'ostalo_odsustvo': float(row['other_leave'] or 0),
                        'bolovanje_manje_30': float(row['sick_leave_lt30'] or 0),
                        'bolovanje_vece_30': float(row['sick_leave_gte30'] or 0)
                    }

                return jsonify({
                    'success': True,
                    'exists': True,
                    'daily_data': daily_data,
                    'obavljeni_poslovi': (header.get('extraordinary_tasks') or header.get('duties_summary') or '')
                })
    except Exception as e:
        logger.error(f"API load timesheet error: {e}")
        return jsonify({'success': False, 'message': str(e)})


@app.route('/request_approval', methods=['POST'])
@login_required
def request_approval():
    """
    Employee requests approval to edit a locked/verified timesheet.
    Creates an entry in timesheet_edit_requests table.
    """
    try:
        # Get form data
        month = request.form.get('month')
        year = request.form.get('year')
        reason = request.form.get('reason', '').strip()

        if not month or not year or not reason:
            return jsonify({
                'success': False,
                'message': 'Месец, година и разлог су обавезни!'
            })

        # Get user info
        user_email = session.get('email')
        user_name = session.get('full_name', 'Unknown')

        if not user_email:
            return jsonify({
                'success': False,
                'message': 'Корисник није пријављен'
            })

        import psycopg
        from psycopg.rows import dict_row

        with psycopg.connect(conninfo=os.environ.get('DATABASE_URL', '').replace('postgresql+psycopg://', 'postgresql://'), row_factory=dict_row) as conn:
            with conn.cursor() as cur:
                # Find the report for this month/year and employee
                cur.execute("""
                    SELECT id, is_verified, is_locked
                    FROM timesheet_reports
                    WHERE employee_name = %s
                      AND month = %s
                      AND year = %s
                    ORDER BY id DESC
                    LIMIT 1
                """, (user_name, month, year))

                report = cur.fetchone()

                if not report:
                    # Create a new empty report for this request
                    cur.execute("""
                        INSERT INTO timesheet_reports
                        (employee_name, month, year, organization_unit, position, is_verified, is_locked, created_at)
                        VALUES (%s, %s, %s, %s, %s, FALSE, FALSE, NOW())
                        RETURNING id
                    """, (user_name, month, year, 'Природњачки музеј', session.get('position', 'Запослени')))
                    report = cur.fetchone()
                    conn.commit()

                report_id = report['id']

                # Check if there's already a pending request
                cur.execute("""
                    SELECT id, status
                    FROM timesheet_edit_requests
                    WHERE report_id = %s
                      AND requester_email = %s
                      AND status = 'pending'
                """, (report_id, user_email))

                existing_request = cur.fetchone()

                if existing_request:
                    return jsonify({
                        'success': False,
                        'message': 'Већ постоји захтев на чекању за овај месец'
                    })

                # Create new edit request
                cur.execute("""
                    INSERT INTO timesheet_edit_requests
                    (report_id, requester_email, reason, status, requested_at)
                    VALUES (%s, %s, %s, 'pending', NOW())
                    RETURNING id
                """, (report_id, user_email, reason))

                request_id = cur.fetchone()['id']
                conn.commit()

        return jsonify({
            'success': True,
            'message': f'Захтев је успешно послат! (ID: {request_id})\nБићете обавештени када администратор обради захтев.'
        })

    except Exception as e:
        logger.error(f"Error submitting edit request: {e}")
        return jsonify({
            'success': False,
            'message': f'Грешка при слању захтева: {str(e)}'
        })


@app.route('/api/timesheet/save', methods=['POST'])
@login_required
def api_save_timesheet():
    """
    API endpoint to save timesheet data to PostgreSQL
    Saves to timesheet_reports and timesheet_entries tables
    """
    import psycopg
    from psycopg.rows import dict_row

    try:
        data = request.get_json()
        month = data.get('month')
        year = data.get('year')
        daily_data = data.get('daily_data', {})
        work_description = data.get('obavljeni_poslovi', '')  # Template uses obavljeni_poslovi

        if not month or not year:
            return jsonify({'success': False, 'message': 'Недостају подаци'})

        user_full_name = session.get('user_name')
        user_email = session.get('user_email')

        if not user_full_name:
            return jsonify({'success': False, 'message': 'Није пријављен'})

        pg_url = os.environ.get('DATABASE_URL', '').replace('postgresql+psycopg://', 'postgresql://')

        with psycopg.connect(pg_url) as conn:
            with conn.cursor() as cur:
                # Check if exists
                cur.execute(
                    "SELECT id FROM timesheet_reports WHERE employee_name = %s AND month = %s AND year = %s",
                    (user_full_name, month, year)
                )
                existing = cur.fetchone()

                if existing:
                    report_id = existing[0]

                    # Update existing report
                    cur.execute(
                        "UPDATE timesheet_reports SET extraordinary_tasks = %s WHERE id = %s",
                        (work_description, report_id)
                    )
                    # Delete existing days - make sure to commit this before insert
                    cur.execute("DELETE FROM timesheet_report_days WHERE report_id = %s", (report_id,))
                    conn.commit()  # Commit the DELETE immediately
                else:
                    # Create new report
                    cur.execute(
                        """INSERT INTO timesheet_reports
                           (employee_name, month, year, extraordinary_tasks)
                           VALUES (%s, %s, %s, %s)
                           RETURNING id""",
                        (user_full_name, month, year, work_description)
                    )
                    report_id = cur.fetchone()[0]

                # Insert daily data (batch) - using UPSERT to avoid duplicates
                if daily_data:
                    insert_data = []
                    for day_str, day_data in daily_data.items():
                        try:
                            day = int(day_str)
                            if any(day_data.values()):
                                insert_data.append((
                                    report_id, day,
                                    day_data.get('rad_na_mestu', 0) or 0,
                                    day_data.get('van_muzeja', 0) or 0,
                                    day_data.get('godisnji_odmor', 0) or 0,
                                    day_data.get('drzavni_praznik', 0) or 0,
                                    day_data.get('placeno_odsustvo', 0) or 0,
                                    day_data.get('ostalo_odsustvo', 0) or 0,
                                    day_data.get('bolovanje_manje_30', 0) or 0,
                                    day_data.get('bolovanje_vece_30', 0) or 0
                                ))
                        except ValueError:
                            continue

                    if insert_data:
                        cur.executemany(
                            """INSERT INTO timesheet_report_days
                               (report_id, day, work_in_museum, work_outside, vacation,
                                public_holiday, paid_leave, other_leave,
                                sick_leave_lt30, sick_leave_gte30)
                               VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                               ON CONFLICT (report_id, day)
                               DO UPDATE SET
                                   work_in_museum = EXCLUDED.work_in_museum,
                                   work_outside = EXCLUDED.work_outside,
                                   vacation = EXCLUDED.vacation,
                                   public_holiday = EXCLUDED.public_holiday,
                                   paid_leave = EXCLUDED.paid_leave,
                                   other_leave = EXCLUDED.other_leave,
                                   sick_leave_lt30 = EXCLUDED.sick_leave_lt30,
                                   sick_leave_gte30 = EXCLUDED.sick_leave_gte30""",
                            insert_data
                        )

                conn.commit()
                return jsonify({'success': True, 'message': 'Сачувано'})

    except Exception as e:
        logger.error(f"API save timesheet error: {e}")
        return jsonify({'success': False, 'message': str(e)})


@app.route('/mineral_database')
@login_required
def mineral_database_app():
    """Route to mineral database - redirects to admin mineral collection."""
    user_email = session.get('user_email')
    user_role = session.get('user_role')

    if not user_has_module_access(user_email, user_role, 'mineral_database'):
        flash('Немате дозволу за приступ бази минерала.', 'error')
        return redirect(url_for('dashboard'))

    # Redirect to integrated mineral collection
    return redirect(url_for('admin_mineral_collection'))

@app.route('/admin')
@admin_required
def admin_panel():
    """Admin panel."""
    return render_template('admin_panel.html')

@app.route('/admin/statistics')
@admin_required
def admin_statistics():
    """Collection statistics dashboard."""
    try:
        # Get mineral database statistics
        mineral_db = get_mineral_database()
        mineral_stats = mineral_db.get_statistics() if mineral_db.available else {}
        rruff_stats = mineral_db.get_rruff_statistics() if mineral_db.available else {}

        # Count mock collection specimens
        meteorite_count = len(get_meteorite_collection_database()['specimens'])
        botany_count = len(BOTANY_COLLECTION_DATABASE['specimens'])
        paleozoology_count = len(PALEOZOOLOGY_COLLECTION_DATABASE['specimens'])
        paleobotany_count = len(PALEOBOTANY_COLLECTION_DATABASE['specimens'])
        geology_count = len(PETROLOGY_COLLECTION_DATABASE['specimens'])
        heritage_count = len(get_cultural_heritage_database().get('heritage_items', []))

        # Calculate total specimens across all collections
        total_specimens = (
            mineral_stats.get('total_minerals', 0) +
            meteorite_count +
            botany_count +
            paleozoology_count +
            paleobotany_count +
            geology_count +
            heritage_count
        )

        # Get image storage statistics
        image_storage = get_image_storage()
        image_metadata = image_storage.metadata if image_storage else {'images': []}
        total_images = len(image_metadata.get('images', []))

        # Count specimens with images
        specimens_with_images = len(set(
            img.get('entity_id') for img in image_metadata.get('images', [])
            if img.get('entity_id')
        ))

        # Calculate image coverage percentage
        image_coverage = (specimens_with_images / total_specimens * 100) if total_specimens > 0 else 0

        # Recent additions (last 30 days) - for now using mock data
        from datetime import datetime, timedelta
        thirty_days_ago = datetime.now() - timedelta(days=30)
        recent_additions = 12  # Mock value - would need created_at dates in collections

        # Prepare statistics data
        stats = {
            'total_specimens': total_specimens,
            'total_images': total_images,
            'specimens_with_images': specimens_with_images,
            'image_coverage': round(image_coverage, 1),
            'recent_additions': recent_additions,
            'collections': {
                'minerals': {
                    'name': 'Минералошка збирка',
                    'count': mineral_stats.get('total_minerals', 0),
                    'icon': 'bi-gem',
                    'color': 'primary',
                    'url': '/admin/mineral_collection'
                },
                'meteorites': {
                    'name': 'Метеорити',
                    'count': meteorite_count,
                    'icon': 'bi-moon-stars',
                    'color': 'warning',
                    'url': '/admin/collection_database/meteorites'
                },
                'botany': {
                    'name': 'Ботаника',
                    'count': botany_count,
                    'icon': 'bi-flower3',
                    'color': 'success',
                    'url': '/admin/collection_database/botany'
                },
                'paleozoology': {
                    'name': 'Палеозоологија',
                    'count': paleozoology_count,
                    'icon': 'bi-bones',
                    'color': 'secondary',
                    'url': '/admin/collection_database/paleozoology'
                },
                'paleobotany': {
                    'name': 'Палеоботаника',
                    'count': paleobotany_count,
                    'icon': 'bi-tree',
                    'color': 'info',
                    'url': '/admin/collection_database/paleobotany'
                },
                'geology': {
                    'name': 'Геологија',
                    'count': geology_count,
                    'icon': 'bi-hexagon',
                    'color': 'dark',
                    'url': '/admin/collection_database/geology'
                },
                'heritage': {
                    'name': 'Културно наслеђе',
                    'count': heritage_count,
                    'icon': 'bi-bank',
                    'color': 'danger',
                    'url': '/admin/collection_database/cultural_heritage'
                }
            },
            'mineral_details': {
                'with_inventory': mineral_stats.get('with_inventory', 0),
                'with_locality': mineral_stats.get('with_locality', 0),
                'top_localities': mineral_stats.get('top_localities', [])[:5]
            },
            'rruff_details': {
                'total': rruff_stats.get('total_minerals', 0),
                'by_crystal_system': rruff_stats.get('by_crystal_system', [])[:7]
            }
        }

        return render_template('admin_statistics.html', stats=stats)

    except Exception as e:
        logging.error(f"Error generating statistics: {e}")
        flash('Грешка при учитавању статистике.', 'error')
        return redirect(url_for('admin_panel'))

@app.route('/admin/qr_generator')
@admin_required
def admin_qr_generator():
    """QR code generation interface."""
    collections = [
        {'id': 'minerals', 'name': 'Минералошка збирка', 'prefix': 'M', 'url': '/admin/mineral_collection'},
        {'id': 'meteorites', 'name': 'Метеорити', 'prefix': 'MET', 'url': '/admin/meteorite_collection'},
        {'id': 'botany', 'name': 'Ботаника', 'prefix': 'BOT', 'url': '/admin/botany_collection'},
        {'id': 'paleozoology', 'name': 'Палеозоологија', 'prefix': 'PAL', 'url': '/admin/paleozoology_collection'},
        {'id': 'paleobotany', 'name': 'Палеоботаника', 'prefix': 'PBOT', 'url': '/admin/paleobotany_collection'},
        {'id': 'geology', 'name': 'Геологија', 'prefix': 'GEO', 'url': '/admin/petrology_collection'},
        {'id': 'heritage', 'name': 'Културно наслеђе', 'prefix': 'CH', 'url': '/admin/cultural_heritage_database'}
    ]
    return render_template('admin_qr_generator.html', collections=collections)

@app.route('/admin/qr_field_selection/<collection_type>', methods=['GET'])
@admin_required
def admin_qr_field_selection(collection_type):
    """Field selection interface for QR code generation."""
    # Define available fields per collection type
    field_definitions = {
        'meteorites': [
            {'id': 'catalog_number', 'label': 'Каталошки број', 'default': True, 'description': 'Идентификациони број примерка'},
            {'id': 'meteorite_name', 'label': 'Назив метеорита', 'default': True, 'description': 'Службени назив метеорита'},
            {'id': 'classification', 'label': 'Класификација', 'default': True, 'description': 'Научна класификација'},
            {'id': 'fall_type', 'label': 'Тип пада', 'default': True, 'description': 'Пад или налаз'},
            {'id': 'fall_date', 'label': 'Датум пада', 'default': True, 'description': 'Када је пао метеорит'},
            {'id': 'location_found', 'label': 'Локација налаза', 'default': True, 'description': 'Где је пронађен'},
            {'id': 'total_mass_kg', 'label': 'Укупна маса (kg)', 'default': False, 'description': 'Тежина у килограмима'},
            {'id': 'specimen_mass', 'label': 'Маса примерка', 'default': False, 'description': 'Маса овог примерка'},
            {'id': 'description', 'label': 'Опис', 'default': False, 'description': 'Детаљан опис примерка'},
            {'id': 'source', 'label': 'Извор', 'default': False, 'description': 'Како је примерак набављен'},
            {'id': 'curator', 'label': 'Кустос', 'default': False, 'description': 'Одговорно лице'},
        ],
        'botany': [
            {'id': 'catalog_number', 'label': 'Каталошки број', 'default': True},
            {'id': 'scientific_name', 'label': 'Научно име', 'default': True},
            {'id': 'common_name_sr', 'label': 'Народно име', 'default': True},
            {'id': 'family', 'label': 'Фамилија', 'default': True},
            {'id': 'habitat', 'label': 'Станиште', 'default': True},
            {'id': 'location_found', 'label': 'Локација', 'default': False},
            {'id': 'date_collected', 'label': 'Датум прикупљања', 'default': False},
            {'id': 'collector', 'label': 'Сакупљач', 'default': False},
            {'id': 'conservation_status', 'label': 'Статус заштите', 'default': False},
            {'id': 'description', 'label': 'Опис', 'default': False},
        ],
        'paleozoology': [
            {'id': 'catalog_number', 'label': 'Каталошки број', 'default': True},
            {'id': 'scientific_name', 'label': 'Научно име', 'default': True},
            {'id': 'common_name_sr', 'label': 'Народно име', 'default': True},
            {'id': 'geological_period', 'label': 'Геолошки период', 'default': True},
            {'id': 'age_million_years', 'label': 'Старост (мил. год.)', 'default': True},
            {'id': 'location_found', 'label': 'Локација налаза', 'default': True},
            {'id': 'class', 'label': 'Класа', 'default': False},
            {'id': 'order', 'label': 'Ред', 'default': False},
            {'id': 'family', 'label': 'Фамилија', 'default': False},
            {'id': 'description', 'label': 'Опис', 'default': False},
        ]
    }

    collection_names = {
        'meteorites': 'Збирка метеорита',
        'botany': 'Ботаничка збирка',
        'paleozoology': 'Палеозоолошка збирка'
    }

    # Get available fields for this collection
    available_fields = field_definitions.get(collection_type, [])
    collection_name = collection_names.get(collection_type, collection_type)

    return render_template('admin_qr_field_selection.html',
                          collection_type=collection_type,
                          collection_name=collection_name,
                          available_fields=available_fields)

@app.route('/admin/qr_labels_with_fields/<collection_type>', methods=['POST'])
@admin_required
def admin_qr_labels_with_fields(collection_type):
    """Generate QR codes with custom field selection."""
    import qrcode
    from io import BytesIO
    import base64

    # Get form data
    selected_fields = request.form.getlist('selected_fields')
    display_mode = request.form.get('display_mode', 'card')
    show_image = 'show_image' in request.form
    action = request.form.get('action', 'generate_all')

    # Store configuration in session for QR view
    session['qr_config'] = {
        'fields': selected_fields,
        'display_mode': display_mode,
        'show_image': show_image
    }

    base_url = "http://192.168.144.48"
    labels = []

    # Encode selected fields for URL
    fields_param = ','.join(selected_fields) if selected_fields else 'all'

    try:
        if collection_type == 'meteorites':
            for specimen in get_meteorite_collection_database()['specimens'][:100]:
                catalog_num = specimen.get('catalog_number', 'N/A')
                # New QR view route with field parameters
                qr_url = f"{base_url}/qr_view/{collection_type}/{catalog_num}?fields={fields_param}&mode={display_mode}&img={1 if show_image else 0}"

                qr = qrcode.QRCode(version=1, box_size=10, border=2)
                qr.add_data(qr_url)
                qr.make(fit=True)
                img = qr.make_image(fill_color="black", back_color="white")

                buffered = BytesIO()
                img.save(buffered, format="PNG")
                img_str = base64.b64encode(buffered.getvalue()).decode()

                labels.append({
                    'catalog_number': catalog_num,
                    'name': specimen.get('meteorite_name', 'Непознато'),
                    'qr_code': img_str,
                    'url': qr_url
                })

        elif collection_type == 'botany':
            for specimen in BOTANY_COLLECTION_DATABASE['specimens'][:100]:
                catalog_num = specimen.get('catalog_number', 'N/A')
                qr_url = f"{base_url}/qr_view/{collection_type}/{catalog_num}?fields={fields_param}&mode={display_mode}&img={1 if show_image else 0}"

                qr = qrcode.QRCode(version=1, box_size=10, border=2)
                qr.add_data(qr_url)
                qr.make(fit=True)
                img = qr.make_image(fill_color="black", back_color="white")

                buffered = BytesIO()
                img.save(buffered, format="PNG")
                img_str = base64.b64encode(buffered.getvalue()).decode()

                labels.append({
                    'catalog_number': catalog_num,
                    'name': specimen.get('scientific_name', 'Непознато'),
                    'qr_code': img_str,
                    'url': qr_url
                })

        elif collection_type == 'paleozoology':
            for specimen in PALEOZOOLOGY_COLLECTION_DATABASE['specimens'][:100]:
                catalog_num = specimen.get('catalog_number', 'N/A')
                qr_url = f"{base_url}/qr_view/{collection_type}/{catalog_num}?fields={fields_param}&mode={display_mode}&img={1 if show_image else 0}"

                qr = qrcode.QRCode(version=1, box_size=10, border=2)
                qr.add_data(qr_url)
                qr.make(fit=True)
                img = qr.make_image(fill_color="black", back_color="white")

                buffered = BytesIO()
                img.save(buffered, format="PNG")
                img_str = base64.b64encode(buffered.getvalue()).decode()

                labels.append({
                    'catalog_number': catalog_num,
                    'name': specimen.get('scientific_name', 'Непознато'),
                    'qr_code': img_str,
                    'url': qr_url
                })

        collection_names = {
            'meteorites': 'Збирка метеорита',
            'botany': 'Ботаничка збирка',
            'paleozoology': 'Палеозоолошка збирка'
        }

        collection_info = {
            'type': collection_type,
            'name': collection_names.get(collection_type, collection_type),
            'count': len(labels)
        }

        # Store the generated data in session for format selection
        session['qr_generated_data'] = {
            'labels': labels,
            'collection_info': collection_info,
            'fields': selected_fields,
            'display_mode': display_mode,
            'show_image': show_image
        }
        
        # Redirect to format selection
        return redirect(url_for('admin_qr_label_format', collection_type=collection_type))

    except Exception as e:
        logging.error(f"Error generating QR codes with fields: {e}")
        flash(f'Грешка при генерисању QR кодова: {str(e)}', 'error')
        return redirect(url_for('admin_qr_field_selection', collection_type=collection_type))

# Box-based QR Code System for Minerals
@app.route('/admin/qr_boxes/minerals', methods=['GET'])
@admin_required
def admin_qr_mineral_boxes():
    """Select mineral storage boxes for QR code generation."""
    mineral_db = get_mineral_database()

    if not mineral_db or not mineral_db.available:
        flash('База минерала није доступна.', 'error')
        return redirect(url_for('admin_qr_generator'))

    # Get all minerals and group by location (box)
    result = mineral_db.get_all_minerals(page=1, per_page=10000)
    if not result or 'minerals' not in result:
        flash('Грешка при учитавању минерала.', 'error')
        return redirect(url_for('admin_qr_generator'))

    minerals = result['minerals']

    # Group minerals by box location
    boxes = {}
    no_location_count = 0

    for mineral in minerals:
        location = mineral.get('gde_se_nalazi')
        if location and str(location).strip() != '':
            location = str(location).strip()
            if location not in boxes:
                boxes[location] = {
                    'box_number': location,
                    'minerals': [],
                    'count': 0
                }
            boxes[location]['minerals'].append(mineral)
            boxes[location]['count'] += 1
        else:
            no_location_count += 1

    # Custom sorting: single numbers first (ascending), then multi-numbers (ascending)
    def sort_box_key(box):
        box_num = box['box_number']

        # Check if it contains comma (multiple numbers)
        has_comma = ',' in box_num

        # Try to extract numeric value for sorting
        try:
            # For single numbers, extract the number
            if not has_comma and box_num.strip().isdigit():
                return (0, int(box_num.strip()), box_num)
            else:
                # For multi-numbers or text, sort alphabetically but after single numbers
                return (1, 999999, box_num.lower())
        except:
            # If can't parse, put at the end
            return (2, 999999, box_num.lower())

    box_list = sorted(boxes.values(), key=sort_box_key)

    return render_template('admin_qr_mineral_boxes.html',
                          boxes=box_list,
                          total_boxes=len(box_list),
                          no_location_count=no_location_count,
                          total_minerals=len(minerals))

@app.route('/admin/qr_boxes/minerals/generate', methods=['POST'])
@admin_required
def admin_generate_box_qr_codes():
    """Generate QR codes for selected mineral boxes."""
    import qrcode
    from io import BytesIO
    import base64

    selected_boxes = request.form.getlist('selected_boxes')

    if not selected_boxes:
        flash('Морате изабрати бар једну кутију.', 'warning')
        return redirect(url_for('admin_qr_mineral_boxes'))

    # Limit the number of boxes to prevent server overload  
    if len(selected_boxes) > 10:  # 10 boxes maximum - balanced limit
        flash('Можете изабрати максимум 10 кутија одједном.', 'warning')
        return redirect(url_for('admin_qr_mineral_boxes'))
    
    logging.info(f"Starting QR generation for {len(selected_boxes)} boxes")

    # Ultra-simple approach - no batching, no complex processing
    base_url = "http://192.168.144.48"
    labels = []

    try:
        # Generate QR codes one by one with minimal processing
        for box_number in selected_boxes:
            try:
                # Generate QR code URL
                from urllib.parse import quote
                qr_url = f"{base_url}/qr_box/minerals/{quote(box_number)}"

                # Create minimal QR code
                qr = qrcode.QRCode(version=1, box_size=1, border=0)
                qr.add_data(qr_url)
                qr.make(fit=True)
                
                # Create image with minimal settings
                img = qr.make_image(fill_color="black", back_color="white")
                
                # Convert to base64
                buffered = BytesIO()
                img.save(buffered, format="PNG")
                img_str = base64.b64encode(buffered.getvalue()).decode()

                # Add to labels
                labels.append({
                    'catalog_number': box_number,
                    'name': 'Кутија',
                    'qr_code': img_str,
                    'url': qr_url,
                    'count': 0
                })
                
                logging.info(f"Generated QR for box {box_number}")
                
            except Exception as box_error:
                logging.error(f"Error generating QR for box {box_number}: {box_error}")
                # Create a placeholder even if QR generation fails
                labels.append({
                    'catalog_number': box_number,
                    'name': 'Кутија (Грешка)',
                    'qr_code': '',
                    'url': f"{base_url}/qr_box/minerals/{box_number}",
                    'count': 0
                })
                continue

    except Exception as e:
        logging.error(f"Error generating QR codes for boxes: {e}")
        # Even if QR generation fails, try to go through format selection with empty labels
        labels = []
        for box_number in selected_boxes:
            labels.append({
                'catalog_number': box_number,
                'name': 'Кутија (Грешка)',
                'qr_code': '',
                'url': f"{base_url}/qr_box/minerals/{box_number}",
                'count': 0
            })
        
        collection_info = {
            'type': 'mineral_boxes',
            'name': 'Кутије минералошке збирке',
            'count': len(labels)
        }

        session['qr_generated_data'] = {
            'labels': labels,
            'collection_info': collection_info,
            'selected_boxes': selected_boxes,
            'is_box_mode': True
        }
        
        flash(f'Грешка при генерисању QR кодова, али можете изабрати формат: {str(e)}', 'warning')
        return redirect(url_for('admin_qr_label_format', collection_type='mineral_boxes'))

    logging.info(f"Successfully generated {len(labels)} QR codes")
    
    if len(labels) == 0:
        flash('Није генерисан ниједан QR код.', 'error')
        return redirect(url_for('admin_qr_mineral_boxes'))
    
    collection_info = {
        'type': 'mineral_boxes',
        'name': 'Кутије минералошке збирке',
        'count': len(labels)
    }

    # Store the generated data in session for format selection
    session['qr_generated_data'] = {
        'labels': labels,
        'collection_info': collection_info,
        'selected_boxes': selected_boxes,
        'is_box_mode': True
    }
    
    logging.info(f"Stored {len(labels)} labels in session, redirecting to format selection")
    
    # Redirect to format selection
    return redirect(url_for('admin_qr_label_format', collection_type='mineral_boxes'))


# Public route for box contents (no auth required)
@app.route('/qr_box/minerals/<box_number>')
def qr_view_mineral_box(box_number):
    """Public mobile-optimized view for mineral box contents."""
    from datetime import datetime
    from urllib.parse import unquote

    box_number = unquote(box_number)

    mineral_db = get_mineral_database()
    if not mineral_db or not mineral_db.available:
        return render_template('error.html',
                             error_title='Грешка',
                             error_message='База минерала није доступна.'), 500

    # Get all minerals
    result = mineral_db.get_all_minerals(page=1, per_page=10000)
    if not result or 'minerals' not in result:
        return render_template('error.html',
                             error_title='Грешка',
                             error_message='Грешка при учитавању минерала.'), 500

    # Filter minerals for this box
    box_minerals = []
    for mineral in result['minerals']:
        location = mineral.get('gde_se_nalazi')
        if location and str(location).strip() == box_number:
            box_minerals.append(mineral)

    if not box_minerals:
        return render_template('error.html',
                             error_title='Кутија није пронађена',
                             error_message=f'Кутија "{box_number}" није пронађена или је празна.'), 404

    return render_template('mineral_box_qr_view.html',
                          box_number=box_number,
                          minerals=box_minerals,
                          total_minerals=len(box_minerals),
                          scan_time=datetime.now().strftime('%d.%m.%Y %H:%M'))

@app.route('/admin/qr_select/<collection_type>', methods=['GET'])
@admin_required
def admin_qr_select_specimens(collection_type):
    """Specimen selection interface with filters."""
    collection_names = {
        'minerals': 'Минералошка збирка',
        'meteorites': 'Метеорити',
        'botany': 'Ботаника',
        'paleozoology': 'Палеозоологија',
        'paleobotany': 'Палеоботаника',
        'geology': 'Геологија',
        'heritage': 'Културно наслеђе'
    }

    collection_info = {
        'type': collection_type,
        'name': collection_names.get(collection_type, collection_type)
    }

    specimens = []

    try:
        if collection_type == 'minerals':
            # Get filters from request
            inv_from = request.args.get('inv_from', type=int)
            inv_to = request.args.get('inv_to', type=int)
            location = request.args.get('location', '')
            locality = request.args.get('locality', '')

            # Get all minerals and filter
            mineral_db = get_mineral_database()
            if mineral_db and mineral_db.available:
                # Get ALL minerals for filtering (no limit)
                result = mineral_db.get_all_minerals(page=1, per_page=10000)
                if result and isinstance(result, dict) and 'minerals' in result:
                    all_minerals = result['minerals']

                    # Apply filters
                    for mineral in all_minerals:
                        if not mineral or not isinstance(mineral, dict):
                            continue

                        # Filter by inventory number range
                        if inv_from is not None or inv_to is not None:
                            inv_num = mineral.get('inventarni_broj')
                            # Skip if no inventory number
                            if inv_num is None:
                                continue

                            # Convert to int for comparison (handle float values)
                            try:
                                inv_num_int = int(float(inv_num))
                            except (ValueError, TypeError):
                                continue

                            # Apply range filters
                            if inv_from is not None and inv_num_int < inv_from:
                                continue
                            if inv_to is not None and inv_num_int > inv_to:
                                continue

                        # Filter by location
                        if location and location.lower() not in (mineral.get('gde_se_nalazi') or '').lower():
                            continue

                        # Filter by locality
                        if locality and locality.lower() not in (mineral.get('lokalitet') or '').lower():
                            continue

                        specimens.append(mineral)

        elif collection_type == 'meteorites':
            catalog_number = request.args.get('catalog_number', '')
            name = request.args.get('name', '')
            location = request.args.get('location', '')

            for specimen in get_meteorite_collection_database()['specimens']:
                # Apply filters
                if catalog_number and catalog_number.upper() not in specimen.get('catalog_number', '').upper():
                    continue
                if name and name.lower() not in (specimen.get('meteorite_name') or '').lower():
                    continue
                if location and location.lower() not in (specimen.get('location_found') or '').lower():
                    continue

                # Add catalog_number as id for consistency
                specimen['id'] = specimen.get('catalog_number')
                specimens.append(specimen)

        elif collection_type == 'botany':
            catalog_number = request.args.get('catalog_number', '')
            name = request.args.get('name', '')

            for specimen in BOTANY_COLLECTION_DATABASE['specimens']:
                if catalog_number and catalog_number.upper() not in specimen.get('catalog_number', '').upper():
                    continue
                if name and name.lower() not in (specimen.get('scientific_name') or '').lower():
                    continue

                specimen['id'] = specimen.get('catalog_number')
                specimens.append(specimen)

        elif collection_type == 'paleozoology':
            catalog_number = request.args.get('catalog_number', '')
            name = request.args.get('name', '')

            for specimen in PALEOZOOLOGY_COLLECTION_DATABASE['specimens']:
                if catalog_number and catalog_number.upper() not in specimen.get('catalog_number', '').upper():
                    continue
                if name and name.lower() not in (specimen.get('scientific_name') or '').lower():
                    continue

                specimen['id'] = specimen.get('catalog_number')
                specimens.append(specimen)

    except Exception as e:
        logging.error(f"Error filtering specimens: {e}")
        flash(f'Грешка при филтрирању: {str(e)}', 'error')

    return render_template('admin_qr_select_specimens.html',
                         collection=collection_info,
                         specimens=specimens)

@app.route('/admin/qr_labels_selected/<collection_type>', methods=['POST'])
@admin_required
def admin_qr_labels_selected(collection_type):
    """Generate QR codes for selected specimens only."""
    import qrcode
    from io import BytesIO
    import base64

    # Get selected specimen IDs
    specimen_ids = request.form.getlist('specimen_ids')

    if not specimen_ids:
        flash('Морате изабрати бар један примерак.', 'warning')
        return redirect(url_for('admin_qr_select_specimens', collection_type=collection_type))

    # Limit the number of specimens to prevent server timeout (502 error)
    MAX_SPECIMENS = 100
    if len(specimen_ids) > MAX_SPECIMENS:
        flash(f'Можете изабрати максимум {MAX_SPECIMENS} примерака одједном. Тренутно изабрано: {len(specimen_ids)}. Молимо смањите број изабраних примерака.', 'warning')
        return redirect(url_for('admin_qr_select_specimens', collection_type=collection_type))

    logging.info(f"Generating QR codes for {len(specimen_ids)} specimens from collection {collection_type}")

    # Use the configured server address instead of request.url_root to ensure correct URL
    base_url = "http://192.168.144.48"
    labels = []

    try:
        if collection_type == 'minerals':
            # Get minerals from database
            mineral_db = get_mineral_database()
            if mineral_db and mineral_db.available:
                for specimen_id in specimen_ids:
                    try:
                        mineral = mineral_db.get_mineral_by_id(int(specimen_id))
                        if not mineral:
                            continue

                        inv_num = mineral.get('inventarni_broj_display', 'N/A')
                        qr_url = f"{base_url}/admin/mineral_detail/{mineral['id']}"

                        # Generate QR code (optimized with smaller box_size for faster generation)
                        qr = qrcode.QRCode(version=1, box_size=5, border=1)
                        qr.add_data(qr_url)
                        qr.make(fit=True)
                        img = qr.make_image(fill_color="black", back_color="white")

                        buffered = BytesIO()
                        img.save(buffered, format="PNG")
                        img_str = base64.b64encode(buffered.getvalue()).decode()

                        labels.append({
                            'catalog_number': inv_num,
                            'name': mineral.get('naziv', 'Непознато'),
                            'qr_code': img_str,
                            'url': qr_url
                        })
                    except Exception as e:
                        logging.error(f"Error processing mineral {specimen_id}: {e}")
                        continue

        else:
            # Handle other collections
            collection_data = {
                'meteorites': get_meteorite_collection_database()['specimens'],
                'botany': BOTANY_COLLECTION_DATABASE['specimens'],
                'paleozoology': PALEOZOOLOGY_COLLECTION_DATABASE['specimens']
            }

            # Map collection types to their route names
            collection_routes = {
                'meteorites': 'meteorite_collection',
                'botany': 'botany_collection',
                'paleozoology': 'paleozoology_collection'
            }

            if collection_type in collection_data:
                route_name = collection_routes.get(collection_type, f"{collection_type}_collection")
                for specimen in collection_data[collection_type]:
                    catalog_num = specimen.get('catalog_number')
                    if catalog_num in specimen_ids:
                        qr_url = f"{base_url}/admin/{route_name}?highlight={catalog_num}"

                        # Generate QR code (optimized with smaller box_size for faster generation)
                        qr = qrcode.QRCode(version=1, box_size=5, border=1)
                        qr.add_data(qr_url)
                        qr.make(fit=True)
                        img = qr.make_image(fill_color="black", back_color="white")

                        buffered = BytesIO()
                        img.save(buffered, format="PNG")
                        img_str = base64.b64encode(buffered.getvalue()).decode()

                        labels.append({
                            'catalog_number': catalog_num,
                            'name': specimen.get('meteorite_name') or specimen.get('scientific_name') or 'Непознато',
                            'qr_code': img_str,
                            'url': qr_url
                        })

        collection_names = {
            'minerals': 'Минералошка збирка',
            'meteorites': 'Метеорити',
            'botany': 'Ботаника',
            'paleozoology': 'Палеозоологија',
            'paleobotany': 'Палеоботаника',
            'geology': 'Геологија',
            'heritage': 'Културно наслеђе'
        }

        collection_info = {
            'type': collection_type,
            'name': collection_names.get(collection_type, collection_type),
            'count': len(labels)
        }

        # Store the generated data in session for format selection
        session['qr_generated_data'] = {
            'labels': labels,
            'collection_info': collection_info,
            'selected_specimens': specimen_ids
        }
        
        # Redirect to format selection
        return redirect(url_for('admin_qr_label_format', collection_type=collection_type))

    except Exception as e:
        import traceback
        logging.error(f"Error generating selected QR codes: {e}")
        logging.error(f"Traceback: {traceback.format_exc()}")
        flash(f'Грешка при генерисању QR кодова: {str(e)}', 'error')
        return redirect(url_for('admin_qr_select_specimens', collection_type=collection_type))

@app.route('/admin/qr_label_format/<collection_type>')
@admin_required
def admin_qr_label_format(collection_type):
    """Show label format selection for QR code generation."""
    logging.info(f"Format selection route called for collection_type: {collection_type}")
    
    # Get collection info
    collection_names = {
        'minerals': 'Минералошка збирка',
        'meteorites': 'Метеорити',
        'botany': 'Ботаника',
        'paleozoology': 'Палеозоологија',
        'paleobotany': 'Палеоботаника',
        'geology': 'Геологија',
        'heritage': 'Културно наслеђе',
        'mineral_boxes': 'Кутије минералошке збирке'
    }
    
    collection_info = {
        'type': collection_type,
        'name': collection_names.get(collection_type, collection_type)
    }
    
    # Set continue URL based on collection type
    continue_url = url_for('admin_qr_labels_with_format', collection_type=collection_type)
    
    return render_template('admin_qr_label_format.html',
                         collection=collection_info,
                         continue_url=continue_url)

@app.route('/admin/qr_labels_with_format/<collection_type>', methods=['POST'])
@admin_required
def admin_qr_labels_with_format(collection_type):
    """Generate QR codes with selected label format."""
    # Get form data
    label_format = request.form.get('label_format', '1')
    print_mode = request.form.get('print_mode', 'regular')
    
    logging.info(f"Received form data - label_format: {label_format}, print_mode: {print_mode}")
    logging.info(f"Form data: {dict(request.form)}")
    
    # Check if we have pre-generated data in session
    if 'qr_generated_data' not in session:
        flash('Грешка: Нема података за генерисање QR кодова.', 'error')
        return redirect(url_for('admin_qr_generator'))
    
    # Get the stored data
    stored_data = session['qr_generated_data']
    labels = stored_data['labels']
    collection_info = stored_data['collection_info']
    
    # If regular mode, render with existing data
    if print_mode == 'regular':
        collection_info['label_format'] = None
        collection_info['print_mode'] = 'regular'
        is_box_mode = stored_data.get('is_box_mode', False)
        return render_template('admin_qr_labels.html',
                             labels=labels,
                             collection=collection_info,
                             is_box_mode=is_box_mode)
    
    # For sticker mode, use the stored data with format information
    collection_info['label_format'] = label_format
    collection_info['print_mode'] = print_mode

    logging.info(f"Rendering labels with format: {label_format}, mode: {print_mode}")
    logging.info(f"Collection info: {collection_info}")

    # Clear the session data after use
    session.pop('qr_generated_data', None)
    
    # Check if this is box mode
    is_box_mode = stored_data.get('is_box_mode', False)
    
    # Render the labels with the selected format
    logging.info(f"Final collection_info before template: {collection_info}")
    
    return render_template('admin_qr_labels.html',
                         labels=labels,
                         collection=collection_info,
                         is_box_mode=is_box_mode)

@app.route('/admin/qr_labels/<collection_type>')
@admin_required
def admin_qr_labels(collection_type):
    """Generate printable QR code labels for a collection."""
    import qrcode
    from io import BytesIO
    import base64

    # Get the base URL for QR codes
    # Use the configured server address instead of request.url_root to ensure correct URL
    base_url = "http://192.168.144.48"

    labels = []

    try:
        if collection_type == 'minerals':
            # Get minerals from database
            mineral_db = get_mineral_database()
            if mineral_db and mineral_db.available:
                result = mineral_db.get_all_minerals(page=1, per_page=100)
                if result and isinstance(result, dict) and 'minerals' in result:
                    minerals = result['minerals']
                    for mineral in minerals:
                        if not mineral or not isinstance(mineral, dict) or 'id' not in mineral:
                            continue

                        inv_num = mineral.get('inventarni_broj_display', 'N/A')
                        # Generate QR code URL
                        qr_url = f"{base_url}/admin/mineral_detail/{mineral['id']}"

                        # Generate QR code image
                        qr = qrcode.QRCode(version=1, box_size=10, border=2)
                        qr.add_data(qr_url)
                        qr.make(fit=True)
                        img = qr.make_image(fill_color="black", back_color="white")

                        # Convert to base64 for embedding in HTML
                        buffered = BytesIO()
                        img.save(buffered, format="PNG")
                        img_str = base64.b64encode(buffered.getvalue()).decode()

                        labels.append({
                            'catalog_number': inv_num,
                            'name': mineral.get('naziv', 'Непознато'),
                            'qr_code': img_str,
                            'url': qr_url
                        })

        elif collection_type == 'meteorites':
            for specimen in get_meteorite_collection_database()['specimens']:
                catalog_num = specimen.get('catalog_number', 'N/A')
                qr_url = f"{base_url}/admin/meteorite_collection?highlight={catalog_num}"

                qr = qrcode.QRCode(version=1, box_size=10, border=2)
                qr.add_data(qr_url)
                qr.make(fit=True)
                img = qr.make_image(fill_color="black", back_color="white")

                buffered = BytesIO()
                img.save(buffered, format="PNG")
                img_str = base64.b64encode(buffered.getvalue()).decode()

                labels.append({
                    'catalog_number': catalog_num,
                    'name': specimen.get('meteorite_name', 'Непознато'),
                    'qr_code': img_str,
                    'url': qr_url
                })

        elif collection_type == 'botany':
            for specimen in BOTANY_COLLECTION_DATABASE['specimens']:
                catalog_num = specimen.get('catalog_number', 'N/A')
                qr_url = f"{base_url}/admin/botany_collection?highlight={catalog_num}"

                qr = qrcode.QRCode(version=1, box_size=10, border=2)
                qr.add_data(qr_url)
                qr.make(fit=True)
                img = qr.make_image(fill_color="black", back_color="white")

                buffered = BytesIO()
                img.save(buffered, format="PNG")
                img_str = base64.b64encode(buffered.getvalue()).decode()

                labels.append({
                    'catalog_number': catalog_num,
                    'name': specimen.get('scientific_name', 'Непознато'),
                    'qr_code': img_str,
                    'url': qr_url
                })

        elif collection_type == 'paleozoology':
            for specimen in PALEOZOOLOGY_COLLECTION_DATABASE['specimens']:
                catalog_num = specimen.get('catalog_number', 'N/A')
                qr_url = f"{base_url}/admin/paleozoology_collection?highlight={catalog_num}"

                qr = qrcode.QRCode(version=1, box_size=10, border=2)
                qr.add_data(qr_url)
                qr.make(fit=True)
                img = qr.make_image(fill_color="black", back_color="white")

                buffered = BytesIO()
                img.save(buffered, format="PNG")
                img_str = base64.b64encode(buffered.getvalue()).decode()

                labels.append({
                    'catalog_number': catalog_num,
                    'name': specimen.get('scientific_name', 'Непознато'),
                    'qr_code': img_str,
                    'url': qr_url
                })

        # Get collection info
        collection_names = {
            'minerals': 'Минералошка збирка',
            'meteorites': 'Метеорити',
            'botany': 'Ботаника',
            'paleozoology': 'Палеозоологија',
            'paleobotany': 'Палеоботаника',
            'geology': 'Геологија',
            'heritage': 'Културно наслеђе'
        }

        collection_info = {
            'type': collection_type,
            'name': collection_names.get(collection_type, collection_type),
            'count': len(labels)
        }

        # Store the generated data in session for format selection
        session['qr_generated_data'] = {
            'labels': labels,
            'collection_info': collection_info,
            'all_specimens': True
        }
        
        # Redirect to format selection
        return redirect(url_for('admin_qr_label_format', collection_type=collection_type))

    except Exception as e:
        import traceback
        logging.error(f"Error generating QR codes: {e}")
        logging.error(f"Traceback: {traceback.format_exc()}")
        flash(f'Грешка при генерисању QR кодова: {str(e)}', 'error')
        return redirect(url_for('admin_qr_generator'))

@app.route('/admin/batch_image_upload', methods=['GET', 'POST'])
@admin_required
def batch_image_upload():
    """Batch image upload interface for museum collections."""
    if request.method == 'POST':
        # Handle form submission
        action = request.form.get('action')
        database = request.form.get('database')
        directory = request.form.get('directory')

        if action == 'preview':
            # Preview matching results
            return render_template('admin_batch_upload_preview.html',
                                 database=database,
                                 directory=directory)
        elif action == 'upload':
            # Process actual upload
            return render_template('admin_batch_upload_results.html',
                                 results={'success': True, 'message': 'Upload completed'})

    # GET request - show upload form
    databases = [
        {'id': 'minerals', 'name': 'Минералошка збирка', 'prefix': 'M'},
        {'id': 'meteorites', 'name': 'Метеорити', 'prefix': 'MET'},
        {'id': 'paleozoology', 'name': 'Палеозоологија', 'prefix': 'PAL'},
        {'id': 'paleobotany', 'name': 'Палеоботаника', 'prefix': 'PB'},
        {'id': 'botany', 'name': 'Ботаника', 'prefix': 'B'},
    ]
    return render_template('admin_batch_image_upload.html', databases=databases)

@app.route('/static/<path:filename>')
def serve_static(filename):
    """Serve static files."""
    return send_from_directory('static', filename)

@app.route('/api/specimen_image/<database>/<entity_type>/<entity_id>')
def get_specimen_image(database, entity_type, entity_id):
    """Get specimen image or placeholder."""
    try:
        image_storage = get_image_storage()
        images = image_storage.get_images_for_entity(database, entity_type, entity_id)

        if images and len(images) > 0:
            # Get first image thumbnail
            image_id = images[0]['image_id']
            image_path = image_storage.get_image_path(image_id, 'medium')

            if image_path and image_path.exists():
                return send_file(image_path, mimetype='image/jpeg')
    except Exception as e:
        logger.error(f"Error loading specimen image: {e}")

    # Return placeholder if no image found
    placeholder_path = os.path.join('static', 'images', 'specimen-placeholder.png')
    if os.path.exists(placeholder_path):
        return send_file(placeholder_path, mimetype='image/png')
    else:
        # Return 404 if even placeholder doesn't exist
        return "No image available", 404

@app.route('/api/specimen_thumbnail/<database>/<entity_type>/<entity_id>')
def get_specimen_thumbnail(database, entity_type, entity_id):
    """Get specimen thumbnail or small placeholder."""
    try:
        image_storage = get_image_storage()
        images = image_storage.get_images_for_entity(database, entity_type, entity_id)

        if images and len(images) > 0:
            # Get first image small thumbnail
            image_id = images[0]['image_id']
            image_path = image_storage.get_image_path(image_id, 'small')

            if image_path and image_path.exists():
                return send_file(image_path, mimetype='image/jpeg')
    except Exception as e:
        logger.error(f"Error loading specimen thumbnail: {e}")

    # Return thumbnail placeholder if no image found
    placeholder_path = os.path.join('static', 'images', 'specimen-placeholder-thumb.png')
    if os.path.exists(placeholder_path):
        return send_file(placeholder_path, mimetype='image/png')
    else:
        # Fallback to regular placeholder
        placeholder_path = os.path.join('static', 'images', 'specimen-placeholder.png')
        if os.path.exists(placeholder_path):
            return send_file(placeholder_path, mimetype='image/png')

    return "No image available", 404

@app.route('/admin/manage_access')
@admin_required
def manage_user_access():
    """Manage user module access."""
    import psycopg
    from psycopg.rows import dict_row

    users_with_access = []

    try:
        # Get users from PostgreSQL
        with psycopg.connect(conninfo=os.environ.get('DATABASE_URL', '').replace('postgresql+psycopg://', 'postgresql://'), row_factory=dict_row) as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT u.email, u.full_name, u.position,
                           COALESCE(d.name, 'Природњачки музеј') as department,
                           COALESCE(r.name, 'user') as role
                    FROM users u
                    LEFT JOIN departments d ON u.department_id = d.id
                    LEFT JOIN roles r ON u.role_id = r.id
                    WHERE u.is_active = TRUE
                    ORDER BY u.full_name
                """)
                users = cur.fetchall()

        for user in users:
            if user['role'] != 'admin':  # Don't show admin users
                # Get actual access status for ALL modules (not filtered by dashboard prefs)
                user_modules = []
                for module_key in MODULE_ACCESS.keys():
                    if user_has_module_access(user['email'], user['role'], module_key):
                        user_modules.append({'key': module_key})
                users_with_access.append({
                    'email': user['email'],
                    'name': user['full_name'],
                    'department': user['department'],
                    'position': user['position'],
                    'modules': user_modules
                })
    except Exception as e:
        logger.error(f"Error loading users for access management: {e}")
        # Fallback to MUSEUM_EMPLOYEES
        for email, user_data in MUSEUM_EMPLOYEES.items():
            if user_data.get('role') != 'admin':
                user_modules = []
                for module_key in MODULE_ACCESS.keys():
                    if user_has_module_access(email, user_data.get('role', 'user'), module_key):
                        user_modules.append({'key': module_key})
                users_with_access.append({
                    'email': email,
                    'name': user_data.get('full_name', email),
                    'department': user_data.get('department', 'N/A'),
                    'modules': user_modules
                })

    selected_user = request.args.get('selected_user', '')
    return render_template('admin_manage_access.html',
                          users=users_with_access,
                          all_modules=MODULE_ACCESS,
                          selected_user=selected_user)

@app.route('/admin/grant_access', methods=['POST'])
@admin_required
def grant_module_access():
    """Grant module access to a user."""
    user_email = request.form.get('user_email')
    module_key = request.form.get('module_key')

    if not user_email or not module_key:
        flash('Недостају параметри за доделу приступа.', 'error')
        return redirect(url_for('manage_user_access'))

    if module_key not in MODULE_ACCESS:
        flash('Непознат модул.', 'error')
        return redirect(url_for('manage_user_access'))

    module = MODULE_ACCESS[module_key]
    module_name = module['name']
    changed = False

    # For modules with default_access=True, remove from restricted_users
    if module.get('default_access', False):
        restricted_users = module.get('restricted_users', [])
        if user_email in restricted_users:
            restricted_users.remove(user_email)
            changed = True
            flash(f'Приступ модулу "{module_name}" је враћен кориснику.', 'success')
        else:
            flash('Корисник већ има приступ овом модулу (подразумевани приступ).', 'info')
    else:
        # For modules with default_access=False, add to authorized_users
        if user_email not in module.get('authorized_users', []):
            if 'authorized_users' not in module:
                module['authorized_users'] = []
            module['authorized_users'].append(user_email)
            changed = True
            flash(f'Приступ модулу "{module_name}" је дат кориснику.', 'success')
        else:
            flash('Корисник већ има приступ овом модулу.', 'info')

    if changed:
        save_module_access()

    return redirect(url_for('manage_user_access', selected_user=user_email))

@app.route('/admin/revoke_access', methods=['POST'])
@admin_required
def revoke_module_access():
    """Revoke module access from a user."""
    user_email = request.form.get('user_email')
    module_key = request.form.get('module_key')

    if not user_email or not module_key:
        flash('Недостају параметри за укидање приступа.', 'error')
        return redirect(url_for('manage_user_access'))

    if module_key not in MODULE_ACCESS:
        flash('Непознат модул.', 'error')
        return redirect(url_for('manage_user_access'))

    module = MODULE_ACCESS[module_key]
    module_name = module['name']
    changed = False

    # For modules with default_access=True, add to restricted_users
    if module.get('default_access', False):
        if 'restricted_users' not in module:
            module['restricted_users'] = []
        if user_email not in module['restricted_users']:
            module['restricted_users'].append(user_email)
            changed = True
            flash(f'Приступ модулу "{module_name}" је укинут кориснику.', 'success')
        else:
            flash('Корисник већ нема приступ овом модулу.', 'info')
    else:
        # For modules with default_access=False, remove from authorized_users
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

@app.route('/admin/employees_database')
@module_access_required('employees_database')
def employees_database():
    """View all employee databases and information."""
    employees_list = get_employee_directory()

    return render_template('admin_employees_database.html',
                          employees=employees_list,
                          total_employees=len(employees_list))

@app.route('/admin/employee_profiles_database')
@module_access_required('employee_profiles')
def employee_profiles_database():
    """Employee profiles database with detailed biographical information."""
    employees = get_employee_directory()
    employees_list = [emp for emp in employees if emp.get('description')]
    
    # Calculate statistics
    total_profiles = len(employees_list)
    total_directory = len(employees)
    with_descriptions = len([e for e in employees_list if e.get('description')])
    departments = len(set([e['department'] for e in employees_list if e.get('department')]))
    
    statistics = {
        'total_profiles': total_profiles,
        'with_descriptions': with_descriptions,
        'total_departments': departments,
        'completion_rate': round((with_descriptions / total_directory * 100), 1) if total_directory > 0 else 0
    }
    
    return render_template('admin_employee_profiles_database.html',
                          employees=employees_list,
                          statistics=statistics,
                          total_profiles=total_profiles)

@app.route('/admin/add_user', methods=['GET', 'POST'])
@admin_required
def add_user():
    """Add new user to the system."""
    if request.method == 'POST':
        # Get form data
        email = request.form.get('email')
        full_name = request.form.get('full_name')
        department = request.form.get('department')
        position = request.form.get('position')
        role = request.form.get('role', 'employee')
        password = request.form.get('password', 'user')

        # Validate required fields
        if not all([email, full_name, department, position]):
            flash('Сви поља су обавезна.', 'error')
            return redirect(url_for('add_user'))

        # Check if user already exists
        if email in MUSEUM_EMPLOYEES:
            flash('Корисник са овом е-mail адресом већ постоји.', 'error')
            return redirect(url_for('add_user'))

        # Add new user
        new_user_id = max([emp['user_id'] for emp in MUSEUM_EMPLOYEES.values()]) + 1
        MUSEUM_EMPLOYEES[email] = {
            'user_id': new_user_id,
            'email': email,
            'full_name': full_name,
            'department': department,
            'position': position,
            'role': role,
            'password': password
        }

        flash(f'Корисник {full_name} је успешно додат у систем. Привремена лозинка: {password}', 'success')
        return redirect(url_for('employees_database'))

    # GET request - show form
    directory = get_employee_directory()
    if directory:
        departments = sorted({emp['department'] for emp in directory if emp.get('department')})
    else:
        departments = sorted({emp['department'] for emp in MUSEUM_EMPLOYEES.values() if emp.get('department')})
    return render_template('admin_add_user.html', departments=departments)

# Duplicate manage_access route removed - using manage_user_access instead

@app.route('/dashboard/customize', methods=['GET', 'POST'])
@login_required
def customize_dashboard():
    """Customize dashboard widget preferences."""
    # Reload preferences to get latest changes
    load_dashboard_preferences()

    user_email = session.get('user_email')
    user_role = session.get('user_role')

    if request.method == 'POST':
        # Get selected widgets from form
        selected_widgets = request.form.getlist('widgets')

        # Update preferences
        if user_email not in DASHBOARD_PREFERENCES:
            DASHBOARD_PREFERENCES[user_email] = {}

        DASHBOARD_PREFERENCES[user_email]['enabled_widgets'] = selected_widgets

        # Save preferences to file
        if save_dashboard_preferences():
            flash('Подешавања видгета успешно сачувана!', 'success')
        else:
            flash('Грешка при чувању подешавања!', 'error')

        return redirect(url_for('dashboard'))
    
    # GET request - show customization form
    # Get all modules user has access to
    all_accessible = []
    for module_key, module_info in MODULE_ACCESS.items():
        if user_has_module_access(user_email, user_role, module_key):
            all_accessible.append({
                'key': module_key,
                'name': module_info['name'],
                'description': module_info['description'],
                'icon': module_info['icon']
            })
    
    # Get current preferences
    current_prefs = DASHBOARD_PREFERENCES.get(user_email, {}).get('enabled_widgets', list(MODULE_ACCESS.keys()))
    
    return render_template('customize_dashboard.html',
                          available_modules=all_accessible,
                          enabled_widgets=current_prefs)

@app.route('/admin/reports')
@admin_required
def system_reports():
    """Generate system reports and analytics."""
    global LIBRARY_DATABASE

    # Ensure datasets are loaded
    if LIBRARY_DATABASE is None:
        LIBRARY_DATABASE = load_library_database()
    employees = get_employee_directory()

    # Calculate system statistics
    total_employees = len(employees)
    total_books = len(LIBRARY_DATABASE['books'])
    exhibit_stats = get_exhibit_statistics()
    total_artifacts = exhibit_stats['total_artifacts']

    # Employee statistics
    admin_count = len([emp for emp in employees if emp.get('role') == 'admin'])
    employee_count = total_employees - admin_count

    # Department breakdown
    dept_stats = {}
    for emp in employees:
        dept = emp.get('department') or 'Непознато'
        dept_stats[dept] = dept_stats.get(dept, 0) + 1

    # Library statistics
    library_stats = LIBRARY_DATABASE['statistics'].copy()
    available_books = len([b for b in LIBRARY_DATABASE['books'] if b['status'] == 'доступна'])
    borrowed_books = len([b for b in LIBRARY_DATABASE['books'] if b['status'] == 'позајмљена'])

    # Exhibits statistics
    displayed_artifacts = exhibit_stats['displayed_artifacts']
    storage_artifacts = exhibit_stats['storage_artifacts']

    # Module access statistics
    timesheet_users = len([
        emp for emp in employees
        if user_has_module_access(emp.get('email', ''), emp.get('role', 'employee'), 'timesheet')
    ])
    database_users = len([
        emp for emp in employees
        if user_has_module_access(emp.get('email', ''), emp.get('role', 'employee'), 'museum_databases')
    ])

    report_data = {
        'system_overview': {
            'total_employees': total_employees,
            'total_books': total_books,
            'total_artifacts': total_artifacts,
            'active_databases': 5,  # Employees, Minerals, Library, Exhibits, Exhibitions
            'planned_databases': 2  # Visitors, Research
        },
        'employee_stats': {
            'total': total_employees,
            'admins': admin_count,
            'employees': employee_count,
            'departments': dept_stats
        },
        'library_stats': {
            'total_books': total_books,
            'available_books': available_books,
            'borrowed_books': borrowed_books,
            'utilization_rate': round((borrowed_books / total_books * 100), 1) if total_books > 0 else 0
        },
        'exhibit_stats': {
            'total_artifacts': total_artifacts,
            'displayed_artifacts': displayed_artifacts,
            'storage_artifacts': storage_artifacts,
            'display_rate': round((displayed_artifacts / total_artifacts * 100), 1) if total_artifacts > 0 else 0
        },
        'access_stats': {
            'timesheet_users': timesheet_users,
            'database_users': database_users,
            'total_with_access': timesheet_users
        }
    }

    return render_template('admin_reports.html', report_data=report_data)


@app.route('/admin/exhibits_database')
@admin_required
def exhibits_database():
    """Detailed inventory of museum artifacts and exhibits."""
    artifacts = EXHIBITS_DATABASE['artifacts']
    statistics = get_exhibit_statistics()
    categories = sorted({a['category'] for a in artifacts})
    statuses = EXHIBITS_DATABASE.get('statuses', sorted({a['status'] for a in artifacts}))
    conditions = EXHIBITS_DATABASE.get('conditions', sorted({a['condition'] for a in artifacts}))

    return render_template('admin_exhibits_database.html',
                          artifacts=artifacts,
                          statistics=statistics,
                          categories=categories,
                          statuses=statuses,
                          conditions=conditions)


@app.route('/admin/exhibitions_database')
@module_access_required('exhibitions_database')
def exhibitions_database():
    """Timeline of gallery exhibitions with analytics."""
    exhibitions_all = sorted(EXHIBITIONS_DATABASE['exhibitions'],
                             key=lambda e: e['start_date'],
                             reverse=True)
    gallery_exhibitions = [e for e in exhibitions_all if e.get('category', 'gallery') != 'touring']
    touring_exhibitions = [e for e in exhibitions_all if e.get('category', 'gallery') == 'touring']
    statistics = get_exhibition_statistics()
    exhibition_types = EXHIBITIONS_DATABASE.get('types',
                                                sorted({e.get('type', 'Изложба') for e in gallery_exhibitions}))

    return render_template('admin_exhibitions_database.html',
                          exhibitions=gallery_exhibitions,
                          touring_exhibitions=touring_exhibitions,
                          statistics=statistics,
                          exhibition_types=exhibition_types)

@app.route('/admin/news')
@module_access_required('news')
def museum_news():
    """Museum news and announcements."""
    articles_all = sorted(NEWS_DATABASE['articles'],
                          key=lambda a: a.get('start_date', ''),
                          reverse=True)
    
    # Count articles by status
    total_articles = len(articles_all)
    recent_articles = [a for a in articles_all[:20]]  # Show 20 most recent
    
    return render_template('admin_news.html',
                          articles=recent_articles,
                          total_articles=total_articles)

@app.route('/admin/library_database')
@module_access_required('library_database')
def library_database():
    """Library database management system."""
    global LIBRARY_DATABASE

    # Ensure library database is loaded
    if LIBRARY_DATABASE is None:
        LIBRARY_DATABASE = load_library_database()

    books = LIBRARY_DATABASE['books']
    categories = LIBRARY_DATABASE['categories']
    statistics = LIBRARY_DATABASE['statistics'].copy()

    # Update statistics based on current data
    statistics['total_books'] = len(books)
    statistics['available_books'] = len([b for b in books if b['status'] == 'доступна'])
    statistics['borrowed_books'] = len([b for b in books if b['status'] == 'позајмљена'])
    statistics['total_categories'] = len(set(book['category'] for book in books))

    return render_template('admin_library_database.html',
                          books=books,
                          categories=categories,
                          statistics=statistics,
                          total_books=len(books))

@app.route('/admin/cultural_heritage_database')
@module_access_required('cultural_heritage')
def cultural_heritage_database():
    """Cultural heritage database management system (Заштићена културна добра)."""
    heritage_db = get_cultural_heritage_database()
    heritage_items = heritage_db['heritage_items']
    heritage_types = heritage_db['heritage_types']
    categories = heritage_db['categories']
    subcategories = heritage_db['subcategories']
    significance_levels = heritage_db['significance_levels']
    locations = heritage_db['locations']
    conditions = heritage_db['conditions']
    protection_statuses = heritage_db['protection_statuses']
    statistics = heritage_db['statistics']

    # Update statistics based on current data
    statistics['total_heritage_items'] = len(heritage_items)
    statistics['exceptional_significance'] = len([h for h in heritage_items if h['significance'] == 'Културно добро од изузетног значаја'])
    statistics['great_significance'] = len([h for h in heritage_items if h['significance'] == 'Културно добро од великог значаја'])
    statistics['regular_significance'] = len([h for h in heritage_items if h['significance'] == 'Културно добро'])
    statistics['natural_heritage'] = len([h for h in heritage_items if h['category'] == 'Природњачко наслеђе'])
    statistics['displayed_items'] = len([h for h in heritage_items if 'Сала' in h['location']])
    statistics['storage_items'] = len([h for h in heritage_items if 'Депо' in h['location']])
    statistics['excellent_condition'] = len([h for h in heritage_items if h['condition'] == 'Одлично'])
    statistics['good_condition'] = len([h for h in heritage_items if h['condition'] == 'Добро'])

    return render_template('admin_cultural_heritage_database.html',
                          heritage_items=heritage_items,
                          heritage_types=heritage_types,
                          categories=categories,
                          subcategories=subcategories,
                          significance_levels=significance_levels,
                          locations=locations,
                          conditions=conditions,
                          protection_statuses=protection_statuses,
                          statistics=statistics,
                          total_heritage_items=len(heritage_items))

# Curator Collection Database Routes

@app.route('/admin/botany_collection')
@module_access_required('curator_collections')
def botany_collection():
    """Botany collection database."""
    # Check if highlighting a specific specimen (from QR code)
    highlight = request.args.get('highlight')
    specimens = BOTANY_COLLECTION_DATABASE['specimens']

    if highlight:
        # Filter to show only the highlighted specimen
        specimens = [s for s in specimens if s.get('catalog_number') == highlight]
        if not specimens:
            flash(f'Примерак са каталошким бројем {highlight} није пронађен.', 'warning')
            specimens = BOTANY_COLLECTION_DATABASE['specimens']

    return render_template('admin_collection_database.html',
                          collection_name='Ботаничка збирка',
                          collection_icon='bi-flower1',
                          specimens=specimens,
                          statistics=BOTANY_COLLECTION_DATABASE['statistics'],
                          collection_type='botany',
                          highlight=highlight)

@app.route('/admin/ichthyology_collection')
@module_access_required('curator_collections')
def ichthyology_collection():
    """Ichthyology collection database."""
    return render_template('admin_collection_database.html',
                          collection_name='Ихтиолошка збирка',
                          collection_icon='bi-water',
                          specimens=ICHTHYOLOGY_COLLECTION_DATABASE['specimens'],
                          statistics=ICHTHYOLOGY_COLLECTION_DATABASE['statistics'],
                          collection_type='ichthyology')

@app.route('/admin/entomology_collection')
@module_access_required('curator_collections')
def entomology_collection():
    """Entomology collection database."""
    return render_template('admin_collection_database.html',
                          collection_name='Ентомолошка збирка',
                          collection_icon='bi-bug',
                          specimens=ENTOMOLOGY_COLLECTION_DATABASE['specimens'],
                          statistics=ENTOMOLOGY_COLLECTION_DATABASE['statistics'],
                          collection_type='entomology')

@app.route('/admin/mycology_collection')
@module_access_required('curator_collections')
def mycology_collection():
    """Mycology collection database."""
    return render_template('admin_collection_database.html',
                          collection_name='Миколошка збирка',
                          collection_icon='bi-tree',
                          specimens=MYCOLOGY_COLLECTION_DATABASE['specimens'],
                          statistics=MYCOLOGY_COLLECTION_DATABASE['statistics'],
                          collection_type='mycology')

@app.route('/admin/herpetology_collection')
@module_access_required('curator_collections')
def herpetology_collection():
    """Herpetology collection database."""
    return render_template('admin_collection_database.html',
                          collection_name='Херпетолошка збирка',
                          collection_icon='bi-emoji-sunglasses',
                          specimens=HERPETOLOGY_COLLECTION_DATABASE['specimens'],
                          statistics=HERPETOLOGY_COLLECTION_DATABASE['statistics'],
                          collection_type='herpetology')

@app.route('/admin/ornithology_collection')
@module_access_required('curator_collections')
def ornithology_collection():
    """Ornithology collection database."""
    return render_template('admin_collection_database.html',
                          collection_name='Орнитолошка збирка',
                          collection_icon='bi-feather',
                          specimens=ORNITHOLOGY_COLLECTION_DATABASE['specimens'],
                          statistics=ORNITHOLOGY_COLLECTION_DATABASE['statistics'],
                          collection_type='ornithology')

@app.route('/admin/paleozoology_collection')
@module_access_required('curator_collections')
def paleozoology_collection():
    """Paleozoology collection database."""
    # Check if highlighting a specific specimen (from QR code)
    highlight = request.args.get('highlight')
    specimens = PALEOZOOLOGY_COLLECTION_DATABASE['specimens']

    if highlight:
        # Filter to show only the highlighted specimen
        specimens = [s for s in specimens if s.get('catalog_number') == highlight]
        if not specimens:
            flash(f'Примерак са каталошким бројем {highlight} није пронађен.', 'warning')
            specimens = PALEOZOOLOGY_COLLECTION_DATABASE['specimens']

    return render_template('admin_collection_database.html',
                          collection_name='Палеозоолошка збирка',
                          collection_icon='bi-gem',
                          specimens=specimens,
                          statistics=PALEOZOOLOGY_COLLECTION_DATABASE['statistics'],
                          collection_type='paleozoology',
                          highlight=highlight)

@app.route('/admin/paleobotany_collection')
@module_access_required('curator_collections')
def paleobotany_collection():
    """Paleobotany collection database."""
    return render_template('admin_collection_database.html',
                          collection_name='Палеоботаничка збирка',
                          collection_icon='bi-flower2',
                          specimens=PALEOBOTANY_COLLECTION_DATABASE['specimens'],
                          statistics=PALEOBOTANY_COLLECTION_DATABASE['statistics'],
                          collection_type='paleobotany')

@app.route('/admin/petrology_collection')
@module_access_required('curator_collections')
def petrology_collection():
    """Petrology collection database."""
    return render_template('admin_collection_database.html',
                          collection_name='Петролошка збирка',
                          collection_icon='bi-mountains',
                          specimens=PETROLOGY_COLLECTION_DATABASE['specimens'],
                          statistics=PETROLOGY_COLLECTION_DATABASE['statistics'],
                          collection_type='petrology')

@app.route('/admin/meteorite_collection')
@module_access_required('curator_collections')
def meteorite_collection():
    """Meteorite collection database."""
    # Get meteorite database (from PostgreSQL or fallback)
    meteorite_db = get_meteorite_collection_database()

    # Check if highlighting a specific specimen (from QR code)
    highlight = request.args.get('highlight')
    specimens = meteorite_db['specimens']

    logging.info(f"Meteorite collection accessed. Highlight parameter: {highlight}")
    logging.info(f"Total specimens before filter: {len(specimens)}")

    if highlight:
        # Filter to show only the highlighted specimen
        specimens = [s for s in specimens if s.get('catalog_number') == highlight]
        logging.info(f"Specimens after filter: {len(specimens)}")
        logging.info(f"Filtered specimens: {specimens}")

        if not specimens:
            flash(f'Примерак са каталошким бројем {highlight} није пронађен.', 'warning')
            specimens = meteorite_db['specimens']
        else:
            flash(f'Приказ QR скенираног примерка: {highlight}', 'info')

    return render_template('admin_collection_database.html',
                          collection_name='Збирка метеорита',
                          collection_icon='bi-stars',
                          specimens=specimens,
                          statistics=meteorite_db['statistics'],
                          collection_type='meteorite',
                          highlight=highlight)

@app.route('/admin/mineral_collection')
@module_access_required('mineral_database')
def admin_mineral_collection():
    """Mineral collection database - Integrated from PrirodnjackiMuzej."""
    mineral_db = get_mineral_database()

    # Get parameters
    search_query = request.args.get('search', '').strip()
    search_mode = request.args.get('search_mode', 'collection')
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 50, type=int)
    sort_by = request.args.get('sort_by', 'id')
    sort_order = request.args.get('sort_order', 'asc')

    # Column selection
    columns_param = request.args.get('columns', '')
    default_columns = ['inventarni_broj', 'naziv', 'predmet', 'lokalitet', 'gde_se_nalazi']
    selected_columns = columns_param.split(',') if columns_param else default_columns

    # Available columns for selector
    available_columns = {
        'inventarni_broj': 'Инв. број',
        'naziv': 'Назив',
        'predmet': 'Предмет',
        'lokalitet': 'Локалитет',
        'gde_se_nalazi': 'Где се налази',
        'nacin_nabavljanja': 'Начин набављања',
        'datum_nabavljanja': 'Датум набављања',
        'legator': 'Легатор/Нашао',
        'identifikovao': 'Идентификовао',
        'kolicina': 'Количина',
        'datum_unosa': 'Датум уноса'
    }

    is_rruff_mode = search_mode == 'rruff'

    # Get RRUFF-specific parameters
    elements = request.args.get('elements', '').strip()
    crystal_system = request.args.get('crystal_system', '').strip()
    ima_status = request.args.get('ima_status', '').strip()

    if is_rruff_mode:
        # RRUFF mode - browse scientific database
        result = mineral_db.get_rruff_minerals(
            page=page,
            per_page=per_page,
            search=search_query,
            crystal_system=crystal_system,
            ima_status=ima_status,
            elements=elements
        )
        stats = {'total_minerals': 0}  # Museum collection stats not needed in RRUFF mode
        rruff_stats = mineral_db.get_rruff_statistics()
    else:
        # Museum collection mode
        if search_query:
            # Search minerals
            minerals_list = mineral_db.search_minerals(search_query)
            result = {
                'minerals': minerals_list,
                'total': len(minerals_list),
                'page': 1,
                'per_page': len(minerals_list),
                'total_pages': 1
            }
        else:
            # Get paginated list
            result = mineral_db.get_all_minerals(page=page, per_page=per_page,
                                                 sort_by=sort_by, sort_order=sort_order)

        # Get statistics
        stats = mineral_db.get_statistics()
        rruff_stats = mineral_db.get_rruff_statistics()

    return render_template('admin_mineral_collection.html',
                          minerals=result['minerals'],
                          total=result['total'],
                          total_minerals=result['total'],
                          page=result['page'],
                          per_page=result['per_page'],
                          total_pages=result['total_pages'],
                          stats=stats,
                          rruff_stats=rruff_stats,
                          search_query=search_query,
                          is_rruff_mode=is_rruff_mode,
                          sort_by=sort_by,
                          sort_order=sort_order,
                          selected_columns=selected_columns,
                          available_columns=available_columns,
                          elements=elements,
                          crystal_system=crystal_system,
                          ima_status=ima_status)

@app.route('/admin/mineral_detail/<int:mineral_id>')
@module_access_required('mineral_database')
def admin_mineral_detail(mineral_id):
    """Mineral detail view."""
    mineral_db = get_mineral_database()
    mineral = mineral_db.get_mineral_by_id(mineral_id)

    if not mineral:
        flash('Минерал није пронађен.', 'error')
        return redirect(url_for('admin_mineral_collection'))

    # Try to get RRUFF scientific data
    rruff_data = None
    if mineral.get('naziv'):
        rruff_data = mineral_db.get_rruff_data_for_mineral(mineral['naziv'])

    return render_template('admin_mineral_detail.html',
                          mineral=mineral,
                          rruff_data=rruff_data)

@app.route('/admin/rruff/detail/<int:mineral_id>')
@module_access_required('mineral_database')
def admin_rruff_detail(mineral_id):
    """RRUFF mineral detail view - shows all scientific data for a RRUFF database entry."""
    try:
        mineral_db = get_mineral_database()
        mineral = mineral_db.get_rruff_mineral_by_id(mineral_id)

        if not mineral:
            flash('RRUFF минерал није пронађен.', 'error')
            return redirect(url_for('admin_mineral_collection', search_mode='rruff'))

        current_app.logger.info(f"Loading RRUFF detail for mineral ID {mineral_id}: {mineral.get('name', 'Unknown')}")
        return render_template('admin_rruff_detail.html', mineral=mineral)
    except Exception as e:
        current_app.logger.error(f"Error loading RRUFF detail for mineral ID {mineral_id}: {e}")
        current_app.logger.exception("Full traceback:")
        flash(f'Грешка при учитавању RRUFF података: {str(e)}', 'error')
        return redirect(url_for('admin_mineral_collection', search_mode='rruff'))

@app.route('/admin/inventory_book')
@admin_required
def inventory_book():
    """Inventory book sub-database - Physical inventory book records."""
    from inventory_reconciliation import InventoryReconciliation

    reconciliation = InventoryReconciliation()

    # Get search parameters
    search_name = request.args.get('search_name', '').strip()
    search_locality = request.args.get('search_locality', '').strip()
    inv_number = request.args.get('inv_number', '').strip()
    sheet_filter = request.args.get('sheet', '').strip()
    page = request.args.get('page', 1, type=int)
    per_page = 100

    # Search inventory
    search_params = {}
    if search_name:
        search_params['name'] = search_name
    if search_locality:
        search_params['locality'] = search_locality
    if inv_number:
        try:
            search_params['inv_number'] = int(inv_number)
        except ValueError:
            pass
    if sheet_filter:
        search_params['sheet'] = sheet_filter

    # Get results
    if search_params:
        items = reconciliation.search_inventory(**search_params)
    else:
        items = reconciliation.get_inventory_book_items()

    # Load revised mineral collection index for cross-linking
    collection_index = reconciliation.get_collection_index()

    # Pagination
    total_items = len(items)
    start_idx = (page - 1) * per_page
    end_idx = start_idx + per_page
    paginated_items = items[start_idx:end_idx]

    # Annotate paginated items with collection matches
    annotated_items = []
    for item in paginated_items:
        item_with_match = dict(item)
        matches = collection_index.get(item.get('inventory_number'), [])
        item_with_match['collection_matches'] = matches
        item_with_match['has_collection_match'] = bool(matches)
        item_with_match['primary_collection_id'] = matches[0]['id'] if matches else None
        item_with_match['collection_match_count'] = len(matches)
        annotated_items.append(item_with_match)

    # Get summary
    summary = reconciliation.get_inventory_summary()

    # Get available sheets for filter
    available_sheets = reconciliation.get_available_sheets()

    return render_template('admin_inventory_book.html',
                          items=annotated_items,
                          total_items=total_items,
                          summary=summary,
                          available_sheets=available_sheets,
                          current_page=page,
                          total_pages=(total_items + per_page - 1) // per_page,
                          search_name=search_name,
                          search_locality=search_locality,
                          inv_number=inv_number,
                          sheet_filter=sheet_filter)

@app.route('/admin/inventory_reconciliation', endpoint='inventory_reconciliation')
@admin_required
def inventory_reconciliation_view():
    """Inventory reconciliation tool - Compare book vs actual collection."""
    from inventory_reconciliation import InventoryReconciliation

    reconciliation = InventoryReconciliation()

    # Get summary
    summary = reconciliation.get_inventory_summary()

    # For now, generate a basic report without collection data
    # In the future, this will be integrated with actual mineral collection data
    report = reconciliation.generate_discrepancy_report()

    return render_template('admin_inventory_reconciliation.html',
                          summary=summary,
                          report=report)

@app.route('/admin/conservation_biology')
@admin_required
def conservation_biology():
    """Conservation biology records database."""
    return render_template('admin_collection_database.html',
                          collection_name='Конзервација биолошких збирки',
                          collection_icon='bi-shield-check',
                          specimens=CONSERVATION_BIOLOGY_DATABASE['records'],
                          statistics=CONSERVATION_BIOLOGY_DATABASE['statistics'],
                          collection_type='conservation')

# Collection PDF export route (placeholder)
@app.route('/admin/export_collection_to_pdf/<collection_type>')
@module_access_required('curator_collections')
def export_collection_to_pdf(collection_type):
    """Export collection to PDF - placeholder route."""
    flash('Функционалност извоза у PDF је у развоју.', 'info')
    # Redirect back to the collection
    collection_routes = {
        'botany': 'botany_collection',
        'ichthyology': 'ichthyology_collection',
        'entomology': 'entomology_collection',
        'mycology': 'mycology_collection',
        'herpetology': 'herpetology_collection',
        'ornithology': 'ornithology_collection',
        'paleozoology': 'paleozoology_collection',
        'paleobotany': 'paleobotany_collection',
        'petrology': 'petrology_collection',
        'meteorite': 'meteorite_collection',
        'conservation': 'conservation_biology'
    }
    return redirect(url_for(collection_routes.get(collection_type, 'museum_databases')))

@app.route('/admin/museum_databases')
@module_access_required('museum_databases')
def museum_databases():
    """Overview of all museum databases."""
    global LIBRARY_DATABASE

    # Ensure library database is loaded
    if LIBRARY_DATABASE is None:
        LIBRARY_DATABASE = load_library_database()

    # Load supporting datasets
    try:
        employee_directory = get_employee_directory()
    except Exception as exc:  # pragma: no cover
        logger.error("Employee directory unavailable: %s", exc)
        employee_directory = []
    employee_count = len(employee_directory)
    profile_count = len([e for e in employee_directory if e.get('description')])

    if employee_count == 0:
        employee_count = len(MUSEUM_EMPLOYEES)
    if profile_count == 0:
        profile_count = len([e for e in MUSEUM_EMPLOYEES.values() if e.get('description')])

    mineral_count = None
    try:
        mineral_db = get_mineral_database()
        if mineral_db and getattr(mineral_db, 'available', False):
            mineral_stats = mineral_db.get_statistics() or {}
            mineral_count = mineral_stats.get('total_minerals')
    except Exception as exc:  # pragma: no cover
        logger.error("Mineral statistics unavailable: %s", exc)

    inventory_total = None
    inventory_unique = None
    try:
        from inventory_reconciliation import InventoryReconciliation
        reconciliation = InventoryReconciliation()
        inventory_summary = reconciliation.get_inventory_summary()
        inventory_total = inventory_summary.get('total_items')
        inventory_unique = inventory_summary.get('unique_inventory_numbers')
    except Exception as exc:  # pragma: no cover - depends on optional DB state
        logger.error("Inventory summary unavailable: %s", exc)

    try:
        bird_stats = bird_ringing_database.get_statistics() or {}
    except Exception as exc:  # pragma: no cover - depends on optional DB state
        logger.error("Bird ringing statistics unavailable: %s", exc)
        bird_stats = {}
    bird_count = bird_stats.get('total_records')
    bird_species = bird_stats.get('unique_species')
    bird_locations = bird_stats.get('unique_locations')

    def collection_total(collection: Dict, stats_key: str = 'total_specimens'):
        if not collection:
            return None
        stats = collection.get('statistics', {})
        value = stats.get(stats_key)
        if value is None:
            if 'specimens' in collection:
                value = len(collection['specimens'])
            elif 'records' in collection:
                value = len(collection['records'])
        return value

    collection_counts = {
        'botany_collection': collection_total(BOTANY_COLLECTION_DATABASE),
        'ichthyology_collection': collection_total(ICHTHYOLOGY_COLLECTION_DATABASE),
        'entomology_collection': collection_total(ENTOMOLOGY_COLLECTION_DATABASE),
        'mycology_collection': collection_total(MYCOLOGY_COLLECTION_DATABASE),
        'herpetology_collection': collection_total(HERPETOLOGY_COLLECTION_DATABASE),
        'ornithology_collection': collection_total(ORNITHOLOGY_COLLECTION_DATABASE),
        'paleozoology_collection': collection_total(PALEOZOOLOGY_COLLECTION_DATABASE),
        'paleobotany_collection': collection_total(PALEOBOTANY_COLLECTION_DATABASE),
        'petrology_collection': collection_total(PETROLOGY_COLLECTION_DATABASE),
        'meteorite_collection': collection_total(get_meteorite_collection_database()),
        'conservation_biology': collection_total(CONSERVATION_BIOLOGY_DATABASE, stats_key='total_records'),
        'zoology_collection': None,
        'geology_conservation': None
    }

    try:
        exhibit_stats = get_exhibit_statistics()
    except Exception as exc:  # pragma: no cover
        logger.error("Exhibit statistics unavailable: %s", exc)
        exhibit_stats = {'total_artifacts': 0, 'displayed_artifacts': 0, 'storage_artifacts': 0}

    try:
        exhibition_stats = get_exhibition_statistics()
    except Exception as exc:  # pragma: no cover
        logger.error("Exhibition statistics unavailable: %s", exc)
        exhibition_stats = {'total_exhibitions': 0}
    databases_info = {
        'employees': {
            'name': 'База запослених',
            'description': 'Информације о свим запосленима музеја',
            'icon': 'bi-people-fill',
            'count': employee_count or '—',
            'status': 'active',
            'url': '/admin/employees_database',
            'color': 'primary'
        },
        'employee_profiles': {
            'name': 'База профила запослених',
            'description': 'Биографије и стручни профили запослених',
            'icon': 'bi-person-badge',
            'count': profile_count or '—',
            'status': 'active',
            'url': '/admin/employee_profiles_database',
            'color': 'info'
        },
        'minerals': {
            'name': 'База минерала',
            'description': 'Колекција минерала и геолошких узорака',
            'icon': 'bi-gem',
            'count': mineral_count or '—',
            'status': 'active',
            'url': '/admin/mineral_collection',
            'color': 'success'
        },
        'inventory_book': {
            'name': 'Књига Инвентара',
            'description': 'Физичка књига инвентара - ревидирани уноси са архивским бројевима',
            'icon': 'bi-book-half',
            'count': inventory_total or '—',
            'status': 'active',
            'url': '/admin/inventory_book',
            'color': 'warning'
        },
        'inventory_reconciliation': {
            'name': 'Упоређивање инвентара',
            'description': 'Алат за упоређивање књиге инвентара са ревидираном базом',
            'icon': 'bi-clipboard-check',
            'count': inventory_unique or inventory_total or '—',
            'status': 'active',
            'url': '/admin/inventory_reconciliation',
            'color': 'danger'
        },
        'library': {
            'name': 'База библиотеке',
            'description': 'Каталог књига и научних публикација',
            'icon': 'bi-book',
            'count': len(LIBRARY_DATABASE.get('books', [])),
            'status': 'active',
            'url': '/admin/library_database',
            'color': 'info'
        },
        'exhibits': {
            'name': 'База експоната',
            'description': 'Инвентар музејских експоната, стање и локације',
            'icon': 'bi-collection',
            'count': exhibit_stats['total_artifacts'],
            'status': 'active',
            'url': '/admin/exhibits_database',
            'color': 'warning'
        },
        'cultural_heritage': {
            'name': 'База заштићених културних добара',
            'description': 'Регистар покретних културних добара под заштитом',
            'icon': 'bi-award',
            'count': len(get_cultural_heritage_database()['heritage_items']),
            'status': 'active',
            'url': '/admin/cultural_heritage_database',
            'color': 'warning'
        },
        'visitors': {
            'name': 'База посетилаца',
            'description': 'Статистике и информације о посетиоцима',
            'icon': 'bi-person-check',
            'count': len(VISITOR_RECORDS),
            'status': 'active',
            'url': '/admin/visitors_database',
            'color': 'secondary'
        },
        'research': {
            'name': 'База истраживања',
            'description': 'Научни радови и истраживачки пројекти',
            'icon': 'bi-search',
            'count': len(RESEARCH_PROJECTS),
            'status': 'active',
            'url': '/admin/research_database',
            'color': 'dark'
        },
        'bird_ringing': {
            'name': 'База прстеновања птица',
            'description': 'Комплетна база података о прстенованим птицама - '
                           f"{bird_species or '325'} врста, {bird_locations or '979'} локација",
            'icon': 'bi-egg',
            'count': bird_count or '—',
            'status': 'active',
            'url': '/admin/bird_ringing_database',
            'color': 'info',
            'curator': 'vuk.popic@nhmbeo.rs'
        },
        'exhibitions': {
            'name': 'База изложби',
            'description': 'Архива галеријских изложби и анализа посећености',
            'icon': 'bi-easel',
            'count': exhibition_stats['total_exhibitions'],
            'status': 'active' if exhibition_stats['total_exhibitions'] else 'planned',
            'url': '/admin/exhibitions_database',
            'color': 'danger'
        },
        
        # CURATOR COLLECTIONS - Biology Department
        'botany_collection': {
            'name': 'Ботаничка збирка',
            'description': 'Хербаријум >40.000 примерака - ендемске биљке Балкана (Др М. Никетић - SANU, В. Стојановић, Др А. Савић, Др М. Несторовић)',
            'icon': 'bi-flower1',
            'count': collection_counts['botany_collection'] or '—',
            'status': 'active',
            'url': '/admin/botany_collection',
            'color': 'success',
            'curators': ['mniketic@nhmbeo.rs', 'verica.stojanovic@nhmbeo.rs', 'aleksandra.savic@nhmbeo.rs', 'marko.nestorovic@nhmbeo.rs']
        },
        'ichthyology_collection': {
            'name': 'Ихтиолошка збирка',
            'description': 'Колекција риба и водених организама - виши кустос (Д. Вучић)',
            'icon': 'bi-water',
            'count': collection_counts['ichthyology_collection'] or '—',
            'status': 'active',
            'url': '/admin/ichthyology_collection',
            'color': 'info',
            'curators': ['dubravka.vucic@nhmbeo.rs']
        },
        'entomology_collection': {
            'name': 'Ентомолошка збирка',
            'description': 'Колекција инсеката - 1.710 врста приказано, збирка Odonata (М. Јовић - координатор Balkan OdoBase, А. Стојановић - конзерватор)',
            'icon': 'bi-bug',
            'count': collection_counts['entomology_collection'] or '—',
            'status': 'active',
            'url': '/admin/entomology_collection',
            'color': 'warning',
            'curators': ['milos.jovic@nhmbeo.rs', 'aleksandar@nhmbeo.rs']
        },
        'mycology_collection': {
            'name': 'Миколошка збирка',
            'description': 'Колекција гљива и макромицета Балкана (Др Б. Иванчевић - 30+ година истраживања)',
            'icon': 'bi-tree',
            'count': collection_counts['mycology_collection'] or '—',
            'status': 'active',
            'url': '/admin/mycology_collection',
            'color': 'success',
            'curators': ['boris@nhmbeo.rs']
        },
        'herpetology_collection': {
            'name': 'Херпетолошка збирка',
            'description': 'Колекција водоземаца и гмизаваца - 20+ година теренских истраживања (Др А. Пауновић)',
            'icon': 'bi-slash-circle',
            'count': collection_counts['herpetology_collection'] or '—',
            'status': 'active',
            'url': '/admin/herpetology_collection',
            'color': 'danger',
            'curators': ['ana.paunovic@nhmbeo.rs']
        },
        'ornithology_collection': {
            'name': 'Орнитолошка збирка',
            'description': 'Колекција птица - Центар за маркирање (прстеновање) птица, програм Euring (Мср В. Попић)',
            'icon': 'bi-stars',
            'count': collection_counts['ornithology_collection'] or '—',
            'status': 'active',
            'url': '/admin/ornithology_collection',
            'color': 'primary',
            'curators': ['vuk.popic@nhmbeo.rs']
        },
        'zoology_collection': {
            'name': 'Општа зоолошка збирка',
            'description': 'Зоолошка колекција - молекуларна биологија и ДНК баркодирање (З. Марковић - MSc)',
            'icon': 'bi-heart',
            'count': collection_counts['zoology_collection'] or '—',
            'status': 'development',
            'url': '#',
            'color': 'info',
            'curators': ['zorana.markovic@nhmbeo.rs']
        },
        'conservation_biology': {
            'name': 'Конзервација биолошких збирки',
            'description': 'Препарација и очување биолошких експоната (Г. Петковски - конзерватор, М. Мрваљевић, Ј. Кокотовић)',
            'icon': 'bi-shield-check',
            'count': collection_counts['conservation_biology'] or '—',
            'status': 'active',
            'url': '/admin/conservation_biology',
            'color': 'secondary',
            'curators': ['gorana.petkovski@nhmbeo.rs', 'milos.mrvaljevic@nhmbeo.rs', 'jovan.kokotovic@nhmbeo.rs']
        },
        
        # CURATOR COLLECTIONS - Geology Department
        'paleozoology_collection': {
            'name': 'Палеозоолошка збирка',
            'description': 'Фосили животиња - први диносауруси Србије, крупни сисари (Др Б. Митровић - начелник, Др З. Марковић, С. Алабурић, Др Д. Ђурић, Р. Пејовић, М. Миливојевић)',
            'icon': 'bi-diagram-3',
            'count': collection_counts['paleozoology_collection'] or '—',
            'status': 'active',
            'url': '/admin/paleozoology_collection',
            'color': 'warning',
            'curators': ['biljana.mitrovic@nhmbeo.rs', 'zoran.markovic@nhmbeo.rs', 'sanja.pavic@nhmbeo.rs', 'dragana.djuric@nhmbeo.rs', 'pejovic.ranko@nhmbeo.rs', 'milos.milivojevic@nhmbeo.rs']
        },
        'paleobotany_collection': {
            'name': 'Палеоботаничка збирка',
            'description': 'Фосилне биљке и праисторијска вегетација - кустос од 1993, професор палеоекологије (Др Д. Ђорђевић-Милутиновић)',
            'icon': 'bi-flower2',
            'count': collection_counts['paleobotany_collection'] or '—',
            'status': 'active',
            'url': '/admin/paleobotany_collection',
            'color': 'success',
            'curators': ['desadjm@nhmbeo.rs']
        },
        'petrology_collection': {
            'name': 'Петролошка збирка',
            'description': 'Колекција стена Србије - петрографија и геохемија (Т. Милић Бабић - виши кустос)',
            'icon': 'bi-layers',
            'count': collection_counts['petrology_collection'] or '—',
            'status': 'active',
            'url': '/admin/petrology_collection',
            'color': 'secondary',
            'curators': ['tatjana.milicbabic@nhmbeo.rs']
        },
        'meteorite_collection': {
            'name': 'Збирка метеорита',
            'description': 'Колекција метеорита Србије - Сокобањски метеорит и други (Др А. Луковић - минералог)',
            'icon': 'bi-star-fill',
            'count': collection_counts['meteorite_collection'] or '—',
            'status': 'active',
            'url': '/admin/meteorite_collection',
            'color': 'warning',
            'curators': ['aca.lukovic@nhmbeo.rs']
        },
        'geology_conservation': {
            'name': 'Геолошка збирка и конзервација',
            'description': 'Геолошки узорци, препарација и конзервација фосила (Б. Радуловић - кустос, Н. Младеновић - конзерватор)',
            'icon': 'bi-geo-alt',
            'count': collection_counts['geology_conservation'] or '—',
            'status': 'development',
            'url': '#',
            'color': 'dark',
            'curators': ['branko.radulovic@nhmbeo.rs', 'nenad.mladenovic@nhmbeo.rs']
        }
    }

    return render_template('admin_museum_databases.html',
                          databases=databases_info,
                          total_databases=len(databases_info))

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

    return dict(
        user_logged_in=user_logged_in,
        user_name=session.get('user_name', ''),
        user_role=session.get('user_role', ''),
        user_email=session.get('user_email', ''),
        is_admin=is_admin,
        endpoint_exists=endpoint_exists
    )

# Simple app runner (complex mounting disabled for now)
def create_app():
    """Create the main application (simplified version)."""
    global LIBRARY_DATABASE

    print("📋 Using simplified museum system")
    print("⚠️ Timesheet system available via instructions")

    # Load library database from JSON
    print("📚 Loading library database...")
    LIBRARY_DATABASE = load_library_database()
    print(f"✓ Loaded {len(LIBRARY_DATABASE.get('books', []))} books")

    return app

# Route handlers for input forms

@app.route('/admin/add_book', methods=['GET', 'POST'])
@admin_required
def add_book():
    """Add new book to library database."""
    global LIBRARY_DATABASE

    # Ensure library database is loaded
    if LIBRARY_DATABASE is None:
        LIBRARY_DATABASE = load_library_database()

    if request.method == 'POST':
        # Get form data
        book_data = {
            'id': len(LIBRARY_DATABASE['books']) + 1,
            'title': request.form.get('title', '').strip(),
            'author': request.form.get('author', '').strip(),
            'isbn': request.form.get('isbn', '').strip(),
            'category': request.form.get('category', '').strip(),
            'year': int(request.form.get('year', 0)) if request.form.get('year', '').strip().isdigit() else None,
            'location': request.form.get('location', '').strip(),
            'status': request.form.get('status', 'доступна').strip(),
            'description': request.form.get('description', '').strip(),
            'pages': int(request.form.get('pages', 0)) if request.form.get('pages', '').strip().isdigit() else None,
            'publisher': request.form.get('publisher', '').strip(),
            'language': request.form.get('language', 'српски').strip()
        }

        # Add to database
        LIBRARY_DATABASE['books'].append(book_data)

        # Save to JSON file
        save_library_database()

        flash('Књига је успешно додата у библиотеку!', 'success')
        return redirect(url_for('library_database'))

    return render_template('admin_add_book.html')

@app.route('/admin/add_heritage_item', methods=['GET', 'POST'])
@admin_required
def add_heritage_item():
    """Add new heritage item to cultural heritage database."""
    if request.method == 'POST':
        # Get form data
        heritage_data = {
            'id': len(get_cultural_heritage_database()['heritage_items']) + 1,
            'name': request.form.get('name', '').strip(),
            'registry_number': request.form.get('registry_number', '').strip(),
            'type': request.form.get('type', '').strip(),
            'category': request.form.get('category', '').strip(),
            'subcategory': request.form.get('subcategory', '').strip(),
            'significance': request.form.get('significance', '').strip(),
            'location': request.form.get('location', '').strip(),
            'condition': request.form.get('condition', '').strip(),
            'protection_date': request.form.get('protection_date', '').strip(),
            'acquisition_date': request.form.get('acquisition_date', '').strip(),
            'description': request.form.get('description', '').strip(),
            'legal_basis': request.form.get('legal_basis', '').strip(),
            'cultural_value': request.form.get('cultural_value', '').strip(),
            'period': request.form.get('period', '').strip(),
            'origin': request.form.get('origin', '').strip(),
            'dimensions': request.form.get('dimensions', '').strip(),
            'material': request.form.get('material', '').strip(),
            'weight': request.form.get('weight', '').strip(),
            'protection_status': request.form.get('protection_status', 'заштићено').strip()
        }

        # Add to database
        get_cultural_heritage_database()['heritage_items'].append(heritage_data)
        flash('Културно добро је успешно додато!', 'success')
        return redirect(url_for('cultural_heritage_database'))

    return render_template('admin_add_heritage_item.html')

@app.route('/admin/add_collection_item/<collection_type>', methods=['GET', 'POST'])
@module_access_required('curator_collections')
def add_collection_item(collection_type):
    """Add new item to a curator collection."""
    # Collection info mapping
    collection_info = {
        'botany': {'name': 'Ботаничка збирка', 'route': 'botany_collection'},
        'ichthyology': {'name': 'Ихтиолошка збирка', 'route': 'ichthyology_collection'},
        'entomology': {'name': 'Ентомолошка збирка', 'route': 'entomology_collection'},
        'mycology': {'name': 'Миколошка збирка', 'route': 'mycology_collection'},
        'herpetology': {'name': 'Херпетолошка збирка', 'route': 'herpetology_collection'},
        'ornithology': {'name': 'Орнитолошка збирка', 'route': 'ornithology_collection'},
        'general_zoology': {'name': 'Општа зоологија', 'route': 'general_zoology_collection'},
        'conservation': {'name': 'Конзервација биолошких збирки', 'route': 'conservation_biology'},
        'conservation_biology': {'name': 'Конзервациона биологија', 'route': 'conservation_biology_collection'},
        'paleozoology': {'name': 'Палеозоолошка збирка', 'route': 'paleozoology_collection'},
        'paleobotany': {'name': 'Палеоботаничка збирка', 'route': 'paleobotany_collection'},
        'petrology': {'name': 'Петролошка збирка', 'route': 'petrology_collection'},
        'meteorite': {'name': 'Збирка метеорита', 'route': 'meteorite_collection'},
        'geology_conservation': {'name': 'Геолошка конзервација', 'route': 'geology_conservation_collection'}
    }

    if collection_type not in collection_info:
        flash('Непозната збирка!', 'error')
        return redirect(url_for('museum_databases'))

    if request.method == 'POST':
        # Generic collection item data structure
        item_data = {
            'id': f"{collection_type}_{int(time.time())}",  # Simple ID generation
            'catalog_number': request.form.get('catalog_number', '').strip(),
            'accession_number': request.form.get('accession_number', '').strip(),
            'scientific_name': request.form.get('scientific_name', '').strip(),
            'common_name': request.form.get('common_name', '').strip(),
            'family': request.form.get('family', '').strip(),
            'genus': request.form.get('genus', '').strip(),
            'collection_location': request.form.get('collection_location', '').strip(),
            'collection_date': request.form.get('collection_date', '').strip(),
            'collector': request.form.get('collector', '').strip(),
            'determiner': request.form.get('determiner', '').strip(),
            'description': request.form.get('description', '').strip(),
            'storage_location': request.form.get('storage_location', '').strip(),
            'preservation_method': request.form.get('preservation_method', '').strip(),
            'condition': request.form.get('condition', '').strip(),
            'completeness': request.form.get('completeness', '').strip(),
            'size': request.form.get('size', '').strip(),
            'weight': request.form.get('weight', '').strip(),
            'age': request.form.get('age', '').strip(),
            'sex': request.form.get('sex', '').strip(),
            'life_stage': request.form.get('life_stage', '').strip(),
            'research_project': request.form.get('research_project', '').strip(),
            'publications': request.form.get('publications', '').strip(),
            'special_notes': request.form.get('special_notes', '').strip(),
            # Geological specific fields
            'acquisition_method': request.form.get('acquisition_method', '').strip(),
            'storage_type': request.form.get('storage_type', '').strip(),
            'storage_conditions': request.form.get('storage_conditions', '').strip(),
            'notes': request.form.get('notes', '').strip(),
            # Petrology specific fields
            'rock_type_main': request.form.get('rock_type_main', '').strip(),
            'rock_type_subtype': request.form.get('rock_type_subtype', '').strip(),
            'mineral_composition': request.form.get('mineral_composition', '').strip(),
            'rock_texture': request.form.get('rock_texture', '').strip(),
            # Paleozoology specific fields
            'fossil_type': request.form.get('fossil_type', '').strip(),
            'anatomical_part': request.form.get('anatomical_part', '').strip(),
            'preservation_type': request.form.get('preservation_type', '').strip(),
            'sediment_type': request.form.get('sediment_type', '').strip(),
            'sediment_description': request.form.get('sediment_description', '').strip(),
            'latitude': request.form.get('latitude', '').strip(),
            'longitude': request.form.get('longitude', '').strip(),
            'formation': request.form.get('formation', '').strip(),
            'estimated_age_range': request.form.get('estimated_age_range', '').strip(),
            'biozone': request.form.get('biozone', '').strip(),
            'preparation_method': request.form.get('preparation_method', '').strip(),
            'type_status': request.form.get('type_status', '').strip(),
            # Paleobotany specific fields
            'plant_type': request.form.get('plant_type', '').strip(),
            'plant_part': request.form.get('plant_part', '').strip(),
            'leaf_morphology': request.form.get('leaf_morphology', '').strip(),
            'venation': request.form.get('venation', '').strip(),
            'paleoecology': request.form.get('paleoecology', '').strip(),
            'division': request.form.get('division', '').strip(),
            'species': request.form.get('species', '').strip(),
            # Meteorite specific fields
            'classification': request.form.get('classification', '').strip(),
            'fall_type': request.form.get('fall_type', '').strip(),
            'fall_date': request.form.get('fall_date', '').strip(),
            'total_mass': request.form.get('total_mass', '').strip(),
            'specimen_mass': request.form.get('specimen_mass', '').strip(),
            'petrologic_type': request.form.get('petrologic_type', '').strip(),
            'weathering_grade': request.form.get('weathering_grade', '').strip(),
            'shock_stage': request.form.get('shock_stage', '').strip(),
            'chemical_composition': request.form.get('chemical_composition', '').strip(),
            'mineralogy': request.form.get('mineralogy', '').strip(),
            'parent_body': request.form.get('parent_body', '').strip(),
            'meteorite_bulletin_number': request.form.get('meteorite_bulletin_number', '').strip(),
            'fragment_type': request.form.get('fragment_type', '').strip(),
            'external_appearance': request.form.get('external_appearance', '').strip(),
            'internal_structure': request.form.get('internal_structure', '').strip(),
            'fusion_crust': request.form.get('fusion_crust', '').strip(),
            'widmanstatten_pattern': request.form.get('widmanstatten_pattern', '').strip(),
            'analytical_methods': request.form.get('analytical_methods', '').strip(),
            'dating_method': request.form.get('dating_method', '').strip(),
            'cosmic_ray_exposure': request.form.get('cosmic_ray_exposure', '').strip(),
            'terrestrial_age': request.form.get('terrestrial_age', '').strip(),
            'date_added': datetime.now().strftime('%Y-%m-%d'),
            'added_by': session.get('user_email', 'system')
        }

        # Here you would normally save to a database
        # For now, we just show a success message
        flash(f'Предмет је успешно додат у збирку {collection_info[collection_type]["name"]}!', 'success')
        return redirect(url_for(collection_info[collection_type]['route']))

    # Determine which form template to use
    if collection_type == 'meteorite':
        template = 'admin_add_meteorite_item.html'
    elif collection_type == 'petrology':
        template = 'admin_add_geological_item.html'
    elif collection_type == 'paleozoology':
        template = 'admin_add_paleozoology_item.html'
    elif collection_type == 'paleobotany':
        template = 'admin_add_paleobotany_item.html'
    else:
        template = 'admin_add_collection_item.html'

    return render_template(template,
                         collection_type=collection_type,
                         collection_name=collection_info[collection_type]['name'],
                         collection_route=collection_info[collection_type]['route'])

@app.route('/admin/add_visitor', methods=['GET', 'POST'])
@admin_required
def add_visitor():
    """Add new visitor record."""
    if request.method == 'POST':
        # Get form data
        visitor_data = {
            'id': len(VISITOR_RECORDS) + 1,
            'date': request.form.get('date', '').strip(),
            'visitor_type': request.form.get('visitor_type', '').strip(),
            'group_size': int(request.form.get('group_size', 1)),
            'age_category': request.form.get('age_category', '').strip(),
            'nationality': request.form.get('nationality', 'Србија').strip(),
            'ticket_type': request.form.get('ticket_type', '').strip(),
            'guided_tour': request.form.get('guided_tour') == 'on',
            'exhibition': request.form.get('exhibition', '').strip(),
            'feedback_rating': request.form.get('feedback_rating', '').strip(),
            'notes': request.form.get('notes', '').strip()
        }

        VISITOR_RECORDS.append(visitor_data)
        flash('Посета је успешно забележена!', 'success')
        return redirect(url_for('visitors_database'))

    return render_template('admin_add_visitor.html')

@app.route('/admin/add_research', methods=['GET', 'POST'])
@admin_required
def add_research():
    """Add new research project record."""
    if request.method == 'POST':
        # Get form data
        research_data = {
            'id': len(RESEARCH_PROJECTS) + 1,
            'title': request.form.get('title', '').strip(),
            'project_code': request.form.get('project_code', '').strip(),
            'principal_investigator': request.form.get('principal_investigator', '').strip(),
            'department': request.form.get('department', '').strip(),
            'research_area': request.form.get('research_area', '').strip(),
            'start_date': request.form.get('start_date', '').strip(),
            'end_date': request.form.get('end_date', '').strip(),
            'funding_source': request.form.get('funding_source', '').strip(),
            'budget': request.form.get('budget', '').strip(),
            'status': request.form.get('status', 'У току').strip(),
            'description': request.form.get('description', '').strip(),
            'publications': request.form.get('publications', '').strip(),
            'collaborators': request.form.get('collaborators', '').strip(),
            'keywords': request.form.get('keywords', '').strip()
        }

        RESEARCH_PROJECTS.append(research_data)
        flash('Истраживачки пројекат је успешно додат!', 'success')
        return redirect(url_for('research_database'))

    return render_template('admin_add_research.html')

@app.route('/admin/visitors_database')
@admin_required
def visitors_database():
    """View visitors database."""
    return render_template('admin_visitors_database.html',
                          visitors=VISITOR_RECORDS,
                          total_visitors=len(VISITOR_RECORDS))

@app.route('/admin/research_database')
@admin_required
def research_database():
    """View research projects database."""
    return render_template('admin_research_database.html',
                          projects=RESEARCH_PROJECTS,
                          total_projects=len(RESEARCH_PROJECTS))

@app.route('/admin/bird_ringing_database')
@module_access_required('bird_ringing_database')
def bird_ringing_database_view():
    """View bird ringing database with pagination and filters."""
    try:
        # Get query parameters
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 50))
        search = request.args.get('search', '').strip() or None
        species_filter = request.args.get('species', '').strip() or None
        location_filter = request.args.get('location', '').strip() or None
        ringer_filter = request.args.get('ringer', '').strip() or None
        year_filter = request.args.get('year', '').strip() or None

        # Get records with pagination
        records, total_count, total_pages = bird_ringing_database.get_all_records(
            page=page,
            per_page=per_page,
            search=search,
            species_filter=species_filter,
            location_filter=location_filter,
            ringer_filter=ringer_filter,
            year_filter=year_filter
        )

        # Get filter options
        all_species = bird_ringing_database.get_all_species()
        all_locations = bird_ringing_database.get_all_locations()
        all_ringers = bird_ringing_database.get_all_ringers()
        all_years = bird_ringing_database.get_all_years()

        # Get statistics
        stats = bird_ringing_database.get_statistics()

        return render_template('admin_bird_ringing_database.html',
                             records=records,
                             total_count=total_count,
                             total_pages=total_pages,
                             current_page=page,
                             per_page=per_page,
                             all_species=all_species,
                             all_locations=all_locations,
                             all_ringers=all_ringers,
                             all_years=all_years,
                             stats=stats,
                             search=search or '',
                             species_filter=species_filter or '',
                             location_filter=location_filter or '',
                             ringer_filter=ringer_filter or '',
                             year_filter=year_filter or '')
    except FileNotFoundError:
        flash('База података о прстеновању птица још увек није учитана. Покрените скрипту за увоз података.', 'error')
        return redirect(url_for('museum_databases'))
    except Exception as e:
        flash(f'Грешка при учитавању базе података: {str(e)}', 'error')
        return redirect(url_for('museum_databases'))

@app.route('/admin/bird_ringing_record/<int:record_id>')
@module_access_required('bird_ringing_database')
def bird_ringing_record_detail(record_id):
    """View detailed information for a single bird ringing record."""
    try:
        record = bird_ringing_database.get_record_by_id(record_id)
        if not record:
            flash('Запис није пронађен.', 'error')
            return redirect(url_for('bird_ringing_database_view'))

        return render_template('admin_bird_ringing_detail.html', record=record)
    except Exception as e:
        flash(f'Грешка при учитавању записа: {str(e)}', 'error')
        return redirect(url_for('bird_ringing_database_view'))

@app.route('/admin/add_bird_ringing', methods=['GET', 'POST'])
@admin_required
def add_bird_ringing():
    """Add a new bird ringing record."""
    if request.method == 'POST':
        try:
            # Collect all form data
            record_data = {
                'ring_number': request.form.get('ring_number', '').strip() or None,
                'color_ring': request.form.get('color_ring', '').strip() or None,
                'species': request.form.get('species', '').strip() or None,
                'age': request.form.get('age', '').strip() or None,
                'sex': request.form.get('sex', '').strip() or None,
                'location': request.form.get('location', '').strip() or None,
                'coordinates': request.form.get('coordinates', '').strip() or None,
                'coordinate_accuracy': request.form.get('coordinate_accuracy', '').strip() or None,
                'date': request.form.get('date', '').strip() or None,
                'time': request.form.get('time', '').strip() or None,
                'metal_ring_position': request.form.get('metal_ring_position', '').strip() or None,
                'plastic_ring': request.form.get('plastic_ring', '').strip() or None,
                'catching_method': request.form.get('catching_method', '').strip() or None,
                'bait': request.form.get('bait', '').strip() or None,
                'manipulation': request.form.get('manipulation', '').strip() or None,
                'status': request.form.get('status', '').strip() or None,
                'clutch_size': request.form.get('clutch_size', '').strip() or None,
                'pullus_age': request.form.get('pullus_age', '').strip() or None,
                'wing_length': request.form.get('wing_length', '').strip() or None,
                'third_primary_feather': request.form.get('third_primary_feather', '').strip() or None,
                'mass': request.form.get('mass', '').strip() or None,
                'molting': request.form.get('molting', '').strip() or None,
                'back_claw': request.form.get('back_claw', '').strip() or None,
                'bill_length': request.form.get('bill_length', '').strip() or None,
                'bill_measurement_method': request.form.get('bill_measurement_method', '').strip() or None,
                'head_length': request.form.get('head_length', '').strip() or None,
                'tarsus': request.form.get('tarsus', '').strip() or None,
                'tarsus_measurement_method': request.form.get('tarsus_measurement_method', '').strip() or None,
                'tail_length': request.form.get('tail_length', '').strip() or None,
                'fat_deposits': request.form.get('fat_deposits', '').strip() or None,
                'pectoral_muscle': request.form.get('pectoral_muscle', '').strip() or None,
                'incubation_patch': request.form.get('incubation_patch', '').strip() or None,
                'alula': request.form.get('alula', '').strip() or None,
                'carpal_feathers': request.form.get('carpal_feathers', '').strip() or None,
                'sex_determination': request.form.get('sex_determination', '').strip() or None,
                'protected_areas': request.form.get('protected_areas', '').strip() or None,
                'ringer': request.form.get('ringer', '').strip() or None,
                'notes': request.form.get('notes', '').strip() or None
            }

            # Insert record
            record_id = bird_ringing_database.insert_record(record_data)

            flash(f'Запис о прстеновању је успешно додат! (ID: {record_id})', 'success')
            return redirect(url_for('bird_ringing_record_detail', record_id=record_id))

        except Exception as e:
            flash(f'Грешка при додавању записа: {str(e)}', 'error')
            return redirect(url_for('add_bird_ringing'))

    # GET request - show form
    try:
        # Get lists for dropdowns
        all_species = bird_ringing_database.get_all_species()
        all_locations = bird_ringing_database.get_all_locations()
        all_ringers = bird_ringing_database.get_all_ringers()

        return render_template('admin_add_bird_ringing.html',
                             all_species=all_species,
                             all_locations=all_locations,
                             all_ringers=all_ringers)
    except Exception as e:
        flash(f'Грешка при учитавању форме: {str(e)}', 'error')
        return redirect(url_for('bird_ringing_database_view'))

@app.route('/museum_terminology')
@login_required
def museum_terminology():
    """Display museum terminology page."""
    return render_template('museum_terminology.html')

@app.route('/vehicle_reservations')
@login_required
def vehicle_reservations():
    """Display vehicle reservation calendar."""
    return render_template('vehicle_reservations.html',
                         vehicles=MUSEUM_VEHICLES,
                         reservations=VEHICLE_RESERVATIONS)

@app.route('/add_vehicle_reservation', methods=['POST'])
@login_required
def add_vehicle_reservation():
    """Add new vehicle reservation."""
    global VEHICLE_RESERVATIONS

    if os.environ.get('DATABASE_URL'):
        try:
            # Add reservation to PostgreSQL
            conn = phase3a_databases.get_db_connection()
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO vehicle_reservations (
                    vehicle_id, reserved_by, purpose, start_date, end_date,
                    start_time, end_time, destination, estimated_km,
                    driver_name, driver_license, passengers, notes, status
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                int(request.form.get('vehicle_id')),
                request.form.get('employee_name', '').strip() or session.get('user_email', 'system'),
                request.form.get('purpose', '').strip(),
                request.form.get('start_date', '').strip(),
                request.form.get('end_date', '').strip(),
                request.form.get('start_time', '').strip() or None,
                request.form.get('end_time', '').strip() or None,
                request.form.get('destination', '').strip(),
                request.form.get('estimated_km', '').strip() or None,
                request.form.get('driver_name', '').strip() or None,
                request.form.get('driver_license', '').strip() or None,
                request.form.get('passengers', '').strip() or None,
                request.form.get('notes', '').strip(),
                'Активна'
            ))
            conn.commit()
            cur.close()
            conn.close()
            flash('Резервација је успешно креирана!', 'success')

            # Reload reservations list
            VEHICLE_RESERVATIONS = load_reservations()
        except Exception as e:
            logging.error(f"Error adding reservation to PostgreSQL: {e}")
            flash(f'Грешка при креирању резервације: {e}', 'error')
    else:
        # Fallback to JSON file
        reservation_data = {
            'id': len(VEHICLE_RESERVATIONS) + 1,
            'vehicle_id': int(request.form.get('vehicle_id')),
            'employee_name': request.form.get('employee_name', '').strip(),
            'start_date': request.form.get('start_date', '').strip(),
            'end_date': request.form.get('end_date', '').strip(),
            'purpose': request.form.get('purpose', '').strip(),
            'destination': request.form.get('destination', '').strip(),
            'notes': request.form.get('notes', '').strip(),
            'created_by': session.get('user_email', 'system'),
            'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }

        VEHICLE_RESERVATIONS.append(reservation_data)

        if save_reservations():
            flash('Резервација је успешно креирана!', 'success')
        else:
            flash('Грешка при чувању резервације!', 'error')

    return redirect(url_for('vehicle_reservations'))

@app.route('/vehicle_management')
@admin_required
def vehicle_management():
    """Display vehicle management page."""
    return render_template('vehicle_management.html',
                         vehicles=MUSEUM_VEHICLES,
                         reservations=VEHICLE_RESERVATIONS)

@app.route('/add_vehicle', methods=['POST'])
@admin_required
def add_vehicle():
    """Add new vehicle."""
    global MUSEUM_VEHICLES

    vehicle_data = {
        'name': request.form.get('name', '').strip(),
        'registration': request.form.get('registration', '').strip(),
        'type': request.form.get('type', '').strip(),
        'capacity': request.form.get('capacity', '').strip(),
        'status': request.form.get('status', 'Активно').strip(),
        'year': request.form.get('year', '').strip(),
        'make_model': request.form.get('make_model', '').strip(),
        'notes': request.form.get('notes', '').strip(),
        'image_ids': []
    }

    if os.environ.get('DATABASE_URL'):
        try:
            # Add vehicle to PostgreSQL
            conn = phase3a_databases.get_db_connection()
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO vehicles (
                    name, registration, type, capacity, status,
                    year, make_model, notes, image_ids
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                vehicle_data['name'],
                vehicle_data['registration'],
                vehicle_data['type'],
                vehicle_data['capacity'],
                vehicle_data['status'],
                vehicle_data['year'],
                vehicle_data['make_model'],
                vehicle_data['notes'],
                vehicle_data['image_ids']
            ))
            conn.commit()
            cur.close()
            conn.close()
            flash('Возило је успешно додато!', 'success')

            # Reload vehicles list
            MUSEUM_VEHICLES = load_vehicles()
        except Exception as e:
            logging.error(f"Error adding vehicle to PostgreSQL: {e}")
            flash(f'Грешка при додавању возила: {e}', 'error')
    else:
        # Fallback to JSON file
        vehicle_data['id'] = max([v['id'] for v in MUSEUM_VEHICLES], default=0) + 1
        MUSEUM_VEHICLES.append(vehicle_data)
        if save_vehicles():
            flash('Возило је успешно додато!', 'success')
        else:
            flash('Грешка при чувању возила!', 'error')

    return redirect(url_for('vehicle_management'))

@app.route('/edit_vehicle', methods=['POST'])
@admin_required
def edit_vehicle():
    """Edit existing vehicle."""
    global MUSEUM_VEHICLES
    vehicle_id = int(request.form.get('vehicle_id'))

    if os.environ.get('DATABASE_URL'):
        try:
            # Update vehicle in PostgreSQL
            conn = phase3a_databases.get_db_connection()
            cur = conn.cursor()
            cur.execute("""
                UPDATE vehicles SET
                    name = %s,
                    registration = %s,
                    type = %s,
                    capacity = %s,
                    status = %s,
                    year = %s,
                    make_model = %s,
                    notes = %s,
                    updated_at = now()
                WHERE id = %s
            """, (
                request.form.get('name', '').strip(),
                request.form.get('registration', '').strip(),
                request.form.get('type', '').strip(),
                request.form.get('capacity', '').strip(),
                request.form.get('status', '').strip(),
                request.form.get('year', '').strip(),
                request.form.get('make_model', '').strip(),
                request.form.get('notes', '').strip(),
                vehicle_id
            ))
            conn.commit()
            cur.close()
            conn.close()
            flash('Возило је успешно ажурирано!', 'success')

            # Reload vehicles list
            MUSEUM_VEHICLES = load_vehicles()
        except Exception as e:
            logging.error(f"Error updating vehicle in PostgreSQL: {e}")
            flash(f'Грешка при ажурирању возила: {e}', 'error')
    else:
        # Fallback to JSON file
        for vehicle in MUSEUM_VEHICLES:
            if vehicle['id'] == vehicle_id:
                vehicle['name'] = request.form.get('name', '').strip()
                vehicle['registration'] = request.form.get('registration', '').strip()
                vehicle['type'] = request.form.get('type', '').strip()
                vehicle['capacity'] = request.form.get('capacity', '').strip()
                vehicle['status'] = request.form.get('status', '').strip()
                break

        if save_vehicles():
            flash('Возило је успешно ажурирано!', 'success')
        else:
            flash('Грешка при чувању измена!', 'error')

    return redirect(url_for('vehicle_management'))

@app.route('/delete_vehicle', methods=['POST'])
@admin_required
def delete_vehicle():
    """Delete vehicle."""
    global MUSEUM_VEHICLES
    vehicle_id = int(request.form.get('vehicle_id'))

    if os.environ.get('DATABASE_URL'):
        try:
            # Check if vehicle has active reservations
            conn = phase3a_databases.get_db_connection()
            cur = conn.cursor()
            cur.execute("""
                SELECT COUNT(*) FROM vehicle_reservations
                WHERE vehicle_id = %s
                AND status = 'Активна'
                AND end_date >= CURRENT_DATE
            """, (vehicle_id,))
            active_count = cur.fetchone()[0]

            if active_count > 0:
                flash('Не можете обрисати возило које има активне резервације!', 'error')
            else:
                # Delete vehicle from PostgreSQL (CASCADE will delete related reservations)
                cur.execute("DELETE FROM vehicles WHERE id = %s", (vehicle_id,))
                conn.commit()
                flash('Возило је успешно обрисано!', 'success')

                # Reload vehicles list
                MUSEUM_VEHICLES = load_vehicles()

            cur.close()
            conn.close()
        except Exception as e:
            logging.error(f"Error deleting vehicle from PostgreSQL: {e}")
            flash(f'Грешка при брисању возила: {e}', 'error')
    else:
        # Fallback to JSON file
        active_reservations = [r for r in VEHICLE_RESERVATIONS
                              if r['vehicle_id'] == vehicle_id and r['end_date'] >= datetime.now().strftime('%Y-%m-%d')]

        if active_reservations:
            flash('Не можете обрисати возило које има активне резервације!', 'error')
        else:
            MUSEUM_VEHICLES = [v for v in MUSEUM_VEHICLES if v['id'] != vehicle_id]

            if save_vehicles():
                flash('Возило је успешно обрисано!', 'success')
            else:
                flash('Грешка при чувању измена!', 'error')

    return redirect(url_for('vehicle_management'))

# Public QR Code View Route (No authentication required)
@app.route('/qr_view/<collection_type>/<catalog_number>')
def qr_view_specimen(collection_type, catalog_number):
    """Public mobile-optimized view for QR code scanned specimens."""
    from datetime import datetime

    # Get URL parameters
    fields_param = request.args.get('fields', 'all')
    display_mode = request.args.get('mode', 'card')
    show_image = request.args.get('img', '1') == '1'

    # Parse selected fields
    if fields_param == 'all':
        selected_fields = None  # Show all fields
    else:
        selected_fields = fields_param.split(',')

    # Field labels for display
    field_labels = {
        'catalog_number': 'Каталошки број',
        'meteorite_name': 'Назив метеорита',
        'scientific_name': 'Научно име',
        'common_name_sr': 'Народно име',
        'classification': 'Класификација',
        'fall_type': 'Тип пада',
        'fall_date': 'Датум пада',
        'location_found': 'Локација налаза',
        'total_mass_kg': 'Укупна маса (kg)',
        'specimen_mass': 'Маса примерка (g)',
        'description': 'Опис',
        'source': 'Извор',
        'curator': 'Кустос',
        'family': 'Фамилија',
        'habitat': 'Станиште',
        'date_collected': 'Датум прикупљања',
        'collector': 'Сакупљач',
        'conservation_status': 'Статус заштите',
        'geological_period': 'Геолошки период',
        'age_million_years': 'Старост (милиони година)',
        'class': 'Класа',
        'order': 'Ред',
        'acquisition_date': 'Датум набавке',
        'quantity': 'Количина',
        'condition': 'Стање',
        'serbian_meteorite': 'Српски метеорит'
    }

    # Collection names
    collection_names = {
        'meteorites': 'Збирка метеорита',
        'botany': 'Ботаничка збирка',
        'paleozoology': 'Палеозоолошка збирка',
        'paleobotany': 'Палеоботаничка збирка'
    }

    # Collection URLs
    collection_urls = {
        'meteorites': '/admin/meteorite_collection',
        'botany': '/admin/botany_collection',
        'paleozoology': '/admin/paleozoology_collection',
        'paleobotany': '/admin/paleobotany_collection'
    }

    # Title fields (what to use as the main title)
    title_fields = {
        'meteorites': 'meteorite_name',
        'botany': 'scientific_name',
        'paleozoology': 'scientific_name',
        'paleobotany': 'scientific_name'
    }

    specimen = None

    # Find the specimen
    try:
        if collection_type == 'meteorites':
            for spec in get_meteorite_collection_database()['specimens']:
                if spec.get('catalog_number') == catalog_number:
                    specimen = spec
                    break

        elif collection_type == 'botany':
            for spec in BOTANY_COLLECTION_DATABASE['specimens']:
                if spec.get('catalog_number') == catalog_number:
                    specimen = spec
                    break

        elif collection_type == 'paleozoology':
            for spec in PALEOZOOLOGY_COLLECTION_DATABASE['specimens']:
                if spec.get('catalog_number') == catalog_number:
                    specimen = spec
                    break

        if not specimen:
            return render_template('error.html',
                                 error_title='Примерак није пронађен',
                                 error_message=f'Примерак са каталошким бројем {catalog_number} није пронађен у систему.'), 404

        # Filter fields if specified
        displayed_fields = {}
        if selected_fields:
            for field in selected_fields:
                if field in specimen:
                    value = specimen[field]
                    # Format boolean values
                    if isinstance(value, bool):
                        value = 'Да' if value else 'Не'
                    displayed_fields[field] = value
        else:
            # Show all fields
            for key, value in specimen.items():
                if value is not None and value != '':
                    if isinstance(value, bool):
                        value = 'Да' if value else 'Не'
                    displayed_fields[key] = value

        # Get image URL
        db_name_map = {
            'meteorites': 'meteorites',
            'botany': 'botany',
            'paleozoology': 'paleozoology'
        }

        entity_id = specimen.get('catalog_number', catalog_number)
        db_name = db_name_map.get(collection_type, collection_type)
        image_url = f"/api/specimen_image/{db_name}/{collection_type}/{entity_id}"

        # Render the mobile-friendly template
        return render_template('specimen_qr_view.html',
                             specimen=specimen,
                             displayed_fields=displayed_fields,
                             field_labels=field_labels,
                             catalog_number=catalog_number,
                             collection_name=collection_names.get(collection_type, collection_type),
                             collection_url=collection_urls.get(collection_type, '/'),
                             title_field=title_fields.get(collection_type, 'catalog_number'),
                             display_mode=display_mode,
                             show_image=show_image,
                             image_url=image_url,
                             scan_time=datetime.now().strftime('%d.%m.%Y %H:%M'))

    except Exception as e:
        logging.error(f"Error displaying QR view: {e}")
        return render_template('error.html',
                             error_title='Грешка',
                             error_message=f'Дошло је до грешке при приказу примерка: {str(e)}'), 500


# ============================================================================
# AI ASSISTANT ROUTES
# ============================================================================

@app.route('/admin/ai_assistant')
@login_required
def ai_assistant():
    """AI Assistant page."""
    assistant = get_museum_assistant()
    provider_info = assistant.get_provider_info()
    provider_available = assistant.check_provider()

    return render_template('admin_ai_assistant.html',
                         ollama_available=provider_available,  # Keep variable name for template compatibility
                         model=provider_info.get('model', 'Not configured'),
                         context_size=16384,
                         provider_name=provider_info.get('name', 'No provider'))


@app.route('/admin/ai_api_config')
@admin_required
def ai_api_config():
    """AI API configuration page - Admin only."""
    from ai_api_providers import load_providers

    data = load_providers()
    providers = data.get('providers', [])
    active_provider_id = data.get('active_provider_id')

    active_provider = None
    if active_provider_id:
        active_provider = next((p for p in providers if p.get('id') == active_provider_id), None)

    return render_template('admin_ai_api_config.html',
                         providers=providers,
                         active_provider_id=active_provider_id,
                         active_provider=active_provider)


@app.route('/api/llm/chat', methods=['POST'])
@login_required
def llm_chat():
    """Chat with AI assistant."""
    try:
        data = request.get_json()
        message = data.get('message', '').strip()

        if not message:
            return {'success': False, 'error': 'Порука је празна'}, 400

        assistant = get_museum_assistant()
        result = assistant.chat(message, include_context=True)

        return result, 200 if result['success'] else 500

    except Exception as e:
        logging.error(f"LLM chat error: {e}")
        return {'success': False, 'error': str(e)}, 500


@app.route('/api/llm/context/mineral/<int:mineral_id>', methods=['POST'])
@login_required
def llm_add_mineral_context(mineral_id):
    """Add mineral to AI context."""
    try:
        mineral_db = get_mineral_database()
        mineral = mineral_db.get_mineral_by_id(mineral_id)

        if not mineral:
            return {'success': False, 'error': 'Минерал није пронађен'}, 404

        assistant = get_museum_assistant()
        success = assistant.add_artifact_context('mineral', mineral)

        if success:
            return {
                'success': True,
                'message': f'Минерал "{mineral.get("naziv", "")}" додат у контекст',
                'context_usage': assistant.get_context_usage()
            }
        else:
            return {'success': False, 'error': 'Грешка при додавању минерала'}, 500

    except Exception as e:
        logging.error(f"Error adding mineral context: {e}")
        return {'success': False, 'error': str(e)}, 500


@app.route('/api/llm/context/book/<book_id>', methods=['POST'])
@login_required
def llm_add_book_context(book_id):
    """Add library book to AI context."""
    try:
        library_db = get_library_database()
        book = next((b for b in library_db.get('books', []) if str(b.get('id')) == str(book_id)), None)

        if not book:
            return {'success': False, 'error': 'Књига није пронађена'}, 404

        assistant = get_museum_assistant()
        success = assistant.add_artifact_context('book', book)

        if success:
            return {
                'success': True,
                'message': f'Књига "{book.get("title", "")}" додата у контекст',
                'context_usage': assistant.get_context_usage()
            }
        else:
            return {'success': False, 'error': 'Грешка при додавању књиге'}, 500

    except Exception as e:
        logging.error(f"Error adding book context: {e}")
        return {'success': False, 'error': str(e)}, 500


@app.route('/api/llm/context/bird_ringing/<int:record_id>', methods=['POST'])
@login_required
def llm_add_bird_ringing_context(record_id):
    """Add bird ringing record to AI context."""
    try:
        record = bird_ringing_database.get_record_by_id(record_id)

        if not record:
            return {'success': False, 'error': 'Запис није пронађен'}, 404

        assistant = get_museum_assistant()
        success = assistant.add_artifact_context('bird_ringing', record)

        if success:
            return {
                'success': True,
                'message': f'Запис о прстенацији додат у контекст',
                'context_usage': assistant.get_context_usage()
            }
        else:
            return {'success': False, 'error': 'Грешка при додавању записа'}, 500

    except Exception as e:
        logging.error(f"Error adding bird ringing context: {e}")
        return {'success': False, 'error': str(e)}, 500


@app.route('/api/llm/context/clear', methods=['POST'])
@login_required
def llm_clear_context():
    """Clear AI conversation context."""
    try:
        assistant = get_museum_assistant()
        assistant.clear_context()

        return {
            'success': True,
            'message': 'Контекст обрисан',
            'context_usage': assistant.get_context_usage()
        }

    except Exception as e:
        logging.error(f"Error clearing context: {e}")
        return {'success': False, 'error': str(e)}, 500


@app.route('/api/llm/context/usage', methods=['GET'])
@login_required
def llm_context_usage():
    """Get current context usage."""
    try:
        assistant = get_museum_assistant()
        return {
            'success': True,
            'usage': assistant.get_context_usage()
        }

    except Exception as e:
        logging.error(f"Error getting context usage: {e}")
        return {'success': False, 'error': str(e)}, 500


@app.route('/api/llm/search', methods=['POST'])
@login_required
def llm_search():
    """Natural language search for artifacts."""
    try:
        data = request.get_json()
        query = data.get('query', '').strip()

        if not query:
            return {'success': False, 'error': 'Упит је празан'}, 400

        assistant = get_museum_assistant()
        result = assistant.search_artifacts_nl(query)

        return result, 200 if result['success'] else 500

    except Exception as e:
        logging.error(f"LLM search error: {e}")
        return {'success': False, 'error': str(e)}, 500


# ============================================================================
# AI API PROVIDER MANAGEMENT ROUTES
# ============================================================================

@app.route('/api/ai/providers', methods=['GET'])
@admin_required
def get_providers():
    """Get all configured AI providers - Admin only."""
    try:
        from ai_api_providers import load_providers
        data = load_providers()
        return {'success': True, 'providers': data.get('providers', [])}, 200
    except Exception as e:
        logging.error(f"Error loading providers: {e}")
        return {'success': False, 'error': str(e)}, 500


@app.route('/api/ai/providers/<provider_id>', methods=['GET'])
@admin_required
def get_provider(provider_id):
    """Get specific provider configuration - Admin only."""
    try:
        from ai_api_providers import load_providers
        data = load_providers()
        provider = next((p for p in data.get('providers', []) if p.get('id') == provider_id), None)

        if not provider:
            return {'success': False, 'error': 'Provider not found'}, 404

        return {'success': True, 'provider': provider}, 200
    except Exception as e:
        logging.error(f"Error loading provider: {e}")
        return {'success': False, 'error': str(e)}, 500


@app.route('/api/ai/providers', methods=['POST'])
@admin_required
def add_provider():
    """Add new AI provider - Admin only."""
    try:
        from ai_api_providers import load_providers, save_providers
        import uuid

        data = request.get_json()

        # Validate required fields
        required_fields = ['name', 'type', 'api_key', 'model']
        for field in required_fields:
            if not data.get(field):
                return {'success': False, 'error': f'Missing required field: {field}'}, 400

        # Generate unique ID
        provider_id = str(uuid.uuid4())

        # Create provider config
        provider = {
            'id': provider_id,
            'name': data['name'],
            'type': data['type'],
            'api_key': data['api_key'],
            'model': data['model']
        }

        # Optional fields
        if data.get('api_base'):
            provider['api_base'] = data['api_base']
        if data.get('auth_header'):
            provider['auth_header'] = data['auth_header']
        if data.get('auth_prefix'):
            provider['auth_prefix'] = data['auth_prefix']
        if data.get('api_version'):
            provider['api_version'] = data['api_version']
        if data.get('site_url'):
            provider['site_url'] = data['site_url']
        if data.get('site_name'):
            provider['site_name'] = data['site_name']

        # Load existing providers
        providers_data = load_providers()
        providers_data['providers'].append(provider)

        # If this is the first provider, activate it
        if not providers_data.get('active_provider_id'):
            providers_data['active_provider_id'] = provider_id

        # Save
        if save_providers(providers_data):
            return {'success': True, 'provider_id': provider_id}, 201
        else:
            return {'success': False, 'error': 'Failed to save provider'}, 500

    except Exception as e:
        logging.error(f"Error adding provider: {e}")
        return {'success': False, 'error': str(e)}, 500


@app.route('/api/ai/providers/<provider_id>', methods=['PUT'])
@admin_required
def update_provider(provider_id):
    """Update existing AI provider - Admin only."""
    try:
        from ai_api_providers import load_providers, save_providers

        data = request.get_json()

        # Load existing providers
        providers_data = load_providers()
        provider = next((p for p in providers_data['providers'] if p.get('id') == provider_id), None)

        if not provider:
            return {'success': False, 'error': 'Provider not found'}, 404

        # Update fields
        if data.get('name'):
            provider['name'] = data['name']
        if data.get('type'):
            provider['type'] = data['type']
        if data.get('api_key'):
            provider['api_key'] = data['api_key']
        if data.get('model'):
            provider['model'] = data['model']
        if data.get('api_base'):
            provider['api_base'] = data['api_base']
        if data.get('auth_header'):
            provider['auth_header'] = data['auth_header']
        if data.get('auth_prefix'):
            provider['auth_prefix'] = data['auth_prefix']
        if data.get('api_version'):
            provider['api_version'] = data['api_version']
        if data.get('site_url'):
            provider['site_url'] = data['site_url']
        if data.get('site_name'):
            provider['site_name'] = data['site_name']

        # Save
        if save_providers(providers_data):
            return {'success': True}, 200
        else:
            return {'success': False, 'error': 'Failed to save provider'}, 500

    except Exception as e:
        logging.error(f"Error updating provider: {e}")
        return {'success': False, 'error': str(e)}, 500


@app.route('/api/ai/providers/<provider_id>', methods=['DELETE'])
@admin_required
def delete_provider(provider_id):
    """Delete AI provider - Admin only."""
    try:
        from ai_api_providers import load_providers, save_providers

        # Load existing providers
        providers_data = load_providers()
        providers_data['providers'] = [p for p in providers_data['providers'] if p.get('id') != provider_id]

        # If deleted provider was active, clear active provider
        if providers_data.get('active_provider_id') == provider_id:
            providers_data['active_provider_id'] = None
            # Activate first available provider if any
            if providers_data['providers']:
                providers_data['active_provider_id'] = providers_data['providers'][0]['id']

        # Save
        if save_providers(providers_data):
            return {'success': True}, 200
        else:
            return {'success': False, 'error': 'Failed to save providers'}, 500

    except Exception as e:
        logging.error(f"Error deleting provider: {e}")
        return {'success': False, 'error': str(e)}, 500


@app.route('/api/ai/providers/<provider_id>/activate', methods=['POST'])
@admin_required
def activate_provider(provider_id):
    """Activate AI provider - Admin only."""
    try:
        from ai_api_providers import load_providers, save_providers

        # Load existing providers
        providers_data = load_providers()

        # Check if provider exists
        provider_exists = any(p.get('id') == provider_id for p in providers_data['providers'])
        if not provider_exists:
            return {'success': False, 'error': 'Provider not found'}, 404

        # Set as active
        providers_data['active_provider_id'] = provider_id

        # Save
        if save_providers(providers_data):
            return {'success': True}, 200
        else:
            return {'success': False, 'error': 'Failed to activate provider'}, 500

    except Exception as e:
        logging.error(f"Error activating provider: {e}")
        return {'success': False, 'error': str(e)}, 500


@app.route('/api/ai/providers/<provider_id>/test', methods=['POST'])
@admin_required
def test_provider(provider_id):
    """Test AI provider connection - Admin only."""
    try:
        from ai_api_providers import load_providers, create_provider

        # Load providers
        providers_data = load_providers()
        provider_config = next((p for p in providers_data['providers'] if p.get('id') == provider_id), None)

        if not provider_config:
            return {'success': False, 'error': 'Provider not found'}, 404

        # Create provider instance
        provider = create_provider(provider_config)
        if not provider:
            return {'success': False, 'error': 'Invalid provider configuration'}, 400

        # Test connection
        connection_ok = provider.check_connection()

        return {'success': connection_ok, 'error': None if connection_ok else 'Connection failed'}, 200

    except Exception as e:
        logging.error(f"Error testing provider: {e}")
        return {'success': False, 'error': str(e)}, 500


@app.route('/api/ai/providers/fetch_models', methods=['POST'])
@admin_required
def fetch_provider_models():
    """Fetch available models from provider API - Admin only."""
    try:
        from ai_api_providers import create_provider

        data = request.get_json()
        provider_type = data.get('type')
        api_key = data.get('api_key')
        api_base = data.get('api_base')

        if not provider_type or not api_key:
            return {'success': False, 'error': 'Missing type or api_key'}, 400

        # Create temporary provider config
        temp_config = {
            'id': 'temp',
            'name': 'temp',
            'type': provider_type,
            'api_key': api_key,
            'model': 'temp'  # Placeholder
        }

        if api_base:
            temp_config['api_base'] = api_base

        # Create provider instance
        provider = create_provider(temp_config)
        if not provider:
            return {'success': False, 'error': 'Invalid provider type'}, 400

        # Get models
        models = provider.get_models()

        return {'success': True, 'models': models}, 200

    except Exception as e:
        logging.error(f"Error fetching models: {e}")
        return {'success': False, 'error': str(e)}, 500



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
