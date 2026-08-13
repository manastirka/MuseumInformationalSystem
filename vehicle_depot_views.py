"""Shared route implementations for vehicle and depot views."""

import logging

from flask import flash, jsonify, make_response, redirect, render_template, request, session, url_for
import audit_support
from psycopg.rows import dict_row

from postgres_service import get_postgres_connection

logger = logging.getLogger(__name__)


def render_vehicle_reservations(*, get_museum_vehicles, get_vehicle_reservations):
    """Render the vehicle reservation page."""
    response = make_response(
        render_template(
            'vehicle_reservations.html',
            vehicles=get_museum_vehicles(),
            reservations=get_vehicle_reservations(),
        )
    )
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response


def handle_add_vehicle_reservation(*, phase3a_databases, get_vehicle_reservations):
    """Create a vehicle reservation. PostgreSQL is the only store."""
    vehicle_id_raw = request.form.get('vehicle_id')
    if not vehicle_id_raw:
        flash('Недостаје ID возила.', 'error')
        return redirect(url_for('vehicles.vehicle_reservations'))
    try:
        vehicle_id = int(vehicle_id_raw)
    except (ValueError, TypeError):
        flash('Неважећи ID возила.', 'error')
        return redirect(url_for('vehicles.vehicle_reservations'))

    if phase3a_databases is None:
        logger.error("Rezervacija nije kreirana: PostgreSQL backend nije dostupan")
        flash('База података није доступна. Резервација није сачувана.', 'error')
        return redirect(url_for('vehicles.vehicle_reservations'))

    conn = None
    try:
        conn = phase3a_databases.get_db_connection()
        cur = conn.cursor()
        cur.execute(
            """
            INSERT INTO vehicle_reservations (
                vehicle_id, reserved_by, purpose, start_date, end_date,
                start_time, end_time, destination, estimated_km,
                driver_name, driver_license, passengers, notes, status
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            -- approved_by/approved_at ostaju NULL (rezervacija još nije odobrena);
            -- id, created_at, updated_at popunjava šema (SERIAL / DEFAULT now()).
            """,
            (
                vehicle_id,
                request.form.get('employee_name', '').strip()
                or session.get('user_email', 'system'),
                request.form.get('purpose', '').strip(),
                request.form.get('start_date', '').strip(),
                request.form.get('end_date', '').strip(),
                request.form.get('start_time', '').strip() or None,
                request.form.get('end_time', '').strip() or None,
                request.form.get('destination', '').strip(),
                request.form.get('estimated_km', '').strip() or None,
                request.form.get('driver_name', '').strip() or None,
                request.form.get('driver_license', '').strip() or None,
                request.form.get('passengers', '').strip() or None,
                request.form.get('notes', '').strip(),
                'Активна',
            ),
        )
        conn.commit()
        cur.close()
        flash('Резервација је успешно креирана!', 'success')
        get_vehicle_reservations(force_reload=True)
    except Exception as exc:
        if conn is not None:
            conn.rollback()
        from psycopg import errors as pg_errors
        if isinstance(exc, pg_errors.ExclusionViolation):
            # EXCLUDE ograničenje (migr. 049): vozilo je već rezervisano u
            # izabranom periodu — konflikt, ne tehnička greška.
            logger.info("Odbijena preklopljena rezervacija vozila %s", vehicle_id)
            flash('Возило је већ резервисано у изабраном периоду. '
                  'Изаберите други термин или друго возило.', 'error')
        else:
            logger.exception("Error adding reservation to PostgreSQL")
            flash('Грешка при креирању резервације. Покушајте поново.', 'error')
    finally:
        if conn is not None:
            conn.close()

    return redirect(url_for('vehicles.vehicle_reservations'))


def render_vehicle_management(*, get_museum_vehicles, get_vehicle_reservations):
    """Render the vehicle management page."""
    return render_template(
        'vehicle_management.html',
        vehicles=get_museum_vehicles(),
        reservations=get_vehicle_reservations(),
    )


