"""
Security Utilities for Museum Information System
Provides password validation, rate limiting helpers, and security decorators
"""

import re
import hashlib
import secrets
from typing import Tuple, Optional, Dict, Any
from functools import wraps
from flask import session, request, flash, redirect, url_for, current_app
from datetime import datetime, timedelta


class PasswordValidator:
    """Validate passwords against security policy."""

    def __init__(self, config):
        self.min_length = config.PASSWORD_MIN_LENGTH
        self.require_uppercase = config.PASSWORD_REQUIRE_UPPERCASE
        self.require_lowercase = config.PASSWORD_REQUIRE_LOWERCASE
        self.require_numbers = config.PASSWORD_REQUIRE_NUMBERS
        self.require_special = config.PASSWORD_REQUIRE_SPECIAL

    def validate(self, password: str) -> Tuple[bool, list]:
        """
        Validate password against policy.

        Args:
            password: Password to validate

        Returns:
            Tuple of (is_valid, list_of_errors)
        """
        errors = []

        if len(password) < self.min_length:
            errors.append(f'Лозинка мора имати најмање {self.min_length} карактера')

        if self.require_uppercase and not re.search(r'[A-Z]', password):
            errors.append('Лозинка мора садржати најмање једно велико слово')

        if self.require_lowercase and not re.search(r'[a-z]', password):
            errors.append('Лозинка мора садржати најмање једно мало слово')

        if self.require_numbers and not re.search(r'\d', password):
            errors.append('Лозинка мора садржати најмање један број')

        if self.require_special and not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            errors.append('Лозинка мора садржати најмање један специјални карактер (!@#$%^&*...)')

        # Check for common weak passwords
        common_passwords = [
            'password', '12345678', 'qwerty', 'admin', 'user', 'admin123',
            'password123', 'letmein', 'welcome', '123456789', 'abc123'
        ]
        if password.lower() in common_passwords:
            errors.append('Лозинка је превише једноставна. Избегавајте честе лозинке.')

        return len(errors) == 0, errors

    def generate_strong_password(self, length: int = 16) -> str:
        """Generate a cryptographically secure random password."""
        alphabet = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()'
        password = ''.join(secrets.choice(alphabet) for _ in range(length))

        # Ensure it meets all requirements
        if self.validate(password)[0]:
            return password
        else:
            return self.generate_strong_password(length)  # Retry if validation fails


class PasswordHasher:
    """Secure password hashing and verification."""

    @staticmethod
    def hash_password(password: str, salt: Optional[str] = None) -> Tuple[str, str]:
        """
        Hash password with salt using SHA-512.

        Args:
            password: Plain text password
            salt: Optional salt (generated if not provided)

        Returns:
            Tuple of (password_hash, salt)
        """
        if salt is None:
            salt = secrets.token_hex(16)

        password_hash = hashlib.sha512((password + salt).encode()).hexdigest()
        return password_hash, salt

    @staticmethod
    def verify_password(password: str, stored_hash: str, salt: str) -> bool:
        """
        Verify password against stored hash.

        Args:
            password: Plain text password to verify
            stored_hash: Stored password hash
            salt: Salt used for hashing

        Returns:
            True if password matches, False otherwise
        """
        hash_to_check, _ = PasswordHasher.hash_password(password, salt)
        return secrets.compare_digest(hash_to_check, stored_hash)


class LoginAttemptTracker:
    """Track and limit login attempts to prevent brute force attacks."""

    def __init__(self):
        # In-memory storage for simplicity
        # For production, use Redis for distributed systems
        self.attempts: Dict[str, list] = {}
        self.lockouts: Dict[str, datetime] = {}

    def record_attempt(self, email: str, success: bool = False) -> None:
        """Record a login attempt."""
        if success:
            # Clear attempts on successful login
            self.attempts.pop(email, None)
            self.lockouts.pop(email, None)
        else:
            # Record failed attempt
            if email not in self.attempts:
                self.attempts[email] = []

            self.attempts[email].append(datetime.utcnow())

            # Keep only recent attempts (last hour)
            cutoff = datetime.utcnow() - timedelta(hours=1)
            self.attempts[email] = [
                attempt for attempt in self.attempts[email]
                if attempt > cutoff
            ]

    def is_locked_out(self, email: str, max_attempts: int, lockout_duration: int) -> Tuple[bool, Optional[int]]:
        """
        Check if account is locked out.

        Args:
            email: User email
            max_attempts: Maximum allowed attempts
            lockout_duration: Lockout duration in seconds

        Returns:
            Tuple of (is_locked, seconds_remaining)
        """
        # Check if explicitly locked out
        if email in self.lockouts:
            lockout_end = self.lockouts[email]
            if datetime.utcnow() < lockout_end:
                remaining = int((lockout_end - datetime.utcnow()).total_seconds())
                return True, remaining
            else:
                # Lockout expired
                self.lockouts.pop(email)
                self.attempts.pop(email, None)
                return False, None

        # Check attempt count
        attempts = self.attempts.get(email, [])
        if len(attempts) >= max_attempts:
            # Lock out the account
            self.lockouts[email] = datetime.utcnow() + timedelta(seconds=lockout_duration)
            return True, lockout_duration

        return False, None

    def get_remaining_attempts(self, email: str, max_attempts: int) -> int:
        """Get number of remaining login attempts."""
        attempts = len(self.attempts.get(email, []))
        return max(0, max_attempts - attempts)


