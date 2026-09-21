"""NULL из базе не сме да се испише као „None“ ни да обори шаблон.

Регресија 21.09.2026 — /admin/library_database је враћао 500 због
`book.title + \x27 \x27 + book.author` где је аутор NULL.
"""
import os
import unittest

os.environ.setdefault("FLASK_ENV", "testing")
os.environ.setdefault("SECRET_KEY", "test-secret")
os.environ.setdefault("REDIS_URL", "")
os.environ.setdefault("SESSION_TYPE", "filesystem")
os.environ.setdefault("SESSION_FILE_DIR", "logs/qa_flask_session")

import app as museum_app  # noqa: E402


def _render(izvor, **ctx):
    with museum_app.app.test_request_context("/"):
        return museum_app.app.jinja_env.from_string(izvor).render(**ctx)


class FinalizeTest(unittest.TestCase):
    def test_none_se_ne_ispisuje(self):
        self.assertEqual(_render("[{{ x }}]", x=None), "[]")

    def test_konkatenacija_sa_none_i_dalje_puca(self):
        """finalize ради тек над РЕЗУЛТАТОМ израза, па `a + b` пукне раније.
        Зато конкатенацију чува посебан тест: test_sabloni_zbir_bez_none.py."""
        with self.assertRaises(TypeError):
            _render("{{ a + ' ' + b }}", a="Зборник", b=None)

    def test_atribut_koji_ne_postoji_i_dalje_puca_glasno(self):
        """Undefined остаје Undefined — finalize не сме да сакрије грешку у имену."""
        from jinja2 import UndefinedError
        with self.assertRaises(UndefinedError):
            _render("{{ nepoznato.polje }}")

    def test_nula_i_prazan_string_prolaze_nepромењени(self):
        self.assertEqual(_render("[{{ x }}][{{ y }}]", x=0, y=False), "[0][False]")


if __name__ == "__main__":
    unittest.main()
