"""Central registry for museum collection list views and access control."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Iterable, Literal, Tuple

import bilja_collections_db

RenderMode = Literal['standard', 'meteorite']


@dataclass(frozen=True)
class CollectionListEntry:
    collection_type: str
    module_key: str
    route_slug: str
    collection_name: str
    collection_icon: str
    database_attr: str
    render_mode: RenderMode = 'standard'
    collection_actions_enabled: bool = True
    collection_add_enabled: bool = True
    collection_export_enabled: bool = True
    strip_source_file: bool = False


_STANDARD_COLLECTIONS: Tuple[CollectionListEntry, ...] = (
    CollectionListEntry(
        'botany', 'botany_collection', 'botany_collection',
        'Ботаничка збирка', 'bi-flower1', 'BOTANY_COLLECTION_DATABASE',
    ),
    CollectionListEntry(
        'ichthyology', 'ichthyology_collection', 'ichthyology_collection',
        'Ихтиолошка збирка', 'museum-icon-fish', 'ICHTHYOLOGY_COLLECTION_DATABASE',
    ),
    CollectionListEntry(
        'entomology', 'entomology_collection', 'entomology_collection',
        'Ентомолошка збирка', 'bi-bug', 'ENTOMOLOGY_COLLECTION_DATABASE',
    ),
    CollectionListEntry(
        'mycology', 'mycology_collection', 'mycology_collection',
        'Миколошка збирка', 'museum-icon-mushroom', 'MYCOLOGY_COLLECTION_DATABASE',
    ),
    CollectionListEntry(
        'herpetology', 'herpetology_collection', 'herpetology_collection',
        'Херпетолошка збирка', 'museum-icon-snake', 'HERPETOLOGY_COLLECTION_DATABASE',
    ),
    CollectionListEntry(
        'ornithology', 'ornithology_collection', 'ornithology_collection',
        'Орнитолошка збирка', 'museum-icon-bird', 'ORNITHOLOGY_COLLECTION_DATABASE',
    ),
    CollectionListEntry(
        'paleozoology', 'paleozoology_collection', 'paleozoology_collection',
        'Палеозоолошка збирка', 'museum-icon-dinosaur', 'PALEOZOOLOGY_COLLECTION_DATABASE',
    ),
    CollectionListEntry(
        'sanja_paleogene_neogene_mammals', 'sanja_paleogene_neogene_mammals',
        'sanja_paleogene_neogene_mammals',
        'Крупни сисари палеогена и неогена', 'museum-icon-mammoth',
        'SANJA_PALEOGENE_NEOGENE_MAMMALS_DATABASE',
        strip_source_file=True,
        collection_actions_enabled=False,
        collection_add_enabled=True,
        collection_export_enabled=False,
    ),
    CollectionListEntry(
        'paleobotany', 'paleobotany_collection', 'paleobotany_collection',
        'Палеоботаничка збирка', 'bi-flower2', 'PALEOBOTANY_COLLECTION_DATABASE',
    ),
    CollectionListEntry(
        'petrology', 'petrology_collection', 'petrology_collection',
        'Петролошка збирка', 'bi-mountains', 'PETROLOGY_COLLECTION_DATABASE',
    ),
    CollectionListEntry(
        'meteorite', 'meteorite_collection', 'meteorite_collection',
        'Збирка метеорита', 'bi-moon-stars', 'METEORITE_COLLECTION_DATABASE',
        render_mode='meteorite',
    ),
)


def _bilja_collection_entries() -> Tuple[CollectionListEntry, ...]:
    entries = []
    for collection_key, cfg in bilja_collections_db.COLLECTIONS.items():
        entries.append(CollectionListEntry(
            collection_type=collection_key,
            module_key=cfg['module_key'],
            route_slug=cfg['route'],
            collection_name=cfg['name_sr'],
            collection_icon=cfg['icon'],
            database_attr=f'{collection_key.upper()}_DATABASE',
            strip_source_file=True,
            collection_actions_enabled=True,
            collection_add_enabled=True,
            collection_export_enabled=False,
        ))
    return tuple(entries)


COLLECTION_LIST_ENTRIES: Tuple[CollectionListEntry, ...] = (
    _STANDARD_COLLECTIONS + _bilja_collection_entries()
)

COLLECTION_LIST_ENTRY_BY_TYPE: Dict[str, CollectionListEntry] = {
    entry.collection_type: entry for entry in COLLECTION_LIST_ENTRIES
}

COLLECTION_TYPE_MODULE_MAP: Dict[str, str] = {
    entry.collection_type: entry.module_key for entry in COLLECTION_LIST_ENTRIES
}
COLLECTION_TYPE_MODULE_MAP['mineral'] = 'mineral_database'


def get_collection_route_map() -> Dict[str, str]:
    """Map collection_type to Flask endpoint slug."""
    return {entry.collection_type: entry.route_slug for entry in COLLECTION_LIST_ENTRIES}


def get_collection_form_info() -> Dict[str, Dict[str, str]]:
    """Map collection_type to display name and route slug for add-item forms."""
    return {
        entry.collection_type: {
            'name': entry.collection_name,
            'route': entry.route_slug,
        }
        for entry in COLLECTION_LIST_ENTRIES
    }


def iter_collection_list_entries() -> Iterable[CollectionListEntry]:
    return COLLECTION_LIST_ENTRIES


def resolve_collection_database(museum_app, entry: CollectionListEntry):
    """Load the in-memory database dict for a registered collection."""
    if entry.render_mode == 'meteorite':
        return museum_app.get_meteorite_collection_database()
    return getattr(museum_app, entry.database_attr, None)


def build_collection_database_map(museum_app) -> Dict[str, dict]:
    """Map module_key to in-memory collection database for overview/counts."""
    return {
        entry.module_key: resolve_collection_database(museum_app, entry)
        for entry in COLLECTION_LIST_ENTRIES
    }


def get_overview_collection_type_map() -> Dict[str, str]:
    """Map overview card key (module_key) to collection_type for QR/image helpers."""
    return {entry.module_key: entry.collection_type for entry in COLLECTION_LIST_ENTRIES}
