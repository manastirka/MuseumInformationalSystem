"""
Security Utilities for Museum Information System
Provides password validation, rate limiting helpers, and security decorators
"""

import re
import hashlib
import secrets
import logging
from typing import Tuple, Optional, Dict, Any, Union
from functools import wraps
from flask import session, request, flash, redirect, url_for, current_app
from datetime import UTC, datetime, timedelta

try:
    import bcrypt
    BCRYPT_AVAILABLE = True
except ImportError:
    BCRYPT_AVAILABLE = False
    logging.critical("bcrypt not installed! Password hashing will use weak SHA-512 fallback. "
                     "Install bcrypt: pip install bcrypt")

try:
    import redis
    REDIS_AVAILABLE = True
except ImportError:
    REDIS_AVAILABLE = False


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
        for _ in range(100):  # Max 100 attempts instead of unbounded recursion
            password = ''.join(secrets.choice(alphabet) for _ in range(length))
            if self.validate(password)[0]:
                return password
        # If we still can't generate a valid password, return the last attempt
        return password


class PasswordHasher:
    """Secure password hashing and verification using bcrypt.

    Bcrypt is designed for password hashing with:
    - Built-in salt generation
    - Configurable work factor (cost)
    - Resistance to GPU/ASIC attacks

    Maintains backward compatibility with legacy SHA-512 hashes.
    """

    # Bcrypt work factor (cost) - 12 is a good balance of security and performance
    # Each increment doubles the computation time
    BCRYPT_ROUNDS = 12

    @staticmethod
    def hash_password(password: str, salt: Optional[str] = None) -> Tuple[str, str]:
        """
        Hash password using bcrypt (preferred) or SHA-512 (fallback).

        Args:
            password: Plain text password
            salt: Optional salt (ignored for bcrypt, used for SHA-512 fallback)

        Returns:
            Tuple of (password_hash, salt)
            For bcrypt: salt is embedded in hash, returned as empty string
        """
        if BCRYPT_AVAILABLE:
            # Bcrypt handles salt internally
            password_bytes = password.encode('utf-8')
            hashed = bcrypt.hashpw(password_bytes, bcrypt.gensalt(rounds=PasswordHasher.BCRYPT_ROUNDS))
            # Return hash as string, empty salt (bcrypt embeds salt in hash)
            return hashed.decode('utf-8'), ''
        else:
            # Fallback to SHA-512 (not recommended for production)
            if salt is None:
                salt = secrets.token_hex(16)
            password_hash = hashlib.sha512((password + salt).encode()).hexdigest()
            return password_hash, salt

    @staticmethod
    def verify_password(password: str, stored_hash: str, salt: str) -> bool:
        """
        Verify password against stored hash.

        Automatically detects hash type (bcrypt vs SHA-512) for backward compatibility.

        Args:
            password: Plain text password to verify
            stored_hash: Stored password hash
            salt: Salt used for hashing (empty for bcrypt)

        Returns:
            True if password matches, False otherwise
        """
        # Detect bcrypt hash (starts with $2a$, $2b$, or $2y$)
        if stored_hash.startswith(('$2a$', '$2b$', '$2y$')):
            if not BCRYPT_AVAILABLE:
                logging.error("Cannot verify bcrypt hash - bcrypt module not installed")
                return False
            try:
                return bcrypt.checkpw(
                    password.encode('utf-8'),
                    stored_hash.encode('utf-8')
                )
            except Exception as e:
                logging.error(f"Bcrypt verification error: {e}")
                return False
        else:
            # Legacy SHA-512 verification
            hash_to_check = hashlib.sha512((password + salt).encode()).hexdigest()
            return secrets.compare_digest(hash_to_check, stored_hash)

    @staticmethod
    def needs_rehash(stored_hash: str) -> bool:
        """
        Check if password needs to be rehashed (e.g., upgrade from SHA-512 to bcrypt).

        Args:
            stored_hash: Currently stored password hash

        Returns:
            True if password should be rehashed on next login
        """
        if not BCRYPT_AVAILABLE:
            return False

        # SHA-512 hashes are 128 hex characters, bcrypt hashes start with $2
        if not stored_hash.startswith(('$2a$', '$2b$', '$2y$')):
            return True  # Legacy hash, needs upgrade

        # Check if bcrypt cost factor is outdated
        try:
            # Extract rounds from bcrypt hash (format: $2b$12$...)
            parts = stored_hash.split('$')
            if len(parts) >= 3:
                current_rounds = int(parts[2])
                if current_rounds < PasswordHasher.BCRYPT_ROUNDS:
                    return True  # Work factor too low
        except (ValueError, IndexError):
            pass

        return False


