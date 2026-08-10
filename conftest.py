"""Заштите на нивоу целе pytest сесије (ревизија 2026-08, батч 3).

1) База: свита СМЕ да ради само над базом чије име се завршава на ``_test``.
   Ако DATABASE_URL није постављен, поставља се безбедан default
   (MIS_TEST_DB_URL или museum_system_test) ПРЕ него што иједан тест модул
   увезе ``app`` — ``load_dotenv()`` не прегазује већ постављен env, па
   ``.env`` (museum_system!) не може да процури у тестове. Ако је
   DATABASE_URL експлицитно постављен на не-``_test`` базу, колекција се
   ПРЕКИДА (уопштен образац из test_monthly_report_integration.py).

2) Assert-и: тест фајл без иједног ``assert``/``pytest.raises`` пролази
   „зелено" шта год да се деси (образац record_pass/record_fail) — таква
   датотека ОБАРА колекцију.
"""

import os
import re
from pathlib import Path

import pytest

_DEFAULT_TEST_DB_URL = (
    'postgresql+psycopg://aleksandarlukovic@localhost:5432/museum_system_test'
)

if not os.environ.get('DATABASE_URL'):
    os.environ['DATABASE_URL'] = os.environ.get(
        'MIS_TEST_DB_URL', _DEFAULT_TEST_DB_URL)


def _db_name(url):
    return url.rstrip('/').rsplit('/', 1)[-1].split('?')[0]


def pytest_configure(config):
    name = _db_name(os.environ.get('DATABASE_URL', ''))
    if not name.endswith('_test'):
        pytest.exit(
            f'DATABASE_URL показује на базу „{name}" која се НЕ завршава на '
            '„_test" — свита ради искључиво над тест базом (нпр. '
            'museum_system_test) да никад не дира продукцијске/дев податке. '
            'Постави DATABASE_URL/MIS_TEST_DB_URL на *_test базу.',
            returncode=4,
        )


_ASSERT_RE = re.compile(r'assert|pytest\.raises')

# Чувар „фајл без assert-а" важи САМО над стварном свитом — легаси стабла
# (стари бекапи, one-off скрипте) нису наши тестови и не смеју да обарају
# колекцију кад их неко експлицитно наведе на командној линији.
_ROOT = Path(__file__).resolve().parent
_LEGACY_DIRS = {
    'PrirodnjackiMuzej', 'localSQLtesting', 'backups',
    'venv', '.venv', 'node_modules',
}


def _u_sviti(path):
    try:
        rel = path.resolve().relative_to(_ROOT)
    except ValueError:
        return False
    return not (set(rel.parts[:-1]) & _LEGACY_DIRS)


def pytest_collection_modifyitems(config, items):
    proveren, bez_asserta = set(), []
    for item in items:
        path = Path(str(getattr(item, 'path', None) or item.fspath))
        if path.suffix != '.py' or path in proveren or not _u_sviti(path):
            continue
        proveren.add(path)
        if not _ASSERT_RE.search(path.read_text(encoding='utf-8', errors='replace')):
            bez_asserta.append(str(path))
    if bez_asserta:
        raise pytest.UsageError(
            'Тест фајл(ови) без иједног assert/pytest.raises — такви тестови '
            'пролазе без обзира на исход. Додај стварне assert-е:\n'
            + '\n'.join(sorted(bez_asserta)))
