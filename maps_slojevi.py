"""Rasterski slojevi karte iz Google Earth Engine-a (sveska 11-mis-slojevi).

Pločice su binarni podaci i NISU u git-u: jednokratno se izvezu iz GEE-a,
izrežu gdal2tiles-om u XYZ šemu i rsync-om prebace u MIS_SLOJEVI_PATH
(produkcija: /data/mis/slojevi), po strukturi ``<sloj>/{z}/{x}/{y}.png``
(docs/mis-slojevi.md). Sloj kog nema na disku se ne nudi u kontrolama karte.
"""

import os
import re
from pathlib import Path

from flask import abort, send_file

# Paleta Dynamic World V1 (katalog GEE, GOOGLE/DYNAMICWORLD/V1) — boje su
# podatak pločica, ne tema; legenda mora da ih ponovi doslovno.
DW_LEGENDA = (
    ('Вода', '#419bdf'), ('Дрвеће', '#397d49'), ('Трава', '#88b053'),
    ('Плавна вегетација', '#7a87c6'), ('Усеви', '#e49635'), ('Жбуње и шикара', '#dfc35a'),
    ('Изграђено', '#c4281b'), ('Голо тле', '#a59b8f'), ('Снег и лед', '#b39fe1'),
)

SLOJEVI = {
    'reljef': {
        'naziv': 'Рељеф (сенчење)',
        'atribucija': 'Рељеф: Copernicus DEM GLO-30 © DLR e.V. 2010–2014 и © Airbus Defence and '
                      'Space GmbH 2014–2018, Copernicus (EU, ESA)',
        'providnost': 0.5,
        'legenda': (),
    },
    'pokrivac-2024': {
        'naziv': 'Покривач земљишта 2024',
        'atribucija': 'Покривач: Dynamic World V1 2024, Google и World Resources Institute (CC BY 4.0)',
        'providnost': 0.7,
        'legenda': DW_LEGENDA,
    },
}

_ZUM = re.compile(r'^\d{1,2}$')


def koren():
    return Path(os.environ.get('MIS_SLOJEVI_PATH', './data/mis_slojevi'))


def dostupni():
    """Slojevi koji postoje na disku, sa opsegom zuma iz imena direktorijuma."""
    ishod = []
    for kljuc, opis in SLOJEVI.items():
        direktorijum = koren() / kljuc
        try:
            zumovi = sorted(int(d.name) for d in direktorijum.iterdir() if d.is_dir() and _ZUM.match(d.name))
        except OSError:
            continue
        if zumovi:
            ishod.append(dict(opis, kljuc=kljuc, min_zoom=zumovi[0], max_zoom=zumovi[-1]))
    return ishod


def posluzi_plocicu(kljuc, z, x, y):
    if kljuc not in SLOJEVI or not (0 <= z <= 22 and 0 <= x < 2 ** z and 0 <= y < 2 ** z):
        abort(404)
    putanja = koren() / kljuc / str(z) / str(x) / f'{y}.png'
    if not putanja.is_file():
        abort(404)
    return send_file(putanja, mimetype='image/png', conditional=True, max_age=30 * 24 * 3600)
