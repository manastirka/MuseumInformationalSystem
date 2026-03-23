"""Shared vehicle bootstrap and persistence helpers."""

import json
import logging
import os


logger = logging.getLogger(__name__)


def default_vehicles():
    """Return seeded vehicle records used when no persisted data exists."""
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


def load_vehicles(*, vehicles_file, database_url=None, phase3a_databases=None):
    """Load vehicles from PostgreSQL or JSON fallback storage."""
    if database_url and phase3a_databases is not None:
        try:
            return phase3a_databases.get_vehicles_list()
        except Exception as exc:
            logger.warning("Failed to load vehicles from PostgreSQL: %s", exc)

    try:
        if os.path.exists(vehicles_file):
            with open(vehicles_file, 'r', encoding='utf-8') as handle:
                return json.load(handle)
    except Exception as exc:
        logger.error("Error loading vehicles: %s", exc)

    return default_vehicles()


def save_vehicles(*, vehicles_file, vehicles):
    """Persist vehicles to JSON fallback storage."""
    try:
        os.makedirs(os.path.dirname(vehicles_file), exist_ok=True)
        with open(vehicles_file, 'w', encoding='utf-8') as handle:
            json.dump(vehicles, handle, ensure_ascii=False, indent=2)
        return True
    except Exception as exc:
        logger.error("Error saving vehicles: %s", exc)
        return False


def load_reservations(*, reservations_file, database_url=None, phase3a_databases=None):
    """Load reservations from PostgreSQL or JSON fallback storage."""
    if database_url and phase3a_databases is not None:
        try:
            return phase3a_databases.get_vehicle_reservations()
        except Exception as exc:
            logger.warning("Failed to load reservations from PostgreSQL: %s", exc)

    try:
        if os.path.exists(reservations_file):
            with open(reservations_file, 'r', encoding='utf-8') as handle:
                return json.load(handle)
    except Exception as exc:
        logger.error("Error loading reservations: %s", exc)

    return []


def save_reservations(*, reservations_file, reservations):
    """Persist reservations to JSON fallback storage."""
    try:
        os.makedirs(os.path.dirname(reservations_file), exist_ok=True)
        with open(reservations_file, 'w', encoding='utf-8') as handle:
            json.dump(reservations, handle, ensure_ascii=False, indent=2)
        return True
    except Exception as exc:
        logger.error("Error saving reservations: %s", exc)
        return False
