"""Shared route implementations for NHM portal views."""

import logging

from flask import jsonify, render_template, request

logger = logging.getLogger(__name__)


def _api_error_response(message, *, status=500, **extra):
    payload = {'success': False, 'error': message}
    payload.update(extra)
    return jsonify(payload), status


def _safe_int(value, default):
    try:
        return int(value)
    except (TypeError, ValueError):
        return default

_MINERAL_TRANSLATIONS = {
    'pirit': 'pyrite', 'kvarc': 'quartz', 'kalcit': 'calcite', 'galenit': 'galena',
    'sfalerit': 'sphalerite', 'halkopirit': 'chalcopyrite', 'magnetit': 'magnetite',
    'hematit': 'hematite', 'limonit': 'limonite', 'malakit': 'malachite',
    'azurit': 'azurite', 'fluorit': 'fluorite', 'barit': 'barite',
    'celestin': 'celestine', 'gips': 'gypsum', 'halit': 'halite',
    'dolomit': 'dolomite', 'siderit': 'siderite', 'aragonit': 'aragonite',
    'rodonit': 'rhodonite', 'rodohrozit': 'rhodochrosite', 'olivin': 'olivine',
    'augit': 'augite', 'biotit': 'biotite', 'muskovit': 'muscovite',
    'ortoklas': 'orthoclase', 'albit': 'albite', 'turmalin': 'tourmaline',
    'granat': 'garnet', 'topaz': 'topaz', 'cirkon': 'zircon', 'apatit': 'apatite',
    'rutil': 'rutile', 'epidot': 'epidote', 'talk': 'talc', 'serpentin': 'serpentine',
    'hlorit': 'chlorite', 'kaolinit': 'kaolinite', 'zeolit': 'zeolite',
    'opal': 'opal', 'kalcedon': 'chalcedony', 'ahat': 'agate', 'ahati': 'agate',
    'jaspis': 'jasper', 'ametist': 'amethyst', 'dijamant': 'diamond',
    'korund': 'corundum', 'rubin': 'ruby', 'safir': 'sapphire', 'smaragd': 'emerald',
    'antimonit': 'stibnite', 'realgar': 'realgar', 'auripigment': 'orpiment',
    'arsenopirit': 'arsenopyrite', 'molibdenit': 'molybdenite', 'kasiterit': 'cassiterite',
    'kuprit': 'cuprite', 'bornit': 'bornite', 'halkozin': 'chalcocite',
    'kovelint': 'covellite', 'cerusit': 'cerussite', 'anglezit': 'anglesite',
    'vulfenit': 'wulfenite', 'smitsonit': 'smithsonite', 'kriolit': 'cryolite',
    'beril': 'beryl', 'spodumen': 'spodumene', 'lazurit': 'lazurite',
    'sodalit': 'sodalite', 'nefelin': 'nepheline', 'leucit': 'leucite',
    'andaluzit': 'andalusite', 'sillimanit': 'sillimanite', 'kijanit': 'kyanite',
    'staurolit': 'staurolite', 'vesuvijan': 'vesuvianite', 'aksinit': 'axinite',
    'datolit': 'datolite', 'prehnit': 'prehnite', 'volastonit': 'wollastonite',
    'diopzid': 'diopside', 'tremolit': 'tremolite', 'aktinolit': 'actinolite',
    'hornblenda': 'hornblende', 'glaukonit': 'glauconite', 'ilmenit': 'ilmenite',
    'kromit': 'chromite', 'spineli': 'spinel', 'magnetiti': 'magnetite',
    'granit': 'granite', 'bazalt': 'basalt', 'andezit': 'andesite',
    'riolit': 'rhyolite', 'gabro': 'gabbro', 'diorit': 'diorite',
    'gnejs': 'gneiss', 'mramor': 'marble', 'kvarcit': 'quartzite',
    'meteorit': 'meteorite', 'fosil': 'fossil', 'mineral': 'mineral',
}
_MINERAL_TRANSLATIONS_REVERSE = {}
for _key, _value in _MINERAL_TRANSLATIONS.items():
    if _value not in _MINERAL_TRANSLATIONS_REVERSE:
        _MINERAL_TRANSLATIONS_REVERSE[_value] = _key


