"""Shared route implementations for map pages and JSON-backed map layers."""

import json
import logging
import os
import re

from flask import current_app, jsonify, render_template, request, send_file

logger = logging.getLogger(__name__)

_ore_deposits_cache = None
_ogk_points_cache = None
_ogk_radovi_cache = None
_stratigraphy_cache = None
_paleo_localities_cache = None
_mining_operations_cache = None
_exploration_licenses_cache = None
_geo_sheets_cache = None
_sanja_mammals_localities_cache = None


def _ogk_group_counts():
    """Return {grupa: N} for the OGK layer switches, or {} if the file is absent.

    The menu badges need the totals before any layer is loaded lazily, so they
    are rendered with the page instead of costing an extra request.
    """
    try:
        data = _load_json_cached(
            '_ogk_points_cache',
            os.path.join(current_app.root_path, 'data', 'ogk_points.json'),
        )
        if isinstance(data, dict):
            return data.get('grupe', {}) or {}
    except Exception as exc:
        logger.error("Error loading OGK group counts: %s", exc)
    return {}


def _ogk_broj_sa_radovima():
    """Return koliko OGK tačaka ima bar jedan potvrđen ili verovatan rad.

    Broji se presek sa tačkama — id iz žetve koji ne postoji u ogk_points.json
    ne sme da naduva brojač na prekidaču koji filtrira baš te tačke. Sam „ima
    rad“ ništa ne znači: žetva je išla po imenu lokaliteta, pa tačka ume da
    nosi osam radova od kojih nijedan nije njen.
    """
    try:
        tacke = _load_json_cached(
            '_ogk_points_cache',
            os.path.join(current_app.root_path, 'data', 'ogk_points.json'),
        )
        poznati = {tacka.get('id') for tacka in (tacke.get('tacke', [])
                                                 if isinstance(tacke, dict) else [])}
        radovi = _ogk_radovi(current_app.root_path)['radovi']
        broj = 0
        for ogk_id, spisak in radovi.items():
            if ogk_id not in poznati:
                continue
            _, potvrdjenih, verovatnih = _prebroj_radove(spisak)
            if potvrdjenih or verovatnih:
                broj += 1
        return broj
    except Exception as exc:
        logger.error("Error counting OGK points with papers: %s", exc)
    return 0


def render_admin_maps():
    """Render the interactive geological map page."""
    return render_template('admin_maps.html',
                           ogk_grupe=_ogk_group_counts(),
                           ogk_sa_radovima=_ogk_broj_sa_radovima())


def render_admin_geological_timeline():
    """Render the geological timeline page."""
    return render_template('admin_geological_timeline.html')


def _load_json_cached(cache_name, file_path):
    """Load read-only map JSON into a module-level cache and return it.

    These map datasets are static layer sources. Avoid runtime lock sidecars here:
    production serves this code as a restricted user that can read data/*.json
    but must not need write permission to create hidden .*.lock files.
    """
    global _ore_deposits_cache
    global _ogk_points_cache
    global _ogk_radovi_cache
    global _stratigraphy_cache
    global _paleo_localities_cache
    global _mining_operations_cache
    global _exploration_licenses_cache
    global _geo_sheets_cache
    global _sanja_mammals_localities_cache

    cache_value = globals()[cache_name]
    if cache_value is None:
        if not os.path.exists(file_path):
            cache_value = []
        else:
            with open(file_path, 'r', encoding='utf-8') as handle:
                cache_value = json.load(handle)
        globals()[cache_name] = cache_value
    return cache_value


def api_ore_deposits(app_root):
    """Serve ore deposit data from JSON."""
    try:
        data = _load_json_cached(
            '_ore_deposits_cache',
            os.path.join(app_root, 'data', 'ore_deposits.json'),
        )
        return jsonify({'success': True, 'data': data})
    except Exception as exc:
        logger.error("Error loading ore deposits: %s", exc)
        return jsonify({'success': False, 'message': 'Грешка при учитавању рудних лежишта'}), 500


# Облик OGK ознаке (нпр. K34-03-0035). Кључ мапе радова се никад не тражи
# сировим стрингом из путање — непознат облик је 404, не претрага речника.
OGK_ID_OBLIK = re.compile(r'^[A-Za-z0-9\-]{1,32}$')