class LoginAttemptTracker:
    """Track and limit login attempts to prevent brute force attacks.

    Uses Redis for distributed tracking across multiple workers when available,
    falls back to in-memory storage for development/single-worker deployments.
    """

    def __init__(self, redis_url: Optional[str] = None):
        """
        Initialize tracker with optional Redis backend.

        Args:
            redis_url: Redis connection URL (e.g., 'redis://localhost:6379/0')
        """
        self.redis_client = None
        self.use_redis = False

        # Try to connect to Redis if available
        if REDIS_AVAILABLE and redis_url:
            try:
                self.redis_client = redis.from_url(redis_url, decode_responses=True)
                self.redis_client.ping()  # Test connection
                self.use_redis = True
                logging.info("LoginAttemptTracker: Using Redis backend")
            except Exception as e:
                logging.warning(f"LoginAttemptTracker: Redis unavailable ({e}), using in-memory")

        # In-memory fallback
        self.attempts: Dict[str, list] = {}
        self.lockouts: Dict[str, datetime] = {}

    def _redis_key(self, prefix: str, email: str) -> str:
        """Generate Redis key for email."""
        # Sanitize email for use as Redis key
        safe_email = email.lower().replace('@', '_at_').replace('.', '_')
        return f"login_tracker:{prefix}:{safe_email}"

    def record_attempt(self, email: str, success: bool = False) -> None:
        """Record a login attempt."""
        if self.use_redis:
            self._record_attempt_redis(email, success)
        else:
            self._record_attempt_memory(email, success)

    def _record_attempt_redis(self, email: str, success: bool) -> None:
        """Record attempt in Redis."""
        attempts_key = self._redis_key("attempts", email)
        lockout_key = self._redis_key("lockout", email)

        if success:
            # Clear attempts on successful login
            self.redis_client.delete(attempts_key, lockout_key)
        else:
            # Record failed attempt with 1 hour TTL
            pipe = self.redis_client.pipeline()
            pipe.lpush(attempts_key, datetime.utcnow().isoformat())
            pipe.ltrim(attempts_key, 0, 99)  # Keep max 100 attempts
            pipe.expire(attempts_key, 3600)  # 1 hour TTL
            pipe.execute()

    def _record_attempt_memory(self, email: str, success: bool) -> None:
        """Record attempt in memory (fallback)."""
        if success:
            self.attempts.pop(email, None)
            self.lockouts.pop(email, None)
        else:
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
        if self.use_redis:
            return self._is_locked_out_redis(email, max_attempts, lockout_duration)
        else:
            return self._is_locked_out_memory(email, max_attempts, lockout_duration)

    def _is_locked_out_redis(self, email: str, max_attempts: int, lockout_duration: int) -> Tuple[bool, Optional[int]]:
        """Check lockout status in Redis."""
        lockout_key = self._redis_key("lockout", email)
        attempts_key = self._redis_key("attempts", email)

        # Check explicit lockout
        lockout_ttl = self.redis_client.ttl(lockout_key)
        if lockout_ttl > 0:
            return True, lockout_ttl

        # Check attempt count
        attempt_count = self.redis_client.llen(attempts_key)
        if attempt_count >= max_attempts:
            # Lock out the account and clear the counter so the lockout does
            # not re-trigger from the stale attempts list once it expires.
            self.redis_client.setex(lockout_key, lockout_duration, "locked")
            self.redis_client.delete(attempts_key)
            return True, lockout_duration

        return False, None

    def _is_locked_out_memory(self, email: str, max_attempts: int, lockout_duration: int) -> Tuple[bool, Optional[int]]:
        """Check lockout status in memory (fallback)."""
        # Check if explicitly locked out
        if email in self.lockouts:
            lockout_end = self.lockouts[email]
            if datetime.utcnow() < lockout_end:
                remaining = int((lockout_end - datetime.utcnow()).total_seconds())
                return True, remaining
            else:
                self.lockouts.pop(email)
                self.attempts.pop(email, None)
                return False, None

        # Check attempt count
        attempts = self.attempts.get(email, [])
        if len(attempts) >= max_attempts:
            self.lockouts[email] = datetime.utcnow() + timedelta(seconds=lockout_duration)
            return True, lockout_duration

        return False, None

    def get_remaining_attempts(self, email: str, max_attempts: int) -> int:
        """Get number of remaining login attempts."""
        if self.use_redis:
            attempts_key = self._redis_key("attempts", email)
            attempt_count = self.redis_client.llen(attempts_key)
        else:
            attempt_count = len(self.attempts.get(email, []))

        return max(0, max_attempts - attempt_count)


