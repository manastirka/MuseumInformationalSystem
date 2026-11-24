#!/usr/bin/env python3
"""Блок ``video`` уџбеника — до базе и до сервиса фајла (UGOVOR-VIDEO.md).

Миграција 065 се примењује сама ако табеле нема; клип је мали mp4 направљен
ffmpeg-ом у привременом директоријуму, FOTOTEKA_MEDIA_PATH показује у други
привремени директоријум (увоз копира фајлове тамо, рута их одатле служи).
"""
import hashlib
import json
import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from test_udzbenik import (BAZA, EMAIL, KOREN, PRIMER, _Osnova, _ime_baze, _pokreni_uvoz, _upit,
                           _osiguraj_semu)
from postgres_service import get_postgres_connection
import app as museum_app

KLJUC = 'udztest-video-klip'
OZNAKA = 'AI ilustracija (Google Flow, 2026) – šematski prikaz, razmere nisu verne'
LEKCIJA = '/api/udzbenik/minerali/lekcija/kristalografija/kristalni-sistemi'


def _osiguraj_065():
    _osiguraj_semu()
    with get_postgres_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT to_regclass('public.udzbenik_video')")
            if cur.fetchone()[0] is None:
                cur.execute((KOREN / 'migration' / '065_udzbenik_video.sql').read_text(encoding='utf-8'))
        conn.commit()


def _sha(putanja):
    return hashlib.sha256(Path(putanja).read_bytes()).hexdigest()


