"""Shared route implementations for mineral science API views."""

import logging
import os
import re
from pathlib import Path

from flask import current_app, jsonify, request, send_from_directory

logger = logging.getLogger(__name__)


def format_chemical_formula(formula):
    """Convert formula markup to Unicode subscript/superscript characters."""
    if not formula:
        return ''

    subscript_map = {
        '0': '₀', '1': '₁', '2': '₂', '3': '₃', '4': '₄',
        '5': '₅', '6': '₆', '7': '₇', '8': '₈', '9': '₉',
        'a': 'ₐ', 'e': 'ₑ', 'h': 'ₕ', 'i': 'ᵢ', 'j': 'ⱼ',
        'k': 'ₖ', 'l': 'ₗ', 'm': 'ₘ', 'n': 'ₙ', 'o': 'ₒ',
        'p': 'ₚ', 'r': 'ᵣ', 's': 'ₛ', 't': 'ₜ', 'u': 'ᵤ',
        'v': 'ᵥ', 'x': 'ₓ',
    }
    superscript_map = {
        '0': '⁰', '1': '¹', '2': '²', '3': '³', '4': '⁴',
        '5': '⁵', '6': '⁶', '7': '⁷', '8': '⁸', '9': '⁹',
        '+': '⁺', '-': '⁻', '=': '⁼', '(': '⁽', ')': '⁾',
        'n': 'ⁿ', 'i': 'ⁱ',
    }

    def replace_subscript(match):
        return ''.join(subscript_map.get(char, char) for char in match.group(1))

    def replace_superscript(match):
        return ''.join(superscript_map.get(char, char) for char in match.group(1))

    formatted = re.sub(r'_([^_]+)_', replace_subscript, formula)
    return re.sub(r'\^([^^]+)\^', replace_superscript, formatted)


def api_get_rruff_data(mineral_name):
    """Get RRUFF scientific data for one or more mineral names."""
    try:
        from mineral_database_pg import get_mineral_database
        from mineral_translator import get_all_translations

        mineral_db = get_mineral_database()
        translations = get_all_translations(mineral_name)

        results = []
        seen_rruff_ids = set()

        for trans in translations:
            english_name = trans['english']
            original_name = trans['original']
            rruff_data = mineral_db.get_rruff_data_for_mineral(english_name)

            if rruff_data:
                rruff_id = rruff_data.get('rruff_id', '')
                if rruff_id and rruff_id in seen_rruff_ids:
                    continue
                seen_rruff_ids.add(rruff_id)

                raw_formula = rruff_data.get('formula_concise') or rruff_data.get('formula_rruff', '')
                results.append(
                    {
                        'original_name': original_name,
                        'english_name': english_name,
                        'found': True,
                        'source': 'RRUFF',
                        'data': {
                            'name': rruff_data.get('name', ''),
                            'rruff_id': rruff_id,
                            'formula': format_chemical_formula(raw_formula),
                            'crystal_system': rruff_data.get('crystal_system', ''),
                            'space_group': rruff_data.get('space_group', ''),
                            'chemistry_elements': rruff_data.get('chemistry_elements', ''),
                            'ima_status': rruff_data.get('ima_status', ''),
                            'ima_number': rruff_data.get('ima_number', ''),
                            'year_first_published': rruff_data.get('year_first_published', ''),
                            'country_type_locality': rruff_data.get('country_type_locality', ''),
                            'structural_groupname': rruff_data.get('structural_groupname', ''),
                            'fleischers_groupname': rruff_data.get('fleischers_groupname', ''),
                            'crystal_morphology': rruff_data.get('crystal_morphology', ''),
                            'oldest_known_age_ma': rruff_data.get('oldest_known_age_ma', ''),
                            'paragenetic_modes': rruff_data.get('paragenetic_modes', ''),
                        },
                    }
                )
                continue

            try:
                from online_mineral_data import (
                    format_online_data_for_display,
                    get_online_mineral_data,
                )

                online_data = get_online_mineral_data(english_name)
                if online_data:
                    formatted = format_online_data_for_display(online_data)
                    online_id = formatted.get('rruff_id', f'WIKI-{english_name[:10].upper()}')
                    if online_id not in seen_rruff_ids:
                        seen_rruff_ids.add(online_id)
                        results.append(
                            {
                                'original_name': original_name,
                                'english_name': english_name,
                                'found': True,
                                'source': 'Wikipedia',
                                'data': {
                                    'name': formatted.get('name', english_name),
                                    'rruff_id': online_id,
                                    'formula': format_chemical_formula(formatted.get('formula', '')),
                                    'crystal_system': formatted.get('crystal_system', ''),
                                    'space_group': formatted.get('space_group', ''),
                                    'chemistry_elements': formatted.get('chemistry_elements', ''),
                                    'ima_status': formatted.get('ima_status', 'Wikipedia'),
                                    'ima_number': formatted.get('ima_number', ''),
                                    'year_first_published': formatted.get('year_first_published', ''),
                                    'country_type_locality': formatted.get('country_type_locality', ''),
                                    'structural_groupname': formatted.get('structural_groupname', ''),
                                    'fleischers_groupname': formatted.get('fleischers_groupname', ''),
                                    'crystal_morphology': formatted.get('crystal_morphology', ''),
                                    'oldest_known_age_ma': '',
                                    'paragenetic_modes': '',
                                    'mohs_hardness': formatted.get('mohs_hardness', ''),
                                    'specific_gravity': formatted.get('specific_gravity', ''),
                                    'color': formatted.get('color', ''),
                                    'luster': formatted.get('luster', ''),
                                    'description': formatted.get('description', ''),
                                    'source_url': formatted.get('source_url', ''),
                                },
                            }
                        )
                        continue
                results.append(
                    {
                        'original_name': original_name,
                        'english_name': english_name,
                        'found': False,
                        'source': None,
                        'data': None,
                    }
                )
            except Exception as online_err:
                logger.warning("Online mineral lookup failed for %s: %s", english_name, online_err)
                results.append(
                    {
                        'original_name': original_name,
                        'english_name': english_name,
                        'found': False,
                        'source': None,
                        'data': None,
                    }
                )

        if results:
            return jsonify(
                {
                    'success': True,
                    'minerals': results,
                    'total_found': sum(1 for result in results if result['found']),
                    'total_parsed': len(results),
                }
            )
        return jsonify({'success': False, 'message': 'Could not parse mineral name'})
    except Exception as exc:
        logger.error("Error fetching RRUFF data for %s: %s", mineral_name, exc)
        return jsonify({'success': False, 'message': str(exc)}), 500


