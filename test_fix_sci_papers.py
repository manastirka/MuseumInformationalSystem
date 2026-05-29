#!/usr/bin/env python3
"""Reproducing tests for sci-papers cluster bug fixes."""

import os

os.environ.setdefault('FLASK_ENV', 'testing')
os.environ.setdefault('SECRET_KEY', 'test-secret')
os.environ.setdefault('REDIS_URL', '')
os.environ.setdefault('SESSION_TYPE', 'filesystem')
os.environ.setdefault('SESSION_FILE_DIR', '/tmp/museum-test-sci-papers')

from unittest.mock import patch

import fetch_scientific_papers
import science_news_updater


class TestFetchMainNoDbPath:
    """Finding 1: main() must not crash on db.DB_PATH at completion."""

    def test_main_completes_without_attribute_error(self):
        localities = [{'name': 'Bor', 'ogk_code': '123', 'tumac': {}}]

        with patch.object(fetch_scientific_papers.os.path, 'exists') as mock_exists, \
                patch.object(fetch_scientific_papers, 'load_json_file', return_value=localities), \
                patch.object(fetch_scientific_papers.db, 'init_database'), \
                patch.object(fetch_scientific_papers, 'fetch_for_locality',
                             return_value={'new_papers': 0, 'linked': 0, 'queries': 0, 'skipped': 0}), \
                patch.object(fetch_scientific_papers, 'save_state'), \
                patch.object(fetch_scientific_papers.db, 'get_statistics',
                             return_value={'total_papers': 0, 'localities_covered': 0}), \
                patch('sys.argv', ['fetch_scientific_papers.py', '--locality', 'Bor']):
            # GEO_MAP_PATH must look present so we reach the completion summary
            mock_exists.return_value = True
            # Should run to completion without AttributeError on db.DB_PATH
            fetch_scientific_papers.main()


class TestRssClassicItemParsing:
    """Finding 2: classic RSS title/description/pubDate must not be lost."""

    RSS_XML = b"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
  <channel>
    <title>Feed</title>
    <item>
      <title>Major earthquake in Serbia near Belgrade</title>
      <description>A significant seismic event was recorded.</description>
      <link>https://example.com/article-1</link>
      <pubDate>2025-05-12</pubDate>
    </item>
    <item>
      <title>Volcano study in Italy</title>
      <description>New research about Vesuvius.</description>
      <link>https://example.com/article-2</link>
      <pubDate>2025-05-13</pubDate>
    </item>
  </channel>
</rss>"""

    def test_classic_rss_titles_descriptions_dates_preserved(self):
        single_feed = [{
            'url': 'https://example.com/rss.xml',
            'category': 'geology',
            'categoryName': 'Геологија',
            'source': 'TestFeed',
            'region': 'world',
        }]

        class FakeResponse:
            status_code = 200
            content = self.RSS_XML

        with patch.object(science_news_updater, 'RSS_FEEDS', single_feed), \
                patch.object(science_news_updater.requests, 'get', return_value=FakeResponse()):
            items = science_news_updater.fetch_rss_news()

        assert len(items) == 2, f"expected 2 items, got {len(items)}: {items}"

        titles = {it['title'] for it in items}
        assert 'Major earthquake in Serbia near Belgrade' in titles
        assert 'No title' not in titles

        first = next(it for it in items
                     if it['title'] == 'Major earthquake in Serbia near Belgrade')
        assert first['summary'] == 'A significant seismic event was recorded.'
        assert first['date'] == '2025-05-12'
        # Title mentions Serbia/Belgrade -> Balkans classification
        assert first['region'] == 'balkans'
