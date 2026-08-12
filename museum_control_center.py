#!/usr/bin/env python3
"""
Museum Information System - Unified Control Center
Comprehensive desktop control panel for all museum system services
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, simpledialog
import subprocess
import os
import signal
import shutil
import queue
import json
import psutil
import threading
import time
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse
import requests
import secrets
import string


PROJECT_ROOT = Path(__file__).resolve().parent
POSTGRES_CONTROL_ROOT = Path('/home/aleksandarlukovic/PostgresControlApp')
POSTGRES_CONTROL_PORT = 5075
POSTGRES_CONTROL_URL = f'http://127.0.0.1:{POSTGRES_CONTROL_PORT}'
SYSTEMD_UNIT_DIRS = (
    Path('/etc/systemd/system'),
    Path('/usr/lib/systemd/system'),
    Path('/lib/systemd/system'),
)
QA_ENV_FILE = PROJECT_ROOT / '.env.qa'
QA_REQUIRED_CYPRESS_ENV_VARS = (
    'CYPRESS_ADMIN_EMAIL',
    'CYPRESS_ADMIN_PASSWORD',
    'CYPRESS_EMPLOYEE_EMAIL',
    'CYPRESS_EMPLOYEE_PASSWORD',
)
QA_OPTIONAL_ENV_VARS = (
    'CYPRESS_FIRST_LOGIN_EMAIL',
    'CYPRESS_FIRST_LOGIN_PASSWORD',
    'CYPRESS_RESET_TARGET_EMAIL',
    'CYPRESS_ARCHIVE_EMAIL',
    'CYPRESS_ARCHIVE_PASSWORD',
)
QA_EMAIL_FIELDS = (
    'CYPRESS_ADMIN_EMAIL',
    'CYPRESS_EMPLOYEE_EMAIL',
    'CYPRESS_FIRST_LOGIN_EMAIL',
    'CYPRESS_RESET_TARGET_EMAIL',
    'CYPRESS_ARCHIVE_EMAIL',
)


def load_env_values(env_path=None):
    """Read simple KEY=VALUE pairs from a local .env file."""
    env_file = Path(env_path or PROJECT_ROOT / '.env')
    values = {}

    if not env_file.exists():
        return values

    def strip_inline_comment(value):
        in_single = False
        in_double = False

        for idx, char in enumerate(value):
            if char == "'" and not in_double:
                in_single = not in_single
            elif char == '"' and not in_single:
                in_double = not in_double
            elif char == '#' and not in_single and not in_double:
                if idx == 0 or value[idx - 1].isspace():
                    return value[:idx].rstrip()

        return value.strip()

    for raw_line in env_file.read_text(encoding='utf-8').splitlines():
        line = raw_line.strip()
        if not line or line.startswith('#') or '=' not in line:
            continue
        key, value = line.split('=', 1)
        value = strip_inline_comment(value.strip())
        if len(value) >= 2 and value[0] == value[-1] and value[0] in ('"', "'"):
            value = value[1:-1]
        values[key.strip()] = value

    return values


def systemd_unit_exists(unit_name):
    return any((unit_dir / f'{unit_name}.service').exists() for unit_dir in SYSTEMD_UNIT_DIRS)


def production_uses_local_cache(env_path=None):
    env_values = load_env_values(env_path)
    session_type = (
        env_values.get('SESSION_TYPE')
        or os.environ.get('SESSION_TYPE')
        or 'filesystem'
    ).lower()

    if session_type != 'redis':
        return False

    redis_url = env_values.get('REDIS_URL') or os.environ.get('REDIS_URL') or 'redis://localhost:6379/0'
    parsed = urlparse(redis_url)

    if parsed.scheme == 'unix':
        return True

    hostname = (parsed.hostname or '').lower()
    return hostname in ('', 'localhost', '127.0.0.1')


def detect_cache_service(env_path=None):
    if not production_uses_local_cache(env_path):
        return None

    candidates = (
        ('valkey', 'valkey-server', 'Valkey / Redis Cache'),
        ('redis', 'redis-server', 'Redis Cache'),
        ('redis-server', 'redis-server', 'Redis Cache'),
    )

    for systemd_service, executable, name in candidates:
        if systemd_unit_exists(systemd_service) and shutil.which(executable):
            return {
                'name': name,
                'port': 6379,
                'path': '/var/lib/redis',
                'service_type': 'systemd',
                'systemd_service': systemd_service,
                'log': None,
                'icon': '🧠',
                'status': 'stopped',
                'description': 'Локални Redis-компатибилни кеш за продукциони рад',
                'order': 2,
                'bulk_start': True,
            }

    return None


def build_services_config(project_root=None, env_path=None):
    root = Path(project_root or PROJECT_ROOT)

    services = {
        'postgresql': {
            'name': 'PostgreSQL База података',
            'port': 5432,
            'path': '/var/lib/pgsql',
            'service_type': 'systemd',
            'systemd_service': 'postgresql',
            'log': None,
            'icon': '🐘',
            'status': 'stopped',
            'description': 'PostgreSQL сервер за све музејске базе података',
            'order': 1,
            'bulk_start': True,
        },
        'museum_system': {
            'name': 'Музејски Информациони Систем',
            'port': 8000,
            'path': str(root),
            'service_type': 'systemd',
            'systemd_service': 'museum-system',
            'log': 'logs/gunicorn_error.log',
            'icon': '🏛️',
            'status': 'stopped',
            'description': 'Главни музејски систем (укључује базу минерала и радне листе)',
            'order': 3,
            'bulk_start': True,
        },
        'nginx': {
            'name': 'Nginx Web Server',
            'port': 80,
            'path': '/etc/nginx',
            'service_type': 'systemd',
            'systemd_service': 'nginx',
            'log': '/var/log/nginx/museum_error.log',
            'icon': '🌐',
            'status': 'stopped',
            'description': 'Веб сервер који служи музејски систем на порту 80',
            'order': 4,
            'bulk_start': True,
        },
        'main_app_dev': {
            'name': 'Развојни Сервер (Dev Mode)',
            'port': 5000,
            'path': str(root),
            'command': ['python3', 'app.py'],
            'log': 'logs/main_app.log',
            'pid_file': 'logs/main_app.pid',
            'icon': '🔧',
            'status': 'stopped',
            'service_type': 'process',
            'description': 'Само за развој и тестирање (не користити у продукцији)',
            'order': 99,
            'bulk_start': False,
        }
    }

    cache_service = detect_cache_service(env_path or root / '.env')
    if cache_service:
        services['cache'] = cache_service

    return services


def build_qa_environment(env_path=None, overrides=None):
    env = os.environ.copy()
    env.update(load_env_values(env_path))
    env.update(load_env_values(QA_ENV_FILE))
    env['PYTHONUNBUFFERED'] = '1'
    env['TERM'] = env.get('TERM', 'dumb')

    if overrides:
        env.update({key: str(value) for key, value in overrides.items()})

    if not env.get('CYPRESS_ADMIN_EMAIL') and env.get('ADMIN_EMAIL'):
        env['CYPRESS_ADMIN_EMAIL'] = env['ADMIN_EMAIL']
    if not env.get('CYPRESS_ARCHIVE_EMAIL') and env.get('CYPRESS_EMPLOYEE_EMAIL'):
        env['CYPRESS_ARCHIVE_EMAIL'] = env['CYPRESS_EMPLOYEE_EMAIL']
    if not env.get('CYPRESS_ARCHIVE_PASSWORD') and env.get('CYPRESS_EMPLOYEE_PASSWORD'):
        env['CYPRESS_ARCHIVE_PASSWORD'] = env['CYPRESS_EMPLOYEE_PASSWORD']

    return env


def get_missing_qa_env_vars(env):
    return [var_name for var_name in QA_REQUIRED_CYPRESS_ENV_VARS if not env.get(var_name)]


def qa_run_needs_browser_credentials(options):
    return str(options.get('QA_INCLUDE_CYPRESS', '1')) == '1'


def is_email_candidate(value):
    if not value:
        return False
    value = str(value).strip()
    return '@' in value and '.' in value.split('@', 1)[-1]


def load_employee_directory_entries(directory_path=None):
    directory_file = Path(directory_path or PROJECT_ROOT / 'data' / 'employee_directory.json')
    if not directory_file.exists():
        return []

    try:
        data = json.loads(directory_file.read_text(encoding='utf-8'))
    except (OSError, json.JSONDecodeError):
        return []

    return data if isinstance(data, list) else []


def build_qa_email_defaults(env, directory_entries=None, db_rows=None):
    defaults = {}
    rows = db_rows or []
    entries = directory_entries or []

    admin_email = env.get('CYPRESS_ADMIN_EMAIL')
    if not is_email_candidate(admin_email):
        admin_email = env.get('ADMIN_EMAIL')
    if not is_email_candidate(admin_email):
        for role, email in rows:
            if role == 'admin' and is_email_candidate(email):
                admin_email = email
                break
    if not is_email_candidate(admin_email):
        for entry in entries:
            role = str(entry.get('role', '')).strip().lower()
            email = entry.get('email', '')
            if role == 'admin' and is_email_candidate(email):
                admin_email = email
                break
    if is_email_candidate(admin_email):
        defaults['CYPRESS_ADMIN_EMAIL'] = admin_email.strip()

    employee_email = env.get('CYPRESS_EMPLOYEE_EMAIL')
    if not is_email_candidate(employee_email):
        for role, email in rows:
            if role != 'admin' and is_email_candidate(email):
                employee_email = email
                break
    if not is_email_candidate(employee_email):
        for entry in entries:
            role = str(entry.get('role', '')).strip().lower()
            email = entry.get('email', '')
            if role != 'admin' and is_email_candidate(email):
                employee_email = email
                break
    if is_email_candidate(employee_email):
        employee_email = employee_email.strip()
        defaults['CYPRESS_EMPLOYEE_EMAIL'] = employee_email
        defaults['CYPRESS_FIRST_LOGIN_EMAIL'] = env.get('CYPRESS_FIRST_LOGIN_EMAIL', '').strip() or employee_email
        defaults['CYPRESS_RESET_TARGET_EMAIL'] = env.get('CYPRESS_RESET_TARGET_EMAIL', '').strip() or employee_email
        defaults['CYPRESS_ARCHIVE_EMAIL'] = env.get('CYPRESS_ARCHIVE_EMAIL', '').strip() or employee_email

    return defaults


def hash_password_for_storage(password):
    """Hash a password in-process and return (password_hash, salt).

    Hashing happens in-process via PasswordHasher so the password is never
    templated into a python3 -c source string (which would allow code
    injection for passwords containing quotes, backslashes or newlines).
    """
    import sys as _sys

    project_root = str(PROJECT_ROOT)
    if project_root not in _sys.path:
        _sys.path.insert(0, project_root)
    from security_utils import PasswordHasher

    return PasswordHasher.hash_password(password)


# PostgreSQL identity for the psql calls below. Defaults match the current dev
# box; override on the new server (where the 'aleksandarlukovic' role won't
# exist) via env, e.g. MUSEUM_DB_USER=museum_app MUSEUM_DB_NAME=museum_system.
_DB_USER = os.environ.get('MUSEUM_DB_USER', 'aleksandarlukovic')
_DB_NAME = os.environ.get('MUSEUM_DB_NAME', 'museum_system')


def build_user_update_command(set_clause, email, variables=None):
    """Build a (psql argv, sql) pair for an UPDATE on users keyed by email.

    Dynamic values are passed as psql variables via -v and referenced inside
    the SQL through the auto-escaping :'name' form, so no user-controlled
    value is interpolated into the SQL text (prevents SQL injection).
    set_clause must reference any extra values via :'name' placeholders.

    The SQL is returned separately (NOT appended via -c) because psql only
    expands :'name' / :name bindings when the statement is read from stdin or
    -f; the caller must feed the returned sql to psql via stdin.
    """
    command = ['psql', '-U', _DB_USER, '-d', _DB_NAME]

    bindings = {'target_email': email}
    if variables:
        bindings.update(variables)

    for name, value in bindings.items():
        command.extend(['-v', f"{name}={value}"])

    sql = f"UPDATE users SET {set_clause} WHERE email = :'target_email'"
    return command, sql


class MuseumControlCenter:
    def __init__(self, root):
        self.root = root
        self.root.title("Центар за контролу - Информациони систем музеја")
        self.root.geometry("1200x800")

        # Cache for sudo password (valid for session)
        self.sudo_password = None
        self.qa_process = None
        self.qa_output_queue = queue.Queue()
        self.qa_log_handle = None
        self.qa_log_path = PROJECT_ROOT / 'logs' / 'control_center_qa.log'
        self.qa_credential_vars = {}
        
        self.services = build_services_config()
        
        self.setup_ui()
        self.update_status_thread = threading.Thread(target=self.auto_update_status, daemon=True)
        self.update_status_thread.start()
    
    def setup_ui(self):
        """Setup the main UI"""
        # Header
        header = tk.Frame(self.root, bg='#2c5d84', height=80)
        header.pack(fill='x')
        header.pack_propagate(False)
        
        title = tk.Label(
            header,
            text="🏛️ Центар за контролу - Информациони систем Природњачког музеја",
            font=('Arial', 16, 'bold'),
            bg='#2c5d84',
            fg='white'
        )
        title.pack(pady=10)

        # Access info
        access_info = tk.Label(
            header,
            text="Приступ систему: http://192.168.144.48 (LAN) • http://localhost (локално)",
            font=('Arial', 10),
            bg='#2c5d84',
            fg='#B0E0E6'
        )
        access_info.pack()
        
        # Main content area with tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Tab 1: Service Control
        self.services_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.services_tab, text='  Сервиси  ')
        self.setup_services_tab()
        
        # Tab 2: Logs
        self.logs_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.logs_tab, text='  Логови  ')
        self.setup_logs_tab()
        
        # Tab 3: System Info
        self.info_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.info_tab, text='  Системске информације  ')
        self.setup_info_tab()
        
        # Tab 4: Database Management
        self.db_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.db_tab, text='  Базе података  ')
        self.setup_database_tab()

        # Tab 5: QA Test Suite
        self.qa_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.qa_tab, text='  QA  ')
        self.setup_qa_tab()

        # Tab 6: User Management / Password Manager
        self.users_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.users_tab, text='  Корисници  ')
        self.setup_users_tab()
        
        # Status bar
        self.status_bar = tk.Label(
            self.root,
            text="Спреман",
            bd=1,
            relief=tk.SUNKEN,
            anchor=tk.W,
            font=('Arial', 9)
        )
        self.status_bar.pack(side='bottom', fill='x')
        
        # Quick action buttons at bottom
        button_frame = tk.Frame(self.root)
        button_frame.pack(side='bottom', fill='x', padx=10, pady=5)
        
        tk.Button(
            button_frame,
            text="🚀 Покрени све сервисе",
            command=self.start_all_services,
            bg='#4CAF50',
            fg='white',
            font=('Arial', 10, 'bold'),
            padx=20,
            pady=5
        ).pack(side='left', padx=5)
        
        tk.Button(
            button_frame,
            text="⏹️ Заустави све сервисе",
            command=self.stop_all_services,
            bg='#f44336',
            fg='white',
            font=('Arial', 10, 'bold'),
            padx=20,
            pady=5
        ).pack(side='left', padx=5)
        
        tk.Button(
            button_frame,
            text="🔄 Рестартуј све",
            command=self.restart_all_services,
            bg='#FF9800',
            fg='white',
            font=('Arial', 10, 'bold'),
            padx=20,
            pady=5
        ).pack(side='left', padx=5)

        tk.Button(
            button_frame,
            text="🔑 Ресетуј лозинку",
            command=self.clear_sudo_password,
            bg='#9E9E9E',
            fg='white',
            font=('Arial', 10, 'bold'),
            padx=20,
            pady=5
        ).pack(side='right', padx=5)

        tk.Button(
            button_frame,
            text="⚙️ Инсталирај сервисе",
            command=self.install_systemd_services,
            bg='#673AB7',
            fg='white',
            font=('Arial', 10, 'bold'),
            padx=20,
            pady=5
        ).pack(side='right', padx=5)

        tk.Button(
            button_frame,
            text="🌐 Поправи Nginx",
            command=self.fix_nginx_config,
            bg='#00BCD4',
            fg='white',
            font=('Arial', 10, 'bold'),
            padx=20,
            pady=5
        ).pack(side='right', padx=5)

        self.root.protocol('WM_DELETE_WINDOW', self.on_window_close)

    def on_window_close(self):
        """Terminate a running QA process and close its log handle before exit."""
        if self.qa_process and self.qa_process.poll() is None:
            try:
                self.qa_process.terminate()
            except Exception:
                pass

        if self.qa_log_handle:
            try:
                self.qa_log_handle.close()
            except Exception:
                pass
            self.qa_log_handle = None

        self.root.destroy()

    def setup_services_tab(self):
        """Setup services control tab"""
        # Services control frame
        services_frame = tk.Frame(self.services_tab)
        services_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        self.service_widgets = {}
        
        for service_id, service in self.get_sorted_services():
            frame = tk.LabelFrame(
                services_frame,
                text=f"{service['icon']} {service['name']}",
                font=('Arial', 12, 'bold'),
                padx=15,
                pady=15
            )
            frame.pack(fill='x', pady=10)
            
            # Info labels
            info_frame = tk.Frame(frame)
            info_frame.pack(side='left', fill='both', expand=True)
            
            status_label = tk.Label(
                info_frame,
                text="● Статус: Проверавам...",
                font=('Arial', 10),
                anchor='w'
            )
            status_label.pack(anchor='w')

            # Display port or socket info
            if service['port']:
                port_label = tk.Label(
                    info_frame,
                    text=f"🔌 Порт: {service['port']}",
                    font=('Arial', 9),
                    anchor='w'
                )
                port_label.pack(anchor='w')

                # Display appropriate URL
                if service['port'] == 80:
                    url_text = "🌐 URL: http://localhost (LAN: http://192.168.144.48)"
                    url = "http://localhost"
                else:
                    url_text = f"🌐 URL: http://localhost:{service['port']}"
                    url = f"http://localhost:{service['port']}"

                url_label = tk.Label(
                    info_frame,
                    text=url_text,
                    font=('Arial', 9),
                    anchor='w',
                    fg='blue',
                    cursor='hand2'
                )
                url_label.pack(anchor='w')
                url_label.bind('<Button-1>', lambda e, u=url: self.open_browser(u))
            elif 'socket' in service:
                socket_label = tk.Label(
                    info_frame,
                    text=f"🔌 Socket: {service['socket']}",
                    font=('Arial', 9),
                    anchor='w'
                )
                socket_label.pack(anchor='w')

            # Show systemd service name if applicable
            if self.is_systemd_service(service):
                systemd_label = tk.Label(
                    info_frame,
                    text=f"⚙️ Systemd: {service['systemd_service']}",
                    font=('Arial', 9),
                    anchor='w'
                )
                systemd_label.pack(anchor='w')
            
            # Control buttons
            button_frame = tk.Frame(frame)
            button_frame.pack(side='right')
            
            start_btn = tk.Button(
                button_frame,
                text="▶️ Покрени",
                command=lambda sid=service_id: self.start_service(sid),
                bg='#4CAF50',
                fg='white',
                padx=15,
                pady=5
            )
            start_btn.pack(side='left', padx=5)
            
            stop_btn = tk.Button(
                button_frame,
                text="⏹️ Заустави",
                command=lambda sid=service_id: self.stop_service(sid),
                bg='#f44336',
                fg='white',
                padx=15,
                pady=5
            )
            stop_btn.pack(side='left', padx=5)
            
            restart_btn = tk.Button(
                button_frame,
                text="🔄 Рестарт",
                command=lambda sid=service_id: self.restart_service(sid),
                bg='#FF9800',
                fg='white',
                padx=15,
                pady=5
            )
            restart_btn.pack(side='left', padx=5)
            
            logs_btn = tk.Button(
                button_frame,
                text="📋 Логови",
                command=lambda sid=service_id: self.show_service_logs(sid),
                bg='#2196F3',
                fg='white',
                padx=15,
                pady=5
            )
            logs_btn.pack(side='left', padx=5)
            
            self.service_widgets[service_id] = {
                'status_label': status_label,
                'start_btn': start_btn,
                'stop_btn': stop_btn,
                'restart_btn': restart_btn
            }
    
    def setup_logs_tab(self):
        """Setup logs viewing tab"""
        control_frame = tk.Frame(self.logs_tab)
        control_frame.pack(fill='x', padx=10, pady=10)
        
        tk.Label(control_frame, text="Изабери сервис:", font=('Arial', 10)).pack(side='left', padx=5)

        default_log_service = self.get_sorted_services()[0][0]
        self.log_service_var = tk.StringVar(value=default_log_service)
        service_combo = ttk.Combobox(
            control_frame,
            textvariable=self.log_service_var,
            values=[service_id for service_id, _ in self.get_sorted_services()],
            state='readonly',
            width=30
        )
        service_combo.pack(side='left', padx=5)
        
        tk.Button(
            control_frame,
            text="🔄 Освежи",
            command=self.refresh_logs,
            padx=10
        ).pack(side='left', padx=5)
        
        tk.Button(
            control_frame,
            text="🗑️ Обриши логове",
            command=self.clear_logs,
            padx=10
        ).pack(side='left', padx=5)
        
        # Auto-refresh checkbox
        self.auto_refresh_var = tk.BooleanVar(value=False)
        tk.Checkbutton(
            control_frame,
            text="Аутоматско освежавање",
            variable=self.auto_refresh_var
        ).pack(side='left', padx=10)
        
        # Log viewer
        self.log_text = scrolledtext.ScrolledText(
            self.logs_tab,
            wrap=tk.WORD,
            font=('Courier', 9),
            bg='#1e1e1e',
            fg='#00ff00'
        )
        self.log_text.pack(fill='both', expand=True, padx=10, pady=10)
    
    def setup_info_tab(self):
        """Setup system information tab"""
        info_frame = tk.Frame(self.info_tab)
        info_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        self.info_text = scrolledtext.ScrolledText(
            info_frame,
            wrap=tk.WORD,
            font=('Courier', 10),
            height=30
        )
        self.info_text.pack(fill='both', expand=True)
        
        tk.Button(
            info_frame,
            text="🔄 Освежи информације",
            command=self.update_system_info,
            padx=20,
            pady=5
        ).pack(pady=10)
        
        self.update_system_info()
    
    def setup_database_tab(self):
        """Setup database management tab"""
        db_frame = tk.Frame(self.db_tab)
        db_frame.pack(fill='both', expand=True, padx=20, pady=20)

        # Database operations
        operations = [
            ("📊 Провери статус база података", self.check_database_status),
            ("🧭 Отвори PostgreSQL Browser", self.open_postgres_control_app),
            ("🐘 Омогући PostgreSQL ауто-старт", self.enable_postgresql_autostart),
            ("💾 Направи резервну копију", self.backup_databases),
            ("📈 Статистика база података", self.show_database_stats),
            ("🔧 Оптимизуј базе података", self.optimize_databases),
        ]

        for text, command in operations:
            # Highlight PostgreSQL button
            if "PostgreSQL" in text:
                bg_color = '#4CAF50'
                fg_color = 'white'
            elif "Browser" in text:
                bg_color = '#0f766e'
                fg_color = 'white'
            else:
                bg_color = '#f0f0f0'
                fg_color = 'black'

            tk.Button(
                db_frame,
                text=text,
                command=command,
                font=('Arial', 11),
                padx=20,
                pady=10,
                width=40,
                bg=bg_color,
                fg=fg_color
            ).pack(pady=10)

        # Database status display
        self.db_status_text = scrolledtext.ScrolledText(
            db_frame,
            wrap=tk.WORD,
            font=('Courier', 9),
            height=15
        )
        self.db_status_text.pack(fill='both', expand=True, pady=20)

    def setup_qa_tab(self):
        """Setup QA test runner tab"""
        qa_frame = tk.Frame(self.qa_tab)
        qa_frame.pack(fill='both', expand=True, padx=20, pady=20)

        header_frame = tk.Frame(qa_frame)
        header_frame.pack(fill='x', pady=(0, 10))

        tk.Label(
            header_frame,
            text="🧪 QA тест пакет",
            font=('Arial', 14, 'bold')
        ).pack(side='left')

        self.qa_status_var = tk.StringVar(value="Спреман за покретање")
        tk.Label(
            header_frame,
            textvariable=self.qa_status_var,
            font=('Arial', 10),
            fg='#2c5d84'
        ).pack(side='right')

        options_frame = tk.LabelFrame(qa_frame, text="Подешавања", font=('Arial', 11, 'bold'), padx=10, pady=10)
        options_frame.pack(fill='x', pady=(0, 10))

        row1 = tk.Frame(options_frame)
        row1.pack(fill='x', pady=5)

        tk.Label(row1, text="Режим сервера:", font=('Arial', 10)).pack(side='left', padx=(0, 5))
        self.qa_server_mode_var = tk.StringVar(value='gunicorn')
        ttk.Combobox(
            row1,
            textvariable=self.qa_server_mode_var,
            values=['flask', 'gunicorn'],
            state='readonly',
            width=12
        ).pack(side='left', padx=(0, 15))

        self.qa_include_lint_var = tk.BooleanVar(value=True)
        tk.Checkbutton(row1, text="Lint", variable=self.qa_include_lint_var).pack(side='left', padx=5)

        self.qa_include_cypress_var = tk.BooleanVar(value=False)
        tk.Checkbutton(row1, text="Cypress E2E", variable=self.qa_include_cypress_var).pack(side='left', padx=5)

        self.qa_include_playwright_var = tk.BooleanVar(value=True)
        tk.Checkbutton(row1, text="Playwright", variable=self.qa_include_playwright_var).pack(side='left', padx=5)

        self.qa_include_k6_var = tk.BooleanVar(value=False)
        tk.Checkbutton(row1, text="k6 load test", variable=self.qa_include_k6_var).pack(side='left', padx=5)

        self.qa_use_redis_var = tk.BooleanVar(value=False)
        tk.Checkbutton(row1, text="Покрени локални Redis/Valkey", variable=self.qa_use_redis_var).pack(side='left', padx=5)

        row2 = tk.Frame(options_frame)
        row2.pack(fill='x', pady=5)

        info_text = (
            "Покреће постојећи `run_qa.sh` пакет. За gunicorn smoke тест "
            "искључите Cypress E2E. Ако је Cypress укључен, QA креденцијали морају "
            "бити подешени у окружењу или `.env`."
        )
        tk.Label(
            row2,
            text=info_text,
            font=('Arial', 9),
            fg='#555555',
            wraplength=900,
            justify='left'
        ).pack(anchor='w')

        credentials_frame = tk.LabelFrame(qa_frame, text="Cypress креденцијали", font=('Arial', 11, 'bold'), padx=10, pady=10)
        credentials_frame.pack(fill='x', pady=(0, 10))

        credential_fields = [
            ('CYPRESS_ADMIN_EMAIL', 'Admin email', False),
            ('CYPRESS_ADMIN_PASSWORD', 'Admin лозинка', True),
            ('CYPRESS_EMPLOYEE_EMAIL', 'Employee email', False),
            ('CYPRESS_EMPLOYEE_PASSWORD', 'Employee лозинка', True),
            ('CYPRESS_FIRST_LOGIN_EMAIL', 'First-login email', False),
            ('CYPRESS_FIRST_LOGIN_PASSWORD', 'First-login лозинка', True),
            ('CYPRESS_RESET_TARGET_EMAIL', 'Reset target email', False),
            ('CYPRESS_ARCHIVE_EMAIL', 'Archive email', False),
            ('CYPRESS_ARCHIVE_PASSWORD', 'Archive лозинка', True),
        ]

        for index, (env_key, label, is_secret) in enumerate(credential_fields):
            row = index // 2
            column = (index % 2) * 2
            tk.Label(credentials_frame, text=label + ':', font=('Arial', 9)).grid(
                row=row,
                column=column,
                sticky='w',
                padx=(0, 5),
                pady=4,
            )
            var = tk.StringVar()
            self.qa_credential_vars[env_key] = var
            tk.Entry(
                credentials_frame,
                textvariable=var,
                width=34,
                show='*' if is_secret else '',
            ).grid(row=row, column=column + 1, sticky='we', padx=(0, 12), pady=4)

        credentials_frame.columnconfigure(1, weight=1)
        credentials_frame.columnconfigure(3, weight=1)

        credentials_actions = tk.Frame(credentials_frame)
        credentials_actions.grid(row=5, column=0, columnspan=4, sticky='w', pady=(8, 0))

        tk.Button(
            credentials_actions,
            text="💾 Сачувај .env.qa",
            command=self.save_qa_credentials,
            padx=12,
            pady=4
        ).pack(side='left', padx=(0, 8))

        tk.Button(
            credentials_actions,
            text="⚡ Попуни email",
            command=self.autofill_qa_credentials,
            padx=12,
            pady=4
        ).pack(side='left', padx=(0, 8))

        tk.Button(
            credentials_actions,
            text="🔄 Учитај",
            command=self.load_qa_credentials,
            padx=12,
            pady=4
        ).pack(side='left', padx=(0, 8))

        tk.Button(
            credentials_actions,
            text="🧹 Очисти",
            command=self.clear_qa_credentials,
            padx=12,
            pady=4
        ).pack(side='left')

        buttons_frame = tk.Frame(qa_frame)
        buttons_frame.pack(fill='x', pady=(0, 10))

        self.qa_start_button = tk.Button(
            buttons_frame,
            text="▶️ Покрени QA",
            command=self.start_qa_suite,
            bg='#4CAF50',
            fg='white',
            font=('Arial', 10, 'bold'),
            padx=20,
            pady=6
        )
        self.qa_start_button.pack(side='left', padx=(0, 8))

        self.qa_stop_button = tk.Button(
            buttons_frame,
            text="⏹️ Заустави QA",
            command=self.stop_qa_suite,
            bg='#f44336',
            fg='white',
            font=('Arial', 10, 'bold'),
            padx=20,
            pady=6,
            state='disabled'
        )
        self.qa_stop_button.pack(side='left', padx=(0, 8))

        tk.Button(
            buttons_frame,
            text="🗑️ Очисти излаз",
            command=self.clear_qa_output,
            padx=15,
            pady=6
        ).pack(side='left', padx=(0, 8))

        tk.Button(
            buttons_frame,
            text="📂 Отвори лог",
            command=self.open_qa_log,
            padx=15,
            pady=6
        ).pack(side='left')

        self.qa_output_text = scrolledtext.ScrolledText(
            qa_frame,
            wrap=tk.WORD,
            font=('Courier', 9),
            bg='#111111',
            fg='#e6e6e6'
        )
        self.qa_output_text.pack(fill='both', expand=True)

        self.append_qa_output(
            "QA интеграција је спремна.\n"
            f"Лог фајл: {self.qa_log_path}\n"
        )
        self.load_qa_credentials()
    
    def is_systemd_service(self, service):
        """Check if service is systemd-managed"""
        return service.get('service_type') == 'systemd'

    def get_sudo_password(self):
        """Get sudo password from user (cached for session)"""
        if self.sudo_password is not None:
            return self.sudo_password

        password = simpledialog.askstring(
            "Sudo лозинка",
            "Унесите вашу лозинку за управљање сервисима:\n(Лозинка ће бити сачувана за ову сесију)",
            show='*',
            parent=self.root
        )

        if password:
            # Test if password is correct
            test_cmd = subprocess.run(
                ['sudo', '-S', 'systemctl', 'is-active', 'nginx'],
                input=password + '\n',
                capture_output=True,
                text=True
            )

            if test_cmd.returncode == 0 or 'sudo: ' not in test_cmd.stderr:
                self.sudo_password = password
                return password
            else:
                messagebox.showerror("Грешка", "Погрешна лозинка!")
                return None
        return None

    def clear_sudo_password(self):
        """Clear cached sudo password"""
        self.sudo_password = None
        messagebox.showinfo("Информација", "Кеширана лозинка је обрисана.\nБићете упитани за лозинку при следећој контроли сервиса.")

    def install_systemd_services(self):
        """Install systemd service files"""
        if not messagebox.askyesno(
            "Инсталација сервиса",
            "Ово ће инсталирати museum-system.service у systemd.\n\n"
            "Наставити?"
        ):
            return

        try:
            # Copy service file
            result = self.run_sudo_command([
                'cp',
                '/home/aleksandarlukovic/MuseumInfoSystem/museum-system.service',
                '/etc/systemd/system/museum-system.service'
            ])

            if result is None or result.returncode != 0:
                messagebox.showerror("Грешка", "Неуспешно копирање сервис фајла")
                return

            # Reload systemd
            result = self.run_sudo_command(['systemctl', 'daemon-reload'])
            if result is None or result.returncode != 0:
                messagebox.showerror("Грешка", "Неуспешно reload systemd")
                return

            # Enable service
            result = self.run_sudo_command(['systemctl', 'enable', 'museum-system'])
            if result is None or result.returncode != 0:
                messagebox.showerror("Грешка", "Неуспешно омогућавање сервиса")
                return

            messagebox.showinfo(
                "Успех",
                "✓ museum-system сервис је успешно инсталиран!\n\n"
                "Сада можете покренути сервис помоћу дугмета 'Покрени'."
            )
            self.update_service_status()

        except Exception as e:
            messagebox.showerror("Грешка", f"Грешка приликом инсталације:\n{str(e)}")

    def fix_nginx_config(self):
        """Fix nginx configuration to use museum system instead of timesheet"""
        if not messagebox.askyesno(
            "Поправка Nginx конфигурације",
            "Ово ће:\n"
            "1. Направити резервну копију старих nginx конфигурација\n"
            "2. Инсталирати нову конфигурацију за музејски систем\n"
            "3. Рестартовати nginx\n\n"
            "После овога ће http://192.168.144.48 показивати музејски систем.\n\n"
            "Наставити?"
        ):
            return

        try:
            # Create backup directory
            result = self.run_sudo_command([
                'mkdir', '-p', '/etc/nginx/conf.d/backup'
            ])
            if result is None:
                return

            # Backup old configs
            configs_to_backup = [
                'museum-timesheet.conf',
                'museum-app.conf',
                'museum-db.conf'
            ]

            for config in configs_to_backup:
                result = self.run_sudo_command([
                    'mv',
                    f'/etc/nginx/conf.d/{config}',
                    f'/etc/nginx/conf.d/backup/{config}'
                ])
                # Continue even if file doesn't exist

            # Install new config
            result = self.run_sudo_command([
                'cp',
                '/home/aleksandarlukovic/MuseumInfoSystem/nginx_museum.conf',
                '/etc/nginx/conf.d/museum-system.conf'
            ])

            if result is None or result.returncode != 0:
                messagebox.showerror("Грешка", "Неуспешно копирање nginx конфигурације")
                return

            # Test nginx config
            result = self.run_sudo_command(['nginx', '-t'])
            if result is None or result.returncode != 0:
                error_msg = result.stderr if result else "Unknown error"
                messagebox.showerror("Грешка", f"Nginx конфигурација није валидна:\n{error_msg}")
                return

            # Restart nginx
            result = self.run_sudo_command(['systemctl', 'restart', 'nginx'])
            if result is None or result.returncode != 0:
                messagebox.showerror("Грешка", "Неуспешан рестарт nginx")
                return

            messagebox.showinfo(
                "Успех",
                "✓ Nginx конфигурација је успешно поправљена!\n\n"
                "Стари конфигурациони фајлови су сачувани у:\n"
                "/etc/nginx/conf.d/backup/\n\n"
                "Сада када приступите http://192.168.144.48\n"
                "требало би да видите музејски систем."
            )
            self.update_service_status()

        except Exception as e:
            messagebox.showerror("Грешка", f"Грешка приликом поправке:\n{str(e)}")

    def run_sudo_command(self, command):
        """Run a command with sudo, prompting for password if needed"""
        password = self.get_sudo_password()
        if password is None:
            return None

        result = subprocess.run(
            ['sudo', '-S'] + command,
            input=password + '\n',
            capture_output=True,
            text=True
        )
        return result

    def check_systemd_status(self, service_name):
        """Check if a systemd service is running"""
        try:
            result = subprocess.run(
                ['systemctl', 'is-active', service_name],
                capture_output=True,
                text=True
            )
            return result.stdout.strip() == 'active'
        except:
            return False

    def check_port(self, port):
        """Check if a port is in use"""
        if port is None:
            return False
        for conn in psutil.net_connections():
            if conn.laddr and conn.laddr.port == port and conn.status == 'LISTEN':
                return True
        return False

    def get_pid_on_port(self, port):
        """Get PID of process using a port"""
        for conn in psutil.net_connections():
            if conn.laddr and conn.laddr.port == port and conn.status == 'LISTEN':
                return conn.pid
        return None
    
    def update_service_status(self):
        """Update status of all services"""
        for service_id, service in self.services.items():
            is_running = False
            pid = None

            if self.is_systemd_service(service):
                # Check systemd service status
                is_running = self.check_systemd_status(service['systemd_service'])
                if is_running:
                    # Try to get PID from systemctl
                    try:
                        result = subprocess.run(
                            ['systemctl', 'show', service['systemd_service'], '--property=MainPID'],
                            capture_output=True,
                            text=True
                        )
                        pid = result.stdout.strip().split('=')[1]
                        if pid == '0':
                            pid = None
                    except:
                        pass
            else:
                # Check port-based service
                is_running = self.check_port(service['port'])
                if is_running:
                    pid = self.get_pid_on_port(service['port'])

            if is_running:
                service['status'] = 'running'
                status_text = f"● Статус: 🟢 Активан" + (f" (PID: {pid})" if pid else "")
                status_color = '#4CAF50'
            else:
                service['status'] = 'stopped'
                status_text = "● Статус: 🔴 Заустављен"
                status_color = '#f44336'

            if service_id in self.service_widgets:
                self.service_widgets[service_id]['status_label'].config(
                    text=status_text,
                    fg=status_color
                )

        # Update status bar
        running = sum(1 for s in self.services.values() if s['status'] == 'running')
        total = len(self.services)
        self.status_bar.config(text=f"Статус: {running}/{total} сервиса активно | {datetime.now().strftime('%H:%M:%S')}")

    def get_bulk_services(self, reverse=False):
        services = [
            (service_id, service)
            for service_id, service in self.get_sorted_services()
            if service.get('bulk_start', True)
        ]
        return list(reversed(services)) if reverse else services

    def get_sorted_services(self):
        services = [
            (service_id, service)
            for service_id, service in self.services.items()
        ]
        return sorted(
            services,
            key=lambda item: item[1].get('order', 50),
        )

    def summarize_bulk_results(self, action_title, results):
        changed = [result for result in results if result['status'] == 'changed']
        skipped = [result for result in results if result['status'] == 'skipped']
        failed = [result for result in results if result['status'] == 'error']

        lines = []
        if changed:
            lines.append("Успешно:")
            lines.extend(f"• {result['service']}" for result in changed)
        if skipped:
            lines.append("")
            lines.append("Без измена:")
            lines.extend(f"• {result['service']} ({result['message']})" for result in skipped)
        if failed:
            lines.append("")
            lines.append("Грешке:")
            lines.extend(f"• {result['service']}: {result['message']}" for result in failed)

        message = '\n'.join(line for line in lines if line is not None).strip()
        if not message:
            message = "Нема сервиса за обраду."

        if failed:
            messagebox.showerror(action_title, message)
        else:
            messagebox.showinfo(action_title, message)
    
    def auto_update_status(self):
        """Auto-update status in background"""
        while True:
            try:
                self.update_service_status()
                if self.auto_refresh_var.get():
                    self.refresh_logs()
            except:
                pass
            time.sleep(2)
    
    def start_service(self, service_id, show_dialogs=True):
        """Start a service"""
        service = self.services[service_id]

        # Check if already running
        if self.is_systemd_service(service):
            if self.check_systemd_status(service['systemd_service']):
                if show_dialogs:
                    messagebox.showwarning("Упозорење", f"{service['name']} је већ покренут!")
                return {'status': 'skipped', 'service': service['name'], 'message': 'већ је покренут'}
        else:
            if self.check_port(service['port']):
                if show_dialogs:
                    messagebox.showwarning("Упозорење", f"{service['name']} је већ покренут!")
                return {'status': 'skipped', 'service': service['name'], 'message': 'већ је покренут'}

        try:
            if self.is_systemd_service(service):
                # Start systemd service with password prompt
                result = self.run_sudo_command(['systemctl', 'start', service['systemd_service']])

                if result is None:
                    return {'status': 'error', 'service': service['name'], 'message': 'отказана sudo ауторизација'}

                if result.returncode != 0:
                    error_msg = result.stderr if result.stderr else result.stdout
                    if show_dialogs:
                        messagebox.showerror("Грешка", f"Грешка при покретању:\n{error_msg}")
                    return {'status': 'error', 'service': service['name'], 'message': error_msg.strip() or 'неуспешно покретање'}

                time.sleep(2)

                if self.check_systemd_status(service['systemd_service']):
                    self.update_service_status()
                    if show_dialogs:
                        messagebox.showinfo("Успех", f"{service['name']} је успешно покренут!")
                    return {'status': 'changed', 'service': service['name'], 'message': 'покренут'}
                else:
                    if show_dialogs:
                        messagebox.showerror("Грешка", f"Проблем приликом покретања {service['name']}")
                    return {'status': 'error', 'service': service['name'], 'message': 'сервис није постао активан'}
            else:
                # Start regular process
                log_path = os.path.join(service['path'], service['log'])
                os.makedirs(os.path.dirname(log_path), exist_ok=True)

                with open(log_path, 'a') as log_file:
                    process = subprocess.Popen(
                        service['command'],
                        stdout=log_file,
                        stderr=subprocess.STDOUT,
                        cwd=service['path']
                    )

                time.sleep(2)

                if self.check_port(service['port']):
                    self.update_service_status()
                    if show_dialogs:
                        messagebox.showinfo("Успех", f"{service['name']} је успешно покренут!")
                    return {'status': 'changed', 'service': service['name'], 'message': 'покренут'}
                else:
                    if show_dialogs:
                        messagebox.showerror("Грешка", f"Проблем приликом покретања {service['name']}")
                    return {'status': 'error', 'service': service['name'], 'message': 'порт није активан'}

        except Exception as e:
            if show_dialogs:
                messagebox.showerror("Грешка", f"Грешка: {str(e)}")
            return {'status': 'error', 'service': service['name'], 'message': str(e)}
    
    def stop_service(self, service_id, show_dialogs=True):
        """Stop a service"""
        service = self.services[service_id]

        # Check if running
        if self.is_systemd_service(service):
            if not self.check_systemd_status(service['systemd_service']):
                if show_dialogs:
                    messagebox.showwarning("Упозорење", f"{service['name']} није покренут!")
                return {'status': 'skipped', 'service': service['name'], 'message': 'није покренут'}
        else:
            pid = self.get_pid_on_port(service['port'])
            if not pid:
                if show_dialogs:
                    messagebox.showwarning("Упозорење", f"{service['name']} није покренут!")
                return {'status': 'skipped', 'service': service['name'], 'message': 'није покренут'}

        try:
            if self.is_systemd_service(service):
                # Stop systemd service with password prompt
                result = self.run_sudo_command(['systemctl', 'stop', service['systemd_service']])

                if result is None:
                    return {'status': 'error', 'service': service['name'], 'message': 'отказана sudo ауторизација'}

                if result.returncode != 0:
                    error_msg = result.stderr if result.stderr else result.stdout
                    if show_dialogs:
                        messagebox.showerror("Грешка", f"Грешка при заустављању:\n{error_msg}")
                    return {'status': 'error', 'service': service['name'], 'message': error_msg.strip() or 'неуспешно заустављање'}

                time.sleep(1)
                self.update_service_status()
                if show_dialogs:
                    messagebox.showinfo("Успех", f"{service['name']} је заустављен!")
                return {'status': 'changed', 'service': service['name'], 'message': 'заустављен'}
            else:
                # Kill regular process
                pid = self.get_pid_on_port(service['port'])
                if pid:
                    try:
                        os.kill(pid, signal.SIGTERM)
                    except ProcessLookupError:
                        pass
                    time.sleep(1)

                    # Force kill if still running
                    if self.check_port(service['port']):
                        try:
                            os.kill(pid, signal.SIGKILL)
                        except ProcessLookupError:
                            pass

                self.update_service_status()
                if show_dialogs:
                    messagebox.showinfo("Успех", f"{service['name']} је заустављен!")
                return {'status': 'changed', 'service': service['name'], 'message': 'заустављен'}

        except Exception as e:
            if show_dialogs:
                messagebox.showerror("Грешка", f"Грешка: {str(e)}")
            return {'status': 'error', 'service': service['name'], 'message': str(e)}
    
    def restart_service(self, service_id, show_dialogs=True):
        """Restart a service"""
        service = self.services[service_id]

        try:
            if self.is_systemd_service(service):
                # Use systemd restart command with password prompt
                result = self.run_sudo_command(['systemctl', 'restart', service['systemd_service']])

                if result is None:
                    return {'status': 'error', 'service': service['name'], 'message': 'отказана sudo ауторизација'}

                if result.returncode != 0:
                    error_msg = result.stderr if result.stderr else result.stdout
                    if show_dialogs:
                        messagebox.showerror("Грешка", f"Грешка при рестартовању:\n{error_msg}")
                    return {'status': 'error', 'service': service['name'], 'message': error_msg.strip() or 'неуспешан рестарт'}

                time.sleep(2)
                self.update_service_status()
                if show_dialogs:
                    messagebox.showinfo("Успех", f"{service['name']} је рестартован!")
                return {'status': 'changed', 'service': service['name'], 'message': 'рестартован'}
            else:
                # Regular process - stop then start
                stop_result = self.stop_service(service_id, show_dialogs=False)
                if stop_result['status'] == 'error':
                    if show_dialogs:
                        messagebox.showerror("Грешка", f"Грешка при рестартовању:\n{stop_result['message']}")
                    return stop_result
                time.sleep(2)
                return self.start_service(service_id, show_dialogs=show_dialogs)

        except Exception as e:
            if show_dialogs:
                messagebox.showerror("Грешка", f"Грешка: {str(e)}")
            return {'status': 'error', 'service': service['name'], 'message': str(e)}
    
    def start_all_services(self):
        """Start all services in correct order"""
        self.update_service_status()
        results = []

        for service_id, _service in self.get_bulk_services():
            results.append(self.start_service(service_id, show_dialogs=False))
            time.sleep(2)

        self.update_service_status()
        self.summarize_bulk_results("Покретање сервиса", results)
    
    def stop_all_services(self):
        """Stop all services"""
        self.update_service_status()
        results = []

        for service_id, _service in self.get_bulk_services(reverse=True):
            results.append(self.stop_service(service_id, show_dialogs=False))
            time.sleep(1)

        self.update_service_status()
        self.summarize_bulk_results("Заустављање сервиса", results)
    
    def restart_all_services(self):
        """Restart all services"""
        self.update_service_status()
        results = []

        for service_id, _service in self.get_bulk_services(reverse=True):
            results.append(self.stop_service(service_id, show_dialogs=False))
            time.sleep(1)

        time.sleep(2)

        for service_id, _service in self.get_bulk_services():
            results.append(self.start_service(service_id, show_dialogs=False))
            time.sleep(2)

        self.update_service_status()
        self.summarize_bulk_results("Рестарт сервиса", results)
    
    def show_service_logs(self, service_id):
        """Show logs for a specific service"""
        self.log_service_var.set(service_id)
        self.notebook.select(self.logs_tab)
        self.refresh_logs()
    
    def refresh_logs(self):
        """Refresh log display"""
        service_id = self.log_service_var.get()
        service = self.services.get(service_id)

        if not service:
            return

        self.log_text.delete('1.0', tk.END)

        try:
            if self.is_systemd_service(service):
                # Use journalctl for systemd services
                result = subprocess.run(
                    ['journalctl', '-u', service['systemd_service'], '-n', '500', '--no-pager'],
                    capture_output=True,
                    text=True
                )

                if result.returncode == 0:
                    self.log_text.insert('1.0', result.stdout)
                    self.log_text.see(tk.END)
                else:
                    self.log_text.insert('1.0', f"Грешка при читању journalctl:\n{result.stderr}")
            else:
                # Read from log file for regular processes
                log_path = os.path.join(service['path'], service['log'])

                if os.path.exists(log_path):
                    with open(log_path, 'r', encoding='utf-8') as f:
                        lines = f.readlines()
                        # Show last 500 lines
                        self.log_text.insert('1.0', ''.join(lines[-500:]))
                        self.log_text.see(tk.END)
                else:
                    self.log_text.insert('1.0', f"Лог фајл не постоји: {log_path}")

        except Exception as e:
            self.log_text.insert('1.0', f"Грешка при читању лога: {str(e)}")
    
    def clear_logs(self):
        """Clear logs for selected service"""
        service_id = self.log_service_var.get()
        service = self.services.get(service_id)

        if self.is_systemd_service(service):
            messagebox.showinfo(
                "Информација",
                "Системски логови (journalctl) се не могу обрисати из ове апликације.\n"
                "Користите команду: sudo journalctl --vacuum-time=1s"
            )
            return

        if messagebox.askyesno("Потврда", f"Обрисати логове за {service['name']}?"):
            log_path = os.path.join(service['path'], service['log'])
            try:
                open(log_path, 'w').close()
                messagebox.showinfo("Успех", "Логови су обрисани!")
                self.refresh_logs()
            except Exception as e:
                messagebox.showerror("Грешка", f"Грешка: {str(e)}")
    
    def update_system_info(self):
        """Update system information display"""
        self.info_text.delete('1.0', tk.END)
        
        info = f"""
