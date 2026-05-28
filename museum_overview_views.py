"""Shared route implementations for museum overview pages."""

import logging
import os
from typing import Dict

from flask import render_template, session

from collection_registry import COLLECTION_LIST_ENTRIES, get_overview_collection_type_map

logger = logging.getLogger(__name__)


def _collection_total(collection: Dict, stats_key: str = 'total_specimens'):
    if not collection:
        return None
    stats = collection.get('statistics', {})
    value = stats.get(stats_key)
    if value is None:
        if 'specimens' in collection:
            value = len(collection['specimens'])
        elif 'records' in collection:
            value = len(collection['records'])
    return value


def _resolve_collection_databases(
    collection_databases=None,
    *,
    get_meteorite_collection_database=None,
    botany_collection_database=None,
    ichthyology_collection_database=None,
    entomology_collection_database=None,
    mycology_collection_database=None,
    herpetology_collection_database=None,
    ornithology_collection_database=None,
    paleozoology_collection_database=None,
    paleobotany_collection_database=None,
    petrology_collection_database=None,
):
    """Support both registry map callers and legacy per-collection kwargs."""
    if collection_databases is not None:
        return collection_databases

    legacy_map = {
        'botany_collection': botany_collection_database,
        'ichthyology_collection': ichthyology_collection_database,
        'entomology_collection': entomology_collection_database,
        'mycology_collection': mycology_collection_database,
        'herpetology_collection': herpetology_collection_database,
        'ornithology_collection': ornithology_collection_database,
        'paleozoology_collection': paleozoology_collection_database,
        'paleobotany_collection': paleobotany_collection_database,
        'petrology_collection': petrology_collection_database,
        'meteorite_collection': (
            get_meteorite_collection_database() if get_meteorite_collection_database else None
        ),
    }

    try:
        import app as museum_app
        from collection_registry import COLLECTION_LIST_ENTRIES, resolve_collection_database

        for entry in COLLECTION_LIST_ENTRIES:
            if entry.module_key not in legacy_map:
                legacy_map[entry.module_key] = resolve_collection_database(museum_app, entry)
    except Exception as exc:  # pragma: no cover
        logger.warning('Could not hydrate registry-backed collection databases: %s', exc)

    return legacy_map


