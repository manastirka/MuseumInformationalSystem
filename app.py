#!/usr/bin/env python3
"""
Museum Information System - Main Flask Application
Integrates localSQLtesting (timesheet) and PrirodnjackiMuzej (mineral database) applications
"""

import os
import sys
import json
import logging
from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from werkzeug.serving import run_simple
import importlib.util

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

# For now, use fallback authentication
# The full auth system requires MySQL setup
print("⚠️ Using fallback authentication (MySQL not configured)")
print("   Login with: admin/admin123 or test/user")
auth_available = False

app = Flask(__name__)
app.config.update({
    'SECRET_KEY': os.environ.get('SECRET_KEY', 'museum-info-system-secret-key'),
    'DEBUG': os.environ.get('FLASK_DEBUG', 'True').lower() == 'true',
})

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
        'authorized_users': ['aca.lukovic@nhmbeo.rs', 'admin']
    },
    'mineral_database': {
        'name': 'База минерала',
        'description': 'Колекција минерала - 5.997 примерака',
        'icon': 'bi-gem',
        'default_access': False,  # Restricted access
        'authorized_users': ['aca.lukovic@nhmbeo.rs', 'admin']
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
        'authorized_users': ['admin', 'aca.lukovic@nhmbeo.rs']
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
    }
}

# Dashboard widget preferences (per user)
# Admins can customize which widgets appear on their dashboard
# Dashboard preferences file
DASHBOARD_PREFS_FILE = 'data/dashboard_preferences.json'

