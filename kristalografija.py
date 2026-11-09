"""Кристалографија за уџбеник: читање CIF-а, симетријски оператори и ширење
јединичне ћелије у P1.

Мотор уџбеника (static/udzbenik/) очекује ТАЧНО облик који је давао
``local_rruff_data.generate_cif_from_dif(..., expand_unitcell=True)``: све
положаје атома у ћелији исписане дословно, уз ``'P 1'`` да читач не
примењује симетрију поново. Овај модул то ради над било којим CIF-ом
(Crystallography Open Database, AMCSD…), без спољне библиотеке: симетријски
оператори се читају из самог CIF-а (``_space_group_symop_operation_xyz`` /
``_symmetry_equiv_pos_as_xyz``) и примењују на асиметричну јединицу.

Правила ширења:
- положај се своди у [0, 1); два положаја на растојању < TOLERANCIJA
  (периодично) су ИСТО место — задржава се први, а атоми се обрађују по
  опадајућој заузетости, па на мешовитом месту (Si0.75/Al0.25 у мусковиту)
  остаје већинска врста;
- провера броја атома: Z × збир формуле за елементе који постоје међу
  положајима (водоник сме да недостаје); по елементу кад су све заузетости 1,
  иначе само укупно.
"""
import math
import re
from fractions import Fraction

TOLERANCIJA = 1e-3
ELEMENTI = frozenset("""H He Li Be B C N O F Ne Na Mg Al Si P S Cl Ar K Ca Sc Ti V Cr Mn Fe Co Ni Cu Zn Ga Ge As Se
Br Kr Rb Sr Y Zr Nb Mo Tc Ru Rh Pd Ag Cd In Sn Sb Te I Xe Cs Ba La Ce Pr Nd Pm Sm Eu Gd Tb Dy Ho Er Tm Yb Lu Hf Ta W
Re Os Ir Pt Au Hg Tl Pb Bi Po At Rn Fr Ra Ac Th Pa U Np Pu Am Cm Bk Cf Es Fm Md No Lr Rf Db Sg Bh Hs Mt D""".split())
TAGOVI_OPERATORA = ('_space_group_symop_operation_xyz', '_symmetry_equiv_pos_as_xyz')
_CLAN = re.compile(r'^([+-]?)(\d+/\d+|\d*\.\d+|\d+)?\*?([xyz])?$')
_NESIGURNOST = re.compile(r'\([^)]*\)')
_ELEMENT_IZ_OZNAKE = re.compile(r'^([A-Za-z]+)')
_FORMULA_CLAN = re.compile(r'([A-Z][a-z]?)(\d*\.?\d*)')


class CifGreska(ValueError):
    """Неисправан или непотпун CIF за ширење у P1."""


# --------------------------------------------------------------------------
# Читање CIF-а (један data_ блок, без зависности)
# --------------------------------------------------------------------------

def _tokeni(tekst):
    """Токени CIF-а: ознаке (_tag), loop_, вредности (''/\"\"/;…; текст)."""
    linije = tekst.splitlines()
    i = 0
    while i < len(linije):
        linija = linije[i]
        if linija.startswith(';'):
            delovi = [linija[1:]]
            i += 1
            while i < len(linije) and not linije[i].startswith(';'):
                delovi.append(linije[i])
                i += 1
            yield '\n'.join(delovi).strip()
            i += 1
            continue
        poz = 0
        while poz < len(linija):
            c = linija[poz]
            if c.isspace():
                poz += 1
            elif c == '#':
                break
            elif c in '\'"':
                kraj = poz + 1
                while kraj < len(linija):
                    if linija[kraj] == c and (kraj + 1 == len(linija) or linija[kraj + 1].isspace()):
                        break
                    kraj += 1
                yield linija[poz + 1:kraj]
                poz = kraj + 1
            else:
                kraj = poz
                while kraj < len(linija) and not linija[kraj].isspace():
                    kraj += 1
                yield linija[poz:kraj]
                poz = kraj
        i += 1


