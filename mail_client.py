#!/usr/bin/env python3
"""
Mail Client Engine — PostgreSQL cache-first architecture.

All browsing reads from a per-user PostgreSQL cache (instant).
A background thread syncs headers + pre-fetches bodies from IMAP.
Message bodies are fetched on-demand and cached locally.
Mark-read flags are queued and flushed to IMAP in the background.
"""

import os
import re
import json
import html as html_lib
import hashlib
import imaplib
import smtplib
import email
import email.utils
import email.header
import email.mime.text
import email.mime.multipart
import email.mime.base
import email.encoders
import logging
import threading
import time
import ipaddress
from pathlib import Path
from urllib.parse import urlparse

from bs4 import BeautifulSoup, Comment
from cryptography.fernet import Fernet
from psycopg.rows import dict_row
from runtime_lock_utils import load_json_file, update_json_file, write_json_file

from postgres_service import get_postgres_connection

logger = logging.getLogger(__name__)

DATA_DIR = Path(__file__).parent / 'data'
SETTINGS_FILE = DATA_DIR / 'mail_settings.json'
KEY_FILE = DATA_DIR / '.mail_key'
CACHE_DIR = DATA_DIR / 'mail_cache'
MAIL_SETTINGS_KEY_ENV = 'MAIL_SETTINGS_ENCRYPTION_KEY'
MAIL_SETTINGS_TABLE = 'mail_user_settings'
MAIL_ALLOWED_HOSTS_KEY = 'mail_allowed_hosts'
MAIL_BANNED_HOSTS_KEY = 'mail_banned_hosts'

_settings_lock = threading.Lock()

TRUSTED_MAIL_DOMAINS = tuple(
    domain.strip().lower()
    for domain in os.environ.get('TRUSTED_MAIL_DOMAINS', 'nhmbeo.rs').split(',')
    if domain.strip()
)

_DANGEROUS_ATTACHMENT_EXTENSIONS = {
    '.ade', '.adp', '.apk', '.app', '.bat', '.chm', '.cmd', '.com', '.cpl',
    '.docm', '.exe', '.hta', '.htm', '.html', '.iso', '.jar', '.js', '.jse',
    '.lnk', '.mht', '.mhtml', '.msi', '.msix', '.pif', '.pptm', '.ps1', '.reg',
    '.scf', '.scr', '.sct', '.sh', '.svg', '.url', '.vb', '.vbe', '.vbs',
    '.ws', '.wsc', '.wsf', '.wsh', '.xlsm', '.xltm',
}

_HTML_DROP_TAGS = {
    'script', 'style', 'iframe', 'frame', 'frameset', 'object', 'embed',
    'form', 'input', 'button', 'textarea', 'select', 'option', 'meta', 'link',
    'base', 'img', 'picture', 'source', 'audio', 'video', 'canvas', 'svg',
}

_HTML_ALLOWED_TAGS = {
    'html', 'body', 'p', 'div', 'span', 'br', 'hr', 'ul', 'ol', 'li',
    'b', 'strong', 'i', 'em', 'u', 's', 'blockquote', 'pre', 'code',
    'table', 'thead', 'tbody', 'tfoot', 'tr', 'th', 'td',
    'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
}

_HTML_ALLOWED_ATTRS = {
    'td': {'colspan', 'rowspan'},
    'th': {'colspan', 'rowspan'},
}

_LOGIN_HINTS = ('login', 'signin', 'verify', 'password', 'auth', 'account', 'sso')

# ===================== Encryption =====================

_fernet_instance = None
_fernet_lock = threading.Lock()
_mail_settings_initialized = False
_mail_settings_init_lock = threading.Lock()


def _production_mode() -> bool:
    return os.environ.get('FLASK_ENV', '').strip().lower() == 'production'


def _shared_mail_settings_enabled() -> bool:
    return bool(os.environ.get('DATABASE_URL'))


def _get_configured_mail_key() -> bytes | None:
    configured = (os.environ.get(MAIL_SETTINGS_KEY_ENV) or '').strip()
    return configured.encode() if configured else None


def _get_legacy_file_fernet() -> Fernet | None:
    if not KEY_FILE.exists():
        return None
    return Fernet(KEY_FILE.read_bytes().strip())


def _legacy_settings_exist() -> bool:
    return SETTINGS_FILE.exists()


def _get_fernet():
    global _fernet_instance
    if _fernet_instance is not None:
        return _fernet_instance
    with _fernet_lock:
        if _fernet_instance is not None:
            return _fernet_instance
        configured_key = _get_configured_mail_key()
        if configured_key:
            _fernet_instance = Fernet(configured_key)
            return _fernet_instance

        if KEY_FILE.exists():
            _fernet_instance = Fernet(KEY_FILE.read_bytes().strip())
            if _production_mode():
                logger.warning(
                    "%s is not set; using existing local mail key file %s.",
                    MAIL_SETTINGS_KEY_ENV,
                    KEY_FILE,
                )
            return _fernet_instance

        if _production_mode():
            raise RuntimeError(
                f"{MAIL_SETTINGS_KEY_ENV} must be set in production, or {KEY_FILE} must exist, "
                "to encrypt and decrypt saved mail credentials."
            )

        if not KEY_FILE.exists():
            # Check if there are existing saved settings that would become
            # undecryptable if we generate a new key
            if SETTINGS_FILE.exists():
                logger.error(
                    "Mail encryption key missing (%s) but saved credentials exist (%s). "
                    "Restore the key file or delete mail_settings.json to re-enter credentials.",
                    KEY_FILE, SETTINGS_FILE,
                )
                raise RuntimeError(
                    "Mail encryption key missing — cannot decrypt saved credentials. "
                    "Restore the key file or remove mail_settings.json."
                )
            DATA_DIR.mkdir(parents=True, exist_ok=True)
            KEY_FILE.write_bytes(Fernet.generate_key())
            try:
                os.chmod(KEY_FILE, 0o600)
            except OSError:
                pass
            logger.info("Generated new mail encryption key at %s", KEY_FILE)
        _fernet_instance = Fernet(KEY_FILE.read_bytes().strip())
        return _fernet_instance


def _encrypt(plaintext: str) -> str:
    return _get_fernet().encrypt(plaintext.encode()).decode()


def _decrypt(token: str) -> str:
    return _get_fernet().decrypt(token.encode()).decode()


# ===================== Mail Host Policy =====================

def _normalize_mail_host(host: str) -> str:
    host = (host or '').strip().lower().rstrip('.')
    if not host:
        raise ValueError('Mail server host is required.')
    if '://' in host:
        raise ValueError('Mail server must be a hostname or IP address, not a URL.')
    if any(char in host for char in '/?#@'):
        raise ValueError('Mail server host is invalid.')

    try:
        ipaddress.ip_address(host)
        return host
    except ValueError:
        pass

    labels = host.split('.')
    if not labels or any(not label for label in labels):
        raise ValueError('Mail server host is invalid.')
    for label in labels:
        if len(label) > 63:
            raise ValueError('Mail server host is invalid.')
        if label.startswith('-') or label.endswith('-'):
            raise ValueError('Mail server host is invalid.')
        if not re.fullmatch(r'[a-z0-9-]+', label):
            raise ValueError('Mail server host is invalid.')

    return host


def normalize_allowed_mail_hosts(raw_hosts) -> list[str]:
    if raw_hosts is None:
        return []

    if isinstance(raw_hosts, str):
        candidates = re.split(r'[\s,;]+', raw_hosts)
    elif isinstance(raw_hosts, (list, tuple, set)):
        candidates = list(raw_hosts)
    else:
        raise ValueError('Allowed mail hosts must be a list or comma-separated string.')

    normalized_hosts = []
    seen = set()
    for candidate in candidates:
        if candidate is None:
            continue
        candidate_text = str(candidate).strip()
        if not candidate_text:
            continue
        normalized = _normalize_mail_host(candidate_text)
        if normalized not in seen:
            normalized_hosts.append(normalized)
            seen.add(normalized)
    return normalized_hosts


def get_allowed_mail_hosts() -> list[str]:
    configured_hosts = []
    env_hosts = os.environ.get('MAIL_ALLOWED_HOSTS', '')
    if env_hosts.strip():
        configured_hosts.extend(normalize_allowed_mail_hosts(env_hosts))

    try:
        from admin_system_views import load_saved_settings

        saved_settings = load_saved_settings() or {}
        saved_hosts = saved_settings.get(MAIL_ALLOWED_HOSTS_KEY, [])
        if saved_hosts:
            for host in normalize_allowed_mail_hosts(saved_hosts):
                if host not in configured_hosts:
                    configured_hosts.append(host)
    except Exception as exc:
        logger.warning("Could not load shared mail host policy: %s", exc)

    return configured_hosts


def get_banned_mail_hosts() -> list[str]:
    configured_hosts = []
    env_hosts = os.environ.get('MAIL_BANNED_HOSTS', '')
    if env_hosts.strip():
        configured_hosts.extend(normalize_allowed_mail_hosts(env_hosts))

    try:
        from admin_system_views import load_saved_settings

        saved_settings = load_saved_settings() or {}
        saved_hosts = saved_settings.get(MAIL_BANNED_HOSTS_KEY, [])
        if saved_hosts:
            for host in normalize_allowed_mail_hosts(saved_hosts):
                if host not in configured_hosts:
                    configured_hosts.append(host)
    except Exception as exc:
        logger.warning("Could not load shared mail deny policy: %s", exc)

    return configured_hosts


def ensure_mail_host_allowed(host: str, *, allowed_hosts=None, banned_hosts=None) -> str:
    normalized_host = _normalize_mail_host(host)
    normalized_allowed_hosts = normalize_allowed_mail_hosts(
        allowed_hosts if allowed_hosts is not None else get_allowed_mail_hosts()
    )
    normalized_banned_hosts = normalize_allowed_mail_hosts(
        banned_hosts if banned_hosts is not None else get_banned_mail_hosts()
    )
    if normalized_host in normalized_banned_hosts:
        raise ValueError(f"Mail server '{normalized_host}' is on the banned host list.")
    if normalized_host not in normalized_allowed_hosts:
        if normalized_allowed_hosts:
            raise ValueError(f"Mail server '{normalized_host}' is not in the allowed host list.")
        if normalized_banned_hosts:
            return normalized_host
        raise ValueError('No mail host policy is configured. Contact an administrator.')
    return normalized_host


