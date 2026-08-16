#!/usr/bin/env python3
"""Подиже тест базу МИС-а од нуле — шема + минимални сид подаци.

ЗАШТО ПОСТОЈИ
    До 16.08.2026. свита је пролазила само на dev машини, зато што је тест
    база тамо ручно попуњена пре ко зна колико. Ниједан фајл у репоу није
    описивао то стање, па је свака нова машина (кућни рачунар, нов сарадник,
    CI) ударала у ~19 падова типа „baza mora imati bar jednog korisnika".
    Ова скрипта чини свиту репродуцибилном било где.

ЗАШТО НЕ САМО МИГРАЦИЈЕ
    `deploy/run_migrations.py` НЕ уме да сагради базу од нуле — миграција
    001 претпоставља да табеле већ постоје и пада са
    „relation timesheet_reports does not exist". Миграције надограђују шему
    коју је првобитно направила апликација. Зато се основна шема учитава из
    tests/fixtures/schema_baseline.sql (снимак стварне шеме), а миграције
    се потом означе као примењене.

БЕЗБЕДНОСТ
    Ради ИСКЉУЧИВО над базом чије име се завршава на `_test`. Свака
    деструктивна радња тражи --execute; без њега је dry-run и само исписује
    шта би урадила.

УПОТРЕБА
    # погледај шта би се десило
    python scripts/seed_test_db.py

    # изгради од нуле (брише постојећу тест базу!)
    python scripts/seed_test_db.py --recreate --execute

    # само досеј подаци, шема остаје
    python scripts/seed_test_db.py --execute
"""
from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

SCHEMA_FIXTURE = REPO_ROOT / "tests" / "fixtures" / "schema_baseline.sql"
PODRAZUMEVANA_BAZA = "museum_system_test"

# Лозинка тест налога. Синтетичка, намерно у коду — ови налози постоје само
# у *_test бази која се брише и прави изнова. Мења се преко MIS_SEED_PASSWORD.
TEST_LOZINKA = os.environ.get("MIS_SEED_PASSWORD", "TestLozinka123!")

ROLE = [
    (1, "admin", "Пун приступ"),
    (2, "employee", "Запослени"),
    (3, "direktor", "Директор — паритет са админом"),
    (4, "sef_odeljenja", "Шеф одељења"),
]

ODELJENJA = [
    (1, "Одељење за минералогију"),
    (2, "Одељење за палеонтологију"),
]

# (id, email, пуно име, role_id, department_id, position)
KORISNICI = [
    (1, "admin@test.local", "Админ Тестовић", 1, None, "администратор система"),
    (2, "direktor@test.local", "Директор Тестовић", 3, None, "директор"),
    (3, "sef@test.local", "Шеф Тестовић", 4, 1, "шеф одељења"),
    (4, "kustos@test.local", "Кустос Тестовић", 2, 1, "кустос"),
    (5, "saradnik@test.local", "Сарадник Тестовић", 2, 2, "стручни сарадник"),
]

# (id, email, пуно име, position, department, is_department_head)
PROFILI = [
    (1, "sef@test.local", "Шеф Тестовић", "шеф одељења",
     "Одељење за минералогију", True),
    (2, "kustos@test.local", "Кустос Тестовић", "кустос",
     "Одељење за минералогију", False),
    (3, "saradnik@test.local", "Сарадник Тестовић", "стручни сарадник",
     "Одељење за палеонтологију", False),
]


def greska(poruka: str) -> int:
    print(f"ОДБИЈЕНО: {poruka}", file=sys.stderr)
    return 1


def ucitaj_dotenv(putanja: Path) -> None:
    if not putanja.is_file():
        return
    for red in putanja.read_text(encoding="utf-8").splitlines():
        red = red.strip()
        if not red or red.startswith("#") or "=" not in red:
            continue
        kljuc, vrednost = red.split("=", 1)
        os.environ.setdefault(kljuc.strip(), vrednost.strip().strip("'\""))


