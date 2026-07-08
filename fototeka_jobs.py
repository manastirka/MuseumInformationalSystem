"""Фототека job queue: enqueue, claim and process derivative/fixity jobs.

The queue lives in the foto_poslovi table and is consumed by the dedicated
worker process (fototeka_worker.py) — never by gunicorn. The web process only
enqueues. Derivatives are written under FOTOTEKA_MEDIA_PATH at paths that are
a pure function of the photo's sha256, so the database never stores them:
    jpg/<sha[:2]>/<sha>.jpg    (~2500px longest side)
    thumb/<sha[:2]>/<sha>.jpg  (~300px longest side)
RAW originals under FOTOTEKA_ARHIVA_PATH are read-only for every code path
here; a failed job never touches them.
"""

import hashlib
import logging
import os
import socket
from datetime import date
from pathlib import Path

from postgres_service import get_postgres_connection


logger = logging.getLogger(__name__)

DERIVATIVE_SIZES = {'jpg': 2500, 'thumb': 300}
JPEG_QUALITY = 85
MAX_ATTEMPTS = 5
BACKOFF_MINUTES = [1, 5, 30, 60]
STALE_LOCK_MINUTES = 15


def get_arhiva_path() -> Path:
    return Path(os.environ.get('FOTOTEKA_ARHIVA_PATH', './data/arhiva'))


def get_media_path() -> Path:
    return Path(os.environ.get('FOTOTEKA_MEDIA_PATH', './data/fototeka_media'))


def derivative_relative_path(sha256: str, kind: str) -> str:
    return f"{kind}/{sha256[:2]}/{sha256}.jpg"


def worker_identity() -> str:
    return f"{socket.gethostname()}:{os.getpid()}"


def _row_to_dict(cursor, row):
    if row is None:
        return None
    if isinstance(row, dict):
        return row
    columns = [column.name for column in cursor.description]
    return dict(zip(columns, row))


def sha256_of_file(file_path: Path) -> str:
    digest = hashlib.sha256()
    with open(file_path, 'rb') as handle:
        for block in iter(lambda: handle.read(65536), b''):
            digest.update(block)
    return digest.hexdigest()


def enqueue_job(cursor, fotografija_id: int, tip: str) -> None:
    """Insert a pending job inside the caller's transaction."""
    cursor.execute(
        """
        INSERT INTO foto_poslovi (fotografija_id, tip)
        VALUES (%s, %s)
        """,
        (fotografija_id, tip),
    )


def reclaim_stale_jobs() -> int:
    """Return jobs stuck in 'radi' (worker died mid-job) to the queue."""
    with get_postgres_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                UPDATE foto_poslovi
                SET status = 'ceka', zakljucan_at = NULL, zakljucao = NULL,
                    updated_at = now()
                WHERE status = 'radi'
                  AND zakljucan_at < now() - make_interval(mins => %s)
                RETURNING id
                """,
                (STALE_LOCK_MINUTES,),
            )
            reclaimed = cur.fetchall()
    if reclaimed:
        logger.warning("Reclaimed %d stale fototeka job(s)", len(reclaimed))
    return len(reclaimed)


def claim_next_job():
    """Atomically claim one due job (FOR UPDATE SKIP LOCKED) and return it
    joined with the photo columns the processors need, or None when idle."""
    with get_postgres_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT id FROM foto_poslovi
                WHERE status = 'ceka'
                  AND (sledeci_pokusaj_at IS NULL OR sledeci_pokusaj_at <= now())
                ORDER BY id
                LIMIT 1
                FOR UPDATE SKIP LOCKED
                """,
            )
            row = cur.fetchone()
            if not row:
                return None
            job_id = row['id'] if isinstance(row, dict) else row[0]
            cur.execute(
                """
                UPDATE foto_poslovi
                SET status = 'radi', zakljucan_at = now(), zakljucao = %s,
                    updated_at = now()
                WHERE id = %s
                """,
                (worker_identity(), job_id),
            )
            cur.execute(
                """
                SELECT p.id, p.fotografija_id, p.tip, p.pokusaji,
                       f.sha256, f.raw_putanja
                FROM foto_poslovi p
                JOIN fotografije f ON f.id = p.fotografija_id
                WHERE p.id = %s
                """,
                (job_id,),
            )
            job = _row_to_dict(cur, cur.fetchone())
            if job and job['tip'] == 'derivati':
                cur.execute(
                    """
                    UPDATE fotografije SET status = 'obrada', updated_at = now()
                    WHERE id = %s
                    """,
                    (job['fotografija_id'],),
                )
            return job


def make_derivatives(raw_full_path: Path, sha256: str) -> None:
    """Generate both derivatives with pyvips; write via temp + os.replace so a
    crash never leaves a half-written file at the final path."""
    import pyvips

    media_root = get_media_path()
    for kind, size in DERIVATIVE_SIZES.items():
        final_path = media_root / derivative_relative_path(sha256, kind)
        final_path.parent.mkdir(parents=True, exist_ok=True)
        temp_path = final_path.with_name(f".tmp_{final_path.name}")
        image = pyvips.Image.thumbnail(
            str(raw_full_path), size, height=size, size='down',
        )
        image.write_to_file(str(temp_path), Q=JPEG_QUALITY)
        os.replace(temp_path, final_path)


