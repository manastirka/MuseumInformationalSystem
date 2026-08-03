"""Route implementations for the phase-3 custom theme creator.

All routes are login-scoped and operate ONLY on the current user's themes
(postgres_auth scopes every query by user_email). Import/paste is validated
through custom_theme.validate_definition before it ever touches the database.
The blueprint wiring lives in blueprints/core.py; this module holds the logic so
it can be unit-tested without the full app.
"""

import json

from flask import Response, jsonify, request, session

import custom_theme
import core_app_views


def _auth():
    from postgres_auth import get_postgres_auth
    return get_postgres_auth()


def _email():
    return session.get('user_email')


def _cookie_kwargs():
    return dict(max_age=31536000, samesite='Lax', path='/',
                secure=request.is_secure, httponly=False)


def _theme_payload(row):
    """Shape a DB row for the JSON API (id, name, definition)."""
    return {
        'id': row['id'],
        'name': row['name'],
        'definition': row['definition'],
    }


def list_custom_themes():
    email = _email()
    if not email:
        return jsonify({'status': 'error', 'message': 'Пријава је обавезна.'}), 401
    themes = _auth().list_custom_themes(email)
    return jsonify({
        'status': 'ok',
        'themes': [_theme_payload(t) for t in themes],
        'active_id': core_app_views.current_custom_theme_id(),
    })


def create_custom_theme():
    email = _email()
    if not email:
        return jsonify({'status': 'error', 'message': 'Пријава је обавезна.'}), 401

    data = request.get_json(silent=True) or {}
    name = custom_theme.normalize_name(data.get('name'))
    if not name:
        return jsonify({'status': 'error', 'message': 'Унесите назив теме.'}), 400
    cleaned, err = custom_theme.validate_definition(data.get('definition'))
    if err:
        return jsonify({'status': 'error', 'message': err}), 400

    new_id = _auth().create_custom_theme(email, name, cleaned)
    if not new_id:
        return jsonify({'status': 'error', 'message': 'Чување није успело.'}), 500
    return jsonify({'status': 'ok', 'id': new_id, 'name': name, 'definition': cleaned})


def update_custom_theme(theme_id):
    email = _email()
    if not email:
        return jsonify({'status': 'error', 'message': 'Пријава је обавезна.'}), 401

    existing = _auth().get_custom_theme(email, theme_id)
    if not existing:
        return jsonify({'status': 'error', 'message': 'Тема није пронађена.'}), 404

    data = request.get_json(silent=True) or {}
    # Name: keep existing when omitted.
    if 'name' in data:
        name = custom_theme.normalize_name(data.get('name'))
        if not name:
            return jsonify({'status': 'error', 'message': 'Унесите назив теме.'}), 400
    else:
        name = existing['name']

    # Definition: keep existing when omitted (rename-only update).
    if 'definition' in data:
        cleaned, err = custom_theme.validate_definition(data.get('definition'))
        if err:
            return jsonify({'status': 'error', 'message': err}), 400
    else:
        cleaned, err = custom_theme.validate_definition(existing['definition'])
        if err:
            return jsonify({'status': 'error', 'message': 'Постојећа дефиниција је неисправна.'}), 400

    if not _auth().update_custom_theme(email, theme_id, name, cleaned):
        return jsonify({'status': 'error', 'message': 'Измена није успела.'}), 500

    # If this is the applied theme, drop the cache so the next render reflects it.
    if core_app_views.current_custom_theme_id() == theme_id:
        core_app_views.invalidate_custom_theme_cache()
    return jsonify({'status': 'ok', 'id': theme_id, 'name': name, 'definition': cleaned})


def duplicate_custom_theme(theme_id):
    email = _email()
    if not email:
        return jsonify({'status': 'error', 'message': 'Пријава је обавезна.'}), 401

    existing = _auth().get_custom_theme(email, theme_id)
    if not existing:
        return jsonify({'status': 'error', 'message': 'Тема није пронађена.'}), 404
    cleaned, err = custom_theme.validate_definition(existing['definition'])
    if err:
        return jsonify({'status': 'error', 'message': 'Постојећа дефиниција је неисправна.'}), 400

    new_name = custom_theme.normalize_name('{} (копија)'.format(existing['name']))
    new_id = _auth().create_custom_theme(email, new_name, cleaned)
    if not new_id:
        return jsonify({'status': 'error', 'message': 'Дуплирање није успело.'}), 500
    return jsonify({'status': 'ok', 'id': new_id, 'name': new_name, 'definition': cleaned})


