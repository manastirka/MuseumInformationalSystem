"""Shared route implementations for travel and finance workflows."""

import json
import logging
import os
import random
from datetime import datetime, timedelta
from io import BytesIO

import requests as http_requests
from flask import jsonify, render_template, request, send_file, session

logger = logging.getLogger(__name__)

TOLL_PRICES_FROM_BELGRADE = {
    'MALI POŽAREVAC': 100, 'UMČARI': 140, 'VODANJ': 170, 'KOLARI': 200,
    'SMEDEREVO': 230, 'POŽAREVAC': 240, 'VELIKA PLANA': 400, 'MARKOVAC': 460,
    'LAPOVO': 500, 'BATOČINA': 520, 'JAGODINA': 640, 'ĆUPRIJA': 710,
    'PARAĆIN': 770, 'ĆIĆEVAC': 860, 'KRUŠEVAC': 970, 'KOŠEVI': 1000,
    'VELIKA DRENOVA': 1050, 'TRSTENIK': 1120, 'VRNJAČKA BANJA': 1190,
    'VRBA': 1260, 'RAŽANJ': 900, 'ALEKSINAC': 1050, 'NIŠ': 1180,
    'MEROŠINA': 1210, 'DOLJEVAC': 1270, 'BRESTOVAC': 1300, 'LESKOVAC': 1430,
    'GRDELICA': 1490, 'PREDEJANE': 1580, 'VLADIČIN HAN': 1720, 'VRANJE': 1850,
    'BUJANOVAC': 1940, 'PREŠEVO': 2060,
    'PIROT': 1570, 'BELA PALANKA': 1400, 'DIMITROVGRAD': 1800,
    'MOROVIĆ': 50, 'ADAŠEVCI': 50, 'KUZMIN': 120, 'SREMSKA MITROVICA': 240,
    'RUMA': 320, 'HRTKOVCI': 380, 'ŠABAC': 460, 'PEĆINCI': 380, 'ŠIMANOVCI': 520,
    'STARA PAZOVA': 100, 'INĐIJA': 100, 'MARADIK': 120, 'BEŠKA': 150,
    'KOVILJ': 230, 'NOVI SAD': 340, 'ZMAJEVO': 430, 'VRBAS': 500,
    'FEKETIĆ': 550, 'BAČKA TOPOLA': 670, 'ŽEDNIK': 730, 'SUBOTICA': 850,
    'UB': 150, 'LAJKOVAC': 220, 'LJIG': 360, 'TAKOVO': 540,
    'PRELJINA': 640, 'ČAČAK': 720, 'LUČANI': 860, 'PRILIPAC': 950,
    'STARA PLANINA': 1600, 'ĐERDAP': 500, 'TARA': 800, 'ZLATIBOR': 900,
    'KOPAONIK': 1200, 'FRUŠKA GORA': 300, 'DIVČIBARE': 400,
    'GOLIJA': 1000, 'RTANJ': 800, 'ZLATAR': 850,
}

DESTINATION_COORDS = {
    'STARA PLANINA': {'lat': 43.3667, 'lon': 22.6000, 'km': 320, 'toll_station': 'PIROT'},
    'ĐERDAP': {'lat': 44.6167, 'lon': 21.8833, 'km': 240, 'toll_station': 'POŽAREVAC'},
    'TARA': {'lat': 43.8833, 'lon': 19.5500, 'km': 180, 'toll_station': 'ČAČAK'},
    'ZLATIBOR': {'lat': 43.7333, 'lon': 19.7000, 'km': 230, 'toll_station': 'ČAČAK'},
    'KOPAONIK': {'lat': 43.2833, 'lon': 20.8167, 'km': 290, 'toll_station': 'KRUŠEVAC'},
    'FRUŠKA GORA': {'lat': 45.1500, 'lon': 19.7833, 'km': 90, 'toll_station': 'NOVI SAD'},
    'DIVČIBARE': {'lat': 44.1167, 'lon': 19.9833, 'km': 120, 'toll_station': 'LAJKOVAC'},
    'GOLIJA': {'lat': 43.3667, 'lon': 20.3167, 'km': 260, 'toll_station': 'KRUŠEVAC'},
    'NIŠ': {'lat': 43.3211, 'lon': 21.8958, 'km': 240, 'toll_station': 'NIŠ'},
    'NOVI SAD': {'lat': 45.2517, 'lon': 19.8369, 'km': 95, 'toll_station': 'NOVI SAD'},
    'SUBOTICA': {'lat': 46.1000, 'lon': 19.6667, 'km': 190, 'toll_station': 'SUBOTICA'},
    'VRANJE': {'lat': 42.5500, 'lon': 21.9000, 'km': 340, 'toll_station': 'VRANJE'},
    'PIROT': {'lat': 43.1533, 'lon': 22.5856, 'km': 310, 'toll_station': 'PIROT'},
    'LESKOVAC': {'lat': 42.9983, 'lon': 21.9461, 'km': 280, 'toll_station': 'LESKOVAC'},
    'ČAČAK': {'lat': 43.8914, 'lon': 20.3497, 'km': 150, 'toll_station': 'ČAČAK'},
    'KRUŠEVAC': {'lat': 43.5833, 'lon': 21.3333, 'km': 200, 'toll_station': 'KRUŠEVAC'},
    'VRNJAČKA BANJA': {'lat': 43.6167, 'lon': 20.9000, 'km': 210, 'toll_station': 'VRNJAČKA BANJA'},
    'JAGODINA': {'lat': 43.9833, 'lon': 21.2500, 'km': 140, 'toll_station': 'JAGODINA'},
    'PARAĆIN': {'lat': 43.8667, 'lon': 21.4000, 'km': 160, 'toll_station': 'PARAĆIN'},
    'ŠABAC': {'lat': 44.7500, 'lon': 19.6833, 'km': 90, 'toll_station': 'ŠABAC'},
    'SREMSKA MITROVICA': {'lat': 44.9667, 'lon': 19.6167, 'km': 75, 'toll_station': 'SREMSKA MITROVICA'},
    'VRBAS': {'lat': 45.5667, 'lon': 19.6333, 'km': 140, 'toll_station': 'VRBAS'},
    'ZAJEČAR': {'lat': 43.9000, 'lon': 22.2833, 'km': 250, 'toll_station': 'PARAĆIN'},
    'BOR': {'lat': 44.0833, 'lon': 22.1000, 'km': 240, 'toll_station': 'PARAĆIN'},
    'KLADOVO': {'lat': 44.6167, 'lon': 22.6167, 'km': 260, 'toll_station': 'POŽAREVAC'},
    'NEGOTIN': {'lat': 44.2333, 'lon': 22.5333, 'km': 260, 'toll_station': 'POŽAREVAC'},
    'SJENICA': {'lat': 43.2667, 'lon': 20.0000, 'km': 280, 'toll_station': 'ČAČAK'},
    'NOVI PAZAR': {'lat': 43.1333, 'lon': 20.5167, 'km': 290, 'toll_station': 'KRUŠEVAC'},
    'UŽICE': {'lat': 43.8500, 'lon': 19.8500, 'km': 190, 'toll_station': 'ČAČAK'},
    'VALJEVO': {'lat': 44.2667, 'lon': 19.8833, 'km': 100, 'toll_station': 'LAJKOVAC'},
    'ARANĐELOVAC': {'lat': 44.3000, 'lon': 20.5500, 'km': 75, 'toll_station': None},
    'KRAGUJEVAC': {'lat': 44.0167, 'lon': 20.9167, 'km': 140, 'toll_station': 'BATOČINA'},
    'SMEDEREVO': {'lat': 44.6667, 'lon': 20.9333, 'km': 50, 'toll_station': 'SMEDEREVO'},
    'POŽAREVAC': {'lat': 44.6167, 'lon': 21.1833, 'km': 80, 'toll_station': 'POŽAREVAC'},
    'DIMITROVGRAD': {'lat': 43.0167, 'lon': 22.7833, 'km': 350, 'toll_station': 'DIMITROVGRAD'},
    'BEOGRAD': {'lat': 44.8167, 'lon': 20.4667, 'km': 0, 'toll_station': None},
}