def parsiraj_cif(tekst):
    """``{'tagovi': {ime: vrednost}, 'petlje': [{ime: [vrednosti]}]}`` првог
    data_ блока. Вредности остају текст (са несигурношћу у заградама)."""
    tagovi, petlje = {}, []
    tokeni = list(_tokeni(tekst))
    i = 0
    while i < len(tokeni):
        t = tokeni[i]
        if t.lower().startswith('data_') or t.lower() in ('global_', 'stop_'):
            i += 1
        elif t.lower() == 'loop_':
            i += 1
            imena = []
            while i < len(tokeni) and tokeni[i].startswith('_'):
                imena.append(tokeni[i].lower())
                i += 1
            vrednosti = []
            while i < len(tokeni) and not tokeni[i].startswith('_') and tokeni[i].lower() not in ('loop_', 'stop_') \
                    and not tokeni[i].lower().startswith('data_'):
                vrednosti.append(tokeni[i])
                i += 1
            if imena and len(vrednosti) % len(imena) != 0:
                raise CifGreska(f'петља {imena[0]}: {len(vrednosti)} вредности није дељиво са {len(imena)} колона')
            petlje.append({ime: vrednosti[k::len(imena)] for k, ime in enumerate(imena)})
        elif t.startswith('_'):
            if i + 1 >= len(tokeni):
                raise CifGreska(f'ознака {t} без вредности')
            tagovi[t.lower()] = tokeni[i + 1]
            i += 2
        else:
            i += 1
    return {'tagovi': tagovi, 'petlje': petlje}


def petlja_sa(cif, ime):
    for petlja in cif['petlje']:
        if ime in petlja:
            return petlja
    return None


def broj(vrednost):
    """'0.3331(2)' → 0.3331; '?'/'.' → None."""
    if vrednost is None:
        return None
    v = _NESIGURNOST.sub('', str(vrednost)).strip()
    if v in ('', '?', '.'):
        return None
    return float(v)


def element_atoma(oznaka, tip=None):
    """Хемијски симбол из ``_atom_site_type_symbol`` ('Fe2+') или из ознаке
    ('Si1', 'O-H6' → O, 'Wat' → O по AMCSD договору)."""
    for kandidat in (tip, oznaka):
        if not kandidat:
            continue
        m = _ELEMENT_IZ_OZNAKE.match(str(kandidat).strip())
        if not m:
            continue
        slova = m.group(1)
        if slova.lower().startswith('wat'):
            return 'O'
        for duzina in (2, 1):
            simbol = slova[:duzina].capitalize()
            if simbol in ELEMENTI:
                return simbol
    raise CifGreska(f'непознат елемент за атом {oznaka!r} ({tip!r})')


def celija_iz(cif):
    t = cif['tagovi']
    try:
        return {k: broj(t['_cell_length_' + k]) for k in 'abc'} | \
               {k: broj(t.get('_cell_angle_' + k, '90')) for k in ('alpha', 'beta', 'gamma')}
    except KeyError as exc:
        raise CifGreska(f'нема {exc.args[0]}') from None


def zapremina(celija):
    ca, cb, cg = (math.cos(math.radians(celija[k])) for k in ('alpha', 'beta', 'gamma'))
    koren = max(0.0, 1 - ca * ca - cb * cb - cg * cg + 2 * ca * cb * cg)
    return celija['a'] * celija['b'] * celija['c'] * math.sqrt(koren)


def atomi_iz(cif):
    """Асиметрична јединица: [{oznaka, element, x, y, z, zauzetost, u_iso}]."""
    petlja = petlja_sa(cif, '_atom_site_fract_x')
    if petlja is None:
        raise CifGreska('нема петље _atom_site_fract_x')
    n = len(petlja['_atom_site_fract_x'])
    oznake = petlja.get('_atom_site_label', [f'A{i + 1}' for i in range(n)])
    tipovi = petlja.get('_atom_site_type_symbol', [None] * n)
    zauzetosti = petlja.get('_atom_site_occupancy', ['1'] * n)
    u_iso = petlja.get('_atom_site_u_iso_or_equiv')
    b_iso = petlja.get('_atom_site_b_iso_or_equiv')
    atomi = []
    for i in range(n):
        x, y, z = (broj(petlja['_atom_site_fract_' + k][i]) for k in 'xyz')
        if None in (x, y, z):
            continue
        u = broj(u_iso[i]) if u_iso else None
        if u is None and b_iso:
            b = broj(b_iso[i])
            u = b / (8 * math.pi ** 2) if b else None
        atomi.append({'oznaka': oznake[i], 'element': element_atoma(oznake[i], tipovi[i]), 'x': x, 'y': y, 'z': z,
                      'zauzetost': broj(zauzetosti[i]) if broj(zauzetosti[i]) is not None else 1.0,
                      'u_iso': u if u is not None else 0.01})
    if not atomi:
        raise CifGreska('нема положаја атома')
    return atomi


