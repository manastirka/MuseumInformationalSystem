#!/usr/bin/env python3
"""Оркестратор рецензије кода — Claude, Codex и Grok, по расположивости.

ЗАШТО РЕД А НЕ БАЛАНСЕР
    Приступ иде преко претплата, не API кључева. Лимити се ресетују по
    прозорима. Рецензија није хитна — стиже после merge-а, нико је не чека.
    Зато: ако је бољи рецензент тренутно потрошен, БОЉЕ ЈЕ САЧЕКАТИ његов
    прозор него сад добити слабију рецензију. Балансер деградира квалитет,
    ред само касни.

    Отуд: ако су сви рецензенти потрошени, овај програм НЕ пада на локални
    модел и НЕ прећуткује — врати излазни кôд 75 (EX_TEMPFAIL) и остави
    задатак у реду. Тајмер га покупи касније.

ЧИТА, НЕ ПИШЕ
    Сваки рецензент се покреће у режиму само за читање. По правилу пројекта,
    Grok и Codex не мењају продукцијски код — ни овде.

УПОТРЕБА
    python3 scripts/review/recenzija.py                     # последњи merge на main
    python3 scripts/review/recenzija.py --opseg HEAD~3..HEAD
    python3 scripts/review/recenzija.py --broj 2            # траже се 2 независне
    python3 scripts/review/recenzija.py --stanje            # ко је слободан
"""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
STANJE = Path.home() / ".mis-recenzija-stanje.json"
IZVESTAJI = Path.home() / "recenzije"

# Колико дуго рецензент „хлади" после сваке врсте неуспеха.
HLADJENJE_LIMIT = 60 * 60      # потрошен лимит — цео сат
HLADJENJE_GRESKA = 10 * 60     # непозната грешка — десет минута

# Обрасци по којима се препознаје да је лимит потрошен, а не да је код лош.
OBRASCI_LIMITA = [
    r"credit balance", r"rate.?limit", r"usage limit", r"quota",
    r"\b429\b", r"too many requests", r"overloaded", r"capacity",
    r"insufficient", r"plan limit", r"try again (later|in)",
]

UPUTSTVO = """Прегледај измене у гиту наведене испод и пријави САМО стварне
проблеме. За сваки налаз дај: фајл и линију, шта тачно не ваља, и конкретан
сценарио у ком пуца (који улаз → који погрешан исход).

Тражи посебно:
- тихо гутање грешака (упис падне, корисник види поруку о успеху)
- паралелни извор истине (фајл/кеш поред базе)
- SQL који даје погрешне бројеве после JOIN-а
- тест који проверава статус 200 уместо стварног стања базе
- хардкодоване путање, кориснике и боје ван токена тема

Ако немаш налаз, напиши тачно: НЕМА НАЛАЗА.
Не предлажи козметику и не преписуј код који ради."""


def sada() -> int:
    return int(time.time())


def ucitaj_stanje() -> dict:
    if STANJE.is_file():
        try:
            return json.loads(STANJE.read_text())
        except Exception:
            pass
    return {}


def upisi_stanje(s: dict) -> None:
    STANJE.write_text(json.dumps(s, ensure_ascii=False, indent=1))


def je_limit(tekst: str) -> bool:
    t = (tekst or "").lower()
    return any(re.search(o, t) for o in OBRASCI_LIMITA)


# --------------------------------------------------------------- рецензенти
def pokreni(cmd: list[str], cwd: Path, timeout: int, kroz_tmux: bool = False,
            ulaz: str | None = None):
    """Врати (returncode, stdout+stderr). Grok тражи да постоји контролни
    терминал а да излаз иде у фајл — зато иде кроз tmux."""
    if kroz_tmux:
        ime = f"recenzija-{sada()}"
        izlaz = Path(f"/tmp/{ime}.out")
        unutra = " ".join(f"'{c}'" if " " in c else c for c in cmd)
        subprocess.run(
            ["tmux", "new-session", "-d", "-s", ime,
             f"{unutra} > {izlaz} 2>&1; echo IZLAZNI_KOD=$? >> {izlaz}"],
            cwd=cwd, check=False,
        )
        kraj = time.time() + timeout
        while time.time() < kraj:
            time.sleep(3)
            if izlaz.is_file() and "IZLAZNI_KOD=" in izlaz.read_text(errors="replace"):
                break
        subprocess.run(["tmux", "kill-session", "-t", ime],
                       check=False, capture_output=True)
        tekst = izlaz.read_text(errors="replace") if izlaz.is_file() else ""
        m = re.search(r"IZLAZNI_KOD=(\d+)", tekst)
        return (int(m.group(1)) if m else 124), tekst
    # `stdin=DEVNULL` остаје подразумевано (codex иначе поједе улаз
    # позиваоца), али кад промпт иде кроз stdin, шаље се овуда.
    p = subprocess.run(
        cmd, cwd=cwd, capture_output=True, text=True, timeout=timeout,
        input=ulaz, stdin=None if ulaz is not None else subprocess.DEVNULL)
    return p.returncode, (p.stdout or "") + (p.stderr or "")


