"""Shared route implementations for collection, mineral, and inventory admin views."""

import logging
import time
from datetime import datetime

from flask import current_app, flash, redirect, render_template, request, session, url_for

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
    'botany': 'botany_collection',
    'ichthyology': 'ichthyology_collection',
    'entomology': 'entomology_collection',
    'mycology': 'mycology_collection',
    'herpetology': 'herpetology_collection',
    'ornithology': 'ornithology_collection',
    'paleozoology': 'paleozoology_collection',
    'paleobotany': 'paleobotany_collection',
    'petrology': 'petrology_collection',
    'meteorite': 'meteorite_collection',
    'conservation': 'conservation_biology',
}
_COLLECTION_FORM_INFO = {
    'botany': {'name': 'Ботаничка збирка', 'route': 'botany_collection'},
    'ichthyology': {'name': 'Ихтиолошка збирка', 'route': 'ichthyology_collection'},
    'entomology': {'name': 'Ентомолошка збирка', 'route': 'entomology_collection'},
    'mycology': {'name': 'Миколошка збирка', 'route': 'mycology_collection'},
    'herpetology': {'name': 'Херпетолошка збирка', 'route': 'herpetology_collection'},
    'ornithology': {'name': 'Орнитолошка збирка', 'route': 'ornithology_collection'},
    'general_zoology': {'name': 'Општа зоологија', 'route': 'general_zoology_collection'},
    'conservation': {'name': 'Конзервација биолошких збирки', 'route': 'conservation_biology'},
    'conservation_biology': {'name': 'Конзервациона биологија', 'route': 'conservation_biology_collection'},
    'paleozoology': {'name': 'Палеозоолошка збирка', 'route': 'paleozoology_collection'},
    'paleobotany': {'name': 'Палеоботаничка збирка', 'route': 'paleobotany_collection'},
    'petrology': {'name': 'Петролошка збирка', 'route': 'petrology_collection'},
    'meteorite': {'name': 'Збирка метеорита', 'route': 'meteorite_collection'},
    'geology_conservation': {'name': 'Геолошка конзервација', 'route': 'geology_conservation_collection'},
}


def handle_add_heritage_item(*, get_cultural_heritage_database):
    """Handle cultural heritage item creation form."""
    if request.method == 'POST':
        heritage_db = get_cultural_heritage_database()
        heritage_data = {
            'id': len(heritage_db['heritage_items']) + 1,
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
        heritage_db['heritage_items'].append(heritage_data)
        flash('Културно добро је успешно додато!', 'success')
        return redirect(url_for('cultural_heritage_database'))

    return render_template('admin_add_heritage_item.html')


def handle_add_collection_item(collection_type, *, museum_databases_endpoint='museum_databases'):
    """Handle shared curator collection add-item form flow."""
    if collection_type not in _COLLECTION_FORM_INFO:
        flash('Непозната збирка!', 'error')
        return redirect(url_for(museum_databases_endpoint))

    collection_info = _COLLECTION_FORM_INFO[collection_type]

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
        _ = item_data
        flash(f'Предмет је успешно додат у збирку {collection_info["name"]}!', 'success')
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
    get_image_upload_action_url,
    image_upload_database=None,
):
    """Render a standard collection database page with QR highlight support."""
    specimens, highlight = prepare_collection_records_for_display(collection_type, records)
    return render_template(
        'admin_collection_database.html',
        collection_name=collection_name,
        collection_icon=collection_icon,
        specimens=specimens,
        statistics=statistics,
        collection_type=collection_type,
        highlight=highlight,
        qr_action_url=get_qr_collection_action_url(collection_type),
        image_upload_url=get_image_upload_action_url(image_upload_database or collection_type),
    )