def validate_mail_server_settings(settings: dict, *, allowed_hosts=None, banned_hosts=None) -> dict:
    validated = dict(settings or {})
    validated['imap_server'] = ensure_mail_host_allowed(
        validated.get('imap_server', ''),
        allowed_hosts=allowed_hosts,
        banned_hosts=banned_hosts,
    )
    validated['smtp_server'] = ensure_mail_host_allowed(
        validated.get('smtp_server', ''),
        allowed_hosts=allowed_hosts,
        banned_hosts=banned_hosts,
    )
    return validated


# ===================== Settings =====================

def _ensure_mail_settings_table(conn):
    global _mail_settings_initialized
    with _mail_settings_init_lock:
        if _mail_settings_initialized:
            return
        with conn.cursor() as cur:
            cur.execute(f"""
                CREATE TABLE IF NOT EXISTS {MAIL_SETTINGS_TABLE} (
                    user_email CITEXT PRIMARY KEY,
                    settings_json JSONB NOT NULL DEFAULT '{{}}'::jsonb,
                    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
                )
            """)
        conn.commit()
        _mail_settings_initialized = True


def _get_mail_settings_connection():
    if not _shared_mail_settings_enabled():
        return None
    try:
        conn = get_postgres_connection(row_factory=dict_row)
        _ensure_mail_settings_table(conn)
        return conn
    except Exception as exc:
        if _production_mode():
            raise RuntimeError(
                "PostgreSQL mail settings storage is unavailable in production."
            ) from exc
        logger.warning("Falling back to file-backed mail settings: %s", exc)
        return None


def _load_legacy_all_settings() -> dict:
    with _settings_lock:
        if not SETTINGS_FILE.exists():
            return {}
        return load_json_file(SETTINGS_FILE, default={})


def _save_legacy_all_settings(data: dict):
    with _settings_lock:
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        write_json_file(SETTINGS_FILE, data)


def _remove_legacy_user_settings(user_email: str):
    with _settings_lock:
        if not SETTINGS_FILE.exists():
            return
        def _remove(data):
            payload = dict(data or {})
            payload.pop(user_email, None)
            return payload

        updated = update_json_file(SETTINGS_FILE, _remove, default={})
        if not updated:
            SETTINGS_FILE.unlink(missing_ok=True)


def _normalize_db_settings(row_value) -> dict | None:
    if row_value is None:
        return None
    if isinstance(row_value, dict):
        return row_value
    if isinstance(row_value, str):
        return json.loads(row_value)
    return dict(row_value)


def _reencrypt_legacy_settings(settings: dict) -> dict:
    migrated = dict(settings)
    legacy_fernet = _get_legacy_file_fernet()
    if legacy_fernet and migrated.get('password'):
        plaintext = legacy_fernet.decrypt(migrated['password'].encode()).decode()
        migrated['password'] = _encrypt(plaintext)
    return migrated


def _load_db_user_settings(user_email: str) -> dict | None:
    conn = _get_mail_settings_connection()
    if not conn:
        return None
    try:
        with conn.cursor() as cur:
            cur.execute(
                f"SELECT settings_json FROM {MAIL_SETTINGS_TABLE} WHERE user_email = %s",
                (user_email,),
            )
            row = cur.fetchone()
        return _normalize_db_settings(row['settings_json']) if row else None
    finally:
        conn.close()


def _save_db_user_settings(user_email: str, settings: dict) -> bool:
    conn = _get_mail_settings_connection()
    if not conn:
        return False
    try:
        with conn.cursor() as cur:
            cur.execute(
                f"""
                INSERT INTO {MAIL_SETTINGS_TABLE}(user_email, settings_json, updated_at)
                VALUES(%s, %s, NOW())
                ON CONFLICT (user_email) DO UPDATE SET
                    settings_json = EXCLUDED.settings_json,
                    updated_at = NOW()
                """,
                (user_email, json.dumps(settings, ensure_ascii=False)),
            )
        conn.commit()
        return True
    finally:
        conn.close()


def _migrate_legacy_user_settings(user_email: str) -> dict | None:
    legacy_settings = _load_legacy_all_settings().get(user_email)
    if not legacy_settings:
        return None

    migrated_settings = _reencrypt_legacy_settings(legacy_settings)
    if _save_db_user_settings(user_email, migrated_settings):
        _remove_legacy_user_settings(user_email)
        logger.info("Migrated mail settings for %s into PostgreSQL shared storage", user_email)
    return migrated_settings


def load_all_settings() -> dict:
    conn = _get_mail_settings_connection()
    if conn:
        try:
            with conn.cursor() as cur:
                cur.execute(f"SELECT user_email, settings_json FROM {MAIL_SETTINGS_TABLE}")
                rows = cur.fetchall()
            return {
                row['user_email']: _normalize_db_settings(row['settings_json']) or {}
                for row in rows
            }
        finally:
            conn.close()
    return _load_legacy_all_settings()


def save_all_settings(data: dict):
    conn = _get_mail_settings_connection()
    if conn:
        try:
            with conn.cursor() as cur:
                for user_email, settings in data.items():
                    cur.execute(
                        f"""
                        INSERT INTO {MAIL_SETTINGS_TABLE}(user_email, settings_json, updated_at)
                        VALUES(%s, %s, NOW())
                        ON CONFLICT (user_email) DO UPDATE SET
                            settings_json = EXCLUDED.settings_json,
                            updated_at = NOW()
                        """,
                        (user_email, json.dumps(settings, ensure_ascii=False)),
                    )
            conn.commit()
            return
        finally:
            conn.close()
    _save_legacy_all_settings(data)


def get_user_settings(user_email: str) -> dict | None:
    settings = _load_db_user_settings(user_email)
    if settings is not None:
        return settings
    if _shared_mail_settings_enabled() and _legacy_settings_exist():
        migrated = _migrate_legacy_user_settings(user_email)
        if migrated is not None:
            return migrated
    return _load_legacy_all_settings().get(user_email)


def save_user_settings(user_email: str, settings: dict):
    if _save_db_user_settings(user_email, settings):
        _remove_legacy_user_settings(user_email)
        return
    s = _load_legacy_all_settings().copy()
    s[user_email] = settings
    _save_legacy_all_settings(s)


def get_user_settings_safe(user_email: str) -> dict | None:
    s = get_user_settings(user_email)
    if s is None:
        return None
    safe = dict(s)
    safe.pop('password', None)
    return safe


# ===================== IMAP Connection Helpers =====================

def _connect_imap(settings, password):
    """Create a fresh IMAP connection (login included)."""
    s = validate_mail_server_settings(settings)
    if s.get('imap_ssl', True):
        conn = imaplib.IMAP4_SSL(s['imap_server'], int(s.get('imap_port', 993)), timeout=15)
    else:
        conn = imaplib.IMAP4(s['imap_server'], int(s.get('imap_port', 143)))
    conn.login(s['email_address'], password)
    return conn


# ===================== IMAP Connection Pool (web requests only) =====================

_POOL_TTL = 270
_NOOP_THRESHOLD = 30

_pool: dict = {}
_pool_lock = threading.Lock()


def _pool_get(user_email: str, settings: dict, password: str):
    now = time.monotonic()
    with _pool_lock:
        entry = _pool.get(user_email)
        if entry and entry['pw'] == password and (now - entry['t'] < _POOL_TTL):
            conn = entry['c']
            if now - entry['t'] < _NOOP_THRESHOLD:
                entry['t'] = now
                return conn
            try:
                conn.noop()
                entry['t'] = now
                return conn
            except Exception:
                try:
                    conn.logout()
                except Exception:
                    pass
                del _pool[user_email]

    conn = _connect_imap(settings, password)

    with _pool_lock:
        old = _pool.get(user_email)
        if old:
            try:
                old['c'].logout()
            except Exception:
                pass
        _pool[user_email] = {
            'c': conn, 't': time.monotonic(), 'pw': password, 'sel': None
        }
    return conn


def _pool_selected(user_email: str) -> tuple[str | None, bool]:
    """Return currently selected folder and readonly state for this user's pool connection."""
    with _pool_lock:
        entry = _pool.get(user_email)
        if entry:
            return entry.get('sel'), entry.get('sel_ro', True)
        return None, True


def _pool_set_selected(user_email: str, folder: str | None, readonly: bool = True):
    """Track which folder is currently selected."""
    with _pool_lock:
        entry = _pool.get(user_email)
        if entry:
            entry['sel'] = folder
            entry['sel_ro'] = readonly


def _pool_release(user_email: str):
    with _pool_lock:
        e = _pool.get(user_email)
        if e:
            e['t'] = time.monotonic()


def _pool_invalidate(user_email: str):
    with _pool_lock:
        e = _pool.pop(user_email, None)
        if e:
            try:
                e['c'].logout()
            except Exception:
                pass


# ===================== PostgreSQL Mail Cache =====================

