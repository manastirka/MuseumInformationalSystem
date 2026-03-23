#!/usr/bin/env python3
"""
Museum Image Storage Engine
Stores image files in ImagesDatabase/ folder with references in PostgreSQL.
When deployed on server, ImagesDatabase/ can be mounted on a storage drive.
"""

import os
import json
import shutil
import hashlib
import logging
import tempfile
from datetime import datetime, timezone
from typing import Optional, List, Dict, Tuple
from pathlib import Path
from PIL import Image
import requests

logger = logging.getLogger(__name__)

# Default path - can be overridden via IMAGE_STORAGE_PATH env variable
# On server, set IMAGE_STORAGE_PATH to storage drive mount point
DEFAULT_STORAGE_PATH = os.environ.get('IMAGE_STORAGE_PATH', './ImagesDatabase')
BACKUP_METADATA_FILENAME = 'metadata.json'
DEFAULT_IMAGE_STORAGE_BACKEND = os.environ.get('IMAGE_STORAGE_BACKEND', 'local').strip().lower() or 'local'


def get_image_storage_backend_name() -> str:
    """Read backend choice at runtime so tests and deployments can override it safely."""
    return os.environ.get('IMAGE_STORAGE_BACKEND', DEFAULT_IMAGE_STORAGE_BACKEND).strip().lower() or 'local'


def _get_db_connection():
    """Get PostgreSQL connection for image metadata."""
    database_url = os.environ.get('DATABASE_URL')
    if not database_url:
        return None
    try:
        import psycopg
        from psycopg.rows import dict_row
        # Convert SQLAlchemy-style URL to psycopg format
        db_url = database_url.replace('postgresql+psycopg://', 'postgresql://')
        conn = psycopg.connect(db_url, row_factory=dict_row)
        return conn
    except Exception as e:
        logger.error(f"Failed to connect to PostgreSQL: {e}")
        return None


class ImageStorageBackend:
    """Storage backend abstraction for image binaries."""

    name = 'base'

    def initialize(self):
        raise NotImplementedError

    def build_ref(self, category: str, filename: str) -> str:
        raise NotImplementedError

    def save_file(self, source_path: Path, category: str, filename: str) -> str:
        raise NotImplementedError

    def resolve_ref(self, ref: str) -> Optional[Path]:
        raise NotImplementedError

    def delete_ref(self, ref: str) -> None:
        raise NotImplementedError

    def is_managed_ref(self, ref: str) -> bool:
        raise NotImplementedError

    def category_dir(self, category: str) -> Path:
        raise NotImplementedError

    def export_category(self, category: str, destination: Path) -> None:
        raise NotImplementedError

    def import_category(self, source: Path, category: str) -> None:
        raise NotImplementedError

    def describe(self) -> str:
        raise NotImplementedError


class LocalFilesystemImageBackend(ImageStorageBackend):
    """Current local-filesystem storage backend, behind an abstraction boundary."""

    name = 'local'
    SCHEME = 'local://'

    def __init__(self, base_path: Path):
        self.base_path = Path(base_path)

    def initialize(self):
        directories = [
            self.base_path,
            self.category_dir('originals'),
            self.category_dir('thumbnails/small'),
            self.category_dir('thumbnails/medium'),
            self.category_dir('thumbnails/large'),
            self.category_dir('temp'),
            self.category_dir('backups'),
        ]
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)

    def build_ref(self, category: str, filename: str) -> str:
        return f"{self.SCHEME}{category.strip('/')}/{filename}"

    def _relative_path_from_ref(self, ref: str) -> Optional[Path]:
        if not ref.startswith(self.SCHEME):
            return None
        relative = ref[len(self.SCHEME):].lstrip('/')
        if not relative:
            return None
        return Path(relative)

    def resolve_ref(self, ref: str) -> Optional[Path]:
        relative = self._relative_path_from_ref(ref)
        if relative is not None:
            return self.base_path / relative

        # Backward compatibility with legacy absolute filesystem paths.
        try:
            return Path(ref)
        except TypeError:
            return None

    def save_file(self, source_path: Path, category: str, filename: str) -> str:
        destination = self.category_dir(category) / filename
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source_path, destination)
        return self.build_ref(category, filename)

    def delete_ref(self, ref: str) -> None:
        resolved = self.resolve_ref(ref)
        if resolved and resolved.exists():
            resolved.unlink()

    def is_managed_ref(self, ref: str) -> bool:
        relative = self._relative_path_from_ref(ref)
        if relative is not None:
            return True

        resolved = self.resolve_ref(ref)
        if resolved is None:
            return False
        try:
            return resolved.resolve().is_relative_to(self.base_path.resolve())
        except OSError:
            return False

    def category_dir(self, category: str) -> Path:
        return self.base_path / Path(category)

    def export_category(self, category: str, destination: Path) -> None:
        shutil.copytree(
            self.category_dir(category),
            destination,
            dirs_exist_ok=True,
        )

    def import_category(self, source: Path, category: str) -> None:
        shutil.copytree(
            source,
            self.category_dir(category),
            dirs_exist_ok=True,
        )

    def describe(self) -> str:
        return str(self.base_path)


