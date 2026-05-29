"""Shared route implementations for the initial QR management flow."""

import base64
import logging
from io import BytesIO
from urllib.parse import quote

import qrcode
from flask import flash, redirect, render_template, request, session, url_for

logger = logging.getLogger(__name__)

QR_FIELD_DEFINITIONS = {
    'meteorite': [
        {'id': 'catalog_number', 'label': 'Каталошки број', 'default': True, 'description': 'Идентификациони број примерка'},
        {'id': 'meteorite_name', 'label': 'Назив метеорита', 'default': True, 'description': 'Службени назив метеорита'},
        {'id': 'classification', 'label': 'Класификација', 'default': True, 'description': 'Научна класификација'},
        {'id': 'fall_type', 'label': 'Тип пада', 'default': True, 'description': 'Пад или налаз'},
        {'id': 'fall_date', 'label': 'Датум пада', 'default': True, 'description': 'Када је пао метеорит'},
        {'id': 'location_found', 'label': 'Локација налаза', 'default': True, 'description': 'Где је пронађен'},
        {'id': 'total_mass_kg', 'label': 'Укупна маса (kg)', 'default': False, 'description': 'Тежина у килограмима'},
        {'id': 'specimen_mass', 'label': 'Маса примерка', 'default': False, 'description': 'Маса овог примерка'},
        {'id': 'description', 'label': 'Опис', 'default': False, 'description': 'Детаљан опис примерка'},
        {'id': 'source', 'label': 'Извор', 'default': False, 'description': 'Како је примерак набављен'},
        {'id': 'curator', 'label': 'Кустос', 'default': False, 'description': 'Одговорно лице'},
    ],
    'botany': [
        {'id': 'catalog_number', 'label': 'Каталошки број', 'default': True},
        {'id': 'scientific_name', 'label': 'Научно име', 'default': True},
        {'id': 'common_name_sr', 'label': 'Народно име', 'default': True},
        {'id': 'family', 'label': 'Фамилија', 'default': True},
        {'id': 'habitat', 'label': 'Станиште', 'default': True},
        {'id': 'location_found', 'label': 'Локација', 'default': False},
        {'id': 'date_collected', 'label': 'Датум прикупљања', 'default': False},
        {'id': 'collector', 'label': 'Сакупљач', 'default': False},
        {'id': 'conservation_status', 'label': 'Статус заштите', 'default': False},
        {'id': 'description', 'label': 'Опис', 'default': False},
    ],
    'paleozoology': [
        {'id': 'catalog_number', 'label': 'Каталошки број', 'default': True},
        {'id': 'scientific_name', 'label': 'Научно име', 'default': True},
        {'id': 'common_name_sr', 'label': 'Народно име', 'default': True},
        {'id': 'geological_period', 'label': 'Геолошки период', 'default': True},
        {'id': 'age_million_years', 'label': 'Старост (мил. год.)', 'default': True},
        {'id': 'location_found', 'label': 'Локација налаза', 'default': True},
        {'id': 'class', 'label': 'Класа', 'default': False},
        {'id': 'order', 'label': 'Ред', 'default': False},
        {'id': 'family', 'label': 'Фамилија', 'default': False},
        {'id': 'description', 'label': 'Опис', 'default': False},
    ],
}

QR_COLLECTION_NAMES = {
    'meteorite': 'Збирка метеорита',
    'botany': 'Ботаничка збирка',
    'paleozoology': 'Палеозоолошка збирка',
}

QR_BASE_URL = "http://192.168.144.48"


def _build_qr_image_data(url, *, version=1, box_size=10, border=2):
    qr = qrcode.QRCode(version=version, box_size=box_size, border=border)
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()


def render_admin_qr_generator(*, user_has_module_access):
    """Legacy QR generator entry point kept as a redirect."""
    flash('QR генератор је премештен у сваку појединачну збирку.', 'info')

    user_email = session.get('user_email', '')
    user_role = session.get('user_role', 'user')
    if user_has_module_access(user_email, user_role, 'museum_databases'):
        return redirect(url_for('museum_databases'))
    return redirect(url_for('dashboard'))


