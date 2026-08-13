"""Shared persistence helpers for module access and dashboard preferences."""

import json
import logging
import os
import time
from copy import deepcopy
from typing import Any, Callable, Optional

from runtime_lock_utils import load_json_file, write_json_file

logger = logging.getLogger(__name__)
SHARED_SETTINGS_TABLE = 'app_shared_settings'
_db_setting_failure_cache: dict[str, float] = {}
_DB_RETRY_INTERVAL_SECONDS = float(os.environ.get('SHARED_SETTINGS_DB_RETRY_INTERVAL_SECONDS', '15'))

# Poslednja pouzdano poznata vrednost po ključu (last-known-good). Puni se pri
# svakom uspešnom čitanju/upisu ka bazi i služi da se pri padu baze NE vrate tiho
# podrazumevane (šire) dozvole. _NO_ROW znači "baza dostupna, ali nema upisa".
_NO_ROW = object()
_UNSET = object()
_last_known_good: dict[str, Any] = {}


class SharedSettingsUnavailable(RuntimeError):
    """Baza za deljena podešavanja nedostupna, a nema last-known-good vrednosti.

    Signalizira pozivaocu da se ponaša fail-closed (najrestriktivnije) umesto da
    posluži permisivne podrazumevane vrednosti.
    """


def _ensure_shared_settings_table(get_postgres_connection: Callable[[], Any]):
    """Ensure the shared settings table exists before reads or writes."""
    with get_postgres_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                f"""
                CREATE TABLE IF NOT EXISTS {SHARED_SETTINGS_TABLE} (
                    setting_key TEXT PRIMARY KEY,
                    setting_value JSONB NOT NULL,
                    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
                )
                """
            )
        conn.commit()


def _load_db_json_setting(
    *,
    get_postgres_connection: Optional[Callable[[], Any]],
    setting_key: str,
):
    """Load a JSON setting blob from PostgreSQL.

    Returns the stored value, or ``_NO_ROW`` when the database is reachable but has
    no row for ``setting_key``. Raises :class:`SharedSettingsUnavailable` when the
    database cannot be consulted, so callers never mistake an outage for
    "no configured value".
    """
    if get_postgres_connection is None:
        return _NO_ROW

    last_failure_at = _db_setting_failure_cache.get(setting_key)
    if last_failure_at is not None and (time.time() - last_failure_at) < _DB_RETRY_INTERVAL_SECONDS:
        raise SharedSettingsUnavailable(
            f"{setting_key}: preskačem čitanje baze tokom {_DB_RETRY_INTERVAL_SECONDS:.0f}s "
            f"backoff-a nakon skorašnjeg pada"
        )

    try:
        _ensure_shared_settings_table(get_postgres_connection)
        with get_postgres_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    f"SELECT setting_value FROM {SHARED_SETTINGS_TABLE} WHERE setting_key = %s",
                    (setting_key,),
                )
                row = cur.fetchone()
        if not row:
            result = _NO_ROW
        else:
            value = row[0] if isinstance(row, tuple) else row['setting_value']
            result = json.loads(value) if isinstance(value, str) else value
    except Exception as exc:
        _db_setting_failure_cache[setting_key] = time.time()
        raise SharedSettingsUnavailable(
            f"{setting_key}: čitanje tabele {SHARED_SETTINGS_TABLE} iz PostgreSQL-a nije uspelo: {exc}"
        ) from exc

    _db_setting_failure_cache.pop(setting_key, None)
    return result


def _save_db_json_setting(
    *,
    get_postgres_connection: Optional[Callable[[], Any]],
    setting_key: str,
    payload: dict,
) -> bool:
    """Persist a JSON setting blob to PostgreSQL."""
    if get_postgres_connection is None:
        return False

    try:
        _ensure_shared_settings_table(get_postgres_connection)
        with get_postgres_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    f"""
                    INSERT INTO {SHARED_SETTINGS_TABLE} (setting_key, setting_value, updated_at)
                    VALUES (%s, %s::jsonb, NOW())
                    ON CONFLICT (setting_key) DO UPDATE SET
                        setting_value = EXCLUDED.setting_value,
                        updated_at = NOW()
                    """,
                    (setting_key, json.dumps(payload, ensure_ascii=False)),
                )
            conn.commit()
        _last_known_good[setting_key] = deepcopy(payload)
        return True
    except Exception as exc:
        logger.warning("Could not save %s to PostgreSQL shared settings: %s", setting_key, exc)
        return False


