#!/usr/bin/env python3
"""Обрада текста — само преобликовање онога што му се да.

ИСТОРИЈА
    16.08.2026. овај алат је радио над локалним моделима (Qwen3.8-27B,
    Gemma 4 31B) на кућној машини. Мерење на осам питања дало је:
    Luna 4/4 и 3/3, Gemma 3/4 и 3/3, Qwen 1/4 и 1/3. Luna је уз то била
    једина тачна на „чему служи Мосова скала", где су оба локална модела
    самоуверено измислила потпуно нетачан одговор.
    Локални модели су зато уклоњени, а мотор пребачен на Luna.

    Цена тога: више ништа не ради без изласка података са машине. Ако икад
    затреба обрада којој подаци не смеју напоље, локални пут се враћа —
    инсталација Ollama-е и преузимање модела траје неколико минута,
    поступак је у пројектној меморији.

ОГРАДА ЈЕ ОСТАЛА
    Модел је бољи, али и даље није извор податка — само алат над податком.
    Програм ОДБИЈА рад без улазног текста, па отворено питање не може ни да
    се постави. Упутство му забрањује допуњавање из сопственог знања: ако
    податак не постоји у улазу, мора да напише НЕДОСТАЈЕ ПОДАТАК.

МОТОР
    GPT-5.6 Luna кроз Codex CLI, дакле кроз ПОСТОЈЕЋУ претплату — не тражи
    ниједан нови кључ. `< /dev/null` је обавезан: codex чита stdin, па би
    иначе појео улаз позиваоца.

УПОТРЕБА
    cat opis.txt | python3 scripts/tekst/obrada.py sredi
    python3 scripts/tekst/obrada.py izvuci --ulaz etiketa.txt
    python3 scripts/tekst/obrada.py --zadaci
"""
from __future__ import annotations

import argparse
import os
import subprocess
import sys
import tempfile
from pathlib import Path

MODEL = os.environ.get("MIS_MODEL", "gpt-5.6-luna")
NAPOR = os.environ.get("MIS_NAPOR", "medium")

OGRADA = (
    "Радиш ИСКЉУЧИВО над текстом који ти је дат испод ознаке ТЕКСТ. "
    "Немој да допуњујеш, тумачиш нити исправљаш садржај из свог знања. "
    "Ако задатак тражи податак који не постоји у датом тексту, напиши тачно: "
    "НЕДОСТАЈЕ ПОДАТАК — и ништа више. "
    "Не додајеш уводне реченице. Враћаш само резултат, без markdown ограде."
)

ZADACI = {
    "preslovi": ("ћирилица ↔ латиница, без икакве друге измене",
                 "Пресловi текст у друго писмо. Не мењај ниједну реч, ред "
                 "речи, интерпункцију ни велика слова."),
    "sredi": ("исправка куцања, размака и великих слова — садржај се НЕ дира",
              "Исправи словне грешке, двоструке размаке, мешање писама и "
              "велика слова. Немој да мењаш ниједну чињеницу, број, име ни "
              "редослед реченица. Ако ниси сигуран да је нешто грешка у "
              "куцању — остави како јесте."),
    "sazmi": ("сажимање датог текста, без нових тврдњи",
              "Сажми текст на највише трећину дужине. Сваку тврдњу у сажетку "
              "мора да покрива дати текст. Ништа не додајеш."),
    "izvuci": ("извлачење поља из текста у JSON",
               "Извуци поља и врати ИСКЉУЧИВО JSON. Поља: naziv, lokalitet, "
               "dimenzije, inventarski_broj, napomena. За свако поље којег "
               "нема у тексту стави null. Ништа не изводиш и не погађаш."),
}

ODBIJENO = {
    "pitanje": "отворено питање — овај алат само преобликује дати текст",
    "kod": "суд о коду — иде на scripts/review/recenzija.py",
    "recenzija": "рецензија — иде на scripts/review/recenzija.py",
    "cinjenica": "провера чињенице — не преко овог алата",
}


def zovi(uputstvo: str, tekst: str, timeout: int) -> str:
    prompt = f"{OGRADA}\n\nЗАДАТАК: {uputstvo}\n\nТЕКСТ:\n{tekst}"
    with tempfile.TemporaryDirectory() as radni:
        izlaz = Path(radni) / "izlaz.txt"
        p = subprocess.run(
            ["codex", "exec", "--skip-git-repo-check", "--sandbox", "read-only",
             "-c", f'model="{MODEL}"', "-c", f'model_reasoning_effort="{NAPOR}"',
             "-o", str(izlaz), prompt],
            cwd=radni, capture_output=True, text=True, timeout=timeout,
            stdin=subprocess.DEVNULL,  # без овога codex поједе улаз позиваоца
        )
        if izlaz.is_file():
            return izlaz.read_text(encoding="utf-8").strip()
        raise RuntimeError((p.stderr or p.stdout or "непознат неуспех")[-300:])


def main() -> int:
    p = argparse.ArgumentParser(
        description="Обрада текста — само преобликовање датог текста.",
        epilog="Отворена питања и суд о коду овде НЕ иду — види --zadaci.")
    p.add_argument("zadatak", nargs="?", help=" | ".join(ZADACI))
    p.add_argument("--ulaz", help="фајл са текстом (иначе се чита stdin)")
    p.add_argument("--timeout", type=int, default=300)
    p.add_argument("--zadaci", action="store_true", help="шта све уме")
    a = p.parse_args()

    if a.zadaci or not a.zadatak:
        print(f"Мотор: {MODEL} (кроз Codex претплату, без API кључа)\n")
        print("Дозвољени задаци:")
        for ime, (opis, _) in ZADACI.items():
            print(f"  {ime:<10} {opis}")
        print("\nОдбијено, и куда иде уместо тога:")
        for ime, zasto in ODBIJENO.items():
            print(f"  {ime:<10} {zasto}")
        return 0

    if a.zadatak in ODBIJENO:
        print(f"ОДБИЈЕНО: {ODBIJENO[a.zadatak]}", file=sys.stderr)
        return 2
    if a.zadatak not in ZADACI:
        print(f"ОДБИЈЕНО: непознат задатак. Дозвољено: {', '.join(ZADACI)}",
              file=sys.stderr)
        return 2

    tekst = (open(a.ulaz, encoding="utf-8").read() if a.ulaz
             else ("" if sys.stdin.isatty() else sys.stdin.read()))
    if not tekst.strip():
        # ОГРАДА: без улазног текста нема посла. Отворено питање не може ни
        # да се постави — то је цела поента.
        print("ОДБИЈЕНО: нема улазног текста.\n"
              "Овај алат само преобликује текст који му се да — не одговара "
              "на питања. Дај текст кроз --ulaz или stdin.", file=sys.stderr)
        return 2

    try:
        print(zovi(ZADACI[a.zadatak][1], tekst, a.timeout))
    except subprocess.TimeoutExpired:
        print(f"Истекло после {a.timeout}s.", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Неуспех: {e}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
