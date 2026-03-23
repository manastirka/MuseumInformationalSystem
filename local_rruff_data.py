#!/usr/bin/env python3
"""
Local RRUFF Data Manager
Indexes and serves local RRUFF data files (powder diffraction, Raman, infrared, chemistry, images).
Provides methods to retrieve data by mineral name or RRUFF ID.
"""

import os
import re
import json
import logging
from typing import Dict, List, Optional, Tuple
from functools import lru_cache
from pathlib import Path

logger = logging.getLogger(__name__)

# Base path for RRUFF data
RRUFF_DATA_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'RRUFF_data')


class LocalRRUFFData:
    """Manager for local RRUFF data files."""

    def __init__(self, data_path: str = RRUFF_DATA_PATH):
        self.data_path = data_path
        self.powder_path = os.path.join(data_path, 'powder')
        self.raman_path = os.path.join(data_path, 'raman')
        self.infrared_path = os.path.join(data_path, 'infrared')
        self.chemistry_path = os.path.join(data_path, 'chemistry')
        self.images_path = data_path  # Images are in the root

        # File index cache
        self._index = None
        self._index_file = os.path.join(data_path, 'rruff_file_index.json')

        # Build or load index
        self._load_or_build_index()

    def _load_or_build_index(self):
        """Load existing index or build new one."""
        if os.path.exists(self._index_file):
            try:
                with open(self._index_file, 'r') as f:
                    self._index = json.load(f)
                logger.info(f"Loaded RRUFF index: {len(self._index.get('minerals', {}))} minerals")
                return
            except Exception as e:
                logger.warning(f"Could not load index: {e}")

        # Build new index
        self._build_index()

    def _build_index(self):
        """Build index of all RRUFF data files."""
        logger.info("Building RRUFF data index...")

        self._index = {
            'minerals': {},  # mineral_name -> { rruff_ids: [...], files: {...} }
            'rruff_ids': {},  # rruff_id -> mineral_name
            'stats': {
                'powder_files': 0,
                'raman_files': 0,
                'infrared_files': 0,
                'chemistry_files': 0,
                'image_files': 0
            }
        }

        # Index powder files
        if os.path.exists(self.powder_path):
            self._index_folder(self.powder_path, 'powder')

        # Index raman files
        if os.path.exists(self.raman_path):
            self._index_folder(self.raman_path, 'raman')

        # Index infrared files
        if os.path.exists(self.infrared_path):
            self._index_folder(self.infrared_path, 'infrared')

        # Index chemistry files
        if os.path.exists(self.chemistry_path):
            self._index_folder(self.chemistry_path, 'chemistry')

        # Index image files
        self._index_images()

        # Save index
        try:
            with open(self._index_file, 'w') as f:
                json.dump(self._index, f)
            logger.info(f"Saved RRUFF index: {len(self._index['minerals'])} minerals")
        except Exception as e:
            logger.error(f"Could not save index: {e}")

    def _parse_filename(self, filename: str) -> Optional[Dict]:
        """Parse RRUFF filename to extract mineral name and RRUFF ID.

        Format: MineralName__RRUFFID__DataType__Format__Hash.ext
        Example: Actinolite__R040063-1__Powder__DIF_File__2d4e3cfca6335429691913bc7ac4.txt
        """
        # Split by double underscore
        parts = filename.split('__')
        if len(parts) < 3:
            return None

        mineral_name = parts[0].replace('_', ' ').replace('-', ' ')
        rruff_id_full = parts[1]

        # Extract base RRUFF ID (without specimen number)
        rruff_id_match = re.match(r'^([RD]\d+)', rruff_id_full)
        if not rruff_id_match:
            return None

        rruff_id = rruff_id_match.group(1)

        # Determine data type and format
        data_type = parts[2] if len(parts) > 2 else 'Unknown'
        data_format = parts[3] if len(parts) > 3 else 'Unknown'

        return {
            'mineral_name': mineral_name,
            'rruff_id': rruff_id,
            'rruff_id_full': rruff_id_full,
            'data_type': data_type,
            'data_format': data_format,
            'filename': filename
        }

    def _index_folder(self, folder_path: str, category: str):
        """Index files in a folder."""
        count = 0
        for filename in os.listdir(folder_path):
            if filename.startswith('.') or filename.endswith('.zip'):
                continue

            parsed = self._parse_filename(filename)
            if not parsed:
                continue

            mineral_name = parsed['mineral_name']
            rruff_id = parsed['rruff_id']

            # Initialize mineral entry
            if mineral_name not in self._index['minerals']:
                self._index['minerals'][mineral_name] = {
                    'rruff_ids': [],
                    'powder': [],
                    'raman': [],
                    'infrared': [],
                    'chemistry': [],
                    'images': []
                }

            # Add RRUFF ID
            if rruff_id not in self._index['minerals'][mineral_name]['rruff_ids']:
                self._index['minerals'][mineral_name]['rruff_ids'].append(rruff_id)

            # Add to rruff_ids index
            self._index['rruff_ids'][rruff_id] = mineral_name

            # Add file to category
            file_info = {
                'filename': filename,
                'rruff_id': parsed['rruff_id_full'],
                'format': parsed['data_format'],
                'path': os.path.join(folder_path, filename)
            }
            self._index['minerals'][mineral_name][category].append(file_info)
            count += 1

        self._index['stats'][f'{category}_files'] = count
        logger.info(f"Indexed {count} {category} files")

    def _index_images(self):
        """Index image files in the root RRUFF data folder."""
        count = 0
        for filename in os.listdir(self.data_path):
            if not (filename.endswith('.jpeg') or filename.endswith('.jpg') or filename.endswith('.png')):
                continue

            parsed = self._parse_filename(filename)
            if not parsed:
                continue

            mineral_name = parsed['mineral_name']
            rruff_id = parsed['rruff_id']

            # Initialize mineral entry
            if mineral_name not in self._index['minerals']:
                self._index['minerals'][mineral_name] = {
                    'rruff_ids': [],
                    'powder': [],
                    'raman': [],
                    'infrared': [],
                    'chemistry': [],
                    'images': []
                }

            # Add RRUFF ID
            if rruff_id not in self._index['minerals'][mineral_name]['rruff_ids']:
                self._index['minerals'][mineral_name]['rruff_ids'].append(rruff_id)

            # Add to rruff_ids index
            self._index['rruff_ids'][rruff_id] = mineral_name

            # Add image
            self._index['minerals'][mineral_name]['images'].append({
                'filename': filename,
                'rruff_id': parsed['rruff_id_full'],
                'path': os.path.join(self.data_path, filename)
            })
            count += 1

        self._index['stats']['image_files'] = count
        logger.info(f"Indexed {count} image files")

    def get_mineral_data(self, mineral_name: str, include_data: bool = True) -> Optional[Dict]:
        """Get all available data for a mineral by name.

        Args:
            mineral_name: Name of the mineral to look up
            include_data: If True, includes parsed XY data for charts

        Returns:
            Dictionary with mineral data including parsed spectra if include_data=True
        """
        # Normalize name
        name_lower = mineral_name.lower().strip()

        # Try exact match first
        found_name = None
        found_data = None
        for indexed_name, data in self._index['minerals'].items():
            if indexed_name.lower() == name_lower:
                found_name = indexed_name
                found_data = data
                break

        # Try partial match if no exact match
        if not found_name:
            for indexed_name, data in self._index['minerals'].items():
                if name_lower in indexed_name.lower() or indexed_name.lower() in name_lower:
                    found_name = indexed_name
                    found_data = data
                    break

        if not found_name:
            return None

        # Build result with basic info
        result = {
            'mineral_name': found_name,
            'rruff_ids': found_data.get('rruff_ids', []),
            'powder': [],
            'raman': [],
            'infrared': [],
            'chemistry': found_data.get('chemistry', []),
            'images': []
        }

        # Process powder files
        for pf in found_data.get('powder', [])[:10]:  # Limit to 10 files
            file_info = {
                'filename': pf.get('filename'),
                'rruff_id': pf.get('rruff_id'),
                'format': pf.get('format'),
                'type': 'DIF' if 'DIF' in pf.get('format', '') else 'XY',
                'path': pf.get('path')
            }
            # Parse XY data if requested
            if include_data and 'DIF' not in pf.get('format', ''):
                xy_result = self.parse_xy_file(pf.get('path'))
                if xy_result and xy_result.get('data'):
                    # Convert to simple [x, y] format for charts
                    file_info['data'] = [[p['x'], p['y']] for p in xy_result['data'][:2000]]
                    file_info['metadata'] = xy_result.get('metadata', {})
            result['powder'].append(file_info)

        # Process raman files
        for rf in found_data.get('raman', [])[:10]:  # Limit to 10 files
            file_info = {
                'filename': rf.get('filename'),
                'rruff_id': rf.get('rruff_id'),
                'format': rf.get('format'),
                'laser': self._extract_laser_info(rf.get('filename', '')),
                'orientation': self._extract_orientation(rf.get('filename', '')),
                'path': rf.get('path')
            }
            # Parse Raman data if requested
            if include_data:
                raman_result = self.parse_xy_file(rf.get('path'))
                if raman_result and raman_result.get('data'):
                    file_info['data'] = [[p['x'], p['y']] for p in raman_result['data'][:2000]]
                    file_info['metadata'] = raman_result.get('metadata', {})
            result['raman'].append(file_info)

        # Process infrared files
        for irf in found_data.get('infrared', [])[:10]:  # Limit to 10 files
            file_info = {
                'filename': irf.get('filename'),
                'rruff_id': irf.get('rruff_id'),
                'format': irf.get('format'),
                'type': 'IR',
                'path': irf.get('path')
            }
            # Parse IR data if requested
            if include_data:
                ir_result = self.parse_xy_file(irf.get('path'))
                if ir_result and ir_result.get('data'):
                    file_info['data'] = [[p['x'], p['y']] for p in ir_result['data'][:2000]]
                    file_info['metadata'] = ir_result.get('metadata', {})
            result['infrared'].append(file_info)

        # Process images (include relative paths for serving)
        for img in found_data.get('images', [])[:10]:  # Limit to 10 images
            img_path = img.get('path', '')
            # Make path relative to RRUFF_data folder
            relative_path = os.path.basename(img_path)
            result['images'].append({
                'filename': img.get('filename'),
                'rruff_id': img.get('rruff_id'),
                'path': img_path,
                'relative_path': relative_path
            })

        return result

    def _extract_laser_info(self, filename: str) -> str:
        """Extract laser wavelength from Raman filename."""
        match = re.search(r'(\d{3})nm', filename)
        if match:
            return f"{match.group(1)}nm"
        return ''

    def _extract_orientation(self, filename: str) -> str:
        """Extract crystal orientation from Raman filename."""
        match = re.search(r'(oriented|unoriented)', filename.lower())
        if match:
            return match.group(1).capitalize()
        return ''

    def get_data_by_rruff_id(self, rruff_id: str) -> Optional[Dict]:
        """Get all available data for a mineral by RRUFF ID."""
        # Normalize ID
        rruff_id = rruff_id.upper().strip()

        # Extract base ID
        base_id = re.match(r'^([RD]\d+)', rruff_id)
        if base_id:
            rruff_id = base_id.group(1)

        if rruff_id in self._index['rruff_ids']:
            mineral_name = self._index['rruff_ids'][rruff_id]
            return self.get_mineral_data(mineral_name)

        return None

    def get_powder_dif_data(self, mineral_name: str) -> Optional[Dict]:
        """Get powder diffraction DIF data for a mineral.
        Returns parsed crystal structure suitable for 3D visualization."""
        mineral_data = self.get_mineral_data(mineral_name)
        if not mineral_data:
            return None

        # Find DIF file
        dif_file = None
        for pf in mineral_data.get('powder', []):
            if 'DIF' in pf.get('format', ''):
                dif_file = pf
                break

        if not dif_file:
            return None

        return self.parse_dif_file(dif_file['path'])

    def parse_dif_file(self, filepath: str) -> Optional[Dict]:
        """Parse a DIF file and extract crystal structure data."""
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()

            result = {
                'mineral_name': '',
                'cell_parameters': {},
                'space_group': '',
                'atoms': [],
                'diffraction_data': [],
                'source': filepath
            }

            lines = content.split('\n')
            in_atom_section = False
            in_diffraction_section = False

            for line in lines:
                line = line.strip()

                # Get mineral name (first line)
                if not result['mineral_name'] and line and not line.startswith('#') and not line.startswith('Diffraction'):
                    result['mineral_name'] = line
                    continue

                # Parse cell parameters
                if line.startswith('CELL PARAMETERS:'):
                    params = line.replace('CELL PARAMETERS:', '').strip().split()
                    if len(params) >= 6:
                        result['cell_parameters'] = {
                            'a': float(params[0]),
                            'b': float(params[1]),
                            'c': float(params[2]),
                            'alpha': float(params[3]),
                            'beta': float(params[4]),
                            'gamma': float(params[5])
                        }

                # Parse space group (handle different formats)
                if line.startswith('SPACE GROUP:'):
                    result['space_group'] = line.replace('SPACE GROUP:', '').strip()
                elif 'ALTERNATE SETTING FOR SPACE GROUP:' in line:
                    result['space_group'] = line.split('SPACE GROUP:')[1].strip()
                elif 'SPACE GROUP' in line and ':' in line:
                    result['space_group'] = line.split(':')[1].strip()

                # Detect atom section start
                if 'ATOM' in line and ('X' in line or 'Y' in line or 'Z' in line):
                    in_atom_section = True
                    in_diffraction_section = False
                    continue

                # Detect diffraction data section
                if '2-THETA' in line or 'INTENSITY' in line:
                    in_atom_section = False
                    in_diffraction_section = True
                    continue

                # Parse atom data
                if in_atom_section and line:
                    parts = line.split()
                    if len(parts) >= 4:
                        try:
                            atom = {
                                'element': parts[0],
                                'x': float(parts[1]),
                                'y': float(parts[2]),
                                'z': float(parts[3])
                            }
                            if len(parts) >= 5:
                                atom['occupancy'] = float(parts[4])
                            if len(parts) >= 6:
                                atom['b_iso'] = float(parts[5])
                            result['atoms'].append(atom)
                        except (ValueError, IndexError):
                            pass

                # Parse diffraction data
                if in_diffraction_section and line:
                    parts = line.split()
                    if len(parts) >= 4:
                        try:
                            diff = {
                                'two_theta': float(parts[0]),
                                'intensity': float(parts[1]),
                                'd_spacing': float(parts[2]),
                                'h': int(parts[3]) if len(parts) > 3 else 0,
                                'k': int(parts[4]) if len(parts) > 4 else 0,
                                'l': int(parts[5]) if len(parts) > 5 else 0
                            }
                            result['diffraction_data'].append(diff)
                        except (ValueError, IndexError):
                            pass

            return result

        except Exception as e:
            logger.error(f"Error parsing DIF file {filepath}: {e}")
            return None

    def get_powder_xy_data(self, mineral_name: str, processed: bool = True) -> Optional[Dict]:
        """Get powder diffraction XY data (2-theta vs intensity)."""
        mineral_data = self.get_mineral_data(mineral_name)
        if not mineral_data:
            return None

        # Find XY file
        target_format = 'XY_Processed' if processed else 'XY_RAW'
        xy_file = None
        for pf in mineral_data.get('powder', []):
            if target_format in pf.get('format', '') or 'Xray_Data_XY' in pf.get('format', ''):
                xy_file = pf
                break

        if not xy_file:
            return None

        return self.parse_xy_file(xy_file['path'])

    def parse_xy_file(self, filepath: str) -> Optional[Dict]:
        """Parse an XY powder diffraction file."""
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()

            result = {
                'metadata': {},
                'data': [],
                'source': filepath
            }

            lines = content.split('\n')

            for line in lines:
                line = line.strip()

                # Parse metadata
                if line.startswith('##'):
                    match = re.match(r'##([^=]+)=(.+)', line)
                    if match:
                        key = match.group(1).strip()
                        value = match.group(2).strip()
                        result['metadata'][key] = value
                    continue

                # Parse data (X, Y format)
                if line and not line.startswith('#'):
                    # Handle both comma and space separated
                    if ',' in line:
                        parts = line.split(',')
                    else:
                        parts = line.split()

                    if len(parts) >= 2:
                        try:
                            x = float(parts[0].strip())
                            y = float(parts[1].strip())
                            result['data'].append({'x': x, 'y': y})
                        except ValueError:
                            pass

            return result

        except Exception as e:
            logger.error(f"Error parsing XY file {filepath}: {e}")
            return None

    def get_raman_data(self, mineral_name: str) -> Optional[Dict]:
        """Get Raman spectroscopy data for a mineral."""
        mineral_data = self.get_mineral_data(mineral_name)
        if not mineral_data:
            return None

        raman_files = mineral_data.get('raman', [])
        if not raman_files:
            return None

        # Get first processed file
        for rf in raman_files:
            if 'Processed' in rf.get('format', ''):
                return self.parse_raman_file(rf['path'])

        # Fall back to any raman file
        return self.parse_raman_file(raman_files[0]['path'])

    def parse_raman_file(self, filepath: str) -> Optional[Dict]:
        """Parse a Raman spectroscopy file."""
        return self.parse_xy_file(filepath)  # Same format as XY files

    def get_infrared_data(self, mineral_name: str) -> Optional[Dict]:
        """Get infrared spectroscopy data for a mineral."""
        mineral_data = self.get_mineral_data(mineral_name)
        if not mineral_data:
            return None

        ir_files = mineral_data.get('infrared', [])
        if not ir_files:
            return None

        return self.parse_xy_file(ir_files[0]['path'])

    def get_image_path(self, mineral_name: str) -> Optional[str]:
        """Get path to mineral specimen image."""
        mineral_data = self.get_mineral_data(mineral_name)
        if not mineral_data:
            return None

        images = mineral_data.get('images', [])
        if not images:
            return None

        return images[0]['path']

    def get_stats(self) -> Dict:
        """Get statistics about indexed data."""
        return {
            'total_minerals': len(self._index['minerals']),
            'total_rruff_ids': len(self._index['rruff_ids']),
            **self._index['stats']
        }

    def search_minerals(self, query: str, limit: int = 20) -> List[Dict]:
        """Search for minerals by name."""
        query_lower = query.lower().strip()
        results = []

        for mineral_name, data in self._index['minerals'].items():
            if query_lower in mineral_name.lower():
                results.append({
                    'mineral_name': mineral_name,
                    'rruff_ids': data['rruff_ids'],
                    'has_powder': len(data['powder']) > 0,
                    'has_raman': len(data['raman']) > 0,
                    'has_infrared': len(data['infrared']) > 0,
                    'has_chemistry': len(data['chemistry']) > 0,
                    'has_images': len(data['images']) > 0
                })

                if len(results) >= limit:
                    break

        return results

    def generate_cif_from_dif(self, mineral_name: str, expand_unitcell: bool = False, supercell: tuple = None) -> Optional[str]:
        """Generate a CIF string from DIF data for 3D visualization.

        Args:
            mineral_name: Name of the mineral
            expand_unitcell: If True, apply symmetry operations to generate full unit cell
            supercell: Tuple (nx, ny, nz) to generate supercell, e.g., (2, 2, 2)
        """
        dif_data = self.get_powder_dif_data(mineral_name)
        if not dif_data or not dif_data.get('atoms'):
            return None

        cell = dif_data.get('cell_parameters', {})
        atoms = dif_data.get('atoms', [])
        space_group = dif_data.get('space_group', 'P 1')

        # Get symmetry operations
        symops = self._get_symmetry_operations(space_group)

        # Generate atoms
        if expand_unitcell or supercell:
            # Apply symmetry operations to expand to full unit cell
            expanded_atoms = self._apply_symmetry_operations(atoms, symops)

            # Apply supercell replication if requested
            if supercell:
                nx, ny, nz = supercell
                expanded_atoms = self._generate_supercell_atoms(expanded_atoms, nx, ny, nz)

            atoms_to_use = expanded_atoms
        else:
            atoms_to_use = atoms

        # Build CIF content
        cif_lines = [
            f"data_{mineral_name.replace(' ', '_')}",
            "",
            "# Cell parameters",
            f"_cell_length_a {cell.get('a', 10):.4f}",
            f"_cell_length_b {cell.get('b', 10):.4f}",
            f"_cell_length_c {cell.get('c', 10):.4f}",
            f"_cell_angle_alpha {cell.get('alpha', 90):.2f}",
            f"_cell_angle_beta {cell.get('beta', 90):.2f}",
            f"_cell_angle_gamma {cell.get('gamma', 90):.2f}",
            f"_cell_volume {self._calculate_cell_volume(cell):.2f}",
            "",
            "# Symmetry",
            f"_symmetry_space_group_name_H-M 'P 1'",
            f"_symmetry_Int_Tables_number 1",
            ""
        ]

        # Add atom sites
        cif_lines.extend([
            "loop_",
            "_atom_site_label",
            "_atom_site_type_symbol",
            "_atom_site_fract_x",
            "_atom_site_fract_y",
            "_atom_site_fract_z",
            "_atom_site_occupancy",
            "_atom_site_U_iso_or_equiv"
        ])

        for i, atom in enumerate(atoms_to_use):
            element = atom.get('element', 'X')
            # Clean element symbol
            element_clean = ''.join(c for c in element if c.isalpha())[:2]
            label = f"{element_clean}{i+1}"
            x = atom.get('x', 0)
            y = atom.get('y', 0)
            z = atom.get('z', 0)
            occ = atom.get('occupancy', 1.0)
            b_iso = atom.get('b_iso', 0.01)
            u_iso = b_iso / 78.9568 if b_iso > 0 else 0.01
            cif_lines.append(f"{label} {element_clean} {x:.5f} {y:.5f} {z:.5f} {occ:.3f} {u_iso:.4f}")

        return '\n'.join(cif_lines)

    def _apply_symmetry_operations(self, atoms: List[Dict], symops: List[str]) -> List[Dict]:
        """Apply symmetry operations to generate all atoms in the unit cell."""
        import re

        expanded_atoms = []
        seen_positions = set()
        tolerance = 0.01

        for atom in atoms:
            x, y, z = atom.get('x', 0), atom.get('y', 0), atom.get('z', 0)
            element = atom.get('element', 'X')
            occ = atom.get('occupancy', 1.0)
            b_iso = atom.get('b_iso', 0.01)

            for symop in symops:
                # Parse and apply symmetry operation
                new_x, new_y, new_z = self._apply_single_symop(x, y, z, symop)

                # Bring back to unit cell (0 to 1)
                new_x = new_x % 1.0
                new_y = new_y % 1.0
                new_z = new_z % 1.0

                # Handle negative zero
                if abs(new_x) < tolerance: new_x = 0.0
                if abs(new_y) < tolerance: new_y = 0.0
                if abs(new_z) < tolerance: new_z = 0.0
                if abs(new_x - 1.0) < tolerance: new_x = 0.0
                if abs(new_y - 1.0) < tolerance: new_y = 0.0
                if abs(new_z - 1.0) < tolerance: new_z = 0.0

                # Check if this position already exists (avoid duplicates)
                pos_key = (element, round(new_x, 2), round(new_y, 2), round(new_z, 2))
                if pos_key not in seen_positions:
                    seen_positions.add(pos_key)
                    expanded_atoms.append({
                        'element': element,
                        'x': new_x,
                        'y': new_y,
                        'z': new_z,
                        'occupancy': occ,
                        'b_iso': b_iso
                    })

        return expanded_atoms

    def _apply_single_symop(self, x: float, y: float, z: float, symop: str) -> tuple:
        """Apply a single symmetry operation string like 'x,y,z' or '-x+1/2,y,-z+1/2'."""
        parts = symop.replace(' ', '').split(',')
        if len(parts) != 3:
            return x, y, z

        results = []
        for part in parts:
            value = 0.0
            part = part.lower()

            # Parse each component
            i = 0
            sign = 1
            while i < len(part):
                c = part[i]

                if c == '+':
                    sign = 1
                    i += 1
                elif c == '-':
                    sign = -1
                    i += 1
                elif c == 'x':
                    value += sign * x
                    sign = 1
                    i += 1
                elif c == 'y':
                    value += sign * y
                    sign = 1
                    i += 1
                elif c == 'z':
                    value += sign * z
                    sign = 1
                    i += 1
                elif c.isdigit() or c == '/':
                    # Parse fraction like 1/2, 1/4, 3/4
                    j = i
                    while j < len(part) and (part[j].isdigit() or part[j] == '/'):
                        j += 1
                    frac_str = part[i:j]
                    if '/' in frac_str:
                        num, denom = frac_str.split('/')
                        frac_value = float(num) / float(denom)
                    else:
                        frac_value = float(frac_str)
                    value += sign * frac_value
                    sign = 1
                    i = j
                else:
                    i += 1

            results.append(value)

        return tuple(results)

    def _generate_supercell_atoms(self, atoms: List[Dict], nx: int, ny: int, nz: int) -> List[Dict]:
        """Generate supercell by replicating atoms."""
        supercell_atoms = []

        for atom in atoms:
            x, y, z = atom.get('x', 0), atom.get('y', 0), atom.get('z', 0)
            element = atom.get('element', 'X')
            occ = atom.get('occupancy', 1.0)
            b_iso = atom.get('b_iso', 0.01)

            for i in range(nx):
                for j in range(ny):
                    for k in range(nz):
                        supercell_atoms.append({
                            'element': element,
                            'x': (x + i) / nx,
                            'y': (y + j) / ny,
                            'z': (z + k) / nz,
                            'occupancy': occ,
                            'b_iso': b_iso
                        })

        return supercell_atoms

    def _calculate_cell_volume(self, cell: Dict) -> float:
        """Calculate unit cell volume from cell parameters."""
        import math
        a = cell.get('a', 10)
        b = cell.get('b', 10)
        c = cell.get('c', 10)
        alpha = math.radians(cell.get('alpha', 90))
        beta = math.radians(cell.get('beta', 90))
        gamma = math.radians(cell.get('gamma', 90))

        cos_alpha = math.cos(alpha)
        cos_beta = math.cos(beta)
        cos_gamma = math.cos(gamma)

        volume = a * b * c * math.sqrt(
            1 - cos_alpha**2 - cos_beta**2 - cos_gamma**2 +
            2 * cos_alpha * cos_beta * cos_gamma
        )
        return volume

    def _get_space_group_number(self, space_group: str) -> int:
        """Get International Tables number for common space groups."""
        sg_numbers = {
            'P 1': 1, 'P -1': 2, 'P 2': 3, 'P 21': 4, 'C 2': 5,
            'P m': 6, 'P c': 7, 'C m': 8, 'C c': 9, 'P 2/m': 10,
            'P 21/m': 11, 'C 2/m': 12, 'P 2/c': 13, 'P 21/c': 14, 'C 2/c': 15,
            'P 2 2 2': 16, 'P 2 2 21': 17, 'P 21 21 2': 18, 'P 21 21 21': 19,
            'C 2 2 21': 20, 'C 2 2 2': 21, 'F 2 2 2': 22, 'I 2 2 2': 23,
            'P m m 2': 25, 'P m c 21': 26, 'P c c 2': 27, 'P m a 2': 28,
            'P n a 21': 33, 'P n n a': 52, 'P b c a': 61, 'P n m a': 62,
            'C m c m': 63, 'C m c a': 64, 'C m m m': 65, 'C c c m': 66,
            'F m m m': 69, 'F d d d': 70, 'I m m m': 71, 'I b a m': 72,
            'P 4': 75, 'P 41': 76, 'P 42': 77, 'P 43': 78, 'I 4': 79,
            'I 41': 80, 'P -4': 81, 'I -4': 82, 'P 4/m': 83, 'P 42/m': 84,
            'P 4/n': 85, 'I 4/m': 87, 'I 41/a': 88,
            'P 4 2 2': 89, 'P 4 21 2': 90, 'P 41 2 2': 91, 'P 42 2 2': 93,
            'I 4 2 2': 97, 'I 41 2 2': 98,
            'P 4 m m': 99, 'P 4 b m': 100, 'P 42 c m': 101,
            'I 4 m m': 107, 'I 4 c m': 108, 'I 41 m d': 109, 'I 41 c d': 110,
            'P -4 2 m': 111, 'P -4 2 c': 112, 'P -4 21 m': 113, 'P -4 21 c': 114,
            'P -4 m 2': 115, 'P -4 c 2': 116, 'P -4 b 2': 117, 'P -4 n 2': 118,
            'I -4 m 2': 119, 'I -4 c 2': 120, 'I -4 2 m': 121, 'I -4 2 d': 122,
            'P 4/m m m': 123, 'P 4/m c c': 124, 'P 4/n b m': 125, 'P 4/n n c': 126,
            'I 4/m m m': 139, 'I 4/m c m': 140, 'I 41/a m d': 141, 'I 41/a c d': 142,
            'P 3': 143, 'P 31': 144, 'P 32': 145, 'R 3': 146,
            'P -3': 147, 'R -3': 148,
            'P 3 1 2': 149, 'P 3 2 1': 150, 'P 31 1 2': 151, 'P 31 2 1': 152,
            'P 32 1 2': 153, 'P 32 2 1': 154, 'R 3 2': 155,
            'P 3 m 1': 156, 'P 3 1 m': 157, 'P 3 c 1': 158, 'P 3 1 c': 159,
            'R 3 m': 160, 'R 3 c': 161,
            'P -3 1 m': 162, 'P -3 1 c': 163, 'P -3 m 1': 164, 'P -3 c 1': 165,
            'R -3 m': 166, 'R -3 c': 167,
            'P 6': 168, 'P 61': 169, 'P 65': 170, 'P 62': 171, 'P 64': 172, 'P 63': 173,
            'P -6': 174, 'P 6/m': 175, 'P 63/m': 176,
            'P 6 2 2': 177, 'P 61 2 2': 178, 'P 65 2 2': 179, 'P 62 2 2': 180,
            'P 64 2 2': 181, 'P 63 2 2': 182,
            'P 6 m m': 183, 'P 6 c c': 184, 'P 63 c m': 185, 'P 63 m c': 186,
            'P -6 m 2': 187, 'P -6 c 2': 188, 'P -6 2 m': 189, 'P -6 2 c': 190,
            'P 6/m m m': 191, 'P 6/m c c': 192, 'P 63/m c m': 193, 'P 63/m m c': 194,
            'P 2 3': 195, 'F 2 3': 196, 'I 2 3': 197, 'P 21 3': 198, 'I 21 3': 199,
            'P m -3': 200, 'P n -3': 201, 'F m -3': 202, 'F d -3': 203,
            'I m -3': 204, 'P a -3': 205, 'I a -3': 206,
            'P 4 3 2': 207, 'P 42 3 2': 208, 'F 4 3 2': 209, 'F 41 3 2': 210,
            'I 4 3 2': 211, 'P 43 3 2': 212, 'P 41 3 2': 213, 'I 41 3 2': 214,
            'P -4 3 m': 215, 'F -4 3 m': 216, 'I -4 3 m': 217, 'P -4 3 n': 218, 'F -4 3 c': 219, 'I -4 3 d': 220,
            'P m -3 m': 221, 'P n -3 n': 222, 'P m -3 n': 223, 'P n -3 m': 224,
            'F m -3 m': 225, 'F m -3 c': 226, 'F d -3 m': 227, 'F d -3 c': 228,
            'I m -3 m': 229, 'I a -3 d': 230
        }
        # Try to match space group
        sg_clean = space_group.strip()
        for sg, num in sg_numbers.items():
            if sg_clean == sg or sg_clean.replace(' ', '') == sg.replace(' ', ''):
                return num
        return 1  # Default to P 1

    def _get_symmetry_operations(self, space_group: str) -> List[str]:
        """Get symmetry operations for common space groups."""
        # Common space group symmetry operations for minerals
        symops = {
            'P 1': ['x,y,z'],
            'P -1': ['x,y,z', '-x,-y,-z'],
            'P 2/m': ['x,y,z', '-x,y,-z', '-x,-y,-z', 'x,-y,z'],
            'P 21/c': ['x,y,z', '-x,y+1/2,-z+1/2', '-x,-y,-z', 'x,-y+1/2,z+1/2'],
            'C 2/m': ['x,y,z', '-x,y,-z', '-x,-y,-z', 'x,-y,z', 'x+1/2,y+1/2,z', '-x+1/2,y+1/2,-z', '-x+1/2,-y+1/2,-z', 'x+1/2,-y+1/2,z'],
            'C 2/c': ['x,y,z', '-x,y,-z+1/2', '-x,-y,-z', 'x,-y,z+1/2', 'x+1/2,y+1/2,z', '-x+1/2,y+1/2,-z+1/2', '-x+1/2,-y+1/2,-z', 'x+1/2,-y+1/2,z+1/2'],
            'P n m a': ['x,y,z', '-x+1/2,-y,z+1/2', '-x,y+1/2,-z', 'x+1/2,-y+1/2,-z+1/2', '-x,-y,-z', 'x+1/2,y,-z+1/2', 'x,-y+1/2,z', '-x+1/2,y+1/2,z+1/2'],
            'P b c a': ['x,y,z', '-x+1/2,-y,z+1/2', '-x,y+1/2,-z+1/2', 'x+1/2,-y+1/2,-z', '-x,-y,-z', 'x+1/2,y,-z+1/2', 'x,-y+1/2,z+1/2', '-x+1/2,y+1/2,z'],
            # Trigonal - Quartz, etc.
            'P3_121': [
                'x,y,z', '-y,x-y,z+1/3', '-x+y,-x,z+2/3',
                'y,x,-z', 'x-y,-y,-z+2/3', '-x,-x+y,-z+1/3'
            ],
            'P3_221': [
                'x,y,z', '-y,x-y,z+2/3', '-x+y,-x,z+1/3',
                'y,x,-z', 'x-y,-y,-z+1/3', '-x,-x+y,-z+2/3'
            ],
            'P3_112': [
                'x,y,z', '-y,x-y,z+1/3', '-x+y,-x,z+2/3',
                '-y,-x,-z+2/3', 'x-y,-y,-z', '-x,-x+y,-z+1/3'
            ],
            'P3_212': [
                'x,y,z', '-y,x-y,z+2/3', '-x+y,-x,z+1/3',
                '-y,-x,-z+1/3', 'x-y,-y,-z', '-x,-x+y,-z+2/3'
            ],
            'R3': [
                'x,y,z', '-y,x-y,z', '-x+y,-x,z'
            ],
            'R-3': [
                'x,y,z', '-y,x-y,z', '-x+y,-x,z',
                '-x,-y,-z', 'y,-x+y,-z', 'x-y,x,-z'
            ],
            'R3m': [
                'x,y,z', '-y,x-y,z', '-x+y,-x,z',
                '-y,-x,z', 'x-y,-y,z', '-x,-x+y,z'
            ],
            'R-3m': [
                'x,y,z', '-y,x-y,z', '-x+y,-x,z', 'y,x,-z', 'x-y,-y,-z', '-x,-x+y,-z',
                '-x,-y,-z', 'y,-x+y,-z', 'x-y,x,-z', '-y,-x,z', '-x+y,y,z', 'x,x-y,z'
            ],
            # Hexagonal
            'P6_3': [
                'x,y,z', '-y,x-y,z', '-x+y,-x,z',
                '-x,-y,z+1/2', 'y,-x+y,z+1/2', 'x-y,x,z+1/2'
            ],
            'P6_3/m': [
                'x,y,z', '-y,x-y,z', '-x+y,-x,z', '-x,-y,z+1/2', 'y,-x+y,z+1/2', 'x-y,x,z+1/2',
                '-x,-y,-z', 'y,-x+y,-z', 'x-y,x,-z', 'x,y,-z+1/2', '-y,x-y,-z+1/2', '-x+y,-x,-z+1/2'
            ],
            'P 63/m m c': [
                'x,y,z', '-y,x-y,z', '-x+y,-x,z', '-x,-y,z+1/2', 'y,-x+y,z+1/2', 'x-y,x,z+1/2',
                'y,x,-z', 'x-y,-y,-z', '-x,-x+y,-z', '-y,-x,-z+1/2', '-x+y,y,-z+1/2', 'x,x-y,-z+1/2',
                '-x,-y,-z', 'y,-x+y,-z', 'x-y,x,-z', 'x,y,-z+1/2', '-y,x-y,-z+1/2', '-x+y,-x,-z+1/2',
                '-y,-x,z', '-x+y,y,z', 'x,x-y,z', 'y,x,z+1/2', 'x-y,-y,z+1/2', '-x,-x+y,z+1/2'
            ],
            # Cubic
            'F d -3 m': [
                'x,y,z', '-x,-y,z', '-x,y,-z', 'x,-y,-z',
                'z,x,y', 'z,-x,-y', '-z,-x,y', '-z,x,-y',
                'y,z,x', '-y,z,-x', 'y,-z,-x', '-y,-z,x',
                'y+1/4,x+1/4,z+1/4', '-y+1/4,-x+1/4,z+1/4', 'y+1/4,-x+1/4,-z+1/4', '-y+1/4,x+1/4,-z+1/4',
                'x+1/4,z+1/4,y+1/4', '-x+1/4,z+1/4,-y+1/4', '-x+1/4,-z+1/4,y+1/4', 'x+1/4,-z+1/4,-y+1/4',
                'z+1/4,y+1/4,x+1/4', 'z+1/4,-y+1/4,-x+1/4', '-z+1/4,y+1/4,-x+1/4', '-z+1/4,-y+1/4,x+1/4'
            ],
            'F m -3 m': [
                'x,y,z', '-x,-y,z', '-x,y,-z', 'x,-y,-z',
                'z,x,y', 'z,-x,-y', '-z,-x,y', '-z,x,-y',
                'y,z,x', '-y,z,-x', 'y,-z,-x', '-y,-z,x',
                'y,x,-z', '-y,-x,-z', 'y,-x,z', '-y,x,z',
                'x,z,-y', '-x,z,y', '-x,-z,-y', 'x,-z,y',
                'z,y,-x', 'z,-y,x', '-z,y,x', '-z,-y,-x',
                '-x,-y,-z', 'x,y,-z', 'x,-y,z', '-x,y,z',
                '-z,-x,-y', '-z,x,y', 'z,x,-y', 'z,-x,y',
                '-y,-z,-x', 'y,-z,x', '-y,z,x', 'y,z,-x',
                '-y,-x,z', 'y,x,z', '-y,x,-z', 'y,-x,-z',
                '-x,-z,y', 'x,-z,-y', 'x,z,y', '-x,z,-y',
                '-z,-y,x', '-z,y,-x', 'z,-y,-x', 'z,y,x'
            ],
            'Pm-3m': [
                'x,y,z', '-x,-y,z', '-x,y,-z', 'x,-y,-z',
                'z,x,y', 'z,-x,-y', '-z,-x,y', '-z,x,-y',
                'y,z,x', '-y,z,-x', 'y,-z,-x', '-y,-z,x',
                'y,x,-z', '-y,-x,-z', 'y,-x,z', '-y,x,z',
                'x,z,-y', '-x,z,y', '-x,-z,-y', 'x,-z,y',
                'z,y,-x', 'z,-y,x', '-z,y,x', '-z,-y,-x',
                '-x,-y,-z', 'x,y,-z', 'x,-y,z', '-x,y,z',
                '-z,-x,-y', '-z,x,y', 'z,x,-y', 'z,-x,y',
                '-y,-z,-x', 'y,-z,x', '-y,z,x', 'y,z,-x',
                '-y,-x,z', 'y,x,z', '-y,x,-z', 'y,-x,-z',
                '-x,-z,y', 'x,-z,-y', 'x,z,y', '-x,z,-y',
                '-z,-y,x', '-z,y,-x', 'z,-y,-x', 'z,y,x'
            ],
            'I 4/m m m': [
                'x,y,z', '-x,-y,z', '-y,x,z', 'y,-x,z', '-x,y,-z', 'x,-y,-z', 'y,x,-z', '-y,-x,-z',
                '-x,-y,-z', 'x,y,-z', 'y,-x,-z', '-y,x,-z', 'x,-y,z', '-x,y,z', '-y,-x,z', 'y,x,z'
            ],
            # Orthorhombic
            'Pmmm': [
                'x,y,z', '-x,-y,z', '-x,y,-z', 'x,-y,-z',
                '-x,-y,-z', 'x,y,-z', 'x,-y,z', '-x,y,z'
            ],
            'Cmcm': [
                'x,y,z', '-x,-y,z+1/2', '-x,y,-z+1/2', 'x,-y,-z',
                '-x,-y,-z', 'x,y,-z+1/2', 'x,-y,z+1/2', '-x,y,z',
                'x+1/2,y+1/2,z', '-x+1/2,-y+1/2,z+1/2', '-x+1/2,y+1/2,-z+1/2', 'x+1/2,-y+1/2,-z',
                '-x+1/2,-y+1/2,-z', 'x+1/2,y+1/2,-z+1/2', 'x+1/2,-y+1/2,z+1/2', '-x+1/2,y+1/2,z'
            ]
        }

        # Normalize space group name for comparison
        def normalize_sg(s):
            """Normalize space group name for comparison."""
            s = s.strip().upper()
            # Remove spaces and underscores, standardize notation
            s = s.replace(' ', '').replace('_', '').replace('-', '')
            return s

        sg_normalized = normalize_sg(space_group)

        # Try to find matching space group
        for sg, ops in symops.items():
            if normalize_sg(sg) == sg_normalized:
                return ops

        # Check for common variations
        sg_variations = {
            'P3221': 'P3_221', 'P3121': 'P3_121', 'P3212': 'P3_212', 'P3112': 'P3_112',
            'P63': 'P6_3', 'P63M': 'P6_3/m', 'P63MMC': 'P 63/m m c',
            'R3M': 'R3m', 'R3C': 'R-3m', 'FM3M': 'F m -3 m', 'FD3M': 'F d -3 m',
            'PM3M': 'Pm-3m', 'I4MMM': 'I 4/m m m'
        }

        if sg_normalized in sg_variations:
            target = sg_variations[sg_normalized]
            for sg, ops in symops.items():
                if normalize_sg(sg) == normalize_sg(target):
                    return ops

        # Default to identity operation only
        return ['x,y,z']

    def get_microprobe_data(self, mineral_name: str) -> Optional[Dict]:
        """Parse microprobe Excel file for a mineral and return structured data.

        Returns:
            Dict with keys: mineral_name, rruff_id, location, elements (list of dicts with
            element, measurements, average, stdev, unit)
        """
        mineral_data = self.get_mineral_data(mineral_name)
        if not mineral_data:
            return None

        chemistry_files = mineral_data.get('chemistry', [])
        if not chemistry_files:
            return None

        # Get first chemistry file
        chem_file = chemistry_files[0]
        file_path = chem_file.get('path')
        if not file_path or not os.path.exists(file_path):
            return None

        try:
            import xlrd
            wb = xlrd.open_workbook(file_path)
            sheet = wb.sheet_by_index(0)

            result = {
                'mineral_name': mineral_data.get('mineral_name', mineral_name),
                'rruff_id': chem_file.get('rruff_id', ''),
                'location': '',
                'elements': [],
                'file': os.path.basename(file_path)
            }

            # Parse header info (first few rows)
            for i in range(min(5, sheet.nrows)):
                row_text = ' '.join([str(c.value) for c in sheet.row(i)])
                if 'Location:' in row_text or 'Locality:' in row_text:
                    # Extract location
                    for cell in sheet.row(i):
                        val = str(cell.value).strip()
                        if val and 'Location' not in val and 'Locality' not in val:
                            result['location'] = val
                            break

            # Find the weight percent section and parse elements
            # Different formats exist:
            # 1. "Wt Percents" header row followed by data
            # 2. "Ox Wt Average Standard Dev" header (Dolomite format)
            # 3. Direct data starting with oxide names (CaO, MgO, etc.)

            in_weight_section = False
            found_cation_section = False

            for i in range(sheet.nrows):
                row = sheet.row(i)
                row_values = [str(c.value).strip() for c in row]
                row_text = ' '.join(row_values).lower()
                first_cell = row_values[0].lower() if row_values else ''

                # Check for weight percent header (various formats)
                if 'wt' in row_text and ('percent' in row_text or first_cell == 'ox'):
                    in_weight_section = True
                    continue

                # Check for cation section (end of weight percent)
                if 'cation' in row_text or ('atom' in row_text and 'weight' in row_text):
                    found_cation_section = True
                    break

                # Start weight section if we see common oxide names in first column
                if not in_weight_section and first_cell in ['cao', 'sio2', 'mgo', 'feo', 'fe2o3', 'al2o3', 'tio2', 'mno', 'na2o', 'k2o', 'pbo', 'zno', 's', 'pb', 'zn', 'fe', 'cu', 'ag']:
                    in_weight_section = True

                if in_weight_section and row_values[0]:
                    element = row_values[0]
                    # Skip header rows
                    if element.lower() in ['', 'oxide', 'element', '#1', '#2', 'ox', 'wt']:
                        continue

                    # Stop at totals row but include it separately
                    if element.lower() in ['totals', 'total', 'suma']:
                        # Parse total and add it
                        measurements = []
                        for val in row_values[1:]:
                            try:
                                num = float(val)
                                measurements.append(num)
                            except (ValueError, TypeError):
                                pass
                        if measurements:
                            result['elements'].append({
                                'element': 'Total',
                                'measurements': [],
                                'average': sum(measurements)/len(measurements),
                                'stdev': 0,
                                'unit': 'wt%'
                            })
                        continue

                    # Skip estimated values markers
                    if '*' in element and 'estimated' in row_text:
                        continue

                    # Parse measurements
                    measurements = []
                    average = None
                    stdev = None

                    for j, val in enumerate(row_values[1:], 1):
                        try:
                            num = float(val)
                            # Check if this is the average column (usually after measurements)
                            if j >= 17 and average is None:
                                average = num
                            elif j >= 18 and stdev is None:
                                stdev = num
                            elif j < 17:
                                measurements.append(num)
                        except (ValueError, TypeError):
                            pass

                    if measurements or average is not None:
                        result['elements'].append({
                            'element': element,
                            'measurements': measurements[:15],  # Limit to 15
                            'average': average or (sum(measurements)/len(measurements) if measurements else 0),
                            'stdev': stdev or 0,
                            'unit': 'wt%'
                        })

            return result if result['elements'] else None

        except Exception as e:
            logger.error(f"Error parsing microprobe file {file_path}: {e}")
            return None


