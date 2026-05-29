"""Support helpers and shared state for geological map terrain assets."""

import io
import logging
import os
import re
import tempfile
import zipfile
from xml.etree import ElementTree as ET

from PIL import Image

logger = logging.getLogger(__name__)

APP_ROOT = os.path.dirname(__file__)
KMZ_PATH = os.path.join(APP_ROOT, 'Karte', 'srbija korigovana.kmz')
DEM_DIR = os.path.join(APP_ROOT, 'data', 'dem_serbia')

_kmz_tile_index = None


def resolve_tile_cache_dir():
    """Return a writable cache directory for extracted geological tiles."""
    preferred = os.path.join(APP_ROOT, 'static', 'map_tiles')
    parent = os.path.dirname(preferred)
    if os.access(parent, os.W_OK):
        return preferred
    return os.environ.get(
        'MUSEUM_TILE_CACHE_DIR',
        os.path.join(tempfile.gettempdir(), 'museum_info_system_map_tiles'),
    )


TILE_CACHE_DIR = resolve_tile_cache_dir()


def build_tile_index():
    """Parse KML inside the KMZ and build a tile index by zoom level."""
    global _kmz_tile_index
    if _kmz_tile_index is not None:
        return _kmz_tile_index

    index = {'levels': {}, 'bounds': {}}
    try:
        with zipfile.ZipFile(KMZ_PATH, 'r') as archive:
            kml_name = None
            for name in archive.namelist():
                if name.lower().endswith('.kml'):
                    kml_name = name
                    break

            if not kml_name:
                logger.error("No KML file found inside KMZ")
                return index

            with archive.open(kml_name) as handle:
                kml_bytes = handle.read()
                try:
                    kml_content = kml_bytes.decode('utf-8')
                except UnicodeDecodeError:
                    kml_content = kml_bytes.decode('iso-8859-1')

            tree = ET.fromstring(kml_content)
            ns = {'kml': 'http://www.opengis.net/kml/2.2'}

            for overlay in tree.iter('{http://www.opengis.net/kml/2.2}GroundOverlay'):
                icon = overlay.find('kml:Icon/kml:href', ns)
                if icon is None:
                    continue
                filename = icon.text.strip()

                match = re.match(r'kml_image_L(\d+)_(\d+)_(\d+)\.tif', filename)
                if not match:
                    continue

                level = int(match.group(1))
                row = int(match.group(2))
                col = int(match.group(3))

                lat_lon_box = overlay.find('kml:LatLonBox', ns)
                if lat_lon_box is None:
                    continue

                north = float(lat_lon_box.find('kml:north', ns).text)
                south = float(lat_lon_box.find('kml:south', ns).text)
                east = float(lat_lon_box.find('kml:east', ns).text)
                west = float(lat_lon_box.find('kml:west', ns).text)

                # Shift geological overlay ~10 m east to align with OSM.
                geo_lng_offset = 0.000125
                east += geo_lng_offset
                west += geo_lng_offset

                tile_info = {
                    'filename': filename,
                    'north': north,
                    'south': south,
                    'east': east,
                    'west': west,
                    'row': row,
                    'col': col,
                }

                index['levels'].setdefault(level, []).append(tile_info)

            all_tiles = [tile for tiles in index['levels'].values() for tile in tiles]
            if all_tiles:
                index['bounds'] = {
                    'north': max(tile['north'] for tile in all_tiles),
                    'south': min(tile['south'] for tile in all_tiles),
                    'east': max(tile['east'] for tile in all_tiles),
                    'west': min(tile['west'] for tile in all_tiles),
                }

        logger.info(
            "Built KMZ tile index: %s tiles across %s levels",
            sum(len(tiles) for tiles in index['levels'].values()),
            len(index['levels']),
        )
    except Exception as exc:
        logger.error("Error building KMZ tile index: %s", exc)

    _kmz_tile_index = index
    return index


def extract_tile_to_cache(filename):
    """Extract one tile from the KMZ into the PNG cache."""
    tif_name = filename + '.tif'
    png_name = filename + '.png'
    png_path = os.path.join(TILE_CACHE_DIR, png_name)

    if os.path.exists(png_path):
        return png_path

    os.makedirs(TILE_CACHE_DIR, exist_ok=True)
    try:
        with zipfile.ZipFile(KMZ_PATH, 'r') as archive:
            with archive.open(tif_name) as handle:
                tif_data = handle.read()

        image = Image.open(io.BytesIO(tif_data))
        if image.mode != 'RGBA':
            image = image.convert('RGBA')
        image.save(png_path, 'PNG', optimize=True)
        return png_path
    except (KeyError, Exception) as exc:
        logger.error("Error extracting tile %s: %s", filename, exc)
        return None
