"""Background-worker bootstrap helpers for the main Flask app."""

import os


BACKGROUND_WORKER_ROLE_ENV = 'MUSEUM_BACKGROUND_WORKER'


def start_background_jobs(
    *,
    background_jobs_started,
    background_jobs_lock_fd,
    background_jobs_lock_path,
    logger,
    try_acquire_process_lock,
    update_science_news_background,
    map_feature_paper_enricher,
):
    """Start recurring background jobs only in the dedicated worker process."""
    if background_jobs_started:
        return False, background_jobs_lock_fd

    if os.environ.get(BACKGROUND_WORKER_ROLE_ENV) != '1':
        logger.warning(
            "Refusing to start background jobs outside the dedicated worker "
            "(set %s=1 only in background_worker.py).",
            BACKGROUND_WORKER_ROLE_ENV,
        )
        return False, background_jobs_lock_fd

    if background_jobs_lock_fd is None:
        background_jobs_lock_fd = try_acquire_process_lock(background_jobs_lock_path)
    if background_jobs_lock_fd is None:
        logger.warning("Background jobs already owned by another process; skipping startup")
        return False, None

    app_root = os.path.dirname(os.path.abspath(__file__))
    update_science_news_background(app_root)
    map_feature_paper_enricher.start_enrichment_background()
    return True, background_jobs_lock_fd


def create_app(*, app, start_background_services: bool, logger):
    """Return the configured Flask app and warn when legacy startup flags are used."""
    if start_background_services:
        logger.warning(
            "Background services are no longer started from the web app. "
            "Run background_worker.py as a separate process instead."
        )
    return app
