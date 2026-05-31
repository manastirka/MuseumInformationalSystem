"""Access-control and auth bootstrap helpers for the main Flask app."""


SPECIALTY_KEYWORDS = {
    'mineral_database': ('минералог', 'минералошк', 'кристалограф'),
    'botany_collection': ('ботаничар', 'ботаник', 'хербаријум', 'флора'),
    'ichthyology_collection': ('ихтиолог',),
    'entomology_collection': ('ентомолог', 'инсект'),
    'mycology_collection': ('миколог', 'гљив'),
    'herpetology_collection': ('херпетолог',),
    'ornithology_collection': ('орнитолог', 'птиц'),
    'paleozoology_collection': ('палеозоолог',),
    'sanja_paleogene_neogene_mammals': ('палеозоолог', 'палеонтолог', 'сисар'),
    'bilja_kenozojske_invertebrate': ('палеозоолог', 'палеонтолог', 'инвертебрат'),
    'bilja_hydrobioidea_radoman': ('биолог', 'малаколог', 'гастропод', 'мекушц'),
    'bilja_suvozemni_puzevi_pavlovic': ('биолог', 'малаколог', 'гастропод', 'мекушц'),
    'bilja_opsta_zbirka_mollusca': ('биолог', 'малаколог', 'мекушц'),
    'bilja_skoljke_tadic': ('биолог', 'малаколог', 'мекушц'),
    'bilja_recentni_morski_mekusci': ('биолог', 'малаколог', 'мекушц'),
    'paleobotany_collection': ('палеоботан',),
    'petrology_collection': ('петролог', 'петролошк'),
    'meteorite_collection': ('метеорит',),
    'bird_ringing_database': ('орнитолог', 'прстеновањ', 'птиц'),
    'biodiversity_map': (
        'ботаничар', 'ботаник', 'ихтиолог', 'ентомолог', 'миколог',
        'херпетолог', 'орнитолог', 'биолог',
    ),
    'maps_karte': (
        'геолог', 'минералог', 'петролог', 'палеозоолог',
        'палеоботан', 'геолошк',
    ),
}

SPECIALTY_COLLECTION_MODULES = (
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
    'paleobotany_collection',
    'petrology_collection',
    'meteorite_collection',
)


def _normalize_text(value):
    return str(value or '').strip().lower()


def _resolve_employee_profile(user_email, employee_directory):
    normalized_email = _normalize_text(user_email)
    if not normalized_email:
        return None

    for entry in employee_directory or []:
        if _normalize_text(entry.get('email')) == normalized_email:
            return entry
    return None


def _profile_matches_specialty(profile, module_key):
    keywords = SPECIALTY_KEYWORDS.get(module_key, ())
    if not keywords or not profile:
        return False

    searchable_text = ' '.join(
        _normalize_text(profile.get(field))
        for field in ('department', 'position', 'description')
    )
    return any(keyword in searchable_text for keyword in keywords)


def _has_direct_module_access(module, user_email):
    if not module:
        return False

    normalized_email = _normalize_text(user_email)
    restricted_users = [_normalize_text(entry) for entry in module.get('restricted_users', [])]
    if module.get('default_access', False) and normalized_email not in restricted_users:
        return True

    authorized_users = [_normalize_text(entry) for entry in module.get('authorized_users', [])]
    return normalized_email in authorized_users


def user_has_module_access(
    user_email,
    user_role,
    module_key,
    *,
    load_module_access,
    module_access,
    get_employee_directory=None,
    resolved_module_access=None,
    resolved_employee_directory=None,
):
    """Check whether a user can access the requested dashboard module."""
    module_access = resolved_module_access if resolved_module_access is not None else (load_module_access() or module_access)

    if user_role == 'admin':
        return True

    module = module_access.get(module_key)
    if not module:
        if module_key == 'museum_databases':
            employee_directory = (
                resolved_employee_directory
                if resolved_employee_directory is not None
                else (get_employee_directory() if get_employee_directory else [])
            )
            profile = _resolve_employee_profile(user_email, employee_directory)
            return any(
                _profile_matches_specialty(profile, specialty_module)
                for specialty_module in SPECIALTY_COLLECTION_MODULES + ('mineral_database',)
            )
        return False

    if _has_direct_module_access(module, user_email):
        return True

    employee_directory = (
        resolved_employee_directory
        if resolved_employee_directory is not None
        else (get_employee_directory() if get_employee_directory else [])
    )
    profile = _resolve_employee_profile(user_email, employee_directory)

    if module_key == 'museum_databases':
        return any(
            user_has_module_access(
                user_email,
                user_role,
                specialty_module,
                load_module_access=load_module_access,
                module_access=module_access,
                get_employee_directory=get_employee_directory,
                resolved_module_access=module_access,
                resolved_employee_directory=employee_directory,
            )
            for specialty_module in SPECIALTY_COLLECTION_MODULES + (
                'mineral_database',
                'library_database',
                'bird_ringing_database',
                'biodiversity_map',
                'maps_karte',
                'nhm_data_portal',
            )
        )

    if module_key == 'curator_collections':
        return any(
            user_has_module_access(
                user_email,
                user_role,
                specialty_module,
                load_module_access=load_module_access,
                module_access=module_access,
                get_employee_directory=get_employee_directory,
                resolved_module_access=module_access,
                resolved_employee_directory=employee_directory,
            )
            for specialty_module in SPECIALTY_COLLECTION_MODULES
        )

    return _profile_matches_specialty(profile, module_key)


def ensure_login_tracker_initialized(
    *,
    initialized,
    is_initialized,
    login_tracker,
    flask_app,
    initialize_shared_state,
    init_login_tracker,
):
    """Initialize the shared login tracker lazily when auth routes need it."""
    if initialized:
        return login_tracker, True

    tracker = initialize_shared_state(flask_app)
    if is_initialized():
        return tracker, True

    init_login_tracker(None)
    return login_tracker, True


def log_fallback_auth_warning_once(*, already_logged, app_config, logger):
    """Emit the fallback-auth status message only once per worker process."""
    if already_logged:
        return True

    if not app_config.get('ENABLE_FALLBACK_AUTH', False):
        logger.info("Fallback authentication is disabled (production mode)")
    else:
        logger.warning("⚠️ USING FALLBACK AUTHENTICATION - NOT SECURE FOR PRODUCTION")
        logger.warning("    Set ENABLE_FALLBACK_AUTH=False in .env for production")
    return True