def render_museum_databases(
    *,
    library_database,
    get_employee_directory,
    get_museum_employees,
    get_mineral_database,
    get_cultural_heritage_database,
    get_exhibit_statistics,
    get_exhibition_statistics,
    bird_ringing_database,
    scientific_papers_database,
    collection_databases=None,
    conservation_biology_database,
    visitor_records,
    research_projects,
    get_qr_collection_action_url,
    get_image_upload_action_url,
    get_image_upload_module_key,
    user_has_module_access,
    get_meteorite_collection_database=None,
    botany_collection_database=None,
    ichthyology_collection_database=None,
    entomology_collection_database=None,
    mycology_collection_database=None,
    herpetology_collection_database=None,
    ornithology_collection_database=None,
    paleozoology_collection_database=None,
    paleobotany_collection_database=None,
    petrology_collection_database=None,
):
    """Render overview of all museum databases."""
    collection_databases = _resolve_collection_databases(
        collection_databases,
        get_meteorite_collection_database=get_meteorite_collection_database,
        botany_collection_database=botany_collection_database,
        ichthyology_collection_database=ichthyology_collection_database,
        entomology_collection_database=entomology_collection_database,
        mycology_collection_database=mycology_collection_database,
        herpetology_collection_database=herpetology_collection_database,
        ornithology_collection_database=ornithology_collection_database,
        paleozoology_collection_database=paleozoology_collection_database,
        paleobotany_collection_database=paleobotany_collection_database,
        petrology_collection_database=petrology_collection_database,
    )
    user_email = session.get('user_email', '')
    user_role = session.get('user_role', 'user')

    try:
        employee_directory = get_employee_directory()
    except Exception as exc:  # pragma: no cover
        logger.error("Employee directory unavailable: %s", exc)
        employee_directory = []
    employee_count = len(employee_directory)
    profile_count = len([entry for entry in employee_directory if entry.get('description')])

    if employee_count == 0:
        employee_count = len(get_museum_employees())
    if profile_count == 0:
        profile_count = len([entry for entry in get_museum_employees().values() if entry.get('description')])

    mineral_count = None
    try:
        mineral_db = get_mineral_database()
        if mineral_db and getattr(mineral_db, 'available', False):
            mineral_stats = mineral_db.get_statistics() or {}
            mineral_count = mineral_stats.get('total_minerals')
    except Exception as exc:  # pragma: no cover
        logger.error("Mineral statistics unavailable: %s", exc)

    try:
        from inventory_reconciliation import InventoryReconciliation

        reconciliation = InventoryReconciliation()
        inventory_summary = reconciliation.get_inventory_summary()
        inventory_total = inventory_summary.get('total_items')
        inventory_unique = inventory_summary.get('unique_inventory_numbers')
    except Exception as exc:  # pragma: no cover
        logger.error("Inventory summary unavailable: %s", exc)
        inventory_total = None
        inventory_unique = None

    try:
        bird_stats = bird_ringing_database.get_statistics() or {}
    except Exception as exc:  # pragma: no cover
        logger.error("Bird ringing statistics unavailable: %s", exc)
        bird_stats = {}
    bird_count = bird_stats.get('total_records')
    bird_species = bird_stats.get('unique_species')
    bird_locations = bird_stats.get('unique_locations')

    collection_counts = {
        entry.module_key: _collection_total(collection_databases.get(entry.module_key))
        for entry in COLLECTION_LIST_ENTRIES
    }
    collection_counts['conservation_biology'] = _collection_total(
        conservation_biology_database,
        stats_key='total_records',
    )
    collection_counts['zoology_collection'] = None
    collection_counts['geology_conservation'] = None

    try:
        exhibit_stats = get_exhibit_statistics()
    except Exception as exc:  # pragma: no cover
        logger.error("Exhibit statistics unavailable: %s", exc)
        exhibit_stats = {'total_artifacts': 0, 'displayed_artifacts': 0, 'storage_artifacts': 0}

    try:
        exhibition_stats = get_exhibition_statistics()
    except Exception as exc:  # pragma: no cover
        logger.error("Exhibition statistics unavailable: %s", exc)
        exhibition_stats = {'total_exhibitions': 0}

    databases_info = {
        'employees': {
            'name': 'База запослених',
            'description': 'Информације о свим запосленима музеја',
            'icon': 'museum-icon-employees',
            'count': employee_count or '—',
            'status': 'active',
            'url': '/admin/employees_database',
            'color': 'primary',
        },
        'employee_profiles': {
            'name': 'База профила запослених',
            'description': 'Биографије и стручни профили запослених',
            'icon': 'museum-icon-profiles',
            'count': profile_count or '—',
            'status': 'active',
            'url': '/admin/employee_profiles_database',
            'color': 'info',
        },
        'minerals': {
            'name': 'База минерала',
            'description': 'Колекција минерала и геолошких узорака',
            'icon': 'museum-icon-minerals',
            'count': mineral_count or '—',
            'status': 'active',
            'url': '/admin/mineral_collection',
            'color': 'success',
        },
        'library': {
            'name': 'База библиотеке',
            'description': 'Каталог књига и научних публикација',
            'icon': 'museum-icon-library',
            'count': len(library_database.get('books', [])),
            'status': 'active',
            'url': '/admin/library_database',
            'color': 'info',
        },
        'nhm_data_portal': {
            'name': 'NHM London Data Portal',
            'description': 'Датасетови Природњачког музеја у Лондону - 35+ милиона записа',
            'icon': 'museum-icon-portal',
            'count': '286',
            'status': 'active',
            'url': '/admin/nhm_data_portal',
            'color': 'danger',
            'external': True,
        },
        'exhibits': {
            'name': 'База експоната',
            'description': 'Инвентар музејских експоната, стање и локације',
            'icon': 'museum-icon-exhibits',
            'count': exhibit_stats['total_artifacts'],
            'status': 'active',
            'url': '/admin/exhibits_database',
            'color': 'warning',
        },
        'cultural_heritage': {
            'name': 'База заштићених културних добара',
            'description': 'Регистар покретних културних добара под заштитом',
            'icon': 'museum-icon-heritage',
            'count': len(get_cultural_heritage_database()['heritage_items']),
            'status': 'active',
            'url': '/admin/cultural_heritage_database',
            'color': 'warning',
        },
        'visitors': {
            'name': 'База посетилаца',
            'description': 'Статистике и информације о посетиоцима',
            'icon': 'museum-icon-visitors',
            'count': len(visitor_records),
            'status': 'active',
            'url': '/admin/visitors_database',
            'color': 'secondary',
        },
        'research': {
            'name': 'База истраживања',
            'description': 'Научни радови и истраживачки пројекти',
            'icon': 'museum-icon-research',
            'count': len(research_projects),
            'status': 'active',
            'url': '/admin/research_database',
            'color': 'dark',
        },
        'bird_ringing': {
            'name': 'База прстеновања птица',
            'description': 'Комплетна база података о прстенованим птицама - '
            f"{bird_species or '325'} врста, {bird_locations or '979'} локација",
            'icon': 'museum-icon-bird-ringing',
            'count': bird_count or '—',
            'status': 'active',
            'url': '/admin/bird_ringing_database',
            'color': 'info',
            'curator': 'vuk.popic@nhmbeo.rs',
        },
        'scientific_papers': {
            'name': 'База научних радова',
            'description': 'Научне публикације повезане са геолошким картама Србије (ОГК)',
            'icon': 'museum-icon-papers',
            'count': scientific_papers_database.get_statistics().get('total_papers', 0)
            if os.path.exists('data/scientific_papers.db')
            else '—',
            'status': 'active' if os.path.exists('data/scientific_papers.db') else 'planned',
            'url': '/admin/scientific_papers',
            'color': 'dark',
        },
        'exhibitions': {
            'name': 'База изложби',
            'description': 'Архива галеријских изложби и анализа посећености',
            'icon': 'museum-icon-exhibitions',
            'count': exhibition_stats['total_exhibitions'],
            'status': 'active' if exhibition_stats['total_exhibitions'] else 'planned',
            'url': '/admin/exhibitions_database',
            'color': 'danger',
        },
        'botany_collection': {
            'name': 'Ботаничка збирка',
            'description': 'Хербаријум >40.000 примерака - ендемске биљке Балкана (Др М. Никетић - SANU, В. Стојановић, Др А. Савић, Др М. Несторовић)',
            'icon': 'museum-icon-botany',
            'count': collection_counts['botany_collection'] or '—',
            'status': 'active',
            'url': '/admin/botany_collection',
            'color': 'success',
            'curators': ['mniketic@nhmbeo.rs', 'verica.stojanovic@nhmbeo.rs', 'aleksandra.savic@nhmbeo.rs', 'marko.nestorovic@nhmbeo.rs'],
        },
        'ichthyology_collection': {
            'name': 'Ихтиолошка збирка',
            'description': 'Колекција риба и водених организама - виши кустос (Д. Вучић)',
            'icon': 'museum-icon-fish',
            'count': collection_counts['ichthyology_collection'] or '—',
            'status': 'active',
            'url': '/admin/ichthyology_collection',
            'color': 'info',
            'curators': ['dubravka.vucic@nhmbeo.rs'],
        },
        'entomology_collection': {
            'name': 'Ентомолошка збирка',
            'description': 'Колекција инсеката - 1.710 врста приказано, збирка Odonata (М. Јовић - координатор Balkan OdoBase, А. Стојановић - конзерватор)',
            'icon': 'museum-icon-entomology',
            'count': collection_counts['entomology_collection'] or '—',
            'status': 'active',
            'url': '/admin/entomology_collection',
            'color': 'warning',
            'curators': ['milos.jovic@nhmbeo.rs', 'aleksandar@nhmbeo.rs'],
        },
        'mycology_collection': {
            'name': 'Миколошка збирка',
            'description': 'Колекција гљива и макромицета Балкана (Др Б. Иванчевић - 30+ година истраживања)',
            'icon': 'museum-icon-mushroom',
            'count': collection_counts['mycology_collection'] or '—',
            'status': 'active',
            'url': '/admin/mycology_collection',
            'color': 'success',
            'curators': ['boris@nhmbeo.rs'],
        },
        'herpetology_collection': {
            'name': 'Херпетолошка збирка',
            'description': 'Колекција водоземаца и гмизаваца - 20+ година теренских истраживања (Др А. Пауновић)',
            'icon': 'museum-icon-snake',
            'count': collection_counts['herpetology_collection'] or '—',
            'status': 'active',
            'url': '/admin/herpetology_collection',
            'color': 'danger',
            'curators': ['ana.paunovic@nhmbeo.rs'],
        },
        'ornithology_collection': {
            'name': 'Орнитолошка збирка',
            'description': 'Колекција птица - Центар за маркирање (прстеновање) птица, програм Euring (Мср В. Попић)',
            'icon': 'museum-icon-bird',
            'count': collection_counts['ornithology_collection'] or '—',
            'status': 'active',
            'url': '/admin/ornithology_collection',
            'color': 'primary',
            'curators': ['vuk.popic@nhmbeo.rs'],
        },
        'zoology_collection': {
            'name': 'Општа зоолошка збирка',
            'description': 'Зоолошка колекција - молекуларна биологија и ДНК баркодирање (З. Марковић - MSc)',
            'icon': 'museum-icon-zoology',
            'count': collection_counts['zoology_collection'] or '—',
            'status': 'development',
            'url': '#',
            'color': 'info',
            'curators': ['zorana.markovic@nhmbeo.rs'],
        },
        'conservation_biology': {
            'name': 'Конзервација биолошких збирки',
            'description': 'Препарација и очување биолошких експоната (Г. Петковски - конзерватор, М. Мрваљевић, Ј. Кокотовић)',
            'icon': 'museum-icon-conservation',
            'count': collection_counts['conservation_biology'] or '—',
            'status': 'active',
            'url': '/admin/conservation_biology',
            'color': 'secondary',
            'curators': ['gorana.petkovski@nhmbeo.rs', 'milos.mrvaljevic@nhmbeo.rs', 'jovan.kokotovic@nhmbeo.rs'],
        },
        'paleozoology_collection': {
            'name': 'Палеозоолошка збирка',
            'description': 'Фосили животиња - први диносауруси Србије, крупни сисари (Др Б. Митровић - начелник, Др З. Марковић, С. Алабурић, Др Д. Ђурић, Р. Пејовић, М. Миливојевић)',
            'icon': 'museum-icon-dinosaur',
            'count': collection_counts['paleozoology_collection'] or '—',
            'status': 'active',
            'url': '/admin/paleozoology_collection',
            'color': 'warning',
            'curators': ['biljana.mitrovic@nhmbeo.rs', 'zoran.markovic@nhmbeo.rs', 'sanja.pavic@nhmbeo.rs', 'dragana.djuric@nhmbeo.rs', 'pejovic.ranko@nhmbeo.rs', 'milos.milivojevic@nhmbeo.rs'],
        },
        'paleobotany_collection': {
            'name': 'Палеоботаничка збирка',
            'description': 'Фосилне биљке и праисторијска вегетација - кустос од 1993, професор палеоекологије (Др Д. Ђорђевић-Милутиновић)',
            'icon': 'museum-icon-paleobotany',
            'count': collection_counts['paleobotany_collection'] or '—',
            'status': 'active',
            'url': '/admin/paleobotany_collection',
            'color': 'success',
            'curators': ['desadjm@nhmbeo.rs'],
        },
        'petrology_collection': {
            'name': 'Петролошка збирка',
            'description': 'Колекција стена Србије - петрографија и геохемија (Т. Милић Бабић - виши кустос)',
            'icon': 'museum-icon-petrology',
            'count': collection_counts['petrology_collection'] or '—',
            'status': 'active',
            'url': '/admin/petrology_collection',
            'color': 'secondary',
            'curators': ['tatjana.milicbabic@nhmbeo.rs'],
        },
        'meteorite_collection': {
            'name': 'Збирка метеорита',
            'description': 'Колекција метеорита Србије - Сокобањски метеорит и други (Др А. Луковић - минералог)',
            'icon': 'museum-icon-shooting-star',
            'count': collection_counts['meteorite_collection'] or '—',
            'status': 'active',
            'url': '/admin/meteorite_collection',
            'color': 'warning',
            'curators': ['aca.lukovic@nhmbeo.rs'],
        },
        'geology_conservation': {
            'name': 'Геолошка збирка и конзервација',
            'description': 'Геолошки узорци, препарација и конзервација фосила (Б. Радуловић - кустос, Н. Младеновић - конзерватор)',
            'icon': 'museum-icon-geology-conservation',
            'count': collection_counts['geology_conservation'] or '—',
            'status': 'development',
            'url': '#',
            'color': 'dark',
            'curators': ['branko.radulovic@nhmbeo.rs', 'nenad.mladenovic@nhmbeo.rs'],
        },
        # --- Bilja mollusc collections ---
        'bilja_kenozojske_invertebrate': {
            'name': 'Кенозојски инвертебрати',
            'description': 'Фосилни инвертебрати (квартар/дилувијум) — палеозоолошка збирка.',
            'icon': 'museum-icon-dinosaur',
            'count': collection_counts.get('bilja_kenozojske_invertebrate') or '—',
            'status': 'active',
            'url': '/admin/bilja_kenozojske_invertebrate',
            'color': 'warning',
            'curators': [],
        },
        'bilja_hydrobioidea_radoman': {
            'name': 'Hydrobioidea — збирка П. Радомана',
            'description': 'Рецентни гастроподи (слатководни/бракични), тип-примерци (холотипови/паратипови).',
            'icon': 'museum-icon-snail',
            'count': collection_counts.get('bilja_hydrobioidea_radoman') or '—',
            'status': 'active',
            'url': '/admin/bilja_hydrobioidea_radoman',
            'color': 'info',
            'curators': [],
        },
        'bilja_suvozemni_puzevi_pavlovic': {
            'name': 'Сувоземни пужеви — П. С. Павловић',
            'description': 'Рецентни копнени гастроподи — историјска збирка П. С. Павловића.',
            'icon': 'museum-icon-snail',
            'count': collection_counts.get('bilja_suvozemni_puzevi_pavlovic') or '—',
            'status': 'active',
            'url': '/admin/bilja_suvozemni_puzevi_pavlovic',
            'color': 'success',
            'curators': [],
        },
        'bilja_opsta_zbirka_mollusca': {
            'name': 'Општа збирка мекушаца',
            'description': 'Општа збирка мекушаца (Bivalvia + Gastropoda), разни сакупљачи.',
            'icon': 'museum-icon-shell',
            'count': collection_counts.get('bilja_opsta_zbirka_mollusca') or '—',
            'status': 'active',
            'url': '/admin/bilja_opsta_zbirka_mollusca',
            'color': 'primary',
            'curators': [],
        },
        'bilja_skoljke_tadic': {
            'name': 'Збирка шкољки — А. Тадић',
            'description': 'Рецентни слатководни бивалви (Unio и др.) — збирка Анте Тадића.',
            'icon': 'museum-icon-shell',
            'count': collection_counts.get('bilja_skoljke_tadic') or '—',
            'status': 'active',
            'url': '/admin/bilja_skoljke_tadic',
            'color': 'info',
            'curators': [],
        },
        'bilja_recentni_morski_mekusci': {
            'name': 'Рецентни морски мекушци',
            'description': 'Рецентни морски мекушци (Bivalvia + Gastropoda).',
            'icon': 'museum-icon-shell',
            'count': collection_counts.get('bilja_recentni_morski_mekusci') or '—',
            'status': 'active',
            'url': '/admin/bilja_recentni_morski_mekusci',
            'color': 'primary',
            'curators': [],
        },
    }

    registry_collection_types = get_overview_collection_type_map()
    qr_database_map = {
        'minerals': 'minerals',
        'cultural_heritage': 'heritage',
        **registry_collection_types,
    }
    for db_key, collection_type in qr_database_map.items():
        if db_key in databases_info:
            databases_info[db_key]['qr_url'] = get_qr_collection_action_url(collection_type)

    image_upload_database_map = {
        'minerals': 'mineral',
        'cultural_heritage': 'cultural_heritage',
        **registry_collection_types,
    }
    for db_key, database in image_upload_database_map.items():
        module_key = get_image_upload_module_key(database)
        if db_key in databases_info and module_key and user_has_module_access(user_email, user_role, module_key):
            databases_info[db_key]['image_upload_url'] = get_image_upload_action_url(database)

    if inventory_total is not None:
        databases_info['minerals']['inventory_total'] = inventory_total
    if inventory_unique is not None:
        databases_info['minerals']['inventory_unique'] = inventory_unique

    return render_template(
        'admin_museum_databases.html',
        databases=databases_info,
        total_databases=len(databases_info),
    )
