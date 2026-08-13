"""Globalni audit trag — helper koji upisuje red u ``audit_log`` (ZADATAK #4).

Modelovano po ``timesheet_audit_log`` (migration/004), ali app-level i
generalizovano na (entity_type, entity_id). Piše se iz Python koda jer:

  * događaji obuhvataju više tabela I JSON skladišta (heterogeno);
  * identitet aktera je u Flask sesiji — DB trigger ga ne vidi.

``record_audit`` ima dva režima (revizija 2026-08, batch 6, stavka 4):

  * **Sa ``cursor=``** — upis ide kroz PROSLEĐENI kursor, tj. u ISTOJ
    transakciji kao poslovna promena. Greška audita se PROPAGIRA i obara
    celu transakciju: promena bez traga ne može da se commit-uje. Ovo je
    kanonski režim za DB entitete — zvati PRE commit-a.
  * **Bez kursora** — zatečeni best-effort posmatrač: zove se posle
    commit-a, piše u zasebnoj kratkoj transakciji, NIKAD ne diže izuzetak
    (otkaz se loguje na ERROR). Ostaje za pozivaoce kod kojih dostupnost
    pobeđuje potpunost traga.

Za FAJLSKE radnje (nema DB transakcije koja bi ih pokrila) postoji outbox
protokol nad tabelom ``audit_outbox`` (migration/046):

  1. ``record_audit_intent(...)`` upiše nameru PRE fajlske radnje i DIŽE
     izuzetak ako upis ne uspe — radnja bez traga se ne izvršava;
  2. posle radnje ``confirm_audit_intent(id, success=...)`` označi ishod;
  3. ``flush_audit_outbox()`` prelije potvrđene redove u ``audit_log``
     (idempotentno, SKIP LOCKED); PENDING stariji od sat vremena (proces
     pao između koraka) prelivaju se sa markerom neразрешеног ishoda.

Automatski se hvataju akter (sesija), IP i user-agent iz zahteva.
"""

import ipaddress
import json
import logging
from typing import Any, Optional

logger = logging.getLogger(__name__)


# Konstante akcija (nisu enforce-ovane u bazi; drže se ovde radi doslednosti).
ACTION_DELETE = 'DELETE'
ACTION_CREATE = 'CREATE'
ACTION_UPDATE = 'UPDATE'
ACTION_PERMISSION_GRANT = 'PERMISSION_GRANT'
ACTION_PERMISSION_REVOKE = 'PERMISSION_REVOKE'
ACTION_USER_CREATE = 'USER_CREATE'
ACTION_USER_UPDATE = 'USER_UPDATE'
ACTION_USER_DELETE = 'USER_DELETE'
ACTION_USER_ROLE_CHANGE = 'USER_ROLE_CHANGE'


def _safe_dumps(value: Any) -> str:
    """JSON serijalizacija otporna na datetime/Decimal/date (kao SQL to_jsonb)."""
    return json.dumps(value, default=str, ensure_ascii=False)


def _acting_user(explicit: Optional[str]) -> str:
    if explicit:
        return explicit
    try:
        from flask import session
        return (
            session.get('user_email')
            or (session.get('user') or {}).get('email')
            or 'system'
        )
    except Exception:
        return 'system'


def _client_ip() -> Optional[str]:
    """Vrati validan IP (INET kolona) ili None — 'unknown'/nevalidno → None."""
    try:
        from security_utils import get_client_ip
        raw = get_client_ip()
        ipaddress.ip_address(raw)  # baci ako nije validan IPv4/IPv6
        return raw
    except Exception:
        return None


def _split_entity_id(entity_id: Any):
    """Razdvoji id na (record_id BIGINT ili None, record_ref TEXT ili None)."""
    if entity_id is None:
        return None, None
    ref = str(entity_id)
    if isinstance(entity_id, bool):
        return None, ref
    if isinstance(entity_id, int):
        return entity_id, ref
    if ref.lstrip('-').isdigit():
        try:
            return int(ref), ref
        except (ValueError, OverflowError):
            return None, ref
    return None, ref


def _user_agent() -> Optional[str]:
    try:
        from flask import request
        return request.headers.get('User-Agent')
    except Exception:
        return None


_INSERT_AUDIT_SQL = """
    INSERT INTO audit_log (
        table_name, record_id, record_ref, action, changed_by,
        old_values, new_values, change_summary,
        ip_address, user_agent
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
"""


def _row_params(action, entity_type, entity_id, summary,
                old_values, new_values, changed_by):
    import psycopg
    resolved_by = _acting_user(changed_by)
    record_id, record_ref = _split_entity_id(entity_id)
    old_json = psycopg.types.json.Json(old_values, dumps=_safe_dumps) if old_values is not None else None
    new_json = psycopg.types.json.Json(new_values, dumps=_safe_dumps) if new_values is not None else None
    return resolved_by, (
        entity_type,
        record_id,
        record_ref,
        action,
        resolved_by,
        old_json,
        new_json,
        summary,
        _client_ip(),
        _user_agent(),
    )


