"""Shared route implementations for project pages and planner wrappers."""

import json
import logging
import os
import time
import uuid
from datetime import datetime
from pathlib import Path

from flask import jsonify, render_template, request, send_from_directory, session, url_for
from runtime_lock_utils import load_json_file, write_json_file

logger = logging.getLogger(__name__)


def render_projects_page():
    """Render the main project overview page."""
    return render_template('admin_projekti.html')


def _extract_project_document_text(file_path):
    """Extract readable text from locally supported project document formats."""
    suffix = file_path.suffix.lower()
    try:
        if suffix == '.docx':
            from docx import Document

            document = Document(str(file_path))
            parts = [paragraph.text.strip() for paragraph in document.paragraphs if paragraph.text and paragraph.text.strip()]
            return '\n\n'.join(parts)
        if suffix == '.rtf':
            from striprtf.striprtf import rtf_to_text

            return rtf_to_text(file_path.read_text('utf-8', errors='ignore')).strip()
    except Exception as exc:
        logger.warning("Project document extraction failed for %s: %s", file_path.name, exc)
    return ''


def _get_project_documentation_items(app_root_path):
    """Build project documentation metadata for inline readers."""
    project_dir = Path(app_root_path) / 'Projekti'
    docs = [
        {
            'filename': 'ER ИЗВЕШТАЈ ПОСЛОДАВЦА....docx',
            'title': 'Захтеви послодавца (ER)',
            'description': 'Техничко-функционални захтеви за пројектовање и изградњу.',
            'icon': 'bi-file-earmark-word',
            'badge': 'DOCX',
            'theme': 'docx',
        },
        {
            'filename': 'Pregled i opis standarda baziran na projektnom zadatku.rtf',
            'title': 'Преглед стандарда',
            'description': 'Национални и међународни стандарди за изградњу и опремање музеја.',
            'icon': 'bi-file-earmark-richtext',
            'badge': 'RTF',
            'theme': 'rtf',
        },
        {
            'filename': 'Geology_department_permanent _exibition_concept.docx',
            'title': 'Концепт геолошке поставке',
            'description': 'Тематски план сталне поставке „Геолошка ризница Србије”.',
            'icon': 'bi-file-earmark-word',
            'badge': 'DOCX',
            'theme': 'docx',
        },
        {
            'filename': 'KONCEPT BIOLOŠKOG DELA STALNE POSTAVKE_draft.pdf',
            'title': 'Концепт биолошке поставке',
            'description': 'PDF преглед концепта биолошког дела сталне поставке.',
            'icon': 'bi-file-earmark-pdf',
            'badge': 'PDF',
            'theme': 'pdf',
        },
    ]

    items = []
    for doc in docs:
        path = project_dir / doc['filename']
        item = dict(doc)
        item['exists'] = path.exists()
        item['inline_type'] = 'pdf' if path.suffix.lower() == '.pdf' else 'text'
        item['content'] = _extract_project_document_text(path) if item['exists'] and item['inline_type'] == 'text' else ''
        item['available_for_reading'] = bool(item['content']) or item['inline_type'] == 'pdf'
        try:
            item['size_label'] = f"{path.stat().st_size / 1024:.0f} KB" if item['exists'] else ''
        except OSError:
            item['size_label'] = ''
        items.append(item)

    return items


def render_project_documentation(*, app_root_path):
    """Render inline project documentation reader."""
    documents = _get_project_documentation_items(app_root_path)
    return render_template('admin_projekti_dokumentacija.html', documents=documents)


def render_project_space_planner():
    """Render the project space planner shell page."""
    return render_template('admin_projekti_space_planner.html')


