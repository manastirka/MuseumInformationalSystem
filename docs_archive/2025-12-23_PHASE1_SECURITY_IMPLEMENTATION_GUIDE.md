# Phase 1 Security Implementation Guide

**Status**: In Progress
**Priority**: 🔴 CRITICAL
**Estimated Time**: 2 weeks
**Created**: December 23, 2025

---

## Overview

This guide provides step-by-step instructions for implementing Phase 1 security improvements to the Museum Information System. Follow these steps in order to ensure a secure, production-ready application.

## Prerequisites Completed ✅

1. ✅ **Updated `.env.example`** - Comprehensive configuration template created
2. ✅ **Updated `requirements.txt`** - Security dependencies added
3. ✅ **Created `config.py`** - Centralized configuration management
4. ✅ **Created `security_utils.py`** - Password validation, hashing, login tracking

## Installation Steps

### Step 1: Install Security Dependencies

```bash
cd /home/aleksandarlukovic/MuseumInfoSystem

# Backup current environment
cp requirements.txt requirements.txt.backup

# Install new dependencies
pip3 install -r requirements.txt

# Verify installations
python3 -c "import flask_wtf; import flask_limiter; import flask_session; print('All security packages installed successfully!')"
```

### Step 2: Create Production .env File

```bash
# Copy example file
cp .env.example .env

# Generate a strong secret key
python3 -c "import secrets; print('SECRET_KEY=' + secrets.token_hex(32))" >> .env.production

# Edit .env file with your actual values
nano .env
```

**CRITICAL**: Set these values in your `.env` file:
```bash
SECRET_KEY=<paste-the-generated-64-char-hex-string>
FLASK_ENV=production
ENABLE_FALLBACK_AUTH=False  # IMPORTANT: Disable in production
WTF_CSRF_ENABLED=True
```

### Step 3: Update .gitignore

Add to `.gitignore` to ensure secrets are never committed:

```bash
# Add to .gitignore
echo "" >> .gitignore
echo "# Security - NEVER commit these files" >> .gitignore
echo ".env" >> .gitignore
echo ".env.production" >> .gitignore
echo ".env.local" >> .gitignore
echo "*.pem" >> .gitignore
echo "*.key" >> .gitignore
```

---

## Code Changes Required

### Change 1: Update app.py Imports (Lines 1-30)

**Add these imports at the top of app.py:**

```python
# Add after existing imports
from config import get_config
from security_utils import (
    PasswordValidator,
    PasswordHasher,
    login_tracker,
    login_required,
    admin_required,
    log_security_event,
    get_client_ip
)
from flask_wtf.csrf import CSRFProtect
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_session import Session
```

### Change 2: Initialize App with Config (Lines 56-60)

**Replace:**
```python
app = Flask(__name__)
app.config.update({
    'SECRET_KEY': os.environ.get('SECRET_KEY', 'museum-info-system-secret-key'),
    'DEBUG': os.environ.get('FLASK_DEBUG', 'True').lower() == 'true',
})
```

**With:**
```python
# Load configuration
config_name = os.environ.get('FLASK_ENV', 'development')
app_config = get_config(config_name)

# Create Flask app
app = Flask(__name__)
app.config.from_object(app_config)

# Initialize security extensions
csrf = CSRFProtect(app)
Session(app)

# Initialize rate limiter
limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"],
    storage_uri=app.config['RATELIMIT_STORAGE_URL']
)

# Initialize password validator
password_validator = PasswordValidator(app.config)
password_hasher = PasswordHasher()
```

### Change 3: Remove Hardcoded Credentials (Lines 253-700)

**CRITICAL CHANGE**: Remove the entire `MUSEUM_EMPLOYEES` dictionary.

**Replace this entire section (lines 253-700+):**
```python
MUSEUM_EMPLOYEES = {
    'admin': {...},
    'slavko.spasic@nhmbeo.rs': {...},
    # ... all 42 employees
}
```

