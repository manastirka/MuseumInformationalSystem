"""Per-user dashboard element configuration (sections and module cards)."""

import json
import logging

from postgres_service import get_postgres_connection

logger = logging.getLogger(__name__)

USER_DASHBOARD_CONFIG_TABLE = 'user_dashboard_config'

# Fixed dashboard sections (non-module elements). Every logged-in role may
# see them, so their access condition is simply "any authenticated user".
DASHBOARD_SECTIONS = {
    'social_feeds': {
        'name': 'Друштвене мреже музеја',
        'description': 'Facebook и Instagram странице Природњачког музеја',
        'icon': 'bi-broadcast',
    },
    'website_news': {
        'name': 'Вести са веб сајта',
        'description': 'Најновије вести са nhmbeo.rs',
        'icon': 'bi-globe',
    },
}

# Default elements for a regular employee without a saved configuration.
DEFAULT_REGULAR_ELEMENTS = ('timesheet', 'news', 'website_news')

# Roles that keep the pre-existing full dashboard by default.
PRIVILEGED_DASHBOARD_ROLES = frozenset({
    'admin',
    'direktor',
    'sef_odeljenja',
    'sef_pravne_sluzbe',
    'sef_racunovodstva',
})


def is_privileged_dashboard_role(user_role):
    """Return True when the role keeps the legacy full dashboard by default."""
    return user_role in PRIVILEGED_DASHBOARD_ROLES


def get_allowed_element_keys(
    user_email,
    user_role,
    *,
    module_access,
    user_has_module_access,
):
    """Return every dashboard element key this user is allowed to see."""
    allowed = list(DASHBOARD_SECTIONS.keys())
    for module_key in module_access:
        if user_has_module_access(user_email, user_role, module_key):
            allowed.append(module_key)
    return allowed


def load_user_dashboard_elements(user_email, *, get_connection=get_postgres_connection):
    """Return the saved element list for a user, or None when unset/unavailable."""
    if not user_email:
        return None
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    f"SELECT enabled_elements FROM {USER_DASHBOARD_CONFIG_TABLE} "
                    "WHERE user_email = %s",
                    (user_email,),
                )
                row = cur.fetchone()
        if not row:
            return None
        value = row[0] if isinstance(row, (list, tuple)) else row['enabled_elements']
        if isinstance(value, str):
            value = json.loads(value)
        if isinstance(value, list):
            return [str(item) for item in value]
        return None
    except Exception as exc:
        logger.warning("Could not load dashboard config for %s: %s", user_email, exc)
        return None


def save_user_dashboard_elements(user_email, elements, *, get_connection=get_postgres_connection):
    """Persist the user's selected dashboard elements. Returns True on success."""
    if not user_email:
        return False
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    f"""
                    INSERT INTO {USER_DASHBOARD_CONFIG_TABLE} (user_email, enabled_elements, updated_at)
                    VALUES (%s, %s::jsonb, NOW())
                    ON CONFLICT (user_email) DO UPDATE SET
                        enabled_elements = EXCLUDED.enabled_elements,
                        updated_at = NOW()
                    """,
                    (user_email, json.dumps(list(elements), ensure_ascii=False)),
                )
            conn.commit()
        return True
    except Exception as exc:
        logger.error("Could not save dashboard config for %s: %s", user_email, exc)
        return False


def resolve_enabled_elements(
    user_email,
    user_role,
    *,
    allowed_keys,
    saved_elements,
    legacy_enabled_widgets,
    admin_widget_users,
    module_keys,
):
    """Return the effective element list for the dashboard.

    Priority: saved per-user config (new table) -> legacy JSON preferences ->
    role-based default. The result is always filtered by allowed_keys, so an
    element the user can no longer access is silently skipped.
    """
    allowed = set(allowed_keys)

    if saved_elements is not None:
        return [key for key in saved_elements if key in allowed]

    if legacy_enabled_widgets is not None:
        # Legacy preferences predate configurable sections: sections stay on.
        elements = list(DASHBOARD_SECTIONS.keys()) + list(legacy_enabled_widgets)
        return [key for key in elements if key in allowed]

    if is_privileged_dashboard_role(user_role) or user_email in admin_widget_users:
        if user_role == 'admin' or user_email in admin_widget_users:
            default_modules = ['museum_databases']
        else:
            default_modules = list(module_keys)
        elements = list(DASHBOARD_SECTIONS.keys()) + default_modules
        return [key for key in elements if key in allowed]

    return [key for key in DEFAULT_REGULAR_ELEMENTS if key in allowed]
