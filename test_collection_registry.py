"""Tests for the central collection registry and generic list routes."""

import os
import subprocess
import sys
from types import SimpleNamespace
from unittest.mock import MagicMock, patch

import pytest

os.environ.setdefault('FLASK_ENV', 'testing')
os.environ.setdefault('SECRET_KEY', 'test-secret')
os.environ.setdefault('REDIS_URL', '')
os.environ.setdefault('SESSION_TYPE', 'filesystem')
os.environ.setdefault('SESSION_FILE_DIR', '/tmp/museum-test-flask-session-collection-registry')

import app as museum_app
import collection_registry
import museum_overview_views
from collection_registry import (
    COLLECTION_LIST_ENTRIES,
    COLLECTION_LIST_ENTRY_BY_TYPE,
    COLLECTION_TYPE_MODULE_MAP,
    CollectionListEntry,
    build_collection_database_map,
    get_collection_form_info,
    get_collection_route_map,
    get_overview_collection_type_map,
    resolve_collection_database,
)


class TestCollectionRegistry:
    def test_all_entries_have_unique_identifiers(self):
        types = [entry.collection_type for entry in COLLECTION_LIST_ENTRIES]
        routes = [entry.route_slug for entry in COLLECTION_LIST_ENTRIES]
        modules = [entry.module_key for entry in COLLECTION_LIST_ENTRIES]

        assert len(types) == len(set(types))
        assert len(routes) == len(set(routes))
        assert len(modules) == len(set(modules))

    def test_module_map_includes_mineral_and_all_list_entries(self):
        for entry in COLLECTION_LIST_ENTRIES:
            assert COLLECTION_TYPE_MODULE_MAP[entry.collection_type] == entry.module_key
        assert COLLECTION_TYPE_MODULE_MAP['mineral'] == 'mineral_database'

    def test_route_and_form_info_match_registry(self):
        route_map = get_collection_route_map()
        form_info = get_collection_form_info()

        for entry in COLLECTION_LIST_ENTRIES:
            assert route_map[entry.collection_type] == entry.route_slug
            assert form_info[entry.collection_type]['name'] == entry.collection_name
            assert form_info[entry.collection_type]['route'] == entry.route_slug

    def test_bilja_entries_loaded_from_pg_registry(self):
        bilja_entries = [
            entry for entry in COLLECTION_LIST_ENTRIES
            if entry.collection_type.startswith('bilja_')
        ]
        assert len(bilja_entries) == 6
        for entry in bilja_entries:
            assert entry.strip_source_file is True
            assert entry.collection_export_enabled is False

    def test_build_collection_database_map_covers_all_registry_entries(self):
        # get_meteorite_collection_database only caches (and so only returns a
        # stable object) when PG has specimens; stub it so the wiring — the map
        # resolves the meteorite entry through that getter — is what's asserted.
        meteorite_sentinel = {'specimens': [], 'statistics': {}}
        with patch.object(
            museum_app, 'get_meteorite_collection_database',
            return_value=meteorite_sentinel,
        ):
            database_map = build_collection_database_map(museum_app)
        assert set(database_map) == {entry.module_key for entry in COLLECTION_LIST_ENTRIES}
        assert database_map['botany_collection'] is museum_app.BOTANY_COLLECTION_DATABASE
        assert database_map['meteorite_collection'] is meteorite_sentinel


