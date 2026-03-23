#!/usr/bin/env python3
"""
Add CSRF tokens to all forms in template files.
This script automatically adds CSRF protection to forms that don't have it.
"""

import os
import re
from pathlib import Path

# CSRF token HTML to insert
CSRF_TOKEN = '    <input type="hidden" name="csrf_token" value="{{ csrf_token() }}"/>'

def has_csrf_token(form_content):
    """Check if form already has a CSRF token."""
    patterns = [
        r'csrf_token\(\)',
        r'name=["\']csrf_token["\']',
        r'{{ csrf_token\(\) }}'
    ]
    for pattern in patterns:
        if re.search(pattern, form_content, re.IGNORECASE):
            return True
    return False

def add_csrf_to_form(html_content):
    """Add CSRF token to forms that don't have it."""
    lines = html_content.split('\n')
    new_lines = []
    i = 0
    forms_updated = 0

    while i < len(lines):
        line = lines[i]
        new_lines.append(line)

        # Check if this line contains a <form> opening tag
        if '<form' in line.lower():
            # Find the end of the form tag (might span multiple lines)
            form_start_idx = i
            form_tag = line

            # If form tag doesn't close on same line, continue reading
            while '>' not in line and i < len(lines) - 1:
                i += 1
                line = lines[i]
                form_tag += '\n' + line
                new_lines.append(line)

            # Now we have the complete opening form tag
            # Look ahead to see if CSRF token already exists
            # Check next 10 lines for csrf_token
            check_lines = '\n'.join(lines[i:min(i+10, len(lines))])

            if not has_csrf_token(check_lines):
                # Add CSRF token on the next line
                # Match the indentation of the form tag
                indent = len(line) - len(line.lstrip())
                csrf_line = ' ' * indent + CSRF_TOKEN.strip()
                new_lines.append(csrf_line)
                forms_updated += 1

        i += 1

    return '\n'.join(new_lines), forms_updated

def process_template(filepath):
    """Process a single template file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # Check if file has forms
        if '<form' not in content.lower():
            return 0, 0

        # Check if already has csrf_token
        original_count = content.lower().count('csrf_token')

        # Add CSRF tokens
        new_content, forms_updated = add_csrf_to_form(content)

        if forms_updated > 0:
            # Write updated content
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"✓ {filepath.name}: Added CSRF tokens to {forms_updated} form(s)")
            return 1, forms_updated
        else:
            print(f"  {filepath.name}: Already has CSRF tokens")
            return 0, 0

    except Exception as e:
        print(f"✗ Error processing {filepath.name}: {e}")
        return 0, 0

def main():
    """Main function to process all templates."""
    templates_dir = Path('/home/aleksandarlukovic/MuseumInfoSystem/templates')

    print("=" * 70)
    print("Adding CSRF Tokens to Template Forms")
    print("=" * 70)
    print()

    # Get all HTML files
    html_files = sorted(templates_dir.glob('*.html'))

    total_files = 0
    total_forms = 0
    updated_files = 0

    for filepath in html_files:
        files_changed, forms_updated = process_template(filepath)
        total_files += 1
        total_forms += forms_updated
        updated_files += files_changed

    print()
    print("=" * 70)
    print("Summary:")
    print(f"  Total template files: {total_files}")
    print(f"  Files updated: {updated_files}")
    print(f"  Forms with CSRF tokens added: {total_forms}")
    print("=" * 70)
    print()

    if updated_files > 0:
        print("✓ CSRF tokens successfully added!")
        print()
        print("Next steps:")
        print("  1. Review the changes: git diff templates/")
        print("  2. Test the application")
        print("  3. Restart the server: sudo systemctl restart museum-system")
    else:
        print("✓ All forms already have CSRF protection!")

if __name__ == '__main__':
    main()
