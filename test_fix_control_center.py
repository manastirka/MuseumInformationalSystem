"""Regression tests for control-center security fixes.

Covers two confirmed vulnerabilities in museum_control_center.py:

1. Command injection: admin-entered password was interpolated into a
   ``python3 -c`` source string (f-string) then executed via subprocess.
   A password containing a double-quote / backslash / newline could inject
   arbitrary code.  Fix: hash in-process; never template the password into
   source and never spawn a subprocess for hashing.

2. SQL injection: the user ``email`` (and other dynamic values) were
   f-string-interpolated into ``UPDATE users ...`` statements run via
   ``psql -c``.  Fix: pass dynamic values as psql variables (``-v``) and
   reference them with the auto-escaping ``:'var'`` form so no value is
   interpolated into the SQL text.
"""

import os
import re

os.environ.setdefault('FLASK_ENV', 'testing')
os.environ.setdefault('SECRET_KEY', 'test-secret')
os.environ.setdefault('REDIS_URL', '')
os.environ.setdefault('SESSION_TYPE', 'filesystem')
os.environ.setdefault('SESSION_FILE_DIR', '/tmp/museum-test-control-center')

import museum_control_center as mcc


class TestHashPasswordForStorageNoInjection:
    """The hashing helper must not template the password into source or
    spawn a subprocess, and must return a verifiable bcrypt hash even for
    passwords that previously broke the python3 -c source literal."""

    def test_helper_exists_and_does_not_use_subprocess(self):
        assert hasattr(mcc, 'hash_password_for_storage'), (
            'hash_password_for_storage helper must exist (in-process hashing)'
        )

    def test_handles_double_quote_password(self):
        # This password terminates a double-quoted Python string literal and
        # injects code in the vulnerable subprocess implementation.
        evil = 'pw"); import os; os.system("touch /tmp/pwned_cc"); ("'
        sentinel = '/tmp/pwned_cc'
        if os.path.exists(sentinel):
            os.remove(sentinel)

        password_hash, salt = mcc.hash_password_for_storage(evil)

        assert isinstance(password_hash, str) and password_hash
        # The injected command must never have executed.
        assert not os.path.exists(sentinel)

        from security_utils import PasswordHasher
        assert PasswordHasher.verify_password(evil, password_hash, salt)

    def test_handles_newline_and_backslash_password(self):
        evil = 'line1\nline2\\with"quote'
        password_hash, salt = mcc.hash_password_for_storage(evil)
        from security_utils import PasswordHasher
        assert PasswordHasher.verify_password(evil, password_hash, salt)

    def test_no_subprocess_in_call(self, monkeypatch):
        called = {'subprocess': False}

        real_run = mcc.subprocess.run

        def fake_run(*args, **kwargs):
            called['subprocess'] = True
            return real_run(*args, **kwargs)

        monkeypatch.setattr(mcc.subprocess, 'run', fake_run)
        mcc.hash_password_for_storage('Primer-lozinke-za-hash-1!')
        assert called['subprocess'] is False, (
            'hashing must happen in-process, not via subprocess'
        )


class TestBuildUserUpdateCommandNoSqlInjection:
    """The psql command builder must not interpolate dynamic values into the
    SQL text; values go through psql -v variables referenced as :'name'."""

    def test_builder_exists(self):
        assert hasattr(mcc, 'build_user_update_command'), (
            'build_user_update_command helper must exist'
        )

    def test_email_not_interpolated_into_sql(self):
        evil_email = "x' OR '1'='1"
        cmd, sql = mcc.build_user_update_command(
            set_clause="is_first_login = TRUE, updated_at = NOW()",
            email=evil_email,
        )
        # The argv must be a list invoking psql.
        assert isinstance(cmd, list)
        assert cmd[0] == 'psql'

        # Regression guard: the SQL must NOT be passed via -c. psql only expands
        # :'name' / :name bindings when the statement is read from stdin or -f;
        # with -c the placeholders are emitted verbatim and the UPDATE fails.
        assert '-c' not in cmd, (
            "SQL must be fed via stdin, not -c (psql -c does not interpolate :'var')"
        )

        # The raw email string must NOT appear in the SQL text; it is supplied
        # via a -v variable and referenced through the auto-escaping :'var' form.
        assert evil_email not in sql, (
            'email must not be interpolated into the SQL string'
        )
        assert re.search(r":'\w+'", sql), (
            "SQL must reference the email via psql :'var' form"
        )
        # The email value must be passed as a -v variable assignment.
        assert any(arg == '-v' for arg in cmd)
        assert any(arg == f'target_email={evil_email}' for arg in cmd)

    def test_extra_values_passed_as_variables(self):
        cmd, sql = mcc.build_user_update_command(
            set_clause="password_hash = :'pw', salt = :'salt', updated_at = NOW()",
            email="user@example.com",
            variables={'pw': "abc'def", 'salt': ''},
        )
        assert '-c' not in cmd
        # No raw value interpolated into the SQL string.
        assert "abc'def" not in sql
        # Provided as a -v variable assignment instead.
        assert any(a == "pw=abc'def" for a in cmd)


class TestNoDefaultPasswords:
    """Revizija 2026-08, stavka 7: bez fiksnih podrazumevanih lozinki u repou;
    privremena/reset lozinka je slučajna (16–20) i prolazi isti PasswordValidator
    kao veb."""

    def test_literal_muzej_lozinke_nema_u_izvoru(self):
        src = open(mcc.__file__, encoding='utf-8').read()
        assert 'Muzej2024' not in src, (
            'fiksna podrazumevana lozinka ne sme postojati u repou'
        )

    def test_generisana_lozinka_je_16_do_20_i_slozena(self):
        gen = mcc.MuseumControlCenter.generate_strong_password
        for _ in range(20):
            pw = gen(object())
            assert 16 <= len(pw) <= 20
            assert any(c.isupper() for c in pw)
            assert any(c.islower() for c in pw)
            assert any(c.isdigit() for c in pw)
            assert any(c in '!@#$%^&*()' for c in pw)

    def test_generisana_lozinka_prolazi_veb_validator(self):
        pw = mcc.MuseumControlCenter.generate_strong_password(object())
        valid, greske = mcc.validate_password_for_storage(pw)
        assert valid, greske

    def test_kratka_lozinka_pada_na_veb_validatoru(self):
        valid, greske = mcc.validate_password_for_storage('Kratka1!')
        assert not valid
        assert greske