def handle_add_vehicle(*, phase3a_databases, get_museum_vehicles):
    """Add a new vehicle. PostgreSQL is the only store."""
    vehicle_data = {
        'name': request.form.get('name', '').strip(),
        'registration': request.form.get('registration', '').strip(),
        'type': request.form.get('type', '').strip(),
        'capacity': request.form.get('capacity', '').strip(),
        'status': request.form.get('status', 'Активно').strip(),
        'year': request.form.get('year', '').strip(),
        'make_model': request.form.get('make_model', '').strip(),
        'notes': request.form.get('notes', '').strip(),
        'image_ids': [],
    }

    if phase3a_databases is None:
        logger.error("Vozilo nije dodato: PostgreSQL backend nije dostupan")
        flash('База података није доступна. Возило није сачувано.', 'error')
        return redirect(url_for('vehicles.vehicle_management'))

    conn = None
    try:
        conn = phase3a_databases.get_db_connection()
        cur = conn.cursor()
        # Ova INSERT lista pokriva SVE kolone koje obrazac za dodavanje vozila
        # (templates/vehicle_management.html) zaista prikuplja. Namerno izostavljene:
        #   - id, created_at, updated_at  -> šema (SERIAL / DEFAULT now());
        #   - vin, model_variant, max_mass_kg, curb_mass_kg, engine_displacement_cc,
        #     engine_power_kw, fuel_type, fuel_consumption -> tehničke specifikacije
        #     koje UI ne unosi; ostaju NULL i pune se uvozom/rekonciliacijom
        #     (scripts/migration/migrate_vehicles_json_to_pg.py).
        cur.execute(
            """
            INSERT INTO vehicles (
                name, registration, type, capacity, status,
                year, make_model, notes, image_ids
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """,
            (
                vehicle_data['name'],
                vehicle_data['registration'],
                vehicle_data['type'],
                vehicle_data['capacity'],
                vehicle_data['status'],
                vehicle_data['year'],
                vehicle_data['make_model'],
                vehicle_data['notes'],
                vehicle_data['image_ids'],
            ),
        )
        conn.commit()
        cur.close()
        flash('Возило је успешно додато!', 'success')
        get_museum_vehicles(force_reload=True)
    except Exception as exc:
        if conn is not None:
            conn.rollback()
        logger.error("Error adding vehicle to PostgreSQL: %s", exc)
        flash('Грешка при додавању возила.', 'error')
    finally:
        if conn is not None:
            conn.close()

    return redirect(url_for('vehicles.vehicle_management'))


def handle_edit_vehicle(*, phase3a_databases, get_museum_vehicles):
    """Edit an existing vehicle. PostgreSQL is the only store."""
    vehicle_id_raw = request.form.get('vehicle_id')
    if not vehicle_id_raw:
        flash('Недостаје ID возила.', 'error')
        return redirect(url_for('vehicles.vehicle_management'))
    try:
        vehicle_id = int(vehicle_id_raw)
    except (ValueError, TypeError):
        flash('Неважећи ID возила.', 'error')
        return redirect(url_for('vehicles.vehicle_management'))

    if phase3a_databases is None:
        logger.error("Vozilo nije ažurirano: PostgreSQL backend nije dostupan")
        flash('База података није доступна. Измене нису сачуване.', 'error')
        return redirect(url_for('vehicles.vehicle_management'))

    conn = None
    try:
        conn = phase3a_databases.get_db_connection()
        cur = conn.cursor()
        cur.execute(
            """
            UPDATE vehicles SET
                name = %s,
                registration = %s,
                type = %s,
                capacity = %s,
                status = %s,
                year = %s,
                make_model = %s,
                notes = %s,
                updated_at = now()
            WHERE id = %s
            """,
            (
                request.form.get('name', '').strip(),
                request.form.get('registration', '').strip(),
                request.form.get('type', '').strip(),
                request.form.get('capacity', '').strip(),
                request.form.get('status', '').strip(),
                request.form.get('year', '').strip(),
                request.form.get('make_model', '').strip(),
                request.form.get('notes', '').strip(),
                vehicle_id,
            ),
        )
        conn.commit()
        cur.close()
        flash('Возило је успешно ажурирано!', 'success')
        get_museum_vehicles(force_reload=True)
    except Exception as exc:
        if conn is not None:
            conn.rollback()
        logger.error("Error updating vehicle in PostgreSQL: %s", exc)
        flash('Грешка при ажурирању возила. Покушајте поново.', 'error')
    finally:
        if conn is not None:
            conn.close()

    return redirect(url_for('vehicles.vehicle_management'))


