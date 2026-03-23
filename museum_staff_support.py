"""Shared library and employee-directory bootstrap helpers."""

import json
import logging
import os


logger = logging.getLogger(__name__)


def default_library_database():
    """Return the empty fallback library payload."""
    return {
        'books': [],
        'categories': [
            'Геологија',
            'Минералогија',
            'Палеонтологија',
            'Ботаника',
            'Зоологија',
            'Ентомологија',
            'Ихтиологија',
            'Општа научна литература',
            'Монографска публикација',
        ],
        'statistics': {
            'total_books': 0,
            'available_books': 0,
            'borrowed_books': 0,
            'total_categories': 0,
        },
    }


def load_library_database(*, library_path, database_url=None, phase3a_databases=None):
    """Load the library database from PostgreSQL or JSON fallback."""
    if database_url and phase3a_databases is not None:
        return phase3a_databases.get_library_database()

    try:
        with open(library_path, 'r', encoding='utf-8') as handle:
            data = json.load(handle)
            logger.info(
                "Loaded library database: %s books",
                data.get('statistics', {}).get('total_books', 0),
            )
            return data
    except FileNotFoundError:
        logger.warning("Library database file not found at %s, using default data", library_path)
    except json.JSONDecodeError as exc:
        logger.error("Error decoding library database JSON: %s", exc)

    return default_library_database()


def save_library_database(*, library_path, library_database):
    """Persist the library database to JSON fallback storage."""
    if library_database is None:
        return False

    try:
        os.makedirs(os.path.dirname(library_path), exist_ok=True)

        library_database['statistics'] = {
            'total_books': len(library_database['books']),
            'available_books': len(
                [book for book in library_database['books'] if book.get('status') == 'доступна']
            ),
            'borrowed_books': len(
                [book for book in library_database['books'] if book.get('status') == 'позајмљена']
            ),
            'total_categories': len(library_database.get('categories', [])),
        }

        with open(library_path, 'w', encoding='utf-8') as handle:
            json.dump(library_database, handle, ensure_ascii=False, indent=2)

        logger.info(
            "Saved library database: %s books",
            library_database['statistics']['total_books'],
        )
        return True
    except Exception as exc:
        logger.error("Error saving library database: %s", exc)
        return False


def load_employee_directory(*, directory_path, database_url=None, phase3a_databases=None):
    """Load employee directory from PostgreSQL or JSON fallback."""
    if database_url and phase3a_databases is not None:
        return phase3a_databases.load_employee_directory()

    try:
        with open(directory_path, 'r', encoding='utf-8') as handle:
            data = json.load(handle)
            logger.info("Loaded employee directory with %d profiles.", len(data))
            return data
    except FileNotFoundError:
        logger.warning("Employee directory not found at %s", directory_path)
    except json.JSONDecodeError as exc:
        logger.error("Error decoding employee directory JSON: %s", exc)

    return []
