"""Phase-C low-severity hardening tests for collection_bootstrap_support.

Covers three confirmed findings:
  1. _get_cached_phase3a_database must not permanently cache an empty/error
     fallback result, so a recovered PostgreSQL backend repopulates on the
     next request instead of serving 0 items for the worker lifetime.
  2. The herpetology fallback Serbian common name must be all-Cyrillic and
     correctly spelled (no Latin a/e mixed into the Cyrillic word).
  3. The static meteorite statistics must be internally consistent with the
     specimen list (counts derived from the data, no drifting hand values).
"""

import os

os.environ.setdefault('FLASK_ENV', 'testing')
os.environ.setdefault('SECRET_KEY', 'test-secret')
os.environ.setdefault('REDIS_URL', '')
os.environ.setdefault('SESSION_TYPE', 'filesystem')
os.environ.setdefault('SESSION_FILE_DIR', '/tmp/museum-test-c-collections-bootstrap')

import app as museum_app  # noqa: F401  (prescribed bootstrap import)
from collection_bootstrap_support import (
    CollectionBootstrapSupport,
    HERPETOLOGY_FALLBACK,
    METEORITE_COLLECTION_DATABASE,
)


class _StubLazyDict(dict):
    """Minimal stand-in for LazyLoadedDict used only at construction time."""

    def __init__(self, loader, label):
        super().__init__()
        self._loader = loader
        self._label = label


class _StubPhase3a:
    """Programmable phase3a loader stub: returns a queued result per call."""

    def __init__(self, heritage_results):
        self._heritage_results = list(heritage_results)
        self.heritage_calls = 0

    def get_cultural_heritage_database(self):
        self.heritage_calls += 1
        if len(self._heritage_results) == 1:
            return self._heritage_results[0]
        return self._heritage_results.pop(0)

    def get_meteorite_collection_database(self):
        return {'specimens': [], 'statistics': {}}


def _empty_heritage():
    return {
        'heritage_items': [],
        'statistics': {'total_heritage_items': 0},
    }


def _loaded_heritage():
    return {
        'heritage_items': [{'id': 1, 'name': 'X'}],
        'statistics': {'total_heritage_items': 1},
    }


def _make_support(phase3a):
    return CollectionBootstrapSupport(
        lazy_loaded_dict_cls=_StubLazyDict,
        database_url='postgresql://stub',
        phase3a_databases=phase3a,
    )


# --- Finding 1: transient DB failure must not be cached permanently ---------

def test_empty_heritage_result_not_cached_permanently():
    """First call hits an error fallback (empty); after DB recovers the next
    call must return the real data, not the cached empty structure."""
    phase3a = _StubPhase3a([_empty_heritage(), _loaded_heritage()])
    support = _make_support(phase3a)

    first = support.get_cultural_heritage_database()
    assert first['statistics']['total_heritage_items'] == 0

    second = support.get_cultural_heritage_database()
    assert second['statistics']['total_heritage_items'] == 1
    assert len(second['heritage_items']) == 1


def test_loaded_heritage_result_is_cached():
    """A successful (non-empty) load is cached: the loader is not re-invoked."""
    phase3a = _StubPhase3a([_loaded_heritage()])
    support = _make_support(phase3a)

    support.get_cultural_heritage_database()
    support.get_cultural_heritage_database()
    assert phase3a.heritage_calls == 1


# --- Finding 2: herpetology fallback common name script/spelling ------------

def test_herpetology_common_name_is_pure_cyrillic():
    salamander = HERPETOLOGY_FALLBACK['specimens'][0]
    assert salamander['scientific_name'] == 'Salamandra salamandra'
    name = salamander['common_name_sr']
    # No Latin letters may appear inside the Cyrillic common name.
    latin = [ch for ch in name if 'a' <= ch.lower() <= 'z']
    assert latin == [], f"Latin characters leaked into Cyrillic name: {latin!r}"
    assert name == 'Обична саламандерица'


# --- Finding 3: meteorite statistics consistency ----------------------------

def test_meteorite_statistics_consistent_with_specimens():
    specimens = METEORITE_COLLECTION_DATABASE['specimens']
    stats = METEORITE_COLLECTION_DATABASE['statistics']

    assert stats['total_specimens'] == len(specimens)

    serbian = sum(1 for s in specimens if s.get('serbian_meteorite'))
    assert stats['serbian_meteorites'] == serbian
    assert stats['international_specimens'] == len(specimens) - serbian

    # No hand-maintained aggregate that contradicts the specimen data.
    if 'iron_meteorites' in stats or 'stony_meteorites' in stats or 'tektites' in stats:
        breakdown = (
            stats.get('iron_meteorites', 0)
            + stats.get('stony_meteorites', 0)
            + stats.get('tektites', 0)
        )
        assert breakdown == len(specimens)
