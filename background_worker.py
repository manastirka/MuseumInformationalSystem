#!/usr/bin/env python3
"""Dedicated background worker entrypoint for recurring museum jobs."""

import logging
import signal
import time

from app import create_app, start_background_jobs


logger = logging.getLogger(__name__)
_stop_requested = False


def _handle_signal(signum, frame):
    del frame
    global _stop_requested
    logger.info("Background worker received signal %s, stopping", signum)
    _stop_requested = True


def build_worker_app():
    """Create the Flask app without starting any web-owned background jobs."""
    return create_app()


def run_worker():
    """Start recurring background jobs in a dedicated long-lived process."""
    build_worker_app()
    started = start_background_jobs()
    if started:
        logger.info("Background worker started recurring jobs")
    else:
        logger.info("Background jobs were already running in this process")

    signal.signal(signal.SIGTERM, _handle_signal)
    signal.signal(signal.SIGINT, _handle_signal)

    while not _stop_requested:
        time.sleep(5)

    logger.info("Background worker stopped")


if __name__ == '__main__':
    run_worker()
