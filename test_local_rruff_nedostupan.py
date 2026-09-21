"""Кад локални RRUFF скуп не постоји на серверу, руте не смеју да враћају 500.

Продукција 04.09.2026: `/api/local_rruff/Sfalerit sa kvarcom` → 500,
`[Errno 2] No such file or directory: \x27/opt/mis/app/RRUFF_data\x27`.
Фасцикла је у .gitignore и постоји само на dev машини; одсуство необавезних
података није грешка сервера.
"""
import json
import os
import unittest
from unittest.mock import patch

os.environ.setdefault("FLASK_ENV", "testing")
os.environ.setdefault("SECRET_KEY", "test-secret")
os.environ.setdefault("REDIS_URL", "")
os.environ.setdefault("SESSION_TYPE", "filesystem")
os.environ.setdefault("SESSION_FILE_DIR", "logs/qa_flask_session")

import app as museum_app  # noqa: E402
import local_rruff_data  # noqa: E402
import mineral_science_views  # noqa: E402


class BezRruffSkupaTest(unittest.TestCase):
    def test_objekat_se_pravi_bez_izuzetka(self):
        rruff = local_rruff_data.LocalRRUFFData("/nepostojeca/putanja/RRUFF_data")
        self.assertFalse(rruff.available)
        self.assertIsNone(rruff.get_mineral_data("Quartz"))

    def _odgovor(self, poziv):
        class Prazan:
            available = False

            def __init__(self, *a, **kw):
                pass

        with patch.object(local_rruff_data, "LocalRRUFFData", Prazan):
            with museum_app.app.test_request_context("/api/local_rruff/Kvarc"):
                return poziv()

    def test_rute_vracaju_200_sa_jasnom_porukom(self):
        pozivi = {
            "data": lambda: mineral_science_views.api_get_local_rruff_data("Кварц"),
            "dif": lambda: mineral_science_views.api_get_local_rruff_dif("Кварц"),
            "cif": lambda: mineral_science_views.api_get_local_rruff_cif("Кварц"),
            "spectrum": lambda: mineral_science_views.api_get_local_rruff_spectrum("raman", "Кварц"),
            "powder_xy": lambda: mineral_science_views.api_get_local_rruff_powder_xy("Кварц"),
        }
        for ime, poziv in pozivi.items():
            with self.subTest(ruta=ime):
                odgovor = self._odgovor(poziv)
                status = odgovor[1] if isinstance(odgovor, tuple) else 200
                telo = odgovor[0] if isinstance(odgovor, tuple) else odgovor
                self.assertEqual(status, 200, ime)
                podaci = json.loads(telo.get_data(as_text=True))
                self.assertFalse(podaci["success"])
                self.assertFalse(podaci["available"])
                self.assertIn("RRUFF", podaci["message"])


if __name__ == "__main__":
    unittest.main()