═══════════════════════════════════════════════════════════════
        ИНФОРМАЦИОНИ СИСТЕМ ПРИРОДЊАЧКОГ МУЗЕЈА
═══════════════════════════════════════════════════════════════

📅 Време: {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}

🖥️  СИСТЕМСКЕ ИНФОРМАЦИЈЕ
────────────────────────────────────────────────────────────────
Оперативни систем: {os.uname().sysname} {os.uname().release}
Процесор: {psutil.cpu_count()} језгара
Искоришћеност CPU: {psutil.cpu_percent()}%
Меморија: {psutil.virtual_memory().percent}% искоришћено
Диск: {psutil.disk_usage('/').percent}% искоришћено

🌐 СТАТУС СЕРВИСА
────────────────────────────────────────────────────────────────
"""
        
        for service_id, service in self.services.items():
            status = "🟢 Активан" if service['status'] == 'running' else "🔴 Заустављен"

            info += f"""
{service['icon']} {service['name']}
   Статус: {status}"""

            if service['port']:
                info += f"\n   Порт: {service['port']}"
                info += f"\n   URL: http://localhost:{service['port']}"
            elif 'socket' in service:
                info += f"\n   Socket: {service['socket']}"

            if self.is_systemd_service(service):
                info += f"\n   Systemd: {service['systemd_service']}"

            info += "\n"
        
        info += "\n" + "="*63 + "\n"
        
        self.info_text.insert('1.0', info)
    
    def check_database_status(self):
        """Check database status"""
        self.db_status_text.delete('1.0', tk.END)
        self.db_status_text.insert('1.0', "Проверавам статус база података...\n\n")

        # Check PostgreSQL (PRIMARY DATABASE - Phase 2 Migration)
        self.db_status_text.insert(tk.END, "🐘 PostgreSQL (Главна база података - Phase 2):\n")
        try:
            # Check if PostgreSQL service is running
            result = subprocess.run(
                ['systemctl', 'is-active', 'postgresql'],
                capture_output=True,
                text=True
            )
            is_running = result.stdout.strip() == 'active'

            if is_running:
                self.db_status_text.insert(tk.END, "   ✅ Сервис: Активан\n")

                # Try to connect and get version
                try:
                    result = subprocess.run(
                        ['psql', '-U', _DB_USER, '-d', _DB_NAME, '-c', 'SELECT version();'],
                        capture_output=True,
                        text=True,
                        timeout=2
                    )
                    if result.returncode == 0:
                        version_candidates = [
                            line.strip()
                            for line in result.stdout.split('\n')
                            if 'PostgreSQL' in line
                        ]
                        version_line = version_candidates[0] if version_candidates else 'непознато'
                        self.db_status_text.insert(tk.END, f"   ✅ Верзија: {version_line}\n")

                        # Get database size
                        result = subprocess.run(
                            ['psql', '-U', _DB_USER, '-d', _DB_NAME, '-t', '-c',
                             "SELECT pg_size_pretty(pg_database_size('museum_system'));"],
                            capture_output=True,
                            text=True,
                            timeout=2
                        )
                        if result.returncode == 0:
                            db_size = result.stdout.strip()
                            self.db_status_text.insert(tk.END, f"   ✅ Величина базе: {db_size}\n")

                        # Get record counts
                        result = subprocess.run(
                            ['psql', '-U', _DB_USER, '-d', _DB_NAME, '-t', '-c',
                             """SELECT 'bird_ringing: ' || COUNT(*) FROM bird_ringing_records
                                UNION ALL SELECT 'minerals: ' || COUNT(*) FROM minerals
                                UNION ALL SELECT 'inventory: ' || COUNT(*) FROM inventory_entries
                                UNION ALL SELECT 'users: ' || COUNT(*) FROM users;"""],
                            capture_output=True,
                            text=True,
                            timeout=2
                        )
                        if result.returncode == 0:
                            self.db_status_text.insert(tk.END, "   📊 Број записа:\n")
                            for line in result.stdout.strip().split('\n'):
                                if line.strip():
                                    self.db_status_text.insert(tk.END, f"      • {line.strip()}\n")
                    else:
                        self.db_status_text.insert(tk.END, "   ⚠️  Не могу да се повежем на базу\n")
                except subprocess.TimeoutExpired:
                    self.db_status_text.insert(tk.END, "   ⚠️  Timeout при повезивању\n")
                except Exception as e:
                    self.db_status_text.insert(tk.END, f"   ⚠️  Грешка: {str(e)}\n")

                # Check if enabled on boot
                result = subprocess.run(
                    ['systemctl', 'is-enabled', 'postgresql'],
                    capture_output=True,
                    text=True
                )
                is_enabled = result.stdout.strip() == 'enabled'
                if is_enabled:
                    self.db_status_text.insert(tk.END, "   ✅ Аутоматски старт: Омогућен\n")
                else:
                    self.db_status_text.insert(tk.END, "   ⚠️  Аутоматски старт: Онемогућен (користите 'Омогући PostgreSQL ауто-старт')\n")
            else:
                self.db_status_text.insert(tk.END, "   ❌ Сервис није покренут\n")
                self.db_status_text.insert(tk.END, "   ℹ️  Покрените PostgreSQL из таба 'Сервиси'\n")
        except Exception as e:
            self.db_status_text.insert(tk.END, f"   ❌ Грешка: {str(e)}\n")

        # Check SQLite (LEGACY - for fallback only)
        self.db_status_text.insert(tk.END, "\n📊 SQLite (Застарело - само за fallback):\n")
        db_path = "/home/aleksandarlukovic/MuseumInfoSystem/PrirodnjackiMuzej/prirodnjacki_muzej.sqlite"
        if os.path.exists(db_path):
            size = os.path.getsize(db_path) / 1024 / 1024
            self.db_status_text.insert(tk.END, f"   ⚠️  Постоји (застарело): {size:.2f} MB\n")
            self.db_status_text.insert(tk.END, "   ℹ️  SQLite се користи само ако PostgreSQL није активан\n")
        else:
            self.db_status_text.insert(tk.END, "   ❌ Није пронађена\n")
    
    def enable_postgresql_autostart(self):
        """Enable PostgreSQL auto-start and configure museum-system dependency"""
        if not messagebox.askyesno(
            "PostgreSQL Ауто-Старт",
            "Ово ће:\n\n"
            "1. Омогућити PostgreSQL да се покреће при подизању система\n"
            "2. Покренути PostgreSQL сада\n"
            "3. Ажурирати museum-system.service да зависи од PostgreSQL\n"
            "4. Рестартовати музејски систем\n\n"
            "Препоручено: Ово је неопходно да би музејски систем користио PostgreSQL базу.\n\n"
            "Наставити?"
        ):
            return

        try:
            self.db_status_text.delete('1.0', tk.END)
            self.db_status_text.insert('1.0', "Подешавам PostgreSQL ауто-старт...\n\n")

            # Step 1: Enable PostgreSQL
            self.db_status_text.insert(tk.END, "1. Омогућавам PostgreSQL за аутоматски старт...\n")
            result = self.run_sudo_command(['systemctl', 'enable', 'postgresql'])
            if result is None or result.returncode != 0:
                messagebox.showerror("Грешка", "Неуспешно омогућавање PostgreSQL")
                return
            self.db_status_text.insert(tk.END, "   ✓ PostgreSQL омогућен\n\n")

            # Step 2: Start PostgreSQL
            self.db_status_text.insert(tk.END, "2. Покрећем PostgreSQL сервис...\n")
            result = self.run_sudo_command(['systemctl', 'start', 'postgresql'])
            if result is None or result.returncode != 0:
                messagebox.showerror("Грешка", "Неуспешно покретање PostgreSQL")
                return
            time.sleep(2)
            self.db_status_text.insert(tk.END, "   ✓ PostgreSQL покренут\n\n")

            # Step 3: Backup museum-system.service
            self.db_status_text.insert(tk.END, "3. Правим резервну копију museum-system.service...\n")
            result = self.run_sudo_command([
                'cp',
                '/etc/systemd/system/museum-system.service',
                '/etc/systemd/system/museum-system.service.backup'
            ])
            if result is None or result.returncode != 0:
                self.db_status_text.insert(tk.END, "   ⚠️  Резервна копија није направљена (можда не постоји)\n\n")
            else:
                self.db_status_text.insert(tk.END, "   ✓ Резервна копија направљена\n\n")

            # Step 4: Update museum-system.service
            self.db_status_text.insert(tk.END, "4. Ажурирам museum-system.service са PostgreSQL зависношћу...\n")

            # Read the enable_postgres_autostart.sh script content for service file
            service_content = """[Unit]
