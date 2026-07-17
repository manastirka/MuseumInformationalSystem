"""Shared route implementations for collection, mineral, and inventory admin views."""

import logging
import json
import os
import tempfile
import time
from datetime import datetime
from pathlib import Path

from flask import current_app, flash, redirect, render_template, request, session, url_for
from core_app_views import current_ui_language
from werkzeug.utils import secure_filename
from collection_registry import get_collection_form_info, get_collection_route_map

logger = logging.getLogger(__name__)

_MINERAL_DEFAULT_COLUMNS = ['inventarni_broj', 'naziv', 'predmet', 'lokalitet', 'gde_se_nalazi']
_MINERAL_COLUMNS_EN = {
    'inventarni_broj': 'Inv. No.',
    'naziv': 'Name',
    'predmet': 'Item',
    'lokalitet': 'Locality',
    'gde_se_nalazi': 'Storage location',
    'nacin_nabavljanja': 'Acquisition method',
    'datum_nabavljanja': 'Acquisition date',
    'legator': 'Donor/Found by',
    'identifikovao': 'Identified by',
    'kolicina': 'Quantity',
    'datum_unosa': 'Entry date',
}
_MINERAL_COLUMNS_SR = {
    'inventarni_broj': 'Инв. број',
    'naziv': 'Назив',
    'predmet': 'Предмет',
    'lokalitet': 'Локалитет',
    'gde_se_nalazi': 'Где се налази',
    'nacin_nabavljanja': 'Начин набављања',
    'datum_nabavljanja': 'Датум набављања',
    'legator': 'Легатор/Нашао',
    'identifikovao': 'Идентификовао',
    'kolicina': 'Количина',
    'datum_unosa': 'Датум уноса',
}
_COLLECTION_ROUTES = {
    **get_collection_route_map(),
    'conservation': 'conservation_biology',
}
_COLLECTION_FORM_INFO = {
    **get_collection_form_info(),
    'general_zoology': {'name': 'Општа зоологија', 'route': 'general_zoology_collection'},
    'conservation': {'name': 'Конзервација биолошких збирки', 'route': 'conservation_biology'},
    'conservation_biology': {'name': 'Конзервациона биологија', 'route': 'conservation_biology_collection'},
    'geology_conservation': {'name': 'Геолошка конзервација', 'route': 'geology_conservation_collection'},
}

_CURATOR_DISPLAY_NAMES = {
    'mniketic@nhmbeo.rs': 'Марјан Никетић',
    'verica.stojanovic@nhmbeo.rs': 'Верица Стојановић',
    'aleksandra.savic@nhmbeo.rs': 'Александра Савић',
    'marko.nestorovic@nhmbeo.rs': 'Марко Несторовић',
    'dubravka.vucic@nhmbeo.rs': 'Дубравка Вучић',
    'milos.jovic@nhmbeo.rs': 'Милош Јовић',
    'aleksandar@nhmbeo.rs': 'Александар Стојановић',
    'boris@nhmbeo.rs': 'Борис Иванчевић',
    'ana.paunovic@nhmbeo.rs': 'Ана Пауновић',
    'vuk.popic@nhmbeo.rs': 'Вук Попић',
    'zorana.markovic@nhmbeo.rs': 'Зорана Марковић',
    'gorana.petkovski@nhmbeo.rs': 'Горана Петковски',
    'milos.mrvaljevic@nhmbeo.rs': 'Милош Мрваљевић',
    'jovan.kokotovic@nhmbeo.rs': 'Јован Кокотовић',
    'biljana.mitrovic@nhmbeo.rs': 'Биљана Митровић',
    'zoran.markovic@nhmbeo.rs': 'Зоран Марковић',
    'sanja.pavic@nhmbeo.rs': 'Сања Алабурић',
    'dragana.djuric@nhmbeo.rs': 'Драгана Ђурић',
    'pejovic.ranko@nhmbeo.rs': 'Ранко Пејовић',
    'milos.milivojevic@nhmbeo.rs': 'Милош Миливојевић',
    'desadjm@nhmbeo.rs': 'Деса Ђорђевић-Милутиновић',
    'tatjana.milicbabic@nhmbeo.rs': 'Татјана Милић Бабић',
    'aca.lukovic@nhmbeo.rs': 'Александар Луковић',
    'branko.radulovic@nhmbeo.rs': 'Бранко Радуловић',
    'nenad.mladenovic@nhmbeo.rs': 'Ненад Младеновић',
}

_COLLECTION_CURATORS = {
    'botany': ['mniketic@nhmbeo.rs', 'verica.stojanovic@nhmbeo.rs', 'aleksandra.savic@nhmbeo.rs', 'marko.nestorovic@nhmbeo.rs'],
    'ichthyology': ['dubravka.vucic@nhmbeo.rs'],
    'entomology': ['milos.jovic@nhmbeo.rs', 'aleksandar@nhmbeo.rs'],
    'mycology': ['boris@nhmbeo.rs'],
    'herpetology': ['ana.paunovic@nhmbeo.rs'],
    'ornithology': ['vuk.popic@nhmbeo.rs'],
    'paleozoology': ['biljana.mitrovic@nhmbeo.rs', 'zoran.markovic@nhmbeo.rs', 'sanja.pavic@nhmbeo.rs', 'dragana.djuric@nhmbeo.rs', 'pejovic.ranko@nhmbeo.rs', 'milos.milivojevic@nhmbeo.rs'],
    'paleobotany': ['desadjm@nhmbeo.rs'],
    'petrology': ['tatjana.milicbabic@nhmbeo.rs'],
    'meteorite': ['aca.lukovic@nhmbeo.rs'],
    'conservation': ['gorana.petkovski@nhmbeo.rs', 'milos.mrvaljevic@nhmbeo.rs', 'jovan.kokotovic@nhmbeo.rs'],
}

