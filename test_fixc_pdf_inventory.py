import os

os.environ.setdefault('FLASK_ENV', 'testing')
os.environ.setdefault('SECRET_KEY', 'test-secret')
os.environ.setdefault('REDIS_URL', '')
os.environ.setdefault('SESSION_TYPE', 'filesystem')
os.environ.setdefault('SESSION_FILE_DIR', '/tmp/museum-test-c-pdf-inventory')

from io import BytesIO

from pdf_export import (
    CollectionPDFExporter,
    SpecimenCertificatePDFExporter,
)
from inventory_reconciliation import InventoryReconciliation


# ---------------------------------------------------------------------------
# Finding 1: markup-like values must not crash Paragraph rendering
# ---------------------------------------------------------------------------

def test_export_collection_with_markup_collection_name():
    buffer = CollectionPDFExporter().export_collection("Збирка <b>", [], None)
    assert isinstance(buffer, BytesIO)
    assert buffer.getvalue()


def test_specimen_certificate_with_markup_catalog_number():
    buffer = SpecimenCertificatePDFExporter().export_specimen_certificate(
        {'catalog_number': 'M<b>'}, "Збирка"
    )
    assert isinstance(buffer, BytesIO)
    assert buffer.getvalue()


def test_specimen_certificate_with_markup_collection_name():
    buffer = SpecimenCertificatePDFExporter().export_specimen_certificate(
        {'catalog_number': '1'}, "Збирка <i>"
    )
    assert isinstance(buffer, BytesIO)
    assert buffer.getvalue()


# ---------------------------------------------------------------------------
# Finding 3: search_inventory must not crash when category/sheet are None
# ---------------------------------------------------------------------------

def _reconciliation_with_items(items):
    recon = InventoryReconciliation()
    recon._inventory_cache = items
    return recon


def test_search_inventory_category_none_does_not_crash():
    recon = _reconciliation_with_items([
        {'inventory_number': 1, 'name': 'Кварц', 'category': 'минерал'},
    ])
    results = recon.search_inventory(category=None)
    assert len(results) == 1


def test_search_inventory_sheet_none_does_not_crash():
    recon = _reconciliation_with_items([
        {'inventory_number': 1, 'name': 'Кварц', 'sheet': 'А1'},
    ])
    results = recon.search_inventory(sheet=None)
    assert len(results) == 1


def test_search_inventory_category_filter_still_works():
    recon = _reconciliation_with_items([
        {'inventory_number': 1, 'name': 'Кварц', 'category': 'минерал'},
        {'inventory_number': 2, 'name': 'Лептир', 'category': 'инсект'},
    ])
    results = recon.search_inventory(category='минерал')
    assert len(results) == 1
    assert results[0]['inventory_number'] == 1
