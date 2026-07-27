"""Helpers for blueprint registration and backwards-compat endpoint wiring."""

from typing import Iterable, Sequence


BLUEPRINT_ALIAS_ENDPOINTS = {
    'qr': (
        'admin_qr_generator',
        'admin_qr_field_selection',
        'admin_qr_labels_with_fields',
        'admin_qr_mineral_boxes',
        'admin_generate_box_qr_codes',
        'admin_qr_select_specimens',
        'admin_qr_labels_selected',
        'admin_qr_label_format',
        'admin_qr_labels_with_format',
        'admin_qr_labels',
    ),
    'content': (
        'system_reports',
        'exhibits_database',
        'exhibitions_database',
        'museum_news',
        'api_save_news',
        'api_website_news',
        'api_weather_details',
        'library_database',
        'nhm_data_portal',
        'api_nhm_search',
        'api_nhm_dataset',
        'api_nhm_resource',
        'api_nhm_datastore',
        'api_nhm_statistics',
        'api_nhm_local_search',
        'api_nhm_local_dataset',
        'api_nhm_local_statistics',
        'api_nhm_local_tags',
        'api_nhm_local_formats',
        'api_nhm_local_authors',
        'api_nhm_download_datasets',
        'api_nhm_data_search_local',
        'api_nhm_data_search_nhm',
        'cultural_heritage_database',
        'add_book',
        'add_heritage_item',
        'add_visitor',
        'add_research',
        'export_research_to_pdf',
        'visitors_database',
        'export_visitors_to_pdf',
        'research_database',
        'bird_ringing_database_view',
        'bird_ringing_record_detail',
        'add_bird_ringing',
        'museum_terminology',
        'exhibition_planner',
        'api_get_exhibitions',
        'api_create_exhibition',
        'api_update_exhibition',
        'api_delete_exhibition',
        'api_update_exhibition_checklist',
    ),
    'travel_finance': (
        'finansijski_zahtevi',
        'zahtev_slobodan_dan',
        'zahtev_godisnji_odmor',
        'zahtev_razno',
        'finansijski_plan',
        'zahtev_nabavka',
        'terenska_aktivnost',
        'zahtev_sluzbeni_put',
        'api_field_trip_create',
        'api_route_calculate',
        'api_nabavka_save',
        'api_nabavka_list',
        'api_nabavka_export_word',
        'api_nabavka_export_word_by_id',
        'api_finansijski_plan_save',
        'api_finansijski_plan_list',
        'api_finansijski_plan_export_word',
        'api_finansijski_plan_export_word_by_id',
    ),
    'timesheet': (
        'timesheet_app',
        'admin_timesheet_main',
        'admin_timesheet_reports',
        'admin_timesheet_archive',
        'admin_timesheet_report_detail',
        'admin_timesheet_employees',
        'admin_timesheet_users',
        'admin_timesheet_unlock',
        'api_admin_timesheet_unlock',
        'admin_timesheet_analytics',
        'api_admin_employee_analytics',
        'api_admin_get_timesheet_report',
        'api_admin_approve_timesheet_report',
        'api_admin_batch_approve_timesheet_reports',
        'api_admin_export_timesheet_report',
        'api_admin_delete_timesheet_report',
        'api_get_notifications',
        'api_mark_notifications_read',
        'api_clear_notifications',
        'timesheet_entry',
        'timesheet_view',
        'api_load_timesheet',
        'api_save_timesheet',
        'api_timesheet_submit',
        'api_timesheet_approve',
        'api_timesheet_reject',
        'api_timesheet_force_edit',
        'admin_timesheet_review',
    ),
    'admin': (
        'admin_panel',
        'admin_system_hub',
        'admin_system_settings',
        'admin_audit_log',
        'api_save_general_settings',
        'api_save_security_settings',
        'api_database_backup',
        'api_table_stats',
        'api_vacuum_database',
        'api_get_logs',
        'api_download_logs',
        'api_clear_cache',
        'admin_statistics',
        'manage_user_access',
        'grant_module_access',
        'revoke_module_access',
        'admin_password_manager',
        'admin_mail_configuration',
        'api_password_manager_users',
        'api_admin_mail_settings_state',
        'api_admin_mail_settings_save',
        'api_admin_mail_test_connection',
        'api_password_manager_reset',
        'api_password_manager_force_change',
        'api_password_manager_toggle_status',
        'api_password_manager_generate',
        'employees_database',
        'employee_profiles_database',
        'add_user',
        'customize_dashboard',
    ),
    'collections': (
        'botany_collection',
        'ichthyology_collection',
        'entomology_collection',
        'mycology_collection',
        'herpetology_collection',
        'ornithology_collection',
        'paleozoology_collection',
        'sanja_paleogene_neogene_mammals',
        'bilja_kenozojske_invertebrate',
        'bilja_hydrobioidea_radoman',
        'bilja_suvozemni_puzevi_pavlovic',
        'bilja_opsta_zbirka_mollusca',
        'bilja_skoljke_tadic',
        'bilja_recentni_morski_mekusci',
        'edit_bilja_item',
        'paleobotany_collection',
        'petrology_collection',
        'meteorite_collection',
        'admin_mineral_collection',
        'admin_mineral_detail',
        'admin_rruff_minerals',
        'admin_rruff_detail',
        'add_mineral',
        'edit_mineral',
        'delete_mineral',
        'inventory_book',
        'inventory_reconciliation',
        'conservation_biology',
        'export_collection_to_pdf',
        'museum_databases',
        'add_collection_item',
    ),
    'media': (
        'qr_view_mineral_box',
        'serve_static',
        'get_specimen_image',
        'get_specimen_image_full',
        'get_specimen_thumbnail',
        'get_image_by_id',
        'qr_view_specimen',
    ),
    'mineral_science': (
        'api_get_rruff_data',
        'api_cod_search',
        'api_cod_get_cif',
        'api_crystal_get_cif_by_url',
        'api_crystal_get_local_cif',
        'api_cod_get_structure',
        'api_get_geochemical_data',
        'api_get_local_rruff_data',
        'api_get_local_rruff_dif',
        'api_get_local_rruff_cif',
        'api_get_local_rruff_spectrum',
        'api_get_local_rruff_powder_xy',
        'api_serve_local_rruff_image',
        'api_get_local_rruff_microprobe',
    ),
    'core': (
        'set_language',
        'index',
        'login',
        'logout',
        'change_password',
        'dashboard',
        'dashboard_classic',
        'mineral_database_app',
    ),
}

