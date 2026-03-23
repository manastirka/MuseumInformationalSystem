#!/usr/bin/env python3
"""
Image Database Manager
Centralized management of image-to-entity relationships via PostgreSQL.
All image references are stored in the 'images' table in PostgreSQL.
Actual image files are stored in ImagesDatabase/ folder.
"""

import os
import json
import logging
from typing import List, Dict, Optional
from datetime import datetime

logger = logging.getLogger(__name__)


def _get_db_connection():
    """Get PostgreSQL connection."""
    database_url = os.environ.get('DATABASE_URL')
    if not database_url:
        return None
    try:
        import psycopg
        from psycopg.rows import dict_row
        db_url = database_url.replace('postgresql+psycopg://', 'postgresql://')
        conn = psycopg.connect(db_url, row_factory=dict_row)
        return conn
    except Exception as e:
        logger.error(f"Failed to connect to PostgreSQL: {e}")
        return None


class ImageDatabaseManager:
    """
    Centralized image database for all museum collections.
    Uses PostgreSQL 'images' table for all image-entity relationships.
    """

    def __init__(self, db_path: str = None):
        """Initialize image database manager. db_path is ignored (kept for compatibility)."""
        pass

    def add_image_to_item(
        self,
        database: str,
        entity_id: str,
        image_id: str,
        metadata: Dict = None
    ) -> bool:
        """
        Record an image-entity relationship in PostgreSQL.
        The actual image record should already exist in the images table
        (created by ImageStorageEngine.store_image).
        """
        conn = _get_db_connection()
        if not conn:
            logger.error("No PostgreSQL connection")
            return False
        try:
            with conn.cursor() as cur:
                # Check if image already exists in images table
                cur.execute("SELECT image_id FROM images WHERE image_id = %s", (image_id,))
                if cur.fetchone():
                    # Update metadata if provided
                    if metadata:
                        cur.execute("""
                            UPDATE images SET custom_metadata = custom_metadata || %s, updated_at = NOW()
                            WHERE image_id = %s
                        """, (json.dumps(metadata), image_id))
                    conn.commit()
                    logger.info(f"Image {image_id} linked to {database}/{entity_id}")
                    return True
                else:
                    logger.warning(f"Image {image_id} not found in images table")
                    return False
        except Exception as e:
            logger.error(f"Error adding image: {e}")
            conn.rollback()
            return False
        finally:
            conn.close()

    def remove_image_from_item(
        self,
        database: str,
        entity_id: str,
        image_id: str
    ) -> bool:
        """Remove an image reference (deletes from images table)."""
        conn = _get_db_connection()
        if not conn:
            return False
        try:
            with conn.cursor() as cur:
                cur.execute("""
                    DELETE FROM images
                    WHERE image_id = %s AND database_name = %s AND entity_id = %s
                """, (image_id, database, str(entity_id)))
            conn.commit()
            logger.info(f"Removed image {image_id} from {database}/{entity_id}")
            return True
        except Exception as e:
            logger.error(f"Error removing image: {e}")
            conn.rollback()
            return False
        finally:
            conn.close()

    def get_item_images(self, database: str, entity_id: str) -> List[str]:
        """Get all image IDs for a database item."""
        conn = _get_db_connection()
        if not conn:
            return []
        try:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT image_id FROM images
                    WHERE database_name = %s AND entity_id = %s
                    ORDER BY created_at
                """, (database, str(entity_id)))
                return [row['image_id'] for row in cur.fetchall()]
        except Exception as e:
            logger.error(f"Error getting images: {e}")
            return []
        finally:
            conn.close()

    def set_item_images(
        self,
        database: str,
        entity_id: str,
        image_ids: List[str]
    ) -> bool:
        """Set all images for a database item (kept for compatibility)."""
        # This is a no-op now since images are managed through the storage engine
        logger.info(f"set_item_images called for {database}/{entity_id} with {len(image_ids)} images")
        return True

    def get_database_items_with_images(self, database: str) -> Dict[str, List[str]]:
        """Get all items with images for a database."""
        conn = _get_db_connection()
        if not conn:
            return {}
        try:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT entity_id, array_agg(image_id ORDER BY created_at) as image_ids
                    FROM images WHERE database_name = %s
                    GROUP BY entity_id
                """, (database,))
                result = {}
                for row in cur.fetchall():
                    result[row['entity_id']] = list(row['image_ids'])
                return result
        except Exception as e:
            logger.error(f"Error getting database items: {e}")
            return {}
        finally:
            conn.close()

    def search_images(
        self,
        database: str = None,
        entity_id: str = None,
        has_images: bool = None
    ) -> List[Dict]:
        """Search for items based on image criteria."""
        conn = _get_db_connection()
        if not conn:
            return []
        try:
            with conn.cursor() as cur:
                conditions = []
                params = []

                if database:
                    conditions.append("database_name = %s")
                    params.append(database)
                if entity_id:
                    conditions.append("entity_id = %s")
                    params.append(str(entity_id))

                where = "WHERE " + " AND ".join(conditions) if conditions else ""

                cur.execute(f"""
                    SELECT database_name, entity_type, entity_id,
                           COUNT(*) as image_count,
                           array_agg(image_id) as image_ids
                    FROM images {where}
                    GROUP BY database_name, entity_type, entity_id
                    ORDER BY database_name, entity_id
                """, params)

                results = []
                for row in cur.fetchall():
                    results.append({
                        'database': row['database_name'],
                        'entity_id': row['entity_id'],
                        'image_count': row['image_count'],
                        'image_ids': list(row['image_ids']),
                        'entity_type': row['entity_type']
                    })
                return results
        except Exception as e:
            logger.error(f"Error searching images: {e}")
            return []
        finally:
            conn.close()

    def get_statistics(self) -> Dict:
        """Get image database statistics."""
        conn = _get_db_connection()
        if not conn:
            return {'total_items_with_images': 0, 'total_images': 0, 'by_database': {}}
        try:
            with conn.cursor() as cur:
                cur.execute("SELECT COUNT(*) as total FROM images")
                total_images = cur.fetchone()['total']

                cur.execute("""
                    SELECT COUNT(DISTINCT (database_name, entity_id)) as total
                    FROM images
                """)
                total_items = cur.fetchone()['total']

                cur.execute("""
                    SELECT database_name,
                           COUNT(DISTINCT entity_id) as items_with_images,
                           COUNT(*) as total_images
                    FROM images GROUP BY database_name
                """)
                by_database = {}
                for row in cur.fetchall():
                    by_database[row['database_name']] = {
                        'items_with_images': row['items_with_images'],
                        'total_images': row['total_images']
                    }

                return {
                    'total_items_with_images': total_items,
                    'total_images': total_images,
                    'by_database': by_database,
                    'last_updated': datetime.now().isoformat()
                }
        except Exception as e:
            logger.error(f"Error getting statistics: {e}")
            return {'total_items_with_images': 0, 'total_images': 0, 'by_database': {}}
        finally:
            conn.close()

    def export_database_images(self, database: str, output_file: str = None) -> Dict:
        """Export image mappings for a specific database."""
        conn = _get_db_connection()
        if not conn:
            return {'database': database, 'items': {}}

        export_data = {
            'database': database,
            'exported': datetime.now().isoformat(),
            'items': {}
        }

        try:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT entity_id, entity_type, image_id, created_at
                    FROM images WHERE database_name = %s
                    ORDER BY entity_id, created_at
                """, (database,))

                for row in cur.fetchall():
                    eid = row['entity_id']
                    if eid not in export_data['items']:
                        export_data['items'][eid] = {
                            'image_ids': [],
                            'entity_type': row['entity_type']
                        }
                    export_data['items'][eid]['image_ids'].append(row['image_id'])

            if output_file:
                with open(output_file, 'w', encoding='utf-8') as f:
                    json.dump(export_data, f, indent=2, ensure_ascii=False, default=str)
                logger.info(f"Exported database images to: {output_file}")

        except Exception as e:
            logger.error(f"Error exporting: {e}")
        finally:
            conn.close()

        return export_data

    def _get_entity_type(self, database: str) -> str:
        """Get entity type for database."""
        entity_types = {
            'mineral': 'collection_item',
            'meteorite': 'collection_item',
            'paleozoology': 'collection_item',
            'paleobotany': 'collection_item',
            'petrology': 'collection_item',
            'botany': 'collection_item',
            'ichthyology': 'collection_item',
            'entomology': 'collection_item',
            'mycology': 'collection_item',
            'herpetology': 'collection_item',
            'ornithology': 'collection_item',
            'conservation': 'collection_item',
            'general_zoology': 'collection_item',
            'geology_conservation': 'collection_item',
            'library': 'book',
            'cultural_heritage': 'heritage_item',
            'employees': 'employee',
            'exhibits': 'exhibit',
            'visitors': 'visitor',
            'research': 'research_project',
            'exhibitions': 'exhibition',
            'bird_ringing': 'bird_record'
        }
        return entity_types.get(database, 'item')


# Singleton instance
_image_db_manager = None

def get_image_db_manager(db_path: str = None) -> ImageDatabaseManager:
    """Get or create singleton ImageDatabaseManager instance."""
    global _image_db_manager
    if _image_db_manager is None:
        _image_db_manager = ImageDatabaseManager()
    return _image_db_manager
