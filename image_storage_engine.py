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
from datetime import datetime
from typing import Optional, List, Dict, Tuple
from pathlib import Path
from PIL import Image
import requests

logger = logging.getLogger(__name__)

# Default path - can be overridden via IMAGE_STORAGE_PATH env variable
# On server, set IMAGE_STORAGE_PATH to storage drive mount point
DEFAULT_STORAGE_PATH = os.environ.get('IMAGE_STORAGE_PATH', './ImagesDatabase')


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
        self._init_directories()
        self._ensure_db_table()
        logger.info(f"Image storage engine initialized at: {self.base_path}")

    def _init_directories(self):
        """Create ImagesDatabase directory structure."""
        directories = [
            self.base_path,
            self.base_path / 'originals',
            self.base_path / 'thumbnails' / 'small',
            self.base_path / 'thumbnails' / 'medium',
            self.base_path / 'thumbnails' / 'large',
            self.base_path / 'temp',
        ]
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)

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
                    thumb_path = self.base_path / 'thumbnails' / size_name / f"{image_id}.jpg"
                    thumbnail.save(thumb_path, 'JPEG', quality=85, optimize=True)
                    thumb_paths[size_name] = str(thumb_path)

            logger.info(f"Generated thumbnails for image: {image_id}")
        except Exception as e:
            logger.error(f"Error generating thumbnails: {e}")
            raise
        return thumb_paths

    def _cleanup_stored_files(self, original_path: Path, thumb_paths: Dict[str, str]):
        """Remove files written to disk when DB persistence fails."""
        for label, path_str in [('original', str(original_path))] + list(thumb_paths.items()):
            try:
                p = Path(path_str)
                if p.exists():
                    p.unlink()
            except OSError as exc:
                logger.warning("Could not clean up %s (%s): %s", label, path_str, exc)

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
            original_path = self.base_path / 'originals' / original_filename
            shutil.copy2(source_path, original_path)

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
                            str(original_path),
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
                    self._cleanup_stored_files(original_path, thumb_paths)
                    return None
                finally:
                    conn.close()
            else:
                logger.warning(f"No PostgreSQL connection - image {image_id} stored on disk only")

            logger.info(f"Image stored: {image_id} -> {original_path}")
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
                        path = Path(row['file_path'])
                        if path.exists():
                            return path
            except Exception as e:
                logger.error(f"Error querying image path: {e}")
            finally:
                conn.close()

        # Fallback: scan filesystem
        if size == 'original':
            for ext in self.ALLOWED_EXTENSIONS:
                path = self.base_path / 'originals' / f"{image_id}{ext}"
                if path.exists():
                    return path
        else:
            path = self.base_path / 'thumbnails' / size / f"{image_id}.jpg"
            if path.exists():
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
                path = Path(path_value)
                if path.exists():
                    path.unlink()

            # Legacy fallback for thumbnails if stored paths were incomplete.
            for size in self.THUMBNAIL_SIZES.keys():
                thumb_path = self.base_path / 'thumbnails' / size / f"{image_id}.jpg"
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

                    response = requests.post(
                        f"{self.server_backup_url}/api/images/backup/receive",
                        files=files,
                        data=data,
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

            backup_dir = self.base_path / 'backups' / backup_name
            backup_dir.mkdir(parents=True, exist_ok=True)

            originals_backup = backup_dir / 'originals'
            shutil.copytree(
                self.base_path / 'originals',
                originals_backup,
                dirs_exist_ok=True
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

            originals_backup = backup_dir / 'originals'
            if originals_backup.exists():
                for image_file in originals_backup.glob('*'):
                    shutil.copy2(
                        image_file,
                        self.base_path / 'originals' / image_file.name
                    )

            # Regenerate thumbnails for restored images
            for image_file in (self.base_path / 'originals').glob('*'):
                image_id = image_file.stem
                self._generate_thumbnails(image_file, image_id)

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
            'storage_path': str(self.base_path),
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


# Singleton instance
_image_storage = None

def get_image_storage(base_path: str = None, server_url: str = None) -> ImageStorageEngine:
    """Get or create singleton ImageStorageEngine instance."""
    global _image_storage
    if _image_storage is None:
        _image_storage = ImageStorageEngine(base_path or DEFAULT_STORAGE_PATH, server_url)
    return _image_storage