_SANJA_DATABASE_PATH = Path('Sanja/sanja_paleogene_neogene_mammals.json')
_SANJA_COLLECTION_GROUP = 'Крупни сисари - палеоген/неоген'
_SANJA_TEXT_FIELDS = (
    'collection_number',
    'collector_number',
    'catalog_number',
    'specimen_name',
    'taxon_name',
    'level',
    'acquisition_method',
    'acquisition_date',
    'database_entry_date',
    'entered_by',
    'donor_collector',
    'identified_by',
    'comment',
    'description',
    'location_found',
    'country',
    'locality_text',
    'exposure',
    'specimen_part_2',
    'specimen_part_3',
    'specimen_part_4',
    'specimen_part_5',
    'storage_location',
    'material',
    'uncertain_determination',
    'biostratigraphic_zone',
    'bibliography_flag',
)
_SANJA_NUMBER_FIELDS = (
    'inventory_sequence',
    'quantity',
    'utm_x',
    'utm_y',
    'utm_z',
    'length_mm',
    'width_mm',
)


def _coerce_sanja_number(value):
    value = (value or '').strip()
    if value == '':
        return ''
    try:
        parsed = float(value)
    except ValueError:
        return value
    if parsed.is_integer():
        return int(parsed)
    return parsed


def _curator_display_value(email_or_name):
    value = str(email_or_name or '').strip()
    return _CURATOR_DISPLAY_NAMES.get(value.lower(), value)


def _collection_curator_display(collection_type):
    curators = _COLLECTION_CURATORS.get(collection_type, [])
    return ', '.join(_curator_display_value(curator) for curator in curators if curator)


def normalize_collection_curators_for_display(collection_type, records):
    """Replace placeholder curator emails with authoritative display names."""
    official_curators = set(_COLLECTION_CURATORS.get(collection_type, []))
    official_display = _collection_curator_display(collection_type)
    normalized = []

    for record in records or []:
        item = dict(record)
        if 'curator' in item:
            curator = str(item.get('curator') or '').strip().lower()
            if curator in official_curators:
                item['curator'] = _curator_display_value(curator)
            elif official_display:
                item['curator'] = official_display
            else:
                item['curator'] = _curator_display_value(curator)
        normalized.append(item)

    return normalized


def _build_sanja_statistics(records):
    localities = sorted({record.get('location_found') for record in records if record.get('location_found')})
    taxa = sorted({record.get('specimen_name') for record in records if record.get('specimen_name')})
    identified_by = sorted({record.get('identified_by') for record in records if record.get('identified_by')})

    return {
        'total_specimens': len(records),
        'total_taxa': len(taxa),
        'total_localities': len(localities),
        'identified_by_count': len(identified_by),
    }


def _sanja_pg():
    """Return the phase3a_databases module when PostgreSQL is configured AND the
    Sanja table exists, else None (so the JSON fallback is used). phase3a_databases
    raises at import without DATABASE_URL, so the import is guarded."""
    if not os.environ.get('DATABASE_URL'):
        return None
    try:
        import phase3a_databases
        if phase3a_databases.sanja_table_exists():
            return phase3a_databases
    except Exception as exc:
        logger.warning("Sanja PostgreSQL backend unavailable, using JSON: %s", exc)
    return None


def _sanja_empty_payload():
    return {
        'metadata': {
            'name': 'Крупни сисари палеогена и неогена',
            'source_file': 'Sanja/sanja BAZA KRUPNI SISAri paleogen neogen.xls',
        },
        'specimens': [],
        'statistics': {},
    }


def _load_sanja_database_payload():
    # Postgres-preferred: the table is the source of truth once it exists.
    pg = _sanja_pg()
    if pg is not None:
        specimens = pg.get_sanja_specimens()
        payload = _sanja_empty_payload()
        payload['specimens'] = specimens
        payload['statistics'] = _build_sanja_statistics(specimens)
        return payload

    # JSON fallback (development / pre-migration).
    try:
        return json.loads(_SANJA_DATABASE_PATH.read_text(encoding='utf-8'))
    except FileNotFoundError:
        # No database yet: legitimately start from an empty payload.
        return _sanja_empty_payload()
    except (OSError, json.JSONDecodeError) as exc:
        # A transient read failure or a corrupt/partial file must NOT be treated
        # as an empty database — saving on top of that would wipe every record.
        logger.error("Could not load Sanja database from %s: %s", _SANJA_DATABASE_PATH, exc)
        raise


