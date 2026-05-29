"""Reproducing tests for the rruff-local cluster (phase B) findings.

Findings:
1. _calculate_cell_volume raises math domain error for inconsistent cell
   angles because the sqrt discriminant can go negative (no clamp).
2. get_mineral_data's fuzzy fallback uses a bidirectional substring match;
   the reverse clause (indexed_name in query) lets a *different* mineral's
   full dataset be returned for a related query (e.g. 'Ferro-actinolite'
   returning 'Actinolite').
3. search_minerals reads per-mineral category keys with bare subscripts,
   so an older/partial index entry missing a category key raises KeyError
   even though get_mineral_data handles the same data defensively.
"""

import os

os.environ.setdefault('FLASK_ENV', 'testing')
os.environ.setdefault('SECRET_KEY', 'test-secret')
os.environ.setdefault('REDIS_URL', '')
os.environ.setdefault('SESSION_TYPE', 'filesystem')
os.environ.setdefault('SESSION_FILE_DIR', '/tmp/museum-test-b-rruff-local')

import tempfile
import unittest

from local_rruff_data import LocalRRUFFData


def _make_empty_manager(tmpdir):
    """Build a manager over an empty data dir (well-formed empty index)."""
    return LocalRRUFFData(data_path=tmpdir)


class CellVolumeDomainTests(unittest.TestCase):
    """_calculate_cell_volume must not crash on inconsistent angles."""

    def test_inconsistent_angles_do_not_raise(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            manager = _make_empty_manager(tmpdir)
            # Physically inconsistent angle triple: the discriminant
            # 1 - cos^2a - cos^2b - cos^2g + 2 cosa cosb cosg goes negative.
            cell = {'a': 5.0, 'b': 5.0, 'c': 5.0,
                    'alpha': 170.0, 'beta': 20.0, 'gamma': 20.0}
            # Before the fix this raises ValueError: math domain error.
            volume = manager._calculate_cell_volume(cell)
            self.assertIsInstance(volume, float)
            self.assertGreaterEqual(volume, 0.0)

    def test_orthogonal_cell_volume_is_correct(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            manager = _make_empty_manager(tmpdir)
            cell = {'a': 2.0, 'b': 3.0, 'c': 4.0,
                    'alpha': 90.0, 'beta': 90.0, 'gamma': 90.0}
            volume = manager._calculate_cell_volume(cell)
            self.assertAlmostEqual(volume, 24.0, places=4)


class FuzzyMatchTests(unittest.TestCase):
    """A related query must not silently return another mineral's data."""

    def _seed(self, manager):
        manager._index['minerals'] = {
            'Actinolite': {
                'rruff_ids': ['R040063'],
                'powder': [{'filename': 'act.txt', 'rruff_id': 'R040063-1',
                            'format': 'XY_Processed', 'path': '/none/act.txt'}],
                'raman': [],
                'infrared': [],
                'chemistry': [],
                'images': []
            }
        }
        manager._index['rruff_ids'] = {'R040063': 'Actinolite'}

    def test_reverse_substring_does_not_return_other_mineral(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            manager = _make_empty_manager(tmpdir)
            self._seed(manager)
            # 'Actinolite' is a substring of 'Ferro-actinolite'. The reverse
            # clause must NOT match: Ferro-actinolite is a distinct mineral
            # and there is no Ferro-actinolite data indexed.
            result = manager.get_mineral_data('Ferro-actinolite', include_data=False)
            self.assertIsNone(result)

    def test_forward_substring_still_matches(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            manager = _make_empty_manager(tmpdir)
            self._seed(manager)
            # A genuine partial query (query is a substring of indexed name)
            # should still resolve.
            result = manager.get_mineral_data('Actino', include_data=False)
            self.assertIsNotNone(result)
            self.assertEqual(result['mineral_name'], 'Actinolite')

    def test_exact_match_still_works(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            manager = _make_empty_manager(tmpdir)
            self._seed(manager)
            result = manager.get_mineral_data('actinolite', include_data=False)
            self.assertIsNotNone(result)
            self.assertEqual(result['mineral_name'], 'Actinolite')


class SearchMineralsRobustnessTests(unittest.TestCase):
    """search_minerals must tolerate entries missing category keys."""

    def test_partial_entry_does_not_raise_keyerror(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            manager = _make_empty_manager(tmpdir)
            # Old-format entry: missing 'chemistry' (and others) key.
            manager._index['minerals'] = {
                'Quartz': {
                    'rruff_ids': ['R040031'],
                    'powder': [{'filename': 'q.txt'}],
                    'raman': [],
                    'infrared': []
                    # 'chemistry' and 'images' intentionally absent
                }
            }
            # Before the fix this raises KeyError: 'chemistry'.
            results = manager.search_minerals('quartz')
            self.assertEqual(len(results), 1)
            entry = results[0]
            self.assertEqual(entry['mineral_name'], 'Quartz')
            self.assertTrue(entry['has_powder'])
            self.assertFalse(entry['has_chemistry'])
            self.assertFalse(entry['has_images'])


if __name__ == '__main__':
    unittest.main()
