#!/usr/bin/env python3
"""
Museum Employee Chat Room backed by PostgreSQL.

Features:
- Group chat (channel='general')
- Direct messages (channel='dm:<low_id>:<high_id>')
- User status: online / busy / offline
- File attachments stored in data/chat_files/
- Unread cursor tracking per user+channel
"""

import threading
import time
from datetime import datetime, timezone
from pathlib import Path

from psycopg.rows import dict_row

from postgres_service import get_postgres_connection

DATA_DIR = Path(__file__).parent / 'data'
CHAT_FILES_DIR = DATA_DIR / 'chat_files'

_SCHEMA_SQL = '''
CREATE TABLE IF NOT EXISTS chat_messages (
    id BIGSERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    user_name TEXT NOT NULL,
    user_email CITEXT NOT NULL,
    user_department TEXT DEFAULT '',
    channel TEXT NOT NULL DEFAULT 'general',
    message TEXT NOT NULL DEFAULT '',
    file_name TEXT,
    file_path TEXT,
    file_size BIGINT,
    file_type TEXT,
    timestamp TEXT NOT NULL,
    ts_epoch DOUBLE PRECISION NOT NULL
);
CREATE INDEX IF NOT EXISTS chat_messages_channel_idx ON chat_messages(channel, ts_epoch DESC);
CREATE INDEX IF NOT EXISTS chat_messages_user_idx ON chat_messages(user_id, channel, ts_epoch DESC);

CREATE TABLE IF NOT EXISTS chat_presence (
    user_id INTEGER PRIMARY KEY,
    user_name TEXT NOT NULL,
    user_email CITEXT NOT NULL,
    user_department TEXT DEFAULT '',
    status TEXT NOT NULL DEFAULT 'online',
    last_seen DOUBLE PRECISION NOT NULL
);

CREATE TABLE IF NOT EXISTS chat_unread_cursors (
    user_id INTEGER NOT NULL,
    channel TEXT NOT NULL,
    last_read_epoch DOUBLE PRECISION NOT NULL DEFAULT 0,
    PRIMARY KEY (user_id, channel)
);
'''

_schema_ready = False
_schema_lock = threading.Lock()


def _get_db():
    global _schema_ready

    DATA_DIR.mkdir(parents=True, exist_ok=True)
    CHAT_FILES_DIR.mkdir(parents=True, exist_ok=True)
    db = get_postgres_connection(row_factory=dict_row)
    try:
        with _schema_lock:
            if not _schema_ready:
                db.execute(_SCHEMA_SQL)
                db.commit()
                _schema_ready = True
    except Exception:
        db.close()
        raise
    return db


VALID_STATUSES = {'online', 'busy', 'offline'}


def touch_presence(user_id: int, user_name: str, user_email: str,
                   department: str = '', status: str = None):
    """Update user's last-seen timestamp. Only overwrites status when explicitly passed."""
    now = time.time()
    with _get_db() as db:
        if status and status in VALID_STATUSES:
            db.execute(
                '''
                INSERT INTO chat_presence(user_id, user_name, user_email, user_department, status, last_seen)
                VALUES(%s, %s, %s, %s, %s, %s)
                ON CONFLICT(user_id) DO UPDATE SET
                    user_name = EXCLUDED.user_name,
                    user_email = EXCLUDED.user_email,
                    user_department = EXCLUDED.user_department,
                    status = EXCLUDED.status,
                    last_seen = EXCLUDED.last_seen
                ''',
                (user_id, user_name, user_email, department, status, now),
            )
        else:
            db.execute(
                '''
                INSERT INTO chat_presence(user_id, user_name, user_email, user_department, status, last_seen)
                VALUES(%s, %s, %s, %s, 'online', %s)
                ON CONFLICT(user_id) DO UPDATE SET
                    user_name = EXCLUDED.user_name,
                    user_email = EXCLUDED.user_email,
                    user_department = EXCLUDED.user_department,
                    last_seen = EXCLUDED.last_seen
                ''',
                (user_id, user_name, user_email, department, now),
            )


def set_user_status(user_id: int, status: str):
    """Explicitly set user status ('online', 'busy', 'offline')."""
    if status not in VALID_STATUSES:
        return
    with _get_db() as db:
        db.execute('UPDATE chat_presence SET status=%s WHERE user_id=%s', (status, user_id))


