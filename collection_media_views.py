"""Shared route implementations for public QR/media views and batch image upload."""

import logging
import os
from datetime import datetime
from urllib.parse import unquote

from flask import current_app, flash, jsonify, redirect, render_template, request, send_file, session, url_for

logger = logging.getLogger(__name__)

QR_SPECIMEN_FIELD_LABELS = {
    'catalog_number': 'Каталошки број',
    'meteorite_name': 'Назив метеорита',
    'scientific_name': 'Научно име',
    'common_name_sr': 'Народно име',
    'classification': 'Класификација',
    'fall_type': 'Тип пада',
    'fall_date': 'Датум пада',
    'location_found': 'Локација налаза',
    'total_mass_kg': 'Укупна маса (kg)',
    'specimen_mass': 'Маса примерка (g)',
    'description': 'Опис',
    'source': 'Извор',
    'curator': 'Кустос',
    'family': 'Фамилија',
    'habitat': 'Станиште',
    'date_collected': 'Датум прикупљања',
    'collector': 'Сакупљач',
    'conservation_status': 'Статус заштите',
    'geological_period': 'Геолошки период',
    'age_million_years': 'Старост (милиони година)',
    'class': 'Класа',
    'order': 'Ред',
    'acquisition_date': 'Датум набавке',
    'quantity': 'Количина',
    'condition': 'Стање',
    'serbian_meteorite': 'Српски метеорит',
}

QR_SPECIMEN_COLLECTION_NAMES = {
    'meteorite': 'Збирка метеорита',
    'botany': 'Ботаничка збирка',
    'paleozoology': 'Палеозоолошка збирка',
    'paleobotany': 'Палеоботаничка збирка',
}

QR_SPECIMEN_COLLECTION_URLS = {
    'meteorite': '/admin/meteorite_collection',
    'botany': '/admin/botany_collection',
    'paleozoology': '/admin/paleozoology_collection',
    'paleobotany': '/admin/paleobotany_collection',
}

QR_SPECIMEN_TITLE_FIELDS = {
    'meteorite': 'meteorite_name',
    'botany': 'scientific_name',
    'paleozoology': 'scientific_name',
    'paleobotany': 'scientific_name',
}

PUBLIC_SPECIMEN_MEDIA_TARGETS = {
    ('meteorites', 'meteorite'),
    ('botany', 'botany'),
    ('paleozoology', 'paleozoology'),
}


def _is_public_specimen_media_target(database, entity_type):
    """Allow anonymous media access only for explicitly public QR collections."""
    normalized_database = str(database or '').strip().lower()
    normalized_entity_type = str(entity_type or '').strip().lower()
    return (normalized_database, normalized_entity_type) in PUBLIC_SPECIMEN_MEDIA_TARGETS


def _authorize_specimen_media_request(database, entity_type):
    """Require collection access unless the request targets a public QR collection."""
    if _is_public_specimen_media_target(database, entity_type):
        return None

    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'Морате бити пријављени'}), 401

    access_checker = getattr(current_app, 'user_has_module_access', None)
    module_key_getter = getattr(current_app, 'get_image_upload_module_key', None)
    if access_checker is None or module_key_getter is None:
        current_app.logger.error('Specimen media access helpers are not configured on the Flask app')
        return jsonify({'success': False, 'message': 'Грешка у конфигурацији апликације'}), 500

    user_email = session.get('user_email', '')
    user_role = session.get('user_role', '')
    module_key = module_key_getter(database)
    if not module_key or not access_checker(user_email, user_role, module_key):
        return jsonify({'success': False, 'message': 'Немате дозволу за приступ овој слици'}), 403

    return None


def _send_placeholder(*placeholder_candidates):
    for placeholder_path in placeholder_candidates:
        if os.path.exists(placeholder_path):
            return send_file(
                placeholder_path,
                mimetype='image/png' if placeholder_path.endswith('.png') else 'image/jpeg',
            )
    return "No image available", 404