PROJECT_SPACE_PLAN_FILE = '03 osnova kota -5,001.jpg'
PROJECT_SPACE_PLAN_IMAGE_SIZE = {'width': 10630, 'height': 1684}
PROJECT_SPACE_DEPOT_PLAN_FILE = 'postavka_depoa-1.jpg'
PROJECT_SPACE_DEPOT_PLAN_IMAGE_SIZE = {'width': 3309, 'height': 2339}
PROJECT_DEPOT_PLAN_AREA_ANNOTATIONS = [
    {'x': 25.22, 'y': 32.86, 'area_m2': 247.32, 'label': '6.8', 'name': '6.8 Depo fosilizovanih kičmenjaka'},
    {'x': 40.31, 'y': 31.83, 'area_m2': 37.90, 'label': '6.9.1 (1-2)', 'name': '6.9.1 Konzerv. radion. 1 i 2'},
    {'x': 50.57, 'y': 32.45, 'area_m2': 192.33, 'label': '6.6', 'name': '6.6 Depo fosilizovanih beskičmenjaka'},
    {'x': 66.17, 'y': 36.49, 'area_m2': 194.27, 'label': '6.4', 'name': '6.4 Depo minerala i meteorita'},
    {'x': 75.54, 'y': 35.68, 'area_m2': 37.90, 'label': '6.9.1 (3-4)', 'name': '6.9.1 Konzerv. radion. 3 i 4'},
    {'x': 83.39, 'y': 35.46, 'area_m2': 265.87, 'label': '6.5', 'name': '6.5 Depo petrološke zbirke'},
    {'x': 17.54, 'y': 45.13, 'area_m2': 50.88, 'label': '2.4', 'name': '2.4 Geološka konzervatorska radionica'},
    {'x': 36.37, 'y': 44.23, 'area_m2': 38.77, 'label': '8.2', 'name': '8.2 Mokra ihtiološka zbirka'},
    {'x': 53.93, 'y': 46.37, 'area_m2': 149.87, 'label': '6.7', 'name': '6.7 Depo zbirke paleoflore'},
    {'x': 67.47, 'y': 48.76, 'area_m2': 22.00, 'label': '3.11', 'name': '3.11 Malakološki depo'},
    {'x': 8.95, 'y': 57.65, 'area_m2': 155.00, 'label': '8.1', 'name': '8.1 Depoi / zbirke otvoreni za publiku'},
    {'x': 24.78, 'y': 56.54, 'area_m2': 164.98, 'label': '2.1', 'name': '2.1 Prijemni prostor za kičmenjake H=5m'},
    {'x': 45.03, 'y': 52.27, 'area_m2': 78.91, 'label': '3.6', 'name': '3.6 Suva ihtiološka zbirka'},
    {'x': 52.22, 'y': 52.27, 'area_m2': 116.78, 'label': '3.5', 'name': '3.5 Zbirke eksponata sisara'},
    {'x': 58.99, 'y': 52.27, 'area_m2': 99.42, 'label': '3.3', 'name': '3.3 Studijske zbirke sisara'},
    {'x': 66.14, 'y': 52.35, 'area_m2': 102.58, 'label': '3.2', 'name': '3.2 Zbirka egzotičnih sisara'},
    {'x': 72.98, 'y': 57.87, 'area_m2': 89.47, 'label': '6.1', 'name': '6.1 Zbirka lovačkog oružja i pribora i lovačkih trofeja'},
    {'x': 81.81, 'y': 55.71, 'area_m2': 183.94, 'label': '3.1', 'name': '3.1 Entomološki depo'},
    {'x': 93.83, 'y': 50.77, 'area_m2': 390.75, 'label': '3.9', 'name': '3.9 Ornitološki depo'},
    {'x': 17.80, 'y': 60.69, 'area_m2': 23.63, 'label': '2.6', 'name': '2.6 Sala za anoksiju'},
    {'x': 27.53, 'y': 61.91, 'area_m2': 45.00, 'label': '2.3', 'name': '2.3 Hladnjača velika'},
    {'x': 33.98, 'y': 61.20, 'area_m2': 55.12, 'label': '2.2', 'name': '2.2 Depo hladnjače'},
    {'x': 36.51, 'y': 58.27, 'area_m2': 30.83, 'label': '2.7', 'name': '2.7 Kupatilo'},
    {'x': 73.01, 'y': 60.75, 'area_m2': 34.31, 'label': 'Radne sobe bio', 'name': 'Radne sobe za bio depoe'},
    {'x': 77.94, 'y': 60.75, 'area_m2': 17.16, 'label': 'Ent. radionica', 'name': 'Entomološka radionica'},
    {'x': 81.29, 'y': 60.80, 'area_m2': 17.16, 'label': 'Prostorija za rad', 'name': 'Prostorija za rad'},
    {'x': 85.46, 'y': 60.75, 'area_m2': 24.19, 'label': 'Ent. lab', 'name': 'Entomološka laboratorija'},
    {'x': 8.58, 'y': 72.27, 'area_m2': 113.45, 'label': 'Depoi/zbirke', 'name': 'Depoi / zbirke otvoreni za publiku'},
    {'x': 17.83, 'y': 72.02, 'area_m2': 38.43, 'label': 'Molekularna lab', 'name': 'Molekularna laboratorija'},
    {'x': 24.42, 'y': 70.76, 'area_m2': 74.26, 'label': '7.1', 'name': '7.1 Koridor'},
    {'x': 31.84, 'y': 70.76, 'area_m2': 45.75, 'label': '3.10', 'name': '3.10 Herpetološki depo suve zbirke'},
    {'x': 50.23, 'y': 70.48, 'area_m2': 300.09, 'label': '3.7', 'name': '3.7 Herbarijum H=5m'},
    {'x': 71.38, 'y': 70.86, 'area_m2': 33.85, 'label': 'Radne sobe herbar.', 'name': 'Radne sobe za herbar. mat.'},
    {'x': 74.86, 'y': 71.93, 'area_m2': 21.96, 'label': 'Radna mikološka', 'name': 'Radna mikološka soba'},
    {'x': 79.33, 'y': 71.93, 'area_m2': 55.81, 'label': '3.8', 'name': '3.8 Fungarijum'},
    {'x': 85.07, 'y': 71.95, 'area_m2': 33.85, 'label': 'Mikološka lab', 'name': 'Mikološka laboratorija'},
]
PROJECT_AUTO_LAYOUT_VERSION = 6
PROJECT_SPACE_PLAN_VIEWS = [
    {'key': 'left', 'label': 'Parking + izložbeni', 'x': 0.0, 'y': 0.0, 'width': 64.9, 'height': 100.0},
    {
        'key': 'depot',
        'label': 'Depoi i laboratorije',
        'x': 0.0,
        'y': 0.0,
        'width': 100.0,
        'height': 100.0,
        'plan_image': PROJECT_SPACE_DEPOT_PLAN_FILE,
        'plan_image_size': PROJECT_SPACE_DEPOT_PLAN_IMAGE_SIZE,
        'area_annotations': PROJECT_DEPOT_PLAN_AREA_ANNOTATIONS,
    },
]
PROJECT_SPACE_LIBRARY = {
    'circulation': {
        'label': 'Комуникација / ходник',
        'keywords': ['ходник', 'комуникација', 'рампа', 'предпростор', 'лоби'],
        'suggestions': {
            'purpose': ['Кретање запослених и транспорт музејске грађе', 'Контролисана комуникација између лабораторија и депоа'],
            'floor_materials': ['епоксидни под', 'терацо', 'противклизна керамика', 'антистатички винил'],
            'wall_materials': ['перива боја', 'HPL заштитни панели', 'керамичка сокла', 'ударно отпорне облоге'],
            'ventilation': ['доводно-одводна вентилација', 'надпритисак у чистим зонама', 'детекција дима'],
            'equipment': ['сигнализација', 'контрола приступа', 'колица за транспорт', 'заштитни браници'],
            'utilities': ['LED расвета', 'противпожарни сензори', 'видео надзор'],
        },
    },
    'specimen_storage': {
        'label': 'Депо / складиште збирки',
        'keywords': ['депо', 'складиште', 'збирка', 'ormar', 'regal'],
        'suggestions': {
            'purpose': ['Смештај збирки у контролисаним микроклиматским условима', 'Карантин и привремено одлагање материјала'],
            'floor_materials': ['епоксидни под са заптивком', 'PU под отпоран на хемикалије', 'антистатички премаз'],
            'wall_materials': ['глатка перива боја', 'PVC зидна заштита', 'панели отпорни на влагу'],
            'ventilation': ['контрола температуре и релативне влажности', 'филтрирани довод ваздуха', '24/7 мониторинг микроклиме'],
            'equipment': ['компактни регали', 'ormari за влажне препарате', 'даталогери', 'дехумидификатор'],
            'utilities': ['резервно напајање', 'аларм за влагу', 'RFID/баркод инфраструктура'],
        },
    },
    'wet_lab': {
        'label': 'Мокра лабораторија',
        'keywords': ['мокра лабораторија', 'washing', 'sample prep', 'wet lab'],
        'suggestions': {
            'purpose': ['Прање, припрема и конзервација узорака', 'Рад са течностима и реагенсима'],
            'floor_materials': ['хемијски отпоран епоксид', 'PU под са сливником', 'противклизни индустријски под'],
            'wall_materials': ['киселоотпорна керамика', 'епоксидни зидни премаз', 'периви санитарни панели'],
            'ventilation': ['локална издувна вентилација', 'digestor', 'негативан притисак'],
            'equipment': ['лаб столови са судопером', 'digestor', 'ormar за реагенсе', 'станица за испирање очију'],
            'utilities': ['деминерализована вода', 'компримован ваздух', 'канализација за техничку воду'],
        },
    },
    'dry_lab': {
        'label': 'Сува лабораторија',
        'keywords': ['сува лабораторија', 'микроскопија', 'аналитика'],
        'suggestions': {
            'purpose': ['Микроскопија, аналитика и документација узорака', 'Рад без слободних течности'],
            'floor_materials': ['антистатички винил', 'епоксидни под', 'гумирани технички под'],
            'wall_materials': ['мат перива боја', 'акустични панели', 'HPL облоге'],
            'ventilation': ['комфорна HVAC вентилација', 'HEPA филтрација по потреби', 'стабилна температура'],
            'equipment': ['микроскопи', 'радне станице', 'фотографски сто', 'ormar за инструменте'],
            'utilities': ['UPS напајање', 'data priključci', 'контролисана расвета'],
        },
    },
    'conservation_lab': {
        'label': 'Конзерваторска лабораторија',
        'keywords': ['конзервација', 'рестаураторска лабораторија'],
        'suggestions': {
            'purpose': ['Конзервација и стабилизација музејских предмета', 'Прецизни третмани и документација стања'],
            'floor_materials': ['епоксидни антистатички под', 'vinyl seamless floor'],
            'wall_materials': ['перива боја без VOC', 'панели отпорни на хемикалије'],
            'ventilation': ['локална екстракција испарења', 'контрола VOC', 'систем филтрације честица'],
            'equipment': ['конзерваторски столови', 'лупе и микроскопи', 'ormar za hemikalije', 'UV/IR лампе'],
            'utilities': ['прецизна LED rasveta', 'дестилована вода', 'UPS'],
        },
    },
    'cold_room': {
        'label': 'Хладна комора / freeze room',
        'keywords': ['хладна комора', 'freeze', 'cold storage'],
        'suggestions': {
            'purpose': ['Привремено или трајно складиштење осетљивих узорака на ниској температури'],
            'floor_materials': ['термоизолациони подни панели', 'противклизна inox rešetka'],
            'wall_materials': ['термоизолациони панели', 'парна брана'],
            'ventilation': ['расхладни систем са alarmом', 'контрола кондензације', 'резервна вентилација'],
            'equipment': ['rashladne komore', 'даталогери температуре', 'алармni sistem'],
            'utilities': ['резервно напајање', 'дренажа кондензата'],
        },
    },
    'chemical_storage': {
        'label': 'Хемијско складиште',
        'keywords': ['хемикалије', 'растварачи', 'опасне материје'],
        'suggestions': {
            'purpose': ['Безбедно складиштење реагенаса и запаљивих материја', 'Одвојене зоне по класи опасности'],
            'floor_materials': ['киселоотпорни епоксид', 'хемијски отпоран премаз са kadicom'],
            'wall_materials': ['епоксидни премаз', 'vatrootporni paneli'],
            'ventilation': ['24h издувна вентилација', 'ATEX опрема по потреби', 'детекција испарења'],
            'equipment': ['ormari za zapaljive materije', 'sekundarne kadice', 'detektori curenja'],
            'utilities': ['противпожарни систем', 'уземљење', 'alarm za gasove'],
        },
    },
    'technical_room': {
        'label': 'Техничка просторија',
        'keywords': ['техничка просторија', 'машинска соба', 'service room'],
        'suggestions': {
            'purpose': ['Смештај техничких инсталација и управљања системима објекта'],
            'floor_materials': ['индустријски епоксид', 'бетон са премазом против прашења'],
            'wall_materials': ['перива техничка боја', 'ватроотпорне облоге'],
            'ventilation': ['присилна вентилација техничког простора', 'одвођење топлоте опреме'],
            'equipment': ['ormari automatike', 'BMS paneli', 'rezervne pumpe', 'мерни ормани'],
            'utilities': ['трофазно напајање', 'кабловске полице', 'service outlets'],
        },
    },
    'hvac_room': {
        'label': 'Вентилациона комора / HVAC',
        'keywords': ['HVAC', 'вентилациона комора', 'klima komora'],
        'suggestions': {
            'purpose': ['Припрема и дистрибуција ваздуха за лабораторије и депое', 'Контрола притисака по зонама'],
            'floor_materials': ['бетон са индустријским премазом', 'антивибрациона подлога'],
            'wall_materials': ['акустични панели', 'ватроотпорна облога'],
            'ventilation': ['AHU са филтрацијом', 'HEPA секција', 'рекуперација топлоте', 'контрола притиска'],
            'equipment': ['AHU', 'ventilatori', 'kanalski grejači', 'ovlaživači/dehumidifiers'],
            'utilities': ['BMS интеграција', 'кондензат одвод', 'service platforme'],
        },
    },
    'garage': {
        'label': 'Гаража / сервисни паркинг',
        'keywords': ['гаража', 'паркинг', 'доставно'],
        'suggestions': {
            'purpose': ['Сервисни приступ, истовар и паркирање службених возила'],
            'floor_materials': ['armirani beton sa tvrdim posipom', 'epoxy traffic coating'],
            'wall_materials': ['перива боја високе отпорности', 'ударне заштите'],
            'ventilation': ['CO детекција', 'jet ventilation', 'димoодвођење'],
            'equipment': ['роло врата', 'пунионица за електро возила', 'рампе', 'заштитни браници'],
            'utilities': ['hydrantska mreža', 'CO senzori', 'pranje poda'],
        },
    },
    'workshop': {
        'label': 'Радионица / припрема',
        'keywords': ['радионица', 'prep room', 'service workshop'],
        'suggestions': {
            'purpose': ['Припрема изложбених елемената и техничка подршка лабораторијама'],
            'floor_materials': ['епоксидни индустријски под', 'гумирани технички под'],
            'wall_materials': ['OSB/HPL заштитне облоге', 'перива боја'],
            'ventilation': ['локално одвођење прашине', 'вентилација алата', 'довољна измена ваздуха'],
            'equipment': ['радни столови', 'ormar za alat', 'aspiracija', 'компресорска линија'],
            'utilities': ['трофазно напајање', 'компримован ваздух', 'tehnička rasveta'],
        },
    },
    'office_support': {
        'label': 'Канцеларија / support',
        'keywords': ['канцеларија', 'support', 'оператер'],
        'suggestions': {
            'purpose': ['Оперативна подршка раду лабораторија и депоа', 'Административна припрема и евиденција'],
            'floor_materials': ['vinyl', 'tepih ploče', 'laminat za komercijalnu upotrebu'],
            'wall_materials': ['перива боја', 'akustični paneli'],
            'ventilation': ['комфорна вентилација', 'fresh air supply', 'контрола CO2'],
            'equipment': ['радне станице', 'ormari za dokumentaciju', 'etiketirke', 'printer/skener'],
            'utilities': ['LAN priključci', 'UPS за ИТ опрему', 'контролисана rasveta'],
        },
    },
}
PROJECT_COMMON_TERMS = {
    'purpose': ['чиста зона', 'прљава зона', 'карантин', 'пријем узорака', 'обрада материјала', 'контролисан приступ'],
    'floor_materials': ['епоксидни под', 'PU под', 'терацо', 'керамика', 'антистатички винил', 'бетон са премазом'],
    'wall_materials': ['перива боја', 'епоксидни премаз', 'HPL панели', 'керамичка облога', 'ватроотпорни панели'],
    'ventilation': ['HEPA филтрација', 'негативан притисак', 'надпритисак', 'рекуперација', 'локална екстракција', 'контрола влажности'],
    'equipment': ['radni sto', 'sudopera', 'digestor', 'ormar za hemikalije', 'regali', 'mikroskopi', 'BMS panel'],
    'utilities': ['UPS', 'трофазно напајање', 'data priključci', 'дестилована вода', 'компримован ваздух', 'сливник'],
}

