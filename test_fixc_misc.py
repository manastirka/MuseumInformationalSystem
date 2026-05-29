import os

os.environ.setdefault('FLASK_ENV', 'testing')
os.environ.setdefault('SECRET_KEY', 'test-secret')
os.environ.setdefault('REDIS_URL', '')
os.environ.setdefault('SESSION_TYPE', 'filesystem')
os.environ.setdefault('SESSION_FILE_DIR', '/tmp/museum-test-c-misc')

import json

import locality_data
import museum_staff_support


def test_geocache_mutations_visible_via_imported_name(tmp_path, monkeypatch):
    """_load_geocache must mutate the shared dict in place so an imported
    `_geocache` name (as in geocode_all_localities.py) reflects later writes."""
    from locality_data import _geocache as script_ref

    cache_file = tmp_path / 'geocache.json'
    cache_file.write_text(json.dumps({'sombor': {'lat': 1.0, 'lon': 2.0}}), encoding='utf-8')
    monkeypatch.setattr(locality_data, 'CACHE_FILE', str(cache_file))

    locality_data._load_geocache()

    # imported name must still point at the live module dict
    assert script_ref is locality_data._geocache
    assert script_ref.get('sombor') == {'lat': 1.0, 'lon': 2.0}

    # a subsequent mutation (as geocode_locality does) must be visible
    locality_data._geocache['__testkey__'] = None
    assert '__testkey__' in script_ref
    assert len(script_ref) == len(locality_data._geocache)


def test_save_library_database_missing_books_key_does_not_crash(tmp_path):
    """A non-None payload lacking the 'books' key must save successfully
    (treated as zero books) rather than silently failing via KeyError."""
    library_path = str(tmp_path / 'library.json')

    payload = {'categories': ['Геологија']}  # intentionally no 'books' key

    result = museum_staff_support.save_library_database(
        library_path=library_path,
        library_database=payload,
    )

    assert result is True
    saved = json.loads((tmp_path / 'library.json').read_text(encoding='utf-8'))
    assert saved['statistics']['total_books'] == 0
    assert saved['statistics']['available_books'] == 0
    assert saved['statistics']['borrowed_books'] == 0
    assert saved['statistics']['total_categories'] == 1


def test_save_library_database_counts_books_correctly(tmp_path):
    """Existing happy path keeps working: book counts/statuses preserved."""
    library_path = str(tmp_path / 'library.json')

    payload = {
        'books': [
            {'status': 'доступна'},
            {'status': 'позајмљена'},
            {'status': 'доступна'},
        ],
        'categories': ['Геологија', 'Минералогија'],
    }

    result = museum_staff_support.save_library_database(
        library_path=library_path,
        library_database=payload,
    )

    assert result is True
    saved = json.loads((tmp_path / 'library.json').read_text(encoding='utf-8'))
    assert saved['statistics']['total_books'] == 3
    assert saved['statistics']['available_books'] == 2
    assert saved['statistics']['borrowed_books'] == 1
    assert saved['statistics']['total_categories'] == 2