def api_cod_search(mineral_name):
    """Search crystal databases by mineral name."""
    try:
        from cod_database import get_cod_database
        from mineral_translator import get_all_translations

        cod_db = get_cod_database()
        translations = get_all_translations(mineral_name)
        all_results = []
        minerals_searched = []
        seen_entries = set()

        for trans in translations:
            english_name = trans['english']
            original_name = trans['original']
            minerals_searched.append(
                {
                    'original': original_name,
                    'english': english_name,
                    'was_translated': trans['was_translated'],
                }
            )

            results = cod_db.search_mineral(english_name, limit=5)
            for result in results:
                entry_key = (
                    f"{result.get('database', 'unknown')}:"
                    f"{result.get('entry_id', result.get('cod_id', ''))}"
                )
                if entry_key in seen_entries:
                    continue
                seen_entries.add(entry_key)
                result['searched_mineral'] = english_name
                result['original_name'] = original_name
                if result.get('database') == 'COD' and not result.get('cod_id'):
                    result['cod_id'] = result.get('entry_id')
                all_results.append(result)

        if all_results:
            databases_found = {}
            for result in all_results:
                database = result.get('database', 'Unknown')
                databases_found[database] = databases_found.get(database, 0) + 1
            return jsonify(
                {
                    'success': True,
                    'mineral_name': mineral_name,
                    'minerals_searched': minerals_searched,
                    'databases_searched': ['COD', 'AMCSD', 'RRUFF', 'Mindat'],
                    'databases_found': databases_found,
                    'results': all_results,
                    'total': len(all_results),
                }
            )

        return jsonify(
            {
                'success': False,
                'message': f'No crystal structures found for: {", ".join([m["english"] for m in minerals_searched])}',
                'mineral_name': mineral_name,
                'minerals_searched': minerals_searched,
                'databases_searched': ['COD', 'AMCSD', 'RRUFF', 'Mindat'],
            }
        )
    except Exception as exc:
        logger.error("Error searching COD for %s: %s", mineral_name, exc)
        return jsonify({'success': False, 'message': str(exc)}), 500


