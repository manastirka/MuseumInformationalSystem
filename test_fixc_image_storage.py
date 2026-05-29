import os

os.environ.setdefault('FLASK_ENV', 'testing')
os.environ.setdefault('SECRET_KEY', 'test-secret')
os.environ.setdefault('REDIS_URL', '')
os.environ.setdefault('SESSION_TYPE', 'filesystem')
os.environ.setdefault('SESSION_FILE_DIR', '/tmp/museum-test-c-image-storage')

import threading
from pathlib import Path
from unittest import mock

import pytest
from PIL import Image

import image_storage_engine
from image_storage_engine import ImageStorageEngine, get_image_storage


def _make_engine(tmp_path, monkeypatch):
    """Build an engine with DB access disabled so we exercise filesystem paths."""
    monkeypatch.setattr(image_storage_engine, '_get_db_connection', lambda: None)
    monkeypatch.setenv('IMAGE_STORAGE_BACKEND', 'local')
    return ImageStorageEngine(str(tmp_path))


def _write_png(path: Path):
    img = Image.new('RGB', (32, 32), (10, 20, 30))
    img.save(path, 'PNG')


# Finding 1: get_image_path must not silently return the original for an
# unrecognized size.
def test_get_image_path_unknown_size_returns_none(tmp_path, monkeypatch):
    engine = _make_engine(tmp_path, monkeypatch)

    # Place an original on disk so the original would resolve if size fell
    # through to the original branch.
    original = engine.storage_backend.category_dir('originals') / 'img123.jpg'
    original.parent.mkdir(parents=True, exist_ok=True)
    _write_png(original)

    # Unknown size must yield None, not the full-size original.
    assert engine.get_image_path('img123', size='originals') is None
    assert engine.get_image_path('img123', size='thumb') is None

    # Sanity: the real original is still resolvable via the correct size.
    assert engine.get_image_path('img123', size='original') == original


# Finding 1 (DB branch): unknown size must short-circuit before any query.
def test_get_image_path_unknown_size_skips_db(tmp_path, monkeypatch):
    monkeypatch.setattr(image_storage_engine, '_get_db_connection', lambda: None)
    monkeypatch.setenv('IMAGE_STORAGE_BACKEND', 'local')
    engine = ImageStorageEngine(str(tmp_path))

    called = {'count': 0}

    def _tracking_conn():
        called['count'] += 1
        return None

    monkeypatch.setattr(image_storage_engine, '_get_db_connection', _tracking_conn)
    assert engine.get_image_path('whatever', size='bogus') is None
    assert called['count'] == 0


# Finding 4: store_image must hash the source file exactly once, including the
# INSERT path that previously re-hashed the file a second time.
def test_store_image_hashes_source_once(tmp_path, monkeypatch):
    # Build the engine with DB disabled so __init__ does not touch PostgreSQL.
    monkeypatch.setattr(image_storage_engine, '_get_db_connection', lambda: None)
    monkeypatch.setenv('IMAGE_STORAGE_BACKEND', 'local')
    engine = ImageStorageEngine(str(tmp_path))

    source = tmp_path / 'source.png'
    _write_png(source)

    # Provide a fake DB connection so the INSERT branch (the second hash site)
    # is exercised.
    fake_cursor = mock.MagicMock()
    fake_cursor.__enter__ = mock.MagicMock(return_value=fake_cursor)
    fake_cursor.__exit__ = mock.MagicMock(return_value=False)
    fake_conn = mock.MagicMock()
    fake_conn.cursor.return_value = fake_cursor
    monkeypatch.setattr(image_storage_engine, '_get_db_connection', lambda: fake_conn)

    real_calculate = ImageStorageEngine._calculate_hash
    calls = {'count': 0}

    def _counting_hash(self, file_path):
        if Path(file_path) == source:
            calls['count'] += 1
        return real_calculate(self, file_path)

    monkeypatch.setattr(ImageStorageEngine, '_calculate_hash', _counting_hash)

    image_id = engine.store_image(str(source), 'mineral', 'collection_item', '42')
    assert image_id is not None
    # The INSERT must have run (DB path exercised), and the source hashed once.
    assert fake_conn.commit.called
    assert calls['count'] == 1


# Finding 3: restore_from_backup must only regenerate thumbnails for images
# listed in the manifest, not for every pre-existing original on disk.
def test_restore_only_regenerates_manifest_images(tmp_path, monkeypatch):
    monkeypatch.setattr(image_storage_engine, '_get_db_connection', lambda: None)
    monkeypatch.setenv('IMAGE_STORAGE_BACKEND', 'local')
    engine = ImageStorageEngine(str(tmp_path))

    originals_dir = engine.storage_backend.category_dir('originals')
    originals_dir.mkdir(parents=True, exist_ok=True)

    # A pre-existing, unrelated original already on disk.
    unrelated = originals_dir / 'unrelated_img.jpg'
    _write_png(unrelated)

    # The image actually contained in the backup manifest.
    manifest_img = originals_dir / 'backup_img.jpg'
    _write_png(manifest_img)

    backup_dir = tmp_path / 'backup'
    backup_dir.mkdir(parents=True, exist_ok=True)
    (backup_dir / 'originals').mkdir(parents=True, exist_ok=True)
    manifest_path = engine._get_backup_manifest_path(backup_dir)
    import json
    manifest_path.write_text(json.dumps({
        'version': 1,
        'images': [
            {'image_id': 'backup_img', 'file_extension': '.jpg'},
        ],
    }), encoding='utf-8')

    regenerated = []

    def _track_thumbs(self, original_path, image_id):
        regenerated.append(image_id)
        return {}

    monkeypatch.setattr(ImageStorageEngine, '_generate_thumbnails', _track_thumbs)
    monkeypatch.setattr(ImageStorageEngine, '_restore_backup_metadata', lambda self, imgs: True)

    assert engine.restore_from_backup(str(backup_dir)) is True

    # Only the manifest image must be regenerated, never the unrelated one.
    assert regenerated == ['backup_img']
    assert 'unrelated_img' not in regenerated


# Finding 2: get_image_storage must be safe under concurrent first-access and
# return a single shared instance per cache key.
def test_get_image_storage_single_instance_under_threads(tmp_path, monkeypatch):
    monkeypatch.setattr(image_storage_engine, '_get_db_connection', lambda: None)
    monkeypatch.setenv('IMAGE_STORAGE_BACKEND', 'local')

    # Isolate the module-level cache for this test.
    monkeypatch.setattr(image_storage_engine, '_image_storage_instances', {})

    base = str(tmp_path / 'store')
    results = []
    barrier = threading.Barrier(8)

    def _worker():
        barrier.wait()
        results.append(get_image_storage(base))

    threads = [threading.Thread(target=_worker) for _ in range(8)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    assert len(results) == 8
    first = results[0]
    assert all(r is first for r in results)


def test_module_imports_cleanly():
    import importlib
    importlib.reload(image_storage_engine)


if __name__ == '__main__':
    raise SystemExit(pytest.main([__file__, '-q']))
