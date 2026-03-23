# Root Folder Cleanup - 2026-03-18

## Goal

Reduce top-level clutter in the repository without deleting files that may still be operationally relevant.

## What Was Cleaned

### Archived to `backups/root_cleanup_20260318/source_backups`

- `app.py.backup.20251223_143958`
- `app.py.backup.phase3a`

### Archived to `backups/root_cleanup_20260318/generated_reports`

- migration validation JSON outputs
- mineral validation/correction/final/update report files
- `final_qa_report.json`
- `combined_inventory.csv`
- `mineral_backup_20260121_123118.json`

### Archived to `backups/root_cleanup_20260318/test_outputs`

- generated test reports (`test_report*.html`, `test_report*.json`)
- generated PDF test artifacts
- `test_results_20251224_120506.log`

### Archived to `backups/root_cleanup_20260318/stray_files`

- `=4.0.0`
- `hp-check.log`
- stray `npm`-named file with a non-printable prefix

### Moved to `docs_archive/root_notes_20260318`

- `BUTTON_LOCATION_GUIDE.html`
- `MIGRATION_PROGRESS.txt`
- `PROGRESS_2025-12-25.txt`
- `PROGRESS_2025-12-26.txt`
- `QUICK_START_MONDAY.txt`
- `SETUP_COMMANDS.txt`
- `UPGRADE_STATUS_2026-02-03.txt`
- `VIRTUAL_DEPOT_CONTEXT.txt`

### Removed

- root `__pycache__/`

## What Was Intentionally Left Alone

- application code modules
- active tests
- deployment/service files
- museum source documents (`.doc`, `.docx`, `.xls`, `.xlsx`, `.pdf`) that may still be business data
- data directories and dataset folders
- migration scripts and utility scripts, because “unused” cannot be proven safely from static inspection alone

## Result

The repository root is cleaner, with obvious backups, generated outputs, and loose session notes moved out of the main application surface while keeping recovery possible.

## Follow-up Script Reorganization

After the initial root cleanup, a second conservative pass moved only standalone utility scripts that:

- are not imported by the app
- are not referenced by the active root test suite
- do not import project-local modules themselves

Those scripts were reorganized into:

- `scripts/data_fixes`
- `scripts/analysis`
- `scripts/assets`
- `scripts/downloads`
- `scripts/import_export`
- `scripts/migration`
- `scripts/reporting`
- `scripts/testing`

Scripts that still import local project modules or are more likely to be operationally coupled were intentionally left at the repository root.

## Verification

- `python3 -m unittest test_startup_lazy_loading.py test_authorization_regressions.py test_timesheet_route_refactor.py`
- Result: `Ran 258 tests`, `OK`

## Follow-up Relic Archival

After a dependency and deployment-reference audit, a final conservative archival pass moved likely relics out of the repository root into:

- `backups/root_cleanup_20260318/relic_candidates`

Moved files:

- `museum-system.service.new`
- `museum-system.service.simple`
- `museum-system.service.updated`
- `timesheet_full_system.py`
- `word_export_ultra_fast.py`
- `database_migrations.py`
- `setup_employees.py`

Why these were moved:

- they are not part of the current app import graph from `app.py`, `wsgi.py`, or the active root test suite
- the service variants are superseded alternates, while `museum-system.service` remains the active root service file
- the Python files appear to be older standalone implementations, migration helpers, or legacy support files rather than current app runtime dependencies

This pass intentionally did not move manual admin tools such as `museum_control_center.py`, nor runtime deployment files such as `gunicorn.conf.py` and `museum-system.service`.