def _send_entity_image(get_image_storage, database, entity_type, entity_id, size):
    try:
        image_storage = get_image_storage()
        primary_image_path_getter = getattr(image_storage, 'get_primary_entity_image_path', None)
        if primary_image_path_getter:
            image_path = primary_image_path_getter(database, entity_type, entity_id, size)
            if image_path and image_path.exists():
                suffix = image_path.suffix.lower()
                mimetype = 'image/png' if suffix == '.png' else 'image/jpeg'
                return send_file(image_path, mimetype=mimetype)

        images = image_storage.get_images_for_entity(database, entity_type, entity_id)
        if images:
            image_id = images[0]['image_id']
            image_path = image_storage.get_image_path(image_id, size)
            if image_path and image_path.exists():
                suffix = image_path.suffix.lower()
                mimetype = 'image/png' if suffix == '.png' else 'image/jpeg'
                return send_file(image_path, mimetype=mimetype)
    except Exception as exc:
        logger.error("Error loading specimen image: %s", exc)
    return None


def handle_batch_image_upload(
    *,
    get_accessible_image_upload_databases,
    normalize_image_upload_database,
    ensure_image_upload_access,
    user_has_module_access,
    get_image_upload_config,
    get_batch_uploader,
    get_image_upload_records,
    get_image_upload_collection_url,
    get_image_upload_display_name,
):
    """Batch image upload interface for museum collections."""
    user_email = session.get('user_email', '')
    user_role = session.get('user_role', 'user')
    databases = get_accessible_image_upload_databases(user_email, user_role)

    database = normalize_image_upload_database(request.values.get('database'))
    if database:
        access_redirect = ensure_image_upload_access(database)
        if access_redirect:
            return access_redirect

    if not databases and user_role != 'admin':
        flash('Немате приступ ниједној збирци са групним отпремањем слика.', 'warning')
        if user_has_module_access(user_email, user_role, 'museum_databases'):
            return redirect(url_for('museum_databases'))
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        action = request.form.get('action')
        directory = (request.form.get('directory') or '').strip()

        config = get_image_upload_config(database)
        if not config:
            flash('Изаберите подржану збирку за отпремање слика.', 'warning')
            return redirect(url_for('batch_image_upload'))

        if not directory:
            flash('Унесите директоријум са сликама.', 'warning')
            return redirect(url_for('batch_image_upload', database=database))

        uploader = get_batch_uploader()
        database_items = get_image_upload_records(database)

        if action == 'preview':
            preview = uploader.preview_batch_upload(directory, database_items, database)
            if preview.get('error'):
                flash('Нису пронађене валидне слике у изабраном директоријуму.', 'warning')
                return redirect(url_for('batch_image_upload', database=database))

            return render_template(
                'admin_batch_upload_preview.html',
                database=database,
                database_name=config['name'],
                directory=directory,
                preview=preview,
                back_url=get_image_upload_collection_url(database),
            )

        if action == 'upload':
            image_files = uploader.scan_directory(directory)
            if not image_files:
                flash('Нису пронађене слике за отпремање.', 'warning')
                return redirect(url_for('batch_image_upload', database=database))

            results = uploader.process_batch_upload(
                image_files=image_files,
                database_items=database_items,
                database=database,
                entity_type=config['entity_type'],
                auto_upload=request.form.get('auto_upload') == 'true',
            )
            return render_template(
                'admin_batch_upload_results.html',
                database=database,
                database_name=config['name'],
                results=results,
                back_url=get_image_upload_collection_url(database),
            )

        flash('Непозната акција групног отпремања.', 'warning')
        return redirect(url_for('batch_image_upload', database=database))

    return render_template(
        'admin_batch_image_upload.html',
        databases=databases,
        selected_database=database,
        selected_database_name=get_image_upload_display_name(database) if database else '',
        back_url=get_image_upload_collection_url(database)
        if database
        else (
            url_for('museum_databases')
            if user_has_module_access(user_email, user_role, 'museum_databases')
            else url_for('dashboard')
        ),
    )


