"""Regression tests for the admin panel reorganization (fix/admin-panel-raspored).

Covers two changes:
1. The vestigial "Управљање сликама" card (leftover of the removed legacy image
   system) is gone, together with its dead /api/images/stats link and the
   orphaned admin_image_gallery.html template.
2. Modules are grouped into clear vertical domain sections.
"""

import os
import unittest
from pathlib import Path


class AdminPanelReorgTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.content = Path('templates/admin_panel.html').read_text(encoding='utf-8')

    # --- Removal of legacy image management ---
    def test_image_management_card_removed(self):
        self.assertNotIn('Управљање сликама', self.content)

    def test_dead_image_stats_link_removed(self):
        self.assertNotIn('/api/images/stats', self.content)

    def test_orphaned_image_gallery_template_deleted(self):
        self.assertFalse(
            os.path.exists('templates/admin_image_gallery.html'),
            'Orphaned admin_image_gallery.html should be deleted',
        )

    # --- Vertical domain sections ---
    def test_domain_section_titles_present(self):
        for title in ('Корисници и приступ', 'Збирке и садржај', 'Систем и логови'):
            self.assertIn(title, self.content, f'Missing section: {title}')

    def test_uses_vertical_module_list(self):
        self.assertIn('admin-module-list', self.content)
        self.assertIn('admin-module-item', self.content)

    # --- Non-system modules still present (nothing lost in the reshuffle) ---
    def test_live_modules_preserved(self):
        for endpoint in (
            "url_for('admin_statistics')",
            "url_for('museum_databases')",
            "url_for('employees_database')",
            "url_for('employee_profiles_database')",
            "url_for('manage_user_access')",
            "url_for('admin_password_manager')",
            "url_for('add_user')",
        ):
            self.assertIn(endpoint, self.content, f'Lost module link: {endpoint}')

    # --- System/logs modules consolidated into the single "Систем" hub item ---
    # (settings/mail/reports/audit now live under /admin/sistem — see test_sistem_hub)
    def test_system_section_is_single_hub_item(self):
        self.assertIn("url_for('admin_system_hub')", self.content)
        for moved in (
            "url_for('admin_system_settings')",
            "url_for('admin_mail_configuration')",
            "url_for('system_reports')",
            "url_for('admin_audit_log')",
        ):
            self.assertNotIn(moved, self.content, f'{moved} should have moved to the hub')

    # --- Do not regress notification wiring (see test_production_readiness) ---
    def test_notification_api_preserved(self):
        self.assertIn("fetch('/api/notifications')", self.content)

    # --- OS-style redesign (feat/admin-panel-os-izgled) ---
    def test_quick_actions_removed(self):
        # Секција брзих администраторских акција је уклоњена у целости.
        self.assertNotIn('Брзе администраторске акције', self.content)

    def test_simulated_quick_action_handlers_removed(self):
        # Пратеће лажне/симулиране акције (backup/restart/логови/ажурирање) су уклоњене.
        for gone in ('performBackup', 'performRestart', 'checkForUpdates',
                     'showLogsModal', 'loadLogs', 'refreshLogs', 'logsModal'):
            self.assertNotIn(gone, self.content, f'Leftover quick-action code: {gone}')

    def test_two_pane_os_layout_present(self):
        # Дводелни распоред: лева навигација секција + десни садржај.
        for marker in ('admin-os-layout', 'admin-os-nav', 'admin-nav-item',
                       'admin-pane', 'selectSection'):
            self.assertIn(marker, self.content, f'Missing OS-layout marker: {marker}')

    def test_settings_search_present(self):
        # Претрага подешавања на врху, филтрира ставке клијентски.
        self.assertIn('applyView', self.content)
        self.assertIn('data-module-search', self.content)


if __name__ == '__main__':
    unittest.main()