def _save_sanja_database_payload(payload):
    payload['statistics'] = _build_sanja_statistics(payload.get('specimens', []))
    payload.setdefault('metadata', {})['updated_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    pg = _sanja_pg()
    if pg is not None:
        # Atomic upsert+prune inside one transaction; PostgreSQL is the store.
        pg.replace_sanja_specimens(payload.get('specimens', []))
    else:
        from runtime_lock_utils import write_json_file
        # Write atomically (temp file + fsync + os.replace under an exclusive lock)
        # so a crash, full disk, or concurrent writer can never truncate the live
        # database into a corrupt/partial file.
        write_json_file(_SANJA_DATABASE_PATH, payload, indent=2)

    try:
        import app as museum_app
        museum_app.SANJA_PALEOGENE_NEOGENE_MAMMALS_DATABASE = payload
    except Exception as exc:
        logger.warning("Could not refresh Sanja database cache after save: %s", exc)


def _find_sanja_record(records, record_id):
    target = str(record_id)
    for record in records:
        if str(record.get('id')) == target:
            return record
    return None


def _apply_sanja_form_data(item_data):
    for field in _SANJA_TEXT_FIELDS:
        item_data[field] = request.form.get(field, '').strip()
    for field in _SANJA_NUMBER_FIELDS:
        item_data[field] = _coerce_sanja_number(request.form.get(field, ''))
    return item_data


def _handle_sanja_paleogene_neogene_mammal_form(collection_info, record_id=None):
    is_edit = record_id is not None
    try:
        payload = _load_sanja_database_payload()
    except (OSError, json.JSONDecodeError):
        # Refuse to proceed on a failed/corrupt read: saving on top of an empty
        # fallback would silently wipe every existing record.
        flash(
            'База крупних сисара палеогена и неогена тренутно није доступна, па '
            'измена није сачувана. Обратите се администратору.',
            'danger',
        )
        return redirect(url_for(collection_info['route']))
    records = payload.setdefault('specimens', [])
    item_data = _find_sanja_record(records, record_id) if is_edit else None

    if is_edit and item_data is None:
        flash('Примерак није пронађен.', 'danger')
        return redirect(url_for(collection_info['route']))

    if request.method == 'POST':
        if not is_edit:
            next_id = max((int(record.get('id') or 0) for record in records), default=0) + 1
            next_source_row = max((int(record.get('source_row') or 1) for record in records), default=1) + 1
            item_data = {
                'id': next_id,
                'source_row': next_source_row,
                'collection_group': _SANJA_COLLECTION_GROUP,
            }
            records.append(item_data)

        _apply_sanja_form_data(item_data)
        _save_sanja_database_payload(payload)

        flash_message = (
            'Примерак је успешно ажуриран.'
            if is_edit
            else 'Предмет је успешно додат у базу крупних сисара палеогена и неогена!'
        )
        flash(flash_message, 'success')
        return redirect(url_for(collection_info['route']))

    return render_template(
        'admin_add_sanja_paleogene_neogene_mammal.html',
        collection_type='sanja_paleogene_neogene_mammals',
        collection_name=collection_info['name'],
        collection_route=collection_info['route'],
        item=item_data or {},
        is_edit=is_edit,
    )


def _handle_add_sanja_paleogene_neogene_mammal_item(collection_info):
    return _handle_sanja_paleogene_neogene_mammal_form(collection_info)


def handle_edit_sanja_paleogene_neogene_mammal_item(record_id):
    collection_info = _COLLECTION_FORM_INFO['sanja_paleogene_neogene_mammals']
    return _handle_sanja_paleogene_neogene_mammal_form(collection_info, record_id=record_id)


# ---------------------------------------------------------------------------
# Bilja mollusc collections (PostgreSQL-backed, schema-driven form)
# ---------------------------------------------------------------------------

def _handle_bilja_collection_form(collection_key, collection_info, record_id=None):
    """Generic add/edit/delete handler for any Bilja collection."""
    import bilja_collections_db as bilja_db

    cfg = bilja_db.COLLECTIONS[collection_key]
    is_edit = record_id is not None

    item_data = None
    if is_edit:
        item_data = bilja_db.find_specimen(collection_key, int(record_id))
        if item_data is None:
            flash('Примерак није пронађен.', 'danger')
            return redirect(url_for(collection_info['route']))

    if request.method == 'POST':
        action = (request.form.get('_action') or '').strip()
        if is_edit and action == 'delete':
            bilja_db.delete_specimen(collection_key, int(record_id))
            flash('Примерак је обрисан.', 'success')
            return redirect(url_for(collection_info['route']))

        form = {k: request.form.get(k, '') for k in
                (tuple(cfg['int_fields']) + tuple(cfg['text_fields']))}

        if is_edit:
            bilja_db.update_specimen(collection_key, int(record_id), form)
            flash('Примерак је успешно ажуриран.', 'success')
        else:
            bilja_db.add_specimen(collection_key, form)
            flash(f'Примерак је додат у збирку: {collection_info["name"]}.', 'success')

        return redirect(url_for(collection_info['route']))

    # Build a field list the template can render generically.
    ordered_fields = [
        {
            'key': field,
            'label': bilja_db.FIELD_LABELS_SR.get(field, field),
            'type': 'int' if field in cfg['int_fields'] else 'text',
            'value': (item_data or {}).get(field, ''),
        }
        for field in (tuple(cfg['int_fields']) + tuple(cfg['text_fields']))
    ]

    return render_template(
        'admin_add_bilja_item.html',
        collection_type=collection_key,
        collection_name=collection_info['name'],
        collection_route=collection_info['route'],
        collection_description=cfg.get('description_sr', ''),
        collection_icon=cfg.get('icon', 'bi-collection'),
        item=item_data or {},
        fields=ordered_fields,
        is_edit=is_edit,
    )


def handle_add_bilja_item(collection_key):
    info = _COLLECTION_FORM_INFO.get(collection_key)
    if not info:
        flash('Непозната збирка.', 'danger')
        return redirect(url_for('museum_databases'))
    return _handle_bilja_collection_form(collection_key, info)


def handle_edit_bilja_item(collection_key, record_id):
    info = _COLLECTION_FORM_INFO.get(collection_key)
    if not info:
        flash('Непозната збирка.', 'danger')
        return redirect(url_for('museum_databases'))
    return _handle_bilja_collection_form(collection_key, info, record_id=record_id)


def handle_add_heritage_item(*, get_cultural_heritage_database):
    """Handle cultural heritage item creation form."""
    if request.method == 'POST':
        heritage_data = {
            'name': request.form.get('name', '').strip(),
            'registry_number': request.form.get('registry_number', '').strip(),
            'type': request.form.get('type', '').strip(),
            'category': request.form.get('category', '').strip(),
            'subcategory': request.form.get('subcategory', '').strip(),
            'significance': request.form.get('significance', '').strip(),
            'location': request.form.get('location', '').strip(),
            'condition': request.form.get('condition', '').strip(),
            'protection_date': request.form.get('protection_date', '').strip(),
            'acquisition_date': request.form.get('acquisition_date', '').strip(),
            'description': request.form.get('description', '').strip(),
            'legal_basis': request.form.get('legal_basis', '').strip(),
            'cultural_value': request.form.get('cultural_value', '').strip(),
            'period': request.form.get('period', '').strip(),
            'origin': request.form.get('origin', '').strip(),
            'dimensions': request.form.get('dimensions', '').strip(),
            'material': request.form.get('material', '').strip(),
            'weight': request.form.get('weight', '').strip(),
            'protection_status': request.form.get('protection_status', 'заштићено').strip(),
        }
        # Persistence for cultural heritage items is not implemented: appending
        # to the cached dict from get_cultural_heritage_database() never reaches
        # the heritage_items table and is lost on the next cache refresh.
        # Do NOT flash success — that silently discards the curator's input.
        logger.warning(
            'handle_add_heritage_item: persistence not implemented; %d submitted '
            'fields were not saved.',
            len(heritage_data),
        )
        flash(
            'Чување културног добра тренутно није омогућено, па предмет није '
            'сачуван. Обратите се администратору.',
            'error',
        )
        return redirect(url_for('cultural_heritage_database'))

    return render_template('admin_add_heritage_item.html')


def handle_add_collection_item(collection_type, *, museum_databases_endpoint='museum_databases'):
    """Handle shared curator collection add-item form flow."""
    if collection_type not in _COLLECTION_FORM_INFO:
        flash('Непозната збирка!', 'error')
        return redirect(url_for(museum_databases_endpoint))

    collection_info = _COLLECTION_FORM_INFO[collection_type]

    if collection_type == 'sanja_paleogene_neogene_mammals':
        return _handle_add_sanja_paleogene_neogene_mammal_item(collection_info)

    if collection_type.startswith('bilja_'):
        return handle_add_bilja_item(collection_type)

    if request.method == 'POST':
        item_data = {
            'id': f"{collection_type}_{int(time.time())}",
            'catalog_number': request.form.get('catalog_number', '').strip(),
            'accession_number': request.form.get('accession_number', '').strip(),
            'scientific_name': request.form.get('scientific_name', '').strip(),
            'common_name': request.form.get('common_name', '').strip(),
            'family': request.form.get('family', '').strip(),
            'genus': request.form.get('genus', '').strip(),
            'collection_location': request.form.get('collection_location', '').strip(),
            'collection_date': request.form.get('collection_date', '').strip(),
            'collector': request.form.get('collector', '').strip(),
            'determiner': request.form.get('determiner', '').strip(),
            'description': request.form.get('description', '').strip(),
            'storage_location': request.form.get('storage_location', '').strip(),
            'preservation_method': request.form.get('preservation_method', '').strip(),
            'condition': request.form.get('condition', '').strip(),
            'completeness': request.form.get('completeness', '').strip(),
            'size': request.form.get('size', '').strip(),
            'weight': request.form.get('weight', '').strip(),
            'age': request.form.get('age', '').strip(),
            'sex': request.form.get('sex', '').strip(),
            'life_stage': request.form.get('life_stage', '').strip(),
            'research_project': request.form.get('research_project', '').strip(),
            'publications': request.form.get('publications', '').strip(),
            'special_notes': request.form.get('special_notes', '').strip(),
            'acquisition_method': request.form.get('acquisition_method', '').strip(),
            'storage_type': request.form.get('storage_type', '').strip(),
            'storage_conditions': request.form.get('storage_conditions', '').strip(),
            'notes': request.form.get('notes', '').strip(),
            'rock_type_main': request.form.get('rock_type_main', '').strip(),
            'rock_type_subtype': request.form.get('rock_type_subtype', '').strip(),
            'mineral_composition': request.form.get('mineral_composition', '').strip(),
            'rock_texture': request.form.get('rock_texture', '').strip(),
            'fossil_type': request.form.get('fossil_type', '').strip(),
            'anatomical_part': request.form.get('anatomical_part', '').strip(),
            'preservation_type': request.form.get('preservation_type', '').strip(),
            'sediment_type': request.form.get('sediment_type', '').strip(),
            'sediment_description': request.form.get('sediment_description', '').strip(),
            'latitude': request.form.get('latitude', '').strip(),
            'longitude': request.form.get('longitude', '').strip(),
            'formation': request.form.get('formation', '').strip(),
            'estimated_age_range': request.form.get('estimated_age_range', '').strip(),
            'biozone': request.form.get('biozone', '').strip(),
            'preparation_method': request.form.get('preparation_method', '').strip(),
            'type_status': request.form.get('type_status', '').strip(),
            'plant_type': request.form.get('plant_type', '').strip(),
            'plant_part': request.form.get('plant_part', '').strip(),
            'leaf_morphology': request.form.get('leaf_morphology', '').strip(),
            'venation': request.form.get('venation', '').strip(),
            'paleoecology': request.form.get('paleoecology', '').strip(),
            'division': request.form.get('division', '').strip(),
            'species': request.form.get('species', '').strip(),
            'classification': request.form.get('classification', '').strip(),
            'fall_type': request.form.get('fall_type', '').strip(),
            'fall_date': request.form.get('fall_date', '').strip(),
            'total_mass': request.form.get('total_mass', '').strip(),
            'specimen_mass': request.form.get('specimen_mass', '').strip(),
            'petrologic_type': request.form.get('petrologic_type', '').strip(),
            'weathering_grade': request.form.get('weathering_grade', '').strip(),
            'shock_stage': request.form.get('shock_stage', '').strip(),
            'chemical_composition': request.form.get('chemical_composition', '').strip(),
            'mineralogy': request.form.get('mineralogy', '').strip(),
            'parent_body': request.form.get('parent_body', '').strip(),
            'meteorite_bulletin_number': request.form.get('meteorite_bulletin_number', '').strip(),
            'fragment_type': request.form.get('fragment_type', '').strip(),
            'external_appearance': request.form.get('external_appearance', '').strip(),
            'internal_structure': request.form.get('internal_structure', '').strip(),
            'fusion_crust': request.form.get('fusion_crust', '').strip(),
            'widmanstatten_pattern': request.form.get('widmanstatten_pattern', '').strip(),
            'analytical_methods': request.form.get('analytical_methods', '').strip(),
            'dating_method': request.form.get('dating_method', '').strip(),
            'cosmic_ray_exposure': request.form.get('cosmic_ray_exposure', '').strip(),
            'terrestrial_age': request.form.get('terrestrial_age', '').strip(),
            'date_added': datetime.now().strftime('%Y-%m-%d'),
            'added_by': session.get('user_email', 'system'),
        }
        # Persistence for these generic collection types is not implemented.
        # Do NOT flash success — that silently discards the curator's input while
        # showing a green confirmation. Log the attempt and report honestly.
        logger.warning(
            'handle_add_collection_item: persistence not implemented for collection '
            '"%s"; %d submitted fields were not saved.',
            collection_type, len(item_data),
        )
        flash(
            f'Чување предмета за збирку {collection_info["name"]} тренутно није '
            'омогућено, па предмет није сачуван. Обратите се администратору.',
            'error',
        )
        return redirect(url_for(collection_info['route']))

    if collection_type == 'meteorite':
        template = 'admin_add_meteorite_item.html'
    elif collection_type == 'petrology':
        template = 'admin_add_geological_item.html'
    elif collection_type == 'paleozoology':
        template = 'admin_add_paleozoology_item.html'
    elif collection_type == 'paleobotany':
        template = 'admin_add_paleobotany_item.html'
    else:
        template = 'admin_add_collection_item.html'

    return render_template(
        template,
        collection_type=collection_type,
        collection_name=collection_info['name'],
        collection_route=collection_info['route'],
    )


def render_standard_collection_database(
    *,
    collection_name,
    collection_icon,
    collection_type,
    records,
    statistics,
    prepare_collection_records_for_display,
    get_qr_collection_action_url,
    collection_actions_enabled=True,
    collection_add_enabled=None,
    collection_export_enabled=None,
):
    """Render a standard collection database page with QR highlight support."""
    specimens, highlight = prepare_collection_records_for_display(collection_type, records)
    specimens = normalize_collection_curators_for_display(collection_type, specimens)
    return render_template(
        'admin_collection_database.html',
        collection_name=collection_name,
        collection_icon=collection_icon,
        specimens=specimens,
        statistics=statistics,
        collection_type=collection_type,
        highlight=highlight,
        qr_action_url=get_qr_collection_action_url(collection_type),
        collection_actions_enabled=collection_actions_enabled,
        collection_add_enabled=collection_actions_enabled if collection_add_enabled is None else collection_add_enabled,
        collection_export_enabled=collection_actions_enabled if collection_export_enabled is None else collection_export_enabled,
    )


def render_cultural_heritage_database(
    *,
    get_cultural_heritage_database,
    prepare_collection_records_for_display,
    get_qr_collection_action_url,
):
    """Render cultural heritage database view."""
    heritage_db = get_cultural_heritage_database()
    all_heritage_items = heritage_db['heritage_items']
    heritage_items, highlight = prepare_collection_records_for_display('heritage', all_heritage_items)
    statistics = dict(heritage_db['statistics'])
    statistics['total_heritage_items'] = len(all_heritage_items)
    statistics['exceptional_significance'] = len(
        [item for item in all_heritage_items if item.get('significance') == 'Културно добро од изузетног значаја']
    )
    statistics['great_significance'] = len(
        [item for item in all_heritage_items if item.get('significance') == 'Културно добро од великог значаја']
    )
    statistics['regular_significance'] = len(
        [item for item in all_heritage_items if item.get('significance') == 'Културно добро']
    )
    statistics['natural_heritage'] = len(
        [item for item in all_heritage_items if item.get('category') == 'Природњачко наслеђе']
    )
    statistics['displayed_items'] = len([item for item in all_heritage_items if 'Сала' in (item.get('location') or '')])
    statistics['storage_items'] = len([item for item in all_heritage_items if 'Депо' in (item.get('location') or '')])
    statistics['excellent_condition'] = len([item for item in all_heritage_items if item.get('condition') == 'Одлично'])
    statistics['good_condition'] = len([item for item in all_heritage_items if item.get('condition') == 'Добро'])

    return render_template(
        'admin_cultural_heritage_database.html',
        heritage_items=heritage_items,
        heritage_types=heritage_db['heritage_types'],
        categories=heritage_db['categories'],
        subcategories=heritage_db['subcategories'],
        significance_levels=heritage_db['significance_levels'],
        locations=heritage_db['locations'],
        conditions=heritage_db['conditions'],
        protection_statuses=heritage_db['protection_statuses'],
        statistics=statistics,
        total_heritage_items=len(all_heritage_items),
        highlight=highlight,
        qr_action_url=get_qr_collection_action_url('heritage'),
    )


def render_meteorite_collection(
    *,
    get_meteorite_collection_database,
    prepare_collection_records_for_display,
    get_qr_collection_action_url,
):
    """Render meteorite collection database."""
    meteorite_db = get_meteorite_collection_database()
    specimens, highlight = prepare_collection_records_for_display('meteorite', meteorite_db['specimens'])
    specimens = normalize_collection_curators_for_display('meteorite', specimens)
    return render_template(
        'admin_collection_database.html',
        collection_name='Збирка метеорита',
        collection_icon='museum-icon-shooting-star',
        specimens=specimens,
        statistics=meteorite_db['statistics'],
        collection_type='meteorite',
        highlight=highlight,
        qr_action_url=get_qr_collection_action_url('meteorite'),
    )


def _priloži_foto_id(minerals):
    """Upisi `foto_id` (glavna fotografija iz Фototeke) na svaki red strane.

    Jedan upit za celu stranu. Ako Фototeka nije dostupna, redovi ostaju bez
    `foto_id` i tabela pada nazad na staru `images` tabelu / placeholder —
    lista se nikad ne rusi zbog slika.
    """
    if not minerals:
        return
    try:
        import fototeka_views

        brojevi = [m.get('inventarni_broj') for m in minerals]
        mapa = fototeka_views.glavne_fotografije_predmeta(session, 'mineral', brojevi)
        for mineral in minerals:
            broj = str(mineral.get('inventarni_broj') or '').strip()
            mineral['foto_id'] = mapa.get(broj)
    except Exception as exc:  # slike nikad ne obaraju listu predmeta
        logger.warning('Фototeka thumbnails unavailable for the collection table: %s', exc)


def render_mineral_collection(*, get_mineral_database):
    """Render mineral collection or RRUFF browser view."""
    mineral_db = get_mineral_database()
    current_lang = current_ui_language()
    # Dormant while English is disabled (always False); kept so re-enabling
    # English restores the English mineral-column set with no other change.
    is_english = current_lang == 'en'

    search_query = request.args.get('search', '').strip()
    search_mode = request.args.get('search_mode', 'collection')
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 50, type=int)
    sort_by = request.args.get('sort_by', 'id')
    sort_order = request.args.get('sort_order', 'asc')

    available_columns = _MINERAL_COLUMNS_EN if is_english else _MINERAL_COLUMNS_SR
    columns_param = request.args.get('columns', '')
    requested_columns = columns_param.split(',') if columns_param else list(_MINERAL_DEFAULT_COLUMNS)
    selected_columns = [col for col in requested_columns if col in available_columns]
    if not selected_columns:
        selected_columns = list(_MINERAL_DEFAULT_COLUMNS)
    is_rruff_mode = search_mode == 'rruff'

    elements = request.args.get('elements', '').strip()
    crystal_system = request.args.get('crystal_system', '').strip()
    ima_status = request.args.get('ima_status', '').strip()

    if is_rruff_mode:
        result = mineral_db.get_rruff_minerals(
            page=page,
            per_page=per_page,
            search=search_query,
            crystal_system=crystal_system,
            ima_status=ima_status,
            elements=elements,
        )
        stats = {'total_minerals': 0}
        rruff_stats = mineral_db.get_rruff_statistics()
    else:
        if search_query:
            result = mineral_db.search_minerals(
                search_query,
                page=page,
                per_page=per_page,
                sort_by=sort_by,
                sort_order=sort_order,
            )
        else:
            result = mineral_db.get_all_minerals(
                page=page,
                per_page=per_page,
                sort_by=sort_by,
                sort_order=sort_order,
            )

        stats = mineral_db.get_statistics()
        rruff_stats = mineral_db.get_rruff_statistics()

    # Thumbnail glavne fotografije iz Фototeke: JEDAN batch upit za celu stranu
    # (ne po redu). Vidljivost se filtrira serverski — tudja privatna fotografija
    # se ne vraca, pa predmet izgleda kao da nema sliku.
    _priloži_foto_id(result.get('minerals') or [])

    return render_template(
        'admin_mineral_collection.html',
        minerals=result['minerals'],
        total=result['total'],
        total_minerals=result['total'],
        page=result['page'],
        per_page=result['per_page'],
        total_pages=result['total_pages'],
        stats=stats,
        rruff_stats=rruff_stats,
        search_query=search_query,
        is_rruff_mode=is_rruff_mode,
        sort_by=sort_by,
        sort_order=sort_order,
        selected_columns=selected_columns,
        available_columns=available_columns,
        elements=elements,
        crystal_system=crystal_system,
        ima_status=ima_status,
    )


