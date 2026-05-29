import os

os.environ.setdefault('FLASK_ENV', 'testing')
os.environ.setdefault('SECRET_KEY', 'test-secret')
os.environ.setdefault('REDIS_URL', '')
os.environ.setdefault('SESSION_TYPE', 'filesystem')
os.environ.setdefault('SESSION_FILE_DIR', '/tmp/museum-test-b-misc')

import importlib

import pytest

migrate = importlib.import_module('migrate_all_employees_to_postgres')


class FakeCursor:
    """Minimal psycopg-like cursor that maps lookup queries to seeded tables."""

    def __init__(self, departments=None, roles=None):
        self.departments = departments or {}
        self.roles = roles or {}
        self.updates = []
        self._result = None

    def execute(self, sql, params=None):
        s = ' '.join(sql.split())
        if 'FROM departments WHERE name' in s:
            name = params[0]
            dept_id = self.departments.get(name)
            self._result = {'id': dept_id} if dept_id is not None else None
        elif 'FROM roles WHERE name' in s:
            name = params[0]
            role_id = self.roles.get(name)
            self._result = {'id': role_id} if role_id is not None else None
        elif s.startswith('UPDATE users'):
            self.updates.append((s, params))
            self._result = None
        else:
            self._result = None

    def fetchone(self):
        return self._result


def test_resolve_lookup_id_returns_id_when_name_matches():
    cur = FakeCursor(departments={'Геолошко одељење': 7}, roles={'admin': 2})
    assert migrate.resolve_lookup_id(cur, 'departments', 'Геолошко одељење') == 7
    assert migrate.resolve_lookup_id(cur, 'roles', 'admin') == 2


def test_resolve_lookup_id_returns_none_when_name_missing():
    cur = FakeCursor(departments={'Геолошко одељење': 7}, roles={'admin': 2})
    assert migrate.resolve_lookup_id(cur, 'departments', 'Nonexistent департмент') is None
    assert migrate.resolve_lookup_id(cur, 'roles', 'curator') is None


def test_update_existing_user_skips_when_role_unresolved():
    # roles table is NOT seeded with 'admin' -> resolving role must fail and
    # the update must be SKIPPED rather than nulling role_id.
    cur = FakeCursor(departments={'Геолошко одељење': 7}, roles={})
    ok = migrate.update_existing_user(
        cur,
        email='biljana.mitrovic@nhmbeo.rs',
        name='Биљана Митровић',
        position='начелник',
        department='Геолошко одељење',
        role='admin',
    )
    assert ok is False
    assert cur.updates == [], "must not run an UPDATE that would null role_id"


def test_update_existing_user_skips_when_department_unresolved():
    cur = FakeCursor(departments={}, roles={'admin': 2})
    ok = migrate.update_existing_user(
        cur,
        email='x@nhmbeo.rs',
        name='Name',
        position='pos',
        department='Геолошко одељење',
        role='admin',
    )
    assert ok is False
    assert cur.updates == []


def test_update_existing_user_runs_with_resolved_ids():
    cur = FakeCursor(departments={'Геолошко одељење': 7}, roles={'admin': 2})
    ok = migrate.update_existing_user(
        cur,
        email='biljana.mitrovic@nhmbeo.rs',
        name='Биљана Митровић',
        position='начелник',
        department='Геолошко одељење',
        role='admin',
    )
    assert ok is True
    assert len(cur.updates) == 1
    sql, params = cur.updates[0]
    # The resolved integer ids must be bound (not name-subqueries that can null).
    assert 7 in params
    assert 2 in params


def test_update_new_user_department_skips_when_unresolved():
    cur = FakeCursor(departments={}, roles={'employee': 1})
    ok = migrate.update_new_user_department(
        cur,
        user_id=42,
        department='Геолошко одељење',
    )
    assert ok is False
    assert cur.updates == []


def test_update_new_user_department_runs_when_resolved():
    cur = FakeCursor(departments={'Геолошко одељење': 7}, roles={'employee': 1})
    ok = migrate.update_new_user_department(
        cur,
        user_id=42,
        department='Геолошко одељење',
    )
    assert ok is True
    assert len(cur.updates) == 1
    sql, params = cur.updates[0]
    assert 7 in params


if __name__ == '__main__':
    raise SystemExit(pytest.main([__file__, '-q']))
