"""Shared persistence helpers for module access and dashboard preferences."""

import json
import logging
import os
from copy import deepcopy
from typing import Any, Callable, Optional


logger = logging.getLogger(__name__)
SHARED_SETTINGS_TABLE = 'app_shared_settings'


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
    """Load a JSON setting blob from PostgreSQL."""
    if get_postgres_connection is None:
        return None

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
                    return None
                value = row[0] if isinstance(row, tuple) else row['setting_value']
                if isinstance(value, str):
                    return json.loads(value)
                return value
    except Exception as exc:
        logger.warning("Falling back to file storage for %s: %s", setting_key, exc)
        return None


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
    """Load shared JSON settings from PostgreSQL first, then file fallback."""
    db_value = _load_db_json_setting(
        get_postgres_connection=get_postgres_connection,
        setting_key=setting_key,
    )
    if isinstance(db_value, dict):
        logger.info("Loaded %s from PostgreSQL shared settings", setting_key)
        return db_value

    try:
        if file_path and current_mtime is not None:
            with open(file_path, 'r', encoding='utf-8') as handle:
                file_value = json.load(handle)
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
    """Save shared JSON settings to PostgreSQL and optional file fallback."""
    saved_to_db = _save_db_json_setting(
        get_postgres_connection=get_postgres_connection,
        setting_key=setting_key,
        payload=payload,
    )

    saved_to_file = False
    if file_path:
        try:
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, 'w', encoding='utf-8') as handle:
                json.dump(payload, handle, ensure_ascii=False, indent=2)
            logger.info("Saved %s to %s", setting_key, file_path)
            saved_to_file = True
        except Exception as exc:
            logger.error("Error saving %s to file: %s", setting_key, exc)

    return saved_to_db or saved_to_file


def load_module_access_data(
    *,
    module_access_file,
    current_mtime,
    default_access,
    get_postgres_connection: Optional[Callable[[], Any]] = None,
):
    """Load and merge persisted module access overrides into defaults."""
    merged_access = deepcopy(default_access)
    try:
        saved_access = load_json_settings_data(
            setting_key='module_access',
            default_value={},
            get_postgres_connection=get_postgres_connection,
            file_path=module_access_file,
            current_mtime=current_mtime,
        )
        for module_key, module_data in saved_access.items():
            if module_key in merged_access:
                if 'authorized_users' in module_data:
                    merged_access[module_key]['authorized_users'] = module_data['authorized_users']
                if 'restricted_users' in module_data:
                    merged_access[module_key]['restricted_users'] = module_data['restricted_users']
    except Exception as exc:
        logger.error("Error loading module access: %s", exc)
        merged_access = deepcopy(default_access)

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
            if 'authorized_users' in module_info and module_info['authorized_users']:
                module_data['authorized_users'] = module_info['authorized_users']
            if 'restricted_users' in module_info and module_info['restricted_users']:
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
    """Load dashboard preferences or return defaults when unavailable."""
    try:
        return load_json_settings_data(
            setting_key='dashboard_preferences',
            default_value=default_prefs,
            get_postgres_connection=get_postgres_connection,
            file_path=dashboard_prefs_file,
            current_mtime=current_mtime,
        )
    except Exception as exc:
        logger.error("Error loading dashboard preferences: %s", exc)

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
