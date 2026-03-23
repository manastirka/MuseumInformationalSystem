# CLAUDE.md

## Project Overview
- Museum Information System — internal web app for the Natural History Museum in Belgrade
- Tech stack: Flask 2.3, PostgreSQL, SQLite (legacy), Jinja2 templates, Gunicorn, nginx, Redis (production)
- Key directories: templates/, data/, db/, scripts/, docs_archive/
- Main commands: `python3 -m pytest test_*.py`, `python3 app.py` (dev), `gunicorn --config gunicorn.conf.py wsgi:application` (prod)
- Remote: git@github.com:manastirka/MuseumInformationalSystem.git (branch: main)

## Git & GitHub Workflow

**IMPORTANT: Commit and push after every meaningful change.**

- After completing a feature, fix, or logical unit of work — commit immediately.
- After every commit, push to origin: `git push origin main`
- Commit messages should be concise and explain **why**, not just what.
- Use granular commits (one logical change per commit), not bulk dumps.
- Always run `python3 -m pytest test_*.py --tb=short` before committing. Only commit if no new failures.
- Never commit `.env`, `data/.mail_key`, or files matching `.gitignore`.
- Never force-push to main.

Commit format:
```
Short summary line (imperative mood)

Optional body explaining why this change was made.

Co-Authored-By: Claude Opus 4.6 (1M context) <noreply@anthropic.com>
```

## Core Principles
- **Plan before coding.** Understand the problem and design the solution before writing any code.
- **Minimal changes.** Only change what is necessary. Don't refactor, add features, or "improve" code beyond the scope of the task.
- **Root cause fixes.** Don't patch symptoms. Find and fix the actual root cause.
- **Simplicity first.** Prefer the simplest solution that works.

## Workflow
- **Always plan complex tasks.** For non-trivial work, enter Plan Mode before writing code.
- **Use sub-agents for big work.** Delegate independent subtasks to parallelize and keep context clean.
- **Verify before done.** No task is complete until:
  - Relevant tests pass (`python3 -m pytest test_*.py --tb=short`)
  - No regressions in existing behavior
  - Changes are committed and pushed to GitHub
- **Commit-push cycle:** After every task completion, commit + push. Don't let changes accumulate uncommitted.

## Bug Fixing Loop
When a bug is reported, do NOT jump to fix it:

1. **Write a reproducing test first.** Create a failing test that captures the bug.
2. **Delegate to sub-agents.** Spin up sub-agents to propose fixes. Each should make the test pass.
3. **Verify & commit.** Confirm test passes, commit the fix + test, push to GitHub.

## Security Rules
- **No f-string SQL.** All SQL must use parameterized queries (`%s`, `?`, `:param`). String concatenation of validated whitelist values is acceptable for ORDER BY/WHERE structure.
- **All API routes must have auth decorators.** No anonymous access to any `/api/` endpoint.
- **Destructive endpoints (delete, backup/restore) require `@admin_required`.**
- **No hardcoded credentials** in production code. Use environment variables.
- **CSRF exemptions** only for multipart FormData uploads and token-authenticated service endpoints.
- Never introduce injection vulnerabilities (SQL, XSS, command injection).

## Project Architecture
- `app.py` — main Flask app, 3700+ lines, 268+ routes (monolith, not yet blueprinted)
- `*_views.py` — 32 view modules (route handler implementations)
- `*_support.py` — business logic support modules
- `*_database.py` / `*_pg.py` — database access (SQLite + PostgreSQL dual support)
- `config.py` — environment-based configuration with Dev/Test/Production classes
- `security_utils.py` — auth decorators, password validation, rate limiting
- `image_api.py` — image management API (Blueprint, auth-protected)
- `image_storage_engine.py` — storage abstraction (local filesystem + S3 backends)
- `phase3a_databases.py` — PostgreSQL data access for Phase 3A migrated tables
- `module_access_support.py` — shared settings via PostgreSQL + file fallback

## Data Layer
- PostgreSQL is primary (65 tables in `museum_system` database)
- JSON files in `data/` are fallback/cache for small config (module_access, dashboard_preferences)
- SQLite databases for legacy mineral/bird data (being migrated)
- All new data should go to PostgreSQL, not JSON files

## Testing
- Run: `python3 -m pytest test_*.py --tb=short`
- Expected: 378+ passing, 1 flaky (test_startup_lazy_loading), 4 pre-existing errors (test_timesheet_integration)
- Key test files: `test_image_api_security.py`, `test_production_readiness.py`, `test_authorization_regressions.py`
- Write tests for security-critical changes before implementing fixes

## Production Deployment
- Gunicorn + nginx + systemd on local network
- `start_production.sh` requires: `REDIS_URL`, `MAIL_SETTINGS_ENCRYPTION_KEY`, `DATABASE_URL`, `SECRET_KEY`
- Default 1 worker (safe for memory-backed state)
- Background jobs run via separate `background_worker.py` process

## Style & Constraints
- Follow existing coding standards and naming conventions
- Match the style of surrounding code
- No hardcoded secrets, no `any` types, no disabling linters
- Don't add comments, docstrings, or type annotations to code you didn't change
- Serbian language in UI strings (Cyrillic), English in code/comments

## Forbidden Actions
- Never run destructive commands without explicit confirmation
- Never commit or push without user approval unless the task explicitly requires it
- Never force-push to main
- If a change could break the running production instance, flag it and wait
