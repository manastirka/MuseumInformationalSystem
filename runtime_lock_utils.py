"""Cross-process runtime guards plus locked JSON file access."""

from __future__ import annotations

import copy
import hashlib
import json
import os
import tempfile
from contextlib import contextmanager
from pathlib import Path
from typing import Any, Callable, Optional

import fcntl


def try_acquire_process_lock(lock_path: str | os.PathLike[str]) -> Optional[int]:
    """Acquire an exclusive non-blocking lock and keep the fd open on success."""
    path = Path(lock_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    fd = os.open(path, os.O_CREAT | os.O_RDWR, 0o600)
    try:
        fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
        os.ftruncate(fd, 0)
        os.write(fd, str(os.getpid()).encode('ascii'))
        os.fsync(fd)
        return fd
    except OSError:
        os.close(fd)
        return None


def _json_lock_path(path: str | os.PathLike[str]) -> Path:
    target = Path(path)
    parent = target.parent
    if os.access(parent, os.W_OK):
        return parent / f'.{target.name}.lock'

    resolved = target.resolve(strict=False)
    digest = hashlib.sha256(str(resolved).encode('utf-8')).hexdigest()[:16]
    lock_root = Path(
        os.environ.get(
            'MUSEUM_JSON_LOCK_DIR',
            os.path.join(tempfile.gettempdir(), 'museum_info_system_json_locks'),
        )
    )
    filename = f'{target.name}.{digest}.lock'
    return lock_root / filename


@contextmanager
def _locked_json_sidecar(path: str | os.PathLike[str], lock_mode: int):
    lock_path = _json_lock_path(path)
    lock_path.parent.mkdir(parents=True, exist_ok=True)
    with open(lock_path, 'a+', encoding='utf-8') as handle:
        fcntl.flock(handle.fileno(), lock_mode)
        try:
            yield
        finally:
            fcntl.flock(handle.fileno(), fcntl.LOCK_UN)


def _copy_default(default: Any) -> Any:
    return copy.deepcopy(default)


def load_json_file(path: str | os.PathLike[str], default: Any = None) -> Any:
    """Load JSON while holding a shared lock that blocks concurrent writers."""
    target = Path(path)
    with _locked_json_sidecar(target, fcntl.LOCK_SH):
        if not target.exists():
            return _copy_default(default)
        with open(target, 'r', encoding='utf-8') as handle:
            return json.load(handle)


def _write_json_unlocked(path: str | os.PathLike[str], payload: Any, **dump_kwargs: Any) -> None:
    """Atomically write JSON to disk using a temp file + replace."""
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)

    fd, tmp_path = tempfile.mkstemp(
        dir=str(target.parent),
        prefix=f'.{target.name}.',
        suffix='.tmp',
        text=True,
    )
    try:
        with os.fdopen(fd, 'w', encoding='utf-8') as handle:
            dump_options = {'ensure_ascii': False, 'indent': 2}
            dump_options.update(dump_kwargs)
            json.dump(payload, handle, **dump_options)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(tmp_path, target)
    finally:
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)


def atomic_write_json(path: str | os.PathLike[str], payload: Any, **dump_kwargs: Any) -> None:
    """Backward-compatible alias for callers that already use atomic writes."""
    _write_json_unlocked(path, payload, **dump_kwargs)


def write_json_file(path: str | os.PathLike[str], payload: Any, **dump_kwargs: Any) -> None:
    """Write JSON while holding an exclusive lock so readers never see partial data."""
    with _locked_json_sidecar(path, fcntl.LOCK_EX):
        _write_json_unlocked(path, payload, **dump_kwargs)


def update_json_file(
    path: str | os.PathLike[str],
    updater: Callable[[Any], Any],
    default: Any = None,
    **dump_kwargs: Any,
) -> Any:
    """Run a read-modify-write JSON update under one exclusive lock."""
    target = Path(path)
    with _locked_json_sidecar(target, fcntl.LOCK_EX):
        if target.exists():
            with open(target, 'r', encoding='utf-8') as handle:
                current = json.load(handle)
        else:
            current = _copy_default(default)
        updated = updater(current)
        _write_json_unlocked(target, updated, **dump_kwargs)
        return updated
