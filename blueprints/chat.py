"""Chat routes extracted from app.py."""

from flask import Blueprint, current_app, jsonify, render_template, request

import chat_views
from security_utils import login_required


chat_bp = Blueprint('chat', __name__)
CHAT_SERVICE_DISABLED_MESSAGE = 'Ћаскаоница је привремено искључена до наредне имплементације.'


@chat_bp.before_request
def ensure_chat_service_enabled():
    """Keep chat routes registered while the service is temporarily shut down."""
    if current_app.config.get('CHAT_SERVICE_ENABLED', False):
        return None

    if request.path.startswith('/api/chat/'):
        return jsonify({'success': False, 'message': CHAT_SERVICE_DISABLED_MESSAGE}), 503

    return (
        render_template(
            'error.html',
            error_code=503,
            error_message=CHAT_SERVICE_DISABLED_MESSAGE,
        ),
        503,
    )


@chat_bp.route('/chat')
@login_required
def chat_room_page():
    """Render the employee chat room."""
    return chat_views.render_chat_room_page()


@chat_bp.route('/api/chat/messages')
@login_required
def api_chat_messages():
    """Get chat messages. Pass ?since=epoch&channel=general for incremental polling."""
    return chat_views.api_chat_messages()


@chat_bp.route('/api/chat/send', methods=['POST'])
@login_required
def api_chat_send():
    """Send a chat message (text and/or file). Accepts JSON or multipart/form-data."""
    return chat_views.api_chat_send()


@chat_bp.route('/api/chat/status', methods=['POST'])
@login_required
def api_chat_status():
    """Set user's chat status (online/busy/offline)."""
    return chat_views.api_chat_status()


@chat_bp.route('/api/chat/file/<filename>')
@login_required
def api_chat_file(filename):
    """Serve a chat file attachment for download."""
    return chat_views.api_chat_file(filename)


@chat_bp.route('/api/chat/leave', methods=['POST'])
@login_required
def api_chat_leave():
    """Clear presence when user leaves chat page (sendBeacon, no CSRF)."""
    return chat_views.api_chat_leave()
