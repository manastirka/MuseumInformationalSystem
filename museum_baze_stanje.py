"""Које базе имају праве музејске податке, а које само демо (placeholder) редове.

Мени „Базе података" по овоме дели ставке: база са правим подацима стоји у
свом одељку (Биологија, Геологија…), база без њих иде у подмени „У развоју".
Подела је динамичка — чим кустос упише први стварни запис, база се сама
пресели у свој одељак, без измене кода.

„Прави подаци" = бар један ред који није из демо семена. Демо семе су редови
које су миграције/скрипте уписале 25–26.12.2025 да стране не буду празне
(каталошки бројеви BOT-2024-001, КД-ПМ-001/2015 …). Ти редови се
препознају по броју, не по датуму, па ни ручно унет запис истог дана не би
био погрешно скривен.

Провера иде на базу највише једном у ROK_KESA секунди по процесу; при паду
базе ништа се не скрива (база се третира као да има податке) и грешка се
логује — мени никад не сме да „изгуби" базу због тренутног квара.
"""

import logging
import threading
import time

from postgres_service import get_postgres_connection

logger = logging.getLogger(__name__)

ROK_KESA = 300  # секунди

# Демо семе по збирци — тачно оно што стоји у бази од децембра 2025.
_SEME_ZBIRKI = {
    'botany': ('BOT-2024-001', 'BOT-2024-002', 'BOT-2024-003', 'BOT-2024-004', 'BOT-2024-005'),
    'entomology': ('ENT-COL-001', 'ENT-HYM-001', 'ENT-LEP-001', 'ENT-LEP-002', 'ENT-ODO-001',
                   'ENT-ORT-001', 'ENT-OD-001'),
    'herpetology': ('HERP-AMP-001', 'HERP-AMP-002', 'HERP-AMP-003', 'HERP-REP-001',
                    'HERP-REP-002', 'HERP-REP-003'),
    'ichthyology': ('ICH-2024-001', 'ICH-2024-002', 'ICH-2024-003'),
    'mycology': ('MYC-2024-001', 'MYC-2024-002', 'MYC-2024-003', 'MYC-2024-004', 'MYC-2024-005'),
    'ornithology': ('ORN-2024-001', 'ORN-2024-002', 'ORN-2024-003', 'ORN-2024-004', 'ORN-2024-005'),
    'paleobotany': ('PALEOBOT-001', 'PALEOBOT-002', 'PALEOBOT-003', 'PALEOBOT-004',
                    'PBOT-2024-001', 'PBOT-2024-002'),
    'paleozoology': ('PALEO-MAM-001', 'PALEO-MAM-002', 'PALEO-MAM-003', 'PALEO-MAM-004',
                     'PALEO-MAM-005', 'PALEO-REP-001', 'PALEO-DINO-001', 'PALEO-PROB-001',
                     'PALEO-MOLL-001'),
    'petrology': ('PETRO-IGN-001', 'PETRO-IGN-002', 'PETRO-MET-001', 'PETRO-SED-001',
                  'PETR-2024-001', 'PETR-2024-002'),
}
# Збирка метеорита (MET-001…018) је СТВАРНА — Александар, 02.09.2026; нема семена.
_SEME_NASLEDJE = ('КД-ПМ-001/2015', 'КД-ПМ-002/2018', 'КД-ПМ-003/2020',
                  'КД-ПМ-004/2019', 'КД-ПМ-005/2021', 'КД-ПМ-006/2017')

