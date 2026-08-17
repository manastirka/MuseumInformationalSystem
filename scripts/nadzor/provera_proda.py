#!/usr/bin/env python3
"""Дневна провера продукције са dev машине, преко Tailscale-а.

ЗАШТО ОДАВДЕ, А НЕ СА ПРОДА
    Прод нема MTA, па јединица која падне не може ником да јавише. Уместо да
    на сервер уводимо тајну (SMTP лозинку) само зарад аларма, проверу ради
    машина која ионако ради 24/7 и већ има ssh кључ за прод.

    Цена тога, поштено: ако dev падне, провера ћути. Зато последњи ред
    извештаја увек носи датум — стар извештај значи да провера не ради.

ШТА ГЛЕДА
    1. да ли је прод уопште достижан
    2. свежину ноћног бекапа базе (не сме бити старији од 26 h)
    3. пале јединице (systemctl is-failed)
    4. маркере аларма у /var/lib/mis/alarm — хватају и пад који је у
       међувремену ручно поправљен, што is-failed више не показује
    5. гране у /data којих нема у бекапу
    6. слободан простор на / и /backup
    7. здравље апликације (/healthz кроз nginx)
    8. када је последњи пут рађена проба враћања бекапа

ИЗЛАЗ
    0 = све у реду, 1 = бар један налаз. Извештај иде на стдио и у
    ~/nadzor/POSLEDNJE.md; при налазу се ствара и ~/nadzor/PROBLEM.

УПОТРЕБА
    python3 scripts/nadzor/provera_proda.py
    python3 scripts/nadzor/provera_proda.py --domacin prod-nadzor
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
import time
from pathlib import Path

KOREN = Path.home() / "nadzor"
POSLEDNJE = KOREN / "POSLEDNJE.md"
DNEVNIK = KOREN / "PREGLED.md"
PROBLEM = KOREN / "PROBLEM"
STANJE = KOREN / "stanje.json"

# Списак јединица које се гледају живи у deploy/nadzor-podaci.sh, НА ПРОДУ —
# зато што надзорни кључ не сме да шаље сопствену наредбу. Овде се броји само
# оно што стигне у одељку ###PALE.

MAX_STAROST_BEKAPA_H = 26      # 24 h + резерва за померање термина
MAX_DANA_OD_PROBE = 40         # проба је месечна (1. у месецу)
MIN_SLOBODNO_ODSTO = 10


def prikupi(domacin: str) -> dict:
    """Повуци стање са прода.

    Наредба се НЕ шаље — надзорни кључ на проду има
    `command="/home/alukovic/bin/nadzor-podaci.sh",restrict`, па ssh увек
    покрене баш тај сакупљач и ништа друго. Ако кључ са dev-а икад процури,
    њиме се не може добити шел на продукцији.
    Извор сакупљача у репоу: deploy/nadzor-podaci.sh
    """
    p = subprocess.run(
        ["ssh", "-o", "BatchMode=yes", "-o", "ConnectTimeout=15", domacin],
        capture_output=True, text=True, timeout=90,
    )
    izlaz = (p.stdout + p.stderr).strip()
    if "###KRAJ" not in izlaz:
        raise RuntimeError(f"ssh {domacin} није дао потпун излаз "
                           f"(кôд {p.returncode}): {izlaz[:300]}")

    odeljci: dict[str, list[str]] = {}
    trenutni = None
    for red in izlaz.splitlines():
        if red.startswith("###"):
            trenutni = red[3:]
            odeljci[trenutni] = []
        elif trenutni:
            odeljci[trenutni].append(red)
    return odeljci


def procena(o: dict) -> tuple[list[str], list[str]]:
    """Врати (налази, у_реду). Налаз = нешто што тражи човека."""
    nalazi: list[str] = []
    u_redu: list[str] = []

    sada = int(o.get("VREME", ["0"])[0] or 0)

    # 1. свежина бекапа
    red = next((r for r in o.get("BEKAP", []) if r.strip()), "")
    if not red:
        nalazi.append("БЕКАП: у /backup/current/db нема ниједног дампа")
    else:
        ts, ime = red.split(None, 1)
        sati = (sada - int(ts)) / 3600
        if sati > MAX_STAROST_BEKAPA_H:
            nalazi.append(f"БЕКАП: последњи дамп је стар {sati:.0f} h "
                          f"({ime}) — ноћни посао није прошао")
        else:
            u_redu.append(f"бекап свеж ({sati:.0f} h, {Path(ime).name})")

    # 2. пале јединице
    pale = []
    ukupno_jedinica = 0
    for red in o.get("PALE", []):
        if not red.strip():
            continue
        ime, stanje = (red.split() + [""])[:2]
        ukupno_jedinica += 1
        if stanje == "failed":
            pale.append(ime)
    if pale:
        nalazi.append("ПАЛЕ ЈЕДИНИЦЕ: " + ", ".join(pale))
    else:
        u_redu.append(f"ниједна од {ukupno_jedinica} јединица није у стању failed")

    # 3. маркери аларма — хватају и пад који је у међувремену поправљен
    markeri = [r.strip() for r in o.get("MARKERI", []) if r.strip()]
    videni = set()
    if STANJE.is_file():
        try:
            videni = set(json.loads(STANJE.read_text()).get("markeri", []))
        except Exception:
            videni = set()
    novi = [m for m in markeri if m not in videni]
    if novi:
        nalazi.append("НОВИ АЛАРМИ (" + str(len(novi)) + "): " + ", ".join(
            Path(m).name for m in novi[-5:]))
    elif markeri:
        u_redu.append(f"аларма укупно {len(markeri)}, ниједан нов")
    else:
        u_redu.append("нема алармних маркера")

    # 4. диск
    for red in o.get("DISK", []):
        delovi = red.split()
        if len(delovi) != 2:
            continue
        tacka, pcent = delovi
        zauzeto = int(pcent.rstrip("%"))
        if 100 - zauzeto < MIN_SLOBODNO_ODSTO:
            nalazi.append(f"ДИСК {tacka}: заузето {zauzeto}%")
        else:
            u_redu.append(f"{tacka} заузет {zauzeto}%")

    # 5. гране података које нису у бекапу
    #
    # 17.08.2026: `/data/mis/media` (223 MB) НЕ постоји у /backup/current/data.
    # То је највероватније намерно — то су изведени приказни фајлови
    # (jpg/thumb) које fototeka worker поново прави из `/data/arhiva`, а
    # arhiva ЈЕСТЕ у бекапу. Скрипта бекапа је root-only, па се не може
    # прочитати и потврдити. Изузетак стоји овде именован, да зна да
    # га неко јесте видео — а свака НОВА грана која испадне из бекапа
    # одмах постаје налаз.
    POZNATI_IZUZECI = {
        'mis/media': 'изведени приказни фајлови, обновиви из mis/arhiva',
        'mis/uploads': 'привремени пријем, празан',
    }
    na_produ_grane = {r.strip() for r in o.get('STABLA_PROD', []) if r.strip()}
    u_bekapu = {r.strip() for r in o.get('STABLA_BEKAP', []) if r.strip()}
    if na_produ_grane and u_bekapu:
        nedostaju = sorted(na_produ_grane - u_bekapu - set(POZNATI_IZUZECI))
        if nedostaju:
            nalazi.append('НИЈЕ У БЕКАПУ: ' + ', '.join(nedostaju))
        else:
            poznato = sorted(set(POZNATI_IZUZECI) & na_produ_grane)
            u_redu.append('све гране /data су у бекапу'
                          + (f' (осим познатих: {", ".join(poznato)})'
                             if poznato else ''))

    # 6. здравље апликације
    zdravlje = " ".join(o.get("ZDRAVLJE", [])).strip()
    if '"status":"ok"' in zdravlje.replace(" ", ""):
        u_redu.append("апликација одговара, healthz ok")
    else:
        nalazi.append(f"ЗДРАВЉЕ: /healthz није ok → {zdravlje[:120] or 'празно'}")

    # 7. проба враћања бекапа
    proba = " ".join(o.get("PROBA", [])).strip()
    if not proba or proba == "n/a":
        nalazi.append("ПРОБА ВРАЋАЊА: нема податка да је икад покренута")
    else:
        try:
            t = time.mktime(time.strptime(proba.split(" CEST")[0].split(" CET")[0],
                                          "%a %Y-%m-%d %H:%M:%S"))
            dana = (sada - t) / 86400
            if dana > MAX_DANA_OD_PROBE:
                nalazi.append(f"ПРОБА ВРАЋАЊА: последња пре {dana:.0f} дана")
            else:
                u_redu.append(f"проба враћања пре {dana:.0f} дана")
        except Exception:
            u_redu.append(f"проба враћања: {proba}")

    STANJE.parent.mkdir(parents=True, exist_ok=True)
    STANJE.write_text(json.dumps({"markeri": markeri}, ensure_ascii=False))
    return nalazi, u_redu


def izvestaj(domacin: str, nalazi: list[str], u_redu: list[str],
             greska: str | None) -> str:
    vreme = time.strftime("%Y-%m-%d %H:%M")
    r = [f"# Провера продукције — {vreme}", ""]
    if greska:
        r += ["**ПРОВЕРА НИЈЕ ПРОШЛА**", "", f"    {greska}", "",
              f"Прод (`{domacin}`) није достижан са dev-а. То може бити и мрежа,",
              "не мора бити сервер — али док се не разреши, нико не гледа прод."]
        return "\n".join(r) + "\n"
    if nalazi:
        r += [f"## Налази ({len(nalazi)})", ""]
        r += [f"- {n}" for n in nalazi]
        r.append("")
    else:
        r += ["## Нема налаза", ""]
    r += ["## Проверено", ""]
    r += [f"- {u}" for u in u_redu]
    r.append("")
    return "\n".join(r)


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--domacin", default="prod-nadzor",
                   help="ssh алијас надзорног приступа проду")
    p.add_argument("--tiho", action="store_true",
                   help="испиши само при налазу")
    a = p.parse_args()

    KOREN.mkdir(parents=True, exist_ok=True)
    greska = None
    nalazi: list[str] = []
    u_redu: list[str] = []
    try:
        nalazi, u_redu = procena(prikupi(a.domacin))
    except Exception as exc:
        greska = f"{type(exc).__name__}: {exc}"

    tekst = izvestaj(a.domacin, nalazi, u_redu, greska)
    POSLEDNJE.write_text(tekst, encoding="utf-8")

    lose = bool(nalazi or greska)
    if lose:
        # Видљив траг који не зависи од тога да ли неко чита стдио.
        PROBLEM.write_text(tekst, encoding="utf-8")
    elif PROBLEM.exists():
        PROBLEM.unlink()

    if not DNEVNIK.exists():
        DNEVNIK.write_text("# Дневник провера продукције\n\n", encoding="utf-8")
    with DNEVNIK.open("a", encoding="utf-8") as f:
        sazetak = ("; ".join(nalazi)[:200] if nalazi
                   else (greska[:200] if greska else "уредно"))
        f.write(f"- {time.strftime('%Y-%m-%d %H:%M')} · "
                f"{'**НАЛАЗ**' if lose else 'ок'} · {sazetak}\n")

    if lose or not a.tiho:
        print(tekst)
    return 1 if lose else 0


if __name__ == "__main__":
    raise SystemExit(main())
