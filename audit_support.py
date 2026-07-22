"""Globalni audit trag — helper koji upisuje red u ``audit_log`` (ZADATAK #4).

Modelovano po ``timesheet_audit_log`` (migration/004), ali app-level i
generalizovano na (entity_type, entity_id). Piše se iz Python koda jer:

  * događaji obuhvataju više tabela I JSON skladišta (heterogeno);
  * identitet aktera je u Flask sesiji — DB trigger ga ne vidi.

``record_audit`` je **best-effort posmatrač**:

  * zove se TEK POŠTO je primarna akcija uspela (nema lažnih zapisa);
  * NIKAD ne diže izuzetak ka pozivaocu — otkaz audita se loguje na ERROR
    (da znamo da trag ima rupu), ali ne sme da sruši ni da rollback-uje
    korisnikovu akciju;
  * automatski hvata aktera (sesija), IP i user-agent iz zahteva.

Piše u zasebnoj (kratkoj) transakciji, nezavisnoj od transakcije primarne
akcije — zato ga treba zvati posle uspešnog commit-a.
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


def record_audit(
    *,
    action: str,
    entity_type: str,
    entity_id: Any = None,
    summary: Optional[str] = None,
    old_values: Optional[dict] = None,
    new_values: Optional[dict] = None,
    changed_by: Optional[str] = None,
    get_postgres_connection=None,
) -> bool:
    """Upiši jedan audit red. Best-effort: na grešku loguje ERROR, ne diže izuzetak.

    Parametri:
        action:        tip akcije (koristi ACTION_* konstante).
        entity_type:   tip entiteta ('mineral', 'user', 'module_access', ...).
        entity_id:     id pogođenog zapisa (biće pretvoren u tekst); NULL ako nema.
        summary:       čitljiv opis akcije.
        old_values:    prethodno stanje (za UPDATE/DELETE) — dict ili None.
        new_values:    novo stanje (za CREATE/UPDATE) — dict ili None.
        changed_by:    email aktera; ako je None, uzima se iz sesije.
    """
    resolved_by = None
    try:
        import psycopg
        if get_postgres_connection is None:
            from postgres_service import get_postgres_connection as gpc
            get_postgres_connection = gpc

        resolved_by = _acting_user(changed_by)
        record_id, record_ref = _split_entity_id(entity_id)
        old_json = psycopg.types.json.Json(old_values, dumps=_safe_dumps) if old_values is not None else None
        new_json = psycopg.types.json.Json(new_values, dumps=_safe_dumps) if new_values is not None else None

        with get_postgres_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO audit_log (
                        table_name, record_id, record_ref, action, changed_by,
                        old_values, new_values, change_summary,
                        ip_address, user_agent
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """,
                    (
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
                    ),
                )
        return True
    except Exception as exc:
        logger.error(
            "AUDIT WRITE FAILED action=%s entity=%s/%s by=%s: %s",
            action, entity_type, entity_id, resolved_by, exc,
        )
        return False
