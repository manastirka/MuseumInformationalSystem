# Phase 2 Database Migration Plan

**Date**: December 24, 2025  
**Goal**: Consolidate all active SQLite data sources into a single PostgreSQL database to unlock enterprise features (concurrency, replication, auditing, full-text search, PostGIS).

---

## 1. Current Data Landscape (Audit)

| Dataset | Path | Tables | Approx. Rows | Notes |
| --- | --- | --- | ---: | --- |
| Mineral inventory | `PrirodnjackiMuzej/prirodnjacki_muzej.sqlite` | `minerali`, `rruff_*` | 2,621 minerals | Mixed Serbian column names, timestamps as TEXT |
| Mineral reference list | `PrirodnjackiMuzej/museum_db.sqlite` | `min_list` | 1,158 | Reference/properties per mineral |
| Bird ringing records | `data/bird_ringing.db` | `bird_ringing` | 157,115 | Heavy read/write load, lat/long stored as TEXT |
| Inventory book | `data/inventory_book.db` | `inventory_book` | 4,031 | Additional revision columns |
| Timesheet system | `localSQLtesting/museum_timesheet.db` | `users`, `zaposleni`, `radna_lista[_dan]`, `user_activity_log` | 42 staff | Currently standalone auth source |
| Legacy/empty files | `museum.db`, `museum_system.db`, backups | — | — | Candidates for archival |

**Implications**
- Multiple SQLite files block cross-dataset queries and consistent backups.
- Column naming varies (Serbian/English mix, spaces) making ORM integration difficult.
- Sensitive data (users) duplicated in SQLite unrelated to central auth logic.

---

## 2. Target PostgreSQL Schema (Draft)

```sql
CREATE DATABASE museum_system ENCODING 'UTF8' TEMPLATE template0;
\c museum_system;

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS pgcrypto;
CREATE EXTENSION IF NOT EXISTS postgis;

CREATE TABLE departments (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT now()
);

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email CITEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    salt TEXT NOT NULL,
    full_name TEXT NOT NULL,
    role TEXT NOT NULL CHECK (role IN ('admin','employee','curator','viewer')),
    department_id INTEGER REFERENCES departments(id),
    position TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT now()
);

CREATE TABLE minerals (
    id SERIAL PRIMARY KEY,
    inventory_number VARCHAR(50) UNIQUE,
    name TEXT,
    acquisition_method TEXT,
    acquisition_date DATE,
    input_date TIMESTAMPTZ,
    input_by TEXT,
    donor TEXT,
    identifier TEXT,
    notes TEXT,
    location TEXT,
    card_locality TEXT,
    bibliography_flag BOOLEAN,
    quantity INTEGER,
    created_at TIMESTAMPTZ DEFAULT now(),
    updated_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE bird_species (
    id SERIAL PRIMARY KEY,
    species_name TEXT UNIQUE NOT NULL
);

CREATE TABLE bird_ringing_records (
    id BIGSERIAL PRIMARY KEY,
    ring_number TEXT,
    species_id INTEGER REFERENCES bird_species(id),
    age SMALLINT,
    sex TEXT,
    location TEXT,
    coordinates GEOGRAPHY(Point, 4326),
    coordinate_accuracy TEXT,
    event_date DATE,
    event_time TIME,
    status TEXT,
    ringer TEXT,
    notes TEXT,
    raw_json JSONB,
    created_at TIMESTAMPTZ DEFAULT now()
);
CREATE INDEX bird_ringing_geo_idx ON bird_ringing_records USING GIST(coordinates);

CREATE TABLE inventory_entries (
    id SERIAL PRIMARY KEY,
    inventory_number TEXT UNIQUE,
    name TEXT,
    locality TEXT,
    quantity TEXT,
    acquisition_info TEXT,
    collector TEXT,
    notes TEXT,
    sheet TEXT,
    row_number INTEGER,
    category TEXT,
    revisited BOOLEAN DEFAULT FALSE,
    physical_location TEXT,
    revision_date DATE,
    created_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE timesheet_entries (
    id BIGSERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    work_date DATE NOT NULL,
    project TEXT,
    hours NUMERIC(4,2),
    notes TEXT,
    created_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE audit_log (
    id BIGSERIAL PRIMARY KEY,
    table_name TEXT NOT NULL,
    record_id BIGINT,
    action TEXT NOT NULL,
    old_values JSONB,
    new_values JSONB,
    performed_by INTEGER REFERENCES users(id),
    performed_at TIMESTAMPTZ DEFAULT now(),
    ip_address INET
);
CREATE INDEX audit_table_idx ON audit_log(table_name, record_id);
```

---

## 3. Migration Approach

1. **Provision PostgreSQL**
   - Create managed instance or local Docker (14.7+), enable extensions listed above.
   - Configure credentials in `.env` (`DATABASE_URL=postgresql://user:pass@host:port/museum_system`).

2. **Schema Deployment**
   - Store SQL above as `db/schema.sql`.
   - Apply via `psql -f db/schema.sql`.

