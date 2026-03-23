#!/usr/bin/env python3
"""Regression tests for production-readiness fixes."""

import os
import sys
import json
import io
import shutil
import tempfile
import types
import importlib.util
import unittest
from pathlib import Path
from unittest.mock import patch, MagicMock

from flask import Flask, jsonify, session
from PIL import Image

import config as config_module
import security_utils
import image_storage_engine
import image_api
import module_access_support
import admin_system_views
import mail_client


class FakeLogger:
    def __init__(self):
        self.calls = []

    def warning(self, message, extra=None):
        self.calls.append(('warning', message, extra))

    def info(self, message, extra=None):
        self.calls.append(('info', message, extra))

    def debug(self, message, extra=None):
        self.calls.append(('debug', message, extra))


class ConfigTests(unittest.TestCase):
    def test_default_config_is_production(self):
        with patch.dict(os.environ, {}, clear=True):
            self.assertIs(config_module.get_config(None), config_module.ProductionConfig)

    def test_production_config_requires_secret_key(self):
        app = Flask(__name__)
        app.config.from_object(config_module.ProductionConfig)
        app.config['SECRET_KEY'] = None

        with patch.dict(os.environ, {'WORKERS': '1', 'REDIS_URL': 'redis://redis:6379/0'}, clear=False):
            with self.assertRaises(RuntimeError):
                config_module.ProductionConfig.init_app(app)

    def test_production_config_requires_redis_url(self):
        app = Flask(__name__)
        app.config.from_object(config_module.ProductionConfig)
        app.config['SECRET_KEY'] = 'production-secret'

        with patch.dict(os.environ, {'WORKERS': '1', 'REDIS_URL': ''}, clear=False):
            with self.assertRaises(RuntimeError):
                config_module.ProductionConfig.init_app(app)

    def test_production_config_requires_redis_session_type(self):
        app = Flask(__name__)
        app.config.from_object(config_module.ProductionConfig)
        app.config['SECRET_KEY'] = 'production-secret'

        with patch.dict(
            os.environ,
            {'WORKERS': '1', 'REDIS_URL': 'redis://redis:6379/0', 'SESSION_TYPE': 'filesystem'},
            clear=False,
        ):
            with self.assertRaises(RuntimeError):
                config_module.ProductionConfig.init_app(app)

    def test_production_config_tolerates_missing_syslog(self):
        app = Flask(__name__)
        app.config.from_object(config_module.ProductionConfig)
        app.config['SECRET_KEY'] = 'production-secret'

        with patch.dict(
            os.environ,
            {'WORKERS': '1', 'REDIS_URL': 'redis://redis:6379/0', 'SESSION_TYPE': 'redis'},
            clear=False,
        ):
            with patch('logging.handlers.SysLogHandler', side_effect=PermissionError('no syslog')):
                config_module.ProductionConfig.init_app(app)

    def test_production_config_uses_redis_rate_limit_with_multiple_workers(self):
        app = Flask(__name__)
        app.config.from_object(config_module.ProductionConfig)
        app.config['SECRET_KEY'] = 'production-secret'
        app.config['RATELIMIT_STORAGE_URL'] = 'memory://'

        with patch.dict(
            os.environ,
            {'WORKERS': '4', 'REDIS_URL': 'redis://redis:6379/0', 'SESSION_TYPE': 'redis'},
            clear=False,
        ):
            with patch('logging.handlers.SysLogHandler', side_effect=PermissionError('no syslog')):
                config_module.ProductionConfig.init_app(app)

        self.assertEqual(app.config['RATELIMIT_STORAGE_URL'], 'redis://redis:6379/0')

    def test_production_config_defaults_rate_limit_storage_to_redis(self):
        app = Flask(__name__)
        app.config.from_object(config_module.ProductionConfig)
        app.config['SECRET_KEY'] = 'production-secret'
        app.config['RATELIMIT_STORAGE_URL'] = 'memory://'

        with patch.dict(
            os.environ,
            {'WORKERS': '1', 'REDIS_URL': 'redis://redis:6379/0', 'SESSION_TYPE': 'redis'},
            clear=False,
        ):
            with patch('logging.handlers.SysLogHandler', side_effect=PermissionError('no syslog')):
                config_module.ProductionConfig.init_app(app)

        self.assertEqual(app.config['RATELIMIT_STORAGE_URL'], 'redis://redis:6379/0')
        self.assertEqual(app.config['SESSION_TYPE'], 'redis')


