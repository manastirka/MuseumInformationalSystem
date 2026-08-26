#!/usr/bin/env python3
"""Оцењује да ли сваки прикупљени рад заиста говори о задатом OGK локалитету.

Мотор: GPT-5.6 Luna кроз Codex претплату (без API кључа).
Излаз: по локалитету један JSON у OUT/<OGK_ID>.json — поновно покретање
прескаче већ урађене, па је посао прекидив и настављив. Кад су сви локалитети
готови, --saberi спаја те фајлове у data/ogk_radovi_ocene.json, који чита
scripts/import_export/build_ogk_radovi.py.

Употреба:
    oceni_radove_ogk.py --lista K34-03-0035,K34-14-0007   # пилот
    oceni_radove_ogk.py --sve --paralelno 4               # пун пролаз
    oceni_radove_ogk.py --saberi                          # спајање у data/
"""
import argparse
import json
import os
import re
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

IZVOR = Path("/mnt/licno/OGK_Srbija_podaci/04_harvest_online/radovi/lokaliteti")
OUT = Path.home() / "ocena_radova" / "out"
LOG = Path.home() / "ocena_radova" / "tok.log"

# Спојени излаз — релативно на корен репоа (скрипта стоји у scripts/tekst/).
KOREN = Path(__file__).resolve().parents[2]
ZBIR = KOREN / "data" / "ogk_radovi_ocene.json"

MODEL = "gpt-5.6-luna"
NAPOR = "medium"
DOZVOLJENE = {"potvrdjen", "verovatan", "nije", "nesigurno"}
METOD = "суд модела над насловом, часописом и апстрактом уз контекст локалитета"
# Редослед у коме се пише raspodela — најјачи суд први, да се фајл чита као
# извештај, а не као случајан испис бројача.
REDOSLED = ("potvrdjen", "verovatan", "nesigurno", "nije")

# Процурела ознака алата из Codex излаза — види mis-minerali-obrada.md
SMECE = re.compile(r"cite(turn\d+\w+\d*)+")


def zapisi(poruka):
    red = f"{time.strftime('%H:%M:%S')} {poruka}"
    print(red, flush=True)
    with LOG.open("a", encoding="utf-8") as f:
        f.write(red + "\n")


def napravi_prompt(d):
    radovi = d.get("radovi") or []
    stavke = []
    for i, r in enumerate(radovi, 1):
        aps = (r.get("abstract") or "").strip()
        aps = (aps[:900] + "…") if len(aps) > 900 else aps
        stavke.append(
            f"{i}. НАСЛОВ: {r.get('title') or '—'}\n"
            f"   АУТОРИ: {r.get('authors') or '—'}\n"
            f"   ЧАСОПИС: {r.get('journal') or '—'} ({r.get('year') or '—'})\n"
            f"   АПСТРАКТ: {aps or 'НЕМА АПСТРАКТА'}"
        )
    return f"""Оцењујеш да ли научни рад заиста говори о ЗАДАТОМ ГЕОЛОШКОМ ЛОКАЛИТЕТУ.

Радови су прикупљени аутоматски, претрагом по ИМЕНУ локалитета, па је међу њима
много случајних поготака имена: исто име насеља у другој држави, презиме аутора,
сасвим друга тема. Твој посао је да их раздвојиш.

ЛОКАЛИТЕТ
- Назив: {d.get('naziv') or '—'}
- Категорија: {d.get('kategorija') or '—'}
- Лист ОГК: {d.get('list_id') or '—'} {d.get('list_naziv') or ''}
- Координате: {d.get('lat')}, {d.get('lon')}
- Земља: {d.get('country') or 'Србија'}
- Сировина: {d.get('sirovina') or '—'}
- Формација/јединица: {d.get('formacija') or '—'}
- Опис из ОГК: {d.get('opis') or '—'}

РАДОВИ
{chr(10).join(stavke)}

За СВАКИ рад врати једну од четири оцене:
- "potvrdjen" — рад обрађује баш овај локалитет или његову непосредну околину, и
  геонаучне је природе (геологија, минералогија, петрологија, палеонтологија,
  хидрогеологија, тектоника, рударство, геохемија, спелеологија).
- "verovatan" — вероватно исти простор или шира околина (иста планина, исти рудни
  рејон, исти басен), али из наслова/апстракта то није сигурно.
- "nije" — рад нема везе са овим локалитетом: друга држава, друго место истог
  имена, или тема ван геонаука (историја, књижевност, шумарство, медицина,
  политика, економија, архитектура). Изузетак: рад који изричито обрађује баш
  овај локалитет из друге струке (нпр. историја рударења баш ту) НИЈЕ "nije".
- "nesigurno" — нема довољно података за суд (само наслов без апстракта, а наслов
  двосмислен).

НЕ ИЗМИШЉАЈ. Ако не можеш да утврдиш где је рад лоциран, оцена је "nesigurno",
никако "potvrdjen". Боље признати несигурност него погодити.

Врати ИСКЉУЧИВО JSON, без иједне речи око њега, без markdown ограде:
{{"ocene":[{{"br":1,"ocena":"potvrdjen","razlog":"кратко, до 120 знакова"}}]}}
Мора да има тачно {len(radovi)} ставки, редом, са "br" од 1 до {len(radovi)}."""


