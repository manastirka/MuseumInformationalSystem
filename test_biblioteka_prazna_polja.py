"""База библиотеке: књиге без аутора/наслова не смеју да руше страну (500).

Регресија 21.09.2026 — зборници без именованог аутора (author IS NULL)
рушили су /admin/library_database кроз конкатенацију у data-search-text.
"""
import os
import unittest

os.environ.setdefault("FLASK_ENV", "testing")
os.environ.setdefault("SECRET_KEY", "test-secret")
os.environ.setdefault("REDIS_URL", "")
os.environ.setdefault("SESSION_TYPE", "filesystem")
os.environ.setdefault("SESSION_FILE_DIR", "logs/qa_flask_session")

import app as museum_app  # noqa: E402
import dashboard_integration_views  # noqa: E402


def _knjiga(**kw):
    osnova = {
        "id": 1,
        "title": "ЗБОРНИК радова",
        "author": None,
        "isbn": None,
        "publisher": None,
        "publication_year": None,
        "category": "Зоологија",
        "subcategory": None,
        "language": None,
        "pages": None,
        "format": None,
        "location": None,
        "shelf_number": None,
        "status": "доступна",
        "description": None,
        "notes": None,
        "keywords": [],
        "detailed_info": None,
    }
    osnova.update(kw)
    return osnova


class BibliotekaPraznaPoljaTest(unittest.TestCase):
    def _render(self, knjige):
        baza = {
            "books": knjige,
            "categories": ["Зоологија"],
            "statistics": {"total_books": len(knjige), "available_books": 0,
                           "borrowed_books": 0, "total_categories": 1},
        }
        with museum_app.app.test_request_context("/admin/library_database"):
            return dashboard_integration_views.render_library_database(
                get_library_database=lambda: baza,
            )

    def test_bez_autora_ne_rusi_stranu(self):
        html = self._render([_knjiga()])
        self.assertIn("зборник радова", html.lower())
        self.assertNotIn(">None<", html)

    def test_sva_opciona_polja_prazna(self):
        html = self._render([_knjiga(title=None, category=None, status=None)])
        self.assertIn("data-search-text=", html)


if __name__ == "__main__":
    unittest.main()
