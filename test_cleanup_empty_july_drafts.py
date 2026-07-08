#!/usr/bin/env python3
"""Tests for `flask cleanup-empty-july-drafts`.

Covers: dry-run lists candidates and changes nothing; execute runs exactly one
DELETE guarded by the empty-draft predicate; the DELETE predicate itself
never matches July drafts that have day rows or entries (lists sa unetim
danima OSTAJU); the interactive database-name confirmation; and the empty
result path.
"""

import os
import unittest
from unittest.mock import patch

os.environ.setdefault('FLASK_ENV', 'testing')
os.environ.setdefault('SECRET_KEY', 'test-secret')
os.environ.setdefault('REDIS_URL', '')
os.environ.setdefault('SESSION_TYPE', 'filesystem')
os.environ.setdefault('SESSION_FILE_DIR', '/tmp/museum-test-flask-session')

import app as museum_app
import cleanup_empty_july_drafts as cleanup

TEST_DB_URL = 'postgresql://tester@localhost:5432/testdb'
TEST_DB_NAME = 'testdb'


class _FakeCursor:
    """Records SQL; returns canned candidate rows for the SELECT, a rowcount
    for the DELETE."""

    def __init__(self, candidates, executed):
        self._candidates = candidates
        self.executed = executed
        self.rowcount = 0
        self._last = ''

    def execute(self, sql, params=None):
        normalized = ' '.join(sql.split())
        self.executed.append((normalized, params))
        self._last = normalized
        if normalized.startswith('DELETE'):
            self.rowcount = len(self._candidates)

    def fetchall(self):
        if 'SELECT' in self._last:
            return list(self._candidates)
        return []

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        return False


class _FakeConnection:
    def __init__(self, candidates, executed, commits):
        self._candidates = candidates
        self.executed = executed
        self.commits = commits

    def cursor(self):
        return _FakeCursor(self._candidates, self.executed)

    def commit(self):
        self.commits.append('commit')

    def rollback(self):
        self.commits.append('rollback')

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        self.commits.append('commit' if exc_type is None else 'rollback')
        return False


class CleanupEmptyJulyDraftsTests(unittest.TestCase):
    def setUp(self):
        self.executed = []
        self.commits = []
        self.candidates = [
            (501, 'Проба Један', 'p1@nhmbeo.rs', '2026-07-08 09:12:00'),
            (502, 'Проба Два', 'p2@nhmbeo.rs', '2026-07-08 09:40:00'),
        ]
        self.runner = museum_app.app.test_cli_runner()

        patchers = [
            patch.object(
                cleanup, 'get_postgres_connection',
                lambda **kwargs: _FakeConnection(
                    self.candidates, self.executed, self.commits
                ),
            ),
            patch.object(cleanup, 'get_database_url', lambda: TEST_DB_URL),
        ]
        for patcher in patchers:
            patcher.start()
            self.addCleanup(patcher.stop)

    def _invoke(self, *args, **kwargs):
        return self.runner.invoke(
            args=['cleanup-empty-july-drafts', *args], **kwargs
        )

    def _write_statements(self):
        return [
            sql for sql, _ in self.executed
            if not sql.upper().startswith('SELECT')
        ]

    def test_dry_run_lists_candidates_and_changes_nothing(self):
        result = self._invoke()
        self.assertEqual(result.exit_code, 0, result.output)
        self.assertEqual(self._write_statements(), [])
        self.assertIn('DRY-RUN', result.output)
        self.assertIn('id=501', result.output)
        self.assertIn('id=502', result.output)
        self.assertIn('--execute', result.output)

    def test_execute_runs_single_guarded_delete(self):
        result = self._invoke('--execute', input=TEST_DB_NAME + '\n')
        self.assertEqual(result.exit_code, 0, result.output)
        deletes = [sql for sql in self._write_statements() if sql.startswith('DELETE')]
        self.assertEqual(len(deletes), 1)
        self.assertEqual(self._write_statements(), deletes)
        # Guard predicate must be part of the DELETE, not a bare id list.
        self.assertIn('NOT EXISTS', deletes[0])
        self.assertIn('timesheet_report_days', deletes[0])
        self.assertIn('timesheet_entries', deletes[0])
        self.assertIn("status = 'DRAFT'", deletes[0])
        self.assertIn('is_verified = FALSE', deletes[0])
        self.assertIn('is_locked = FALSE', deletes[0])
        self.assertIn('commit', self.commits)
        self.assertNotIn('rollback', self.commits)
        self.assertIn('GOTOVO', result.output)

    def test_execute_targets_only_july_2026(self):
        result = self._invoke('--execute', input=TEST_DB_NAME + '\n')
        self.assertEqual(result.exit_code, 0, result.output)
        delete_params = [
            params for sql, params in self.executed if sql.startswith('DELETE')
        ]
        self.assertEqual(delete_params, [(7, 2026)])

    def test_execute_rejects_wrong_db_name(self):
        result = self._invoke('--execute', input='pogresna\n')
        self.assertNotEqual(result.exit_code, 0)
        self.assertEqual(self._write_statements(), [])
        self.assertIn('ne poklapa', result.output)

    def test_empty_result_no_delete(self):
        self.candidates = []
        result = self._invoke('--execute', input=TEST_DB_NAME + '\n')
        self.assertEqual(result.exit_code, 0, result.output)
        self.assertEqual(self._write_statements(), [])
        self.assertIn('Nema praznih', result.output)

    def test_predicate_excludes_lists_with_days_or_entries(self):
        """The shared predicate must require BOTH NOT EXISTS clauses, so any
        July draft with day rows or entries is never selected/deleted."""
        predicate = ' '.join(cleanup._EMPTY_DRAFT_PREDICATE.split())
        self.assertIn(
            'NOT EXISTS ( SELECT 1 FROM timesheet_report_days', predicate
        )
        self.assertIn(
            'NOT EXISTS ( SELECT 1 FROM timesheet_entries', predicate
        )


if __name__ == '__main__':
    unittest.main()