def render_admin_qr_field_selection(collection_type, *, normalize_qr_collection_type, ensure_qr_collection_access):
    """Field selection interface for QR code generation."""
    collection_type = normalize_qr_collection_type(collection_type)
    access_redirect = ensure_qr_collection_access(collection_type)
    if access_redirect:
        return access_redirect

    return render_template(
        'admin_qr_field_selection.html',
        collection_type=collection_type,
        collection_name=QR_COLLECTION_NAMES.get(collection_type, collection_type),
        available_fields=QR_FIELD_DEFINITIONS.get(collection_type, []),
    )


def handle_admin_qr_labels_with_fields(
    collection_type,
    *,
    normalize_qr_collection_type,
    ensure_qr_collection_access,
    get_meteorite_collection_database,
    botany_collection_database,
    paleozoology_collection_database,
):
    """Generate QR codes with a selected field configuration."""
    collection_type = normalize_qr_collection_type(collection_type)
    access_redirect = ensure_qr_collection_access(collection_type)
    if access_redirect:
        return access_redirect

    selected_fields = request.form.getlist('selected_fields')
    display_mode = request.form.get('display_mode', 'card')
    show_image = 'show_image' in request.form

    session['qr_config'] = {
        'fields': selected_fields,
        'display_mode': display_mode,
        'show_image': show_image,
    }

    fields_param = ','.join(selected_fields) if selected_fields else 'all'
    labels = []

    try:
        if collection_type == 'meteorite':
            specimens = get_meteorite_collection_database()['specimens'][:100]
            name_key = 'meteorite_name'
        elif collection_type == 'botany':
            specimens = botany_collection_database['specimens'][:100]
            name_key = 'scientific_name'
        elif collection_type == 'paleozoology':
            specimens = paleozoology_collection_database['specimens'][:100]
            name_key = 'scientific_name'
        else:
            specimens = []
            name_key = 'name'

        for specimen in specimens:
            catalog_num = specimen.get('catalog_number', 'N/A')
            qr_url = (
                f"{QR_BASE_URL}/qr_view/{collection_type}/{catalog_num}"
                f"?fields={fields_param}&mode={display_mode}&img={1 if show_image else 0}"
            )
            labels.append(
                {
                    'catalog_number': catalog_num,
                    'name': specimen.get(name_key, 'Непознато'),
                    'qr_code': _build_qr_image_data(qr_url),
                    'url': qr_url,
                }
            )

        session['qr_generated_data'] = {
            'labels': labels,
            'collection_info': {
                'type': collection_type,
                'name': QR_COLLECTION_NAMES.get(collection_type, collection_type),
                'count': len(labels),
            },
            'fields': selected_fields,
            'display_mode': display_mode,
            'show_image': show_image,
        }

        return redirect(url_for('qr.admin_qr_label_format', collection_type=collection_type))
    except Exception as exc:
        logger.error("Error generating QR codes with fields: %s", exc)
        flash('Грешка при генерисању QR кодова.', 'error')
        return redirect(url_for('qr.admin_qr_field_selection', collection_type=collection_type))


def render_admin_qr_mineral_boxes(*, ensure_qr_collection_access, get_mineral_database):
    """Select mineral storage boxes for QR code generation."""
    access_redirect = ensure_qr_collection_access('minerals')
    if access_redirect:
        return access_redirect

    mineral_db = get_mineral_database()
    if not mineral_db or not mineral_db.available:
        flash('База минерала није доступна.', 'error')
        return redirect(url_for('admin_mineral_collection'))

    result = mineral_db.get_all_minerals(page=1, per_page=10000)
    if not result or 'minerals' not in result:
        flash('Грешка при учитавању минерала.', 'error')
        return redirect(url_for('admin_mineral_collection'))

    boxes = {}
    no_location_count = 0
    minerals = result['minerals']
    for mineral in minerals:
        location = mineral.get('gde_se_nalazi')
        if location and str(location).strip() != '':
            location = str(location).strip()
            boxes.setdefault(location, {'box_number': location, 'minerals': [], 'count': 0})
            boxes[location]['minerals'].append(mineral)
            boxes[location]['count'] += 1
        else:
            no_location_count += 1

    def sort_box_key(box):
        box_num = box['box_number']
        has_comma = ',' in box_num
        try:
            if not has_comma and box_num.strip().isdigit():
                return (0, int(box_num.strip()), box_num)
            return (1, 999999, box_num.lower())
        except Exception:
            return (2, 999999, box_num.lower())

    box_list = sorted(boxes.values(), key=sort_box_key)
    return render_template(
        'admin_qr_mineral_boxes.html',
        boxes=box_list,
        total_boxes=len(box_list),
        no_location_count=no_location_count,
        total_minerals=len(minerals),
    )


