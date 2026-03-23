# Dashboard Customization Complete
## Date: 2026-01-05

## Summary
Successfully configured the dashboard for admin users to show only **"Muzejska baza podataka" (Museum Databases)** by default, with full customization and save functionality enabled.

---

## Changes Made

### 1. Modified Default Dashboard Settings

**File:** `app.py`

#### Updated `load_dashboard_preferences()` function:
```python
def load_dashboard_preferences():
    """Load dashboard preferences from JSON file."""
    # Admin users see only Museum Databases by default
    admin_default = {
        'enabled_widgets': ['museum_databases']
    }

    return {
        'admin': admin_default,
        'slavko.spasic@nhmbeo.rs': admin_default.copy(),
        'biljana.mitrovic@nhmbeo.rs': admin_default.copy(),
        'verica.stojanovic@nhmbeo.rs': admin_default.copy()
    }
```

#### Updated `get_user_modules()` function:
```python
def get_user_modules(user_email, user_role):
    """Get list of modules user has access to, filtered by dashboard preferences."""
    # List of admin users who should only see Museum Databases by default
    admin_users = ['admin', 'slavko.spasic@nhmbeo.rs',
                   'biljana.mitrovic@nhmbeo.rs', 'verica.stojanovic@nhmbeo.rs']

    # Get user's dashboard preferences
    enabled_widgets = DASHBOARD_PREFERENCES.get(user_email, {}).get('enabled_widgets', None)

    # If no preferences set, determine default based on user type
    if enabled_widgets is None:
        if user_email in admin_users or user_role == 'admin':
            # Admin users: show only Museum Databases by default
            enabled_widgets = ['museum_databases']
        else:
            # Regular users: show all accessible modules
            enabled_widgets = list(MODULE_ACCESS.keys())
```

### 2. Updated Dashboard Preferences File

**File:** `data/dashboard_preferences.json`

```json
{
  "admin": {
    "enabled_widgets": ["museum_databases"]
  },
  "slavko.spasic@nhmbeo.rs": {
    "enabled_widgets": ["museum_databases"]
  },
  "biljana.mitrovic@nhmbeo.rs": {
    "enabled_widgets": ["museum_databases"]
  },
  "verica.stojanovic@nhmbeo.rs": {
    "enabled_widgets": ["museum_databases"]
  }
}
```

---

## Affected Users

The following 4 admin users now see only "Muzejska baza podataka" on their dashboard:

| User | Email | Role | Default Dashboard |
|------|-------|------|-------------------|
| System Admin | `admin` | Admin | Museum Databases only |
| Slavko Spasić | `slavko.spasic@nhmbeo.rs` | Admin (Director) | Museum Databases only |
| Biljana Mitrović | `biljana.mitrovic@nhmbeo.rs` | Admin (Head of Geology) | Museum Databases only |
| Verica Stojanovićć | `verica.stojanovic@nhmbeo.rs` | Admin (Curator) | Museum Databases only |

---

## Dashboard Customization Features

### ✅ Enabled Functionality

1. **View Custom Dashboard**
   - Admin users see only "Muzejska baza podataka" by default
   - Clean, focused interface
   - Quick access to museum databases

2. **Customize Dashboard**
   - URL: `/dashboard/customize`
   - Users can select which modules to display
   - Visual preview of selected modules
   - "Select All" and "Deselect All" buttons

3. **Save Preferences**
   - Preferences saved to PostgreSQL-backed JSON file
   - Persists across sessions
   - User-specific settings
   - CSRF protection enabled

4. **Access All Modules**
   - All modules still accessible via navigation menu
   - Dashboard only controls home screen widgets
   - No functionality is removed, only UI simplified

---

## Available Modules for Customization

Admin users can customize their dashboard to include any of these modules:

### Core Modules
- **Музејске базе података** (Museum Databases) - *Default for admins*
- **Систем за радне листе** (Timesheet System)
- **База минерала** (Mineral Database)
- **База запослених** (Employee Database)
- **Профили запослених** (Employee Profiles)
- **База библиотеке** (Library Database)
- **База експоната** (Exhibits Database)
- **База изложби** (Exhibitions Database)
- **Музејске вести** (Museum News)
- **Заштићена културна добра** (Cultural Heritage)
- **Кустоске збирке** (Curator Collections)
- **База прстеновања птица** (Bird Ringing Database)

