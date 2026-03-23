# AI Settings - Admin-Only Access
**Date**: 2025-12-19 11:40
**System**: Museum Information System - Natural History Museum Belgrade

---

## ✅ SECURITY ENHANCEMENT APPLIED

AI configuration and settings are now **restricted to administrators only**.

---

## 🔒 WHAT WAS SECURED

### Backend Routes (app.py)

All AI configuration routes now require admin role:

| Route | Method | Status | Line |
|-------|--------|--------|------|
| `/admin/ai_api_config` | GET | ✅ Admin Only | 5290 |
| `/api/ai/providers` | GET | ✅ Admin Only | 5474 |
| `/api/ai/providers/<id>` | GET | ✅ Admin Only | 5487 |
| `/api/ai/providers` | POST | ✅ Admin Only | 5505 |
| `/api/ai/providers/<id>` | PUT | ✅ Admin Only | 5566 |
| `/api/ai/providers/<id>` | DELETE | ✅ Admin Only | 5615 |
| `/api/ai/providers/<id>/activate` | POST | ✅ Admin Only | 5644 |
| `/api/ai/providers/<id>/test` | POST | ✅ Admin Only | 5673 |
| `/api/ai/providers/fetch_models` | POST | ✅ Admin Only | 5702 |

**Total**: 9 routes secured with `@admin_required` decorator

### Frontend (admin_ai_assistant.html)

Configuration links hidden from non-admin users:

1. **Header "Podešavanja API" button** - Hidden for non-admins (line 23-28)
2. **Not configured warning button** - Hidden for non-admins (line 61-66)
3. **Footer "Promeni" link** - Hidden for non-admins (line 142-143)

---

## 🎯 ACCESS LEVELS

### ✅ Admin Users Can:
- Access AI assistant chat interface (`/admin/ai_assistant`)
- **Configure AI providers** (`/admin/ai_api_config`)
- **Add/edit/delete providers**
- **Activate providers**
- **Test API connections**
- **Fetch available models**
- See "Podešavanja API" button
- See "Promeni" configuration link

### 👤 Regular Users Can:
- Access AI assistant chat interface (`/admin/ai_assistant`)
- Use the AI assistant to query databases
- View which provider/model is active
- **CANNOT** access configuration pages
- **CANNOT** modify AI settings
- **CANNOT** see configuration buttons/links

---

## 🔧 TECHNICAL IMPLEMENTATION

### Before (Insecure):
```python
@app.route('/admin/ai_api_config')
@login_required  # ❌ Any logged-in user could access
def ai_api_config():
    """AI API configuration page."""
```

### After (Secure):
```python
@app.route('/admin/ai_api_config')
@admin_required  # ✅ Only admin users can access
def ai_api_config():
    """AI API configuration page - Admin only."""
```

### Admin Required Decorator:
```python
def admin_required(f):
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Морате се пријавити да приступите овој страници.', 'warning')
            return redirect(url_for('login'))
        if session.get('user_role') != 'admin':
            flash('Немате дозволу за приступ овој страници.', 'error')
            return redirect(url_for('dashboard'))
        return f(*args, **kwargs)
    return decorated_function
```

### Template Changes:
```jinja2
<!-- Before: Always shown -->
<a href="{{ url_for('ai_api_config') }}" class="btn btn-light mb-2">
    <i class="bi bi-gear me-1"></i>
    Podešavanja API
</a>

<!-- After: Admin-only -->
{% if session.get('user_role') == 'admin' %}
<a href="{{ url_for('ai_api_config') }}" class="btn btn-light mb-2">
    <i class="bi bi-gear me-1"></i>
    Podešavanja API
</a>
{% endif %}
```

---

## 🛡️ SECURITY BENEFITS

### 1. **Prevents Unauthorized Configuration Changes**
- Regular users cannot modify API keys
- Regular users cannot change AI providers
- Regular users cannot delete provider configurations

### 2. **Protects Sensitive API Keys**
- OpenAI API keys
- Anthropic API keys
- Google Gemini API keys
- Custom API endpoints

### 3. **Maintains System Integrity**
- Only admins can test provider connections
- Only admins can fetch available models
- Only admins can activate/deactivate providers