# Load dashboard preferences from file
def load_dashboard_preferences():
    """Load dashboard preferences from JSON file."""
    try:
        if os.path.exists(DASHBOARD_PREFS_FILE):
            with open(DASHBOARD_PREFS_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
    except Exception as e:
        print(f"Error loading dashboard preferences: {e}")

    # Return default preferences if file doesn't exist or error occurs
    return {
        'admin': {
            'enabled_widgets': ['timesheet']  # Default: only timesheet widget
        }
    }

def save_dashboard_preferences():
    """Save dashboard preferences to JSON file."""
    try:
        os.makedirs(os.path.dirname(DASHBOARD_PREFS_FILE), exist_ok=True)
        with open(DASHBOARD_PREFS_FILE, 'w', encoding='utf-8') as f:
            json.dump(DASHBOARD_PREFERENCES, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        print(f"Error saving dashboard preferences: {e}")
        return False

DASHBOARD_PREFERENCES = load_dashboard_preferences()

def user_has_module_access(user_email, user_role, module_key):
    """Check if user has access to specific module."""
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
    accessible_modules = []
    
    # Get user's dashboard preferences
    enabled_widgets = DASHBOARD_PREFERENCES.get(user_email, {}).get('enabled_widgets', None)
    
    # If no preferences set, show all accessible modules
    if enabled_widgets is None:
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
MUSEUM_EMPLOYEES = {
    # Administrator
    'admin': {
        'user_id': 1,
        'email': 'admin',
        'full_name': 'System Administrator',
        'department': 'Administration',
        'position': 'System Administrator',
        'role': 'admin',
        'password': 'admin123',
        'description': 'Администратор информационог система музеја. Одговоран за управљање корисницима, техничку подршку и одржавање система.'
    },

    # Museum Director
    'slavko.spasic@nhmbeo.rs': {
        'user_id': 2,
        'email': 'slavko.spasic@nhmbeo.rs',
        'full_name': 'Славко Спасић',
        'department': 'ДИРЕКТОР',
        'position': 'виши кустос',
        'role': 'employee',
        'password': 'user',
        'description': 'Магистар наука (MSc), директор музеја и виши кустос. Води институцију са визијом модернизације и обезбеђења нове зграде музеја. Председник ICOM Србије. Под његовим руковођењем Природњачки музеј бележи значајне пројекте и јубилеје. Његов приступ спаја управљање музејом са музеологијом и позиционира Музеј као прву институцију специјализовану за научно проучавање, заштиту и презентацију националне природне баштине.'
    },

    # General and Legal Affairs Department
    'ana.zivanovic@nhmbeo.rs': {
        'user_id': 3,
        'email': 'ana.zivanovic@nhmbeo.rs',
        'full_name': 'Ана Живановић',
        'department': 'ОДСЕК ОПШТИХ И ПРАВНИХ ПОСЛОВА',
        'position': 'секретар',
        'role': 'employee',
        'password': 'user',
        'description': 'ВСС, секретар музеја. Координира опште и правне послове музеја, осигурава административну подршку раду установе.'
    },
    'ana.kovacevic@nhmbeo.rs': {
        'user_id': 4,
        'email': 'ana.kovacevic@nhmbeo.rs',
        'full_name': 'Ана Ковачевић',
        'department': 'ОДСЕК ОПШТИХ И ПРАВНИХ ПОСЛОВА',
        'position': 'технички секретар',
        'role': 'employee',
        'password': 'user',
        'description': 'ВСС, технички секретар. Пружа логистичку и техничку подршку у канцеларијском пословању музеја. Помаже у организацији догађаја и комуникацији.'
    },
    'bora.m@nhmbeo.rs': {
        'user_id': 5,
        'email': 'bora.m@nhmbeo.rs',
        'full_name': 'Бора Милићевић',
        'department': 'ОДСЕК ОПШТИХ И ПРАВНИХ ПОСЛОВА',
        'position': 'препаратор – ликовни техничар',
        'role': 'employee',
        'password': 'user',
        'description': 'ССС, техничар у музејској делатности. Задужен за техничке послове при поставци изложби и одржавању збирки. Његове фотографије и илустрације коришћене су на изложбама музеја. Специјализован за геологију и изложбене поставке.'
    },
    'pedja@nhmbeo.rs': {
        'user_id': 6,
        'email': 'pedja@nhmbeo.rs',
        'full_name': 'Предраг Илић',
        'department': 'ОДСЕК ОПШТИХ И ПРАВНИХ ПОСЛОВА',
        'position': 'препаратор – техничар графичке припреме',
        'role': 'employee',
        'password': 'user',
        'description': 'ССС, техничар у музејској делатности. Учествује у припреми и транспорту експоната, теренском прикупљању узорака и одржавању опреме за истраживања на терену. Техничка подршка за биологију и логистику.'
    },
    'biblioteka@nhmbeo.rs': {
        'user_id': 7,
        'email': 'biblioteka@nhmbeo.rs',
        'full_name': 'Оливера Аломеровић',
        'department': 'ОДСЕК ОПШТИХ И ПРАВНИХ ПОСЛОВА',
        'position': 'дипл. библиотекар',
        'role': 'employee',
        'password': 'user',
        'description': 'Магистар наука (Msr), дипломирани библиотекар Оливера Аломеровић. Управница библиотеке Природњачког музеја са преко 22.000 књига. Обезбеђује литературу и документацију за истраживаче. Одржава COBISS каталог музеја.'
    },

    # Finance Department
    'dusica.ivic@nhmbeo.rs': {
        'user_id': 8,
        'email': 'dusica.ivic@nhmbeo.rs',
        'full_name': 'Душица Ивић',
        'department': 'ГРУПА ЗА ФИНАНСИЈСКО-РАЧУНОВОДСТВЕНЕ ПОСЛОВЕ',
        'position': 'помоћник директора-руководилац одељења финансија',
        'role': 'employee',
        'password': 'user',
        'description': 'Магистар наука (MSc), помоћник директора-руководилац финансијског одељења. Дугогодишња финансијска стручњакиња, брине о буџету и финансијском пословању музеја. Учествује у стратешком вођењу установе као заменица директора.'
    },
    'milenar@nhmbeo.rs': {
        'user_id': 9,
        'email': 'milenar@nhmbeo.rs',
        'full_name': 'Милена Радочај',
        'department': 'ГРУПА ЗА ФИНАНСИЈСКО-РАЧУНОВОДСТВЕНЕ ПОСЛОВЕ',
        'position': 'финансијско-рачуноводствени референт',
        'role': 'employee',
        'password': 'user',
        'description': 'ВСС, финансијско-рачуноводствени референт. Обавља књиговодствене и финансијске послове. Одговорна за обрачуне и извештаје о финансијском пословању музеја.'
    },
    'milica@nhmbeo.rs': {
        'user_id': 10,
        'email': 'milica@nhmbeo.rs',
        'full_name': 'Милица Томић',
        'department': 'ГРУПА ЗА ФИНАНСИЈСКО-РАЧУНОВОДСТВЕНЕ ПОСЛОВЕ',
        'position': 'финансијско-рачуноводствени сарадник',
        'role': 'employee',
        'password': 'user',
        'description': 'ВСС, финансијско-рачуноводствени сарадник. Помаже у вођењу финансијске евиденције, припрема финансијске документе и учествује у спровођењу финансијских планова музеја.'
    },

    # Education and Marketing Department
    'draganav@nhmbeo.rs': {
        'user_id': 11,
        'email': 'draganav@nhmbeo.rs',
        'full_name': 'Драгана Вучићевић',
        'department': 'ГРУПА ЗА ЕДУКАЦИЈУ, КОМУНИКАЦИЈУ И МАРКЕТИНГ',
        'position': 'виши кустос',
        'role': 'employee',
        'password': 'user',
        'description': 'Дипломирани инжењер, виши кустос, руководилац едукације и маркетинга. Организаторка едукативних програма и промотивних активности музеја. Аутор и коаутор више изложби и публикација за популаризацију науке. Координира односе са јавношћу музеја.'
    },
    'simka.vukojevic@nhmbeo.rs': {
        'user_id': 12,
        'email': 'simka.vukojevic@nhmbeo.rs',
        'full_name': 'Симка Вукојевић',
        'department': 'ГРУПА ЗА ЕДУКАЦИЈУ, КОМУНИКАЦИЈУ И МАРКЕТИНГ',
        'position': 'музејски педагог',
        'role': 'employee',
        'password': 'user',
        'description': 'Магистар наука (Msr), музејски педагог. Осмишљава и реализује педагошке програме за школе и породице. Креира радионице, води интерактивна вођења и прилагођава научни садржај различитим узрастима посетилаца.'
    },

    # Gallery Department
    'milica.rakic@nhmbeo.rs': {
        'user_id': 13,
        'email': 'milica.rakic@nhmbeo.rs',
        'full_name': 'Милица Ракић',
        'department': 'ГРУПА ЗА ИЗЛОЖБЕНЕ ПОСЛОВЕ – ГАЛЕРИЈА',
        'position': 'организаторка туристичке и услужне делатности',
        'role': 'employee',
        'password': 'user',
        'description': 'ВСС, организаторка туристичке и услужне делатности (Галерија). Организује посете и догађаје у Галерији Природњачког музеја на Калемегдану. Координира туристичке програме и сарадњу са посетиоцима, чинећи изложбе доступним широкој публици.'
    },

    # Biology Department (key members)
    'mniketic@nhmbeo.rs': {
        'user_id': 14,
        'email': 'mniketic@nhmbeo.rs',
        'full_name': 'Марјан Никетић',
        'department': 'БИОЛОШКО ОДЕЉЕЊЕ',
        'position': 'руководилац Биолошког одељења, музејски саветник ботаничар',
        'role': 'employee',
        'password': 'user',
        'description': 'Доктор наука, дописни члан Српске академије наука и уметности (SANU) изабран 4. новембра 2021. године. Истакнути српски ботаничар са 147 објављених научних радова. Описао је (самостално или са сарадницима) 8 нових биљних врста за науку и открио преко 160 биљних врста нових за флору Србије. Уредник је часописа Bulletin PM и прикупио >40.000 примерака за хербаријум музеја, што чини окоснicu проучавања балканске флоре.'
    },
    'dubravka.vucic@nhmbeo.rs': {
        'user_id': 15,
        'email': 'dubravka.vucic@nhmbeo.rs',
        'full_name': 'Дубравка Вучић',
        'department': 'БИОЛОШКО ОДЕЉЕЊЕ',
        'position': 'музејски саветник ихтиолог',
        'role': 'employee',
        'password': 'user',
        'description': 'ВСС, музејски саветник ихтиолог (виши кустос). Истакнута кустоскиња ихтиолошких збирки. Ауторка изложбе "Кавијар" о историји и биологији јесетри и кавијара. Стручни саветник у пројектима о ајкулама – њено знање било је кључно за изложбу "Ајкуле" 2025.'
    },
    'milos.jovic@nhmbeo.rs': {
        'user_id': 16,
        'email': 'milos.jovic@nhmbeo.rs',
        'full_name': 'Милош Јовић',
        'department': 'БИОЛОШКО ОДЕЉЕЊЕ',
        'position': 'музејски саветник ентомолог',
        'role': 'employee',
        'password': 'user',
        'description': 'Магистар наука (MSc), музејски саветник ентомолог. Куратор ентомолошких збирки, посебно Odonata. Национални координатор пројекта Balkan OdoBase (регионалне базе података о вилинским коњицима). Објавио радове о диверзитету и народним називима инсеката. Аутор изложби за популаризацију инсеката (аутор трибине о свету инсеката за децу).'
    },

    # Geology Department (key members)
    'biljana.mitrovic@nhmbeo.rs': {
        'user_id': 17,
        'email': 'biljana.mitrovic@nhmbeo.rs',
        'full_name': 'Биљана Митровић',
        'department': 'ГЕОЛОШКО ОДЕЉЕЊЕ',
        'position': 'начелник Геолошког одељења, музејски саветник палеозоолог',
        'role': 'employee',
        'password': 'user',
        'description': 'Доктор наука, начелник Геолошког одељења, музејски саветник палеозоолог. Водећи стручњак за фосилне пужеве и шкољке раног терцијара Србије. Објавила радове о миоценским копненим пуж евима и описала нове врсте фосилних пужева из Србије. Коаутор више изложби (нпр. "Fosili kao odrazi prošlosti") представљајући публикуму геолошку баштину. Експерт за палеонтологију безкичмењака.'
    },
    'zoran.markovic@nhmbeo.rs': {
        'user_id': 18,
        'email': 'zoran.markovic@nhmbeo.rs',
        'full_name': 'Зоран Марковић',
        'department': 'ГЕОЛОШКО ОДЕЉЕЊЕ',
        'position': 'музејски саветник палеозоолог',
        'role': 'employee',
        'password': 'user',
        'description': 'Доктор наука, музејски саветник палеозоолог. Угледни палеонтолог који је предводио откриће првих фосила диносауруса у Србији (сауропод и теропод, Креда). Објавио рад о тим фосилима у међународном часопису. Специјалиста за фосиле великих сисара и диносауруса касне креде, аутор бројних научних студија. Коаутор изложби "Surlaši – divovi prošlosti" о праисторијским слоновима.'
    },
    'aca.lukovic@nhmbeo.rs': {
        'user_id': 19,
        'email': 'aca.lukovic@nhmbeo.rs',
        'full_name': 'Александар Луковић',
        'department': 'ГЕОЛОШКО ОДЕЉЕЊЕ',
        'position': 'кустос минералог',
        'role': 'employee',
        'password': 'user',
        'description': 'Доктор наука, кустос минералог. Доктор минералогије и кристалограф, кустос минералошке збирке. Коаутор изложби о рударству и минералима, нпр. "Minerali Trepče" (посвећена чувеном руднику) и "Mineralno blago Jugoslavije" (Музеј Југославије) – аутор пратећег каталога. Такође познат као гитариста рок групе S.A.R.S., чиме спаја науку и уметност. Објавио научне радове о минералним текстурама и налазиштима.'
    },
    
    # Additional General and Legal Affairs employees
    'danijela.mijailovic@nhmbeo.rs': {
        'user_id': 20,
        'email': 'danijela.mijailovic@nhmbeo.rs',
        'full_name': 'Данијела Мијаиловић',
        'department': 'ОДСЕК ОПШТИХ И ПРАВНИХ ПОСЛОВА',
        'position': 'радник за одржавање хигијене',
        'role': 'employee',
        'password': 'user',
        'description': 'Радник на одржавању хигијене. Брине о хигијени и чистоћи у радним просторијама и изложбеном простору музеја. Доприноси безбедности експоната кроз уредно одржавање простора.'
    },
    'nevenka.jankovic@nhmbeo.rs': {
        'user_id': 21,
        'email': 'nevenka.jankovic@nhmbeo.rs',
        'full_name': 'Невенка Јанковић',
        'department': 'ОДСЕК ОПШТИХ И ПРАВНИХ ПОСЛОВА',
        'position': 'радник за одржавање хигијене',
        'role': 'employee',
        'password': 'user',
        'description': 'Радник на одржавању хигијене. Задужена за свакодневно чишћење и одржавање музејске зграде и галерије, чиме обезбеђује пријатан и безбедан амбијент за посетиоце и запослене.'
    },
    
    # Additional Gallery Department employees
    'snezana.jovanovic@nhmbeo.rs': {
        'user_id': 22,
        'email': 'snezana.jovanovic@nhmbeo.rs',
        'full_name': 'Снежана Јовановић',
        'department': 'ГРУПА ЗА ИЗЛОЖБЕНЕ ПОСЛОВЕ – ГАЛЕРИЈА',
        'position': 'водич',
        'role': 'employee',
        'password': 'user',
        'description': 'ССС, водич у музеју. Музејска водичкиња са дугогодишњим искуством. Одржава стручно вођење кроз изложбе, пружа посетиоцима објашњења и приче о експонатима на популаран начин.'
    },
    
    # Additional Biology Department employees
    'boris@nhmbeo.rs': {
        'user_id': 23,
        'email': 'boris@nhmbeo.rs',
        'full_name': 'Борис Иванчевић',
        'department': 'БИОЛОШКО ОДЕЉЕЊЕ',
        'position': 'музејски саветник миколог',
        'role': 'employee',
        'password': 'user',
        'description': 'Доктор наука микологије са преко 30 година истраживања гљива. Објавио је велики број научних радова о диверзитету и заштити макромицета Балкана. Приредио Preliminarni spisak makromiceta od međunarodnog značaja (1995) ради очувања ретких врста.'
    },
    'ana.paunovic@nhmbeo.rs': {
        'user_id': 24,
        'email': 'ana.paunovic@nhmbeo.rs',
        'full_name': 'Ана Пауновић',
        'department': 'БИОЛОШКО ОДЕЉЕЊЕ',
        'position': 'музејски саветник херпетолог',
        'role': 'employee',
        'password': 'user',
        'description': 'Доктор наука, музејски саветник херпетолог. Биолошкиња са 20+ година рада у музеју и теренског истраживања водоземаца и гмизаваца широм Србије. Ауторка или коауторка бројних научних радова, музејских изложби и уџбеника из биологије. Посебно посвећена едукацији јавности и заштити водених екосистема (ронилац и природњак ентузијаста).'
    },
    'aleksandar@nhmbeo.rs': {
        'user_id': 25,
        'email': 'aleksandar@nhmbeo.rs',
        'full_name': 'Александар Стојановић',
        'department': 'БИОЛОШКО ОДЕЉЕЊЕ',
        'position': 'конзерватор ентомолог',
        'role': 'employee',
        'password': 'user',
        'description': 'Дипломирани инжењер, конзерватор ентомолог. Задужен за препарацију и очување инсеката у збиркама музеја. Коаутор изложбе "Кроз свет инсеката Србије" (2015) са 1.710 приказаних врста инсеката и аутор каталога те изложбе. Унапређује технике конзервације и презентације инсектног материјала.'
    },
    'aleksandra.savic@nhmbeo.rs': {
        'user_id': 26,
        'email': 'aleksandra.savic@nhmbeo.rs',
        'full_name': 'Александра Савић',
        'department': 'БИОЛОШКО ОДЕЉЕЊЕ',
        'position': 'музејски саветник ботаничар / етноботаничар',
        'role': 'employee',
        'password': 'user',
        'description': 'Доктор наука, музејски саветник ботаничар/етноботаничар. Биолошкиња која је основала Збирку воћа у музеју, проучавајући старе аутохтоне сорте воћа Балкана. Ауторка путујуће изложбе "Старо и нестало воће Србије" (50 гостовања, 60.000 посетилаца) и истоимене монографије. Коауторка изложбе "Хиландарски медицински кодекс" (2023) о средњовековној медицини. Добитница више струковних признања за популаризацију и заштиту агробиодиверзитета Србије.'
    },
    'verica.stojanovic@nhmbeo.rs': {
        'user_id': 27,
        'email': 'verica.stojanovic@nhmbeo.rs',
        'full_name': 'Верица Стојановић',
        'department': 'БИОЛОШКО ОДЕЉЕЊЕ',
        'position': 'кустос приправник',
        'role': 'employee',
        'password': 'user',
        'description': 'Магистар наука (Mr/Mag.), руководилац Биолошког одељења, кустос ботаничар. Специјалиста за флору Србије, посебно заштићене и инвазивне биљке. Водила истраживања о угроженим врстама (нпр. нестанку крагујевачког слеза услед уништења станишта). Учествује у едукацији јавности о биљном биодиверзитету.'
    },
    'gorana.petkovski@nhmbeo.rs': {
        'user_id': 28,
        'email': 'gorana.petkovski@nhmbeo.rs',
        'full_name': 'Горана Петковски',
        'department': 'БИОЛОШКО ОДЕЉЕЊЕ',
        'position': 'конзерватор',
        'role': 'employee',
        'password': 'user',
        'description': 'ВСС, конзерватор (биолошке збирке). Бави се препарирањем и чувањем биолошких препарата (хербаријумских примерака, животињских дермопрепарата). Њен рад иза сцене омогућава дугорочно очување музејских примерака и њихову спремност за излагање и истраживање.'
    },
    'marko.nestorovic@nhmbeo.rs': {
        'user_id': 29,
        'email': 'marko.nestorovic@nhmbeo.rs',
        'full_name': 'Марко Несторовић',
        'department': 'БИОЛОШКО ОДЕЉЕЊЕ',
        'position': 'музејски саветник ботаничар / херболог',
        'role': 'employee',
        'password': 'user',
        'description': 'Доктор наука, музејски саветник ботаничар/херболог. Ботаничар специјализован за коровску флору и алергене биљке урбаних средина. Коаутор приручника "Alergene biljke" (2011). Објавио радове о диверзитету корова и учествовао у истраживањима инвазивних биљака. Активно ради на едукацији о алергеним врстама и њиховом утицају на здравље људи.'
    },
    'zorana.markovic@nhmbeo.rs': {
        'user_id': 30,
        'email': 'zorana.markovic@nhmbeo.rs',
        'full_name': 'Зорана Марковић',
        'department': 'БИОЛОШКО ОДЕЉЕЊЕ',
        'position': 'кустос',
        'role': 'employee',
        'password': 'user',
        'description': 'Магистар наука (MSc), кустос истраживач (биолог). Млади кустос-истраживач (придружила се 2021). Учествује у пројектима ДНК баркодирања животиња – проучава генетичку разноликост вилинских коњица и других организама на молекуларном нивоу. Сарађује са другим научним институцијама и помаже у унапређењу молекуларне лабораторије музеја.'
    },
    'vuk.popic@nhmbeo.rs': {
        'user_id': 31,
        'email': 'vuk.popic@nhmbeo.rs',
        'full_name': 'Вук Попић',
        'department': 'БИОЛОШКО ОДЕЉЕЊЕ',
        'position': 'кустос приправник',
        'role': 'employee',
        'password': 'user',
        'description': 'Магистар наука (Msr), кустос орнитолог. Орнитолог ангажован на праћењу и проучавању птица Србије. Учествује у националном програму прстеновања птица (Euring) ради истраживања сеоба и популација. Бави се заштитом угрожених врста птица и популаризацијом орнитологије кроз јавна предавања и медије.'
    },
    'milos.mrvaljevic@nhmbeo.rs': {
        'user_id': 32,
        'email': 'milos.mrvaljevic@nhmbeo.rs',
        'full_name': 'Милош Мрваљевић',
        'department': 'БИОЛОШКО ОДЕЉЕЊЕ',
        'position': 'препаратор приправник',
        'role': 'employee',
        'password': 'user',
        'description': 'БСц, препараторски приправник (биологија). Асистент препаратора који се обучава у таксидермији и конзервацији. Учествовао на терену у прикупљању материјала и припреми нових експоната. Стиче искуство кроз рад на препарирању ситних животиња за изложбе и едукативне програме музеја.'
    },
    'jovan.kokotovic@nhmbeo.rs': {
        'user_id': 33,
        'email': 'jovan.kokotovic@nhmbeo.rs',
        'full_name': 'Јован Кокотовић',
        'department': 'БИОЛОШКО ОДЕЉЕЊЕ',
        'position': 'кустос приправник',
        'role': 'employee',
        'password': 'user',
        'description': 'Магистар наука (MSc), кустос приправник (биологија). Млади биолог на кустоској пракси. Ангажован на прикупљању и обради података о биодиверзитету за музејске збирке. Учи кустоске вештине кроз рад на мањим пројектима, теренским истраживањима и асистирање старијим кустосима у организацији збирки.'
    },
    
    # Additional Geology Department employees
    'sanja.pavic@nhmbeo.rs': {
        'user_id': 34,
        'email': 'sanja.pavic@nhmbeo.rs',
        'full_name': 'Сања Алабурић',
        'department': 'ГЕОЛОШКО ОДЕЉЕЊЕ',
        'position': 'музејски саветник палеозоолог',
        'role': 'employee',
        'password': 'user',
        'description': 'Магистар наука (Msr), музејски саветник палеозоолог. Бави се фосилним кичмењацима из терцијара и квартара. Коауторка изложби "Surlaši – divovi iz naše geološke prošlosti" (праисторијски слонови) и "Ledeno doba" које приближавају палеонтологију публици. Сарадник на научним истраживањима фосилних крупних сисара (нпр. Deinotherium – праисторијски слонови). Специјалиста за палеонтологију сисара кенозоика.'
    },
    'amaran@nhmbeo.rs': {
        'user_id': 35,
        'email': 'amaran@nhmbeo.rs',
        'full_name': 'Александра Маран Стевановић',
        'department': 'ГЕОЛОШКО ОДЕЉЕЊЕ',
        'position': 'музејски саветник палеозоолог',
        'role': 'employee',
        'password': 'user',
        'description': 'Доктор геолошких наука, музејски саветник палеозоолог. Експерт за еволуцију кичмењака. Објављује радове у међународним научним часописима.'
    },
    'desadjm@nhmbeo.rs': {
        'user_id': 36,
        'email': 'desadjm@nhmbeo.rs',
        'full_name': 'Деса Ђорђевић-Милутиновић',
        'department': 'ГЕОЛОШКО ОДЕЉЕЊЕ',
        'position': 'музејски саветник, палеоботаничар',
        'role': 'employee',
        'password': 'user',
        'description': 'Доктор наука, музејски саветник палеоботаничар. Кустос Палеоботаничке збирке (од 1993) и професор палеоекологије на Биолошком факултету. Реконструише праисторијске екосистеме на основу фосилних биљака. Објавила радове о флори неогена и члан је међународних палеоботаничких организација. Учествовала у више изложби (нпр. о пиониру палеонтологије Николи Пантићу). Популарише науку кроз интервјуе истичући да је "палеоботаника увид у свет пре нас".'
    },
    'dragana.djuric@nhmbeo.rs': {
        'user_id': 37,
        'email': 'dragana.djuric@nhmbeo.rs',
        'full_name': 'Драгана Ђурић',
        'department': 'ГЕОЛОШКО ОДЕЉЕЊЕ',
        'position': 'музејски саветник палеозоолог',
        'role': 'employee',
        'password': 'user',
        'description': 'Доктор наука, музејски саветник палеозоолог. Доктор наука о еволуцији кичмењака. Проучава фосилне вертебрате и еволутивне промене. Саговорница РТС-а за тему еволуције кичмењака. Коауторка изложбе "Ledeno doba" (2012) о мегафауни плеистоцена. Учествује у интердисциплинарним пројектима (нпр. геоархеолошка истраживања) и популарише палеонтологију кроз медије и предавања.'
    },
    'tatjana.milicbabic@nhmbeo.rs': {
        'user_id': 38,
        'email': 'tatjana.milicbabic@nhmbeo.rs',
        'full_name': 'Татјана Милић Бабић',
        'department': 'ГЕОЛОШКО ОДЕЉЕЊЕ',
        'position': 'виши кустос петролог',
        'role': 'employee',
        'password': 'user',
        'description': 'Дипломирани геолог, виши кустос петролог. Геолог-петролог са богатим теренским искуством. Кураторка петролошке збирке и ауторка низа изложби о стенама и минералима: "I bi svetlost" (изложба минерала, 2010), "Mozaik prirode" (2012) и др. Стручњак за метеорите – објашњавала је класификацију српских метеорита (нпр. Сокобањски метеорит, хондрит) широј публици.'
    },
    'pejovic.ranko@nhmbeo.rs': {
        'user_id': 39,
        'email': 'pejovic.ranko@nhmbeo.rs',
        'full_name': 'Ранко Пејовић',
        'department': 'ГЕОЛОШКО ОДЕЉЕЊЕ',
        'position': 'кустос палеозоолог',
        'role': 'employee',
        'password': 'user',
        'description': 'Дипломирани инжењер геологије (Dipl. inž.), кустос палеозоолог. Искусни кустос палеонтолог који деценијама истражује фосилни свет. Аутор изложбе "Fosilizacija" (2025) о процесима очувања живота кроз геолошку прошлост. Његова стручност и посвећеност истраживању древног живота резултирали су богатом збирком фосила и мултидисциплинарним поставкама. Публиковао радове о палеозојским и мезозојским фосилима (нпр. фосилним мекушцима).'
    },
    'milos.milivojevic@nhmbeo.rs': {
        'user_id': 40,
        'email': 'milos.milivojevic@nhmbeo.rs',
        'full_name': 'Милош Миливојевић',
        'department': 'ГЕОЛОШКО ОДЕЉЕЊЕ',
        'position': 'виши препаратор за геолошке збирке',
        'role': 'employee',
        'password': 'user',
        'description': 'ССС, виши препаратор за геолошке збирке. Главни препаратор палеонтолошких узорака – специјалиста за чишћење, конзервацију и монтажу фосилних скелета. Био је део научног тима који је открио прве остатке диносауруса у Србији, лично учествујући у ископавању и припреми фосилних зуба теропода и кости сауропода. Његова експертиза у препарирању фосила кључна је за истраживања и изложбе (нпр. припрема мамутових кљова за изложбе о леденом добу).'
    },
    'branko.radulovic@nhmbeo.rs': {
        'user_id': 41,
        'email': 'branko.radulovic@nhmbeo.rs',
        'full_name': 'Бранко Радуловић',
        'department': 'ГЕОЛОШКО ОДЕЉЕЊЕ',
        'position': 'кустос за геолошке збирке',
        'role': 'employee',
        'password': 'user',
        'description': 'Магистар наука (Msr), кустос за геолошке збирке. Кустос геолошких збирки задужен за богату колекцију фосила и минерала. Коаутор изложбе "Fosili kao odrazi prošlosti" (2024) која приказује палеонтолошко благо – од еоценских пужева до мамутових кљова. Учествује у теренским истраживањима (прикупљање фосила широм Балкана) и доприноси стручној обради геолошких колекција.'
    },
    'nenad.mladenovic@nhmbeo.rs': {
        'user_id': 42,
        'email': 'nenad.mladenovic@nhmbeo.rs',
        'full_name': 'Ненад Младеновић',
        'department': 'ГЕОЛОШКО ОДЕЉЕЊЕ',
        'position': 'конзерватор приправник',
        'role': 'employee',
        'password': 'user',
        'description': 'Магистар наука (Msr), конзерватор у геолошком одељењу. Конзерватор специјализован за геолошке узорке – фосиле и минерале. Брине о заштити и чувању фосилних примерака (чишћење, стабилизација, складиштење). Пружао техничку подршку изложбама (нпр. у постав ци "Fosilizacija" био део тима за сценографију и инсталацију експоната). Његов рад осигурава дуговечност геолошких артефаката у збирци.'
    }
}

# Library Database
LIBRARY_DATABASE = {
    'books': [
        {
            'id': 1,
            'title': 'Геологија Србије',
            'author': 'Проф. Др Милош Петровић',
            'isbn': '978-86-123-4567-8',
            'category': 'Геологија',
            'year': 2020,
            'location': 'Полица А1-15',
            'status': 'доступна',
            'description': 'Свеобухватан приказ геолошке грађе територије Србије',
            'pages': 450,
            'publisher': 'Геолошки завод Србије',
            'language': 'српски'
        },
        {
            'id': 2,
            'title': 'Минералогија',
            'author': 'Др Ана Стојановић',
            'isbn': '978-86-987-6543-2',
            'category': 'Минералогија',
            'year': 2019,
            'location': 'Полица Б2-08',
            'status': 'позајмљена',
            'description': 'Основе минералогије са посебним освртом на минерале Балкана',
            'pages': 320,
            'publisher': 'Рудничко-геолошки факултет',
            'language': 'српски'
        },
        {
            'id': 3,
            'title': 'Палеонтологија кичмењака',
            'author': 'Проф. Др Зоран Марковић',
            'isbn': '978-86-555-7890-1',
            'category': 'Палеонтологија',
            'year': 2021,
            'location': 'Полица Ц1-22',
            'status': 'доступна',
            'description': 'Еволуција и развој кичмењака кроз геолошке епохе',
            'pages': 280,
            'publisher': 'Биолошки факултет',
            'language': 'српски'
        },
        {
            'id': 4,
            'title': 'Флора Србије',
            'author': 'Проф. Др Марјан Никетић',
            'isbn': '978-86-321-4560-9',
            'category': 'Ботаника',
            'year': 2018,
            'location': 'Полица Д3-12',
            'status': 'доступна',
            'description': 'Систематски приказ биљних врста на територији Србије',
            'pages': 680,
            'publisher': 'Природно-математички факултет',
            'language': 'српски'
        },
        {
            'id': 5,
            'title': 'Entomology of the Balkans',
            'author': 'Dr. Miloš Jović',
            'isbn': '978-3-16-148410-0',
            'category': 'Ентомологија',
            'year': 2022,
            'location': 'Полица Е1-05',
            'status': 'доступна',
            'description': 'Comprehensive guide to insect species of the Balkan Peninsula',
            'pages': 540,
            'publisher': 'Academic Press',
            'language': 'енглески'
        }
    ],
    'categories': ['Геологија', 'Минералогија', 'Палеонтологија', 'Ботаника', 'Зоологија', 'Ентомологија', 'Ихтиологија', 'Општа научна литература'],
    'statistics': {
        'total_books': 5,
        'available_books': 4,
        'borrowed_books': 1,
        'total_categories': 6
    }
}

# Curator Collection Databases - Sample Data

# Botany Collection Database
BOTANY_COLLECTION_DATABASE = {
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

# Ichthyology Collection Database  
ICHTHYOLOGY_COLLECTION_DATABASE = {
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

# Entomology Collection Database
ENTOMOLOGY_COLLECTION_DATABASE = {
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

# Mycology Collection Database
MYCOLOGY_COLLECTION_DATABASE = {
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

# Herpetology Collection Database
HERPETOLOGY_COLLECTION_DATABASE = {
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

# Ornithology Collection Database
ORNITHOLOGY_COLLECTION_DATABASE = {
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

# Paleozoology Collection Database
PALEOZOOLOGY_COLLECTION_DATABASE = {
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

# Paleobotany Collection Database
PALEOBOTANY_COLLECTION_DATABASE = {
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

# Petrology Collection Database
PETROLOGY_COLLECTION_DATABASE = {
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

# Vehicle data files
VEHICLES_FILE = 'data/museum_vehicles.json'
RESERVATIONS_FILE = 'data/vehicle_reservations.json'

def load_vehicles():
    """Load vehicles from JSON file."""
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
    """Save vehicles to JSON file."""
    try:
        os.makedirs(os.path.dirname(VEHICLES_FILE), exist_ok=True)
        with open(VEHICLES_FILE, 'w', encoding='utf-8') as f:
            json.dump(MUSEUM_VEHICLES, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        print(f"Error saving vehicles: {e}")
        return False

def load_reservations():
    """Load reservations from JSON file."""
    try:
        if os.path.exists(RESERVATIONS_FILE):
            with open(RESERVATIONS_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
    except Exception as e:
        print(f"Error loading reservations: {e}")
    return []

def save_reservations():
    """Save reservations to JSON file."""
    try:
        os.makedirs(os.path.dirname(RESERVATIONS_FILE), exist_ok=True)
        with open(RESERVATIONS_FILE, 'w', encoding='utf-8') as f:
            json.dump(VEHICLE_RESERVATIONS, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        print(f"Error saving reservations: {e}")
        return False

# Museum Vehicles Database
MUSEUM_VEHICLES = load_vehicles()

# Vehicle Reservations Database
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

def authenticate_fallback_user(email, password):
    """Authenticate user using fallback employee database."""
    if email in MUSEUM_EMPLOYEES:
        user = MUSEUM_EMPLOYEES[email]
        if user['password'] == password:
            return user
    return None

# Authentication decorator
def login_required(f):
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Морате се пријавити да приступите овој страници.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Морате се пријавити да приступите овој страници.', 'warning')
            return redirect(url_for('login'))
        if session.get('user_role') != 'admin':
            flash('Немате дозволу за приступ овој страници.', 'error')
            return redirect(url_for('dashboard'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def index():
    """Main landing page."""
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login."""
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '').strip()

        if not auth_available:
            # Fallback authentication with real museum employees
            user_info = authenticate_fallback_user(email, password)
            if user_info:
                session['user_id'] = user_info['user_id']
                session['user_email'] = user_info['email']
                session['user_name'] = user_info['full_name']
                session['user_role'] = user_info['role']
                session['user_department'] = user_info['department']
                flash(f'Добродошли, {user_info["full_name"]}! (Fallback режим)', 'success')
                return redirect(url_for('dashboard'))
            else:
                flash('Погрешан емејл или лозинка! Користите музејску емејл адресу и лозинку "user".', 'error')
                return render_template('login.html')

        # Authenticate user with main system
        user_info = auth_system.authenticate_user(email, password)

        if user_info:
            # Store user info in session
            session['user_id'] = user_info['user_id']
            session['user_email'] = user_info['email']
            session['user_name'] = user_info['full_name']
            session['user_role'] = user_info['role']
            session['user_department'] = user_info.get('department', '')

            flash(f'Добrodошли, {user_info["full_name"]}!', 'success')

            # Handle first login password change
            if user_info.get('is_first_login'):
                return redirect(url_for('change_password'))

            return redirect(url_for('dashboard'))
        else:
            flash('Погрешан емејл или лозинка!', 'error')

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
    """Change user password."""
    if request.method == 'POST':
        current_password = request.form.get('current_password', '')
        new_password = request.form.get('new_password', '')
        confirm_password = request.form.get('confirm_password', '')

        if not all([current_password, new_password, confirm_password]):
            flash('Сва поља су обавезна!', 'error')
            return render_template('change_password.html')

        if new_password != confirm_password:
            flash('Нове лозинке се не слажу!', 'error')
            return render_template('change_password.html')

        if len(new_password) < 6:
            flash('Лозинка мора имати најмање 6 карактера!', 'error')
            return render_template('change_password.html')

        if not auth_available:
            flash('Промена лозинке није доступна у fallback режиму.', 'warning')
            return redirect(url_for('dashboard'))

        if auth_system.change_password(session['user_id'], current_password, new_password):
            flash('Лозинка је успешно промењена!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Грешка при промени лозинке. Проверите тренутну лозинку.', 'error')

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

    return render_template('timesheet_integration.html')

@app.route('/mineral_database')
@login_required
def mineral_database_app():
    """Route to mineral database integration."""
    user_email = session.get('user_email')
    user_role = session.get('user_role')

    if not user_has_module_access(user_email, user_role, 'mineral_database'):
        flash('Немате дозволу за приступ бази минерала.', 'error')
        return redirect(url_for('dashboard'))

    return render_template('mineral_integration.html')

@app.route('/admin')
@admin_required
def admin_panel():
    """Admin panel."""
    return render_template('admin_panel.html')

@app.route('/admin/manage_access')
@admin_required
def manage_user_access():
    """Manage user module access."""
    # Get all users and their current access
    users_with_access = []

    for email, user_data in MUSEUM_EMPLOYEES.items():
        if user_data['role'] != 'admin':  # Don't show admin users
            user_modules = get_user_modules(email, user_data['role'])
            users_with_access.append({
                'email': email,
                'name': user_data['full_name'],
                'department': user_data['department'],
                'modules': user_modules
            })

    return render_template('admin_manage_access.html',
                          users=users_with_access,
                          all_modules=MODULE_ACCESS)

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

    # Add user to authorized list for this module
    if user_email not in MODULE_ACCESS[module_key].get('authorized_users', []):
        if 'authorized_users' not in MODULE_ACCESS[module_key]:
            MODULE_ACCESS[module_key]['authorized_users'] = []
        MODULE_ACCESS[module_key]['authorized_users'].append(user_email)

        module_name = MODULE_ACCESS[module_key]['name']
        flash(f'Приступ модулу "{module_name}" је дат кориснику {user_email}.', 'success')
    else:
        flash('Корисник већ има приступ овом модулу.', 'warning')

    return redirect(url_for('manage_user_access'))

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

    # Remove user from authorized list
    authorized_users = MODULE_ACCESS[module_key].get('authorized_users', [])
    if user_email in authorized_users:
        authorized_users.remove(user_email)
        module_name = MODULE_ACCESS[module_key]['name']
        flash(f'Приступ модулу "{module_name}" је укинут кориснику {user_email}.', 'success')
    else:
        flash('Корисник није имао приступ овом модулу.', 'warning')

    return redirect(url_for('manage_user_access'))

@app.route('/admin/employees_database')
@admin_required
def employees_database():
    """View all employee databases and information."""
    # Convert dictionary to list of employee objects for easier template processing
    employees_list = []
    for email, emp_data in MUSEUM_EMPLOYEES.items():
        employee = emp_data.copy()
        employee['email'] = email
        employees_list.append(employee)

    return render_template('admin_employees_database.html',
                          employees=employees_list,
                          total_employees=len(employees_list))

@app.route('/admin/employee_profiles_database')
@admin_required
def employee_profiles_database():
    """Employee profiles database with detailed biographical information."""
    # Convert dictionary to list with full profile information
    employees_list = []
    for email, emp_data in MUSEUM_EMPLOYEES.items():
        employee = emp_data.copy()
        employee['email'] = email
        # Only include employees with descriptions
        if 'description' in employee and employee['description']:
            employees_list.append(employee)
    
    # Calculate statistics
    total_profiles = len(employees_list)
    with_descriptions = len([e for e in employees_list if e.get('description')])
    departments = len(set([e['department'] for e in employees_list if e.get('department')]))
    
    statistics = {
        'total_profiles': total_profiles,
        'with_descriptions': with_descriptions,
        'total_departments': departments,
        'completion_rate': round((with_descriptions / len(MUSEUM_EMPLOYEES) * 100), 1) if len(MUSEUM_EMPLOYEES) > 0 else 0
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

        flash(f'Корисник {full_name} је успешно додат у систем.', 'success')
        return redirect(url_for('employees_database'))

    # GET request - show form
    departments = list(set([emp['department'] for emp in MUSEUM_EMPLOYEES.values()]))
    return render_template('admin_add_user.html', departments=departments)

@app.route('/admin/manage_access', methods=['GET'])
@admin_required
def manage_access():
    """Manage user access to different modules."""
    employees_list = []
    for email, emp_data in MUSEUM_EMPLOYEES.items():
        employee = emp_data.copy()
        employee['email'] = email
        # Add current access information
        employee['modules'] = get_user_modules(email, emp_data['role'])
        employees_list.append(employee)

    return render_template('admin_manage_access.html',
                          employees=employees_list,
                          modules=MODULE_ACCESS)

@app.route('/dashboard/customize', methods=['GET', 'POST'])
@login_required
def customize_dashboard():
    """Customize dashboard widget preferences."""
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
    # Calculate system statistics
    total_employees = len(MUSEUM_EMPLOYEES)
    total_books = len(LIBRARY_DATABASE['books'])
    total_artifacts = len(EXHIBITS_DATABASE['artifacts'])

    # Employee statistics
    admin_count = len([emp for emp in MUSEUM_EMPLOYEES.values() if emp['role'] == 'admin'])
    employee_count = total_employees - admin_count

    # Department breakdown
    dept_stats = {}
    for emp in MUSEUM_EMPLOYEES.values():
        dept = emp['department']
        dept_stats[dept] = dept_stats.get(dept, 0) + 1

    # Library statistics
    library_stats = LIBRARY_DATABASE['statistics'].copy()
    available_books = len([b for b in LIBRARY_DATABASE['books'] if b['status'] == 'доступна'])
    borrowed_books = len([b for b in LIBRARY_DATABASE['books'] if b['status'] == 'позајмљена'])

    # Exhibits statistics
    exhibit_stats = EXHIBITS_DATABASE['statistics'].copy()
    displayed_artifacts = len([a for a in EXHIBITS_DATABASE['artifacts'] if a['status'] == 'изложен'])
    storage_artifacts = len([a for a in EXHIBITS_DATABASE['artifacts'] if a['status'] == 'у депоу'])

    # Module access statistics
    timesheet_users = len([email for email in MUSEUM_EMPLOYEES.keys()
                          if user_has_module_access(email, MUSEUM_EMPLOYEES[email]['role'], 'timesheet')])

    database_users = len([email for email in MUSEUM_EMPLOYEES.keys()
                         if user_has_module_access(email, MUSEUM_EMPLOYEES[email]['role'], 'museum_databases')])

    report_data = {
        'system_overview': {
            'total_employees': total_employees,
            'total_books': total_books,
            'total_artifacts': total_artifacts,
            'active_databases': 4,  # Employees, Minerals, Library, Exhibits
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

@app.route('/admin/library_database')
@admin_required
def library_database():
    """Library database management system."""
    books = LIBRARY_DATABASE['books']
    categories = LIBRARY_DATABASE['categories']
    statistics = LIBRARY_DATABASE['statistics']

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
@admin_required
def cultural_heritage_database():
    """Cultural heritage database management system (Заштићена културна добра)."""
    heritage_items = CULTURAL_HERITAGE_DATABASE['heritage_items']
    heritage_types = CULTURAL_HERITAGE_DATABASE['heritage_types']
    categories = CULTURAL_HERITAGE_DATABASE['categories']
    subcategories = CULTURAL_HERITAGE_DATABASE['subcategories']
    significance_levels = CULTURAL_HERITAGE_DATABASE['significance_levels']
    locations = CULTURAL_HERITAGE_DATABASE['locations']
    conditions = CULTURAL_HERITAGE_DATABASE['conditions']
    protection_statuses = CULTURAL_HERITAGE_DATABASE['protection_statuses']
    statistics = CULTURAL_HERITAGE_DATABASE['statistics']

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
@admin_required
def botany_collection():
    """Botany collection database."""
    return render_template('admin_collection_database.html',
                          collection_name='Ботаничка збирка',
                          collection_icon='bi-flower1',
                          specimens=BOTANY_COLLECTION_DATABASE['specimens'],
                          statistics=BOTANY_COLLECTION_DATABASE['statistics'],
                          collection_type='botany')

@app.route('/admin/ichthyology_collection')
@admin_required
def ichthyology_collection():
    """Ichthyology collection database."""
    return render_template('admin_collection_database.html',
                          collection_name='Ихтиолошка збирка',
                          collection_icon='bi-water',
                          specimens=ICHTHYOLOGY_COLLECTION_DATABASE['specimens'],
                          statistics=ICHTHYOLOGY_COLLECTION_DATABASE['statistics'],
                          collection_type='ichthyology')

@app.route('/admin/entomology_collection')
@admin_required
def entomology_collection():
    """Entomology collection database."""
    return render_template('admin_collection_database.html',
                          collection_name='Ентомолошка збирка',
                          collection_icon='bi-bug',
                          specimens=ENTOMOLOGY_COLLECTION_DATABASE['specimens'],
                          statistics=ENTOMOLOGY_COLLECTION_DATABASE['statistics'],
                          collection_type='entomology')

@app.route('/admin/mycology_collection')
@admin_required
def mycology_collection():
    """Mycology collection database."""
    return render_template('admin_collection_database.html',
                          collection_name='Миколошка збирка',
                          collection_icon='bi-tree',
                          specimens=MYCOLOGY_COLLECTION_DATABASE['specimens'],
                          statistics=MYCOLOGY_COLLECTION_DATABASE['statistics'],
                          collection_type='mycology')

@app.route('/admin/herpetology_collection')
@admin_required
def herpetology_collection():
    """Herpetology collection database."""
    return render_template('admin_collection_database.html',
                          collection_name='Херпетолошка збирка',
                          collection_icon='bi-emoji-sunglasses',
                          specimens=HERPETOLOGY_COLLECTION_DATABASE['specimens'],
                          statistics=HERPETOLOGY_COLLECTION_DATABASE['statistics'],
                          collection_type='herpetology')

@app.route('/admin/ornithology_collection')
@admin_required
def ornithology_collection():
    """Ornithology collection database."""
    return render_template('admin_collection_database.html',
                          collection_name='Орнитолошка збирка',
                          collection_icon='bi-feather',
                          specimens=ORNITHOLOGY_COLLECTION_DATABASE['specimens'],
                          statistics=ORNITHOLOGY_COLLECTION_DATABASE['statistics'],
                          collection_type='ornithology')

@app.route('/admin/paleozoology_collection')
@admin_required
def paleozoology_collection():
    """Paleozoology collection database."""
    return render_template('admin_collection_database.html',
                          collection_name='Палеозоолошка збирка',
                          collection_icon='bi-gem',
                          specimens=PALEOZOOLOGY_COLLECTION_DATABASE['specimens'],
                          statistics=PALEOZOOLOGY_COLLECTION_DATABASE['statistics'],
                          collection_type='paleozoology')

@app.route('/admin/paleobotany_collection')
@admin_required
def paleobotany_collection():
    """Paleobotany collection database."""
    return render_template('admin_collection_database.html',
                          collection_name='Палеоботаничка збирка',
                          collection_icon='bi-flower2',
                          specimens=PALEOBOTANY_COLLECTION_DATABASE['specimens'],
                          statistics=PALEOBOTANY_COLLECTION_DATABASE['statistics'],
                          collection_type='paleobotany')

@app.route('/admin/petrology_collection')
@admin_required
def petrology_collection():
    """Petrology collection database."""
    return render_template('admin_collection_database.html',
                          collection_name='Петролошка збирка',
                          collection_icon='bi-mountains',
                          specimens=PETROLOGY_COLLECTION_DATABASE['specimens'],
                          statistics=PETROLOGY_COLLECTION_DATABASE['statistics'],
                          collection_type='petrology')

@app.route('/admin/meteorite_collection')
@admin_required
def meteorite_collection():
    """Meteorite collection database."""
    return render_template('admin_collection_database.html',
                          collection_name='Збирка метеорита',
                          collection_icon='bi-stars',
                          specimens=METEORITE_COLLECTION_DATABASE['specimens'],
                          statistics=METEORITE_COLLECTION_DATABASE['statistics'],
                          collection_type='meteorite')

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

@app.route('/admin/museum_databases')
@admin_required
def museum_databases():
    """Overview of all museum databases."""
    # Database statistics
    databases_info = {
        'employees': {
            'name': 'База запослених',
            'description': 'Информације о свим запосленима музеја',
            'icon': 'bi-people-fill',
            'count': len(MUSEUM_EMPLOYEES),
            'status': 'active',
            'url': '/admin/employees_database',
            'color': 'primary'
        },
        'employee_profiles': {
            'name': 'База профила запослених',
            'description': 'Биографије и стручни профили запослених',
            'icon': 'bi-person-badge',
            'count': len([e for e in MUSEUM_EMPLOYEES.values() if e.get('description')]),
            'status': 'active',
            'url': '/admin/employee_profiles_database',
            'color': 'info'
        },
        'minerals': {
            'name': 'База минерала',
            'description': 'Колекција минерала и геолошких узорака',
            'icon': 'bi-gem',
            'count': '5997',  # Professional mineral database
            'status': 'active',
            'url': '/mineral_database',
            'color': 'success'
        },
        'library': {
            'name': 'База библиотеке',
            'description': 'Каталог књига и научних публикација',
            'icon': 'bi-book',
            'count': len(LIBRARY_DATABASE['books']),
            'status': 'active',
            'url': '/admin/library_database',
            'color': 'info'
        },
        'cultural_heritage': {
            'name': 'База заштићених културних добара',
            'description': 'Регистар покретних културних добара под заштитом',
            'icon': 'bi-award',
            'count': len(CULTURAL_HERITAGE_DATABASE['heritage_items']),
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
        
        # CURATOR COLLECTIONS - Biology Department
        'botany_collection': {
            'name': 'Ботаничка збирка',
            'description': 'Хербаријум >40.000 примерака - ендемске биљке Балкана (Др М. Никетић - SANU, В. Стојановић, Др А. Савић, Др М. Несторовић)',
            'icon': 'bi-flower1',
            'count': '>40,000',
            'status': 'active',
            'url': '/admin/botany_collection',
            'color': 'success',
            'curators': ['mniketic@nhmbeo.rs', 'verica.stojanovic@nhmbeo.rs', 'aleksandra.savic@nhmbeo.rs', 'marko.nestorovic@nhmbeo.rs']
        },
        'ichthyology_collection': {
            'name': 'Ихтиолошка збирка',
            'description': 'Колекција риба и водених организама - виши кустос (Д. Вучић)',
            'icon': 'bi-water',
            'count': 'N/A',
            'status': 'active',
            'url': '/admin/ichthyology_collection',
            'color': 'info',
            'curators': ['dubravka.vucic@nhmbeo.rs']
        },
        'entomology_collection': {
            'name': 'Ентомолошка збирка',
            'description': 'Колекција инсеката - 1.710 врста приказано, збирка Odonata (М. Јовић - координатор Balkan OdoBase, А. Стојановић - конзерватор)',
            'icon': 'bi-bug',
            'count': '1,710+',
            'status': 'active',
            'url': '/admin/entomology_collection',
            'color': 'warning',
            'curators': ['milos.jovic@nhmbeo.rs', 'aleksandar@nhmbeo.rs']
        },
        'mycology_collection': {
            'name': 'Миколошка збирка',
            'description': 'Колекција гљива и макромицета Балкана (Др Б. Иванчевић - 30+ година истраживања)',
            'icon': 'bi-tree',
            'count': 'N/A',
            'status': 'active',
            'url': '/admin/mycology_collection',
            'color': 'success',
            'curators': ['boris@nhmbeo.rs']
        },
        'herpetology_collection': {
            'name': 'Херпетолошка збирка',
            'description': 'Колекција водоземаца и гмизаваца - 20+ година теренских истраживања (Др А. Пауновић)',
            'icon': 'bi-slash-circle',
            'count': 'N/A',
            'status': 'active',
            'url': '/admin/herpetology_collection',
            'color': 'danger',
            'curators': ['ana.paunovic@nhmbeo.rs']
        },
        'ornithology_collection': {
            'name': 'Орнитолошка збирка',
            'description': 'Колекција птица - Центар за маркирање (прстеновање) птица, програм Euring (Мср В. Попић)',
            'icon': 'bi-stars',
            'count': 'N/A',
            'status': 'active',
            'url': '/admin/ornithology_collection',
            'color': 'primary',
            'curators': ['vuk.popic@nhmbeo.rs']
        },
        'zoology_collection': {
            'name': 'Општа зоолошка збирка',
            'description': 'Зоолошка колекција - молекуларна биологија и ДНК баркодирање (З. Марковић - MSc)',
            'icon': 'bi-heart',
            'count': 'N/A',
            'status': 'development',
            'url': '#',
            'color': 'info',
            'curators': ['zorana.markovic@nhmbeo.rs']
        },
        'conservation_biology': {
            'name': 'Конзервација биолошких збирки',
            'description': 'Препарација и очување биолошких експоната (Г. Петковски - конзерватор, М. Мрваљевић, Ј. Кокотовић)',
            'icon': 'bi-shield-check',
            'count': 'N/A',
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
            'count': 'N/A',
            'status': 'active',
            'url': '/admin/paleozoology_collection',
            'color': 'warning',
            'curators': ['biljana.mitrovic@nhmbeo.rs', 'zoran.markovic@nhmbeo.rs', 'sanja.pavic@nhmbeo.rs', 'dragana.djuric@nhmbeo.rs', 'pejovic.ranko@nhmbeo.rs', 'milos.milivojevic@nhmbeo.rs']
        },
        'paleobotany_collection': {
            'name': 'Палеоботаничка збирка',
            'description': 'Фосилне биљке и праисторијска вегетација - кустос од 1993, професор палеоекологије (Др Д. Ђорђевић-Милутиновић)',
            'icon': 'bi-flower2',
            'count': 'N/A',
            'status': 'active',
            'url': '/admin/paleobotany_collection',
            'color': 'success',
            'curators': ['desadjm@nhmbeo.rs']
        },
        'petrology_collection': {
            'name': 'Петролошка збирка',
            'description': 'Колекција стена Србије - петрографија и геохемија (Т. Милић Бабић - виши кустос)',
            'icon': 'bi-layers',
            'count': 'N/A',
            'status': 'active',
            'url': '/admin/petrology_collection',
            'color': 'secondary',
            'curators': ['tatjana.milicbabic@nhmbeo.rs']
        },
        'meteorite_collection': {
            'name': 'Збирка метеорита',
            'description': 'Колекција метеорита Србије - Сокобањски метеорит и други (Др А. Луковић - минералог)',
            'icon': 'bi-star-fill',
            'count': 'N/A',
            'status': 'active',
            'url': '/admin/meteorite_collection',
            'color': 'warning',
            'curators': ['aca.lukovic@nhmbeo.rs']
        },
        'geology_conservation': {
            'name': 'Геолошка збирка и конзервација',
            'description': 'Геолошки узорци, препарација и конзервација фосила (Б. Радуловић - кустос, Н. Младеновић - конзерватор)',
            'icon': 'bi-geo-alt',
            'count': 'N/A',
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

    return dict(
        user_logged_in=user_logged_in,
        user_name=session.get('user_name', ''),
        user_role=session.get('user_role', ''),
        user_email=session.get('user_email', ''),
        is_admin=is_admin
    )

# Simple app runner (complex mounting disabled for now)
def create_app():
    """Create the main application (simplified version)."""
    print("📋 Using simplified museum system")
    print("⚠️ Timesheet system available via instructions")
    return app

# Route handlers for input forms

@app.route('/admin/add_book', methods=['GET', 'POST'])
@admin_required
def add_book():
    """Add new book to library database."""
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
            'id': len(CULTURAL_HERITAGE_DATABASE['heritage_items']) + 1,
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
        CULTURAL_HERITAGE_DATABASE['heritage_items'].append(heritage_data)
        flash('Културно добро је успешно додато!', 'success')
        return redirect(url_for('cultural_heritage_database'))

    return render_template('admin_add_heritage_item.html')

@app.route('/admin/add_collection_item/<collection_type>', methods=['GET', 'POST'])
@admin_required
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

    # Save reservations to file
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
    vehicle_data = {
        'id': max([v['id'] for v in MUSEUM_VEHICLES], default=0) + 1,
        'name': request.form.get('name', '').strip(),
        'registration': request.form.get('registration', '').strip(),
        'type': request.form.get('type', '').strip(),
        'capacity': request.form.get('capacity', '').strip(),
        'status': request.form.get('status', 'Активно').strip(),
        'year': request.form.get('year', '').strip(),
        'make_model': request.form.get('make_model', '').strip(),
        'notes': request.form.get('notes', '').strip()
    }

    MUSEUM_VEHICLES.append(vehicle_data)

    # Save vehicles to file
    if save_vehicles():
        flash('Возило је успешно додато!', 'success')
    else:
        flash('Грешка при чувању возила!', 'error')

    return redirect(url_for('vehicle_management'))

@app.route('/edit_vehicle', methods=['POST'])
@admin_required
def edit_vehicle():
    """Edit existing vehicle."""
    vehicle_id = int(request.form.get('vehicle_id'))

    for vehicle in MUSEUM_VEHICLES:
        if vehicle['id'] == vehicle_id:
            vehicle['name'] = request.form.get('name', '').strip()
            vehicle['registration'] = request.form.get('registration', '').strip()
            vehicle['type'] = request.form.get('type', '').strip()
            vehicle['capacity'] = request.form.get('capacity', '').strip()
            vehicle['status'] = request.form.get('status', '').strip()
            break

    # Save vehicles to file
    if save_vehicles():
        flash('Возило је успешно ажурирано!', 'success')
    else:
        flash('Грешка при чувању измена!', 'error')

    return redirect(url_for('vehicle_management'))

@app.route('/delete_vehicle', methods=['POST'])
@admin_required
def delete_vehicle():
    """Delete vehicle."""
    vehicle_id = int(request.form.get('vehicle_id'))

    # Check if vehicle has active reservations
    active_reservations = [r for r in VEHICLE_RESERVATIONS
                          if r['vehicle_id'] == vehicle_id and r['end_date'] >= datetime.now().strftime('%Y-%m-%d')]

    if active_reservations:
        flash('Не можете обрисати возило које има активне резервације!', 'error')
    else:
        global MUSEUM_VEHICLES
        MUSEUM_VEHICLES = [v for v in MUSEUM_VEHICLES if v['id'] != vehicle_id]

        # Save vehicles to file
        if save_vehicles():
            flash('Возило је успешно обрисано!', 'success')
        else:
            flash('Грешка при чувању измена!', 'error')

    return redirect(url_for('vehicle_management'))

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