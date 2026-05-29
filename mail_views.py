"""Shared route implementations for the mail client."""

import io
import logging
import zipfile
from urllib.parse import quote

from flask import Response, jsonify, render_template, request, session

import admin_system_views
from observability import add_sentry_breadcrumb, capture_observability_exception

logger = logging.getLogger(__name__)


def _server_error_response(message):
    return jsonify({'success': False, 'message': message}), 500


def render_mail_client_page():
    """Render the three-pane email client."""
    return render_template('admin_mail_client.html')


def render_mail_settings_page():
    """Render the email settings page."""
    return render_template('admin_mail_settings.html')


def api_mail_contacts(*, get_employee_directory):
    """Return all museum employee emails as a contact list."""
    try:
        employees = get_employee_directory()
        contacts = []
        for emp in (employees or []):
            email = emp.get('email', '').strip()
            if not email:
                continue
            contacts.append(
                {
                    'name': emp.get('full_name', ''),
                    'email': email,
                    'department': emp.get('department', ''),
                    'position': emp.get('position', ''),
                }
            )
        contacts.sort(key=lambda contact: contact['name'])
        return jsonify({'success': True, 'contacts': contacts})
    except Exception as exc:
        logger.error("Mail contacts error: %s", exc)
        return jsonify({'success': True, 'contacts': []})


def api_mail_init():
    """Return folders and first message page in one call."""
    folder = request.args.get('folder', 'INBOX')
    try:
        page = int(request.args.get('page', 1))
    except (TypeError, ValueError):
        page = 1
    search = request.args.get('search', '').strip() or None
    sort_by = request.args.get('sort', 'date')
    sort_dir = request.args.get('dir', 'desc')
    try:
        add_sentry_breadcrumb(
            category='mail',
            message='Mail init requested',
            data={'folder': folder, 'page': page, 'search': bool(search)},
        )
        from mail_client import MailClient

        mc = MailClient(session['user_email'])
        try:
            data = mc.get_init_data(
                folder=folder,
                page=page,
                search=search,
                sort_by=sort_by,
                sort_dir=sort_dir,
            )
            return jsonify({'success': True, **data})
        finally:
            mc.close()
    except ValueError as exc:
        return jsonify({'success': False, 'message': str(exc)}), 400
    except Exception as exc:
        logger.error("Mail init error: %s", exc)
        capture_observability_exception(
            exc,
            tags={'component': 'mail', 'operation': 'init'},
            extra={'folder': folder, 'page': page, 'search': bool(search)},
            user={'email': session.get('user_email')},
        )
        return jsonify({'success': False, 'message': 'Грешка при повезивању на сервер поште.'}), 500


def api_mail_folders():
    """List IMAP folders with unread counts."""
    try:
        add_sentry_breadcrumb(
            category='mail',
            message='Mail folders requested',
        )
        from mail_client import MailClient

        mc = MailClient(session['user_email'])
        try:
            folders = mc.list_folders()
            return jsonify({'success': True, 'folders': folders})
        finally:
            mc.close()
    except ValueError as exc:
        return jsonify({'success': False, 'message': str(exc)}), 400
    except Exception as exc:
        logger.error("Mail folders error: %s", exc)
        return jsonify({'success': False, 'message': 'Грешка при повезивању на сервер поште.'}), 500


def api_mail_messages():
    """Return paginated messages for a folder."""
    folder = request.args.get('folder', 'INBOX')
    try:
        page = int(request.args.get('page', 1))
    except (TypeError, ValueError):
        page = 1
    search = request.args.get('search', '').strip() or None
    sort_by = request.args.get('sort', 'date')
    sort_dir = request.args.get('dir', 'desc')
    try:
        from mail_client import MailClient

        mc = MailClient(session['user_email'])
        try:
            result = mc.list_messages(
                folder=folder,
                page=page,
                search=search,
                sort_by=sort_by,
                sort_dir=sort_dir,
            )
            return jsonify({'success': True, **result})
        finally:
            mc.close()
    except ValueError as exc:
        return jsonify({'success': False, 'message': str(exc)}), 400
    except Exception as exc:
        logger.error("Mail messages error: %s", exc)
        return jsonify({'success': False, 'message': 'Грешка при учитавању порука.'}), 500


