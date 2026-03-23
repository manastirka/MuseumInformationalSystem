#!/usr/bin/env python3
"""
Script to remove hardcoded MUSEUM_EMPLOYEES credentials from app.py
Replaces the 444-line dictionary with a secure fallback function
"""

import re

print("Removing hardcoded credentials from app.py...")

# Read the file
with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Find the start and end of MUSEUM_EMPLOYEES dictionary
# It starts with "MUSEUM_EMPLOYEES = {" and ends before "# Library Database"
start_marker = "# Fallback employee database for when MySQL is not available\nMUSEUM_EMPLOYEES = {"
end_marker = "}\n\n# Library Database - will be loaded from JSON"

# Replacement text - secure fallback function
replacement = """# Fallback employee database for when MySQL is not available
def get_fallback_employees():
    \"\"\"
    Fallback employee data for development/testing ONLY.
    NEVER use in production - set ENABLE_FALLBACK_AUTH=False in .env

    Returns minimal admin account if fallback auth is enabled in config.
    \"\"\"
    if not app.config.get('ENABLE_FALLBACK_AUTH', False):
        logger.info("Fallback authentication is disabled (production mode)")
        return {}

    logger.warning("⚠️ USING FALLBACK AUTHENTICATION - NOT SECURE FOR PRODUCTION")
    logger.warning("    Set ENABLE_FALLBACK_AUTH=False in .env for production")

    # Return minimal admin account only
    # Password will be hashed and validated through proper authentication flow
    return {
        app.config.get('ADMIN_EMAIL', 'admin@nhmbeo.rs'): {
            'user_id': 1,
            'email': app.config.get('ADMIN_EMAIL', 'admin@nhmbeo.rs'),
            'full_name': 'System Administrator',
            'department': 'Administration',
            'position': 'System Administrator',
            'role': 'admin',
            # Password stored in config, not hardcoded
            'requires_password_check': True,
            'description': 'Администратор информационог система музеја.'
        }
    }

# Initialize fallback employees
MUSEUM_EMPLOYEES = get_fallback_employees()

# Library Database - will be loaded from JSON"""

# Find and replace
if start_marker in content and end_marker in content:
    # Find positions
    start_pos = content.find(start_marker)
    end_pos = content.find(end_marker)

    if start_pos != -1 and end_pos != -1 and start_pos < end_pos:
        # Calculate how much we're removing
        removed_section = content[start_pos:end_pos]
        removed_lines = removed_section.count('\n')

        print(f"Found MUSEUM_EMPLOYEES dictionary:")
        print(f"  Start position: {start_pos}")
        print(f"  End position: {end_pos}")
        print(f"  Removing {removed_lines} lines")
        print(f"  Removing {len(removed_section)} characters")

        # Perform replacement
        new_content = content[:start_pos] + replacement + content[end_pos:]

        # Write back
        with open('app.py', 'w', encoding='utf-8') as f:
            f.write(new_content)

        print("✅ Successfully removed hardcoded credentials!")
        print(f"   Reduced file by {removed_lines} lines")
        print(f"   Replaced with secure fallback function")
        print("\n⚠️  IMPORTANT:")
        print("   1. Set ENABLE_FALLBACK_AUTH=False in production .env")
        print("   2. Configure ADMIN_EMAIL and ADMIN_DEFAULT_PASSWORD in .env")
        print("   3. Admin will be forced to change password on first login")

    else:
        print("❌ Could not find proper start/end positions")
        print(f"   start_pos: {start_pos}, end_pos: {end_pos}")
else:
    print("❌ Could not find markers in file")
    print(f"   start_marker found: {start_marker in content}")
    print(f"   end_marker found: {end_marker in content}")
