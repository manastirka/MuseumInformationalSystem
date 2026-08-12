"""Revizija 2026-08, stavka 4: Sanja/Bilja zbirke.

Pokriva: (1) probe kvar sa podešenim DATABASE_URL prekida rad umesto tihog
JSON fallback-a; (2) Sanja edit ide row-level (bez replace/delete-all) uz
verziju i odbijanje stale write-a; (3) Bilja view proverava povratne
vrednosti update/delete pre flash-a; (4) demo primerci samo uz eksplicitan
DEMO_MODE/TESTING — u produkciji CollectionUnavailableError (503).
"""

import os

os.environ.setdefault('FLASK_ENV', 'testing')
os.environ.setdefault('SECRET_KEY', 'test-secret')
os.environ.setdefault('REDIS_URL', '')
os.environ.setdefault('SESSION_TYPE', 'filesystem')
os.environ.setdefault('SESSION_FILE_DIR', '/tmp/museum-test-revizija-zbirke')

from unittest import mock

import pytest
from flask import Flask

import bilja_collections_db
import collection_management_views as cmv
from collection_bootstrap_support import (
    CollectionBootstrapSupport,
    CollectionUnavailableError,
)


class _StaleError(RuntimeError):
    pass


def _fake_pg():
    fake = mock.MagicMock()
    fake.SanjaStaleWriteError = _StaleError
    return fake


def _make_app():
    app = Flask(__name__)
    app.secret_key = 'test-secret'
    app.add_url_rule('/sanja', 'sanja_paleogene_neogene_mammals', lambda: '')
    app.add_url_rule('/bilja-kenoz', 'bilja_kenozojske_invertebrate', lambda: '')
    app.add_url_rule('/museum', 'museum_databases', lambda: '')
    return app


def _get_flashes():
    from flask import get_flashed_messages
    return get_flashed_messages(with_categories=True)


_SANJA_ITEM = {
    'id': 5,
    'source_row': 6,
    'specimen_name': 'Mammuthus',
    'collection_group': 'Крупни сисари - палеоген/неоген',
    'updated_at': '2026-08-01T10:00:00+00:00',
}


# ---------------------------------------------------------------------------
# Sanja: probe kvar ne sme tiho da preusmeri na JSON
# ---------------------------------------------------------------------------

def test_sanja_probe_kvar_prekida_umesto_json_fallbacka():
    fake = mock.MagicMock()
    fake.sanja_table_exists.side_effect = RuntimeError('connection refused')
    with mock.patch.dict(os.environ, {'DATABASE_URL': 'postgresql://x'}), \
         mock.patch.dict('sys.modules', {'phase3a_databases': fake}):
        with pytest.raises(RuntimeError):
            cmv._sanja_pg()


def test_sanja_probe_kvar_u_formi_javlja_gresku_bez_upisa():
    app = _make_app()
    with mock.patch.object(cmv, '_sanja_pg', side_effect=RuntimeError('down')):
        with app.test_request_context(
            '/admin/edit_sanja/5', method='POST',
            data={'specimen_name': 'X'},
        ):
            resp = cmv.handle_edit_sanja_paleogene_neogene_mammal_item('5')
            flashes = _get_flashes()
    categories = {cat for cat, _ in flashes}
    assert 'success' not in categories
    assert 'danger' in categories
    assert resp.status_code in (301, 302)


# ---------------------------------------------------------------------------
# Sanja: edit je row-level, sa verzijom; stale write se odbija
# ---------------------------------------------------------------------------

def test_sanja_edit_koristi_row_level_update_sa_verzijom():
    app = _make_app()
    fake = _fake_pg()
    fake.get_sanja_specimen.return_value = dict(_SANJA_ITEM)
    fake.update_sanja_specimen.return_value = True
    with mock.patch.object(cmv, '_sanja_pg', return_value=fake), \
         mock.patch.object(cmv, '_refresh_sanja_app_cache'):
        with app.test_request_context(
            '/admin/edit_sanja/5', method='POST',
            data={'specimen_name': 'Mammuthus novi',
                  '_version': '2026-08-01T10:00:00+00:00'},
        ):
            resp = cmv.handle_edit_sanja_paleogene_neogene_mammal_item('5')
            flashes = _get_flashes()

    assert resp.status_code in (301, 302)
    fake.update_sanja_specimen.assert_called_once()
    args = fake.update_sanja_specimen.call_args[0]
    assert args[0] == 5
    assert args[1]['specimen_name'] == 'Mammuthus novi'
    assert 'updated_at' not in args[1]
    assert args[2] == '2026-08-01T10:00:00+00:00'
    # UI edit ne sme da radi ceo-payload upis (delete-all-not-in-list)
    fake.replace_sanja_specimens.assert_not_called()
    assert {cat for cat, _ in flashes} == {'success'}