def api_cod_get_cif(entry_id):
    """Get CIF content for a database entry."""
    try:
        from cod_database import get_cod_database

        crystal_db = get_cod_database()
        database = request.args.get('database', 'COD').upper()
        cif_content = crystal_db.get_cif_by_id(database, entry_id)

        if not cif_content and database == 'COD':
            cif_content = crystal_db.get_cif_data(f"https://www.crystallography.net/cod/{entry_id}.cif")

        if cif_content:
            return jsonify(
                {
                    'success': True,
                    'database': database,
                    'entry_id': entry_id,
                    'cod_id': entry_id if database == 'COD' else None,
                    'cif_content': cif_content,
                }
            )
        return jsonify(
            {
                'success': False,
                'message': f'CIF file not found for {database} ID {entry_id}',
            }
        ), 404
    except Exception as exc:
        logger.error("Error fetching CIF for %s: %s", entry_id, exc)
        return jsonify({'success': False, 'message': str(exc)}), 500


def api_crystal_get_cif_by_url():
    """Get CIF content by direct URL."""
    try:
        from cod_database import get_cod_database

        cif_url = request.args.get('url')
        if not cif_url:
            return jsonify({'success': False, 'message': 'URL parameter required'}), 400

        cif_content = get_cod_database().get_cif_data(cif_url)
        if cif_content:
            return jsonify({'success': True, 'url': cif_url, 'cif_content': cif_content})
        return jsonify({'success': False, 'message': f'CIF file not found at {cif_url}'}), 404
    except Exception as exc:
        logger.error("Error fetching CIF from URL: %s", exc)
        return jsonify({'success': False, 'message': str(exc)}), 500


def api_crystal_get_local_cif(entry_id):
    """Get CIF from local storage or on-demand fetch."""
    try:
        from cod_database import get_cod_database

        if entry_id.startswith('R') and entry_id[1:].isdigit():
            database = 'RRUFF'
            cif_dir = Path(current_app.root_path) / 'data' / 'cif_files'
        else:
            database = 'COD'
            cif_dir = Path(current_app.root_path) / 'data' / 'cif_files' / 'cod'

        cif_path = cif_dir / f"{entry_id}.cif"
        if cif_path.exists():
            return jsonify(
                {
                    'success': True,
                    'entry_id': entry_id,
                    'database': database,
                    'source': 'local',
                    'cif_content': cif_path.read_text(encoding='utf-8'),
                }
            )

        cif_content = get_cod_database().get_cif_by_id(database, entry_id)
        if cif_content:
            return jsonify(
                {
                    'success': True,
                    'entry_id': entry_id,
                    'database': database,
                    'source': 'fetched',
                    'cif_content': cif_content,
                }
            )
        return jsonify({'success': False, 'message': f'CIF file not found for {entry_id}'}), 404
    except Exception as exc:
        logger.error("Error fetching CIF for %s: %s", entry_id, exc)
        return jsonify({'success': False, 'message': str(exc)}), 500


def api_cod_get_structure(mineral_name):
    """Get crystal structure data for a mineral."""
    try:
        from cod_database import get_cod_database
        from mineral_translator import get_all_translations

        cod_db = get_cod_database()
        structures = []
        for trans in get_all_translations(mineral_name):
            english_name = trans['english']
            structure = cod_db.get_mineral_structure(english_name)
            if structure:
                structure['original_name'] = trans['original']
                structure['english_name'] = english_name
                structures.append(structure)

        if structures:
            return jsonify(
                {
                    'success': True,
                    'mineral_name': mineral_name,
                    'structures': structures,
                    'total': len(structures),
                }
            )

        english_names = [translation['english'] for translation in get_all_translations(mineral_name)]
        return jsonify(
            {
                'success': False,
                'message': f'No crystal structure found for: {", ".join(english_names)}',
                'mineral_name': mineral_name,
                'minerals_searched': english_names,
            }
        )
    except Exception as exc:
        logger.error("Error fetching crystal structure for %s: %s", mineral_name, exc)
        return jsonify({'success': False, 'message': str(exc)}), 500