FUEL_PRICES_LOCAL = {
    'Бензин': 174,
    'Дизел': 191,
    'BMB 95': 174,
    'BMB 100': 189,
    'Евродизел': 191,
}

FINANCIAL_PLAN_CATEGORY_NAMES = {
    'akvizicija_teren': '1. АКВИЗИЦИЈА - НАБАВКА МУЗЕЈСКИХ ПРЕДМЕТА НА ТЕРЕНУ',
    'akvizicija_otkup': '2. АКВИЗИЦИЈА - НАБАВКА МУЗЕЈСКИХ ПРЕДМЕТА ОТКУПОМ',
    'prepariranje': '3. ПРЕПАРИРАЊЕ И КОНЗЕРВАЦИЈА',
    'odrzavanje': '4. ОДРЖАВАЊЕ ЗБИРКИ И ДЕПОА',
    'oprema': '5. НАБАВКА НЕОПХОДНЕ ОПРЕМЕ',
    'skupovi': '6. СТРУЧНИ И НАУЧНИ СКУПОВИ',
    'projekti': '7. РЕАЛИЗАЦИЈА СТРУЧНИХ И НАУЧНИХ ПРОЈЕКАТА',
    'izlozbe': '8. ИЗЛОЖБЕНА ДЕЛАТНОСТ',
    'izdavacka': '9. ИЗДАВАЧКА ДЕЛАТНОСТ',
    'literatura': '10. НАБАВКА ЛИТЕРАТУРЕ И ПЕРИОДИКЕ',
    'usavrsavanje': '11. УСАВРШАВАЊЕ И САРАДЊА',
}


def render_financial_requests_page():
    return render_template('zahtevi/finansijski_zahtevi.html', page_title='Финансијски захтеви')


def render_day_off_request_page():
    return render_template(
        'zahtevi/zahtev_slobodan_dan.html',
        page_title='Захтев за слободан дан',
        user_full_name=session.get('user_name', ''),
    )


def render_vacation_request_page():
    return render_template(
        'zahtevi/zahtev_godisnji_odmor.html',
        page_title='Захтев за годишњи одмор',
        user_full_name=session.get('user_name', ''),
    )


def render_misc_request_page():
    return render_template(
        'zahtevi/zahtev_razno.html',
        page_title='Захтев разно',
        user_full_name=session.get('user_name', ''),
    )


def render_financial_plan_page():
    return render_template('finansije/finansijski_plan.html', page_title='Финансијски план')


def render_procurement_request_page():
    return render_template('finansije/zahtev_nabavka.html', page_title='Захтев за набавку')


def render_field_activity_page():
    return render_template('terenska_aktivnost.html', page_title='Теренска активност')


def render_business_trip_request_page(*, get_museum_vehicles):
    vehicles = get_museum_vehicles()
    active_vehicles = [vehicle for vehicle in vehicles if vehicle.get('status') == 'Активно']
    department_heads = [
        {'name': 'др Биљана Митровић', 'role': 'шеф геолошког одељења'},
        {'name': 'Верица Стојановић', 'role': 'шеф биолошког одељења'},
        {'name': 'Душица Ивић', 'role': 'помоћник директора-руководилац одељења финансија'},
    ]
    return render_template(
        'zahtevi/zahtev_sluzbeni_put.html',
        page_title='Захтев за службени пут',
        user_full_name=session.get('user_name', ''),
        vehicles=active_vehicles,
        department_heads=department_heads,
    )


