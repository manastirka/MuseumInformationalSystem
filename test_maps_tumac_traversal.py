"""Revizija 2026-08 (batch 6, stavka 11): path traversal na tumaču
geološkog lista.

Nalaz: folder_name jeste sanitizovan, ali tumac_file iz
geological_map_sheets.json NIJE — ide u os.path.join pa send_file bez
resolve+prefix provere, pa zlonameran unos u JSON-u može da servira
proizvoljan fajl (npr. .env). Primenjen isti obrazac kao u fototeci:
(root / tumac_file).resolve() + odbijanje svega što ne počinje root + sep.
"""

import os

os.environ.setdefault('FLASK_ENV', 'testing')
os.environ.setdefault('SECRET_KEY', 'test-secret')
os.environ.setdefault('REDIS_URL', '')
os.environ.setdefault('SESSION_TYPE', 'filesystem')
os.environ.setdefault('SESSION_FILE_DIR', '/tmp/museum-test-maps-tumac')

import flask
import pytest

import maps_layer_views


@pytest.fixture
def app_root(tmp_path):
    tumaci = tmp_path / 'Karte' / 'Tumaci Srbija'
    tumaci.mkdir(parents=True)
    (tumaci / 'tumac-l34.pdf').write_bytes(b'%PDF-1.4 legitiman tumac')
    # "Tajna" van korena tumača — meta traversal napada.
    (tmp_path / 'tajna.env').write_text('SECRET_KEY=ne-sme-da-procuri',
                                        encoding='utf-8')
    return tmp_path


def _call(monkeypatch, app_root, tumac_file):
    monkeypatch.setattr(
        maps_layer_views, '_get_geological_sheets',
        lambda root: [{'folder': 'list-1', 'tumac': {'tumac_file': tumac_file}}])
    test_app = flask.Flask(__name__)
    with test_app.test_request_context('/'):
        return maps_layer_views.api_geological_sheet_tumac('list-1', str(app_root))


def test_traversal_u_tumac_file_se_odbija(monkeypatch, app_root):
    response = _call(monkeypatch, app_root, '../../tajna.env')
    payload, status = response if isinstance(response, tuple) else (response, 200)
    assert status == 400, 'putanja van korena mora biti odbijena'
    assert 'ne-sme-da-procuri' not in str(getattr(payload, 'get_data', lambda: b'')())


def test_apsolutna_putanja_se_odbija(monkeypatch, app_root):
    response = _call(monkeypatch, app_root, '/etc/passwd')
    _, status = response if isinstance(response, tuple) else (response, 200)
    assert status == 400


def test_legitiman_tumac_se_sluzi(monkeypatch, app_root):
    response = _call(monkeypatch, app_root, 'tumac-l34.pdf')
    assert not isinstance(response, tuple)
    assert response.status_code == 200
    assert response.mimetype == 'application/pdf'
    response.close()


def test_nepostojeci_tumac_daje_404(monkeypatch, app_root):
    response = _call(monkeypatch, app_root, 'nema-ovog.pdf')
    _, status = response if isinstance(response, tuple) else (response, 200)
    assert status == 404


def test_traversal_u_imenu_slike_lista_se_odbija(monkeypatch, app_root):
    """Isti JSON hrani i imena slika lista — i ta putanja mora kroz proveru."""
    monkeypatch.setattr(
        maps_layer_views, '_get_geological_sheets',
        lambda root: [{'folder': 'list-1',
                       'files': {'front': '../../../tajna.env'}}])
    test_app = flask.Flask(__name__)
    with test_app.test_request_context('/'):
        response = maps_layer_views.api_geological_sheet_image(
            'list-1', 'front', str(app_root))
    _, status = response if isinstance(response, tuple) else (response, 200)
    assert status == 400
