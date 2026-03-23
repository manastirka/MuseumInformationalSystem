"""Shared persistence helpers for module access and dashboard preferences."""

import json
import logging
import os
from copy import deepcopy


logger = logging.getLogger(__name__)


def load_module_access_data(*, module_access_file, current_mtime, default_access):
    """Load and merge persisted module access overrides into defaults."""
    merged_access = deepcopy(default_access)
    try:
        if current_mtime is not None:
            with open(module_access_file, 'r', encoding='utf-8') as handle:
                saved_access = json.load(handle)
                for module_key, module_data in saved_access.items():
                    if module_key in merged_access:
                        if 'authorized_users' in module_data:
                            merged_access[module_key]['authorized_users'] = module_data['authorized_users']
                        if 'restricted_users' in module_data:
                            merged_access[module_key]['restricted_users'] = module_data['restricted_users']
            logger.info("Loaded module access settings from %s", module_access_file)
    except Exception as exc:
        logger.error("Error loading module access: %s", exc)
        merged_access = deepcopy(default_access)

    return merged_access


def save_module_access_data(*, module_access_file, module_access):
    """Persist module access overrides to JSON."""
    try:
        os.makedirs(os.path.dirname(module_access_file), exist_ok=True)
        access_data = {}
        for module_key, module_info in module_access.items():
            module_data = {}
            if 'authorized_users' in module_info and module_info['authorized_users']:
                module_data['authorized_users'] = module_info['authorized_users']
            if 'restricted_users' in module_info and module_info['restricted_users']:
                module_data['restricted_users'] = module_info['restricted_users']
            if module_data:
                access_data[module_key] = module_data

        with open(module_access_file, 'w', encoding='utf-8') as handle:
            json.dump(access_data, handle, ensure_ascii=False, indent=2)

        logger.info("Saved module access settings to %s", module_access_file)
        return True
    except Exception as exc:
        logger.error("Error saving module access: %s", exc)
        return False


def load_dashboard_preferences_data(*, dashboard_prefs_file, current_mtime, default_prefs):
    """Load dashboard preferences or return defaults when unavailable."""
    try:
        if current_mtime is not None:
            with open(dashboard_prefs_file, 'r', encoding='utf-8') as handle:
                preferences = json.load(handle)
            logger.info("Loaded dashboard preferences from %s", dashboard_prefs_file)
            return preferences
    except Exception as exc:
        logger.error("Error loading dashboard preferences: %s", exc)

    return deepcopy(default_prefs)


def save_dashboard_preferences_data(*, dashboard_prefs_file, dashboard_preferences):
    """Persist dashboard preferences to JSON."""
    try:
        os.makedirs(os.path.dirname(dashboard_prefs_file), exist_ok=True)
        with open(dashboard_prefs_file, 'w', encoding='utf-8') as handle:
            json.dump(dashboard_preferences, handle, ensure_ascii=False, indent=2)

        logger.info("Saved dashboard preferences to %s", dashboard_prefs_file)
        return True
    except Exception as exc:
        logger.error("Error saving dashboard preferences: %s", exc)
        return False
