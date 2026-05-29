import importlib
import os
import ssl

os.environ.setdefault('FLASK_ENV', 'testing')
os.environ.setdefault('SECRET_KEY', 'test-secret')
os.environ.setdefault('REDIS_URL', '')
os.environ.setdefault('SESSION_TYPE', 'filesystem')
os.environ.setdefault('SESSION_FILE_DIR', '/tmp/museum-test-b-rruff-db')


def _reload_module(monkeypatch_env=None):
    if monkeypatch_env is not None:
        for key, value in monkeypatch_env.items():
            if value is None:
                os.environ.pop(key, None)
            else:
                os.environ[key] = value
    import online_mineral_data
    return importlib.reload(online_mineral_data)


def test_default_context_verifies_tls():
    """By default (no override env), the SSL context must verify certificates."""
    os.environ.pop('ALLOW_INSECURE_UPSTREAM_TLS', None)
    mod = _reload_module()

    ctx = mod.ssl_context
    assert ctx.verify_mode == ssl.CERT_REQUIRED, (
        "TLS verify_mode must be CERT_REQUIRED by default, "
        f"got {ctx.verify_mode!r}"
    )
    assert ctx.check_hostname is True, (
        "Hostname checking must be enabled by default"
    )
    assert mod._VERIFY_TLS is True


def test_insecure_opt_in_via_env():
    """Setting ALLOW_INSECURE_UPSTREAM_TLS disables verification (opt-in)."""
    try:
        mod = _reload_module({'ALLOW_INSECURE_UPSTREAM_TLS': '1'})
        ctx = mod.ssl_context
        assert mod._VERIFY_TLS is False
        assert ctx.verify_mode == ssl.CERT_NONE
        assert ctx.check_hostname is False
    finally:
        os.environ.pop('ALLOW_INSECURE_UPSTREAM_TLS', None)
        _reload_module()
