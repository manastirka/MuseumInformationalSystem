"""Custom theme (phase 3) — definition schema, validation, colour maths and the
controls -> --pal-* token mapping.

A custom theme is a *private* per-user look built from individual colour picks.
It renders through the SAME --pal-* token layer as the flat palettes (migrations
033/037): the twelve picked colours plus shadow strength and corner radius are
mapped here to concrete --pal-* values, which the server injects inline on
<html data-palette="custom">. There is no new CSS engine and no server-side
per-request colour drift — the database stores the semantic picks, this module
resolves them deterministically, and the same formulas are mirrored in
static/js/theme_creator.js for the live preview.

Security: import/paste is never trusted. validate_definition() rebuilds a clean
definition from known keys only, rejecting anything malformed, so a hostile JSON
file can never smuggle arbitrary CSS through the --pal-* values (every value is a
validated hex colour, a known enum, or a bounded integer).
"""

import re

# The twelve user-picked colours (spec point 1). Order is the picker order.
COLOR_KEYS = (
    'primary',    # osnovna boja aplikacije (primarni brend/akcije)
    'header',     # boja zaglavlja (gornja traka + zaglavlje tabela)
    'sidebar',    # boja bočnog menija
    'body',       # boja pozadine radne površine
    'card',       # boja kartica/panela
    'accent',     # akcentna boja (linkovi/isticanja, može ≠ primary)
    'selection',  # boja selektovanog reda
    'button',     # boja dugmadi (može ≠ primary)
    'text',       # boja teksta
    'border',     # boja okvira/linija
    'link',       # boja linkova
    'warning',    # boja upozorenja
)

SHADOW_OPTIONS = ('none', 'soft', 'medium', 'strong')
RADIUS_MIN = 0
RADIUS_MAX = 20

# Sane, AA-clean starting point (a calm blue-on-white look) shown when a user
# opens the creator with no theme loaded. Mirrors the app's default character.
DEFAULT_DEFINITION = {
    'colors': {
        'primary': '#1d5fab',
        'header': '#16375d',
        'sidebar': '#143257',
        'body': '#f1f5fb',
        'card': '#ffffff',
        'accent': '#1d5fab',
        'selection': '#d9e7fa',
        'button': '#1d5fab',
        'text': '#1f2a37',
        'border': '#d5dde9',
        'link': '#1d5fab',
        'warning': '#8a5606',
    },
    'shadow': 'soft',
    'radius': 8,
}

_HEX3 = re.compile(r'^#?([0-9a-fA-F]{3})$')
_HEX6 = re.compile(r'^#?([0-9a-fA-F]{6})$')

# Box-shadow strings for the four shadow strengths (mapped to --pal-shadow).
_SHADOW_CSS = {
    'none': 'none',
    'soft': '0 1px 3px rgba(15, 23, 42, 0.08), 0 1px 2px rgba(15, 23, 42, 0.06)',
    'medium': '0 4px 12px rgba(15, 23, 42, 0.12), 0 2px 4px rgba(15, 23, 42, 0.08)',
    'strong': '0 10px 28px rgba(15, 23, 42, 0.22), 0 4px 10px rgba(15, 23, 42, 0.16)',
}


# --------------------------------------------------------------------------- #
# Colour maths (kept trivial and mirrored 1:1 in theme_creator.js)
# --------------------------------------------------------------------------- #

def normalize_hex(value):
    """Return a lowercase #rrggbb string, or None if not a valid hex colour."""
    if not isinstance(value, str):
        return None
    text = value.strip()
    m6 = _HEX6.match(text)
    if m6:
        return '#' + m6.group(1).lower()
    m3 = _HEX3.match(text)
    if m3:
        r, g, b = m3.group(1).lower()
        return '#' + r + r + g + g + b + b
    return None


def _to_rgb(hex_color):
    h = hex_color.lstrip('#')
    return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16))


def _to_hex(rgb):
    return '#' + ''.join('{:02x}'.format(max(0, min(255, int(round(c))))) for c in rgb)


def darken(hex_color, factor):
    """Scale each channel toward black by `factor` (0..1)."""
    r, g, b = _to_rgb(hex_color)
    return _to_hex((r * (1 - factor), g * (1 - factor), b * (1 - factor)))


def lighten(hex_color, factor):
    """Scale each channel toward white by `factor` (0..1)."""
    r, g, b = _to_rgb(hex_color)
    return _to_hex((r + (255 - r) * factor,
                    g + (255 - g) * factor,
                    b + (255 - b) * factor))


def _channel_lin(c):
    cs = c / 255.0
    return cs / 12.92 if cs <= 0.03928 else ((cs + 0.055) / 1.055) ** 2.4


def relative_luminance(hex_color):
    r, g, b = _to_rgb(hex_color)
    return 0.2126 * _channel_lin(r) + 0.7152 * _channel_lin(g) + 0.0722 * _channel_lin(b)


