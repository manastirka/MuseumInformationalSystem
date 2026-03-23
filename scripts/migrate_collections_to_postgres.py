#!/usr/bin/env python3
"""
Migrate Biological Collections from app.py to PostgreSQL
Phase 3C Migration - All 9 biological collections
"""

import os
import sys
import psycopg
from datetime import datetime
from dotenv import load_dotenv

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Load environment variables
load_dotenv()

DATABASE_URL = os.environ.get('DATABASE_URL')
if not DATABASE_URL:
    print("ERROR: DATABASE_URL environment variable not set")
    sys.exit(1)

# Convert SQLAlchemy-style URL to psycopg format
DB_URL = DATABASE_URL.replace('postgresql+psycopg://', 'postgresql://')

# Define all collection data (extracted from app.py)
COLLECTIONS_DATA = {
    'botany': {
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
        ]
    },
    'ichthyology': {
        'specimens': [
            {
                'catalog_number': 'ICH-2024-001',
                'scientific_name': 'Acipenser ruthenus',
                'common_name_sr': 'Кечига',
                'family': 'Acipenseridae',
                'location_found': 'Дунав, Србија',
                'habitat': 'Слатководна',
                'date_collected': '2022-08-15',
                'measurements': {'length_cm': 85, 'weight_kg': 4.5, 'age_estimated': '12 година'},
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
                'measurements': {'length_cm': 120, 'weight_kg': 18, 'age_estimated': '8 година'},
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
                'measurements': {'length_cm': 18, 'weight_kg': 0.15, 'age_estimated': '3 године'},
                'condition': 'Одличан препарат',
                'conservation_status': 'Угрожена (EN)',
                'description': 'Балкански ендем. Карактеристичне зебрасте пруге.',
                'curator': 'dubravka.vucic@nhmbeo.rs'
            }
        ]
    },
    'entomology': {
        'specimens': [
            {
                'catalog_number': 'ENT-LEP-001',
                'scientific_name': 'Parnassius apollo',
                'common_name_sr': 'Аполонов лептир',
                'family': 'Papilionidae',
                'order_name': 'Lepidoptera',
                'location_found': 'Копаоник, Србија',
                'altitude': '1400-2000m',
                'date_collected': '2023-07-10',
                'collector': 'Г. Петковски',
                'condition': 'Одличан препарат',
                'endemic_status': 'Релик терцијара',
                'conservation_status': 'Строго заштићена (EN)',
                'description': 'Ендемични балкански лептир. Реликт из терцијара.',
                'curator': 'goran.petkovski@nhmbeo.rs'
            },
            {
                'catalog_number': 'ENT-LEP-002',
                'scientific_name': 'Graellsia isabellae',
                'common_name_sr': 'Изабелин лептир',
                'family': 'Saturniidae',
                'order_name': 'Lepidoptera',
                'location_found': 'Тара, Србија',
                'altitude': '800-1200m',
                'date_collected': '2022-05-18',
                'collector': 'Г. Петковски',
                'condition': 'Одлично',
                'conservation_status': 'Угрожена',
                'description': 'Један од најлепших европских лептира.',
                'curator': 'goran.petkovski@nhmbeo.rs'
            },
            {
                'catalog_number': 'ENT-COL-001',
                'scientific_name': 'Rosalia alpina',
                'common_name_sr': 'Алпски стрижибуба',
                'family': 'Cerambycidae',
                'order_name': 'Coleoptera',
                'location_found': 'Шара, Србија',
                'altitude': '900-1600m',
                'date_collected': '2023-06-25',
                'collector': 'Г. Петковски',
                'condition': 'Одлично',
                'conservation_status': 'Строго заштићена',
                'description': 'Велики плави стрижибуба. Индикатор очуваних шума.',
                'curator': 'goran.petkovski@nhmbeo.rs'
            },
            {
                'catalog_number': 'ENT-HYM-001',
                'scientific_name': 'Vespa crabro',
                'common_name_sr': 'Стршљен',
                'family': 'Vespidae',
                'order_name': 'Hymenoptera',
                'location_found': 'Фрушка гора, Србија',
                'date_collected': '2023-08-10',
                'collector': 'Г. Петковски',
                'condition': 'Добар препарат',
                'description': 'Највећа врста осе у Европи.',
                'curator': 'goran.petkovski@nhmbeo.rs'
            },
            {
                'catalog_number': 'ENT-ORT-001',
                'scientific_name': 'Saga pedo',
                'common_name_sr': 'Степски скакавац',
                'family': 'Tettigoniidae',
                'order_name': 'Orthoptera',
                'location_found': 'Делиблатска пешчара, Србија',
                'date_collected': '2022-07-05',
                'collector': 'Г. Петковски',
                'condition': 'Одлично',
                'conservation_status': 'Критично угрожена (CR)',
                'description': 'Највећи скакавац Европе. Партеногенетска репродукција.',
                'curator': 'goran.petkovski@nhmbeo.rs'
            },
            {
                'catalog_number': 'ENT-ODO-001',
                'scientific_name': 'Calopteryx splendens',
                'common_name_sr': 'Обични вилински коњиц',
                'family': 'Calopterygidae',
                'order_name': 'Odonata',
                'location_found': 'Обедска бара, Србија',
                'date_collected': '2023-06-12',
                'collector': 'Г. Петковски',
                'condition': 'Одлично',
                'description': 'Велики плави вилински коњиц.',
                'curator': 'goran.petkovski@nhmbeo.rs'
            }
        ]
    },
    'mycology': {
        'specimens': [
            {
                'catalog_number': 'MYC-2024-001',
                'scientific_name': 'Boletus edulis',
                'common_name_sr': 'Вргањ',
                'family': 'Boletaceae',
                'location_found': 'Златибор, Србија',
                'altitude': '800-1200m',
                'date_collected': '2023-09-15',
                'collector': 'Др М. Караџић',
                'condition': 'Сушени препарат',
                'description': 'Јестива врста. Најцењенија гљива у Србији.',
                'curator': 'milan.karadzic@nhmbeo.rs'
            },
            {
                'catalog_number': 'MYC-2024-002',
                'scientific_name': 'Amanita muscaria',
                'common_name_sr': 'Мухара',
                'family': 'Amanitaceae',
                'location_found': 'Тара, Србија',
                'altitude': '600-1400m',
                'date_collected': '2023-10-05',
                'collector': 'Др М. Караџић',
                'condition': 'Одлично',
                'description': 'Отровна гљива са црвеним шеширом и белим пегама.',
                'curator': 'milan.karadzic@nhmbeo.rs'
            },
            {
                'catalog_number': 'MYC-2024-003',
                'scientific_name': 'Cantharellus cibarius',
                'common_name_sr': 'Лисичарка',
                'family': 'Cantharellaceae',
                'location_found': 'Копаоник, Србија',
                'altitude': '900-1500m',
                'date_collected': '2023-08-20',
                'collector': 'Др М. Караџић',
                'condition': 'Сушени препарат',
                'description': 'Јестива врста са жутим шеширом.',
                'curator': 'milan.karadzic@nhmbeo.rs'
            },
            {
                'catalog_number': 'MYC-2024-004',
                'scientific_name': 'Morchella esculenta',
                'common_name_sr': 'Смр',
                'family': 'Morchellaceae',
                'location_found': 'Фрушка гора, Србија',
                'date_collected': '2023-04-12',
                'collector': 'Др М. Караџић',
                'condition': 'Сушени препарат',
                'description': 'Ретка пролећна гљива. Врло цењена.',
                'curator': 'milan.karadzic@nhmbeo.rs'
            },
            {
                'catalog_number': 'MYC-2024-005',
                'scientific_name': 'Ganoderma lucidum',
                'common_name_sr': 'Сјајна трутица',
                'family': 'Ganodermataceae',
                'location_found': 'Ђердап, Србија',
                'date_collected': '2023-07-18',
                'collector': 'Др М. Караџић',
                'condition': 'Одлично',
                'description': 'Медицинска гљива. Лековита врста.',
                'curator': 'milan.karadzic@nhmbeo.rs'
            }
        ]
    },
    'herpetology': {
        'specimens': [
            {
                'catalog_number': 'HERP-AMP-001',
                'scientific_name': 'Salamandra salamandra',
                'common_name_sr': 'Шарени даждевњак',
                'family': 'Salamandridae',
                'order_name': 'Caudata',
                'class_name': 'Amphibia',
                'location_found': 'Тара, Србија',
                'altitude': '400-1200m',
                'date_collected': '2023-05-15',
                'collector': 'М. Мрваљевић',
                'condition': 'Влажан препарат',
                'conservation_status': 'Заштићена',
                'description': 'Најпознатији балкански даждевњак.',
                'curator': 'milos.mrvaljevic@nhmbeo.rs'
            },
            {
                'catalog_number': 'HERP-AMP-002',
                'scientific_name': 'Bombina variegata',
                'common_name_sr': 'Планински кукавичар',
                'family': 'Bombinatoridae',
                'order_name': 'Anura',
                'class_name': 'Amphibia',
                'location_found': 'Копаоник, Србија',
                'date_collected': '2022-06-10',
                'collector': 'М. Мрваљевић',
                'condition': 'Влажан препарат',
                'conservation_status': 'Угрожена',
                'description': 'Мали жабац са наранџастим трбухом.',
                'curator': 'milos.mrvaljevic@nhmbeo.rs'
            },
            {
                'catalog_number': 'HERP-REP-001',
                'scientific_name': 'Vipera ammodytes',
                'common_name_sr': 'Поскок',
                'family': 'Viperidae',
                'order_name': 'Squamata',
                'class_name': 'Reptilia',
                'location_found': 'Ртањ, Србија',
                'date_collected': '2023-07-22',
                'collector': 'М. Мрваљевић',
                'condition': 'Влажан препарат',
                'conservation_status': 'Заштићена',
                'description': 'Најотровнија европска змија.',
                'curator': 'milos.mrvaljevic@nhmbeo.rs'
            },
            {
                'catalog_number': 'HERP-REP-002',
                'scientific_name': 'Lacerta viridis',
                'common_name_sr': 'Зелени гуштер',
                'family': 'Lacertidae',
                'order_name': 'Squamata',
                'class_name': 'Reptilia',
                'location_found': 'Фрушка гора, Србија',
                'date_collected': '2023-06-05',
                'collector': 'М. Мрваљевић',
                'condition': 'Сув препарат',
                'description': 'Велики зелени гуштер. Најчешћи у Србији.',
                'curator': 'milos.mrvaljevic@nhmbeo.rs'
            },
            {
                'catalog_number': 'HERP-REP-003',
                'scientific_name': 'Testudo hermanni',
                'common_name_sr': 'Шумска корњача',
                'family': 'Testudinidae',
                'order_name': 'Testudines',
                'class_name': 'Reptilia',
                'location_found': 'Југоисточна Србија',
                'date_collected': '2022-08-18',
                'collector': 'М. Мрваљевић',
                'condition': 'Сув препарат',
                'conservation_status': 'Критично угрожена (CR)',
                'description': 'Европска шумска корњача. Веома ретка у Србији.',
                'curator': 'milos.mrvaljevic@nhmbeo.rs'
            },
            {
                'catalog_number': 'HERP-AMP-003',
                'scientific_name': 'Triturus ivanbureschi',
                'common_name_sr': 'Ивана-Бурешев мрмољак',
                'family': 'Salamandridae',
                'order_name': 'Caudata',
                'class_name': 'Amphibia',
                'location_found': 'Јужна Србија',
                'date_collected': '2023-04-20',
                'collector': 'М. Мрваљевић',
                'condition': 'Влажан препарат',
                'endemic_status': 'Балкански ендем',
                'conservation_status': 'Угрожена',
                'description': 'Новооткривена балканска врста мрмољка.',
                'curator': 'milos.mrvaljevic@nhmbeo.rs'
            }
        ]
    },
    'ornithology': {
        'specimens': [
            {
                'catalog_number': 'ORN-2024-001',
                'scientific_name': 'Aquila chrysaetos',
                'common_name_sr': 'Орао крсташ',
                'family': 'Accipitridae',
                'order_name': 'Accipitriformes',
                'location_found': 'Стара планина, Србија',
                'altitude': '1400-2000m',
                'date_collected': '2022-11-10',
                'collector': 'Д. Савић',
                'measurements': {'wing_span': 210, 'length_cm': 85, 'weight_kg': 4.5},
                'condition': 'Одличан препарат',
                'conservation_status': 'Строго заштићена',
                'description': 'Највећи грабљивац Србије.',
                'curator': 'dusan.savic@nhmbeo.rs'
            },
            {
                'catalog_number': 'ORN-2024-002',
                'scientific_name': 'Bubo bubo',
                'common_name_sr': 'Велика ушара',
                'family': 'Strigidae',
                'order_name': 'Strigiformes',
                'location_found': 'Ђердап, Србија',
                'date_collected': '2023-03-15',
                'collector': 'Д. Савић',
                'measurements': {'wing_span': 180, 'length_cm': 70},
                'condition': 'Одлично',
                'conservation_status': 'Заштићена',
                'description': 'Највећа сова у Србији.',
                'curator': 'dusan.savic@nhmbeo.rs'
            },
            {
                'catalog_number': 'ORN-2024-003',
                'scientific_name': 'Alcedo atthis',
                'common_name_sr': 'Водомар',
                'family': 'Alcedinidae',
                'order_name': 'Coraciiformes',
                'location_found': 'Обедска бара, Србија',
                'date_collected': '2023-08-20',
                'collector': 'Д. Савић',
                'measurements': {'length_cm': 17, 'weight_g': 40},
                'condition': 'Одлично',
                'description': 'Плава птица риболовка.',
                'curator': 'dusan.savic@nhmbeo.rs'
            },
            {
                'catalog_number': 'ORN-2024-004',
                'scientific_name': 'Dendrocopos major',
                'common_name_sr': 'Велики детлић',
                'family': 'Picidae',
                'order_name': 'Piciformes',
                'location_found': 'Фрушка гора, Србија',
                'date_collected': '2023-02-10',
                'collector': 'Д. Савић',
                'condition': 'Одлично',
                'description': 'Најчешћи детлић у Србији.',
                'curator': 'dusan.savic@nhmbeo.rs'
            },
            {
                'catalog_number': 'ORN-2024-005',
                'scientific_name': 'Upupa epops',
                'common_name_sr': 'Пупавац',
                'family': 'Upupidae',
                'order_name': 'Bucerotiformes',
                'location_found': 'Панонска низија, Србија',
                'date_collected': '2023-05-05',
                'collector': 'Д. Савић',
                'condition': 'Одлично',
                'description': 'Птица са карактеристичном крестом.',
                'curator': 'dusan.savic@nhmbeo.rs'
            }
        ]
    },
    'paleozoology': {
        'specimens': [
            {
                'catalog_number': 'PALEO-MAM-001',
                'scientific_name': 'Mammuthus primigenius',
                'common_name_sr': 'Вунасти мамут',
                'family': 'Elephantidae',
                'order_name': 'Proboscidea',
                'location_found': 'Костолац, Србија',
                'date_collected': '2015-06-20',
                'collector': 'Др Ј. Миленковић',
                'age': 'Плеистоцен (50,000 година)',
                'condition': 'Парцијални скелет',
                'description': 'Парцијални скелет младог мамута. Леденодобски џин.',
                'curator': 'jovana.milenkovic@nhmbeo.rs'
            },
            {
                'catalog_number': 'PALEO-MAM-002',
                'scientific_name': 'Ursus spelaeus',
                'common_name_sr': 'Пећински медвед',
                'family': 'Ursidae',
                'order_name': 'Carnivora',
                'location_found': 'Ресавска пећина, Србија',
                'date_collected': '2018-09-12',
                'collector': 'Др Ј. Миленковић',
                'age': 'Плеистоцен (30,000 година)',
                'condition': 'Лобања и зуби',
                'description': 'Изумрли европски медвед. Живео у пећинама.',
                'curator': 'jovana.milenkovic@nhmbeo.rs'
            },
            {
                'catalog_number': 'PALEO-REP-001',
                'scientific_name': 'Mosasaurus sp.',
                'common_name_sr': 'Мозазаур',
                'family': 'Mosasauridae',
                'order_name': 'Squamata',
                'location_found': 'Сењски рудник, Србија',
                'date_collected': '2010-05-15',
                'collector': 'Др Ј. Миленковић',
                'age': 'Креда (80 милиона година)',
                'condition': 'Зуби и фрагменти лобање',
                'description': 'Морски гмизавац из доба диносауруса.',
                'curator': 'jovana.milenkovic@nhmbeo.rs'
            },
            {
                'catalog_number': 'PALEO-MAM-003',
                'scientific_name': 'Coelodonta antiquitatis',
                'common_name_sr': 'Вунасти носорог',
                'family': 'Rhinocerotidae',
                'order_name': 'Perissodactyla',
                'location_found': 'Дунав, Вишњица',
                'date_collected': '2012-08-05',
                'collector': 'Др Ј. Миленковић',
                'age': 'Плеистоцен (40,000 година)',
                'condition': 'Парцијална лобања',
                'description': 'Леденодобски носорог са две рогове.',
                'curator': 'jovana.milenkovic@nhmbeo.rs'
            },
            {
                'catalog_number': 'PALEO-MAM-004',
                'scientific_name': 'Bison priscus',
                'common_name_sr': 'Степски бизон',
                'family': 'Bovidae',
                'order_name': 'Artiodactyla',
                'location_found': 'Делиблатска пешчара',
                'date_collected': '2016-07-18',
                'collector': 'Др Ј. Миленковић',
                'age': 'Плеистоцен (25,000 година)',
                'condition': 'Рогови и фрагменти костију',
                'description': 'Предак данашњих бизона.',
                'curator': 'jovana.milenkovic@nhmbeo.rs'
            },
            {
                'catalog_number': 'PALEO-MAM-005',
                'scientific_name': 'Megaloceros giganteus',
                'common_name_sr': 'Џиновски јелен',
                'family': 'Cervidae',
                'order_name': 'Artiodactyla',
                'location_found': 'Воћин, Србија',
                'date_collected': '2014-04-22',
                'collector': 'Др Ј. Миленковић',
                'age': 'Плеистоцен (12,000 година)',
                'condition': 'Парцијални рогови',
                'description': 'Јелен са рогањем распона до 3.6 м.',
                'curator': 'jovana.milenkovic@nhmbeo.rs'
            }
        ]
    },
    'paleobotany': {
        'specimens': [
            {
                'catalog_number': 'PALEOBOT-001',
                'scientific_name': 'Calamites sp.',
                'common_name_sr': 'Фосилна прeslica',
                'family': 'Calamitaceae',
                'order_name': 'Equisetales',
                'location_found': 'Колубара, Србија',
                'date_collected': '2019-06-15',
                'collector': 'Др Н. Вукчевић',
                'age': 'Карбон (300 милиона година)',
                'condition': 'Одличан фосил',
                'description': 'Стабло древне прeslice. Градитељ карбонских шума.',
                'curator': 'nikola.vukcevic@nhmbeo.rs'
            },
            {
                'catalog_number': 'PALEOBOT-002',
                'scientific_name': 'Lepidodendron sp.',
                'common_name_sr': 'Лепидодендрон',
                'family': 'Lepidodendraceae',
                'order_name': 'Lepidodendrales',
                'location_found': 'Ресавица, Србија',
                'date_collected': '2017-08-20',
                'collector': 'Др Н. Вукчевић',
                'age': 'Карбон (310 милиона година)',
                'condition': 'Отисак коре',
                'description': 'Древна папрат-дрво. Могла је достићи 30м висине.',
                'curator': 'nikola.vukcevic@nhmbeo.rs'
            },
            {
                'catalog_number': 'PALEOBOT-003',
                'scientific_name': 'Pterophyllum sp.',
                'common_name_sr': 'Фосилна папрат',
                'family': 'Pteridophyta',
                'location_found': 'Алексинац, Србија',
                'date_collected': '2020-05-10',
                'collector': 'Др Н. Вукчевић',
                'age': 'Тријас (220 милиона година)',
                'condition': 'Комплетан лист',
                'description': 'Очувана папратна фронда из тријаса.',
                'curator': 'nikola.vukcevic@nhmbeo.rs'
            },
            {
                'catalog_number': 'PALEOBOT-004',
                'scientific_name': 'Ginkgo sp.',
                'common_name_sr': 'Фосилни гинко',
                'family': 'Ginkgoaceae',
                'location_found': 'Неготин, Србија',
                'date_collected': '2018-09-05',
                'collector': 'Др Н. Вукчевић',
                'age': 'Јура (180 милиона година)',
                'condition': 'Очуван лист',
                'description': 'Лист древног гинка. Жива фосилна врста.',
                'curator': 'nikola.vukcevic@nhmbeo.rs'
            }
        ]
    },
    'petrology': {
        'specimens': [
            {
                'catalog_number': 'PETRO-IGN-001',
                'scientific_name': 'Granit',
                'common_name_sr': 'Гранит',
                'location_found': 'Бујановац, Србија',
                'date_collected': '2021-07-10',
                'collector': 'Др П. Николић',
                'description': 'Магматска стена. Кварц, фелдспат, слуда.',
                'curator': 'petar.nikolic@nhmbeo.rs'
            },
            {
                'catalog_number': 'PETRO-MET-001',
                'scientific_name': 'Gnajis',
                'common_name_sr': 'Гнајс',
                'location_found': 'Копаоник, Србија',
                'date_collected': '2022-06-15',
                'collector': 'Др П. Николић',
                'description': 'Метаморфна стена. Настала од гранита.',
                'curator': 'petar.nikolic@nhmbeo.rs'
            },
            {
                'catalog_number': 'PETRO-SED-001',
                'scientific_name': 'Kreč',
                'common_name_sr': 'Кречњак',
                'location_found': 'Ђердап, Србија',
                'date_collected': '2020-08-20',
                'collector': 'Др П. Николић',
                'description': 'Седиментна стена. Калцијум карбонат.',
                'curator': 'petar.nikolic@nhmbeo.rs'
            },
            {
                'catalog_number': 'PETRO-IGN-002',
                'scientific_name': 'Bazalt',
                'common_name_sr': 'Базалт',
                'location_found': 'Мали Крш, Србија',
                'date_collected': '2021-09-10',
                'collector': 'Др П. Николић',
                'description': 'Вулканска стена. Тамна, ситнозрна.',
                'curator': 'petar.nikolic@nhmbeo.rs'
            }
        ]
    }
}