# Global instance - initialized without Redis by default
# Call init_login_tracker(redis_url) from app initialization to enable Redis
login_tracker = LoginAttemptTracker()


def init_login_tracker(redis_url: Optional[str] = None) -> LoginAttemptTracker:
    """
    Initialize or reinitialize the global login tracker with Redis support.

    Call this during app initialization with Redis URL to enable distributed tracking.

    Args:
        redis_url: Redis connection URL (e.g., 'redis://localhost:6379/0')

    Returns:
        The configured LoginAttemptTracker instance
    """
    global login_tracker
    new_tracker = LoginAttemptTracker(redis_url=redis_url)
    # Preserve object identity so already-imported references stay current.
    login_tracker.__dict__.clear()
    login_tracker.__dict__.update(new_tracker.__dict__)
    return login_tracker


def login_required(f):
    """Decorator to require login for a route."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        from flask import request, jsonify

        if 'user_id' not in session:
            # Check if this is an API request - return JSON instead of redirect
            is_api_request = request.path.startswith('/api/') or request.is_json
            if is_api_request:
                return jsonify({'success': False, 'message': 'Морате бити пријављени'}), 401

            flash('Морате бити пријављени да бисте приступили овој страници.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


def admin_required(f):
    """Decorator to require admin-level role for a route.

    The museum director (`direktor`) has full admin parity by business
    decision (2026-06): both roles pass this check. For purely technical
    routes that must stay closed to the director (password manager, SMTP,
    system settings, DB ops) use `admin_only` instead.
    """
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

        if session.get('user_role') not in ('admin', 'direktor'):
            if is_api_request:
                return jsonify({'success': False, 'message': 'Немате дозволу за приступ'}), 403
            flash('Немате дозволу за приступ овој страници.', 'danger')
            return redirect(url_for('dashboard'))

        return f(*args, **kwargs)
    return decorated_function


def admin_only(f):
    """Decorator to require strictly the `admin` role — the director does
    NOT pass (no parity here, decision 2026-08).

    Use on purely technical routes: password manager, SMTP settings,
    system settings, DB operations (backup/restore/logs).
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        from flask import request, jsonify

        is_api_request = request.path.startswith('/api/')

        if 'user_id' not in session:
            if is_api_request:
                return jsonify({'success': False, 'message': 'Морате бити пријављени'}), 401
            flash('Морате бити пријављени да бисте приступили овој страници.', 'warning')
            return redirect(url_for('login'))

        if session.get('user_role') != 'admin':
            if is_api_request:
                return jsonify({'success': False, 'message': 'Ова радња је дозвољена само администратору.'}), 403
            flash('Ова радња је дозвољена само администратору.', 'danger')
            return redirect(url_for('dashboard'))

        return f(*args, **kwargs)
    return decorated_function


