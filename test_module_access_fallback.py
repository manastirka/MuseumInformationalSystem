"""Regresija: pad baze NE sme tiho da vrati podrazumevane (šire) dozvole.

Pokriva zahtev iz ANALIZA-2026-07 (zadatak #2):
  1) DB greška uz postojeći keš -> služi se POSLEDNJA POZNATA vrednost (LKG),
     nikad tihi default; greška se loguje na ERROR nivou.
  2) DB greška bez keša (hladni start) -> fail closed: najrestriktivnije dozvole
     (default_access=False, prazni authorized/restricted); ERROR log.
  3) ISTI obrazac na deljenom helperu (system_settings, dashboard_prefs).
"""

import logging
import unittest
from unittest.mock import MagicMock

import module_access_support as mas


def _raising_conn(message='db unavailable'):
    """get_postgres_connection koji pukne čim se pozove (kao pad baze)."""
    return MagicMock(side_effect=RuntimeError(message))


class _OneRowCursor:
    def __init__(self, value):
        self._value = value
        self.executed = []

    def __enter__(self):
        return self

    def __exit__(self, *a):
        return False

    def execute(self, query, params=None):
        self.executed.append((query, params))

    def fetchone(self):
        # SELECT setting_value ... -> vrati red; CREATE TABLE i sl. -> None
        if self.executed and 'SELECT' in self.executed[-1][0]:
            return {'setting_value': self._value}
        return None


class _OneRowConn:
    def __init__(self, value):
        self.cursor_obj = _OneRowCursor(value)

    def __enter__(self):
        return self

    def __exit__(self, *a):
        return False

    def cursor(self):
        return self.cursor_obj

    def commit(self):
        pass

    def close(self):
        pass


def _healthy_conn_factory(value):
    return lambda: _OneRowConn(value)


class ModuleAccessFallbackTests(unittest.TestCase):
    def setUp(self):
        # Izoluj procesni keš između testova.
        mas._db_setting_failure_cache.clear()
        mas._last_known_good.clear()
        self.default_access = {
            'timesheet': {
                'name': 'Радне листе',
                'default_access': True,     # svi po difoltu
                'restricted_users': [],
            },
            'mineral_database': {
                'name': 'База минерала',
                'default_access': False,
                'authorized_users': ['admin', 'aca.lukovic@nhmbeo.rs'],
            },
        }

    # --- 1) LKG: postojeći korisnik zadržava dozvole iz keša na pad baze ---
    def test_db_failure_serves_last_known_good(self):
        # Prvi uspešan load iz baze: mineral_database dozvoljen SAMO adminu
        # (npr. aci je pristup opozvan), timesheet ostaje podrazumevan.
        overrides = {'mineral_database': {'authorized_users': ['admin']}}
        good = mas.load_module_access_data(
            module_access_file='/tmp/unused.json',
            current_mtime=None,
            default_access=self.default_access,
            get_postgres_connection=_healthy_conn_factory(overrides),
        )
        self.assertEqual(good['mineral_database']['authorized_users'], ['admin'])

        # Sada baza pada. Mora se poslužiti LKG (opoziv i dalje važi),
        # a NE tihi default koji bi vratio aci pristup.
        with self.assertLogs('module_access_support', level='ERROR') as logs:
            served = mas.load_module_access_data(
                module_access_file='/tmp/unused.json',
                current_mtime=None,
                default_access=self.default_access,
                get_postgres_connection=_raising_conn(),
            )
        self.assertEqual(
            served['mineral_database']['authorized_users'], ['admin'],
            'Pad baze je vratio opozvanog korisnika (tihi default) umesto LKG',
        )
        self.assertTrue(any('last-known-good' in m.lower() for m in logs.output))

    # --- 2) Hladni start + baza nedostupna -> fail closed (najrestriktivnije) ---
    def test_cold_start_db_down_fails_closed(self):
        with self.assertLogs('module_access_support', level='ERROR') as logs:
            served = mas.load_module_access_data(
                module_access_file='/tmp/unused.json',
                current_mtime=None,
                default_access=self.default_access,
                get_postgres_connection=_raising_conn(),
            )
        # timesheet po difoltu daje pristup SVIMA (default_access=True) — na
        # hladnom startu bez keša to NE sme da procuri.
        self.assertFalse(
            served['timesheet']['default_access'],
            'Hladni start bez baze je zadržao default_access=True (najšire) za timesheet',
        )
        self.assertEqual(served['timesheet'].get('restricted_users'), [])
        self.assertEqual(served['mineral_database']['default_access'], False)
        self.assertEqual(served['mineral_database'].get('authorized_users'), [])
        self.assertTrue(any('fail' in m.lower() or 'restrict' in m.lower() for m in logs.output))

    # --- 3a) Deljeni helper: DB greška bez keša baca (ne vraća tihi default) ---
    def test_shared_loader_raises_without_cache(self):
        with self.assertRaises(mas.SharedSettingsUnavailable):
            with self.assertLogs('module_access_support', level='ERROR'):
                mas.load_json_settings_data(
                    setting_key='system_settings',
                    default_value={'smtp': 'default'},
                    get_postgres_connection=_raising_conn(),
                    file_path=None,
                    current_mtime=None,
                )

    # --- 3b) Deljeni helper: DB greška uz keš služi LKG, ne default ---
    def test_shared_loader_serves_cache_on_failure(self):
        mas.load_json_settings_data(
            setting_key='system_settings',
            default_value={},
            get_postgres_connection=_healthy_conn_factory({'smtp': 'real.host'}),
        )
        with self.assertLogs('module_access_support', level='ERROR'):
            served = mas.load_json_settings_data(
                setting_key='system_settings',
                default_value={'smtp': 'default'},
                get_postgres_connection=_raising_conn(),
            )
        self.assertEqual(served, {'smtp': 'real.host'})

    # --- Regres: nekonfigurisan DB (dev, file mode) i dalje radi bez izuzetka ---
    def test_file_mode_no_db_still_defaults(self):
        served = mas.load_module_access_data(
            module_access_file='/tmp/unused.json',
            current_mtime=None,
            default_access=self.default_access,
            get_postgres_connection=None,
        )
        # bez baze i bez fajla -> podrazumevano ponašanje (merge praznih override-a)
        self.assertEqual(served['timesheet']['default_access'], True)


if __name__ == '__main__':
    logging.basicConfig(level=logging.CRITICAL)
    unittest.main()
