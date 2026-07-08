#!/usr/bin/env python3
"""Monthly Фототека fixity enqueue (systemd timer oneshot).

Queues a fixity job for the RAW originals least recently verified; the
fototeka worker then re-hashes each and flags any mismatch. Safe to run more
often than monthly — enqueue_fixity_batch skips photos that already have a
pending/running fixity job."""

import logging

from dotenv import load_dotenv

load_dotenv()

import fototeka_jobs  # noqa: E402 - needs the .env loaded first


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(name)s: %(message)s',
)
logger = logging.getLogger('fototeka_fixity')


def main():
    queued = fototeka_jobs.enqueue_fixity_batch()
    logger.info('Enqueued %d fixity job(s)', queued)


if __name__ == '__main__':
    main()
