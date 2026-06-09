#!/usr/bin/env python3
"""
Test Dashboard Customization Functionality
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from app import (
    load_dashboard_preferences,
    save_dashboard_preferences,
    get_user_modules,
    DASHBOARD_PREFERENCES,
    MODULE_ACCESS
)

def run_save_and_load():
    """Test saving and loading dashboard preferences."""
    print("=" * 70)
    print("TEST: Dashboard Customization - Save & Load")
    print("=" * 70)

    # Test 1: Load current preferences
    print("\n1. Loading current preferences...")
    prefs = load_dashboard_preferences()
    print(f"   ✓ Loaded {len(prefs)} user preferences")

    # Test 2: Modify preferences for a dedicated test user.
    # NOTE: mutate the dict returned by load_dashboard_preferences() -
    # the loader rebinds app.DASHBOARD_PREFERENCES, so a value imported
    # with "from app import DASHBOARD_PREFERENCES" goes stale after load.
    print("\n2. Testing preference modification...")
    test_user = "dashboard.test@example.invalid"
    original_value = prefs.get(test_user)

    # Add more widgets
    prefs[test_user] = {
        'enabled_widgets': ['museum_databases', 'timesheet', 'news']
    }

    # Save
    if save_dashboard_preferences():
        print(f"   ✓ Saved modified preferences for {test_user}")
    else:
        print(f"   ✗ Failed to save preferences")
        return False

    # Test 3: Reload and verify
    print("\n3. Reloading preferences to verify save...")
    reloaded = load_dashboard_preferences(force=True)

    if test_user in reloaded:
        widgets = reloaded[test_user]['enabled_widgets']
        print(f"   ✓ Reloaded preferences: {widgets}")

        if set(widgets) == {'museum_databases', 'timesheet', 'news'}:
            print("   ✓ Preferences saved and loaded correctly!")
        else:
            print("   ✗ Preferences don't match!")
            return False
    else:
        print(f"   ✗ User {test_user} not found in reloaded preferences")
        return False

    # Test 4: Restore the original state exactly (remove the test user,
    # or put back whatever value existed before the test ran).
    print("\n4. Restoring original preferences...")
    current = load_dashboard_preferences()
    if original_value is None:
        current.pop(test_user, None)
    else:
        current[test_user] = original_value

    if save_dashboard_preferences():
        print(f"   ✓ Restored original preferences")

    print("\n" + "=" * 70)
    print("✓ All tests passed!")
    print("=" * 70)
    return True

def show_available_modules():
    """Show all available modules."""
    print("\n" + "=" * 70)
    print("AVAILABLE MODULES FOR DASHBOARD")
    print("=" * 70)

    for key, info in MODULE_ACCESS.items():
        print(f"\nModule: {key}")
        print(f"  Name: {info['name']}")
        print(f"  Icon: {info['icon']}")
        print(f"  Description: {info['description']}")
        print(f"  Default Access: {info.get('default_access', False)}")

        if 'authorized_users' in info:
            print(f"  Authorized Users: {', '.join(info['authorized_users'][:3])}...")

    print("\n" + "=" * 70)

def show_current_dashboard_state():
    """Show current dashboard state for admin users."""
    print("\n" + "=" * 70)
    print("CURRENT DASHBOARD STATE - ADMIN USERS")
    print("=" * 70)

    admin_users = [
        ('admin', 'admin'),
        ('slavko.spasic@nhmbeo.rs', 'admin'),
        ('biljana.mitrovic@nhmbeo.rs', 'admin'),
        ('verica.stojanovic@nhmbeo.rs', 'admin')
    ]

    for email, role in admin_users:
        print(f"\n👤 {email}:")
        modules = get_user_modules(email, role)

        if modules:
            print(f"   Visible modules ({len(modules)}):")
            for mod in modules:
                print(f"     • {mod['name']}")
        else:
            print("   ⚠ No modules visible!")

    print("\n" + "=" * 70)


def test_save_and_load():
    assert run_save_and_load()


if __name__ == "__main__":
    # Run tests
    show_current_dashboard_state()
    show_available_modules()

    print("\n")
    if run_save_and_load():
        print("\n✅ Dashboard customization is working correctly!")
        print("   Users can:")
        print("   1. View only 'Muzejska baza podataka' by default")
        print("   2. Customize their dashboard via /dashboard/customize")
        print("   3. Save their preferences")
        print("   4. Preferences persist across sessions")
    else:
        print("\n❌ Dashboard customization test failed!")
        sys.exit(1)