# ARG_MAX: цео diff иде у промпт, а `execve` има горњу границу за све
# аргументе заједно. Мерџ `a507044` је дао diff од 549 KB и `claude` је падао
# са `OSError: [Errno 7] Argument list too long` — ШЕСТ пута заредом, а нигде
# трага, јер ред одустаје тек после 20 покушаја. Промпт зато иде кроз stdin.
def recenzent_claude(prompt: str, timeout: int):
    kod, izlaz = pokreni(
        ["claude", "-p", "--output-format", "json"], REPO, timeout,
        ulaz=prompt)
    try:
        d = json.loads(izlaz[izlaz.index("{"):izlaz.rindex("}") + 1])
        if d.get("is_error"):
            return None, str(d.get("result", ""))[:400]
        return str(d.get("result", "")).strip(), None
    except Exception:
        return (None, izlaz[-400:]) if kod else (izlaz.strip(), None)


def recenzent_codex(prompt: str, timeout: int):
    out = Path(f"/tmp/codex-recenzija-{sada()}.txt")
    kod, izlaz = pokreni(
        ["codex", "exec", "--sandbox", "read-only", "-o", str(out), "-"],
        REPO, timeout, ulaz=prompt)
    if kod == 0 and out.is_file():
        return out.read_text(errors="replace").strip(), None
    return None, izlaz[-400:]


def recenzent_grok(prompt: str, timeout: int):
    pf = Path(f"/tmp/grok-prompt-{sada()}.txt")
    pf.write_text(prompt, encoding="utf-8")
    kod, izlaz = pokreni(
        ["grok", "--output-format", "json", "--prompt-file", str(pf),
         "--sandbox", "read-only"], REPO, timeout, kroz_tmux=True)
    if kod != 0:
        return None, izlaz[-400:]
    try:
        d = json.loads(izlaz[izlaz.index("{"):izlaz.rindex("}") + 1])
        for k in ("result", "text", "message", "output"):
            if d.get(k):
                return str(d[k]).strip(), None
        return json.dumps(d, ensure_ascii=False)[:4000], None
    except Exception:
        return izlaz.strip()[:4000], None


RECENZENTI = {
    "claude": recenzent_claude,
    "codex": recenzent_codex,
    "grok": recenzent_grok,
}
PODRAZUMEVANI_RED = ["claude", "codex", "grok"]


# --------------------------------------------------------------------- git
def git(*a) -> str:
    return subprocess.run(["git", *a], cwd=REPO, capture_output=True,
                          text=True).stdout.strip()


def opseg_postoji(opseg: str) -> bool:
    """Да ли git уме да разреши оба краја опсега.

    Битно: `git()` намерно чита само stdout, па нераздрешив опсег даје празан
    стринг који је до 16.08.2026 изгледао исто као „нема шта да се прегледа".
    Због тога је `red.py` брисао ставку из реда и уписивао „готово" за merge
    који никад није прегледан. Отуд ова изричита провера.
    """
    for kraj in [k for k in opseg.split("..") if k]:
        p = subprocess.run(["git", "rev-parse", "--verify", "--quiet", kraj + "^{commit}"],
                           cwd=REPO, capture_output=True, text=True)
        if p.returncode != 0:
            return False
    return True


def podrazumevani_opseg() -> str:
    """Последњи merge на main — то је оно што треба прегледати."""
    h = git("log", "--merges", "-1", "--format=%H")
    return f"{h}^..{h}" if h else "HEAD~1..HEAD"


# Измене које не траже рецензију. НАМЕРНО правило, не модел: одлуку „да ли
# ово треба прегледати" не сме да доноси ништа што уме да погреши, иначе се
# рецензија тихо не уради. Локални модели су мерено непоуздани (види
# MIS/poredjenje-modela.md) и овде немају шта да траже.
TRIVIJALNI_NASTAVCI = {".md", ".txt", ".rst"}
TRIVIJALNI_DIREKTORIJUMI = ("docs/", "docs_archive/")


def je_trivijalno(opseg: str) -> str | None:
    """Врати разлог за прескакање, или None ако рецензија треба."""
    fajlovi = [f for f in git("diff", "--name-only", opseg).splitlines() if f]
    if not fajlovi:
        return None
    for f in fajlovi:
        nastavak = "." + f.rsplit(".", 1)[-1] if "." in f else ""
        if nastavak in TRIVIJALNI_NASTAVCI:
            continue
        if any(f.startswith(d) for d in TRIVIJALNI_DIREKTORIJUMI):
            continue
        return None
    return f"мењано само {len(fajlovi)} документационих фајлова"