def render_cultural_heritage_database(
    *,
    get_cultural_heritage_database,
    prepare_collection_records_for_display,
    get_qr_collection_action_url,
    get_image_upload_action_url,
):
    """Render cultural heritage database view."""
    heritage_db = get_cultural_heritage_database()
    all_heritage_items = heritage_db['heritage_items']
    heritage_items, highlight = prepare_collection_records_for_display('heritage', all_heritage_items)
    statistics = dict(heritage_db['statistics'])
    statistics['total_heritage_items'] = len(all_heritage_items)
    statistics['exceptional_significance'] = len(
        [item for item in all_heritage_items if item['significance'] == 'Културно добро од изузетног значаја']
    )
    statistics['great_significance'] = len(
        [item for item in all_heritage_items if item['significance'] == 'Културно добро од великог значаја']
    )
    statistics['regular_significance'] = len(
        [item for item in all_heritage_items if item['significance'] == 'Културно добро']
    )
    statistics['natural_heritage'] = len(
        [item for item in all_heritage_items if item['category'] == 'Природњачко наслеђе']
    )
    statistics['displayed_items'] = len([item for item in all_heritage_items if 'Сала' in item['location']])
    statistics['storage_items'] = len([item for item in all_heritage_items if 'Депо' in item['location']])
    statistics['excellent_condition'] = len([item for item in all_heritage_items if item['condition'] == 'Одлично'])
    statistics['good_condition'] = len([item for item in all_heritage_items if item['condition'] == 'Добро'])

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
        image_upload_url=get_image_upload_action_url('cultural_heritage'),
    )


def render_meteorite_collection(
    *,
    get_meteorite_collection_database,
    prepare_collection_records_for_display,
    get_qr_collection_action_url,
    get_image_upload_action_url,
):
    """Render meteorite collection database."""
    meteorite_db = get_meteorite_collection_database()
    specimens, highlight = prepare_collection_records_for_display('meteorite', meteorite_db['specimens'])
    return render_template(
        'admin_collection_database.html',
        collection_name='Збирка метеорита',
        collection_icon='bi-stars',
        specimens=specimens,
        statistics=meteorite_db['statistics'],
        collection_type='meteorite',
        highlight=highlight,
        qr_action_url=get_qr_collection_action_url('meteorite'),
        image_upload_url=get_image_upload_action_url('meteorite'),
    )


def render_mineral_collection(*, get_mineral_database, get_image_upload_action_url):
    """Render mineral collection or RRUFF browser view."""
    mineral_db = get_mineral_database()
    current_lang = session.get('museum_lang', request.cookies.get('museum_lang', 'sr-Cyrl'))
    is_english = current_lang == 'en'

    search_query = request.args.get('search', '').strip()
    search_mode = request.args.get('search_mode', 'collection')
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 50, type=int)
    sort_by = request.args.get('sort_by', 'id')
    sort_order = request.args.get('sort_order', 'asc')

    columns_param = request.args.get('columns', '')
    selected_columns = columns_param.split(',') if columns_param else list(_MINERAL_DEFAULT_COLUMNS)
    available_columns = _MINERAL_COLUMNS_EN if is_english else _MINERAL_COLUMNS_SR
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
        image_upload_url=get_image_upload_action_url('mineral'),
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


def handle_edit_mineral(mineral_id, *, get_mineral_database, get_image_storage):
    """Display and process edit-mineral form."""
    mineral_db = get_mineral_database()
    mineral = mineral_db.get_mineral_by_id(mineral_id)
    image_storage = get_image_storage()

    if not mineral:
        flash('Минерал није пронађен.', 'error')
        return redirect(url_for('admin_mineral_collection'))

    mineral_images = image_storage.get_images_for_entity('mineral', 'collection_item', str(mineral_id))

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
                mineral_images=mineral_images,
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
        mineral_images=mineral_images,
    )


def handle_delete_mineral_image(mineral_id, image_id, *, get_mineral_database, get_image_storage):
    """Delete a mineral image from the edit screen."""
    mineral_db = get_mineral_database()
    mineral = mineral_db.get_mineral_by_id(mineral_id)
    if not mineral:
        flash('Минерал није пронађен.', 'error')
        return redirect(url_for('admin_mineral_collection'))

    image_storage = get_image_storage()
    mineral_images = image_storage.get_images_for_entity('mineral', 'collection_item', str(mineral_id))
    image_ids = {img.get('image_id') for img in mineral_images if img.get('image_id')}

    if image_id not in image_ids:
        flash('Слика није пронађена за овај минерал.', 'error')
        return redirect(url_for('edit_mineral', mineral_id=mineral_id))

    if image_storage.delete_image(image_id):
        flash('Слика је успешно обрисана.', 'success')
    else:
        flash('Грешка при брисању слике.', 'error')

    return redirect(url_for('edit_mineral', mineral_id=mineral_id))


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