def contrast_ratio(hex_a, hex_b):
    """WCAG 2.x contrast ratio between two colours (>= 1.0)."""
    la = relative_luminance(hex_a)
    lb = relative_luminance(hex_b)
    hi, lo = (la, lb) if la >= lb else (lb, la)
    return (hi + 0.05) / (lo + 0.05)


def best_ink(bg_hex):
    """Pick the readable ink (near-white or near-black) for a background."""
    white, black = '#ffffff', '#111111'
    return white if contrast_ratio(white, bg_hex) >= contrast_ratio(black, bg_hex) else black


# --------------------------------------------------------------------------- #
# Validation
# --------------------------------------------------------------------------- #

def validate_definition(raw):
    """Validate and normalise a custom theme definition.

    Rebuilds a clean definition from known keys only — untrusted input (import
    or paste) can never inject unknown keys or non-colour values. Returns
    (cleaned_dict, None) on success or (None, error_message) on failure.
    """
    if not isinstance(raw, dict):
        return None, 'Дефиниција теме мора бити објекат.'

    raw_colors = raw.get('colors')
    if not isinstance(raw_colors, dict):
        return None, 'Недостаје скуп боја (colors).'

    colors = {}
    for key in COLOR_KEYS:
        norm = normalize_hex(raw_colors.get(key))
        if norm is None:
            return None, 'Неисправна или недостајућа боја: {}.'.format(key)
        colors[key] = norm

    shadow = raw.get('shadow', 'soft')
    if shadow not in SHADOW_OPTIONS:
        return None, 'Неисправна јачина сенке.'

    radius = raw.get('radius', 8)
    if isinstance(radius, bool) or not isinstance(radius, (int, float)):
        return None, 'Неисправан степен заобљености.'
    radius = int(round(radius))
    if radius < RADIUS_MIN or radius > RADIUS_MAX:
        return None, 'Заобљеност мора бити између {} и {} px.'.format(RADIUS_MIN, RADIUS_MAX)

    return {'colors': colors, 'shadow': shadow, 'radius': radius}, None


def normalize_name(raw):
    """Trim a theme name to a stored-safe value, or return None if empty."""
    if not isinstance(raw, str):
        return None
    name = ' '.join(raw.split()).strip()
    if not name:
        return None
    return name[:80]


# --------------------------------------------------------------------------- #
# controls -> --pal-* token mapping
# --------------------------------------------------------------------------- #

def pal_tokens(definition):
    """Map a *validated* definition to the concrete --pal-* token dict.

    The shared `[data-palette]` block in main.css maps these --pal-* values to
    the real design tokens, so a custom theme reuses the entire flat-palette
    engine. Optional identity vars (--pal-accent/-btn/-link/-warning/-on-accent/
    -shadow) are consumed there with fallbacks, so they only affect 'custom'.
    """
    c = definition['colors']
    primary, header, sidebar = c['primary'], c['header'], c['sidebar']
    body, card, accent = c['body'], c['card'], c['accent']
    selection, button, text = c['selection'], c['button'], c['text']
    border, link, warning = c['border'], c['link'], c['warning']

    tokens = {
        '--pal-primary': primary,
        '--pal-primary-dark': darken(primary, 0.15),
        '--pal-primary-light': lighten(primary, 0.15),
        '--pal-bg-body': body,
        '--pal-bg-card': card,
        '--pal-bg-nav': header,
        '--pal-elevated': darken(card, 0.03),
        '--pal-hover': darken(card, 0.06),
        '--pal-stripe': darken(card, 0.035),
        '--pal-text': text,
        '--pal-text2': lighten(text, 0.18),
        '--pal-muted': lighten(text, 0.32),
        '--pal-border': border,
        '--pal-thead-bg': header,
        '--pal-thead-text': best_ink(header),
        '--pal-sel-bg': selection,
        '--pal-sel-text': best_ink(selection),
        '--pal-side-bg': sidebar,
        '--pal-side-text': best_ink(sidebar),
        # Identity overrides consumed via fallback in the mapping block:
        '--pal-accent': accent,
        '--pal-accent-dark': darken(accent, 0.15),
        '--pal-btn': button,
        '--pal-btn-dark': darken(button, 0.15),
        '--pal-on-accent': best_ink(button),
        '--pal-link': link,
        '--pal-warning': warning,
        '--pal-shadow': _SHADOW_CSS[definition['shadow']],
        '--pal-radius-card': '{}px'.format(definition['radius'] + 2),
        '--pal-radius-btn': '{}px'.format(definition['radius']),
    }
    return tokens


def pal_css(definition):
    """Serialise pal_tokens() to an inline style string for the <html> tag."""
    return ''.join('{}:{};'.format(k, v) for k, v in pal_tokens(definition).items())


def bs_theme(definition):
    """Bootstrap base ('dark'/'light') chosen by the card/body luminance so
    Bootstrap's own component chrome (dropdowns, modals) reads correctly under a
    dark custom theme. Custom never uses the app dark-flat layer."""
    return 'dark' if relative_luminance(definition['colors']['card']) < 0.4 else 'light'