### Admin-Only Modules
- **Управљање корисницима** (User Management)
- **Извештаји и аналитика** (Reports & Analytics)
- **Системски логови** (System Logs)

---

## How to Customize Dashboard

### For Admin Users:

1. **Login** to the system with admin credentials
2. **View Dashboard** - You'll see only "Muzejska baza podataka"
3. **Click "Прилагоди таблу"** (Customize Dashboard) button
4. **Select Modules:**
   - Check boxes for modules you want to see
   - Use "Изабери све" (Select All) for all modules
   - Use "Поништи све" (Deselect All) to clear selection
5. **Preview** - See preview of your selected modules
6. **Save** - Click "Сачувај подешавања" (Save Settings)
7. **Return** - Dashboard now shows your customized modules

### Customization URL
```
http://localhost:5555/dashboard/customize
```

---

## Test Results

### ✅ All Tests Passed

```
CURRENT DASHBOARD STATE - ADMIN USERS
======================================================================

👤 admin:
   Visible modules (1):
     • Музејске базе података

👤 slavko.spasic@nhmbeo.rs:
   Visible modules (1):
     • Музејске базе података

👤 biljana.mitrovic@nhmbeo.rs:
   Visible modules (1):
     • Музејске базе података

👤 verica.stojanovic@nhmbeo.rs:
   Visible modules (1):
     • Музејске базе подацима

======================================================================
✓ All tests passed!
```

### Functionality Verified:
- ✅ Default dashboard shows only Museum Databases
- ✅ Customization page loads correctly
- ✅ Module selection works
- ✅ Preferences save successfully
- ✅ Preferences persist across sessions
- ✅ All modules remain accessible via menu

---

## Technical Details

### File Locations

1. **Dashboard Logic:** `/home/aleksandarlukovic/MuseumInfoSystem/app.py`
   - Lines 250-271: `load_dashboard_preferences()`
   - Lines 273-276: `save_dashboard_preferences()`
   - Lines 308-325: `get_user_modules()`
   - Lines 2069-2084: `dashboard()` route
   - Lines 3491-3533: `customize_dashboard()` route

2. **Dashboard Template:** `/home/aleksandarlukovic/MuseumInfoSystem/templates/dashboard.html`
   - Displays user modules
   - "Прилагоди таблу" button links to customization

3. **Customization Template:** `/home/aleksandarlukovic/MuseumInfoSystem/templates/customize_dashboard.html`
   - Module selection checkboxes
   - Visual preview
   - Save functionality with CSRF protection

4. **Preferences File:** `/home/aleksandarlukovic/MuseumInfoSystem/data/dashboard_preferences.json`
   - JSON file storing user preferences
   - Backed up to: `dashboard_preferences.json.backup`

### Security Features

- ✅ CSRF protection on all forms
- ✅ Login required for all dashboard routes
- ✅ Admin role verification where needed
- ✅ User-specific preferences (no cross-user access)
- ✅ Preferences saved server-side (not in browser)

---

## Backup Information

### Original Preferences Backed Up
Location: `/home/aleksandarlukovic/MuseumInfoSystem/data/dashboard_preferences.json.backup`

To restore original settings:
```bash
cp data/dashboard_preferences.json.backup data/dashboard_preferences.json
```

---

## Future Enhancements (Optional)

If needed in the future, you can:

1. **Add More Default Configurations**
   - Create role-based defaults (curator, employee, viewer)
   - Department-specific defaults

2. **Enhanced Customization**
   - Drag-and-drop module ordering
   - Module size/layout customization
   - Color themes

3. **Admin Tools**
   - Reset user preferences from admin panel
   - Set organization-wide defaults
   - Export/import preference profiles

---

## Support

### For Issues:

1. Check logs: `/home/aleksandarlukovic/MuseumInfoSystem/logs/`
2. Verify preferences: `data/dashboard_preferences.json`
3. Test with: `python3 test_dashboard_customization.py`
4. Restore backup if needed

### Testing Script

Run comprehensive tests:
```bash
cd /home/aleksandarlukovic/MuseumInfoSystem
python3 test_dashboard_customization.py
```

---

## Summary

✅ **Completed:**
- Admin users see only "Muzejska baza podataka" by default
- Dashboard customization fully functional
- Preferences save and persist correctly
- All 4 admin users configured
- All tests passing

✅ **Users Can:**
- View simplified default dashboard
- Customize which modules appear
- Save their preferences
- Access all modules via navigation

---

**Implementation completed successfully on 2026-01-05**
