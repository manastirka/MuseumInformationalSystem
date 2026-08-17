"""Прекидачи одобравања — понашање мора да буде досадно предвидиво.

Прекидач који се сам угаси због грешке горе је од непостојећег: контрола
нестане, а нико не примети. Зато сваки нејасан случај овде мора да заврши у
УКЉУЧЕНО, и то се овде доказује.
"""
import os
from unittest import mock

import pytest

import odobravanje_prekidac as prekidac


@pytest.fixture(autouse=True)
def _bez_env(monkeypatch):
    monkeypatch.delenv(prekidac.ENV_IZVESTAJI, raising=False)
    monkeypatch.delenv(prekidac.ENV_DOKUMENTI, raising=False)


def _sa_podesavanjima(vrednosti):
    """Подметни system_settings без дизања целе апликације."""
    lazni = mock.MagicMock()
    lazni.load_saved_settings.return_value = vrednosti
    return mock.patch.dict('sys.modules', {'admin_system_views': lazni})


def test_bez_podesavanja_je_ukljuceno():
    with _sa_podesavanjima({}):
        assert prekidac.odobravanje_izvestaja_ukljuceno() is True
        assert prekidac.odobravanje_dokumenata_ukljuceno() is True


def test_izricito_iskljuceno():
    with _sa_podesavanjima({prekidac.KLJUC_IZVESTAJI: False}):
        assert prekidac.odobravanje_izvestaja_ukljuceno() is False
        # Други ток се НЕ гаси успут — два прекидача, две одлуке.
        assert prekidac.odobravanje_dokumenata_ukljuceno() is True


@pytest.mark.parametrize('vrednost,ocekivano', [
    (True, True), (False, False),
    ('da', True), ('ne', False),
    ('1', True), ('0', False),
    ('true', True), ('off', False),
])
def test_razumljive_vrednosti(vrednost, ocekivano):
    with _sa_podesavanjima({prekidac.KLJUC_DOKUMENTI: vrednost}):
        assert prekidac.odobravanje_dokumenata_ukljuceno() is ocekivano


@pytest.mark.parametrize('smece', ['mozda', '', 'da/ne', 3, [], {'a': 1}])
def test_besmislena_vrednost_ne_gasi_kontrolu(smece):
    with _sa_podesavanjima({prekidac.KLJUC_IZVESTAJI: smece}):
        assert prekidac.odobravanje_izvestaja_ukljuceno() is True


def test_pad_baze_ne_gasi_kontrolu():
    """Ако подешавања не могу да се прочитају, остаје како је било."""
    lazni = mock.MagicMock()
    lazni.load_saved_settings.side_effect = RuntimeError('baza pala')
    with mock.patch.dict('sys.modules', {'admin_system_views': lazni}):
        assert prekidac.odobravanje_izvestaja_ukljuceno() is True
        assert prekidac.odobravanje_dokumenata_ukljuceno() is True


def test_okruzenje_preklapa_podesavanja(monkeypatch):
    """Излаз у нужди: кад админ страница не ради, env има последњу реч."""
    monkeypatch.setenv(prekidac.ENV_IZVESTAJI, '0')
    with _sa_podesavanjima({prekidac.KLJUC_IZVESTAJI: True}):
        assert prekidac.odobravanje_izvestaja_ukljuceno() is False

    monkeypatch.setenv(prekidac.ENV_IZVESTAJI, '1')
    with _sa_podesavanjima({prekidac.KLJUC_IZVESTAJI: False}):
        assert prekidac.odobravanje_izvestaja_ukljuceno() is True


def test_besmislen_env_se_zanemaruje_a_ne_tumaci(monkeypatch):
    monkeypatch.setenv(prekidac.ENV_DOKUMENTI, 'mozda')
    with _sa_podesavanjima({prekidac.KLJUC_DOKUMENTI: False}):
        # Пада назад на подешавања, не измишља вредност.
        assert prekidac.odobravanje_dokumenata_ukljuceno() is False


def test_stanje_prikazuje_i_env_preklop(monkeypatch):
    monkeypatch.setenv(prekidac.ENV_DOKUMENTI, 'ne')
    with _sa_podesavanjima({prekidac.KLJUC_IZVESTAJI: False}):
        s = prekidac.stanje()
    assert s[prekidac.KLJUC_IZVESTAJI] is False
    assert s[prekidac.KLJUC_DOKUMENTI] is False
    assert s['env_preklop'][prekidac.ENV_DOKUMENTI] is False
    assert s['env_preklop'][prekidac.ENV_IZVESTAJI] is None


def test_bez_odobrenja_nije_odobreno():
    """Најважнија тврдња: нова стања се НЕ преклапају са одобреним.

    Ако неко икад дода 'BEZ_ODOBRENJA' у листу одобрених да би „радила
    статистика", овај тест пада.
    """
    assert prekidac.STATUS_IZVESTAJ_BEZ != 'APPROVED'
    assert prekidac.STATUS_DOKUMENT_BEZ != 'odobreno'
    assert 'APPROVED' in prekidac.IZVESTAJ_ZAVRSEN
    assert prekidac.STATUS_IZVESTAJ_BEZ in prekidac.IZVESTAJ_ZAVRSEN
    assert 'SUBMITTED' in prekidac.IZVESTAJ_NEIZMENJIV
    assert set(prekidac.IZVESTAJ_ZAVRSEN) <= set(prekidac.IZVESTAJ_NEIZMENJIV)
    assert prekidac.STATUS_DOKUMENT_BEZ in prekidac.DOKUMENT_VAZECI
    assert 'odobreno' in prekidac.DOKUMENT_VAZECI


def test_podrazumevano_bez_ijednog_podesavanja_i_bez_baze():
    """Гола инсталација: ништа подешено, апликација се тек диже."""
    if 'admin_system_views' in os.environ:  # никад — само да linter ћути
        return
    with _sa_podesavanjima(None):
        assert prekidac.odobravanje_izvestaja_ukljuceno() is True
