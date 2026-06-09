#!/usr/bin/env python3
"""
Test Login Rate Limiting
Tests that the login endpoint properly limits repeated failed attempts
"""

import requests
from time import sleep
import sys

def run_rate_limiting(base_url='http://localhost:5555'):
    """Test login rate limiting."""
    login_url = f'{base_url}/login'

    print("=" * 70)
    print("Museum Information System - Login Rate Limiting Test")
    print("=" * 70)
    print()
    print(f"Testing URL: {login_url}")
    print(f"Expected limit: 5 attempts per minute")
    print()

    # Check if server is running
    try:
        response = requests.get(base_url, timeout=5)
        print(f"✓ Server is running (status {response.status_code})")
    except requests.exceptions.RequestException as e:
        print(f"✗ Cannot connect to server: {e}")
        print("\nPlease start the server first:")
        print("  python3 app.py")
        return 1

    print()
    print("Performing rapid login attempts with invalid credentials...")
    print("-" * 70)

    results = []
    for i in range(7):  # Try 7 attempts (should block after 5)
        try:
            response = requests.post(
                login_url,
                data={
                    'email': 'test@example.com',
                    'password': 'wrong_password',
                    'csrf_token': ''  # Will be rejected by CSRF, but tests rate limit
                },
                allow_redirects=False,
                timeout=5
            )

            status = response.status_code
            results.append((i + 1, status))

            if status == 429:  # Too Many Requests
                print(f"  Attempt {i+1}: Status {status} - ✓ RATE LIMITED (expected after 5)")
            elif status in [200, 302, 400]:  # Normal responses
                print(f"  Attempt {i+1}: Status {status} - Request allowed")
            else:
                print(f"  Attempt {i+1}: Status {status} - Unexpected response")

        except requests.exceptions.RequestException as e:
            print(f"  Attempt {i+1}: Error - {e}")
            results.append((i + 1, 'error'))

        # Small delay between requests
        sleep(0.5)

    print()
    print("=" * 70)
    print("RESULTS")
    print("=" * 70)

    # Analyze results
    allowed_count = sum(1 for _, status in results if status in [200, 302, 400])
    blocked_count = sum(1 for _, status in results if status == 429)

    print(f"Total attempts: {len(results)}")
    print(f"Allowed: {allowed_count}")
    print(f"Blocked (429): {blocked_count}")
    print()

    # Check if rate limiting is working
    if blocked_count >= 2:  # At least attempts 6 and 7 should be blocked
        print("✓ RATE LIMITING IS WORKING")
        print(f"  {blocked_count} requests were properly rate-limited")
        return 0
    elif blocked_count == 0 and allowed_count == 7:
        print("✗ RATE LIMITING IS NOT WORKING")
        print("  All requests were allowed through")
        print()
        print("Possible issues:")
        print("  1. Flask-Limiter not initialized in app.py")
        print("  2. RATELIMIT_ENABLED=False in .env")
        print("  3. Rate limit decorator not applied to login route")
        return 1
    else:
        print("⚠ RATE LIMITING MAY BE WORKING INCORRECTLY")
        print(f"  Expected at least 2 blocked requests, got {blocked_count}")
        return 1


def run_rate_limit_reset():
    """Test that rate limits reset after time period."""
    print("\n" + "=" * 70)
    print("Testing rate limit reset (60 second wait)")
    print("=" * 70)
    print()

    print("Waiting 60 seconds for rate limit to reset...")
    for i in range(60, 0, -10):
        print(f"  {i} seconds remaining...")
        sleep(10)

    print("\nAttempting login after reset...")
    try:
        response = requests.post(
            'http://localhost:5555/login',
            data={
                'email': 'test@example.com',
                'password': 'wrong_password'
            },
            timeout=5
        )

        if response.status_code in [200, 302, 400]:
            print("✓ Rate limit reset successfully - request allowed")
            return 0
        elif response.status_code == 429:
            print("✗ Rate limit did NOT reset - still blocked")
            return 1
        else:
            print(f"? Unexpected status code: {response.status_code}")
            return 1

    except requests.exceptions.RequestException as e:
        print(f"✗ Error: {e}")
        return 1



def _server_available(base_url='http://localhost:5555'):
    """Return True when the application server is reachable."""
    try:
        requests.get(base_url, timeout=3)
        return True
    except requests.exceptions.RequestException:
        return False


# Pytest entry points: live-server tests, skipped when the app is not running.

def test_rate_limiting():
    if not _server_available():
        import pytest
        pytest.skip('Application server is not running - live rate-limit test skipped')
    assert run_rate_limiting() == 0


def test_rate_limit_reset():
    if not _server_available():
        import pytest
        pytest.skip('Application server is not running - live rate-limit test skipped')
    assert run_rate_limit_reset() == 0


if __name__ == '__main__':
    # Run main test
    result = run_rate_limiting()

    if result == 0:
        # Optionally test reset (takes 60 seconds)
        print("\nRate limiting is working!")
        print("\nTo test rate limit reset (takes 60 seconds):")
        print("  python3 run_rate_limiting.py --test-reset")

        if '--test-reset' in sys.argv:
            result = run_rate_limit_reset()

    sys.exit(result)