_SCHEMA = '''
CREATE TABLE IF NOT EXISTS mail_cache_folders (
    user_email CITEXT NOT NULL,
    name TEXT NOT NULL,
    uidvalidity BIGINT DEFAULT 0,
    highest_uid BIGINT DEFAULT 0,
    last_synced_at DOUBLE PRECISION DEFAULT 0,
    message_count INTEGER DEFAULT 0,
    unseen INTEGER DEFAULT 0,
    PRIMARY KEY (user_email, name)
);
ALTER TABLE mail_cache_folders
    ADD COLUMN IF NOT EXISTS last_synced_at DOUBLE PRECISION DEFAULT 0;
ALTER TABLE mail_cache_folders
    ADD COLUMN IF NOT EXISTS message_count INTEGER DEFAULT 0;
CREATE TABLE IF NOT EXISTS mail_cache_messages (
    user_email CITEXT NOT NULL,
    folder TEXT NOT NULL,
    uid BIGINT NOT NULL,
    from_name TEXT DEFAULT '',
    from_address TEXT DEFAULT '',
    reply_to_name TEXT DEFAULT '',
    reply_to_address TEXT DEFAULT '',
    subject TEXT DEFAULT '',
    date_iso TEXT DEFAULT '',
    received_iso TEXT DEFAULT '',
    sort_date_iso TEXT DEFAULT '',
    is_read BOOLEAN DEFAULT FALSE,
    has_body BOOLEAN DEFAULT FALSE,
    text_body TEXT DEFAULT '',
    html_body TEXT DEFAULT '',
    to_json TEXT DEFAULT '[]',
    cc_json TEXT DEFAULT '[]',
    attachments_json TEXT DEFAULT '[]',
    links_json TEXT DEFAULT '[]',
    PRIMARY KEY (user_email, folder, uid)
);
ALTER TABLE mail_cache_messages
    ADD COLUMN IF NOT EXISTS received_iso TEXT DEFAULT '';
ALTER TABLE mail_cache_messages
    ADD COLUMN IF NOT EXISTS sort_date_iso TEXT DEFAULT '';
CREATE INDEX IF NOT EXISTS mail_cache_messages_folder_idx
    ON mail_cache_messages(user_email, folder, uid DESC);
CREATE INDEX IF NOT EXISTS mail_cache_messages_date_idx
    ON mail_cache_messages(user_email, folder, date_iso DESC, uid DESC);
CREATE INDEX IF NOT EXISTS mail_cache_messages_sort_date_idx
    ON mail_cache_messages(user_email, folder, sort_date_iso DESC, uid DESC);
CREATE INDEX IF NOT EXISTS mail_cache_messages_sender_idx
    ON mail_cache_messages(user_email, folder, lower(from_name), uid DESC);
CREATE INDEX IF NOT EXISTS mail_cache_messages_subject_idx
    ON mail_cache_messages(user_email, folder, lower(subject), uid DESC);
CREATE INDEX IF NOT EXISTS mail_cache_messages_read_idx
    ON mail_cache_messages(user_email, folder, is_read, uid DESC);
CREATE TABLE IF NOT EXISTS mail_cache_meta (
    user_email CITEXT NOT NULL,
    key TEXT NOT NULL,
    value TEXT,
    PRIMARY KEY (user_email, key)
);
CREATE TABLE IF NOT EXISTS mail_cache_pending_reads (
    user_email CITEXT NOT NULL,
    folder TEXT NOT NULL,
    uid BIGINT NOT NULL,
    PRIMARY KEY (user_email, folder, uid)
);
'''


def _db_path(user_email: str) -> Path:
    h = hashlib.sha256(user_email.encode()).hexdigest()[:16]
    return CACHE_DIR / f'{h}.db'


# Track schema initialization this process
_db_initialized = False
_db_init_lock = threading.Lock()


def _get_db(user_email: str):
    global _db_initialized

    db = get_postgres_connection(row_factory=dict_row)
    with _db_init_lock:
        if not _db_initialized:
            db.execute(_SCHEMA)
            db.commit()
            _db_initialized = True
    return db


def _row_value(row, *keys, default=None):
    if row is None:
        return default
    if hasattr(row, 'keys'):
        for key in keys:
            if key in row:
                return row[key]
        return default
    for key in keys:
        if isinstance(key, int) and len(row) > key:
            return row[key]
    return default


def _has_cached_messages(db, user_email: str, folder='INBOX') -> bool:
    r = db.execute(
        'SELECT COUNT(*) AS message_count FROM mail_cache_messages WHERE user_email=%s AND folder=%s',
        (user_email, folder),
    ).fetchone()
    return _row_value(r, 'message_count', 0, default=0) > 0


def _cached_message_count(db, user_email: str, folder='INBOX') -> int:
    r = db.execute(
        'SELECT COUNT(*) AS message_count FROM mail_cache_messages WHERE user_email=%s AND folder=%s',
        (user_email, folder),
    ).fetchone()
    return int(_row_value(r, 'message_count', 0, default=0) or 0)


def _has_any_cached_mail(db, user_email: str) -> bool:
    folder_row = db.execute(
        'SELECT 1 AS ok FROM mail_cache_folders WHERE user_email=%s LIMIT 1',
        (user_email,),
    ).fetchone()
    if folder_row:
        return True
    message_row = db.execute(
        'SELECT 1 AS ok FROM mail_cache_messages WHERE user_email=%s LIMIT 1',
        (user_email,),
    ).fetchone()
    return bool(message_row)


def _last_sync_ts(db, user_email: str) -> float:
    r = db.execute(
        "SELECT value FROM mail_cache_meta WHERE user_email=%s AND key='last_sync'",
        (user_email,),
    ).fetchone()
    return float(_row_value(r, 'value', 0, default=0.0)) if r else 0.0


def _set_sync_ts(db, user_email: str):
    db.execute(
        """
        INSERT INTO mail_cache_meta(user_email, key, value)
        VALUES(%s, 'last_sync', %s)
        ON CONFLICT (user_email, key) DO UPDATE SET value = EXCLUDED.value
        """,
        (user_email, str(time.time())),
    )
    db.commit()


def _last_flag_sync_ts(db, user_email: str) -> float:
    r = db.execute(
        "SELECT value FROM mail_cache_meta WHERE user_email=%s AND key='last_flag_sync'",
        (user_email,),
    ).fetchone()
    return float(_row_value(r, 'value', 0, default=0.0)) if r else 0.0


def _set_flag_sync_ts(db, user_email: str):
    db.execute(
        """
        INSERT INTO mail_cache_meta(user_email, key, value)
        VALUES(%s, 'last_flag_sync', %s)
        ON CONFLICT (user_email, key) DO UPDATE SET value = EXCLUDED.value
        """,
        (user_email, str(time.time())),
    )
    db.commit()


def _folder_last_sync_ts(db, user_email: str, folder='INBOX') -> float:
    r = db.execute(
        'SELECT last_synced_at FROM mail_cache_folders WHERE user_email=%s AND name=%s',
        (user_email, folder),
    ).fetchone()
    return float(_row_value(r, 'last_synced_at', 0, default=0.0)) if r else 0.0


def _set_folder_sync_ts(db, user_email: str, folder='INBOX'):
    db.execute(
        '''
        INSERT INTO mail_cache_folders(user_email, name, last_synced_at)
        VALUES(%s, %s, %s)
        ON CONFLICT(user_email, name) DO UPDATE
            SET last_synced_at = EXCLUDED.last_synced_at
        ''',
        (user_email, folder, time.time()),
    )
    db.commit()


def _folder_sync_stale(db, user_email: str, folder='INBOX', ttl: int | None = None) -> bool:
    ttl = _FOLDER_SYNC_TTL if ttl is None else ttl
    if not _has_cached_messages(db, user_email, folder):
        return True
    last_folder_sync = _folder_last_sync_ts(db, user_email, folder)
    return (time.time() - last_folder_sync) > ttl


def _folder_has_more_history(db, user_email: str, folder='INBOX') -> bool:
    folder_row = db.execute(
        'SELECT message_count FROM mail_cache_folders WHERE user_email=%s AND name=%s',
        (user_email, folder),
    ).fetchone()
    message_count = int(_row_value(folder_row, 'message_count', 0, default=0) or 0)
    if message_count <= 0:
        return False
    return _cached_message_count(db, user_email, folder) < message_count


# ===================== Email Parsing Helpers =====================

def _decode_header_value(raw):
    if raw is None:
        return ''
    parts = email.header.decode_header(raw)
    out = []
    for data, charset in parts:
        if isinstance(data, bytes):
            out.append(data.decode(charset or 'utf-8', errors='replace'))
        else:
            out.append(data)
    return ' '.join(out)


def _parse_address(raw):
    name, addr = email.utils.parseaddr(raw or '')
    return _decode_header_value(name), addr


def _parse_address_list(raw):
    if not raw:
        return []
    return [{'name': _decode_header_value(n), 'address': a}
            for n, a in email.utils.getaddresses([raw])]


def _parse_date(raw):
    if not raw:
        return ''
    try:
        return email.utils.parsedate_to_datetime(raw).isoformat()
    except Exception:
        return raw


def _parse_internaldate_meta(meta: str) -> str:
    if not meta:
        return ''
    match = re.search(r'INTERNALDATE\s+"([^"]+)"', meta)
    if not match:
        return ''
    try:
        return email.utils.parsedate_to_datetime(match.group(1)).isoformat()
    except Exception:
        return ''


def _address_domain(address: str) -> str:
    if not address or '@' not in address:
        return ''
    return address.rsplit('@', 1)[-1].strip().lower()


def _is_trusted_domain(domain: str) -> bool:
    if not domain:
        return False
    return any(
        domain == trusted or domain.endswith(f'.{trusted}')
        for trusted in TRUSTED_MAIL_DOMAINS
    )


def _extract_urls_from_text(text: str) -> list[str]:
    urls = []
    for raw in re.findall(r'https?://[^\s<>"\']+', text or ''):
        url = raw.rstrip(').,;!?]}>')
        if url:
            urls.append(url)
    return urls


def _analyze_link(url: str, sender_domain: str = '', label: str = '') -> dict | None:
    try:
        parsed = urlparse((url or '').strip())
    except Exception:
        return None

    scheme = (parsed.scheme or '').lower()
    host = (parsed.hostname or '').lower()
    reasons = []

    if scheme not in {'http', 'https', 'mailto'}:
        reasons.append('unsupported_scheme')

    if host:
        try:
            ipaddress.ip_address(host)
            reasons.append('ip_host')
        except ValueError:
            pass

        if 'xn--' in host:
            reasons.append('punycode_host')

        url_lower = url.lower()
        if any(hint in url_lower for hint in _LOGIN_HINTS) and not _is_trusted_domain(host):
            reasons.append('external_login_page')

        if sender_domain and _is_trusted_domain(sender_domain) and not _is_trusted_domain(host):
            reasons.append('internal_sender_external_link')

        if scheme == 'http' and not host.startswith(('localhost', '127.', '::1')):
            reasons.append('insecure_http')

    if label:
        label_domain_match = re.search(r'([a-z0-9.-]+\.[a-z]{2,})', label.lower())
        if label_domain_match:
            label_domain = label_domain_match.group(1)
            if host and label_domain != host and not host.endswith(f'.{label_domain}') and not label_domain.endswith(f'.{host}'):
                reasons.append('label_domain_mismatch')

    return {
        'url': url,
        'label': label or host or url,
        'host': host,
        'scheme': scheme,
        'suspicious': bool(reasons),
        'reasons': reasons,
    }


