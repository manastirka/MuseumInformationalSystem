"""Shared museum content bootstrap data and helper functions."""

import json
import logging
import os


logger = logging.getLogger(__name__)


def _load_json_list(filename):
    """Load a list payload from the local data directory."""
    data_path = os.path.join('data', filename)
    try:
        with open(data_path, 'r', encoding='utf-8') as handle:
            data = json.load(handle)
            if isinstance(data, list):
                return data
            logger.warning("Expected list in %s, got %s", filename, type(data))
    except FileNotFoundError:
        logger.warning("Data file not found at %s", data_path)
    except json.JSONDecodeError as exc:
        logger.error("Unable to parse %s: %s", filename, exc)
    return []


def load_exhibitions_data(*, database_url=None, phase3a_databases=None):
    """Load exhibitions from PostgreSQL or the JSON fallback."""
    if database_url and phase3a_databases is not None:
        return phase3a_databases.load_exhibitions_data()
    return _load_json_list('exhibitions.json')


def load_news_data(*, database_url=None, phase3a_databases=None):
    """Load news articles from PostgreSQL or the JSON fallback."""
    if database_url and phase3a_databases is not None:
        return phase3a_databases.load_news_data()
    return _load_json_list('news.json')


def build_exhibitions_database(*, load_exhibitions_data):
    """Build the exhibition cache payload on demand."""
    exhibitions = load_exhibitions_data()
    return {
        'exhibitions': exhibitions,
        'types': sorted({entry.get('type', 'Изложба') for entry in exhibitions}) or ['Изложба'],
    }


def build_news_database(*, load_news_data):
    """Build the news cache payload on demand."""
    articles = load_news_data()
    return {
        'articles': articles,
        'types': sorted({entry.get('type', 'Изложба') for entry in articles}) or ['Изложба'],
    }


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
            'description': 'Комплетни остатак мамута приморакса пронађен током истраживања у Обедској бари. Кључни експонат изложбе "Сурлаши – дивови прошлости".',
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
            'description': 'Највећи српски метеорит, хондрит са високим уделом никла. Представља кључни пример свемирског материјала у збирци.',
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
            'description': 'Серија узорака тефре и пепела из различитих фаза ерупције Везува. Користи се у едукативним програмима и научним анализама.',
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
            'description': 'Ручно припремљен хербаријум са ретким и заштићеним врстама орхидеја. Рестаурирала кустос Снежана Марковић 2022. године.',
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
            'description': 'Референтна колекција водених вилина коју је сакупио др Милош Јовић. У току је превентивна конзервација и дигитализација.',
        },
    ],
    'categories': ['Палеонтологија', 'Минералогија', 'Геологија', 'Ботаника', 'Зоологија'],
    'statuses': ['изложен', 'у депоу', 'у конзервацији'],
    'conditions': ['Одлично', 'Добро', 'Захтева конзервацију'],
}


def get_exhibit_statistics(*, exhibits_database):
    """Aggregate exhibit metrics from the artifacts dataset."""
    artifacts = exhibits_database['artifacts']
    displayed = len([artifact for artifact in artifacts if artifact['status'] == 'изложен'])
    storage = len([artifact for artifact in artifacts if artifact['status'] == 'у депоу'])
    excellent = len([artifact for artifact in artifacts if artifact['condition'] == 'Одлично'])
    distinct_categories = len({artifact['category'] for artifact in artifacts})

    return {
        'total_artifacts': len(artifacts),
        'displayed_artifacts': displayed,
        'storage_artifacts': storage,
        'excellent_condition': excellent,
        'total_categories': distinct_categories,
    }


def get_exhibition_statistics(*, exhibitions_database, current_year):
    """Aggregate exhibition metrics for dashboard and detail views."""
    exhibitions = [
        exhibition
        for exhibition in exhibitions_database['exhibitions']
        if exhibition.get('category', 'gallery') != 'touring'
    ]
    active = len([exhibition for exhibition in exhibitions if exhibition['status'] == 'Активна'])
    completed = len(
        [
            exhibition
            for exhibition in exhibitions
            if exhibition['status'] in ('Завршена', 'Историјска')
        ]
    )
    planned = len([exhibition for exhibition in exhibitions if exhibition['status'] == 'Планирана'])
    total_visitors = sum(exhibition['visitor_count'] for exhibition in exhibitions)
    annual = len(
        [
            exhibition
            for exhibition in exhibitions
            if exhibition['start_date'].startswith(str(current_year))
        ]
    )

    return {
        'total_exhibitions': len(exhibitions),
        'active_exhibitions': active,
        'completed_exhibitions': completed,
        'planned_exhibitions': planned,
        'total_visitors': total_visitors,
        'annual_exhibitions': annual,
    }
