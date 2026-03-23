"""
NHM Dataset Downloader and Local Storage Manager
Downloads all datasets from Natural History Museum London Data Portal
and enables local search functionality.
"""

import os
import json
import logging
import time
import hashlib
from datetime import datetime
from typing import Dict, List, Optional, Any
from concurrent.futures import ThreadPoolExecutor, as_completed
import urllib.request
import urllib.error

from nhm_data_portal_api import NHMDataPortalAPI

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuration
NHM_DATA_DIR = os.path.join(os.path.dirname(__file__), 'data', 'nhm_datasets')
METADATA_FILE = os.path.join(NHM_DATA_DIR, 'datasets_metadata.json')
INDEX_FILE = os.path.join(NHM_DATA_DIR, 'search_index.json')
DOWNLOAD_LOG_FILE = os.path.join(NHM_DATA_DIR, 'download_log.json')


class NHMDatasetDownloader:
    """
    Downloads and manages NHM datasets locally.
    """

    def __init__(self, data_dir: str = NHM_DATA_DIR):
        self.data_dir = data_dir
        self.api = NHMDataPortalAPI()
        self.metadata_file = os.path.join(data_dir, 'datasets_metadata.json')
        self.index_file = os.path.join(data_dir, 'search_index.json')
        self.download_log_file = os.path.join(data_dir, 'download_log.json')

        # Ensure directory exists
        os.makedirs(data_dir, exist_ok=True)

    def download_all_datasets(self, include_resources: bool = False,
                               max_workers: int = 5,
                               progress_callback=None) -> Dict[str, Any]:
        """
        Download all dataset metadata from NHM Data Portal.

        Args:
            include_resources: If True, also download resource files (can be large!)
            max_workers: Number of parallel download threads
            progress_callback: Optional callback function(current, total, dataset_name)

        Returns:
            Download statistics
        """
        logger.info("Starting NHM dataset download...")
        start_time = time.time()

        # Get list of all datasets
        logger.info("Fetching dataset list...")
        all_dataset_names = self.api.get_all_datasets()
        total = len(all_dataset_names)
        logger.info(f"Found {total} datasets to download")

        # Download metadata for each dataset
        datasets = []
        errors = []
        downloaded = 0

        def download_dataset(name):
            try:
                dataset = self.api.get_dataset(name)
                if dataset:
                    return ('success', name, dataset)
                else:
                    return ('error', name, 'Dataset not found')
            except Exception as e:
                return ('error', name, str(e))

        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = {executor.submit(download_dataset, name): name
                       for name in all_dataset_names}

            for future in as_completed(futures):
                result = future.result()
                status, name, data = result

                if status == 'success':
                    datasets.append(data)
                    downloaded += 1
                else:
                    errors.append({'name': name, 'error': data})
                    logger.warning(f"Failed to download {name}: {data}")

                if progress_callback:
                    progress_callback(downloaded + len(errors), total, name)

                # Log progress every 50 datasets
                if (downloaded + len(errors)) % 50 == 0:
                    logger.info(f"Progress: {downloaded + len(errors)}/{total}")

        # Save metadata
        metadata = {
            'download_date': datetime.now().isoformat(),
            'total_datasets': len(datasets),
            'source': 'Natural History Museum London Data Portal',
            'source_url': 'https://data.nhm.ac.uk',
            'datasets': datasets
        }

        with open(self.metadata_file, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, ensure_ascii=False, indent=2)

        logger.info(f"Saved metadata to {self.metadata_file}")

        # Build search index
        self._build_search_index(datasets)

        # Save download log
        elapsed = time.time() - start_time
        log = {
            'timestamp': datetime.now().isoformat(),
            'total_datasets': total,
            'downloaded': downloaded,
            'errors': len(errors),
            'error_details': errors,
            'elapsed_seconds': round(elapsed, 2),
            'include_resources': include_resources
        }

        with open(self.download_log_file, 'w', encoding='utf-8') as f:
            json.dump(log, f, ensure_ascii=False, indent=2)

        logger.info(f"Download complete: {downloaded}/{total} datasets in {elapsed:.1f}s")

        return {
            'success': True,
            'total': total,
            'downloaded': downloaded,
            'errors': len(errors),
            'elapsed_seconds': round(elapsed, 2)
        }

    def _build_search_index(self, datasets: List[Dict]) -> None:
        """
        Build a search index from dataset metadata for fast local search.
        """
        logger.info("Building search index...")

        index = {
            'created': datetime.now().isoformat(),
            'total_datasets': len(datasets),
            'datasets': [],
            'tags': {},
            'authors': {},
            'formats': {},
            'keywords': {}
        }

        for ds in datasets:
            # Create searchable entry
            entry = {
                'id': ds.get('id', ''),
                'name': ds.get('name', ''),
                'title': ds.get('title', ''),
                'title_lower': ds.get('title', '').lower(),
                'notes': ds.get('notes', ''),
                'notes_lower': ds.get('notes', '').lower(),
                'author': ds.get('author', ''),
                'author_lower': ds.get('author', '').lower(),
                'tags': [t.get('name', '').lower() for t in ds.get('tags', [])],
                'num_resources': len(ds.get('resources', [])),
                'formats': list(set(r.get('format', '').upper()
                                    for r in ds.get('resources', []) if r.get('format'))),
                'metadata_modified': ds.get('metadata_modified', ''),
                'portal_url': ds.get('portal_url', ''),
            }

            index['datasets'].append(entry)

            # Index by tags
            for tag in entry['tags']:
                if tag:
                    if tag not in index['tags']:
                        index['tags'][tag] = []
                    index['tags'][tag].append(entry['name'])

            # Index by author
            author = entry['author_lower']
            if author:
                if author not in index['authors']:
                    index['authors'][author] = []
                index['authors'][author].append(entry['name'])

            # Index by format
            for fmt in entry['formats']:
                if fmt:
                    if fmt not in index['formats']:
                        index['formats'][fmt] = []
                    index['formats'][fmt].append(entry['name'])

            # Extract keywords from title and notes
            text = f"{entry['title_lower']} {entry['notes_lower']}"
            words = set(w for w in text.split() if len(w) > 3 and w.isalpha())
            for word in words:
                if word not in index['keywords']:
                    index['keywords'][word] = []
                if len(index['keywords'][word]) < 100:  # Limit to avoid huge lists
                    index['keywords'][word].append(entry['name'])

        with open(self.index_file, 'w', encoding='utf-8') as f:
            json.dump(index, f, ensure_ascii=False)

        logger.info(f"Search index built: {len(index['datasets'])} datasets, "
                    f"{len(index['tags'])} tags, {len(index['keywords'])} keywords")

    def update_datasets(self) -> Dict[str, Any]:
        """
        Update local datasets with any new or modified datasets from NHM.
        """
        if not os.path.exists(self.metadata_file):
            return self.download_all_datasets()

        # Load existing metadata
        with open(self.metadata_file, 'r', encoding='utf-8') as f:
            existing = json.load(f)

        existing_names = {ds['name'] for ds in existing.get('datasets', [])}
        existing_modified = {ds['name']: ds.get('metadata_modified', '')
                            for ds in existing.get('datasets', [])}

        # Get current list from API
        current_names = set(self.api.get_all_datasets())

        # Find new and potentially updated datasets
        new_names = current_names - existing_names
        logger.info(f"Found {len(new_names)} new datasets")

        # Download new datasets
        new_datasets = []
        for name in new_names:
            try:
                dataset = self.api.get_dataset(name)
                if dataset:
                    new_datasets.append(dataset)
            except Exception as e:
                logger.error(f"Failed to download {name}: {e}")

        # Merge with existing
        all_datasets = existing.get('datasets', []) + new_datasets

        # Update metadata
        metadata = {
            'download_date': existing.get('download_date'),
            'last_update': datetime.now().isoformat(),
            'total_datasets': len(all_datasets),
            'source': 'Natural History Museum London Data Portal',
            'source_url': 'https://data.nhm.ac.uk',
            'datasets': all_datasets
        }

        with open(self.metadata_file, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, ensure_ascii=False, indent=2)

        # Rebuild search index
        self._build_search_index(all_datasets)

        return {
            'success': True,
            'new_datasets': len(new_datasets),
            'total_datasets': len(all_datasets)
        }


