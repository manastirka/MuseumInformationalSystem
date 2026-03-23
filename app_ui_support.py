"""Shared dashboard and collection-page helper functions."""

from flask import request


DEFAULT_ADMIN_WIDGET_USERS = [
    'admin',
    'slavko.spasic@nhmbeo.rs',
    'biljana.mitrovic@nhmbeo.rs',
    'verica.stojanovic@nhmbeo.rs',
]


def get_user_modules(
    user_email,
    user_role,
    *,
    load_module_access,
    load_dashboard_preferences,
    dashboard_preferences,
    module_access,
    user_has_module_access,
    admin_users=None,
):
    """Get dashboard modules visible to the current user."""
    module_access = load_module_access() or module_access
    dashboard_preferences = load_dashboard_preferences() or dashboard_preferences

    accessible_modules = []
    admin_users = admin_users or DEFAULT_ADMIN_WIDGET_USERS
    enabled_widgets = dashboard_preferences.get(user_email, {}).get('enabled_widgets')

    if enabled_widgets is None:
        if user_email in admin_users or user_role == 'admin':
            enabled_widgets = ['museum_databases']
        else:
            enabled_widgets = list(module_access.keys())

    for module_key, module_info in module_access.items():
        if user_has_module_access(user_email, user_role, module_key) and module_key in enabled_widgets:
            accessible_modules.append(
                {
                    'key': module_key,
                    'name': module_info['name'],
                    'description': module_info['description'],
                    'icon': module_info['icon'],
                }
            )

    return accessible_modules


def prepare_collection_records_for_display(collection_type, records, *, apply_qr_highlight_filter):
    """Apply QR highlight filtering for collection pages and return the active highlight."""
    highlight = request.args.get('highlight')
    prepared_records = apply_qr_highlight_filter(records, collection_type, highlight)
    return prepared_records, highlight