class ObjectStorageImageBackend(ImageStorageBackend):
    """S3-compatible object storage backend with local cache and export/import support."""

    name = 'object'
    SCHEME = 'object://'

    def __init__(self, base_path: Path):
        self.base_path = Path(base_path)
        self.bucket = (os.environ.get('AWS_S3_BUCKET') or '').strip()
        if not self.bucket:
            raise RuntimeError("AWS_S3_BUCKET is required for object image storage")

        self.region = os.environ.get('AWS_REGION', 'eu-central-1').strip() or 'eu-central-1'
        self.endpoint_url = (os.environ.get('AWS_S3_ENDPOINT_URL') or '').strip() or None
        self.prefix = os.environ.get('IMAGE_STORAGE_OBJECT_PREFIX', 'museum-images').strip().strip('/')
        self.cache_path = Path(
            os.environ.get('IMAGE_STORAGE_CACHE_PATH', str(self.base_path / 'cache'))
        )
        self.backup_path = Path(
            os.environ.get('IMAGE_STORAGE_BACKUP_PATH', str(self.base_path / 'backups'))
        )

        try:
            import boto3
        except ImportError as exc:
            raise RuntimeError(
                "boto3 is required for IMAGE_STORAGE_BACKEND=object"
            ) from exc

        client_kwargs = {'region_name': self.region}
        if self.endpoint_url:
            client_kwargs['endpoint_url'] = self.endpoint_url
        self.client = boto3.client('s3', **client_kwargs)

    def initialize(self):
        for directory in (
            self.cache_path,
            self.category_dir('originals'),
            self.category_dir('thumbnails/small'),
            self.category_dir('thumbnails/medium'),
            self.category_dir('thumbnails/large'),
            self.category_dir('temp'),
            self.backup_path,
        ):
            directory.mkdir(parents=True, exist_ok=True)

    def _normalize_category(self, category: str) -> str:
        return category.strip('/').replace('\\', '/')

    def _object_key(self, category: str, filename: str) -> str:
        key_parts = [part for part in (self.prefix, self._normalize_category(category), filename.strip('/')) if part]
        return '/'.join(key_parts)

    def build_ref(self, category: str, filename: str) -> str:
        return f"{self.SCHEME}{self._normalize_category(category)}/{filename.strip('/')}"

    def _relative_path_from_ref(self, ref: str) -> Optional[Path]:
        if not ref.startswith(self.SCHEME):
            return None
        relative = ref[len(self.SCHEME):].lstrip('/')
        if not relative:
            return None
        return Path(relative)

    def _iter_category_keys(self, category: str):
        prefix = self._object_key(category, '')
        continuation_token = None
        while True:
            kwargs = {'Bucket': self.bucket, 'Prefix': prefix}
            if continuation_token:
                kwargs['ContinuationToken'] = continuation_token
            response = self.client.list_objects_v2(**kwargs)
            for item in response.get('Contents', []):
                key = item.get('Key')
                if key and not key.endswith('/'):
                    yield key
            if not response.get('IsTruncated'):
                break
            continuation_token = response.get('NextContinuationToken')

    def resolve_ref(self, ref: str) -> Optional[Path]:
        relative = self._relative_path_from_ref(ref)
        if relative is not None:
            cache_target = self.cache_path / relative
            if cache_target.exists():
                return cache_target

            cache_target.parent.mkdir(parents=True, exist_ok=True)
            category = relative.parent.as_posix()
            filename = relative.name
            object_key = self._object_key(category, filename)
            try:
                self.client.download_file(self.bucket, object_key, str(cache_target))
            except Exception as exc:
                logger.error("Failed to download image object %s: %s", object_key, exc)
                return None
            return cache_target

        try:
            return Path(ref)
        except TypeError:
            return None

    def save_file(self, source_path: Path, category: str, filename: str) -> str:
        object_key = self._object_key(category, filename)
        self.client.upload_file(str(source_path), self.bucket, object_key)

        cache_target = self.cache_path / self._normalize_category(category) / filename
        cache_target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source_path, cache_target)
        return self.build_ref(category, filename)

    def delete_ref(self, ref: str) -> None:
        relative = self._relative_path_from_ref(ref)
        if relative is None:
            resolved = self.resolve_ref(ref)
            if resolved and resolved.exists():
                resolved.unlink()
            return

        category = relative.parent.as_posix()
        filename = relative.name
        object_key = self._object_key(category, filename)
        self.client.delete_object(Bucket=self.bucket, Key=object_key)

        cache_target = self.cache_path / relative
        if cache_target.exists():
            cache_target.unlink()

    def is_managed_ref(self, ref: str) -> bool:
        return self._relative_path_from_ref(ref) is not None

    def category_dir(self, category: str) -> Path:
        normalized = self._normalize_category(category)
        if normalized == 'backups':
            return self.backup_path
        return self.cache_path / normalized

    def export_category(self, category: str, destination: Path) -> None:
        destination.mkdir(parents=True, exist_ok=True)
        category_prefix = self._normalize_category(category).rstrip('/')
        for key in self._iter_category_keys(category):
            object_path = Path(key)
            relative_parts = object_path.parts[len(tuple(filter(None, self.prefix.split('/')))):]
            if not relative_parts:
                continue
            relative = Path(*relative_parts)
            if relative.parts[0] != category_prefix:
                continue
            relative_suffix = Path(*relative.parts[1:]) if len(relative.parts) > 1 else Path(relative.name)
            destination_path = destination / relative_suffix
            destination_path.parent.mkdir(parents=True, exist_ok=True)
            self.client.download_file(self.bucket, key, str(destination_path))

    def import_category(self, source: Path, category: str) -> None:
        source = Path(source)
        if not source.exists():
            return
        for image_file in source.rglob('*'):
            if not image_file.is_file():
                continue
            relative = image_file.relative_to(source).as_posix()
            self.save_file(image_file, category, relative)

    def describe(self) -> str:
        base = f"s3://{self.bucket}"
        if self.prefix:
            return f"{base}/{self.prefix}"
        return base


