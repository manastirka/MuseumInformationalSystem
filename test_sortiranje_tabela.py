"""Сортирање табела: скрипта је укључена глобално и не дира табеле са
сопственим сортирањем."""
import re
import subprocess
import unittest
from pathlib import Path

KOREN = Path(__file__).resolve().parent


class SortiranjeTabelaTest(unittest.TestCase):
    def test_skripta_ukljucena_u_base(self):
        base = (KOREN / 'templates' / 'base.html').read_text(encoding='utf-8')
        self.assertIn("filename='js/sortiranje_tabela.js'", base)
        # иде после translator.js да пресловљавање не поремети иницијализацију
        self.assertLess(base.index("js/translator.js"), base.index("js/sortiranje_tabela.js"))

    def test_skripta_prepoznaje_sopstveno_sortiranje(self):
        js = (KOREN / 'static' / 'js' / 'sortiranje_tabela.js').read_text(encoding='utf-8')
        for selektor in ('th.sortable', 'th.sortable-header', 'th[data-sort]', 'sort_by'):
            self.assertIn(selektor, js)
        self.assertIn('data-sortiranje="ne"', js)
        # чисте функције изложене за Node тестове
        self.assertIn('global.MISSortiranje', js)

    def test_node_testovi_prolaze(self):
        rezultat = subprocess.run(
            ['node', '--test', str(KOREN / 'tests' / 'js' / 'sortiranje-tabela.test.js')],
            capture_output=True, text=True, timeout=60, cwd=str(KOREN))
        self.assertEqual(rezultat.returncode, 0, rezultat.stdout[-2000:] + rezultat.stderr[-2000:])
        self.assertTrue(re.search(r'^# pass [1-9]', rezultat.stdout, re.M), rezultat.stdout[-500:])
        self.assertIn('# fail 0', rezultat.stdout)


if __name__ == '__main__':
    unittest.main()
