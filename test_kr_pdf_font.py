"""Доказ да К-Р PDF има праву ћирилицу (не квадратиће).

Генерише PDF, ИЗВЛАЧИ текст назад и потврђује стварну ћирилицу + латиничне
дијакритике; уз то проверава да је уграђени (embedded) фонт заиста употребљен,
па исправност не зависи од системских фонтова на продукцији.
"""

import os
from datetime import date

os.environ.setdefault('DATABASE_URL', 'postgresql://localhost/museum_system')

import pypdf
from pdf_export import export_kr_dosije_pdf


def _dosije():
    return {
        'evidencioni_broj': 'КР-ГЕО-2026-001',
        'odeljenje': 'geo',
        'predmet_tip': 'zbirka',
        'database_name': 'mineral',
        'inventarni_broj': '2051',
        'kolektorski_broj': None,
        # латинични дијакритици који се мешају у подацима (č, ž, š)
        'naziv_predmeta': 'Kvarc, žbackan sa čađavim škriljcem (Стари Трг)',
        'narucilac': None,
        'opis_pre': 'Стање пре радова: површинска корозија.',
        'opis_postupak': 'Извршена конзервација и рестаурација предмета.',
        'opis_posle': 'Стање након радова: стабилизовано.',
        'period_od': date(2022, 12, 23), 'period_do': date(2023, 1, 7),
        'period_tekst': None, 'napomena': 'Напомена о раду.',
        'izvrsioci': [{'user_email': None, 'ime_tekst': 'Ненад Младеновић'}],
        'fotografije': {'pre': [], 'tokom': [], 'posle': []},
    }


def _extract(buf):
    reader = pypdf.PdfReader(buf)
    text = '\n'.join((p.extract_text() or '') for p in reader.pages)
    fonts = set()
    for p in reader.pages:
        res = p.get('/Resources')
        fdict = res.get('/Font') if res else None
        if not fdict:
            continue
        for ref in fdict.values():
            base = ref.get_object().get('/BaseFont')
            if base:
                fonts.add(str(base))
    return text, fonts


def test_pdf_sadrzi_stvarnu_cirilicu():
    text, _ = _extract(export_kr_dosije_pdf(_dosije()))
    low = text.lower()
    assert 'досије' in low, f'нема ћириличног „досије" у извученом тексту: {text[:200]!r}'
    assert 'конзерв' in low, 'нема ћириличног „конзерв(ација)" у тексту'
    # Serbian-specific ћирилична слова се такође исправно исписују
    assert 'Стари' in text or 'стари' in low


def test_pdf_ima_latinicne_dijakritike():
    text, _ = _extract(export_kr_dosije_pdf(_dosije()))
    for ch in ('č', 'ž', 'š'):
        assert ch in text, f'латинични дијакритик {ch!r} недостаје (квадратић?)'


def _fontovi_kojima_se_crta_cirilica(buf):
    """Скуп фонтова којима су СТВАРНО исцртани ћирилични глифови (pdfminer)."""
    from pdfminer.pdfpage import PDFPage
    from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
    from pdfminer.converter import PDFPageAggregator
    from pdfminer.layout import LAParams, LTChar
    buf.seek(0)
    rm = PDFResourceManager()
    dev = PDFPageAggregator(rm, laparams=LAParams())
    interp = PDFPageInterpreter(rm, dev)
    fonts = set()

    def walk(obj):
        for x in obj:
            if isinstance(x, LTChar):
                ch = x.get_text()
                if ch and 'Ѐ' <= ch <= 'ӿ':   # ћирилични опсег
                    fonts.add(x.fontname)
            elif hasattr(x, '__iter__'):
                walk(x)

    for page in PDFPage.get_pages(buf):
        interp.process_page(page)
        walk(dev.get_result())
    return fonts


def test_pdf_koristi_ugradjeni_font():
    """Ћирилични глифови морају бити исцртани УГРАЂЕНИМ фонтом (Liberation
    Serif из репоа, embedded subset), а не Helvetica-ом — да ради и на
    продукцији без системских фонтова."""
    buf = export_kr_dosije_pdf(_dosije())
    fonts = _fontovi_kojima_se_crta_cirilica(buf)
    assert fonts, 'ниједан ћирилични глиф није исцртан?'
    for fn in fonts:
        assert 'LiberationSerif' in fn, \
            f'ћирилица се црта фонтом без пуне подршке: {fn}'
        assert '+' in fn, f'фонт није уграђен (нема subset префикс): {fn}'
    assert not any('Helvetica' in fn for fn in fonts), \
        f'ћирилица се црта Helvetica-ом (квадратићи): {fonts}'


def test_bazni_exporter_takodje_ima_cirilicu():
    """Иста поправка важи за СВЕ PDF извозе (не само К-Р): базни exporter мора
    да исцрта ћирилицу уграђеним фонтом (нпр. сертификат узорка)."""
    from pdf_export import export_specimen_certificate_pdf
    specimen = {'inventarni_broj': 'M2051', 'naziv': 'Кварц са пиритом',
                'description': 'Конзервација č ž š'}
    buf = export_specimen_certificate_pdf(specimen, 'Минералошка збирка')
    text, _ = _extract(buf)
    assert 'ертификат' in text, f'нема ћирилице у базном извозу: {text[:150]!r}'
    fonts = _fontovi_kojima_se_crta_cirilica(buf)
    assert fonts, 'ниједан ћирилични глиф исцртан у базном извозу?'
    for fn in fonts:
        assert 'LiberationSerif' in fn, f'базни извоз не користи уграђени фонт: {fn}'
