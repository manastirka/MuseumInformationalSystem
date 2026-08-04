#!/usr/bin/env python3
"""Тестови за усклађивање инвентарске књиге и физичке базе депоа.

Покрива четири захтева (одлука кустоса, feat/knjiga-vs-depo):
  1. Ознака границе 3572 (штампана књига постоји само до 3572).
  2. Увоз књижних записа означава ФИЗИЧКИ НЕПОТВРЂЕНО (confirmed=False, source).
  3. Допуна попуњава САМО празна поља — никад не гази попуњено.
  4. Конфликт (различито име/количина) иде у ПРЕГЛЕД, не у аутоматску измену.

Језгро су чисте функције, па тестови не траже базу.
"""

import unittest

import uskladi_knjiga_depo_cli as u


class PrintedBookBoundaryTests(unittest.TestCase):
    """Захтев 1: ознака 1..3572."""

    def test_boundary_inclusive_and_exclusive(self):
        self.assertTrue(u.is_in_printed_book(1))
        self.assertTrue(u.is_in_printed_book(3572))
        self.assertTrue(u.is_in_printed_book('3572'))
        self.assertFalse(u.is_in_printed_book(3573))
        self.assertFalse(u.is_in_printed_book('3573'))

    def test_m_prefix_normalizes_to_digits(self):
        # M-префикс: само цифре. Реалних M ≤ 3572 нема, али функција је чиста.
        self.assertEqual(u.normalize_number('M4333'), 4333)
        self.assertFalse(u.is_in_printed_book('M4333'))

    def test_intruder_and_empty_excluded(self):
        self.assertFalse(u.is_in_printed_book('2932317'))  # уљез > 3572
        self.assertFalse(u.is_in_printed_book(''))
        self.assertFalse(u.is_in_printed_book(None))
        self.assertFalse(u.is_in_printed_book('0'))


class ImportMarksUnconfirmedTests(unittest.TestCase):
    """Захтев 2: уписани књижни ред је физички непотврђен."""

    def test_build_insert_row_flags(self):
        row = u.build_insert_row({'inventory_number': '100', 'name': 'Kvarc',
                                  'locality': 'Трепча', 'acquisition_info': 'поклон',
                                  'collector': 'Петровић', 'notes': 'леп примерак',
                                  'quantity': '3'})
        self.assertIs(row['physical_presence_confirmed'], False)
        self.assertEqual(row['source'], u.IMPORT_SOURCE)
        self.assertEqual(row['item_name'], 'Kvarc')
        self.assertEqual(row['card_locality'], 'Трепча')
        self.assertEqual(row['acquisition_method'], 'поклон')
        self.assertEqual(row['quantity'], 3)
        self.assertIn('Сакупљач: Петровић', row['comments'])
        self.assertIn('штампане инвентарске књиге', row['comments'])

    def test_plan_inserts_missing_as_unconfirmed(self):
        book = [{'inventory_number': '100', 'name': 'Kvarc'}]
        minerals = []  # депо нема тај број
        plan = u.plan_reconciliation(book, minerals)
        self.assertEqual(plan['summary']['inserts'], 1)
        self.assertIs(plan['inserts'][0]['row']['physical_presence_confirmed'], False)
        self.assertEqual(plan['inserts'][0]['row']['source'], u.IMPORT_SOURCE)


class FillDoesNotOverwriteTests(unittest.TestCase):
    """Захтев 3: допуна само празних поља."""

    def test_empty_field_filled(self):
        book = {'locality': 'Бор', 'acquisition_info': 'откуп', 'notes': 'x'}
        mineral = {'card_locality': None, 'acquisition_method': '', 'comments': None}
        fills = u.compute_fills(book, mineral)
        self.assertEqual(fills['card_locality'], 'Бор')
        self.assertEqual(fills['acquisition_method'], 'откуп')
        self.assertIn('x', fills['comments'])

    def test_filled_field_never_overwritten(self):
        book = {'locality': 'Бор', 'acquisition_info': 'откуп', 'notes': 'ново'}
        mineral = {'card_locality': 'Мајданпек', 'acquisition_method': 'поклон',
                   'comments': 'постоји'}
        fills = u.compute_fills(book, mineral)
        self.assertEqual(fills, {})  # ништа се не гази

    def test_partial_fill_only_empty(self):
        book = {'locality': 'Бор', 'acquisition_info': 'откуп'}
        mineral = {'card_locality': 'Мајданпек', 'acquisition_method': None, 'comments': 'x'}
        fills = u.compute_fills(book, mineral)
        self.assertNotIn('card_locality', fills)      # попуњено — не дира
        self.assertEqual(fills['acquisition_method'], 'откуп')  # празно — попуни


class ConflictGoesToPreviewTests(unittest.TestCase):
    """Захтев 4: конфликт у преглед, не у измену."""

    def test_name_classification(self):
        self.assertEqual(u.classify_name_conflict('Kvarc', 'Kvarc'), 'same')
        # Разлика само у писму/дијакритици => исти кључ => 'same' (није конфликт).
        self.assertEqual(u.classify_name_conflict('Антимон', 'Antimon'), 'same')
        self.assertEqual(u.classify_name_conflict('Ćuprija', 'Cuprija'), 'same')
        # Ситна слова разлика (C↔S) али различит кључ => вероватна транслитерација.
        self.assertEqual(u.classify_name_conflict('Celestin', 'Selestin'), 'transliteration')
        # Суштински другачије => кустос пресуђује.
        self.assertEqual(u.classify_name_conflict('Antracit', 'Pirit sa galenitom'), 'substantive')

    def test_conflict_not_in_fills_and_name_never_edited(self):
        book = [{'inventory_number': '34', 'name': 'Antracit', 'locality': 'X'}]
        minerals = [{'id': 9, 'inventory_number': '34', 'item_name': 'Pirit sa galenitom',
                     'card_locality': None}]
        plan = u.plan_reconciliation(book, minerals)
        # Конфликт постоји, у прегледу
        names = [c for c in plan['conflicts'] if c['field'] == 'name']
        self.assertEqual(len(names), 1)
        self.assertEqual(names[0]['kind'], 'substantive')
        # НЕ уписује (број постоји), НЕ мења item_name (fills никад не садрже item_name)
        self.assertEqual(plan['summary']['inserts'], 0)
        for f in plan['fills']:
            self.assertNotIn('item_name', f['fields'])

    def test_quantity_conflict_detected(self):
        book = {'inventory_number': '5', 'name': 'Kvarc', 'quantity': '10'}
        mineral = {'inventory_number': '5', 'item_name': 'Kvarc', 'quantity': 3}
        conflicts = u.detect_conflicts(book, mineral)
        qty = [c for c in conflicts if c['field'] == 'quantity']
        self.assertEqual(len(qty), 1)
        self.assertEqual(qty[0]['book_value'], '10')
        self.assertEqual(qty[0]['db_value'], 3)


if __name__ == '__main__':
    unittest.main()