class TestCollectionListRoutes:
    base_url = 'https://localhost'

    def _login_admin(self, client):
        with client.session_transaction() as sess:
            sess['user_id'] = 1
            sess['user_email'] = 'user@example.com'
            sess['user_name'] = 'Test User'
            sess['user_role'] = 'admin'
            sess['is_admin'] = True

    def test_all_registry_routes_are_registered(self):
        for entry in COLLECTION_LIST_ENTRIES:
            endpoint = f'collections.{entry.route_slug}'
            assert endpoint in museum_app.app.view_functions, endpoint

    @pytest.mark.parametrize('collection_type', ['botany', 'bilja_skoljke_tadic'])
    def test_generic_route_delegates_to_renderer(self, collection_type):
        entry = COLLECTION_LIST_ENTRY_BY_TYPE[collection_type]
        client = museum_app.app.test_client()
        self._login_admin(client)

        with patch.object(
            museum_app.collection_management_views,
            'render_standard_collection_database',
            return_value=museum_app.app.response_class('ok', status=200),
        ) as mocked_handler:
            response = client.get(f'/admin/{entry.route_slug}', base_url=self.base_url)

        assert response.status_code == 200
        kwargs = mocked_handler.call_args.kwargs
        assert kwargs['collection_type'] == entry.collection_type
        assert kwargs['collection_name'] == entry.collection_name

    def test_botany_route_preserves_existing_contract(self):
        client = museum_app.app.test_client()
        self._login_admin(client)

        with patch.object(
            museum_app.collection_management_views,
            'render_standard_collection_database',
            return_value=museum_app.app.response_class('ok', status=200),
        ) as mocked_handler:
            response = client.get('/admin/botany_collection', base_url=self.base_url)

        assert response.status_code == 200
        mocked_handler.assert_called_once_with(
            collection_name='Ботаничка збирка',
            collection_icon='bi-flower1',
            collection_type='botany',
            records=museum_app.BOTANY_COLLECTION_DATABASE['specimens'],
            statistics=museum_app.BOTANY_COLLECTION_DATABASE['statistics'],
            prepare_collection_records_for_display=museum_app.prepare_collection_records_for_display,
            get_qr_collection_action_url=museum_app.get_qr_collection_action_url,
        )

    def test_meteorite_route_still_uses_specialized_renderer(self):
        client = museum_app.app.test_client()
        self._login_admin(client)

        with patch.object(
            museum_app.collection_management_views,
            'render_meteorite_collection',
            return_value=museum_app.app.response_class('ok', status=200),
        ) as mocked_handler:
            response = client.get('/admin/meteorite_collection', base_url=self.base_url)

        assert response.status_code == 200
        mocked_handler.assert_called_once_with(
            get_meteorite_collection_database=museum_app.get_meteorite_collection_database,
            prepare_collection_records_for_display=museum_app.prepare_collection_records_for_display,
            get_qr_collection_action_url=museum_app.get_qr_collection_action_url,
        )