def api_mail_message(uid):
    """Fetch a single message by UID."""
    folder = request.args.get('folder', 'INBOX')
    try:
        from mail_client import MailClient

        mc = MailClient(session['user_email'])
        try:
            msg = mc.get_message(uid, folder=folder)
            if msg is None:
                return jsonify({'success': False, 'message': 'Порука није пронађена.'}), 404
            return jsonify({'success': True, 'message': msg})
        finally:
            mc.close()
    except ValueError as exc:
        return jsonify({'success': False, 'message': str(exc)}), 400
    except Exception as exc:
        logger.error("Mail message error: %s", exc)
        return jsonify({'success': False, 'message': 'Грешка при учитавању поруке.'}), 500


def api_mail_attachment(uid, att_index):
    """Download a single attachment."""
    folder = request.args.get('folder', 'INBOX')
    try:
        from mail_client import MailClient

        mc = MailClient(session['user_email'])
        try:
            result = mc.get_attachment(uid, att_index, folder=folder)
            if result is None:
                return jsonify({'success': False, 'message': 'Прилог није пронађен.'}), 404
            filename, content_type, data = result
            response = Response(data, mimetype=content_type)
            safe_filename = filename.encode('ascii', errors='replace').decode()
            response.headers['Content-Disposition'] = (
                f'attachment; filename="{safe_filename}"; '
                f"filename*=UTF-8''{quote(filename)}"
            )
            response.headers['Content-Length'] = len(data)
            return response
        finally:
            mc.close()
    except ValueError as exc:
        return jsonify({'success': False, 'message': str(exc)}), 400
    except Exception as exc:
        logger.error("Mail attachment error: %s", exc)
        return jsonify({'success': False, 'message': 'Грешка при преузимању прилога.'}), 500