def api_get_geochemical_data(mineral_name):
    """Get geochemical data for a mineral."""
    try:
        from earthchem_georoc_api import get_geochemical_data as fetch_geochemical_data
        from earthchem_georoc_api import format_geochemical_data_for_display
        from mineral_translator import get_all_translations

        all_results = []
        seen_sources = set()

        for trans in get_all_translations(mineral_name):
            english_name = trans['english']
            original_name = trans['original']
            geo_data = fetch_geochemical_data(english_name)

            if geo_data and geo_data.get('total_samples', 0) > 0:
                formatted = format_geochemical_data_for_display(geo_data)
                source_key = f"{english_name}_{formatted['source']}"
                if source_key in seen_sources:
                    continue
                seen_sources.add(source_key)
                all_results.append(
                    {
                        'original_name': original_name,
                        'english_name': english_name,
                        'found': True,
                        'data': formatted,
                    }
                )
            else:
                all_results.append(
                    {
                        'original_name': original_name,
                        'english_name': english_name,
                        'found': False,
                        'data': None,
                    }
                )

        if all_results:
            return jsonify(
                {
                    'success': True,
                    'minerals': all_results,
                    'total_found': sum(1 for result in all_results if result['found']),
                    'total_parsed': len(all_results),
                }
            )
        return jsonify({'success': False, 'message': 'No geochemical data found'})
    except Exception as exc:
        logger.error("Error fetching geochemical data for %s: %s", mineral_name, exc)
        return jsonify({'success': False, 'message': str(exc)}), 500


def api_get_local_rruff_data(mineral_name):
    """Get local RRUFF data for a mineral."""
    try:
        from local_rruff_data import LocalRRUFFData
        from mineral_translator import get_all_translations

        rruff = LocalRRUFFData()
        all_results = []
        seen_minerals = set()

        for trans in get_all_translations(mineral_name):
            english_name = trans['english']
            original_name = trans['original']
            if english_name.lower() in seen_minerals:
                continue
            seen_minerals.add(english_name.lower())

            mineral_data = rruff.get_mineral_data(english_name)
            all_results.append(
                {
                    'original_name': original_name,
                    'english_name': english_name,
                    'found': bool(mineral_data),
                    'data': mineral_data,
                }
            )

        if all_results:
            return jsonify(
                {
                    'success': True,
                    'minerals': all_results,
                    'total_found': sum(1 for result in all_results if result['found']),
                    'total_parsed': len(all_results),
                }
            )
        return jsonify({'success': False, 'message': 'No local RRUFF data found'})
    except Exception as exc:
        logger.error("Error fetching local RRUFF data for %s: %s", mineral_name, exc)
        return jsonify({'success': False, 'message': str(exc)}), 500


def api_get_local_rruff_dif(mineral_name):
    """Get local RRUFF DIF data."""
    try:
        from local_rruff_data import LocalRRUFFData
        from mineral_translator import get_all_translations

        rruff = LocalRRUFFData()
        for trans in get_all_translations(mineral_name):
            english_name = trans['english']
            dif_data = rruff.get_powder_dif_data(english_name)
            if dif_data:
                return jsonify(
                    {
                        'success': True,
                        'mineral_name': english_name,
                        'original_name': trans['original'],
                        'data': dif_data,
                    }
                )

        return jsonify({'success': False, 'message': f'No DIF data found for {mineral_name}'})
    except Exception as exc:
        logger.error("Error fetching DIF data for %s: %s", mineral_name, exc)
        return jsonify({'success': False, 'message': str(exc)}), 500