def _ogk_radovi(app_root):
    """Return {ogk_id: [rad, ...]} for the harvested papers, cached per process.

    Missing or malformed ``data/ogk_radovi.json`` is never swallowed: the point
    layer keeps working, but the caller learns it through ``"nedostaje"`` and
    the reason is logged as a warning.
    """
    global _ogk_radovi_cache

    if _ogk_radovi_cache is None:
        putanja = os.path.join(app_root, 'data', 'ogk_radovi.json')
        ucitano = {'radovi': {}, 'izvor': 'nedostaje'}
        if not os.path.exists(putanja):
            logger.warning("OGK radovi: %s ne postoji — тачке остају без радова",
                           putanja)
        else:
            try:
                with open(putanja, 'r', encoding='utf-8') as handle:
                    podaci = json.load(handle)
                radovi = podaci.get('radovi') if isinstance(podaci, dict) else None
                if not isinstance(radovi, dict):
                    logger.warning("OGK radovi: %s нема исправну мапу 'radovi'",
                                   putanja)
                else:
                    ucitano = {'radovi': radovi, 'izvor': 'ok'}
            except (OSError, ValueError) as exc:
                logger.warning("OGK radovi: %s се не да прочитати (%s)",
                               putanja, exc)
        _ogk_radovi_cache = ucitano
    return _ogk_radovi_cache


# Оцене које рад може да носи, редом од најјаче ка најслабијој. „neoceneno“ је
# рад који суд још није стигао — не сме да се сабере са „nije“.
OCENE_RADA = ('potvrdjen', 'verovatan', 'nesigurno', 'neoceneno', 'nije')


def _prebroj_radove(spisak):
    """Return (ukupno, potvrdjenih, verovatnih) za spisak radova lokaliteta."""
    if not isinstance(spisak, list):
        return 0, 0, 0
    potvrdjenih = verovatnih = 0
    for rad in spisak:
        if not isinstance(rad, dict):
            continue
        if rad.get('ocena') == 'potvrdjen':
            potvrdjenih += 1
        elif rad.get('ocena') == 'verovatan':
            verovatnih += 1
    return len(spisak), potvrdjenih, verovatnih


def _raspodela_ocena(spisak):
    """Return {ocena: N} po svim ocenama — nepoznata oznaka pada u „neoceneno“."""
    raspodela = dict.fromkeys(OCENE_RADA, 0)
    for rad in spisak if isinstance(spisak, list) else []:
        ocena = rad.get('ocena') if isinstance(rad, dict) else None
        raspodela['neoceneno' if ocena not in raspodela else ocena] += 1
    return raspodela


def api_ogk_points(app_root):
    """Serve OGK 1:100 000 point data from JSON for the map layers.

    Optional ``?grupe=rudnici,busotine`` filters server-side; without it the
    whole set is returned. An unknown group name is not silently dropped — it
    comes back as a 400 so a typo in the layer menu cannot look like an empty
    layer. Every point carries how many harvested papers it has (``n_radova``)
    and how many of those were judged to be about this very locality
    (``n_radova_potvrdjenih`` / ``n_radova_verovatnih``), so the menu can filter
    without a second request.
    """
    try:
        data = _load_json_cached(
            '_ogk_points_cache',
            os.path.join(app_root, 'data', 'ogk_points.json'),
        )
        if not isinstance(data, dict):
            data = {'ukupno': 0, 'grupe': {}, 'tacke': []}

        tacke = data.get('tacke', [])
        grupe = data.get('grupe', {})

        trazene_raw = (request.args.get('grupe') or '').strip()
        if trazene_raw:
            trazene = [naziv.strip() for naziv in trazene_raw.split(',') if naziv.strip()]
            nepoznate = [naziv for naziv in trazene if naziv not in grupe]
            if nepoznate:
                return jsonify({
                    'success': False,
                    'message': 'Непозната група слоја: ' + ', '.join(nepoznate),
                }), 400
            izabrane = set(trazene)
            tacke = [tacka for tacka in tacke if tacka.get('grupa') in izabrane]
            grupe = {naziv: broj for naziv, broj in grupe.items() if naziv in izabrane}

        radovi = _ogk_radovi(app_root)
        # Копија по тачки: кеш тачака остаје онакав какав је на диску.
        obogacene = []
        for tacka in tacke:
            ukupno_radova, potvrdjenih, verovatnih = _prebroj_radove(
                radovi['radovi'].get(tacka.get('id')))
            obogacena = dict(tacka)
            obogacena['n_radova'] = ukupno_radova
            obogacena['n_radova_potvrdjenih'] = potvrdjenih
            obogacena['n_radova_verovatnih'] = verovatnih
            obogacene.append(obogacena)

        return jsonify({
            'success': True,
            'data': {
                'generisano': data.get('generisano', ''),
                'izvor': data.get('izvor', ''),
                'ukupno': len(obogacene),
                'grupe': grupe,
                'radovi_izvor': radovi['izvor'],
                'tacke': obogacene,
            },
        })
    except Exception as exc:
        logger.error("Error loading OGK points: %s", exc)
        return jsonify({'success': False, 'message': 'Грешка при учитавању OGK тачака'}), 500


