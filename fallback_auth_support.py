"""Shared fallback employee and authentication helpers."""


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
    admin_username = app_config.get('ADMIN_USERNAME', 'admin')

    if not admin_password:
        logger.error(
            "Fallback authentication is enabled but ADMIN_DEFAULT_PASSWORD is not configured"
        )
        return None

    normalized_email = email.strip().lower()
    admin_aliases = {
        admin_email.lower(),
        admin_username.lower(),
        'admin',
    }

    if normalized_email not in admin_aliases or password != admin_password:
        return None

    stored_email = admin_email if normalized_email == admin_email.lower() else (admin_username or admin_email)
    return {
        'user_id': 1,
        'email': stored_email.lower(),
        'full_name': 'System Administrator',
        'department': 'Administration',
        'position': 'Administrator',
        'role': 'admin',
        'is_first_login': True,
    }