def _translate_words(query, mapping):
    query_lower = query.lower().strip()
    words = query_lower.split()
    translated_words = []
    any_translated = False

    for word in words:
        if word in mapping:
            translated_words.append(mapping[word])
            any_translated = True
        else:
            translated_words.append(word)

    if any_translated:
        return ' '.join(translated_words), query
    return query, None


def render_nhm_data_portal():
    """Natural History Museum London Data Portal dashboard."""
    from nhm_data_portal_api import get_nhm_api
    from nhm_dataset_downloader import get_nhm_local_search

    nhm = get_nhm_api()
    local_search = get_nhm_local_search()

    local_available = local_search.is_available()
    local_stats = local_search.get_statistics() if local_available else {}
    api_status = nhm.get_status()

    use_local = request.args.get('source', 'local' if local_available else 'api') == 'local'
    search_query = request.args.get('q', '').strip()
    department = request.args.get('department', '')
    tag_filter = request.args.get('tag', '').strip()
    format_filter = request.args.get('format', '').strip()
    page = _safe_int(request.args.get('page', 1), 1)
    if page < 1:
        page = 1
    rows = 20
    offset = (page - 1) * rows

    results = None
    error = None
    total_results = 0
    all_tags = []
    all_formats = []

    if use_local and local_available:
        try:
            filters = {}
            if tag_filter:
                filters['tag'] = tag_filter
            if format_filter:
                filters['format'] = format_filter
            if department:
                search_query = f"{search_query} {department}".strip()

            search_result = local_search.search(
                query=search_query,
                filters=filters,
                limit=rows,
                offset=offset,
            )

            if search_result['success']:
                results = {
                    'results': search_result['results'],
                    'count': search_result['total'],
                }
                total_results = search_result['total']

            all_tags = local_search.get_all_tags()[:50]
            all_formats = local_search.get_all_formats()
        except Exception as exc:
            error = 'Грешка приликом локалне претраге.'
            logger.error("NHM local search error: %s", exc)
    elif api_status['connected']:
        try:
            if search_query:
                results = nhm.search_datasets(query=search_query, rows=rows, start=offset)
            elif department:
                results = nhm.search_by_department(department, rows=rows, start=offset)
            else:
                results = nhm.search_datasets(
                    rows=rows,
                    start=offset,
                    sort='metadata_modified desc',
                )

            total_results = results.get('count', 0)
        except Exception as exc:
            error = 'Грешка приликом претраге.'
            logger.error("NHM Data Portal search error: %s", exc)
    else:
        error = 'NHM Data Portal није доступан и локални подаци нису преузети.'

    total_pages = (total_results + rows - 1) // rows if total_results > 0 else 1
    status = {
        'connected': api_status['connected'],
        'local_available': local_available,
        'local_datasets': local_stats.get('total_datasets', 0),
        'local_download_date': local_stats.get('download_date', ''),
        'total_datasets': local_stats.get('total_datasets', 0)
        if local_available
        else api_status.get('total_datasets', 286),
        'using_local': use_local and local_available,
    }

    return render_template(
        'admin_nhm_data_portal.html',
        status=status,
        search_query=search_query,
        department=department,
        tag_filter=tag_filter,
        format_filter=format_filter,
        results=results,
        total_results=total_results,
        page=page,
        total_pages=total_pages,
        rows=rows,
        error=error,
        departments=nhm.DEPARTMENTS,
        all_tags=all_tags,
        all_formats=all_formats,
    )


def api_nhm_search():
    """Search NHM datasets via the remote API."""
    from nhm_data_portal_api import get_nhm_api

    nhm = get_nhm_api()
    if not nhm.get_status()['connected']:
        return _api_error_response('NHM Data Portal недоступан', status=503)

    query = request.args.get('q', '').strip()
    rows = min(_safe_int(request.args.get('rows', 25), 25), 100)
    start = _safe_int(request.args.get('start', 0), 0)

    try:
        results = nhm.search_datasets(query=query or '*:*', rows=rows, start=start)
        return jsonify({'success': True, 'results': results, 'query': query})
    except Exception as exc:
        logger.error("NHM search error: %s", exc)
        return _api_error_response('Грешка при претрази NHM података')


