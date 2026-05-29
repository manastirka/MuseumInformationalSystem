import os

os.environ.setdefault('FLASK_ENV', 'testing')
os.environ.setdefault('SECRET_KEY', 'test-secret')
os.environ.setdefault('REDIS_URL', '')
os.environ.setdefault('SESSION_TYPE', 'filesystem')
os.environ.setdefault('SESSION_FILE_DIR', '/tmp/museum-test-b-image-storage')

import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from PIL import Image

import image_storage_engine


def _make_engine(base_path: Path):
    with patch.object(image_storage_engine.ImageStorageEngine, '_ensure_db_table', return_value=None):
        return image_storage_engine.ImageStorageEngine(str(base_path))


def _write_valid_png(path: Path, image_id: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    img = Image.new('RGB', (32, 32), (10, 20, 30))
    img.save(path / f"{image_id}.png", 'PNG')


class TestRestoreFromBackupResilience(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.tmp = Path(self._tmp.name)
        self.backup_dir = self.tmp / 'backup'
        (self.backup_dir / 'originals').mkdir(parents=True)
        # One valid image
        _write_valid_png(self.backup_dir / 'originals', 'good-1')
        # A stray, undecodable file
        (self.backup_dir / 'originals' / '.DS_Store').write_bytes(b'not an image')
        # Manifest references only the valid image
        manifest = {'images': [{'image_id': 'good-1', 'file_extension': '.png'}]}
        (self.backup_dir / 'metadata.json').write_text(json.dumps(manifest), encoding='utf-8')

    def tearDown(self):
        self._tmp.cleanup()

    def test_restore_continues_past_undecodable_file_and_persists_metadata(self):
        engine = _make_engine(self.tmp / 'store')

        generated = []
        original_generate = engine._generate_thumbnails

        def tracking_generate(original_path, image_id):
            # Use the real implementation so undecodable files raise as in production.
            result = original_generate(original_path, image_id)
            generated.append(image_id)
            return result

        with patch.object(engine, '_restore_backup_metadata', return_value=True) as mock_meta, \
                patch.object(engine, '_generate_thumbnails', side_effect=tracking_generate):
            result = engine.restore_from_backup(str(self.backup_dir))

        # Restore must succeed despite the stray undecodable .DS_Store file.
        self.assertTrue(result)
        # Metadata restore (DB rows) must run so valid files are not left orphaned.
        mock_meta.assert_called_once()
        # Thumbnails for the valid image must have been generated.
        self.assertIn('good-1', generated)

    def test_restore_continues_past_subdirectory_entry(self):
        # import_category (object backend) can create nested subdirs under originals.
        engine = _make_engine(self.tmp / 'store2')
        originals = engine.storage_backend.category_dir('originals')
        originals.mkdir(parents=True, exist_ok=True)
        _write_valid_png(originals, 'good-2')
        (originals / 'nested-subdir').mkdir()

        with patch.object(engine, '_restore_backup_metadata', return_value=True) as mock_meta, \
                patch.object(engine.storage_backend, 'import_category', return_value=None):
            manifest = {'images': [{'image_id': 'good-2', 'file_extension': '.png'}]}
            (self.backup_dir / 'metadata.json').write_text(json.dumps(manifest), encoding='utf-8')
            result = engine.restore_from_backup(str(self.backup_dir))

        self.assertTrue(result)
        mock_meta.assert_called_once()


if __name__ == '__main__':
    unittest.main()