class TestCollectionRegistryEdgeCases:
    def test_collection_total_handles_missing_and_empty_databases(self):
        assert museum_overview_views._collection_total(None) is None
        assert museum_overview_views._collection_total({}) is None
        assert museum_overview_views._collection_total({'specimens': [{}, {}]}) == 2
        assert museum_overview_views._collection_total(
            {'records': ['a'], 'statistics': {'total_records': 5}},
            stats_key='total_records',
        ) == 5

    def test_resolve_collection_database_returns_none_for_missing_attr(self):
        entry = CollectionListEntry(
            'ghost', 'ghost_collection', 'ghost_collection',
            'Ghost', 'bi-ghost', 'MISSING_COLLECTION_DATABASE',
        )
        fake_app = SimpleNamespace(get_meteorite_collection_database=lambda: {'specimens': []})
        assert resolve_collection_database(fake_app, entry) is None

    def test_build_collection_database_map_tolerates_missing_database_attr(self):
        fake_app = SimpleNamespace(
            get_meteorite_collection_database=lambda: {'specimens': [], 'statistics': {}},
        )
        with patch.object(
            collection_registry,
            'COLLECTION_LIST_ENTRIES',
            (
                CollectionListEntry(
                    'ghost', 'ghost_collection', 'ghost_collection',
                    'Ghost', 'bi-ghost', 'MISSING_COLLECTION_DATABASE',
                ),
            ),
        ):
            database_map = collection_registry.build_collection_database_map(fake_app)
        assert database_map == {'ghost_collection': None}

    def test_overview_collection_type_map_matches_registry_module_keys(self):
        type_map = get_overview_collection_type_map()
        for entry in COLLECTION_LIST_ENTRIES:
            assert type_map[entry.module_key] == entry.collection_type

    @pytest.mark.parametrize('collection_type', ['botany', 'bilja_skoljke_tadic', 'meteorite'])
    def test_unauthenticated_collection_route_redirects_to_login(self, collection_type):
        entry = COLLECTION_LIST_ENTRY_BY_TYPE[collection_type]
        client = museum_app.app.test_client()
        response = client.get(f'/admin/{entry.route_slug}', base_url='https://localhost')
        assert response.status_code == 302
        assert '/login' in response.headers['Location']

    @pytest.mark.parametrize('collection_type', ['botany', 'bilja_skoljke_tadic'])
    def test_collection_route_blocks_user_without_module_access(self, collection_type):
        entry = COLLECTION_LIST_ENTRY_BY_TYPE[collection_type]
        client = museum_app.app.test_client()
        with client.session_transaction() as sess:
            sess['user_id'] = 2
            sess['user_email'] = 'curator@example.com'
            sess['user_role'] = 'employee'

        original_checker = museum_app.app.user_has_module_access
        museum_app.app.user_has_module_access = lambda email, role, key: False
        try:
            response = client.get(f'/admin/{entry.route_slug}', base_url='https://localhost')
        finally:
            museum_app.app.user_has_module_access = original_checker

        assert response.status_code == 302
        assert '/dashboard' in response.headers['Location']

    def test_export_unknown_collection_type_redirects_to_overview(self):
        client = museum_app.app.test_client()
        with client.session_transaction() as sess:
            sess['user_id'] = 1
            sess['user_email'] = 'user@example.com'
            sess['user_role'] = 'admin'

        response = client.get(
            '/admin/export_collection_to_pdf/not_a_real_collection',
            base_url='https://localhost',
        )
        assert response.status_code == 302
        assert '/admin/museum_databases' in response.headers['Location']

    def test_edit_bilja_unknown_collection_redirects_to_overview(self):
        client = museum_app.app.test_client()
        with client.session_transaction() as sess:
            sess['user_id'] = 1
            sess['user_email'] = 'user@example.com'
            sess['user_role'] = 'admin'

        response = client.get(
            '/admin/edit_bilja/not_a_real_collection/1',
            base_url='https://localhost',
        )
        assert response.status_code == 302
        assert '/admin/museum_databases' in response.headers['Location']

    def test_sanja_collection_strips_source_file(self):
        entry = COLLECTION_LIST_ENTRY_BY_TYPE['sanja_paleogene_neogene_mammals']
        client = museum_app.app.test_client()
        with client.session_transaction() as sess:
            sess['user_id'] = 1
            sess['user_email'] = 'user@example.com'
            sess['user_role'] = 'admin'

        # The real database is loaded from environment data that an empty test
        # DB does not have; stub it so the strip behavior is what's under test.
        stub_database = {
            'specimens': [
                {'id': 1, 'name': 'Mammut', 'source_file': 'sanja.xlsx'},
                {'id': 2, 'name': 'Deinotherium', 'source_file': 'sanja.xlsx'},
            ],
            'statistics': {'total': 2},
        }
        with patch.object(
            museum_app, entry.database_attr, stub_database,
        ), patch.object(
            museum_app.collection_management_views,
            'render_standard_collection_database',
            return_value=museum_app.app.response_class('ok', status=200),
        ) as mocked_handler:
            response = client.get(f'/admin/{entry.route_slug}', base_url='https://localhost')

        assert response.status_code == 200
        records = mocked_handler.call_args.kwargs['records']
        assert records
        assert all('source_file' not in record for record in records)
        assert [record['name'] for record in records] == ['Mammut', 'Deinotherium']

    def test_museum_overview_renders_with_empty_collection_map(self):
        client = museum_app.app.test_client()
        with client.session_transaction() as sess:
            sess['user_id'] = 1
            sess['user_email'] = 'user@example.com'
            sess['user_role'] = 'admin'

        with patch.object(
            museum_app.museum_overview_views,
            'render_museum_databases',
            return_value=museum_app.app.response_class('ok', status=200),
        ) as mocked_handler:
            response = client.get('/admin/museum_databases', base_url='https://localhost')

        assert response.status_code == 200
        collection_databases = mocked_handler.call_args.kwargs['collection_databases']
        assert set(collection_databases) == {entry.module_key for entry in COLLECTION_LIST_ENTRIES}

    def test_legacy_endpoint_aliases_remain_registered(self):
        for entry in COLLECTION_LIST_ENTRIES:
            assert entry.route_slug in museum_app.app.view_functions