class SecurityUtilsTests(unittest.TestCase):
    def test_init_login_tracker_preserves_object_identity(self):
        original_tracker = security_utils.login_tracker
        configured_tracker = security_utils.init_login_tracker(None)

        self.assertIs(original_tracker, configured_tracker)

    def test_init_login_tracker_passes_redis_url(self):
        original_tracker = security_utils.login_tracker
        fake_tracker = types.SimpleNamespace(use_redis=True, redis_client='client', attempts={}, lockouts={})

        with patch('security_utils.LoginAttemptTracker', return_value=fake_tracker) as tracker_cls:
            configured_tracker = security_utils.init_login_tracker('redis://redis:6379/0')

        tracker_cls.assert_called_once_with(redis_url='redis://redis:6379/0')
        self.assertIs(configured_tracker, original_tracker)
        self.assertTrue(configured_tracker.use_redis)

    def test_module_access_required_uses_current_app_checker(self):
        app = Flask(__name__)
        app.secret_key = 'test-secret'
        app.user_has_module_access = lambda email, role, module_key: (
            email == 'user@example.com' and role == 'user' and module_key == 'maps'
        )

        @app.route('/api/protected')
        @security_utils.module_access_required('maps')
        def protected():
            return jsonify({'success': True})

        client = app.test_client()
        with client.session_transaction() as sess:
            sess['user_id'] = 1
            sess['user_email'] = 'user@example.com'
            sess['user_role'] = 'user'

        response = client.get('/api/protected')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {'success': True})

    def test_log_security_event_uses_user_email_session_key(self):
        app = Flask(__name__)
        app.secret_key = 'test-secret'
        fake_logger = FakeLogger()

        with app.test_request_context('/login'):
            session['user_email'] = 'audit@example.com'

            with patch('logging.getLogger', return_value=fake_logger):
                security_utils.log_security_event('login_success', {'email': 'audit@example.com'})

        self.assertTrue(fake_logger.calls)
        _, _, extra = fake_logger.calls[0]
        self.assertEqual(extra['user_email'], 'audit@example.com')


class FakeCursor:
    def __init__(self, rows=None, one=None):
        self.rows = rows or []
        self.one = one
        self.executed = []

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False

    def execute(self, query, params=None):
        self.executed.append((query, params))

    def fetchall(self):
        return self.rows

    def fetchone(self):
        if self.one is not None:
            return self.one
        if self.rows:
            return self.rows[0]
        return None


class FakeConnection:
    def __init__(self, rows=None, one=None):
        self.cursor_obj = FakeCursor(rows, one=one)
        self.committed = False
        self.rolled_back = False

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False

    def cursor(self):
        return self.cursor_obj

    def commit(self):
        self.committed = True

    def rollback(self):
        self.rolled_back = True

    def close(self):
        pass


class FakeS3Client:
    def __init__(self):
        self.objects = {}

    def upload_file(self, source_path, bucket, key):
        self.objects[(bucket, key)] = Path(source_path).read_bytes()

    def download_file(self, bucket, key, destination_path):
        payload = self.objects[(bucket, key)]
        destination = Path(destination_path)
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(payload)

    def delete_object(self, Bucket, Key):
        self.objects.pop((Bucket, Key), None)

    def list_objects_v2(self, Bucket, Prefix, ContinuationToken=None):
        contents = [
            {'Key': key}
            for (bucket, key), _payload in sorted(self.objects.items())
            if bucket == Bucket and key.startswith(Prefix)
        ]
        return {'Contents': contents, 'IsTruncated': False}