def load_json_settings_data(
    *,
    setting_key: str,
    default_value: dict,
    get_postgres_connection: Optional[Callable[[], Any]] = None,
    file_path: Optional[str] = None,
    current_mtime=None,
):
    """Load shared JSON settings from PostgreSQL first, then file fallback.

    Pad baze se NIKAD ne pretvara tiho u podrazumevanu vrednost: kada je baza
    nedostupna, vraća se poslednja pouzdano poznata vrednost (last-known-good), a
    ako ničeg nema u kešu diže se :class:`SharedSettingsUnavailable` da pozivalac
    može da se ponaša fail-closed umesto da posluži permisivni default.
    """
    try:
        db_value = _load_db_json_setting(
            get_postgres_connection=get_postgres_connection,
            setting_key=setting_key,
        )
    except SharedSettingsUnavailable as exc:
        cached = _last_known_good.get(setting_key, _UNSET)
        if cached is _NO_ROW:
            logger.error(
                "Deljena podešavanja '%s': baza nedostupna (%s); služim last-known-good "
                "(nema sačuvanih override-a)", setting_key, exc,
            )
            return deepcopy(default_value)
        if cached is not _UNSET:
            logger.error(
                "Deljena podešavanja '%s': baza nedostupna (%s); služim last-known-good vrednost",
                setting_key, exc,
            )
            return deepcopy(cached)
        logger.error(
            "Deljena podešavanja '%s': baza nedostupna (%s) i nema last-known-good u kešu; "
            "signaliziram pozivaocu da se ponaša fail-closed", setting_key, exc,
        )
        raise

    if get_postgres_connection is not None:
        _last_known_good[setting_key] = deepcopy(db_value) if isinstance(db_value, dict) else _NO_ROW

    if isinstance(db_value, dict):
        logger.info("Loaded %s from PostgreSQL shared settings", setting_key)
        return db_value

    if get_postgres_connection is not None:
        # Baza je dostupna, reda nema: to znači "nema posebnih podešavanja",
        # ne "pročitaj fajl" — inače stara ovlašćenja iz JSON fajla vaskrsnu
        # mimo baze. Fajl ulazi u igru samo eksplicitnim import-om
        # (scripts/migration/import_shared_setting_json.py).
        return deepcopy(default_value)

    try:
        if file_path and current_mtime is not None:
            file_value = load_json_file(file_path)
            logger.info("Loaded %s from %s", setting_key, file_path)
            return file_value
    except Exception as exc:
        logger.error("Error loading %s from file: %s", setting_key, exc)

    return deepcopy(default_value)


def save_json_settings_data(
    *,
    setting_key: str,
    payload: dict,
    get_postgres_connection: Optional[Callable[[], Any]] = None,
    file_path: Optional[str] = None,
) -> bool:
    """Save shared JSON settings to PostgreSQL, or to file when DB is not configured.

    Kada je baza konfigurisana ona je JEDINI izvor istine: pad DB upisa vraća
    False i NE piše falbek fajl — fajl se pri čitanju ionako ignoriše čim DB red
    postoji, pa bi takav upis tiho nestao. Fajl služi samo kad baze nema.
    """
    saved_to_db = _save_db_json_setting(
        get_postgres_connection=get_postgres_connection,
        setting_key=setting_key,
        payload=payload,
    )
    if saved_to_db:
        return True

    if get_postgres_connection is not None:
        logger.error(
            "Deljena podešavanja '%s': DB upis nije uspeo — prijavljujem neuspeh "
            "pozivaocu (bez falbek fajla)", setting_key,
        )
        return False

    saved_to_file = False
    if file_path:
        try:
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            write_json_file(file_path, payload)
            logger.info("Saved %s to %s", setting_key, file_path)
            saved_to_file = True
        except Exception as exc:
            logger.error("Error saving %s to file: %s", setting_key, exc)

    return saved_to_file