EXPLICIT_ENDPOINT_ALIASES = {
    'rruff_minerals': 'collections.admin_rruff_minerals',
}

BLUEPRINT_REGISTRATION_ORDER = (
    'projects',
    'qr',
    'mail',
    'chat',
    'vehicles',
    'science',
    'maps',
    'content',
    'travel_finance',
    'timesheet',
    'admin',
    'collections',
    'media',
    'mineral_science',
    'core',
)

CSRF_EXEMPT_ENDPOINTS = (
    'chat.api_chat_leave',
    'core.set_language',
    'set_language',
)

LIMITED_ENDPOINTS = (
    ('admin.api_password_manager_reset', "5 per minute"),
    ('api_password_manager_reset', "5 per minute"),
    ('core.login', "5 per minute"),
    ('login', "5 per minute"),
    ('media.qr_view_mineral_box', "30 per minute"),
    ('qr_view_mineral_box', "30 per minute"),
    ('media.get_specimen_image', "600 per minute"),
    ('get_specimen_image', "600 per minute"),
    ('media.get_specimen_image_full', "600 per minute"),
    ('get_specimen_image_full', "600 per minute"),
    ('media.get_specimen_thumbnail', "600 per minute"),
    ('get_specimen_thumbnail', "600 per minute"),
    ('media.qr_view_specimen', "30 per minute"),
    ('qr_view_specimen', "30 per minute"),
)

LIMIT_EXEMPT_ENDPOINTS = (
    'media.get_image_by_id',
    'get_image_by_id',
    'maps.api_map_tile_index',
    'api_map_tile_index',
    'maps.api_map_tile',
    'api_map_tile',
    'maps.api_geological_sheet_image',
    'api_geological_sheet_image',
    'maps.api_map_elevation',
    'api_map_elevation',
)