def clear_presence(user_id: int):
    """Remove user from presence table (called on logout or page leave)."""
    with _get_db() as db:
        db.execute('DELETE FROM chat_presence WHERE user_id=%s', (user_id,))


def get_online_users(threshold_seconds: int = 15) -> list:
    """Return users active in the last N seconds with status field."""
    cutoff = time.time() - threshold_seconds
    with _get_db() as db:
        rows = db.execute(
            '''
            SELECT user_id, user_name, user_department, status
            FROM chat_presence
            WHERE last_seen > %s
            ORDER BY user_name
            ''',
            (cutoff,),
        ).fetchall()
    return [{
        'user_id': r['user_id'],
        'name': r['user_name'],
        'department': r['user_department'],
        'status': r['status'],
    } for r in rows]


def get_attachment_channel(stored_name: str):
    """Kanal poruke kojoj prilog pripada, ili None ako ga nijedna poruka ne
    referencira. Osnova za proveru pristupa pri preuzimanju (krug 4, stavka 7):
    UUID ime fajla nije tajna, pa pristup mora da prati učešće u razgovoru."""
    with _get_db() as db:
        row = db.execute(
            'SELECT channel FROM chat_messages WHERE file_path = %s '
            'ORDER BY id LIMIT 1',
            (stored_name,),
        ).fetchone()
    return row['channel'] if row else None


def user_in_channel(user_id: int, channel: str) -> bool:
    """Da li korisnik učestvuje u kanalu: 'general' je otvoren svim
    prijavljenim, dm:<a>:<b> samo dvojici učesnika."""
    if not channel.startswith('dm:'):
        return True
    parts = channel.split(':')
    return len(parts) == 3 and str(user_id) in (parts[1], parts[2])


def make_dm_channel(user_id_a: int, user_id_b: int) -> str:
    """Return canonical DM channel name: dm:<low>:<high>."""
    low, high = sorted([int(user_id_a), int(user_id_b)])
    return f'dm:{low}:{high}'


def get_user_channels(user_id: int) -> list:
    """Return conversation list with unread counts and last message preview."""
    uid = int(user_id)
    dm_prefix_a = f'dm:{uid}:%'
    dm_prefix_b = f'dm:%:{uid}'
    channels = []
    with _get_db() as db:
        rows = db.execute(
            '''
            SELECT DISTINCT channel
            FROM chat_messages
            WHERE channel = 'general'
               OR channel LIKE %s
               OR channel LIKE %s
            ORDER BY channel
            ''',
            (dm_prefix_a, dm_prefix_b),
        ).fetchall()

        for row in rows:
            ch = row['channel']
            if ch.startswith('dm:'):
                parts = ch.split(':')
                if len(parts) == 3 and uid not in (int(parts[1]), int(parts[2])):
                    continue

            last_msg = db.execute(
                '''
                SELECT user_name, message, file_name, ts_epoch
                FROM chat_messages
                WHERE channel=%s
                ORDER BY ts_epoch DESC
                LIMIT 1
                ''',
                (ch,),
            ).fetchone()

            cursor_row = db.execute(
                '''
                SELECT last_read_epoch
                FROM chat_unread_cursors
                WHERE user_id=%s AND channel=%s
                ''',
                (uid, ch),
            ).fetchone()
            last_read = cursor_row['last_read_epoch'] if cursor_row else 0

            unread = db.execute(
                '''
                SELECT COUNT(*) AS cnt
                FROM chat_messages
                WHERE channel=%s AND ts_epoch > %s AND user_id != %s
                ''',
                (ch, last_read, uid),
            ).fetchone()['cnt']

            other_name = ''
            other_id = 0
            other_dept = ''
            if ch.startswith('dm:'):
                parts = ch.split(':')
                other_uid = int(parts[1]) if int(parts[2]) == uid else int(parts[2])
                other_id = other_uid
                other_row = db.execute(
                    '''
                    SELECT user_name, user_department
                    FROM chat_presence
                    WHERE user_id=%s
                    ''',
                    (other_uid,),
                ).fetchone()
                if other_row:
                    other_name = other_row['user_name']
                    other_dept = other_row['user_department'] or ''
                else:
                    msg_row = db.execute(
                        '''
                        SELECT user_name
                        FROM chat_messages
                        WHERE channel=%s AND user_id=%s
                        ORDER BY ts_epoch DESC
                        LIMIT 1
                        ''',
                        (ch, other_uid),
                    ).fetchone()
                    other_name = msg_row['user_name'] if msg_row else f'Корисник #{other_uid}'

            preview = ''
            last_epoch = 0
            last_sender = ''
            if last_msg:
                last_epoch = last_msg['ts_epoch']
                last_sender = last_msg['user_name']
                if last_msg['file_name']:
                    preview = f"📎 {last_msg['file_name']}"
                else:
                    preview = (last_msg['message'] or '')[:60]

            channels.append({
                'id': ch,
                'type': 'dm' if ch.startswith('dm:') else 'group',
                'name': other_name if ch.startswith('dm:') else 'Општи чат',
                'other_id': other_id,
                'other_dept': other_dept,
                'unread': unread,
                'last_epoch': last_epoch,
                'last_sender': last_sender,
                'preview': preview,
            })

    channels.sort(key=lambda c: (0 if c['id'] == 'general' else 1, -c['last_epoch']))
    if not any(c['id'] == 'general' for c in channels):
        channels.insert(0, {
            'id': 'general',
            'type': 'group',
            'name': 'Општи чат',
            'other_id': 0,
            'other_dept': '',
            'unread': 0,
            'last_epoch': 0,
            'last_sender': '',
            'preview': '',
        })
    return channels