def _dedupe_links(links: list[dict]) -> list[dict]:
    deduped = {}
    ordered = []
    for item in links:
        if not item or not item.get('url'):
            continue
        key = item['url']
        if key in deduped:
            existing = deduped[key]
            merged = set(existing.get('reasons', []))
            merged.update(item.get('reasons', []))
            existing['reasons'] = sorted(merged)
            existing['suspicious'] = bool(existing['reasons'])
            if not existing.get('label') and item.get('label'):
                existing['label'] = item['label']
            continue
        clone = dict(item)
        deduped[key] = clone
        ordered.append(clone)
    return ordered


def _sanitize_html_email(html_body: str, sender_domain: str = '') -> tuple[str, list[dict]]:
    if not html_body:
        return '', []

    soup = BeautifulSoup(html_body, 'lxml')
    links = []

    for comment in soup.find_all(string=lambda text: isinstance(text, Comment)):
        comment.extract()

    for tag in soup.find_all(_HTML_DROP_TAGS):
        tag.decompose()

    for anchor in soup.find_all('a'):
        href = (anchor.get('href') or '').strip()
        label = ' '.join(anchor.get_text(' ', strip=True).split())
        if href:
            analyzed = _analyze_link(href, sender_domain=sender_domain, label=label)
            if analyzed:
                links.append(analyzed)
        replacement = soup.new_tag('span')
        replacement['class'] = 'mail-disabled-link'
        replacement['title'] = 'Links are disabled in HTML preview'
        replacement.string = label or href or 'link'
        anchor.replace_with(replacement)

    for tag in soup.find_all(True):
        if tag.name not in _HTML_ALLOWED_TAGS:
            tag.unwrap()
            continue
        allowed_attrs = _HTML_ALLOWED_ATTRS.get(tag.name, set())
        for attr_name in list(tag.attrs):
            if attr_name not in allowed_attrs:
                del tag.attrs[attr_name]

    body_html = soup.body.decode_contents() if soup.body else str(soup)
    sanitized = f"""<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <style>
    body {{
      font-family: Arial, sans-serif;
      line-height: 1.6;
      color: #2f241d;
      margin: 0;
      padding: 0.75rem;
      background: #fffdf8;
      word-break: break-word;
    }}
    table {{
      border-collapse: collapse;
      max-width: 100%;
    }}
    th, td {{
      border: 1px solid rgba(110, 82, 54, 0.18);
      padding: 0.35rem 0.5rem;
      vertical-align: top;
    }}
    .mail-disabled-link {{
      color: #7a4a2d;
      text-decoration: underline dotted;
      font-weight: 600;
    }}
  </style>
</head>
<body>{body_html}</body>
</html>"""
    return sanitized, _dedupe_links(links)


def _annotate_attachments(attachments: list[dict]) -> list[dict]:
    annotated = []
    for attachment in attachments:
        item = dict(attachment)
        filename = (item.get('filename') or '').strip().lower()
        dangerous = False
        if '.' in filename:
            ext = f".{filename.rsplit('.', 1)[-1]}"
            dangerous = ext in _DANGEROUS_ATTACHMENT_EXTENSIONS
        item['dangerous'] = dangerous
        annotated.append(item)
    return annotated


def _build_message_security(from_address: str, reply_to_address: str, links: list[dict], attachments: list[dict]) -> dict:
    sender_domain = _address_domain(from_address)
    reply_domain = _address_domain(reply_to_address)
    dangerous_attachments = [attachment for attachment in attachments if attachment.get('dangerous')]
    suspicious_links = [link for link in links if link.get('suspicious')]
    score = 0
    reasons = []

    external_sender = bool(sender_domain and not _is_trusted_domain(sender_domain))
    reply_to_mismatch = bool(reply_to_address and reply_to_address.lower() != (from_address or '').lower())

    if external_sender:
        score += 2
        reasons.append('external_sender')
    if reply_to_mismatch:
        score += 3
        reasons.append('reply_to_mismatch')
    if suspicious_links:
        score += min(6, 2 * len(suspicious_links))
        reasons.append('suspicious_links')
    if dangerous_attachments:
        score += min(4, 2 * len(dangerous_attachments))
        reasons.append('dangerous_attachments')

    if score >= 7:
        risk_level = 'high'
    elif score >= 3:
        risk_level = 'medium'
    else:
        risk_level = 'low'

    return {
        'sender_domain': sender_domain,
        'reply_to_address': reply_to_address,
        'reply_to_domain': reply_domain,
        'external_sender': external_sender,
        'reply_to_mismatch': reply_to_mismatch,
        'suspicious_links': suspicious_links,
        'dangerous_attachments': dangerous_attachments,
        'html_links_disabled': bool(links),
        'score': score,
        'risk_level': risk_level,
        'reasons': reasons,
    }


def _parse_message_body(raw_bytes):
    """Parse RFC822 bytes into a structured dict."""
    msg = email.message_from_bytes(raw_bytes)

    fname, faddr = _parse_address(msg.get('From', ''))
    reply_name, reply_addr = _parse_address(msg.get('Reply-To', ''))
    to_list = _parse_address_list(msg.get('To', ''))
    cc_list = _parse_address_list(msg.get('Cc', ''))
    subject = _decode_header_value(msg.get('Subject', ''))
    date_iso = _parse_date(msg.get('Date', ''))

    html_body = ''
    text_body = ''
    attachments = []

    att_index = 0
    if msg.is_multipart():
        for part in msg.walk():
            ct = part.get_content_type()
            cd = str(part.get('Content-Disposition', ''))
            if 'attachment' in cd:
                attachments.append({
                    'index': att_index,
                    'filename': _decode_header_value(part.get_filename() or 'attachment'),
                    'content_type': ct,
                    'size': len(part.get_payload(decode=True) or b''),
                })
                att_index += 1
            elif ct == 'text/html':
                pl = part.get_payload(decode=True)
                html_body = pl.decode(part.get_content_charset() or 'utf-8', errors='replace')
            elif ct == 'text/plain' and not html_body:
                pl = part.get_payload(decode=True)
                text_body = pl.decode(part.get_content_charset() or 'utf-8', errors='replace')
    else:
        ct = msg.get_content_type()
        pl = msg.get_payload(decode=True)
        cs = msg.get_content_charset() or 'utf-8'
        if ct == 'text/html':
            html_body = pl.decode(cs, errors='replace') if pl else ''
        else:
            text_body = pl.decode(cs, errors='replace') if pl else ''

    sender_domain = _address_domain(faddr)
    sanitized_html, html_links = _sanitize_html_email(html_body, sender_domain=sender_domain)
    attachments = _annotate_attachments(attachments)
    text_links = [
        _analyze_link(url, sender_domain=sender_domain, label=url)
        for url in _extract_urls_from_text(text_body)
    ]
    links = _dedupe_links(html_links + text_links)

    return {
        'from_name': fname or (faddr.split('@')[0] if faddr else ''),
        'from_address': faddr,
        'reply_to_name': reply_name,
        'reply_to_address': reply_addr,
        'to': to_list,
        'cc': cc_list,
        'subject': subject,
        'date': date_iso,
        'html_body': sanitized_html,
        'text_body': text_body,
        'attachments': attachments,
        'links': links,
    }


def _store_body_in_cache(db, user_email: str, folder, uid, parsed):
    """Store parsed message body in PostgreSQL cache."""
    uid_int = int(uid)
    update_cursor = db.execute(
        '''
        UPDATE mail_cache_messages
        SET has_body=TRUE, text_body=%s, html_body=%s,
            reply_to_name=%s, reply_to_address=%s, to_json=%s, cc_json=%s,
            attachments_json=%s, links_json=%s
        WHERE user_email=%s AND folder=%s AND uid=%s
        ''',
        (
            parsed['text_body'], parsed['html_body'],
            parsed['reply_to_name'], parsed['reply_to_address'],
            json.dumps(parsed['to'], ensure_ascii=False),
            json.dumps(parsed['cc'], ensure_ascii=False),
            json.dumps(parsed['attachments'], ensure_ascii=False),
            json.dumps(parsed['links'], ensure_ascii=False),
            user_email, folder, uid_int,
        ),
    )
    if update_cursor.rowcount == 0:
        db.execute(
            '''
            INSERT INTO mail_cache_messages(
                user_email, folder, uid, from_name, from_address,
                reply_to_name, reply_to_address, subject, date_iso, is_read,
                has_body, text_body, html_body, to_json, cc_json, attachments_json,
                links_json
            )
            VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, FALSE, TRUE, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (user_email, folder, uid) DO UPDATE SET
                from_name = EXCLUDED.from_name,
                from_address = EXCLUDED.from_address,
                reply_to_name = EXCLUDED.reply_to_name,
                reply_to_address = EXCLUDED.reply_to_address,
                subject = EXCLUDED.subject,
                date_iso = EXCLUDED.date_iso,
                has_body = EXCLUDED.has_body,
                text_body = EXCLUDED.text_body,
                html_body = EXCLUDED.html_body,
                to_json = EXCLUDED.to_json,
                cc_json = EXCLUDED.cc_json,
                attachments_json = EXCLUDED.attachments_json,
                links_json = EXCLUDED.links_json
            ''',
            (
                user_email, folder, uid_int,
                parsed['from_name'], parsed['from_address'],
                parsed['reply_to_name'], parsed['reply_to_address'],
                parsed['subject'], parsed['date'],
                parsed['text_body'], parsed['html_body'],
                json.dumps(parsed['to'], ensure_ascii=False),
                json.dumps(parsed['cc'], ensure_ascii=False),
                json.dumps(parsed['attachments'], ensure_ascii=False),
                json.dumps(parsed['links'], ensure_ascii=False),
            ),
        )
    db.commit()


