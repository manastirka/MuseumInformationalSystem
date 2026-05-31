# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview
Museum Information System — internal web app for the Natural History Museum in Belgrade (Природњачки музеј у Београду). Manages mineral/biological collections, employee timesheets, maps, scientific papers, QR labels, mail, and more.

- **Stack:** Flask 2.3, PostgreSQL (primary), SQLite (legacy), Jinja2, Gunicorn, nginx, Redis (production)
- **Remote:** git@github.com:manastirka/MuseumInformationalSystem.git (branch: main)

## Commands

```bash
# Dev server
python3 app.py

# Production
gunicorn --config gunicorn.conf.py wsgi:application

# Run all tests
python3 -m pytest test_*.py --tb=short

# Run a single test file
python3 -m pytest test_image_api_security.py --tb=short

# Run a single test
python3 -m pytest test_image_api_security.py::TestImageAPISecurity::test_upload_requires_auth --tb=short
```

**Test baseline:** 510 tests collected. 1 flaky (`test_startup_lazy_loading`), 4 pre-existing errors (`test_timesheet_integration`). Run tests before committing — no new failures allowed.

## Architecture

### Route Registration Pattern
`app.py` (~1300 lines) is the main Flask app. Routes are served through **15 blueprints** in `blueprints/` plus 2 directly registered (`image_api`, `archive_signature_bp`):

```
app.py  →  app_blueprint_support.register_standard_blueprints()
               → blueprints/collections.py, blueprints/admin.py, ...
```

Bulk registration and legacy endpoint aliasing happen via `app_core_support.py` and `app_blueprint_support.py`.

### Blueprint → Views → Support Pattern
Each blueprint in `blueprints/*.py` defines routes and delegates to `*_views.py` helper modules:

```
blueprints/collections.py          # routes + decorators
  → collection_management_views.py # rendering/formatting helpers
  → import app as museum_app       # shared state (collections data, helper functions)
```

**Important:** Blueprints use `import app as museum_app` (deferred import inside route functions) to access global state from `app.py`. This avoids circular imports.

### Module Layers
- `blueprints/*.py` — route definitions (15 modules: admin, chat, collections, content, core, mail, maps, media, mineral_science, projects, qr, science, timesheet, travel_finance, vehicles)
- `*_views.py` (32 files) — view helper functions called by blueprints
- `*_support.py` (21 files) — business logic
- `*_database.py` / `*_pg.py` (12 files) — data access (SQLite + PostgreSQL dual implementations)
- `security_utils.py` — auth decorators: `@login_required`, `@admin_required`, `@module_access_required(key)`
- `config.py` — environment-based config classes (Dev/Test/Production)

### Data Layer
- PostgreSQL is primary (65+ tables in `museum_system` database)
- `mineral_database.py` (SQLite) vs `mineral_database_pg.py` (PostgreSQL) — selected at import time based on `DATABASE_URL` env var
- JSON files in `data/` — fallback/cache for small config (module_access, dashboard_preferences)
- All new data must go to PostgreSQL, not JSON files

### Image System
- `image_api.py` — Blueprint with auth-protected endpoints for image CRUD
- `image_storage_engine.py` — storage abstraction (local filesystem + S3 backends)
- `image_database_manager.py` — image metadata in PostgreSQL

## Git & GitHub Workflow

**Commit and push after every meaningful change.**

- Always run tests before committing. Only commit if no new failures.
- After every commit: `git push origin main`
- Never commit `.env`, `data/.mail_key`, or files matching `.gitignore`.
- Never force-push to main.

Commit format:
```
Short summary line (imperative mood)

Optional body explaining why this change was made.

Co-Authored-By: Claude Opus 4.6 (1M context) <noreply@anthropic.com>
```

## Security Rules
- **No f-string SQL.** All SQL must use parameterized queries (`%s`, `?`, `:param`). Whitelisted string concat is OK for ORDER BY/WHERE structure.
- **All API routes must have auth decorators.** No anonymous access to `/api/` endpoints.
- **Destructive endpoints (delete, backup/restore) require `@admin_required`.**
- **CSRF exemptions** only for multipart FormData uploads and token-authenticated service endpoints.

## Production Deployment
- Gunicorn + nginx + systemd on local network
- `start_production.sh` requires: `REDIS_URL`, `MAIL_SETTINGS_ENCRYPTION_KEY`, `DATABASE_URL`, `SECRET_KEY`
- Default 1 worker (safe for memory-backed state)
- Background jobs: separate `background_worker.py` process

## Style
- Serbian language in UI strings (Cyrillic), English in code/comments
- Match surrounding code style — don't introduce new patterns
\n## Rile addendum (2026-04-17) — Claude Code best practices\n- Drži sesije kratke i fokusirane; context window je najvažniji resurs.\n- U promptu daj proverljiv cilj (testovi/lint/build/screenshot poređenje), ne samo opis zadatka.\n- Radi redosledom: explore -> plan -> implement, posebno za rizične izmene.\n- Navedi konkretne fajlove, ograničenja i postojeće obrasce iz koda.\n- Traži root-cause fix (ne maskiranje grešaka), pa obavezno verifikuj rezultat komandom.\n

## Rile local sandbox addendum (2026-04-17)
- MuseumInfoSystem fokus: prioritet su integritet podataka eksponata i bezbedan rad sa eksportom/importom.
- Za izmene servisa: pre promene napiši restart+status check korak i potvrdi health endpoint/ključne funkcije.