class ImageBackupTests(unittest.TestCase):
    def setUp(self):
        self.tmpdir = Path(tempfile.mkdtemp(prefix='image-backup-test-'))

    def tearDown(self):
        shutil.rmtree(self.tmpdir, ignore_errors=True)

    def _new_engine(self, base_path: Path):
        with patch.object(image_storage_engine.ImageStorageEngine, '_ensure_db_table', return_value=None):
            return image_storage_engine.ImageStorageEngine(str(base_path))

    def _object_storage_env(self):
        return {
            'IMAGE_STORAGE_BACKEND': 'object',
            'AWS_S3_BUCKET': 'museum-images-test',
            'IMAGE_STORAGE_OBJECT_PREFIX': 'museum-images',
        }

    def test_create_local_backup_writes_metadata_manifest(self):
        base_path = self.tmpdir / 'store'
        originals = base_path / 'originals'
        originals.mkdir(parents=True)
        image_id = 'img_1'
        original_file = originals / f'{image_id}.jpg'
        original_file.write_bytes(b'jpeg-bytes')

        fake_row = {
            'image_id': image_id,
            'database_name': 'mineral',
            'entity_type': 'collection_item',
            'entity_id': '42',
            'original_filename': 'original.jpg',
            'file_extension': '.jpg',
            'file_path': str(original_file),
            'thumbnail_small': '',
            'thumbnail_medium': '',
            'thumbnail_large': '',
            'description': 'desc',
            'file_size': 10,
            'file_hash': 'abc123',
            'width': 1,
            'height': 1,
            'custom_metadata': {'label': 'value'},
            'backed_up': False,
            'backup_date': None,
            'created_at': None,
            'updated_at': None,
        }
        fake_conn = FakeConnection([fake_row])
        engine = self._new_engine(base_path)

        with patch('image_storage_engine._get_db_connection', return_value=fake_conn):
            backup_dir = engine.create_local_backup('snapshot')

        self.assertIsNotNone(backup_dir)
        manifest_path = backup_dir / image_storage_engine.BACKUP_METADATA_FILENAME
        self.assertTrue(manifest_path.exists())
        manifest = json.loads(manifest_path.read_text(encoding='utf-8'))
        self.assertEqual(manifest['image_count'], 1)
        self.assertEqual(manifest['images'][0]['image_id'], image_id)

    def test_restore_from_backup_rehydrates_metadata(self):
        base_path = self.tmpdir / 'restore-store'
        backup_dir = self.tmpdir / 'backup'
        originals_backup = backup_dir / 'originals'
        originals_backup.mkdir(parents=True)
        image_id = 'img_restore'
        backup_image = originals_backup / f'{image_id}.jpg'
        Image.new('RGB', (2, 2), color='white').save(backup_image, format='JPEG')
        manifest = {
            'version': 1,
            'images': [{
                'image_id': image_id,
                'database_name': 'mineral',
                'entity_type': 'collection_item',
                'entity_id': '42',
                'original_filename': 'restored.jpg',
                'file_extension': '.jpg',
                'description': 'desc',
                'file_hash': 'abc123',
                'width': 2,
                'height': 2,
                'custom_metadata': {'label': 'value'},
                'backed_up': True,
                'backup_date': None,
                'created_at': None,
                'updated_at': None,
            }]
        }
        (backup_dir / image_storage_engine.BACKUP_METADATA_FILENAME).write_text(
            json.dumps(manifest),
            encoding='utf-8',
        )

        fake_conn = FakeConnection()
        engine = self._new_engine(base_path)

        with patch('image_storage_engine._get_db_connection', return_value=fake_conn):
            with patch.object(engine, '_generate_thumbnails', return_value={}):
                restored = engine.restore_from_backup(str(backup_dir))

        self.assertTrue(restored)
        self.assertTrue((base_path / 'originals' / f'{image_id}.jpg').exists())
        self.assertTrue(fake_conn.committed)
        self.assertTrue(any('INSERT INTO images' in query for query, _ in fake_conn.cursor_obj.executed))

    def test_object_storage_backup_and_restore_round_trip(self):
        fake_client = FakeS3Client()
        fake_boto3 = types.SimpleNamespace(client=lambda service_name, **kwargs: fake_client)
        image_id = 'img_object_restore'
        source_image = self.tmpdir / 'source.jpg'
        Image.new('RGB', (3, 3), color='white').save(source_image, format='JPEG')

        fake_row = {
            'image_id': image_id,
            'database_name': 'mineral',
            'entity_type': 'collection_item',
            'entity_id': '42',
            'original_filename': 'original.jpg',
            'file_extension': '.jpg',
            'file_path': f'object://originals/{image_id}.jpg',
            'thumbnail_small': '',
            'thumbnail_medium': '',
            'thumbnail_large': '',
            'description': 'desc',
            'file_size': source_image.stat().st_size,
            'file_hash': 'abc123',
            'width': 3,
            'height': 3,
            'custom_metadata': {'label': 'value'},
            'backed_up': True,
            'backup_date': None,
            'created_at': None,
            'updated_at': None,
        }
        source_conn = FakeConnection([fake_row])
        restore_conn = FakeConnection()

        with patch.dict(os.environ, self._object_storage_env(), clear=False):
            with patch.dict(sys.modules, {'boto3': fake_boto3}):
                with patch.object(image_storage_engine.ImageStorageEngine, '_ensure_db_table', return_value=None):
                    source_engine = image_storage_engine.ImageStorageEngine(str(self.tmpdir / 'source-store'))
                    restore_engine = image_storage_engine.ImageStorageEngine(str(self.tmpdir / 'restore-store'))

                source_engine.storage_backend.save_file(source_image, 'originals', f'{image_id}.jpg')

                with patch('image_storage_engine._get_db_connection', return_value=source_conn):
                    backup_dir = source_engine.create_local_backup('snapshot-object')

                self.assertIsNotNone(backup_dir)
                self.assertTrue((backup_dir / 'originals' / f'{image_id}.jpg').exists())

                object_key = f'museum-images/originals/{image_id}.jpg'
                fake_client.delete_object(Bucket='museum-images-test', Key=object_key)
                self.assertNotIn(('museum-images-test', object_key), fake_client.objects)

                with patch('image_storage_engine._get_db_connection', return_value=restore_conn):
                    restored = restore_engine.restore_from_backup(str(backup_dir))

        self.assertTrue(restored)
        self.assertIn(('museum-images-test', object_key), fake_client.objects)
        self.assertIn(
            ('museum-images-test', f'museum-images/thumbnails/small/{image_id}.jpg'),
            fake_client.objects,
        )
        self.assertTrue(restore_conn.committed)
        insert_calls = [params for query, params in restore_conn.cursor_obj.executed if 'INSERT INTO images' in query]
        self.assertTrue(insert_calls)
        self.assertEqual(insert_calls[0][6], f'object://originals/{image_id}.jpg')

    def test_backup_to_server_posts_to_receiver_with_token_and_preserves_metadata(self):
        fake_client = FakeS3Client()
        fake_boto3 = types.SimpleNamespace(client=lambda service_name, **kwargs: fake_client)
        image_id = 'img_remote_backup'
        source_image = self.tmpdir / 'remote-source.jpg'
        Image.new('RGB', (4, 4), color='white').save(source_image, format='JPEG')

        source_row = {
            'image_id': image_id,
            'database_name': 'mineral',
            'entity_type': 'collection_item',
            'entity_id': '42',
            'original_filename': 'original.jpg',
            'file_extension': '.jpg',
            'file_path': f'object://originals/{image_id}.jpg',
            'thumbnail_small': '',
            'thumbnail_medium': '',
            'thumbnail_large': '',
            'description': 'desc',
            'file_size': source_image.stat().st_size,
            'file_hash': 'abc123',
            'width': 4,
            'height': 4,
            'custom_metadata': {'label': 'value'},
            'backed_up': False,
            'backup_date': None,
            'created_at': None,
            'updated_at': None,
        }
        select_conn = FakeConnection([source_row])
        receiver_conn = FakeConnection()
        update_conn = FakeConnection()

        receiver_app = Flask(__name__)
        receiver_app.config['TESTING'] = True
        receiver_app.register_blueprint(image_api.image_api, url_prefix='/api/images')
        receiver_client = receiver_app.test_client()

        def fake_post(url, files=None, data=None, headers=None, timeout=None):
            del url, timeout
            uploaded = files['file']
            uploaded.seek(0)
            response = receiver_client.post(
                '/api/images/backup/receive',
                data={
                    'image_id': data['image_id'],
                    'metadata': data['metadata'],
                    'file': (io.BytesIO(uploaded.read()), 'backup.jpg'),
                },
                headers=headers,
                content_type='multipart/form-data',
            )
            return types.SimpleNamespace(status_code=response.status_code, text=response.get_data(as_text=True))

        env = {
            'IMAGE_STORAGE_BACKEND': 'object',
            'AWS_S3_BUCKET': 'museum-images-test',
            'IMAGE_STORAGE_OBJECT_PREFIX': 'museum-images',
            'IMAGE_BACKUP_TOKEN': 'backup-token',
        }
        with patch.dict(os.environ, env, clear=False):
            with patch.dict(sys.modules, {'boto3': fake_boto3}):
                image_storage_engine._image_storage_instances.clear()
                with patch.object(image_storage_engine.ImageStorageEngine, '_ensure_db_table', return_value=None):
                    source_engine = image_storage_engine.ImageStorageEngine(
                        str(self.tmpdir / 'source-store'),
                        'https://backup.example.com',
                    )
                    source_engine.storage_backend.save_file(source_image, 'originals', f'{image_id}.jpg')
                    source_engine.get_image_path = lambda _image_id, size='original': source_engine.storage_backend.resolve_ref(  # noqa: E731
                        f'object://originals/{image_id}.jpg'
                    )

                    with patch('image_storage_engine._get_db_connection', side_effect=[select_conn, receiver_conn, update_conn]):
                        with patch('image_storage_engine.requests.post', side_effect=fake_post):
                            backed_up = source_engine.backup_to_server(image_id)

        self.assertTrue(backed_up)
        self.assertTrue(update_conn.committed)
        receiver_inserts = [params for query, params in receiver_conn.cursor_obj.executed if 'INSERT INTO images' in query]
        self.assertTrue(receiver_inserts)
        self.assertEqual(receiver_inserts[0][1], 'mineral')
        self.assertEqual(receiver_inserts[0][2], 'collection_item')
        self.assertEqual(receiver_inserts[0][3], '42')


