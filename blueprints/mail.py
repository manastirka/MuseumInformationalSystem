"""Mail client routes extracted from app.py."""

from functools import wraps

from flask import Blueprint, current_app, flash, jsonify, redirect, session, url_for

import mail_views
from security_utils import admin_required, login_required


mail_bp = Blueprint('mail', __name__)

MAILBOX_ADMIN_FORBIDDEN_MESSAGE = 'Поштанско сандуче није доступно администратору.'


def mailbox_access_required(api=False):
    """Block mailbox access for administrator accounts."""
    def decorator(view_func):
        @wraps(view_func)
        def wrapped(*args, **kwargs):
            if session.get('user_role') == 'admin':
                if api:
                    return jsonify({'success': False, 'message': MAILBOX_ADMIN_FORBIDDEN_MESSAGE}), 403
                flash(MAILBOX_ADMIN_FORBIDDEN_MESSAGE, 'warning')
                return redirect(url_for('dashboard'))
            return view_func(*args, **kwargs)

        return wrapped

    return decorator


@mail_bp.route('/mail')
@login_required
@mailbox_access_required()
def mail_client_page():
    """Render the three-pane email client."""
    return mail_views.render_mail_client_page()


@mail_bp.route('/mail/settings')
@admin_required
def mail_settings_page():
    """Backward-compatible redirect to centralized admin mail settings."""
    return redirect(url_for('admin_mail_configuration'))


@mail_bp.route('/api/mail/contacts')
@login_required
@mailbox_access_required(api=True)
def api_mail_contacts():
    """Return all museum employee emails as a contact list."""
    return mail_views.api_mail_contacts(
        get_employee_directory=current_app.get_employee_directory,
    )


@mail_bp.route('/api/mail/init')
@login_required
@mailbox_access_required(api=True)
def api_mail_init():
    """Combined init: return folders + first message page in one call."""
    return mail_views.api_mail_init()


@mail_bp.route('/api/mail/folders')
@login_required
@mailbox_access_required(api=True)
def api_mail_folders():
    """List IMAP folders with unread counts."""
    return mail_views.api_mail_folders()


@mail_bp.route('/api/mail/messages')
@login_required
@mailbox_access_required(api=True)
def api_mail_messages():
    """Paginated message list for a folder."""
    return mail_views.api_mail_messages()


@mail_bp.route('/api/mail/message/<uid>')
@login_required
@mailbox_access_required(api=True)
def api_mail_message(uid):
    """Fetch a single message by UID."""
    return mail_views.api_mail_message(uid)


@mail_bp.route('/api/mail/attachment/<uid>/<int:att_index>')
@login_required
@mailbox_access_required(api=True)
def api_mail_attachment(uid, att_index):
    """Download a message attachment by UID and attachment index."""
    return mail_views.api_mail_attachment(uid, att_index)


@mail_bp.route('/api/mail/attachments-all/<uid>')
@login_required
@mailbox_access_required(api=True)
def api_mail_attachments_all(uid):
    """Download all attachments as a ZIP file."""
    return mail_views.api_mail_attachments_all(uid)


@mail_bp.route('/api/mail/send', methods=['POST'])
@login_required
@mailbox_access_required(api=True)
def api_mail_send():
    """Send an email via SMTP, with optional file attachments."""
    return mail_views.api_mail_send()


@mail_bp.route('/api/mail/delete', methods=['POST'])
@login_required
@mailbox_access_required(api=True)
def api_mail_delete():
    """Delete a message."""
    return mail_views.api_mail_delete()


@mail_bp.route('/api/mail/read-state', methods=['POST'])
@login_required
@mailbox_access_required(api=True)
def api_mail_read_state():
    """Set read/unread state for a message."""
    return mail_views.api_mail_read_state()


@mail_bp.route('/api/mail/move', methods=['POST'])
@login_required
@mailbox_access_required(api=True)
def api_mail_move():
    """Move a message between folders."""
    return mail_views.api_mail_move()


@mail_bp.route('/api/mail/check')
@login_required
@mailbox_access_required(api=True)
def api_mail_check():
    """Return unread count for navbar badge."""
    return mail_views.api_mail_check()


@mail_bp.route('/api/mail/sync', methods=['POST'])
@login_required
@mailbox_access_required(api=True)
def api_mail_sync():
    """Trigger an immediate IMAP sync."""
    return mail_views.api_mail_sync()


@mail_bp.route('/api/mail/settings', methods=['GET'])
@admin_required
def api_mail_settings_get():
    """Return mail settings for the current user."""
    return mail_views.api_mail_settings_get()


@mail_bp.route('/api/mail/settings', methods=['POST'])
@admin_required
def api_mail_settings_save():
    """Save mail settings for the current user."""
    return mail_views.api_mail_settings_save()


@mail_bp.route('/api/mail/test-connection', methods=['POST'])
@admin_required
def api_mail_test_connection():
    """Test IMAP or SMTP connection."""
    return mail_views.api_mail_test_connection()
