#!/usr/bin/env python3
"""Фототека је једини систем за слике предмета — стари batch upload је уклоњен.

Покрива три ствари:
  1. предмет без фотографије даје уредан плацехолдер, без грешке;
  2. старе руте (batch upload, image_api) враћају 404;
  3. фототека ток је нетакнут (регресија).
"""

import os
import unittest
from pathlib import Path
from unittest.mock import patch

os.environ.setdefault('FLASK_ENV', 'testing')
os.environ.setdefault('SECRET_KEY', 'test-secret')
os.environ.setdefault('REDIS_URL', '')
os.environ.setdefault('SESSION_TYPE', 'filesystem')
os.environ.setdefault('SESSION_FILE_DIR', '/tmp/museum-test-flask-session')

import app as museum_app
import collection_media_views


class PredmetBezFotografijeTests(unittest.TestCase):
    """Предмет без фототека фотографије -> плацехолдер, никад грешка."""

    def setUp(self):
        self.client = museum_app.app.test_client()
        self.base_url = 'https://localhost'

    def _login(self, *, role='admin'):
        with self.client.session_transaction() as sess:
            sess['user_id'] = 1
            sess['user_email'] = 'user@example.com'
            sess['user_name'] = 'Test User'
            sess['user_role'] = role
            sess['is_admin'] = role == 'admin'

    def test_thumbnail_bez_fototeke_daje_placeholder(self):
        self._login()
        with patch.object(collection_media_views, '_fototeka_entity_response', return_value=None):
            response = self.client.get(
                '/api/specimen_thumbnail/minerals/mineral/12', base_url=self.base_url
            )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.mimetype, 'image/png')
        response.close()

    def test_slika_bez_fototeke_daje_placeholder(self):
        self._login()
        with patch.object(collection_media_views, '_fototeka_entity_response', return_value=None):
            response = self.client.get(
                '/api/specimen_image/minerals/mineral/12', base_url=self.base_url
            )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.mimetype, 'image/png')
        response.close()

    def test_pokvarena_fototeka_ne_ruси_stranicu_nego_pada_na_placeholder(self):
        """Ако упит ка Фототеци пукне, корисник добија плацехолдер, не 500."""
        self._login()
        with patch.object(
            collection_media_views,
            'get_postgres_connection',
            create=True,
            side_effect=RuntimeError('фототека недоступна'),
        ):
            response = self.client.get(
                '/api/specimen_thumbnail/minerals/mineral/12', base_url=self.base_url
            )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.mimetype, 'image/png')
        response.close()

    def test_send_entity_image_bez_fototeke_vraca_none_bez_legacy_pokusaja(self):
        """Без фототека фотографије нема резервног пута — само None."""
        with patch.object(collection_media_views, '_fototeka_entity_response', return_value=None):
            with museum_app.app.test_request_context('/'):
                rezultat = collection_media_views._send_entity_image(
                    'minerals', 'mineral', '12', 'small'
                )
        self.assertIsNone(rezultat)