def roles_required(*roles):
    """Decorator factory: allow only the listed roles (admin and direktor are
    NOT implied — list them explicitly where they should pass)."""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            from flask import request, jsonify

            is_api_request = request.path.startswith('/api/')

            if 'user_id' not in session:
                if is_api_request:
                    return jsonify({'success': False, 'message': 'Морате бити пријављени'}), 401
                flash('Морате бити пријављени да бисте приступили овој страници.', 'warning')
                return redirect(url_for('login'))

            if session.get('user_role') not in roles:
                if is_api_request:
                    return jsonify({'success': False, 'message': 'Немате дозволу за приступ'}), 403
                flash('Немате дозволу за приступ овој страници.', 'danger')
                return redirect(url_for('dashboard'))

            return f(*args, **kwargs)
        return decorated_function
    return decorator


def admin_or_department_head_required(f):
    """Allow admins, directors, or non-admins with `is_department_head=True`.

    Use on timesheet admin routes that a department head is permitted to reach
    in order to view or verify reports for their own department. The per-report
    department scoping happens inside the view itself. Directors see all
    departments (same scope as admins).
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        from flask import request, jsonify

        is_api_request = request.path.startswith('/api/')

        if 'user_id' not in session:
            if is_api_request:
                return jsonify({'success': False, 'message': 'Морате бити пријављени'}), 401
            flash('Морате бити пријављени да бисте приступили овој страници.', 'warning')
            return redirect(url_for('login'))

        if session.get('user_role') in ('admin', 'direktor'):
            return f(*args, **kwargs)

        if session.get('is_department_head'):
            return f(*args, **kwargs)

        if is_api_request:
            return jsonify({'success': False, 'message': 'Немате дозволу за приступ'}), 403
        flash('Немате дозволу за приступ овој страници.', 'danger')
        return redirect(url_for('dashboard'))

    return decorated_function


def admin_or_director_required(f):
    """Allow admins or the museum director.

    Use on business/oversight admin routes (statistics, org-wide views) that
    the director legitimately needs, but that are not purely technical. Kept
    separate from purely technical routes (password manager, SMTP, system
    settings, DB ops) which are `admin_only` (director excluded).
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        from flask import request, jsonify

        is_api_request = request.path.startswith('/api/')

        if 'user_id' not in session:
            if is_api_request:
                return jsonify({'success': False, 'message': 'Морате бити пријављени'}), 401
            flash('Морате бити пријављени да бисте приступили овој страници.', 'warning')
            return redirect(url_for('login'))

        if session.get('user_role') in ('admin', 'direktor'):
            return f(*args, **kwargs)

        if is_api_request:
            return jsonify({'success': False, 'message': 'Немате дозволу за приступ'}), 403
        flash('Немате дозволу за приступ овој страници.', 'danger')
        return redirect(url_for('dashboard'))

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
            access_checker = getattr(current_app, 'user_has_module_access', None)

            is_api_request = request.path.startswith('/api/')

            if 'user_id' not in session:
                if is_api_request:
                    return jsonify({'success': False, 'message': 'Морате бити пријављени'}), 401
                flash('Морате бити пријављени да бисте приступили овој страници.', 'warning')
                return redirect(url_for('login'))

            user_email = session.get('user_email', '')
            user_role = session.get('user_role', '')

            if access_checker is None:
                current_app.logger.error('user_has_module_access is not configured on the Flask app')
                if is_api_request:
                    return jsonify({'success': False, 'message': 'Грешка у конфигурацији апликације'}), 500
                flash('Грешка у конфигурацији апликације.', 'danger')
                return redirect(url_for('dashboard'))

            if not access_checker(user_email, user_role, module_key):
                if is_api_request:
                    return jsonify({'success': False, 'message': 'Немате дозволу за приступ овом модулу'}), 403
                flash('Немате дозволу за приступ овом модулу.', 'danger')
                return redirect(url_for('dashboard'))

            return f(*args, **kwargs)
        return decorated_function
    return decorator