def api_get_local_rruff_cif(mineral_name):
    """Generate CIF from local RRUFF DIF data."""
    try:
        from local_rruff_data import LocalRRUFFData
        from mineral_translator import get_all_translations

        view_mode = request.args.get('view_mode', 'asymmetric')
        rruff = LocalRRUFFData()

        for trans in get_all_translations(mineral_name):
            english_name = trans['english']
            if view_mode == 'unitcell':
                cif_content = rruff.generate_cif_from_dif(english_name, expand_unitcell=True)
            elif view_mode == 'supercell':
                cif_content = rruff.generate_cif_from_dif(
                    english_name,
                    expand_unitcell=True,
                    supercell=(2, 2, 2),
                )
            else:
                cif_content = rruff.generate_cif_from_dif(english_name)

            if cif_content:
                return jsonify(
                    {
                        'success': True,
                        'mineral_name': english_name,
                        'original_name': trans['original'],
                        'view_mode': view_mode,
                        'cif_content': cif_content,
                    }
                )

        return jsonify(
            {
                'success': False,
                'message': f'No DIF data available to generate CIF for {mineral_name}',
            }
        )
    except Exception as exc:
        logger.error("Error generating CIF for %s: %s", mineral_name, exc)
        return jsonify({'success': False, 'message': str(exc)}), 500


def api_get_local_rruff_spectrum(spectrum_type, mineral_name):
    """Get Raman or infrared spectrum data."""
    try:
        from local_rruff_data import LocalRRUFFData
        from mineral_translator import get_all_translations

        if spectrum_type not in ['raman', 'infrared']:
            return jsonify(
                {
                    'success': False,
                    'message': 'Invalid spectrum type. Use "raman" or "infrared"',
                }
            ), 400

        rruff = LocalRRUFFData()
        for trans in get_all_translations(mineral_name):
            english_name = trans['english']
            spectrum_data = (
                rruff.get_raman_data(english_name)
                if spectrum_type == 'raman'
                else rruff.get_infrared_data(english_name)
            )
            if spectrum_data:
                return jsonify(
                    {
                        'success': True,
                        'mineral_name': english_name,
                        'original_name': trans['original'],
                        'spectrum_type': spectrum_type,
                        'data': spectrum_data,
                    }
                )

        return jsonify(
            {
                'success': False,
                'message': f'No {spectrum_type} data found for {mineral_name}',
            }
        )
    except Exception as exc:
        logger.error("Error fetching %s data for %s: %s", spectrum_type, mineral_name, exc)
        return jsonify({'success': False, 'message': str(exc)}), 500


def api_get_local_rruff_powder_xy(mineral_name):
    """Get local RRUFF powder XY data."""
    try:
        from local_rruff_data import LocalRRUFFData
        from mineral_translator import get_all_translations

        rruff = LocalRRUFFData()
        for trans in get_all_translations(mineral_name):
            english_name = trans['english']
            xy_data = rruff.get_powder_xy_data(english_name)
            if xy_data:
                return jsonify(
                    {
                        'success': True,
                        'mineral_name': english_name,
                        'original_name': trans['original'],
                        'data': xy_data,
                    }
                )

        return jsonify({'success': False, 'message': f'No powder XY data found for {mineral_name}'})
    except Exception as exc:
        logger.error("Error fetching powder XY data for %s: %s", mineral_name, exc)
        return jsonify({'success': False, 'message': str(exc)}), 500


def api_serve_local_rruff_image(image_path):
    """Serve a local RRUFF image file."""
    try:
        rruff_data_path = os.path.join(current_app.root_path, 'RRUFF_data')
        full_path = os.path.normpath(os.path.join(rruff_data_path, image_path))
        if not full_path.startswith(os.path.normpath(rruff_data_path)):
            return jsonify({'success': False, 'message': 'Invalid path'}), 403
        return send_from_directory(os.path.dirname(full_path), os.path.basename(full_path))
    except Exception as exc:
        logger.error("Error serving RRUFF image %s: %s", image_path, exc)
        return jsonify({'success': False, 'message': str(exc)}), 500


def api_get_local_rruff_microprobe(mineral_name):
    """Get local RRUFF microprobe data."""
    try:
        from local_rruff_data import get_local_rruff_data
        from mineral_translator import translate_mineral_name

        rruff = get_local_rruff_data()
        english_name, _ = translate_mineral_name(mineral_name)
        if not english_name:
            english_name = mineral_name

        microprobe = rruff.get_microprobe_data(english_name)
        if not microprobe:
            return jsonify(
                {
                    'success': False,
                    'message': f'No microprobe data found for {mineral_name}',
                }
            ), 404
        return jsonify({'success': True, 'data': microprobe})
    except Exception as exc:
        logger.error("Error getting microprobe data for %s: %s", mineral_name, exc)
        return jsonify({'success': False, 'message': str(exc)}), 500
