"""Разрешавање затеченог кад се одобравање угаси.

Овде се доказују две ствари које се лако тихо покваре:
  1. dry-run СТВАРНО не мења ништа (иначе је „провера пре" бесмислена);
  2. свака промена статуса добије ред у историји — колико редова, толико
     трагова, из исте трансакције.
"""
from unittest import mock

import pytest

import odobravanje_razresavanje as razresavanje


class LazniKursor:
    def __init__(self, odgovori=None):
        self.izvrseno = []
        self._odgovori = list(odgovori or [])
        self.executemany_pozivi = []

    def execute(self, sql, params=None):
        self.izvrseno.append((sql, params))

    def executemany(self, sql, seq):
        self.executemany_pozivi.append((sql, list(seq)))

    def fetchall(self):
        return self._odgovori.pop(0) if self._odgovori else []

    def fetchone(self):
        v = self._odgovori.pop(0) if self._odgovori else None
        return v

    def __enter__(self):
        return self

    def __exit__(self, *a):
        return False


class LaznaVeza:
    def __init__(self, kursor):
        self._kursor = kursor
        self.commit_pozvan = 0

    def cursor(self, **kw):
        return self._kursor

    def commit(self):
        self.commit_pozvan += 1

    def __enter__(self):
        return self

    def __exit__(self, *a):
        return False


def _veza(kursor):
    return mock.patch.object(razresavanje, 'get_postgres_connection',
                             lambda *a, **k: LaznaVeza(kursor))


def _upisi(kursor):
    return [(s, p) for s, p in kursor.izvrseno if s.strip().upper().startswith('UPDATE')]


def test_dry_run_izvestaja_ne_menja_nista():
    k = LazniKursor([[(11,), (12,), (13,)]])
    with _veza(k):
        r = razresavanje.razresi_izvestaje('proba', izvrsi=False)
    assert r == {'pronadjeno': 3, 'promenjeno': 0, 'izvrseno': False}
    assert _upisi(k) == [], 'dry-run не сме да упише ништа'
    assert k.executemany_pozivi == []


def test_izvrsenje_menja_i_ostavlja_trag():
    k = LazniKursor([[(11,), (12,)]])
    k.rowcount = 2
    with _veza(k):
        r = razresavanje.razresi_izvestaje('aca@nhmbeo.rs', izvrsi=True)
    assert r['pronadjeno'] == 2
    upisi = _upisi(k)
    assert len(upisi) == 1
    sql, params = upisi[0]
    assert params[0] == 'BEZ_ODOBRENJA'
    # Само поднете. Враћене (REJECTED) су код запосленог, нацрти нису поднети.
    assert "status = 'SUBMITTED'" in sql
    assert 'REJECTED' not in sql and 'DRAFT' not in sql

    assert len(k.executemany_pozivi) == 1, 'историја мора да се упише'
    _, redovi = k.executemany_pozivi[0]
    assert len(redovi) == 2, 'колико измењених, толико редова историје'
    assert all(red[1] == 'BEZ_ODOBRENJA' for red in redovi)
    assert all(red[2] == 'aca@nhmbeo.rs' for red in redovi)
    assert all('одобравање искључено' in red[3].lower() for red in redovi)


def test_nema_zatecenih_nema_upisa():
    k = LazniKursor([[]])
    with _veza(k):
        r = razresavanje.razresi_izvestaje('proba', izvrsi=True)
    assert r['promenjeno'] == 0
    assert _upisi(k) == []


def test_dokumenti_dry_run_ne_dira():
    k = LazniKursor([[(5, 1), (9, 2)], (4,)])
    with _veza(k):
        r = razresavanje.razresi_dokumente('proba', izvrsi=False)
    assert r['dokumenata'] == 2
    assert r['verzija_na_cekanju'] == 4
    assert r['promenjeno'] == 0
    assert _upisi(k) == []


def test_dokumenti_najnovija_vazi_ostalo_u_arhivu():
    k = LazniKursor([[(5, 1), (9, 2)], (4,)])
    k.rowcount = 2
    with _veza(k):
        razresavanje.razresi_dokumente('aca@nhmbeo.rs', izvrsi=True)

    upisi = _upisi(k)
    assert len(upisi) == 2, 'прво архивирање старих, па додела важења'

    arhiva_sql, arhiva_params = upisi[0]
    assert "SET status = 'arhivirano'" in arhiva_sql
    assert arhiva_params[0] == [1, 2], 'само документи којих се тиче'
    assert arhiva_params[1] == [5, 9], 'изабране верзије се НЕ архивирају'
    # Претходно важеће И остале на чекању — да важећа остане тачно једна.
    assert set(arhiva_params[2]) == {'odobreno', 'bez_odobrenja', 'na_odobrenju'}

    vazi_sql, vazi_params = upisi[1]
    assert vazi_params[0] == 'bez_odobrenja'
    assert vazi_params[1] == [5, 9]
    assert "'odobreno'" not in vazi_sql, 'без рецензента нема статуса одобрене'

    assert len(k.executemany_pozivi) == 1
    _, redovi = k.executemany_pozivi[0]
    assert len(redovi) == 2
    assert all(red[2] == 'aca@nhmbeo.rs' for red in redovi)


def test_prebroj_ne_menja_nista():
    k = LazniKursor([(7,), (3,)])
    with _veza(k):
        z = razresavanje.prebroj_zatecene()
    assert z == {'izvestaji': 7, 'dokumenti': 3}
    assert _upisi(k) == []


@pytest.mark.parametrize('funkcija', [
    razresavanje.razresi_izvestaje,
    razresavanje.razresi_dokumente,
])
def test_podrazumevano_je_dry_run(funkcija):
    """Позив без `izvrsi` не сме да мења базу — ако се то икад преокрене,
    свака дијагностичка провера постаје деструктивна."""
    k = LazniKursor([[], (0,)])
    with _veza(k):
        r = funkcija('proba')
    assert r['izvrseno'] is False
    assert _upisi(k) == []
