import os

os.environ.setdefault('FLASK_ENV', 'testing')
os.environ.setdefault('SECRET_KEY', 'test-secret')
os.environ.setdefault('REDIS_URL', '')
os.environ.setdefault('SESSION_TYPE', 'filesystem')
os.environ.setdefault('SESSION_FILE_DIR', '/tmp/museum-test-b-mail-client')

import email
from unittest import mock

import mail_client


def _make_client():
    """Build a MailClient without running __init__ (which needs DB + crypto)."""
    client = mail_client.MailClient.__new__(mail_client.MailClient)
    client.user_email = 'staff@nhmbeo.rs'
    client.settings = {
        'email_address': 'staff@nhmbeo.rs',
        'imap_server': 'mail.nhmbeo.rs',
        'imap_port': 993,
        'imap_ssl': True,
        'smtp_server': 'mail.nhmbeo.rs',
        'smtp_port': 587,
        'smtp_starttls': True,
    }
    client._password = 'secret'
    client.db = None
    return client


def _html_part_text(msg_string):
    """Return the decoded text of the text/html MIME part."""
    msg = email.message_from_string(msg_string)
    for part in msg.walk():
        if part.get_content_type() == 'text/html':
            payload = part.get_payload(decode=True)
            charset = part.get_content_charset() or 'utf-8'
            return payload.decode(charset, errors='replace')
    raise AssertionError('no text/html part found')


def _send_and_capture(body, attachments=None):
    client = _make_client()
    captured = {}
    fake_smtp = mock.MagicMock()
    fake_smtp.sendmail.side_effect = lambda f, r, m: captured.__setitem__('msg_string', m)

    with mock.patch.object(mail_client.smtplib, 'SMTP', return_value=fake_smtp), \
         mock.patch.object(mail_client, 'validate_mail_server_settings',
                           side_effect=lambda s: dict(s)), \
         mock.patch.object(mail_client.MailClient, '_imap',
                           side_effect=Exception('skip sent-folder append')):
        result = client.send_message('rcpt@example.com', 'Subj', body,
                                      attachments=attachments)

    assert result is True
    return captured['msg_string']


# ===================== Finding 1: HTML injection in send_message =====================

def test_send_message_escapes_html_metacharacters_no_attachment():
    body = 'Hello </pre><script>alert(1)</script><pre>world'
    html_text = _html_part_text(_send_and_capture(body))

    # The dangerous raw markup must NOT survive into the HTML part.
    assert '<script>alert(1)</script>' not in html_text
    assert '</pre><script>' not in html_text
    # Escaped form should be present instead.
    assert '&lt;script&gt;' in html_text


def test_send_message_escapes_html_metacharacters_with_attachment():
    body = 'Break</pre><b>out</b>'
    attachments = [{
        'filename': 'note.txt',
        'content_type': 'text/plain',
        'data': b'hi',
    }]
    html_text = _html_part_text(_send_and_capture(body, attachments=attachments))

    assert '</pre><b>out</b>' not in html_text
    assert '&lt;b&gt;out&lt;/b&gt;' in html_text


# ===================== Finding 2: IMAP leak in delete_message_async =====================

def test_delete_message_async_logs_out_on_store_failure():
    client = _make_client()

    conn = mock.MagicMock()
    conn.uid.side_effect = Exception('STORE rejected')

    captured = {}

    def _capture_thread(target=None, daemon=None, name=None, args=(), kwargs=None):
        captured['target'] = target
        return mock.MagicMock()

    with mock.patch.object(mail_client, '_remove_cached_message'), \
         mock.patch.object(mail_client, '_connect_imap', return_value=conn), \
         mock.patch.object(mail_client.threading, 'Thread', side_effect=_capture_thread):
        client.delete_message_async(123, 'INBOX')
        # Run the captured background body while the patches are still active.
        captured['target']()

    # Connection must be cleaned up even though uid('store') raised.
    assert conn.logout.called


# ===================== Finding 3: IMAP leak in trigger_sync =====================

def test_trigger_sync_logs_out_when_prefetch_raises():
    client = _make_client()

    conn = mock.MagicMock()
    fake_db = mock.MagicMock()

    captured = {}

    def _capture_thread(target=None, daemon=None, name=None, args=(), kwargs=None):
        captured['target'] = target
        return mock.MagicMock()

    with mock.patch.object(mail_client, '_connect_imap', return_value=conn), \
         mock.patch.object(mail_client, '_get_db', return_value=fake_db), \
         mock.patch.object(mail_client, 'do_sync', return_value=True), \
         mock.patch.object(mail_client, '_prefetch_bodies',
                           side_effect=Exception('DB error in prefetch query')), \
         mock.patch.object(mail_client, '_flush_pending_reads'), \
         mock.patch.object(mail_client.threading, 'Thread', side_effect=_capture_thread):
        client.trigger_sync('INBOX')
        # Run the captured background body while the patches are still active;
        # the closure's `thread` is already bound to the returned mock by now.
        captured['target']()

    # IMAP connection opened in _do must be logged out despite the raise.
    assert conn.logout.called
