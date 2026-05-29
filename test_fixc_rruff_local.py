import os

os.environ.setdefault('FLASK_ENV', 'testing')
os.environ.setdefault('SECRET_KEY', 'test-secret')
os.environ.setdefault('REDIS_URL', '')
os.environ.setdefault('SESSION_TYPE', 'filesystem')
os.environ.setdefault('SESSION_FILE_DIR', '/tmp/museum-test-c-rruff-local')

from unittest.mock import patch

import local_rruff_data
from local_rruff_data import LocalRRUFFData


def _make_instance():
    # Avoid touching the real filesystem index during __init__.
    with patch.object(LocalRRUFFData, '_load_or_build_index', lambda self: None):
        inst = LocalRRUFFData.__new__(LocalRRUFFData)
        inst._index = {'minerals': {}, 'rruff_ids': {}, 'stats': {}}
    return inst


# ---------------------------------------------------------------------------
# Finding 1: a legitimately measured average of exactly 0.0 must be preserved,
# not silently replaced by the recomputed mean of the measurement columns.
# ---------------------------------------------------------------------------
def test_microprobe_zero_average_is_preserved(tmp_path):
    inst = _make_instance()

    # Build a fake xlrd workbook/sheet exposing one oxide row whose authoritative
    # average (column index 17) is exactly 0.0 while its measurement columns
    # (indices 1..15) are non-zero. The bug recomputed the mean (~5.0) instead.
    class FakeCell:
        def __init__(self, value):
            self.value = value

    class FakeSheet:
        def __init__(self, rows):
            self._rows = rows
            self.nrows = len(rows)

        def row(self, i):
            return [FakeCell(v) for v in self._rows[i]]

    # Header row makes the parser enter the weight-percent section.
    header = ['Ox'] + ['Wt'] * 17
    # 18 measurement columns of 5.0, then average=0.0 at index 17, stdev=0.0 at 18.
    data_row = ['CaO'] + [5.0] * 16 + [0.0, 0.0]
    rows = [header, data_row]

    class FakeWorkbook:
        def sheet_by_index(self, idx):
            return FakeSheet(rows)

    chem_path = tmp_path / 'chem.xls'
    chem_path.write_text('stub')

    inst.get_mineral_data = lambda name: {
        'mineral_name': 'TestMineral',
        'chemistry': [{'path': str(chem_path), 'rruff_id': 'R000001'}],
    }

    import sys
    import types

    fake_xlrd = types.SimpleNamespace(open_workbook=lambda p: FakeWorkbook())
    with patch.dict(sys.modules, {'xlrd': fake_xlrd}):
        result = inst.get_microprobe_data('TestMineral')

    assert result is not None
    cao = next(e for e in result['elements'] if e['element'] == 'CaO')
    # The authoritative reported average of exactly 0.0 must be kept.
    assert cao['average'] == 0.0


# ---------------------------------------------------------------------------
# Finding 2: default (asymmetric) CIF must not claim P1 with no symmetry
# operators for a non-P1 mineral. Either it expands the atoms, or it writes
# the real space group plus a _symmetry_equiv_pos_as_xyz loop so a viewer can
# reconstruct the full cell.
# ---------------------------------------------------------------------------
def test_default_cif_declares_symmetry_for_non_p1_mineral():
    inst = _make_instance()

    # A non-P1 mineral (P 21/c, monoclinic, IT number 14) with a single
    # asymmetric-unit atom. The DIF gives only the asymmetric unit.
    inst.get_powder_dif_data = lambda name: {
        'mineral_name': 'Diopside',
        'cell_parameters': {'a': 8.0, 'b': 9.0, 'c': 7.0,
                            'alpha': 90.0, 'beta': 106.0, 'gamma': 90.0},
        'space_group': 'P 21/c',
        'atoms': [{'element': 'Si', 'x': 0.1, 'y': 0.2, 'z': 0.3,
                   'occupancy': 1.0, 'b_iso': 0.5}],
    }

    cif = inst.generate_cif_from_dif('Diopside')
    assert cif is not None

    # Count literal atom_site rows in the loop.
    lines = cif.split('\n')
    atom_rows = [l for l in lines if l.startswith('Si')]

    # P 21/c has 4 symmetry operations. Either the atoms were expanded (more
    # than one literal atom row), or the CIF carries the symmetry-equivalent
    # positions loop AND the real space group (so a viewer fills the cell).
    has_symmetry_loop = '_symmetry_equiv_pos_as_xyz' in cif
    declares_p1_only = ("'P 1'" in cif and '_symmetry_Int_Tables_number 1' in cif)

    if len(atom_rows) <= 1:
        # Only the asymmetric atom is listed -> we MUST carry symmetry info.
        assert has_symmetry_loop, "Default CIF lists only asymmetric atoms but has no symmetry operators"
        assert not declares_p1_only, "Default CIF still claims P1 for a non-P1 mineral"
        # The real space group symbol/number must be declared.
        assert "'P 21/c'" in cif
        assert '_symmetry_Int_Tables_number 14' in cif
        # The inversion centre operation of P 21/c must be present.
        assert '-x,-y,-z' in cif.replace(' ', '')


def test_expanded_cif_keeps_p1_identity():
    # Sanity: the explicit unitcell/supercell paths pre-expand atoms to literal
    # positions, so they must stay P1 (identity only) to avoid double-applying
    # symmetry in a viewer.
    inst = _make_instance()
    inst.get_powder_dif_data = lambda name: {
        'mineral_name': 'Diopside',
        'cell_parameters': {'a': 8.0, 'b': 9.0, 'c': 7.0,
                            'alpha': 90.0, 'beta': 106.0, 'gamma': 90.0},
        'space_group': 'P 21/c',
        'atoms': [{'element': 'Si', 'x': 0.1, 'y': 0.2, 'z': 0.3,
                   'occupancy': 1.0, 'b_iso': 0.5}],
    }
    cif = inst.generate_cif_from_dif('Diopside', expand_unitcell=True)
    assert cif is not None
    assert "'P 1'" in cif
    # No symmetry-equiv loop when atoms are already expanded (literal positions).
    assert '_symmetry_equiv_pos_as_xyz' not in cif


def test_smoke_import():
    assert hasattr(local_rruff_data, 'LocalRRUFFData')