def delete_custom_theme(theme_id):
    email = _email()
    if not email:
        return jsonify({'status': 'error', 'message': 'Пријава је обавезна.'}), 401

    was_active = core_app_views.current_custom_theme_id() == theme_id
    if not _auth().delete_custom_theme(email, theme_id):
        return jsonify({'status': 'error', 'message': 'Тема није пронађена.'}), 404

    response = jsonify({'status': 'ok'})
    if was_active:
        # The user was rendering this theme — fall back to the default palette
        # in the session and cookies too (the DB was already reset).
        session['museum_palette'] = core_app_views.DEFAULT_PALETTE
        session['museum_custom_id'] = None
        core_app_views.invalidate_custom_theme_cache()
        response.set_cookie('museum_palette', core_app_views.DEFAULT_PALETTE, **_cookie_kwargs())
        response.set_cookie('museum_custom_id', '', **_cookie_kwargs())
    return response


def apply_custom_theme(theme_id):
    email = _email()
    if not email:
        return jsonify({'status': 'error', 'message': 'Пријава је обавезна.'}), 401

    row = _auth().get_custom_theme(email, theme_id)
    if not row:
        return jsonify({'status': 'error', 'message': 'Тема није пронађена.'}), 404
    cleaned, err = custom_theme.validate_definition(row['definition'])
    if err:
        return jsonify({'status': 'error', 'message': 'Дефиниција теме је неисправна.'}), 400

    session['museum_palette'] = 'custom'
    session['museum_custom_id'] = theme_id
    core_app_views.invalidate_custom_theme_cache()
    _auth().set_active_custom_theme(email, theme_id)

    response = jsonify({
        'status': 'ok',
        'id': theme_id,
        'pal_css': custom_theme.pal_css(cleaned),
        'bs_theme': custom_theme.bs_theme(cleaned),
    })
    kwargs = _cookie_kwargs()
    response.set_cookie('museum_palette', 'custom', **kwargs)
    response.set_cookie('museum_custom_id', str(theme_id), **kwargs)
    return response


def export_custom_theme(theme_id):
    email = _email()
    if not email:
        return jsonify({'status': 'error', 'message': 'Пријава је обавезна.'}), 401

    row = _auth().get_custom_theme(email, theme_id)
    if not row:
        return jsonify({'status': 'error', 'message': 'Тема није пронађена.'}), 404
    cleaned, err = custom_theme.validate_definition(row['definition'])
    if err:
        return jsonify({'status': 'error', 'message': 'Дефиниција теме је неисправна.'}), 400

    bundle = {
        'mis_custom_theme': 1,
        'name': row['name'],
        'definition': cleaned,
    }
    payload = json.dumps(bundle, ensure_ascii=False, indent=2)
    # The HTTP filename must be latin-1 safe: Cyrillic names (isalnum() is True
    # for them) would raise when Werkzeug encodes the header. Keep an ASCII
    # slug for the plain filename and carry the real (UTF-8) name via filename*.
    ascii_slug = ''.join(
        ch if (ch.isascii() and (ch.isalnum() or ch in '-_')) else '_'
        for ch in row['name'].replace(' ', '_')
    ).strip('_') or 'tema'
    from urllib.parse import quote
    resp = Response(payload, mimetype='application/json; charset=utf-8')
    resp.headers['Content-Disposition'] = (
        "attachment; filename=\"mis-tema-{}.json\"; filename*=UTF-8''{}".format(
            ascii_slug, quote('mis-tema-{}.json'.format(row['name']))
        )
    )
    return resp


def import_custom_theme():
    """Accept a pasted/uploaded theme bundle. NEVER trusts the payload: the
    definition is fully re-validated and rebuilt before any DB write."""
    email = _email()
    if not email:
        return jsonify({'status': 'error', 'message': 'Пријава је обавезна.'}), 401

    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify({'status': 'error', 'message': 'Датотека није исправан JSON.'}), 400

    # Accept either a full export bundle ({name, definition}) or a bare
    # definition. A supplied name is normalised; missing name gets a default.
    definition_raw = data.get('definition', data)
    cleaned, err = custom_theme.validate_definition(definition_raw)
    if err:
        return jsonify({'status': 'error', 'message': 'Неисправна тема: {}'.format(err)}), 400

    name = custom_theme.normalize_name(data.get('name')) or 'Увезена тема'
    new_id = _auth().create_custom_theme(email, name, cleaned)
    if not new_id:
        return jsonify({'status': 'error', 'message': 'Увоз није успео.'}), 500
    return jsonify({'status': 'ok', 'id': new_id, 'name': name, 'definition': cleaned})