def api_nhm_dataset(dataset_id):
    """Get NHM dataset metadata."""
    from nhm_data_portal_api import get_nhm_api

    nhm = get_nhm_api()
    if not nhm.get_status()['connected']:
        return _api_error_response('NHM Data Portal недоступан', status=503)

    try:
        dataset = nhm.get_dataset(dataset_id)
        if not dataset:
            return _api_error_response('Датасет није пронађен', status=404)
        return jsonify({'success': True, 'dataset': dataset})
    except Exception as exc:
        logger.error("NHM dataset error: %s", exc)
        return _api_error_response('Грешка при учитавању NHM датасета')


def api_nhm_resource(resource_id):
    """Get NHM resource metadata."""
    from nhm_data_portal_api import get_nhm_api

    nhm = get_nhm_api()
    if not nhm.get_status()['connected']:
        return _api_error_response('NHM Data Portal недоступан', status=503)

    try:
        resource = nhm.get_resource(resource_id)
        if not resource:
            return _api_error_response('Ресурс није пронађен', status=404)
        return jsonify({'success': True, 'resource': resource})
    except Exception as exc:
        logger.error("NHM resource error: %s", exc)
        return _api_error_response('Грешка при учитавању NHM ресурса')


def api_nhm_datastore(resource_id):
    """Search inside an NHM datastore resource."""
    from nhm_data_portal_api import get_nhm_api

    nhm = get_nhm_api()
    if not nhm.get_status()['connected']:
        return _api_error_response('NHM Data Portal недоступан', status=503)

    try:
        query = request.args.get('q', '')
        limit = min(int(request.args.get('limit', 100)), 500)
        offset = int(request.args.get('offset', 0))
        results = nhm.datastore_search(
            resource_id=resource_id,
            query=query,
            limit=limit,
            offset=offset,
        )
        return jsonify({'success': True, 'results': results})
    except Exception as exc:
        logger.error("NHM datastore error: %s", exc)
        return _api_error_response('Грешка при претрази NHM datastore ресурса')


def api_nhm_statistics():
    """Get NHM site statistics."""
    from nhm_data_portal_api import get_nhm_api

    nhm = get_nhm_api()
    try:
        stats = nhm.get_site_statistics()
        return jsonify({'success': True, 'statistics': stats})
    except Exception as exc:
        logger.error("NHM statistics error: %s", exc)
        return _api_error_response('Грешка при учитавању NHM статистике')


def api_nhm_local_search():
    """Search locally downloaded NHM datasets."""
    from nhm_dataset_downloader import get_nhm_local_search

    search = get_nhm_local_search()
    if not search.is_available():
        return (
            jsonify(
                {
                    'success': False,
                    'error': 'Локални подаци нису доступни. Потребно је преузети датасетове.',
                    'available': False,
                }
            ),
            404,
        )

    query = request.args.get('q', '').strip()
    tag = request.args.get('tag', '').strip()
    author = request.args.get('author', '').strip()
    format_type = request.args.get('format', '').strip()
    limit = max(1, min(_safe_int(request.args.get('limit', 50), 50), 200))
    offset = max(0, _safe_int(request.args.get('offset', 0), 0))

    filters = {}
    if tag:
        filters['tag'] = tag
    if author:
        filters['author'] = author
    if format_type:
        filters['format'] = format_type

    try:
        return jsonify(search.search(query, filters=filters, limit=limit, offset=offset))
    except Exception as exc:
        logger.error("NHM local search error: %s", exc)
        return _api_error_response('Грешка при локалној претрази NHM података')


def api_nhm_local_dataset(dataset_name):
    """Get a locally stored NHM dataset."""
    from nhm_dataset_downloader import get_nhm_local_search

    search = get_nhm_local_search()
    if not search.is_available():
        return _api_error_response('Локални подаци нису доступни', status=404)

    try:
        dataset = search.get_dataset(dataset_name)
        if not dataset:
            return _api_error_response('Датасет није пронађен', status=404)
        return jsonify({'success': True, 'dataset': dataset})
    except Exception as exc:
        logger.error("NHM local dataset error: %s", exc)
        return _api_error_response('Грешка при учитавању локалног NHM датасета')


