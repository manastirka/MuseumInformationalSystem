"""Правна верификација у Архиви — прекидач и заставица из шаблона.

Пре ове измене корак после потписа подносиоца био је ЖИЧАНО
`pending_legal_verification`, па `requires_legal_verification` из
`signature_templates` није значио ништа — приказивао се у подешавањима, а
ток је ишао мимо њега. Тестови испод чувају и прекидач и заставицу.
"""
from unittest import mock

import pytest

import odobravanje_prekidac as prekidac


@pytest.fixture(autouse=True)
def _bez_env(monkeypatch):
    for ime in (prekidac.ENV_IZVESTAJI, prekidac.ENV_DOKUMENTI,
                prekidac.ENV_ROK, prekidac.ENV_VERIFIKACIJA):
        monkeypatch.delenv(ime, raising=False)


def _sa(vrednosti):
    lazni = mock.MagicMock()
    lazni.load_saved_settings.return_value = vrednosti
    return mock.patch.dict('sys.modules', {'admin_system_views': lazni})


# --- сам прекидач -----------------------------------------------------------

def test_podrazumevano_je_verifikacija_ukljucena():
    with _sa({}):
        assert prekidac.verifikacija_arhive_ukljucena() is True


def test_izricito_iskljucena_ne_dira_ostale():
    with _sa({prekidac.KLJUC_VERIFIKACIJA: False}):
        assert prekidac.verifikacija_arhive_ukljucena() is False
        assert prekidac.odobravanje_izvestaja_ukljuceno() is True
        assert prekidac.rok_predaje_ukljucen() is True


def test_pad_baze_ne_gasi_verifikaciju():
    lazni = mock.MagicMock()
    lazni.load_saved_settings.side_effect = RuntimeError('baza pala')
    with mock.patch.dict('sys.modules', {'admin_system_views': lazni}):
        assert prekidac.verifikacija_arhive_ukljucena() is True


def test_env_preklapa(monkeypatch):
    monkeypatch.setenv(prekidac.ENV_VERIFIKACIJA, '0')
    with _sa({prekidac.KLJUC_VERIFIKACIJA: True}):
        assert prekidac.verifikacija_arhive_ukljucena() is False


def test_stanje_nosi_sva_cetiri():
    with _sa({}):
        s = prekidac.stanje()
    for k in (prekidac.KLJUC_IZVESTAJI, prekidac.KLJUC_DOKUMENTI,
              prekidac.KLJUC_ROK, prekidac.KLJUC_VERIFIKACIJA):
        assert k in s, k
    assert prekidac.ENV_VERIFIKACIJA in s['env_preklop']


# --- рачунање следећег статуса ---------------------------------------------
# Логика живи у `archive_signature_blueprint`, унутар руте иза базе. Овде се
# проверава сама одлука, издвојена истим редоследом услова — да се правило
# може доказати без дизања целог тока потписивања.

def _sledeci_status(trazi_verifikaciju, trazi_odobrenje, prekidac_ukljucen):
    if trazi_verifikaciju and not prekidac_ukljucen:
        trazi_verifikaciju = False
    if trazi_verifikaciju:
        return 'pending_legal_verification'
    if trazi_odobrenje:
        return 'pending_approval'
    return 'verified'


def test_ukljucena_verifikacija_zadrzava_stari_tok():
    assert _sledeci_status(True, True, True) == 'pending_legal_verification'


def test_iskljucena_verifikacija_preskace_pravnu_sluzbu():
    assert _sledeci_status(True, True, False) == 'pending_approval'


def test_iskljucena_verifikacija_ne_proglasava_verifikovanim():
    """Кад одобравач ипак треба, документ иде њему — не у 'verified'."""
    assert _sledeci_status(True, True, False) != 'verified'


def test_bez_verifikacije_i_bez_odobravaca_je_verified():
    assert _sledeci_status(False, False, True) == 'verified'


def test_sablon_bez_verifikacije_se_postuje_i_kad_je_prekidac_ukljucen():
    """Заставица из шаблона важи сама за себе — то је оно што раније није
    радило: ток је ишао на правну службу без обзира на њу."""
    assert _sledeci_status(False, True, True) == 'pending_approval'


def test_nepoznat_tip_dokumenta_ide_najstrozim_putem():
    """Ако шаблона нема, кôд узима (True, True) — не најлакши пут."""
    assert _sledeci_status(True, True, True) == 'pending_legal_verification'