Description=Museum Information System - Gunicorn
After=network.target postgresql.service
Requires=postgresql.service
Wants=postgresql.service

[Service]
Type=exec
User=nginx
Group=nginx
WorkingDirectory=/home/aleksandarlukovic/MuseumInfoSystem
Environment="PATH=/home/aleksandarlukovic/.local/bin:/usr/local/bin:/usr/bin:/bin"
Environment="PYTHONPATH=/home/aleksandarlukovic/MuseumInfoSystem"
Environment="FLASK_ENV=production"
Environment="GUNICORN_BIND=127.0.0.1:8000"
Environment="GUNICORN_PIDFILE=/run/museum/museum_info_system.pid"
Environment="LOG_DIR=/var/log/museum-info-system"
Environment="LOG_FILE=/var/log/museum-info-system/museum_info_system.log"
Environment="GUNICORN_RUN_USER=nginx"
Environment="GUNICORN_RUN_GROUP=nginx"
ExecStartPre=/usr/bin/mkdir -p /home/aleksandarlukovic/MuseumInfoSystem/storage/uploads
ExecStartPre=/usr/bin/rm -f /run/museum/museum_info_system.pid
ExecStart=/bin/bash /home/aleksandarlukovic/MuseumInfoSystem/systemd_start.sh
ExecReload=/bin/kill -s HUP $MAINPID
KillMode=mixed
TimeoutStopSec=35
PrivateTmp=true
Restart=always
RestartSec=10
ProtectSystem=strict
ProtectHome=read-only
NoNewPrivileges=true
ReadWritePaths=/home/aleksandarlukovic/MuseumInfoSystem/data
ReadWritePaths=/home/aleksandarlukovic/MuseumInfoSystem/exports
ReadWritePaths=/home/aleksandarlukovic/MuseumInfoSystem/storage
ReadWritePaths=/home/aleksandarlukovic/MuseumInfoSystem/flask_session
ReadWritePaths=/var/log/museum-info-system
ReadWritePaths=/run/museum
RuntimeDirectory=museum
LogsDirectory=museum-info-system