# Ставке менија које могу да буду „у развоју". Кључ = оно што шаблон пита;
# modul = кључ за has_module_access; odeljak = где стоји кад има податке.
NAV_BAZE = (
    {'kljuc': 'botany_collection', 'modul': 'botany_collection', 'endpoint': 'botany_collection',
     'ikona': 'bi bi-flower1', 'naziv': 'Ботаничка збирка', 'odeljak': 'Биологија'},
    {'kljuc': 'ornithology_collection', 'modul': 'ornithology_collection', 'endpoint': 'ornithology_collection',
     'ikona': 'museum-icon-bird', 'naziv': 'Орнитолошка збирка', 'odeljak': 'Биологија'},
    {'kljuc': 'ichthyology_collection', 'modul': 'ichthyology_collection', 'endpoint': 'ichthyology_collection',
     'ikona': 'museum-icon-fish', 'naziv': 'Ихтиолошка збирка', 'odeljak': 'Биологија'},
    {'kljuc': 'herpetology_collection', 'modul': 'herpetology_collection', 'endpoint': 'herpetology_collection',
     'ikona': 'museum-icon-snake', 'naziv': 'Херпетолошка збирка', 'odeljak': 'Биологија'},
    {'kljuc': 'entomology_collection', 'modul': 'entomology_collection', 'endpoint': 'entomology_collection',
     'ikona': 'bi bi-bug-fill', 'naziv': 'Ентомолошка збирка', 'odeljak': 'Биологија'},
    {'kljuc': 'mycology_collection', 'modul': 'mycology_collection', 'endpoint': 'mycology_collection',
     'ikona': 'museum-icon-mushroom', 'naziv': 'Миколошка збирка', 'odeljak': 'Биологија'},
    {'kljuc': 'petrology_collection', 'modul': 'petrology_collection', 'endpoint': 'petrology_collection',
     'ikona': 'bi bi-bricks', 'naziv': 'Петролошка збирка', 'odeljak': 'Геологија'},
    {'kljuc': 'meteorite_collection', 'modul': 'meteorite_collection', 'endpoint': 'meteorite_collection',
     'ikona': 'museum-icon-shooting-star', 'naziv': 'Збирка метеорита', 'odeljak': 'Геологија'},
    {'kljuc': 'paleozoology_collection', 'modul': 'paleozoology_collection', 'endpoint': 'paleozoology_collection',
     'ikona': 'museum-icon-dinosaur', 'naziv': 'Палеозоолошка збирка', 'odeljak': 'Палеозоологија'},
    {'kljuc': 'sanja_paleogene_neogene_mammals', 'modul': 'sanja_paleogene_neogene_mammals',
     'endpoint': 'sanja_paleogene_neogene_mammals', 'ikona': 'museum-icon-mammoth',
     'naziv': 'Крупни сисари палеоген/неоген', 'odeljak': 'Палеозоологија'},
    {'kljuc': 'paleobotany_collection', 'modul': 'paleobotany_collection', 'endpoint': 'paleobotany_collection',
     'ikona': 'bi bi-leaf', 'naziv': 'Палеоботаничка збирка', 'odeljak': 'Геологија'},
    {'kljuc': 'visitors_database', 'modul': 'employees_database', 'endpoint': 'visitors_database',
     'ikona': 'bi bi-person-walking', 'naziv': 'База посетилаца', 'odeljak': 'Музејске евиденције'},
    {'kljuc': 'research_database', 'modul': 'employees_database', 'endpoint': 'research_database',
     'ikona': 'bi bi-mortarboard', 'naziv': 'Истраживачки пројекти', 'odeljak': 'Музејске евиденције'},
    {'kljuc': 'exhibits_database', 'modul': 'exhibits_database', 'endpoint': 'exhibits_database',
     'ikona': 'bi bi-box', 'naziv': 'База експоната', 'odeljak': 'Музејске евиденције'},
    {'kljuc': 'cultural_heritage', 'modul': 'cultural_heritage', 'endpoint': 'cultural_heritage_database',
     'ikona': 'bi bi-bank', 'naziv': 'Културно наслеђе', 'odeljak': 'Музејске евиденције'},
)

