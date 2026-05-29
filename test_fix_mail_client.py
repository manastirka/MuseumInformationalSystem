#!/usr/bin/env python3
"""Regression test for pooled IMAP selection tracker desync after send_message
Sent-folder probing when no Sent folder is found.

See finding: 'Pooled IMAP selection tracker desynced after send_message
Sent-folder probing' (mail_client.py send_message, lines ~2180-2192).
"""

import os

os.environ.setdefault('FLASK_ENV', 'testing')
os.environ.setdefault('SECRET_KEY', 'test-secret')
os.environ.setdefault('REDIS_URL', '')
os.environ.setdefault('SESSION_TYPE', 'filesystem')
os.environ.setdefault('SESSION_FILE_DIR', '/tmp/museum-test-mail-client')

import unittest
from unittest import mock

import mail_client


class FakeIMAP:
    """Minimal IMAP stand-in: SELECT always fails (no Sent folder exists)."""

    def __init__(self):
        self.selected = 'PRIOR_SELECTED'
        self.select_calls = []
        self.append_calls = []

    def select(self, mailbox=None, readonly=False):
        self.select_calls.append((mailbox, readonly))
        # RFC 3501: a failed SELECT leaves the connection with no mailbox.
        self.selected = None
        return ('NO', [b'mailbox not found'])

    def append(self, *args, **kwargs):
        self.append_calls.append((args, kwargs))
        return ('OK', [b'appended'])


class SentFolderTrackerDesyncTest(unittest.TestCase):
    USER = 'tracker-test@example.com'

    def setUp(self):
        # Build a MailClient without running __init__ (no DB / decryption needed).
        self.client = mail_client.MailClient.__new__(mail_client.MailClient)
        self.client.user_email = self.USER
        self.client.settings = {
            'email_address': self.USER,
            'smtp_server': 'mail.example.com',
            'imap_server': 'mail.example.com',
        }
        self.client._password = 'pw'

        self.fake_imap = FakeIMAP()

        # Seed the pool with a tracked selection from a PRIOR request, mimicking
        # the persistent per-user pool entry.
        with mail_client._pool_lock:
            mail_client._pool[self.USER] = {
                'c': self.fake_imap,
                't': 0.0,
                'pw': 'pw',
                'sel': 'INBOX',
                'sel_ro': True,
            }

    def tearDown(self):
        with mail_client._pool_lock:
            mail_client._pool.pop(self.USER, None)

    def test_tracker_reset_when_no_sent_folder_found(self):
        # SMTP send is irrelevant to the tracker bug; stub it out entirely.
        with mock.patch.object(self.client, '_imap', return_value=self.fake_imap), \
                mock.patch('mail_client.validate_mail_server_settings',
                           side_effect=lambda s: dict(s)), \
                mock.patch('mail_client.smtplib.SMTP') as smtp_cls:
            smtp_instance = smtp_cls.return_value
            smtp_instance.ehlo.return_value = ('OK', [])
            smtp_instance.starttls.return_value = ('OK', [])
            smtp_instance.login.return_value = ('OK', [])
            smtp_instance.sendmail.return_value = {}

            result = self.client.send_message('dest@example.com', 'Subj', 'Body')

        self.assertTrue(result)
        # The probing loop SELECTed several Sent candidates; the real connection
        # now has NO mailbox selected.
        self.assertTrue(self.fake_imap.select_calls)
        self.assertIsNone(self.fake_imap.selected)

        # Bug: the pool tracker still claims 'INBOX' is selected, so a later
        # _select_folder(INBOX, readonly=True) would skip re-SELECTing and
        # operate on the wrong/no mailbox. Correct behavior: tracker reset.
        sel, _sel_ro = mail_client._pool_selected(self.USER)
        self.assertIsNone(
            sel,
            "pool selection tracker must be reset after Sent-folder probing "
            "even when no Sent folder is found",
        )


if __name__ == '__main__':
    unittest.main()
