#!/usr/bin/env python3
"""
Test Password Validation
Tests the password validator against museum security policy
"""

from security_utils import PasswordValidator
from config import DevelopmentConfig

def run_password_validation():
    """Test password validation rules."""
    validator = PasswordValidator(DevelopmentConfig)

    print("=" * 70)
    print("Museum Information System - Password Validation Test")
    print("=" * 70)
    print()

    # Test weak passwords (should fail)
    weak_passwords = [
        ('short', 'Too short'),
        ('alllowercase123!', 'No uppercase'),
        ('ALLUPPERCASE123!', 'No lowercase'),
        ('NoSpecialChar123', 'No special character'),
        ('NoNumbers!Lower', 'No numbers'),
        ('admin123', 'Common weak password'),
        ('password', 'Common weak password'),
        ('12345678', 'Common weak password'),
        ('qwerty', 'Too short and common'),
    ]

    print("Testing WEAK passwords (should all fail):")
    print("-" * 70)
    failed_count = 0
    for pwd, reason in weak_passwords:
        valid, errors = validator.validate(pwd)
        status = '✗ FAILED (as expected)' if not valid else '✓ PASSED (unexpected!)'
        print(f"  Password: {pwd:20} - {status}")
        if errors:
            for error in errors:
                print(f"    - {error}")
        if not valid:
            failed_count += 1
        print()

    print(f"Result: {failed_count}/{len(weak_passwords)} weak passwords correctly rejected")
    print()

    # Test strong passwords (should pass)
    strong_passwords = [
        'StrongP@ssw0rd123',
        'MyS3cur3P@ss!',
        'C0mpl3x&Secure#2024',
        'Museum$ecure2025!',
        'NaturalHistory!123',
        'Belgrade@Museum#456'
    ]

    print("\nTesting STRONG passwords (should all pass):")
    print("-" * 70)
    passed_count = 0
    for pwd in strong_passwords:
        valid, errors = validator.validate(pwd)
        status = '✓ PASSED (as expected)' if valid else '✗ FAILED (unexpected!)'
        print(f"  Password: {pwd:30} - {status}")
        if errors:
            for error in errors:
                print(f"    - {error}")
        if valid:
            passed_count += 1
        print()

    print(f"Result: {passed_count}/{len(strong_passwords)} strong passwords correctly accepted")
    print()

    # Test password generation
    print("\nTesting PASSWORD GENERATION:")
    print("-" * 70)
    generated = validator.generate_strong_password(16)
    print(f"Generated password: {generated}")
    valid, errors = validator.validate(generated)
    print(f"Validation: {'✓ PASSED' if valid else '✗ FAILED'}")
    if errors:
        for error in errors:
            print(f"  - {error}")
    print()

    # Summary
    print("=" * 70)
    print("SUMMARY")
    print("=" * 70)
    weak_score = failed_count / len(weak_passwords) * 100
    strong_score = passed_count / len(strong_passwords) * 100

    print(f"Weak password rejection rate: {weak_score:.1f}%")
    print(f"Strong password acceptance rate: {strong_score:.1f}%")

    if weak_score == 100 and strong_score == 100:
        print("\n✓ ALL TESTS PASSED - Password validation working correctly!")
        return 0
    else:
        print("\n✗ SOME TESTS FAILED - Review password validation logic")
        return 1



def test_password_validation():
    assert run_password_validation() == 0


if __name__ == '__main__':
    import sys
    sys.exit(run_password_validation())