def register_blueprint_endpoint_aliases(flask_app, blueprint_name: str, endpoint_names: Sequence[str]) -> None:
    """Expose backward-compatible endpoint names for newly extracted blueprints."""
    for endpoint_name in endpoint_names:
        old_endpoint = endpoint_name
        new_endpoint = f'{blueprint_name}.{endpoint_name}'
        if old_endpoint in flask_app.view_functions:
            continue
        view_func = flask_app.view_functions.get(new_endpoint)
        rules = list(flask_app.url_map._rules_by_endpoint.get(new_endpoint, ()))
        if view_func is None or not rules:
            continue
        for rule in rules:
            methods = sorted(m for m in rule.methods if m not in {'HEAD', 'OPTIONS'})
            options = {}
            if rule.defaults:
                options['defaults'] = rule.defaults
            if getattr(rule, 'subdomain', None):
                options['subdomain'] = rule.subdomain
            if hasattr(rule, 'strict_slashes'):
                options['strict_slashes'] = rule.strict_slashes
            flask_app.add_url_rule(
                rule.rule,
                endpoint=old_endpoint,
                view_func=view_func,
                methods=methods,
                **options,
            )


def register_standard_blueprints(flask_app, blueprint_map: dict[str, object]) -> None:
    """Register the extracted blueprints in the canonical order."""
    for blueprint_name in BLUEPRINT_REGISTRATION_ORDER:
        flask_app.register_blueprint(blueprint_map[blueprint_name])


def register_explicit_endpoint_aliases(flask_app) -> None:
    """Register legacy endpoint aliases that do not match the new blueprint endpoint name."""
    for old_endpoint, new_endpoint in EXPLICIT_ENDPOINT_ALIASES.items():
        if old_endpoint in flask_app.view_functions:
            continue
        view_func = flask_app.view_functions.get(new_endpoint)
        rules = list(flask_app.url_map._rules_by_endpoint.get(new_endpoint, ()))
        if view_func is None or not rules:
            continue
        for rule in rules:
            methods = sorted(m for m in rule.methods if m not in {'HEAD', 'OPTIONS'})
            options = {}
            if rule.defaults:
                options['defaults'] = rule.defaults
            if getattr(rule, 'subdomain', None):
                options['subdomain'] = rule.subdomain
            if hasattr(rule, 'strict_slashes'):
                options['strict_slashes'] = rule.strict_slashes
            flask_app.add_url_rule(
                rule.rule,
                endpoint=old_endpoint,
                view_func=view_func,
                methods=methods,
                **options,
            )


def apply_blueprint_aliases(flask_app) -> None:
    """Apply all legacy endpoint aliases after blueprint registration."""
    for blueprint_name, endpoint_names in BLUEPRINT_ALIAS_ENDPOINTS.items():
        register_blueprint_endpoint_aliases(flask_app, blueprint_name, endpoint_names)
    register_explicit_endpoint_aliases(flask_app)


def apply_csrf_exemptions(flask_app, csrf) -> None:
    """Apply CSRF exemptions to specific registered endpoints."""
    for endpoint_name in CSRF_EXEMPT_ENDPOINTS:
        view = flask_app.view_functions.get(endpoint_name)
        if view is not None:
            csrf.exempt(view)


def apply_endpoint_rate_limits(flask_app, limiter) -> None:
    """Apply route-specific rate limits and exemptions after registration."""
    for endpoint_name, limit in LIMITED_ENDPOINTS:
        view = flask_app.view_functions.get(endpoint_name)
        if view is not None:
            limiter.limit(limit)(view)

    for endpoint_name in LIMIT_EXEMPT_ENDPOINTS:
        view = flask_app.view_functions.get(endpoint_name)
        if view is not None:
            limiter.exempt(view)


def bind_legacy_view_symbols(flask_app, symbol_names: Iterable[str]) -> dict[str, object]:
    """Return module-level symbol aliases for view functions that external code still imports."""
    return {
        symbol_name: flask_app.view_functions.get(f'media.{symbol_name}')
        for symbol_name in symbol_names
    }
