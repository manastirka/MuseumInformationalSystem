"""Reproducing test: stale vehicle reservation list on back/forward navigation.

Bug report (2026-07-07): open the reservation list, navigate away (e.g. to
the geological map), navigate back — recently added reservations are missing
until a manual refresh. The list is embedded server-side into the page
(`{{ reservations | tojson }}` in vehicle_reservations.html), so a page
served from the browser bfcache/HTTP cache shows a stale snapshot.

The dashboard already solves this (core_app_views.render_dashboard sends
'Cache-Control: no-cache, no-store, must-revalidate' + Pragma + Expires;
'no-store' also keeps the page out of the bfcache in Chrome/Firefox).
render_vehicle_reservations must do the same.
"""

import os
from unittest import mock

os.environ.setdefault('FLASK_ENV', 'testing')
os.environ.setdefault('SECRET_KEY', 'test-secret')

import flask
import pytest

import vehicle_depot_views


@pytest.fixture
def app():
    application = flask.Flask(__name__)
    application.secret_key = 'test-secret'
    return application


def test_vehicle_reservations_response_disables_browser_caching(app):
    with app.test_request_context('/vehicle_reservations'):
        with mock.patch.object(vehicle_depot_views, 'render_template', return_value=''):
            result = vehicle_depot_views.render_vehicle_reservations(
                get_museum_vehicles=lambda *a, **k: [],
                get_vehicle_reservations=lambda *a, **k: [],
            )
        response = app.make_response(result)

    assert response.headers.get('Cache-Control') == 'no-cache, no-store, must-revalidate'
    assert response.headers.get('Pragma') == 'no-cache'
    assert response.headers.get('Expires') == '0'
