"""
Natural History Museum London - Data Portal API Integration
Based on CKAN API v3: https://docs.ckan.org/en/latest/api/index.html

Provides access to 284+ datasets and 35+ million specimen records
from the Natural History Museum, London.
"""

import json
import logging
import urllib.request
import urllib.parse
from typing import Dict, List, Optional, Any
from functools import lru_cache
import os

# Configure logging
logger = logging.getLogger(__name__)


class NHMDataPortalAPI:
    """
    Client for Natural History Museum London Data Portal (CKAN-based).

    The NHM Data Portal provides access to:
    - 284+ scientific datasets
    - 35.2 million specimen records
    - Collections: Entomology, Zoology, Botany, Palaeontology, Mineralogy
    """

    BASE_URL = "https://data.nhm.ac.uk/api/3/action"
    PORTAL_URL = "https://data.nhm.ac.uk"

    # Main collection departments
    DEPARTMENTS = {
        'entomology': {'name': 'Entomology', 'records': '2.5M'},
        'zoology': {'name': 'Zoology', 'records': '1.3M'},
        'botany': {'name': 'Botany', 'records': '1.2M'},
        'palaeontology': {'name': 'Palaeontology', 'records': '630K'},
        'mineralogy': {'name': 'Mineralogy', 'records': '376K'},
    }

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the NHM Data Portal API client.

        Args:
            api_key: Optional API key for authenticated requests (not required for read operations)
        """
        self.api_key = api_key or os.environ.get('NHM_API_KEY', '')
        self.timeout = 30  # seconds (larger datasets may take longer)
        self.user_agent = 'MuseumInfoSystem/1.0 (Natural History Museum Belgrade; nhmbeo.rs)'

    def _make_request(self, action: str, params: Optional[Dict] = None,
                      method: str = 'GET') -> Optional[Dict]:
        """
        Make a request to the CKAN API.

        Args:
            action: API action name (e.g., 'package_search')
            params: Query parameters
            method: HTTP method (GET or POST)

        Returns:
            JSON response as dictionary, or None on error
        """
        url = f"{self.BASE_URL}/{action}"

        if params and method == 'GET':
            url = f"{url}?{urllib.parse.urlencode(params)}"

        try:
            headers = {'User-Agent': self.user_agent}

            if self.api_key:
                headers['Authorization'] = self.api_key

            if method == 'POST':
                data = json.dumps(params).encode('utf-8') if params else None
                headers['Content-Type'] = 'application/json'
                req = urllib.request.Request(url, data=data, headers=headers, method='POST')
            else:
                req = urllib.request.Request(url, headers=headers)

            with urllib.request.urlopen(req, timeout=self.timeout) as response:
                data = json.loads(response.read().decode('utf-8'))

                if not data.get('success', False):
                    error = data.get('error', {})
                    logger.error(f"NHM API error: {error}")
                    return None

                return data.get('result')

        except urllib.error.URLError as e:
            logger.error(f"NHM API network error: {e}")
            return None
        except json.JSONDecodeError as e:
            logger.error(f"NHM API JSON parse error: {e}")
            return None
        except Exception as e:
            logger.error(f"NHM API unexpected error: {e}")
            return None

    # =========================================================================
    # DATASET OPERATIONS
    # =========================================================================

    def get_dataset_list(self, limit: int = 100, offset: int = 0) -> List[str]:
        """
        Get list of all dataset names/IDs.

        Args:
            limit: Maximum number of results
            offset: Offset for pagination

        Returns:
            List of dataset names
        """
        params = {'limit': limit, 'offset': offset}
        result = self._make_request('package_list', params)
        return result if result else []

    def get_all_datasets(self) -> List[str]:
        """
        Get complete list of all datasets (handles pagination).

        Returns:
            Complete list of all dataset names
        """
        all_datasets = []
        offset = 0
        limit = 500

        while True:
            batch = self.get_dataset_list(limit=limit, offset=offset)
            if not batch:
                break
            all_datasets.extend(batch)
            if len(batch) < limit:
                break
            offset += limit

        return all_datasets

    def search_datasets(self, query: str = '', rows: int = 25, start: int = 0,
                        sort: str = 'score desc', fq: str = '',
                        facet_fields: List[str] = None) -> Dict[str, Any]:
        """
        Search datasets using Solr query syntax.

        Args:
            query: Search query (Solr syntax supported)
            rows: Number of results to return (max 1000)
            start: Offset for pagination
            sort: Sort order (e.g., 'score desc', 'metadata_modified desc')
            fq: Filter query for faceting
            facet_fields: List of fields to facet on

        Returns:
            Dictionary with 'count', 'results', and 'facets'
        """
        params = {
            'q': query or '*:*',
            'rows': min(rows, 1000),
            'start': start,
            'sort': sort,
        }

        if fq:
            params['fq'] = fq

        if facet_fields:
            params['facet.field'] = json.dumps(facet_fields)

        result = self._make_request('package_search', params)

        if not result:
            return {'count': 0, 'results': [], 'facets': {}}

        # Process results
        datasets = []
        for pkg in result.get('results', []):
            datasets.append(self._format_dataset(pkg))

        return {
            'count': result.get('count', 0),
            'results': datasets,
            'facets': result.get('search_facets', {}),
            'query': query,
            'rows': rows,
            'start': start
        }

    def get_dataset(self, dataset_id: str) -> Optional[Dict]:
        """
        Get full metadata for a specific dataset.

        Args:
            dataset_id: Dataset name or ID

        Returns:
            Complete dataset metadata dictionary
        """
        params = {'id': dataset_id}
        result = self._make_request('package_show', params)

        if not result:
            return None

        return self._format_dataset_full(result)

    def get_dataset_resources(self, dataset_id: str) -> List[Dict]:
        """
        Get all resources for a dataset.

        Args:
            dataset_id: Dataset name or ID

        Returns:
            List of resource dictionaries
        """
        dataset = self.get_dataset(dataset_id)
        if not dataset:
            return []

        return dataset.get('resources', [])

    # =========================================================================
    # RESOURCE OPERATIONS
    # =========================================================================

    def get_resource(self, resource_id: str) -> Optional[Dict]:
        """
        Get metadata for a specific resource.

        Args:
            resource_id: Resource UUID

        Returns:
            Resource metadata dictionary
        """
        params = {'id': resource_id}
        result = self._make_request('resource_show', params)

        if not result:
            return None

        return self._format_resource(result)

    def search_resources(self, query: str, limit: int = 20,
                         offset: int = 0) -> Dict[str, Any]:
        """
        Search resources across all datasets.

        Args:
            query: Search query in format 'field:term' (e.g., 'format:csv')
            limit: Maximum results
            offset: Pagination offset

        Returns:
            Dictionary with 'count' and 'results'
        """
        params = {
            'query': query,
            'limit': limit,
            'offset': offset
        }

        result = self._make_request('resource_search', params)

        if not result:
            return {'count': 0, 'results': []}

        resources = []
        for res in result.get('results', []):
            resources.append(self._format_resource(res))

        return {
            'count': result.get('count', 0),
            'results': resources
        }

    # =========================================================================
    # DATASTORE OPERATIONS (for tabular data)
    # =========================================================================

    def datastore_search(self, resource_id: str, query: str = '',
                         filters: Dict = None, fields: List[str] = None,
                         limit: int = 100, offset: int = 0) -> Dict[str, Any]:
        """
        Search within a datastore resource (tabular data).

        Args:
            resource_id: Resource UUID
            query: Full-text search query
            filters: Dictionary of field filters
            fields: List of fields to return
            limit: Maximum records
            offset: Pagination offset

        Returns:
            Dictionary with records and metadata
        """
        params = {
            'resource_id': resource_id,
            'limit': limit,
            'offset': offset
        }

        if query:
            params['q'] = query
        if filters:
            params['filters'] = json.dumps(filters)
        if fields:
            params['fields'] = ','.join(fields)

        result = self._make_request('datastore_search', params)

        if not result:
            return {'total': 0, 'records': [], 'fields': []}

        return {
            'total': result.get('total', 0),
            'records': result.get('records', []),
            'fields': result.get('fields', []),
            'resource_id': resource_id
        }

    def datastore_search_sql(self, sql: str) -> Dict[str, Any]:
        """
        Execute SQL query on datastore resources.

        Args:
            sql: SQL SELECT statement

        Returns:
            Query results
        """
        params = {'sql': sql}
        result = self._make_request('datastore_search_sql', params)

        if not result:
            return {'records': [], 'fields': []}

        return {
            'records': result.get('records', []),
            'fields': result.get('fields', [])
        }

    # =========================================================================
    # ORGANIZATION & TAG OPERATIONS
    # =========================================================================

    @lru_cache(maxsize=1)
    def get_organization(self) -> Optional[Dict]:
        """
        Get Natural History Museum organization info.

        Returns:
            Organization metadata
        """
        params = {'id': 'natural-history-museum'}
        result = self._make_request('organization_show', params)
        return result

    @lru_cache(maxsize=1)
    def get_tags(self, vocabulary_id: str = None) -> List[Dict]:
        """
        Get list of all tags.

        Args:
            vocabulary_id: Optional vocabulary filter

        Returns:
            List of tag dictionaries
        """
        params = {}
        if vocabulary_id:
            params['vocabulary_id'] = vocabulary_id

        result = self._make_request('tag_list', params)
        return result if result else []

    def get_tag_info(self, tag_name: str) -> Optional[Dict]:
        """
        Get information about a specific tag.

        Args:
            tag_name: Tag name

        Returns:
            Tag metadata including associated datasets
        """
        params = {'id': tag_name}
        return self._make_request('tag_show', params)

    # =========================================================================
    # STATISTICS & INFO
    # =========================================================================

    def get_site_statistics(self) -> Dict[str, Any]:
        """
        Get portal statistics.

        Returns:
            Statistics dictionary
        """
        # Get dataset count
        search_result = self.search_datasets(rows=0)
        dataset_count = search_result.get('count', 0)

        # Get all datasets for more stats
        all_datasets = self.get_dataset_list(limit=500)

        return {
            'total_datasets': dataset_count,
            'dataset_names': len(all_datasets),
            'departments': self.DEPARTMENTS,
            'portal_url': self.PORTAL_URL,
            'api_url': self.BASE_URL,
            'total_records_estimate': '35.2 million',
            'total_specimens_estimate': '80 million'
        }

    # =========================================================================
    # CATEGORY-SPECIFIC SEARCHES
    # =========================================================================

    def search_by_department(self, department: str, rows: int = 25,
                             start: int = 0) -> Dict[str, Any]:
        """
        Search datasets by department/collection type.

        Args:
            department: Department name (entomology, zoology, botany, etc.)
            rows: Number of results
            start: Offset

        Returns:
            Search results filtered by department
        """
        # Use tags or full-text search for department
        return self.search_datasets(
            query=department,
            rows=rows,
            start=start
        )

    def search_specimens(self, scientific_name: str = '', genus: str = '',
                         family: str = '', collection: str = '',
                         rows: int = 50) -> Dict[str, Any]:
        """
        Search specimen records across collections.

        Args:
            scientific_name: Scientific name to search
            genus: Genus name
            family: Family name
            collection: Collection/department
            rows: Number of results

        Returns:
            Matching datasets/resources
        """
        query_parts = []

        if scientific_name:
            query_parts.append(f'"{scientific_name}"')
        if genus:
            query_parts.append(f'genus:{genus}')
        if family:
            query_parts.append(f'family:{family}')
        if collection:
            query_parts.append(collection)

        query = ' '.join(query_parts) if query_parts else '*:*'

        return self.search_datasets(query=query, rows=rows)

    # =========================================================================
    # HELPER METHODS
    # =========================================================================

    def _format_dataset(self, pkg: Dict) -> Dict:
        """Format dataset for display (summary)."""
        return {
            'id': pkg.get('id', ''),
            'name': pkg.get('name', ''),
            'title': pkg.get('title', ''),
            'notes': pkg.get('notes', '')[:300] + '...' if len(pkg.get('notes', '')) > 300 else pkg.get('notes', ''),
            'author': pkg.get('author', ''),
            'license_title': pkg.get('license_title', ''),
            'num_resources': len(pkg.get('resources', [])),
            'num_tags': len(pkg.get('tags', [])),
            'tags': [t.get('display_name', t.get('name', '')) for t in pkg.get('tags', [])[:5]],
            'metadata_created': pkg.get('metadata_created', ''),
            'metadata_modified': pkg.get('metadata_modified', ''),
            'state': pkg.get('state', ''),
            'portal_url': f"{self.PORTAL_URL}/dataset/{pkg.get('name', '')}",
        }

    def _format_dataset_full(self, pkg: Dict) -> Dict:
        """Format dataset with full details."""
        resources = []
        for res in pkg.get('resources', []):
            resources.append(self._format_resource(res))

        return {
            'id': pkg.get('id', ''),
            'name': pkg.get('name', ''),
            'title': pkg.get('title', ''),
            'notes': pkg.get('notes', ''),
            'author': pkg.get('author', ''),
            'author_email': pkg.get('author_email', ''),
            'maintainer': pkg.get('maintainer', ''),
            'maintainer_email': pkg.get('maintainer_email', ''),
            'license_id': pkg.get('license_id', ''),
            'license_title': pkg.get('license_title', ''),
            'license_url': pkg.get('license_url', ''),
            'organization': pkg.get('organization', {}),
            'resources': resources,
            'tags': [{'name': t.get('name', ''), 'display_name': t.get('display_name', '')}
                     for t in pkg.get('tags', [])],
            'extras': pkg.get('extras', []),
            'metadata_created': pkg.get('metadata_created', ''),
            'metadata_modified': pkg.get('metadata_modified', ''),
            'state': pkg.get('state', ''),
            'type': pkg.get('type', 'dataset'),
            'portal_url': f"{self.PORTAL_URL}/dataset/{pkg.get('name', '')}",
            'doi': pkg.get('doi', ''),
            'citation': pkg.get('citation', ''),
        }

    def _format_resource(self, res: Dict) -> Dict:
        """Format resource for display."""
        return {
            'id': res.get('id', ''),
            'name': res.get('name', ''),
            'description': res.get('description', ''),
            'format': res.get('format', '').upper(),
            'url': res.get('url', ''),
            'url_type': res.get('url_type', ''),
            'size': res.get('size'),
            'mimetype': res.get('mimetype', ''),
            'created': res.get('created', ''),
            'last_modified': res.get('last_modified', ''),
            'datastore_active': res.get('datastore_active', False),
            'download_url': res.get('url', ''),
        }

    def check_connection(self) -> bool:
        """
        Check if the API connection is working.

        Returns:
            True if connection successful, False otherwise
        """
        try:
            result = self._make_request('site_read')
            return result is not None
        except Exception:
            return False

    def get_status(self) -> Dict[str, Any]:
        """
        Get API status and configuration info.

        Returns:
            Status dictionary
        """
        connected = self.check_connection()
        stats = {}

        if connected:
            try:
                stats = self.get_site_statistics()
            except Exception as e:
                logger.warning(f"Could not get stats: {e}")

        return {
            'configured': True,  # No API key required for read operations
            'connected': connected,
            'base_url': self.BASE_URL,
            'portal_url': self.PORTAL_URL,
            'total_datasets': stats.get('total_datasets', 0),
            'api_docs': 'https://docs.ckan.org/en/latest/api/index.html',
        }


# Singleton instance for use across the application
_nhm_api_instance = None


def get_nhm_api() -> NHMDataPortalAPI:
    """
    Get or create singleton NHM API instance.

    Returns:
        NHMDataPortalAPI instance
    """
    global _nhm_api_instance
    if _nhm_api_instance is None:
        _nhm_api_instance = NHMDataPortalAPI()
    return _nhm_api_instance


# Test functionality
if __name__ == '__main__':
    print("Testing Natural History Museum London Data Portal API...")

    api = NHMDataPortalAPI()

    # Check status
    status = api.get_status()
    print(f"\nAPI Status: {'Connected' if status['connected'] else 'Not connected'}")
    print(f"Total datasets: {status.get('total_datasets', 'unknown')}")

    if status['connected']:
        # Test dataset search
        print("\n--- Testing Dataset Search ---")
        results = api.search_datasets('minerals', rows=5)
        print(f"Search 'minerals': {results['count']} datasets found")

        for ds in results['results'][:3]:
            print(f"\n  Title: {ds['title'][:60]}...")
            print(f"  Resources: {ds['num_resources']}")
            print(f"  Tags: {', '.join(ds['tags'][:3])}")

        # Test getting a specific dataset
        print("\n--- Testing Dataset Details ---")
        if results['results']:
            dataset = api.get_dataset(results['results'][0]['name'])
            if dataset:
                print(f"Dataset: {dataset['title']}")
                print(f"Author: {dataset['author']}")
                print(f"License: {dataset['license_title']}")
                print(f"Resources: {len(dataset['resources'])}")

        # Test department search
        print("\n--- Testing Department Search ---")
        entomology = api.search_by_department('entomology', rows=3)
        print(f"Entomology datasets: {entomology['count']}")

    else:
        print("\nConnection failed. Check network connectivity.")
