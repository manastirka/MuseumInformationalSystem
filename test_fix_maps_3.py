#!/usr/bin/env python3
"""Regression tests for connection leaks in map_feature_paper_enricher.

Findings (maps-3):
  1. get_feature_paper_summary leaks the pooled DB connection if any SELECT /
     dict() conversion raises (no try/finally around conn.close()).
  2. get_feature_paper_count leaks the pooled DB connection if the query or the
     ['count'] subscript raises.

Both functions acquire a connection via db.get_connection(); for pooled
connections .close() is the ONLY path that returns the connection to the bounded
pool. If close() is skipped on the exception path the pool eventually exhausts.
"""

import os
import unittest
from unittest.mock import MagicMock, patch

os.environ.setdefault('FLASK_ENV', 'testing')
os.environ.setdefault('SECRET_KEY', 'test-secret')
os.environ.setdefault('REDIS_URL', '')
os.environ.setdefault('SESSION_TYPE', 'filesystem')
os.environ.setdefault('SESSION_FILE_DIR', '/tmp/museum-test-maps-3')

import map_feature_paper_enricher as enricher


class FeaturePaperConnectionLeakTests(unittest.TestCase):
    def test_summary_closes_connection_when_query_raises(self):
        conn = MagicMock()
        conn.execute.side_effect = RuntimeError("connection dropped")

        with patch.object(enricher.db, 'get_connection', return_value=conn):
            with self.assertRaises(RuntimeError):
                enricher.get_feature_paper_summary('ore', 'Бор')

        conn.close.assert_called_once()

    def test_count_closes_connection_when_query_raises(self):
        conn = MagicMock()
        conn.execute.side_effect = RuntimeError("query error")

        with patch.object(enricher.db, 'get_connection', return_value=conn):
            with self.assertRaises(RuntimeError):
                enricher.get_feature_paper_count('ore', 'Бор')

        conn.close.assert_called_once()


if __name__ == '__main__':
    unittest.main()
