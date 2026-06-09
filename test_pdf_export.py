#!/usr/bin/env python3
"""
Test script for PDF export functionality
"""

import os

from pdf_export import (
    export_collection_pdf,
    export_visitor_report_pdf,
    export_research_project_pdf,
    export_specimen_certificate_pdf
)

# Write generated PDFs next to this script instead of a hardcoded home path
OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))


def run_collection_export():
    """Test collection PDF export"""
    print("Testing collection export...")

    # Sample collection data
    collection_name = "Тест збирка"
    specimens = [
        {
            'catalog_number': 'TEST-001',
            'scientific_name': 'Testus exampleus',
            'common_name_sr': 'Тест примерак',
            'family': 'Testaceae',
            'location_found': 'Тест локација',
            'date_collected': '2025-01-01',
            'collector': 'Тест колектор',
            'condition': 'Одлично',
            'description': 'Ово је тест примерак за PDF извоз'
        },
        {
            'catalog_number': 'TEST-002',
            'scientific_name': 'Exemplarus testicus',
            'common_name_sr': 'Други тест примерак',
            'family': 'Testaceae',
            'location_found': 'Београд, Србија',
            'date_collected': '2025-01-02',
            'collector': 'Др Тест Тестовић',
            'condition': 'Добро',
            'description': 'Још један тест примерак'
        }
    ]

    statistics = {
        'total_specimens': 2,
        'total_species': 2,
        'curators': 1
    }

    try:
        pdf_buffer = export_collection_pdf(collection_name, specimens, statistics)

        # Save to file
        with open(os.path.join(OUTPUT_DIR, 'test_collection_export.pdf'), 'wb') as f:
            f.write(pdf_buffer.read())

        print("✓ Collection export successful! File saved: test_collection_export.pdf")
        return True
    except Exception as e:
        print(f"✗ Collection export failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def run_visitor_report_export():
    """Test visitor report PDF export"""
    print("\nTesting visitor report export...")

    # Sample visitor records
    visitor_records = [
        {
            'id': 1,
            'date': '2025-01-01',
            'visitor_type': 'Школска група',
            'group_name': 'ОШ "Тест школа"',
            'number_of_visitors': 30,
            'age_group': '10-12 година',
            'guide': 'Тест водич',
            'exhibition_visited': 'Тест изложба',
            'duration_minutes': 90,
            'ticket_type': 'Групна',
            'total_revenue': 1500,
            'educational_program': 'Тест програм',
            'feedback': 'Одлично!'
        },
        {
            'id': 2,
            'date': '2025-01-02',
            'visitor_type': 'Индивидуални посетиоци',
            'group_name': '',
            'number_of_visitors': 10,
            'age_group': 'Мешано',
            'guide': '',
            'exhibition_visited': 'Минералошка збирка',
            'duration_minutes': 60,
            'ticket_type': 'Појединачни',
            'total_revenue': 500,
            'educational_program': '',
            'feedback': ''
        }
    ]

    try:
        pdf_buffer = export_visitor_report_pdf(visitor_records, '2025-01-01', '2025-01-31')

        # Save to file
        with open(os.path.join(OUTPUT_DIR, 'test_visitor_report.pdf'), 'wb') as f:
            f.write(pdf_buffer.read())

        print("✓ Visitor report export successful! File saved: test_visitor_report.pdf")
        return True
    except Exception as e:
        print(f"✗ Visitor report export failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def run_research_project_export():
    """Test research project PDF export"""
    print("\nTesting research project export...")

    # Sample research project
    project = {
        'id': 1,
        'project_name': 'Тест истраживачки пројекат',
        'principal_investigator': 'Др Тест Истраживач',
        'start_year': '2023',
        'end_year': '2025',
        'status': 'У току',
        'budget': '1.000.000',
        'specimens_studied': 50,
        'field_trips': 10,
        'description': 'Ово је тест пројекат за проверу PDF извоза. Пројекат обухвата истраживање различитих аспеката природне историје.',
        'key_findings': 'Важна открића у области тест истраживања.',
        'publications': ['Тест публикација 1 (2024)', 'Тест публикација 2 (2025)'],
        'collaborators': ['Тест сарадник 1', 'Тест сарадник 2'],
        'international_collaborations': ['Тест универзитет, САД']
    }

    try:
        pdf_buffer = export_research_project_pdf(project)

        # Save to file
        with open(os.path.join(OUTPUT_DIR, 'test_research_project.pdf'), 'wb') as f:
            f.write(pdf_buffer.read())

        print("✓ Research project export successful! File saved: test_research_project.pdf")
        return True
    except Exception as e:
        print(f"✗ Research project export failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def run_specimen_certificate_export():
    """Test specimen certificate PDF export"""
    print("\nTesting specimen certificate export...")

    # Sample specimen
    specimen = {
        'catalog_number': 'CERT-001',
        'scientific_name': 'Certificatus testus',
        'common_name_sr': 'Тест сертификат',
        'family': 'Testaceae',
        'location_found': 'Београд, Србија',
        'date_collected': '2025-01-01',
        'collector': 'Др Тест Колектор',
        'condition': 'Одлично',
        'endemic_status': 'Ендемична врста',
        'conservation_status': 'Заштићена',
        'description': 'Ово је тест примерак за сертификат'
    }

    collection_name = 'Тест збирка'

    try:
        pdf_buffer = export_specimen_certificate_pdf(specimen, collection_name)

        # Save to file
        with open(os.path.join(OUTPUT_DIR, 'test_specimen_certificate.pdf'), 'wb') as f:
            f.write(pdf_buffer.read())

        print("✓ Specimen certificate export successful! File saved: test_specimen_certificate.pdf")
        return True
    except Exception as e:
        print(f"✗ Specimen certificate export failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False



# Pytest entry points - assert on the script helpers above.

def test_collection_export():
    assert run_collection_export()


def test_visitor_report_export():
    assert run_visitor_report_export()


def test_research_project_export():
    assert run_research_project_export()


def test_specimen_certificate_export():
    assert run_specimen_certificate_export()


def main():
    """Run all tests"""
    print("=" * 60)
    print("PDF Export System - Test Suite")
    print("=" * 60)

    results = []

    # Run tests
    results.append(("Collection Export", run_collection_export()))
    results.append(("Visitor Report Export", run_visitor_report_export()))
    results.append(("Research Project Export", run_research_project_export()))
    results.append(("Specimen Certificate Export", run_specimen_certificate_export()))

    # Summary
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for test_name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status}: {test_name}")

    print(f"\nTotal: {passed}/{total} tests passed")

    if passed == total:
        print("\n✓ All PDF export tests passed successfully!")
        print("\nGenerated test files:")
        print("  - test_collection_export.pdf")
        print("  - test_visitor_report.pdf")
        print("  - test_research_project.pdf")
        print("  - test_specimen_certificate.pdf")
        return 0
    else:
        print("\n✗ Some tests failed. Please check the errors above.")
        return 1


if __name__ == '__main__':
    exit(main())
