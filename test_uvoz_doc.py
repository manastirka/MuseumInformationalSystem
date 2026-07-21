"""Тестови за .doc подршку увоза радних листа.

Покрива: детекцију формата по magic бајтовима, .doc → .docx конверзију преко
LibreOffice (исти резултат као .docx), и јасне поруке кад soffice није доступан
или фајл није ни .doc ни .docx.
"""

import io
import os
import subprocess
import sys
import tempfile

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'tests', 'fixtures', 'radne_liste'))

import doc_konverzija as dk
import radna_lista_word_parser as rl
import make_fixtures as mk


def _soffice():
    import shutil
    return shutil.which('soffice') or shutil.which('libreoffice')


_NEED_SOFFICE = pytest.mark.skipif(_soffice() is None, reason='soffice није доступан')


def _docx_to_doc(docx_bytes):
    """Направи .doc из .docx преко LibreOffice (за фикстуру)."""
    with tempfile.TemporaryDirectory() as t:
        src = os.path.join(t, 'x.docx')
        with open(src, 'wb') as fh:
            fh.write(docx_bytes)
        subprocess.run(
            [_soffice(), '--headless', f'-env:UserInstallation=file://{t}/p',
             '--convert-to', 'doc', '--outdir', t, src],
            capture_output=True, timeout=90,
        )
        with open(os.path.join(t, 'x.doc'), 'rb') as fh:
            return fh.read()


# --- детекција формата (без soffice) ---
def test_detect_docx_po_magic():
    fmt, _ = dk.detect_format(mk.build_correct_matrix_days_rows().read())
    assert fmt == 'docx'


def test_detect_doc_po_magic():
    ole = b'\xd0\xcf\x11\xe0\xa1\xb1\x1a\xe1' + b'\x00' * 100
    assert dk.detect_format(ole)[0] == 'doc'


def test_detect_nepoznat_kaze_sta_je():
    assert dk.detect_format(b'%PDF-1.7 ...')[0] == 'unknown'
    assert 'PDF' in dk.detect_format(b'%PDF-1.7 ...')[1]


def test_neither_doc_ni_docx_jasna_poruka():
    with pytest.raises(rl.RadnaListaParseError) as ei:
        rl.parse_radna_lista(io.BytesIO(b'%PDF-1.7 nije word'))
    msg = str(ei.value)
    assert 'није ни .doc ни .docx' in msg and 'PDF' in msg


# --- soffice недоступан → јасна порука (mock) ---
def test_soffice_nedostupan_poruka(monkeypatch):
    monkeypatch.setattr(dk, '_find_soffice', lambda: None)
    ole = b'\xd0\xcf\x11\xe0\xa1\xb1\x1a\xe1' + b'\x00' * 100
    with pytest.raises(rl.RadnaListaParseError) as ei:
        rl.parse_radna_lista(io.BytesIO(ole))
    assert 'Увоз .doc формата тренутно није могућ' in str(ei.value)


# --- .doc даје исти резултат као .docx (захтева soffice) ---
@_NEED_SOFFICE
def test_doc_isti_rezultat_kao_docx():
    docx_bytes = mk.build_correct_matrix_days_rows().read()
    doc_bytes = _docx_to_doc(docx_bytes)
    assert dk.detect_format(doc_bytes)[0] == 'doc'

    r_doc = rl.parse_radna_lista(io.BytesIO(doc_bytes))
    r_docx = rl.parse_radna_lista(io.BytesIO(docx_bytes))
    assert r_doc['employee_name'] == r_docx['employee_name']
    assert r_doc['month'] == r_docx['month'] and r_doc['year'] == r_docx['year']
    assert r_doc['daily_data'] == r_docx['daily_data']
    assert r_doc['totals'] == r_docx['totals']


@_NEED_SOFFICE
def test_ekstenzija_ne_odlucuje_format():
    """Фајл .doc садржаја али преименован — детекција по садржају, не имену."""
    doc_bytes = _docx_to_doc(mk.build_correct_matrix_days_rows().read())
    # magic је OLE без обзира на „име"
    assert dk.detect_format(doc_bytes)[0] == 'doc'
    r = rl.parse_radna_lista(io.BytesIO(doc_bytes))
    assert r['month'] == 9 and r['employee_name']