def api_field_trip_create(*, get_vehicle_reservations, save_reservations):
    """Create field trip request with vehicle reservation and timesheet entries."""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'success': False, 'message': 'Нема података'})

        result = {
            'success': True,
            'vehicle_reserved': False,
            'timesheet_updated': False,
            'message': 'Захтев за службени пут је креиран',
        }

        vehicle_id = data.get('vehicle_id')
        if vehicle_id:
            try:
                if os.environ.get('DATABASE_URL'):
                    import psycopg
                    from psycopg.rows import dict_row

                    pg_url = os.environ.get('DATABASE_URL', '').replace('postgresql+psycopg://', 'postgresql://')
                    with psycopg.connect(pg_url, row_factory=dict_row) as conn:
                        with conn.cursor() as cur:
                            cur.execute(
                                """
                                INSERT INTO vehicle_reservations (
                                    vehicle_id, reserved_by, purpose, start_date, end_date,
                                    destination, notes, status
                                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                                """,
                                (
                                    int(vehicle_id),
                                    session.get('user_name', session.get('user_email', 'system')),
                                    f"Теренски рад: {data.get('purpose', '')}",
                                    data.get('start_date'),
                                    data.get('end_date'),
                                    data.get('location', ''),
                                    f"Службени пут - {data.get('location')}",
                                    'Активна',
                                ),
                            )
                            conn.commit()
                            result['vehicle_reserved'] = True
                else:
                    reservations = get_vehicle_reservations()
                    reservations.append(
                        {
                            'id': len(reservations) + 1,
                            'vehicle_id': int(vehicle_id),
                            'employee_name': session.get('user_name', ''),
                            'start_date': data.get('start_date'),
                            'end_date': data.get('end_date'),
                            'purpose': f"Теренски рад: {data.get('purpose', '')}",
                            'destination': data.get('location', ''),
                            'created_by': session.get('user_email', 'system'),
                            'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                        }
                    )
                    save_reservations()
                    result['vehicle_reserved'] = True
            except Exception as exc:
                logger.error("Vehicle reservation error: %s", exc)
                result['vehicle_error'] = str(exc)

        if data.get('update_timesheet') and data.get('start_date') and data.get('end_date'):
            try:
                start = datetime.strptime(data['start_date'], '%Y-%m-%d')
                end = datetime.strptime(data['end_date'], '%Y-%m-%d')

                if os.environ.get('DATABASE_URL'):
                    import psycopg
                    from psycopg.rows import dict_row

                    pg_url = os.environ.get('DATABASE_URL', '').replace('postgresql+psycopg://', 'postgresql://')
                    user_name = session.get('user_name', '')

                    with psycopg.connect(pg_url, row_factory=dict_row) as conn:
                        with conn.cursor() as cur:
                            current = start
                            while current <= end:
                                cur.execute(
                                    """
                                    SELECT id FROM timesheet_reports
                                    WHERE employee_name = %s AND month = %s AND year = %s
                                    """,
                                    (user_name, current.month, current.year),
                                )
                                report = cur.fetchone()
                                if report:
                                    cur.execute(
                                        """
                                        INSERT INTO timesheet_report_days (report_id, day, work_outside)
                                        VALUES (%s, %s, 8)
                                        ON CONFLICT (report_id, day)
                                        DO UPDATE SET work_outside = 8, work_in_museum = 0
                                        """,
                                        (report['id'], current.day),
                                    )
                                current += timedelta(days=1)
                            conn.commit()
                            result['timesheet_updated'] = True
            except Exception as exc:
                logger.error("Timesheet update error: %s", exc)
                result['timesheet_error'] = str(exc)

        return jsonify(result)
    except Exception as exc:
        logger.error("Field trip creation error: %s", exc)
        return jsonify({'success': False, 'message': str(exc)})


def api_accommodation_search():
    """Search for accommodation options using Google Places or OpenStreetMap."""
    try:
        data = request.get_json()
        location = data.get('location', '')
        check_in = data.get('check_in', '')
        check_out = data.get('check_out', '')
        guests = int(data.get('guests', 2))
        max_price = int(data.get('max_price', 10000))

        accommodations = []
        source_info = ''
        google_api_key = os.environ.get('GOOGLE_API_KEY', '')

        if google_api_key:
            try:
                response = http_requests.get(
                    "https://maps.googleapis.com/maps/api/place/textsearch/json",
                    params={
                        'query': f'hotels in {location} Serbia',
                        'key': google_api_key,
                        'language': 'sr',
                    },
                    timeout=10,
                )
                places_data = response.json()
                if places_data.get('status') == 'OK' and places_data.get('results'):
                    source_info = 'Google Places'
                    for idx, place in enumerate(places_data['results'][:5]):
                        rating = place.get('rating', 3.5)
                        base_price = 2500 + (rating - 3) * 1500
                        price = min(int(base_price + random.randint(-500, 500)), max_price)
                        accommodations.append(
                            {
                                'id': idx + 1,
                                'name': place.get('name', f'Смештај {idx + 1}'),
                                'type': 'Хотел' if 'hotel' in place.get('name', '').lower() else 'Смештај',
                                'price_per_night': price,
                                'rating': rating,
                                'amenities': ['WiFi', 'Паркинг'] if rating >= 4 else ['WiFi'],
                                'source': 'google.com',
                                'distance': place.get('formatted_address', ''),
                                'place_id': place.get('place_id', ''),
                            }
                        )
            except Exception as exc:
                logger.warning("Google Places API error: %s", exc)

        if not accommodations:
            try:
                geo_response = http_requests.get(
                    "https://nominatim.openstreetmap.org/search",
                    params={'q': f'{location}, Serbia', 'format': 'json', 'limit': 1},
                    headers={'User-Agent': 'MuseumInfoSystem/1.0'},
                    timeout=10,
                )
                geo_data = geo_response.json()

                if geo_data:
                    lat = float(geo_data[0]['lat'])
                    lon = float(geo_data[0]['lon'])
                    osm_response = http_requests.post(
                        "https://overpass-api.de/api/interpreter",
                        data={
                            'data': f"""
                            [out:json][timeout:10];
                            (
                              node["tourism"="hotel"](around:10000,{lat},{lon});
                              node["tourism"="guest_house"](around:10000,{lat},{lon});
                              node["tourism"="hostel"](around:10000,{lat},{lon});
                              node["tourism"="motel"](around:10000,{lat},{lon});
                              way["tourism"="hotel"](around:10000,{lat},{lon});
                              way["tourism"="guest_house"](around:10000,{lat},{lon});
                            );
                            out center 10;
                            """
                        },
                        timeout=15,
                    )
                    osm_data = osm_response.json()
                    if osm_data.get('elements'):
                        source_info = 'OpenStreetMap'
                        type_map = {
                            'hotel': 'Хотел',
                            'guest_house': 'Пансион',
                            'hostel': 'Хостел',
                            'motel': 'Мотел',
                            'apartment': 'Апартман',
                        }
                        price_map = {
                            'hotel': (3500, 6000),
                            'guest_house': (2000, 4000),
                            'hostel': (1500, 2500),
                            'motel': (2500, 4000),
                            'apartment': (3000, 5000),
                        }
                        for idx, element in enumerate(osm_data['elements'][:5]):
                            tags = element.get('tags', {})
                            tourism_type = tags.get('tourism', 'hotel')
                            name = tags.get('name', tags.get('name:sr', f'Смештај {idx + 1}'))
                            low, high = price_map.get(tourism_type, (3000, 3000))
                            price = min(random.randint(low, high), max_price)
                            elem_lat = element.get('lat', element.get('center', {}).get('lat', lat))
                            accommodations.append(
                                {
                                    'id': idx + 1,
                                    'name': name,
                                    'type': type_map.get(tourism_type, 'Смештај'),
                                    'price_per_night': price,
                                    'rating': round(random.uniform(3.5, 4.8), 1),
                                    'amenities': ['WiFi']
                                    + (['Паркинг'] if tags.get('parking') else [])
                                    + (['Доручак'] if tags.get('breakfast') else []),
                                    'source': 'openstreetmap.org',
                                    'distance': f'{round(abs(elem_lat - lat) * 111, 1)} км од центра',
                                    'osm_id': element.get('id'),
                                }
                            )
            except Exception as exc:
                logger.warning("OpenStreetMap API error: %s", exc)

        if not accommodations:
            source_info = 'Демо подаци'
            accommodations = [
                {
                    'id': 1,
                    'name': f'Хотел "{location}" Центар',
                    'type': 'Хотел',
                    'price_per_night': min(4500, max_price),
                    'rating': 4.2,
                    'amenities': ['WiFi', 'Паркинг', 'Доручак'],
                    'source': 'demo',
                    'distance': '0.5 км од центра',
                },
                {
                    'id': 2,
                    'name': f'Апартман "{location}" View',
                    'type': 'Апартман',
                    'price_per_night': min(3200, max_price),
                    'rating': 4.5,
                    'amenities': ['WiFi', 'Кухиња', 'Паркинг'],
                    'source': 'demo',
                    'distance': '1.2 км од центра',
                },
                {
                    'id': 3,
                    'name': f'Пансион "{location}" Traditional',
                    'type': 'Пансион',
                    'price_per_night': min(2800, max_price),
                    'rating': 4.0,
                    'amenities': ['WiFi', 'Доручак', 'Вечера'],
                    'source': 'demo',
                    'distance': '0.8 км од центра',
                },
            ]

        for accommodation in accommodations:
            booking_search = location.replace(' ', '+')
            accommodation['booking_url'] = (
                "https://www.booking.com/searchresults.html"
                f"?ss={booking_search}&checkin={check_in}&checkout={check_out}&group_adults={guests}"
            )

        return jsonify(
            {
                'success': True,
                'location': location,
                'accommodations': accommodations,
                'source': source_info,
                'note': f'Подаци из {source_info}. Цене су оријентационе - за резервацију контактирајте рачуноводство.',
            }
        )
    except Exception as exc:
        logger.error("Accommodation search error: %s", exc)
        return jsonify({'success': False, 'message': str(exc)})


def _find_destination(dest_input):
    dest_upper = dest_input.upper().strip()
    for dest_name, info in DESTINATION_COORDS.items():
        if dest_name in dest_upper or dest_upper in dest_name:
            return dest_name, info
    for dest_name, info in DESTINATION_COORDS.items():
        for dest_word in dest_name.split():
            for input_word in dest_upper.split():
                if dest_word in input_word or input_word in dest_word:
                    return dest_name, info
    return None, None


def api_route_calculate(*, get_museum_vehicles):
    """Calculate route distance and toll from static database."""
    try:
        data = request.get_json()
        destinations = data.get('destinations', [])
        if not destinations:
            single_dest = data.get('destination', '').strip()
            if single_dest:
                destinations = [single_dest]
        if not destinations:
            return jsonify({'success': False, 'message': 'Није унета дестинација'})

        vehicle_id = data.get('vehicle_id')
        fuel_consumption = 10.0
        fuel_type = 'Бензин'
        vehicle_name = ''

        if vehicle_id == 'sopstveni':
            fuel_consumption = float(data.get('consumption', 8.0))
            fuel_type = data.get('fuel_type', 'BMB 95')
            vehicle_name = 'Сопствено возило'
        elif vehicle_id:
            for vehicle in get_museum_vehicles():
                if vehicle['id'] == int(vehicle_id):
                    fuel_consumption = vehicle.get('fuel_consumption', 10.0)
                    fuel_type = vehicle.get('fuel_type', 'Бензин')
                    vehicle_name = vehicle.get('name', '')
                    break

        fuel_price = FUEL_PRICES_LOCAL.get(fuel_type, 174)
        total_distance = 0
        total_toll = 0
        matched_destinations = []
        toll_stations = set()
        route_segments = []
        previous_location = 'Београд'

        for dest_input in destinations:
            matched_dest, dest_info = _find_destination(dest_input)
            if dest_info:
                segment_km = dest_info['km']
                toll_station = dest_info.get('toll_station')
                segment_toll = 0
                if toll_station:
                    toll_one_way = TOLL_PRICES_FROM_BELGRADE.get(toll_station, 0)
                    if toll_station not in toll_stations:
                        total_toll += toll_one_way
                        segment_toll = toll_one_way
                        toll_stations.add(toll_station)
                total_distance += segment_km
                matched_destinations.append(matched_dest)
                route_segments.append(
                    {
                        'from': previous_location,
                        'to': matched_dest,
                        'distance_km': segment_km,
                        'toll_station': toll_station,
                        'toll_cost': segment_toll,
                        'cumulative_km': total_distance,
                    }
                )
                previous_location = matched_dest
            else:
                matched_destinations.append(dest_input)
                route_segments.append(
                    {
                        'from': previous_location,
                        'to': dest_input,
                        'distance_km': 0,
                        'toll_station': None,
                        'toll_cost': 0,
                        'cumulative_km': total_distance,
                        'unknown': True,
                    }
                )
                previous_location = dest_input

        return_distance = total_distance
        return_toll = total_toll
        if matched_destinations:
            last_dest = matched_destinations[-1].upper()
            for dest_name, info in DESTINATION_COORDS.items():
                if dest_name in last_dest or last_dest in dest_name:
                    return_distance = info['km']
                    toll_station = info.get('toll_station')
                    return_toll = TOLL_PRICES_FROM_BELGRADE.get(toll_station, 0) if toll_station else 0
                    break

        route_segments.append(
            {
                'from': previous_location,
                'to': 'Београд',
                'distance_km': return_distance,
                'toll_station': 'повратак',
                'toll_cost': return_toll,
                'is_return': True,
            }
        )

        if total_distance <= 0:
            return jsonify(
                {
                    'success': False,
                    'destination': ', '.join(destinations),
                    'distance_km': 0,
                    'message': 'Дестинација није пронађена. Унесите километражу ручно.',
                    'known_destinations': list(DESTINATION_COORDS.keys())[:20],
                }
            )

        distance_round_trip = total_distance + return_distance
        toll_round_trip = total_toll + return_toll
        fuel_liters = distance_round_trip * fuel_consumption / 100
        fuel_cost = int(fuel_liters * fuel_price)
        route_parts = ['Београд'] + matched_destinations + ['Београд']
        return jsonify(
            {
                'success': True,
                'source': 'Database',
                'destinations': matched_destinations,
                'destination': ' → '.join(matched_destinations),
                'distance_km_outbound': total_distance,
                'distance_km_return': return_distance,
                'distance_round_trip': distance_round_trip,
                'toll_station': ', '.join(sorted(toll_stations)) if toll_stations else 'без путарине',
                'toll_stations': list(toll_stations),
                'toll_outbound': total_toll,
                'toll_return': return_toll,
                'toll_round_trip': toll_round_trip,
                'fuel_consumption': fuel_consumption,
                'fuel_type': fuel_type,
                'fuel_liters': round(fuel_liters, 1),
                'fuel_price_per_liter': fuel_price,
                'fuel_cost': fuel_cost,
                'vehicle_name': vehicle_name,
                'total_transport_cost': fuel_cost + toll_round_trip,
                'route_info': ' → '.join(route_parts),
                'segments': route_segments,
            }
        )
    except Exception as exc:
        logger.error("Route calculation error: %s", exc)
        return jsonify({'success': False, 'message': str(exc)})


def _build_procurement_document(data):
    from docx import Document
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    from docx.shared import Cm, Pt

    doc = Document()
    for section in doc.sections:
        section.top_margin = Cm(2)
        section.bottom_margin = Cm(2)
        section.left_margin = Cm(2)
        section.right_margin = Cm(2)

    title = doc.add_paragraph()
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = title.add_run('ДИРЕКТОРУ ПРИРОДЊАЧКОГ МУЗЕЈА, БЕОГРАД')
    run.bold = True
    run.font.size = Pt(14)

    doc.add_paragraph()
    header_table = doc.add_table(rows=2, cols=3)
    header_table.style = 'Table Grid'
    header_table.cell(0, 0).merge(header_table.cell(1, 0))
    header_table.cell(0, 0).text = '[LOGO]'
    header_table.cell(0, 0).paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
    header_table.cell(0, 1).merge(header_table.cell(1, 1))
    cell = header_table.cell(0, 1)
    paragraph = cell.paragraphs[0]
    paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = paragraph.add_run('ЗАХТЕВ\n')
    run.bold = True
    run.font.size = Pt(16)
    paragraph.add_run('за набавку / наруџбу')
    header_table.cell(0, 2).text = f"Датум подношења:\n{data.get('datum', '')}"

    doc.add_paragraph()
    applicant_table = doc.add_table(rows=1, cols=2)
    applicant_table.style = 'Table Grid'
    applicant_table.cell(0, 0).text = f"Подносилац захтева:\n{data.get('podnosilac', '')}"
    applicant_table.cell(0, 1).text = "Потпис:\n\n"
    doc.add_paragraph()

    items = data.get('items', [])
    items_table = doc.add_table(rows=len(items) + 3, cols=5)
    items_table.style = 'Table Grid'
    items_table.cell(0, 0).merge(items_table.cell(1, 0))
    items_table.cell(0, 0).text = 'Р.бр.'
    items_table.cell(0, 1).merge(items_table.cell(1, 1))
    items_table.cell(0, 1).text = 'Добро / услуга'
    items_table.cell(0, 2).merge(items_table.cell(0, 3))
    items_table.cell(0, 2).text = 'Динара'
    items_table.cell(0, 4).merge(items_table.cell(1, 4))
    items_table.cell(0, 4).text = 'Примио добро / услугу / средства:'
    items_table.cell(1, 2).text = 'Процењено'
    items_table.cell(1, 3).text = 'Реализовано'

    for idx, item in enumerate(items):
        row_idx = idx + 2
        items_table.cell(row_idx, 0).text = f"{item.get('rbr', idx + 1)}."
        items_table.cell(row_idx, 1).text = item.get('description', '')
        items_table.cell(row_idx, 2).text = f"{item.get('estimated', 0):,.2f}"
        items_table.cell(row_idx, 3).text = f"{item.get('realized', 0):,.2f}"
        items_table.cell(row_idx, 4).text = item.get('receiver', '')

    total_row = len(items) + 2
    items_table.cell(total_row, 0).merge(items_table.cell(total_row, 1))
    items_table.cell(total_row, 0).text = 'СВЕГА:'
    items_table.cell(total_row, 0).paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.RIGHT
    items_table.cell(total_row, 2).text = f"{data.get('totalEstimated', 0):,.2f}"
    items_table.cell(total_row, 3).text = f"{data.get('totalRealized', 0):,.2f}"

    doc.add_paragraph()
    approval_table = doc.add_table(rows=2, cols=2)
    approval_table.style = 'Table Grid'
    approval_table.cell(0, 0).text = (
        f"На терет активности:\n{data.get('teretAktivnosti', '')}\n{data.get('teretAktivnostiOpis', '')}"
    )
    approval_table.cell(0, 1).text = f"Сагласан руководилац:\n{data.get('saglasanRukovodilac', '')}\n\n"
    approval_table.cell(1, 0).text = (
        f"Да постоје расположива наменска средства, потврђује шеф рачуноводства:\n{data.get('sefRacunovodstva', '')}\n\n"
    )
    approval_table.cell(1, 1).text = f"Одобрава набавку / наруџбу, директор:\n{data.get('direktor', '')}\n\n"
    return doc


def _send_docx_document(doc, download_name):
    file_stream = BytesIO()
    doc.save(file_stream)
    file_stream.seek(0)
    return send_file(
        file_stream,
        mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        as_attachment=True,
        download_name=download_name,
    )


def api_nabavka_save():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'success': False, 'message': 'Нема података'})

        import psycopg
        from psycopg.rows import dict_row

        db_url = os.environ.get('DATABASE_URL', '').replace('postgresql+psycopg://', 'postgresql://')
        with psycopg.connect(conninfo=db_url, row_factory=dict_row) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    CREATE TABLE IF NOT EXISTS procurement_requests (
                        id SERIAL PRIMARY KEY,
                        datum DATE NOT NULL,
                        podnosilac VARCHAR(255) NOT NULL,
                        items JSONB NOT NULL,
                        total_estimated DECIMAL(12,2) DEFAULT 0,
                        total_realized DECIMAL(12,2) DEFAULT 0,
                        teret_aktivnosti VARCHAR(100),
                        teret_aktivnosti_opis TEXT,
                        saglasan_rukovodilac VARCHAR(255),
                        sef_racunovodstva VARCHAR(255),
                        direktor VARCHAR(255),
                        status VARCHAR(50) DEFAULT 'pending',
                        user_email VARCHAR(255),
                        created_at TIMESTAMP DEFAULT NOW(),
                        updated_at TIMESTAMP DEFAULT NOW()
                    )
                    """
                )
                cur.execute(
                    """
                    INSERT INTO procurement_requests
                    (datum, podnosilac, items, total_estimated, total_realized,
                     teret_aktivnosti, teret_aktivnosti_opis, saglasan_rukovodilac,
                     sef_racunovodstva, direktor, user_email)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    RETURNING id
                    """,
                    (
                        data.get('datum'),
                        data.get('podnosilac'),
                        json.dumps(data.get('items', []), ensure_ascii=False),
                        data.get('totalEstimated', 0),
                        data.get('totalRealized', 0),
                        data.get('teretAktivnosti'),
                        data.get('teretAktivnostiOpis'),
                        data.get('saglasanRukovodilac'),
                        data.get('sefRacunovodstva'),
                        data.get('direktor'),
                        session.get('user_email'),
                    ),
                )
                new_id = cur.fetchone()['id']
                conn.commit()
        return jsonify({'success': True, 'message': f'Захтев сачуван (ID: {new_id})', 'id': new_id})
    except Exception as exc:
        logger.exception("Error saving procurement request")
        return jsonify({'success': False, 'message': str(exc)})


def api_nabavka_list():
    try:
        import psycopg
        from psycopg.rows import dict_row

        db_url = os.environ.get('DATABASE_URL', '').replace('postgresql+psycopg://', 'postgresql://')
        with psycopg.connect(conninfo=db_url, row_factory=dict_row) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT EXISTS (
                        SELECT FROM information_schema.tables
                        WHERE table_name = 'procurement_requests'
                    )
                    """
                )
                if not cur.fetchone()['exists']:
                    return jsonify({'success': True, 'requests': []})

                user_email = session.get('user_email')
                user_role = session.get('user_role')
                if user_role == 'admin':
                    cur.execute(
                        """
                        SELECT id, datum::text, podnosilac, items, total_estimated as procenjeno,
                               status, created_at
                        FROM procurement_requests
                        ORDER BY created_at DESC
                        LIMIT 50
                        """
                    )
                else:
                    cur.execute(
                        """
                        SELECT id, datum::text, podnosilac, items, total_estimated as procenjeno,
                               status, created_at
                        FROM procurement_requests
                        WHERE user_email = %s
                        ORDER BY created_at DESC
                        LIMIT 50
                        """,
                        (user_email,),
                    )
                requests = cur.fetchall()

        formatted = []
        for req in requests:
            items = req['items'] if isinstance(req['items'], list) else json.loads(req['items'])
            opis = items[0]['description'][:50] + '...' if items else 'Без описа'
            formatted.append(
                {
                    'id': req['id'],
                    'datum': req['datum'],
                    'opis': opis,
                    'procenjeno': float(req['procenjeno'] or 0),
                    'status': req['status'],
                }
            )
        return jsonify({'success': True, 'requests': formatted})
    except Exception as exc:
        logger.error("Error listing procurement requests: %s", exc)
        return jsonify({'success': True, 'requests': []})