@unittest.skipUnless(shutil.which('ffmpeg'), 'ffmpeg није инсталиран')
class VideoTest(_Osnova):
    @classmethod
    def setUpClass(cls):
        _osiguraj_065()
        cls.ulaz = Path(tempfile.mkdtemp(prefix='udztest-video-'))
        (cls.ulaz / 'poster').mkdir()
        subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-f', 'lavfi', '-i', 'testsrc=size=320x180:rate=10',
                        '-t', '1', '-pix_fmt', 'yuv420p', str(cls.ulaz / 'klip.mp4')], check=True)
        subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-ss', '0.5', '-i', str(cls.ulaz / 'klip.mp4'),
                        '-frames:v', '1', str(cls.ulaz / 'poster' / 'klip.jpg')], check=True)

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.ulaz, ignore_errors=True)

    def setUp(self):
        super().setUp()
        self.media = Path(tempfile.mkdtemp(prefix='udztest-media-'))
        self.addCleanup(shutil.rmtree, self.media, True)
        okruzenje = mock.patch.dict(os.environ, {'FOTOTEKA_MEDIA_PATH': str(self.media), 'FOTOTEKA_XACCEL': ''})
        okruzenje.start()
        self.addCleanup(okruzenje.stop)

    # -- pomoćno --------------------------------------------------------------

    def _stavka(self, **izmene):
        v = {'kljuc': KLJUC, 'fajl': 'klip.mp4', 'sha256': _sha(self.ulaz / 'klip.mp4'),
             'poster': 'poster/klip.jpg', 'poster_sha256': _sha(self.ulaz / 'poster' / 'klip.jpg'),
             'mime': 'video/mp4', 'trajanje_s': 1.0, 'sirina_px': 320, 'visina_px': 180, 'zvuk': False,
             'opis': 'Тестни клип.', 'ai': True, 'oznaka': OZNAKA, 'autor': 'Google Flow', 'licenca': None}
        v.update(izmene)
        return v

    def _fajl(self, videi=None, blok=None, javno=None):
        podaci = json.loads(PRIMER.read_text(encoding='utf-8'))
        podaci['videi'] = [self._stavka()] if videi is None else videi
        if javno:
            podaci['udzbenik'].update(status='objavljen', javno=True)
            for p in podaci['poglavlja']:
                for lek in p['lekcije']:
                    lek['status'] = 'objavljen'
        blokovi = podaci['poglavlja'][0]['lekcije'][0]['sadrzaj']['blokovi']
        blokovi.insert(1, blok or {'id': 'video-test', 'tip': 'video', 'video': KLJUC, 'napomena': 'Гледајте.'})
        f = tempfile.NamedTemporaryFile('w', suffix='.json', delete=False, encoding='utf-8')
        json.dump(podaci, f, ensure_ascii=False)
        f.close()
        self.addCleanup(os.unlink, f.name)
        return f.name

    def _uvoz(self, fajl, *dodatno, izvrsi=True):
        argv = ['--fajl', fajl, '--video-dir', str(self.ulaz), *dodatno]
        if izvrsi:
            argv += ['--execute', _ime_baze(), '--autor', EMAIL]
        return _pokreni_uvoz(*argv)

    def _red(self):
        r = _upit("""SELECT putanja, poster_putanja, sha256, velicina_b, opis, ai, oznaka, trajanje_s
                     FROM udzbenik_video WHERE kljuc = %s""", (KLJUC,))
        return r[0] if r else None

    # -- uvoz -----------------------------------------------------------------

    def test_dry_run_ne_upisuje_ni_ne_kopira(self):
        kod, out, err = self._uvoz(self._fajl(), izvrsi=False)
        self.assertEqual(kod, 0, err + out)
        self.assertIn(f'+ video {KLJUC} (dodaje)', out)
        self.assertIsNone(self._red())
        self.assertEqual(list(self.media.iterdir()), [])

    def test_execute_upisuje_red_i_kopira_fajlove_pa_ponovo_isto(self):
        kod, out, err = self._uvoz(self._fajl())
        self.assertEqual(kod, 0, err + out)
        putanja, poster, sha, velicina, opis, ai, oznaka, trajanje = self._red()
        self.assertEqual(sha, _sha(self.ulaz / 'klip.mp4'))
        self.assertEqual(putanja, f'udzbenik-video/{sha[:2]}/{sha}.mp4')
        self.assertEqual((self.media / putanja).read_bytes(), (self.ulaz / 'klip.mp4').read_bytes())
        self.assertEqual(velicina, (self.ulaz / 'klip.mp4').stat().st_size)
        self.assertTrue((self.media / poster).is_file())
        self.assertEqual((opis, ai, oznaka, float(trajanje)), ('Тестни клип.', True, OZNAKA, 1.0))
        kod, out, err = self._uvoz(self._fajl())
        self.assertEqual(kod, 0, err + out)
        self.assertIn(f'= video {KLJUC} (isto)', out)
        kod, out, err = self._uvoz(self._fajl(videi=[self._stavka(opis='Нови опис.')]))
        self.assertIn(f'~ video {KLJUC} (menja)', out)
        self.assertEqual(self._red()[4], 'Нови опис.')

    def test_pogresan_sha_ne_upisuje_nista(self):
        kod, out, err = self._uvoz(self._fajl(videi=[self._stavka(sha256='0' * 64)]))
        self.assertEqual(kod, 1)
        self.assertIn('sha256 фајла', err)
        self.assertIsNone(self._red())
        self.assertEqual(_upit("SELECT count(*) FROM udzbenik WHERE zbirka = 'minerali'")[0][0], 0)

    def test_ai_bez_oznake_i_bez_video_dir_su_greske(self):
        stavka = self._stavka()
        del stavka['oznaka']
        kod, out, err = self._uvoz(self._fajl(videi=[stavka]))
        self.assertEqual(kod, 1)
        self.assertIn("'oznaka' is a required property", err)
        kod, out, err = _pokreni_uvoz('--fajl', self._fajl())
        self.assertEqual(kod, 1)
        self.assertIn('--video-dir', err)

    def test_blok_sa_nepoznatim_kljucem_je_greska(self):
        kod, out, err = self._uvoz(self._fajl(videi=[], blok={'id': 'v', 'tip': 'video', 'video': 'nema-ga'}))
        self.assertEqual(kod, 1)
        self.assertIn("клип 'nema-ga' не постоји", err)

    def test_blok_bez_kljuca_u_semi_je_greska(self):
        kod, out, err = self._uvoz(self._fajl(blok={'id': 'v', 'tip': 'video', 'video': KLJUC, 'autoplay': True}))
        self.assertEqual(kod, 1)

    # -- API lekcije i fajl ---------------------------------------------------

    def _blok_iz_api(self):
        d = self.get(LEKCIJA).get_json()
        return next(b for b in d['lekcija']['blokovi'] if b['tip'] == 'video')

    def test_lekcija_razresava_blok_iz_baze(self):
        self.assertEqual(self._uvoz(self._fajl())[0], 0)
        self._prijava()
        b = self._blok_iz_api()
        self.assertEqual(b['src'], f'/api/udzbenik/video/{KLJUC}')
        self.assertEqual(b['poster'], f'/api/udzbenik/video/{KLJUC}/poster')
        self.assertEqual((b['mime'], b['trajanje_s'], b['sirina_px'], b['visina_px']), ('video/mp4', 1.0, 320, 180))
        self.assertEqual((b['opis'], b['ai'], b['oznaka'], b['napomena']), ('Тестни клип.', True, OZNAKA, 'Гледајте.'))
        self.assertNotIn('nedostupan', b)

    def test_obrisan_zapis_daje_nedostupan(self):
        self.assertEqual(self._uvoz(self._fajl())[0], 0)
        _upit('DELETE FROM udzbenik_video WHERE kljuc = %s RETURNING id', (KLJUC,))
        self._prijava()
        b = self._blok_iz_api()
        self.assertTrue(b['nedostupan'])
        self.assertEqual(b['razlog'], 'video ne postoji')

    def test_fajl_ceo_i_range_206(self):
        self.assertEqual(self._uvoz(self._fajl())[0], 0)
        self._prijava()
        bajtovi = (self.ulaz / 'klip.mp4').read_bytes()
        r = self.get(f'/api/udzbenik/video/{KLJUC}')
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.mimetype, 'video/mp4')
        self.assertEqual(r.headers.get('Accept-Ranges'), 'bytes')
        self.assertEqual(r.get_data(), bajtovi)
        r = self.get(f'/api/udzbenik/video/{KLJUC}', headers={'Range': 'bytes=100-199'})
        self.assertEqual(r.status_code, 206)
        self.assertEqual(r.headers['Content-Range'], f'bytes 100-199/{len(bajtovi)}')
        self.assertEqual(r.get_data(), bajtovi[100:200])
        r = self.get(f'/api/udzbenik/video/{KLJUC}', headers={'Range': f'bytes={len(bajtovi) - 10}-'})
        self.assertEqual(r.status_code, 206)
        self.assertEqual(r.get_data(), bajtovi[-10:])
        p = self.get(f'/api/udzbenik/video/{KLJUC}/poster')
        self.assertEqual((p.status_code, p.mimetype), (200, 'image/jpeg'))
        self.assertEqual(p.get_data(), (self.ulaz / 'poster' / 'klip.jpg').read_bytes())

    def test_xaccel_prazan_odgovor_na_internu_putanju(self):
        self.assertEqual(self._uvoz(self._fajl())[0], 0)
        self._prijava()
        with mock.patch.dict(os.environ, {'FOTOTEKA_XACCEL': '1'}):
            r = self.get(f'/api/udzbenik/video/{KLJUC}')
        sha = _sha(self.ulaz / 'klip.mp4')
        self.assertEqual(r.headers.get('X-Accel-Redirect'), f'/_zasticeno/derivati/udzbenik-video/{sha[:2]}/{sha}.mp4')
        self.assertEqual(r.get_data(), b'')

    def test_anonimni_nacrt_404_javni_200(self):
        self.assertEqual(self._uvoz(self._fajl())[0], 0)
        self.assertEqual(self.get(f'/api/udzbenik/video/{KLJUC}').status_code, 404)
        self.assertEqual(self.get(f'/api/udzbenik/video/{KLJUC}/poster').status_code, 404)
        self.assertEqual(self._uvoz(self._fajl(javno=True))[0], 0)
        self.assertEqual(self.get(f'/api/udzbenik/video/{KLJUC}').status_code, 200)

    def test_nepostojeci_kljuc_404_i_nestao_fajl_404(self):
        self._prijava()
        self.assertEqual(self.get('/api/udzbenik/video/nema-ga').status_code, 404)
        self.assertEqual(self._uvoz(self._fajl())[0], 0)
        putanja = self._red()[0]
        (self.media / putanja).unlink()
        self.assertEqual(self.get(f'/api/udzbenik/video/{KLJUC}').status_code, 404)

    def test_migracija_ai_mora_imati_oznaku(self):
        import psycopg
        self.assertEqual(self._uvoz(self._fajl())[0], 0)
        with self.assertRaises(psycopg.errors.CheckViolation):
            _upit('UPDATE udzbenik_video SET oznaka = NULL WHERE kljuc = %s RETURNING id', (KLJUC,))