class NHMLocalSearch:
    """
    Search through locally downloaded NHM datasets.
    """

    def __init__(self, data_dir: str = NHM_DATA_DIR):
        self.data_dir = data_dir
        self.metadata_file = os.path.join(data_dir, 'datasets_metadata.json')
        self.index_file = os.path.join(data_dir, 'search_index.json')
        self._metadata = None
        self._index = None

    @property
    def metadata(self) -> Optional[Dict]:
        """Load and cache metadata."""
        if self._metadata is None:
            if os.path.exists(self.metadata_file):
                with open(self.metadata_file, 'r', encoding='utf-8') as f:
                    self._metadata = json.load(f)
        return self._metadata

    @property
    def index(self) -> Optional[Dict]:
        """Load and cache search index."""
        if self._index is None:
            if os.path.exists(self.index_file):
                with open(self.index_file, 'r', encoding='utf-8') as f:
                    self._index = json.load(f)
        return self._index

    def is_available(self) -> bool:
        """Check if local data is available."""
        return os.path.exists(self.metadata_file) and os.path.exists(self.index_file)

    def get_statistics(self) -> Dict[str, Any]:
        """Get statistics about local data."""
        if not self.is_available():
            return {
                'available': False,
                'total_datasets': 0,
                'message': 'Local data not downloaded yet'
            }

        meta = self.metadata
        idx = self.index

        return {
            'available': True,
            'total_datasets': meta.get('total_datasets', 0),
            'download_date': meta.get('download_date', ''),
            'last_update': meta.get('last_update', ''),
            'total_tags': len(idx.get('tags', {})) if idx else 0,
            'total_authors': len(idx.get('authors', {})) if idx else 0,
            'total_formats': len(idx.get('formats', {})) if idx else 0,
        }

    def search(self, query: str, filters: Dict = None,
               limit: int = 50, offset: int = 0) -> Dict[str, Any]:
        """
        Search through local datasets.

        Args:
            query: Search query (searches title, notes, author, tags)
            filters: Optional filters {'tag': '...', 'author': '...', 'format': '...'}
            limit: Maximum results
            offset: Pagination offset

        Returns:
            Search results with datasets and metadata
        """
        if not self.is_available():
            return {
                'success': False,
                'error': 'Local data not available. Please download datasets first.',
                'results': [],
                'total': 0
            }

        idx = self.index
        query_lower = query.lower().strip()
        results = []

        # Get candidate datasets
        if query_lower:
            # Search in title, notes, author, tags
            candidates = set()

            for ds in idx.get('datasets', []):
                # Check title
                if query_lower in ds.get('title_lower', ''):
                    candidates.add(ds['name'])
                    continue

                # Check notes
                if query_lower in ds.get('notes_lower', ''):
                    candidates.add(ds['name'])
                    continue

                # Check author
                if query_lower in ds.get('author_lower', ''):
                    candidates.add(ds['name'])
                    continue

                # Check tags
                for tag in ds.get('tags', []):
                    if query_lower in tag:
                        candidates.add(ds['name'])
                        break

            # Also check keyword index for partial matches
            for keyword, names in idx.get('keywords', {}).items():
                if query_lower in keyword:
                    candidates.update(names)
        else:
            # No query - return all
            candidates = {ds['name'] for ds in idx.get('datasets', [])}

        # Apply filters
        if filters:
            if filters.get('tag'):
                tag_filter = filters['tag'].lower()
                tag_datasets = set(idx.get('tags', {}).get(tag_filter, []))
                candidates = candidates.intersection(tag_datasets)

            if filters.get('author'):
                author_filter = filters['author'].lower()
                author_datasets = set()
                for author, names in idx.get('authors', {}).items():
                    if author_filter in author:
                        author_datasets.update(names)
                candidates = candidates.intersection(author_datasets)

            if filters.get('format'):
                format_filter = filters['format'].upper()
                format_datasets = set(idx.get('formats', {}).get(format_filter, []))
                candidates = candidates.intersection(format_datasets)

        # Get full dataset info for candidates
        dataset_map = {ds['name']: ds for ds in idx.get('datasets', [])}

        for name in candidates:
            if name in dataset_map:
                results.append(dataset_map[name])

        # Sort: title matches first, then by modification date (newest first)
        # Python's sort is stable, so we can sort twice
        results.sort(key=lambda ds: ds.get('metadata_modified', '') or '', reverse=True)
        if query_lower:
            results.sort(key=lambda ds: query_lower not in ds.get('title_lower', ''))

        total = len(results)
        results = results[offset:offset + limit]

        return {
            'success': True,
            'results': results,
            'total': total,
            'query': query,
            'filters': filters,
            'limit': limit,
            'offset': offset
        }

    def get_dataset(self, dataset_name: str) -> Optional[Dict]:
        """Get full metadata for a specific dataset."""
        if not self.is_available():
            return None

        meta = self.metadata
        for ds in meta.get('datasets', []):
            if ds.get('name') == dataset_name or ds.get('id') == dataset_name:
                return ds

        return None

    def get_all_tags(self) -> List[Dict]:
        """Get all tags with counts."""
        if not self.is_available():
            return []

        idx = self.index
        tags = []

        for tag, datasets in idx.get('tags', {}).items():
            tags.append({
                'name': tag,
                'count': len(datasets)
            })

        tags.sort(key=lambda x: -x['count'])
        return tags

    def get_all_formats(self) -> List[Dict]:
        """Get all resource formats with counts."""
        if not self.is_available():
            return []

        idx = self.index
        formats = []

        for fmt, datasets in idx.get('formats', {}).items():
            formats.append({
                'name': fmt,
                'count': len(datasets)
            })

        formats.sort(key=lambda x: -x['count'])
        return formats

    def get_all_authors(self, limit: int = 100) -> List[Dict]:
        """Get all authors with counts."""
        if not self.is_available():
            return []

        idx = self.index
        authors = []

        for author, datasets in idx.get('authors', {}).items():
            authors.append({
                'name': author,
                'count': len(datasets)
            })

        authors.sort(key=lambda x: -x['count'])
        return authors[:limit]

    def get_datasets_by_tag(self, tag: str, limit: int = 50) -> List[Dict]:
        """Get all datasets with a specific tag."""
        return self.search('', filters={'tag': tag}, limit=limit)

    def get_datasets_by_format(self, format_type: str, limit: int = 50) -> List[Dict]:
        """Get all datasets with a specific resource format."""
        return self.search('', filters={'format': format_type}, limit=limit)