def api_nabavka_export_word():
    try:
        data = request.get_json()
        return _send_docx_document(
            _build_procurement_document(data),
            f"Zahtev_za_nabavku_{data.get('datum', 'unknown')}.docx",
        )
    except Exception as exc:
        logger.exception("Error exporting procurement request")
        return jsonify({'success': False, 'message': str(exc)}), 500


def api_nabavka_export_word_by_id(request_id, *, can_access_owned_record):
    try:
        import psycopg
        from psycopg.rows import dict_row

        db_url = os.environ.get('DATABASE_URL', '').replace('postgresql+psycopg://', 'postgresql://')
        with psycopg.connect(conninfo=db_url, row_factory=dict_row) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM procurement_requests WHERE id = %s", (request_id,))
                req = cur.fetchone()
                if not req:
                    return jsonify({'success': False, 'message': 'Захтев није пронађен'}), 404
                if not can_access_owned_record(
                    req.get('user_email'),
                    session.get('user_email', ''),
                    session.get('user_role', ''),
                ):
                    return jsonify({'success': False, 'message': 'Немате приступ овом захтеву'}), 403

        items = req['items'] if isinstance(req['items'], list) else json.loads(req['items'])
        data = {
            'datum': str(req['datum']),
            'podnosilac': req['podnosilac'],
            'items': items,
            'totalEstimated': float(req['total_estimated'] or 0),
            'totalRealized': float(req['total_realized'] or 0),
            'teretAktivnosti': req['teret_aktivnosti'] or '',
            'teretAktivnostiOpis': req['teret_aktivnosti_opis'] or '',
            'saglasanRukovodilac': req['saglasan_rukovodilac'] or '',
            'sefRacunovodstva': req['sef_racunovodstva'] or '',
            'direktor': req['direktor'] or '',
        }
        return _send_docx_document(
            _build_procurement_document(data),
            f"Zahtev_za_nabavku_{request_id}_{data['datum']}.docx",
        )
    except Exception as exc:
        logger.exception("Error exporting procurement request by id")
        return jsonify({'success': False, 'message': str(exc)}), 500


