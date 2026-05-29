"""Behavior tests for LOW-severity hardening fixes in the control-center cluster.

Covers:
- check_database_status: PostgreSQL version parsing must not IndexError when
  psql stdout has fewer than 3 lines / non-default formatting (finding #1).
- stop_service: a port-based service whose PID vanishes between the guard and
  the kill must not raise TypeError from os.kill(None, ...) (finding #4).
- window close: a WM_DELETE_WINDOW handler must exist that closes a leaked QA
  log handle and terminates a live QA process (finding #2).
"""

import os

os.environ.setdefault('FLASK_ENV', 'testing')
os.environ.setdefault('SECRET_KEY', 'test-secret')
os.environ.setdefault('REDIS_URL', '')
os.environ.setdefault('SESSION_TYPE', 'filesystem')
os.environ.setdefault('SESSION_FILE_DIR', '/tmp/museum-test-c-control-center')

import signal
import types

import museum_control_center as mcc
from museum_control_center import MuseumControlCenter


class FakeText:
    """Minimal stand-in for a tkinter ScrolledText widget."""

    def __init__(self):
        self.buffer = []

    def delete(self, *args, **kwargs):
        self.buffer = []

    def insert(self, index, text):
        self.buffer.append(text)

    def text(self):
        return ''.join(self.buffer)


def _bare_instance():
    """Create a MuseumControlCenter without running __init__ (no Tk needed)."""
    return object.__new__(MuseumControlCenter)


def _completed(stdout='', returncode=0, stderr=''):
    return types.SimpleNamespace(stdout=stdout, returncode=returncode, stderr=stderr)


# --- Finding #1: version_line index parsing -------------------------------

def test_check_database_status_handles_short_version_stdout(monkeypatch):
    """psql 'SELECT version()' returning fewer than 3 lines must not crash."""
    app = _bare_instance()
    app.db_status_text = FakeText()

    calls = {'n': 0}

    def fake_run(cmd, *args, **kwargs):
        calls['n'] += 1
        # 1: systemctl is-active postgresql -> active
        if cmd[:2] == ['systemctl', 'is-active']:
            return _completed(stdout='active\n')
        if cmd[:2] == ['systemctl', 'is-enabled']:
            return _completed(stdout='enabled\n')
        if cmd[0] == 'psql':
            sql = cmd[-1]
            if 'version()' in sql:
                # Non-default formatting: only one header-less line, no row 3.
                return _completed(stdout='PostgreSQL 16.2 on x86_64\n')
            if 'pg_database_size' in sql:
                return _completed(stdout='42 MB\n')
            return _completed(stdout='users: 3\n')
        return _completed(stdout='')

    monkeypatch.setattr(mcc.subprocess, 'run', fake_run)
    monkeypatch.setattr(mcc.os.path, 'exists', lambda p: False)

    # Must not raise IndexError.
    app.check_database_status()

    out = app.db_status_text.text()
    assert 'PostgreSQL 16.2' in out


def test_check_database_status_handles_empty_version_stdout(monkeypatch):
    """Completely empty/row-less stdout with returncode 0 must not crash."""
    app = _bare_instance()
    app.db_status_text = FakeText()

    def fake_run(cmd, *args, **kwargs):
        if cmd[:2] == ['systemctl', 'is-active']:
            return _completed(stdout='active\n')
        if cmd[:2] == ['systemctl', 'is-enabled']:
            return _completed(stdout='enabled\n')
        if cmd[0] == 'psql':
            sql = cmd[-1]
            if 'version()' in sql:
                return _completed(stdout='\n')
            return _completed(stdout='')
        return _completed(stdout='')

    monkeypatch.setattr(mcc.subprocess, 'run', fake_run)
    monkeypatch.setattr(mcc.os.path, 'exists', lambda p: False)

    app.check_database_status()  # must not raise IndexError

    out = app.db_status_text.text()
    assert 'Верзија' in out


# --- Finding #4: stop_service os.kill with stale/None PID ------------------

def test_stop_service_vanished_pid_does_not_raise(monkeypatch):
    """If the PID frees between the guard and the kill, no TypeError."""
    app = _bare_instance()
    app.services = {
        'dev': {'name': 'Dev', 'port': 5000, 'service_type': 'process'}
    }

    # Guard sees a live PID; the kill-time lookup returns None (race).
    pids = iter([4242, None])
    monkeypatch.setattr(app, 'get_pid_on_port', lambda port: next(pids))
    monkeypatch.setattr(app, 'is_systemd_service', lambda svc: False)
    monkeypatch.setattr(app, 'check_port', lambda port: False)
    monkeypatch.setattr(app, 'update_service_status', lambda: None)

    killed = []
    monkeypatch.setattr(mcc.os, 'kill', lambda pid, sig: killed.append((pid, sig)))

    result = app.stop_service('dev', show_dialogs=False)

    # os.kill(None, ...) would raise TypeError; the fix must avoid that.
    assert result['status'] != 'error' or 'TypeError' not in str(result.get('message', ''))
    assert (None, signal.SIGTERM) not in killed


def test_stop_service_already_gone_process_is_not_error(monkeypatch):
    """A process that exits before SIGTERM is treated as stopped, not error."""
    app = _bare_instance()
    app.services = {
        'dev': {'name': 'Dev', 'port': 5000, 'service_type': 'process'}
    }

    monkeypatch.setattr(app, 'get_pid_on_port', lambda port: 4242)
    monkeypatch.setattr(app, 'is_systemd_service', lambda svc: False)
    monkeypatch.setattr(app, 'check_port', lambda port: False)
    monkeypatch.setattr(app, 'update_service_status', lambda: None)

    def fake_kill(pid, sig):
        raise ProcessLookupError("No such process")

    monkeypatch.setattr(mcc.os, 'kill', fake_kill)

    result = app.stop_service('dev', show_dialogs=False)
    assert result['status'] != 'error'


# --- Finding #2: WM_DELETE_WINDOW handler closes leaked QA handle ----------

def test_close_handler_exists_and_closes_qa_handle(tmp_path):
    """A close handler must exist and close an open QA log handle."""
    assert hasattr(MuseumControlCenter, 'on_window_close')

    app = _bare_instance()
    log_file = tmp_path / 'qa.log'
    handle = open(log_file, 'w', encoding='utf-8')
    app.qa_log_handle = handle
    app.qa_process = None

    destroyed = {'v': False}
    app.root = types.SimpleNamespace(destroy=lambda: destroyed.__setitem__('v', True))

    app.on_window_close()

    assert handle.closed
    assert app.qa_log_handle is None
    assert destroyed['v'] is True


def test_close_handler_terminates_live_qa_process(tmp_path):
    """A live QA process is terminated on window close."""
    app = _bare_instance()
    log_file = tmp_path / 'qa.log'
    app.qa_log_handle = open(log_file, 'w', encoding='utf-8')

    terminated = {'v': False}

    class FakeProc:
        def poll(self):
            return None

        def terminate(self):
            terminated['v'] = True

    app.qa_process = FakeProc()
    app.root = types.SimpleNamespace(destroy=lambda: None)

    app.on_window_close()

    assert terminated['v'] is True
    assert app.qa_log_handle is None