def napravi_prompt(opseg: str) -> tuple[str, str]:
    komiti = git("log", "--format=%h %s", opseg)
    fajlovi = git("diff", "--stat", opseg)
    diff = git("diff", opseg)
    if len(diff) > 120_000:
        diff = diff[:120_000] + "\n\n[…diff скраћен на 120 000 знакова…]"
    telo = (f"{UPUTSTVO}\n\n=== КОМИТИ ({opseg}) ===\n{komiti}\n\n"
            f"=== ИЗМЕЊЕНИ ФАЈЛОВИ ===\n{fajlovi}\n\n=== DIFF ===\n{diff}\n")
    return telo, komiti


# -------------------------------------------------------------------- главни
def prikazi_stanje() -> int:
    s, t = ucitaj_stanje(), sada()
    print(f"{'рецензент':<10} {'стање':<12} разлог")
    for ime in PODRAZUMEVANI_RED:
        r = s.get(ime, {})
        do = r.get("hladan_do", 0)
        if do > t:
            print(f"{ime:<10} {'хлади ' + str((do - t) // 60) + ' min':<12} "
                  f"{r.get('razlog', '')[:70]}")
        else:
            print(f"{ime:<10} {'слободан':<12}")
    return 0


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--opseg", default=None, help="git опсег (подр. последњи merge)")
    p.add_argument("--red", default=",".join(PODRAZUMEVANI_RED),
                   help="редослед рецензената, зарезом")
    p.add_argument("--broj", type=int, default=1,
                   help="колико независних рецензија је потребно")
    p.add_argument("--timeout", type=int, default=900, help="секунди по рецензенту")
    p.add_argument("--stanje", action="store_true", help="само прикажи ко је слободан")
    p.add_argument("--svakako", action="store_true",
                   help="прегледај и кад су мењани само документациони фајлови")
    a = p.parse_args()

    if a.stanje:
        return prikazi_stanje()

    opseg = a.opseg or podrazumevani_opseg()

    if not opseg_postoji(opseg):
        print(f"Опсег {opseg} се не може разрешити — коммит не постоји у овом "
              f"клону. Ово НИЈЕ „нема шта да се прегледа”.", file=sys.stderr)
        return 2

    prompt, komiti = napravi_prompt(opseg)
    if not komiti:
        print(f"Нема коммита у опсегу {opseg} — нема шта да се прегледа.")
        return 0

    if not a.svakako and (razlog := je_trivijalno(opseg)):
        print(f"Прескачем {opseg}: {razlog}.")
        print("Квота фронтир модела се чува за измене кода. "
              "Форсирај са --svakako ако ипак хоћеш рецензију.")
        return 0

    stanje = ucitaj_stanje()
    IZVESTAJI.mkdir(exist_ok=True)
    nalazi, preskoceni = [], []

    for ime in [x.strip() for x in a.red.split(",") if x.strip() in RECENZENTI]:
        if len(nalazi) >= a.broj:
            break
        r = stanje.get(ime, {})
        if r.get("hladan_do", 0) > sada():
            preskoceni.append(f"{ime} (хлади још {(r['hladan_do'] - sada()) // 60} min)")
            continue

        print(f"→ {ime} …", flush=True)
        t0 = time.time()
        try:
            tekst, greska = RECENZENTI[ime](prompt, a.timeout)
        except subprocess.TimeoutExpired:
            tekst, greska = None, f"истекло после {a.timeout}s"

        if tekst:
            print(f"  {ime}: готово за {time.time() - t0:.0f}s")
            nalazi.append((ime, tekst))
            stanje.pop(ime, None)
        else:
            limit = je_limit(greska or "")
            stanje[ime] = {
                "hladan_do": sada() + (HLADJENJE_LIMIT if limit else HLADJENJE_GRESKA),
                "razlog": ("лимит: " if limit else "грешка: ") + (greska or "")[:200],
            }
            print(f"  {ime}: {'ЛИМИТ' if limit else 'ГРЕШКА'} → "
                  f"хлади {(HLADJENJE_LIMIT if limit else HLADJENJE_GRESKA) // 60} min")
        upisi_stanje(stanje)

    if not nalazi:
        print("\nНиједан рецензент није био расположив.")
        if preskoceni:
            print("  прескочени: " + ", ".join(preskoceni))
        print("Рецензија ОСТАЈЕ У РЕДУ — не пада се на слабији модел.")
        return 75  # EX_TEMPFAIL: тајмер нека покуша поново

    oznaka = git("rev-parse", "--short", opseg.split("..")[-1] or "HEAD")
    put = IZVESTAJI / f"{oznaka}.md"
    delovi = [f"# Рецензија {opseg}\n", f"Коммити:\n```\n{komiti}\n```\n"]
    for ime, tekst in nalazi:
        delovi.append(f"\n## {ime}\n\n{tekst}\n")
    if preskoceni:
        delovi.append("\n---\nНису учествовали: " + ", ".join(preskoceni) + "\n")
    put.write_text("".join(delovi), encoding="utf-8")

    print(f"\nИзвештај: {put}")
    for ime, tekst in nalazi:
        prazno = "НЕМА НАЛАЗА" in tekst.upper()
        print(f"  {ime}: {'без налаза' if prazno else str(len(tekst)) + ' знакова налаза'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
