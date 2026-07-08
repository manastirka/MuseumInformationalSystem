#!/usr/bin/env python3
"""One-time migration: legacy `images` table -> Фототека `fotografije`.

Copies every original from the legacy image store (ImagesDatabase) into the
Фототека RAW archive by origin, inserts a first-class `fotografije` row (with a
collection link when the entity resolves to an inventory number), and enqueues
the derivative job. It is:

  * copy-only  — never moves or deletes the legacy files or the images table;
  * idempotent — a photo already present (matched by real sha256) is skipped,
    so the script can be re-run safely after an interruption;
  * dry-run by default — pass --commit to actually write.

Mineral entities (database 'mineral'/'minerals') resolve entity_id -> the
mineral's inventory_number and link as a collection item; anything that does
not resolve is migrated unlinked into the reception queue so nothing is lost.

Usage:
    python migrate_images_to_fototeka.py            # dry run
    python migrate_images_to_fototeka.py --commit
    python migrate_images_to_fototeka.py --commit --limit 10
"""

import argparse
import json
import os
import shutil
import sys
from pathlib import Path

from dotenv import load_dotenv

REPO_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(REPO_ROOT))
load_dotenv(REPO_ROOT / '.env')

import fototeka_jobs  # noqa: E402
from postgres_service import get_postgres_connection  # noqa: E402


MIGRATION_AUTHOR = 'migracija-fototeka@mis'
MINERAL_DATABASES = {'mineral', 'minerals'}


def _scalar(row, key):
    if row is None:
        return None
    return row.get(key) if isinstance(row, dict) else row[0]


def _row_to_dict(cursor, row):
    if row is None:
        return None
    if isinstance(row, dict):
        return row
    return dict(zip([c.name for c in cursor.description], row))


def _resolve_original(file_path: str):
    """Locate the legacy original on disk. `file_path` is stored relative to
    the repo root (e.g. 'ImagesDatabase/originals/x.jpg'); also try under
    IMAGE_STORAGE_PATH in case the store was relocated."""
    candidates = [REPO_ROOT / file_path, Path(file_path)]
    storage = Path(os.environ.get('IMAGE_STORAGE_PATH', './ImagesDatabase'))
    stripped = file_path.split('ImagesDatabase/', 1)[-1]
    candidates.append(storage / stripped)
    for candidate in candidates:
        if candidate.is_file():
            return candidate
    return None


def _resolve_mineral_link(cur, entity_id):
    """entity_id (mineral row id, as text) -> (inventory_number, item_name)."""
    try:
        mineral_id = int(str(entity_id).strip())
    except (TypeError, ValueError):
        return None
    cur.execute(
        'SELECT inventory_number, item_name FROM minerals WHERE id = %s',
        (mineral_id,),
    )
    row = _row_to_dict(cur, cur.fetchone())
    if not row or not row.get('inventory_number'):
        return None
    return row['inventory_number'], row.get('item_name')


def _plan_row(cur, image):
    """Decide the target link and RAW layout for one images row. Returns a
    plan dict, or an error string on a missing file."""
    original = _resolve_original(image['file_path'])
    if original is None:
        return f"missing file: {image['file_path']}"

    veza = None
    opis = None
    if image['database_name'] in MINERAL_DATABASES:
        resolved = _resolve_mineral_link(cur, image['entity_id'])
        if resolved:
            inv, item_name = resolved
            veza = {'tip': 'predmet', 'database_name': 'mineral',
                    'inventarni_broj': inv}
            opis = item_name

    sha256 = fototeka_jobs.sha256_of_file(original)
    original_ime = image.get('original_filename') or original.name
    created = image.get('created_at')
    raw_rel = fototeka_jobs.raw_intake_relative_path(
        veza_predmet=((veza['database_name'], veza['inventarni_broj'])
                      if veza else None),
        original_ime=original_ime,
        sha256=sha256,
        datum=created.date() if created is not None else None,
    )
    return {
        'original': original,
        'sha256': sha256,
        'original_ime': original_ime,
        'ext': original.suffix.lower(),
        'veza': veza,
        'opis': opis,
        'raw_rel': raw_rel,
        'u_prijemnom_redu': veza is None,
        'width': image.get('width'),
        'height': image.get('height'),
        'file_size': image.get('file_size'),
    }


