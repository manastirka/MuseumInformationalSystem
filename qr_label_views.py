"""Shared route implementations for QR specimen selection and label rendering."""

import base64
import logging
from io import BytesIO

import qrcode
from flask import flash, redirect, render_template, request, session, url_for

logger = logging.getLogger(__name__)

QR_BASE_URL = "http://192.168.144.48"
MAX_SPECIMENS = 100


def _build_qr_image_data(url, *, version=1, box_size=5, border=1):
    qr = qrcode.QRCode(version=version, box_size=box_size, border=border)
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()


def render_admin_qr_select_specimens(
    collection_type,
    *,
    normalize_qr_collection_type,
    ensure_qr_collection_access,
    get_qr_collection_name,
    get_qr_collection_url,
    get_mineral_database,
    get_qr_collection_records,
    get_qr_record_identifier,
    get_qr_record_catalog_label,
    get_qr_record_name,
    get_qr_record_summary,
    get_qr_record_location,
):
    """Specimen selection interface with filters."""
    collection_type = normalize_qr_collection_type(collection_type)
    access_redirect = ensure_qr_collection_access(collection_type)
    if access_redirect:
        return access_redirect

    collection_info = {
        'type': collection_type,
        'name': get_qr_collection_name(collection_type),
        'url': get_qr_collection_url(collection_type),
    }
    specimens = []

    try:
        if collection_type == 'minerals':
            inv_from = request.args.get('inv_from', type=int)
            inv_to = request.args.get('inv_to', type=int)
            location = request.args.get('location', '').strip()
            locality = request.args.get('locality', '').strip()

            mineral_db = get_mineral_database()
            if mineral_db and mineral_db.available:
                result = mineral_db.get_all_minerals(page=1, per_page=10000)
                if result and isinstance(result, dict) and 'minerals' in result:
                    for mineral in result['minerals']:
                        if not mineral or not isinstance(mineral, dict):
                            continue

                        if inv_from is not None or inv_to is not None:
                            inv_num = mineral.get('inventarni_broj')
                            if inv_num is None:
                                continue
                            try:
                                inv_num_int = int(float(inv_num))
                            except (ValueError, TypeError):
                                continue
                            if inv_from is not None and inv_num_int < inv_from:
                                continue
                            if inv_to is not None and inv_num_int > inv_to:
                                continue

                        if location and location.lower() not in (mineral.get('gde_se_nalazi') or '').lower():
                            continue
                        if locality and locality.lower() not in (mineral.get('lokalitet') or '').lower():
                            continue

                        specimens.append(mineral)
        else:
            catalog_number = request.args.get('catalog_number', '').strip()
            name = request.args.get('name', '').strip()
            location = request.args.get('location', '').strip()

            for record in get_qr_collection_records(collection_type):
                identifier = get_qr_record_identifier(record, collection_type)
                if not identifier:
                    continue

                specimen = {
                    'id': identifier,
                    'catalog_number': get_qr_record_catalog_label(record, collection_type),
                    'name': get_qr_record_name(record, collection_type),
                    'classification': get_qr_record_summary(record, collection_type),
                    'location': get_qr_record_location(record, collection_type),
                }

                if catalog_number and catalog_number.upper() not in specimen['catalog_number'].upper():
                    continue
                if name and name.lower() not in specimen['name'].lower():
                    continue
                if location and location.lower() not in specimen['location'].lower():
                    continue

                specimens.append(specimen)
    except Exception as exc:
        logger.error("Error filtering specimens: %s", exc)
        flash('Грешка при филтрирању.', 'error')

    return render_template(
        'admin_qr_select_specimens.html',
        collection=collection_info,
        specimens=specimens,
    )