def render_mineral_detail(mineral_id, *, get_mineral_database):
    """Render one mineral detail page."""
    mineral_db = get_mineral_database()
    mineral = mineral_db.get_mineral_by_id(mineral_id)

    if not mineral:
        flash('Минерал није пронађен.', 'error')
        return redirect(url_for('admin_mineral_collection'))

    rruff_data = None
    if mineral.get('naziv'):
        rruff_data = mineral_db.get_rruff_data_for_mineral(mineral['naziv'])

    # Kartica predmeta je do sada gledala SAMO staru `images` putanju, pa je
    # predmet sa fotografijom iz Фototeke prikazivao placeholder. Isti batch
    # lookup kao u tabeli (poštuje vidljivost).
    _priloži_foto_id([mineral])

    return render_template('admin_mineral_detail.html', mineral=mineral, rruff_data=rruff_data)


def redirect_rruff_minerals():
    """Redirect to the mineral collection in RRUFF mode."""
    return redirect(url_for('admin_mineral_collection', search_mode='rruff'))


def render_rruff_detail(mineral_id, *, get_mineral_database):
    """Render one RRUFF mineral detail page."""
    try:
        mineral_db = get_mineral_database()
        mineral = mineral_db.get_rruff_mineral_by_id(mineral_id)

        if not mineral:
            flash('RRUFF минерал није пронађен.', 'error')
            return redirect(url_for('admin_mineral_collection', search_mode='rruff'))

        current_app.logger.info("Loading RRUFF detail for mineral ID %s: %s", mineral_id, mineral.get('name', 'Unknown'))
        return render_template('admin_rruff_detail.html', mineral=mineral)
    except Exception as exc:
        current_app.logger.error("Error loading RRUFF detail for mineral ID %s: %s", mineral_id, exc)
        current_app.logger.exception("Full traceback:")
        flash('Грешка при учитавању RRUFF података.', 'error')
        return redirect(url_for('admin_mineral_collection', search_mode='rruff'))