def migrate_collections():
    """Migrate all biological collections to PostgreSQL."""

    print("=" * 80)
    print("BIOLOGICAL COLLECTIONS MIGRATION TO POSTGRESQL")
    print("Phase 3C - All 9 Collections")
    print("=" * 80)

    # Connect to PostgreSQL
    print(f"\n1. Connecting to PostgreSQL...")
    try:
        conn = psycopg.connect(DB_URL)
        cur = conn.cursor()
        print(f"   ✓ Connected to database")
    except Exception as e:
        print(f"   ✗ ERROR: Failed to connect - {e}")
        return False

    # Check if table exists and is empty
    print(f"\n2. Checking collection_specimens table...")
    try:
        cur.execute("SELECT COUNT(*) FROM collection_specimens")
        existing_count = cur.fetchone()[0]
        print(f"   ✓ Table exists with {existing_count} existing records")

        if existing_count > 0:
            response = input(f"\n   WARNING: Table has {existing_count} records. Delete and re-import? (yes/no): ")
            if response.lower() == 'yes':
                cur.execute("DELETE FROM collection_specimens")
                conn.commit()
                print(f"   ✓ Deleted {existing_count} existing records")
            else:
                print(f"   → Skipping migration (table not empty)")
                conn.close()
                return True
    except Exception as e:
        print(f"   ✗ ERROR: Table check failed - {e}")
        conn.close()
        return False

    # Count total specimens
    total_specimens = sum(len(data['specimens']) for data in COLLECTIONS_DATA.values())
    print(f"\n3. Migrating {total_specimens} specimens from 9 collections...")

    insert_sql = """
        INSERT INTO collection_specimens (
            catalog_number, collection_type, scientific_name, common_name_sr,
            family, order_name, class_name, location_found, locality_details,
            habitat, altitude, date_collected, collector, age, sex, condition,
            measurements, endemic_status, conservation_status, storage_location,
            herbarium_number, curator, description, notes, status
        ) VALUES (
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
            %s::jsonb, %s, %s, %s, %s, %s, %s, %s, %s
        )
    """

    migrated = 0
    errors = 0

    for collection_type, collection_data in COLLECTIONS_DATA.items():
        specimens = collection_data['specimens']
        print(f"\n   → Migrating {collection_type}: {len(specimens)} specimens...")

        for specimen in specimens:
            try:
                # Parse date
                date_collected = specimen.get('date_collected')

                # Get measurements as JSONB
                measurements = specimen.get('measurements')
                if measurements:
                    import json
                    measurements_json = json.dumps(measurements)
                else:
                    measurements_json = None

                # Clean values
                def clean_value(val):
                    if val == '' or val is None:
                        return None
                    return val

                cur.execute(insert_sql, (
                    specimen.get('catalog_number'),
                    collection_type,
                    specimen.get('scientific_name'),
                    clean_value(specimen.get('common_name_sr')),
                    clean_value(specimen.get('family')),
                    clean_value(specimen.get('order_name')),
                    clean_value(specimen.get('class_name')),
                    clean_value(specimen.get('location_found')),
                    clean_value(specimen.get('locality_details')),
                    clean_value(specimen.get('habitat')),
                    clean_value(specimen.get('altitude')),
                    date_collected,
                    clean_value(specimen.get('collector')),
                    clean_value(specimen.get('age')),
                    clean_value(specimen.get('sex')),
                    clean_value(specimen.get('condition')),
                    measurements_json,
                    clean_value(specimen.get('endemic_status')),
                    clean_value(specimen.get('conservation_status')),
                    clean_value(specimen.get('storage_location')),
                    clean_value(specimen.get('herbarium_number')),
                    clean_value(specimen.get('curator')),
                    clean_value(specimen.get('description')),
                    clean_value(specimen.get('notes')),
                    'active'
                ))

                migrated += 1

            except Exception as e:
                errors += 1
                print(f"   ✗ ERROR migrating {specimen.get('catalog_number')}: {e}")
                continue

        print(f"   ✓ Migrated {len(specimens)} {collection_type} specimens")

    # Commit transaction
    try:
        conn.commit()
        print(f"\n   ✓ Committed {migrated} specimens to database")
    except Exception as e:
        print(f"   ✗ ERROR: Commit failed - {e}")
        conn.rollback()
        conn.close()
        return False

    # Verify migration
    print(f"\n4. Verifying migration...")
    cur.execute("SELECT COUNT(*) FROM collection_specimens")
    final_count = cur.fetchone()[0]
    print(f"   ✓ PostgreSQL count: {final_count}")
    print(f"   ✓ Source count: {total_specimens}")

    if final_count == total_specimens:
        print(f"   ✓ SUCCESS: All specimens migrated correctly!")
    else:
        print(f"   ⚠ WARNING: Count mismatch")

    # Get statistics by collection
    print(f"\n5. Collection statistics...")
    cur.execute("""
        SELECT collection_type, COUNT(*)
        FROM collection_specimens
        GROUP BY collection_type
        ORDER BY collection_type
    """)
    collections = cur.fetchall()
    print(f"\n   Specimens by collection:")
    for coll_type, count in collections:
        print(f"     - {coll_type}: {count} specimens")

    # Close connection
    cur.close()
    conn.close()

    print("\n" + "=" * 80)
    print(f"MIGRATION COMPLETE")
    print(f"  Total specimens: {total_specimens}")
    print(f"  Migrated: {migrated}")
    print(f"  Errors: {errors}")
    print(f"  Success rate: {(migrated/total_specimens*100):.1f}%")
    print("=" * 80)

    return errors == 0


if __name__ == '__main__':
    success = migrate_collections()
    sys.exit(0 if success else 1)