def render_qr_view_mineral_box(box_number, *, get_mineral_database):
    """Public mobile-optimized view for mineral box contents."""
    box_number = unquote(box_number)
    mineral_db = get_mineral_database()
    if not mineral_db or not mineral_db.available:
        return (
            render_template(
                'error.html',
                error_title='Грешка',
                error_message='База минерала није доступна.',
            ),
            500,
        )

    try:
        from sqlalchemy import text as sa_text

        with mineral_db.engine.connect() as conn:
            rows = conn.execute(
                sa_text("SELECT * FROM minerals WHERE TRIM(storage_location) = :box_num"),
                {"box_num": box_number},
            ).mappings().all()
            box_minerals = []
            for row in rows:
                mineral = dict(row)
                mineral['gde_se_nalazi'] = mineral.get('storage_location', '')
                mineral['naziv'] = mineral.get('item_name', '')
                mineral['inventarni_broj'] = mineral.get('inventory_number', '')
                mineral['lokalitet'] = mineral.get('card_locality', '')
                mineral['legator'] = mineral.get('donor', '')
                mineral['identifikovao'] = mineral.get('identifier', '')
                mineral['kolicina'] = mineral.get('quantity', '')
                mineral['napomena'] = mineral.get('comments', '')
                box_minerals.append(mineral)
    except Exception:
        result = mineral_db.get_all_minerals(page=1, per_page=10000)
        if not result or 'minerals' not in result:
            return (
                render_template(
                    'error.html',
                    error_title='Грешка',
                    error_message='Грешка при учитавању минерала.',
                ),
                500,
            )
        box_minerals = [
            mineral
            for mineral in result['minerals']
            if str(mineral.get('gde_se_nalazi', '')).strip() == box_number
        ]

    if not box_minerals:
        return (
            render_template(
                'error.html',
                error_title='Кутија није пронађена',
                error_message=f'Кутија "{box_number}" није пронађена или је празна.',
            ),
            404,
        )

    return render_template(
        'mineral_box_qr_view.html',
        box_number=box_number,
        minerals=box_minerals,
        total_minerals=len(box_minerals),
        scan_time=datetime.now().strftime('%d.%m.%Y %H:%M'),
    )


def get_specimen_image(database, entity_type, entity_id, *, get_image_storage):
    """Get specimen image or placeholder."""
    auth_response = _authorize_specimen_media_request(database, entity_type)
    if auth_response is not None:
        return auth_response

    response = _send_entity_image(get_image_storage, database, entity_type, entity_id, 'medium')
    if response is not None:
        return response
    return _send_placeholder(os.path.join('static', 'images', 'specimen-placeholder.png'))


def get_specimen_image_full(database, entity_type, entity_id, *, get_image_storage):
    """Get full-size specimen image."""
    auth_response = _authorize_specimen_media_request(database, entity_type)
    if auth_response is not None:
        return auth_response

    response = _send_entity_image(get_image_storage, database, entity_type, entity_id, 'original')
    if response is not None:
        return response
    return get_specimen_image(database, entity_type, entity_id, get_image_storage=get_image_storage)


def get_specimen_thumbnail(database, entity_type, entity_id, *, get_image_storage):
    """Get specimen thumbnail or small placeholder."""
    auth_response = _authorize_specimen_media_request(database, entity_type)
    if auth_response is not None:
        return auth_response

    response = _send_entity_image(get_image_storage, database, entity_type, entity_id, 'small')
    if response is not None:
        return response
    return _send_placeholder(
        os.path.join('static', 'images', 'specimen-placeholder-thumb.png'),
        os.path.join('static', 'images', 'specimen-placeholder.png'),
    )


