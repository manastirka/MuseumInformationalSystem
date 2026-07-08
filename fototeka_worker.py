#!/usr/bin/env python3
"""Dedicated Фототека worker: consumes the foto_poslovi queue (derivatives,
fixity checks). Runs as its own systemd service (deploy/mis-fototeka-worker
.service), never inside gunicorn."""

import logging
import signal
import sys
import time

from dotenv import load_dotenv

load_dotenv()

import fototeka_jobs  # noqa: E402 - needs the .env loaded first


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(name)s: %(message)s',
)
logger = logging.getLogger('fototeka_worker')

IDLE_SLEEP_SECONDS = 5
RECLAIM_EVERY_SECONDS = 300

_stop_requested = False


def _handle_signal(signum, frame):
    del frame
    global _stop_requested
    logger.info("Fototeka worker received signal %s, stopping", signum)
    _stop_requested = True


def _check_pyvips():
    """Refuse to start without pyvips — a loud failure beats a silently
    idle derivative queue."""
    try:
        import pyvips
    except Exception as exc:
        logger.critical("pyvips/libvips is not available: %s", exc)
        sys.exit(1)
    logger.info(
        "pyvips OK (libvips %d.%d)", pyvips.version(0), pyvips.version(1),
    )


def run_worker():
    _check_pyvips()
    signal.signal(signal.SIGTERM, _handle_signal)
    signal.signal(signal.SIGINT, _handle_signal)
    logger.info("Fototeka worker started as %s", fototeka_jobs.worker_identity())

    last_reclaim = 0.0
    while not _stop_requested:
        now = time.monotonic()
        if now - last_reclaim >= RECLAIM_EVERY_SECONDS:
            try:
                fototeka_jobs.reclaim_stale_jobs()
            except Exception:
                logger.exception("Stale-job reclaim failed")
            last_reclaim = now

        try:
            job = fototeka_jobs.claim_next_job()
        except Exception:
            logger.exception("Claiming a job failed; backing off")
            time.sleep(IDLE_SLEEP_SECONDS)
            continue

        if job is None:
            time.sleep(IDLE_SLEEP_SECONDS)
            continue

        logger.info(
            "Processing job %s (%s) for photo %s",
            job['id'], job['tip'], job['fotografija_id'],
        )
        if fototeka_jobs.process_job(job):
            logger.info("Job %s done", job['id'])

    logger.info("Fototeka worker stopped")


if __name__ == '__main__':
    run_worker()
