"""Runtime state helpers used by the main Flask app bootstrap."""

from typing import Any, Callable


def get_file_mtime(path: str):
    """Return the current file mtime, or None when the file is absent."""
    import os

    try:
        return os.path.getmtime(path)
    except OSError:
        return None


def load_module_access_state(
    *,
    current_state,
    stored_mtime,
    file_mtime,
    force: bool,
    use_shared_db: bool,
    module_access_file: str,
    module_access_defaults,
    get_postgres_connection,
    load_module_access_data,
):
    """Resolve the current module-access payload and updated cache mtime."""
    if not use_shared_db and not force and file_mtime == stored_mtime:
        return current_state, stored_mtime

    new_state = load_module_access_data(
        module_access_file=module_access_file,
        current_mtime=file_mtime,
        default_access=module_access_defaults,
        get_postgres_connection=get_postgres_connection if use_shared_db else None,
    )
    new_mtime = None if use_shared_db else file_mtime
    return new_state, new_mtime


def save_module_access_state(
    *,
    module_access_file: str,
    module_access,
    use_shared_db: bool,
    get_postgres_connection,
    save_module_access_data,
    get_file_mtime_func: Callable[[str], Any],
):
    """Persist module-access data and return success plus updated mtime."""
    saved = save_module_access_data(
        module_access_file=module_access_file,
        module_access=module_access,
        get_postgres_connection=get_postgres_connection if use_shared_db else None,
    )
    if not saved:
        return False, None
    return True, (None if use_shared_db else get_file_mtime_func(module_access_file))


def load_dashboard_preferences_state(
    *,
    current_state,
    stored_mtime,
    file_mtime,
    force: bool,
    use_shared_db: bool,
    dashboard_prefs_file: str,
    default_prefs,
    get_postgres_connection,
    load_dashboard_preferences_data,
):
    """Resolve dashboard preferences and updated cache mtime."""
    if not use_shared_db and not force and file_mtime == stored_mtime:
        return current_state, stored_mtime

    new_state = load_dashboard_preferences_data(
        dashboard_prefs_file=dashboard_prefs_file,
        current_mtime=file_mtime,
        default_prefs=default_prefs,
        get_postgres_connection=get_postgres_connection if use_shared_db else None,
    )
    new_mtime = None if use_shared_db else file_mtime
    return new_state, new_mtime


def save_dashboard_preferences_state(
    *,
    dashboard_prefs_file: str,
    dashboard_preferences,
    use_shared_db: bool,
    get_postgres_connection,
    save_dashboard_preferences_data,
    get_file_mtime_func: Callable[[str], Any],
):
    """Persist dashboard preferences and return success plus updated mtime."""
    saved = save_dashboard_preferences_data(
        dashboard_prefs_file=dashboard_prefs_file,
        dashboard_preferences=dashboard_preferences,
        get_postgres_connection=get_postgres_connection if use_shared_db else None,
    )
    if not saved:
        return False, None
    return True, (None if use_shared_db else get_file_mtime_func(dashboard_prefs_file))


def get_cached_value(*, current_value, force_reload: bool, loader):
    """Resolve a cached value, loading it only on first use or explicit refresh."""
    if force_reload or current_value is None:
        return loader()
    return current_value