# ---------------------------------------------------------------------------
# Curator auto-assignment: keyword patterns → curator name
# Each rule is (keywords_in_name_or_purpose, curator_full_name).
# First matching rule wins; order = most specific first.
# ---------------------------------------------------------------------------
_ROOM_CURATOR_RULES = [
    # Geology — minerals & meteorites
    (['mineral', 'метеорит', 'минерал'],
     'Александар Луковић'),
    # Geology — petrology
    (['petrolo', 'петроло', 'стенск'],
     'Татјана Милић Бабић'),
    # Geology — paleoflora / paleobotany
    (['paleoflor', 'палеофлор', 'палеобот', 'окамењено дрвеће', 'фосилизован.*флор', 'отисци биљака'],
     'Деса Ђорђевић-Милутиновић'),
    # Geology — fossilized invertebrates (beskičmenjaci)
    (['beskičmenjak', 'бескичмењак', 'фосилизован.*бескичмењ'],
     'Биљана Митровић'),
    # Geology — conservation workshop
    (['geološk.*konzerv', 'геолошк.*конзерв', 'konzerv.*radion', 'конзерв.*радион',
      'конзервација.*геолошк', 'конзервација.*палеонтолошк', 'стабилизација.*музејск'],
     'Ненад Младеновић'),
    # Biology — ichthyology
    (['ihtiolo', 'ихтиоло'],
     'Дубравка Вучић'),
    # Biology — entomology depot/lab
    (['entomolo.*labor', 'ентомоло.*лаб', 'entomolo.*depo', 'ентомоло.*депо',
      'ентомолошк.*збирк', 'инсект'],
     'Милош Јовић'),
    # Biology — entomology workshop / conservation
    (['entomolo.*radion', 'ентомоло.*радион', 'препарирање.*инсек',
      'конзерватор.*ентомол'],
     'Александар Стојановић'),
    # Biology — ornithology
    (['ornitolo', 'орнитоло', 'птиц', 'перје', 'јаја'],
     'Вук Попић'),
    # Biology — herpetology
    (['herpetolo', 'херпетоло', 'гмизав', 'водоземац'],
     'Ана Пауновић'),
    # Biology — mycology (fungarium, lab, work room)
    (['mikolo', 'миколо', 'fungarij', 'фунгариј', 'гљив'],
     'Борис Иванчевић'),
    # Biology — herbarium
    (['herbar', 'хербар'],
     'Марјан Никетић'),
    # Biology — mammals (sisari)
    (['sisar', 'сисар', 'дермопласт', 'крзн', 'лобањ'],
     'Верица Стојановић'),
    # Biology — malacology (modern mollusks)
    (['malakolo', 'малаколо', 'мекушц', 'шкољк', 'пужев'],
     'Биљана Митровић'),
    # Biology — molecular lab
    (['molekular', 'молекулар', 'ДНК', 'PCR', 'електрофореза'],
     'Зорана Марковић'),
    # Shared biology workrooms
    (['radne sobe za bio', 'радне собе.*био', 'обрада биолошк'],
     'Верица Стојановић'),
    # Hunting collection
    (['lovačk', 'ловачк', 'oružj', 'оружј', 'трофеј'],
     'Верица Стојановић'),
    # Public-facing depots — director oversight
    (['otvoreni za publiku', 'отворен.*публик', 'видљиви депо'],
     'Славко Спасић'),
    # Cold rooms / anoxia — shared conservation
    (['hladnjač', 'хладњач', 'hladna komora', 'хладна комора', 'анокси', 'anoksij'],
     'Горана Петковски'),
    # Reception / intake of specimens
    (['prijemni', 'пријемн', 'тријаж'],
     'Горана Петковски'),
    # Geology — fossilized vertebrates (kičmenjaci) — after prijemni to avoid matching intake rooms
    (['kičmenjak', 'кичмењак', 'фосилизован.*кичмењ', 'диносаурус'],
     'Зоран Марковић'),
]


def _assign_curator_for_space(space):
    """Return curator name based on room name and purpose keyword matching."""
    import re
    name = (space.get('name') or '').lower()
    specs = space.get('specs') or {}
    purpose = (specs.get('purpose') or '').lower()
    search_text = name + ' ' + purpose

    for keywords, curator_name in _ROOM_CURATOR_RULES:
        for kw in keywords:
            if re.search(kw.lower(), search_text):
                return curator_name
    return ''


