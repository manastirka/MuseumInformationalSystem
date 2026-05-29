#!/usr/bin/env python3
"""
Batch Image Upload System
Handles multiple image uploads with smart matching to database items
"""

import os
import json
import logging
from typing import List, Dict, Optional
from pathlib import Path
from datetime import datetime
from image_storage_engine import get_image_storage
from image_matcher import get_image_matcher
from runtime_lock_utils import load_json_file, write_json_file

logger = logging.getLogger(__name__)


class BatchImageUploader:
    """Batch upload and match images to database items."""

    def __init__(self):
        """Initialize batch uploader."""
        self.storage = get_image_storage()
        self.matcher = get_image_matcher()
        self.upload_log_path = Path('./data/image_uploads')
        self.upload_log_path.mkdir(parents=True, exist_ok=True)

    def scan_directory(self, directory: str, extensions: List[str] = None) -> List[str]:
        """
        Scan directory for image files.

        Args:
            directory: Directory to scan
            extensions: List of file extensions (default: common image formats)

        Returns:
            List of image file paths
        """
        if extensions is None:
            extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.tiff']

        image_files = []
        dir_path = Path(directory)

        if not dir_path.exists():
            logger.error(f"Directory not found: {directory}")
            return []

        for ext in extensions:
            image_files.extend([str(f) for f in dir_path.glob(f'*{ext}')])
            image_files.extend([str(f) for f in dir_path.glob(f'*{ext.upper()}')])

        logger.info(f"Found {len(image_files)} images in {directory}")
        return sorted(image_files)

    def process_batch_upload(
        self,
        image_files: List[str],
        database_items: List[Dict],
        database: str,
        entity_type: str,
        auto_upload: bool = False,
        id_field: str = 'id'
    ) -> Dict:
        """
        Process batch image upload with matching.

        Args:
            image_files: List of image file paths
            database_items: List of database items to match against
            database: Database name
            entity_type: Entity type (e.g., 'collection_item', 'book')
            auto_upload: Automatically upload high-confidence matches
            id_field: Field name for entity ID in database items

        Returns:
            Upload results dictionary
        """
        # Match images to database items
        match_results = self.matcher.batch_match_images(
            image_files,
            database_items,
            database
        )

        upload_results = {
            'uploaded': [],
            'pending_review': [],
            'failed': [],
            'skipped': [],
            'summary': {
                'total_images': len(image_files),
                'uploaded_count': 0,
                'pending_count': 0,
                'failed_count': 0,
                'skipped_count': 0
            }
        }

        # Process high-confidence matches (auto-upload if enabled)
        for match in match_results['matched']:
            try:
                item = match['item']
                entity_id = str(item.get(id_field, ''))

                if not entity_id:
                    logger.warning(f"No ID found for item: {item}")
                    upload_results['failed'].append({
                        'image_path': match['image_path'],
                        'reason': 'No entity ID found'
                    })
                    upload_results['summary']['failed_count'] += 1
                    continue

                if auto_upload:
                    # Upload image
                    image_id = self.storage.store_image(
                        file_path=match['image_path'],
                        database=database,
                        entity_type=entity_type,
                        entity_id=entity_id,
                        description=f"Auto-uploaded: {match['metadata']['name'] or 'No description'}",
                        metadata={
                            'auto_matched': True,
                            'match_score': match['score'],
                            'match_reasons': match['match_reasons'],
                            'original_filename': os.path.basename(match['image_path'])
                        }
                    )

                    if image_id:
                        upload_results['uploaded'].append({
                            'image_id': image_id,
                            'image_path': match['image_path'],
                            'entity_id': entity_id,
                            'item': item,
                            'confidence': match['confidence'],
                            'score': match['score']
                        })
                        upload_results['summary']['uploaded_count'] += 1
                        logger.info(f"Uploaded: {os.path.basename(match['image_path'])} -> {entity_id}")
                    else:
                        upload_results['failed'].append({
                            'image_path': match['image_path'],
                            'reason': 'Storage error'
                        })
                        upload_results['summary']['failed_count'] += 1
                else:
                    # Add to pending review
                    upload_results['pending_review'].append({
                        'image_path': match['image_path'],
                        'entity_id': entity_id,
                        'item': item,
                        'confidence': match['confidence'],
                        'score': match['score'],
                        'metadata': match['metadata']
                    })
                    upload_results['summary']['pending_count'] += 1

            except Exception as e:
                logger.error(f"Error uploading {match['image_path']}: {e}")
                upload_results['failed'].append({
                    'image_path': match['image_path'],
                    'reason': str(e)
                })
                upload_results['summary']['failed_count'] += 1

        # Process ambiguous matches (always pending review)
        for match in match_results['ambiguous']:
            item = match['item']
            entity_id = str(item.get(id_field, ''))

            upload_results['pending_review'].append({
                'image_path': match['image_path'],
                'entity_id': entity_id,
                'item': item,
                'confidence': match['confidence'],
                'score': match['score'],
                'metadata': match['metadata']
            })
            upload_results['summary']['pending_count'] += 1

        # Process unmatched images
        for unmatched in match_results['unmatched']:
            upload_results['skipped'].append({
                'image_path': unmatched['image_path'],
                'metadata': unmatched['metadata'],
                'reason': 'No matching database item found'
            })
            upload_results['summary']['skipped_count'] += 1

        # Save upload log
        self._save_upload_log(database, upload_results)

        return upload_results

    def upload_single_image_to_item(
        self,
        image_path: str,
        database: str,
        entity_type: str,
        entity_id: str,
        description: str = None,
        metadata: Dict = None
    ) -> Optional[str]:
        """
        Upload a single image to a specific database item.

        Args:
            image_path: Path to image file
            database: Database name
            entity_type: Entity type
            entity_id: Entity ID
            description: Optional description
            metadata: Optional metadata

        Returns:
            Image ID or None
        """
        try:
            # Extract metadata from filename if not provided
            if not description:
                file_metadata = self.matcher.extract_metadata_from_filename(
                    os.path.basename(image_path)
                )
                description = file_metadata.get('name', 'Uploaded image')

            image_id = self.storage.store_image(
                file_path=image_path,
                database=database,
                entity_type=entity_type,
                entity_id=entity_id,
                description=description,
                metadata=metadata or {}
            )

            logger.info(f"Uploaded image {image_path} as {image_id}")
            return image_id

        except Exception as e:
            logger.error(f"Error uploading image: {e}")
            return None

    def update_database_item_images(
        self,
        database: str,
        entity_id: str,
        image_ids: List[str],
        update_callback=None
    ) -> bool:
        """
        Update database item with image IDs.

        Args:
            database: Database name
            entity_id: Entity ID
            image_ids: List of image IDs to add
            update_callback: Optional callback function to update database

        Returns:
            Success status
        """
        if update_callback:
            try:
                return update_callback(database, entity_id, image_ids)
            except Exception as e:
                logger.error(f"Error updating database: {e}")
                return False
        else:
            logger.warning("No update callback provided")
            return False

    def _save_upload_log(self, database: str, results: Dict):
        """Save upload log to file."""
        try:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            log_file = self.upload_log_path / f"{database}_{timestamp}.json"

            write_json_file(log_file, results, default=str)

            logger.info(f"Upload log saved: {log_file}")
        except Exception as e:
            logger.error(f"Error saving upload log: {e}")

    def get_upload_logs(self, database: str = None) -> List[Dict]:
        """Get upload logs, optionally filtered by database."""
        logs = []

        for log_file in sorted(self.upload_log_path.glob('*.json'), reverse=True):
            if database and not log_file.stem.startswith(database):
                continue

            try:
                log_data = load_json_file(log_file, default={})
                log_data['log_file'] = log_file.name
                log_data['timestamp'] = log_file.stem.split('_', 1)[-1]
                logs.append(log_data)
            except Exception as e:
                logger.error(f"Error reading log {log_file}: {e}")

        return logs

    def preview_batch_upload(
        self,
        directory: str,
        database_items: List[Dict],
        database: str
    ) -> Dict:
        """
        Preview batch upload without uploading.

        Args:
            directory: Directory containing images
            database_items: List of database items
            database: Database name

        Returns:
            Preview results
        """
        image_files = self.scan_directory(directory)

        if not image_files:
            return {
                'error': 'No images found in directory',
                'matched': [],
                'unmatched': [],
                'ambiguous': []
            }

        match_results = self.matcher.batch_match_images(
            image_files,
            database_items,
            database
        )

        return {
            'total_images': len(image_files),
            'matched_count': len(match_results['matched']),
            'unmatched_count': len(match_results['unmatched']),
            'ambiguous_count': len(match_results['ambiguous']),
            'error_count': len(match_results['errors']),
            'matched': match_results['matched'][:10],  # First 10 for preview
            'unmatched': match_results['unmatched'][:10],
            'ambiguous': match_results['ambiguous'][:10],
            'errors': match_results['errors']
        }


# Singleton instance
_batch_uploader = None

def get_batch_uploader() -> BatchImageUploader:
    """Get or create singleton BatchImageUploader instance."""
    global _batch_uploader
    if _batch_uploader is None:
        _batch_uploader = BatchImageUploader()
    return _batch_uploader
