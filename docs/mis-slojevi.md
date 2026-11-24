# Rasterski slojevi karte iz Google Earth Engine-a (reljef, pokrivač 2024)

Geološka karta (`/admin/maps`, grupa **Подлога**) nudi dva dodatna sloja čim
njihove pločice postoje na disku:

| Ključ | Prekidač | Izvor | Atribucija (ispisuje je Leaflet) |
|---|---|---|---|
| `reljef` | Рељеф (сенчење) | Copernicus DEM GLO-30, `ee.Terrain.hillshade` | © DLR e.V. 2010–2014 i © Airbus Defence and Space GmbH 2014–2018, Copernicus (EU, ESA) |
| `pokrivac-2024` | Покривач земљишта 2024 | Dynamic World V1, modalna klasa 2024 | Google i World Resources Institute, CC BY 4.0 |

Pločice su **binarni podaci i ne idu u git** (`data/mis_slojevi/` je u
`.gitignore`). Kod sloja je u `maps_slojevi.py`, ruta
`/api/map/slojevi/<sloj>/<z>/<x>/<y>.png` (samo prijavljeni korisnici).

## Struktura

```
$MIS_SLOJEVI_PATH/
  reljef/{z}/{x}/{y}.png          # XYZ šema (y od severa), kao OSM
  pokrivac-2024/{z}/{x}/{y}.png
```

Opseg zuma čita se iz imena direktorijuma (`6` … `12`), pa Leaflet iznad
najvećeg zuma uvećava poslednje pločice. Sloj bez direktorijuma se ne prikazuje.

## Pravljenje (jednom, van MIS-a)

1. Sveska `/tmp/petro/colab/11-mis-slojevi.ipynb` (Earth Engine nalog kustosa):
   izvoz GeoTIFF-ova Srbije na Google Drive, zatim lokalno `gdal2tiles.py --xyz`.
   Koraci, procena veličine i provere su u `rad/11/README-slojevi.md` uz svesku.
2. Rezultat: lokalni direktorijum `slojevi/` sa `reljef/` i `pokrivac-2024/`.

## Prebacivanje na produkciju (rsync)

```bash
# sa mašine na kojoj su pločice napravljene
rsync -av --info=progress2 slojevi/ <korisnik>@192.168.144.194:/data/mis/slojevi/
# na PROD-u: servis mis mora da čita (ne i da piše)
sudo chown -R mis:mis /data/mis/slojevi
sudo find /data/mis/slojevi -type d -exec chmod 755 {} +
sudo find /data/mis/slojevi -type f -exec chmod 644 {} +
```

U prod `.env` dodati `MIS_SLOJEVI_PATH=/data/mis/slojevi` i restartovati servis
(`sudo systemctl restart mis`; preload — HUP nije dovoljan). Provera: na karti se
u grupi „Подлога“ pojave prekidači, a
`curl -k -b <kolačić> https://<host>/api/map/slojevi/reljef/8/142/93.png` vraća PNG.

Noćni backup ne mora da čuva pločice — mogu se ponovo napraviti iz sveske 11.