PROJECT_DEPOT_AUTO_DETECTED_SPACES = [
    {'id': 'depot-6.8', 'name': '6.8 Depo fosilizovanih kičmenjaka', 'room_type': 'specimen_storage', 'area_m2': 247.32, 'x': 22.21, 'y': 31.0, 'width': 6.35, 'height': 8.98,
     'specs': {'purpose': 'Чување фосилизованих кичмењака — контролисана температура и влажност', 'floor_materials': 'Епоксидни под са заптивком', 'wall_materials': 'Глатка перива боја, PVC зидна заштита', 'ventilation': 'Контрола температуре и релативне влажности, 24/7 мониторинг микроклиме', 'equipment': 'Компактни регали, даталогери, дехумидификатор', 'utilities': 'Резервно напајање, аларм за влагу, RFID инфраструктура'}},
    {'id': 'depot-6.9.1-12', 'name': '6.9.1 Konzerv. radion. 1 i 2', 'room_type': 'conservation_lab', 'area_m2': 37.9, 'x': 38.59, 'y': 30.83, 'width': 3.51, 'height': 9.15,
     'specs': {'purpose': 'Конзервација и стабилизација геолошких и палеонтолошких узорака', 'floor_materials': 'Епоксидни антистатички под', 'wall_materials': 'Перива боја без VOC, панели отпорни на хемикалије', 'ventilation': 'Локална екстракција испарења, контрола VOC', 'equipment': 'Конзерваторски столови, лупе и микроскопи, ormar za hemikalije', 'utilities': 'Прецизна LED расвета, дестилована вода, UPS'}},
    {'id': 'depot-6.6', 'name': '6.6 Depo fosilizovanih beskičmenjaka', 'room_type': 'specimen_storage', 'area_m2': 192.33, 'x': 49.26, 'y': 30.83, 'width': 6.59, 'height': 9.15,
     'specs': {'purpose': 'Чување фосилизованих бескичмењака у контролисаним условима', 'floor_materials': 'Епоксидни под са заптивком', 'wall_materials': 'Глатка перива боја, PVC зидна заштита', 'ventilation': 'Контрола температуре и релативне влажности, филтрирани довод ваздуха', 'equipment': 'Компактни регали, фиоке за фосиле, даталогери', 'utilities': 'Резервно напајање, аларм за влагу'}},
    {'id': 'depot-6.4', 'name': '6.4 Depo minerala i meteorita', 'room_type': 'specimen_storage', 'area_m2': 194.27, 'x': 62.8, 'y': 30.83, 'width': 6.59, 'height': 9.15,
     'specs': {'purpose': 'Чување збирке минерала и метеорита — стабилна температура, ниска влажност', 'floor_materials': 'Антистатички епоксидни под', 'wall_materials': 'Глатка перива боја, панели отпорни на влагу', 'ventilation': 'Контрола температуре (18–22°C) и влажности (40–50% RH), 24/7 мониторинг', 'equipment': 'Специјализовани ормари за минерале, компактни регали, даталогери, UV-филтер расвета', 'utilities': 'Резервно напајање, аларм за влагу, RFID/баркод инфраструктура'}},
    {'id': 'depot-6.9.1-34', 'name': '6.9.1 Konzerv. radion. 3 i 4', 'room_type': 'conservation_lab', 'area_m2': 37.9, 'x': 74.04, 'y': 30.83, 'width': 2.75, 'height': 9.15,
     'specs': {'purpose': 'Конзервација и стабилизација музејских предмета', 'floor_materials': 'Епоксидни антистатички под', 'wall_materials': 'Перива боја без VOC, панели отпорни на хемикалије', 'ventilation': 'Локална екстракција испарења, контрола VOC', 'equipment': 'Конзерваторски столови, лупе и микроскопи, UV/IR лампе', 'utilities': 'Прецизна LED расвета, дестилована вода, UPS'}},
    {'id': 'depot-6.5', 'name': '6.5 Depo petrološke zbirke', 'room_type': 'specimen_storage', 'area_m2': 265.87, 'x': 77.2, 'y': 22.5, 'width': 12.4, 'height': 17.4,
     'specs': {'purpose': 'Чување петролошке збирке — стенски узорци, препарати и тежи примерци', 'floor_materials': 'Ојачани епоксидни под (велико оптерећење)', 'wall_materials': 'Глатка перива боја, PVC зидна заштита', 'ventilation': 'Контрола температуре и влажности, филтрирани довод ваздуха', 'equipment': 'Тешки регали за стенске узорке, компактни ормари, палете, колица', 'utilities': 'Резервно напајање, аларм за влагу'}},
    {'id': 'depot-2.4', 'name': '2.4 Geološka konzervatorska radionica', 'room_type': 'conservation_lab', 'area_m2': 50.88, 'x': 10.5, 'y': 43.2, 'width': 4.7, 'height': 6.3,
     'specs': {'purpose': 'Конзервација геолошких узорака — препарација, лепљење, стабилизација', 'floor_materials': 'Хемијски отпоран епоксид', 'wall_materials': 'Перива боја без VOC, епоксидни зидни премаз', 'ventilation': 'Локална екстракција прашине и испарења, digestor', 'equipment': 'Конзерваторски столови, брусилица, орман за алат и хемикалије, лупе', 'utilities': 'Компримован ваздух, дестилована вода, UPS, технички прикључци'}},
    {'id': 'depot-8.2', 'name': '8.2 Mokra ihtiološka zbirka', 'room_type': 'wet_lab', 'area_m2': 38.77, 'x': 33.58, 'y': 43.22, 'width': 5.77, 'height': 6.33,
     'specs': {'purpose': 'Чување ихтиолошких препарата у течном конзервансу (алкохол, формалин)', 'floor_materials': 'Хемијски отпоран епоксид са сливником', 'wall_materials': 'Киселоотпорна керамика, епоксидни зидни премаз', 'ventilation': 'Локална издувна вентилација, негативан притисак, детекција испарења', 'equipment': 'Стаклене посуде за мокре препарате, регали од нерђајућег челика, станица за испирање очију', 'utilities': 'Деминерализована вода, канализација за техничку воду, вентилација хазмат'}},
    {'id': 'depot-6.7', 'name': '6.7 Depo zbirke paleoflore', 'room_type': 'specimen_storage', 'area_m2': 149.87, 'x': 49.26, 'y': 43.2, 'width': 6.59, 'height': 6.33,
     'specs': {'purpose': 'Чување фосилизоване флоре — отисци биљака и окамењено дрвеће', 'floor_materials': 'Епоксидни под са заптивком', 'wall_materials': 'Глатка перива боја, PVC зидна заштита', 'ventilation': 'Контрола температуре и влажности, филтрирани довод ваздуха', 'equipment': 'Компактни регали, фиоке за отиске, даталогери', 'utilities': 'Резервно напајање, аларм за влагу'}},
    {'id': 'depot-3.11', 'name': '3.11 Malakološki depo', 'room_type': 'specimen_storage', 'area_m2': 22.0, 'x': 65.97, 'y': 45.49, 'width': 3.26, 'height': 4.06,
     'specs': {'purpose': 'Чување малаколошке збирке — шкољке, пужеви, мекушци', 'floor_materials': 'Антистатички епоксидни под', 'wall_materials': 'Глатка перива боја', 'ventilation': 'Контрола влажности (45–55% RH), стабилна температура', 'equipment': 'Ормари са фиокама, силика-гел уметци, даталогери', 'utilities': 'Резервно напајање, аларм за влагу'}},
    {'id': 'depot-8.1', 'name': '8.1 Depoi / zbirke otvoreni za publiku', 'room_type': 'specimen_storage', 'area_m2': 155.0, 'x': 2.0, 'y': 43.2, 'width': 8.0, 'height': 22.0,
     'specs': {'purpose': 'Видљиви депо — отворен за публику, приказ збирки кроз стакло', 'floor_materials': 'Терацо или антистатички винил', 'wall_materials': 'Перива боја, стаклене преграде', 'ventilation': 'Комфорна HVAC вентилација, контрола CO2', 'equipment': 'Витрине, расвета са UV-филтером, информативни панели', 'utilities': 'LED расвета, видео надзор, противпожарни сензори'}},
    {'id': 'depot-2.1', 'name': '2.1 Prijemni prostor za kičmenjake', 'room_type': 'specimen_storage', 'area_m2': 164.98, 'x': 15.56, 'y': 50.11, 'width': 13.0, 'height': 9.15,
     'specs': {'purpose': 'Пријем, тријажа и привремено складиштење великих кичмењачких узорака', 'floor_materials': 'Ојачани епоксидни под (велико оптерећење)', 'wall_materials': 'Перива боја, ударно отпорне облоге', 'ventilation': 'Доводно-одводна вентилација, детекција дима', 'equipment': 'Велике палете, колица за транспорт, вага, привремени регали', 'utilities': 'Трофазно напајање, широка врата за утовар, контрола приступа'}},
    {'id': 'depot-3.6', 'name': '3.6 Suva ihtiološka zbirka', 'room_type': 'dry_lab', 'area_m2': 78.91, 'x': 42.64, 'y': 50.11, 'width': 5.17, 'height': 9.15,
     'specs': {'purpose': 'Чување сувих ихтиолошких препарата — скелети, крљушти, отолити', 'floor_materials': 'Антистатички винил', 'wall_materials': 'Мат перива боја', 'ventilation': 'Стабилна температура (18–22°C), контрола влажности (45–55% RH)', 'equipment': 'Ормари са фиокама, регали, даталогери', 'utilities': 'Резервно напајање, контролисана расвета'}},
    {'id': 'depot-3.5', 'name': '3.5 Zbirke eksponata sisara', 'room_type': 'specimen_storage', 'area_m2': 116.78, 'x': 49.26, 'y': 50.11, 'width': 6.59, 'height': 9.15,
     'specs': {'purpose': 'Чување препарираних сисара — дермопластика, крзна, лобање', 'floor_materials': 'Епоксидни под са заптивком', 'wall_materials': 'Глатка перива боја, PVC зидна заштита', 'ventilation': 'Контрола температуре и влажности, заштита од инсеката', 'equipment': 'Велики ормари за дермопластику, нафталинске замке, даталогери', 'utilities': 'Резервно напајање, аларм за влагу, видео надзор'}},
    {'id': 'depot-3.3', 'name': '3.3 Studijske zbirke sisara', 'room_type': 'specimen_storage', 'area_m2': 99.42, 'x': 56.03, 'y': 50.11, 'width': 6.59, 'height': 9.15,
     'specs': {'purpose': 'Студијска збирка сисара — лобање, скелети, козе за научна истраживања', 'floor_materials': 'Антистатички епоксидни под', 'wall_materials': 'Глатка перива боја', 'ventilation': 'Контрола температуре и влажности, филтрирани довод ваздуха', 'equipment': 'Компактни регали, фиоке за лобање, мерне станице', 'utilities': 'Резервно напајање, RFID/баркод инфраструктура'}},
    {'id': 'depot-3.2', 'name': '3.2 Zbirka egzotičnih sisara', 'room_type': 'specimen_storage', 'area_m2': 102.58, 'x': 62.8, 'y': 50.06, 'width': 6.59, 'height': 9.19,
     'specs': {'purpose': 'Чување препарираних егзотичних сисара — CITES документација обавезна', 'floor_materials': 'Епоксидни под са заптивком', 'wall_materials': 'Глатка перива боја, PVC зидна заштита', 'ventilation': 'Контрола температуре и влажности, заштита од инсеката', 'equipment': 'Велики ормари, дермопластике, нафталинске замке, даталогери', 'utilities': 'Резервно напајање, аларм за влагу, контрола приступа'}},
    {'id': 'depot-6.1', 'name': '6.1 Zbirka lovačkog oružja i pribora', 'room_type': 'specimen_storage', 'area_m2': 89.47, 'x': 69.57, 'y': 49.94, 'width': 6.47, 'height': 9.32,
     'specs': {'purpose': 'Чување ловачког оружја, трофеја и ловачког прибора', 'floor_materials': 'Епоксидни под', 'wall_materials': 'Перива боја, ударно отпорне облоге', 'ventilation': 'Контрола влажности (40–50% RH) — превенција корозије метала', 'equipment': 'Оружарски ормари (закључани), регали за трофеје, дехумидификатор', 'utilities': 'Безбедносни аларм, контрола приступа, видео надзор'}},
    {'id': 'depot-3.1', 'name': '3.1 Entomološki depo', 'room_type': 'specimen_storage', 'area_m2': 183.94, 'x': 76.43, 'y': 49.94, 'width': 6.5, 'height': 9.32,
     'specs': {'purpose': 'Чување ентомолошке збирке — инсекти у фиокама са нафталином/парадихлорбензолом', 'floor_materials': 'Антистатички епоксидни под', 'wall_materials': 'Глатка перива боја, заптивене фуге', 'ventilation': 'Контрола температуре (18–20°C) и влажности (40–50% RH), заштита од инсеката', 'equipment': 'Ентомолошки ормари са фиокама, пинсете, лупе, IPM замке', 'utilities': 'Резервно напајање, аларм за влагу, RFID инфраструктура'}},
    {'id': 'depot-3.9', 'name': '3.9 Ornitološki depo', 'room_type': 'specimen_storage', 'area_m2': 390.75, 'x': 90.0, 'y': 21.2, 'width': 6.5, 'height': 47.5,
     'specs': {'purpose': 'Чување орнитолошке збирке — препарирани примерци, јаја, перје', 'floor_materials': 'Антистатички епоксидни под', 'wall_materials': 'Глатка перива боја, заптивене фуге', 'ventilation': 'Контрола температуре (18–20°C) и влажности (45–55% RH), заштита од инсеката', 'equipment': 'Компактни регали, фиоке за студијске скинове, ормари за јаја, IPM замке', 'utilities': 'Резервно напајање, аларм за влагу, RFID/баркод инфраструктура'}},
    {'id': 'depot-2.6', 'name': '2.6 Sala za anoksiju', 'room_type': 'chemical_storage', 'area_m2': 23.63, 'x': 15.65, 'y': 59.81, 'width': 4.23, 'height': 5.13,
     'specs': {'purpose': 'Третман музејске грађе бескисеоничном атмосфером (анокси третман) — уништавање инсеката', 'floor_materials': 'Епоксидни под са заптивком', 'wall_materials': 'Херметички затворени панели, парна брана', 'ventilation': 'Затворени систем за анокси третман, детекција кисеоника, аларм за N₂', 'equipment': 'Анокси коморе, боце са азотом, детектори O₂, вакуум пумпе', 'utilities': 'Довод азота, UPS, безбедносни аларм'}},
    {'id': 'depot-2.3', 'name': '2.3 Hladnjača velika', 'room_type': 'cold_room', 'area_m2': 45.0, 'x': 22.21, 'y': 59.81, 'width': 6.35, 'height': 5.13,
     'specs': {'purpose': 'Велика хладна комора за привремено складиштење органских узорака на ниској температури', 'floor_materials': 'Термоизолациони подни панели, противклизна inox rešetka', 'wall_materials': 'Термоизолациони панели, парна брана', 'ventilation': 'Расхладни систем са алармом (-20°C до +4°C), контрола кондензације', 'equipment': 'Расхладне коморе, даталогери температуре, алармни систем', 'utilities': 'Резервно напајање, дренажа кондензата'}},
    {'id': 'depot-2.2', 'name': '2.2 Depo hladnjače', 'room_type': 'cold_room', 'area_m2': 55.12, 'x': 29.19, 'y': 59.81, 'width': 6.35, 'height': 5.13,
     'specs': {'purpose': 'Депо хладњаче — дугорочно хладно складиштење осетљивих биолошких узорака', 'floor_materials': 'Термоизолациони подни панели', 'wall_materials': 'Термоизолациони панели, парна брана', 'ventilation': 'Расхладни систем са алармом, контрола кондензације, резервна вентилација', 'equipment': 'Регали за хладно складиштење, даталогери', 'utilities': 'Резервно напајање, дренажа кондензата'}},
    {'id': 'depot-2.7', 'name': '2.7 Kupatilo', 'room_type': 'technical_room', 'area_m2': 30.83, 'x': 33.58, 'y': 54.3, 'width': 5.77, 'height': 4.96,
     'specs': {'purpose': 'Санитарни чвор за запослене у зони депоа и лабораторија', 'floor_materials': 'Противклизна керамика', 'wall_materials': 'Керамичка облога, санитарни панели', 'ventilation': 'Издувна вентилација, негативан притисак', 'equipment': 'Санитарна опрема, тушеви за декотаминацију', 'utilities': 'Топла/хладна вода, канализација'}},
    {'id': 'depot-radne-bio', 'name': 'Radne sobe za bio depoe', 'room_type': 'dry_lab', 'area_m2': 34.31, 'x': 69.78, 'y': 59.81, 'width': 6.26, 'height': 5.13,
     'specs': {'purpose': 'Радне собе за обраду биолошких узорака — сортирање, етикетирање, документација', 'floor_materials': 'Антистатички винил', 'wall_materials': 'Мат перива боја', 'ventilation': 'Комфорна HVAC вентилација, контрола CO2', 'equipment': 'Радне станице, микроскопи, фотографски сто, ormar za instrumente', 'utilities': 'UPS напајање, LAN прикључци, контролисана расвета'}},
    {'id': 'depot-ent-rad', 'name': 'Entomološka radionica', 'room_type': 'workshop', 'area_m2': 17.16, 'x': 76.43, 'y': 59.81, 'width': 3.05, 'height': 5.13,
     'specs': {'purpose': 'Припрема ентомолошких препарата — препарирање, распростирање, етикетирање инсеката', 'floor_materials': 'Антистатички винил', 'wall_materials': 'Мат перива боја', 'ventilation': 'Локално одвођење прашине, довољна измена ваздуха', 'equipment': 'Радни столови за ентомологију, пинсете, микроскопи, лампе, распростирачи', 'utilities': 'Прецизна LED расвета, UPS'}},
    {'id': 'depot-prost-rad', 'name': 'Prostorija za rad', 'room_type': 'office_support', 'area_m2': 17.16, 'x': 79.66, 'y': 59.81, 'width': 3.02, 'height': 5.13,
     'specs': {'purpose': 'Канцеларијска подршка раду лабораторија и депоа', 'floor_materials': 'Ламинат или винил', 'wall_materials': 'Перива боја', 'ventilation': 'Комфорна вентилација, контрола CO2', 'equipment': 'Радне станице, ормари за документацију, printer/skener', 'utilities': 'LAN прикључци, UPS за ИТ опрему'}},
    {'id': 'depot-ent-lab', 'name': 'Entomološka laboratorija', 'room_type': 'dry_lab', 'area_m2': 24.19, 'x': 83.32, 'y': 59.81, 'width': 4.35, 'height': 5.13,
     'specs': {'purpose': 'Лабораторија за ентомолошка истраживања — детерминација, морфометрија, фотографија', 'floor_materials': 'Антистатички винил', 'wall_materials': 'Мат перива боја, акустични панели', 'ventilation': 'Комфорна HVAC вентилација, HEPA филтрација по потреби', 'equipment': 'Стереомикроскопи, фотографски сто, радне станице, ormar za instrumente', 'utilities': 'UPS напајање, data прикључци, контролисана расвета'}},
    {'id': 'depot-depoi-pub', 'name': 'Depoi / zbirke otvoreni za publiku', 'room_type': 'specimen_storage', 'area_m2': 113.45, 'x': 2.0, 'y': 69.4, 'width': 13.2, 'height': 8.5,
     'specs': {'purpose': 'Видљиви депо — отворен за публику, приказ збирки кроз стакло', 'floor_materials': 'Терацо или антистатички винил', 'wall_materials': 'Перива боја, стаклене преграде', 'ventilation': 'Комфорна HVAC вентилација, контрола CO2', 'equipment': 'Витрине, расвета са UV-филтером, информативни панели', 'utilities': 'LED расвета, видео надзор, противпожарни сензори'}},
    {'id': 'depot-mol-lab', 'name': 'Molekularna laboratorija', 'room_type': 'wet_lab', 'area_m2': 38.43, 'x': 15.65, 'y': 69.39, 'width': 4.23, 'height': 8.51,
     'specs': {'purpose': 'Молекуларна анализа — екстракција ДНК/РНК, PCR, електрофореза', 'floor_materials': 'Хемијски отпоран епоксид, антистатички', 'wall_materials': 'Епоксидни зидни премаз, периви санитарни панели', 'ventilation': 'HEPA филтрација, позитиван/негативан притисак по зонама, ламинарни кабинет', 'equipment': 'PCR апарат, центрифуге, ламинарни кабинет, фрижидер -20°C/-80°C, електрофореза', 'utilities': 'UPS, деминерализована вода, медицински гас, LAN'}},
    {'id': 'depot-7.1', 'name': '7.1 Koridor', 'room_type': 'circulation', 'area_m2': 74.26, 'x': 22.21, 'y': 69.39, 'width': 6.56, 'height': 8.51,
     'specs': {'purpose': 'Кретање запослених и транспорт музејске грађе између депоа', 'floor_materials': 'Епоксидни под, противклизни', 'wall_materials': 'Перива боја, HPL заштитни панели, ударно отпорне облоге', 'ventilation': 'Доводно-одводна вентилација, детекција дима', 'equipment': 'Сигнализација, контрола приступа, колица за транспорт', 'utilities': 'LED расвета, противпожарни сензори, видео надзор'}},
    {'id': 'depot-3.10', 'name': '3.10 Herpetološki depo suve zbirke', 'room_type': 'specimen_storage', 'area_m2': 45.75, 'x': 29.19, 'y': 69.39, 'width': 5.08, 'height': 8.51,
     'specs': {'purpose': 'Чување херпетолошких сувих препарата — гмизавци, водоземци', 'floor_materials': 'Антистатички епоксидни под', 'wall_materials': 'Глатка перива боја', 'ventilation': 'Контрола температуре (18–22°C) и влажности (45–55% RH)', 'equipment': 'Ормари са фиокама, регали, даталогери, IPM замке', 'utilities': 'Резервно напајање, аларм за влагу'}},
    {'id': 'depot-3.7', 'name': '3.7 Herbarijum H=5m', 'room_type': 'specimen_storage', 'area_m2': 300.09, 'x': 35.7, 'y': 69.4, 'width': 27.0, 'height': 8.5,
     'specs': {'purpose': 'Хербаријум висине 5 метара — чување херб. листова, компактни регали', 'floor_materials': 'Ојачани епоксидни под (оптерећење компактних регала)', 'wall_materials': 'Глатка перива боја, заптивене фуге', 'ventilation': 'Контрола температуре (18–20°C) и влажности (40–50% RH), заштита од инсеката', 'equipment': 'Компактни регали висине 5m са подвижним мердевинама, IPM замке, даталогери', 'utilities': 'Резервно напајање, аларм за влагу, RFID инфраструктура'}},
    {'id': 'depot-radne-herb', 'name': 'Radne sobe za herbar. mat.', 'room_type': 'dry_lab', 'area_m2': 33.85, 'x': 69.36, 'y': 69.26, 'width': 3.93, 'height': 8.68,
     'specs': {'purpose': 'Обрада хербаријумског материјала — монтирање, етикетирање, дигитализација', 'floor_materials': 'Антистатички винил', 'wall_materials': 'Мат перива боја', 'ventilation': 'Комфорна HVAC вентилација', 'equipment': 'Радни столови, пресе за биљке, скенер за дигитализацију, микроскопи', 'utilities': 'LAN прикључци, UPS, контролисана расвета'}},
    {'id': 'depot-mikol-soba', 'name': 'Radna mikološka soba', 'room_type': 'dry_lab', 'area_m2': 21.96, 'x': 73.71, 'y': 69.39, 'width': 2.45, 'height': 5.43,
     'specs': {'purpose': 'Обрада миколошких узорака — сушење, детерминација, микроскопија гљива', 'floor_materials': 'Антистатички винил', 'wall_materials': 'Мат перива боја', 'ventilation': 'Комфорна вентилација, контрола влажности', 'equipment': 'Микроскопи, сушара, радни сто, орман за инструменте', 'utilities': 'UPS, контролисана расвета'}},
    {'id': 'depot-3.8', 'name': '3.8 Fungarijum', 'room_type': 'specimen_storage', 'area_m2': 55.81, 'x': 76.34, 'y': 69.39, 'width': 6.44, 'height': 8.51,
     'specs': {'purpose': 'Чување миколошке збирке — сушени примерци гљива у затвореним ормарима', 'floor_materials': 'Антистатички епоксидни под', 'wall_materials': 'Глатка перива боја, заптивене фуге', 'ventilation': 'Контрола температуре (18–20°C) и влажности (40–50% RH), заштита од инсеката', 'equipment': 'Ормари за фунгаријум, силика-гел, IPM замке, даталогери', 'utilities': 'Резервно напајање, аларм за влагу'}},
    {'id': 'depot-mikol-lab', 'name': 'Mikološka laboratorija', 'room_type': 'wet_lab', 'area_m2': 33.85, 'x': 83.32, 'y': 69.39, 'width': 3.72, 'height': 8.51,
     'specs': {'purpose': 'Миколошка лабораторија — култивација, микроскопија и препарација гљива', 'floor_materials': 'Хемијски отпоран епоксид', 'wall_materials': 'Епоксидни зидни премаз, периви санитарни панели', 'ventilation': 'Ламинарни кабинет, локална издувна вентилација', 'equipment': 'Ламинарни кабинет, микроскопи, аутоклав, термостат/инкубатор', 'utilities': 'Деминерализована вода, UPS, компримован ваздух'}},
]
PROJECT_AUTO_DETECTED_SPACES = [
    {'id': 'auto-g1', 'name': 'G1 Kolska rampa', 'room_type': 'garage', 'x': 1400, 'y': 1045, 'width': 710, 'height': 285, 'unit': 'px', 'area_m2': 45.5},
    {'id': 'auto-g2', 'name': 'G2 Kolska rampa', 'room_type': 'garage', 'x': 2365, 'y': 1040, 'width': 715, 'height': 290, 'unit': 'px', 'area_m2': 46.6},
    {'id': 'auto-g3', 'name': 'G3 Parking', 'room_type': 'garage', 'x': 470, 'y': 120, 'width': 2420, 'height': 985, 'unit': 'px', 'area_m2': 535.4},
    {'id': 'auto-g4', 'name': 'G4 Tehnika', 'room_type': 'technical_room', 'x': 2080, 'y': 1045, 'width': 500, 'height': 275, 'unit': 'px', 'area_m2': 30.9},
    {'id': 'auto-g5', 'name': 'G5 Kolski prilaz za muzej', 'room_type': 'garage', 'x': 2835, 'y': 675, 'width': 310, 'height': 655, 'unit': 'px', 'area_m2': 45.6},
    {'id': 'auto-17', 'name': '1.7 Izložbeni prostor', 'room_type': 'circulation', 'x': 2975, 'y': 95, 'width': 2870, 'height': 1015, 'unit': 'px', 'area_m2': 655.0},
    {'id': 'auto-12', 'name': '12 Garderoba', 'room_type': 'office_support', 'x': 5850, 'y': 170, 'width': 535, 'height': 180, 'unit': 'px', 'area_m2': 21.6},
    {'id': 'auto-82', 'name': '8.2 Kuhinja restorana', 'room_type': 'office_support', 'x': 6515, 'y': 130, 'width': 260, 'height': 312, 'unit': 'px', 'area_m2': 38.77},
    {'id': 'auto-141', 'name': '1.4.1 Prodavnica suvenira', 'room_type': 'office_support', 'x': 6210, 'y': 455, 'width': 558, 'height': 169, 'unit': 'px', 'area_m2': 21.2},
    {'id': 'auto-16', 'name': '1.6 Amfiteatar', 'room_type': 'office_support', 'x': 6210, 'y': 630, 'width': 558, 'height': 450, 'unit': 'px', 'area_m2': 56.5},
    {'id': 'auto-15', 'name': '1.5 Nadzor', 'room_type': 'office_support', 'x': 5955, 'y': 820, 'width': 250, 'height': 245, 'unit': 'px', 'area_m2': 13.8},
    {'id': 'auto-81', 'name': '8.1 Hodnik kuhinje', 'room_type': 'circulation', 'x': 6775, 'y': 610, 'width': 105, 'height': 490, 'unit': 'px', 'area_m2': 155.0},
    {'id': 'auto-71', 'name': '7.1 Koridor depoa', 'room_type': 'circulation', 'x': 6170, 'y': 1085, 'width': 3225, 'height': 63, 'unit': 'px', 'area_m2': 74.26},
    {'id': 'auto-21', 'name': '2.1 Prijemni prostor za kičmenjake', 'room_type': 'specimen_storage', 'x': 6770, 'y': 805, 'width': 790, 'height': 275, 'unit': 'px', 'area_m2': 164.98},
    {'id': 'auto-22', 'name': '2.2 Depo hladnjače', 'room_type': 'cold_room', 'x': 6980, 'y': 1115, 'width': 700, 'height': 250, 'unit': 'px', 'area_m2': 55.12},
    {'id': 'auto-24', 'name': '2.4 Konzervatorska radionica', 'room_type': 'conservation_lab', 'x': 6520, 'y': 1115, 'width': 460, 'height': 250, 'unit': 'px', 'area_m2': 50.88},
    {'id': 'auto-26', 'name': '2.6 Sala za anoksiju', 'room_type': 'wet_lab', 'x': 7235, 'y': 640, 'width': 325, 'height': 165, 'unit': 'px', 'area_m2': 23.63},
    {'id': 'auto-610', 'name': '6.10 Herpetološke mokre zbirke', 'room_type': 'wet_lab', 'x': 7560, 'y': 805, 'width': 340, 'height': 95, 'unit': 'px', 'area_m2': 7.3},
    {'id': 'auto-27', 'name': '2.7 Kupatilo', 'room_type': 'wet_lab', 'x': 7560, 'y': 900, 'width': 340, 'height': 65, 'unit': 'px', 'area_m2': 30.83},
    {'id': 'auto-23', 'name': '2.3 Hladnjača velika', 'room_type': 'cold_room', 'x': 7560, 'y': 965, 'width': 340, 'height': 115, 'unit': 'px', 'area_m2': 45.0},
    {'id': 'auto-694', 'name': '6.94 Konzerv. radion. 4', 'room_type': 'conservation_lab', 'x': 6765, 'y': 640, 'width': 115, 'height': 160, 'unit': 'px', 'area_m2': 18.95},
    {'id': 'auto-693', 'name': '6.93 Konzerv. radion. 3', 'room_type': 'conservation_lab', 'x': 6880, 'y': 640, 'width': 120, 'height': 160, 'unit': 'px', 'area_m2': 18.95},
    {'id': 'auto-692', 'name': '6.92 Konzerv. radion. 2', 'room_type': 'conservation_lab', 'x': 7000, 'y': 640, 'width': 115, 'height': 160, 'unit': 'px', 'area_m2': 18.95},
    {'id': 'auto-691', 'name': '6.91 Konzerv. radion. 1', 'room_type': 'conservation_lab', 'x': 7115, 'y': 640, 'width': 120, 'height': 160, 'unit': 'px', 'area_m2': 18.95},
    {'id': 'auto-31', 'name': '3.1 Entomološki depo', 'room_type': 'specimen_storage', 'x': 8190, 'y': 640, 'width': 1100, 'height': 165, 'unit': 'px', 'area_m2': 183.94},
    {'id': 'auto-35', 'name': '3.5 Zbirke eksponata sisara', 'room_type': 'specimen_storage', 'x': 8190, 'y': 805, 'width': 620, 'height': 275, 'unit': 'px', 'area_m2': 116.78},
    {'id': 'auto-34', 'name': '3.4 Zbirke lovačkih trofeja', 'room_type': 'specimen_storage', 'x': 7800, 'y': 805, 'width': 390, 'height': 275, 'unit': 'px', 'area_m2': 24.1},
    {'id': 'auto-33', 'name': '3.3 Studijske zbirke sisara', 'room_type': 'specimen_storage', 'x': 8580, 'y': 805, 'width': 560, 'height': 275, 'unit': 'px', 'area_m2': 99.42},
    {'id': 'auto-61', 'name': '6.1 Zbirka lovačkog oružja i pribora', 'room_type': 'specimen_storage', 'x': 9140, 'y': 805, 'width': 285, 'height': 110, 'unit': 'px', 'area_m2': 89.47},
    {'id': 'auto-32', 'name': '3.2 Zbirka egzotičnih sisara', 'room_type': 'specimen_storage', 'x': 9425, 'y': 805, 'width': 365, 'height': 275, 'unit': 'px', 'area_m2': 102.58},
    {'id': 'auto-36', 'name': '3.6 Suva ihtiološka zbirka', 'room_type': 'dry_lab', 'x': 9140, 'y': 915, 'width': 285, 'height': 165, 'unit': 'px', 'area_m2': 78.91},
    {'id': 'auto-310', 'name': '3.10 Herpetološki depo / suve zbirke', 'room_type': 'specimen_storage', 'x': 9085, 'y': 640, 'width': 400, 'height': 165, 'unit': 'px', 'area_m2': 45.75},
    {'id': 'auto-63', 'name': '6.3 Depo opreme za kičmenjake', 'room_type': 'specimen_storage', 'x': 9485, 'y': 640, 'width': 215, 'height': 165, 'unit': 'px', 'area_m2': 8.0},
    {'id': 'auto-38', 'name': '3.8 Fungarijum', 'room_type': 'specimen_storage', 'x': 9790, 'y': 805, 'width': 180, 'height': 275, 'unit': 'px', 'area_m2': 55.81},
    {'id': 'auto-39', 'name': '3.9 Ornitološki depo', 'room_type': 'specimen_storage', 'x': 9700, 'y': 255, 'width': 410, 'height': 1110, 'unit': 'px', 'area_m2': 390.75},
    {'id': 'auto-37', 'name': '3.7 Herbarijum', 'room_type': 'specimen_storage', 'x': 8190, 'y': 1148, 'width': 1505, 'height': 217, 'unit': 'px', 'area_m2': 300.09},
    {'id': 'auto-311', 'name': '3.11 Malakološki depo', 'room_type': 'specimen_storage', 'x': 8690, 'y': 640, 'width': 250, 'height': 165, 'unit': 'px', 'area_m2': 22.0},
    {'id': 'auto-67', 'name': '6.7 Depo zbirke paleoflore', 'room_type': 'specimen_storage', 'x': 7680, 'y': 1115, 'width': 510, 'height': 250, 'unit': 'px', 'area_m2': 149.87},
    {'id': 'auto-66', 'name': '6.6 Depo fosilizovanih beskičmenjaka', 'room_type': 'specimen_storage', 'x': 6745, 'y': 255, 'width': 705, 'height': 310, 'unit': 'px', 'area_m2': 192.33},
    {'id': 'auto-64', 'name': '6.4 Depo minerala i meteorita', 'room_type': 'specimen_storage', 'x': 7450, 'y': 255, 'width': 705, 'height': 310, 'unit': 'px', 'area_m2': 194.27},
    {'id': 'auto-65', 'name': '6.5 Depo petrološke zbirke', 'room_type': 'specimen_storage', 'x': 8155, 'y': 255, 'width': 720, 'height': 310, 'unit': 'px', 'area_m2': 265.87},
    {'id': 'auto-68', 'name': '6.8 Depo fosilizovanih kičmenjaka', 'room_type': 'specimen_storage', 'x': 8875, 'y': 255, 'width': 515, 'height': 310, 'unit': 'px', 'area_m2': 247.32},
]