def api_ogk_point_radovi(app_root, ogk_id):
    """Serve the harvested papers of a single OGK point.

    A point that exists but has no papers is a 200 with an empty list — that is
    not an error. An unknown (or malformed) id is a 404, so a typo cannot look
    like a locality that nobody ever wrote about.
    """
    try:
        ogk_id = (ogk_id or '').strip()
        if not OGK_ID_OBLIK.match(ogk_id):
            return jsonify({
                'success': False,
                'message': 'Неисправна ознака OGK тачке.',
            }), 404

        data = _load_json_cached(
            '_ogk_points_cache',
            os.path.join(app_root, 'data', 'ogk_points.json'),
        )
        tacke = data.get('tacke', []) if isinstance(data, dict) else []
        tacka = next((t for t in tacke if t.get('id') == ogk_id), None)
        if tacka is None:
            return jsonify({
                'success': False,
                'message': 'Непозната OGK тачка: ' + ogk_id,
            }), 404

        spisak = _ogk_radovi(app_root)['radovi'].get(ogk_id) or []
        if not isinstance(spisak, list):
            spisak = []
        ukupno_radova, potvrdjenih, verovatnih = _prebroj_radove(spisak)

        return jsonify({
            'success': True,
            'data': {
                'id': ogk_id,
                'naziv': tacka.get('naziv', ''),
                # Сваки рад носи и ``ocena`` и ``razlog`` из data/ogk_radovi.json
                # — поповер тиме кустосу каже зашто рад стоји ту где стоји.
                'radovi': spisak,
                'n_radova': ukupno_radova,
                'n_radova_potvrdjenih': potvrdjenih,
                'n_radova_verovatnih': verovatnih,
                'po_oceni': _raspodela_ocena(spisak),
            },
        })
    except Exception as exc:
        logger.error("Error loading OGK point papers for %s: %s", ogk_id, exc)
        return jsonify({'success': False, 'message': 'Грешка при учитавању радова'}), 500


def api_stratigraphy_localities(app_root):
    """Serve stratigraphy locality data from JSON."""
    try:
        data = _load_json_cached(
            '_stratigraphy_cache',
            os.path.join(app_root, 'data', 'stratigraphy_localities.json'),
        )
        return jsonify({'success': True, 'data': data})
    except Exception as exc:
        logger.error("Error loading stratigraphy localities: %s", exc)
        return jsonify({'success': False, 'message': 'Грешка при учитавању стратиграфских локалитета'}), 500


def api_paleo_localities(app_root):
    """Serve paleontological locality data from JSON."""
    try:
        data = _load_json_cached(
            '_paleo_localities_cache',
            os.path.join(app_root, 'data', 'paleo_localities.json'),
        )
        return jsonify({'success': True, 'data': data})
    except Exception as exc:
        logger.error("Error loading paleontological localities: %s", exc)
        return jsonify({'success': False, 'message': 'Грешка при учитавању палеонтолошких локалитета'}), 500


def api_mining_operations(app_root):
    """Serve mining operations data from JSON."""
    try:
        data = _load_json_cached(
            '_mining_operations_cache',
            os.path.join(app_root, 'data', 'mining_operations_serbia.json'),
        )
        return jsonify({'success': True, 'data': data})
    except Exception as exc:
        logger.error("Error loading mining operations: %s", exc)
        return jsonify({'success': False, 'message': 'Грешка при учитавању рударских операција'}), 500


def api_exploration_licenses(app_root):
    """Serve exploration license data from JSON."""
    try:
        data = _load_json_cached(
            '_exploration_licenses_cache',
            os.path.join(app_root, 'data', 'exploration_licenses_map.json'),
        )
        return jsonify({'success': True, 'data': data})
    except Exception as exc:
        logger.error("Error loading exploration licenses: %s", exc)
        return jsonify({'success': False, 'message': 'Грешка при учитавању истражних лиценци'}), 500


def _get_geological_sheets(app_root):
    """Return geological map sheet metadata."""
    return _load_json_cached(
        '_geo_sheets_cache',
        os.path.join(app_root, 'data', 'geological_map_sheets.json'),
    )


def api_geological_sheets(app_root):
    """Serve geological map sheet metadata."""
    try:
        return jsonify({'success': True, 'data': _get_geological_sheets(app_root)})
    except Exception as exc:
        logger.error("Error loading geological sheets: %s", exc)
        return jsonify({'success': False, 'message': 'Грешка при учитавању листова карте'}), 500


