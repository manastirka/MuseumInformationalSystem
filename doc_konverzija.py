"""Детекција Word формата по magic бајтовима + конверзија .doc → .docx.

Прави фајлови запослених су често стари .doc (бинарни OLE), а парсер чита .docx.
Формат се одлучује по САДРЖАЈУ (magic бајтови), не по екстензији — људи
преименују фајлове. .doc се конвертује кроз LibreOffice (soffice --headless),
sandbox-овано: привремени директоријум + изолован профил + timeout + чишћење.
"""

import os
import shutil
import subprocess
import tempfile


class SofficeUnavailable(Exception):
    """LibreOffice (soffice) није доступан за конверзију .doc → .docx."""


class DocConversionError(Exception):
    """Конверзија .doc → .docx није успела (timeout, оштећен фајл…)."""


# Magic потписи.
_OLE_MAGIC = b'\xd0\xcf\x11\xe0\xa1\xb1\x1a\xe1'   # OLE2 (стари .doc/.xls/.ppt)
_ZIP_MAGIC = b'PK\x03\x04'                          # ZIP контејнер (.docx/.xlsx…)


def detect_format(data):
    """Врати ('docx'|'doc'|'unknown', опис). Опис за unknown каже шта јесте."""
    head = data[:8] if data else b''
    if head.startswith(_ZIP_MAGIC):
        return 'docx', 'Office Open XML (ZIP)'
    if head.startswith(_OLE_MAGIC):
        return 'doc', 'стари Word (OLE)'
    return 'unknown', _describe(data)


def _describe(data):
    head = data[:8] if data else b''
    if head.startswith(b'%PDF'):
        return 'PDF документ'
    if head[:4] in (b'{\\rt',) or head.startswith(b'{\\rtf'):
        return 'RTF документ'
    if head.startswith(b'\x89PNG') or head[:3] == b'\xff\xd8\xff' or head[:6] in (b'GIF87a', b'GIF89a'):
        return 'слика'
    if not data:
        return 'празна датотека'
    try:
        data[:512].decode('utf-8')
        return 'обичан текст'
    except UnicodeDecodeError:
        return 'непознат бинарни формат'


def _find_soffice():
    return shutil.which('soffice') or shutil.which('libreoffice')


def convert_doc_to_docx(data, timeout=60):
    """Конвертуј .doc бајтове у .docx бајтове преко LibreOffice.

    Диже SofficeUnavailable ако нема soffice, DocConversionError на неуспех.
    Ради у привременом директоријуму са изолованим корисничким профилом
    (без судара са другим soffice процесима) и чисти за собом.
    """
    soffice = _find_soffice()
    if not soffice:
        raise SofficeUnavailable('soffice/libreoffice није пронађен на систему')

    with tempfile.TemporaryDirectory(prefix='rl_doc_') as tmp:
        src = os.path.join(tmp, 'ulaz.doc')
        profile = os.path.join(tmp, 'profile')
        with open(src, 'wb') as fh:
            fh.write(data)
        cmd = [
            soffice, '--headless', '--norestore', '--nologo',
            f'-env:UserInstallation=file://{profile}',
            '--convert-to', 'docx', '--outdir', tmp, src,
        ]
        try:
            proc = subprocess.run(cmd, capture_output=True, timeout=timeout)
        except subprocess.TimeoutExpired:
            raise DocConversionError(f'конверзија је прекорачила {timeout}s')
        except OSError as exc:
            raise DocConversionError(f'покретање soffice није успело: {exc}')

        out = os.path.join(tmp, 'ulaz.docx')
        if not os.path.isfile(out):
            err = (proc.stderr or b'').decode('utf-8', 'replace').strip()
            raise DocConversionError(err or 'soffice није произвео .docx')
        with open(out, 'rb') as fh:
            return fh.read()


def ensure_docx_bytes(data, timeout=60):
    """Врати .docx бајтове за дате улазне бајтове (конвертује .doc по потреби).

    Диже SofficeUnavailable / DocConversionError / ValueError(опис) за непознат
    формат — позивалац те претвара у корисничке поруке.
    """
    fmt, desc = detect_format(data)
    if fmt == 'docx':
        return data
    if fmt == 'doc':
        return convert_doc_to_docx(data, timeout=timeout)
    raise ValueError(desc)