def izvuci_json(tekst):
    """Codex зна да дода реч-две око JSON-а или markdown ограду."""
    t = SMECE.sub("", tekst).strip()
    t = re.sub(r"^```(?:json)?\s*|\s*```$", "", t, flags=re.M).strip()
    pocetak = t.find("{")
    if pocetak < 0:
        raise ValueError("нема JSON-а у одговору")
    # балансирање витичастих заграда — одговор уме да носи реп текста
    dubina = 0
    for i in range(pocetak, len(t)):
        if t[i] == "{":
            dubina += 1
        elif t[i] == "}":
            dubina -= 1
            if dubina == 0:
                return json.loads(t[pocetak:i + 1])
    raise ValueError("незатворен JSON")


def obradi(ogk_id):
    cilj = OUT / f"{ogk_id}.json"
    if cilj.exists():
        return ogk_id, "preskocen", 0

    d = json.loads((IZVOR / ogk_id / "dosije.json").read_text(encoding="utf-8"))
    radovi = d.get("radovi") or []
    if not radovi:
        return ogk_id, "nema radova", 0

    izlaz = OUT / f".{ogk_id}.sirovo"
    poc = time.time()
    rez = subprocess.run(
        ["codex", "exec", "--skip-git-repo-check", "--sandbox", "read-only",
         "-c", f'model="{MODEL}"', "-c", f'model_reasoning_effort="{NAPOR}"',
         "-o", str(izlaz), napravi_prompt(d)],
        stdin=subprocess.DEVNULL, capture_output=True, text=True, timeout=600,
    )
    trajanje = round(time.time() - poc, 1)
    if rez.returncode != 0 or not izlaz.exists():
        return ogk_id, f"PAO codex rc={rez.returncode} {rez.stderr.strip()[:200]}", trajanje

    try:
        podaci = izvuci_json(izlaz.read_text(encoding="utf-8"))
        ocene = podaci["ocene"]
    except Exception as e:                       # noqa: BLE001
        return ogk_id, f"PAO parsiranje: {e}", trajanje

    if len(ocene) != len(radovi):
        return ogk_id, f"PAO broj: {len(ocene)} umesto {len(radovi)}", trajanje

    upis = []
    for i, (o, r) in enumerate(zip(ocene, radovi), 1):
        oc = str(o.get("ocena", "")).strip().lower()
        if oc not in DOZVOLJENE:
            return ogk_id, f"PAO ocena „{oc}“ na {i}", trajanje
        upis.append({
            "br": i,
            "doi": r.get("doi") or "",
            "url": r.get("url") or "",
            "naslov": r.get("title") or "",
            "ocena": oc,
            "razlog": SMECE.sub("", str(o.get("razlog", ""))).strip()[:160],
        })

    cilj.write_text(json.dumps({
        "ogk_id": ogk_id, "naziv": d.get("naziv"),
        "model": MODEL, "napor": NAPOR,
        "ocenjeno": time.strftime("%Y-%m-%d"),
        "ocene": upis,
    }, ensure_ascii=False, indent=1), encoding="utf-8")
    izlaz.unlink(missing_ok=True)
    return ogk_id, "ok", trajanje