def _financial_plan_totals(years_data):
    total_2026 = sum(item.get('amount', 0) for items in years_data.get('2026', {}).values() for item in items)
    total_2027 = sum(item.get('amount', 0) for items in years_data.get('2027', {}).values() for item in items)
    total_2028 = sum(item.get('amount', 0) for items in years_data.get('2028', {}).values() for item in items)
    return total_2026, total_2027, total_2028, total_2026 + total_2027 + total_2028


def api_finansijski_plan_save(*, get_postgres_connection):
    try:
        data = request.get_json()
        years_data = data.get('years', {})
        total_2026, total_2027, total_2028, grand_total = _financial_plan_totals(years_data)

        with get_postgres_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    CREATE TABLE IF NOT EXISTS financial_plans (
                        id SERIAL PRIMARY KEY,
                        odeljenje VARCHAR(100),
                        odeljenje_text VARCHAR(200),
                        kustos VARCHAR(200),
                        datum_izrade DATE,
                        plan_data JSONB,
                        total_2026 DECIMAL(15,2),
                        total_2027 DECIMAL(15,2),
                        total_2028 DECIMAL(15,2),
                        grand_total DECIMAL(15,2),
                        user_email VARCHAR(200),
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                    """
                )
                cur.execute(
                    """
                    INSERT INTO financial_plans
                    (odeljenje, odeljenje_text, kustos, datum_izrade, plan_data,
                     total_2026, total_2027, total_2028, grand_total, user_email)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    RETURNING id
                    """,
                    (
                        data.get('odeljenje'),
                        data.get('odeljenjeText'),
                        data.get('kustos'),
                        data.get('datumIzrade'),
                        json.dumps(years_data),
                        total_2026,
                        total_2027,
                        total_2028,
                        grand_total,
                        session.get('user_email', ''),
                    ),
                )
                plan_id = cur.fetchone()[0]
                conn.commit()
        return jsonify({'success': True, 'id': plan_id})
    except Exception as exc:
        logger.error("Error saving financial plan: %s", exc)
        return jsonify({'success': False, 'message': str(exc)}), 500


def api_finansijski_plan_list(*, get_postgres_connection, current_user_is_admin):
    try:
        with get_postgres_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT EXISTS (
                        SELECT FROM information_schema.tables
                        WHERE table_name = 'financial_plans'
                    )
                    """
                )
                if not cur.fetchone()[0]:
                    return jsonify({'success': True, 'plans': []})

                if current_user_is_admin():
                    cur.execute(
                        """
                        SELECT id, datum_izrade, odeljenje_text, kustos, grand_total
                        FROM financial_plans
                        ORDER BY created_at DESC
                        """
                    )
                else:
                    cur.execute(
                        """
                        SELECT id, datum_izrade, odeljenje_text, kustos, grand_total
                        FROM financial_plans
                        WHERE user_email = %s
                        ORDER BY created_at DESC
                        """,
                        (session.get('user_email', ''),),
                    )
                rows = cur.fetchall()

        plans = []
        for row in rows:
            plans.append(
                {
                    'id': row[0],
                    'datum': str(row[1]) if row[1] else '',
                    'odeljenje': row[2] or '',
                    'kustos': row[3] or '',
                    'ukupno': float(row[4]) if row[4] else 0,
                }
            )
        return jsonify({'success': True, 'plans': plans})
    except Exception as exc:
        logger.error("Error listing financial plans: %s", exc)
        return jsonify({'success': False, 'message': str(exc)}), 500