def _build_storage_backend(base_storage_path: str) -> ImageStorageBackend:
    """Construct the configured image binary storage backend."""
    backend_name = get_image_storage_backend_name()
    base_path = Path(base_storage_path or DEFAULT_STORAGE_PATH)
    if backend_name == 'local':
        return LocalFilesystemImageBackend(base_path)
    if backend_name in {'object', 's3', 'minio'}:
        return ObjectStorageImageBackend(base_path)
    raise RuntimeError(f"Unsupported IMAGE_STORAGE_BACKEND: {backend_name}")


class ImageStorageEngine:
    """
    Universal image storage engine for all museum databases.
    Files stored in ImagesDatabase/ folder, references in PostgreSQL.
    """

    ALLOWED_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.tiff'}
    MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
    THUMBNAIL_SIZES = {
        'small': (150, 150),
        'medium': (300, 300),
        'large': (600, 600)
    }

    def __init__(self, base_storage_path: str = None, server_backup_url: str = None):
        self.base_path = Path(base_storage_path or DEFAULT_STORAGE_PATH)
        self.server_backup_url = server_backup_url
        self.storage_backend = _build_storage_backend(self.base_path)
        self.storage_backend.initialize()
        self._ensure_db_table()
        logger.info(
            "Image storage engine initialized at: %s (backend=%s)",
            self.storage_backend.describe(),
            self.storage_backend.name,
        )

    def _ensure_db_table(self):
        """Ensure images table exists in PostgreSQL."""
        conn = _get_db_connection()
        if not conn:
            logger.warning("No PostgreSQL connection - image metadata will not be persisted")
            return
        try:
            with conn.cursor() as cur:
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS images (
                        id SERIAL PRIMARY KEY,
                        image_id VARCHAR(255) UNIQUE NOT NULL,
                        database_name VARCHAR(100) NOT NULL,
                        entity_type VARCHAR(100) NOT NULL,
                        entity_id VARCHAR(255) NOT NULL,
                        original_filename VARCHAR(500),
                        file_extension VARCHAR(10) NOT NULL,
                        file_path VARCHAR(1000) NOT NULL,
                        thumbnail_small VARCHAR(1000),
                        thumbnail_medium VARCHAR(1000),
                        thumbnail_large VARCHAR(1000),
                        description TEXT DEFAULT '',
                        file_size BIGINT DEFAULT 0,
                        file_hash VARCHAR(64),
                        width INTEGER,
                        height INTEGER,
                        custom_metadata JSONB DEFAULT '{}',
                        backed_up BOOLEAN DEFAULT FALSE,
                        backup_date TIMESTAMPTZ,
                        created_at TIMESTAMPTZ DEFAULT NOW(),
                        updated_at TIMESTAMPTZ DEFAULT NOW()
                    )
                """)
                cur.execute("CREATE INDEX IF NOT EXISTS idx_images_database_entity ON images(database_name, entity_type, entity_id)")
                cur.execute("CREATE INDEX IF NOT EXISTS idx_images_database_name ON images(database_name)")
                cur.execute("CREATE INDEX IF NOT EXISTS idx_images_entity_id ON images(entity_id)")
            conn.commit()
        except Exception as e:
            logger.error(f"Error ensuring images table: {e}")
            conn.rollback()
        finally:
            conn.close()

    def _calculate_hash(self, file_path: Path) -> str:
        """Calculate SHA256 hash of file."""
        sha256_hash = hashlib.sha256()
        with open(file_path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()

    def _validate_image(self, file_path: Path) -> Tuple[bool, str]:
        """Validate image file."""
        if not file_path.exists():
            return False, "File does not exist"
        if file_path.stat().st_size > self.MAX_FILE_SIZE:
            return False, f"File size exceeds {self.MAX_FILE_SIZE / 1024 / 1024}MB limit"
        if file_path.suffix.lower() not in self.ALLOWED_EXTENSIONS:
            return False, f"Invalid file type. Allowed: {', '.join(self.ALLOWED_EXTENSIONS)}"
        try:
            with Image.open(file_path) as img:
                img.verify()
            return True, ""
        except Exception as e:
            return False, f"Invalid image file: {str(e)}"

    def _get_image_dimensions(self, file_path: Path) -> Tuple[int, int]:
        """Get image width and height."""
        try:
            with Image.open(file_path) as img:
                return img.size
        except Exception:
            return (0, 0)

    def _generate_thumbnails(self, original_path: Path, image_id: str) -> Dict[str, str]:
        """Generate thumbnails in multiple sizes. Returns dict of size->path."""
        thumb_paths = {}
        try:
            with Image.open(original_path) as img:
                if img.mode in ('RGBA', 'LA', 'P'):
                    background = Image.new('RGB', img.size, (255, 255, 255))
                    if img.mode == 'P':
                        img = img.convert('RGBA')
                    background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
                    img = background

                for size_name, dimensions in self.THUMBNAIL_SIZES.items():
                    thumbnail = img.copy()
                    thumbnail.thumbnail(dimensions, Image.Resampling.LANCZOS)
                    with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as temp_file:
                        temp_path = Path(temp_file.name)
                    try:
                        thumbnail.save(temp_path, 'JPEG', quality=85, optimize=True)
                        thumb_paths[size_name] = self.storage_backend.save_file(
                            temp_path,
                            f'thumbnails/{size_name}',
                            f"{image_id}.jpg",
                        )
                    finally:
                        temp_path.unlink(missing_ok=True)

            logger.info(f"Generated thumbnails for image: {image_id}")
        except Exception as e:
            logger.error(f"Error generating thumbnails: {e}")
            raise
        return thumb_paths

    def _cleanup_stored_files(self, original_ref: str, thumb_paths: Dict[str, str]):
        """Remove stored objects/files when DB persistence fails."""
        for label, storage_ref in [('original', original_ref)] + list(thumb_paths.items()):
            try:
                self.storage_backend.delete_ref(storage_ref)
            except Exception as exc:
                logger.warning("Could not clean up %s (%s): %s", label, storage_ref, exc)

    def _serialize_image_row(self, row: Dict) -> Dict:
        """Convert DB row objects into JSON-safe backup metadata."""
        result = dict(row)
        for key in ('created_at', 'updated_at', 'backup_date'):
            if result.get(key):
                result[key] = result[key].isoformat()
        return result

    def _get_backup_manifest_path(self, backup_dir: Path) -> Path:
        """Return the metadata manifest path for a backup directory."""
        return backup_dir / BACKUP_METADATA_FILENAME

    def _export_backup_metadata(self) -> Optional[List[Dict]]:
        """Export metadata rows for images stored under this engine's base path."""
        conn = _get_db_connection()
        if not conn:
            logger.error("Cannot create restorable image backup without PostgreSQL metadata access")
            return None

        try:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM images ORDER BY created_at")
                rows = cur.fetchall()

            metadata_rows = []
            for row in rows:
                serialized = self._serialize_image_row(row)
                file_path = serialized.get('file_path')
                if not file_path:
                    continue

                if self.storage_backend.is_managed_ref(file_path):
                    metadata_rows.append(serialized)

            return metadata_rows
        except Exception as exc:
            logger.error("Failed to export image metadata for backup: %s", exc)
            return None
        finally:
            conn.close()

    def _restore_backup_metadata(self, manifest_images: List[Dict]) -> bool:
        """Restore PostgreSQL metadata rows for files present in the restored backup."""
        conn = _get_db_connection()
        if not conn:
            logger.error("Cannot restore image backup metadata without PostgreSQL access")
            return False

        try:
            with conn.cursor() as cur:
                for image in manifest_images:
                    image_id = image['image_id']
                    file_extension = image.get('file_extension') or Path(image.get('file_path', '')).suffix or '.jpg'
                    original_path = self.storage_backend.category_dir('originals') / f"{image_id}{file_extension}"
                    if not original_path.exists():
                        logger.error("Restored original file missing for image %s", image_id)
                        conn.rollback()
                        return False

                    width = image.get('width')
                    height = image.get('height')
                    if not width or not height:
                        width, height = self._get_image_dimensions(original_path)

                    custom_metadata = image.get('custom_metadata') or {}
                    if isinstance(custom_metadata, str):
                        try:
                            custom_metadata = json.loads(custom_metadata)
                        except json.JSONDecodeError:
                            custom_metadata = {}

                    cur.execute("""
                        INSERT INTO images (
                            image_id, database_name, entity_type, entity_id,
                            original_filename, file_extension, file_path,
                            thumbnail_small, thumbnail_medium, thumbnail_large,
                            description, file_size, file_hash, width, height,
                            custom_metadata, backed_up, backup_date, created_at, updated_at
                        ) VALUES (
                            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
                        )
                        ON CONFLICT (image_id) DO UPDATE SET
                            database_name = EXCLUDED.database_name,
                            entity_type = EXCLUDED.entity_type,
                            entity_id = EXCLUDED.entity_id,
                            original_filename = EXCLUDED.original_filename,
                            file_extension = EXCLUDED.file_extension,
                            file_path = EXCLUDED.file_path,
                            thumbnail_small = EXCLUDED.thumbnail_small,
                            thumbnail_medium = EXCLUDED.thumbnail_medium,
                            thumbnail_large = EXCLUDED.thumbnail_large,
                            description = EXCLUDED.description,
                            file_size = EXCLUDED.file_size,
                            file_hash = EXCLUDED.file_hash,
                            width = EXCLUDED.width,
                            height = EXCLUDED.height,
                            custom_metadata = EXCLUDED.custom_metadata,
                            backed_up = EXCLUDED.backed_up,
                            backup_date = EXCLUDED.backup_date,
                            created_at = EXCLUDED.created_at,
                            updated_at = EXCLUDED.updated_at
                    """, (
                        image_id,
                        image.get('database_name', image.get('database', 'unknown')),
                        image.get('entity_type', 'unknown'),
                        str(image.get('entity_id', '')),
                        image.get('original_filename', ''),
                        file_extension,
                        self.storage_backend.build_ref('originals', f"{image_id}{file_extension}"),
                        self.storage_backend.build_ref('thumbnails/small', f"{image_id}.jpg"),
                        self.storage_backend.build_ref('thumbnails/medium', f"{image_id}.jpg"),
                        self.storage_backend.build_ref('thumbnails/large', f"{image_id}.jpg"),
                        image.get('description', ''),
                        original_path.stat().st_size,
                        image.get('file_hash', ''),
                        width,
                        height,
                        json.dumps(custom_metadata),
                        bool(image.get('backed_up', False)),
                        image.get('backup_date'),
                        image.get('created_at'),
                        image.get('updated_at'),
                    ))

            conn.commit()
            return True
        except Exception as exc:
            logger.error("Failed to restore image metadata from backup: %s", exc)
            conn.rollback()
            return False
        finally:
            conn.close()

    def store_image(
        self,
        file_path: str,
        database: str,
        entity_type: str,
        entity_id: str,
        description: str = "",
        metadata: Dict = None
    ) -> Optional[str]:
        """
        Store an image file in ImagesDatabase/ and record reference in PostgreSQL.

        Args:
            file_path: Path to source image file
            database: Database name (e.g., 'mineral', 'library', 'employees')
            entity_type: Entity type (e.g., 'collection_item', 'book', 'employee')
            entity_id: ID of the entity this image belongs to
            description: Optional description
            metadata: Additional metadata dictionary

        Returns:
            image_id on success, None on failure
        """
        try:
            source_path = Path(file_path)

            is_valid, error_msg = self._validate_image(source_path)
            if not is_valid:
                logger.error(f"Image validation failed: {error_msg}")
                return None

            # Generate unique image ID
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            file_hash = self._calculate_hash(source_path)[:8]
            image_id = f"{database}_{entity_type}_{entity_id}_{timestamp}_{file_hash}"

            # Copy to ImagesDatabase/originals/
            original_filename = f"{image_id}{source_path.suffix}"
            original_ref = self.storage_backend.save_file(source_path, 'originals', original_filename)
            original_path = self.storage_backend.resolve_ref(original_ref)

            # Get image dimensions
            width, height = self._get_image_dimensions(original_path)

            # Generate thumbnails
            thumb_paths = self._generate_thumbnails(original_path, image_id)

            file_size = original_path.stat().st_size

            # Store reference in PostgreSQL
            conn = _get_db_connection()
            if conn:
                try:
                    with conn.cursor() as cur:
                        cur.execute("""
                            INSERT INTO images (
                                image_id, database_name, entity_type, entity_id,
                                original_filename, file_extension, file_path,
                                thumbnail_small, thumbnail_medium, thumbnail_large,
                                description, file_size, file_hash,
                                width, height, custom_metadata
                            ) VALUES (
                                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                                %s, %s, %s, %s, %s, %s
                            )
                        """, (
                            image_id, database, entity_type, str(entity_id),
                            source_path.name, source_path.suffix,
                            original_ref,
                            thumb_paths.get('small', ''),
                            thumb_paths.get('medium', ''),
                            thumb_paths.get('large', ''),
                            description, file_size, self._calculate_hash(source_path),
                            width, height,
                            json.dumps(metadata or {})
                        ))
                    conn.commit()
                except Exception as e:
                    logger.error(f"Error saving image reference to PostgreSQL: {e}")
                    conn.rollback()
                    # Clean up orphaned files on DB failure
                    self._cleanup_stored_files(original_ref, thumb_paths)
                    return None
                finally:
                    conn.close()
            else:
                logger.warning(f"No PostgreSQL connection - image {image_id} stored on disk only")

            logger.info(f"Image stored: {image_id} -> {original_ref}")
            return image_id

        except Exception as e:
            logger.error(f"Error storing image: {e}")
            return None

    def get_image_path(self, image_id: str, size: str = 'original') -> Optional[Path]:
        """
        Get path to image file.

        Args:
            image_id: Image identifier
            size: 'original', 'small', 'medium', or 'large'

        Returns:
            Path to image file or None if not found
        """
        # First try PostgreSQL
        conn = _get_db_connection()
        if conn:
            try:
                with conn.cursor() as cur:
                    if size == 'original':
                        cur.execute("SELECT file_path FROM images WHERE image_id = %s", (image_id,))
                    elif size == 'small':
                        cur.execute("SELECT thumbnail_small AS file_path FROM images WHERE image_id = %s", (image_id,))
                    elif size == 'medium':
                        cur.execute("SELECT thumbnail_medium AS file_path FROM images WHERE image_id = %s", (image_id,))
                    elif size == 'large':
                        cur.execute("SELECT thumbnail_large AS file_path FROM images WHERE image_id = %s", (image_id,))
                    else:
                        cur.execute("SELECT file_path FROM images WHERE image_id = %s", (image_id,))

                    row = cur.fetchone()
                    if row and row['file_path']:
                        path = self.storage_backend.resolve_ref(row['file_path'])
                        if path and path.exists():
                            return path
            except Exception as e:
                logger.error(f"Error querying image path: {e}")
            finally:
                conn.close()

        # Fallback: scan filesystem
        if size == 'original':
            for ext in self.ALLOWED_EXTENSIONS:
                path = self.storage_backend.resolve_ref(
                    self.storage_backend.build_ref('originals', f"{image_id}{ext}")
                )
                if path and path.exists():
                    return path
        else:
            path = self.storage_backend.resolve_ref(
                self.storage_backend.build_ref(f'thumbnails/{size}', f"{image_id}.jpg")
            )
            if path and path.exists():
                return path

        logger.warning(f"Image file not found: {image_id} (size={size})")
        return None

    def get_image_metadata(self, image_id: str) -> Optional[Dict]:
        """Get metadata for an image from PostgreSQL."""
        conn = _get_db_connection()
        if not conn:
            return None
        try:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM images WHERE image_id = %s", (image_id,))
                row = cur.fetchone()
                if row:
                    result = dict(row)
                    # Convert datetime objects to ISO strings
                    for key in ('created_at', 'updated_at', 'backup_date'):
                        if result.get(key):
                            result[key] = result[key].isoformat()
                    return result
        except Exception as e:
            logger.error(f"Error getting image metadata: {e}")
        finally:
            conn.close()
        return None

    def get_images_for_entity(self, database: str, entity_type: str, entity_id: str) -> List[Dict]:
        """Get all images for a specific entity from PostgreSQL."""
        conn = _get_db_connection()
        if not conn:
            return []
        try:
            with conn.cursor() as cur:
                entity_id = str(entity_id)

                # Mineral images exist under both legacy and current identifiers.
                if database in ('mineral', 'minerals') and entity_type in ('mineral', 'collection_item'):
                    cur.execute("""
                        SELECT * FROM images
                        WHERE entity_id = %s
                          AND (
                                (database_name = 'minerals' AND entity_type = 'mineral')
                             OR (database_name = 'mineral' AND entity_type = 'collection_item')
                             OR (database_name = 'mineral' AND entity_type = 'mineral')
                             OR (database_name = 'minerals' AND entity_type = 'collection_item')
                          )
                        ORDER BY created_at
                    """, (entity_id,))
                else:
                    cur.execute("""
                        SELECT * FROM images
                        WHERE database_name = %s AND entity_type = %s AND entity_id = %s
                        ORDER BY created_at
                    """, (database, entity_type, entity_id))
                rows = cur.fetchall()
                results = []
                for row in rows:
                    result = dict(row)
                    for key in ('created_at', 'updated_at', 'backup_date'):
                        if result.get(key):
                            result[key] = result[key].isoformat()
                    results.append(result)
                return results
        except Exception as e:
            logger.error(f"Error getting entity images: {e}")
        finally:
            conn.close()
        return []

    def delete_image(self, image_id: str) -> bool:
        """Delete an image file and its PostgreSQL reference."""
        try:
            conn = _get_db_connection()
            if not conn:
                logger.error(f"Cannot delete image {image_id}: no PostgreSQL connection")
                return False

            file_paths = []
            try:
                with conn.cursor() as cur:
                    cur.execute("""
                        SELECT file_extension, file_path, thumbnail_small, thumbnail_medium, thumbnail_large
                        FROM images
                        WHERE image_id = %s
                    """, (image_id,))
                    row = cur.fetchone()
                    if not row:
                        logger.error(f"Cannot delete image {image_id}: metadata record not found")
                        return False

                    file_paths = [
                        row.get('file_path'),
                        row.get('thumbnail_small'),
                        row.get('thumbnail_medium'),
                        row.get('thumbnail_large')
                    ]

                    cur.execute("DELETE FROM images WHERE image_id = %s", (image_id,))
                    if cur.rowcount != 1:
                        conn.rollback()
                        logger.error(f"Delete affected {cur.rowcount} rows for image {image_id}")
                        return False

                conn.commit()
            except Exception as e:
                logger.error(f"Error deleting image from PostgreSQL: {e}")
                conn.rollback()
                return False
            finally:
                conn.close()

            for path_value in file_paths:
                if not path_value:
                    continue
                self.storage_backend.delete_ref(path_value)

            # Legacy fallback for thumbnails if stored paths were incomplete.
            for size in self.THUMBNAIL_SIZES.keys():
                thumb_path = self.storage_backend.category_dir(f'thumbnails/{size}') / f"{image_id}.jpg"
                if thumb_path.exists():
                    thumb_path.unlink()

            logger.info(f"Image deleted: {image_id}")
            return True

        except Exception as e:
            logger.error(f"Error deleting image: {e}")
            return False

    def get_images_by_database(self, database: str) -> List[Dict]:
        """Get all images for a database."""
        conn = _get_db_connection()
        if not conn:
            return []
        try:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT * FROM images WHERE database_name = %s ORDER BY created_at
                """, (database,))
                rows = cur.fetchall()
                results = []
                for row in rows:
                    result = dict(row)
                    for key in ('created_at', 'updated_at', 'backup_date'):
                        if result.get(key):
                            result[key] = result[key].isoformat()
                    results.append(result)
                return results
        except Exception as e:
            logger.error(f"Error getting database images: {e}")
        finally:
            conn.close()
        return []

    def backup_to_server(self, image_id: str = None) -> bool:
        """Backup images to server."""
        if not self.server_backup_url:
            logger.warning("No server backup URL configured")
            return False

        try:
            conn = _get_db_connection()
            if not conn:
                return False

            try:
                with conn.cursor() as cur:
                    if image_id:
                        cur.execute("SELECT * FROM images WHERE image_id = %s AND backed_up = FALSE", (image_id,))
                    else:
                        cur.execute("SELECT * FROM images WHERE backed_up = FALSE")
                    rows = cur.fetchall()
            finally:
                conn.close()

            failed = 0
            for row in rows:
                img_id = row['image_id']
                original_path = self.get_image_path(img_id, 'original')
                if not original_path:
                    failed += 1
                    continue

                with open(original_path, 'rb') as fh:
                    files = {'file': fh}
                    data = {
                        'image_id': img_id,
                        'metadata': json.dumps(dict(row), default=str)
                    }
                    headers = {}
                    backup_token = os.environ.get('IMAGE_BACKUP_TOKEN')
                    if backup_token:
                        headers['X-Backup-Token'] = backup_token

                    response = requests.post(
                        f"{self.server_backup_url}/api/images/backup/receive",
                        files=files,
                        data=data,
                        headers=headers,
                        timeout=30
                    )

                if response.status_code in (200, 201):
                    conn2 = _get_db_connection()
                    if conn2:
                        try:
                            with conn2.cursor() as cur:
                                cur.execute("""
                                    UPDATE images SET backed_up = TRUE, backup_date = NOW()
                                    WHERE image_id = %s
                                """, (img_id,))
                            conn2.commit()
                        finally:
                            conn2.close()
                    logger.info(f"Backed up image to server: {img_id}")
                else:
                    logger.error(f"Server backup failed for {img_id}: {response.status_code}")
                    failed += 1

            if failed:
                logger.warning("Server backup completed with %d failures out of %d images", failed, len(rows))
            return failed == 0

        except Exception as e:
            logger.error(f"Error backing up to server: {e}")
            return False

    def create_local_backup(self, backup_name: str = None) -> Optional[Path]:
        """Create a complete local backup of all images."""
        try:
            if not backup_name:
                backup_name = datetime.now().strftime('%Y%m%d_%H%M%S')

            backup_dir = self.storage_backend.category_dir('backups') / backup_name
            backup_dir.mkdir(parents=True, exist_ok=True)

            originals_backup = backup_dir / 'originals'
            self.storage_backend.export_category('originals', originals_backup)

            metadata_rows = self._export_backup_metadata()
            if metadata_rows is None:
                shutil.rmtree(backup_dir, ignore_errors=True)
                raise RuntimeError("Image metadata export failed; backup was not created")

            manifest = {
                'version': 1,
                'created_at': datetime.now(timezone.utc).isoformat(),
                'storage_path': str(self.base_path),
                'image_count': len(metadata_rows),
                'images': metadata_rows,
            }
            self._get_backup_manifest_path(backup_dir).write_text(
                json.dumps(manifest, indent=2),
                encoding='utf-8',
            )

            logger.info(f"Local backup created: {backup_dir}")
            return backup_dir

        except Exception as e:
            logger.error(f"Error creating local backup: {e}")
            return None

    def restore_from_backup(self, backup_path: str) -> bool:
        """Restore images from a backup directory."""
        try:
            backup_dir = Path(backup_path)
            if not backup_dir.exists():
                logger.error(f"Backup directory not found: {backup_path}")
                return False

            manifest_path = self._get_backup_manifest_path(backup_dir)
            if not manifest_path.exists():
                logger.error("Backup manifest not found: %s", manifest_path)
                return False

            manifest = json.loads(manifest_path.read_text(encoding='utf-8'))
            manifest_images = manifest.get('images', [])

            originals_backup = backup_dir / 'originals'
            if originals_backup.exists():
                self.storage_backend.import_category(originals_backup, 'originals')

            # Regenerate thumbnails for restored images
            for image_file in self.storage_backend.category_dir('originals').glob('*'):
                image_id = image_file.stem
                self._generate_thumbnails(image_file, image_id)

            if not self._restore_backup_metadata(manifest_images):
                return False

            logger.info(f"Restored from backup: {backup_path}")
            return True

        except Exception as e:
            logger.error(f"Error restoring from backup: {e}")
            return False

    def get_storage_stats(self) -> Dict:
        """Get storage statistics from PostgreSQL."""
        stats = {
            'total_images': 0,
            'total_size_mb': 0,
            'backed_up_count': 0,
            'storage_path': self.storage_backend.describe(),
            'databases': []
        }

        conn = _get_db_connection()
        if not conn:
            return stats

        try:
            with conn.cursor() as cur:
                cur.execute("SELECT COUNT(*) as cnt FROM images")
                stats['total_images'] = cur.fetchone()['cnt']

                cur.execute("SELECT COALESCE(SUM(file_size), 0) as total FROM images")
                stats['total_size_mb'] = round(float(cur.fetchone()['total']) / 1024 / 1024, 2)

                cur.execute("SELECT COUNT(*) as cnt FROM images WHERE backed_up = TRUE")
                stats['backed_up_count'] = cur.fetchone()['cnt']

                cur.execute("SELECT DISTINCT database_name FROM images")
                stats['databases'] = [row['database_name'] for row in cur.fetchall()]
        except Exception as e:
            logger.error(f"Error getting storage stats: {e}")
        finally:
            conn.close()

        return stats

    # Legacy compatibility property
    @property
    def metadata(self) -> Dict:
        """Legacy compatibility: load all image metadata as dict keyed by image_id."""
        result = {}
        conn = _get_db_connection()
        if not conn:
            return result
        try:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM images")
                for row in cur.fetchall():
                    image_id = row['image_id']
                    result[image_id] = {
                        'database': row['database_name'],
                        'entity_type': row['entity_type'],
                        'entity_id': row['entity_id'],
                        'original_filename': row['original_filename'],
                        'file_extension': row['file_extension'],
                        'description': row['description'],
                        'upload_date': row['created_at'].isoformat() if row['created_at'] else '',
                        'file_size': row['file_size'],
                        'file_hash': row['file_hash'],
                        'custom_metadata': row['custom_metadata'] or {},
                        'backed_up': row['backed_up']
                    }
        except Exception as e:
            logger.error(f"Error loading legacy metadata: {e}")
        finally:
            conn.close()
        return result


# Cache storage engines by resolved storage path and backup URL so callers can
# safely use isolated stores (for example a dedicated backup receiver path).
_image_storage_instances: Dict[Tuple[str, Optional[str], str], ImageStorageEngine] = {}


def get_image_storage(base_path: str = None, server_url: str = None) -> ImageStorageEngine:
    """Get or create an ImageStorageEngine instance for the requested storage path."""
    resolved_base = str(Path(base_path or DEFAULT_STORAGE_PATH).resolve())
    cache_key = (resolved_base, server_url, get_image_storage_backend_name())
    storage = _image_storage_instances.get(cache_key)
    if storage is None:
        storage = ImageStorageEngine(resolved_base, server_url)
        _image_storage_instances[cache_key] = storage
    return storage
