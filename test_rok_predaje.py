"""Рок предаје радних листа — и кад важи, и кад је угашен.

Прекидач гаси РОК, не и здрав разум: месец који још није почео остаје
немогућ. Ако то икад испадне, овај тест пада.
"""
from datetime import datetime
from unittest import mock

import pytest

import odobravanje_prekidac
import timesheet_postgres as tp


def _sada(godina, mesec, dan):
    """Замрзни „данас" — иначе би тест зависио од датума покретања."""
    lazni = mock.MagicMock(wraps=datetime)
    lazni.now.return_value = datetime(godina, mesec, dan, 12, 0, 0)
    return mock.patch.object(tp, 'datetime', lazni)


def _rok(ukljucen):
    return mock.patch.object(odobravanje_prekidac, 'rok_predaje_ukljucen',
                             lambda: ukljucen)


# --- рок УКЉУЧЕН: понашање остаје као раније --------------------------------

@pytest.mark.parametrize('dan,ocekivano', [(1, True), (10, True), (11, False), (28, False)])
def test_ukljucen_rok_pusta_samo_do_desetog(dan, ocekivano):
    with _rok(True), _sada(2026, 8, dan):
        moze, poruka = tp.can_submit_for_review(7, 2026)
    assert moze is ocekivano
    if not ocekivano:
        assert 'до 10.' in poruka


def test_ukljucen_rok_pusta_tekuci_mesec_uvek():
    with _rok(True), _sada(2026, 8, 28):
        assert tp.can_submit_for_review(8, 2026)[0] is True


def test_ukljucen_rok_decembar_prelazi_u_januar():
    with _rok(True), _sada(2027, 1, 5):
        assert tp.can_submit_for_review(12, 2026)[0] is True


# --- рок УГАШЕН -------------------------------------------------------------

@pytest.mark.parametrize('dan', [1, 10, 11, 28])
def test_ugasen_rok_pusta_prosli_mesec_bilo_kog_dana(dan):
    with _rok(False), _sada(2026, 8, dan):
        assert tp.can_submit_for_review(7, 2026)[0] is True


def test_ugasen_rok_pusta_i_davno_prosle_mesece():
    """Поента гашења: заостали извештај из марта може да се преда у августу."""
    with _rok(False), _sada(2026, 8, 28):
        assert tp.can_submit_for_review(3, 2026)[0] is True
        assert tp.can_submit_for_review(11, 2025)[0] is True


def test_ugasen_rok_pusta_tekuci_mesec():
    with _rok(False), _sada(2026, 8, 28):
        assert tp.can_submit_for_review(8, 2026)[0] is True


@pytest.mark.parametrize('mesec,godina', [(9, 2026), (12, 2026), (1, 2027)])
def test_ugasen_rok_NE_otvara_buducnost(mesec, godina):
    """Најважнија тврдња: без рока се и даље не пријављује рад који се
    није десио. Ако ово икад прође, запослени може да поднесе лист за
    децембар у августу."""
    with _rok(False), _sada(2026, 8, 28):
        moze, poruka = tp.can_submit_for_review(mesec, godina)
    assert moze is False
    assert 'није почео' in poruka


# --- измена прати подношење -------------------------------------------------

@pytest.mark.parametrize('status', ['DRAFT', 'REJECTED'])
def test_ugasen_rok_dozvoljava_i_izmenu_proslog_meseca(status):
    """Ако сме да се поднесе, мора и да се измени — иначе је недоследно."""
    with _rok(False), _sada(2026, 8, 28):
        assert tp.can_edit_timesheet_by_status(7, 2026, status)[0] is True


def test_ugasen_rok_ne_otvara_izmenu_buduceg_meseca():
    with _rok(False), _sada(2026, 8, 28):
        moze, poruka = tp.can_edit_timesheet_by_status(9, 2026, 'DRAFT')
    assert moze is False
    assert 'није почео' in poruka


@pytest.mark.parametrize('status', ['SUBMITTED', 'APPROVED', 'BEZ_ODOBRENJA'])
def test_zavrsena_lista_se_ne_menja_ni_bez_roka(status):
    """Гашење рока НЕ отвара већ предате листе — то је друга ограда."""
    with _rok(False), _sada(2026, 8, 28):
        moze, poruka = tp.can_edit_timesheet_by_status(7, 2026, status)
    assert moze is False
    assert 'поднета' in poruka or 'одобрена' in poruka


def test_ukljucen_rok_blokira_izmenu_posle_desetog():
    with _rok(True), _sada(2026, 8, 28):
        assert tp.can_edit_timesheet_by_status(7, 2026, 'DRAFT')[0] is False


def test_podrazumevano_je_rok_ukljucen():
    """Без подешавања правило остаје као што је било."""
    lazni = mock.MagicMock()
    lazni.load_saved_settings.return_value = {}
    with mock.patch.dict('sys.modules', {'admin_system_views': lazni}):
        assert odobravanje_prekidac.rok_predaje_ukljucen() is True
