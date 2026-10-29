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


def _cubic_rocksalt_instance(a=5.64):
    inst = _make_instance()
    inst.get_powder_dif_data = lambda name: {
        'mineral_name': 'Halite',
        'cell_parameters': {'a': a, 'b': a, 'c': a,
                            'alpha': 90.0, 'beta': 90.0, 'gamma': 90.0},
        'space_group': 'P 1',
        'atoms': [{'element': 'Na', 'x': 0.0, 'y': 0.0, 'z': 0.0, 'occupancy': 1.0, 'b_iso': 0.5},
                  {'element': 'Cl', 'x': 0.5, 'y': 0.5, 'z': 0.5, 'occupancy': 1.0, 'b_iso': 0.5}],
    }
    return inst


def _parse_cif(cif):
    """Return ({cell tag: float}, [(x, y, z) fractional]) from our own CIF text."""
    cell, atoms, in_atoms = {}, [], False
    for line in cif.split('\n'):
        parts = line.split()
        if not parts:
            continue
        if parts[0].startswith('_cell_'):
            cell[parts[0]] = float(parts[1])
        elif parts[0] == '_atom_site_U_iso_or_equiv':
            in_atoms = True
        elif in_atoms and len(parts) == 7 and not parts[0].startswith('_'):
            atoms.append(tuple(float(v) for v in parts[2:5]))
    return cell, atoms


def _min_distance(cell, atoms):
    # Cubic cell: Cartesian = fractional * a. No periodic images on purpose —
    # the listed atoms alone must keep the same nearest-neighbour spacing.
    import itertools
    import math
    a = cell['_cell_length_a']
    return min(a * math.sqrt(sum((p[i] - q[i]) ** 2 for i in range(3)))
               for p, q in itertools.combinations(atoms, 2))


def test_supercell_scales_cell_lengths_and_keeps_spacing():
    # Bug: _generate_supercell_atoms divides fractional coordinates by nx/ny/nz
    # while _cell_length_a/b/c and _cell_volume stayed unscaled, so a (2,2,2)
    # supercell was 8x denser than the real crystal.
    inst = _cubic_rocksalt_instance(a=5.64)
    cell_1, atoms_1 = _parse_cif(inst.generate_cif_from_dif('Halite', expand_unitcell=True))
    cell_8, atoms_8 = _parse_cif(inst.generate_cif_from_dif('Halite', expand_unitcell=True,
                                                            supercell=(2, 2, 2)))
    assert cell_1['_cell_length_a'] == 5.64
    assert len(atoms_1) == 2

    assert cell_8['_cell_length_a'] == 11.28
    assert cell_8['_cell_length_b'] == 11.28
    assert cell_8['_cell_length_c'] == 11.28
    for angle in ('alpha', 'beta', 'gamma'):
        assert cell_8['_cell_angle_' + angle] == 90.0
    assert abs(cell_8['_cell_volume'] - 5.64 ** 3 * 8) < 0.01  # CIF rounds to 2 decimals
    assert len(atoms_8) == 8 * len(atoms_1)
    assert all(0.0 <= v < 1.0 for atom in atoms_8 for v in atom)
    assert abs(_min_distance(cell_8, atoms_8) - _min_distance(cell_1, atoms_1)) < 1e-6


def test_supercell_anisotropic_scales_each_axis():
    inst = _cubic_rocksalt_instance(a=4.0)
    cell, atoms = _parse_cif(inst.generate_cif_from_dif('Halite', expand_unitcell=True,
                                                        supercell=(1, 2, 3)))
    assert (cell['_cell_length_a'], cell['_cell_length_b'], cell['_cell_length_c']) == (4.0, 8.0, 12.0)
    assert len(atoms) == 2 * 6
    assert cell['_cell_volume'] == 384.0


def test_supercell_does_not_mutate_source_cell():
    inst = _cubic_rocksalt_instance(a=5.0)
    dif = inst.get_powder_dif_data('Halite')
    inst.get_powder_dif_data = lambda name: dif
    inst.generate_cif_from_dif('Halite', expand_unitcell=True, supercell=(2, 2, 2))
    assert dif['cell_parameters'] == {'a': 5.0, 'b': 5.0, 'c': 5.0,
                                      'alpha': 90.0, 'beta': 90.0, 'gamma': 90.0}
    # A second call must not compound the scaling.
    cell, _ = _parse_cif(inst.generate_cif_from_dif('Halite', expand_unitcell=True, supercell=(2, 2, 2)))
    assert cell['_cell_length_a'] == 10.0


def test_mineral_science_view_mode_supercell_route_still_serves():
    # /api/local_rruff_cif?view_mode=supercell (admin_mineral_detail.html) is the
    # other caller of the supercell path; it must get the rescaled cell, no error.
    import json

    import app as museum_app
    import mineral_science_views

    inst = _cubic_rocksalt_instance(a=5.64)

    class Fake:
        available = True

        def __init__(self, *a, **k):
            pass

        def generate_cif_from_dif(self, *a, **k):
            return inst.generate_cif_from_dif(*a, **k)

    with patch.object(local_rruff_data, 'LocalRRUFFData', Fake), \
            museum_app.app.test_request_context('/api/local_rruff_cif/Halite?view_mode=supercell'):
        odgovor = mineral_science_views.api_get_local_rruff_cif('Halite')
    telo = odgovor[0] if isinstance(odgovor, tuple) else odgovor
    podaci = json.loads(telo.get_data(as_text=True))
    assert podaci['success'] is True
    assert podaci['view_mode'] == 'supercell'
    cell, atoms = _parse_cif(podaci['cif_content'])
    assert cell['_cell_length_a'] == 11.28
    assert len(atoms) == 16


def test_smoke_import():
    assert hasattr(local_rruff_data, 'LocalRRUFFData')
