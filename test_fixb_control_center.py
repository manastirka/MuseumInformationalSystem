import os
import sys
import types

os.environ.setdefault('FLASK_ENV', 'testing')
os.environ.setdefault('SECRET_KEY', 'test-secret')
os.environ.setdefault('REDIS_URL', '')
os.environ.setdefault('SESSION_TYPE', 'filesystem')
os.environ.setdefault('SESSION_FILE_DIR', '/tmp/museum-test-b-control-center')

from unittest import mock

import pytest

import museum_control_center as mcc


class _FakeConn:
    def __init__(self, laddr, status):
        self.laddr = laddr
        self.status = status
        self.pid = 4321


class _FakeSelf:
    """Minimal stand-in for MuseumControlCenter to exercise unbound methods."""
    pass


def test_check_port_handles_empty_laddr():
    """psutil.net_connections() can yield connections with an empty laddr
    tuple (); accessing .port on it must not raise AttributeError."""
    conns = [
        _FakeConn((), 'NONE'),                       # empty laddr -> falsy
        _FakeConn(types.SimpleNamespace(port=8080), 'LISTEN'),
    ]
    with mock.patch.object(mcc.psutil, 'net_connections', return_value=conns):
        assert mcc.MuseumControlCenter.check_port(_FakeSelf(), 8080) is True
        assert mcc.MuseumControlCenter.check_port(_FakeSelf(), 9999) is False


def test_get_pid_on_port_handles_empty_laddr():
    conns = [
        _FakeConn((), 'NONE'),                       # empty laddr -> falsy
        _FakeConn(types.SimpleNamespace(port=8080), 'LISTEN'),
    ]
    with mock.patch.object(mcc.psutil, 'net_connections', return_value=conns):
        assert mcc.MuseumControlCenter.get_pid_on_port(_FakeSelf(), 8080) == 4321
        assert mcc.MuseumControlCenter.get_pid_on_port(_FakeSelf(), 9999) is None


def test_start_service_does_not_mutate_process_cwd(tmp_path):
    """Starting a port-based service must not change the process-wide CWD;
    Popen already receives cwd=service['path']."""
    service_dir = tmp_path / 'svc'
    service_dir.mkdir()

    fake = _FakeSelf()
    fake.services = {
        'svc': {
            'name': 'Test Service',
            'path': str(service_dir),
            'log': 'logs/test.log',
            'command': ['true'],
            'port': 8080,
        }
    }
    fake.is_systemd_service = lambda service: False
    # Not running before start; running after start.
    check_port_results = iter([False, True])
    fake.check_port = lambda port: next(check_port_results)
    fake.update_service_status = lambda: None

    captured = {}

    class _FakeProc:
        pass

    def _fake_popen(command, **kwargs):
        captured['cwd'] = kwargs.get('cwd')
        return _FakeProc()

    original_cwd = os.getcwd()
    try:
        with mock.patch.object(mcc.subprocess, 'Popen', _fake_popen), \
                mock.patch.object(mcc.time, 'sleep', lambda *a, **k: None):
            result = mcc.MuseumControlCenter.start_service(fake, 'svc', show_dialogs=False)
        cwd_after = os.getcwd()
    finally:
        os.chdir(original_cwd)

    assert cwd_after == original_cwd, "start_service must not mutate process CWD"
    assert captured['cwd'] == str(service_dir)
    assert result['status'] == 'changed'