def _adjust_folder_unseen(db, user_email: str, folder, delta):
    if not folder or delta == 0:
        return
    db.execute(
        '''
        UPDATE mail_cache_folders
        SET unseen = CASE
            WHEN COALESCE(unseen, 0) + %s < 0 THEN 0
            ELSE COALESCE(unseen, 0) + %s
        END
        WHERE user_email=%s AND name=%s
        ''',
        (delta, delta, user_email, folder),
    )


def _set_cached_read_state(db, user_email: str, folder, uid, is_read) -> bool:
    row = db.execute(
        'SELECT is_read FROM mail_cache_messages WHERE user_email=%s AND folder=%s AND uid=%s',
        (user_email, folder, uid)
    ).fetchone()
    if not row:
        return False

    next_state = bool(is_read)
    prev_state = bool(row['is_read'])
    if prev_state == next_state:
        return False

    db.execute(
        'UPDATE mail_cache_messages SET is_read=%s WHERE user_email=%s AND folder=%s AND uid=%s',
        (next_state, user_email, folder, uid)
    )
    _adjust_folder_unseen(db, user_email, folder, -1 if is_read else 1)
    return True


def _remove_cached_message(db, user_email: str, folder, uid):
    row = db.execute(
        'SELECT is_read FROM mail_cache_messages WHERE user_email=%s AND folder=%s AND uid=%s',
        (user_email, folder, uid)
    ).fetchone()
    if row and not bool(row['is_read']):
        _adjust_folder_unseen(db, user_email, folder, -1)

    db.execute(
        'DELETE FROM mail_cache_messages WHERE user_email=%s AND folder=%s AND uid=%s',
        (user_email, folder, uid),
    )
    db.execute(
        'DELETE FROM mail_cache_pending_reads WHERE user_email=%s AND folder=%s AND uid=%s',
        (user_email, folder, uid),
    )
    db.commit()


# ===================== IMAP Sync Engine =====================

_MAX_INITIAL_SYNC = 200
_FOLDER_SYNC_TTL = 180
_BG_FOLDER_BATCH_SIZE = 4
_HEADER_FETCH_CHUNK = 40


def do_sync(
    M,
    db,
    user_email: str,
    folder='INBOX',
    refresh_folder_list=True,
    backfill_history: bool = True,
) -> bool:
    """Sync a single folder. Skips flag sync if no new messages found."""
    try:
        if refresh_folder_list:
            _sync_folder_list(M, db, user_email)
        new_count = _sync_headers(M, db, user_email, folder)
        if new_count is None:
            return False
        older_count = 0
        if backfill_history:
            older_count = _backfill_older_headers(M, db, user_email, folder)
            if older_count is None:
                return False
        last_flag = _last_flag_sync_ts(db, user_email)
        if new_count > 0 or older_count > 0 or (time.time() - last_flag) > 600:
            _sync_flags(M, db, user_email, folder, limit=100)
            _set_flag_sync_ts(db, user_email)
        _set_folder_sync_ts(db, user_email, folder)
        _set_sync_ts(db, user_email)
        return True
    except Exception as e:
        logger.warning(f"Mail sync error for {folder}: {e}")
        return False


def _folder_sort_key(name: str):
    n = (name or '').lower()
    if n == 'inbox' or 'inbox' in n or 'пристиг' in n:
        return (0, name.lower())
    if 'sent' in n or 'послат' in n:
        return (1, name.lower())
    if 'draft' in n or 'нацрт' in n:
        return (2, name.lower())
    if 'archive' in n or 'архив' in n:
        return (3, name.lower())
    if 'junk' in n or 'spam' in n or 'нежељ' in n:
        return (4, name.lower())
    if 'trash' in n or 'deleted' in n or 'смеће' in n or 'smece' in n:
        return (5, name.lower())
    return (100, name.lower())


def _background_folder_queue(db, user_email: str) -> list[str]:
    rows = db.execute(
        'SELECT name FROM mail_cache_folders WHERE user_email=%s',
        (user_email,),
    ).fetchall()
    names = [r['name'] for r in rows if r and r.get('name')]
    if 'INBOX' not in names:
        names.append('INBOX')
    unique_names = list(dict.fromkeys(names))
    return sorted(unique_names, key=_folder_sort_key)


def _background_folder_batch(folders: list[str], cursor: int, batch_size: int = _BG_FOLDER_BATCH_SIZE):
    others = [folder for folder in folders if folder != 'INBOX']
    if not others:
        return [], 0
    if cursor >= len(others):
        cursor = 0
    batch = []
    for offset in range(min(batch_size, len(others))):
        batch.append(others[(cursor + offset) % len(others)])
    next_cursor = (cursor + len(batch)) % len(others) if others else 0
    return batch, next_cursor


def _chunks(items, size: int):
    for start in range(0, len(items), size):
        yield items[start:start + size]


def _backfill_older_headers(M, db, user_email: str, folder, chunk_size: int = _HEADER_FETCH_CHUNK) -> int | None:
    row = db.execute(
        '''
        SELECT MIN(uid) AS min_uid, COUNT(*) AS cached_count
        FROM mail_cache_messages
        WHERE user_email=%s AND folder=%s
        ''',
        (user_email, folder),
    ).fetchone()
    min_uid = _row_value(row, 'min_uid', 0, default=0) or 0
    cached_count = _row_value(row, 'cached_count', 0, default=0) or 0
    folder_row = db.execute(
        'SELECT message_count FROM mail_cache_folders WHERE user_email=%s AND name=%s',
        (user_email, folder),
    ).fetchone()
    message_count = int(_row_value(folder_row, 'message_count', 0, default=0) or 0)

    if not min_uid or cached_count >= message_count:
        return 0

    st, data = M.uid('search', None, f'UID 1:{int(min_uid) - 1}')
    if st != 'OK':
        logger.warning("Mail older-header search failed for folder %s: %s", folder, data)
        return None
    if not data or not data[0] or not data[0].strip():
        return 0

    older_uids = data[0].split()
    if not older_uids:
        return 0
    batch = older_uids[-chunk_size:]
    st_fetch, fdata = M.uid(
        'fetch',
        b','.join(batch),
        '(UID FLAGS INTERNALDATE BODY.PEEK[HEADER.FIELDS (FROM SUBJECT DATE)])'
    )
    if st_fetch != 'OK':
        logger.warning("Mail older-header fetch failed for folder %s: %s", folder, fdata)
        return None
    return _store_fetched_headers(db, user_email, folder, fdata)


def _sync_folder_list(M, db, user_email: str):
    """Sync folder names and unseen counts."""
    st, data = M.list()
    if st != 'OK':
        return
    names = []
    for item in (data or []):
        if item is None:
            continue
        line = item.decode('utf-8', errors='replace') if isinstance(item, bytes) else item
        parts = line.split(' "')
        if len(parts) >= 2:
            names.append(parts[-1].strip().strip('"'))

    for name in names:
        unseen = 0
        try:
            st2, cnt = M.status(f'"{name}"', '(UNSEEN)')
            if st2 == 'OK' and cnt:
                text = cnt[0].decode() if isinstance(cnt[0], bytes) else cnt[0]
                m = re.search(r'UNSEEN\s+(\d+)', text)
                unseen = int(m.group(1)) if m else 0
        except Exception:
            pass
        db.execute(
            '''
            INSERT INTO mail_cache_folders(user_email, name, unseen)
            VALUES(%s, %s, %s)
            ON CONFLICT(user_email, name) DO UPDATE SET unseen = EXCLUDED.unseen
            ''',
            (user_email, name, unseen),
        )
    db.commit()


def _sync_headers(M, db, user_email: str, folder) -> int | None:
    """Incremental header sync using UIDs. Returns count of new messages or None on hard failure."""
    st, resp = M.select(f'"{folder}"', readonly=True)
    if st != 'OK':
        logger.warning("Mail SELECT failed for folder %s: %s", folder, resp)
        return None
    exists = int(resp[0])
    db.execute(
        'UPDATE mail_cache_folders SET message_count=%s WHERE user_email=%s AND name=%s',
        (exists, user_email, folder),
    )
    db.commit()
    if exists == 0:
        return 0

    row = db.execute(
        'SELECT uidvalidity, highest_uid FROM mail_cache_folders WHERE user_email=%s AND name=%s',
        (user_email, folder),
    ).fetchone()
    highest_uid = row['highest_uid'] if row else 0
    total_count = 0

    if highest_uid > 0:
        st3, data = M.uid('search', None, f'UID {highest_uid + 1}:*')
        if st3 != 'OK':
            logger.warning("Mail UID search failed for folder %s: %s", folder, data)
            return None
        if not data[0] or not data[0].strip():
            return 0
        new_uids = [u for u in data[0].split() if int(u) > highest_uid]
        if not new_uids:
            return 0

        for batch in _chunks(new_uids, _HEADER_FETCH_CHUNK):
            uid_set = b','.join(batch)
            st4, fdata = M.uid('fetch', uid_set,
                                '(UID FLAGS INTERNALDATE BODY.PEEK[HEADER.FIELDS (FROM SUBJECT DATE)])')
            if st4 != 'OK':
                logger.warning("Mail UID fetch failed for folder %s: %s", folder, fdata)
                return None
            total_count += _store_fetched_headers(db, user_email, folder, fdata)

        max_uid = max(int(u) for u in new_uids)
        if max_uid > highest_uid:
            db.execute(
                'UPDATE mail_cache_folders SET highest_uid=%s WHERE user_email=%s AND name=%s',
                (max_uid, user_email, folder),
            )
            db.commit()
        return total_count
    else:
        start_seq = max(1, exists - _MAX_INITIAL_SYNC + 1)
        ranges = []
        batch_end = exists
        while batch_end >= start_seq:
            batch_start = max(start_seq, batch_end - _HEADER_FETCH_CHUNK + 1)
            ranges.append((batch_start, batch_end))
            batch_end = batch_start - 1

        for batch_start, batch_end in ranges:
            st3, fdata = M.fetch(
                f'{batch_start}:{batch_end}'.encode(),
                '(UID FLAGS INTERNALDATE BODY.PEEK[HEADER.FIELDS (FROM SUBJECT DATE)])'
            )
            if st3 != 'OK':
                logger.warning("Mail initial fetch failed for folder %s: %s", folder, fdata)
                return None
            total_count += _store_fetched_headers(db, user_email, folder, fdata)

        max_uid = db.execute(
            'SELECT MAX(uid) AS max_uid FROM mail_cache_messages WHERE user_email=%s AND folder=%s',
            (user_email, folder),
        ).fetchone()
        max_uid = _row_value(max_uid, 'max_uid', 0, default=0) or 0
        db.execute(
            'UPDATE mail_cache_folders SET highest_uid=%s WHERE user_email=%s AND name=%s',
            (max_uid, user_email, folder),
        )
        db.commit()
        return total_count


