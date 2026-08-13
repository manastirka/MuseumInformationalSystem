#!/usr/bin/env python3
"""Чувар писма у шаблонима: ниједна реч у templates/**/*.html не сме да
меша ћирилицу и латиницу унутар исте речи (нпр. „заштićено", „Воденe",
„изnad"). Такве грешке се виде на обе варијанте писма јер транслитерација
(cyrToLat) ради само над чистом ћирилицом.

Скенер игнорише escape секвенце (\\n, \\t, \\r) у JS стринговима и има
експлицитну allow-листу за легитимне мешане токене (regex опсези знакова).
"""

import re
from pathlib import Path

TEMPLATES = Path(__file__).resolve().parent / 'templates'

_CYR = re.compile(r'[Ѐ-ӿ]')
_LAT = re.compile(r'[A-Za-zĆćČčĐđŠšŽž]')
_WORD = re.compile(r'[0-9A-Za-zЀ-ӿĆćČčĐđŠšŽž_]+')
_ESCAPE = re.compile(r'\\[ntr]')

# Легитимни мешани токени — сваки унос мора имати образложење.
ALLOWED = {
    # dashboard.html: JS regex опсег знакова [A-ZА-ЯČĆŽŠĐ] — није реч.
    ('dashboard.html', 'ZА'),
    ('dashboard.html', 'ЯČĆŽŠĐ'),
}


def _mixed_script_words(text):
    for lineno, line in enumerate(text.splitlines(), 1):
        for word in _WORD.findall(_ESCAPE.sub(' ', line)):
            if _CYR.search(word) and _LAT.search(word):
                yield lineno, word


def test_nijedan_sablon_nema_mesano_pismo_u_reci():
    assert TEMPLATES.is_dir(), f'нема templates директоријума: {TEMPLATES}'
    prekrsaji = []
    for path in sorted(TEMPLATES.rglob('*.html')):
        rel = str(path.relative_to(TEMPLATES))
        text = path.read_text(encoding='utf-8', errors='replace')
        for lineno, word in _mixed_script_words(text):
            if (rel, word) in ALLOWED:
                continue
            prekrsaji.append(f'{rel}:{lineno}: „{word}"')
    assert not prekrsaji, (
        'Мешано писмо унутар речи у шаблонима (ћирилица + латиница). '
        'Исправи реч у чисту ћирилицу или, ако је легитимно (regex и сл.), '
        'додај у ALLOWED са образложењем:\n' + '\n'.join(prekrsaji))


def test_skener_hvata_mesanu_rec():
    """Доказ да скенер уопште гризе: „заштићено" чисто, „заштićено" пада."""
    assert not list(_mixed_script_words('<option value="заштићено">'))
    nadjeno = list(_mixed_script_words('<option value="заштićено">'))
    assert nadjeno and nadjeno[0][1] == 'заштićено'
    # escape секвенца уз ћирилицу није мешана реч
    assert not list(_mixed_script_words("msg = 'Ред 1\\nНапомена';"))