def api_nhm_local_statistics():
    """Get statistics about locally downloaded NHM data."""
    from nhm_dataset_downloader import get_nhm_local_search

    search = get_nhm_local_search()
    try:
        return jsonify({'success': True, 'statistics': search.get_statistics()})
    except Exception as exc:
        logger.error("NHM local statistics error: %s", exc)
        return _api_error_response('Грешка при учитавању локалне NHM статистике')


def api_nhm_local_tags():
    """Get all tags from local NHM datasets."""
    from nhm_dataset_downloader import get_nhm_local_search

    search = get_nhm_local_search()
    if not search.is_available():
        return _api_error_response('Локални подаци нису доступни', status=404)

    try:
        return jsonify({'success': True, 'tags': search.get_all_tags()})
    except Exception as exc:
        logger.error("NHM local tags error: %s", exc)
        return _api_error_response('Грешка при учитавању NHM тагова')


def api_nhm_local_formats():
    """Get all resource formats from local NHM datasets."""
    from nhm_dataset_downloader import get_nhm_local_search

    search = get_nhm_local_search()
    if not search.is_available():
        return _api_error_response('Локални подаци нису доступни', status=404)

    try:
        return jsonify({'success': True, 'formats': search.get_all_formats()})
    except Exception as exc:
        logger.error("NHM local formats error: %s", exc)
        return _api_error_response('Грешка при учитавању NHM формата')


def api_nhm_local_authors():
    """Get all authors from local NHM datasets."""
    from nhm_dataset_downloader import get_nhm_local_search

    search = get_nhm_local_search()
    if not search.is_available():
        return _api_error_response('Локални подаци нису доступни', status=404)

    try:
        return jsonify({'success': True, 'authors': search.get_all_authors(limit=100)})
    except Exception as exc:
        logger.error("NHM local authors error: %s", exc)
        return _api_error_response('Грешка при учитавању NHM аутора')


def api_nhm_download_datasets():
    """Download or update NHM datasets."""
    from nhm_dataset_downloader import get_nhm_downloader

    downloader = get_nhm_downloader()
    try:
        action = request.json.get('action', 'update') if request.is_json else 'update'
        if action == 'full':
            result = downloader.download_all_datasets()
        else:
            result = downloader.update_datasets()
        return jsonify({'success': True, 'result': result})
    except Exception as exc:
        logger.error("NHM download error: %s", exc)
        return _api_error_response('Грешка при преузимању NHM датасетова')


