#!/usr/bin/env python3
"""Тестови за чишћење колоне minerals.quantity (feat/ciscenje-kolicina).

Правила (извор = inventory_entries.quantity):
  1) N+1 = збир            5) „ima X a ne Y“ → X
  2) број + текст напомена  6) чист текст → NULL
  3) датум → acquisition_date + quantity NULL (+ траг у comments)
  4) римски → арапски       7) чист број 1–99 → не дира се

+ понашање опрезног блока 3544–3568: САМО правило датума и заштита физички
потврђеног малог броја (1–99) од брисања датумом.

Језгро су чисте функције, па тестови не траже базу.
"""

import unittest

import ciscenje_kolicina_cli as k


class DateParsingTests(unittest.TestCase):
    """Правило 3 — парсирање датума (језгро)."""

    def test_full_dmy(self):
        self.assertEqual(k.parse_date('13.5.2002.'), ('2002-05-13', None))
        self.assertEqual(k.parse_date('8.2.2008.'), ('2008-02-08', None))
        self.assertEqual(k.parse_date('12.8.2004'), ('2004-08-12', None))

    def test_with_inv_prefix(self):
        self.assertEqual(k.parse_date('Inv. 20.8.2009.'), ('2009-08-20', None))
        self.assertEqual(k.parse_date('Inventarisano 8.6.2007.'), ('2007-06-08', None))

    def test_month_year_assumes_first_of_month(self):
        iso, assumption = k.parse_date('Inventarisano maj 2006.')
        self.assertEqual(iso, '2006-05-01')
        self.assertIsNotNone(assumption)

    def test_year_only_assumes_first_of_january(self):
        iso, assumption = k.parse_date('2006')
        self.assertEqual(iso, '2006-01-01')
        self.assertIsNotNone(assumption)

    def test_non_date_returns_none(self):
        self.assertIsNone(k.parse_date('2+1'))
        self.assertIsNone(k.parse_date('Raspada se'))
        self.assertIsNone(k.parse_date('oko 5000'))
        self.assertIsNone(k.parse_date(''))

    def test_invalid_date_rejected(self):
        self.assertIsNone(k.parse_date('31.2.2001.'))


class ClassifyRuleTests(unittest.TestCase):
    """По једно правило."""

    def test_rule1_sum(self):
        self.assertEqual(k.classify_quantity('2+1')['quantity'], 3)
        self.assertEqual(k.classify_quantity('8+1')['quantity'], 9)
        r = k.classify_quantity('3+5+5+1+4+16')
        self.assertEqual(r['quantity'], 34)
        self.assertEqual(r['action'], 'set')
        self.assertEqual(r['comment_add'], '')

    def test_rule2_number_plus_text(self):
        r = k.classify_quantity('3+1 Ima 3 kom')
        self.assertEqual(r['quantity'], 4)
        self.assertEqual(r['comment_add'], 'Ima 3 kom')
        r2 = k.classify_quantity('1+1 eksponat')
        self.assertEqual(r2['quantity'], 2)
        self.assertEqual(r2['comment_add'], 'eksponat')
        r3 = k.classify_quantity('2, Peščar formacija "Denbaba"')
        self.assertEqual(r3['quantity'], 2)
        self.assertIn('Peščar', r3['comment_add'])

    def test_rule3_date(self):
        r = k.classify_quantity('13.5.2002.')
        self.assertEqual(r['action'], 'date')
        self.assertIsNone(r['quantity'])
        self.assertEqual(r['date_iso'], '2002-05-13')
        self.assertIn(k.COMMENT_BOOK_PREFIX, r['comment_add'])
        self.assertIn('13.5.2002.', r['comment_add'])

    def test_rule4_roman(self):
        self.assertEqual(k.classify_quantity('I')['quantity'], 1)
        self.assertEqual(k.classify_quantity('II')['quantity'], 2)
        self.assertEqual(k.classify_quantity('IV')['quantity'], 4)
        # „IX horizont“ је локација, не количина.
        self.assertEqual(k.classify_quantity('IX horizont')['action'], 'null')

    def test_rule5_ima_x_a_ne_y(self):
        r = k.classify_quantity('ima 21 a ne 25')
        self.assertEqual(r['quantity'], 21)
        self.assertEqual(r['comment_add'], 'ima 21 a ne 25')
        self.assertEqual(k.classify_quantity('ima 4 a ne 6')['quantity'], 4)

    def test_rule6_pure_text_null(self):
        for txt in ('Raspada se', 'ormar u kanc', 'Plus 1 antimonit?',
                    'Pb i Zn', 'samo etiketa'):
            r = k.classify_quantity(txt)
            self.assertEqual(r['action'], 'null', txt)
            self.assertIsNone(r['quantity'])
            self.assertEqual(r['comment_add'], txt)

    def test_rule7_clean_small_number(self):
        r = k.classify_quantity('2')
        self.assertEqual(r['action'], 'set')
        self.assertEqual(r['quantity'], 2)
        self.assertEqual(r['comment_add'], '')
        self.assertEqual(k.classify_quantity('99')['quantity'], 99)

    def test_empty_is_skip(self):
        self.assertEqual(k.classify_quantity('')['action'], 'skip')
        self.assertEqual(k.classify_quantity(None)['action'], 'skip')

    def test_big_number_and_merged_columns_go_to_review(self):
        self.assertEqual(k.classify_quantity('130')['action'], 'review')   # ≥100
        self.assertEqual(k.classify_quantity('2+1    3')['action'], 'review')  # спој колона
        self.assertEqual(k.classify_quantity('10   11')['action'], 'review')

    def test_horizont_number_is_location_not_count(self):
        # „7 Horizont“ = 7. хоризонт (стратиграфија), не 7 комада.
        self.assertEqual(k.classify_quantity('7 Horizont')['action'], 'null')