def csrf_exempt(f):
    """Mark a view as CSRF-exempt for introspection only.

    NOTE: Flask-WTF's CSRFProtect does NOT honor the ``csrf_exempt`` attribute
    set here; this decorator alone does not exempt a route. Real exemption is
    applied at app init by ``app_blueprint_support.apply_csrf_exemptions``,
    which calls ``csrf.exempt(view)`` for every endpoint listed in
    ``CSRF_EXEMPT_ENDPOINTS``. To exempt a route, add its endpoint name there.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        return f(*args, **kwargs)
    # Mark function as CSRF exempt (introspection flag; see note above)
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
    """Get client IP address from Werkzeug's ProxyFix-corrected remote_addr.

    ProxyFix middleware (configured in app.py) handles X-Forwarded-For
    parsing with trusted proxy count, so we use request.remote_addr directly.
    """
    return request.remote_addr or 'unknown'


def validate_session_auth_version():
    """Опозив сесије при промени права (ревизија 2026-08, ставка 6).

    Свака промена права налога (деактивација, промена улоге, промена/reset
    лозинке) подиже ``users.auth_version``; сесија носи верзију из тренутка
    пријаве. Сесија са старом верзијом (или без ње — старе сесије пре увођења)
    се руши одмах уместо да живи до истека. Враћа response за прекид захтева
    или None када је сесија важећа.

    Fail-open на грешци провере: у прекиду базе ионако ниједан захтев не
    пролази, а масовно рушење сесија због пролазног квара би било горе.
    """
    import logging
    from flask import jsonify, redirect, url_for

    if 'user_id' not in session:
        return None
    if session.get('auth_source', 'primary') != 'primary':
        return None  # fallback nalozi ne postoje u bazi
    if request.path.startswith('/static/'):
        return None

    try:
        from postgres_service import get_postgres_connection
        with get_postgres_connection() as conn:
            with conn.cursor() as cur:
                cur.execute('SELECT auth_version FROM users WHERE id = %s AND is_active = TRUE',
                            (session['user_id'],))
                row = cur.fetchone()
    except Exception as exc:
        logging.getLogger(__name__).warning(
            'auth_version provera nije uspela (fail-open): %s', exc)
        return None

    if row is None:
        current_version = None
    elif isinstance(row, dict):
        current_version = row.get('auth_version')
    else:
        current_version = row[0]

    if row is not None and session.get('auth_version') == current_version:
        return None

    log_security_event('session_revoked', {
        'user_id': session.get('user_id'),
        'session_auth_version': session.get('auth_version'),
        'current_auth_version': current_version,
    })
    session.clear()
    if request.path.startswith('/api/'):
        return jsonify({'success': False,
                        'message': 'Сесија је опозвана — пријавите се поново.'}), 401
    flash('Ваша сесија је опозвана (промена налога или лозинке) — пријавите се поново.', 'warning')
    return redirect(url_for('login'))


def log_security_event(event_type: str, details: Dict[str, Any]) -> None:
    """Log security-related events."""
    import logging
    logger = logging.getLogger('security')

    event_data = {
        'type': event_type,
        'timestamp': datetime.now(UTC).isoformat(),
        'ip_address': get_client_ip(),
        'user_agent': request.headers.get('User-Agent', 'unknown'),
        'user_email': session.get('user_email') or session.get('user', {}).get('email', 'anonymous'),
        **details
    }

    if event_type in ['login_failed', 'account_locked', 'unauthorized_access']:
        logger.warning(f"Security event: {event_type}", extra=event_data)
    elif event_type in ['password_changed', 'login_success']:
        logger.info(f"Security event: {event_type}", extra=event_data)
    else:
        logger.debug(f"Security event: {event_type}", extra=event_data)