def _finish_job(job_id: int, fotografija_id: int, tip: str) -> None:
    with get_postgres_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                UPDATE foto_poslovi
                SET status = 'uspeh', poslednja_greska = NULL, updated_at = now()
                WHERE id = %s
                """,
                (job_id,),
            )
            if tip == 'derivati':
                cur.execute(
                    """
                    UPDATE fotografije SET status = 'spremna', updated_at = now()
                    WHERE id = %s
                    """,
                    (fotografija_id,),
                )


def _fail_job(job_id: int, fotografija_id: int, tip: str, attempts_before: int, error: str) -> None:
    attempts = attempts_before + 1
    final = attempts >= MAX_ATTEMPTS
    backoff = BACKOFF_MINUTES[min(attempts - 1, len(BACKOFF_MINUTES) - 1)]
    with get_postgres_connection() as conn:
        with conn.cursor() as cur:
            if final:
                cur.execute(
                    """
                    UPDATE foto_poslovi
                    SET status = 'greska', pokusaji = %s, poslednja_greska = %s,
                        updated_at = now()
                    WHERE id = %s
                    """,
                    (attempts, error, job_id),
                )
                if tip == 'derivati':
                    cur.execute(
                        """
                        UPDATE fotografije SET status = 'greska', updated_at = now()
                        WHERE id = %s
                        """,
                        (fotografija_id,),
                    )
            else:
                cur.execute(
                    """
                    UPDATE foto_poslovi
                    SET status = 'ceka', pokusaji = %s, poslednja_greska = %s,
                        sledeci_pokusaj_at = now() + make_interval(mins => %s),
                        zakljucan_at = NULL, zakljucao = NULL, updated_at = now()
                    WHERE id = %s
                    """,
                    (attempts, error, backoff, job_id),
                )
    logger.error(
        "Fototeka job %s (%s, photo %s) failed attempt %d/%d%s: %s",
        job_id, tip, fotografija_id, attempts, MAX_ATTEMPTS,
        ' — GIVING UP' if final else f', retry in {backoff}min', error,
    )


def _process_fixity(fotografija_id: int, sha256: str, raw_full_path: Path) -> None:
    ok = raw_full_path.is_file() and sha256_of_file(raw_full_path) == sha256
    if not ok:
        logger.error(
            "FIXITY MISMATCH for photo %s: %s", fotografija_id, raw_full_path,
        )
    with get_postgres_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                UPDATE fotografije
                SET fixity_ok = %s, fixity_proveren_at = now(), updated_at = now()
                WHERE id = %s
                """,
                (ok, fotografija_id),
            )


def process_job(job) -> bool:
    """Run one claimed job to completion, recording success or retry/failure.
    Returns True on success."""
    raw_full_path = get_arhiva_path() / job['raw_putanja']
    try:
        if job['tip'] == 'derivati':
            make_derivatives(raw_full_path, job['sha256'])
        elif job['tip'] == 'fixity':
            _process_fixity(job['fotografija_id'], job['sha256'], raw_full_path)
        else:
            raise ValueError(f"Unknown job type: {job['tip']}")
    except Exception as exc:  # noqa: BLE001 - every failure goes to the retry path
        _fail_job(job['id'], job['fotografija_id'], job['tip'], job['pokusaji'], str(exc))
        return False
    _finish_job(job['id'], job['fotografija_id'], job['tip'])
    return True


def enqueue_fixity_batch(limit: int = 500) -> int:
    """Queue a fixity check for the photos least recently verified. Called by
    the monthly systemd timer (planned for a later phase)."""
    with get_postgres_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO foto_poslovi (fotografija_id, tip)
                SELECT f.id, 'fixity'
                FROM fotografije f
                WHERE f.obrisana = FALSE
                  AND NOT EXISTS (
                      SELECT 1 FROM foto_poslovi p
                      WHERE p.fotografija_id = f.id AND p.tip = 'fixity'
                        AND p.status IN ('ceka', 'radi')
                  )
                ORDER BY f.fixity_proveren_at ASC NULLS FIRST
                LIMIT %s
                RETURNING id
                """,
                (limit,),
            )
            queued = cur.fetchall()
    return len(queued)


def raw_intake_relative_path(*, veza_predmet=None, veza_teren=None,
                             original_ime: str, sha256: str,
                             datum: date | None = None) -> str:
    """RAW layout by ORIGIN at intake (never moved afterwards):
    zbirke/<zbirka>/<inv-broj>/ for collection items,
    teren/<godina>/<akcija>/ for field trips, razno/<godina>/ otherwise."""
    safe_name = Path(original_ime or 'fotografija').name
    stem = Path(safe_name).stem or 'fotografija'
    ext = Path(safe_name).suffix.lower() or '.jpg'
    filename = f"{stem}__{sha256[:8]}{ext}"
    if veza_predmet:
        database_name, inventarni_broj = veza_predmet
        return f"zbirke/{_safe_segment(database_name)}/{_safe_segment(inventarni_broj)}/{filename}"
    if veza_teren:
        godina, naziv = veza_teren
        return f"teren/{int(godina)}/{_safe_segment(naziv)}/{filename}"
    godina = (datum or date.today()).year
    return f"razno/{godina}/{filename}"


def _safe_segment(value) -> str:
    """Directory segment readable without the application: keep letters
    (including Cyrillic), digits, dash, underscore and space; everything else
    (path separators, dots) becomes an underscore. Dropping dots means a
    stray '..' can never form, so no segment can act as parent traversal."""
    text = str(value or '').strip() or 'nepoznato'
    cleaned = ''.join(
        ch if (ch.isalnum() or ch in '-_ ') else '_' for ch in text
    ).strip(' _')
    return cleaned.replace(' ', '_') or 'nepoznato'