def api_mail_attachments_all(uid):
    """Download all attachments as a ZIP file."""
    folder = request.args.get('folder', 'INBOX')
    try:
        from mail_client import MailClient

        mc = MailClient(session['user_email'])
        try:
            files = mc.get_all_attachments(uid, folder=folder)
            if not files:
                return jsonify({'success': False, 'message': 'Нема прилога.'}), 404

            buffer = io.BytesIO()
            with zipfile.ZipFile(buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
                seen = {}
                for filename, data in files:
                    if filename in seen:
                        seen[filename] += 1
                        name, ext = (filename.rsplit('.', 1) + [''])[:2]
                        filename = f"{name}_{seen[filename]}.{ext}" if ext else f"{name}_{seen[filename]}"
                    else:
                        seen[filename] = 0
                    zip_file.writestr(filename, data)

            zip_data = buffer.getvalue()
            response = Response(zip_data, mimetype='application/zip')
            response.headers['Content-Disposition'] = 'attachment; filename="attachments.zip"'
            response.headers['Content-Length'] = len(zip_data)
            return response
        finally:
            mc.close()
    except ValueError as exc:
        return jsonify({'success': False, 'message': str(exc)}), 400
    except Exception as exc:
        logger.error("Mail attachments-all error: %s", exc)
        return jsonify({'success': False, 'message': 'Грешка при преузимању прилога.'}), 500


def api_mail_send():
    """Send an email via SMTP, with optional attachments."""
    if request.content_type and 'multipart' in request.content_type:
        to = request.form.get('to', '').strip()
        subject = request.form.get('subject', '').strip()
        body = request.form.get('body', '')
        cc = request.form.get('cc', '').strip()
        files = request.files.getlist('attachments')
    else:
        data = request.get_json(force=True)
        to = data.get('to', '').strip()
        subject = data.get('subject', '').strip()
        body = data.get('body', '')
        cc = data.get('cc', '').strip()
        files = []

    if not to:
        return jsonify({'success': False, 'message': 'Примаоц је обавезан.'}), 400

    attachments = []
    total_size = 0
    for uploaded in files:
        if uploaded and uploaded.filename:
            file_data = uploaded.read()
            total_size += len(file_data)
            if total_size > 25 * 1024 * 1024:
                return jsonify(
                    {
                        'success': False,
                        'message': 'Прилози су превелики (макс. 25MB укупно).',
                    }
                ), 400
            attachments.append(
                {
                    'filename': uploaded.filename,
                    'content_type': uploaded.content_type or 'application/octet-stream',
                    'data': file_data,
                }
            )

    try:
        from mail_client import MailClient

        mc = MailClient(session['user_email'])
        try:
            mc.send_message(
                to=to,
                subject=subject,
                body=body,
                cc=cc,
                attachments=attachments if attachments else None,
            )
            return jsonify({'success': True, 'message': 'Порука је послата.'})
        finally:
            mc.close()
    except ValueError as exc:
        return jsonify({'success': False, 'message': str(exc)}), 400
    except Exception as exc:
        logger.error("Mail send error: %s", exc)
        capture_observability_exception(
            exc,
            tags={'component': 'mail', 'operation': 'send'},
            extra={'to': to, 'cc': cc, 'attachment_count': len(attachments)},
            user={'email': session.get('user_email')},
        )
        return _server_error_response('Грешка при слању поруке.')


def api_mail_delete():
    """Delete a message — removes from cache immediately, IMAP delete in background."""
    data = request.get_json(force=True)
    uid = data.get('uid')
    folder = data.get('folder', 'INBOX')
    if not uid:
        return jsonify({'success': False, 'message': 'UID поруке је обавезан.'}), 400

    try:
        from mail_client import MailClient

        user_email = session['user_email']
        mc = MailClient(user_email)
        try:
            mc.delete_message_async(str(uid), folder=folder)
            return jsonify({'success': True, 'message': 'Порука је обрисана.'})
        finally:
            mc.close()
    except Exception as exc:
        logger.error("Mail delete error: %s", exc)
        return _server_error_response('Грешка при брисању поруке.')


def api_mail_read_state():
    """Set the read state for a message."""
    data = request.get_json(force=True)
    uid = data.get('uid')
    folder = data.get('folder', 'INBOX')
    is_read = bool(data.get('is_read', True))
    if not uid:
        return jsonify({'success': False, 'message': 'UID поруке је обавезан.'}), 400

    try:
        from mail_client import MailClient

        mc = MailClient(session['user_email'])
        try:
            mc.set_message_read_state(str(uid), folder=folder, is_read=is_read)
            return jsonify(
                {
                    'success': True,
                    'message': (
                        'Порука је означена као прочитана.'
                        if is_read
                        else 'Порука је означена као непрочитана.'
                    ),
                }
            )
        finally:
            mc.close()
    except Exception as exc:
        logger.error("Mail read-state error: %s", exc)
        return _server_error_response('Грешка при промени статуса поруке.')


def api_mail_move():
    """Move a message between folders."""
    data = request.get_json(force=True)
    uid = data.get('uid')
    src = data.get('src_folder', 'INBOX')
    dst = data.get('dst_folder')
    if not uid or not dst:
        return jsonify({'success': False, 'message': 'UID и одредишни фолдер су обавезни.'}), 400

    try:
        from mail_client import MailClient

        mc = MailClient(session['user_email'])
        try:
            mc.move_message(str(uid), src, dst)
            return jsonify({'success': True, 'message': 'Порука је премештена.'})
        finally:
            mc.close()
    except Exception as exc:
        logger.error("Mail move error: %s", exc)
        return _server_error_response('Грешка при премештању поруке.')


def api_mail_check():
    """Return unread count for the navbar badge."""
    try:
        from mail_client import MailClient

        mc = MailClient(session['user_email'])
        try:
            count = mc.unread_count()
            return jsonify({'success': True, 'unread': count})
        finally:
            mc.close()
    except Exception:
        return jsonify({'success': True, 'unread': 0})


def api_mail_sync():
    """Trigger an immediate IMAP sync."""
    folder = request.get_json(force=True).get('folder', 'INBOX') if request.is_json else 'INBOX'
    try:
        from mail_client import MailClient

        mc = MailClient(session['user_email'])
        try:
            mc.trigger_sync(folder)
            return jsonify({'success': True, 'message': 'Синхронизовано.'})
        finally:
            mc.close()
    except ValueError as exc:
        return jsonify({'success': False, 'message': str(exc)}), 400
    except Exception as exc:
        logger.error("Mail sync error: %s", exc)
        return _server_error_response('Грешка при синхронизацији поште.')


def api_mail_settings_get():
    """Return mail settings for the current user."""
    from mail_client import MAIL_ALLOWED_HOSTS_KEY, get_allowed_mail_hosts, get_user_settings_safe

    settings = get_user_settings_safe(session['user_email'])
    saved_settings = admin_system_views.load_saved_settings() or {}
    return jsonify(
        {
            'success': True,
            'settings': settings,
            'allowed_hosts': saved_settings.get(MAIL_ALLOWED_HOSTS_KEY, get_allowed_mail_hosts()),
        }
    )


def api_mail_settings_save():
    """Save mail settings for the current user."""
    data = request.get_json(force=True)
    from mail_client import (
        MAIL_ALLOWED_HOSTS_KEY,
        _encrypt,
        get_user_settings,
        get_allowed_mail_hosts,
        normalize_allowed_mail_hosts,
        save_user_settings,
        validate_mail_server_settings,
    )

    user_email = session['user_email']
    existing = get_user_settings(user_email) or {}
    saved_settings = admin_system_views.load_saved_settings() or {}
    raw_allowed_hosts = (
        data.get('allowed_hosts')
        if 'allowed_hosts' in data
        else saved_settings.get(MAIL_ALLOWED_HOSTS_KEY, get_allowed_mail_hosts())
    )
    allowed_hosts = normalize_allowed_mail_hosts(raw_allowed_hosts)

    try:
        settings = {
            'imap_server': data.get('imap_server', '').strip(),
            'imap_port': int(data.get('imap_port', 993)),
            'imap_ssl': bool(data.get('imap_ssl', True)),
            'smtp_server': data.get('smtp_server', '').strip(),
            'smtp_port': int(data.get('smtp_port', 587)),
            'smtp_starttls': bool(data.get('smtp_starttls', True)),
            'email_address': data.get('email_address', '').strip(),
        }
    except (TypeError, ValueError):
        return jsonify({'success': False, 'message': 'Порт мора бити број.'}), 400

    password = data.get('password', '').strip()
    if password:
        settings['password'] = _encrypt(password)
    elif 'password' in existing:
        settings['password'] = existing['password']
    else:
        return jsonify({'success': False, 'message': 'Лозинка је обавезна.'}), 400

    try:
        settings = validate_mail_server_settings(settings, allowed_hosts=allowed_hosts)
    except ValueError as exc:
        return jsonify({'success': False, 'message': str(exc)}), 400

    saved_settings[MAIL_ALLOWED_HOSTS_KEY] = allowed_hosts
    if not admin_system_views.save_settings(saved_settings):
        return jsonify({'success': False, 'message': 'Није могуће сачувати листу дозвољених host-ова.'}), 500

    save_user_settings(user_email, settings)
    return jsonify({'success': True, 'message': 'Подешавања су сачувана.'})


def api_mail_test_connection():
    """Test IMAP or SMTP connectivity."""
    try:
        data = request.get_json(force=True)
        conn_type = data.get('type', 'imap')
        email_address = data.get('email_address', '').strip()
        password = data.get('password', '').strip()
        from mail_client import MAIL_ALLOWED_HOSTS_KEY, get_allowed_mail_hosts, normalize_allowed_mail_hosts

        if not password:
            from mail_client import _decrypt, get_user_settings

            existing = get_user_settings(session['user_email'])
            if existing and 'password' in existing:
                try:
                    password = _decrypt(existing['password'])
                except Exception:
                    return jsonify({'success': False, 'message': 'Лозинка је потребна за тест.'}), 400
            else:
                return jsonify({'success': False, 'message': 'Лозинка је потребна за тест.'}), 400

        saved_settings = admin_system_views.load_saved_settings() or {}
        raw_allowed_hosts = (
            data.get('allowed_hosts')
            if 'allowed_hosts' in data
            else saved_settings.get(MAIL_ALLOWED_HOSTS_KEY, get_allowed_mail_hosts())
        )
        allowed_hosts = normalize_allowed_mail_hosts(raw_allowed_hosts)
        from mail_client import test_imap_connection, test_smtp_connection

        if conn_type == 'imap':
            result = test_imap_connection(
                server=data.get('imap_server', ''),
                port=int(data.get('imap_port', 993)),
                ssl=bool(data.get('imap_ssl', True)),
                email_address=email_address,
                password=password,
                allowed_hosts=allowed_hosts,
            )
        else:
            result = test_smtp_connection(
                server=data.get('smtp_server', ''),
                port=int(data.get('smtp_port', 587)),
                starttls=bool(data.get('smtp_starttls', True)),
                email_address=email_address,
                password=password,
                allowed_hosts=allowed_hosts,
            )

        return jsonify(result)
    except ValueError as exc:
        return jsonify({'success': False, 'message': str(exc)}), 400
    except Exception as exc:
        logger.error("Mail test connection error: %s", exc)
        capture_observability_exception(
            exc,
            tags={'component': 'mail', 'operation': 'test_connection'},
            extra={'connection_type': conn_type, 'email_address': email_address},
            user={'email': session.get('user_email')},
        )
        return _server_error_response('Грешка при тестирању mail конекције.')
