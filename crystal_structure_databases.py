#!/usr/bin/env python3
"""
Multi-Database Crystal Structure Search
Searches multiple crystallographic databases:
- Local RRUFF Database (PostgreSQL) - PRIMARY SOURCE with 5997 minerals
- Local CIF Files - Downloaded crystal structure files
- COD (Crystallography Open Database) - External
- AMCSD (American Mineralogist Crystal Structure Database) - External
"""

import os
import requests
import logging
import re
import concurrent.futures
from typing import List, Dict, Optional
from urllib.parse import quote
from pathlib import Path
from runtime_lock_utils import load_json_file

logger = logging.getLogger(__name__)

# Database URL
DATABASE_URL = os.environ.get('DATABASE_URL', 'postgresql+psycopg://aleksandarlukovic@localhost:5432/museum_system')

# Local CIF file storage
CIF_STORAGE_DIR = Path('/home/aleksandarlukovic/MuseumInfoSystem/data/cif_files')
COD_CIF_DIR = Path('/home/aleksandarlukovic/MuseumInfoSystem/data/cif_files/cod')


class CrystalStructureSearch:
    """Multi-database crystal structure search client."""

    def __init__(self):
        """Initialize the multi-database search client."""
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'MuseumInfoSystem/1.0 (Natural History Museum Belgrade)'
        })
        self.timeout = 10
        self._local_db = None
        self._cif_cache = {}

    def _get_local_db(self):
        """Get local mineral database instance."""
        if self._local_db is None:
            try:
                from mineral_database_pg import get_mineral_database
                self._local_db = get_mineral_database()
            except Exception as e:
                logger.error(f"Failed to connect to local database: {e}")
        return self._local_db

    def _get_local_cif(self, rruff_id: str) -> Optional[str]:
        """Get CIF content from local storage if available."""
        if not rruff_id:
            return None
        cif_path = CIF_STORAGE_DIR / f"{rruff_id}.cif"
        if cif_path.exists():
            try:
                content = cif_path.read_text(encoding='utf-8')
                if 'data_' in content or '_cell_' in content:
                    return content
            except Exception as e:
                logger.debug(f"Error reading local CIF {rruff_id}: {e}")
        return None

    def _save_local_cif(self, rruff_id: str, content: str) -> bool:
        """Save CIF content to local storage."""
        if not rruff_id or not content:
            return False
        try:
            CIF_STORAGE_DIR.mkdir(parents=True, exist_ok=True)
            cif_path = CIF_STORAGE_DIR / f"{rruff_id}.cif"
            cif_path.write_text(content, encoding='utf-8')
            return True
        except Exception as e:
            logger.debug(f"Error saving local CIF {rruff_id}: {e}")
        return False

    def _get_local_cod_cif(self, cod_id: str) -> Optional[str]:
        """Get CIF content from local COD storage if available."""
        if not cod_id:
            return None
        cif_path = COD_CIF_DIR / f"{cod_id}.cif"
        if cif_path.exists():
            try:
                content = cif_path.read_text(encoding='utf-8')
                if 'data_' in content or '_cell_' in content:
                    return content
            except Exception as e:
                logger.debug(f"Error reading local COD CIF {cod_id}: {e}")
        return None

    def _download_cod_cif_rsync(self, cod_id: str) -> Optional[str]:
        """Download a COD CIF file using rsync and cache it locally."""
        import subprocess

        COD_CIF_DIR.mkdir(parents=True, exist_ok=True)
        cif_path = COD_CIF_DIR / f"{cod_id}.cif"

        # Build rsync path: COD uses structure like /1/00/00/1000001.cif
        cod_str = str(cod_id)
        path_parts = [
            cod_str[0],
            cod_str[1:3] if len(cod_str) > 2 else '00',
            cod_str[3:5] if len(cod_str) > 4 else '00'
        ]
        remote_path = f"rsync://www.crystallography.net/cif/{'/'.join(path_parts)}/{cod_str}.cif"

        try:
            result = subprocess.run(
                ['rsync', '-az', remote_path, str(cif_path)],
                capture_output=True,
                timeout=30
            )
            if result.returncode == 0 and cif_path.exists():
                content = cif_path.read_text(encoding='utf-8')
                if 'data_' in content or '_cell_' in content:
                    logger.info(f"Downloaded COD CIF {cod_id} via rsync")
                    return content
        except Exception as e:
            logger.debug(f"Rsync download failed for COD {cod_id}: {e}")

        return None

    def search_all_databases(self, mineral_name: str, limit_per_db: int = 3, skip_external: bool = True) -> List[Dict]:
        """
        Search all available databases for a mineral.
        Prioritizes local databases (RRUFF + local COD).

        Args:
            mineral_name: Name of the mineral to search for
            limit_per_db: Maximum results per database
            skip_external: Skip slow external API searches (default True since we have local COD)

        Returns:
            Combined list of results from all databases
        """
        if not mineral_name:
            return []

        all_results = []

        # 1. Search local COD files FIRST (has CIF for 3D visualization)
        cod_results = self._search_local_cod(mineral_name, limit_per_db)
        all_results.extend(cod_results)

        # 2. Search local RRUFF database (has metadata but no CIF)
        local_results = self._search_local_rruff(mineral_name, limit_per_db)
        all_results.extend(local_results)

        # 3. Only try external databases if requested (slow, often timeout)
        if not skip_external:
            external_results = self._search_external_databases(mineral_name, limit_per_db)
            all_results.extend(external_results)

        return all_results

    def _search_local_cod(self, mineral_name: str, limit: int = 5) -> List[Dict]:
        """Search local COD CIF files by mineral name."""
        results = []
        try:
            # Search in COD filename index if exists
            index_file = COD_CIF_DIR / 'mineral_index.json'
            if index_file.exists():
                index = load_json_file(index_file, default={})
                if mineral_name.lower() in index:
                    for cod_id in index[mineral_name.lower()][:limit]:
                        cif_path = COD_CIF_DIR / f"{cod_id}.cif"
                        if cif_path.exists():
                            results.append(self._make_cod_entry(cod_id, mineral_name))

            # If no index, try common COD IDs for this mineral name
            # (The CIF files contain mineral names in metadata)
            if not results:
                # Quick scan of local files for matching mineral
                for cif_file in list(COD_CIF_DIR.glob('*.cif'))[:1000]:  # Limit scan
                    try:
                        content = cif_file.read_text(encoding='utf-8', errors='ignore')[:2000]
                        if mineral_name.lower() in content.lower():
                            cod_id = cif_file.stem
                            results.append(self._make_cod_entry(cod_id, mineral_name))
                            if len(results) >= limit:
                                break
                    except:
                        continue

        except Exception as e:
            logger.debug(f"Local COD search error: {e}")

        return results

    def _make_cod_entry(self, cod_id: str, mineral_name: str) -> Dict:
        """Create a COD result entry."""
        cif_path = COD_CIF_DIR / f"{cod_id}.cif"
        entry = {
            'database': 'COD',
            'database_full': 'Crystallography Open Database (Local)',
            'entry_id': cod_id,
            'formula': '',
            'compound_name': mineral_name,
            'a': '', 'b': '', 'c': '',
            'alpha': '', 'beta': '', 'gamma': '',
            'space_group': '',
            'crystal_system': '',
            'has_local_cif': True,
            'cif_url': f"/api/crystal/local/{cod_id}",
            'info_url': f"https://www.crystallography.net/cod/{cod_id}.html"
        }
        # Parse cell params from local CIF
        if cif_path.exists():
            try:
                content = cif_path.read_text(encoding='utf-8')
                self._parse_cell_params(entry, content)
                # Try to get formula
                for line in content.split('\n')[:100]:
                    if '_chemical_formula_sum' in line:
                        parts = line.split("'")
                        if len(parts) >= 2:
                            entry['formula'] = parts[1]
                        break
            except:
                pass
        return entry

    def _search_local_rruff(self, mineral_name: str, limit: int = 5) -> List[Dict]:
        """Search local RRUFF database (PostgreSQL)."""
        results = []
        try:
            db = self._get_local_db()
            if not db:
                return []

            # Get RRUFF data for this mineral
            rruff_data = db.get_rruff_data_for_mineral(mineral_name)

            if rruff_data:
                rruff_id = rruff_data.get('rruff_id', '')

                # Check for local CIF file
                local_cif = self._get_local_cif(rruff_id)
                has_local_cif = local_cif is not None

                entry = {
                    'database': 'RRUFF',
                    'database_full': 'RRUFF Project (Local Database)',
                    'entry_id': rruff_id,
                    'formula': rruff_data.get('formula_rruff', '') or rruff_data.get('formula_ima', ''),
                    'compound_name': rruff_data.get('name', mineral_name),
                    'a': '',
                    'b': '',
                    'c': '',
                    'alpha': '',
                    'beta': '',
                    'gamma': '',
                    'space_group': rruff_data.get('space_group', ''),
                    'crystal_system': rruff_data.get('crystal_system', ''),
                    'authors': 'RRUFF Project',
                    'journal': 'RRUFF Database',
                    'year': rruff_data.get('year_first_published', ''),
                    'ima_status': rruff_data.get('ima_status', ''),
                    'chemistry_elements': rruff_data.get('chemistry_elements', ''),
                    'has_local_cif': has_local_cif,
                    'cif_url': f"/api/crystal/local/{rruff_id}" if has_local_cif else '',  # Only provide URL if CIF exists
                    'info_url': f"https://rruff.info/{rruff_id}" if rruff_id else f"https://rruff.info/{quote(mineral_name)}",
                    'cif_unavailable': not has_local_cif  # Flag that CIF is not available
                }

                # Parse cell parameters from local CIF if available
                if local_cif:
                    self._parse_cell_params(entry, local_cif)

                results.append(entry)
                logger.info(f"Found {mineral_name} in local RRUFF database: {rruff_id} (local CIF: {has_local_cif})")

        except Exception as e:
            logger.error(f"Error searching local RRUFF for {mineral_name}: {e}")

        return results

    def _search_external_databases(self, mineral_name: str, limit_per_db: int = 2) -> List[Dict]:
        """Search external databases in parallel."""
        all_results = []

        with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
            futures = {
                executor.submit(self._search_cod, mineral_name, limit_per_db): 'COD',
                executor.submit(self._search_amcsd_direct, mineral_name, limit_per_db): 'AMCSD',
            }

            try:
                for future in concurrent.futures.as_completed(futures, timeout=15):
                    db_name = futures[future]
                    try:
                        results = future.result(timeout=3)
                        if results:
                            all_results.extend(results)
                            logger.info(f"Found {len(results)} results from {db_name}")
                    except Exception as e:
                        logger.debug(f"External search {db_name} failed: {e}")
            except concurrent.futures.TimeoutError:
                logger.warning("External database searches timed out")

        return all_results

    def _search_cod(self, mineral_name: str, limit: int = 3) -> List[Dict]:
        """Search Crystallography Open Database."""
        try:
            clean_name = re.sub(r'\s*\([^)]*\)', '', mineral_name).strip()

            url = "https://www.crystallography.net/cod/result"
            params = {'text': clean_name, 'format': 'json'}

            response = self.session.get(url, params=params, timeout=self.timeout)

            if response.status_code == 200:
                try:
                    results = response.json()
                    if isinstance(results, list) and results:
                        formatted = []
                        for entry in results[:limit]:
                            cod_id = str(entry.get('file', ''))
                            # Check if we have this CIF locally
                            has_local = (COD_CIF_DIR / f"{cod_id}.cif").exists()
                            formatted.append({
                                'database': 'COD',
                                'database_full': 'Crystallography Open Database',
                                'entry_id': cod_id,
                                'formula': entry.get('formula', ''),
                                'compound_name': entry.get('compname', '') or mineral_name,
                                'a': str(entry.get('a', '')),
                                'b': str(entry.get('b', '')),
                                'c': str(entry.get('c', '')),
                                'alpha': str(entry.get('alpha', '')),
                                'beta': str(entry.get('beta', '')),
                                'gamma': str(entry.get('gamma', '')),
                                'space_group': entry.get('sg', ''),
                                'crystal_system': '',
                                'authors': entry.get('authors', ''),
                                'journal': entry.get('journal', ''),
                                'year': str(entry.get('year', '')),
                                'doi': entry.get('doi', ''),
                                'has_local_cif': has_local,
                                'cif_url': f"/api/crystal/local/{cod_id}",
                                'info_url': f"https://www.crystallography.net/cod/{cod_id}.html"
                            })
                        return formatted
                except Exception as e:
                    logger.debug(f"COD JSON parse error: {e}")

            return []

        except Exception as e:
            logger.debug(f"COD search error: {e}")
            return []

    def _search_amcsd_direct(self, mineral_name: str, limit: int = 3) -> List[Dict]:
        """Search AMCSD by constructing direct CIF URLs."""
        results = []
        try:
            clean_name = mineral_name.strip().lower()

            # AMCSD has a known structure for mineral CIF files
            # Try to construct a valid reference
            results.append({
                'database': 'AMCSD',
                'database_full': 'American Mineralogist Crystal Structure Database',
                'entry_id': clean_name,
                'formula': '',
                'compound_name': mineral_name,
                'a': '', 'b': '', 'c': '',
                'alpha': '', 'beta': '', 'gamma': '',
                'space_group': '',
                'crystal_system': '',
                'authors': '',
                'journal': 'American Mineralogist',
                'year': '',
                'cif_url': f"http://rruff.geo.arizona.edu/AMS/xtal_data/CIFfiles/{quote(mineral_name)}.cif",
                'info_url': f"http://rruff.geo.arizona.edu/AMS/minerals/{quote(mineral_name)}"
            })

        except Exception as e:
            logger.debug(f"AMCSD search error: {e}")

        return results

    def get_cif_data(self, cif_url: str) -> Optional[str]:
        """Fetch CIF file content from URL."""
        if not cif_url:
            return None

        if cif_url in self._cif_cache:
            return self._cif_cache[cif_url]

        try:
            response = self.session.get(cif_url, timeout=self.timeout)
            if response.status_code == 200:
                content = response.text
                # Verify it looks like a CIF file
                if 'data_' in content or '_cell_' in content or '_atom_' in content:
                    # Cache only successful fetches so a transient failure is
                    # never memoized as a permanent "not found".
                    if len(self._cif_cache) >= 200:
                        self._cif_cache.clear()
                    self._cif_cache[cif_url] = content
                    return content
            return None

        except Exception as e:
            logger.debug(f"Error fetching CIF from {cif_url}: {e}")
            return None

    def get_cif_by_id(self, database: str, entry_id: str) -> Optional[str]:
        """Get CIF content by database and entry ID.

        Tries local files first, then remote sources.
        For COD: uses rsync if HTTP fails (more reliable).
        """
        db_upper = database.upper()

        # 1. Try local files first
        if db_upper == 'COD':
            local_cif = self._get_local_cod_cif(entry_id)
            if local_cif:
                return local_cif
        elif db_upper == 'RRUFF':
            local_cif = self._get_local_cif(entry_id)
            if local_cif:
                return local_cif

        # 2. Try HTTP download
        cif_url = None
        if db_upper == 'COD':
            cif_url = f"https://www.crystallography.net/cod/{entry_id}.cif"
        elif db_upper == 'AMCSD':
            cif_url = f"http://rruff.geo.arizona.edu/AMS/xtal_data/CIFfiles/{entry_id}.cif"
        elif db_upper == 'RRUFF':
            cif_url = f"https://rruff.info/{entry_id}.cif"

        if cif_url:
            cif = self.get_cif_data(cif_url)
            if cif:
                # Cache locally for future use
                if db_upper == 'COD':
                    COD_CIF_DIR.mkdir(parents=True, exist_ok=True)
                    (COD_CIF_DIR / f"{entry_id}.cif").write_text(cif, encoding='utf-8')
                elif db_upper == 'RRUFF':
                    self._save_local_cif(entry_id, cif)
                return cif

        # 3. Try rsync for COD (more reliable when HTTP times out)
        if db_upper == 'COD':
            cif = self._download_cod_cif_rsync(entry_id)
            if cif:
                return cif

        # 4. Try alternative RRUFF URLs
        if db_upper == 'RRUFF':
            alternatives = [
                f"https://www.rruff.net/{entry_id}.cif",
                f"https://rruff.info/repository/sample_child_record_cif/{entry_id}.cif",
            ]
            for alt_url in alternatives:
                cif = self.get_cif_data(alt_url)
                if cif:
                    self._save_local_cif(entry_id, cif)
                    return cif

        return None

    def search_mineral(self, mineral_name: str, limit: int = 5) -> List[Dict]:
        """Search for a mineral across all databases."""
        return self.search_all_databases(mineral_name, limit_per_db=max(2, limit // 2))

    def get_mineral_structure(self, mineral_name: str) -> Optional[Dict]:
        """Get the first available crystal structure for a mineral."""
        results = self.search_all_databases(mineral_name, limit_per_db=1)

        for entry in results:
            cif_url = entry.get('cif_url')
            if cif_url:
                cif_content = self.get_cif_data(cif_url)
                if cif_content:
                    entry['cif_content'] = cif_content
                    # Parse cell parameters from CIF
                    self._parse_cell_params(entry, cif_content)
                    return entry

        return results[0] if results else None

    def _parse_cell_params(self, entry: Dict, cif_content: str) -> None:
        """Parse cell parameters from CIF content and update entry."""
        try:
            lines = cif_content.split('\n')
            for line in lines:
                line = line.strip()
                if line.startswith('_cell_length_a'):
                    entry['a'] = self._extract_cif_number(line)
                elif line.startswith('_cell_length_b'):
                    entry['b'] = self._extract_cif_number(line)
                elif line.startswith('_cell_length_c'):
                    entry['c'] = self._extract_cif_number(line)
                elif line.startswith('_cell_angle_alpha'):
                    entry['alpha'] = self._extract_cif_number(line)
                elif line.startswith('_cell_angle_beta'):
                    entry['beta'] = self._extract_cif_number(line)
                elif line.startswith('_cell_angle_gamma'):
                    entry['gamma'] = self._extract_cif_number(line)
                elif '_symmetry_space_group' in line or '_space_group_name' in line:
                    parts = line.split()
                    if len(parts) > 1 and not entry.get('space_group'):
                        entry['space_group'] = ' '.join(parts[1:]).strip("'\"")
        except Exception as e:
            logger.debug(f"Error parsing CIF: {e}")

    def _extract_cif_number(self, line: str) -> str:
        """Extract numeric value from CIF line."""
        try:
            parts = line.split()
            if len(parts) > 1:
                # Remove uncertainty in parentheses, e.g., "5.123(4)"
                num_str = re.sub(r'\([^)]*\)', '', parts[1])
                return num_str
        except:
            pass
        return ''


# Singleton instance
_crystal_db = None


def get_crystal_structure_database() -> CrystalStructureSearch:
    """Get singleton crystal structure database instance."""
    global _crystal_db
    if _crystal_db is None:
        _crystal_db = CrystalStructureSearch()
    return _crystal_db


def get_cod_database() -> CrystalStructureSearch:
    """Backwards compatibility alias."""
    return get_crystal_structure_database()