def sanitize_project_space(raw_space, *, project_space_library):
    """Normalize one space-planner payload entry."""
    if not isinstance(raw_space, dict):
        return None

    def _as_float(value, default=0.0):
        try:
            num = float(value)
        except (TypeError, ValueError):
            num = default
        return max(0.0, min(100.0, round(num, 4)))

    def _sanitize_points(raw_points):
        points = []
        if not isinstance(raw_points, list):
            return points
        for raw_point in raw_points:
            if not isinstance(raw_point, dict):
                continue
            points.append(
                {
                    'x': _as_float(raw_point.get('x')),
                    'y': _as_float(raw_point.get('y')),
                }
            )
        return points

    shape = str(raw_space.get('shape', 'rect')).strip().lower()
    if shape not in {'rect', 'polygon'}:
        shape = 'rect'

    points = _sanitize_points(raw_space.get('points'))
    if shape == 'polygon' and len(points) < 3:
        shape = 'rect'
        points = []

    if shape == 'polygon':
        min_x = min(point['x'] for point in points)
        min_y = min(point['y'] for point in points)
        max_x = max(point['x'] for point in points)
        max_y = max(point['y'] for point in points)
        x = min_x
        y = min_y
        width = max(0.1, round(max_x - min_x, 4))
        height = max(0.1, round(max_y - min_y, 4))
    else:
        x = _as_float(raw_space.get('x'))
        y = _as_float(raw_space.get('y'))
        width = _as_float(raw_space.get('width'))
        height = _as_float(raw_space.get('height'))

    specs = raw_space.get('specs') if isinstance(raw_space.get('specs'), dict) else {}
    room_type = str(raw_space.get('room_type', '')).strip()
    if room_type not in project_space_library:
        room_type = ''

    try:
        area_m2 = float(raw_space.get('area_m2', 0))
        if area_m2 < 0:
            area_m2 = 0.0
        area_m2 = round(area_m2, 2)
    except (TypeError, ValueError):
        area_m2 = 0.0

    return {
        'id': str(raw_space.get('id', '')).strip() or f"space-{int(time.time() * 1000)}-{uuid.uuid4().hex[:8]}",
        'name': str(raw_space.get('name', '')).strip(),
        'room_type': room_type,
        'shape': shape,
        'points': points,
        'x': x,
        'y': y,
        'width': width,
        'height': height,
        'area_m2': area_m2,
        'specs': {
            'purpose': str(specs.get('purpose', '')).strip(),
            'floor_materials': str(specs.get('floor_materials', '')).strip(),
            'wall_materials': str(specs.get('wall_materials', '')).strip(),
            'ventilation': str(specs.get('ventilation', '')).strip(),
            'equipment': str(specs.get('equipment', '')).strip(),
            'utilities': str(specs.get('utilities', '')).strip(),
            'notes': str(specs.get('notes', '')).strip(),
            'curator': str(specs.get('curator', '')).strip(),
        },
    }


