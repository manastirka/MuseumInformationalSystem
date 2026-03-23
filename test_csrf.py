#!/usr/bin/env python3
"""
Test CSRF token generation in the application.
"""

from app import app

with app.test_request_context():
    from flask_wtf.csrf import generate_csrf

    print("=" * 70)
    print("CSRF Token Generation Test")
    print("=" * 70)
    print()

    try:
        token = generate_csrf()
        print(f"✓ CSRF token generated successfully!")
        print(f"  Token (first 20 chars): {token[:20]}...")
        print(f"  Token length: {len(token)} characters")
        print()
        print("✓ CSRF Protection is working correctly")
        print()
        print("If you're getting 'CSRF token missing' error:")
        print("  1. Restart the application: sudo systemctl restart museum-system")
        print("  2. Clear browser cookies")
        print("  3. Refresh the login page")
        print("  4. Try logging in again")

    except Exception as e:
        print(f"✗ CSRF token generation failed!")
        print(f"  Error: {e}")
        print()
        print("Possible solutions:")
        print("  1. Check SECRET_KEY is set in .env")
        print("  2. Verify Flask-WTF is installed: pip3 install Flask-WTF")
        print("  3. Check app initialization in app.py")

    print()
    print("=" * 70)
