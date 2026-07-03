"""Reproduces the broken per-day forecast conditions on the RHMZ page.

RHMZ switched its 5-day forecast row to numeric GIF icons
(``repository/ikonice/prognoza/<N>.gif``) carrying a generic ``alt="Pojava"``.
The text-based icon parser could no longer infer a condition, so every day fell
back to condition ``none`` / "Без детаљног описа" (temperatures still parsed).

The fixture ``tests/fixtures/rhmz_forecast_page.html`` is a real RHMZ forecast
page whose ``Pojava`` row uses icon codes [6, 4, 3, 2, 2]; the test verifies the
numeric legend resolves each to the correct condition fully offline.
"""

from pathlib import Path

import dashboard_data_support as dds

_FORECAST_PAGE = Path(__file__).parent / 'tests' / 'fixtures' / 'rhmz_forecast_page.html'

_VALID_CONDITIONS = {'clear', 'cloudy', 'drizzle', 'fog', 'rain', 'snow', 'thunderstorm'}


def test_forecast_icon_codes_resolve_to_conditions():
    result = dds._parse_rhmz_forecast_page(_FORECAST_PAGE.read_text(encoding='utf-8'))
    days = result['days']
    assert len(days) == 5

    # Pojava row icon codes in the fixture: [6, 4, 3, 2, 2].
    expected = [
        ('rain', 'Могући пљускови'),
        ('cloudy', 'Мало и умерено облачно'),
        ('clear', 'Претежно сунчано'),
        ('clear', 'Сунчано'),
        ('clear', 'Сунчано'),
    ]
    assert [(d['condition'], d['description']) for d in days] == expected

    # The regression we are fixing: no day should fall back to the unknown state.
    assert all(d['condition'] != 'none' for d in days)
    assert all(d['description'] != 'Без детаљног описа' for d in days)


def test_icon_legend_is_complete_and_uses_valid_conditions():
    legend = dds._RHMZ_FORECAST_ICON_CODES
    assert set(range(1, 21)).issubset(legend.keys())
    for code, (condition, description) in legend.items():
        assert condition in _VALID_CONDITIONS, (code, condition)
        assert isinstance(description, str) and description