def build_project_auto_detected_spaces(
    *,
    project_auto_detected_spaces,
    project_space_library,
    project_space_plan_image_size,
):
    """Normalize seeded room bounds and prefill specs from the room type library."""
    if not project_auto_detected_spaces:
        return []

    detected_spaces = []
    for raw_space in project_auto_detected_spaces:
        room_type = raw_space.get('room_type', '')
        template = project_space_library.get(room_type, {})
        suggestions = template.get('suggestions', {})
        raw_specs = raw_space.get('specs') if isinstance(raw_space.get('specs'), dict) else {}
        uses_pixels = raw_space.get('unit') == 'px'
        x = raw_space.get('x', 0)
        y = raw_space.get('y', 0)
        width = raw_space.get('width', 0)
        height = raw_space.get('height', 0)
        if uses_pixels:
            x = (x / project_space_plan_image_size['width']) * 100
            y = (y / project_space_plan_image_size['height']) * 100
            width = (width / project_space_plan_image_size['width']) * 100
            height = (height / project_space_plan_image_size['height']) * 100
        sanitized = sanitize_project_space(
            {
                **raw_space,
                'x': x,
                'y': y,
                'width': width,
                'height': height,
                'specs': {
                    'purpose': raw_specs.get('purpose') or (suggestions.get('purpose') or [''])[0],
                    'floor_materials': raw_specs.get('floor_materials') or (suggestions.get('floor_materials') or [''])[0],
                    'wall_materials': raw_specs.get('wall_materials') or (suggestions.get('wall_materials') or [''])[0],
                    'ventilation': raw_specs.get('ventilation') or (suggestions.get('ventilation') or [''])[0],
                    'equipment': raw_specs.get('equipment') or (suggestions.get('equipment') or [''])[0],
                    'utilities': raw_specs.get('utilities') or (suggestions.get('utilities') or [''])[0],
                    'notes': raw_specs.get('notes')
                    or 'Експериментално препознато на основу текста са плана и легенде; проверити границе простора.',
                },
            },
            project_space_library=project_space_library,
        )
        if sanitized:
            detected_spaces.append(sanitized)
    return detected_spaces