def migrate(commit, limit):
    arhiva_root = fototeka_jobs.get_arhiva_path()
    stats = {'total': 0, 'planned': 0, 'migrated': 0, 'dedup': 0,
             'unlinked': 0, 'missing': 0, 'errors': 0}

    with get_postgres_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT image_id, database_name, entity_type, entity_id,
                       file_path, original_filename, file_size, width, height,
                       created_at
                FROM images
                ORDER BY image_id
                """
            )
            images = [_row_to_dict(cur, r) for r in cur.fetchall()]

    if limit:
        images = images[:limit]
    stats['total'] = len(images)

    for image in images:
        try:
            with get_postgres_connection() as conn:
                with conn.cursor() as cur:
                    plan = _plan_row(cur, image)
                    if isinstance(plan, str):
                        stats['missing'] += 1
                        print(f"  SKIP  {image['image_id']}: {plan}")
                        continue

                    cur.execute(
                        'SELECT id FROM fotografije WHERE sha256 = %s',
                        (plan['sha256'],),
                    )
                    if cur.fetchone():
                        stats['dedup'] += 1
                        print(f"  DEDUP {image['image_id']}: already migrated")
                        continue

                    target = 'предмет' if plan['veza'] else 'пријемни ред'
                    print(f"  {'MIGR ' if commit else 'PLAN '}"
                          f"{image['image_id']} -> {target} ({plan['raw_rel']})")
                    stats['planned'] += 1
                    if plan['veza'] is None:
                        stats['unlinked'] += 1

                    if not commit:
                        continue

                    raw_full = arhiva_root / plan['raw_rel']
                    raw_full.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(plan['original'], raw_full)

                    file_size = plan['file_size'] or raw_full.stat().st_size
                    cur.execute(
                        """
                        INSERT INTO fotografije
                            (sha256, raw_putanja, original_ime, ekstenzija,
                             velicina_bajtova, width, height, autor_email,
                             datum_snimanja, exif, opis, poreklo, u_prijemnom_redu)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, NULL, %s, %s,
                                'import', %s)
                        RETURNING id
                        """,
                        (plan['sha256'], plan['raw_rel'], plan['original_ime'],
                         plan['ext'], file_size, plan['width'], plan['height'],
                         MIGRATION_AUTHOR, json.dumps({}), plan['opis'],
                         plan['u_prijemnom_redu']),
                    )
                    fotografija_id = _scalar(cur.fetchone(), 'id')
                    if plan['veza']:
                        cur.execute(
                            """
                            INSERT INTO foto_veza_predmet
                                (fotografija_id, database_name, inventarni_broj)
                            VALUES (%s, %s, %s)
                            ON CONFLICT (fotografija_id, database_name, inventarni_broj)
                            DO NOTHING
                            """,
                            (fotografija_id, plan['veza']['database_name'],
                             plan['veza']['inventarni_broj']),
                        )
                    fototeka_jobs.enqueue_job(cur, fotografija_id, 'derivati')
                    stats['migrated'] += 1
        except Exception as exc:  # noqa: BLE001 - report and continue
            stats['errors'] += 1
            print(f"  ERROR {image.get('image_id')}: {exc}")

    print()
    print('=== Резултат ===')
    print(f"  укупно images:      {stats['total']}")
    done = stats['migrated'] if commit else stats['planned']
    print(f"  {'мигрирано' if commit else 'за миграцију'}:     {done}")
    print(f"  од тога без везе:   {stats['unlinked']} (пријемни ред)")
    print(f"  већ мигрирано:      {stats['dedup']}")
    print(f"  недостаје фајл:     {stats['missing']}")
    print(f"  грешке:             {stats['errors']}")
    if not commit:
        print('\n(dry-run — ништа није уписано; покрени са --commit за стварну миграцију)')
    return stats


def main():
    parser = argparse.ArgumentParser(
        description='Migrate the legacy images table into Фототека.')
    parser.add_argument('--commit', action='store_true',
                        help='actually copy files and write rows (default: dry run)')
    parser.add_argument('--limit', type=int, default=None,
                        help='process at most N images')
    args = parser.parse_args()
    migrate(commit=args.commit, limit=args.limit)


if __name__ == '__main__':
    main()
