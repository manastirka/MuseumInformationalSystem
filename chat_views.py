"""Shared route implementations for the chat room."""

import re
import uuid

from flask import jsonify, render_template, request, send_file, session
from werkzeug.utils import secure_filename


def render_chat_room_page():
    """Render the employee chat room."""
    return render_template('admin_chat_room.html')


def api_chat_messages():
    """Get chat messages for the selected channel."""
    from chat_room import (
        get_messages,
        get_online_users,
        get_user_channels,
        mark_channel_read,
        touch_presence,
    )

    since = float(request.args.get('since', 0))
    channel = request.args.get('channel', 'general')
    user_id = session['user_id']

    if channel.startswith('dm:'):
        parts = channel.split(':')
        if len(parts) != 3 or user_id not in (int(parts[1]), int(parts[2])):
            return jsonify({'success': False, 'message': 'Немате приступ овом каналу.'}), 403

    touch_presence(
        user_id,
        session['user_name'],
        session['user_email'],
        session.get('user_department', ''),
    )
    messages = get_messages(since_epoch=since, limit=100, channel=channel)
    online = get_online_users()
    channels = get_user_channels(user_id)
    mark_channel_read(user_id, channel)

    return jsonify(
        {
            'success': True,
            'messages': messages,
            'online': online,
            'channels': channels,
        }
    )


def api_chat_send():
    """Send a chat message with optional attachment."""
    from chat_room import CHAT_FILES_DIR, send_message, touch_presence

    user_id = session['user_id']
    user_name = session['user_name']
    user_email = session['user_email']
    user_department = session.get('user_department', '')

    touch_presence(user_id, user_name, user_email, user_department)

    if request.content_type and 'multipart/form-data' in request.content_type:
        text = (request.form.get('message') or '').strip()
        channel = request.form.get('channel', 'general')
        uploaded = request.files.get('file')
    else:
        data = request.get_json(force=True)
        text = (data.get('message') or '').strip()
        channel = data.get('channel', 'general')
        uploaded = None

    if channel.startswith('dm:'):
        parts = channel.split(':')
        if len(parts) != 3 or user_id not in (int(parts[1]), int(parts[2])):
            return jsonify({'success': False, 'message': 'Немате приступ овом каналу.'}), 403

    file_name = None
    file_path = None
    file_size = None
    file_type = None

    if uploaded and uploaded.filename:
        allowed_extensions = {
            '.jpg',
            '.jpeg',
            '.png',
            '.gif',
            '.pdf',
            '.xlsx',
            '.xls',
            '.csv',
            '.doc',
            '.docx',
        }
        original_name = secure_filename(uploaded.filename) or 'file'
        ext = ''
        if '.' in original_name:
            ext = '.' + original_name.rsplit('.', 1)[1].lower()
        if ext not in allowed_extensions:
            return jsonify({'success': False, 'message': 'Недозвољен тип фајла.'}), 400

        stored_name = uuid.uuid4().hex + ext
        CHAT_FILES_DIR.mkdir(parents=True, exist_ok=True)
        save_path = CHAT_FILES_DIR / stored_name
        uploaded.save(str(save_path))

        actual_size = save_path.stat().st_size
        if actual_size > 10 * 1024 * 1024:
            save_path.unlink(missing_ok=True)
            return jsonify({'success': False, 'message': 'Фајл је превелик (макс. 10MB).'}), 400

        file_name = uploaded.filename
        file_path = stored_name
        file_size = actual_size
        file_type = uploaded.content_type or 'application/octet-stream'

    if not text and not file_name:
        return jsonify({'success': False, 'message': 'Порука не може бити празна.'}), 400
    if text and len(text) > 2000:
        return jsonify({'success': False, 'message': 'Порука је предугачка (макс. 2000 карактера).'}), 400

    msg = send_message(
        user_id=user_id,
        user_name=user_name,
        user_email=user_email,
        department=user_department,
        message=text,
        channel=channel,
        file_name=file_name,
        file_path=file_path,
        file_size=file_size,
        file_type=file_type,
    )
    return jsonify({'success': True, 'msg': msg})


def api_chat_status():
    """Set the current user's chat status."""
    from chat_room import VALID_STATUSES, set_user_status, touch_presence

    data = request.get_json(force=True)
    status = data.get('status', '')
    if status not in VALID_STATUSES:
        return jsonify({'success': False, 'message': 'Невалидан статус.'}), 400

    user_id = session['user_id']
    touch_presence(
        user_id,
        session['user_name'],
        session['user_email'],
        session.get('user_department', ''),
        status=status,
    )
    set_user_status(user_id, status)
    return jsonify({'success': True, 'status': status})


def api_chat_file(filename):
    """Serve a chat attachment."""
    from chat_room import CHAT_FILES_DIR

    if not re.match(r'^[a-f0-9]{32}\.\w{1,5}$', filename):
        return jsonify({'success': False, 'message': 'Невалидан фајл.'}), 404

    file_path = CHAT_FILES_DIR / filename
    if not file_path.is_file():
        return jsonify({'success': False, 'message': 'Фајл није пронађен.'}), 404

    return send_file(str(file_path), as_attachment=True)


def api_chat_leave():
    """Clear presence when the user leaves chat."""
    from chat_room import clear_presence

    clear_presence(session['user_id'])
    return jsonify({'success': True})