class ImageStorageBackendTests(unittest.TestCase):
    def setUp(self):
        self.tmpdir = Path(tempfile.mkdtemp(prefix='image-backend-test-'))

    def tearDown(self):
        shutil.rmtree(self.tmpdir, ignore_errors=True)

    def test_local_backend_uses_storage_refs(self):
        backend = image_storage_engine.LocalFilesystemImageBackend(self.tmpdir)
        backend.initialize()

        storage_ref = backend.build_ref('originals', 'example.jpg')
        self.assertEqual(storage_ref, 'local://originals/example.jpg')
        self.assertEqual(backend.resolve_ref(storage_ref), self.tmpdir / 'originals' / 'example.jpg')
        self.assertTrue(backend.is_managed_ref(storage_ref))

    def test_store_image_persists_backend_refs_in_metadata(self):
        source_image = self.tmpdir / 'source.jpg'
        Image.new('RGB', (4, 4), color='white').save(source_image, format='JPEG')
        fake_conn = FakeConnection()

        with patch.object(image_storage_engine.ImageStorageEngine, '_ensure_db_table', return_value=None):
            engine = image_storage_engine.ImageStorageEngine(str(self.tmpdir / 'store'))

        with patch('image_storage_engine._get_db_connection', return_value=fake_conn):
            image_id = engine.store_image(
                file_path=str(source_image),
                database='mineral',
                entity_type='collection_item',
                entity_id='42',
                description='desc',
                metadata={'label': 'value'},
            )

        self.assertIsNotNone(image_id)
        insert_calls = [params for query, params in fake_conn.cursor_obj.executed if 'INSERT INTO images' in query]
        self.assertTrue(insert_calls)
        file_ref = insert_calls[0][6]
        thumb_small_ref = insert_calls[0][7]
        self.assertTrue(file_ref.startswith('local://originals/'))
        self.assertTrue(thumb_small_ref.startswith('local://thumbnails/small/'))
        resolved = engine.storage_backend.resolve_ref(file_ref)
        self.assertIsNotNone(resolved)
        self.assertTrue(resolved.exists())

    def test_object_backend_saves_and_downloads_via_cache(self):
        source_image = self.tmpdir / 'source.jpg'
        source_image.write_bytes(b'object-storage-test')
        fake_client = FakeS3Client()
        fake_boto3 = types.SimpleNamespace(client=lambda service_name, **kwargs: fake_client)

        env = {
            'IMAGE_STORAGE_BACKEND': 'object',
            'AWS_S3_BUCKET': 'museum-images-test',
            'IMAGE_STORAGE_OBJECT_PREFIX': 'museum-images',
            'IMAGE_STORAGE_CACHE_PATH': str(self.tmpdir / 'cache'),
        }
        with patch.dict(os.environ, env, clear=False):
            with patch.dict(sys.modules, {'boto3': fake_boto3}):
                backend = image_storage_engine.ObjectStorageImageBackend(self.tmpdir / 'object-store')
                backend.initialize()

                storage_ref = backend.save_file(source_image, 'originals', 'example.jpg')
                self.assertEqual(storage_ref, 'object://originals/example.jpg')
                self.assertIn(
                    ('museum-images-test', 'museum-images/originals/example.jpg'),
                    fake_client.objects,
                )

                cached_copy = backend.category_dir('originals') / 'example.jpg'
                cached_copy.unlink()

                resolved = backend.resolve_ref(storage_ref)
                self.assertIsNotNone(resolved)
                self.assertEqual(resolved.read_bytes(), b'object-storage-test')

    def test_store_image_persists_object_storage_refs_in_metadata(self):
        source_image = self.tmpdir / 'source.jpg'
        Image.new('RGB', (4, 4), color='white').save(source_image, format='JPEG')
        fake_conn = FakeConnection()
        fake_client = FakeS3Client()
        fake_boto3 = types.SimpleNamespace(client=lambda service_name, **kwargs: fake_client)

        env = {
            'IMAGE_STORAGE_BACKEND': 'object',
            'AWS_S3_BUCKET': 'museum-images-test',
            'IMAGE_STORAGE_OBJECT_PREFIX': 'museum-images',
            'IMAGE_STORAGE_CACHE_PATH': str(self.tmpdir / 'cache'),
        }
        with patch.dict(os.environ, env, clear=False):
            with patch.dict(sys.modules, {'boto3': fake_boto3}):
                with patch.object(image_storage_engine.ImageStorageEngine, '_ensure_db_table', return_value=None):
                    engine = image_storage_engine.ImageStorageEngine(str(self.tmpdir / 'store'))

                with patch('image_storage_engine._get_db_connection', return_value=fake_conn):
                    image_id = engine.store_image(
                        file_path=str(source_image),
                        database='mineral',
                        entity_type='collection_item',
                        entity_id='42',
                        description='desc',
                        metadata={'label': 'value'},
                    )

        self.assertIsNotNone(image_id)
        insert_calls = [params for query, params in fake_conn.cursor_obj.executed if 'INSERT INTO images' in query]
        self.assertTrue(insert_calls)
        file_ref = insert_calls[0][6]
        thumb_small_ref = insert_calls[0][7]
        self.assertTrue(file_ref.startswith('object://originals/'))
        self.assertTrue(thumb_small_ref.startswith('object://thumbnails/small/'))
        self.assertIn(
            ('museum-images-test', f"museum-images/originals/{Path(file_ref.split('object://', 1)[1]).name}"),
            fake_client.objects,
        )