def test_sanja_stale_write_se_odbija_bez_uspeha():
    app = _make_app()
    fake = _fake_pg()
    fake.get_sanja_specimen.return_value = dict(_SANJA_ITEM)
    fake.update_sanja_specimen.side_effect = _StaleError('stale')
    with mock.patch.object(cmv, '_sanja_pg', return_value=fake), \
         mock.patch.object(cmv, '_refresh_sanja_app_cache'):
        with app.test_request_context(
            '/admin/edit_sanja/5', method='POST',
            data={'specimen_name': 'X', '_version': 'zastarela-verzija'},
        ):
            resp = cmv.handle_edit_sanja_paleogene_neogene_mammal_item('5')
            flashes = _get_flashes()

    categories = {cat for cat, _ in flashes}
    assert 'success' not in categories
    assert 'danger' in categories
    fake.replace_sanja_specimens.assert_not_called()
    assert resp.status_code in (301, 302)


# ---------------------------------------------------------------------------
# Bilja: povratna vrednost update/delete se proverava pre flash-a
# ---------------------------------------------------------------------------

def test_bilja_update_nestalog_primerka_ne_javlja_uspeh():
    app = _make_app()
    item = {'id': 3, 'redni_broj': 3}
    with mock.patch.object(bilja_collections_db, 'find_specimen', return_value=item), \
         mock.patch.object(bilja_collections_db, 'update_specimen', return_value=False):
        with app.test_request_context(
            '/admin/edit_bilja/bilja_kenozojske_invertebrate/3',
            method='POST', data={'redni_broj': '3'},
        ):
            resp = cmv.handle_edit_bilja_item('bilja_kenozojske_invertebrate', 3)
            flashes = _get_flashes()

    categories = {cat for cat, _ in flashes}
    assert 'success' not in categories
    assert 'danger' in categories
    assert resp.status_code in (301, 302)


def test_bilja_delete_nestalog_primerka_ne_javlja_uspeh_ni_audit():
    app = _make_app()
    item = {'id': 3, 'redni_broj': 3}
    with mock.patch.object(bilja_collections_db, 'find_specimen', return_value=item), \
         mock.patch.object(bilja_collections_db, 'delete_specimen', return_value=False), \
         mock.patch.object(cmv.audit_support, 'record_audit') as record_audit:
        with app.test_request_context(
            '/admin/edit_bilja/bilja_kenozojske_invertebrate/3',
            method='POST', data={'_action': 'delete'},
        ):
            resp = cmv.handle_edit_bilja_item('bilja_kenozojske_invertebrate', 3)
            flashes = _get_flashes()

    categories = {cat for cat, _ in flashes}
    assert 'success' not in categories
    assert 'danger' in categories
    record_audit.assert_not_called()
    assert resp.status_code in (301, 302)


# ---------------------------------------------------------------------------
# Demo primerci: samo uz eksplicitan DEMO_MODE/TESTING
# ---------------------------------------------------------------------------

def _support(database_url, phase3a):
    return CollectionBootstrapSupport(
        lazy_loaded_dict_cls=lambda loader, label: {},
        database_url=database_url,
        phase3a_databases=phase3a,
    )


def _production_env():
    env = {k: v for k, v in os.environ.items()
           if k not in ('FLASK_ENV', 'TESTING', 'DEMO_MODE')}
    return mock.patch.dict(os.environ, env, clear=True)


def test_demo_fallback_zabranjen_u_produkciji_bez_baze():
    support = _support(None, None)
    with _production_env():
        with pytest.raises(CollectionUnavailableError):
            support.load_collection_database('botany', {'specimens': []})


def test_demo_fallback_zabranjen_u_produkciji_kad_baza_padne():
    fake = mock.MagicMock()
    fake.get_botany_collection.side_effect = RuntimeError('db down')
    support = _support('postgresql://x', fake)
    with _production_env():
        with pytest.raises(CollectionUnavailableError):
            support.load_collection_database('botany', {'specimens': []})


def test_demo_fallback_dozvoljen_uz_demo_mode():
    support = _support(None, None)
    with _production_env(), mock.patch.dict(os.environ, {'DEMO_MODE': '1'}):
        assert support.load_collection_database('botany', {'x': 1}) == {'x': 1}


def test_demo_fallback_dozvoljen_u_test_okruzenju():
    # FLASK_ENV=testing je postavljen na vrhu fajla — kao u celoj sviti.
    support = _support(None, None)
    assert support.load_collection_database('botany', {'x': 1}) == {'x': 1}