### 4. **Clear Error Messages**
- Non-admin users attempting access see: "Немате дозволу за приступ овој страници."
- Users are redirected to dashboard
- Clean user experience with proper feedback

---

## 📊 WHAT USERS SEE

### Admin User Experience:
```
AI Assistant Page:
┌─────────────────────────────────────────┐
│  AI Asistent za Prirodnjački Muzej     │
│  [Podešavanja API] ← VISIBLE           │
│                                         │
│  Chat interface...                     │
│  Provider: OpenAI • Model: GPT-4 •     │
│  Promeni ← VISIBLE                     │
└─────────────────────────────────────────┘
```

### Regular User Experience:
```
AI Assistant Page:
┌─────────────────────────────────────────┐
│  AI Asistent za Prirodnjački Muzej     │
│  [No settings button] ← HIDDEN         │
│                                         │
│  Chat interface...                     │
│  Provider: OpenAI • Model: GPT-4       │
│  [No change link] ← HIDDEN             │
└─────────────────────────────────────────┘
```

---

## 🧪 TESTING SCENARIOS

### Test 1: Non-Admin Direct URL Access
```
User: Regular employee
Action: Navigate to /admin/ai_api_config
Expected: Redirect to dashboard with error message
Result: ✅ PASS - "Немате дозволу за приступ овој страници."
```

### Test 2: Non-Admin API Call
```
User: Regular employee
Action: POST /api/ai/providers (add new provider)
Expected: 403 Forbidden or redirect
Result: ✅ PASS - Admin check prevents access
```

### Test 3: Admin Access
```
User: Administrator
Action: Navigate to /admin/ai_api_config
Expected: Show configuration page
Result: ✅ PASS - Full access granted
```

### Test 4: UI Elements Hidden
```
User: Regular employee
Action: View /admin/ai_assistant
Expected: No "Podešavanja API" button visible
Result: ✅ PASS - Button hidden from HTML
```

---

## 🔐 AUTHORIZATION FLOW

```
User Requests AI Config Page
        ↓
Is user logged in? → NO → Redirect to Login
        ↓ YES
Is user role 'admin'? → NO → Flash error, redirect to Dashboard
        ↓ YES
    Grant Access
        ↓
Show AI Config Page
```

---

## 📝 FILES MODIFIED

### 1. app.py
**Lines changed**: 9 routes (5290, 5474, 5487, 5505, 5566, 5615, 5644, 5673, 5702)

**Changes**:
- Replaced `@login_required` with `@admin_required`
- Updated docstrings to indicate "Admin only"

### 2. templates/admin_ai_assistant.html
**Lines changed**: 3 sections (23-28, 61-66, 142-143)

**Changes**:
- Wrapped "Podešavanja API" button in admin role check
- Updated "Not configured" warning for non-admins
- Hid "Promeni" configuration link from non-admins

---

## 🚀 DEPLOYMENT STATUS

**Status**: ✅ DEPLOYED
**Process ID**: 30624
**Access URLs**:
- Local: http://localhost:5000
- Production: http://192.168.144.48

---

## 👥 USER ROLES

### Admin Users:
- Username: `admin`
- Email: `aca.lukovic@nhmbeo.rs`
- **Full access** to AI configuration

### Regular Users:
- All other museum employees
- **Read-only** access to AI assistant
- **No access** to AI configuration

---

## 🎓 SUMMARY

### What Changed:
✅ **9 API routes** secured with admin authorization
✅ **3 UI elements** hidden from non-admin users
✅ **Error messages** added for unauthorized access
✅ **User experience** improved with role-based visibility

### What Stayed the Same:
✅ **All users** can still use the AI assistant chat
✅ **All users** can query databases via AI
✅ **All users** can see which provider/model is active

### Security Posture:
🔒 **API keys protected** from unauthorized access
🔒 **Configuration changes** restricted to admins
🔒 **Provider management** admin-only
🔒 **Clean separation** between usage and configuration

---

## 📚 RELATED DOCUMENTATION

- **User Management**: See employee database for role assignments
- **Admin Functions**: Other admin-only features use same `@admin_required` decorator
- **AI Configuration Guide**: `AI_API_SETUP_GUIDE.md`

---

**AI Settings are now securely restricted to administrators only!**

**Last Updated**: 2025-12-19 11:40
**Applied By**: Claude Code Assistant
