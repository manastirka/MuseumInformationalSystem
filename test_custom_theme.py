"""Tests for the phase-3 custom theme creator (definition validation, colour
maths, controls -> --pal-* mapping, and the set_theme custom path)."""

import os

os.environ.setdefault('FLASK_ENV', 'testing')
os.environ.setdefault('SECRET_KEY', 'test-secret')
os.environ.setdefault('REDIS_URL', '')
os.environ.setdefault('SESSION_TYPE', 'filesystem')
os.environ.setdefault('SESSION_FILE_DIR', '/tmp/museum-test-custom-theme')

import pytest
from flask import Flask, session

import custom_theme as ct
import core_app_views


@pytest.fixture
def theme_app():
    flask_app = Flask(__name__)
    flask_app.config['SECRET_KEY'] = 'test-secret'
    return flask_app


def _good_colors():
    return dict(ct.DEFAULT_DEFINITION['colors'])


# ---- normalize_hex --------------------------------------------------------

@pytest.mark.parametrize('raw,expected', [
    ('#1D5FAB', '#1d5fab'),
    ('1d5fab', '#1d5fab'),
    ('#abc', '#aabbcc'),
    ('ABC', '#aabbcc'),
])
def test_normalize_hex_accepts(raw, expected):
    assert ct.normalize_hex(raw) == expected


@pytest.mark.parametrize('raw', ['red', '#12', '#1234', '#12g4ab', '', None, 123, '#12345'])
def test_normalize_hex_rejects(raw):
    assert ct.normalize_hex(raw) is None


# ---- validate_definition --------------------------------------------------

def test_validate_default_ok():
    cleaned, err = ct.validate_definition(ct.DEFAULT_DEFINITION)
    assert err is None
    assert set(cleaned['colors']) == set(ct.COLOR_KEYS)
    assert cleaned['shadow'] in ct.SHADOW_OPTIONS
    assert ct.RADIUS_MIN <= cleaned['radius'] <= ct.RADIUS_MAX


def test_validate_rejects_non_dict():
    assert ct.validate_definition([1, 2])[0] is None
    assert ct.validate_definition('x')[0] is None
    assert ct.validate_definition(None)[0] is None


def test_validate_rejects_missing_colors():
    assert ct.validate_definition({'shadow': 'soft', 'radius': 8})[0] is None


def test_validate_rejects_bad_color():
    colors = _good_colors()
    colors['primary'] = 'rgb(0,0,0)'
    assert ct.validate_definition({'colors': colors, 'shadow': 'soft', 'radius': 8})[0] is None


def test_validate_rejects_missing_color_key():
    colors = _good_colors()
    del colors['text']
    assert ct.validate_definition({'colors': colors, 'shadow': 'soft', 'radius': 8})[0] is None


def test_validate_rejects_bad_shadow():
    assert ct.validate_definition({'colors': _good_colors(), 'shadow': 'glow', 'radius': 8})[0] is None


@pytest.mark.parametrize('radius', [-1, 21, 999, True, 'x', None, [1]])
def test_validate_rejects_bad_radius(radius):
    assert ct.validate_definition({'colors': _good_colors(), 'shadow': 'soft', 'radius': radius})[0] is None


def test_validate_drops_unknown_keys():
    """Untrusted import: unknown keys must never survive into the cleaned dict."""
    raw = {'colors': dict(_good_colors(), evil='</style><script>'),
           'shadow': 'soft', 'radius': 8, 'onload': 'boom'}
    cleaned, err = ct.validate_definition(raw)
    assert err is None
    assert set(cleaned.keys()) == {'colors', 'shadow', 'radius'}
    assert set(cleaned['colors'].keys()) == set(ct.COLOR_KEYS)


def test_validate_normalizes_3digit_and_case():
    colors = _good_colors()
    colors['primary'] = '#ABC'
    cleaned, err = ct.validate_definition({'colors': colors, 'shadow': 'soft', 'radius': 8.6})
    assert err is None
    assert cleaned['colors']['primary'] == '#aabbcc'
    assert cleaned['radius'] == 9  # rounded


# ---- colour maths (pinned; mirror of theme_creator.js) --------------------

def test_contrast_extremes():
    assert round(ct.contrast_ratio('#ffffff', '#000000'), 1) == 21.0
    assert round(ct.contrast_ratio('#123456', '#123456'), 2) == 1.0


def test_best_ink():
    assert ct.best_ink('#ffffff') == '#111111'
    assert ct.best_ink('#000000') == '#ffffff'
    assert ct.best_ink('#1d5fab') == '#ffffff'