3. **Data Extraction**
   - Use Python/SQLite to fetch records in batches (1,000 rows) to avoid memory spikes.
   - Normalize column names (e.g., `"Inv. broj"` → `inventory_number`).
   - Parse dates (Serbian locales) using `datetime.strptime`.
   - Convert lat/long strings to floats before constructing PostGIS POINT.

4. **Transformation Logic**
   - Maintain mapping dictionaries for enumerations (sex, status, acquisition methods).
   - Deduplicate emails before inserting into `users`.
   - Derive `bird_species` table by distinct species names.

5. **Loading**
   - Use `psycopg` COPY for large tables (`bird_ringing_records`, `inventory_entries`).
   - Wrap each dataset in a transaction; log failures per batch.
   - Record counts before/after, compare to SQLite `COUNT(*)`.

6. **Validation**
   - Spot-check 10 random records per table.
   - Run aggregate queries (e.g., SUM, MIN/MAX dates) to confirm parity.
   - Keep SQLite read-only until sign-off.

7. **Application Updates**
   - Introduce SQLAlchemy models or repository layer targeting PostgreSQL.
   - Update `config.py` to prefer Postgres when `DATABASE_URL` is set.
   - Remove fallback SQLite paths once migrated.

**Artifacts committed so far**
- `db/schema.sql` – run via `psql -f db/schema.sql "$DATABASE_URL"` to provision tables, including the `staging_bird_ringing` helper.
- `scripts/migrate_to_postgres.py` – invoke with `python scripts/migrate_to_postgres.py --dataset bird_ringing --batch-size 2000` after setting `DATABASE_URL`; additional dataset handlers will follow the same pattern.

---

## 4. Work Breakdown & Next Actions

| Task | Owner | ETA | Notes |
| --- | --- | --- | --- |
| Finalize PostgreSQL infrastructure (DB, network, backups) | DevOps | 0.5 day | Include monitoring/alerting |
| Commit `db/schema.sql` + migration script skeleton | App Team | 0.5 day | Use Alembic or raw SQL |
| Build `scripts/migrate_to_postgres.py` with batch ETL | Backend | 1–2 days | Uses `sqlite3` + `psycopg` |
| Dry-run migration (no writes) to CSV | Backend | 0.5 day | Validate transforms |
| Full migration + validation | Backend + QA | 1 day | Document verification steps |
| Update Flask app to use Postgres | Backend | 1 day | SQLAlchemy recommended |
| Regression testing (auth, minerals, library, reports) | QA | 1–2 days | Utilize existing manual suites |

**Dependencies**
- Production-ready Phase 1 security baseline (complete).
- PostgreSQL credentials and network access.

**Risks & Mitigations**
- *Large bird_ringing table slows COPY*: stream via COPY FROM STDIN to keep under memory limits.
- *Mixed locales/dates*: define parsers with fallback logging; store raw JSON for auditing.
- *Downtime*: run migration while app stays on SQLite; switch only after verification.

---

## 5. Deliverables Checklist

- [ ] `db/schema.sql` applied to Postgres
- [ ] `scripts/migrate_to_postgres.py` completed
- [ ] Migration logs archived (`logs/migration_<timestamp>.log`)
- [ ] Validation report (counts, checksum, spot checks)
- [ ] App configuration updated (`DATABASE_URL`, disabling SQLite usage)
- [ ] Documentation updated (`README.md`, `CURRENT_SYSTEM_STATE.md`)
- [ ] Phase 2 sign-off meeting scheduled

Once these items are complete, the system will be positioned for **Phase 3** (application refactor + advanced monitoring) using the consolidated PostgreSQL backend.

---

## Operational Runbook (Draft)

1. **Provision schema**
   ```bash
   export DATABASE_URL=postgresql://user:pass@host:5432/museum_system
   psql "$DATABASE_URL" -f db/schema.sql
   ```
2. **Stage data per dataset**
   ```bash
   python scripts/migrate_to_postgres.py --dataset bird_ringing --batch-size 2000
   python scripts/migrate_to_postgres.py --dataset minerals --batch-size 1000
   python scripts/migrate_to_postgres.py --dataset inventory --batch-size 1000
   ```
   *(Timesheet migration placeholder will follow the same convention.)*
3. **Promote into production tables**
   ```bash
   psql "$DATABASE_URL" -f db/promote_from_staging.sql
   ```
4. **Validate counts**
   ```bash
   sqlite3 data/bird_ringing.db "select count(*) from bird_ringing;"
   psql "$DATABASE_URL" -c "select count(*) from bird_ringing_records;"
   # Repeat for minerals/inventory and compare
   ```
5. **Update application configuration**
   - Set `DATABASE_URL` in `.env`.
   - Switch Flask data access layer to PostgreSQL (SQLAlchemy/psycopg).
6. **Regression testing**
   - Run manual smoke tests (login, dashboards, data-heavy reports).
   - Execute automated tests (add/extend PyTest suites once DB layer refactored).

Document outcomes for each step in `logs/migration_<timestamp>.log` and capture screenshots/results to include with Phase 2 sign-off.
