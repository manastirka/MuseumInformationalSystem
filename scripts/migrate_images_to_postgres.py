#!/usr/bin/env python3
"""
Migrate existing images from storage/images/ to ImagesDatabase/
and import references into PostgreSQL images table.

This script:
1. Reads metadata.json from old storage/images/ location
2. Copies image files to ImagesDatabase/
3. Inserts references into PostgreSQL images table
4. Verifies the migration
"""

import os
import sys
import json
import shutil
import logging
from pathlib import Path
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Paths
OLD_STORAGE = Path('./storage/images')
NEW_STORAGE = Path(os.environ.get('IMAGE_STORAGE_PATH', './ImagesDatabase'))
OLD_METADATA = OLD_STORAGE / 'metadata.json'

# Load DATABASE_URL from .env if not already set
if not os.environ.get('DATABASE_URL'):
    env_file = Path('.env')
    if env_file.exists():
        for line in env_file.read_text().splitlines():
            if line.startswith('DATABASE_URL='):
                os.environ['DATABASE_URL'] = line.split('=', 1)[1].strip()
                break


def get_db_connection():
    database_url = os.environ.get('DATABASE_URL')
    if not database_url:
        logger.error("DATABASE_URL not set")
        return None
    import psycopg
    from psycopg.rows import dict_row
    db_url = database_url.replace('postgresql+psycopg://', 'postgresql://')
    return psycopg.connect(db_url, row_factory=dict_row)


def migrate():
    logger.info("=" * 60)
    logger.info("Image Migration: storage/images/ -> ImagesDatabase/")
    logger.info("=" * 60)

    # Check old metadata exists
    if not OLD_METADATA.exists():
        logger.warning(f"No metadata.json found at {OLD_METADATA}")
        logger.info("Checking if images already exist in new location...")
        existing = list((NEW_STORAGE / 'originals').glob('*')) if (NEW_STORAGE / 'originals').exists() else []
        logger.info(f"Found {len(existing)} images in {NEW_STORAGE}/originals/")
        return

    # Load old metadata
    with open(OLD_METADATA, 'r', encoding='utf-8') as f:
        metadata = json.load(f)

    logger.info(f"Found {len(metadata)} images in old metadata")

    # Ensure new directories exist
    for subdir in ['originals', 'thumbnails/small', 'thumbnails/medium', 'thumbnails/large', 'temp']:
        (NEW_STORAGE / subdir).mkdir(parents=True, exist_ok=True)

    # Connect to PostgreSQL
    conn = get_db_connection()
    if not conn:
        logger.error("Cannot connect to PostgreSQL")
        return

    migrated = 0
    skipped = 0
    errors = 0

    try:
        with conn.cursor() as cur:
            # Check how many already migrated
            cur.execute("SELECT COUNT(*) as cnt FROM images")
            existing_count = cur.fetchone()['cnt']
            logger.info(f"PostgreSQL images table already has {existing_count} records")

            for image_id, meta in metadata.items():
                try:
                    # Check if already in PostgreSQL
                    cur.execute("SELECT image_id FROM images WHERE image_id = %s", (image_id,))
                    if cur.fetchone():
                        skipped += 1
                        continue

                    file_ext = meta.get('file_extension', '.jpg')

                    # Copy original file
                    old_original = OLD_STORAGE / 'originals' / f"{image_id}{file_ext}"
                    new_original = NEW_STORAGE / 'originals' / f"{image_id}{file_ext}"

                    if old_original.exists() and not new_original.exists():
                        shutil.copy2(old_original, new_original)

                    # Copy thumbnails
                    for size in ['small', 'medium', 'large']:
                        old_thumb = OLD_STORAGE / 'thumbnails' / size / f"{image_id}.jpg"
                        new_thumb = NEW_STORAGE / 'thumbnails' / size / f"{image_id}.jpg"
                        if old_thumb.exists() and not new_thumb.exists():
                            shutil.copy2(old_thumb, new_thumb)

                    # Get file size
                    file_size = 0
                    if new_original.exists():
                        file_size = new_original.stat().st_size
                    elif old_original.exists():
                        file_size = old_original.stat().st_size

                    # Insert into PostgreSQL
                    cur.execute("""
                        INSERT INTO images (
                            image_id, database_name, entity_type, entity_id,
                            original_filename, file_extension, file_path,
                            thumbnail_small, thumbnail_medium, thumbnail_large,
                            description, file_size, file_hash,
                            custom_metadata, backed_up, created_at
                        ) VALUES (
                            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                            %s, %s, %s, %s, %s, %s
                        )
                        ON CONFLICT (image_id) DO NOTHING
                    """, (
                        image_id,
                        meta.get('database', 'unknown'),
                        meta.get('entity_type', 'item'),
                        str(meta.get('entity_id', '')),
                        meta.get('original_filename', ''),
                        file_ext,
                        str(new_original),
                        str(NEW_STORAGE / 'thumbnails' / 'small' / f"{image_id}.jpg"),
                        str(NEW_STORAGE / 'thumbnails' / 'medium' / f"{image_id}.jpg"),
                        str(NEW_STORAGE / 'thumbnails' / 'large' / f"{image_id}.jpg"),
                        meta.get('description', ''),
                        file_size,
                        meta.get('file_hash', ''),
                        json.dumps(meta.get('custom_metadata', {})),
                        meta.get('backed_up', False),
                        meta.get('upload_date', datetime.now().isoformat())
                    ))

                    migrated += 1
                    logger.info(f"Migrated: {image_id}")

                except Exception as e:
                    logger.error(f"Error migrating {image_id}: {e}")
                    errors += 1

            conn.commit()

    except Exception as e:
        logger.error(f"Migration error: {e}")
        conn.rollback()
    finally:
        conn.close()

    # Verify
    logger.info("")
    logger.info("=" * 60)
    logger.info("Migration Summary:")
    logger.info(f"  Migrated:  {migrated}")
    logger.info(f"  Skipped:   {skipped} (already in PostgreSQL)")
    logger.info(f"  Errors:    {errors}")
    logger.info(f"  Total:     {len(metadata)}")
    logger.info("=" * 60)

    # Verify PostgreSQL
    conn = get_db_connection()
    if conn:
        try:
            with conn.cursor() as cur:
                cur.execute("SELECT COUNT(*) as cnt FROM images")
                total = cur.fetchone()['cnt']
                cur.execute("SELECT database_name, COUNT(*) as cnt FROM images GROUP BY database_name")
                by_db = {row['database_name']: row['cnt'] for row in cur.fetchall()}
            logger.info(f"\nPostgreSQL images table: {total} total records")
            for db_name, count in by_db.items():
                logger.info(f"  {db_name}: {count} images")
        finally:
            conn.close()

    # Verify files
    new_originals = list((NEW_STORAGE / 'originals').glob('*'))
    logger.info(f"\nImagesDatabase/originals/: {len(new_originals)} files")


if __name__ == '__main__':
    migrate()