def _store_fetched_headers(db, user_email: str, folder, fetch_data) -> int:
    """Parse IMAP FETCH response and insert/update headers in PostgreSQL."""
    rows = []
    for item in fetch_data:
        if not isinstance(item, tuple) or len(item) < 2:
            continue
        meta = item[0].decode('utf-8', errors='replace') if isinstance(item[0], bytes) else item[0]
        hdr = item[1]

        uid_m = re.search(r'UID\s+(\d+)', meta)
        if not uid_m:
            continue
        uid = int(uid_m.group(1))
        is_read = '\\Seen' in meta

        msg = email.message_from_bytes(hdr) if isinstance(hdr, bytes) else email.message_from_string(hdr)
        fname, faddr = _parse_address(msg.get('From', ''))
        subject = _decode_header_value(msg.get('Subject', '(нема наслова)'))
        date_iso = _parse_date(msg.get('Date', ''))
        received_iso = _parse_internaldate_meta(meta)
        sort_date_iso = received_iso or date_iso or ''

        rows.append((
            folder, uid,
            fname or (faddr.split('@')[0] if faddr else 'Unknown'),
            faddr, subject, date_iso, received_iso, sort_date_iso, is_read,
        ))

    if rows:
        with db.cursor() as cur:
            cur.executemany(
                '''
                INSERT INTO mail_cache_messages(
                    user_email, folder, uid, from_name, from_address, subject, date_iso, received_iso, sort_date_iso, is_read
                )
                VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (user_email, folder, uid) DO UPDATE SET
                    from_name = EXCLUDED.from_name,
                    from_address = EXCLUDED.from_address,
                    subject = EXCLUDED.subject,
                    date_iso = EXCLUDED.date_iso,
                    received_iso = EXCLUDED.received_iso,
                    sort_date_iso = EXCLUDED.sort_date_iso,
                    is_read = EXCLUDED.is_read
                ''',
                [(user_email, *row) for row in rows],
            )
        db.commit()
    return len(rows)


def _sync_flags(M, db, user_email: str, folder, limit=100):
    """Update read/unread flags for recent cached messages."""
    cached = db.execute(
        'SELECT uid FROM mail_cache_messages WHERE user_email=%s AND folder=%s ORDER BY uid DESC LIMIT %s',
        (user_email, folder, limit)
    ).fetchall()
    if not cached:
        return
    uid_list = [str(r['uid']) for r in cached]
    uid_set = ','.join(uid_list).encode()

    st, data = M.uid('fetch', uid_set, '(UID FLAGS INTERNALDATE)')
    if st != 'OK':
        return

    updates = []
    for item in data:
        text = ''
        if isinstance(item, tuple):
            text = item[0].decode('utf-8', errors='replace') if isinstance(item[0], bytes) else item[0]
        elif isinstance(item, bytes):
            text = item.decode('utf-8', errors='replace')
        else:
            continue
        uid_m = re.search(r'UID\s+(\d+)', text)
        if not uid_m:
            continue
        uid = int(uid_m.group(1))
        is_read = '\\Seen' in text
        received_iso = _parse_internaldate_meta(text)
        sort_date_iso = received_iso or ''
        updates.append((is_read, received_iso, sort_date_iso, folder, uid))

    if updates:
        with db.cursor() as cur:
            cur.executemany(
                '''
                UPDATE mail_cache_messages
                SET is_read=%s,
                    received_iso=COALESCE(NULLIF(%s, ''), received_iso),
                    sort_date_iso=COALESCE(NULLIF(%s, ''), sort_date_iso)
                WHERE user_email=%s AND folder=%s AND uid=%s
                ''',
                [
                    (is_read, received_iso, sort_date_iso, user_email, folder_name, uid)
                    for (is_read, received_iso, sort_date_iso, folder_name, uid) in updates
                ],
            )
        db.commit()


def _prefetch_bodies(M, db, user_email: str, folder='INBOX', limit=10):
    """Pre-fetch RFC822 bodies for recent messages that haven't been opened yet.
    Called by bg worker after sync — folder should already be SELECTed."""
    rows = db.execute('''
        SELECT uid FROM mail_cache_messages
        WHERE user_email=%s AND folder=%s AND has_body=FALSE
        ORDER BY uid DESC LIMIT %s
    ''', (user_email, folder, limit)).fetchall()

    if not rows:
        return

    for row in rows:
        uid = row['uid']
        try:
            st, data = M.uid('fetch', str(uid).encode(), '(RFC822)')
            if st != 'OK' or not data or data[0] is None:
                continue
            raw = data[0][1] if isinstance(data[0], tuple) else data[0]
            parsed = _parse_message_body(raw)
            _store_body_in_cache(db, user_email, folder, uid, parsed)
        except Exception as e:
            logger.debug(f"Prefetch body error for uid {uid}: {e}")
            continue


def _flush_pending_reads(M, db, user_email: str):
    """Push locally-marked-as-read flags to IMAP server."""
    rows = db.execute(
        'SELECT folder, uid FROM mail_cache_pending_reads WHERE user_email=%s',
        (user_email,),
    ).fetchall()
    if not rows:
        return

    by_folder = {}
    for r in rows:
        by_folder.setdefault(r['folder'], []).append(r['uid'])

    for folder, uids in by_folder.items():
        try:
            M.select(f'"{folder}"')
            uid_set = ','.join(str(u) for u in uids).encode()
            M.uid('store', uid_set, '+FLAGS', '\\Seen')
        except Exception as e:
            logger.debug(f"Flush pending reads error for {folder}: {e}")
            continue

    db.execute('DELETE FROM mail_cache_pending_reads WHERE user_email=%s', (user_email,))
    db.commit()


# ===================== Background Sync Thread =====================

_sync_threads: dict = {}
_sync_tlock = threading.Lock()
_manual_sync_jobs: dict = {}
_manual_sync_lock = threading.Lock()


def ensure_bg_sync(user_email: str, settings: dict, password: str):
    """Start a background sync daemon for this user if not already running."""
    with _sync_tlock:
        t = _sync_threads.get(user_email)
        if t and t.is_alive():
            return
        t = threading.Thread(target=_bg_sync_worker,
                             args=(user_email, settings, password),
                             daemon=True, name=f'mail-sync-{user_email[:12]}')
        _sync_threads[user_email] = t
        t.start()


def _bg_sync_worker(user_email, settings, password):
    """Background worker: syncs headers, pre-fetches bodies, flushes read flags.
    Uses its own IMAP connection (NOT from pool) to avoid contention.
    Runs every 5 min, dies after 30 min."""
    deadline = time.monotonic() + 1800
    db = _get_db(user_email)
    M = None
    folder_cursor = 0

    def _sync_background_batch(initial=False):
        nonlocal folder_cursor
        _ensure_conn()
        _sync_folder_list(M, db, user_email)

        # Keep INBOX hottest because it is the primary working folder.
        do_sync(M, db, user_email, 'INBOX', refresh_folder_list=False)
        _prefetch_bodies(M, db, user_email, 'INBOX', limit=50 if initial else 20)

        folders = _background_folder_queue(db, user_email)
        batch_size = max(_BG_FOLDER_BATCH_SIZE, 6) if initial else _BG_FOLDER_BATCH_SIZE
        batch, folder_cursor = _background_folder_batch(folders, folder_cursor, batch_size=batch_size)
        for folder in batch:
            do_sync(M, db, user_email, folder, refresh_folder_list=False)
            _prefetch_bodies(M, db, user_email, folder, limit=12 if initial else 6)

        _flush_pending_reads(M, db, user_email)

    def _ensure_conn():
        nonlocal M
        if M is not None:
            try:
                M.noop()
                return
            except Exception:
                try:
                    M.logout()
                except Exception:
                    pass
                M = None
        M = _connect_imap(settings, password)

    # Immediate first pass: sync INBOX plus a first batch of other folders so
    # the user can switch folders without waiting on a cold cache.
    time.sleep(1)
    try:
        _sync_background_batch(initial=True)
    except Exception as e:
        logger.debug(f"Initial body prefetch error: {e}")

    while time.monotonic() < deadline:
        time.sleep(300)
        try:
            _sync_background_batch(initial=False)
        except Exception as e:
            logger.debug(f"Background mail sync error: {e}")
            try:
                if M:
                    M.logout()
            except Exception:
                pass
            M = None

    # Cleanup
    if M:
        try:
            M.logout()
        except Exception:
            pass
    try:
        db.close()
    except Exception:
        pass


# ===================== MailClient =====================