def _build_mineral_form_data(*, input_by):
    return {
        'inventory_number': request.form.get('inventory_number', '').strip(),
        'item_name': request.form.get('item_name', '').strip(),
        'acquisition_method': request.form.get('acquisition_method', '').strip(),
        'acquisition_date': request.form.get('acquisition_date', '').strip() or None,
        'input_date': request.form.get('input_date', '').strip() or None,
        'input_by': input_by,
        'donor': request.form.get('donor', '').strip(),
        'identifier': request.form.get('identifier', '').strip(),
        'comments': request.form.get('comments', '').strip(),
        'description': request.form.get('description', '').strip(),
        'storage_location': request.form.get('storage_location', '').strip(),
        'card_locality': request.form.get('card_locality', '').strip(),
        'bibliography_flag': request.form.get('bibliography_flag') == 'on',
        'quantity': request.form.get('quantity', 1, type=int),
    }


def handle_add_mineral(*, get_mineral_database):
    """Display and process add-mineral form."""
    mineral_db = get_mineral_database()

    if request.method == 'POST':
        mineral_data = _build_mineral_form_data(input_by=session.get('user_email', 'system'))
        if not mineral_data['item_name']:
            flash('Назив минерала је обавезан!', 'error')
            return render_template(
                'admin_add_mineral.html',
                mineral_data=mineral_data,
                next_inventory_number=mineral_db.get_next_inventory_number(),
            )

        new_id = mineral_db.add_mineral(mineral_data)
        if new_id:
            flash(f'Минерал је успешно додат! (ID: {new_id})', 'success')
            return redirect(url_for('admin_mineral_detail', mineral_id=new_id))

        flash('Грешка при додавању минерала!', 'error')
        return render_template(
            'admin_add_mineral.html',
            mineral_data=mineral_data,
            next_inventory_number=mineral_db.get_next_inventory_number(),
        )

    return render_template(
        'admin_add_mineral.html',
        mineral_data={},
        next_inventory_number=mineral_db.get_next_inventory_number(),
    )