def operatori_iz(cif):
    for ime in TAGOVI_OPERATORA:
        petlja = petlja_sa(cif, ime)
        if petlja:
            return [parsiraj_operator(op) for op in petlja[ime]]
        if ime in cif['tagovi']:
            return [parsiraj_operator(cif['tagovi'][ime])]
    t = cif['tagovi']
    grupa = t.get('_symmetry_space_group_name_h-m') or t.get('_space_group_name_h-m_alt') or ''
    if grupa.replace(' ', '') == 'P1':
        return [parsiraj_operator('x,y,z')]
    raise CifGreska('нема симетријских оператора у CIF-у')


def formula_iz(cif):
    """'Mg2 O4 Si' → {'Mg': 2.0, 'O': 4.0, 'Si': 1.0}; Z из _cell_formula_units_Z."""
    t = cif['tagovi']
    formula = {}
    for simbol, kolicina in _FORMULA_CLAN.findall(t.get('_chemical_formula_sum', '')):
        if simbol in ELEMENTI:
            formula[simbol] = formula.get(simbol, 0.0) + (float(kolicina) if kolicina else 1.0)
    z = broj(t.get('_cell_formula_units_z'))
    return formula, (int(round(z)) if z else None)


def citat_iz(cif):
    t = cif['tagovi']
    petlja = petlja_sa(cif, '_publ_author_name')
    autori = petlja['_publ_author_name'] if petlja else ([t['_publ_author_name']] if '_publ_author_name' in t else [])
    naslov = ' '.join((t.get('_publ_section_title') or '').split())
    return {
        'autori': [' '.join(a.split()) for a in autori],
        'godina': int(broj(t.get('_journal_year')) or 0) or None,
        'casopis': t.get('_journal_name_full'),
        'tom': t.get('_journal_volume'),
        'strane': '–'.join(s for s in (t.get('_journal_page_first'), t.get('_journal_page_last')) if s),
        'doi': t.get('_journal_paper_doi'),
        'naslov': naslov or None,
        'amcsd': t.get('_database_code_amcsd'),
    }


def uslovi_iz(cif):
    t = cif['tagovi']
    return {
        'temperatura_k': broj(t.get('_diffrn_ambient_temperature') or t.get('_cell_measurement_temperature')),
        'pritisak_kpa': broj(t.get('_diffrn_ambient_pressure') or t.get('_cell_measurement_pressure')),
    }


# --------------------------------------------------------------------------
# Симетрија
# --------------------------------------------------------------------------

def parsiraj_operator(op):
    """'x,-y+1/2,z' → 3 торке (cx, cy, cz, konstanta) као Fraction."""
    delovi = str(op).replace(' ', '').lower().split(',')
    if len(delovi) != 3:
        raise CifGreska(f'оператор {op!r} нема три компоненте')
    izlaz = []
    for deo in delovi:
        koef = {'x': Fraction(0), 'y': Fraction(0), 'z': Fraction(0)}
        konst = Fraction(0)
        clanovi = re.findall(r'[+-]?[^+-]+', deo)
        if not clanovi or ''.join(clanovi) != deo:
            raise CifGreska(f'оператор {op!r}: неразумљива компонента {deo!r}')
        for clan in clanovi:
            m = _CLAN.match(clan)
            if not m or not (m.group(2) or m.group(3)):
                raise CifGreska(f'оператор {op!r}: неразумљив члан {clan!r}')
            znak = -1 if m.group(1) == '-' else 1
            kolicina = Fraction(m.group(2)) if m.group(2) else Fraction(1)
            if m.group(3):
                koef[m.group(3)] += znak * kolicina
            else:
                konst += znak * kolicina
        izlaz.append((koef['x'], koef['y'], koef['z'], konst))
    return tuple(izlaz)


def primeni_operator(operator, x, y, z):
    return tuple(float(cx * x + cy * y + cz * z + k) for cx, cy, cz, k in
                 ((float(a), float(b), float(c), float(d)) for a, b, c, d in operator))


def u_celiju(v):
    v = v % 1.0
    return 0.0 if v < TOLERANCIJA or v > 1.0 - TOLERANCIJA else v


