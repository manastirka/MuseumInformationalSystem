import os

os.environ.setdefault('FLASK_ENV', 'testing')
os.environ.setdefault('SECRET_KEY', 'test-secret')
os.environ.setdefault('REDIS_URL', '')
os.environ.setdefault('SESSION_TYPE', 'filesystem')
os.environ.setdefault('SESSION_FILE_DIR', '/tmp/museum-test-b-georoc')

import csv
import ssl

import local_georoc_data
import earthchem_georoc_api


# ---------------------------------------------------------------------------
# Finding 2: rows with empty MINERAL column inflate every mineral's statistics
# ---------------------------------------------------------------------------

def _write_csv(path, rows):
    fieldnames = ['MINERAL', 'LOCATION', 'ROCK NAME', 'TECTONIC SETTING',
                  'CITATION', 'SIO2(WT%)', 'CAO(WT%)']
    with open(path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def test_empty_mineral_rows_excluded_for_specific_mineral(tmp_path, monkeypatch):
    """A specific-mineral search must not count rows whose MINERAL cell is empty."""
    csv_path = tmp_path / 'CARBONATES.csv'
    rows = [
        {'MINERAL': 'Dolomite', 'CAO(WT%)': '30'},
        {'MINERAL': 'Dolomite', 'CAO(WT%)': '31'},
        {'MINERAL': '', 'CAO(WT%)': '99'},   # unlabeled -> must be excluded
        {'MINERAL': '', 'CAO(WT%)': '99'},   # unlabeled -> must be excluded
        {'MINERAL': 'Calcite', 'CAO(WT%)': '55'},  # different mineral -> excluded
    ]
    _write_csv(str(csv_path), rows)

    monkeypatch.setattr(local_georoc_data, '_data_cache', {})
    monkeypatch.setattr(local_georoc_data, 'get_csv_file_for_mineral',
                        lambda name: str(csv_path))

    data = local_georoc_data.get_georoc_data('dolomite')
    assert data is not None
    # Only the two real Dolomite rows should be counted.
    assert data['total_samples'] == 2
    # The CaO mean must reflect only the dolomite rows (30, 31), not the 99s.
    assert data['major_elements']['CaO']['mean'] == 30.5
    assert data['major_elements']['CaO']['max'] == 31.0


def test_generic_category_still_includes_all_rows(tmp_path, monkeypatch):
    """A generic category search (e.g. 'carbonate') keeps including every row."""
    csv_path = tmp_path / 'CARBONATES.csv'
    rows = [
        {'MINERAL': 'Dolomite', 'CAO(WT%)': '30'},
        {'MINERAL': '', 'CAO(WT%)': '40'},
        {'MINERAL': 'Calcite', 'CAO(WT%)': '55'},
    ]
    _write_csv(str(csv_path), rows)

    monkeypatch.setattr(local_georoc_data, '_data_cache', {})
    monkeypatch.setattr(local_georoc_data, 'get_csv_file_for_mineral',
                        lambda name: str(csv_path))

    data = local_georoc_data.get_georoc_data('carbonate')
    assert data is not None
    assert data['total_samples'] == 3


# ---------------------------------------------------------------------------
# Finding 1: TLS verification must default ON and be configurable
# ---------------------------------------------------------------------------

def test_ssl_context_verifies_by_default():
    """By default the module SSL context must verify certs and hostnames."""
    ctx = earthchem_georoc_api.ssl_context
    assert ctx.check_hostname is True
    assert ctx.verify_mode == ssl.CERT_REQUIRED


def test_insecure_tls_opt_in(monkeypatch):
    """The opt-in env var disables verification only when explicitly set."""
    monkeypatch.setenv('ALLOW_INSECURE_UPSTREAM_TLS', '1')
    ctx = earthchem_georoc_api.build_ssl_context()
    assert ctx.check_hostname is False
    assert ctx.verify_mode == ssl.CERT_NONE