def default_project_space_planner_state(*, auto_layout_version, project_space_plan_file):
    """Return the default project space planner state payload."""
    return {
        'version': 1,
        'auto_layout_version': auto_layout_version,
        'plan': {
            'filename': project_space_plan_file,
            'title': 'Основа кота -5,00',
        },
        'spaces': [],
        'last_active_view': None,
        'last_updated_at': None,
        'last_updated_by': None,
    }


def save_project_space_planner_state(
    payload,
    user_name,
    *,
    planner_file,
    auto_layout_version,
    project_space_plan_file,
):
    """Persist the project space planner state to disk."""
    state = default_project_space_planner_state(
        auto_layout_version=auto_layout_version,
        project_space_plan_file=project_space_plan_file,
    )
    state['spaces'] = payload.get('spaces', [])
    if payload.get('last_active_view'):
        state['last_active_view'] = payload['last_active_view']
    state['last_updated_at'] = datetime.utcnow().isoformat() + 'Z'
    state['last_updated_by'] = user_name
    planner_file.parent.mkdir(parents=True, exist_ok=True)
    backup_dir = planner_file.parent / 'space_planner_backups'
    backup_dir.mkdir(exist_ok=True)
    if planner_file.exists():
        import shutil

        timestamp = datetime.utcnow().strftime('%Y%m%d_%H%M%S')
        backup_path = backup_dir / f'space_planner_{timestamp}.json'
        try:
            shutil.copy2(str(planner_file), str(backup_path))
        except Exception:
            pass
        try:
            backups = sorted(backup_dir.glob('space_planner_*.json'))
            for old_backup in backups[:-20]:
                old_backup.unlink(missing_ok=True)
        except Exception:
            pass

    sample_positions = [(space.get('id'), space.get('x'), space.get('y')) for space in state['spaces'][:3]]
    logger.info(
        "Space planner SAVE by '%s': %s spaces, view=%s, sample=%s",
        user_name,
        len(state['spaces']),
        state.get('last_active_view'),
        sample_positions,
    )
    write_json_file(planner_file, state)
    return state