[Install]
WantedBy=multi-user.target
"""

            # Write to temporary file
            import tempfile
            with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.service') as tmp:
                tmp.write(service_content)
                tmp_path = tmp.name

            # Copy to systemd directory
            result = self.run_sudo_command([
                'cp',
                tmp_path,
                '/etc/systemd/system/museum-system.service'
            ])

            # Clean up temp file
            os.unlink(tmp_path)

            if result is None or result.returncode != 0:
                messagebox.showerror("Грешка", "Неуспешно ажурирање сервис фајла")
                return
            self.db_status_text.insert(tk.END, "   ✓ museum-system.service ажуриран\n\n")

            # Step 5: Reload systemd
            self.db_status_text.insert(tk.END, "5. Учитавам systemd конфигурацију...\n")
            result = self.run_sudo_command(['systemctl', 'daemon-reload'])
            if result is None or result.returncode != 0:
                messagebox.showerror("Грешка", "Неуспешан reload systemd")
                return
            self.db_status_text.insert(tk.END, "   ✓ Systemd конфигурација учитана\n\n")

            # Step 6: Restart museum-system
            self.db_status_text.insert(tk.END, "6. Рестартујем музејски систем...\n")
            result = self.run_sudo_command(['systemctl', 'restart', 'museum-system'])
            if result is None or result.returncode != 0:
                messagebox.showerror("Грешка", "Неуспешан рестарт музејског система")
                return
            time.sleep(2)
            self.db_status_text.insert(tk.END, "   ✓ Музејски систем рестартован\n\n")

            # Step 7: Verify
            self.db_status_text.insert(tk.END, "7. Верификација...\n")
            result = subprocess.run(
                ['systemctl', 'is-active', 'postgresql'],
                capture_output=True,
                text=True
            )
            pg_running = result.stdout.strip() == 'active'

            result = subprocess.run(
                ['systemctl', 'is-active', 'museum-system'],
                capture_output=True,
                text=True
            )
            museum_running = result.stdout.strip() == 'active'

            if pg_running and museum_running:
                self.db_status_text.insert(tk.END, "   ✓ PostgreSQL: Активан\n")
                self.db_status_text.insert(tk.END, "   ✓ Музејски систем: Активан\n\n")

                self.db_status_text.insert(tk.END, "="*60 + "\n")
                self.db_status_text.insert(tk.END, "✅ УСПЕШНО ЗАВРШЕНО!\n")
                self.db_status_text.insert(tk.END, "="*60 + "\n\n")
                self.db_status_text.insert(tk.END, "PostgreSQL ће сада:\n")
                self.db_status_text.insert(tk.END, "  • Покретати се аутоматски при подизању система\n")
                self.db_status_text.insert(tk.END, "  • Покретати се пре музејског система\n")
                self.db_status_text.insert(tk.END, "  • Бити коришћен као главна база података\n\n")
                self.db_status_text.insert(tk.END, "Проверите логове музејског система да потврдите да користи PostgreSQL.\n")

                messagebox.showinfo(
                    "Успех",
                    "✅ PostgreSQL ауто-старт је успешно подешен!\n\n"
                    "PostgreSQL и музејски систем су активни.\n"
                    "Системи ће се аутоматски покретати при подизању сервера."
                )
            else:
                self.db_status_text.insert(tk.END, f"   ⚠️  PostgreSQL: {'Активан' if pg_running else 'Неактиван'}\n")
                self.db_status_text.insert(tk.END, f"   ⚠️  Музејски систем: {'Активан' if museum_running else 'Неактиван'}\n")
                messagebox.showwarning(
                    "Упозорење",
                    "Конфигурација је примењена, али неки сервиси можда нису активни.\n"
                    "Проверите статус у табу 'Сервиси'."
                )

            # Update service status
            self.update_service_status()

        except Exception as e:
            self.db_status_text.insert(tk.END, f"\n\n❌ ГРЕШКА: {str(e)}\n")
            messagebox.showerror("Грешка", f"Грешка приликом подешавања:\n{str(e)}")

    def backup_databases(self):
        """Backup databases"""
        messagebox.showinfo("Информација", "Функција резервне копије је у развоју")

    def show_database_stats(self):
        """Show database statistics"""
        messagebox.showinfo("Информација", "Функција статистике је у развоју")

    def optimize_databases(self):
        """Optimize databases"""
        messagebox.showinfo("Информација", "Функција оптимизације је у развоју")

    def open_postgres_control_app(self):
        """Start the local PostgreSQL browser app and open it in the browser."""
        if not POSTGRES_CONTROL_ROOT.exists():
            messagebox.showerror(
                "PostgreSQL Browser",
                f"Апликација није пронађена:\n{POSTGRES_CONTROL_ROOT}"
            )
            return

        if not (POSTGRES_CONTROL_ROOT / 'app.py').exists():
            messagebox.showerror(
                "PostgreSQL Browser",
                f"Недостаје app.py у:\n{POSTGRES_CONTROL_ROOT}"
            )
            return

        self.db_status_text.delete('1.0', tk.END)
        self.db_status_text.insert('1.0', "Покрећем PostgreSQL Browser...\n\n")

        try:
            if self.check_port(POSTGRES_CONTROL_PORT):
                self.db_status_text.insert(
                    tk.END,
                    f"✅ PostgreSQL Browser је већ активан: {POSTGRES_CONTROL_URL}\n"
                )
            else:
                logs_dir = POSTGRES_CONTROL_ROOT / 'logs'
                logs_dir.mkdir(exist_ok=True)
                log_path = logs_dir / 'postgres_control_app.log'
                log_handle = open(log_path, 'a', encoding='utf-8')
                try:
                    subprocess.Popen(
                        ['python3', 'app.py'],
                        cwd=str(POSTGRES_CONTROL_ROOT),
                        stdout=log_handle,
                        stderr=subprocess.STDOUT,
                        start_new_session=True
                    )
                finally:
                    log_handle.close()

                for _attempt in range(15):
                    time.sleep(0.3)
                    if self.check_port(POSTGRES_CONTROL_PORT):
                        break

                if not self.check_port(POSTGRES_CONTROL_PORT):
                    self.db_status_text.insert(
                        tk.END,
                        f"❌ Није успело покретање. Проверите лог:\n{log_path}\n"
                    )
                    messagebox.showerror(
                        "PostgreSQL Browser",
                        f"Није успело покретање PostgreSQL Browser-а.\n\nЛог:\n{log_path}"
                    )
                    return

                self.db_status_text.insert(
                    tk.END,
                    f"✅ PostgreSQL Browser покренут: {POSTGRES_CONTROL_URL}\n"
                    f"Лог: {log_path}\n"
                )

            self.db_status_text.insert(
                tk.END,
                "\nУнесите PostgreSQL корисника и лозинку у отвореном прозору, затим изаберите базу.\n"
            )
            self.open_browser(POSTGRES_CONTROL_URL)
        except Exception as exc:
            self.db_status_text.insert(tk.END, f"❌ Грешка: {exc}\n")
            messagebox.showerror("PostgreSQL Browser", f"Грешка:\n{exc}")
    
    def open_browser(self, url):
        """Open URL in browser"""
        subprocess.Popen(['xdg-open', url])

    def append_qa_output(self, text):
        self.qa_output_text.insert(tk.END, text)
        self.qa_output_text.see(tk.END)

    def clear_qa_output(self):
        self.qa_output_text.delete('1.0', tk.END)

    def open_qa_log(self):
        if self.qa_log_path.exists():
            subprocess.Popen(['xdg-open', str(self.qa_log_path)])
        else:
            messagebox.showinfo("Информација", f"Лог фајл још не постоји:\n{self.qa_log_path}")

    def build_qa_runner_options(self):
        options = {
            'QA_SERVER_MODE': self.qa_server_mode_var.get(),
            'QA_INCLUDE_LINT': '1' if self.qa_include_lint_var.get() else '0',
            'QA_INCLUDE_CYPRESS': '1' if self.qa_include_cypress_var.get() else '0',
            'QA_INCLUDE_PLAYWRIGHT': '1' if self.qa_include_playwright_var.get() else '0',
            'QA_INCLUDE_K6': '1' if self.qa_include_k6_var.get() else '0',
            'QA_USE_REDIS': '1' if self.qa_use_redis_var.get() else '0',
        }
        for env_key, var in self.qa_credential_vars.items():
            value = var.get().strip()
            if value:
                options[env_key] = value
        return options

    def load_qa_credentials(self):
        env = build_qa_environment(PROJECT_ROOT / '.env')
        for env_key, var in self.qa_credential_vars.items():
            var.set(env.get(env_key, ''))
        self.autofill_qa_credentials(show_dialog=False)

    def clear_qa_credentials(self):
        for var in self.qa_credential_vars.values():
            var.set('')

    def save_qa_credentials(self):
        lines = [
            "# QA credentials for Cypress/Playwright runs",
            "# Stored separately from the main .env on purpose.",
        ]
        for env_key, var in self.qa_credential_vars.items():
            value = var.get().strip()
            if value:
                lines.append(f"{env_key}={value}")

        QA_ENV_FILE.write_text('\n'.join(lines) + '\n', encoding='utf-8')
        messagebox.showinfo("Успех", f"QA креденцијали су сачувани у:\n{QA_ENV_FILE}")

    def fetch_qa_db_candidate_rows(self):
        try:
            result = subprocess.run(
                [
                    'psql',
                    '-U', _DB_USER,
                    '-d', _DB_NAME,
                    '-t', '-A', '-F', '|',
                    '-c',
                    """SELECT COALESCE(r.name, 'employee') AS role, u.email
                       FROM users u
                       LEFT JOIN roles r ON u.role_id = r.id
                       WHERE u.is_active = TRUE
                       ORDER BY CASE WHEN COALESCE(r.name, 'employee') = 'admin' THEN 0 ELSE 1 END,
                                u.full_name"""
                ],
                capture_output=True,
                text=True,
                timeout=5
            )
        except (subprocess.TimeoutExpired, OSError):
            return []

        if result.returncode != 0:
            return []

        rows = []
        for raw_line in result.stdout.strip().splitlines():
            if not raw_line:
                continue
            role, _, email = raw_line.partition('|')
            rows.append((role.strip().lower() or 'employee', email.strip()))
        return rows

    def autofill_qa_credentials(self, show_dialog=True):
        env = build_qa_environment(PROJECT_ROOT / '.env')
        defaults = build_qa_email_defaults(
            env,
            directory_entries=load_employee_directory_entries(),
            db_rows=self.fetch_qa_db_candidate_rows(),
        )

        updated_fields = []
        for env_key, value in defaults.items():
            if env_key not in QA_EMAIL_FIELDS:
                continue
            current = self.qa_credential_vars[env_key].get().strip()
            if current:
                continue
            self.qa_credential_vars[env_key].set(value)
            updated_fields.append(env_key)

        if show_dialog:
            if updated_fields:
                messagebox.showinfo(
                    "Аутопопуна QA",
                    "QA email поља су попуњена из локалне конфигурације и базе."
                )
            else:
                messagebox.showinfo(
                    "Аутопопуна QA",
                    "Нема нових QA email вредности за попуну.\n"
                    "Очистите поља ако желите поновну аутопопуну."
                )

    def start_qa_suite(self):
        if self.qa_process and self.qa_process.poll() is None:
            messagebox.showwarning("Упозорење", "QA пакет је већ покренут.")
            return

        runner_options = self.build_qa_runner_options()
        env = build_qa_environment(PROJECT_ROOT / '.env', runner_options)
        if qa_run_needs_browser_credentials(runner_options):
            missing_vars = get_missing_qa_env_vars(env)
        else:
            missing_vars = []
        if missing_vars:
            messagebox.showerror(
                "Недостају QA променљиве",
                "QA пакет захтева следеће променљиве окружења:\n\n"
                + '\n'.join(missing_vars)
            )
            return

        log_dir = self.qa_log_path.parent
        log_dir.mkdir(parents=True, exist_ok=True)
        self.qa_log_handle = open(self.qa_log_path, 'w', encoding='utf-8')

        command = ['/bin/bash', str(PROJECT_ROOT / 'run_qa.sh')]
        self.clear_qa_output()
        self.append_qa_output("Покрећем QA пакет...\n")
        self.append_qa_output(f"Команда: {' '.join(command)}\n")
        self.append_qa_output(f"Режим: {env['QA_SERVER_MODE']}\n\n")

        try:
            self.qa_process = subprocess.Popen(
                command,
                cwd=str(PROJECT_ROOT),
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1,
                env=env,
            )
        except Exception as exc:
            if self.qa_log_handle:
                self.qa_log_handle.close()
                self.qa_log_handle = None
            self.qa_status_var.set("Неуспешно покретање QA пакета")
            messagebox.showerror("Грешка", f"Не могу да покренем QA пакет:\n{exc}")
            return

        self.qa_status_var.set("QA пакет је у току...")
        self.qa_start_button.config(state='disabled')
        self.qa_stop_button.config(state='normal')

        reader_thread = threading.Thread(target=self._stream_qa_output, daemon=True)
        reader_thread.start()
        self.root.after(150, self.poll_qa_output)

    def _stream_qa_output(self):
        if not self.qa_process or not self.qa_process.stdout:
            return

        try:
            for line in self.qa_process.stdout:
                self.qa_output_queue.put(line)
                if self.qa_log_handle and not self.qa_log_handle.closed:
                    self.qa_log_handle.write(line)
                    self.qa_log_handle.flush()
        finally:
            if self.qa_process.stdout:
                self.qa_process.stdout.close()

    def poll_qa_output(self):
        while True:
            try:
                line = self.qa_output_queue.get_nowait()
            except queue.Empty:
                break
            self.append_qa_output(line)

        if self.qa_process and self.qa_process.poll() is None:
            self.root.after(150, self.poll_qa_output)
            return

        if self.qa_process:
            exit_code = self.qa_process.poll()
            self.finish_qa_suite(exit_code if exit_code is not None else 1)

    def finish_qa_suite(self, exit_code):
        while True:
            try:
                line = self.qa_output_queue.get_nowait()
            except queue.Empty:
                break
            self.append_qa_output(line)

        if self.qa_log_handle:
            self.qa_log_handle.close()
            self.qa_log_handle = None

        self.qa_process = None
        self.qa_start_button.config(state='normal')
        self.qa_stop_button.config(state='disabled')

        if exit_code == 0:
            self.qa_status_var.set("QA пакет је успешно завршен")
            self.append_qa_output("\nQA пакет је успешно завршен.\n")
        else:
            self.qa_status_var.set(f"QA пакет је неуспешан (код {exit_code})")
            self.append_qa_output(f"\nQA пакет је завршен са грешком (код {exit_code}).\n")

    def stop_qa_suite(self):
        if not self.qa_process or self.qa_process.poll() is not None:
            self.qa_status_var.set("Нема активног QA процеса")
            self.qa_stop_button.config(state='disabled')
            self.qa_start_button.config(state='normal')
            return

        self.append_qa_output("\nПокушавам да зауставим QA пакет...\n")
        self.qa_process.terminate()
        self.qa_status_var.set("QA пакет се зауставља...")

    def setup_users_tab(self):
        """Setup user management / password manager tab"""
        users_frame = tk.Frame(self.users_tab)
        users_frame.pack(fill='both', expand=True, padx=20, pady=20)

        # Header
        header_frame = tk.Frame(users_frame)
        header_frame.pack(fill='x', pady=(0, 15))

        tk.Label(
            header_frame,
            text="🔑 Менаџер лозинки",
            font=('Arial', 14, 'bold')
        ).pack(side='left')

        tk.Button(
            header_frame,
            text="🔄 Освежи листу",
            command=self.load_users_list,
            bg='#2196F3',
            fg='white',
            padx=15,
            pady=5
        ).pack(side='right')

        # Users list frame
        list_frame = tk.LabelFrame(users_frame, text="Листа корисника", font=('Arial', 11, 'bold'), padx=10, pady=10)
        list_frame.pack(fill='both', expand=True, pady=(0, 15))

        # Treeview for users
        columns = ('email', 'full_name', 'role', 'status', 'last_login')
        self.users_tree = ttk.Treeview(list_frame, columns=columns, show='headings', height=12)

        self.users_tree.heading('email', text='Email')
        self.users_tree.heading('full_name', text='Име и презиме')
        self.users_tree.heading('role', text='Улога')
        self.users_tree.heading('status', text='Статус')
        self.users_tree.heading('last_login', text='Последња пријава')

        self.users_tree.column('email', width=200)
        self.users_tree.column('full_name', width=180)
        self.users_tree.column('role', width=80)
        self.users_tree.column('status', width=120)
        self.users_tree.column('last_login', width=150)

        scrollbar = ttk.Scrollbar(list_frame, orient='vertical', command=self.users_tree.yview)
        self.users_tree.configure(yscrollcommand=scrollbar.set)

        self.users_tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')

        # Action buttons frame
        actions_frame = tk.LabelFrame(users_frame, text="Акције", font=('Arial', 11, 'bold'), padx=10, pady=10)
        actions_frame.pack(fill='x', pady=(0, 15))

        button_row1 = tk.Frame(actions_frame)
        button_row1.pack(fill='x', pady=5)

        tk.Button(
            button_row1,
            text="🔑 Ресетуј лозинку",
            command=self.reset_user_password,
            bg='#FF9800',
            fg='white',
            font=('Arial', 10, 'bold'),
            padx=20,
            pady=8
        ).pack(side='left', padx=5)

        tk.Button(
            button_row1,
            text="🔄 Захтевај промену",
            command=self.force_password_change,
            bg='#9C27B0',
            fg='white',
            font=('Arial', 10, 'bold'),
            padx=20,
            pady=8
        ).pack(side='left', padx=5)

        tk.Button(
            button_row1,
            text="✅ Активирај/Деактивирај",
            command=self.toggle_user_status,
            bg='#607D8B',
            fg='white',
            font=('Arial', 10, 'bold'),
            padx=20,
            pady=8
        ).pack(side='left', padx=5)

        tk.Button(
            button_row1,
            text="🎲 Генериши лозинку",
            command=self.show_generated_password,
            bg='#00BCD4',
            fg='white',
            font=('Arial', 10, 'bold'),
            padx=20,
            pady=8
        ).pack(side='left', padx=5)

        # Second row of buttons
        button_row2 = tk.Frame(actions_frame)
        button_row2.pack(fill='x', pady=5)

        tk.Button(
            button_row2,
            text="🔓 Ресетуј и прикажи",
            command=self.reset_and_show_password,
            bg='#E91E63',
            fg='white',
            font=('Arial', 10, 'bold'),
            padx=20,
            pady=8
        ).pack(side='left', padx=5)

        tk.Button(
            button_row2,
            text="⏱️ Привремена лозинка",
            command=self.set_temporary_password,
            bg='#795548',
            fg='white',
            font=('Arial', 10, 'bold'),
            padx=20,
            pady=8
        ).pack(side='left', padx=5)

        # Password generator frame
        gen_frame = tk.LabelFrame(users_frame, text="Генератор лозинке", font=('Arial', 11, 'bold'), padx=10, pady=10)
        gen_frame.pack(fill='x')

        gen_inner = tk.Frame(gen_frame)
        gen_inner.pack(fill='x')

        tk.Label(gen_inner, text="Генерисана лозинка:", font=('Arial', 10)).pack(side='left', padx=5)

        self.generated_password_var = tk.StringVar()
        self.password_entry = tk.Entry(
            gen_inner,
            textvariable=self.generated_password_var,
            font=('Courier', 12),
            width=30,
            state='readonly'
        )
        self.password_entry.pack(side='left', padx=5)

        tk.Button(
            gen_inner,
            text="📋 Копирај",
            command=self.copy_generated_password,
            padx=10
        ).pack(side='left', padx=5)

        tk.Button(
            gen_inner,
            text="🎲 Нова",
            command=self.generate_new_password,
            padx=10
        ).pack(side='left', padx=5)

        # Password policy info
        policy_frame = tk.Frame(gen_frame)
        policy_frame.pack(fill='x', pady=(10, 0))

        tk.Label(
            policy_frame,
            text="Политика лозинки: мин. 8 карактера, велико слово, мало слово, број, специјални карактер",
            font=('Arial', 9),
            fg='#666666'
        ).pack(anchor='w')

        # Load users on start
        self.root.after(500, self.load_users_list)

    def load_users_list(self):
        """Load users from PostgreSQL database"""
        # Clear existing items
        for item in self.users_tree.get_children():
            self.users_tree.delete(item)

        try:
            result = subprocess.run(
                ['psql', '-U', _DB_USER, '-d', _DB_NAME, '-t', '-A', '-F', '|', '-c',
                 """SELECT u.email, u.full_name, COALESCE(r.name, 'employee') as role,
                    CASE WHEN u.is_active THEN
                        CASE WHEN u.is_first_login THEN 'Прва пријава' ELSE 'Активан' END
                    ELSE 'Неактиван' END as status,
                    COALESCE(TO_CHAR(u.last_login_at, 'DD.MM.YYYY HH24:MI'), 'Никад') as last_login
                    FROM users u
                    LEFT JOIN roles r ON u.role_id = r.id
                    ORDER BY u.full_name"""],
                capture_output=True,
                text=True,
                timeout=5
            )

            if result.returncode == 0:
                for line in result.stdout.strip().split('\n'):
                    if line:
                        parts = line.split('|')
                        if len(parts) >= 5:
                            email, full_name, role, status, last_login = parts[:5]
                            role_display = 'Админ' if role == 'admin' else 'Запослени'
                            self.users_tree.insert('', 'end', values=(email, full_name, role_display, status, last_login))
            else:
                messagebox.showerror("Грешка", f"Грешка при учитавању корисника:\n{result.stderr}")
        except subprocess.TimeoutExpired:
            messagebox.showerror("Грешка", "Timeout при повезивању са базом")
        except Exception as e:
            messagebox.showerror("Грешка", f"Грешка: {str(e)}")

    def get_selected_user(self):
        """Get currently selected user from tree"""
        selection = self.users_tree.selection()
        if not selection:
            messagebox.showwarning("Упозорење", "Молимо изаберите корисника из листе.")
            return None
        item = self.users_tree.item(selection[0])
        return item['values']  # (email, full_name, role, status, last_login)

    def reset_user_password(self):
        """Reset password for selected user"""
        user = self.get_selected_user()
        if not user:
            return

        email, full_name, role, status, _ = user

        # Ask for new password
        new_password = simpledialog.askstring(
            "Ресетуј лозинку",
            f"Унесите нову лозинку за корисника:\n{full_name} ({email})\n\n"
            f"Или оставите празно за аутоматски генерисану лозинку:",
            parent=self.root
        )

        if new_password is None:  # Cancelled
            return

        if new_password == '':
            # Generate password
            new_password = self.generate_strong_password()
            messagebox.showinfo(
                "Генерисана лозинка",
                f"Генерисана лозинка за {full_name}:\n\n{new_password}\n\n"
                "Запамтите ову лозинку!"
            )

        # Ask about force change
        force_change = messagebox.askyesno(
            "Захтевај промену",
            "Да ли да корисник мора да промени лозинку при следећој пријави?"
        )

        try:
            # Hash the password using bcrypt via Python (in-process)
            password_hash, salt = hash_password_for_storage(new_password)

            # Update in database
            is_first_login = 'TRUE' if force_change else 'FALSE'
            update_command, update_sql = build_user_update_command(
                set_clause="password_hash = :'password_hash', "
                           "salt = :'salt', "
                           "is_first_login = :first_login, "
                           "auth_version = auth_version + 1, "
                           "updated_at = NOW()",
                email=email,
                variables={
                    'password_hash': password_hash,
                    'salt': salt,
                    'first_login': is_first_login,
                },
            )

            result = subprocess.run(
                update_command,
                input=update_sql,
                capture_output=True,
                text=True,
                timeout=5
            )

            if result.returncode == 0:
                messagebox.showinfo("Успех", f"Лозинка за {full_name} је успешно ресетована!")
                self.load_users_list()
            else:
                messagebox.showerror("Грешка", f"Грешка при ажурирању:\n{result.stderr}")

        except Exception as e:
            messagebox.showerror("Грешка", f"Грешка: {str(e)}")

    def force_password_change(self):
        """Force user to change password on next login"""
        user = self.get_selected_user()
        if not user:
            return

        email, full_name, role, status, _ = user

        if status == 'Прва пријава':
            messagebox.showinfo("Информација", f"Корисник {full_name} већ мора да промени лозинку.")
            return

        if not messagebox.askyesno(
            "Потврда",
            f"Да ли сте сигурни да желите да захтевате промену лозинке за:\n{full_name} ({email})?"
        ):
            return

        try:
            update_command, update_sql = build_user_update_command(
                set_clause="is_first_login = TRUE, updated_at = NOW()",
                email=email,
            )

            result = subprocess.run(
                update_command,
                input=update_sql,
                capture_output=True,
                text=True,
                timeout=5
            )

            if result.returncode == 0:
                messagebox.showinfo("Успех", f"Корисник {full_name} мора да промени лозинку при следећој пријави.")
                self.load_users_list()
            else:
                messagebox.showerror("Грешка", f"Грешка:\n{result.stderr}")

        except Exception as e:
            messagebox.showerror("Грешка", f"Грешка: {str(e)}")

    def toggle_user_status(self):
        """Activate or deactivate user"""
        user = self.get_selected_user()
        if not user:
            return

        email, full_name, role, status, _ = user

        is_active = status != 'Неактиван'
        new_status = not is_active
        action = "деактивирате" if is_active else "активирате"
        new_status_text = "деактивиран" if is_active else "активиран"

        if not messagebox.askyesno(
            "Потврда",
            f"Да ли сте сигурни да желите да {action} корисника:\n{full_name} ({email})?"
        ):
            return

        try:
            update_command, update_sql = build_user_update_command(
                set_clause="is_active = :is_active, auth_version = auth_version + 1, updated_at = NOW()",
                email=email,
                variables={'is_active': str(new_status).upper()},
            )

            result = subprocess.run(
                update_command,
                input=update_sql,
                capture_output=True,
                text=True,
                timeout=5
            )

            if result.returncode == 0:
                messagebox.showinfo("Успех", f"Корисник {full_name} је {new_status_text}.")
                self.load_users_list()
            else:
                messagebox.showerror("Грешка", f"Грешка:\n{result.stderr}")

        except Exception as e:
            messagebox.showerror("Грешка", f"Грешка: {str(e)}")

    def reset_and_show_password(self):
        """Reset password to a new generated one and show it to admin"""
        user = self.get_selected_user()
        if not user:
            return

        email, full_name, role, status, _ = user

        if not messagebox.askyesno(
            "Потврда",
            f"Да ли сте сигурни да желите да ресетујете лозинку за:\n{full_name} ({email})?\n\n"
            "Нова лозинка ће бити генерисана и приказана."
        ):
            return

        # Generate new password
        new_password = self.generate_strong_password()

        try:
            # Hash the password using bcrypt via Python (in-process)
            password_hash, salt = hash_password_for_storage(new_password)

            # Update in database with force change on next login
            update_command, update_sql = build_user_update_command(
                set_clause="password_hash = :'password_hash', "
                           "salt = :'salt', "
                           "is_first_login = TRUE, "
                           "auth_version = auth_version + 1, "
                           "updated_at = NOW()",
                email=email,
                variables={
                    'password_hash': password_hash,
                    'salt': salt,
                },
            )

            result = subprocess.run(
                update_command,
                input=update_sql,
                capture_output=True,
                text=True,
                timeout=5
            )

            if result.returncode == 0:
                # Show password in a dialog and copy to clipboard
                self.generated_password_var.set(new_password)
                self.root.clipboard_clear()
                self.root.clipboard_append(new_password)
                self.root.update()

                messagebox.showinfo(
                    "Лозинка ресетована",
                    f"Лозинка за {full_name} је успешно ресетована!\n\n"
                    f"═══════════════════════════════\n"
                    f"НОВА ЛОЗИНКА:\n\n"
                    f"{new_password}\n"
                    f"═══════════════════════════════\n\n"
                    f"Лозинка је копирана у клипборд.\n\n"
                    f"Корисник мора да промени лозинку\n"
                    f"при следећој пријави."
                )
                self.load_users_list()
            else:
                messagebox.showerror("Грешка", f"Грешка при ажурирању:\n{result.stderr}")

        except Exception as e:
            messagebox.showerror("Грешка", f"Грешка: {str(e)}")

    def set_temporary_password(self):
        """Set a known temporary password for user"""
        user = self.get_selected_user()
        if not user:
            return

        email, full_name, role, status, _ = user

        # Default temporary password
        temp_password = "Muzej2024!"

        # Ask admin if they want to change it
        custom_pass = simpledialog.askstring(
            "Привремена лозинка",
            f"Постављање привремене лозинке за:\n{full_name} ({email})\n\n"
            f"Подразумевана привремена лозинка: {temp_password}\n\n"
            f"Унесите другу лозинку или оставите празно за подразумевану:",
            parent=self.root
        )

        if custom_pass is None:  # Cancelled
            return

        if custom_pass.strip():
            temp_password = custom_pass.strip()

        if not messagebox.askyesno(
            "Потврда",
            f"Да ли сте сигурни да желите да поставите привремену лозинку:\n\n"
            f"Корисник: {full_name}\n"
            f"Лозинка: {temp_password}\n\n"
            f"Корисник ће морати да промени лозинку при следећој пријави."
        ):
            return

        try:
            # Hash the password using bcrypt via Python (in-process)
            password_hash, salt = hash_password_for_storage(temp_password)

            # Update in database with force change on next login
            update_command, update_sql = build_user_update_command(
                set_clause="password_hash = :'password_hash', "
                           "salt = :'salt', "
                           "is_first_login = TRUE, "
                           "auth_version = auth_version + 1, "
                           "updated_at = NOW()",
                email=email,
                variables={
                    'password_hash': password_hash,
                    'salt': salt,
                },
            )

            result = subprocess.run(
                update_command,
                input=update_sql,
                capture_output=True,
                text=True,
                timeout=5
            )

            if result.returncode == 0:
                # Copy to clipboard
                self.root.clipboard_clear()
                self.root.clipboard_append(temp_password)
                self.root.update()

                messagebox.showinfo(
                    "Успех",
                    f"Привремена лозинка за {full_name} је постављена!\n\n"
                    f"═══════════════════════════════\n"
                    f"ПРИВРЕМЕНА ЛОЗИНКА:\n\n"
                    f"{temp_password}\n"
                    f"═══════════════════════════════\n\n"
                    f"Лозинка је копирана у клипборд.\n\n"
                    f"Корисник МОРА да промени лозинку\n"
                    f"при следећој пријави!"
                )
                self.load_users_list()
            else:
                messagebox.showerror("Грешка", f"Грешка при ажурирању:\n{result.stderr}")

        except Exception as e:
            messagebox.showerror("Грешка", f"Грешка: {str(e)}")

    def generate_strong_password(self, length=16):
        """Generate a strong random password"""
        import secrets
        import string

        alphabet = string.ascii_letters + string.digits + '!@#$%^&*()'

        while True:
            password = ''.join(secrets.choice(alphabet) for _ in range(length))
            # Check requirements
            has_upper = any(c.isupper() for c in password)
            has_lower = any(c.islower() for c in password)
            has_digit = any(c.isdigit() for c in password)
            has_special = any(c in '!@#$%^&*()' for c in password)

            if has_upper and has_lower and has_digit and has_special:
                return password

    def generate_new_password(self):
        """Generate and display a new password"""
        password = self.generate_strong_password()
        self.generated_password_var.set(password)

    def show_generated_password(self):
        """Generate and show password in dialog"""
        password = self.generate_strong_password()
        self.generated_password_var.set(password)
        messagebox.showinfo(
            "Генерисана лозинка",
            f"Нова јака лозинка:\n\n{password}\n\n"
            "Лозинка је такође приказана у пољу испод листе корисника."
        )

    def copy_generated_password(self):
        """Copy generated password to clipboard"""
        password = self.generated_password_var.get()
        if password:
            self.root.clipboard_clear()
            self.root.clipboard_append(password)
            self.root.update()
            messagebox.showinfo("Копирано", "Лозинка је копирана у клипборд!")
        else:
            messagebox.showwarning("Упозорење", "Нема генерисане лозинке за копирање.")

def main():
    root = tk.Tk()
    app = MuseumControlCenter(root)
    root.mainloop()

if __name__ == '__main__':
    main()