class SharedSettingsPersistenceTests(unittest.TestCase):
    def test_module_access_loads_from_postgres_shared_settings(self):
        fake_conn = FakeConnection(one={'setting_value': {
            'example': {'authorized_users': ['user@example.com']}
        }})

        loaded = module_access_support.load_module_access_data(
            module_access_file='/tmp/unused.json',
            current_mtime=None,
            default_access={'example': {'authorized_users': [], 'restricted_users': [], 'name': 'Example'}},
            get_postgres_connection=lambda: fake_conn,
        )

        self.assertEqual(loaded['example']['authorized_users'], ['user@example.com'])

    def test_dashboard_preferences_save_writes_postgres_shared_settings(self):
        fake_conn = FakeConnection()

        saved = module_access_support.save_dashboard_preferences_data(
            dashboard_prefs_file='/tmp/unused-dashboard.json',
            dashboard_preferences={'user@example.com': {'enabled_widgets': ['news']}},
            get_postgres_connection=lambda: fake_conn,
        )

        self.assertTrue(saved)
        executed_sql = ' '.join(query for query, _ in fake_conn.cursor_obj.executed)
        self.assertIn('INSERT INTO app_shared_settings', executed_sql)
        self.assertTrue(fake_conn.committed)

    def test_admin_system_settings_load_uses_shared_storage(self):
        fake_conn = FakeConnection(one={'setting_value': {'institution_name': 'Shared Museum'}})

        with patch.dict(os.environ, {'DATABASE_URL': 'postgresql://example'}, clear=False):
            with patch.object(admin_system_views, 'get_postgres_connection', return_value=fake_conn):
                loaded = admin_system_views.load_saved_settings()

        self.assertEqual(loaded['institution_name'], 'Shared Museum')


