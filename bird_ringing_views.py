"""Shared route implementations for bird ringing views."""

import logging

from flask import flash, redirect, render_template, request, url_for

logger = logging.getLogger(__name__)


def render_bird_ringing_database(*, bird_ringing_database, museum_databases_endpoint):
    """Render the bird ringing database view."""
    try:
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 50))
        search = request.args.get('search', '').strip() or None
        species_filter = request.args.get('species', '').strip() or None
        location_filter = request.args.get('location', '').strip() or None
        ringer_filter = request.args.get('ringer', '').strip() or None
        year_filter = request.args.get('year', '').strip() or None

        records, total_count, total_pages = bird_ringing_database.get_all_records(
            page=page,
            per_page=per_page,
            search=search,
            species_filter=species_filter,
            location_filter=location_filter,
            ringer_filter=ringer_filter,
            year_filter=year_filter,
        )

        return render_template(
            'admin_bird_ringing_database.html',
            records=records,
            total_count=total_count,
            total_pages=total_pages,
            current_page=page,
            per_page=per_page,
            all_species=bird_ringing_database.get_all_species(),
            all_locations=bird_ringing_database.get_all_locations(),
            all_ringers=bird_ringing_database.get_all_ringers(),
            all_years=bird_ringing_database.get_all_years(),
            stats=bird_ringing_database.get_statistics(),
            search=search or '',
            species_filter=species_filter or '',
            location_filter=location_filter or '',
            ringer_filter=ringer_filter or '',
            year_filter=year_filter or '',
        )
    except FileNotFoundError:
        flash(
            'База података о прстеновању птица још увек није учитана. Покрените скрипту за увоз података.',
            'error',
        )
        return redirect(url_for(museum_databases_endpoint))
    except Exception as exc:
        logger.error("Error loading bird ringing database: %s", exc)
        flash('Грешка при учитавању базе података.', 'error')
        return redirect(url_for(museum_databases_endpoint))


def render_bird_ringing_record_detail(*, record_id, bird_ringing_database, list_endpoint):
    """Render a single bird ringing record detail page."""
    try:
        record = bird_ringing_database.get_record_by_id(record_id)
        if not record:
            flash('Запис није пронађен.', 'error')
            return redirect(url_for(list_endpoint))
        return render_template('admin_bird_ringing_detail.html', record=record)
    except Exception as exc:
        logger.error("Error loading bird ringing record %s: %s", record_id, exc)
        flash('Грешка при учитавању записа.', 'error')
        return redirect(url_for(list_endpoint))


def handle_add_bird_ringing(*, bird_ringing_database, detail_endpoint, list_endpoint):
    """Handle add-bird-ringing form rendering and submission."""
    if request.method == 'POST':
        try:
            record_data = {
                'ring_number': request.form.get('ring_number', '').strip() or None,
                'color_ring': request.form.get('color_ring', '').strip() or None,
                'species': request.form.get('species', '').strip() or None,
                'age': request.form.get('age', '').strip() or None,
                'sex': request.form.get('sex', '').strip() or None,
                'location': request.form.get('location', '').strip() or None,
                'coordinates': request.form.get('coordinates', '').strip() or None,
                'coordinate_accuracy': request.form.get('coordinate_accuracy', '').strip() or None,
                'date': request.form.get('date', '').strip() or None,
                'time': request.form.get('time', '').strip() or None,
                'metal_ring_position': request.form.get('metal_ring_position', '').strip() or None,
                'plastic_ring': request.form.get('plastic_ring', '').strip() or None,
                'catching_method': request.form.get('catching_method', '').strip() or None,
                'bait': request.form.get('bait', '').strip() or None,
                'manipulation': request.form.get('manipulation', '').strip() or None,
                'status': request.form.get('status', '').strip() or None,
                'clutch_size': request.form.get('clutch_size', '').strip() or None,
                'pullus_age': request.form.get('pullus_age', '').strip() or None,
                'wing_length': request.form.get('wing_length', '').strip() or None,
                'third_primary_feather': request.form.get('third_primary_feather', '').strip() or None,
                'mass': request.form.get('mass', '').strip() or None,
                'molting': request.form.get('molting', '').strip() or None,
                'back_claw': request.form.get('back_claw', '').strip() or None,
                'bill_length': request.form.get('bill_length', '').strip() or None,
                'bill_measurement_method': request.form.get('bill_measurement_method', '').strip() or None,
                'head_length': request.form.get('head_length', '').strip() or None,
                'tarsus': request.form.get('tarsus', '').strip() or None,
                'tarsus_measurement_method': request.form.get('tarsus_measurement_method', '').strip() or None,
                'tail_length': request.form.get('tail_length', '').strip() or None,
                'fat_deposits': request.form.get('fat_deposits', '').strip() or None,
                'pectoral_muscle': request.form.get('pectoral_muscle', '').strip() or None,
                'incubation_patch': request.form.get('incubation_patch', '').strip() or None,
                'alula': request.form.get('alula', '').strip() or None,
                'carpal_feathers': request.form.get('carpal_feathers', '').strip() or None,
                'sex_determination': request.form.get('sex_determination', '').strip() or None,
                'protected_areas': request.form.get('protected_areas', '').strip() or None,
                'ringer': request.form.get('ringer', '').strip() or None,
                'notes': request.form.get('notes', '').strip() or None,
            }

            record_id = bird_ringing_database.insert_record(record_data)
            flash(f'Запис о прстеновању је успешно додат! (ID: {record_id})', 'success')
            return redirect(url_for(detail_endpoint, record_id=record_id))
        except Exception as exc:
            logger.error("Error adding bird ringing record: %s", exc)
            flash('Грешка при додавању записа.', 'error')
            return redirect(url_for('add_bird_ringing'))

    try:
        return render_template(
            'admin_add_bird_ringing.html',
            all_species=bird_ringing_database.get_all_species(),
            all_locations=bird_ringing_database.get_all_locations(),
            all_ringers=bird_ringing_database.get_all_ringers(),
        )
    except Exception as exc:
        logger.error("Error loading bird ringing form: %s", exc)
        flash('Грешка при учитавању форме.', 'error')
        return redirect(url_for(list_endpoint))