def handle_edit_mineral(mineral_id, *, get_mineral_database):
    """Display and process edit-mineral form."""
    mineral_db = get_mineral_database()
    mineral = mineral_db.get_mineral_by_id(mineral_id)

    if not mineral:
        flash('Минерал није пронађен.', 'error')
        return redirect(url_for('admin_mineral_collection'))

    if request.method == 'POST':
        mineral_data = _build_mineral_form_data(
            input_by=request.form.get('input_by', '').strip(),
        )
        if not mineral_data['item_name']:
            flash('Назив минерала је обавезан!', 'error')
            return render_template(
                'admin_add_mineral.html',
                mineral_data=mineral_data,
                edit_mode=True,
                mineral_id=mineral_id,
            )

        if mineral_db.update_mineral(mineral_id, mineral_data):
            flash('Минерал је успешно ажуриран!', 'success')
            return redirect(url_for('admin_mineral_detail', mineral_id=mineral_id))

        flash('Грешка при ажурирању минерала!', 'error')

    mineral_data = {
        'inventory_number': mineral.get('inventarni_broj', ''),
        'item_name': mineral.get('naziv', ''),
        'acquisition_method': mineral.get('nacin_nabavljanja', ''),
        'acquisition_date': mineral.get('datum_nabavljanja', ''),
        'input_date': mineral.get('datum_unosa', ''),
        'input_by': mineral.get('uneo_u_bazu', ''),
        'donor': mineral.get('legator', ''),
        'identifier': mineral.get('identifikovao', ''),
        'comments': mineral.get('komentar', ''),
        'description': mineral.get('napomena', ''),
        'storage_location': mineral.get('gde_se_nalazi', ''),
        'card_locality': mineral.get('lokalitet', ''),
        'bibliography_flag': mineral.get('u_bibliografiji', False),
        'quantity': mineral.get('kolicina', 1),
    }
    return render_template(
        'admin_add_mineral.html',
        mineral_data=mineral_data,
        edit_mode=True,
        mineral_id=mineral_id,
    )


