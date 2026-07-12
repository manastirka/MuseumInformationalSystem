#!/usr/bin/env python3
"""Batch import of photos from the shared intake folder (Samba).

Dry run is the DEFAULT — nothing is written until --izvrsi is passed:

    python fototeka_import.py                 # dry-run preview, prints summary
    python fototeka_import.py --izvrsi        # real import (izvor=cli)
    python fototeka_import.py --izvrsi --izvor timer   # systemd timer run

The engine (fototeka_views.run_batch_import) walks every per-user folder
under FOTOTEKA_IMPORT_PATH, classifies files by the naming convention,
dedups by sha256, moves originals to obradjeno//duplikati//neuspesno/ and
logs the run to fototeka_uvoz_run. The fototeka worker builds derivatives
asynchronously."""

import argparse
import logging
import sys

from dotenv import load_dotenv

load_dotenv()

import fototeka_views  # noqa: E402 - needs the .env loaded first


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(name)s: %(message)s',
)
logger = logging.getLogger('fototeka_import')


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--izvrsi', action='store_true',
                        help='stvarni uvoz (bez ovoga: dry-run, nula upisa)')
    parser.add_argument('--izvor', choices=('cli', 'timer'), default='cli',
                        help='izvor pokretanja za log (default: cli)')
    parser.add_argument('--zbirka', default='mineral',
                        help='podrazumevana zbirka za inventarne brojeve')
    args = parser.parse_args(argv)

    rezime = fototeka_views.run_batch_import(
        dry_run=not args.izvrsi,
        default_zbirka=args.zbirka,
        izvor=args.izvor,
    )

    rezim = 'DRY-RUN (ništa nije upisano)' if not args.izvrsi else 'UVOZ'
    logger.info(
        '%s: ukupno=%d uvezeno=%d (prijemni_red=%d) duplikata=%d neuspesno=%d run_id=%s',
        rezim, rezime['ukupno'], rezime['uvezeno'], rezime['u_prijemni_red'],
        rezime['duplikata'], rezime['neuspesno'], rezime['run_id'],
    )
    for stavka in rezime['stavke']:
        if stavka['ishod'] in ('neuspesno', 'duplikat'):
            logger.warning('%s/%s: %s — %s', stavka['folder'], stavka['datoteka'],
                           stavka['ishod'], stavka['poruka'])
    return 0


if __name__ == '__main__':
    sys.exit(main())
