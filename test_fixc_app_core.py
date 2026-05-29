"""Phase C app-core hardening: reproducing test for the bilja fallback aliasing.

LOW-severity finding (data-integrity): in the import-failure branch the six
BILJA_*_DATABASE globals were each assigned `dict(_empty_bilja)`. `dict()` is a
SHALLOW copy, so all six globals shared the SAME inner `'specimens'` list and the
SAME `'metadata'`/`'statistics'` dict objects. An in-place mutation of one
collection's empty `specimens` list would silently bleed into the other five.

This test drives exactly the except branch (by poisoning app.py's own
`import bilja_collections_db`) and asserts the six fallback globals are mutually
independent objects: mutating one collection's `specimens`/`metadata`/`statistics`
must NOT affect the others.
"""

import os
import subprocess
import sys
import textwrap

os.environ.setdefault('FLASK_ENV', 'testing')
os.environ.setdefault('SECRET_KEY', 'test-secret')
os.environ.setdefault('REDIS_URL', '')
os.environ.setdefault('SESSION_TYPE', 'filesystem')
os.environ.setdefault('SESSION_FILE_DIR', '/tmp/museum-test-c-app-core')

REPO_ROOT = os.path.dirname(os.path.abspath(__file__))

BILJA_GLOBALS = [
    'BILJA_KENOZOJSKE_INVERTEBRATE_DATABASE',
    'BILJA_HYDROBIOIDEA_RADOMAN_DATABASE',
    'BILJA_SUVOZEMNI_PUZEVI_PAVLOVIC_DATABASE',
    'BILJA_OPSTA_ZBIRKA_MOLLUSCA_DATABASE',
    'BILJA_SKOLJKE_TADIC_DATABASE',
    'BILJA_RECENTNI_MORSKI_MEKUSCI_DATABASE',
]


def test_bilja_fallback_globals_are_independent_objects():
    """Each fallback bilja global must own a distinct specimens/metadata/statistics."""
    names = repr(BILJA_GLOBALS)
    script = textwrap.dedent(
        f"""
        import os
        import sys

        os.environ.setdefault('FLASK_ENV', 'testing')
        os.environ.setdefault('SECRET_KEY', 'test-secret')
        os.environ.setdefault('REDIS_URL', '')
        os.environ.setdefault('SESSION_TYPE', 'filesystem')
        os.environ.setdefault('SESSION_FILE_DIR', '/tmp/museum-test-c-app-core')

        # Pre-import the early importers so they cache a real reference and
        # are not re-imported during `import app`.
        import collection_registry  # noqa: F401
        import collection_management_views  # noqa: F401

        # Poison only future fresh imports so app.py's own
        # `import bilja_collections_db` raises ImportError, driving exactly the
        # except branch under test.
        sys.modules['bilja_collections_db'] = None

        import app  # must not raise

        names = {names}
        dbs = [getattr(app, n) for n in names]

        # Distinct inner objects per collection (no aliasing).
        spec_ids = {{id(d['specimens']) for d in dbs}}
        meta_ids = {{id(d['metadata']) for d in dbs}}
        stat_ids = {{id(d['statistics']) for d in dbs}}
        assert len(spec_ids) == len(dbs), 'specimens lists are aliased'
        assert len(meta_ids) == len(dbs), 'metadata dicts are aliased'
        assert len(stat_ids) == len(dbs), 'statistics dicts are aliased'

        # In-place mutation of one must not bleed into the others.
        dbs[0]['specimens'].append({{'leaked': True}})
        dbs[0]['metadata']['leaked'] = True
        dbs[0]['statistics']['leaked'] = 1
        for d in dbs[1:]:
            assert d['specimens'] == [], 'specimens mutation bled across collections'
            assert d['metadata'] == {{}}, 'metadata mutation bled across collections'
            assert d['statistics'] == {{}}, 'statistics mutation bled across collections'

        print('FALLBACK_INDEPENDENT_OK')
        """
    )
    child_env = dict(os.environ)
    child_env.update({
        'FLASK_ENV': 'testing',
        'SECRET_KEY': 'test-secret',
        'REDIS_URL': '',
        'SESSION_TYPE': 'filesystem',
        'SESSION_FILE_DIR': '/tmp/museum-test-c-app-core',
    })
    child_env.pop('DATABASE_URL', None)
    result = subprocess.run(
        [sys.executable, '-c', script],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        env=child_env,
    )
    assert result.returncode == 0, (
        'bilja fallback globals are aliased (shallow dict copy).\n'
        f'STDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}'
    )
    assert 'FALLBACK_INDEPENDENT_OK' in result.stdout