# Singleton instances
_downloader = None
_local_search = None


def get_nhm_downloader() -> NHMDatasetDownloader:
    """Get singleton downloader instance."""
    global _downloader
    if _downloader is None:
        _downloader = NHMDatasetDownloader()
    return _downloader


def get_nhm_local_search() -> NHMLocalSearch:
    """Get singleton local search instance."""
    global _local_search
    if _local_search is None:
        _local_search = NHMLocalSearch()
    return _local_search


# CLI interface
if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='NHM Dataset Downloader')
    parser.add_argument('action', choices=['download', 'update', 'search', 'stats'],
                        help='Action to perform')
    parser.add_argument('--query', '-q', help='Search query')
    parser.add_argument('--tag', help='Filter by tag')
    parser.add_argument('--format', help='Filter by format')

    args = parser.parse_args()

    if args.action == 'download':
        print("Downloading all NHM datasets...")
        downloader = get_nhm_downloader()

        def progress(current, total, name):
            print(f"\r[{current}/{total}] {name[:50]}...", end='', flush=True)

        result = downloader.download_all_datasets(progress_callback=progress)
        print(f"\n\nDownload complete!")
        print(f"  Total: {result['total']}")
        print(f"  Downloaded: {result['downloaded']}")
        print(f"  Errors: {result['errors']}")
        print(f"  Time: {result['elapsed_seconds']}s")

    elif args.action == 'update':
        print("Updating NHM datasets...")
        downloader = get_nhm_downloader()
        result = downloader.update_datasets()
        print(f"Update complete!")
        print(f"  New datasets: {result['new_datasets']}")
        print(f"  Total: {result['total_datasets']}")

    elif args.action == 'search':
        search = get_nhm_local_search()

        if not search.is_available():
            print("Local data not available. Run 'download' first.")
        else:
            filters = {}
            if args.tag:
                filters['tag'] = args.tag
            if args.format:
                filters['format'] = args.format

            results = search.search(args.query or '', filters=filters)
            print(f"Found {results['total']} datasets\n")

            for ds in results['results'][:10]:
                print(f"  - {ds['title'][:60]}")
                if ds['tags']:
                    print(f"    Tags: {', '.join(ds['tags'][:5])}")

    elif args.action == 'stats':
        search = get_nhm_local_search()
        stats = search.get_statistics()

        print("NHM Local Data Statistics")
        print("=" * 40)
        print(f"Available: {stats['available']}")
        if stats['available']:
            print(f"Total datasets: {stats['total_datasets']}")
            print(f"Download date: {stats['download_date']}")
            print(f"Last update: {stats.get('last_update', 'N/A')}")
            print(f"Total tags: {stats['total_tags']}")
            print(f"Total authors: {stats['total_authors']}")
            print(f"Total formats: {stats['total_formats']}")