class MailSettingsPersistenceTests(unittest.TestCase):
    def setUp(self):
        self.tmpdir = Path(tempfile.mkdtemp(prefix='mail-settings-test-'))
        self.addCleanup(shutil.rmtree, self.tmpdir, ignore_errors=True)
        self.original_fernet = mail_client._fernet_instance
        self.original_table_flag = mail_client._mail_settings_initialized
        mail_client._fernet_instance = None
        mail_client._mail_settings_initialized = False

    def tearDown(self):
        mail_client._fernet_instance = self.original_fernet
        mail_client._mail_settings_initialized = self.original_table_flag

    def test_save_user_settings_writes_postgres_shared_storage(self):
        fake_conn = FakeConnection()
        env = {
            'DATABASE_URL': 'postgresql://example',
            'MAIL_SETTINGS_ENCRYPTION_KEY': mail_client.Fernet.generate_key().decode(),
        }
        with patch.dict(os.environ, env, clear=False):
            with patch.object(mail_client, 'get_postgres_connection', return_value=fake_conn):
                mail_client.save_user_settings(
                    'user@example.com',
                    {'imap_server': 'imap.example.com', 'password': mail_client._encrypt('secret')},
                )

        executed_sql = ' '.join(query for query, _ in fake_conn.cursor_obj.executed)
        self.assertIn('INSERT INTO mail_user_settings', executed_sql)
        self.assertTrue(fake_conn.committed)

    def test_get_user_settings_reads_from_postgres_shared_storage(self):
        fake_conn = FakeConnection(one={'settings_json': {'imap_server': 'imap.example.com', 'password': 'token'}})
        with patch.dict(os.environ, {'DATABASE_URL': 'postgresql://example'}, clear=False):
            with patch.object(mail_client, 'get_postgres_connection', return_value=fake_conn):
                loaded = mail_client.get_user_settings('user@example.com')

        self.assertEqual(loaded['imap_server'], 'imap.example.com')

    def test_get_user_settings_migrates_legacy_file_settings_and_reencrypts(self):
        user_email = 'user@example.com'
        legacy_key = mail_client.Fernet.generate_key()
        legacy_fernet = mail_client.Fernet(legacy_key)
        legacy_password = legacy_fernet.encrypt(b'legacy-secret').decode()
        legacy_file = self.tmpdir / 'mail_settings.json'
        legacy_file.write_text(json.dumps({
            user_email: {
                'imap_server': 'legacy.example.com',
                'password': legacy_password,
            }
        }), encoding='utf-8')
        key_file = self.tmpdir / '.mail_key'
        key_file.write_bytes(legacy_key)

        fake_conn = FakeConnection()
        env = {
            'DATABASE_URL': 'postgresql://example',
            'MAIL_SETTINGS_ENCRYPTION_KEY': mail_client.Fernet.generate_key().decode(),
        }
        with patch.dict(os.environ, env, clear=False):
            with patch.object(mail_client, 'SETTINGS_FILE', legacy_file):
                with patch.object(mail_client, 'KEY_FILE', key_file):
                    with patch.object(mail_client, 'get_postgres_connection', return_value=fake_conn):
                        loaded = mail_client.get_user_settings(user_email)

        self.assertEqual(loaded['imap_server'], 'legacy.example.com')
        self.assertEqual(mail_client._decrypt(loaded['password']), 'legacy-secret')
        self.assertFalse(legacy_file.exists())
        executed_sql = ' '.join(query for query, _ in fake_conn.cursor_obj.executed)
        self.assertIn('INSERT INTO mail_user_settings', executed_sql)

    def test_mail_settings_fail_closed_in_production_when_postgres_is_unavailable(self):
        env = {
            'FLASK_ENV': 'production',
            'DATABASE_URL': 'postgresql://example',
            'MAIL_SETTINGS_ENCRYPTION_KEY': mail_client.Fernet.generate_key().decode(),
        }
        with patch.dict(os.environ, env, clear=False):
            with patch.object(mail_client, 'get_postgres_connection', side_effect=RuntimeError('db down')):
                with self.assertRaises(RuntimeError):
                    mail_client.get_user_settings('user@example.com')


