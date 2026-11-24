#!/usr/bin/env python3
"""Блок ``colab`` уџбеника (UGOVOR-COLAB.md): увоз по шеми и API га прослеђује
непромењеног; празан url (линк се попуњава касније) је дозвољен, туђ домен није."""
import json
import os
import tempfile

from test_udzbenik import BAZA, EMAIL, PRIMER, _Osnova, _ime_baze, _pokreni_uvoz

LEKCIJA = '/api/udzbenik/minerali/lekcija/kristalografija/kristalni-sistemi'
URL = 'https://colab.research.google.com/github/primer/sveska/blob/main/03-kristalografija-cif.ipynb'


class ColabTest(_Osnova):
    def _fajl(self, *blokovi):
        podaci = json.loads(PRIMER.read_text(encoding='utf-8'))
        podaci['poglavlja'][0]['lekcije'][0]['sadrzaj']['blokovi'][1:1] = list(blokovi)
        f = tempfile.NamedTemporaryFile('w', suffix='.json', delete=False, encoding='utf-8')
        json.dump(podaci, f, ensure_ascii=False)
        f.close()
        self.addCleanup(os.unlink, f.name)
        return f.name

    def _blok(self, bid, url, **dodatno):
        return dict({'id': bid, 'tip': 'colab', 'url': url, 'naslov': 'Кристалографија у Colab-у'}, **dodatno)

    def test_prazan_i_pravi_url_prolaze_api_prosledjuje(self):
        prazan = self._blok('colab-prazan', '')
        pravi = self._blok('colab-pravi', URL, opis='Опис.', sveska='03-kristalografija-cif.ipynb')
        kod, out, err = _pokreni_uvoz('--fajl', self._fajl(prazan, pravi), '--execute', _ime_baze(), '--autor', EMAIL)
        self.assertEqual(kod, 0, err + out)
        self._prijava()
        blokovi = self.get(LEKCIJA).get_json()['lekcija']['blokovi']
        colab = [b for b in blokovi if b['tip'] == 'colab']
        self.assertEqual(colab, [prazan, pravi])

    def test_tudj_domen_i_visak_polja_su_greske(self):
        for blok in (self._blok('c1', 'https://example.com/sveska.ipynb'),
                     self._blok('c2', 'javascript:alert(1)'),
                     self._blok('c3', URL, slika=1),
                     {'id': 'c4', 'tip': 'colab', 'url': URL}):
            kod, out, err = _pokreni_uvoz('--fajl', self._fajl(blok), '--dry-run')
            self.assertEqual(kod, 1, blok)
