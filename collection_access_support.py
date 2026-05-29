"""Shared QR and batch-image-upload helper logic for collection views."""

import logging
from urllib.parse import quote

from flask import flash, redirect, session, url_for


logger = logging.getLogger(__name__)


class CollectionAccessSupport:
    """Encapsulate QR and image-upload metadata plus access helpers."""

    def __init__(
        self,
        *,
        user_has_module_access,
        get_mineral_database,
        get_meteorite_collection_database,
        get_cultural_heritage_database,
        botany_collection_database,
        ichthyology_collection_database,
        entomology_collection_database,
        mycology_collection_database,
        herpetology_collection_database,
        ornithology_collection_database,
        paleozoology_collection_database,
        paleobotany_collection_database,
        petrology_collection_database,
    ):
        self.user_has_module_access = user_has_module_access
        self.get_mineral_database = get_mineral_database
        self.get_meteorite_collection_database = get_meteorite_collection_database
        self.get_cultural_heritage_database = get_cultural_heritage_database
        self.botany_collection_database = botany_collection_database
        self.ichthyology_collection_database = ichthyology_collection_database
        self.entomology_collection_database = entomology_collection_database
        self.mycology_collection_database = mycology_collection_database
        self.herpetology_collection_database = herpetology_collection_database
        self.ornithology_collection_database = ornithology_collection_database
        self.paleozoology_collection_database = paleozoology_collection_database
        self.paleobotany_collection_database = paleobotany_collection_database
        self.petrology_collection_database = petrology_collection_database

        self.qr_collection_aliases = {
            'meteorites': 'meteorite',
            'geology': 'petrology',
        }
        self.qr_field_labels = {
            'catalog_number': 'Каталошки број',
            'registry_number': 'Регистарски број',
            'record_number': 'Број записа',
            'meteorite_name': 'Назив метеорита',
            'scientific_name': 'Научно име',
            'common_name_sr': 'Народно име',
            'family': 'Фамилија',
            'classification': 'Класификација',
            'rock_name': 'Назив стене',
            'rock_type': 'Тип стене',
            'geological_age': 'Геолошка старост',
            'geological_period': 'Геолошки период',
            'age_million_years': 'Старост (милиони година)',
            'specimen_name': 'Назив примерка',
            'name': 'Назив',
            'subcategory': 'Поткатегорија',
            'category': 'Категорија',
            'significance': 'Значај',
            'condition': 'Стање',
            'location': 'Локација',
            'location_found': 'Локација налаза',
            'habitat': 'Станиште',
            'description': 'Опис',
            'period': 'Период',
            'date_collected': 'Датум прикупљања',
            'collector': 'Сакупљач',
            'curator': 'Кустос',
        }
        self.qr_collection_config = {
            'minerals': {
                'name': 'Минералошка збирка',
                'route': 'admin_mineral_collection',
                'module': 'mineral_database',
            },
            'meteorite': {
                'name': 'Збирка метеорита',
                'route': 'meteorite_collection',
                'module': 'meteorite_collection',
                'loader': self.get_meteorite_collection_database,
                'data_key': 'specimens',
            },
            'botany': {
                'name': 'Ботаничка збирка',
                'route': 'botany_collection',
                'module': 'botany_collection',
                'loader': lambda: self.botany_collection_database,
                'data_key': 'specimens',
            },
            'ichthyology': {
                'name': 'Ихтиолошка збирка',
                'route': 'ichthyology_collection',
                'module': 'ichthyology_collection',
                'loader': lambda: self.ichthyology_collection_database,
                'data_key': 'specimens',
            },
            'entomology': {
                'name': 'Ентомолошка збирка',
                'route': 'entomology_collection',
                'module': 'entomology_collection',
                'loader': lambda: self.entomology_collection_database,
                'data_key': 'specimens',
            },
            'mycology': {
                'name': 'Миколошка збирка',
                'route': 'mycology_collection',
                'module': 'mycology_collection',
                'loader': lambda: self.mycology_collection_database,
                'data_key': 'specimens',
            },
            'herpetology': {
                'name': 'Херпетолошка збирка',
                'route': 'herpetology_collection',
                'module': 'herpetology_collection',
                'loader': lambda: self.herpetology_collection_database,
                'data_key': 'specimens',
            },
            'ornithology': {
                'name': 'Орнитолошка збирка',
                'route': 'ornithology_collection',
                'module': 'ornithology_collection',
                'loader': lambda: self.ornithology_collection_database,
                'data_key': 'specimens',
            },
            'paleozoology': {
                'name': 'Палеозоолошка збирка',
                'route': 'paleozoology_collection',
                'module': 'paleozoology_collection',
                'loader': lambda: self.paleozoology_collection_database,
                'data_key': 'specimens',
            },
            'paleobotany': {
                'name': 'Палеоботаничка збирка',
                'route': 'paleobotany_collection',
                'module': 'paleobotany_collection',
                'loader': lambda: self.paleobotany_collection_database,
                'data_key': 'specimens',
            },
            'petrology': {
                'name': 'Петролошка збирка',
                'route': 'petrology_collection',
                'module': 'petrology_collection',
                'loader': lambda: self.petrology_collection_database,
                'data_key': 'specimens',
            },
            'heritage': {
                'name': 'Културно наслеђе',
                'route': 'cultural_heritage_database',
                'module': 'cultural_heritage',
                'loader': self.get_cultural_heritage_database,
                'data_key': 'heritage_items',
            },
        }
        self.image_upload_aliases = {
            'minerals': 'mineral',
            'meteorites': 'meteorite',
            'heritage': 'cultural_heritage',
        }
        self.image_upload_config = {
            'mineral': {
                'name': 'Минералошка збирка',
                'prefix': 'M',
                'route': 'admin_mineral_collection',
                'module': 'mineral_database',
                'loader': self.load_all_mineral_records_for_image_upload,
                'entity_type': 'collection_item',
            },
            'meteorite': {
                'name': 'Збирка метеорита',
                'prefix': 'MET',
                'route': 'meteorite_collection',
                'module': 'meteorite_collection',
                'loader': lambda: self.get_meteorite_collection_database().get('specimens', []),
                'entity_type': 'collection_item',
            },
            'botany': {
                'name': 'Ботаничка збирка',
                'prefix': 'BOT',
                'route': 'botany_collection',
                'module': 'botany_collection',
                'loader': lambda: self.botany_collection_database.get('specimens', []),
                'entity_type': 'collection_item',
            },
            'ichthyology': {
                'name': 'Ихтиолошка збирка',
                'prefix': 'ICH',
                'route': 'ichthyology_collection',
                'module': 'ichthyology_collection',
                'loader': lambda: self.ichthyology_collection_database.get('specimens', []),
                'entity_type': 'collection_item',
            },
            'entomology': {
                'name': 'Ентомолошка збирка',
                'prefix': 'ENT',
                'route': 'entomology_collection',
                'module': 'entomology_collection',
                'loader': lambda: self.entomology_collection_database.get('specimens', []),
                'entity_type': 'collection_item',
            },
            'mycology': {
                'name': 'Миколошка збирка',
                'prefix': 'MYC',
                'route': 'mycology_collection',
                'module': 'mycology_collection',
                'loader': lambda: self.mycology_collection_database.get('specimens', []),
                'entity_type': 'collection_item',
            },
            'herpetology': {
                'name': 'Херпетолошка збирка',
                'prefix': 'HERP',
                'route': 'herpetology_collection',
                'module': 'herpetology_collection',
                'loader': lambda: self.herpetology_collection_database.get('specimens', []),
                'entity_type': 'collection_item',
            },
            'ornithology': {
                'name': 'Орнитолошка збирка',
                'prefix': 'ORN',
                'route': 'ornithology_collection',
                'module': 'ornithology_collection',
                'loader': lambda: self.ornithology_collection_database.get('specimens', []),
                'entity_type': 'collection_item',
            },
            'paleozoology': {
                'name': 'Палеозоолошка збирка',
                'prefix': 'PAL',
                'route': 'paleozoology_collection',
                'module': 'paleozoology_collection',
                'loader': lambda: self.paleozoology_collection_database.get('specimens', []),
                'entity_type': 'collection_item',
            },
            'paleobotany': {
                'name': 'Палеоботаничка збирка',
                'prefix': 'PBOT',
                'route': 'paleobotany_collection',
                'module': 'paleobotany_collection',
                'loader': lambda: self.paleobotany_collection_database.get('specimens', []),
                'entity_type': 'collection_item',
            },
            'petrology': {
                'name': 'Петролошка збирка',
                'prefix': 'PETR',
                'route': 'petrology_collection',
                'module': 'petrology_collection',
                'loader': lambda: self.petrology_collection_database.get('specimens', []),
                'entity_type': 'collection_item',
            },
            'cultural_heritage': {
                'name': 'Културно наслеђе',
                'prefix': 'КД',
                'route': 'cultural_heritage_database',
                'module': 'cultural_heritage',
                'loader': lambda: self.get_cultural_heritage_database().get('heritage_items', []),
                'entity_type': 'heritage_item',
            },
        }

    def normalize_qr_collection_type(self, collection_type):
        """Normalize legacy QR collection aliases to canonical collection ids."""
        return self.qr_collection_aliases.get(collection_type, collection_type)

    def get_qr_collection_config(self, collection_type):
        """Return QR collection configuration for a canonical or aliased collection id."""
        return self.qr_collection_config.get(self.normalize_qr_collection_type(collection_type))

    def get_qr_collection_name(self, collection_type):
        """Get the human-readable name for a QR-enabled collection."""
        config = self.get_qr_collection_config(collection_type)
        return config['name'] if config else collection_type

    def get_qr_collection_module_key(self, collection_type):
        """Get the module access key required for a QR-enabled collection."""
        config = self.get_qr_collection_config(collection_type)
        return config['module'] if config else None

    def get_qr_collection_url(self, collection_type):
        """Get the collection landing page URL for a QR-enabled collection."""
        config = self.get_qr_collection_config(collection_type)
        if not config:
            return url_for('museum_databases')
        return url_for(config['route'])

    def get_qr_collection_action_url(self, collection_type):
        """Get the scoped QR selection URL for a collection, or None if unsupported."""
        config = self.get_qr_collection_config(collection_type)
        if not config:
            return None
        return url_for(
            'admin_qr_select_specimens',
            collection_type=self.normalize_qr_collection_type(collection_type),
        )

    def get_qr_collection_records(self, collection_type):
        """Load raw records for a QR-enabled collection."""
        config = self.get_qr_collection_config(collection_type)
        if not config or 'loader' not in config:
            return []

        try:
            data = config['loader']() or {}
        except Exception as exc:  # pragma: no cover - depends on DB availability
            logger.error("Failed to load QR records for %s: %s", collection_type, exc)
            return []

        return data.get(config.get('data_key', 'specimens'), [])

    @staticmethod
    def _first_populated_value(record, candidate_keys):
        """Return the first non-empty value from the given keys."""
        if not isinstance(record, dict):
            return None

        for key in candidate_keys:
            value = record.get(key)
            if value not in (None, '', [], {}):
                return value
        return None

    def get_qr_record_identifier(self, record, collection_type):
        """Get the stable identifier used by QR flows for a record."""
        collection_type = self.normalize_qr_collection_type(collection_type)

        if collection_type == 'heritage':
            value = self._first_populated_value(record, ['registry_number', 'inventory_number', 'id'])
        else:
            value = self._first_populated_value(record, ['catalog_number', 'record_number', 'id'])

        return str(value).strip() if value not in (None, '') else ''

    def get_qr_record_catalog_label(self, record, collection_type):
        """Get the human-facing catalog label for a record."""
        collection_type = self.normalize_qr_collection_type(collection_type)

        if collection_type == 'heritage':
            value = self._first_populated_value(record, ['registry_number', 'inventory_number', 'id'])
        else:
            value = self._first_populated_value(record, ['catalog_number', 'record_number', 'id'])

        return str(value).strip() if value not in (None, '') else 'N/A'

    def get_qr_record_name(self, record, collection_type):
        """Get the primary display name for a record."""
        collection_type = self.normalize_qr_collection_type(collection_type)

        preferred_names = {
            'meteorite': ['meteorite_name', 'scientific_name', 'name'],
            'petrology': ['rock_name', 'scientific_name', 'name'],
            'heritage': ['name', 'subcategory', 'category'],
        }
        generic_names = [
            'scientific_name',
            'specimen_name',
            'common_name_sr',
            'name',
            'rock_name',
            'subcategory',
            'category',
        ]

        value = self._first_populated_value(record, preferred_names.get(collection_type, generic_names))
        return str(value).strip() if value not in (None, '') else 'Непознато'

    def get_qr_record_summary(self, record, collection_type):
        """Get a secondary summary field for list and label rendering."""
        collection_type = self.normalize_qr_collection_type(collection_type)

        preferred_summaries = {
            'meteorite': ['classification', 'fall_type', 'location_found'],
            'petrology': ['rock_type', 'geological_age', 'location_found'],
            'heritage': ['category', 'significance', 'condition'],
        }
        generic_summaries = [
            'classification',
            'type',
            'rock_type',
            'family',
            'geological_period',
            'age_million_years',
            'category',
            'condition',
        ]

        value = self._first_populated_value(
            record,
            preferred_summaries.get(collection_type, generic_summaries),
        )
        return str(value).strip() if value not in (None, '') else '-'

    def get_qr_record_location(self, record, collection_type):
        """Get the best-effort location field for filter UI."""
        collection_type = self.normalize_qr_collection_type(collection_type)

        preferred_locations = {'heritage': ['location']}
        generic_locations = ['location_found', 'location', 'habitat']

        value = self._first_populated_value(
            record,
            preferred_locations.get(collection_type, generic_locations),
        )
        return str(value).strip() if value not in (None, '') else ''

    def build_collection_highlight_qr_url(self, base_url, collection_type, identifier):
        """Build an authenticated collection-page QR URL with a highlight filter."""
        collection_url = self.get_qr_collection_url(collection_type)
        return f"{base_url}{collection_url}?highlight={quote(str(identifier))}"

    def apply_qr_highlight_filter(self, records, collection_type, highlight):
        """Filter collection records to a single highlighted record when present."""
        if not highlight:
            return records

        filtered_records = [
            record
            for record in records
            if self.get_qr_record_identifier(record, collection_type) == str(highlight).strip()
        ]
        if filtered_records:
            return filtered_records

        flash(f'Запис са идентификатором {highlight} није пронађен.', 'warning')
        return records

    def ensure_qr_collection_access(self, collection_type):
        """Return a redirect response when the current user cannot access QR for this collection."""
        module_key = self.get_qr_collection_module_key(collection_type)

        if not module_key:
            flash('QR генератор није доступан за ову збирку.', 'warning')
            return redirect(url_for('museum_databases'))

        user_email = session.get('user_email', '')
        user_role = session.get('user_role', 'user')

        if self.user_has_module_access(user_email, user_role, module_key):
            return None

        flash('Немате приступ QR генератору за ову збирку.', 'error')

        if self.user_has_module_access(user_email, user_role, 'museum_databases'):
            return redirect(url_for('museum_databases'))
        return redirect(url_for('dashboard'))

    def load_all_mineral_records_for_image_upload(self):
        """Load all mineral records for batch image matching."""
        mineral_db = self.get_mineral_database()
        if not mineral_db or not getattr(mineral_db, 'available', False):
            return []

        per_page = 5000
        records = []

        try:
            result = mineral_db.get_all_minerals(
                page=1,
                per_page=per_page,
                sort_by='inventarni_broj',
                sort_order='asc',
            ) or {}
            records.extend(result.get('minerals', []))

            total_pages = result.get('total_pages', 1) or 1
            for page in range(2, total_pages + 1):
                page_result = mineral_db.get_all_minerals(
                    page=page,
                    per_page=per_page,
                    sort_by='inventarni_broj',
                    sort_order='asc',
                ) or {}
                records.extend(page_result.get('minerals', []))
        except Exception as exc:  # pragma: no cover - depends on DB availability
            logger.error("Failed to load mineral records for batch upload: %s", exc)
            return []

        return records

    def normalize_image_upload_database(self, database):
        """Normalize legacy or UI aliases to canonical image-upload database ids."""
        if not database:
            return ''
        database = str(database).strip()
        return self.image_upload_aliases.get(database, database)

    def get_image_upload_config(self, database):
        """Return batch image upload configuration for a supported collection."""
        return self.image_upload_config.get(self.normalize_image_upload_database(database))

    def get_image_upload_module_key(self, database):
        """Get the module access key required for batch image upload."""
        config = self.get_image_upload_config(database)
        return config['module'] if config else None

    def get_image_upload_collection_url(self, database):
        """Get the collection landing page URL for a supported image-upload collection."""
        config = self.get_image_upload_config(database)
        if not config:
            user_email = session.get('user_email', '')
            user_role = session.get('user_role', 'user')
            if self.user_has_module_access(user_email, user_role, 'museum_databases'):
                return url_for('museum_databases')
            return url_for('dashboard')
        return url_for(config['route'])

    def get_image_upload_action_url(self, database):
        """Get the scoped batch image upload URL for a collection."""
        config = self.get_image_upload_config(database)
        if not config:
            return None
        return url_for(
            'batch_image_upload',
            database=self.normalize_image_upload_database(database),
        )

    def get_image_upload_display_name(self, database):
        """Get human-readable name for a batch image upload collection."""
        config = self.get_image_upload_config(database)
        return config['name'] if config else database

    def get_accessible_image_upload_databases(self, user_email, user_role):
        """List image-upload collections available to the current user."""
        databases = []

        for database_id, config in self.image_upload_config.items():
            if self.user_has_module_access(user_email, user_role, config['module']):
                databases.append(
                    {
                        'id': database_id,
                        'name': config['name'],
                        'prefix': config['prefix'],
                    }
                )

        return databases

    def normalize_image_upload_record(self, record, database):
        """Add common matching fields across heterogeneous collection records."""
        if not isinstance(record, dict):
            return record

        normalized = dict(record)
        database = self.normalize_image_upload_database(database)

        inventory_value = self._first_populated_value(
            normalized,
            [
                'inventarni_broj',
                'inventory_number',
                'catalog_number',
                'record_number',
                'registry_number',
                'id',
            ],
        )
        if inventory_value not in (None, ''):
            normalized.setdefault('inventarni_broj', str(inventory_value).strip())

        if database == 'cultural_heritage':
            heritage_value = self._first_populated_value(
                normalized,
                ['registry_number', 'inventory_number', 'id'],
            )
            if heritage_value not in (None, ''):
                normalized.setdefault('registry_number', str(heritage_value).strip())
                normalized.setdefault('heritage_id', str(heritage_value).strip())

        display_name = self._first_populated_value(
            normalized,
            [
                'naziv',
                'name',
                'item_name',
                'specimen_name',
                'scientific_name',
                'common_name_sr',
                'rock_name',
                'subcategory',
                'category',
            ],
        )
        if display_name not in (None, ''):
            normalized.setdefault('name', str(display_name).strip())

        locality = self._first_populated_value(
            normalized,
            ['lokalitet', 'locality', 'location_found', 'origin', 'location', 'habitat'],
        )
        if locality not in (None, ''):
            normalized.setdefault('locality', str(locality).strip())

        return normalized

    def get_image_upload_records(self, database):
        """Load normalized records for batch image upload matching."""
        config = self.get_image_upload_config(database)
        if not config or 'loader' not in config:
            return []

        try:
            records = config['loader']() or []
        except Exception as exc:  # pragma: no cover - depends on DB availability
            logger.error("Failed to load image upload records for %s: %s", database, exc)
            return []

        return [
            self.normalize_image_upload_record(record, database)
            for record in records
            if isinstance(record, dict)
        ]

    def ensure_image_upload_access(self, database):
        """Return a redirect response when the current user cannot use image upload for a collection."""
        module_key = self.get_image_upload_module_key(database)

        if not module_key:
            flash('Групно отпремање слика није доступно за ову збирку.', 'warning')
            user_email = session.get('user_email', '')
            user_role = session.get('user_role', 'user')
            if self.user_has_module_access(user_email, user_role, 'museum_databases'):
                return redirect(url_for('museum_databases'))
            return redirect(url_for('dashboard'))

        user_email = session.get('user_email', '')
        user_role = session.get('user_role', 'user')

        if self.user_has_module_access(user_email, user_role, module_key):
            return None

        flash('Немате приступ групном отпремању слика за ову збирку.', 'error')

        if self.user_has_module_access(user_email, user_role, 'museum_databases'):
            return redirect(url_for('museum_databases'))
        return redirect(url_for('dashboard'))
