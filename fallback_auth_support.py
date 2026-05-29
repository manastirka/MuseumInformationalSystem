"""Shared fallback employee and authentication helpers."""

import secrets


_DISALLOWED_FALLBACK_PASSWORDS = {
    'Museum2025!Secure',
}


def get_fallback_employees(app_config):
    """
    Return fallback employee data for development/testing only.

    This must never be enabled in production.
    """
    if not app_config.get('ENABLE_FALLBACK_AUTH', False):
        return {}

    admin_email = app_config.get('ADMIN_EMAIL', 'admin@nhmbeo.rs')
    return {
        admin_email: {
            'user_id': 1,
            'email': admin_email,
            'full_name': 'System Administrator',
            'department': 'Administration',
            'position': 'System Administrator',
            'role': 'admin',
            'requires_password_check': True,
            'description': 'Администратор информационог система музеја.',
        }
    }


def authenticate_fallback_user(email, password, *, app_config, logger):
    """
    Authenticate a user against the configured fallback admin account.

    Development only. Do not use in production.
    """
    if not app_config.get('ENABLE_FALLBACK_AUTH', False):
        return None

    admin_email = app_config.get('ADMIN_EMAIL', 'admin@nhmbeo.rs')
    admin_password = app_config.get('ADMIN_DEFAULT_PASSWORD')
    admin_username = (app_config.get('ADMIN_USERNAME') or '').strip()

    if not admin_password:
        logger.error(
            "Fallback authentication is enabled but ADMIN_DEFAULT_PASSWORD is not configured"
        )
        return None
    if admin_password in _DISALLOWED_FALLBACK_PASSWORDS:
        logger.error(
            "Fallback authentication is enabled with a blocked bootstrap password; rotate ADMIN_DEFAULT_PASSWORD"
        )
        return None

    normalized_email = email.strip().lower()
    admin_aliases = {admin_email.lower()}
    if admin_username:
        admin_aliases.add(admin_username.lower())

    if normalized_email not in admin_aliases:
        return None
    if not secrets.compare_digest(password, admin_password):
        return None

    return {
        'user_id': 1,
        'email': admin_email.lower(),
        'full_name': 'System Administrator',
        'department': 'Administration',
        'position': 'Administrator',
        'role': 'admin',
        'is_first_login': True,
        'auth_source': 'fallback',
        'login_identifier': normalized_email,
    }
