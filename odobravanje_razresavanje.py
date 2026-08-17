"""Разрешавање затеченог посла кад се одобравање искључи.

Гашење прекидача има смисла само ако ослободи и оно што већ стоји у реду —
иначе извештаји поднети јуче настављају да чекају потпис који неће доћи, а
запослени не разуме зашто његов из прошлог месеца виси а овомесечни не.

Правила су намерно уска:
  * радне листе: само `SUBMITTED` → `BEZ_ODOBRENJA`. `REJECTED` се НЕ дира —
    те су враћене запосленом и он их поново подноси, тада већ по новом
    правилу. `DRAFT` није ни поднет.
  * документи: `na_odobrenju` → `bez_odobrenja`, али само НАЈНОВИЈА верзија
    сваког документа. Старије верзије на чекању иду у архиву, као и раније
    важеће — документ не сме да заврши са две важеће верзије.

Свака промена оставља траг: радне листе у `timesheet_status_history`,
документи у `document_audit_log`. Тихо померање десетина редова без записа не
долази у обзир.

Модул намерно НЕ увози Flask ни `session` — зову га и веб и командна линија.
"""
from __future__ import annotations

import logging

from postgres_service import get_postgres_connection

import odobravanje_prekidac

logger = logging.getLogger(__name__)

BELESKA_IZVESTAJ = ('Одобравање искључено — извештај је затворен без потписа '
                    'шефа и директора')
BELESKA_DOKUMENT = 'Одобравање искључено — верзија је постала важећа без прегледа'


def prebroj_zatecene() -> dict:
    """Колико чека одобрење — за приказ ПРЕ него што се прекидач угаси."""
    with get_postgres_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT COUNT(*) FROM timesheet_reports WHERE status = 'SUBMITTED'")
            izvestaji = cur.fetchone()[0]
            cur.execute(
                "SELECT COUNT(*) FROM document_versions WHERE status = 'na_odobrenju'")
            dokumenti = cur.fetchone()[0]
    return {'izvestaji': izvestaji, 'dokumenti': dokumenti}


def razresi_izvestaje(ko: str, *, izvrsi: bool = False) -> dict:
    """Затворити радне листе које чекају потпис. Без `izvrsi` само броји."""
    with get_postgres_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT id FROM timesheet_reports WHERE status = 'SUBMITTED' FOR UPDATE")
            ids = [r[0] for r in cur.fetchall()]
            if not izvrsi or not ids:
                return {'pronadjeno': len(ids), 'promenjeno': 0, 'izvrseno': izvrsi}

            cur.execute(
                """
                UPDATE timesheet_reports
                SET status = %s
                WHERE id = ANY(%s) AND status = 'SUBMITTED'
                """,
                (odobravanje_prekidac.STATUS_IZVESTAJ_BEZ, ids),
            )
            promenjeno = cur.rowcount
            # Историја се пише из ИСТЕ трансакције — ако падне, пада и измена
            # статуса. Промена без трага у историји овде не постоји.
            cur.executemany(
                """
                INSERT INTO timesheet_status_history
                (report_id, old_status, new_status, changed_by, note)
                VALUES (%s, 'SUBMITTED', %s, %s, %s)
                """,
                [(i, odobravanje_prekidac.STATUS_IZVESTAJ_BEZ, ko, BELESKA_IZVESTAJ)
                 for i in ids],
            )
            conn.commit()
    logger.info("Одобравање искључено: затворено %s радних листа (%s)", promenjeno, ko)
    return {'pronadjeno': len(ids), 'promenjeno': promenjeno, 'izvrseno': True}


def razresi_dokumente(ko: str, *, izvrsi: bool = False) -> dict:
    """Учинити важећом најновију верзију на чекању, остало у архиву."""
    with get_postgres_connection() as conn:
        with conn.cursor() as cur:
            # Најновија верзија на чекању по документу — она постаје важећа.
            cur.execute(
                """
                SELECT DISTINCT ON (document_id) id, document_id
                FROM document_versions
                WHERE status = 'na_odobrenju'
                ORDER BY document_id, version_no DESC, id DESC
                FOR UPDATE
                """
            )
            izabrane = cur.fetchall()
            cur.execute(
                "SELECT COUNT(*) FROM document_versions WHERE status = 'na_odobrenju'")
            ukupno_na_cekanju = cur.fetchone()[0]

            if not izvrsi or not izabrane:
                return {'dokumenata': len(izabrane),
                        'verzija_na_cekanju': ukupno_na_cekanju,
                        'promenjeno': 0, 'izvrseno': izvrsi}

            id_izabranih = [r[0] for r in izabrane]
            dokumenti = [r[1] for r in izabrane]

            # 1. све раније важеће и остале верзије на чекању тих докумената
            #    иду у архиву — да важећа остане тачно једна.
            cur.execute(
                """
                UPDATE document_versions
                SET status = 'arhivirano'
                WHERE document_id = ANY(%s)
                  AND id <> ALL(%s)
                  AND status = ANY(%s)
                """,
                (dokumenti, id_izabranih,
                 list(odobravanje_prekidac.DOKUMENT_VAZECI) + ['na_odobrenju']),
            )
            arhivirano = cur.rowcount

            # 2. изабране постају важеће, БЕЗ рецензента.
            cur.execute(
                """
                UPDATE document_versions
                SET status = %s
                WHERE id = ANY(%s) AND status = 'na_odobrenju'
                """,
                (odobravanje_prekidac.STATUS_DOKUMENT_BEZ, id_izabranih),
            )
            promenjeno = cur.rowcount

            cur.executemany(
                """
                INSERT INTO document_audit_log
                (document_id, version_id, action, actor_email, note)
                VALUES (%s, %s, 'bez_odobrenja', %s, %s)
                """,
                [(d, v, ko, BELESKA_DOKUMENT) for v, d in izabrane],
            )
            conn.commit()
    logger.info("Одобравање докумената искључено: %s верзија важи, %s архивирано (%s)",
                promenjeno, arhivirano, ko)
    return {'dokumenata': len(izabrane), 'verzija_na_cekanju': ukupno_na_cekanju,
            'promenjeno': promenjeno, 'arhivirano': arhivirano, 'izvrseno': True}