def pg_url(ime_baze: str) -> str:
    """URL ка датој бази, изведен из DATABASE_URL или из PG* променљивих."""
    sirovi = os.environ.get("DATABASE_URL", "").strip()
    if sirovi:
        osnov = sirovi.replace("postgresql+psycopg://", "postgresql://")
        # замени име базе на крају URL-а
        pre, _, _ = osnov.rpartition("/")
        return f"{pre}/{ime_baze}"
    korisnik = os.environ.get("PGUSER", os.environ.get("USER", "postgres"))
    host = os.environ.get("PGHOST", "localhost")
    port = os.environ.get("PGPORT", "5432")
    return f"postgresql://{korisnik}@{host}:{port}/{ime_baze}"


def pokreni_psql(url: str, *argumenti: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        ["psql", "-v", "ON_ERROR_STOP=1", "-q", url, *argumenti],
        capture_output=True, text=True,
    )


def napravi_bazu(ime: str, izvrsi: bool) -> int:
    admin_url = pg_url("postgres")
    if not izvrsi:
        print(f"  [dry-run] DROP DATABASE IF EXISTS {ime}; CREATE DATABASE {ime};")
        return 0
    for sql in (f'DROP DATABASE IF EXISTS "{ime}"', f'CREATE DATABASE "{ime}"'):
        rez = pokreni_psql(admin_url, "-c", sql)
        if rez.returncode != 0:
            return greska(f"{sql} → {rez.stderr.strip()}")
    print(f"  база {ime} направљена изнова")
    return 0


def ucitaj_semu(ime: str, izvrsi: bool) -> int:
    if not SCHEMA_FIXTURE.is_file():
        return greska(f"нема {SCHEMA_FIXTURE.relative_to(REPO_ROOT)}")
    if not izvrsi:
        print(f"  [dry-run] CREATE EXTENSION postgis; psql -f {SCHEMA_FIXTURE.name}")
        return 0
    url = pg_url(ime)
    rez = pokreni_psql(url, "-c", "CREATE EXTENSION IF NOT EXISTS postgis")
    if rez.returncode != 0:
        return greska(
            "PostGIS није доступан. Инсталирај пакет postgresql-postgis "
            f"(детаљ: {rez.stderr.strip()})"
        )
    rez = pokreni_psql(url, "-f", str(SCHEMA_FIXTURE))
    if rez.returncode != 0:
        return greska(f"учитавање шеме пало: {rez.stderr.strip()[:400]}")
    print(f"  шема учитана из {SCHEMA_FIXTURE.relative_to(REPO_ROOT)}")
    return 0


def zasej(ime: str, izvrsi: bool) -> int:
    import psycopg
    from security_utils import PasswordHasher

    if not izvrsi:
        print(f"  [dry-run] {len(ROLE)} ролa, {len(ODELJENJA)} одељења, "
              f"{len(KORISNICI)} корисника, {len(PROFILI)} профила")
        return 0

    hasher = PasswordHasher()
    lozinka_hash, salt = hasher.hash_password(TEST_LOZINKA)

    with psycopg.connect(pg_url(ime)) as veza:
        with veza.cursor() as kur:
            for rid, naziv, opis in ROLE:
                kur.execute(
                    "INSERT INTO roles (id, name, description) VALUES (%s, %s, %s) "
                    "ON CONFLICT (id) DO UPDATE SET name = EXCLUDED.name",
                    (rid, naziv, opis),
                )
            for did, naziv in ODELJENJA:
                kur.execute(
                    "INSERT INTO departments (id, name) VALUES (%s, %s) "
                    "ON CONFLICT (id) DO UPDATE SET name = EXCLUDED.name",
                    (did, naziv),
                )
            for uid, email, ime_p, rid, did, pozicija in KORISNICI:
                kur.execute(
                    """
                    INSERT INTO users (id, email, password_hash, salt, full_name,
                                       role_id, department_id, position,
                                       is_active, is_first_login)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, TRUE, FALSE)
                    ON CONFLICT (id) DO UPDATE SET
                        email = EXCLUDED.email,
                        password_hash = EXCLUDED.password_hash,
                        salt = EXCLUDED.salt,
                        full_name = EXCLUDED.full_name,
                        role_id = EXCLUDED.role_id,
                        department_id = EXCLUDED.department_id
                    """,
                    (uid, email, lozinka_hash, salt, ime_p, rid, did, pozicija),
                )
            for pid, email, ime_p, pozicija, odeljenje, sef in PROFILI:
                kur.execute(
                    """
                    INSERT INTO employee_profiles (id, email, full_name, position,
                                                   department, is_department_head)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    ON CONFLICT (id) DO UPDATE SET
                        email = EXCLUDED.email,
                        full_name = EXCLUDED.full_name,
                        is_department_head = EXCLUDED.is_department_head
                    """,
                    (pid, email, ime_p, pozicija, odeljenje, sef),
                )
            # секвенце да следећи INSERT не удари у постојеће id-јеве
            for tabela in ("roles", "departments", "users", "employee_profiles"):
                kur.execute(
                    f"SELECT setval(pg_get_serial_sequence('{tabela}', 'id'), "
                    f"COALESCE((SELECT MAX(id) FROM {tabela}), 1))"
                )
        veza.commit()

    print(f"  засејано: {len(KORISNICI)} корисника, {len(PROFILI)} профила "
          f"(лозинка свих: {TEST_LOZINKA})")
    return 0