class StareRuteSuUklonjeneTests(unittest.TestCase):
    """Стари batch upload и image_api више не постоје."""

    def setUp(self):
        self.client = museum_app.app.test_client()
        self.base_url = 'https://localhost'

    def _login(self, *, role='admin'):
        with self.client.session_transaction() as sess:
            sess['user_id'] = 1
            sess['user_email'] = 'admin@example.com'
            sess['user_name'] = 'Test Admin'
            sess['user_role'] = role
            sess['is_admin'] = role == 'admin'

    def test_batch_image_upload_ruta_vraca_404(self):
        self._login()
        response = self.client.get('/admin/batch_image_upload', base_url=self.base_url)
        self.assertEqual(response.status_code, 404)

    def test_batch_image_upload_post_vraca_404(self):
        self._login()
        response = self.client.post(
            '/admin/batch_image_upload',
            data={'action': 'preview', 'directory': '/tmp'},
            base_url=self.base_url,
        )
        self.assertEqual(response.status_code, 404)

    def test_image_api_upload_vise_ne_prima_post(self):
        """`/api/images/upload` је нестао. Путања се сада поклапа са читањем
        `/api/images/<image_id>` (image_id='upload'), које прима само GET — отуда
        405, а не 404. Битно је да отпремање више нигде не пролази."""
        self._login()
        response = self.client.post('/api/images/upload', base_url=self.base_url)
        self.assertEqual(response.status_code, 405)

    def test_image_api_stats_ruta_vraca_404(self):
        self._login()
        response = self.client.get('/api/images/stats', base_url=self.base_url)
        self.assertEqual(response.status_code, 404)

    def test_delete_mineral_image_ruta_vraca_404(self):
        self._login()
        response = self.client.post(
            '/admin/edit_mineral/12/delete_image/x', base_url=self.base_url
        )
        self.assertEqual(response.status_code, 404)

    def test_nijedan_endpoint_se_ne_zove_batch_image_upload(self):
        endpoints = {rule.endpoint for rule in museum_app.app.url_map.iter_rules()}
        self.assertNotIn('batch_image_upload', endpoints)
        self.assertNotIn('media.batch_image_upload', endpoints)
        self.assertFalse({e for e in endpoints if e.startswith('image_api.')})

    def test_moduli_starog_sistema_se_ne_uvoze(self):
        for modul in ('batch_image_upload', 'image_api'):
            with self.assertRaises(ImportError):
                __import__(modul)


class LegacyTragoviUKoduTests(unittest.TestCase):
    """Легаци резерва не сме да се врати кроз шаблоне."""

    def test_sabloni_ne_pominju_legacy_rezervu(self):
        for putanja in ('templates/admin_mineral_collection.html',
                        'templates/admin_mineral_detail.html'):
            sadrzaj = Path(putanja).read_text(encoding='utf-8')
            self.assertNotIn('has_image', sadrzaj, putanja)
            self.assertNotIn('batch_image_upload', sadrzaj, putanja)

    def test_mineral_tabela_ima_placeholder_granu(self):
        sadrzaj = Path('templates/admin_mineral_collection.html').read_text(encoding='utf-8')
        self.assertIn("images/specimen-placeholder-thumb.png", sadrzaj)
        self.assertIn('mineral.foto_id', sadrzaj)

    def test_has_image_sql_cita_fototeku_a_ne_images_tabelu(self):
        import mineral_database_pg

        sql = mineral_database_pg.MineralDatabase._HAS_IMAGE_SQL
        self.assertIn('foto_veza_predmet', sql)
        self.assertIn('fotografije', sql)
        self.assertNotIn('FROM images', sql)


class FototekaTokNetaknutTests(unittest.TestCase):
    """Регресија: фототека ток ради исто као пре реза."""

    def test_fototeka_rute_i_dalje_postoje(self):
        endpoints = {rule.endpoint for rule in museum_app.app.url_map.iter_rules()}
        for endpoint in ('fototeka.fototeka_galerija', 'fototeka.fototeka_media',
                         'fototeka.fototeka_fotografija', 'fototeka.fototeka_import',
                         'fototeka.fototeka_prijemni_red'):
            self.assertIn(endpoint, endpoints)

    def test_fototeka_i_dalje_koristi_image_matcher(self):
        """image_matcher је остао jer га Фототека користи за инв. обрасце."""
        import fototeka_views

        self.assertTrue(fototeka_views.image_matcher.ImageMatcher.INVENTORY_PATTERNS)

    def test_fototeka_sluzi_derivat_kad_fotografija_postoji(self):
        """Кад Фототека има фотографију, служи се њен дериват (не плацехолдер)."""
        import tempfile

        with tempfile.TemporaryDirectory() as tmp:
            derivat = Path(tmp) / 'ab' / 'abcdef.jpg'
            derivat.parent.mkdir(parents=True)
            derivat.write_bytes(b'\xff\xd8\xff\xdb-jpeg-derivat')

            class FakeCursor:
                def __enter__(self): return self
                def __exit__(self, *a): return False
                def execute(self, *a, **k): pass
                def fetchone(self): return {'sha256': 'abcdef'}

            class FakeConn:
                def __enter__(self): return self
                def __exit__(self, *a): return False
                def cursor(self): return FakeCursor()

            import fototeka_jobs

            with patch.dict('sys.modules'), \
                 patch.object(fototeka_jobs, 'get_media_path', return_value=Path(tmp)), \
                 patch.object(fototeka_jobs, 'derivative_relative_path',
                              return_value=Path('ab/abcdef.jpg')), \
                 patch('postgres_service.get_postgres_connection', return_value=FakeConn()):
                with museum_app.app.test_request_context('/'):
                    odgovor = collection_media_views._fototeka_entity_response(
                        'minerals', 'mineral', '12', 'small'
                    )

            self.assertIsNotNone(odgovor)
            self.assertEqual(odgovor.status_code, 200)
            odgovor.close()

    def test_fototeka_ne_sluzi_ne_mineral_zbirke(self):
        with museum_app.app.test_request_context('/'):
            self.assertIsNone(
                collection_media_views._fototeka_entity_response(
                    'botany', 'specimen', '3', 'small'
                )
            )


