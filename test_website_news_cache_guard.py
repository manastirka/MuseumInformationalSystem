import threading
import time

import dashboard_data_support as dds


class _FakeResponse:
    text = "<article><h2><a href='/vest-1'>Vest 1</a></h2><p>Opis</p></article>"

    def raise_for_status(self):
        return None


def _reset_news_cache():
    with dds._website_news_cache_lock:
        dds._website_news_cache['data'] = None
        dds._website_news_cache['timestamp'] = None


def test_fetch_website_news_avoids_concurrent_upstream_stampede(monkeypatch):
    _reset_news_cache()

    started = threading.Event()
    release = threading.Event()
    call_count = {'value': 0}

    def fake_get(*_args, **_kwargs):
        call_count['value'] += 1
        started.set()
        release.wait(timeout=2)
        return _FakeResponse()

    monkeypatch.setattr(dds.requests, 'get', fake_get)

    results = []

    worker = threading.Thread(target=lambda: results.append(dds.fetch_website_news(limit=1)))
    worker.start()
    assert started.wait(timeout=1)

    second_result = dds.fetch_website_news(limit=1)
    release.set()
    worker.join(timeout=2)

    assert call_count['value'] == 1
    assert second_result == []
    assert results[0][0]['title'] == 'Vest 1'


def test_fetch_website_news_returns_stale_cache_during_refresh(monkeypatch):
    with dds._website_news_cache_lock:
        dds._website_news_cache['data'] = [{'title': 'Cached', 'link': '/cached', 'image': '', 'date': '', 'excerpt': ''}]
        dds._website_news_cache['timestamp'] = time.time() - (dds._WEBSITE_NEWS_CACHE_TTL_SECONDS + 5)

    started = threading.Event()
    release = threading.Event()

    def fake_get(*_args, **_kwargs):
        started.set()
        release.wait(timeout=2)
        return _FakeResponse()

    monkeypatch.setattr(dds.requests, 'get', fake_get)

    worker = threading.Thread(target=lambda: dds.fetch_website_news(limit=1))
    worker.start()
    assert started.wait(timeout=1)

    stale_result = dds.fetch_website_news(limit=1)
    release.set()
    worker.join(timeout=2)

    assert stale_result == [{'title': 'Cached', 'link': '/cached', 'image': '', 'date': '', 'excerpt': ''}]
