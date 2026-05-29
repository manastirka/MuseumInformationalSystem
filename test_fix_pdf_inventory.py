import os

os.environ.setdefault('FLASK_ENV', 'testing')
os.environ.setdefault('SECRET_KEY', 'test-secret')
os.environ.setdefault('REDIS_URL', '')
os.environ.setdefault('SESSION_TYPE', 'filesystem')
os.environ.setdefault('SESSION_FILE_DIR', '/tmp/museum-test-pdf-inventory')

import pytest

from pdf_export import export_research_project_pdf


def test_description_with_unclosed_tag_does_not_crash():
    """Free-text description containing an angle-bracket tag-like token must not
    crash ReportLab Paragraph wrapping (previously raised ValueError -> HTTP 500)."""
    project = {
        'project_name': 'Тест пројекат',
        'description': 'Истраживање <b>минерала без затварања тага',
    }
    buffer = export_research_project_pdf(project)
    data = buffer.getvalue()
    assert data.startswith(b'%PDF')


def test_publications_and_collaborators_with_closing_tag_do_not_crash():
    """List items with stray closing tags must not crash the build."""
    project = {
        'project_name': 'Тест <i>пројекат',
        'publications': ['Публикација </para> hack', 'Друга <b>публикација'],
        'collaborators': ['Сарадник </font> x', 'Други <unknown> сарадник'],
    }
    buffer = export_research_project_pdf(project)
    assert buffer.getvalue().startswith(b'%PDF')


def test_project_name_with_tag_like_token_does_not_crash():
    """project_name itself is user-controlled and embedded in a Paragraph."""
    project = {
        'project_name': 'Назив </para> експлоит',
    }
    buffer = export_research_project_pdf(project)
    assert buffer.getvalue().startswith(b'%PDF')


def test_ampersand_alone_still_works():
    """Sanity: plain ampersand text must continue to produce a valid PDF."""
    project = {
        'project_name': 'A & B',
        'description': 'Истраживање A & B минерала',
    }
    buffer = export_research_project_pdf(project)
    assert buffer.getvalue().startswith(b'%PDF')
