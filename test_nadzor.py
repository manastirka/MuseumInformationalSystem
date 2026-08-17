"""Провера надзора продукције — доказ да налази стварно настају.

Надзор чија провера никад не пада не разликује се од непостојећег надзора.
Зато сваки случај овде поставља конкретан квар и тражи ТАЧАН налаз.
"""
import importlib.util
import time
from pathlib import Path

import pytest

PUT = Path(__file__).parent / 'scripts' / 'nadzor' / 'provera_proda.py'


@pytest.fixture()
def nadzor(tmp_path, monkeypatch):
    spec = importlib.util.spec_from_file_location('provera_proda', PUT)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    # Модул иначе пише у ~/nadzor; у тесту не сме да дира прави дом.
    monkeypatch.setattr(m, 'KOREN', tmp_path)
    monkeypatch.setattr(m, 'STANJE', tmp_path / 'stanje.json')
    return m


def _odeljci(**preklopi):
    sada = int(time.time())
    osnovno = {
        'VREME': [str(sada)],
        'BEKAP': [f'{sada - 3600} /backup/current/db/mis_db-danas.sql.gz'],
        'PALE': [
            'mis.service active',
            'nginx.service active',
            'backup-nhmb.timer active',
        ],
        'MARKERI': [],
        'DISK': ['/           16%', '/backup      1%'],
        'ZDRAVLJE': ['{"db":"ok","redis":"ok","status":"ok"}'],
        'PROBA': [time.strftime('%a %Y-%m-%d %H:%M:%S CEST',
                                time.localtime(sada - 5 * 86400))],
    }
    osnovno.update(preklopi)
    return osnovno


def test_zdravo_stanje_nema_nalaza(nadzor):
    nalazi, u_redu = nadzor.procena(_odeljci())
    assert nalazi == [], nalazi
    assert len(u_redu) >= 6


def test_zastareo_bekap_je_nalaz(nadzor):
    sada = int(time.time())
    nalazi, _ = nadzor.procena(_odeljci(
        BEKAP=[f'{sada - 40 * 3600} /backup/current/db/mis_db-prekjuce.sql.gz']))
    assert any('БЕКАП' in n and '40 h' in n for n in nalazi), nalazi


def test_bekapa_uopste_nema(nadzor):
    nalazi, _ = nadzor.procena(_odeljci(BEKAP=[]))
    assert any('нема ниједног дампа' in n for n in nalazi), nalazi


def test_pala_jedinica_je_nalaz(nadzor):
    nalazi, _ = nadzor.procena(_odeljci(PALE=[
        'mis.service active',
        'backup-nhmb.service failed',
    ]))
    assert any('ПАЛЕ ЈЕДИНИЦЕ' in n and 'backup-nhmb.service' in n
               for n in nalazi), nalazi


def test_nov_alarmni_marker_je_nalaz_pa_utihne(nadzor):
    """Маркер се пријављује једном; други пут је већ виђен.

    Ово је поента маркера: хвата пад који је у међувремену ручно поправљен,
    па га `systemctl is-failed` више не показује.
    """
    o = _odeljci(MARKERI=['/var/lib/mis/alarm/2026-08-17T023001-backup-nhmb.service.txt'])
    nalazi, _ = nadzor.procena(o)
    assert any('НОВИ АЛАРМИ' in n for n in nalazi), nalazi
    nalazi2, u_redu2 = nadzor.procena(o)
    assert nalazi2 == [], nalazi2
    assert any('ниједан нов' in u for u in u_redu2), u_redu2


def test_pun_disk_je_nalaz(nadzor):
    nalazi, _ = nadzor.procena(_odeljci(DISK=['/           93%', '/backup      1%']))
    assert any('ДИСК /' in n and '93' in n for n in nalazi), nalazi


def test_aplikacija_ne_odgovara(nadzor):
    nalazi, _ = nadzor.procena(_odeljci(ZDRAVLJE=['NEDOSTUPNO']))
    assert any('ЗДРАВЉЕ' in n for n in nalazi), nalazi


def test_baza_pala_a_http_radi(nadzor):
    """healthz врати 200 са status:degraded — сервер живи, база не."""
    nalazi, _ = nadzor.procena(_odeljci(
        ZDRAVLJE=['{"db":"fail","redis":"ok","status":"degraded"}']))
    assert any('ЗДРАВЉЕ' in n for n in nalazi), nalazi


def test_zaboravljena_proba_vracanja(nadzor):
    sada = int(time.time())
    nalazi, _ = nadzor.procena(_odeljci(
        PROBA=[time.strftime('%a %Y-%m-%d %H:%M:%S CEST',
                             time.localtime(sada - 90 * 86400))]))
    assert any('ПРОБА ВРАЋАЊА' in n and '90' in n for n in nalazi), nalazi


def test_nedostupan_prod_je_greska_a_ne_tiho_ok(nadzor):
    """ssh који не прође мора да буде видљив налаз, не празан извештај."""
    tekst = nadzor.izvestaj('prod-nadzor', [], [], 'RuntimeError: ssh пао')
    assert 'ПРОВЕРА НИЈЕ ПРОШЛА' in tekst
    assert 'ssh пао' in tekst


def test_kolektor_na_produ_ne_menja_stanje():
    """Сакупљач сме САМО да чита — ниједна наредба која мења прод."""
    izvor = (Path(__file__).parent / 'deploy' / 'nadzor-podaci.sh').read_text(
        encoding='utf-8')
    tela = [r for r in izvor.splitlines()
            if r.strip() and not r.lstrip().startswith('#')]
    zabranjeno = ('rm ', 'mv ', 'systemctl start', 'systemctl stop',
                  'systemctl restart', 'psql', 'dropdb', 'chmod', 'chown',
                  '> /', '>> /')
    for red in tela:
        for z in zabranjeno:
            assert z not in red, f'сакупљач мења стање: {red!r}'