**With a fallback function (only for development):**
```python
def get_fallback_employees():
    """
    Fallback employee data for development/testing ONLY.
    NEVER use in production - set ENABLE_FALLBACK_AUTH=False in .env
    """
    if not app.config.get('ENABLE_FALLBACK_AUTH', False):
        return {}

    logger.warning("⚠️ USING FALLBACK AUTHENTICATION - NOT SECURE FOR PRODUCTION")

    # Return minimal admin account only
    return {
        'admin': {
            'user_id': 1,
            'email': app.config['ADMIN_EMAIL'],
            'full_name': 'System Administrator',
            'department': 'Administration',
            'position': 'Administrator',
            'role': 'admin',
            # Password will be validated through proper hashing
            'description': 'System administrator account'
        }
    }

# Use function instead of hardcoded dict
MUSEUM_EMPLOYEES = get_fallback_employees()
```

### Change 4: Secure Login Route (Lines 2080-2150)

**Find the login route and update it:**

```python
@app.route('/login', methods=['GET', 'POST'])
@limiter.limit("5 per minute")  # Rate limit login attempts
def login():
    """User login with security enhancements."""
    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')

        # Validate inputs
        if not email or not password:
            flash('Молимо унесите имејл и лозинку.', 'error')
            return render_template('login.html')

        # Check for account lockout
        max_attempts = app.config['MAX_LOGIN_ATTEMPTS']
        lockout_duration = app.config['ACCOUNT_LOCKOUT_DURATION']

        is_locked, seconds_remaining = login_tracker.is_locked_out(
            email, max_attempts, lockout_duration
        )

        if is_locked:
            minutes = seconds_remaining // 60
            flash(
                f'Налог је закључан због превише неуспешних покушаја. '
                f'Покушајте поново за {minutes} минута.',
                'danger'
            )
            log_security_event('account_locked', {
                'email': email,
                'remaining_seconds': seconds_remaining
            })
            return render_template('login.html')

        # Try authentication
        authenticated_user = None

        try:
            if auth_available:
                # Primary: Use MySQL authentication
                from localSQLtesting.auth_system import auth_system
                authenticated_user = auth_system.authenticate_user(email, password)
            elif app.config.get('ENABLE_FALLBACK_AUTH', False):
                # Fallback: Development only
                logger.warning(f"Using fallback auth for: {email}")
                authenticated_user = authenticate_fallback(email, password)
            else:
                flash('Систем аутентикације није доступан.', 'error')
                return render_template('login.html')

        except Exception as e:
            logger.error(f"Authentication error for {email}: {e}")
            flash('Грешка при пријављивању. Покушајте поново.', 'error')
            return render_template('login.html')

        if authenticated_user:
            # Successful login
            session['user'] = authenticated_user
            session.permanent = True  # Use configured timeout

            # Reset login attempts
            login_tracker.record_attempt(email, success=True)

            # Log successful login
            log_security_event('login_success', {
                'email': email,
                'user_id': authenticated_user.get('user_id')
            })

            # Check if password change required
            if authenticated_user.get('is_first_login', False):
                flash('Морате променити лозинку при првој пријави.', 'warning')
                return redirect(url_for('change_password'))

            flash(f'Добродошли, {authenticated_user["full_name"]}!', 'success')
            return redirect(url_for('dashboard'))
        else:
            # Failed login
            login_tracker.record_attempt(email, success=False)
            remaining = login_tracker.get_remaining_attempts(email, max_attempts)

            flash(
                f'Неисправни подаци за пријаву. '
                f'Преостало покушаја: {remaining}',
                'danger'
            )

            log_security_event('login_failed', {
                'email': email,
                'remaining_attempts': remaining
            })

            return render_template('login.html')

    return render_template('login.html')


def authenticate_fallback(email: str, password: str) -> Optional[dict]:
    """
    Fallback authentication for development only.
    DO NOT USE IN PRODUCTION.
    """
    if not app.config.get('ENABLE_FALLBACK_AUTH', False):
        return None

    # For admin account, check against configured credentials
    if email == app.config['ADMIN_EMAIL']:
        if password == app.config['ADMIN_DEFAULT_PASSWORD']:
            return {
                'user_id': 1,
                'email': email,
                'full_name': 'System Administrator',
                'department': 'Administration',
                'position': 'Administrator',
                'role': 'admin',
                'is_first_login': True  # Force password change
            }

    return None
```

### Change 5: Secure Password Change Route (Lines 2151-2200)