class TestCollectionProductionMode:
    PRODUCTION_ENV = {
        'FLASK_ENV': 'production',
        'SECRET_KEY': 'test-production-secret',
        'REDIS_URL': 'redis://127.0.0.1:6379/0',
        'SESSION_TYPE': 'redis',
        'WORKERS': '1',
        'ENABLE_FALLBACK_AUTH': 'False',
        'WTF_CSRF_ENABLED': 'False',
    }

    def test_production_import_registers_all_registry_routes(self):
        script = """
import os
os.environ.update({env!r})
import app
from collection_registry import COLLECTION_LIST_ENTRIES
missing = [
    entry.route_slug
    for entry in COLLECTION_LIST_ENTRIES
    if f"collections.{{entry.route_slug}}" not in app.app.view_functions
]
if missing:
    raise SystemExit("missing routes: " + ",".join(missing))
if app.app.config.get("FLASK_ENV") != "production":
    raise SystemExit("expected production config")
if app.app.config.get("SESSION_TYPE") != "redis":
    raise SystemExit("expected redis sessions")
print("OK")
""".format(env=self.PRODUCTION_ENV)
        result = subprocess.run(
            [sys.executable, '-c', script],
            cwd=os.path.dirname(__file__),
            capture_output=True,
            text=True,
            check=False,
        )
        assert result.returncode == 0, result.stderr or result.stdout

    def test_production_import_builds_collection_database_map(self):
        script = """
import os
os.environ.update({env!r})
import app
from collection_registry import COLLECTION_LIST_ENTRIES, build_collection_database_map
database_map = build_collection_database_map(app)
expected = {{entry.module_key for entry in COLLECTION_LIST_ENTRIES}}
if set(database_map) != expected:
    raise SystemExit(f"map mismatch: {{set(database_map)!r}} vs {{expected!r}}")
if database_map["botany_collection"] is not app.BOTANY_COLLECTION_DATABASE:
    raise SystemExit("botany database mismatch")
print("OK")
""".format(env=self.PRODUCTION_ENV)
        result = subprocess.run(
            [sys.executable, '-c', script],
            cwd=os.path.dirname(__file__),
            capture_output=True,
            text=True,
            check=False,
        )
        assert result.returncode == 0, result.stderr or result.stdout

    def test_production_config_switches_rate_limit_to_redis_with_multiple_workers(self):
        import config as config_module
        from flask import Flask

        app = Flask(__name__)
        app.config.from_object(config_module.ProductionConfig)
        app.config['SECRET_KEY'] = 'production-secret'
        app.config['RATELIMIT_STORAGE_URL'] = 'memory://'

        with patch.dict(
            os.environ,
            {
                **self.PRODUCTION_ENV,
                'WORKERS': '4',
            },
            clear=False,
        ), patch('logging.handlers.SysLogHandler', side_effect=PermissionError('no syslog')):
            config_module.ProductionConfig.init_app(app)

        assert app.config['RATELIMIT_STORAGE_URL'] == self.PRODUCTION_ENV['REDIS_URL']

    def test_production_museum_databases_route_requires_auth(self):
        script = """
import os
os.environ.update({env!r})
import app
client = app.app.test_client()
response = client.get('/admin/museum_databases', base_url='https://localhost')
if response.status_code != 302 or '/login' not in response.headers.get('Location', ''):
    raise SystemExit(f"expected login redirect, got {{response.status_code}} {{response.headers.get('Location')}}")
print("OK")
""".format(env=self.PRODUCTION_ENV)
        result = subprocess.run(
            [sys.executable, '-c', script],
            cwd=os.path.dirname(__file__),
            capture_output=True,
            text=True,
            check=False,
        )
        assert result.returncode == 0, result.stderr or result.stdout
