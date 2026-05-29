"""Reproducing test for the app-core cluster bug.

Bug: when `import bilja_collections_db` fails at the app.py module-level
`try` (line ~1198), the except branch logs a warning and assigns empty
fallback dicts but never binds `_bilja_db`. The module-level registration
loop (`for ... in _bilja_db.COLLECTIONS.items()`) then references `_bilja_db`
unconditionally, raising `NameError` and aborting Flask startup — defeating
the graceful-degradation fallback the except branch was written to provide.

We reproduce surgically: the modules that import `bilja_collections_db`
early in app.py's import chain (collection_registry / collection_management_views)
are imported first so they cache a real reference. We then poison
`sys.modules['bilja_collections_db'] = None` so that ONLY app.py's own
`import bilja_collections_db as _bilja_db` (executed later) raises ImportError,
driving exactly the except branch under test.
"""

import os
import subprocess
import sys
import textwrap

os.environ.setdefault('FLASK_ENV', 'testing')
os.environ.setdefault('SECRET_KEY', 'test-secret')
os.environ.setdefault('REDIS_URL', '')
os.environ.setdefault('SESSION_TYPE', 'filesystem')
os.environ.setdefault('SESSION_FILE_DIR', '/tmp/museum-test-app-core')

REPO_ROOT = os.path.dirname(os.path.abspath(__file__))


def test_app_imports_when_bilja_db_import_fails_at_app_level():
    """Importing app must succeed even if its own bilja import fails."""
    script = textwrap.dedent(
        """
        import os
        import sys

        os.environ.setdefault('FLASK_ENV', 'testing')
        os.environ.setdefault('SECRET_KEY', 'test-secret')
        os.environ.setdefault('REDIS_URL', '')
        os.environ.setdefault('SESSION_TYPE', 'filesystem')
        os.environ.setdefault('SESSION_FILE_DIR', '/tmp/museum-test-app-core')

        # Pre-import the early importers so they cache a real reference and
        # are not re-imported during `import app`.
        import collection_registry  # noqa: F401
        import collection_management_views  # noqa: F401

        # Now poison only future fresh imports of the module. Setting the
        # sys.modules entry to None makes `import bilja_collections_db` raise
        # ImportError, exactly mirroring an import-time dependency failure at
        # app.py's own import statement.
        sys.modules['bilja_collections_db'] = None

        import app  # must not raise

        # Graceful fallback must have produced empty bilja collections.
        assert app.BILJA_KENOZOJSKE_INVERTEBRATE_DATABASE == {
            'metadata': {}, 'specimens': [], 'statistics': {}
        }
        print('IMPORT_OK')
        """
    )
    # Hermetic env: the parent pytest process may have mutated os.environ
    # (e.g. another test sets FLASK_ENV='development'), which the child would
    # otherwise inherit and fail `import app` for an unrelated config reason.
    child_env = dict(os.environ)
    child_env.update({
        'FLASK_ENV': 'testing',
        'SECRET_KEY': 'test-secret',
        'REDIS_URL': '',
        'SESSION_TYPE': 'filesystem',
        'SESSION_FILE_DIR': '/tmp/museum-test-app-core',
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
        'app import failed when its bilja_collections_db import failed.\n'
        f'STDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}'
    )
    assert 'IMPORT_OK' in result.stdout
    assert 'NameError' not in result.stderr