```python
@app.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    """Change user password with validation."""
    if request.method == 'POST':
        current_password = request.form.get('current_password', '')
        new_password = request.form.get('new_password', '')
        confirm_password = request.form.get('confirm_password', '')

        # Validate inputs
        if not all([current_password, new_password, confirm_password]):
            flash('Попуните сва поља.', 'error')
            return render_template('change_password.html')

        if new_password != confirm_password:
            flash('Нове лозинке се не подударају.', 'error')
            return render_template('change_password.html')

        # Validate password strength
        is_valid, errors = password_validator.validate(new_password)
        if not is_valid:
            for error in errors:
                flash(error, 'error')
            return render_template('change_password.html')

        # Change password
        user = session.get('user', {})
        user_id = user.get('user_id')

        try:
            if auth_available:
                from localSQLtesting.auth_system import auth_system
                success = auth_system.change_password(
                    user_id, current_password, new_password
                )
            else:
                # Cannot change password in fallback mode
                flash('Промена лозинке није доступна у режиму развоја.', 'warning')
                return render_template('change_password.html')

            if success:
                log_security_event('password_changed', {
                    'user_id': user_id,
                    'email': user.get('email')
                })

                flash('Лозинка је успешно промењена.', 'success')
                return redirect(url_for('dashboard'))
            else:
                flash('Неисправна тренутна лозинка.', 'error')
                return render_template('change_password.html')

        except Exception as e:
            logger.error(f"Password change error: {e}")
            flash('Грешка при промени лозинке.', 'error')
            return render_template('change_password.html')

    return render_template('change_password.html')
```

### Change 6: Update All Protected Routes

**Replace all instances of `@login_required` and `@admin_required` decorators:**

Find routes like:
```python
@app.route('/dashboard')
def dashboard():
    # ...
```

Update to:
```python
@app.route('/dashboard')
@login_required  # Use imported decorator from security_utils
def dashboard():
    # ...
```

**For admin routes:**
```python
@app.route('/admin/mineral_collection')
@admin_required  # Use imported decorator
def admin_mineral_collection():
    # ...
```

### Change 7: Add CSRF Tokens to All Forms

**Update all HTML templates with forms:**

```html
<!-- Add this inside every <form> tag -->
<form method="POST" action="...">
    {{ csrf_token() }}  <!-- Add this line -->
    <!-- rest of form fields -->
</form>
```

**Example - login.html:**
```html
<form method="POST" action="{{ url_for('login') }}">
    <input type="hidden" name="csrf_token" value="{{ csrf_token() }}"/>

    <div class="mb-3">
        <label for="email" class="form-label">Имејл</label>
        <input type="email" class="form-control" id="email" name="email" required>
    </div>
    <!-- ... rest of form -->
</form>
```

### Change 8: Update localSQLtesting/auth_system.py

**Update password hashing to use our new PasswordHasher:**

```python
# In localSQLtesting/auth_system.py

# Add import at top
from security_utils import PasswordHasher, PasswordValidator

class AuthenticationSystem:
    def __init__(self):
        self.db = db_manager
        self.password_hasher = PasswordHasher()
        self.create_auth_tables()
        self.ensure_admin_user()

    def _hash_password(self, password: str, salt: str = None) -> Tuple[str, str]:
        """Use centralized password hasher."""
        return self.password_hasher.hash_password(password, salt)

    def _verify_password(self, password: str, stored_hash: str, salt: str) -> bool:
        """Use centralized password verification."""
        return self.password_hasher.verify_password(password, stored_hash, salt)
```

---

## Testing Plan

### Test 1: Password Validation

```python
# Test script: test_password_validation.py
from security_utils import PasswordValidator
from config import DevelopmentConfig

validator = PasswordValidator(DevelopmentConfig)

# Test weak passwords (should fail)
weak_passwords = [
    'short',
    'alllowercase123!',
    'ALLUPPERCASE123!',
    'NoSpecialChar123',
    'admin123',
    'password'
]

print("Testing weak passwords (should all fail):")
for pwd in weak_passwords:
    valid, errors = validator.validate(pwd)
    print(f"  {pwd}: {'✗ FAILED' if not valid else '✓ PASSED'}")
    if errors:
        for error in errors:
            print(f"    - {error}")

# Test strong passwords (should pass)
strong_passwords = [
    'StrongP@ssw0rd123',
    'MyS3cur3P@ss!',
    'C0mpl3x&Secure#2024'
]

print("\nTesting strong passwords (should all pass):")
for pwd in strong_passwords:
    valid, errors = validator.validate(pwd)
    print(f"  {pwd}: {'✓ PASSED' if valid else '✗ FAILED'}")
```