def handle_delete_mineral(mineral_id, *, get_mineral_database):
    """Delete a mineral from the collection."""
    mineral_db = get_mineral_database()
    if mineral_db.delete_mineral(mineral_id):
        flash('Минерал је успешно обрисан!', 'success')
    else:
        flash('Грешка при брисању минерала!', 'error')
    return redirect(url_for('admin_mineral_collection'))


def _inventory_sort_key(sort_by, item):
    value = item.get(sort_by, '')
    if value is None:
        value = ''

    if sort_by == 'inventory_number':
        if isinstance(value, (int, float)):
            return (0, value, '')

        str_value = str(value)
        if str_value.startswith('M') and str_value[1:].isdigit():
            return (1, int(str_value[1:]), str_value)
        try:
            return (0, int(str_value), '')
        except (ValueError, TypeError):
            return (2, 0, str_value.lower())

    return str(value).lower() if value else ''


def render_inventory_book():
    """Render inventory book page."""
    from inventory_reconciliation import InventoryReconciliation

    reconciliation = InventoryReconciliation()
    search_name = request.args.get('search_name', '').strip()
    search_locality = request.args.get('search_locality', '').strip()
    inv_number = request.args.get('inv_number', '').strip()
    sheet_filter = request.args.get('sheet', '').strip()
    page = request.args.get('page', 1, type=int)
    per_page = 100

    sort_by = request.args.get('sort_by', 'inventory_number').strip()
    sort_order = request.args.get('sort_order', 'asc').strip()
    valid_sort_columns = [
        'inventory_number',
        'name',
        'locality',
        'quantity',
        'acquisition_info',
        'collector_donator',
        'sheet',
    ]
    if sort_by not in valid_sort_columns:
        sort_by = 'inventory_number'
    if sort_order not in ['asc', 'desc']:
        sort_order = 'asc'

    search_params = {}
    if search_name:
        search_params['name'] = search_name
    if search_locality:
        search_params['locality'] = search_locality
    if inv_number:
        search_params['inv_number'] = inv_number
    if sheet_filter:
        search_params['sheet'] = sheet_filter

    if search_params:
        items = reconciliation.search_inventory(**search_params)
    else:
        items = reconciliation.get_inventory_book_items()

    items = sorted(
        items,
        key=lambda item: _inventory_sort_key(sort_by, item),
        reverse=(sort_order == 'desc'),
    )
    collection_index = reconciliation.get_collection_index()

    total_items = len(items)
    start_idx = (page - 1) * per_page
    end_idx = start_idx + per_page
    annotated_items = []
    for item in items[start_idx:end_idx]:
        item_with_match = dict(item)
        matches = collection_index.get(item.get('inventory_number'), [])
        item_with_match['collection_matches'] = matches
        item_with_match['has_collection_match'] = bool(matches)
        item_with_match['primary_collection_id'] = matches[0]['id'] if matches else None
        item_with_match['collection_match_count'] = len(matches)
        annotated_items.append(item_with_match)

    return render_template(
        'admin_inventory_book.html',
        items=annotated_items,
        total_items=total_items,
        summary=reconciliation.get_inventory_summary(),
        available_sheets=reconciliation.get_available_sheets(),
        current_page=page,
        total_pages=(total_items + per_page - 1) // per_page,
        search_name=search_name,
        search_locality=search_locality,
        inv_number=inv_number,
        sheet_filter=sheet_filter,
        sort_by=sort_by,
        sort_order=sort_order,
    )


def render_inventory_reconciliation():
    """Render inventory reconciliation report."""
    from inventory_reconciliation import InventoryReconciliation

    reconciliation = InventoryReconciliation()
    return render_template(
        'admin_inventory_reconciliation.html',
        summary=reconciliation.get_inventory_summary(),
        report=reconciliation.generate_discrepancy_report(),
    )


def render_conservation_biology(*, conservation_biology_database):
    """Render conservation biology database."""
    return render_template(
        'admin_collection_database.html',
        collection_name='Конзервација биолошких збирки',
        collection_icon='bi-shield-check',
        specimens=conservation_biology_database['records'],
        statistics=conservation_biology_database['statistics'],
        collection_type='conservation',
    )


def export_collection_to_pdf(collection_type):
    """Redirect collection PDF export requests to the current collection page."""
    flash('Функционалност извоза у PDF је у развоју.', 'info')
    return redirect(url_for(_COLLECTION_ROUTES.get(collection_type, 'museum_databases')))