class MailClient:
    """Cache-first mail client. All reads from PostgreSQL cache; IMAP for sync + body fetch."""

    def __init__(self, user_email: str):
        self.user_email = user_email
        self.settings = get_user_settings(user_email)
        if self.settings is None:
            raise ValueError('Подешавања поште нису конфигурисана.')
        self.settings = validate_mail_server_settings(self.settings)
        try:
            self._password = _decrypt(self.settings['password'])
        except Exception:
            raise ValueError('Грешка при дешифровању лозинке. Поново сачувајте подешавања.')
        self.db = _get_db(user_email)

    def _imap(self):
        return _pool_get(self.user_email, self.settings, self._password)

    def _select_folder(self, M, folder, readonly=True):
        """SELECT folder on pool connection, skipping if already selected."""
        cur, cur_ro = _pool_selected(self.user_email)
        if cur == folder and (readonly or not cur_ro):
            return
        M.select(f'"{folder}"', readonly=readonly)
        _pool_set_selected(self.user_email, folder, readonly=readonly)

    def close(self):
        _pool_release(self.user_email)
        try:
            self.db.close()
        except Exception:
            pass

    # --- Ensure cache is warm ---

    def _ensure_synced(self, folder='INBOX'):
        """Warm the requested folder cache when it is empty or stale."""
        should_sync = _folder_sync_stale(self.db, self.user_email, folder)
        if should_sync:
            try:
                M = self._imap()
                sync_ok = do_sync(M, self.db, self.user_email, folder)
                if not sync_ok:
                    _pool_invalidate(self.user_email)
                    M = self._imap()
                    sync_ok = do_sync(M, self.db, self.user_email, folder)
                if sync_ok:
                    _pool_set_selected(self.user_email, folder)
                else:
                    logger.warning("Mail sync could not warm folder %s for %s", folder, self.user_email)
                    _pool_invalidate(self.user_email)
            except Exception as e:
                logger.warning(f"Initial mail sync failed: {e}")
                _pool_invalidate(self.user_email)
        ensure_bg_sync(self.user_email, self.settings, self._password)

    # --- Public API (all read from PostgreSQL cache) ---

    def list_folders(self):
        rows = self.db.execute(
            'SELECT name, unseen FROM mail_cache_folders WHERE user_email=%s ORDER BY name',
            (self.user_email,),
        ).fetchall()
        return [{'name': r['name'], 'unseen': r['unseen']} for r in rows]

    # Allowed sort columns to prevent SQL injection
    _SORT_COLUMNS = {
        'date': 'sort_date_iso',
        'sender': 'from_name',
        'subject': 'subject',
        'unread': 'is_read',
    }

    def list_messages(self, folder='INBOX', page=1, per_page=50, search=None,
                      sort_by='date', sort_dir='desc'):
        need_background_sync = _folder_sync_stale(self.db, self.user_email, folder)
        if not need_background_sync and not search:
            need_background_sync = _folder_has_more_history(self.db, self.user_email, folder)

        if need_background_sync:
            try:
                self.trigger_sync(folder)
            except Exception as e:
                logger.warning("Could not schedule background sync for %s: %s", folder, e)
        offset = (page - 1) * per_page
        col = self._SORT_COLUMNS.get(sort_by, 'uid')
        if col not in ('sort_date_iso', 'from_name', 'subject', 'is_read', 'uid'):
            col = 'uid'
        direction = 'ASC' if sort_dir == 'asc' else 'DESC'
        # Build ORDER BY from validated whitelist values only
        if sort_by == 'unread':
            order_clause = 'is_read ASC, uid DESC' if sort_dir == 'desc' else 'is_read DESC, uid DESC'
        else:
            order_clause = col + ' ' + direction

        base_select = 'SELECT uid, from_name, from_address, subject, date_iso, is_read FROM mail_cache_messages'
        base_where = ' WHERE user_email=%s AND folder=%s'
        search_filter = ' AND (subject ILIKE %s OR from_name ILIKE %s OR from_address ILIKE %s)'
        order_suffix = ' ORDER BY ' + order_clause + ' LIMIT %s OFFSET %s'

        if search:
            like = '%' + search + '%'
            rows = self.db.execute(
                base_select + base_where + search_filter + order_suffix,
                (self.user_email, folder, like, like, like, per_page, offset),
            ).fetchall()
            total = self.db.execute(
                'SELECT COUNT(*) AS message_count FROM mail_cache_messages' + base_where + search_filter,
                (self.user_email, folder, like, like, like),
            ).fetchone()
            total = _row_value(total, 'message_count', 0, default=0)
        else:
            rows = self.db.execute(
                base_select + base_where + order_suffix,
                (self.user_email, folder, per_page, offset),
            ).fetchall()
            total = self.db.execute(
                'SELECT COUNT(*) AS message_count FROM mail_cache_messages' + base_where,
                (self.user_email, folder),
            ).fetchone()
            total = _row_value(total, 'message_count', 0, default=0)

        messages = [{
            'uid': str(r['uid']),
            'from_name': r['from_name'],
            'from_address': r['from_address'],
            'subject': r['subject'],
            'date': r['date_iso'],
            'is_read': bool(r['is_read']),
        } for r in rows]

        pages = max(1, (total + per_page - 1) // per_page)
        return {'messages': messages, 'total': total, 'page': page, 'pages': pages}

    def get_init_data(self, folder='INBOX', page=1, per_page=50, search=None,
                      sort_by='date', sort_dir='desc'):
        """Return cached folders + messages with cache-first startup."""
        try:
            self.trigger_sync(folder)
        except Exception as e:
            logger.warning("Could not schedule initial sync for %s: %s", folder, e)
        ensure_bg_sync(self.user_email, self.settings, self._password)
        folders = self.list_folders()
        msgs = self.list_messages(
            folder=folder,
            page=page,
            per_page=per_page,
            search=search,
            sort_by=sort_by,
            sort_dir=sort_dir,
        )
        inbox_unread = 0
        for f in folders:
            if f['name'] == 'INBOX':
                inbox_unread = f['unseen']
                break
        return {
            'folders': folders,
            'inbox_unread': inbox_unread,
            **msgs,
        }

    def get_message(self, uid, folder='INBOX', mark_read=True):
        """Return message — from cache if body exists, else fetch from IMAP.
        Mark-read is done locally (instant) and queued for bg IMAP flush."""
        uid_int = int(uid)

        # Check local cache first
        row = self.db.execute(
            'SELECT * FROM mail_cache_messages WHERE user_email=%s AND folder=%s AND uid=%s',
            (self.user_email, folder, uid_int)
        ).fetchone()

        if row and row['has_body']:
            # Serve from local cache — instant
            if mark_read and not row['is_read']:
                _set_cached_read_state(self.db, self.user_email, folder, uid_int, True)
                # Queue mark-read for IMAP (bg worker will flush)
                self.db.execute(
                    '''
                    INSERT INTO mail_cache_pending_reads(user_email, folder, uid)
                    VALUES(%s, %s, %s)
                    ON CONFLICT (user_email, folder, uid) DO NOTHING
                    ''',
                    (self.user_email, folder, uid_int))
                self.db.commit()

            raw_html_body = row['html_body'] or ''
            sender_domain = _address_domain(row['from_address'])
            links = json.loads(row['links_json']) if row['links_json'] else []
            sanitized_html = raw_html_body
            if raw_html_body and not raw_html_body.lstrip().startswith('<!DOCTYPE html>'):
                sanitized_html, html_links = _sanitize_html_email(raw_html_body, sender_domain=sender_domain)
                links = _dedupe_links(links + html_links)
                self.db.execute(
                    '''
                    UPDATE mail_cache_messages
                    SET html_body=%s, links_json=%s
                    WHERE user_email=%s AND folder=%s AND uid=%s
                    ''',
                    (sanitized_html, json.dumps(links, ensure_ascii=False), self.user_email, folder, uid_int)
                )
                self.db.commit()
            if not links:
                links = _dedupe_links([
                    _analyze_link(url, sender_domain=sender_domain, label=url)
                    for url in _extract_urls_from_text(row['text_body'] or '')
                ])
                if links:
                    self.db.execute(
                        '''
                        UPDATE mail_cache_messages
                        SET links_json=%s
                        WHERE user_email=%s AND folder=%s AND uid=%s
                        ''',
                        (json.dumps(links, ensure_ascii=False), self.user_email, folder, uid_int)
                    )
                    self.db.commit()
            attachments = _annotate_attachments(
                json.loads(row['attachments_json']) if row['attachments_json'] else []
            )
            return {
                'uid': str(uid),
                'from_name': row['from_name'],
                'from_address': row['from_address'],
                'reply_to_name': row['reply_to_name'] or '',
                'reply_to_address': row['reply_to_address'] or '',
                'to': json.loads(row['to_json']) if row['to_json'] else [],
                'cc': json.loads(row['cc_json']) if row['cc_json'] else [],
                'subject': row['subject'],
                'date': row['date_iso'],
                'html_body': sanitized_html,
                'text_body': row['text_body'] or '',
                'attachments': attachments,
                'links': links,
                'security': _build_message_security(
                    row['from_address'],
                    row['reply_to_address'] or '',
                    links,
                    attachments,
                ),
            }

        # Not cached — fetch from IMAP
        M = self._imap()
        self._select_folder(M, folder, readonly=True)
        st, data = M.uid('fetch', str(uid).encode(), '(RFC822)')
        if st != 'OK' or not data or data[0] is None:
            return None

        raw = data[0][1] if isinstance(data[0], tuple) else data[0]
        parsed = _parse_message_body(raw)
        _store_body_in_cache(self.db, self.user_email, folder, uid_int, parsed)

        # Mark read locally + queue for bg flush (no IMAP roundtrip now)
        if mark_read:
            _set_cached_read_state(self.db, self.user_email, folder, uid_int, True)
            self.db.execute(
                '''
                INSERT INTO mail_cache_pending_reads(user_email, folder, uid)
                VALUES(%s, %s, %s)
                ON CONFLICT (user_email, folder, uid) DO NOTHING
                ''',
                (self.user_email, folder, uid_int))
            self.db.commit()

        return {
            'uid': str(uid),
            **parsed,
            'security': _build_message_security(
                parsed['from_address'],
                parsed['reply_to_address'],
                parsed['links'],
                parsed['attachments'],
            ),
        }

    def set_message_read_state(self, uid, folder='INBOX', is_read=True):
        uid_int = int(uid)
        changed = _set_cached_read_state(self.db, self.user_email, folder, uid_int, is_read)

        if is_read:
            self.db.execute(
                '''
                INSERT INTO mail_cache_pending_reads(user_email, folder, uid)
                VALUES(%s, %s, %s)
                ON CONFLICT (user_email, folder, uid) DO NOTHING
                ''',
                (self.user_email, folder, uid_int)
            )
            self.db.commit()
            return True

        self.db.execute(
            'DELETE FROM mail_cache_pending_reads WHERE user_email=%s AND folder=%s AND uid=%s',
            (self.user_email, folder, uid_int)
        )
        self.db.commit()

        M = self._imap()
        self._select_folder(M, folder, readonly=False)
        st, _ = M.uid('store', str(uid).encode(), '-FLAGS', '\\Seen')
        return st == 'OK' or changed

    def get_attachment(self, uid, att_index, folder='INBOX'):
        """Fetch a specific attachment by index. Returns (filename, content_type, data) or None."""
        M = self._imap()
        self._select_folder(M, folder, readonly=True)
        st, data = M.uid('fetch', str(uid).encode(), '(RFC822)')
        if st != 'OK' or not data or data[0] is None:
            return None

        raw = data[0][1] if isinstance(data[0], tuple) else data[0]
        msg = email.message_from_bytes(raw)

        idx = 0
        for part in msg.walk():
            cd = str(part.get('Content-Disposition', ''))
            if 'attachment' in cd:
                if idx == att_index:
                    filename = _decode_header_value(part.get_filename() or 'attachment')
                    ct = part.get_content_type()
                    payload = part.get_payload(decode=True) or b''
                    return filename, ct, payload
                idx += 1
        return None

    def get_all_attachments(self, uid, folder='INBOX'):
        """Fetch all attachments as a list of (filename, data) tuples."""
        M = self._imap()
        self._select_folder(M, folder, readonly=True)
        st, data = M.uid('fetch', str(uid).encode(), '(RFC822)')
        if st != 'OK' or not data or data[0] is None:
            return []

        raw = data[0][1] if isinstance(data[0], tuple) else data[0]
        msg = email.message_from_bytes(raw)

        results = []
        for part in msg.walk():
            cd = str(part.get('Content-Disposition', ''))
            if 'attachment' in cd:
                filename = _decode_header_value(part.get_filename() or 'attachment')
                payload = part.get_payload(decode=True) or b''
                results.append((filename, payload))
        return results

    def send_message(self, to, subject, body, cc='', attachments=None, **_kw):
        """Send an email. attachments is a list of dicts with keys:
        filename (str), content_type (str), data (bytes)."""
        s = validate_mail_server_settings(self.settings)
        has_attachments = attachments and len(attachments) > 0

        if has_attachments:
            msg = email.mime.multipart.MIMEMultipart('mixed')
            body_part = email.mime.multipart.MIMEMultipart('alternative')
            body_part.attach(email.mime.text.MIMEText(body, 'plain', 'utf-8'))
            html = f'<html><body><pre style="font-family:inherit;white-space:pre-wrap">{html_lib.escape(body)}</pre></body></html>'
            body_part.attach(email.mime.text.MIMEText(html, 'html', 'utf-8'))
            msg.attach(body_part)
            for att in attachments:
                maintype, _, subtype = (att.get('content_type') or 'application/octet-stream').partition('/')
                part = email.mime.base.MIMEBase(maintype, subtype or 'octet-stream')
                part.set_payload(att['data'])
                email.encoders.encode_base64(part)
                part.add_header('Content-Disposition', 'attachment',
                                filename=att.get('filename', 'attachment'))
                msg.attach(part)
        else:
            msg = email.mime.multipart.MIMEMultipart('alternative')
            msg.attach(email.mime.text.MIMEText(body, 'plain', 'utf-8'))
            html = f'<html><body><pre style="font-family:inherit;white-space:pre-wrap">{html_lib.escape(body)}</pre></body></html>'
            msg.attach(email.mime.text.MIMEText(html, 'html', 'utf-8'))

        msg['From'] = s['email_address']
        msg['To'] = to
        if cc:
            msg['Cc'] = cc
        msg['Subject'] = subject
        msg['Date'] = email.utils.formatdate(localtime=True)
        msg['Message-ID'] = email.utils.make_msgid()

        srv = None
        try:
            if s.get('smtp_starttls', True):
                srv = smtplib.SMTP(s['smtp_server'], int(s.get('smtp_port', 587)), timeout=15)
                srv.ehlo(); srv.starttls(); srv.ehlo()
            else:
                srv = smtplib.SMTP_SSL(s['smtp_server'], int(s.get('smtp_port', 465)), timeout=15)
            srv.login(s['email_address'], self._password)
            rcpt = [a.strip() for a in to.split(',')]
            if cc:
                rcpt += [a.strip() for a in cc.split(',')]
            msg_string = msg.as_string()
            srv.sendmail(s['email_address'], rcpt, msg_string)
        finally:
            if srv:
                try:
                    srv.quit()
                except Exception:
                    pass

        # Append to Sent folder via IMAP so the message appears in Sent Items
        try:
            M = self._imap()
            # Try common Sent folder names
            sent_folder = None
            for candidate in ('Sent', 'INBOX.Sent', 'Sent Messages', 'Sent Items',
                              '[Gmail]/Sent Mail', 'INBOX/Sent'):
                st, _ = M.select(f'"{candidate}"')
                if st == 'OK':
                    sent_folder = candidate
                    break
            _pool_set_selected(self.user_email, None)  # probing changed selection
            if sent_folder:
                M.append(f'"{sent_folder}"', '\\Seen',
                         imaplib.Time2Internaldate(time.time()),
                         msg_string.encode('utf-8'))
            else:
                logger.warning("Could not find Sent folder to save sent message")
        except Exception as e:
            logger.warning(f"Failed to save message to Sent folder: {e}")

        return True

    def delete_message(self, uid, folder='INBOX'):
        M = self._imap()
        self._select_folder(M, folder, readonly=False)
        _pool_set_selected(self.user_email, None)  # EXPUNGE invalidates state
        M.uid('store', str(uid).encode(), '+FLAGS', '\\Deleted')
        M.expunge()
        _remove_cached_message(self.db, self.user_email, folder, int(uid))
        return True

    def delete_message_async(self, uid, folder='INBOX'):
        """Remove from cache immediately, do IMAP delete in background thread."""
        _remove_cached_message(self.db, self.user_email, folder, int(uid))
        user_email = self.user_email
        settings = self.settings
        password = self._password

        def _bg_delete():
            conn = None
            try:
                conn = _connect_imap(settings, password)
                conn.select(f'"{folder}"', readonly=False)
                conn.uid('store', str(uid).encode(), '+FLAGS', '\\Deleted')
                conn.expunge()
            except Exception as e:
                logger.debug(f"Background IMAP delete error for uid {uid}: {e}")
            finally:
                if conn:
                    try:
                        conn.logout()
                    except Exception:
                        pass

        t = threading.Thread(target=_bg_delete, daemon=True)
        t.start()
        return True

    def move_message(self, uid, src_folder, dst_folder):
        M = self._imap()
        self._select_folder(M, src_folder, readonly=False)
        _pool_set_selected(self.user_email, None)  # state changes
        ub = str(uid).encode()
        st, _ = M.uid('copy', ub, f'"{dst_folder}"')
        if st == 'OK':
            M.uid('store', ub, '+FLAGS', '\\Deleted')
            M.expunge()
            _remove_cached_message(self.db, self.user_email, src_folder, int(uid))
            return True
        return False

    def unread_count(self, folder='INBOX'):
        row = self.db.execute(
            'SELECT unseen FROM mail_cache_folders WHERE user_email=%s AND name=%s',
            (self.user_email, folder),
        ).fetchone()
        return row['unseen'] if row else 0

    def trigger_sync(self, folder='INBOX'):
        """Non-blocking: kicks off sync in a background thread and returns immediately."""
        user_email = self.user_email
        settings = self.settings
        password = self._password
        sync_key = (user_email, folder)

        with _manual_sync_lock:
            existing = _manual_sync_jobs.get(sync_key)
            if existing and existing.is_alive():
                return
            _manual_sync_jobs[sync_key] = None

        def _do():
            conn = None
            db = None
            try:
                try:
                    conn = _connect_imap(settings, password)
                    db = _get_db(user_email)
                    do_sync(conn, db, user_email, folder)
                    _prefetch_bodies(conn, db, user_email, folder, limit=30)
                    _flush_pending_reads(conn, db, user_email)
                except Exception as e:
                    logger.warning(f"Manual sync error: {e}")
                finally:
                    if conn:
                        try:
                            conn.logout()
                        except Exception:
                            pass
                    if db:
                        try:
                            db.close()
                        except Exception:
                            pass
            finally:
                with _manual_sync_lock:
                    job = _manual_sync_jobs.get(sync_key)
                    if job is thread:
                        _manual_sync_jobs.pop(sync_key, None)

        thread = threading.Thread(target=_do, daemon=True)
        with _manual_sync_lock:
            _manual_sync_jobs[sync_key] = thread
        thread.start()


# ===================== Connection Tests =====================

def test_imap_connection(server, port, ssl, email_address, password, allowed_hosts=None, banned_hosts=None):
    try:
        server = ensure_mail_host_allowed(server, allowed_hosts=allowed_hosts, banned_hosts=banned_hosts)
        if ssl:
            M = imaplib.IMAP4_SSL(server, int(port), timeout=10)
        else:
            M = imaplib.IMAP4(server, int(port))
        M.login(email_address, password)
        M.logout()
        return {'success': True, 'message': 'IMAP веза успешна!'}
    except Exception as e:
        return {'success': False, 'message': f'IMAP грешка: {e}'}


def test_smtp_connection(server, port, starttls, email_address, password, allowed_hosts=None, banned_hosts=None):
    try:
        server = ensure_mail_host_allowed(server, allowed_hosts=allowed_hosts, banned_hosts=banned_hosts)
        if starttls:
            S = smtplib.SMTP(server, int(port), timeout=10)
            S.ehlo(); S.starttls(); S.ehlo()
        else:
            S = smtplib.SMTP_SSL(server, int(port), timeout=10)
        S.login(email_address, password)
        S.quit()
        return {'success': True, 'message': 'SMTP веза успешна!'}
    except Exception as e:
        return {'success': False, 'message': f'SMTP грешка: {e}'}
