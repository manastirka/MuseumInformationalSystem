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

# Extensions the bundled libvips can decode into a derivative. Anything else
# (camera RAW: CR2/NEF/ARW/DNG..., and BMP) is archived as-is but gets no
# auto-derivative — status 'bez_derivata' instead of an endless retry.
DERIVABLE_EXTENSIONS = {
    '.jpg', '.jpeg', '.jpe', '.jfif', '.png', '.tif', '.tiff',
    '.webp', '.gif', '.heic', '.heif', '.avif',
}


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


def reconcile_intake_pending(min_age_minutes: int = 30) -> dict:
    """Idempotentno uparivanje namera intake-a sa stvarnim stanjem (stavka 5).

    Za svaku nameru (fototeka_intake_pending) stariju od praga:
      * red fotografije postoji  -> finalizacija je ispala, briše se samo namera;
      * reda nema, RAW postoji   -> siroče propalog commit-a: briše se RAW i namera;
      * reda nema, RAW ne postoji-> briše se namera (fajl nikad nije postavljen
        ili ga je cleanup već uklonio).
    Sme da se pušta koliko god puta (worker je zove periodično)."""
    stats = {'finalized': 0, 'orphan_removed': 0, 'stale_cleared': 0}
    arhiva = get_arhiva_path()
    with get_postgres_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT id, raw_putanja FROM fototeka_intake_pending
                WHERE created_at < now() - make_interval(mins => %s)
                ORDER BY id
                FOR UPDATE SKIP LOCKED
                """,
                (min_age_minutes,),
            )
            pending = cur.fetchall()
            for row in pending:
                pending_id = row['id'] if isinstance(row, dict) else row[0]
                raw_rel = row['raw_putanja'] if isinstance(row, dict) else row[1]
                cur.execute('SELECT 1 FROM fotografije WHERE raw_putanja = %s',
                            (raw_rel,))
                if cur.fetchone():
                    stats['finalized'] += 1
                else:
                    raw_full = arhiva / raw_rel
                    if raw_full.exists():
                        try:
                            raw_full.unlink()
                            stats['orphan_removed'] += 1
                            logger.warning(
                                "Intake reconcile: uklonjeno RAW siroče %s", raw_rel)
                        except OSError:
                            logger.exception(
                                "Intake reconcile: RAW siroče %s nije uklonjeno — "
                                "namera ostaje za sledeći prolaz", raw_rel)
                            continue
                    else:
                        stats['stale_cleared'] += 1
                cur.execute('DELETE FROM fototeka_intake_pending WHERE id = %s',
                            (pending_id,))
    return stats


def reclaim_stale_jobs() -> int:
    """Return jobs stuck in 'radi' (worker died mid-job) to the queue.

    A stale 'radi' job means the worker died mid-job — possibly a native
    libvips crash / OOM kill that never ran _fail_job. Count that as an attempt
    so a file that reliably kills the worker eventually dead-letters to 'greska'
    instead of looping forever and taking the service down with it."""
    with get_postgres_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                UPDATE foto_poslovi
                SET pokusaji = pokusaji + 1,
                    status = CASE WHEN pokusaji + 1 >= %s THEN 'greska' ELSE 'ceka' END,
                    poslednja_greska = CASE WHEN pokusaji + 1 >= %s
                        THEN 'worker прекинут (могуће crash/OOM) — исцрпљени покушаји'
                        ELSE 'worker прекинут усред посла — враћено у ред' END,
                    sledeci_pokusaj_at = NULL,
                    zakljucan_at = NULL, zakljucao = NULL, updated_at = now()
                WHERE status = 'radi'
                  AND zakljucan_at < now() - make_interval(mins => %s)
                RETURNING id, fotografija_id, tip, status
                """,
                (MAX_ATTEMPTS, MAX_ATTEMPTS, STALE_LOCK_MINUTES),
            )
            reclaimed = [_row_to_dict(cur, row) for row in cur.fetchall()]
            # A dead-lettered derivative job must flip its photo to 'greska'
            # (mirrors _fail_job) so the UI stops showing "obrada u toku".
            for job in reclaimed:
                if job['status'] == 'greska' and job['tip'] == 'derivati':
                    cur.execute(
                        """
                        UPDATE fotografije SET status = 'greska', updated_at = now()
                        WHERE id = %s
                        """,
                        (job['fotografija_id'],),
                    )
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
                       f.sha256, f.raw_putanja, f.ekstenzija
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
    crash never leaves a half-written file at the final path. The temp name is
    per-process so a stale-reclaim retry or a second worker handling the same
    sha never write the same temp file and corrupt each other's output; a
    leftover temp is always cleaned up."""
    import pyvips

    media_root = get_media_path()
    for kind, size in DERIVATIVE_SIZES.items():
        final_path = media_root / derivative_relative_path(sha256, kind)
        final_path.parent.mkdir(parents=True, exist_ok=True)
        temp_path = final_path.with_name(f".tmp_{os.getpid()}_{final_path.name}")
        try:
            image = pyvips.Image.thumbnail(
                str(raw_full_path), size, height=size, size='down',
            )
            image.write_to_file(str(temp_path), Q=JPEG_QUALITY)
            os.replace(temp_path, final_path)
        finally:
            if temp_path.exists():
                temp_path.unlink()


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


def _process_fixity(fotografija_id: int, sha256: str, raw_full_path: Path) -> dict:
    """Verify one archival original and return a machine-readable report.

    A mismatch also emits one structured ERROR line suitable for journald and
    log alerts. It distinguishes a missing original from changed bytes and
    includes both hashes so an operator has enough information to investigate.
    """
    file_exists = raw_full_path.is_file()
    actual_sha256 = sha256_of_file(raw_full_path) if file_exists else None
    ok = file_exists and actual_sha256 == sha256
    if ok:
        status = 'ok'
    elif not file_exists:
        status = 'missing_file'
    else:
        status = 'checksum_mismatch'

    report = {
        'ok': ok,
        'fotografija_id': fotografija_id,
        'status': status,
        'raw_putanja': str(raw_full_path),
        'expected_sha256': sha256,
        'actual_sha256': actual_sha256,
    }
    if not ok:
        logger.error(
            "FOTOTEKA_FIXITY_MISMATCH photo_id=%s reason=%s path=%s "
            "expected_sha256=%s actual_sha256=%s",
            fotografija_id, status, raw_full_path, sha256,
            actual_sha256 or '<missing>',
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
    return report


def _mark_no_derivative(job_id: int, fotografija_id: int, reason: str) -> None:
    """The archival original cannot be decoded (camera RAW, BMP, ...). The
    photo stays valid with status 'bez_derivata'; a curator may attach a JPG
    preview later. The job succeeds — no retry storm."""
    with get_postgres_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                UPDATE foto_poslovi
                SET status = 'uspeh', poslednja_greska = %s, updated_at = now()
                WHERE id = %s
                """,
                (f'bez derivata: {reason}', job_id),
            )
            cur.execute(
                """
                UPDATE fotografije SET status = 'bez_derivata', updated_at = now()
                WHERE id = %s
                """,
                (fotografija_id,),
            )
    logger.info(
        "Fototeka photo %s archived without derivative (%s)", fotografija_id, reason,
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
    except Exception as exc:  # noqa: BLE001
        ext = (job.get('ekstenzija') or '').lower()
        # A format libvips genuinely can't decode is a permanent condition —
        # mark 'bez_derivata' (no retry storm). But a transient OS-level
        # failure (disk full, I/O error, out of memory) must RETRY, not be
        # frozen as permanent just because the extension is non-derivable.
        transient = isinstance(exc, (OSError, MemoryError))
        if (job['tip'] == 'derivati' and ext not in DERIVABLE_EXTENSIONS
                and not transient):
            _mark_no_derivative(job['id'], job['fotografija_id'], str(exc))
            return True
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
    # Full sha256 (not a truncated prefix): the intake path must be unique per
    # exact content so two different files can never collide onto the same
    # archive path and overwrite each other's write-once original.
    filename = f"{stem}__{sha256}{ext}"
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
