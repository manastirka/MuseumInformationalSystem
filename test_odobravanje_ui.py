"""Картица прекидача у админ панелу — да приказ никад не тврди више него што зна."""
import os

os.environ.setdefault('FLASK_ENV', 'testing')
os.environ.setdefault('SECRET_KEY', 'test-secret')

import pytest
from jinja2 import Environment, FileSystemLoader, select_autoescape

SABLON = 'admin_system_settings.html'


@pytest.fixture(scope='module')
def kartica():
    env = Environment(loader=FileSystemLoader('templates'),
                      autoescape=select_autoescape(['html']))
    izvor = env.loader.get_source(env, SABLON)[0]
    env.parse(izvor)  # цео шаблон мора да се парсира
    pocetak = izvor.index('<!-- Одобравање -->')
    kraj = izvor.index('<!-- Main Settings Sections -->')
    return env.from_string(izvor[pocetak:kraj])


def _stanje(**preklopi):
    s = {
        'odobravanje_izvestaja': True,
        'odobravanje_dokumenata': False,
        'odobravanje_izvestaja_rok': True,
        'rok_predaje_izvestaja': True,
        'env_preklop': {'MIS_ODOBRAVANJE_IZVESTAJA': None,
                        'MIS_ODOBRAVANJE_DOKUMENATA': None,
                        'MIS_ROK_PREDAJE': None},
        'zateceno': {'izvestaji': 34, 'dokumenti': 2},
    }
    s.update(preklopi)
    return s


def test_oba_stanja_su_razlicito_prikazana(kartica):
    html = kartica.render(odobravanje=_stanje())
    assert 'одобравање укључено' in html
    assert 'одобравање искључено' in html


def test_broj_zatecenih_se_vidi_pre_gasenja(kartica):
    """Админ мора да зна КОЛИКО ће се затворити пре него што кликне."""
    html = kartica.render(odobravanje=_stanje())
    assert '34' in html and '2' in html


def test_objasnjeno_da_bez_odobravanja_nije_odobreno(kartica):
    html = kartica.render(odobravanje=_stanje())
    assert 'Без одобравања' in html
    assert 'празна' in html, 'мора да пише да поља потписа остају празна'


def test_neocitano_stanje_ne_tvrdi_da_je_ukljuceno_ni_iskljuceno(kartica):
    """Ако стање није очитано, страница то КАЖЕ уместо да претпостави."""
    html = kartica.render(odobravanje=None)
    assert 'не може очитати' in html
    assert 'одобравање укључено' not in html
    assert 'одобравање искључено' not in html


def test_env_preklop_je_vidljivo_upozorenje(kartica):
    """Дугме без ефекта је горе од дугмета којег нема — мора да се каже."""
    html = kartica.render(odobravanje=_stanje(
        env_preklop={'MIS_ODOBRAVANJE_IZVESTAJA': False,
                     'MIS_ODOBRAVANJE_DOKUMENATA': None,
                     'MIS_ROK_PREDAJE': None}))
    assert 'окружења преклапа' in html

    bez = kartica.render(odobravanje=_stanje())
    assert 'окружења преклапа' not in bez


def test_rok_ima_svoje_reci_a_ne_odobravanje(kartica):
    """Рок није одобравање — ознака мора да каже „важи", не „укључено"."""
    html = kartica.render(odobravanje=_stanje())
    assert 'рок važi' not in html          # ћирилица, не мешано писмо
    assert 'рок важи' in html
    assert 'Месец који још није почео остаје' in html \
        or 'месец који још није почео' in html.lower()
