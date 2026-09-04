"""Guard protiv vraćanja hardkodovanih boja na prioritetnim ekranima
(revizija 2026-08, batch 6, stavka 2).

Dve linije odbrane:
1. Strukturna: popravljeni selektori moraju koristiti var(--*) tokene —
   svaki povratak hex literala u te deklaracije obara test.
2. Merna: parovi tokena na koje su ekrani mapirani moraju zadovoljiti WCAG AA
   (4.5:1) u svetlom i tamnom režimu — promena vrednosti tokena koja obara
   kontrast takođe obara test (formula je ista kao u custom_theme.py).

Javni QR prikazi su samostalni dokumenti (bez main.css): tamo boje žive u
lokalnom :root bloku, pa se meri AA nad tim lokalnim --qr-* tokenima, a van
:root ne sme biti color/background hex literala.
"""

import re
from pathlib import Path

import pytest

import custom_theme as ct

ROOT = Path(__file__).parent

HEX_RE = re.compile(r'#[0-9a-fA-F]{3,8}\b')
AA = 4.5


def _read(rel):
    return (ROOT / rel).read_text(encoding='utf-8')


def _style_css(rel):
    """Sav CSS jednog ekrana: .css sirovo, .html spojeni <style> blokovi
    plus CSS fajlovi koje taj šablon povlači preko <link> (izdvojeni stilovi
    strana žive u static/css/, videti test_stilovi_izdvojeni.py)."""
    text = _read(rel)
    if rel.endswith('.css'):
        return text
    delovi = re.findall(r'<style[^>]*>(.*?)</style>', text, re.S)
    for ime in re.findall(r"filename='(css/[\w./-]+\.css)'", text):
        put = ROOT / 'static' / ime
        if put.exists():
            delovi.append(put.read_text(encoding='utf-8'))
    return '\n'.join(delovi)


def _rule_bodies(css, selector):
    """Tela pravila u kojima se selektor javlja tačno u listi selektora."""
    css = re.sub(r'/\*.*?\*/', '', css, flags=re.S)
    bodies = []
    for m in re.finditer(r'([^{}]+)\{([^{}]*)\}', css):
        selectors = [s.strip() for s in m.group(1).split(',')]
        if selector in selectors:
            bodies.append(m.group(2))
    return bodies


def _tokens_from_block(block_body):
    return dict(re.findall(r'(--[\w-]+)\s*:\s*([^;]+);', block_body))


def _resolve(tokens_layers, name, _depth=0):
    """Vrednost tokena kroz slojeve (kasniji sloj pobedjuje), prati var()."""
    assert _depth < 10, 'ciklus u tokenima: {}'.format(name)
    value = None
    for layer in tokens_layers:
        if name in layer:
            value = layer[name].strip()
    assert value is not None, 'token {} nije definisan'.format(name)
    m = re.fullmatch(r'var\((--[\w-]+)\)', value)
    if m:
        return _resolve(tokens_layers, m.group(1), _depth + 1)
    return value


# ---------------------------------------------------------------------------
# 1. Strukturna zaštita: popravljeni selektori su na tokenima, bez hex boja
# ---------------------------------------------------------------------------

FIXED_SELECTORS = [
    ('templates/admin_mineral_collection.html', '.table-header-light th'),
    # .page-header минерала замењен заједничким макроом (templates/_zaglavlje_strane.html, CSS у main.css)
    ('static/css/main.css', '.zaglavlje'),
    ('templates/admin_mineral_collection.html', '.nav-tabs-custom .nav-link'),
    ('templates/admin_mineral_collection.html', '.nav-tabs-custom .nav-link.active'),
    ('templates/admin_mineral_detail.html', '.mineral-name-box'),
    ('templates/admin_mineral_detail.html', '.mineral-locality-box'),
    ('templates/admin_mineral_detail.html', '.rruff-label-box'),
    ('templates/admin_mineral_detail.html', '.rruff-value-box'),
    ('templates/admin_mineral_detail.html', '.mineral-name'),
    ('templates/admin_mineral_detail.html', '.mineral-locality'),
    ('templates/admin_mineral_detail.html', '.box-modal-content'),
    ('templates/admin_mineral_detail.html', '.rruff-loading'),
    ('templates/admin_archive_dashboard.html', '.empty-state'),
    # revizija 2026-08, stavka 9: projekti — svakodnevni ekran bez ijednog
    # data-theme override-a; bele kartice/sivi tekst mapirani na tokene, pa
    # tamni režim dolazi sam od sebe.
    ('templates/admin_projekti.html', '.section-title'),
    ('templates/admin_projekti.html', '.plan-card .card-title'),
    ('templates/admin_projekti.html', '.plan-card .card-text'),
    ('templates/admin_projekti.html', '.doc-item'),
    ('templates/admin_projekti.html', '.key-info-card'),
    ('templates/admin_projekti.html', '.key-info-card h6'),
]


@pytest.mark.parametrize('rel,selector', FIXED_SELECTORS,
                         ids=['{}::{}'.format(Path(r).name, s) for r, s in FIXED_SELECTORS])
def test_fixed_selector_uses_tokens(rel, selector):
    bodies = _rule_bodies(_style_css(rel), selector)
    assert bodies, '{}: nema pravila za {}'.format(rel, selector)
    for body in bodies:
        hexes = HEX_RE.findall(body)
        assert not hexes, '{} {}: vraćena hardkodovana boja {}'.format(rel, selector, hexes)
        assert 'var(--' in body, '{} {}: ne koristi tokene'.format(rel, selector)