class ObrisiLegacySlikeKomandaTests(unittest.TestCase):
    """Команда је dry-run по подразумеваном и не дира ништа без --execute."""

    def test_komanda_je_registrovana(self):
        self.assertIn('obrisi-legacy-slike', museum_app.app.cli.commands)

    def test_dry_run_ne_brise_nista(self):
        import obrisi_legacy_slike_cli
        from click.testing import CliRunner

        redovi = [{
            'image_id': 'img-1', 'database_name': 'mineral', 'entity_type': 'collection_item',
            'entity_id': '12', 'file_path': 'ImagesDatabase/originals/a.jpg',
            'thumbnail_small': '', 'thumbnail_medium': '', 'thumbnail_large': '',
            'file_size': 1024,
        }]

        with patch.object(obrisi_legacy_slike_cli, 'get_postgres_connection') as fake_conn, \
             patch.object(obrisi_legacy_slike_cli, '_tabela_postoji', return_value=True), \
             patch.object(obrisi_legacy_slike_cli, 'popis_legacy_slika', return_value=redovi), \
             patch.object(obrisi_legacy_slike_cli, 'pokrivenost_fototekom',
                          return_value=(['M 12'], [])), \
             patch.object(obrisi_legacy_slike_cli, 'obrisi') as fake_obrisi:
            fake_conn.return_value.__enter__.return_value.cursor.return_value.__enter__ \
                .return_value = object()
            rezultat = CliRunner().invoke(
                museum_app.app.cli.commands['obrisi-legacy-slike'], [],
                obj={}, catch_exceptions=False,
            )

        self.assertEqual(rezultat.exit_code, 0, rezultat.output)
        self.assertIn('Dry-run', rezultat.output)
        fake_obrisi.assert_not_called()

    def test_dry_run_prijavljuje_predmete_bez_fototeke(self):
        import obrisi_legacy_slike_cli
        from click.testing import CliRunner

        redovi = [{
            'image_id': 'img-1', 'database_name': 'mineral', 'entity_type': 'collection_item',
            'entity_id': '12', 'file_path': '', 'thumbnail_small': '',
            'thumbnail_medium': '', 'thumbnail_large': '', 'file_size': 0,
        }]

        with patch.object(obrisi_legacy_slike_cli, 'get_postgres_connection') as fake_conn, \
             patch.object(obrisi_legacy_slike_cli, '_tabela_postoji', return_value=True), \
             patch.object(obrisi_legacy_slike_cli, 'popis_legacy_slika', return_value=redovi), \
             patch.object(obrisi_legacy_slike_cli, 'pokrivenost_fototekom',
                          return_value=([], ['M 12'])), \
             patch.object(obrisi_legacy_slike_cli, 'obrisi') as fake_obrisi:
            fake_conn.return_value.__enter__.return_value.cursor.return_value.__enter__ \
                .return_value = object()
            rezultat = CliRunner().invoke(
                museum_app.app.cli.commands['obrisi-legacy-slike'], [],
                obj={}, catch_exceptions=False,
            )

        self.assertEqual(rezultat.exit_code, 0, rezultat.output)
        self.assertIn('остаје на плацехолдеру', rezultat.output)
        self.assertIn('M 12', rezultat.output)
        fake_obrisi.assert_not_called()


if __name__ == '__main__':
    unittest.main()