def handle_admin_qr_labels_selected(
    collection_type,
    *,
    normalize_qr_collection_type,
    ensure_qr_collection_access,
    get_mineral_database,
    get_qr_collection_records,
    get_qr_record_identifier,
    get_qr_record_catalog_label,
    get_qr_record_name,
    build_collection_highlight_qr_url,
    get_qr_collection_name,
):
    """Generate QR codes for selected specimens only."""
    collection_type = normalize_qr_collection_type(collection_type)
    access_redirect = ensure_qr_collection_access(collection_type)
    if access_redirect:
        return access_redirect

    specimen_ids = request.form.getlist('specimen_ids')
    if not specimen_ids:
        flash('Морате изабрати бар један примерак.', 'warning')
        return redirect(url_for('admin_qr_select_specimens', collection_type=collection_type))
    if len(specimen_ids) > MAX_SPECIMENS:
        flash(
            f'Можете изабрати максимум {MAX_SPECIMENS} примерака одједном. Тренутно изабрано: {len(specimen_ids)}. Молимо смањите број изабраних примерака.',
            'warning',
        )
        return redirect(url_for('admin_qr_select_specimens', collection_type=collection_type))

    logger.info("Generating QR codes for %s specimens from collection %s", len(specimen_ids), collection_type)
    labels = []

    try:
        if collection_type == 'minerals':
            mineral_db = get_mineral_database()
            if mineral_db and mineral_db.available:
                for specimen_id in specimen_ids:
                    try:
                        mineral = mineral_db.get_mineral_by_id(int(specimen_id))
                        if not mineral:
                            continue
                        qr_url = f"{QR_BASE_URL}/admin/mineral_detail/{mineral['id']}"
                        labels.append(
                            {
                                'catalog_number': mineral.get('inventarni_broj_display', 'N/A'),
                                'name': mineral.get('naziv', 'Непознато'),
                                'qr_code': _build_qr_image_data(qr_url),
                                'url': qr_url,
                            }
                        )
                    except Exception as exc:
                        logger.error("Error processing mineral %s: %s", specimen_id, exc)
        else:
            record_lookup = {}
            for record in get_qr_collection_records(collection_type):
                identifier = get_qr_record_identifier(record, collection_type)
                if identifier:
                    record_lookup[identifier] = record

            for specimen_id in specimen_ids:
                record = record_lookup.get(str(specimen_id))
                if not record:
                    continue
                qr_url = build_collection_highlight_qr_url(QR_BASE_URL, collection_type, specimen_id)
                labels.append(
                    {
                        'catalog_number': get_qr_record_catalog_label(record, collection_type),
                        'name': get_qr_record_name(record, collection_type),
                        'qr_code': _build_qr_image_data(qr_url),
                        'url': qr_url,
                    }
                )

        session['qr_generated_data'] = {
            'labels': labels,
            'collection_info': {
                'type': collection_type,
                'name': get_qr_collection_name(collection_type),
                'count': len(labels),
            },
            'selected_specimens': specimen_ids,
            'back_url': url_for('admin_qr_select_specimens', collection_type=collection_type),
        }
        return redirect(url_for('admin_qr_label_format', collection_type=collection_type))
    except Exception as exc:
        logger.exception("Error generating selected QR codes")
        flash('Грешка при генерисању QR кодова.', 'error')
        return redirect(url_for('admin_qr_select_specimens', collection_type=collection_type))


def render_admin_qr_label_format(
    collection_type,
    *,
    normalize_qr_collection_type,
    ensure_qr_collection_access,
    get_qr_collection_name,
    get_qr_collection_url,
):
    """Show label format selection for QR code generation."""
    collection_type = normalize_qr_collection_type(collection_type)
    if collection_type != 'mineral_boxes':
        access_redirect = ensure_qr_collection_access(collection_type)
        if access_redirect:
            return access_redirect

    logger.info("Format selection route called for collection_type: %s", collection_type)

    collection_info = {
        'type': collection_type,
        'name': 'Кутије минералошке збирке'
        if collection_type == 'mineral_boxes'
        else get_qr_collection_name(collection_type),
    }

    stored_data = session.get('qr_generated_data', {})
    back_url = stored_data.get('back_url')
    if not back_url:
        back_url = (
            url_for('admin_qr_mineral_boxes')
            if collection_type == 'mineral_boxes'
            else get_qr_collection_url(collection_type)
        )

    return render_template(
        'admin_qr_label_format.html',
        collection=collection_info,
        continue_url=url_for('admin_qr_labels_with_format', collection_type=collection_type),
        back_url=back_url,
    )


