#!/usr/bin/env python3
"""Локални модел — само преобликовање текста који му се да.

ЗАШТО ОГРАДА
    Мерење 16.08.2026 (види MIS/poredjenje-modela.md): од осам питања, на
    четири је бар један локални модел одговорио самоуверено и НЕТАЧНО.
    Qwen је дао SQL који изгледа исправно а надувава број запослених.
    Обе моделе питање „чему служи Мосова скала" одвело је у потпуну измишљотину.

    Закључак: локални модел не сме да буде ИЗВОР податка. Може да буде
    само АЛАТ над податком који му дамо.

ШТА ОГРАДА ЗНАЧИ У ПРАКСИ
    Овај програм ОДБИЈА да ради без улазног текста. Не може му се поставити
    отворено питање. Сваки задатак је облика „ево текста, преобликуј га":
    пресловљавање, сређивање, сажимање, извлачење поља.

    Системски промпт му забрањује да допуњује из свог знања: ако податак не
    постоји у улазу, мора да напише НЕДОСТАЈЕ ПОДАТАК уместо да измисли.

ШТА ОВО НИЈЕ
    Није рецензент кода. Није извор чињеница о минералима. Није замена за
    фронтир моделе. Ако ти треба суд о коду или провера чињенице — иде на
    `scripts/review/recenzija.py`, не овде.

УПОТРЕБА
    cat opis.txt | python3 scripts/lokalni/lokalni.py sredi
    python3 scripts/lokalni/lokalni.py preslovi --ulaz opis.txt
    python3 scripts/lokalni/lokalni.py izvuci --ulaz etiketa.txt
    python3 scripts/lokalni/lokalni.py --zadaci        # шта све уме
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.request

OLLAMA = os.environ.get("MIS_OLLAMA", "http://127.0.0.1:11434")

# Gemma је тачнија (мерено 3/4 наспрам 1/4 на стручним питањима), Qwen 2.3×
# бржи. За послове где тачност значи — Gemma. За чисто механичке — Qwen.
GEMMA = "hf.co/bartowski/google_gemma-4-31B-it-GGUF:Q4_K_M"
QWEN = "qwen3.8-27b"

OGRADA = (
    "Радиш ИСКЉУЧИВО над текстом који ти је дат испод. "
    "Немој да допуњујеш, тумачиш нити исправљаш садржај из свог знања. "
    "Ако задатак тражи податак који не постоји у датом тексту, напиши тачно: "
    "НЕДОСТАЈЕ ПОДАТАК — и ништа више. "
    "Не додајеш уводне реченице типа „Ево резултата”. Враћаш само резултат."
)

ZADACI = {
    "preslovi": {
        "opis": "ћирилица ↔ латиница, без икакве друге измене",
        "model": QWEN,
        "uputstvo": "Пресловi текст у друго писмо. Не мењај ниједну реч, "
                    "ред речи, интерпункцију ни велика слова.",
    },
    "sredi": {
        "opis": "исправка куцања, размака и великих слова — садржај се НЕ дира",
        "model": GEMMA,
        "uputstvo": "Исправи словне грешке, двоструке размаке, мешање писама "
                    "и велика слова. Немој да мењаш ниједну чињеницу, број, "
                    "име ни редослед реченица. Ако ниси сигуран да је нешто "
                    "грешка у куцању — остави како јесте.",
    },
    "sazmi": {
        "opis": "сажимање датог текста, без нових тврдњи",
        "model": GEMMA,
        "uputstvo": "Сажми текст на највише трећину дужине. Сваку тврдњу у "
                    "сажетку мора да покрива дати текст. Ништа не додајеш.",
    },
    "izvuci": {
        "opis": "извлачење поља из текста у JSON",
        "model": GEMMA,
        "uputstvo": "Извуци поља и врати ИСКЉУЧИВО JSON, без markdown ограде. "
                    "Поља: naziv, lokalitet, dimenzije, inventarski_broj, "
                    "napomena. За свако поље којег нема у тексту стави null. "
                    "Ништа не изводиш и не погађаш.",
    },
}

# Задаци који НИСУ дозвољени, са објашњењем куда иду уместо тога.
ODBIJENO = {
    "pitanje": "отворено питање — локални модел је мерено нетачан; питај "
               "фронтир модел",
    "kod": "суд о коду — иде на scripts/review/recenzija.py",
    "recenzija": "рецензија — иде на scripts/review/recenzija.py",
    "cinjenica": "провера чињенице — локални модел измишља; не користи га за то",
}


def zovi(model: str, sistem: str, tekst: str, timeout: int) -> str:
    telo = json.dumps({
        "model": model,
        "system": OGRADA + " " + sistem,
        "prompt": tekst,
        "think": False,
        "stream": False,
        # ниска температура: посао је механички, не тражи маштовитост
        "options": {"temperature": 0.2},
    }).encode()
    req = urllib.request.Request(f"{OLLAMA}/api/generate", data=telo,
                                 headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.load(r).get("response", "").strip()


def main() -> int:
    p = argparse.ArgumentParser(
        description="Локални модел — само преобликовање датог текста.",
        epilog="Отворена питања и суд о коду овде НЕ иду — види --zadaci.")
    p.add_argument("zadatak", nargs="?", help="preslovi | sredi | sazmi | izvuci")
    p.add_argument("--ulaz", help="фајл са текстом (иначе се чита stdin)")
    p.add_argument("--model", choices=["gemma", "qwen"],
                   help="преклопи подразумевани модел за задатак")
    p.add_argument("--timeout", type=int, default=300)
    p.add_argument("--zadaci", action="store_true", help="шта све уме")
    a = p.parse_args()

    if a.zadaci or not a.zadatak:
        print("Дозвољени задаци:")
        for ime, z in ZADACI.items():
            print(f"  {ime:<10} {z['opis']}")
            print(f"{'':<12}модел: {'Gemma 4' if z['model'] == GEMMA else 'Qwen 3.8'}")
        print("\nОдбијено, и куда иде уместо тога:")
        for ime, zasto in ODBIJENO.items():
            print(f"  {ime:<10} {zasto}")
        return 0

    if a.zadatak in ODBIJENO:
        print(f"ОДБИЈЕНО: {ODBIJENO[a.zadatak]}", file=sys.stderr)
        return 2
    if a.zadatak not in ZADACI:
        print(f"ОДБИЈЕНО: непознат задатак „{a.zadatak}”. "
              f"Дозвољено: {', '.join(ZADACI)}", file=sys.stderr)
        return 2

    tekst = (open(a.ulaz, encoding="utf-8").read() if a.ulaz
             else ("" if sys.stdin.isatty() else sys.stdin.read()))
    if not tekst.strip():
        # ОВО је ограда: без улазног текста нема посла. Отворено питање
        # не може ни да се постави.
        print("ОДБИЈЕНО: нема улазног текста.\n"
              "Овај алат само преобликује текст који му се да — не одговара "
              "на питања. Дај текст кроз --ulaz или stdin.", file=sys.stderr)
        return 2

    z = ZADACI[a.zadatak]
    model = {"gemma": GEMMA, "qwen": QWEN}.get(a.model or "", z["model"])
    try:
        print(zovi(model, z["uputstvo"], tekst, a.timeout))
    except urllib.error.URLError as e:
        print(f"Локални модел није доступан на {OLLAMA}: {e}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