def test_darken_lighten_pins():
    assert ct.darken('#646464', 0.5) == '#323232'
    assert ct.lighten('#000000', 0.5) == '#808080'
    assert ct.darken('#ffffff', 0.0) == '#ffffff'


# ---- pal token mapping ----------------------------------------------------

def test_pal_tokens_shape():
    cleaned, _ = ct.validate_definition(ct.DEFAULT_DEFINITION)
    tokens = ct.pal_tokens(cleaned)
    for key in ('--pal-primary', '--pal-bg-nav', '--pal-side-bg', '--pal-thead-text',
                '--pal-sel-text', '--pal-on-accent', '--pal-link', '--pal-warning',
                '--pal-shadow', '--pal-radius-card', '--pal-radius-btn'):
        assert key in tokens
    assert tokens['--pal-primary'] == cleaned['colors']['primary']
    assert tokens['--pal-radius-btn'] == '8px'
    assert tokens['--pal-radius-card'] == '10px'
    # thead/side/sel ink is derived by contrast, not copied
    assert tokens['--pal-thead-text'] in ('#ffffff', '#111111')


def test_pal_css_is_declaration_string():
    cleaned, _ = ct.validate_definition(ct.DEFAULT_DEFINITION)
    css = ct.pal_css(cleaned)
    assert '--pal-primary:#1d5fab;' in css
    # No stray quotes/angle brackets that could break out of style="..."
    assert '"' not in css and '<' not in css and '>' not in css


def test_bs_theme_by_luminance():
    light, _ = ct.validate_definition(ct.DEFAULT_DEFINITION)
    assert ct.bs_theme(light) == 'light'
    dark_def = {'colors': dict(_good_colors(), card='#161b22'), 'shadow': 'soft', 'radius': 8}
    dark, _ = ct.validate_definition(dark_def)
    assert ct.bs_theme(dark) == 'dark'


# ---- normalize_name -------------------------------------------------------

def test_normalize_name():
    assert ct.normalize_name('  Моја   тема  ') == 'Моја тема'
    assert ct.normalize_name('') is None
    assert ct.normalize_name('   ') is None
    assert ct.normalize_name(None) is None
    assert len(ct.normalize_name('x' * 200)) == 80


# ---- core_app_views: palette + set_theme custom path ----------------------

def test_normalize_palette_accepts_custom():
    assert core_app_views.normalize_theme_palette('custom') == 'custom'


def test_current_custom_theme_id_parsing(theme_app):
    with theme_app.test_request_context('/'):
        session['museum_custom_id'] = 7
        assert core_app_views.current_custom_theme_id() == 7
        session['museum_custom_id'] = None
        assert core_app_views.current_custom_theme_id() is None
        session['museum_custom_id'] = 'x'
        assert core_app_views.current_custom_theme_id() is None
        session['museum_custom_id'] = -3
        assert core_app_views.current_custom_theme_id() is None


def test_set_theme_custom_requires_id(theme_app):
    """palette=custom without a custom_id is rejected (would render token-less)."""
    with theme_app.test_request_context(
        '/set_theme', method='POST',
        json={'mode': 'light', 'accent': 'podrazumevano', 'palette': 'custom'},
    ):
        response = core_app_views.set_theme_preference()
    status = response[1] if isinstance(response, tuple) else response.status_code
    assert status == 400


def test_set_theme_custom_anonymous_ok(theme_app):
    """Anonymous (no DB) custom set with a positive id stores session + cookie."""
    with theme_app.test_request_context(
        '/set_theme', method='POST',
        json={'mode': 'light', 'accent': 'podrazumevano', 'palette': 'custom', 'custom_id': 5},
    ):
        response = core_app_views.set_theme_preference()
        assert session['museum_palette'] == 'custom'
        assert session['museum_custom_id'] == 5
    assert response.status_code == 200
    cookies = response.headers.getlist('Set-Cookie')
    assert any('museum_palette=custom' in c for c in cookies)
    assert any('museum_custom_id=5' in c for c in cookies)


def test_set_theme_leaving_custom_clears_id(theme_app):
    with theme_app.test_request_context(
        '/set_theme', method='POST',
        json={'mode': 'light', 'accent': 'podrazumevano', 'palette': 'plava-tamna'},
    ):
        session['museum_custom_id'] = 5
        response = core_app_views.set_theme_preference()
        assert session['museum_palette'] == 'plava-tamna'
        assert session['museum_custom_id'] is None
    cookies = response.headers.getlist('Set-Cookie')
    # museum_custom_id cookie is cleared (empty value) when leaving custom
    assert any('museum_custom_id=;' in c or 'museum_custom_id="";' in c
               or 'museum_custom_id=;' in c.replace(' ', '') for c in cookies)