def handle_admin_qr_labels_with_format(
    collection_type,
    *,
    normalize_qr_collection_type,
    ensure_qr_collection_access,
    get_qr_collection_url,
):
    """Render QR codes with the selected label format."""
    collection_type = normalize_qr_collection_type(collection_type)
    if collection_type != 'mineral_boxes':
        access_redirect = ensure_qr_collection_access(collection_type)
        if access_redirect:
            return access_redirect

    label_format = request.form.get('label_format', '1')
    print_mode = request.form.get('print_mode', 'regular')

    logger.info("Received form data - label_format: %s, print_mode: %s", label_format, print_mode)
    logger.info("Form data: %s", dict(request.form))

    if 'qr_generated_data' not in session:
        flash('Грешка: Нема података за генерисање QR кодова.', 'error')
        if collection_type == 'mineral_boxes':
            return redirect(url_for('admin_qr_mineral_boxes'))
        return redirect(get_qr_collection_url(collection_type))

    stored_data = session['qr_generated_data']
    labels = stored_data['labels']
    collection_info = stored_data['collection_info']
    back_url = stored_data.get('back_url')
    if not back_url:
        back_url = (
            url_for('admin_qr_mineral_boxes')
            if collection_type == 'mineral_boxes'
            else get_qr_collection_url(collection_type)
        )

    if print_mode == 'regular':
        collection_info['label_format'] = None
        collection_info['print_mode'] = 'regular'
        return render_template(
            'admin_qr_labels.html',
            labels=labels,
            collection=collection_info,
            is_box_mode=stored_data.get('is_box_mode', False),
            back_url=back_url,
        )

    collection_info['label_format'] = label_format
    collection_info['print_mode'] = print_mode
    logger.info("Rendering labels with format: %s, mode: %s", label_format, print_mode)
    logger.info("Collection info: %s", collection_info)

    session.pop('qr_generated_data', None)
    logger.info("Final collection_info before template: %s", collection_info)
    return render_template(
        'admin_qr_labels.html',
        labels=labels,
        collection=collection_info,
        is_box_mode=stored_data.get('is_box_mode', False),
        back_url=back_url,
    )


def render_admin_qr_labels(
    collection_type,
    *,
    normalize_qr_collection_type,
    ensure_qr_collection_access,
    get_mineral_database,
    get_qr_collection_records,
    get_qr_record_identifier,
    get_qr_record_catalog_label,
    get_qr_record_name,
    build_collection_highlight_qr_url,
    get_qr_collection_name,
    get_qr_collection_url,
):
    """Generate printable QR code labels for a collection."""
    collection_type = normalize_qr_collection_type(collection_type)
    access_redirect = ensure_qr_collection_access(collection_type)
    if access_redirect:
        return access_redirect

    labels = []

    try:
        if collection_type == 'minerals':
            mineral_db = get_mineral_database()
            if mineral_db and mineral_db.available:
                result = mineral_db.get_all_minerals(page=1, per_page=100)
                if result and isinstance(result, dict) and 'minerals' in result:
                    for mineral in result['minerals']:
                        if not mineral or not isinstance(mineral, dict) or 'id' not in mineral:
                            continue
                        qr_url = f"{QR_BASE_URL}/admin/mineral_detail/{mineral['id']}"
                        labels.append(
                            {
                                'catalog_number': mineral.get('inventarni_broj_display', 'N/A'),
                                'name': mineral.get('naziv', 'Непознато'),
                                'qr_code': _build_qr_image_data(qr_url, box_size=10, border=2),
                                'url': qr_url,
                            }
                        )
        else:
            for record in get_qr_collection_records(collection_type):
                identifier = get_qr_record_identifier(record, collection_type)
                if not identifier:
                    continue
                qr_url = build_collection_highlight_qr_url(QR_BASE_URL, collection_type, identifier)
                labels.append(
                    {
                        'catalog_number': get_qr_record_catalog_label(record, collection_type),
                        'name': get_qr_record_name(record, collection_type),
                        'qr_code': _build_qr_image_data(qr_url, box_size=10, border=2),
                        'url': qr_url,
                    }
                )

        session['qr_generated_data'] = {
            'labels': labels,
            'collection_info': {
                'type': collection_type,
                'name': get_qr_collection_name(collection_type),
                'count': len(labels),
            },
            'all_specimens': True,
            'back_url': get_qr_collection_url(collection_type),
        }
        return redirect(url_for('admin_qr_label_format', collection_type=collection_type))
    except Exception:
        logger.exception("Error generating QR codes")
        flash('Грешка при генерисању QR кодова.', 'error')
        return redirect(get_qr_collection_url(collection_type))
