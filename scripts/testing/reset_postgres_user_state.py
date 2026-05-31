#!/usr/bin/env python3
"""Reset a PostgreSQL-backed test user's password and first-login state."""

import os
import sys
from pathlib import Path

try:
    import psycopg
except ImportError as exc:  # pragma: no cover - defensive guard for local tooling
    raise SystemExit(f"psycopg is required: {exc}")

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from security_utils import PasswordHasher


def _load_dotenv(dotenv_path: Path) -> None:
    """Load .env entries while tolerating CRLF line endings."""
    if not dotenv_path.exists():
        return

    for raw_line in dotenv_path.read_text(encoding="utf-8", errors="ignore").splitlines():
        line = raw_line.strip().rstrip("\r")
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


def main() -> int:
    email = os.environ.get("TEST_RESET_EMAIL", "").strip()
    password = os.environ.get("TEST_RESET_PASSWORD", "")
    first_login_flag = os.environ.get("TEST_RESET_FIRST_LOGIN", "0").strip().lower()
    is_first_login = first_login_flag in {"1", "true", "yes"}

    if not email:
        print("TEST_RESET_EMAIL is required", file=sys.stderr)
        return 1

    _load_dotenv(REPO_ROOT / ".env")
    database_url = os.environ.get("DATABASE_URL", "").strip()
    if not database_url:
        print("DATABASE_URL is not configured", file=sys.stderr)
        return 1

    pg_url = database_url.replace("postgresql+psycopg://", "postgresql://")
    password_hash, salt = PasswordHasher().hash_password(password)

    with psycopg.connect(pg_url) as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                UPDATE users
                SET password_hash = %s,
                    salt = %s,
                    is_first_login = %s,
                    updated_at = NOW()
                WHERE LOWER(email) = LOWER(%s)
                """,
                (password_hash, salt, is_first_login, email),
            )
            updated_rows = cur.rowcount
        conn.commit()

    if updated_rows != 1:
        print(f"user not found or not updated: {email}", file=sys.stderr)
        return 1

    print(f"reset {email} first_login={is_first_login}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
