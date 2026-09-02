"""Collection-access bootstrap helpers for the main Flask app."""

import collection_access_support


def build_collection_access_bindings(
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
    """Create the collection-access helper object and its exported bindings."""
    support = collection_access_support.CollectionAccessSupport(
        user_has_module_access=user_has_module_access,
        get_mineral_database=get_mineral_database,
        get_meteorite_collection_database=get_meteorite_collection_database,
        get_cultural_heritage_database=get_cultural_heritage_database,
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
    return {
        '_collection_access_support': support,
        'QR_COLLECTION_ALIASES': support.qr_collection_aliases,
        'QR_FIELD_LABELS': support.qr_field_labels,
        'QR_COLLECTION_CONFIG': support.qr_collection_config,
        'IMAGE_UPLOAD_ALIASES': support.image_upload_aliases,
        'IMAGE_UPLOAD_CONFIG': support.image_upload_config,
        'normalize_qr_collection_type': support.normalize_qr_collection_type,
        'get_qr_collection_config': support.get_qr_collection_config,
        'get_qr_collection_name': support.get_qr_collection_name,
        'get_qr_collection_module_key': support.get_qr_collection_module_key,
        'get_qr_collection_url': support.get_qr_collection_url,
        'get_qr_collection_records': support.get_qr_collection_records,
        'get_qr_record_identifier': support.get_qr_record_identifier,
        'get_qr_record_catalog_label': support.get_qr_record_catalog_label,
        'get_qr_record_name': support.get_qr_record_name,
        'get_qr_record_summary': support.get_qr_record_summary,
        'get_qr_record_location': support.get_qr_record_location,
        'apply_qr_highlight_filter': support.apply_qr_highlight_filter,
        'normalize_image_upload_database': support.normalize_image_upload_database,
        'get_image_upload_config': support.get_image_upload_config,
        'get_image_upload_module_key': support.get_image_upload_module_key,
    }


def bind_collection_helpers_to_app(
    app,
    *,
    get_image_upload_module_key,
    user_has_module_access,
    normalize_qr_collection_type,
    get_qr_collection_name,
    get_qr_collection_url,
    get_qr_collection_records,
    get_qr_record_identifier,
    get_qr_record_catalog_label,
    get_qr_record_name,
    get_qr_record_summary,
    get_qr_record_location,
    get_meteorite_collection_database,
    get_mineral_database,
    botany_collection_database,
    paleozoology_collection_database,
    get_employee_directory,
):
    """Expose collection helpers on the Flask app for downstream modules."""
    app.get_image_upload_module_key = get_image_upload_module_key
    app.user_has_module_access = user_has_module_access
    app.normalize_qr_collection_type = normalize_qr_collection_type
    app.get_qr_collection_name = get_qr_collection_name
    app.get_qr_collection_url = get_qr_collection_url
    app.get_qr_collection_records = get_qr_collection_records
    app.get_qr_record_identifier = get_qr_record_identifier
    app.get_qr_record_catalog_label = get_qr_record_catalog_label
    app.get_qr_record_name = get_qr_record_name
    app.get_qr_record_summary = get_qr_record_summary
    app.get_qr_record_location = get_qr_record_location
    app.get_meteorite_collection_database = get_meteorite_collection_database
    app.get_mineral_database = get_mineral_database
    app.botany_collection_database = botany_collection_database
    app.paleozoology_collection_database = paleozoology_collection_database
    app.get_employee_directory = get_employee_directory
