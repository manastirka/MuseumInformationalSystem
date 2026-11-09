#!/usr/bin/env python3
"""kristalografija.py — CIF → P1 без спољне библиотеке, над правим COD/AMCSD
фајловима (tests/fixtures/cod). Мотор уџбеника очекује тачно облик који је
давао generate_cif_from_dif(expand_unitcell=True), па се и он проверава."""
import re
import unittest
from fractions import Fraction
from pathlib import Path

import kristalografija as k

FIKSTURE = Path(__file__).resolve().parent / 'tests' / 'fixtures' / 'cod'


def _cif(cod_id):
    return (FIKSTURE / f'{cod_id}.cif').read_text(encoding='utf-8')


class OperatoriTest(unittest.TestCase):
    def test_parsiranje_oblika_iz_cod_a(self):
        x, y, z = (Fraction(1), Fraction(0), Fraction(0)), (0, 1, 0), (0, 0, 1)
        self.assertEqual(k.parsiraj_operator('x,y,z'), ((1, 0, 0, 0), (0, 1, 0, 0), (0, 0, 1, 0)))
        self.assertEqual(k.parsiraj_operator('1/2+x,-y,1/2-z'), ((1, 0, 0, Fraction(1, 2)), (0, -1, 0, 0),
                                                                 (0, 0, -1, Fraction(1, 2))))
        self.assertEqual(k.parsiraj_operator('-y,x-y,z'), ((0, -1, 0, 0), (1, -1, 0, 0), (0, 0, 1, 0)),
                         'хексагонални оператор са два члана')
        self.assertEqual(k.parsiraj_operator('2/3+x,1/3+y,1/3+z')[0], (1, 0, 0, Fraction(2, 3)), 'R центрирање')
        self.assertEqual(k.parsiraj_operator('X, Y+0.5, -Z'), ((1, 0, 0, 0), (0, 1, 0, Fraction(1, 2)), (0, 0, -1, 0)))
        del x, y, z

    def test_primena_i_svodjenje_u_celiju(self):
        op = k.parsiraj_operator('-x+1/2,y,-z')
        self.assertEqual(tuple(round(v, 6) for v in k.primeni_operator(op, 0.1, 0.2, 0.3)), (0.4, 0.2, -0.3))
        self.assertEqual(k.u_celiju(-0.3), 0.7)
        self.assertEqual(k.u_celiju(0.9995), 0.0, 'крај ћелије је исто што и почетак')
        self.assertTrue(k.isto_mesto((0.0005, 0.5, 0.5), (0.9999, 0.5, 0.5)), 'периодично поређење')

    def test_neispravan_operator_je_greska(self):
        for los in ('x,y', 'x,y,z,w', 'x,y,q', 'x+,y,z', 'abc,y,z'):
            with self.assertRaises(k.CifGreska, msg=los):
                k.parsiraj_operator(los)


class CitanjeCifTest(unittest.TestCase):
    def test_tagovi_petlje_i_tekst_u_tackazarezu(self):
        cif = k.parsiraj_cif(_cif(9000594))
        self.assertEqual(cif['tagovi']['_chemical_formula_sum'], 'Fe S2')
        self.assertEqual(cif['tagovi']['_symmetry_space_group_name_h-m'], 'P a -3')
        self.assertIn('weakly anisotropic pyrite', cif['tagovi']['_publ_section_title'])
        self.assertEqual(len(k.petlja_sa(cif, '_symmetry_equiv_pos_as_xyz')['_symmetry_equiv_pos_as_xyz']), 24)
        self.assertEqual(k.petlja_sa(cif, '_publ_author_name')['_publ_author_name'], ['Bayliss, P.'])
        self.assertEqual(k.broj('0.3331(2)'), 0.3331)
        self.assertIsNone(k.broj('?'))

    def test_element_iz_oznake_i_tipa(self):
        self.assertEqual(k.element_atoma('Si1'), 'Si')
        self.assertEqual(k.element_atoma('O-H6', 'O'), 'O')
        self.assertEqual(k.element_atoma('Fe2', 'Fe2+'), 'Fe')
        self.assertEqual(k.element_atoma('Wat1'), 'O', 'AMCSD договор: Wat = вода')
        self.assertEqual(k.element_atoma('Cl'), 'Cl')
        self.assertEqual(k.element_atoma('S'), 'S')
        with self.assertRaises(k.CifGreska):
            k.element_atoma('Xx9')

    def test_citat_uslovi_i_formula(self):
        cif = k.parsiraj_cif(_cif(9013321))
        citat = k.citat_iz(cif)
        self.assertEqual((citat['autori'], citat['godina'], citat['casopis'], citat['tom']),
                         (['Antao, S. M.', 'Hassan, I.', 'Wang, J.', 'Lee, P. L.', 'Toby, B. H.'], 2008,
                          'The Canadian Mineralogist', '46'))
        self.assertEqual(citat['doi'], '10.3749/canmin.46.5.1501')
        self.assertEqual(citat['strane'], '1501–1509')
        self.assertEqual(k.formula_iz(cif), ({'O': 2.0, 'Si': 1.0}, 3))
        self.assertEqual(k.uslovi_iz(k.parsiraj_cif(_cif(9003308))), {'temperatura_k': 298.15, 'pritisak_kpa': 0.0})
        self.assertEqual(k.uslovi_iz(cif), {'temperatura_k': None, 'pritisak_kpa': None})


