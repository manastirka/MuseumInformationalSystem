# Подизање радне машине од нуле

Овај документ настао је 16.08.2026, кад је кућни рачунар постао друга dev
машина и испало да свеж клон репоа **не може да пусти тест свиту** — падало
је 27 тестова, ниједан због грешке у коду. Све је било окружење или подаци
којих нема у гиту.

Провера да је документ тачан: пратећи само ове кораке, на потпуно новој
машини свита иде **1929 прошло / 0 палих**.

---

## 1. Системски пакети

```bash
sudo apt-get install -y \
    postgresql postgresql-postgis postgresql-postgis-scripts \
    redis-server python3-tk nodejs npm \
    build-essential python3-venv git
```

Зашто баш ови — сваки је откривен тако што је без њега нешто пало:

| пакет | без њега пада |
|---|---|
| `postgresql-postgis` | 44 каскадне грешке при учитавању шеме (гео табеле траже тип `geography`) |
| `redis-server` | `test_collection_registry` — подиже апликацију у продукцијској конфигурацији, која тражи Redis за сесије |
| `python3-tk` | 3 фајла `test_*_control_center.py` — `museum_control_center.py` увози `tkinter` |
| `nodejs` | `test_revizija_bezbednost::test_xss_payload_izlazi_escapovan_iz_modala` |

## 2. PostgreSQL

Локалне везе иду без лозинке (као на dev машини). У `pg_hba.conf`:

```
local   all   all                trust
host    all   all  127.0.0.1/32  trust
host    all   all  ::1/128       trust
```

па `sudo systemctl reload postgresql`.

Затим роле. **Обе су потребне** — `aleksandarlukovic` зато што је
хардкодована као подразумевани корисник у `DATABASE_URL` у ~10 фајлова
(`mineral_database_pg.py`, `timesheet_postgres.py`, `conftest.py`, …).
То је ставка техничког дуга; док стоји, свака машина мора да има ту ролу.

```bash
sudo -u postgres createuser -s "$USER"
sudo -u postgres createuser -s aleksandarlukovic
```

## 3. Репо и окружење

```bash
git clone git@github.com:manastirka/MuseumInformationalSystem.git MuseumInfoSystem
cd MuseumInfoSystem
python3 -m venv venv
./venv/bin/pip install -r requirements.txt
```

## 4. Тест база

```bash
./venv/bin/python scripts/seed_test_db.py --recreate --execute
```

Скрипта ради три ствари: направи базу изнова, учита шему из
`tests/fixtures/schema_baseline.sql`, и упише минималне сид податке
(4 роле, 2 одељења, 5 корисника, 3 профила — све синтетичко).

**Зашто шема из fixture-а, а не миграцијама:** `deploy/run_migrations.py`
не уме да сагради базу од нуле. Миграција `001` претпоставља да табеле већ
постоје и пада са `relation "timesheet_reports" does not exist` — миграције
надограђују шему коју је првобитно направила апликација. Fixture је снимак
те шеме са свим примењеним миграцијама.

**Зашто `schema_migrations` остаје празна:** три теста у
`test_revizija_operativa.py` проверавају заштитне механизме CLI-ја
(`apply` без `--execute`, погрешно име базе, без `--database`) и активирају
се само ако постоји нешто непримењено. Њихов сопствени коментар то и каже.
Ако пустиш `--baseline`, `apply` враћа „Nothing to apply", провере се не
активирају и та три теста падну.

### Ако икад буде требало обновити fixture

Сними га на машини са **најстаријим** PostgreSQL-ом у флоти:

```bash
pg_dump --schema-only --no-owner --no-privileges -d museum_system_test \
    > tests/fixtures/schema_baseline.sql
```

Смер важи само тако. Снимак са PostgreSQL-а 18 садржи
`SET transaction_timeout = 0`, што 16 не познаје и одбија цео фајл;
обрнуто ради без проблема. Тренутно: dev (fedora) 16.11, кућа 18.4 —
дакле fixture се прави **на dev-у**.

## 5. Провера

```bash
./venv/bin/python -m pytest test_*.py -q
```

Очекивано: **1929 прошло, 0 палих, 17 прескочених**.
(На dev машини 1937 прошло / 9 прескочених — разлика су само условни
прескоци, не падови.)

---

## Шта ово НЕ покрива

- **`.env`** — свако окружење има свој, не путује кроз гит. За саму свиту
  није потребан; `conftest.py` поставља безбедан default на `_test` базу.
- **Медији** (`static/img/`, `static/images/`, `static/map_tiles/`, ~1.9 GB)
  и подаци збирки (`Bilja/`, `Sanja/`, `data/arhiva/`) — путују rsync-ом.
  Без њих апликација ради, само у логу пише `Collection unavailable`.
  Изузетак су две placeholder слике по 4 KB, које **јесу** у гиту јер их
  код тражи по имену.
- **QA свита у прегледачу** (cypress/playwright/k6) — тражи покренут сервер
  и додатне кредненцијале, види `docs/qa_automation.md`.

## Правило које је извучено из целог овог посла

**Ако га код или тест отвара по имену, он је извор — иде у гит.**

Четири фајла су „радила" на dev машини само зато што леже ту неверзионисана:
`systemd_start.sh`, `museum-system.service`, и две placeholder слике. Ниједан
се није видео као проблем годинама, јер нико никад није направио свеж клон.
Исто важи и за стање базе: свита је зависила од ручно направљених корисника
на једној машини. Отуд ова скрипта и овај документ.
