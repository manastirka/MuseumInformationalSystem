#!/usr/bin/env python3
"""Ред рецензија — прима merge-ове, обрађује их кад рецензент буде слободан.

КАКО СЕ УКЛАПА
    git post-merge кука  →  `red.py dodaj <hash>`  →  ред у ~/recenzije/red/
    systemd тајмер (15 min) →  `red.py obradi`  →  recenzija.py по ставци

    Ако `recenzija.py` врати 75 (сви рецензенти потрошени), ставка ОСТАЈЕ у
    реду и тајмер је покупи следећи пут. То је цела поента: рецензија касни,
    не деградира.

    Ставка се одустаје тек после довољно покушаја (подразумевано 20 ≈ 5 сати),
    и тада иде у `~/recenzije/odustalo/` — не нестаје тихо.

УПОТРЕБА
    python3 scripts/review/red.py dodaj <hash>
    python3 scripts/review/red.py obradi        # тајмер ово зове
    python3 scripts/review/red.py pregled       # шта чека, шта је урађено
"""
from __future__ import annotations

import subprocess
import sys
import time
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
KOREN = Path.home() / "recenzije"
RED = KOREN / "red"
ODUSTALO = KOREN / "odustalo"
DNEVNIK = KOREN / "PREGLED.md"
RECENZIJA = REPO / "scripts" / "review" / "recenzija.py"

MAX_POKUSAJA = 20  # 20 × 15 min ≈ 5 сати чекања пре одустајања


def python() -> str:
    v = REPO / "venv" / "bin" / "python"
    return str(v) if v.is_file() else sys.executable


def dodaj(h: str) -> int:
    RED.mkdir(parents=True, exist_ok=True)
    stavka = RED / h
    if stavka.exists():
        print(f"{h} је већ у реду")
        return 0
    stavka.write_text("pokusaja=0\n")
    print(f"{h} додат у ред")
    return 0


def zabelezi(red: str) -> None:
    KOREN.mkdir(parents=True, exist_ok=True)
    if not DNEVNIK.exists():
        DNEVNIK.write_text("# Преглед рецензија\n\n")
    with DNEVNIK.open("a", encoding="utf-8") as f:
        f.write(red + "\n")


def obradi() -> int:
    if not RED.is_dir():
        return 0
    stavke = sorted(RED.iterdir(), key=lambda p: p.stat().st_mtime)
    if not stavke:
        return 0

    for stavka in stavke:
        h = stavka.name
        podaci = dict(
            r.split("=", 1) for r in stavka.read_text().splitlines() if "=" in r
        )
        pokusaja = int(podaci.get("pokusaja", 0)) + 1
        vreme = time.strftime("%Y-%m-%d %H:%M")

        p = subprocess.run(
            [python(), str(RECENZIJA), "--opseg", f"{h}^..{h}"],
            cwd=REPO, capture_output=True, text=True,
        )
        izlaz = (p.stdout or "").strip()

        if p.returncode == 0:
            stavka.unlink()
            preskoceno = "Прескачем" in izlaz
            zabelezi(f"- `{h}` · {vreme} · "
                     + ("прескочено (само документација)" if preskoceno
                        else f"готово, извештај `recenzije/{h}.md`"))
            print(f"{h}: готово")
        elif p.returncode == 75:
            stavka.write_text(f"pokusaja={pokusaja}\n")
            if pokusaja >= MAX_POKUSAJA:
                ODUSTALO.mkdir(parents=True, exist_ok=True)
                stavka.rename(ODUSTALO / h)
                zabelezi(f"- `{h}` · {vreme} · **ОДУСТАЛО** после {pokusaja} "
                         f"покушаја — ниједан рецензент није био слободан")
                print(f"{h}: одустало после {pokusaja} покушаја")
            else:
                print(f"{h}: сви заузети, чека даље ({pokusaja}/{MAX_POKUSAJA})")
            # Ако су сви потрошени, нема сврхе пробати остале ставке сада.
            break
        else:
            stavka.write_text(f"pokusaja={pokusaja}\n")
            print(f"{h}: грешка (кôд {p.returncode}), покушај {pokusaja}")
            if pokusaja >= MAX_POKUSAJA:
                ODUSTALO.mkdir(parents=True, exist_ok=True)
                stavka.rename(ODUSTALO / h)
                zabelezi(f"- `{h}` · {vreme} · **ОДУСТАЛО** — "
                         f"{(p.stderr or izlaz)[:120]}")
    return 0


def pregled() -> int:
    cekaju = sorted(RED.iterdir()) if RED.is_dir() else []
    odustalo = sorted(ODUSTALO.iterdir()) if ODUSTALO.is_dir() else []
    izvestaji = sorted(KOREN.glob("*.md")) if KOREN.is_dir() else []

    print(f"чека у реду: {len(cekaju)}")
    for s in cekaju:
        pok = s.read_text().strip().split("=")[-1]
        print(f"  {s.name}  (покушаја: {pok})")
    if odustalo:
        print(f"одустало: {len(odustalo)}")
        for s in odustalo:
            print(f"  {s.name}")
    print(f"извештаја: {len([i for i in izvestaji if i.name != 'PREGLED.md'])}")
    print(f"\nСтање рецензената:")
    subprocess.run([python(), str(RECENZIJA), "--stanje"], cwd=REPO)
    return 0


def main() -> int:
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    naredba = sys.argv[1]
    if naredba == "dodaj":
        if len(sys.argv) < 3:
            print("недостаје hash", file=sys.stderr)
            return 2
        return dodaj(sys.argv[2])
    if naredba == "obradi":
        return obradi()
    if naredba == "pregled":
        return pregled()
    print(f"непозната наредба: {naredba}", file=sys.stderr)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
