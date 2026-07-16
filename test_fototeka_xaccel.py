#!/usr/bin/env python3
"""X-Accel-Redirect isporuka slika (zadatak #1 iz ANALIZA-2026-07).

Dokazuje:
  - flag OFF (default) => postojeće ponašanje: Flask strimuje fajl (send_file),
    bez X-Accel-Redirect header-a (regresija);
  - flag ON => odgovor ima X-Accel-Redirect na tačnu internu putanju, PRAZAN
    body, tačan MIME; provera prava je IDENTIČNA (403 za tuđu privatnu, 404 za
    nepostojeću) — Flask i dalje odlučuje, nginx samo isporučuje.
"""

import os
from pathlib import Path
from unittest.mock import patch

import fototeka_jobs
from test_fototeka import _RouteTestCase, _photo, AUTHOR, OTHER, SHA


def _xaccel(value):
    return patch.dict(os.environ, {'FOTOTEKA_XACCEL': value})


class ServeDerivatXAccelTests(_RouteTestCase):

    def _write_derivative(self, kind='thumb'):
        rel = fototeka_jobs.derivative_relative_path(SHA, kind)
        full = Path(self.media) / rel
        full.parent.mkdir(parents=True, exist_ok=True)
        full.write_bytes(b'\xff\xd8\xff\xe0JPEGDATA')  # realan JPEG magic + telo
        return rel

    def test_flag_off_streams_file_as_before(self):
        rel = self._write_derivative('thumb')
        self.use_db({'FROM fotografije WHERE id': _photo()})
        self.login(AUTHOR)
        with _xaccel(''):
            resp = self.get('/fototeka/media/5/thumb')
        self.assertEqual(resp.status_code, 200)
        self.assertNotIn('X-Accel-Redirect', resp.headers)
        self.assertEqual(resp.mimetype, 'image/jpeg')
        # Flask je zaista poslao bajtove fajla
        self.assertEqual(resp.data, (Path(self.media) / rel).read_bytes())

    def test_flag_on_emits_xaccel_header_empty_body(self):
        rel = self._write_derivative('thumb')
        self.use_db({'FROM fotografije WHERE id': _photo()})
        self.login(AUTHOR)
        with _xaccel('1'):
            resp = self.get('/fototeka/media/5/thumb')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.headers.get('X-Accel-Redirect'), '/_zasticeno/derivati/' + rel)
        self.assertEqual(resp.data, b'')                 # nginx puni telo, ne Flask
        self.assertEqual(resp.mimetype, 'image/jpeg')    # MIME tačan
        # cache-control iz _apply_private_cache_headers je zadržan
        self.assertIn('private', resp.headers.get('Cache-Control', ''))

    def test_flag_on_private_of_other_author_is_403(self):
        self._write_derivative('thumb')
        self.use_db({'FROM fotografije WHERE id': _photo(vidljivost='privatno')})
        self.login(OTHER)  # nije autor, nije admin/direktor
        with _xaccel('1'):
            resp = self.get('/fototeka/media/5/thumb')
        self.assertEqual(resp.status_code, 403)
        self.assertNotIn('X-Accel-Redirect', resp.headers)  # nema curenja fajla

    def test_flag_on_missing_photo_is_404(self):
        self.use_db({})  # DB ne vraća red
        self.login(AUTHOR)
        with _xaccel('1'):
            resp = self.get('/fototeka/media/5/thumb')
        self.assertEqual(resp.status_code, 404)
        self.assertNotIn('X-Accel-Redirect', resp.headers)

    def test_flag_on_processing_still_serves_placeholder(self):
        # status != 'spremna' => placeholder (Flask, ne X-Accel) i u ON režimu
        self.use_db({'FROM fotografije WHERE id': _photo(status='obrada')})
        self.login(AUTHOR)
        with _xaccel('1'):
            resp = self.get('/fototeka/media/5/thumb')
        self.assertIn(resp.status_code, (200, 404))
        self.assertNotIn('X-Accel-Redirect', resp.headers)


class ServeRawXAccelTests(_RouteTestCase):

    def _write_raw(self, rel='razno/2026/proba__aaaaaaaa.jpg'):
        full = Path(self.arhiva) / rel
        full.parent.mkdir(parents=True, exist_ok=True)
        full.write_bytes(b'RAWORIGINALBYTES')
        return rel

    def test_flag_off_streams_raw_as_attachment(self):
        rel = self._write_raw()
        self.use_db({'FROM fotografije WHERE id': _photo(raw_putanja=rel)})
        self.login(AUTHOR)
        with _xaccel(''):
            resp = self.get('/fototeka/raw/5')
        self.assertEqual(resp.status_code, 200)
        self.assertNotIn('X-Accel-Redirect', resp.headers)
        self.assertEqual(resp.data, b'RAWORIGINALBYTES')
        self.assertIn('attachment', resp.headers.get('Content-Disposition', ''))

    def test_flag_on_emits_xaccel_for_raw(self):
        rel = self._write_raw()
        self.use_db({'FROM fotografije WHERE id': _photo(raw_putanja=rel)})
        self.login(AUTHOR)
        with _xaccel('1'):
            resp = self.get('/fototeka/raw/5')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.headers.get('X-Accel-Redirect'), '/_zasticeno/raw/' + rel)
        self.assertEqual(resp.data, b'')
        self.assertIn('attachment', resp.headers.get('Content-Disposition', ''))

    def test_flag_on_private_raw_of_other_author_is_403(self):
        rel = self._write_raw()
        self.use_db({'FROM fotografije WHERE id': _photo(raw_putanja=rel, vidljivost='privatno')})
        self.login(OTHER)
        with _xaccel('1'):
            resp = self.get('/fototeka/raw/5')
        self.assertEqual(resp.status_code, 403)
        self.assertNotIn('X-Accel-Redirect', resp.headers)

    def test_flag_on_missing_raw_file_is_404(self):
        # DB ima red, ali fajl ne postoji na disku => 404 (ne X-Accel na nepostojeće)
        self.use_db({'FROM fotografije WHERE id': _photo(raw_putanja='razno/2026/nema.jpg')})
        self.login(AUTHOR)
        with _xaccel('1'):
            resp = self.get('/fototeka/raw/5')
        self.assertEqual(resp.status_code, 404)
        self.assertNotIn('X-Accel-Redirect', resp.headers)

    def test_flag_on_normalizes_traversal_inside_arhiva(self):
        # raw_putanja sa `..` koja se JOŠ UVEK razrešava unutar arhive: send_file
        # (flag OFF) posluži razrešeni fajl, pa X-Accel URI mora biti taj isti
        # razrešeni put. Sirov `..` u URI-ju nginx normalizuje PRE poklapanja
        # `location`, pa bi ispao iz interne lokacije => oba režima moraju dati
        # istu, već normalizovanu putanju.
        self._write_raw()
        petljava = 'razno/2026/../../razno/2026/proba__aaaaaaaa.jpg'
        self.use_db({'FROM fotografije WHERE id': _photo(raw_putanja=petljava)})
        self.login(AUTHOR)
        with _xaccel('1'):
            resp = self.get('/fototeka/raw/5')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(
            resp.headers.get('X-Accel-Redirect'),
            '/_zasticeno/raw/razno/2026/proba__aaaaaaaa.jpg',
        )
        self.assertNotIn('..', resp.headers.get('X-Accel-Redirect', ''))


if __name__ == '__main__':
    import unittest
    unittest.main()
