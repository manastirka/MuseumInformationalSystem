"""Верзија статичког фајла за кеш (?v=<mtime>) — исти принцип који је већ
коришћен за weather_particles.js, само уопштен за све CSS/JS фајлове.

Разлог: издвојени CSS страна се кешира у прегледачу; без верзије корисник
после деплоја види стари изглед док не очисти кеш.
"""
import os
import time
from pathlib import Path

_KOREN = Path(__file__).resolve().parent / 'static'
_KES = {}


def verzija_statike(relativna_putanja):
    """Врати mtime фајла из static/ као цео број (за ?v=)."""
    kljuc = str(relativna_putanja)
    if kljuc in _KES and not os.environ.get('FLASK_DEBUG'):
        return _KES[kljuc]
    try:
        v = int((_KOREN / kljuc).stat().st_mtime)
    except OSError:
        v = int(time.time())
    _KES[kljuc] = v
    return v
