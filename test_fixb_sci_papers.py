import os

os.environ.setdefault('FLASK_ENV', 'testing')
os.environ.setdefault('SECRET_KEY', 'test-secret')
os.environ.setdefault('REDIS_URL', '')
os.environ.setdefault('SESSION_TYPE', 'filesystem')
os.environ.setdefault('SESSION_FILE_DIR', '/tmp/museum-test-b-sci-papers')

import fetch_scientific_papers as fsp


def test_parse_openalex_work_with_biblio_null():
    """A work with explicit biblio: null must not raise AttributeError."""
    work = {
        'id': 'https://openalex.org/W123',
        'title': 'Some geology paper',
        'biblio': None,
    }

    result = fsp.parse_openalex_work(work, search_query='geology Serbia')

    assert result['volume'] == ''
    assert result['issue'] == ''
    assert result['openalex_id'] == 'https://openalex.org/W123'


def test_parse_openalex_work_with_biblio_values():
    """When biblio is present, volume/issue are extracted normally."""
    work = {
        'id': 'https://openalex.org/W456',
        'title': 'Another paper',
        'biblio': {'volume': '12', 'issue': '3'},
    }

    result = fsp.parse_openalex_work(work, search_query='q')

    assert result['volume'] == '12'
    assert result['issue'] == '3'


def test_parse_openalex_work_with_biblio_missing():
    """When biblio key is missing entirely, volume/issue default to ''."""
    work = {
        'id': 'https://openalex.org/W789',
        'title': 'No biblio paper',
    }

    result = fsp.parse_openalex_work(work, search_query='q')

    assert result['volume'] == ''
    assert result['issue'] == ''
