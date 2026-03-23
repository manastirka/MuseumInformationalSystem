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
import psutil
import threading
import time
from datetime import datetime
import requests
import secrets
import string

class MuseumControlCenter:
    def __init__(self, root):
        self.root = root
        self.root.title("Центар за контролу - Информациони систем музеја")
        self.root.geometry("1200x800")

        # Cache for sudo password (valid for session)
        self.sudo_password = None
        
        # Service configurations
        # Note: Mineral Database and Timesheet are now integrated into the main Museum System
        # Access them at: http://192.168.144.48/mineral_database and http://192.168.144.48/timesheet
        self.services = {
            'postgresql': {
                'name': 'PostgreSQL База података',
                'port': 5432,
                'path': '/var/lib/pgsql',
                'service_type': 'systemd',
                'systemd_service': 'postgresql',
                'log': None,  # Uses journalctl
                'icon': '🐘',
                'status': 'stopped',
                'description': 'PostgreSQL сервер за све музејске базе података',
                'order': 1  # Start first
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
                'order': 3
            },
            'museum_system': {
                'name': 'Музејски Информациони Систем',
                'port': 8000,  # Internal port, accessed via nginx on port 80
                'path': '/home/aleksandarlukovic/MuseumInfoSystem',
                'service_type': 'systemd',
                'systemd_service': 'museum-system',
                'log': 'logs/gunicorn_error.log',
                'icon': '🏛️',
                'status': 'stopped',
                'description': 'Главни музејски систем (укључује базу минерала и радне листе)',
                'order': 2
            },
            'main_app_dev': {
                'name': 'Развојни Сервер (Dev Mode)',
                'port': 5000,
                'path': '/home/aleksandarlukovic/MuseumInfoSystem',
                'command': ['python3', 'app.py'],
                'log': 'logs/main_app.log',
                'pid_file': 'logs/main_app.pid',
                'icon': '🔧',
                'status': 'stopped',
                'service_type': 'process',
                'description': 'Само за развој и тестирање (не користити у продукцији)',
                'order': 99
            }
        }
        
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

        # Tab 5: User Management / Password Manager
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
    
    def setup_services_tab(self):
        """Setup services control tab"""
        # Services control frame
        services_frame = tk.Frame(self.services_tab)
        services_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        self.service_widgets = {}
        
        for service_id, service in self.services.items():
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

        self.log_service_var = tk.StringVar(value='postgresql')
        service_combo = ttk.Combobox(
            control_frame,
            textvariable=self.log_service_var,
            values=['postgresql', 'nginx', 'museum_system', 'main_app_dev'],
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
            if conn.laddr.port == port and conn.status == 'LISTEN':
                return True
        return False
    
    def get_pid_on_port(self, port):
        """Get PID of process using a port"""
        for conn in psutil.net_connections():
            if conn.laddr.port == port and conn.status == 'LISTEN':
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
    
    def start_service(self, service_id):
        """Start a service"""
        service = self.services[service_id]

        # Check if already running
        if self.is_systemd_service(service):
            if self.check_systemd_status(service['systemd_service']):
                messagebox.showwarning("Упозорење", f"{service['name']} је већ покренут!")
                return
        else:
            if self.check_port(service['port']):
                messagebox.showwarning("Упозорење", f"{service['name']} је већ покренут!")
                return

        try:
            if self.is_systemd_service(service):
                # Start systemd service with password prompt
                result = self.run_sudo_command(['systemctl', 'start', service['systemd_service']])

                if result is None:
                    return  # User cancelled password prompt

                if result.returncode != 0:
                    error_msg = result.stderr if result.stderr else result.stdout
                    messagebox.showerror("Грешка", f"Грешка при покретању:\n{error_msg}")
                    return

                time.sleep(2)

                if self.check_systemd_status(service['systemd_service']):
                    messagebox.showinfo("Успех", f"{service['name']} је успешно покренут!")
                    self.update_service_status()
                else:
                    messagebox.showerror("Грешка", f"Проблем приликом покретања {service['name']}")
            else:
                # Start regular process
                os.chdir(service['path'])

                # Start process
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
                    messagebox.showinfo("Успех", f"{service['name']} је успешно покренут!")
                    self.update_service_status()
                else:
                    messagebox.showerror("Грешка", f"Проблем приликом покретања {service['name']}")

        except Exception as e:
            messagebox.showerror("Грешка", f"Грешка: {str(e)}")
    
    def stop_service(self, service_id):
        """Stop a service"""
        service = self.services[service_id]

        # Check if running
        if self.is_systemd_service(service):
            if not self.check_systemd_status(service['systemd_service']):
                messagebox.showwarning("Упозорење", f"{service['name']} није покренут!")
                return
        else:
            pid = self.get_pid_on_port(service['port'])
            if not pid:
                messagebox.showwarning("Упозорење", f"{service['name']} није покренут!")
                return

        try:
            if self.is_systemd_service(service):
                # Stop systemd service with password prompt
                result = self.run_sudo_command(['systemctl', 'stop', service['systemd_service']])

                if result is None:
                    return  # User cancelled password prompt

                if result.returncode != 0:
                    error_msg = result.stderr if result.stderr else result.stdout
                    messagebox.showerror("Грешка", f"Грешка при заустављању:\n{error_msg}")
                    return

                time.sleep(1)
                messagebox.showinfo("Успех", f"{service['name']} је заустављен!")
                self.update_service_status()
            else:
                # Kill regular process
                pid = self.get_pid_on_port(service['port'])
                os.kill(pid, signal.SIGTERM)
                time.sleep(1)

                # Force kill if still running
                if self.check_port(service['port']):
                    os.kill(pid, signal.SIGKILL)

                messagebox.showinfo("Успех", f"{service['name']} је заустављен!")
                self.update_service_status()

        except Exception as e:
            messagebox.showerror("Грешка", f"Грешка: {str(e)}")
    
    def restart_service(self, service_id):
        """Restart a service"""
        service = self.services[service_id]

        try:
            if self.is_systemd_service(service):
                # Use systemd restart command with password prompt
                result = self.run_sudo_command(['systemctl', 'restart', service['systemd_service']])

                if result is None:
                    return  # User cancelled password prompt

                if result.returncode != 0:
                    error_msg = result.stderr if result.stderr else result.stdout
                    messagebox.showerror("Грешка", f"Грешка при рестартовању:\n{error_msg}")
                    return

                time.sleep(2)
                messagebox.showinfo("Успех", f"{service['name']} је рестартован!")
                self.update_service_status()
            else:
                # Regular process - stop then start
                self.stop_service(service_id)
                time.sleep(2)
                self.start_service(service_id)

        except Exception as e:
            messagebox.showerror("Грешка", f"Грешка: {str(e)}")
    
    def start_all_services(self):
        """Start all services in correct order"""
        # Sort services by order field (PostgreSQL first, then museum system, then nginx)
        sorted_services = sorted(
            self.services.items(),
            key=lambda x: x[1].get('order', 50)
        )

        for service_id, service in sorted_services:
            if service['status'] != 'running':
                self.start_service(service_id)
                time.sleep(3)
    
    def stop_all_services(self):
        """Stop all services"""
        for service_id in self.services.keys():
            if self.services[service_id]['status'] == 'running':
                self.stop_service(service_id)
                time.sleep(1)
    
    def restart_all_services(self):
        """Restart all services"""
        self.stop_all_services()
        time.sleep(3)
        self.start_all_services()
    
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
                        ['psql', '-U', 'aleksandarlukovic', '-d', 'museum_system', '-c', 'SELECT version();'],
                        capture_output=True,
                        text=True,
                        timeout=2
                    )
                    if result.returncode == 0:
                        version_line = result.stdout.split('\n')[2].strip()
                        self.db_status_text.insert(tk.END, f"   ✅ Верзија: {version_line}\n")

                        # Get database size
                        result = subprocess.run(
                            ['psql', '-U', 'aleksandarlukovic', '-d', 'museum_system', '-t', '-c',
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
                            ['psql', '-U', 'aleksandarlukovic', '-d', 'museum_system', '-t', '-c',
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
User=aleksandarlukovic
Group=aleksandarlukovic
WorkingDirectory=/home/aleksandarlukovic/MuseumInfoSystem
Environment="PATH=/home/aleksandarlukovic/.local/bin:/usr/local/bin:/usr/bin:/bin"
Environment="PYTHONPATH=/home/aleksandarlukovic/MuseumInfoSystem"
Environment="ENABLE_FALLBACK_AUTH=True"
Environment="FLASK_ENV=development"
ExecStart=/usr/bin/python3 -m gunicorn --config gunicorn.conf.py wsgi:application
ExecReload=/bin/kill -s HUP $MAINPID
KillMode=mixed
TimeoutStopSec=5
PrivateTmp=false
Restart=always
RestartSec=10

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
    
    def open_browser(self, url):
        """Open URL in browser"""
        subprocess.Popen(['xdg-open', url])

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
                ['psql', '-U', 'aleksandarlukovic', '-d', 'museum_system', '-t', '-A', '-F', '|', '-c',
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
            # Hash the password using bcrypt via Python
            hash_script = f'''
import sys
sys.path.insert(0, '/home/aleksandarlukovic/MuseumInfoSystem')
from security_utils import PasswordHasher
hasher = PasswordHasher()
password_hash, salt = hasher.hash_password("{new_password}")
print(f"{{password_hash}}|{{salt}}")
'''
            result = subprocess.run(
                ['python3', '-c', hash_script],
                capture_output=True,
                text=True,
                timeout=10
            )

            if result.returncode != 0:
                messagebox.showerror("Грешка", f"Грешка при хеширању лозинке:\n{result.stderr}")
                return

            password_hash, salt = result.stdout.strip().split('|')

            # Update in database
            is_first_login = 'TRUE' if force_change else 'FALSE'
            update_sql = f"""UPDATE users
                SET password_hash = '{password_hash}',
                    salt = '{salt}',
                    is_first_login = {is_first_login},
                    updated_at = NOW()
                WHERE email = '{email}'"""

            result = subprocess.run(
                ['psql', '-U', 'aleksandarlukovic', '-d', 'museum_system', '-c', update_sql],
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
            result = subprocess.run(
                ['psql', '-U', 'aleksandarlukovic', '-d', 'museum_system', '-c',
                 f"UPDATE users SET is_first_login = TRUE, updated_at = NOW() WHERE email = '{email}'"],
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
            result = subprocess.run(
                ['psql', '-U', 'aleksandarlukovic', '-d', 'museum_system', '-c',
                 f"UPDATE users SET is_active = {str(new_status).upper()}, updated_at = NOW() WHERE email = '{email}'"],
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
            # Hash the password using bcrypt via Python
            hash_script = f'''
import sys
sys.path.insert(0, '/home/aleksandarlukovic/MuseumInfoSystem')
from security_utils import PasswordHasher
hasher = PasswordHasher()
password_hash, salt = hasher.hash_password("{new_password}")
print(f"{{password_hash}}|{{salt}}")
'''
            result = subprocess.run(
                ['python3', '-c', hash_script],
                capture_output=True,
                text=True,
                timeout=10
            )

            if result.returncode != 0:
                messagebox.showerror("Грешка", f"Грешка при хеширању лозинке:\n{result.stderr}")
                return

            password_hash, salt = result.stdout.strip().split('|')

            # Update in database with force change on next login
            update_sql = f"""UPDATE users
                SET password_hash = '{password_hash}',
                    salt = '{salt}',
                    is_first_login = TRUE,
                    updated_at = NOW()
                WHERE email = '{email}'"""

            result = subprocess.run(
                ['psql', '-U', 'aleksandarlukovic', '-d', 'museum_system', '-c', update_sql],
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
            # Hash the password using bcrypt via Python
            hash_script = f'''
import sys
sys.path.insert(0, '/home/aleksandarlukovic/MuseumInfoSystem')
from security_utils import PasswordHasher
hasher = PasswordHasher()
password_hash, salt = hasher.hash_password("{temp_password}")
print(f"{{password_hash}}|{{salt}}")
'''
            result = subprocess.run(
                ['python3', '-c', hash_script],
                capture_output=True,
                text=True,
                timeout=10
            )

            if result.returncode != 0:
                messagebox.showerror("Грешка", f"Грешка при хеширању лозинке:\n{result.stderr}")
                return

            password_hash, salt = result.stdout.strip().split('|')

            # Update in database with force change on next login
            update_sql = f"""UPDATE users
                SET password_hash = '{password_hash}',
                    salt = '{salt}',
                    is_first_login = TRUE,
                    updated_at = NOW()
                WHERE email = '{email}'"""

            result = subprocess.run(
                ['psql', '-U', 'aleksandarlukovic', '-d', 'museum_system', '-c', update_sql],
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