def mark_channel_read(user_id: int, channel: str, up_to_epoch: float = None):
    """Mark a channel as read up to the given epoch (defaults to now)."""
    now = time.time() if up_to_epoch is None else up_to_epoch
    with _get_db() as db:
        db.execute(
            '''
            INSERT INTO chat_unread_cursors(user_id, channel, last_read_epoch)
            VALUES(%s, %s, %s)
            ON CONFLICT(user_id, channel) DO UPDATE SET last_read_epoch = EXCLUDED.last_read_epoch
            ''',
            (user_id, channel, now),
        )


def send_message(user_id: int, user_name: str, user_email: str, department: str,
                 message: str = '', channel: str = 'general',
                 file_name: str = None, file_path: str = None,
                 file_size: int = None, file_type: str = None) -> dict:
    """Store a chat message (text and/or file). Returns the saved message dict."""
    now = time.time()
    ts_iso = datetime.now(timezone.utc).isoformat()
    with _get_db() as db:
        msg_id = db.execute(
            '''
            INSERT INTO chat_messages(
                user_id, user_name, user_email, user_department,
                channel, message, file_name, file_path, file_size, file_type,
                timestamp, ts_epoch
            )
            VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING id
            ''',
            (
                user_id, user_name, user_email, department,
                channel, (message or '').strip(), file_name, file_path, file_size, file_type,
                ts_iso, now,
            ),
        ).fetchone()['id']
    return {
        'id': msg_id,
        'user_id': user_id,
        'user_name': user_name,
        'department': department,
        'channel': channel,
        'message': (message or '').strip(),
        'file_name': file_name,
        'file_path': file_path,
        'file_size': file_size,
        'file_type': file_type,
        'timestamp': ts_iso,
        'ts_epoch': now,
    }


def get_messages(since_epoch: float = 0, limit: int = 100, channel: str = 'general') -> list:
    """Get messages for a channel, newer than since_epoch. Returns oldest-first."""
    with _get_db() as db:
        if since_epoch > 0:
            rows = db.execute(
                '''
                SELECT *
                FROM chat_messages
                WHERE channel=%s AND ts_epoch > %s
                ORDER BY ts_epoch ASC
                LIMIT %s
                ''',
                (channel, since_epoch, limit),
            ).fetchall()
        else:
            rows = db.execute(
                '''
                SELECT *
                FROM (
                    SELECT *
                    FROM chat_messages
                    WHERE channel=%s
                    ORDER BY ts_epoch DESC
                    LIMIT %s
                ) recent
                ORDER BY ts_epoch ASC
                ''',
                (channel, limit),
            ).fetchall()
    return [{
        'id': r['id'],
        'user_id': r['user_id'],
        'user_name': r['user_name'],
        'department': r['user_department'],
        'channel': r['channel'],
        'message': r['message'],
        'file_name': r['file_name'],
        'file_path': r['file_path'],
        'file_size': r['file_size'],
        'file_type': r['file_type'],
        'timestamp': r['timestamp'],
        'ts_epoch': r['ts_epoch'],
    } for r in rows]