def _build_financial_plan_document(data):
    from docx import Document
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    from docx.shared import Cm, Pt

    doc = Document()
    for section in doc.sections:
        section.top_margin = Cm(2)
        section.bottom_margin = Cm(2)
        section.left_margin = Cm(2.5)
        section.right_margin = Cm(2.5)

    years_data = data.get('years', {})
    for year in ['2027', '2028', '2029']:
        year_data = years_data.get(year, {})
        header = doc.add_paragraph()
        header.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = header.add_run("Предлог финансијског плана")
        run.bold = True
        run.font.size = Pt(14)

        year_para = doc.add_paragraph()
        year_para.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = year_para.add_run(f"Година: {year}")
        run.bold = True
        run.font.size = Pt(12)

        dept_para = doc.add_paragraph()
        dept_para.alignment = WD_ALIGN_PARAGRAPH.CENTER
        dept_para.add_run(f"Одељење: {data.get('odeljenjeText', '')}").font.size = Pt(11)

        doc.add_paragraph()
        year_total = 0
        for category_key, category_name in FINANCIAL_PLAN_CATEGORY_NAMES.items():
            items = year_data.get(category_key, [])
            if not items:
                continue

            cat_header = doc.add_paragraph()
            run = cat_header.add_run(category_name)
            run.bold = True
            run.font.size = Pt(11)

            table = doc.add_table(rows=1, cols=3)
            table.style = 'Table Grid'
            hdr_cells = table.rows[0].cells
            hdr_cells[0].text = 'р.б.'
            hdr_cells[1].text = 'Активност'
            hdr_cells[2].text = 'Износ'
            for cell in hdr_cells:
                cell.paragraphs[0].runs[0].bold = True
                cell.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER

            category_total = 0
            for item in items:
                row_cells = table.add_row().cells
                row_cells[0].text = f"{item.get('rbr', '')}."
                row_cells[1].text = item.get('activity', '')
                amount = item.get('amount', 0)
                row_cells[2].text = f"{amount:,.0f}".replace(',', '.')
                row_cells[2].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.RIGHT
                category_total += amount

            total_row = table.add_row().cells
            total_row[0].text = ''
            total_row[1].text = 'УКУПНО:'
            total_row[1].paragraphs[0].runs[0].bold = True
            total_row[1].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.RIGHT
            total_row[2].text = f"{category_total:,.0f}".replace(',', '.')
            total_row[2].paragraphs[0].runs[0].bold = True
            total_row[2].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.RIGHT
            year_total += category_total
            doc.add_paragraph()

        year_total_para = doc.add_paragraph()
        year_total_para.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        run = year_total_para.add_run(f"УКУПНО ЗА {year}. ГОДИНУ: {year_total:,.0f} РСД".replace(',', '.'))
        run.bold = True
        run.font.size = Pt(12)
        if year != '2029':
            doc.add_page_break()

    doc.add_paragraph()
    doc.add_paragraph()
    sig_para = doc.add_paragraph()
    sig_para.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    sig_para.add_run(f"Кустос: {data.get('kustos', '')}")
    date_para = doc.add_paragraph()
    date_para.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    date_para.add_run(f"Датум: {data.get('datumIzrade', '')}")
    return doc