def saberi(cilj):
    """Спаја OUT/<OGK_ID>.json у један фајл за build_ogk_radovi.py.

    Уписује се и `naslov` — без њега спајање по редном броју не би имало чиме
    да се провери, а тихо померен редослед у жетви значио би да сваки рад носи
    туђу оцену.
    """
    ocene = {}
    raspodela = dict.fromkeys(REDOSLED, 0)
    ukupno = 0
    for putanja in sorted(OUT.glob("*.json")):
        podaci = json.loads(putanja.read_text(encoding="utf-8"))
        ogk_id = podaci.get("ogk_id") or putanja.stem
        spisak = []
        for stavka in podaci.get("ocene") or []:
            ocena = stavka.get("ocena")
            if ocena not in DOZVOLJENE:
                raise ValueError(f"{ogk_id}: недозвољена оцена „{ocena}“")
            raspodela[ocena] += 1
            ukupno += 1
            spisak.append({
                "br": stavka["br"],
                "naslov": stavka.get("naslov") or "",
                "ocena": ocena,
                "razlog": stavka.get("razlog") or "",
            })
        if spisak:
            ocene[ogk_id] = spisak

    if not ocene:
        raise ValueError(f"нема ниједне оцене у {OUT} — ништа није уписано")

    cilj.write_text(json.dumps({
        "generisano": time.strftime("%Y-%m-%d"),
        "model": MODEL,
        "napor": NAPOR,
        "metod": METOD,
        "ukupno_lokaliteta": len(ocene),
        "ukupno_ocena": ukupno,
        "raspodela": raspodela,
        "ocene": ocene,
    }, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"Уписано: {cilj} ({len(ocene)} локалитета, {ukupno} оцена)")
    for kljuc in REDOSLED:
        print(f"  {kljuc:<12} {raspodela[kljuc]:>5}")


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--lista", help="ID-еви раздвојени зарезом")
    p.add_argument("--sve", action="store_true")
    p.add_argument("--saberi", action="store_true",
                   help="споји OUT/*.json у data/ogk_radovi_ocene.json")
    p.add_argument("--zbir", default=str(ZBIR),
                   help="путања спојеног излаза (подразумевано %(default)s)")
    p.add_argument("--paralelno", type=int, default=3)
    a = p.parse_args()

    if a.saberi:
        if not OUT.exists():
            sys.exit(f"нема оцена за сабирање: {OUT}")
        saberi(Path(a.zbir))
        return

    if not IZVOR.exists():
        sys.exit(f"извор није доступан: {IZVOR}")
    OUT.mkdir(parents=True, exist_ok=True)

    if a.lista:
        idevi = [x.strip() for x in a.lista.split(",") if x.strip()]
    elif a.sve:
        idevi = sorted(
            d.name for d in IZVOR.iterdir()
            if d.is_dir() and (json.loads((d / "dosije.json").read_text(encoding="utf-8")).get("radovi") or [])
        )
    else:
        sys.exit("задај --lista, --sve или --saberi")

    zapisi(f"почетак: {len(idevi)} локалитета, паралелно {a.paralelno}")
    brojac = {"ok": 0, "preskocen": 0, "pao": 0}
    with ThreadPoolExecutor(max_workers=a.paralelno) as ex:
        poslovi = {ex.submit(obradi, i): i for i in idevi}
        for n, f in enumerate(as_completed(poslovi), 1):
            ogk_id, stanje, t = f.result()
            kljuc = "ok" if stanje == "ok" else ("preskocen" if stanje in ("preskocen", "nema radova") else "pao")
            brojac[kljuc] += 1
            if kljuc != "preskocen":
                zapisi(f"[{n}/{len(idevi)}] {ogk_id} {stanje} {t}s")
    zapisi(f"крај: ok={brojac['ok']} прескочено={brojac['preskocen']} ПАЛО={brojac['pao']}")


if __name__ == "__main__":
    main()