def _fail_closed_module_access(default_access):
    """Najrestriktivnija verzija dozvola: svaki modul deny-all.

    Skida sve override-e (default_access=False, prazni authorized/restricted) tako
    da pad baze NIKAD ne može da proširi pristup. Admin i direktor zadržavaju
    pristup preko provere uloge uzvodno (`user_has_module_access`).
    """
    locked = deepcopy(default_access)
    for module_info in locked.values():
        if isinstance(module_info, dict):
            module_info['default_access'] = False
            module_info['authorized_users'] = []
            module_info['restricted_users'] = []
    return locked


def load_module_access_data(
    *,
    module_access_file,
    current_mtime,
    default_access,
    get_postgres_connection: Optional[Callable[[], Any]] = None,
):
    """Load and merge persisted module access overrides into defaults.

    Pri padu baze bez last-known-good vrednosti ponaša se fail-closed (najrestriktivnije)
    umesto da tiho vrati permisivne podrazumevane dozvole.
    """
    merged_access = deepcopy(default_access)
    try:
        saved_access = load_json_settings_data(
            setting_key='module_access',
            default_value={},
            get_postgres_connection=get_postgres_connection,
            file_path=module_access_file,
            current_mtime=current_mtime,
        )
    except SharedSettingsUnavailable:
        logger.error(
            "Modul-pristup nedostupan i nema last-known-good u kešu; prelazim na "
            "fail-closed (najrestriktivniji pristup) dok se PostgreSQL ne oporavi"
        )
        return _fail_closed_module_access(default_access)

    try:
        for module_key, module_data in (saved_access or {}).items():
            if module_key in merged_access:
                if 'authorized_users' in module_data:
                    merged_access[module_key]['authorized_users'] = module_data['authorized_users']
                if 'restricted_users' in module_data:
                    merged_access[module_key]['restricted_users'] = module_data['restricted_users']
    except Exception as exc:
        logger.error("Error merging module access overrides: %s; failing closed", exc)
        return _fail_closed_module_access(default_access)

    return merged_access


def save_module_access_data(
    *,
    module_access_file,
    module_access,
    get_postgres_connection: Optional[Callable[[], Any]] = None,
):
    """Persist module access overrides to JSON."""
    try:
        access_data = {}
        for module_key, module_info in module_access.items():
            module_data = {}
            if 'authorized_users' in module_info:
                module_data['authorized_users'] = module_info['authorized_users']
            if 'restricted_users' in module_info:
                module_data['restricted_users'] = module_info['restricted_users']
            if module_data:
                access_data[module_key] = module_data

        return save_json_settings_data(
            setting_key='module_access',
            payload=access_data,
            get_postgres_connection=get_postgres_connection,
            file_path=module_access_file,
        )
    except Exception as exc:
        logger.error("Error saving module access: %s", exc)
        return False


def load_dashboard_preferences_data(
    *,
    dashboard_prefs_file,
    current_mtime,
    default_prefs,
    get_postgres_connection: Optional[Callable[[], Any]] = None,
):
    """Load dashboard preferences or return defaults when unavailable.

    Dashboard preferencije nisu kontrola pristupa, pa pad baze bez last-known-good
    pada na podrazumevane vrednosti — ali se greška LOGUJE na ERROR nivou umesto
    da se proguta tiho (last-known-good služi sam :func:`load_json_settings_data`).
    """
    try:
        return load_json_settings_data(
            setting_key='dashboard_preferences',
            default_value=default_prefs,
            get_postgres_connection=get_postgres_connection,
            file_path=dashboard_prefs_file,
            current_mtime=current_mtime,
        )
    except SharedSettingsUnavailable:
        logger.error(
            "Dashboard preferencije nedostupne i nema last-known-good u kešu; "
            "koristim podrazumevane dok se PostgreSQL ne oporavi"
        )
        return deepcopy(default_prefs)


def save_dashboard_preferences_data(
    *,
    dashboard_prefs_file,
    dashboard_preferences,
    get_postgres_connection: Optional[Callable[[], Any]] = None,
):
    """Persist dashboard preferences to JSON."""
    try:
        return save_json_settings_data(
            setting_key='dashboard_preferences',
            payload=dashboard_preferences,
            get_postgres_connection=get_postgres_connection,
            file_path=dashboard_prefs_file,
        )
    except Exception as exc:
        logger.error("Error saving dashboard preferences: %s", exc)
        return False
