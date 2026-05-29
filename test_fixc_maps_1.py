"""Focused regression tests for maps-1 hardening fixes (Phase C)."""

import os

os.environ.setdefault('FLASK_ENV', 'testing')
os.environ.setdefault('SECRET_KEY', 'test-secret')
os.environ.setdefault('REDIS_URL', '')
os.environ.setdefault('SESSION_TYPE', 'filesystem')
os.environ.setdefault('SESSION_FILE_DIR', '/tmp/museum-test-c-maps-1')

import maps_profile_support


def _find_serpentinite_low_value_branch():
    """Return an (r, g, b) that lands in the hue 12-52 / low value-saturation branch."""
    for r in range(256):
        for g in range(256):
            for b in range(256):
                hue, sat, val = maps_profile_support.rgb_to_hsv(r, g, b)
                if 12 <= hue <= 52 and 18 <= sat <= 75 and 20 <= val <= 62:
                    earlier = (
                        (265 <= hue <= 345 and sat > 12)
                        or (195 <= hue <= 265 and sat > 12)
                        or (155 <= hue <= 198 and sat > 12)
                        or (68 <= hue <= 158 and sat > 12)
                        or (sat < 8 and 20 < val < 90)
                    )
                    if not earlier:
                        return (r, g, b)
    return None


def test_ophiolite_serpentinite_era_color_is_canonical_teal():
    """Serpentinite classified via the hue 12-52 branch must carry the Офиолити teal era_color."""
    rgb = _find_serpentinite_low_value_branch()
    assert rgb is not None, "could not find an RGB hitting the target branch"

    result = maps_profile_support.classify_geo_color(rgb[0], rgb[1], rgb[2])

    assert result is not None
    assert result['era'] == 'Офиолити'
    assert result['unit_name_en'] == 'Serpentinite'
    # era_color must match the canonical Офиолити color, not the Paleozoik brown.
    assert result['era_color'] == '#00695c'
    # color is already canonical-corrected; assert consistency too.
    assert result['color'] == '#00695c'


def test_other_ophiolite_branches_already_canonical():
    """Any color classified as Офиолити must carry the teal era_color (regression guard)."""
    seen = 0
    for r in range(0, 256, 3):
        for g in range(0, 256, 3):
            for b in range(0, 256, 3):
                result = maps_profile_support.classify_geo_color(r, g, b)
                if result and result['era'] == 'Офиолити':
                    seen += 1
                    assert result['era_color'] == '#00695c', (
                        f"({r},{g},{b}) -> {result['unit_name_en']} "
                        f"era_color {result['era_color']}"
                    )
    assert seen > 0, "expected at least one Офиолити classification across the RGB sweep"