def test_dark_forced_light_header_overrides_removed():
    """Nasilno svetlo zaglavlje tabele u dark režimu je uklonjeno — tokeni
    sami prate temu, override bi vratio fiksne boje."""
    css = _style_css('templates/admin_mineral_collection.html')
    assert '[data-theme="dark"] .table-header-light' not in css
    assert '[data-theme="dark"] .nav-tabs-custom' not in css


def test_ai_overseer_css_has_no_hex_colors():
    css = _style_css('static/css/ai-overseer.css')
    hexes = HEX_RE.findall(css)
    assert not hexes, 'ai-overseer.css: hardkodovane boje {}'.format(sorted(set(hexes)))


# ---------------------------------------------------------------------------
# 2. Merna zaštita: tokeni na koje su ekrani mapirani zadovoljavaju AA
# ---------------------------------------------------------------------------

def _main_css_layers():
    css = _read('static/css/main.css')
    root = re.search(r':root\s*\{(.*?)\n\}', css, re.S)
    dark = re.search(r'\[data-theme="dark"\]\s*\{(.*?)\n\}', css, re.S)
    assert root and dark, 'main.css: nema :root ili [data-theme=dark] bloka'
    return _tokens_from_block(root.group(1)), _tokens_from_block(dark.group(1))


TOKEN_PAIRS = [
    ('--text-primary', '--bg-card'),
    ('--text-primary', '--bg-elevated'),
    ('--text-primary', '--bg-hover'),
    ('--text-secondary', '--bg-card'),
    ('--text-secondary', '--bg-elevated'),
    # revizija 2026-08, stavka 9: --text-muted je imao ~2.5:1 ugradjeno u sam
    # token svetle palete — od sada se meri kao i ostali parovi.
    ('--text-muted', '--bg-card'),
    ('--text-muted', '--bg-body'),
    ('--on-accent', '--primary'),
    ('--on-accent', '--primary-dark'),
    ('--success-text', '--success-soft'),
    # Порука о неуспелом учитавању слоја карте (.map-layer-error) — исти
    # разлог као --success-text: --danger као ТЕКСТ пада AA у тамној теми
    # (3.04:1 на --bg-card), па се греша исписује на овом пару.
    ('--status-busy-text', '--status-busy-bg'),
]


@pytest.mark.parametrize('mode', ['light', 'dark'])
@pytest.mark.parametrize('fg,bg', TOKEN_PAIRS)
def test_token_pairs_meet_aa(fg, bg, mode):
    root, dark = _main_css_layers()
    layers = [root] if mode == 'light' else [root, dark]
    fg_hex = ct.normalize_hex(_resolve(layers, fg))
    bg_hex = ct.normalize_hex(_resolve(layers, bg))
    assert fg_hex and bg_hex, '{}/{} nisu hex boje'.format(fg, bg)
    ratio = ct.contrast_ratio(fg_hex, bg_hex)
    assert ratio >= AA, '{} na {} u {} režimu: {:.2f}:1 < {}:1'.format(
        fg, bg, mode, ratio, AA)


# ---------------------------------------------------------------------------
# 3. Javni QR prikazi: lokalni --qr-* tokeni + AA nad njima
# ---------------------------------------------------------------------------

QR_FILES = ['templates/qr_nalepnica.html']

QR_PAIRS = [
    ('--qr-text', '--qr-surface'),
    ('--qr-muted', '--qr-surface'),
    ('--qr-on-header', '--qr-header-1'),
    ('--qr-on-header', '--qr-header-2'),
    ('--qr-accent', '--qr-surface'),
]


def _qr_layers(rel):
    css = _style_css(rel)
    root = re.search(r':root\s*\{(.*?)\}', css, re.S)
    assert root, '{}: nema :root bloka'.format(rel)
    return css, [_tokens_from_block(root.group(1))]


@pytest.mark.parametrize('rel', QR_FILES, ids=[Path(p).name for p in QR_FILES])
def test_qr_view_colors_only_in_root(rel):
    css, _ = _qr_layers(rel)
    stripped = re.sub(r':root\s*\{.*?\}', '', css, flags=re.S)
    offenders = []
    for m in re.finditer(
            r'(?:^|;|\{)\s*((?:background(?:-color)?|color|border(?:-[a-z]+)?-color|border(?:-[a-z]+)?)\s*:[^;}]*)',
            stripped):
        decl = m.group(1)
        if HEX_RE.search(decl):
            offenders.append(decl.strip())
    assert not offenders, '{}: hardkodovane boje van :root: {}'.format(rel, offenders)


@pytest.mark.parametrize('rel', QR_FILES, ids=[Path(p).name for p in QR_FILES])
@pytest.mark.parametrize('fg,bg', QR_PAIRS)
def test_qr_view_token_pairs_meet_aa(rel, fg, bg):
    _, layers = _qr_layers(rel)
    if fg not in layers[0]:
        pytest.skip('{} nema {} (nije u upotrebi)'.format(rel, fg))
    fg_hex = ct.normalize_hex(_resolve(layers, fg))
    bg_hex = ct.normalize_hex(_resolve(layers, bg))
    assert fg_hex and bg_hex, '{}: {}/{} nisu hex boje'.format(rel, fg, bg)
    ratio = ct.contrast_ratio(fg_hex, bg_hex)
    assert ratio >= AA, '{}: {} na {}: {:.2f}:1 < {}:1'.format(rel, fg, bg, ratio, AA)