def api_nhm_data_search_local():
    """Search local museum databases with Serbian/English mineral translation."""
    query = request.args.get('q', '').strip()
    data_type = request.args.get('type', 'all')
    limit = max(1, min(_safe_int(request.args.get('limit', 50), 50), 100))

    if not query:
        return jsonify({'success': True, 'results': [], 'total': 0})

    translated_query, _ = _translate_words(query, _MINERAL_TRANSLATIONS_REVERSE)
    search_queries = [query.lower()]
    if translated_query.lower() != query.lower():
        search_queries.append(translated_query.lower())

    results = []

    try:
        if data_type in ('all', 'minerals'):
            from mineral_database_pg import MineralDatabase

            mineral_db = MineralDatabase()
            if mineral_db.available:
                seen_ids = set()
                for search_query in search_queries:
                    search_result = mineral_db.search_minerals(search_query)
                    if isinstance(search_result, dict):
                        minerals = search_result.get('minerals', search_result.get('results', []))
                    else:
                        minerals = search_result if isinstance(search_result, list) else []

                    for mineral in list(minerals):
                        mineral_id = mineral.get('id') or mineral.get('inventarni_broj')
                        if mineral_id is not None:
                            if mineral_id in seen_ids:
                                continue
                            seen_ids.add(mineral_id)
                        results.append(
                            {
                                'type': 'mineral',
                                'id': mineral.get('id'),
                                'naziv': mineral.get('naziv') or mineral.get('predmet'),
                                'inventarni_broj': mineral.get('inventarni_broj'),
                                'lokalitet': mineral.get('lokalitet'),
                                'gde_se_nalazi': mineral.get('gde_se_nalazi'),
                                'hemijska_formula': mineral.get('hemijska_formula'),
                                'kristalni_sistem': mineral.get('kristalni_sistem'),
                                'boja': mineral.get('boja'),
                                'sjaj': mineral.get('sjaj'),
                                'tvrdoca': mineral.get('tvrdoca'),
                                'gustina': mineral.get('gustina'),
                                'cep': mineral.get('cep'),
                                'lom': mineral.get('lom'),
                                'providnost': mineral.get('providnost'),
                                'napomena': mineral.get('napomena'),
                                'drzava': mineral.get('drzava'),
                                'kutija': mineral.get('kutija'),
                            }
                        )

        if data_type in ('all', 'specimens') and len(results) < limit:
            try:
                from bird_ringing_database import get_bird_ringing_database

                bird_db = get_bird_ringing_database()
                birds = bird_db.search(query, limit=20)
                for bird in birds:
                    results.append(
                        {
                            'type': 'bird',
                            'naziv': bird.get('species') or bird.get('scientific_name'),
                            'locality': bird.get('locality') or bird.get('location'),
                        }
                    )
            except Exception:
                logger.debug("Bird ringing local search unavailable", exc_info=True)

        return jsonify(
            {
                'success': True,
                'results': results[:limit],
                'total': len(results),
                'query': query,
                'translated_query': translated_query if translated_query != query else None,
            }
        )
    except Exception as exc:
        logger.error("Local data search error: %s", exc)
        return _api_error_response('Грешка при претрази локалних података', results=[])


def api_nhm_data_search_nhm():
    """Search NHM specimen data via API with Serbian/English mineral translation."""
    from nhm_data_portal_api import get_nhm_api

    query = request.args.get('q', '').strip()
    limit = max(1, min(_safe_int(request.args.get('limit', 50), 50), 100))
    offset = max(_safe_int(request.args.get('offset', 0), 0), 0)

    if not query:
        return jsonify({'success': True, 'results': [], 'total': 0})

    translated_query, _ = _translate_words(query, _MINERAL_TRANSLATIONS)
    nhm = get_nhm_api()

    if not nhm.get_status()['connected']:
        return _api_error_response('NHM API unavailable', status=503, results=[])

    try:
        specimen_resource = '05ff2255-c38a-40c9-b657-4ccb55ab2feb'
        logger.info(
            "NHM search: original='%s', translated='%s', offset=%s",
            query,
            translated_query,
            offset,
        )
        result = nhm.datastore_search(
            specimen_resource,
            query=translated_query,
            limit=limit,
            offset=offset,
        )
        logger.info(
            "NHM search result: total=%s, records=%s",
            result.get('total', 0),
            len(result.get('records', [])),
        )

        records = []
        for record in result.get('records', []):
            records.append(
                {
                    '_id': record.get('_id'),
                    'scientificName': record.get('scientificName'),
                    'catalogNumber': record.get('catalogNumber'),
                    'country': record.get('country'),
                    'locality': record.get('locality'),
                    'collectionCode': record.get('collectionCode'),
                    'typeStatus': record.get('typeStatus'),
                    'family': record.get('family'),
                    'genus': record.get('genus'),
                    'specificEpithet': record.get('specificEpithet'),
                    'recordedBy': record.get('recordedBy'),
                    'year': record.get('year'),
                    'decimalLatitude': record.get('decimalLatitude'),
                    'decimalLongitude': record.get('decimalLongitude'),
                    'basisOfRecord': record.get('basisOfRecord'),
                    'associatedMedia': bool(record.get('associatedMedia')),
                }
            )

        return jsonify(
            {
                'success': True,
                'results': records,
                'total': result.get('total', len(records)),
                'query': query,
                'translated_query': translated_query if translated_query != query else None,
            }
        )
    except Exception as exc:
        logger.error("NHM data search error: %s", exc)
        return _api_error_response('Грешка при претрази NHM specimen података', results=[])
