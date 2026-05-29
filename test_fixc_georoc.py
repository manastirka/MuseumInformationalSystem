"""Behavior tests for LOW-severity hardening fixes in the georoc cluster.

Covers:
- local_georoc_data cache key must include max_samples
- local_georoc_data per-row mineral filter must strip whitespace
- earthchem_georoc_api 'magnesite' rock association (typo 'magneite')
"""

import os

os.environ.setdefault('FLASK_ENV', 'testing')
os.environ.setdefault('SECRET_KEY', 'test-secret')
os.environ.setdefault('REDIS_URL', '')
os.environ.setdefault('SESSION_TYPE', 'filesystem')
os.environ.setdefault('SESSION_FILE_DIR', '/tmp/museum-test-c-georoc')

import io

import local_georoc_data
import earthchem_georoc_api


CSV_HEADER = (
    "MINERAL,LOCATION,ROCK NAME,TECTONIC SETTING,CITATION,SIO2(WT%),MGO(WT%),SR(PPM)\n"
)


def _make_csv(rows):
    return CSV_HEADER + "".join(rows)


def _patch_csv(monkeypatch, csv_text, mineral_filename='X.csv'):
    """Force get_csv_file_for_mineral to resolve and open(...) to read csv_text."""
    monkeypatch.setattr(
        local_georoc_data, 'get_csv_file_for_mineral',
        lambda name: '/fake/' + mineral_filename
    )

    real_open = open

    def fake_open(path, *args, **kwargs):
        if str(path).startswith('/fake/'):
            return io.StringIO(csv_text)
        return real_open(path, *args, **kwargs)

    monkeypatch.setattr('builtins.open', fake_open)


def test_cache_key_includes_max_samples(monkeypatch):
    """Different max_samples on the same mineral must not collide in the cache."""
    local_georoc_data._data_cache.clear()

    rows = [
        f"olivine,Loc{i},dunite,arc,[ref{i}],40.0,45.0,5.0\n" for i in range(10)
    ]
    _patch_csv(monkeypatch, _make_csv(rows))

    first = local_georoc_data.get_georoc_data('olivine', max_samples=3)
    second = local_georoc_data.get_georoc_data('olivine', max_samples=8)

    assert first is not None and second is not None
    # If the cache key ignores max_samples, the second call returns the cached
    # first result (3 samples) instead of 8.
    assert first['total_samples'] == 3
    assert second['total_samples'] == 8


def test_generic_category_filter_strips_whitespace(monkeypatch):
    """A whitespace-padded generic category must still include all rows."""
    local_georoc_data._data_cache.clear()

    # Rows with assorted MINERAL labels; generic 'carbonate' should include all.
    rows = [
        "calcite,L1,limestone,arc,[r1],0.0,1.0,10.0\n",
        "dolomite,L2,dolostone,arc,[r2],0.0,2.0,20.0\n",
        "siderite,L3,iron,arc,[r3],0.0,3.0,30.0\n",
    ]
    _patch_csv(monkeypatch, _make_csv(rows))

    data = local_georoc_data.get_georoc_data('carbonate ', max_samples=5000)

    assert data is not None
    # 'carbonate ' (padded) is a generic category once stripped -> all 3 rows.
    assert data['total_samples'] == 3


def test_magnesite_has_correct_rock_associations():
    """'magnesite' must resolve to its carbonate rock associations, not default."""
    rocks = earthchem_georoc_api.get_mineral_rock_associations('magnesite')

    default = earthchem_georoc_api.MINERAL_ROCK_ASSOCIATIONS['default']
    assert rocks != default
    assert 'dolostone' in rocks
    assert 'serpentinite' in rocks
    # The misspelled key must no longer exist.
    assert 'magneite' not in earthchem_georoc_api.MINERAL_ROCK_ASSOCIATIONS
    assert 'magnesite' in earthchem_georoc_api.MINERAL_ROCK_ASSOCIATIONS