def load_project_space_planner_state(
    *,
    planner_file,
    auto_layout_version,
    project_space_plan_file,
    project_space_library,
    project_space_plan_image_size,
    project_auto_detected_spaces,
    project_depot_auto_detected_spaces,
):
    """Load and auto-sync project planner state from disk."""
    if not planner_file.exists():
        logger.info("Space planner LOAD: file does not exist, returning defaults")
        return default_project_space_planner_state(
            auto_layout_version=auto_layout_version,
            project_space_plan_file=project_space_plan_file,
        )

    try:
        data = load_json_file(planner_file, default={})
        if not isinstance(data, dict):
            logger.warning("Space planner LOAD: file is not a dict, returning defaults")
            return default_project_space_planner_state(
                auto_layout_version=auto_layout_version,
                project_space_plan_file=project_space_plan_file,
            )
        state = default_project_space_planner_state(
            auto_layout_version=auto_layout_version,
            project_space_plan_file=project_space_plan_file,
        )
        state.update(
            {
                'plan': data.get('plan') or state['plan'],
                'spaces': data.get('spaces') if isinstance(data.get('spaces'), list) else [],
                'last_active_view': data.get('last_active_view'),
                'last_updated_at': data.get('last_updated_at'),
                'last_updated_by': data.get('last_updated_by'),
                'version': data.get('version', 1),
                'auto_layout_version': data.get('auto_layout_version', 0),
            }
        )
        sample = [(space.get('id'), space.get('x'), space.get('y')) for space in state['spaces'][:3]]
        logger.info(
            "Space planner LOAD: %s spaces, auto_layout_v=%s, view=%s, sample=%s",
            len(state['spaces']),
            state['auto_layout_version'],
            state.get('last_active_view'),
            sample,
        )
        if state.get('auto_layout_version') != auto_layout_version:
            detected_by_id = {
                space['id']: space
                for space in build_project_auto_detected_spaces(
                    project_auto_detected_spaces=project_auto_detected_spaces,
                    project_space_library=project_space_library,
                    project_space_plan_image_size=project_space_plan_image_size,
                )
            }
            for space in project_depot_auto_detected_spaces:
                sanitized = sanitize_project_space(space, project_space_library=project_space_library)
                if sanitized:
                    detected_by_id[sanitized['id']] = sanitized

            synced_spaces = []
            for stored_space in state['spaces']:
                if not isinstance(stored_space, dict):
                    continue
                space_id = str(stored_space.get('id', '')).strip()
                if space_id in detected_by_id:
                    detected_space = dict(detected_by_id[space_id])
                    detected_space['specs'] = dict(detected_space.get('specs', {}))
                    stored_specs = stored_space.get('specs') if isinstance(stored_space.get('specs'), dict) else {}
                    for field in ('name', 'room_type'):
                        if str(stored_space.get(field, '')).strip():
                            detected_space[field] = stored_space.get(field)
                    for field in ('x', 'y', 'width', 'height'):
                        if field not in stored_space:
                            continue
                        try:
                            value = float(stored_space.get(field))
                            if value >= 0:
                                detected_space[field] = value
                        except (TypeError, ValueError):
                            pass
                    if isinstance(stored_space.get('points'), list) and stored_space['points']:
                        detected_space['points'] = stored_space['points']
                    if 'area_m2' in stored_space:
                        try:
                            stored_area = float(stored_space.get('area_m2'))
                            if stored_area >= 0:
                                detected_space['area_m2'] = stored_area
                        except (TypeError, ValueError):
                            pass
                    for field, value in stored_specs.items():
                        if str(value).strip():
                            detected_space['specs'][field] = str(value).strip()
                    synced_spaces.append(detected_space)
                else:
                    synced_spaces.append(stored_space)
            state['spaces'] = synced_spaces
            state['auto_layout_version'] = auto_layout_version
            try:
                save_project_space_planner_state(
                    {'spaces': synced_spaces, 'last_active_view': state.get('last_active_view')},
                    state.get('last_updated_by', 'auto-sync'),
                    planner_file=planner_file,
                    auto_layout_version=auto_layout_version,
                    project_space_plan_file=project_space_plan_file,
                )
            except Exception:
                pass
        return state
    except Exception as exc:
        logger.warning("Failed to load project space planner state: %s", exc)
        return default_project_space_planner_state(
            auto_layout_version=auto_layout_version,
            project_space_plan_file=project_space_plan_file,
        )


def api_project_space_planner_get(
    *,
    planner_file,
    auto_layout_version,
    project_space_plan_views,
    project_space_plan_file,
    project_space_plan_image_size,
    project_space_library,
    project_common_terms,
    project_auto_detected_spaces,
    project_depot_auto_detected_spaces,
):
    """Return stored room zones and terminology for the project plan editor."""
    state = load_project_space_planner_state(
        planner_file=planner_file,
        auto_layout_version=auto_layout_version,
        project_space_plan_file=project_space_plan_file,
        project_space_library=project_space_library,
        project_space_plan_image_size=project_space_plan_image_size,
        project_auto_detected_spaces=project_auto_detected_spaces,
        project_depot_auto_detected_spaces=project_depot_auto_detected_spaces,
    )
    for space in state.get('spaces', []):
        specs = space.get('specs') or {}
        if not specs.get('curator'):
            assigned = _assign_curator_for_space(space)
            if assigned:
                specs['curator'] = assigned
                space['specs'] = specs

    views_with_urls = []
    for view in project_space_plan_views:
        normalized_view = dict(view)
        if 'plan_image' in normalized_view:
            normalized_view['plan_image_url'] = url_for('projects.projekti_file', filename=normalized_view['plan_image'])
        views_with_urls.append(normalized_view)

    curators = []
    try:
        import psycopg
        from psycopg.rows import dict_row

        pg_url = os.environ.get('DATABASE_URL', '').replace('postgresql+psycopg://', 'postgresql://')
        with psycopg.connect(pg_url, row_factory=dict_row) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT full_name, email, position
                    FROM users
                    WHERE is_active = TRUE
                    ORDER BY full_name
                    """
                )
                for row in cur.fetchall():
                    curators.append(
                        {
                            'name': row['full_name'],
                            'email': row.get('email', ''),
                            'position': row.get('position', ''),
                        }
                    )
    except Exception as exc:
        logger.warning("Could not load curators for space planner: %s", exc)

    return jsonify(
        {
            'success': True,
            'plan_image_url': url_for('projects.projekti_file', filename=project_space_plan_file),
            'plan_image_size': project_space_plan_image_size,
            'plan_views': views_with_urls,
            'state': state,
            'room_library': project_space_library,
            'common_terms': project_common_terms,
            'detected_spaces': build_project_auto_detected_spaces(
                project_auto_detected_spaces=project_auto_detected_spaces,
                project_space_library=project_space_library,
                project_space_plan_image_size=project_space_plan_image_size,
            ),
            'depot_detected_spaces': [
                sanitize_project_space(space, project_space_library=project_space_library)
                for space in project_depot_auto_detected_spaces
                if sanitize_project_space(space, project_space_library=project_space_library)
            ],
            'curators': curators,
        }
    )


def api_project_space_planner_save(
    *,
    planner_file,
    auto_layout_version,
    project_space_plan_file,
    project_space_library,
):
    """Persist room zones and room specifications for the project plan editor."""
    payload = request.get_json(force=True) or {}
    raw_spaces = payload.get('spaces')
    if not isinstance(raw_spaces, list):
        return jsonify({'success': False, 'message': 'Листа просторија је обавезна.'}), 400

    spaces = []
    for raw_space in raw_spaces:
        space = sanitize_project_space(raw_space, project_space_library=project_space_library)
        if not space:
            continue
        if space['width'] <= 0 or space['height'] <= 0:
            continue
        spaces.append(space)

    save_payload = {'spaces': spaces}
    if payload.get('last_active_view'):
        save_payload['last_active_view'] = str(payload['last_active_view']).strip()
    state = save_project_space_planner_state(
        save_payload,
        session.get('user_name') or session.get('user_email') or 'unknown',
        planner_file=planner_file,
        auto_layout_version=auto_layout_version,
        project_space_plan_file=project_space_plan_file,
    )
    return jsonify({'success': True, 'state': state})


def serve_project_file(filename, *, project_directory='Projekti'):
    """Serve a file from the project documentation directory."""
    return send_from_directory(project_directory, filename)