# Singleton instance
_local_rruff_instance = None


def get_local_rruff_data() -> LocalRRUFFData:
    """Get singleton instance of LocalRRUFFData."""
    global _local_rruff_instance
    if _local_rruff_instance is None:
        _local_rruff_instance = LocalRRUFFData()
    return _local_rruff_instance


# Test
if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    rruff = get_local_rruff_data()
    print("\n=== RRUFF Data Statistics ===")
    stats = rruff.get_stats()
    for key, value in stats.items():
        print(f"  {key}: {value}")

    # Test mineral lookup
    print("\n=== Testing Actinolite ===")
    data = rruff.get_mineral_data('Actinolite')
    if data:
        print(f"  RRUFF IDs: {data['rruff_ids']}")
        print(f"  Powder files: {len(data['powder'])}")
        print(f"  Raman files: {len(data['raman'])}")
        print(f"  Images: {len(data['images'])}")

    # Test DIF parsing
    print("\n=== Testing DIF Data ===")
    dif = rruff.get_powder_dif_data('Actinolite')
    if dif:
        print(f"  Cell parameters: {dif['cell_parameters']}")
        print(f"  Space group: {dif['space_group']}")
        print(f"  Atoms: {len(dif['atoms'])}")
        print(f"  Diffraction peaks: {len(dif['diffraction_data'])}")