def get_image_by_id(image_id, *, get_image_storage):
    """Serve an image directly by image id."""
    size = request.args.get('size', 'original').strip().lower()
    if size not in {'original', 'small', 'medium', 'large'}:
        size = 'original'

    try:
        image_storage = get_image_storage()
        metadata = image_storage.get_image_metadata(image_id)
        if not metadata:
            return "No image available", 404

        auth_response = _authorize_specimen_media_request(
            metadata.get('database_name'), metadata.get('entity_type')
        )
        if auth_response is not None:
            return auth_response

        image_path = image_storage.get_image_path(image_id, size)
        if image_path and image_path.exists():
            suffix = image_path.suffix.lower()
            mimetype = 'image/png' if suffix == '.png' else 'image/jpeg'
            return send_file(image_path, mimetype=mimetype)
    except Exception as exc:
        logger.error("Error loading image %s: %s", image_id, exc)

    return "No image available", 404


def render_qr_view_specimen(
    collection_type,
    catalog_number,
    *,
    normalize_qr_collection_type,
    get_meteorite_collection_database,
    botany_collection_database,
    paleozoology_collection_database,
):
    """Public mobile-optimized view for QR code scanned specimens."""
    collection_type = normalize_qr_collection_type(collection_type)
    fields_param = request.args.get('fields', 'all')
    display_mode = request.args.get('mode', 'card')
    show_image = request.args.get('img', '1') == '1'
    selected_fields = None if fields_param == 'all' else fields_param.split(',')

    specimen = None
    try:
        if collection_type == 'meteorite':
            for spec in get_meteorite_collection_database()['specimens']:
                if spec.get('catalog_number') == catalog_number:
                    specimen = spec
                    break
        elif collection_type == 'botany':
            for spec in botany_collection_database['specimens']:
                if spec.get('catalog_number') == catalog_number:
                    specimen = spec
                    break
        elif collection_type == 'paleozoology':
            for spec in paleozoology_collection_database['specimens']:
                if spec.get('catalog_number') == catalog_number:
                    specimen = spec
                    break

        if specimen is None:
            records_loader = getattr(current_app, 'get_qr_collection_records', None)
            if records_loader is not None:
                for spec in records_loader(collection_type) or []:
                    if isinstance(spec, dict) and spec.get('catalog_number') == catalog_number:
                        specimen = spec
                        break

        if not specimen:
            return (
                render_template(
                    'error.html',
                    error_title='Примерак није пронађен',
                    error_message=f'Примерак са каталошким бројем {catalog_number} није пронађен у систему.',
                ),
                404,
            )

        displayed_fields = {}
        if selected_fields:
            for field in selected_fields:
                if field in specimen:
                    value = specimen[field]
                    displayed_fields[field] = 'Да' if isinstance(value, bool) and value else 'Не' if isinstance(value, bool) else value
        else:
            for key, value in specimen.items():
                if value is not None and value != '':
                    displayed_fields[key] = 'Да' if isinstance(value, bool) and value else 'Не' if isinstance(value, bool) else value

        db_name_map = {
            'meteorite': 'meteorites',
            'botany': 'botany',
            'paleozoology': 'paleozoology',
        }
        entity_id = specimen.get('catalog_number', catalog_number)
        db_name = db_name_map.get(collection_type, collection_type)
        image_url = f"/api/specimen_image/{db_name}/{collection_type}/{entity_id}"

        return render_template(
            'specimen_qr_view.html',
            specimen=specimen,
            displayed_fields=displayed_fields,
            field_labels=QR_SPECIMEN_FIELD_LABELS,
            catalog_number=catalog_number,
            collection_name=QR_SPECIMEN_COLLECTION_NAMES.get(collection_type, collection_type),
            collection_url=QR_SPECIMEN_COLLECTION_URLS.get(collection_type, '/'),
            title_field=QR_SPECIMEN_TITLE_FIELDS.get(collection_type, 'catalog_number'),
            display_mode=display_mode,
            show_image=show_image,
            image_url=image_url,
            scan_time=datetime.now().strftime('%d.%m.%Y %H:%M'),
        )
    except Exception as exc:
        logger.error("Error displaying QR view: %s", exc)
        return (
            render_template(
                'error.html',
                error_title='Грешка',
                error_message='Дошло је до грешке при приказу примерка.',
            ),
            500,
        )
