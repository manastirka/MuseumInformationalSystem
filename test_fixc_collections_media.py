"""Behavior tests for LOW-severity hardening fixes in the collections-media cluster.

Covers:
- render_qr_view_specimen must resolve specimens for every registered QR
  collection (e.g. paleobotany), not only the three hard-coded ones, so a
  /qr_view/paleobotany/<n> request no longer always returns a 404.

Templates are mocked so the tests assert the function's control flow
(which collection branch resolved the specimen and the resulting status)
rather than rendered HTML.
"""

import os

os.environ.setdefault('FLASK_ENV', 'testing')
os.environ.setdefault('SECRET_KEY', 'test-secret')
os.environ.setdefault('REDIS_URL', '')
os.environ.setdefault('SESSION_TYPE', 'filesystem')
os.environ.setdefault('SESSION_FILE_DIR', '/tmp/museum-test-c-collections-media')

from flask import Flask

import collection_media_views


def _make_app(qr_records_by_type):
    """Build a minimal Flask app exposing get_qr_collection_records like the real app."""
    app = Flask(__name__)

    def get_qr_collection_records(collection_type):
        return qr_records_by_type.get(collection_type, [])

    app.get_qr_collection_records = get_qr_collection_records
    return app


def _identity_normalize(collection_type):
    return collection_type


def _empty_db():
    return {'specimens': []}


def _fake_render(monkeypatch):
    """Capture the template name + context instead of rendering real templates."""
    captured = {}

    def fake_render_template(template_name, **context):
        captured['template'] = template_name
        captured['context'] = context
        return 'RENDERED:' + template_name

    monkeypatch.setattr(collection_media_views, 'render_template', fake_render_template)
    return captured


def test_paleobotany_specimen_resolves_not_404(monkeypatch):
    """A registered QR collection outside the hard-coded chain must resolve."""
    captured = _fake_render(monkeypatch)
    specimen = {'catalog_number': 'PB-1', 'scientific_name': 'Ginkgo biloba'}
    app = _make_app({'paleobotany': [specimen]})

    with app.test_request_context('/qr_view/paleobotany/PB-1'):
        result = collection_media_views.render_qr_view_specimen(
            'paleobotany',
            'PB-1',
            normalize_qr_collection_type=_identity_normalize,
            get_meteorite_collection_database=_empty_db,
            botany_collection_database=_empty_db(),
            paleozoology_collection_database=_empty_db(),
        )

    status = result[1] if isinstance(result, tuple) else 200
    assert status != 404
    assert captured['template'] == 'specimen_qr_view.html'
    assert captured['context']['specimen'] is specimen
    assert captured['context']['displayed_fields'].get('scientific_name') == 'Ginkgo biloba'


def test_unknown_collection_still_404(monkeypatch):
    """A truly unknown collection with no records must still 404."""
    captured = _fake_render(monkeypatch)
    app = _make_app({})

    with app.test_request_context('/qr_view/paleobotany/PB-9'):
        result = collection_media_views.render_qr_view_specimen(
            'paleobotany',
            'PB-9',
            normalize_qr_collection_type=_identity_normalize,
            get_meteorite_collection_database=_empty_db,
            botany_collection_database=_empty_db(),
            paleozoology_collection_database=_empty_db(),
        )

    assert isinstance(result, tuple)
    assert result[1] == 404
    assert captured['template'] == 'error.html'


def test_meteorite_path_unchanged(monkeypatch):
    """The existing hard-coded meteorite path must keep working."""
    captured = _fake_render(monkeypatch)
    specimen = {'catalog_number': 'MET-1', 'meteorite_name': 'Soko Banja'}

    def meteorite_db():
        return {'specimens': [specimen]}

    app = _make_app({})

    with app.test_request_context('/qr_view/meteorite/MET-1'):
        result = collection_media_views.render_qr_view_specimen(
            'meteorite',
            'MET-1',
            normalize_qr_collection_type=_identity_normalize,
            get_meteorite_collection_database=meteorite_db,
            botany_collection_database=_empty_db(),
            paleozoology_collection_database=_empty_db(),
        )

    status = result[1] if isinstance(result, tuple) else 200
    assert status != 404
    assert captured['template'] == 'specimen_qr_view.html'
    assert captured['context']['specimen'] is specimen
