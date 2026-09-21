"""У шаблонима ниједан сабирак не сме да буде голо поље из базе.

21.09.2026: `book.title + \x27 \x27 + book.author` је оборио /admin/library_database
(`TypeError: can only concatenate str (not "NoneType") to str`) чим се појавио
зборник без аутора. `finalize` не помаже — он ради тек над резултатом израза,
а израз пукне раније. Зато правило: сваки сабирак који је поље (`x.y`) мора
имати заштиту — `(x.y or \x27\x27)`, `(x.y or 0)` или `|default(...)`.
"""
import glob
import re
import unittest

IZRAZ = re.compile(r"\{\{(.*?)\}\}", re.S)
OPERAND = r"""(?:[\w\.]+|\([^()]*\)|'[^']*'|\"[^\"]*\")"""
PAR = re.compile("(" + OPERAND + r")\s*\+\s*(" + OPERAND + ")")
BROJ = re.compile(r"^[\d\.]+$")


def nalazi():
    problemi = []
    for putanja in sorted(glob.glob("templates/**/*.html", recursive=True)):
        tekst = open(putanja, encoding="utf-8", errors="replace").read()
        for m in IZRAZ.finditer(tekst):
            izraz = m.group(1)
            if "+" not in izraz:
                continue
            for operandi in PAR.findall(izraz):
                for operand in operandi:
                    if operand.startswith("(") or BROJ.match(operand):
                        continue
                    if "." in operand:
                        red = tekst[: m.start()].count("\n") + 1
                        problemi.append((putanja, red, operand, " ".join(izraz.split())[:90]))
    return problemi


class ZbirBezNoneTest(unittest.TestCase):
    def test_nema_golog_sabirka_iz_baze(self):
        problemi = nalazi()
        poruka = "\n".join(
            f"  {p}:{r}  голо поље `{o}` у изразу: {{{{ {i} }}}}" for p, r, o, i in problemi
        )
        self.assertEqual(
            problemi,
            [],
            "Незаштићен сабирак у шаблону (NULL из базе обара страну):\n" + poruka,
        )

    def test_provera_zaista_hvata_obrazac(self):
        """Да тест не би тихо прошао ако се регуларни израз поквари."""
        import tempfile, os, shutil
        d = tempfile.mkdtemp()
        try:
            os.makedirs(os.path.join(d, "templates"))
            sa = os.path.join(d, "templates", "x.html")
            open(sa, "w", encoding="utf-8").write("{{ book.title + \x27 \x27 + book.author }}")
            staro = os.getcwd()
            os.chdir(d)
            try:
                self.assertTrue(nalazi(), "образац више не бива откривен")
            finally:
                os.chdir(staro)
        finally:
            shutil.rmtree(d)


if __name__ == "__main__":
    unittest.main()