Run test:
```bash
python3 test_password_validation.py
```

### Test 2: Login Rate Limiting

```python
# Test script: test_rate_limiting.py
import requests
from time import sleep

LOGIN_URL = 'http://localhost:5555/login'

print("Testing login rate limiting (max 5 attempts per minute)...")
for i in range(7):
    response = requests.post(LOGIN_URL, data={
        'email': 'test@nhmbeo.rs',
        'password': 'wrong_password'
    })

    print(f"Attempt {i+1}: Status {response.status_code}")

    if i >= 4:  # Should be blocked after 5 attempts
        if response.status_code == 429:  # Too Many Requests
            print("✓ Rate limiting working correctly!")
        else:
            print("✗ Rate limiting NOT working!")

    sleep(1)
```

### Test 3: CSRF Protection

```bash
# Try to POST without CSRF token (should fail)
curl -X POST http://localhost:5555/login \
  -d "email=test@nhmbeo.rs&password=test" \
  -i

# Should return 400 Bad Request with CSRF error
```

### Test 4: Session Security

```python
# Check session cookie attributes
import requests

session = requests.Session()
response = session.get('http://localhost:5555/login')

cookies = session.cookies.get_dict()
print("Session cookies:", cookies)

# Verify cookie attributes (should be HttpOnly, Secure in production)
for cookie in session.cookies:
    print(f"\nCookie: {cookie.name}")
    print(f"  HttpOnly: {cookie.has_nonstandard_attr('HttpOnly')}")
    print(f"  Secure: {cookie.secure}")
    print(f"  SameSite: {cookie.get_nonstandard_attr('SameSite')}")
```

---

## Deployment Checklist

Before deploying to production:

- [ ] Set `FLASK_ENV=production` in `.env`
- [ ] Set `ENABLE_FALLBACK_AUTH=False` in `.env`
- [ ] Generate and set strong `SECRET_KEY` (64+ characters)
- [ ] Set `SESSION_COOKIE_SECURE=True` (requires HTTPS)
- [ ] Change `ADMIN_DEFAULT_PASSWORD` to strong password
- [ ] Verify all forms have CSRF tokens
- [ ] Test rate limiting on login
- [ ] Test password validation
- [ ] Review security logs
- [ ] Backup database before deployment
- [ ] Test rollback procedure

---

## Security Verification

Run this security checklist:

```bash
# 1. Check for hardcoded secrets
grep -r "password.*=.*['\"]" *.py | grep -v "password_hash" | grep -v "get(" | grep -v ".env"

# Should return NO results

# 2. Verify .env is in .gitignore
grep "^\.env$" .gitignore

# Should show: .env

# 3. Check SECRET_KEY is not default
grep "SECRET_KEY=your-secret-key" .env

# Should return NO results

# 4. Verify CSRF is enabled
grep "WTF_CSRF_ENABLED=True" .env

# Should show: WTF_CSRF_ENABLED=True
```

---

## Rollback Plan

If issues occur:

```bash
# 1. Stop the application
sudo systemctl stop museum-system

# 2. Restore backup
cp app.py.backup app.py
cp requirements.txt.backup requirements.txt

# 3. Reinstall old dependencies
pip3 install -r requirements.txt

# 4. Restart
sudo systemctl start museum-system
```

---

## Next Steps (Week 2)

After completing Week 1 changes:

1. Implement Flask-Session with Redis for server-side sessions
2. Add comprehensive input validation
3. Enhanced audit logging with JSON format
4. Security headers (CSP, HSTS, X-Frame-Options)
5. Automated security testing

---

## Support & Questions

If you encounter issues during implementation:

1. Check logs: `tail -f logs/museum_info_system.log`
2. Verify environment: `python3 -c "from config import get_config; print(get_config())"`
3. Test imports: `python3 -c "import security_utils; print('OK')"`

---

**Last Updated**: December 23, 2025
**Status**: Week 1 Implementation Ready