def handle_admin_generate_box_qr_codes(*, ensure_qr_collection_access):
    """Generate QR codes for selected mineral boxes."""
    access_redirect = ensure_qr_collection_access('minerals')
    if access_redirect:
        return access_redirect

    selected_boxes = request.form.getlist('selected_boxes')
    if not selected_boxes:
        flash('Морате изабрати бар једну кутију.', 'warning')
        return redirect(url_for('qr.admin_qr_mineral_boxes'))
    if len(selected_boxes) > 10:
        flash('Можете изабрати максимум 10 кутија одједном.', 'warning')
        return redirect(url_for('qr.admin_qr_mineral_boxes'))

    logger.info("Starting QR generation for %s boxes", len(selected_boxes))
    labels = []

    try:
        for box_number in selected_boxes:
            try:
                qr_url = f"{QR_BASE_URL}/qr_box/minerals/{quote(box_number)}"
                labels.append(
                    {
                        'catalog_number': box_number,
                        'name': 'Кутија',
                        'qr_code': _build_qr_image_data(qr_url, box_size=1, border=0),
                        'url': qr_url,
                        'count': 0,
                    }
                )
                logger.info("Generated QR for box %s", box_number)
            except Exception as box_error:
                logger.error("Error generating QR for box %s: %s", box_number, box_error)
                labels.append(
                    {
                        'catalog_number': box_number,
                        'name': 'Кутија (Грешка)',
                        'qr_code': '',
                        'url': f"{QR_BASE_URL}/qr_box/minerals/{box_number}",
                        'count': 0,
                    }
                )
    except Exception as exc:
        logger.error("Error generating QR codes for boxes: %s", exc)
        labels = [
            {
                'catalog_number': box_number,
                'name': 'Кутија (Грешка)',
                'qr_code': '',
                'url': f"{QR_BASE_URL}/qr_box/minerals/{box_number}",
                'count': 0,
            }
            for box_number in selected_boxes
        ]
        session['qr_generated_data'] = {
            'labels': labels,
            'collection_info': {
                'type': 'mineral_boxes',
                'name': 'Кутије минералошке збирке',
                'count': len(labels),
            },
            'selected_boxes': selected_boxes,
            'is_box_mode': True,
            'back_url': url_for('qr.admin_qr_mineral_boxes'),
        }
        flash('Грешка при генерисању QR кодова, али можете изабрати формат.', 'warning')
        return redirect(url_for('qr.admin_qr_label_format', collection_type='mineral_boxes'))

    logger.info("Successfully generated %s QR codes", len(labels))
    if len(labels) == 0:
        flash('Није генерисан ниједан QR код.', 'error')
        return redirect(url_for('qr.admin_qr_mineral_boxes'))

    session['qr_generated_data'] = {
        'labels': labels,
        'collection_info': {
            'type': 'mineral_boxes',
            'name': 'Кутије минералошке збирке',
            'count': len(labels),
        },
        'selected_boxes': selected_boxes,
        'is_box_mode': True,
        'back_url': url_for('qr.admin_qr_mineral_boxes'),
    }
    logger.info("Stored %s labels in session, redirecting to format selection", len(labels))
    return redirect(url_for('qr.admin_qr_label_format', collection_type='mineral_boxes'))
