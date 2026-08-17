"""Прекидачи одобравања — раде ли месечни извештаји и документи кроз потписе.

ЗАШТО ПОСТОЈИ
    Ланац одобравања претпоставља да шефови одељења и директор редовно
    потписују. Кад то изостане, извештаји запослених остају заглављени у
    SUBMITTED, а документи у `na_odobrenju` — посао стоји због туђе инерције.
    Ова два прекидача гасе захтев за потписом, свако за свој ток.

ШТА ГАШЕЊЕ НЕ РАДИ
    НЕ проглашава ништа одобреним. Извештај послат док је прекидач угашен
    добија статус `BEZ_ODOBRENJA` (документ `bez_odobrenja`), поља за потписе
    остају празна, а приказ каже „Без одобравања" — никад „Одобрено".
    Разлика мора да остане видљива и годинама касније: извештај који нико
    није потписао не сме да личи на потписан.

ПОДРАЗУМЕВАНО ЈЕ УКЉУЧЕНО
    Изостанак подешавања, недоступна база, покварен JSON — све води у
    УКЉУЧЕНО. Одобравање се гаси само изричитом одлуком, никад грешком.

РЕДОСЛЕД ПРВЕНСТВА
    1. променљива окружења (`MIS_ODOBRAVANJE_IZVESTAJA` / `..._DOKUMENATA`)
       — излаз у нужди кад админ страница не ради;
    2. `system_settings` у бази, које админ панел уређује без рестарта;
    3. подразумевано УКЉУЧЕНО.
"""
from __future__ import annotations

import logging
import os

logger = logging.getLogger(__name__)

KLJUC_IZVESTAJI = "odobravanje_izvestaja"
KLJUC_DOKUMENTI = "odobravanje_dokumenata"

ENV_IZVESTAJI = "MIS_ODOBRAVANJE_IZVESTAJA"
ENV_DOKUMENTI = "MIS_ODOBRAVANJE_DOKUMENATA"

# Статуси које уводи угашен прекидач.
STATUS_IZVESTAJ_BEZ = "BEZ_ODOBRENJA"
STATUS_DOKUMENT_BEZ = "bez_odobrenja"

# Статуси који значе „ово је важећа, употребљива верзија документа".
DOKUMENT_VAZECI = ("odobreno", STATUS_DOKUMENT_BEZ)
# Статуси који значе „извештај је завршен, не чека никога".
IZVESTAJ_ZAVRSEN = ("APPROVED", STATUS_IZVESTAJ_BEZ)
# Статуси у којима се извештај више НЕ мења: предат на преглед или завршен.
IZVESTAJ_NEIZMENJIV = ("SUBMITTED",) + IZVESTAJ_ZAVRSEN

ISTINITO = {"1", "true", "da", "yes", "on"}
NEISTINITO = {"0", "false", "ne", "no", "off"}


def _iz_okruzenja(ime: str):
    sirovo = os.environ.get(ime)
    if sirovo is None:
        return None
    v = sirovo.strip().lower()
    if v in ISTINITO:
        return True
    if v in NEISTINITO:
        return False
    logger.warning(
        "%s има неразумљиву вредност %r — занемарујем је и читам подешавања",
        ime, sirovo)
    return None


def _iz_podesavanja(kljuc: str) -> bool:
    """Прочитај прекидач из system_settings.

    Увоз је намерно унутар функције: `admin_system_views` увози Flask и слој
    приказа, а овај модул зову и подаци (`timesheet_postgres`). Овако нема
    кружног увоза, а кеш подешавања остаје ЈЕДАН — иначе би исти прекидач
    важио у различитим тренуцима на различитим местима.
    """
    try:
        import admin_system_views
        podesavanja = admin_system_views.load_saved_settings() or {}
    except Exception as exc:
        # Fail-closed: не знамо шта пише, значи остаје како је било — са
        # одобравањем. Тихо гашење контроле због пада базе не долази у обзир.
        logger.error("Прекидач %s се не може прочитати (%s) — остаје УКЉУЧЕНО",
                     kljuc, exc)
        return True

    vrednost = podesavanja.get(kljuc)
    if vrednost is None:
        return True
    if isinstance(vrednost, bool):
        return vrednost
    if isinstance(vrednost, str):
        v = vrednost.strip().lower()
        if v in ISTINITO:
            return True
        if v in NEISTINITO:
            return False
    logger.warning("Прекидач %s има неочекивану вредност %r — узимам УКЉУЧЕНО",
                   kljuc, vrednost)
    return True


def _ukljuceno(kljuc: str, env_ime: str) -> bool:
    iz_env = _iz_okruzenja(env_ime)
    if iz_env is not None:
        return iz_env
    return _iz_podesavanja(kljuc)


def odobravanje_izvestaja_ukljuceno() -> bool:
    """Траже ли месечни извештаји потпис шефа и директора."""
    return _ukljuceno(KLJUC_IZVESTAJI, ENV_IZVESTAJI)


def odobravanje_dokumenata_ukljuceno() -> bool:
    """Тражи ли нова верзија документа одобрење пре употребе."""
    return _ukljuceno(KLJUC_DOKUMENTI, ENV_DOKUMENTI)


def stanje() -> dict:
    """Обе вредности одједном — за приказ у админ панелу и дијагностику."""
    return {
        KLJUC_IZVESTAJI: odobravanje_izvestaja_ukljuceno(),
        KLJUC_DOKUMENTI: odobravanje_dokumenata_ukljuceno(),
        "env_preklop": {
            ENV_IZVESTAJI: _iz_okruzenja(ENV_IZVESTAJI),
            ENV_DOKUMENTI: _iz_okruzenja(ENV_DOKUMENTI),
        },
    }