def isto_mesto(p, q):
    return all(min(abs(p[i] - q[i]), 1.0 - abs(p[i] - q[i])) < TOLERANCIJA for i in range(3))


def prosiri_u_p1(atomi, operatori):
    """Сви положаји у ћелији; на истом месту остаје први (већа заузетост прва)."""
    izlaz = []
    for atom in sorted(atomi, key=lambda a: -a['zauzetost']):
        for operator in operatori:
            polozaj = tuple(u_celiju(v) for v in primeni_operator(operator, atom['x'], atom['y'], atom['z']))
            if any(isto_mesto(polozaj, (p['x'], p['y'], p['z'])) for p in izlaz):
                continue
            izlaz.append(dict(atom, x=polozaj[0], y=polozaj[1], z=polozaj[2]))
    return izlaz


def proveri_broj_atoma(formula, z, atomi_p1):
    """Грешка ако број положаја не одговара Z × формули (без елемената којих
    нема међу положајима, нпр. H). По елементу само кад су заузетости пуне."""
    if not formula or not z:
        raise CifGreska('нема формуле или Z за проверу броја атома')
    prisutni = {a['element'] for a in atomi_p1}
    ocekivano = {el: z * n for el, n in formula.items() if el in prisutni}
    ukupno = int(round(sum(ocekivano.values())))
    if len(atomi_p1) != ukupno:
        raise CifGreska(f'број атома у P1 је {len(atomi_p1)}, а Z × формула даје {ukupno}')
    pune_zauzetosti = all(abs(a['zauzetost'] - 1.0) < 1e-6 for a in atomi_p1)
    if pune_zauzetosti and all(abs(n - round(n)) < 1e-6 for n in formula.values()):
        for el, n in ocekivano.items():
            stvarno = sum(1 for a in atomi_p1 if a['element'] == el)
            if stvarno != int(round(n)):
                raise CifGreska(f'{el}: {stvarno} положаја у P1, а Z × формула даје {int(round(n))}')
    return ukupno


# --------------------------------------------------------------------------
# Излаз — исти облик као local_rruff_data.generate_cif_from_dif(expand_unitcell=True)
# --------------------------------------------------------------------------

def cif_p1(ime, celija, atomi_p1):
    linije = [
        f"data_{ime.replace(' ', '_')}",
        '',
        '# Cell parameters',
        f"_cell_length_a {celija['a']:.4f}",
        f"_cell_length_b {celija['b']:.4f}",
        f"_cell_length_c {celija['c']:.4f}",
        f"_cell_angle_alpha {celija['alpha']:.2f}",
        f"_cell_angle_beta {celija['beta']:.2f}",
        f"_cell_angle_gamma {celija['gamma']:.2f}",
        f'_cell_volume {zapremina(celija):.2f}',
        '',
        '# Symmetry',
        "_symmetry_space_group_name_H-M 'P 1'",
        '_symmetry_Int_Tables_number 1',
        '',
        'loop_',
        '_atom_site_label',
        '_atom_site_type_symbol',
        '_atom_site_fract_x',
        '_atom_site_fract_y',
        '_atom_site_fract_z',
        '_atom_site_occupancy',
        '_atom_site_U_iso_or_equiv',
    ]
    for i, a in enumerate(atomi_p1):
        linije.append(f"{a['element']}{i + 1} {a['element']} {a['x']:.5f} {a['y']:.5f} {a['z']:.5f} "
                      f"{a['zauzetost']:.3f} {a['u_iso']:.4f}")
    return '\n'.join(linije)


def struktura_p1(tekst_cif, ime):
    """CIF текст → (cif_p1, подаци) са провером броја атома."""
    cif = parsiraj_cif(tekst_cif)
    celija = celija_iz(cif)
    atomi = prosiri_u_p1(atomi_iz(cif), operatori_iz(cif))
    formula, z = formula_iz(cif)
    broj_atoma = proveri_broj_atoma(formula, z, atomi)
    return cif_p1(ime, celija, atomi), {
        'celija': celija, 'formula': formula, 'z': z, 'broj_atoma': broj_atoma,
        'prostorna_grupa': cif['tagovi'].get('_symmetry_space_group_name_h-m'),
        'citat': citat_iz(cif), 'uslovi': uslovi_iz(cif),
    }