# Global instance
login_tracker = LoginAttemptTracker()


def login_required(f):
    """Decorator to require login for a route."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Морате бити пријављени да бисте приступили овој страници.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


def admin_required(f):
    """Decorator to require admin role for a route."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        from flask import request, jsonify

        # Check if this is an API request
        is_api_request = request.path.startswith('/api/')

        if 'user_id' not in session:
            if is_api_request:
                return jsonify({'success': False, 'message': 'Морате бити пријављени'}), 401
            flash('Морате бити пријављени да бисте приступили овој страници.', 'warning')
            return redirect(url_for('login'))

        if session.get('user_role') != 'admin':
            if is_api_request:
                return jsonify({'success': False, 'message': 'Немате дозволу за приступ'}), 403
            flash('Немате дозволу за приступ овој страници.', 'danger')
            return redirect(url_for('dashboard'))

        return f(*args, **kwargs)
    return decorated_function


def module_access_required(module_key):
    """Decorator to require module access for a route.

    Use this instead of @admin_required when you want to allow
    non-admin users with granted module access.

    Usage:
        @app.route('/admin/library_database')
        @module_access_required('library_database')
        def library_database():
            ...
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            from flask import request, jsonify
            # Import here to avoid circular imports
            from app import user_has_module_access

            is_api_request = request.path.startswith('/api/')

            if 'user_id' not in session:
                if is_api_request:
                    return jsonify({'success': False, 'message': 'Морате бити пријављени'}), 401
                flash('Морате бити пријављени да бисте приступили овој страници.', 'warning')
                return redirect(url_for('login'))

            user_email = session.get('user_email', '')
            user_role = session.get('user_role', '')

            if not user_has_module_access(user_email, user_role, module_key):
                if is_api_request:
                    return jsonify({'success': False, 'message': 'Немате дозволу за приступ овом модулу'}), 403
                flash('Немате дозволу за приступ овом модулу.', 'danger')
                return redirect(url_for('dashboard'))

            return f(*args, **kwargs)
        return decorated_function
    return decorator


def csrf_exempt(f):
    """Decorator to exempt a route from CSRF protection."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        return f(*args, **kwargs)
    # Mark function as CSRF exempt
    decorated_function.csrf_exempt = True
    return decorated_function


def generate_secure_token(length: int = 32) -> str:
    """Generate a cryptographically secure random token."""
    return secrets.token_urlsafe(length)


def sanitize_filename(filename: str) -> str:
    """Sanitize filename to prevent directory traversal attacks."""
    # Remove any path components
    filename = filename.replace('\\', '/').split('/')[-1]

    # Remove dangerous characters
    filename = re.sub(r'[^\w\s.-]', '', filename)

    # Limit length
    if len(filename) > 255:
        name, ext = filename.rsplit('.', 1) if '.' in filename else (filename, '')
        filename = name[:255-len(ext)-1] + '.' + ext if ext else name[:255]

    return filename


def allowed_file(filename: str, allowed_extensions: set) -> bool:
    """Check if file extension is allowed."""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in allowed_extensions


def get_client_ip() -> str:
    """Get client IP address, considering proxy headers."""
    if request.headers.get('X-Forwarded-For'):
        # Behind proxy
        ip = request.headers.get('X-Forwarded-For').split(',')[0].strip()
    elif request.headers.get('X-Real-IP'):
        ip = request.headers.get('X-Real-IP')
    else:
        ip = request.remote_addr or 'unknown'

    return ip


def log_security_event(event_type: str, details: Dict[str, Any]) -> None:
    """Log security-related events."""
    import logging
    logger = logging.getLogger('security')

    event_data = {
        'type': event_type,
        'timestamp': datetime.utcnow().isoformat(),
        'ip_address': get_client_ip(),
        'user_agent': request.headers.get('User-Agent', 'unknown'),
        'user_email': session.get('user', {}).get('email', 'anonymous'),
        **details
    }

    if event_type in ['login_failed', 'account_locked', 'unauthorized_access']:
        logger.warning(f"Security event: {event_type}", extra=event_data)
    elif event_type in ['password_changed', 'login_success']:
        logger.info(f"Security event: {event_type}", extra=event_data)
    else:
        logger.debug(f"Security event: {event_type}", extra=event_data)