def api_finansijski_plan_export_word():
    try:
        data = request.get_json()
        return _send_docx_document(
            _build_financial_plan_document(data),
            f"Finansijski_plan_{data.get('datumIzrade', 'unknown')}.docx",
        )
    except Exception as exc:
        logger.exception("Error exporting financial plan")
        return jsonify({'success': False, 'message': str(exc)}), 500


def api_finansijski_plan_export_word_by_id(
    plan_id,
    *,
    get_postgres_connection,
    can_access_owned_record,
):
    try:
        with get_postgres_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT odeljenje, odeljenje_text, kustos, datum_izrade, plan_data
                    FROM financial_plans WHERE id = %s
                    """,
                    (plan_id,),
                )
                row = cur.fetchone()
                if not row:
                    return jsonify({'success': False, 'message': 'План није пронађен'}), 404
                cur.execute("SELECT user_email FROM financial_plans WHERE id = %s", (plan_id,))
                owner_row = cur.fetchone()
                owner_email = owner_row[0] if owner_row else None
                if not can_access_owned_record(
                    owner_email,
                    session.get('user_email', ''),
                    session.get('user_role', ''),
                ):
                    return jsonify({'success': False, 'message': 'Немате приступ овом плану'}), 403

        data = {
            'odeljenje': row[0],
            'odeljenjeText': row[1],
            'kustos': row[2],
            'datumIzrade': str(row[3]) if row[3] else '',
            'years': row[4] if row[4] else {},
        }
        return _send_docx_document(
            _build_financial_plan_document(data),
            f"Finansijski_plan_{plan_id}_{data['datumIzrade']}.docx",
        )
    except Exception as exc:
        logger.exception("Error exporting financial plan by id")
        return jsonify({'success': False, 'message': str(exc)}), 500