class WsgiTests(unittest.TestCase):
    def _load_wsgi_module(self):
        module_name = 'wsgi_test_module'
        fake_app_module = types.ModuleType('app')
        fake_app_module.create_app = MagicMock(return_value=object())
        app_module_original = sys.modules.get('app')
        sys.modules['app'] = fake_app_module
        try:
            spec = importlib.util.spec_from_file_location(
                module_name,
                Path(__file__).resolve().parent / 'wsgi.py',
            )
            module = importlib.util.module_from_spec(spec)
            assert spec.loader is not None
            spec.loader.exec_module(module)
            return fake_app_module.create_app
        finally:
            if app_module_original is not None:
                sys.modules['app'] = app_module_original
            else:
                sys.modules.pop('app', None)

    def test_wsgi_builds_web_app_without_background_jobs(self):
        create_app_mock = self._load_wsgi_module()
        create_app_mock.assert_called_once_with()


class BackgroundWorkerTests(unittest.TestCase):
    def test_background_worker_starts_jobs_in_dedicated_process(self):
        module_name = 'background_worker_test_module'
        fake_app_module = types.ModuleType('app')
        fake_app_module.create_app = MagicMock(return_value=object())
        fake_app_module.start_background_jobs = MagicMock(return_value=True)
        app_module_original = sys.modules.get('app')
        sys.modules['app'] = fake_app_module
        try:
            spec = importlib.util.spec_from_file_location(
                module_name,
                Path(__file__).resolve().parent / 'background_worker.py',
            )
            module = importlib.util.module_from_spec(spec)
            assert spec.loader is not None
            spec.loader.exec_module(module)
            module._stop_requested = True
            with patch.object(module.signal, 'signal'):
                module.run_worker()
        finally:
            if app_module_original is not None:
                sys.modules['app'] = app_module_original
            else:
                sys.modules.pop('app', None)

        fake_app_module.create_app.assert_called_once_with()
        fake_app_module.start_background_jobs.assert_called_once_with()


class StartProductionScriptTests(unittest.TestCase):
    def test_production_startup_requires_mail_key_and_uses_background_worker(self):
        script = (Path(__file__).resolve().parent / 'start_production.sh').read_text(encoding='utf-8')
        self.assertIn('MAIL_SETTINGS_ENCRYPTION_KEY', script)
        self.assertIn('BACKGROUND_WORKER_ENABLED', script)
        self.assertNotIn('START_BACKGROUND_SERVICES', script)


if __name__ == '__main__':
    unittest.main()