def record_audit(
    *,
    action: str,
    entity_type: str,
    entity_id: Any = None,
    summary: Optional[str] = None,
    old_values: Optional[dict] = None,
    new_values: Optional[dict] = None,
    changed_by: Optional[str] = None,
    cursor=None,
    get_postgres_connection=None,
) -> bool:
    """Upiši jedan audit red.

    Sa ``cursor=``: upis ide kroz prosleđeni kursor — ISTA transakcija kao
    poslovna promena, greška se PROPAGIRA (promena bez traga se ne commit-uje).
    Bez kursora: best-effort — na grešku loguje ERROR i vraća False.

    Parametri:
        action:        tip akcije (koristi ACTION_* konstante).
        entity_type:   tip entiteta ('mineral', 'user', 'module_access', ...).
        entity_id:     id pogođenog zapisa (biće pretvoren u tekst); NULL ako nema.
        summary:       čitljiv opis akcije.
        old_values:    prethodno stanje (za UPDATE/DELETE) — dict ili None.
        new_values:    novo stanje (za CREATE/UPDATE) — dict ili None.
        changed_by:    email aktera; ako je None, uzima se iz sesije.
        cursor:        otvoren kursor transakcije poslovne promene.
    """
    if cursor is not None:
        _, params = _row_params(action, entity_type, entity_id, summary,
                                old_values, new_values, changed_by)
        cursor.execute(_INSERT_AUDIT_SQL, params)
        return True

    resolved_by = None
    try:
        if get_postgres_connection is None:
            from postgres_service import get_postgres_connection as gpc
            get_postgres_connection = gpc

        resolved_by, params = _row_params(action, entity_type, entity_id, summary,
                                          old_values, new_values, changed_by)
        with get_postgres_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(_INSERT_AUDIT_SQL, params)
        return True
    except Exception as exc:
        logger.error(
            "AUDIT WRITE FAILED action=%s entity=%s/%s by=%s: %s",
            action, entity_type, entity_id, resolved_by, exc,
        )
        return False


# ---------------------------------------------------------------------------
# Outbox protokol za fajlske radnje (migration/046)
# ---------------------------------------------------------------------------

def record_audit_intent(
    *,
    action: str,
    entity_type: str,
    entity_id: Any = None,
    summary: Optional[str] = None,
    old_values: Optional[dict] = None,
    new_values: Optional[dict] = None,
    changed_by: Optional[str] = None,
    get_postgres_connection=None,
) -> int:
    """Upiši NAMERU fajlske radnje u audit_outbox, PRE izvršenja radnje.

    Diže izuzetak ako upis ne uspe — fajlska radnja bez traga se ne izvršava.
    Vraća id outbox reda (za confirm_audit_intent).
    """
    if get_postgres_connection is None:
        from postgres_service import get_postgres_connection as gpc
        get_postgres_connection = gpc
    _, params = _row_params(action, entity_type, entity_id, summary,
                            old_values, new_values, changed_by)
    with get_postgres_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO audit_outbox (
                    table_name, record_id, record_ref, action, changed_by,
                    old_values, new_values, change_summary,
                    ip_address, user_agent
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING id
                """,
                params,
            )
            return cur.fetchone()[0]


def confirm_audit_intent(outbox_id: int, *, success: bool,
                         get_postgres_connection=None) -> None:
    """Označi ishod fajlske radnje za raniju nameru (best-effort).

    Uspeh → CONFIRMED (flush je prenosi u audit_log); neuspeh → ABORTED
    (flush je briše — radnja se nije desila, lažan trag ne sme da nastane).
    """
    try:
        if get_postgres_connection is None:
            from postgres_service import get_postgres_connection as gpc
            get_postgres_connection = gpc
        with get_postgres_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "UPDATE audit_outbox SET status = %s WHERE id = %s",
                    ('CONFIRMED' if success else 'ABORTED', outbox_id),
                )
    except Exception as exc:
        logger.error("AUDIT OUTBOX CONFIRM FAILED id=%s: %s", outbox_id, exc)


def flush_audit_outbox(get_postgres_connection=None, limit: int = 200) -> int:
    """Prelij dozrele outbox redove u audit_log (idempotentno, best-effort).

    Prelivaju se CONFIRMED redovi i PENDING stariji od sat vremena (proces
    pao između namere i potvrde — trag se čuva uz marker neразрешеног
    ishoda); ABORTED se brišu. Vraća broj prelivenih redova.
    """
    try:
        if get_postgres_connection is None:
            from postgres_service import get_postgres_connection as gpc
            get_postgres_connection = gpc
        with get_postgres_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("DELETE FROM audit_outbox WHERE status = 'ABORTED'")
                cur.execute(
                    """
                    WITH ready AS (
                        SELECT id FROM audit_outbox
                        WHERE flushed_at IS NULL
                          AND (status = 'CONFIRMED'
                               OR (status = 'PENDING'
                                   AND created_at < now() - interval '1 hour'))
                        ORDER BY id
                        LIMIT %s
                        FOR UPDATE SKIP LOCKED
                    ), ins AS (
                        INSERT INTO audit_log (
                            table_name, record_id, record_ref, action, changed_by,
                            old_values, new_values, change_summary,
                            ip_address, user_agent
                        )
                        SELECT o.table_name, o.record_id, o.record_ref, o.action,
                               o.changed_by, o.old_values, o.new_values,
                               CASE WHEN o.status = 'PENDING'
                                    THEN COALESCE(o.change_summary, '') || ' [исход непотврђен]'
                                    ELSE o.change_summary END,
                               o.ip_address, o.user_agent
                        FROM audit_outbox o
                        JOIN ready r ON r.id = o.id
                    )
                    UPDATE audit_outbox SET flushed_at = now()
                    WHERE id IN (SELECT id FROM ready)
                    """,
                    (limit,),
                )
                return cur.rowcount
    except Exception as exc:
        logger.error("AUDIT OUTBOX FLUSH FAILED: %s", exc)
        return 0
