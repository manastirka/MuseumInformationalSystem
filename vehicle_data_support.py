"""Vehicle and reservation persistence — PostgreSQL is the single source of truth.

Ranije je ovaj modul čitao/pisao i JSON fajl kao paralelni izvor. To je
uklonjeno (ZADATAK #3, jul 2026): baza je jedini izvor istine. Ključna
posledica je da se pad baze **nikad ne maskira** vraćanjem zastarelih JSON
podataka — greška se loguje na ERROR nivou i propagira pozivaocu, koji je
tada dužan da je prikaže korisniku (fail-loud umesto fail-silent).

Jedini keš je in-memory keš u ``app.py`` (``_MUSEUM_VEHICLES_CACHE`` /
``_VEHICLE_RESERVATIONS_CACHE``), koji se invalidira ``force_reload``-om
posle svakog upisa (write-through).
"""

import logging

logger = logging.getLogger(__name__)


class VehicleStoreUnavailable(RuntimeError):
    """Baza vozila/rezervacija nije dostupna — nema tihog JSON fallback-a."""


def load_vehicles(*, phase3a_databases):
    """Load vehicles from PostgreSQL. Raises on failure — no silent fallback."""
    if phase3a_databases is None:
        raise VehicleStoreUnavailable(
            "PostgreSQL backend (phase3a_databases) nije dostupan — vozila se ne mogu učitati"
        )
    try:
        return phase3a_databases.get_vehicles_list()
    except Exception as exc:
        logger.error("Neuspešno učitavanje vozila iz PostgreSQL-a: %s", exc)
        raise


def load_reservations(*, phase3a_databases):
    """Load reservations from PostgreSQL. Raises on failure — no silent fallback."""
    if phase3a_databases is None:
        raise VehicleStoreUnavailable(
            "PostgreSQL backend (phase3a_databases) nije dostupan — rezervacije se ne mogu učitati"
        )
    try:
        return phase3a_databases.get_vehicle_reservations()
    except Exception as exc:
        logger.error("Neuspešno učitavanje rezervacija iz PostgreSQL-a: %s", exc)
        raise