def test_current_custom_theme_render_noncustom_is_empty(theme_app):
    with theme_app.test_request_context('/'):
        session['museum_palette'] = 'plava-klasicna'
        css, bs = core_app_views.current_custom_theme_render()
        assert css == ''
        assert bs == 'light'


# ---- AA contrast enforcement on save paths --------------------------------

def _all_white_definition():
    colors = _good_colors()
    for key in ('text', 'body', 'card', 'link'):
        colors[key] = '#ffffff'
    return {'colors': colors, 'shadow': 'soft', 'radius': 8}


def test_contrast_failures_reports_failing_pairs():
    cleaned, err = ct.validate_definition(_all_white_definition())
    assert err is None
    fails = ct.contrast_failures(cleaned)
    labels = [label for label, _ in fails]
    assert 'Текст на позадини' in labels
    assert 'Текст на картици' in labels
    assert 'Линк на картици' in labels
    assert all(ratio < ct.AA_MIN_RATIO for _, ratio in fails)


def test_contrast_failures_default_is_clean():
    assert ct.contrast_failures(ct.DEFAULT_DEFINITION) == []


def test_validate_require_aa_accepts_default():
    cleaned, err = ct.validate_definition(ct.DEFAULT_DEFINITION, require_aa=True)
    assert err is None
    assert cleaned is not None


def test_validate_require_aa_rejects_and_names_pair():
    cleaned, err = ct.validate_definition(_all_white_definition(), require_aa=True)
    assert cleaned is None
    assert 'Текст на позадини' in err
    assert '1.00:1' in err


def test_validate_without_require_aa_stays_lenient():
    """Read paths (render/apply/export of stored themes) must keep working."""
    cleaned, err = ct.validate_definition(_all_white_definition())
    assert err is None
    assert cleaned is not None


class _ThemeAuthStub:
    def __init__(self, existing=None):
        self.created = []
        self.updated = []
        self.existing = existing

    def create_custom_theme(self, email, name, definition):
        self.created.append((email, name, definition))
        return 1

    def get_custom_theme(self, email, theme_id):
        return self.existing

    def update_custom_theme(self, email, theme_id, name, definition):
        self.updated.append((email, theme_id, name, definition))
        return True


def test_create_route_rejects_aa_failing_theme(theme_app, monkeypatch):
    import custom_theme_views as views
    stub = _ThemeAuthStub()
    monkeypatch.setattr(views, '_auth', lambda: stub)
    with theme_app.test_request_context(
        '/podesavanja/teme', method='POST',
        json={'name': 'Бела', 'definition': _all_white_definition()},
    ):
        session['user_email'] = 'test@example.com'
        response = views.create_custom_theme()
    payload, status = response if isinstance(response, tuple) else (response, 200)
    assert status == 400
    body = payload.get_json()
    assert body['status'] == 'error'
    assert 'Текст на позадини' in body['message']
    assert ':1' in body['message']
    assert stub.created == []


def test_update_route_rejects_aa_failing_definition(theme_app, monkeypatch):
    import custom_theme_views as views
    stub = _ThemeAuthStub(existing={'id': 7, 'name': 'Стара', 'definition': dict(ct.DEFAULT_DEFINITION)})
    monkeypatch.setattr(views, '_auth', lambda: stub)
    with theme_app.test_request_context(
        '/podesavanja/teme/7', method='POST',
        json={'definition': _all_white_definition()},
    ):
        session['user_email'] = 'test@example.com'
        response = views.update_custom_theme(7)
    payload, status = response if isinstance(response, tuple) else (response, 200)
    assert status == 400
    assert 'AA' in payload.get_json()['message']
    assert stub.updated == []


def test_import_route_rejects_aa_failing_theme(theme_app, monkeypatch):
    import custom_theme_views as views
    stub = _ThemeAuthStub()
    monkeypatch.setattr(views, '_auth', lambda: stub)
    with theme_app.test_request_context(
        '/podesavanja/teme/uvoz', method='POST',
        json={'mis_custom_theme': 1, 'name': 'Бела', 'definition': _all_white_definition()},
    ):
        session['user_email'] = 'test@example.com'
        response = views.import_custom_theme()
    payload, status = response if isinstance(response, tuple) else (response, 200)
    assert status == 400
    assert 'AA' in payload.get_json()['message']
    assert stub.created == []