def oznaci_migracije(ime: str, izvrsi: bool) -> int:
    """Означи све миграције као примењене (`baseline`).

    НАМЕРНО НИЈЕ ПОДРАЗУМЕВАНО. Три теста у test_revizija_operativa.py
    (`test_run_migrations_*`) траже да у бази ПОСТОЈИ бар нешто непримењено —
    њихов сопствени коментар каже „baza je već potpuno pending (uobičajeno za
    museum_system_test)". Ако се baseline пусти, `apply` враћа „Nothing to
    apply", заштитне провере се никад не активирају и та три теста падну.

    Дакле подразумевано стање тест базе је: шема из fixture-а + ПРАЗНА
    schema_migrations. Користи --baseline само ако ти треба база означена
    као потпуно мигрирана (нпр. за ручну проверу `apply` тока).
    """
    skripta = REPO_ROOT / "deploy" / "run_migrations.py"
    if not skripta.is_file():
        print("  (нема deploy/run_migrations.py — прескачем означавање)")
        return 0
    if not izvrsi:
        print("  [dry-run] run_migrations.py baseline --execute --database " + ime)
        return 0
    okruzenje = dict(os.environ, DATABASE_URL=pg_url(ime))
    rez = subprocess.run(
        [sys.executable, str(skripta), "baseline", "--execute", "--database", ime],
        capture_output=True, text=True, env=okruzenje, cwd=str(REPO_ROOT),
    )
    if rez.returncode != 0:
        print(f"  УПОЗОРЕЊЕ: baseline није прошао: {rez.stderr.strip()[:300]}")
        return 0
    print("  миграције означене као примењене")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Подиже МИС тест базу од нуле (шема + сид подаци).",
    )
    parser.add_argument("--database", default=PODRAZUMEVANA_BAZA,
                        help=f"име базе (подразумевано {PODRAZUMEVANA_BAZA})")
    parser.add_argument("--recreate", action="store_true",
                        help="обриши и направи базу изнова пре учитавања шеме")
    parser.add_argument("--execute", action="store_true",
                        help="стварно изврши; без овога је dry-run")
    parser.add_argument("--baseline", action="store_true",
                        help="означи миграције примењенима (обара 3 теста "
                             "у test_revizija_operativa.py — види docstring)")
    args = parser.parse_args()

    ucitaj_dotenv(REPO_ROOT / ".env")

    if not args.database.endswith("_test"):
        return greska(
            f"име базе „{args.database}” не завршава се на _test. "
            "Ова скрипта не сме да дира продукцијске ни дев базе."
        )

    print(f"База: {args.database}   режим: "
          f"{'ИЗВРШАВАЊЕ' if args.execute else 'dry-run'}")

    if args.recreate:
        if (kod := napravi_bazu(args.database, args.execute)):
            return kod
        if (kod := ucitaj_semu(args.database, args.execute)):
            return kod
        if args.baseline and (kod := oznaci_migracije(args.database, args.execute)):
            return kod

    if (kod := zasej(args.database, args.execute)):
        return kod

    if not args.execute:
        print("\nНишта није промењено. Додај --execute да се стварно изврши.")
    else:
        print("\nГотово. Свита се сад покреће са: pytest test_*.py -q")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