def api_sanja_mammals_localities(app_root):
    """Serve Sanja mammals locality data enriched with linked specimens.

    Each locality gets a ``specimens`` array built by matching the first
    3 digits of each specimen's ``catalog_number`` to the locality ``code``.
    """
    try:
        localities = _load_json_cached(
            '_sanja_mammals_localities_cache',
            os.path.join(app_root, 'Sanja', 'sanja_mammals_localities.json'),
        )

        # Build a code→specimens index from the live Sanja database.
        import app as museum_app
        db = museum_app.SANJA_PALEOGENE_NEOGENE_MAMMALS_DATABASE
        specimens = db.get('specimens', [])

        from collections import defaultdict
        by_code = defaultdict(list)
        for s in specimens:
            cn = (s.get('catalog_number') or '').strip()
            if len(cn) >= 3:
                by_code[cn[:3]].append({
                    'id': s.get('id'),
                    'catalog_number': cn,
                    'specimen_name': s.get('specimen_name', ''),
                    'material': s.get('material', ''),
                    'identified_by': s.get('identified_by', ''),
                    'description': s.get('description', ''),
                    'location_found': s.get('location_found', ''),
                    'quantity': s.get('quantity', ''),
                    'uncertain_determination': s.get('uncertain_determination', ''),
                })

        result = []
        for loc in localities:
            code = loc.get('code', '')
            entry = dict(loc)
            entry['specimens'] = by_code.get(code, [])
            entry['specimen_count'] = len(entry['specimens'])
            result.append(entry)

        return jsonify({'success': True, 'data': result})
    except Exception as exc:
        logger.error("Error loading Sanja mammals localities: %s", exc)
        return jsonify({'success': False, 'message': 'Грешка при учитавању локалитета крупних сисара'}), 500


def api_geological_sheet_image(folder_name, image_type, app_root):
    """Serve individual JPG images from geological map sheet folders."""
    if image_type not in ('karta', 'legenda', 'profili', 'stub'):
        return jsonify({'success': False, 'message': 'Непознат тип слике'}), 400
    if '..' in folder_name or '/' in folder_name or '\\' in folder_name:
        return jsonify({'success': False, 'message': 'Неважећи назив фасцикле'}), 400

    try:
        sheets = _get_geological_sheets(app_root)
    except Exception:
        return jsonify({'success': False, 'message': 'Грешка при учитавању података'}), 500

    sheet = next((item for item in sheets if item['folder'] == folder_name), None)
    if not sheet:
        return jsonify({'success': False, 'message': 'Лист карте није пронађен'}), 404
    if image_type not in sheet.get('files', {}):
        return jsonify({'success': False, 'message': 'Слика није доступна за овај лист'}), 404

    filename = sheet['files'][image_type]
    # filename dolazi iz istog JSON-a kao tumac_file — ista resolve+prefix
    # provera (stavka 11).
    from pathlib import Path
    sheet_root = Path(app_root, 'Karte', 'Final - Srbija', folder_name).resolve()
    file_path = (sheet_root / filename).resolve()
    if not str(file_path).startswith(str(sheet_root) + os.sep):
        return jsonify({'success': False, 'message': 'Неважећи назив'}), 400
    if not file_path.is_file():
        return jsonify({'success': False, 'message': 'Датотека није пронађена'}), 404

    return send_file(str(file_path), mimetype='image/jpeg', max_age=86400)


def api_geological_sheet_tumac(folder_name, app_root):
    """Serve tumac PDF/DOC file for a geological map sheet."""
    if '..' in folder_name or '/' in folder_name or '\\' in folder_name:
        return jsonify({'success': False, 'message': 'Неважећи назив'}), 400

    try:
        sheets = _get_geological_sheets(app_root)
    except Exception:
        return jsonify({'success': False, 'message': 'Грешка при учитавању'}), 500

    sheet = next((item for item in sheets if item['folder'] == folder_name), None)
    if not sheet or 'tumac' not in sheet:
        return jsonify({'success': False, 'message': 'Тумач није пронађен'}), 404

    tumac_file = sheet['tumac']['tumac_file']
    # tumac_file dolazi iz geological_map_sheets.json (nije sanitizovan kao
    # folder_name) — isti obrazac kao fototeka: resolve + provera prefiksa,
    # sve van korena se odbija.
    from pathlib import Path
    tumac_root = Path(app_root, 'Karte', 'Tumaci Srbija').resolve()
    file_path = (tumac_root / tumac_file).resolve()
    if not str(file_path).startswith(str(tumac_root) + os.sep):
        return jsonify({'success': False, 'message': 'Неважећи назив'}), 400
    if not file_path.is_file():
        return jsonify({'success': False, 'message': 'Датотека није пронађена'}), 404

    mimetype = 'application/pdf' if tumac_file.lower().endswith('.pdf') else 'application/msword'
    return send_file(str(file_path), mimetype=mimetype, max_age=86400)