def handle_delete_vehicle(
    *,
    phase3a_databases,
    get_museum_vehicles,
):
    """Delete a vehicle. PostgreSQL is the only store."""
    vehicle_id_raw = request.form.get('vehicle_id')
    if not vehicle_id_raw:
        flash('Недостаје ID возила.', 'error')
        return redirect(url_for('vehicles.vehicle_management'))
    try:
        vehicle_id = int(vehicle_id_raw)
    except (ValueError, TypeError):
        flash('Неважећи ID возила.', 'error')
        return redirect(url_for('vehicles.vehicle_management'))

    if phase3a_databases is None:
        logger.error("Vozilo nije obrisano: PostgreSQL backend nije dostupan")
        flash('База података није доступна. Возило није обрисано.', 'error')
        return redirect(url_for('vehicles.vehicle_management'))

    conn = None
    try:
        conn = phase3a_databases.get_db_connection()
        cur = conn.cursor()
        cur.execute(
            """
            SELECT COUNT(*) FROM vehicle_reservations
            WHERE vehicle_id = %s
            AND status = 'Активна'
            AND end_date >= CURRENT_DATE
            """,
            (vehicle_id,),
        )
        active_count = cur.fetchone()[0]

        if active_count > 0:
            flash('Не можете обрисати возило које има активне резервације!', 'error')
        else:
            cur.execute("DELETE FROM vehicles WHERE id = %s", (vehicle_id,))
            conn.commit()
            audit_support.record_audit(
                action=audit_support.ACTION_DELETE,
                entity_type='vehicle',
                entity_id=vehicle_id,
                summary=f'Обрисано возило #{vehicle_id}',
            )
            flash('Возило је успешно обрисано!', 'success')
            get_museum_vehicles(force_reload=True)

        cur.close()
    except Exception as exc:
        if conn is not None:
            conn.rollback()
        logger.error("Error deleting vehicle from PostgreSQL: %s", exc)
        flash('Грешка при брисању возила. Покушајте поново.', 'error')
    finally:
        if conn is not None:
            conn.close()

    return redirect(url_for('vehicles.vehicle_management'))


def render_virtual_depot():
    """Render the virtual depot page."""
    return render_template('admin_virtual_depot.html')


def api_get_depot_boxes():
    """Return all depot boxes with mineral counts."""
    try:
        with get_postgres_connection(row_factory=dict_row) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT
                        storage_location as box_id,
                        COUNT(*) as mineral_count
                    FROM minerals
                    WHERE storage_location IS NOT NULL
                    AND storage_location != ''
                    AND storage_location ~ '^[0-9]+[AB]?$'
                    GROUP BY storage_location
                    ORDER BY
                        CAST(REGEXP_REPLACE(storage_location, '[^0-9]', '', 'g') AS INTEGER),
                        storage_location
                    """
                )
                boxes = cur.fetchall()

        return jsonify(
            {
                'success': True,
                'boxes': [dict(row) for row in boxes],
                'total_boxes': len(boxes),
            }
        )
    except Exception as exc:
        logger.error("Error fetching depot boxes: %s", exc)
        return jsonify({'success': False, 'message': str(exc)}), 500


def api_get_box_contents(box_id):
    """Return the contents of a specific depot box."""
    try:
        with get_postgres_connection(row_factory=dict_row) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT
                        id,
                        inventory_number,
                        item_name,
                        card_locality,
                        quantity,
                        description,
                        donor,
                        acquisition_method
                    FROM minerals
                    WHERE storage_location = %s
                    ORDER BY inventory_number
                    """,
                    (box_id,),
                )
                minerals = cur.fetchall()

        return jsonify(
            {
                'success': True,
                'box_id': box_id,
                'minerals': [dict(row) for row in minerals],
                'count': len(minerals),
            }
        )
    except Exception as exc:
        logger.error("Error fetching box contents: %s", exc)
        return jsonify({'success': False, 'message': str(exc)}), 500
