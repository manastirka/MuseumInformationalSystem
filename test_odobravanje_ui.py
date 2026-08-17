"""Картица прекидача у админ панелу — да приказ никад не тврди више него што зна."""
import os
import pathlib

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


# --- позив ка серверу -------------------------------------------------------

@pytest.fixture(scope='module')
def blok():
    """Само наш део скрипте — остатак стране има своје, старије позиве."""
    izvor = (pathlib.Path('templates') / SABLON).read_text(encoding='utf-8')
    # Почетак је помоћник `misOdgovor`, не сам слушалац догађаја — иначе
    # би тело помоћника испало из исечка и тест би проверавао пола ствари.
    pocetak = izvor.index('async function misOdgovor')
    return izvor[pocetak:]


def test_poziv_ide_kroz_secureFetch(blok):
    """CSRFProtect важи за цео app (app.py:373). Голи `fetch` добије HTML
    страницу грешке 400, а `response.json()` на њој пукне са
    „Unexpected token '<'" — порука која кориснику не значи ништа.
    Тачно то се десило 17.08.2026 при првом покушају гашења прекидача.

    Токен додаје `secureFetch` из базног шаблона — не измишља се други
    начин, јер два начина значе да ће један остати без токена.
    """
    assert blok.count('secureFetch(') == 2, 'оба POST позива иду кроз secureFetch'
    assert 'await fetch(' not in blok, 'остао је голи fetch без CSRF токена'


def test_odgovor_koji_nije_json_daje_razumljivu_poruku(blok):
    """Кад сервер врати HTML, корисник мора да сазна ШТА се десило —
    не да добије грешку парсера."""
    assert 'misOdgovor' in blok
    assert 'HTTP ' in blok, 'порука мора да носи стварни статус'
    assert 'await r.json()' not in blok, 'сирови r.json() пуца на HTML одговору'


def test_oba_bazna_sablona_daju_secureFetch_i_token():
    """Страница се рендерује самостално и у iframe-у (?embedded=1). Ако
    један од два базна шаблона нема помоћник или мета ознаку, дугме би
    радило само на једном месту."""
    for baza in ('base.html', 'base_embedded.html'):
        tekst = (pathlib.Path('templates') / baza).read_text(encoding='utf-8')
        assert 'name="csrf-token"' in tekst, baza
        assert 'function secureFetch' in tekst, baza


# --- делимичан неуспех ------------------------------------------------------

def test_delimican_neuspeh_ne_vraca_prekidac(blok):
    """Упис прекидача и разрешавање затеченог су ДВЕ трансакције.

    Ако друга падне, прекидач је већ уписан. Враћање дугмета на старо би
    приказ довело у раскорак са базом — панел би тврдио „укључено" док база
    каже „искључено". Нашла рецензија мерџа `a507044`.
    """
    assert 'prekidac_upisan' in blok, \
        'клијент мора да разликује делимичан од потпуног неуспеха'
    # У тој грани се излази без `vrati()` — дугме остаје тамо где јесте.
    grana = blok[blok.index('rez.prekidac_upisan'):]
    kraj = grana.index('throw new Error')
    assert 'vrati()' not in grana[:kraj], \
        'делимичан неуспех не сме да враћа прекидач'


def test_server_ne_tvrdi_da_nista_nije_promenjeno(izvor_servera):
    """Порука мора да каже да је прекидач ЈЕСТЕ промењен, и шта још треба."""
    deo = izvor_servera[izvor_servera.index('def api_odobravanje'):]
    deo = deo[:deo.index('def api_save_general_settings')]
    assert "'prekidac_upisan': True" in deo
    assert 'Прекидач ЈЕСТЕ промењен' in deo
    assert 'scripts/odobravanje.py' in deo, \
        'порука мора да каже КАКО да се посао доврши'


@pytest.fixture(scope='module')
def izvor_servera():
    return pathlib.Path('admin_system_views.py').read_text(encoding='utf-8')
