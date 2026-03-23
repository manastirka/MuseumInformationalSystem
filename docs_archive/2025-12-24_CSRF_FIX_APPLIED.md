# CSRF Token Issue - FIXED! ✅

**Date**: December 24, 2025
**Issue**: "The CSRF session token is missing" error on login
**Root Cause**: `.env` file was not being loaded, so SESSION_COOKIE_SECURE was True (default), preventing cookies over HTTP

---

## ✅ Fix Applied

**Changed File**: `app.py` (lines 22-24)

Added `.env` file loading:
```python
# Load environment variables from .env file
from dotenv import load_dotenv
load_dotenv()
```

This loads your `.env` configuration **before** the Flask app initializes, ensuring:
- `SESSION_COOKIE_SECURE=False` (allows cookies over HTTP in development)
- `WTF_CSRF_ENABLED=True` (CSRF protection active)
- All other `.env` settings are properly loaded

---

## 🔄 Restart Required

You MUST restart the application for this fix to work:

### Option 1: Using systemctl (Recommended)
```bash
sudo systemctl restart museum-system
sudo systemctl status museum-system
```

### Option 2: Manual restart
```bash
# Kill old process
pkill -f "gunicorn.*museum"

# Start new process
cd /home/aleksandarlukovic/MuseumInfoSystem
source venv/bin/activate
gunicorn -c gunicorn.conf.py wsgi:application &
```

### Option 3: Use stop/start scripts
```bash
./stop_all.sh
./start_all.sh
```

---

## 🧪 After Restart

1. **Clear browser cookies** (important!)
   - Open login page
   - Press F12 → Application tab → Cookies → Clear all
   - Or just use Incognito/Private mode

2. **Refresh the login page**

3. **Try logging in**:
   - Email: `admin`
   - Password: `admin123`

4. **Verify CSRF token in page source**:
   ```bash
   curl -s http://localhost:5555/login | grep csrf_token
   ```

   Should show:
   ```html
   <input type="hidden" name="csrf_token" value="[long token value]"/>
   ```

---

## ✅ Expected Behavior

After restart + clearing cookies:

| Action | Expected Result |
|--------|----------------|
| Visit login page | ✅ CSRF token generated |
| View page source | ✅ `csrf_token` visible in HTML |
| Submit login form | ✅ Form accepted, no CSRF error |
| Check logs | ✅ No "CSRF token missing" errors |

---

## 🔍 Verification Commands

```bash
# 1. Check if .env is being loaded
python3 -c "
from dotenv import load_dotenv
import os
load_dotenv()
print('SESSION_COOKIE_SECURE:', os.environ.get('SESSION_COOKIE_SECURE'))
print('WTF_CSRF_ENABLED:', os.environ.get('WTF_CSRF_ENABLED'))
"

# Expected output:
# SESSION_COOKIE_SECURE: False
# WTF_CSRF_ENABLED: True

# 2. Test CSRF token generation
python3 test_csrf.py

# Expected: ✓ CSRF token generated successfully!

# 3. Check running process
pgrep -f "gunicorn.*museum" && echo "✓ App is running" || echo "✗ App not running"
```

---

## 📝 What Was Wrong

### Before Fix:
1. `app.py` imported `config` module
2. `config.py` tried to read `os.environ.get('SESSION_COOKIE_SECURE', 'True')`
3. `.env` file was **never loaded**, so environment was empty
4. Default value `'True'` was used
5. `SESSION_COOKIE_SECURE=True` prevented cookies over HTTP
6. No session cookie = No CSRF validation possible

### After Fix:
1. `app.py` calls `load_dotenv()` **first**
2. `.env` file is loaded into `os.environ`
3. `config.py` reads `SESSION_COOKIE_SECURE=False` from environment
4. Session cookies work over HTTP
5. CSRF tokens validated successfully ✅

---

## 🎯 Summary

**Problem**: `.env` file wasn't loaded
**Solution**: Added `load_dotenv()` to app.py
**Action Required**: Restart application + Clear browser cookies
**Expected Result**: Login works without CSRF errors

---

**Status**: ✅ **FIX APPLIED - RESTART REQUIRED**

After you restart and clear cookies, login should work perfectly!