class PlanDateOnlyBlockTests(unittest.TestCase):
    """Опрезни блок 3544–3568: САМО датум + заштита малог чистог броја."""

    def test_clean_small_count_protected(self):
        # Количина је физички потврђена 1 иако књига има датум → НЕ ДИРА СЕ.
        minerals = [{'id': 1, 'number': 3549, 'quantity': 1, 'comments': None,
                     'acquisition_date': None}]
        book = {3549: '12.8.2004.'}
        plan = k.plan_cleanup(minerals, book, only_dates=True)
        self.assertEqual(plan['summary']['changes_total'], 0)
        self.assertEqual(plan['summary']['clean_total'], 1)
        self.assertEqual(plan['clean'][0]['number'], 3549)

    def test_date_fills_empty_acquisition_date(self):
        # Количина покварена (датум-број), acq празан → упиши датум, quantity NULL.
        minerals = [{'id': 2, 'number': 3560, 'quantity': 1352002, 'comments': None,
                     'acquisition_date': None}]
        book = {3560: '13.5.2002.'}
        plan = k.plan_cleanup(minerals, book, only_dates=True)
        self.assertEqual(plan['summary']['changes_total'], 1)
        ch = plan['changes'][0]
        self.assertTrue(ch['set_null'])
        self.assertEqual(ch['new_date'], '2002-05-13')
        self.assertIn('13.5.2002.', ch['comment_add'])

    def test_filled_acquisition_date_conflict_goes_to_review(self):
        import datetime
        minerals = [{'id': 3, 'number': 3557, 'quantity': 1352002, 'comments': None,
                     'acquisition_date': datetime.date(2007, 12, 20)}]
        book = {3557: 'Inventarisano 8.2.2008.'}
        plan = k.plan_cleanup(minerals, book, only_dates=True)
        self.assertEqual(plan['summary']['changes_total'], 0)
        self.assertEqual(plan['summary']['review_total'], 1)
        rev = plan['review'][0]
        self.assertEqual(rev['existing_date'], '2007-12-20')
        self.assertEqual(rev['book_date'], '2008-02-08')

    def test_same_acquisition_date_only_clears_quantity(self):
        import datetime
        minerals = [{'id': 4, 'number': 3558, 'quantity': 8022008, 'comments': None,
                     'acquisition_date': datetime.date(2008, 2, 8)}]
        book = {3558: '8.2.2008.'}
        plan = k.plan_cleanup(minerals, book, only_dates=True)
        ch = plan['changes'][0]
        self.assertTrue(ch['set_null'])
        self.assertIsNone(ch['new_date'])  # датум већ уписан, не дира се

    def test_only_dates_routes_non_dates_to_review(self):
        minerals = [{'id': 5, 'number': 3561, 'quantity': 999, 'comments': None,
                     'acquisition_date': None}]
        book = {3561: '2+1'}  # збир, али у блоку важи само датум
        plan = k.plan_cleanup(minerals, book, only_dates=True)
        self.assertEqual(plan['summary']['changes_total'], 0)
        self.assertEqual(plan['summary']['review_total'], 1)

    def test_comment_appended_not_overwritten(self):
        minerals = [{'id': 6, 'number': 3560, 'quantity': 1352002,
                     'comments': 'постоји белешка', 'acquisition_date': None}]
        book = {3560: '13.5.2002.'}
        plan = k.plan_cleanup(minerals, book, only_dates=True)
        # план носи само додатак; спајање ради база (CASE у SQL-у), али додатак
        # не сме прегазити — проверавамо да носи прави текст.
        self.assertIn('13.5.2002.', plan['changes'][0]['comment_add'])
        self.assertNotIn('постоји белешка', plan['changes'][0]['comment_add'])


class PlanAllRulesTests(unittest.TestCase):
    """Са свим правилима (--sva-pravila) — за касније шире пуштање."""

    def test_sum_change_recorded(self):
        # Количина недостаје (није чист мали број) → збир се примени.
        minerals = [{'id': 1, 'number': 100, 'quantity': None, 'comments': None,
                     'acquisition_date': None}]
        book = {100: '2+1'}
        plan = k.plan_cleanup(minerals, book, only_dates=False)
        ch = plan['changes'][0]
        self.assertEqual(ch['new_quantity'], 3)
        self.assertFalse(ch['set_null'])

    def test_clean_small_never_touched_even_in_full_mode(self):
        minerals = [{'id': 1, 'number': 100, 'quantity': 3, 'comments': None,
                     'acquisition_date': None}]
        book = {100: '13.5.2002.'}
        plan = k.plan_cleanup(minerals, book, only_dates=False)
        self.assertEqual(plan['summary']['changes_total'], 0)
        self.assertEqual(plan['summary']['clean_total'], 1)


if __name__ == '__main__':
    unittest.main()