_ZBIRKA_PO_KLJUCU = {
    'botany_collection': 'botany', 'ornithology_collection': 'ornithology',
    'ichthyology_collection': 'ichthyology', 'herpetology_collection': 'herpetology',
    'entomology_collection': 'entomology', 'mycology_collection': 'mycology',
    'petrology_collection': 'petrology', 'paleozoology_collection': 'paleozoology',
    'paleobotany_collection': 'paleobotany',
}


def _upiti():
    """(кључ, SQL, параметри) — сваки враћа број СТВАРНИХ редова."""
    upiti = []
    for kljuc, zbirka in _ZBIRKA_PO_KLJUCU.items():
        upiti.append((
            kljuc,
            "SELECT count(*) FROM collection_specimens "
            "WHERE collection_type = %s AND COALESCE(catalog_number, '') <> ALL(%s)",
            (zbirka, list(_SEME_ZBIRKI[zbirka])),
        ))
    upiti.append(('meteorite_collection', "SELECT count(*) FROM meteorite_specimens", ()))
    upiti.append(('cultural_heritage',
                  "SELECT count(*) FROM heritage_items WHERE COALESCE(registry_number, '') <> ALL(%s)",
                  (list(_SEME_NASLEDJE),)))
    # Сањина збирка: два пробна реда („new", „new specimen") без иједног поља.
    upiti.append(('sanja_paleogene_neogene_mammals',
                  "SELECT count(*) FROM sanja_paleogene_neogene_mammals "
                  "WHERE COALESCE(specimen->>'catalog_number', '') <> '' "
                  "   OR COALESCE(specimen->>'taxon_name', '') <> ''",
                  ()))
    upiti.append(('visitors_database', "SELECT count(*) FROM visitor_records", ()))
    upiti.append(('research_database', "SELECT count(*) FROM research_projects", ()))
    upiti.append(('exhibits_database', "SELECT count(*) FROM exhibition_items", ()))
    return upiti


def izbroj_stvarne_redove():
    """Речник кључ → број стварних редова. Пад упита = None (непознато)."""
    rezultat = {}
    try:
        with get_postgres_connection() as conn:
            for kljuc, sql, parametri in _upiti():
                try:
                    with conn.cursor() as cur:
                        cur.execute(sql, parametri)
                        rezultat[kljuc] = int(cur.fetchone()[0])
                    conn.commit()
                except Exception as exc:
                    conn.rollback()
                    logger.warning("Стање базе %s није утврђено: %s", kljuc, exc)
                    rezultat[kljuc] = None
    except Exception as exc:
        logger.error("Стање база за мени није прочитано (база недоступна): %s", exc)
    return rezultat


_kes = {'vreme': 0.0, 'brojevi': {}}
_brava = threading.Lock()


def _brojevi(sada=None):
    sada = time.time() if sada is None else sada
    with _brava:
        if sada - _kes['vreme'] > ROK_KESA:
            _kes['brojevi'] = izbroj_stvarne_redove()
            _kes['vreme'] = sada
        return _kes['brojevi']


def osvezi():
    """Одбаци кеш (после уписа у тесту или после увоза)."""
    with _brava:
        _kes['vreme'] = 0.0
        _kes['brojevi'] = {}


def u_razvoju(kljuc):
    """True само кад је ПОТВРЂЕНО да база нема стварних редова."""
    broj = _brojevi().get(kljuc)
    return broj == 0


def stavke_u_razvoju():
    """Ставке менија које иду у подмени „У развоју", редом као у NAV_BAZE."""
    brojevi = _brojevi()
    return [dict(s) for s in NAV_BAZE if brojevi.get(s['kljuc']) == 0]


def stanje_svih():
    """За надзор/тестове: кључ → {'stvarnih': n, 'u_razvoju': bool}."""
    brojevi = _brojevi()
    return {
        s['kljuc']: {'stvarnih': brojevi.get(s['kljuc']), 'u_razvoju': brojevi.get(s['kljuc']) == 0}
        for s in NAV_BAZE
    }