class ProsirenjeTest(unittest.TestCase):
    def _p1(self, cod_id, ime):
        return k.struktura_p1(_cif(cod_id), ime)

    def test_broj_atoma_po_celiji(self):
        for cod_id, ime, ocekivano in ((9003308, 'halit', 8), (9000594, 'pirit', 12), (9013321, 'kvarc', 9),
                                       (9000095, 'kalcit', 30)):
            _, podaci = self._p1(cod_id, ime)
            self.assertEqual(podaci['broj_atoma'], ocekivano, ime)

    def test_po_elementu_i_bez_duplikata(self):
        _, podaci = self._p1(9003308, 'halit')
        cif = k.parsiraj_cif(_cif(9003308))
        atomi = k.prosiri_u_p1(k.atomi_iz(cif), k.operatori_iz(cif))
        self.assertEqual(sorted(a['element'] for a in atomi), ['Cl'] * 4 + ['Na'] * 4)
        polozaji = [(round(a['x'], 3), round(a['y'], 3), round(a['z'], 3)) for a in atomi]
        self.assertEqual(len(set(polozaji)), 8, '192 оператора × 2 атома → 8 различитих места')
        self.assertEqual(podaci['prostorna_grupa'], 'F m -3 m')

    def test_mesovito_mesto_zadrzava_vecinsku_vrstu(self):
        """Мусковит 2M1: Si0.75/Al0.25 на истом тетраедарском месту — једно
        место, Si; укупно 76 положаја (Z=4 × 19 без H)."""
        p1, podaci = self._p1(9000837, 'muskovit')
        self.assertEqual(podaci['broj_atoma'], 76)
        self.assertNotIn('H', {a['element'] for a in k.atomi_iz(k.parsiraj_cif(_cif(9000837)))})
        redovi = [r for r in p1.splitlines() if re.match(r'^[A-Z][a-z]?\d+ ', r)]
        self.assertEqual(len(redovi), 76)
        self.assertEqual(sum(1 for r in redovi if r.startswith('Si')), 16,
                         'сва 16 T места (2 × 8f) носе већинску врсту Si')
        self.assertEqual(sum(1 for r in redovi if r.startswith('Al')), 8, 'само октаедарски Al (8f)')
        self.assertEqual(sum(1 for r in redovi if r.startswith('K')), 4)

    def test_pogresan_z_je_greska(self):
        tekst = _cif(9000594).replace('_cell_formula_units_Z            4', '_cell_formula_units_Z            8')
        with self.assertRaises(k.CifGreska) as ctx:
            k.struktura_p1(tekst, 'pirit')
        self.assertIn('12', str(ctx.exception))
        self.assertIn('24', str(ctx.exception))

    def test_oblik_izlaza_kao_rruff_generate_cif_from_dif(self):
        p1, podaci = self._p1(9000594, 'pirit')
        linije = p1.splitlines()
        self.assertEqual(linije[0], 'data_pirit')
        self.assertIn('_cell_length_a 5.4166', linije)
        self.assertIn('_cell_angle_gamma 90.00', linije)
        self.assertIn('_cell_volume 158.92', linije)
        self.assertIn("_symmetry_space_group_name_H-M 'P 1'", linije)
        self.assertIn('_symmetry_Int_Tables_number 1', linije)
        i = linije.index('loop_')
        self.assertEqual(linije[i + 1:i + 8], ['_atom_site_label', '_atom_site_type_symbol', '_atom_site_fract_x',
                                               '_atom_site_fract_y', '_atom_site_fract_z', '_atom_site_occupancy',
                                               '_atom_site_U_iso_or_equiv'])
        atomi = linije[i + 8:]
        self.assertEqual(len(atomi), 12)
        self.assertRegex(atomi[0], r'^Fe1 Fe 0\.00000 0\.00000 0\.00000 1\.000 0\.0036$')
        obrazac = re.compile(r'^(Fe|S)\d+ (Fe|S) \d\.\d{5} \d\.\d{5} \d\.\d{5} 1\.000 \d\.\d{4}$')
        self.assertTrue(all(obrazac.match(a) for a in atomi))
        self.assertNotIn('_symmetry_equiv_pos_as_xyz', p1, 'читач не сме поново да примени симетрију')

    def test_cif_bez_operatora_prolazi_samo_za_p1(self):
        tekst = 'data_x\n_cell_length_a 3\n_cell_length_b 3\n_cell_length_c 3\n_symmetry_space_group_name_H-M "P 1"\n' \
                '_chemical_formula_sum "Cu"\n_cell_formula_units_Z 1\nloop_\n_atom_site_label\n_atom_site_fract_x\n' \
                '_atom_site_fract_y\n_atom_site_fract_z\nCu 0 0 0\n'
        p1, podaci = k.struktura_p1(tekst, 'bakar')
        self.assertEqual(podaci['broj_atoma'], 1)
        with self.assertRaises(k.CifGreska):
            k.struktura_p1(tekst.replace('"P 1"', '"F m -3 m"'), 'bakar')


if __name__ == '__main__':
    unittest.main()
