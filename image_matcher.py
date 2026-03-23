#!/usr/bin/env python3
"""
Smart Image Filename Matcher
Extracts inventory numbers, names, and localities from image filenames
and matches them with database records
"""

import re
import os
import logging
from typing import List, Dict, Optional, Tuple
from pathlib import Path
from difflib import SequenceMatcher

logger = logging.getLogger(__name__)


class ImageMatcher:
    """
    Smart image filename parser and database matcher.
    Matches images to database items based on inventory numbers, names, and localities.
    """

    # Database-specific inventory number patterns
    INVENTORY_PATTERNS = {
        'mineral': {
            'prefixes': ['M', 'MIN'],
            'pattern': r'((?:M|MIN)[-_\s]?\d{1,6})',  # M-12345, M12345, M 12345
            'field_name': 'inventarni_broj',
            'match_field': 'inventarni_broj'  # Field to match in database
        },
        'meteorite': {
            'prefixes': ['MET', 'METEOR'],
            'pattern': r'((?:MET|METEOR)[-_\s]?\d{1,6})',
            'field_name': 'catalog_number',
            'match_field': 'catalog_number'
        },
        'paleozoology': {
            'prefixes': ['PAL', 'PALEO'],
            'pattern': r'((?:PAL|PALEO)[-_\s]?(?:[A-Z]{2,10}[-_\s]?)?\d{1,6})',
            'field_name': 'catalog_number',
            'match_field': 'catalog_number'
        },
        'paleobotany': {
            'prefixes': ['PBOT', 'PB'],
            'pattern': r'((?:PBOT|PALBOT|PB)[-_\s]?(?:\d{4}[-_\s]?)?\d{1,6})',
            'field_name': 'catalog_number',
            'match_field': 'catalog_number'
        },
        'petrology': {
            'prefixes': ['PETR', 'PET'],
            'pattern': r'((?:PETR|PET|P)[-_\s]?(?:\d{4}[-_\s]?)?\d{1,6})',
            'field_name': 'catalog_number',
            'match_field': 'catalog_number'
        },
        'botany': {
            'prefixes': ['BOT', 'B'],
            'pattern': r'((?:BOT|B)[-_\s]?(?:\d{4}[-_\s]?)?\d{1,6})',
            'field_name': 'catalog_number',
            'match_field': 'catalog_number'
        },
        'ichthyology': {
            'prefixes': ['ICH', 'I'],
            'pattern': r'((?:ICH|I)[-_\s]?(?:\d{4}[-_\s]?)?\d{1,6})',
            'field_name': 'catalog_number',
            'match_field': 'catalog_number'
        },
        'entomology': {
            'prefixes': ['ENT', 'E'],
            'pattern': r'((?:ENT|E)[-_\s]?(?:[A-Z]{2,10}[-_\s]?)?\d{1,6})',
            'field_name': 'catalog_number',
            'match_field': 'catalog_number'
        },
        'mycology': {
            'prefixes': ['MYC', 'MY'],
            'pattern': r'((?:MYC|MY)[-_\s]?(?:\d{4}[-_\s]?)?\d{1,6})',
            'field_name': 'catalog_number',
            'match_field': 'catalog_number'
        },
        'herpetology': {
            'prefixes': ['HERP', 'H'],
            'pattern': r'((?:HERP|H)[-_\s]?(?:[A-Z]{2,10}[-_\s]?)?\d{1,6})',
            'field_name': 'catalog_number',
            'match_field': 'catalog_number'
        },
        'ornithology': {
            'prefixes': ['ORN', 'O'],
            'pattern': r'((?:ORN|O)[-_\s]?(?:\d{4}[-_\s]?)?\d{1,6})',
            'field_name': 'catalog_number',
            'match_field': 'catalog_number'
        },
        'library': {
            'prefixes': ['LIB', 'BOOK'],
            'pattern': r'((?:LIB|BOOK)[-_\s]?\d{1,6})',
            'field_name': 'book_id'
        },
        'cultural_heritage': {
            'prefixes': ['КД', 'CH'],
            'pattern': r'((?:КД|KD|CH|CULT)[-_\s]?(?:ПМ|PM)?[-_\s]?\d{1,6}(?:[/_-]\d{2,4})?)',
            'field_name': 'registry_number',
            'match_field': 'registry_number'
        }
    }

    # Generic number pattern (fallback)
    GENERIC_PATTERN = r'(\d{1,6})'

    def __init__(self):
        """Initialize the image matcher."""
        pass

    def normalize_identifier(self, value: str) -> str:
        """Normalize identifier strings for resilient comparison."""
        if not value:
            return ''
        return re.sub(r'[^0-9A-ZА-Я]+', '', str(value).upper())

    def extract_inventory_number(self, filename: str, database: str = None) -> Optional[str]:
        """
        Extract inventory number from filename.

        Args:
            filename: Image filename
            database: Optional database name for specific pattern matching

        Returns:
            Inventory number or None
        """
        # Remove file extension
        name = Path(filename).stem

        # If database specified, try its specific pattern
        if database and database in self.INVENTORY_PATTERNS:
            pattern = self.INVENTORY_PATTERNS[database]['pattern']
            match = re.search(pattern, name, re.IGNORECASE)
            if match:
                return match.group(1).strip().upper()

        # Try all database patterns
        for db_name, config in self.INVENTORY_PATTERNS.items():
            pattern = config['pattern']
            match = re.search(pattern, name, re.IGNORECASE)
            if match:
                return match.group(1).strip().upper()

        # Fallback: extract any 1-6 digit number
        match = re.search(self.GENERIC_PATTERN, name)
        if match:
            return match.group(1)

        return None

    def extract_metadata_from_filename(self, filename: str) -> Dict[str, str]:
        """
        Extract metadata from filename.
        Expected formats:
        - M12345_Quartz_Serbia.jpg
        - 12345-Кварц-Србија.jpg
        - M-12345_Quartz_Rudnik_Serbia.jpg

        Returns:
            Dictionary with inventory_number, name, locality
        """
        name = Path(filename).stem
        metadata = {
            'inventory_number': None,
            'name': None,
            'locality': None,
            'original_filename': filename
        }

        # Extract inventory number
        metadata['inventory_number'] = self.extract_inventory_number(filename)

        # Split by common separators
        parts = re.split(r'[-_\s]+', name)

        # Remove inventory number part from name extraction
        if metadata['inventory_number']:
            # Filter out parts that contain the inventory number
            parts = [p for p in parts if not re.search(r'\d{1,6}', p)]

        # Extract name and locality
        # Heuristic: First non-number part is name, last part could be locality
        non_empty_parts = [p for p in parts if p and len(p) > 1]

        if len(non_empty_parts) >= 1:
            metadata['name'] = non_empty_parts[0]

        if len(non_empty_parts) >= 2:
            # Last part is likely locality if it's a known place or contains certain keywords
            last_part = non_empty_parts[-1]
            locality_keywords = ['Serbia', 'Србија', 'Belgrade', 'Београд', 'Rudnik', 'Рудник']
            if any(kw.lower() in last_part.lower() for kw in locality_keywords) or len(last_part) > 3:
                metadata['locality'] = last_part
            else:
                # Middle parts could be additional name or locality
                if len(non_empty_parts) >= 3:
                    metadata['name'] = ' '.join(non_empty_parts[:-1])
                    metadata['locality'] = non_empty_parts[-1]

        return metadata

    def similarity_score(self, str1: str, str2: str) -> float:
        """Calculate similarity score between two strings (0-1)."""
        if not str1 or not str2:
            return 0.0
        return SequenceMatcher(None, str1.lower(), str2.lower()).ratio()

    def match_to_database_item(
        self,
        metadata: Dict[str, str],
        database_items: List[Dict],
        database: str
    ) -> Optional[Dict]:
        """
        Match extracted metadata to a database item.

        Args:
            metadata: Extracted metadata from filename
            database_items: List of database items to match against
            database: Database name

        Returns:
            Best matching item with confidence score
        """
        if not database_items:
            return None

        inv_number = metadata['inventory_number']
        name = metadata.get('name')
        locality = metadata.get('locality')

        best_match = None
        best_score = 0.0

        # Get field names for this database
        db_config = self.INVENTORY_PATTERNS.get(database, {})
        inv_field = db_config.get('match_field', db_config.get('field_name', 'inventarni_broj'))

        for item in database_items:
            score = 0.0
            match_reasons = []

            # Primary match: Inventory number (highest weight)
            item_inv = item.get(inv_field, '')

            # Handle float inventory numbers (like in mineral database)
            if isinstance(item_inv, float):
                item_inv = str(int(item_inv))
            else:
                item_inv = str(item_inv) if item_inv else ''

            if inv_number and item_inv:
                # Clean both for comparison
                inv_clean = self.normalize_identifier(inv_number)
                item_clean = self.normalize_identifier(item_inv)

                # Exact match
                if inv_clean == item_clean:
                    score += 100.0
                    match_reasons.append('inventory_exact')
                elif inv_clean in item_clean or item_clean in inv_clean:
                    score += 90.0
                    match_reasons.append('inventory_partial')
                else:
                    # Partial number match
                    inv_digits = re.findall(r'\d+', inv_clean)
                    item_digits = re.findall(r'\d+', item_clean)
                    if inv_digits and item_digits:
                        if inv_digits == item_digits:
                            score += 85.0
                            match_reasons.append('inventory_digit_groups_match')
                        elif inv_digits[-1] == item_digits[-1]:
                            score += 75.0
                            match_reasons.append('inventory_last_group_match')
                        elif inv_digits[0] == item_digits[0]:
                            score += 70.0
                            match_reasons.append('inventory_first_group_match')

            # Secondary match: Name/Title (medium weight)
            if name:
                for field in ['naziv', 'name', 'item_name', 'specimen_name', 'scientific_name', 'common_name_sr', 'mineral_name', 'title', 'species', 'rock_name']:
                    item_name = item.get(field, '')
                    if item_name:
                        name_similarity = self.similarity_score(name, str(item_name))
                        if name_similarity > 0.6:
                            score += name_similarity * 30.0
                            match_reasons.append(f'name_{name_similarity:.2f}')
                        break

            # Tertiary match: Locality (lower weight)
            if locality:
                for field in ['lokalitet', 'locality', 'location_found', 'location', 'origin', 'habitat']:
                    item_locality = item.get(field, '')
                    if item_locality:
                        locality_similarity = self.similarity_score(locality, str(item_locality))
                        if locality_similarity > 0.6:
                            score += locality_similarity * 20.0
                            match_reasons.append(f'locality_{locality_similarity:.2f}')
                        break

            # Update best match
            if score > best_score:
                best_score = score
                best_match = {
                    'item': item,
                    'score': score,
                    'confidence': 'high' if score >= 100 else 'medium' if score >= 50 else 'low',
                    'match_reasons': match_reasons,
                    'metadata': metadata
                }

        return best_match if best_score >= 30 else None

    def batch_match_images(
        self,
        image_files: List[str],
        database_items: List[Dict],
        database: str
    ) -> Dict[str, List]:
        """
        Batch match multiple images to database items.

        Args:
            image_files: List of image file paths
            database_items: List of database items
            database: Database name

        Returns:
            Dictionary with matched, unmatched, and ambiguous results
        """
        results = {
            'matched': [],      # Confident matches
            'unmatched': [],    # No match found
            'ambiguous': [],    # Multiple possible matches
            'errors': []        # Processing errors
        }

        for image_file in image_files:
            try:
                # Extract metadata
                metadata = self.extract_metadata_from_filename(os.path.basename(image_file))

                # Match to database
                match = self.match_to_database_item(metadata, database_items, database)

                if match:
                    match['image_path'] = image_file
                    if match['confidence'] == 'high':
                        results['matched'].append(match)
                    else:
                        results['ambiguous'].append(match)
                else:
                    results['unmatched'].append({
                        'image_path': image_file,
                        'metadata': metadata
                    })

            except Exception as e:
                logger.error(f"Error matching {image_file}: {e}")
                results['errors'].append({
                    'image_path': image_file,
                    'error': str(e)
                })

        return results

    def suggest_filename_format(self, database: str) -> str:
        """Get suggested filename format for a database."""
        if database in self.INVENTORY_PATTERNS:
            prefix = self.INVENTORY_PATTERNS[database]['prefixes'][0]
            return f"{prefix}12345_Naziv_Lokalitet.jpg"
        return "12345_Naziv_Lokalitet.jpg"

    def validate_filename(self, filename: str, database: str = None) -> Tuple[bool, str]:
        """
        Validate if filename contains required information.

        Returns:
            (is_valid, message)
        """
        metadata = self.extract_metadata_from_filename(filename)

        if not metadata['inventory_number']:
            return False, f"No inventory number found. Suggested format: {self.suggest_filename_format(database)}"

        if not metadata['name']:
            return False, "No name/title found in filename"

        return True, "Filename format is valid"


# Singleton instance
_image_matcher = None

def get_image_matcher() -> ImageMatcher:
    """Get or create singleton ImageMatcher instance."""
    global _image_matcher
    if _image_matcher is None:
        _image_matcher = ImageMatcher()
    return _image_matcher
