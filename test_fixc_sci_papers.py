"""Phase C low-severity hardening tests for the sci-papers cluster."""

import os
from unittest import mock

os.environ.setdefault('FLASK_ENV', 'testing')
os.environ.setdefault('SECRET_KEY', 'test-secret')
os.environ.setdefault('REDIS_URL', '')
os.environ.setdefault('SESSION_TYPE', 'filesystem')
os.environ.setdefault('SESSION_FILE_DIR', '/tmp/museum-test-c-sci-papers')

import fetch_scientific_papers as fsp
import science_news_updater as snu
import scientific_papers_database as spdb


# Finding 3: OpenAlex work with explicit title:null must not yield None title.
def test_parse_openalex_work_null_title_coerced_to_empty_string():
    parsed = fsp.parse_openalex_work({'id': 'W1', 'title': None})
    assert parsed['title'] == ''


def test_parse_openalex_work_missing_title_coerced_to_empty_string():
    parsed = fsp.parse_openalex_work({'id': 'W1'})
    assert parsed['title'] == ''


def test_parse_openalex_work_real_title_preserved():
    parsed = fsp.parse_openalex_work({'id': 'W1', 'title': 'Geology of Bor'})
    assert parsed['title'] == 'Geology of Bor'


# Finding 2: determine_region must use word boundaries, not substrings.
def test_determine_region_no_false_positive_on_substrings():
    # 'carbon' contains 'bor', 'avalanche' contains 'avala' -> must NOT tag Balkan.
    region, _ = snu.determine_region('Carbon dating of an avalanche deposit')
    assert region == 'world'


def test_determine_region_true_balkan_keyword_still_matches():
    region, name = snu.determine_region('New survey of the Bor copper mine')
    assert region == 'balkans'
    assert name == 'Балкан'


def test_determine_region_europe_keyword_with_trailing_space_token():
    # 'uk ' / 'eu ' style tokens must still match as whole words.
    region, _ = snu.determine_region('Study conducted in the UK this year')
    assert region == 'europe'


# Finding 1: unvalidated per_page/page must be clamped before division.
def _fake_conn(total_count):
    captured = {}

    def execute(sql, params=None):
        result = mock.Mock()
        if 'LIMIT' in sql:
            captured['params'] = params
            result.fetchall.return_value = []
        else:
            result.fetchone.return_value = {'count': total_count}
        return result

    conn = mock.Mock()
    conn.execute.side_effect = execute
    conn.close.return_value = None
    return conn, captured


def test_get_all_papers_per_page_zero_does_not_raise_zerodivision():
    conn, captured = _fake_conn(10)
    with mock.patch.object(spdb, 'get_connection', return_value=conn):
        papers, total_count, total_pages = spdb.get_all_papers(page=1, per_page=0)
    assert total_pages >= 1
    # offset must be non-negative; per_page clamped to >= 1.
    assert captured['params'][-1] == 0  # offset
    assert captured['params'][-2] >= 1  # per_page (limit)


def test_get_all_papers_negative_page_clamped_to_nonnegative_offset():
    conn, captured = _fake_conn(10)
    with mock.patch.object(spdb, 'get_connection', return_value=conn):
        spdb.get_all_papers(page=-5, per_page=50)
    assert captured['params'][-1] >= 0  # offset must not be negative


def test_get_papers_by_locality_per_page_zero_does_not_raise():
    conn, captured = _fake_conn(7)
    with mock.patch.object(spdb, 'get_connection', return_value=conn):
        papers, total_count, total_pages = spdb.get_papers_by_locality('Bor', page=1, per_page=0)
    assert total_pages >= 1
    assert captured['params'][-1] == 0  # offset
    assert captured['params'][-2] >= 1  # per_page (limit)
