# ANALIZA MIS aplikacije — jul 2026.

**Spoljna revizija koda** — Museum Information System, Prirodnjački muzej Beograd.
Flask + PostgreSQL 18, gunicorn + nginx, ~38 korisnika pred širim rollout-om.

## Metoda

Revizija je rađena isključivo čitanjem koda na DEV mašini (commit `4369612`, grana
`main`), bez izmena i bez merenja pod opterećenjem. Pet nezavisnih pregleda —
arhitektura, bezbednost, performanse, kvalitet, UX doslednost — svaki nad punim
repoom (~272 `.py` fajla u korenu, `blueprints/` sa 21 modulom, ~100 Jinja šablona,
`migration/` + `db/`). Svaka tvrdnja nosi referencu fajl:linija; tvrdnje o
ponašanju pod opterećenjem označene su kao procena i traže `EXPLAIN ANALYZE` /
load test za potvrdu.

Opšti utisak, pošteno: **sistem je znatno zreliji nego što bi se očekivalo za
interni alat ove veličine** — bezbednosno jezgro je čvrsto, startup je promišljeno
lazy, migracije imaju pravi runner, a regresiona test-disciplina je stvarna.
Glavni rizici pred rollout su: (1) propusna moć serviranja slika kroz 4 sinhrona
workera, (2) „dva izvora istine" obrasci koji tiho maskiraju kvarove baze,
(3) odsustvo audit traga van radnih listi, i (4) nedoslednost UX obrazaca koja će
sa 38 korisnika generisati nepotrebne pozive podršci.

---

## 1. ARHITEKTURA

### 1.1 app.py vs blueprints — migracija ruta ZAVRŠENA, migracija stanja NIJE

Pohvala koja se mora izreći: **`app.py` (1609 linija) više nema nijednu
`@app.route` rutu.** Sve rute žive u `blueprints/*.py` kao tanki adapteri koji
pozivaju `*_views.py` biblioteke (npr. `blueprints/timesheet.py:16-24` →
`timesheet_admin_views.render_timesheet_app`). To je velika, uspešno izvedena
refaktor operacija.

Ali `app.py` je postao **globalni servisni lokator sa deljenim stanjem**:

- JSON persistencija i globalni keševi: `load_module_access`/`save_module_access`
  (`app.py:901-943`), `load_vehicles`/`save_vehicles` (`app.py:1324-1355`),
  `_MUSEUM_VEHICLES_CACHE`, `MODULE_ACCESS`, `DASHBOARD_PREFERENCES`
  (`app.py:948-961`, `1360-1385`).
- **Najbolniji dug: cirkularna zavisnost `import app as museum_app` — 127 pojava
  u 52 fajla.** Blueprintovi rade lazy import unutar tela funkcije
  (`blueprints/timesheet.py:22`, `blueprints/collections.py:37`) upravo zato što
  bi import na vrhu modula pukao. Dekompozicija tako nije stvarna — sve i dalje
  prolazi kroz `app`.
- Dvostruki mehanizam registracije blueprintova: 5 ručno (`app.py:382-386`), 15
  kroz `register_standard_blueprints` (`app.py:387-405`), plus alias sloj
  `BLUEPRINT_ALIAS_ENDPOINTS` (`app_blueprint_support.py:5-140`) koji drži stare
  `url_for` pozive u šablonima živim.
- `app.py:90-142` uvozi ~35 `*_views.py` modula od kojih je većina redundantna
  (blueprintovi ih sami uvoze).

**Redosled rešavanja** (svaki korak samostalno isporučiv):
1. izdvojiti deljeno stanje u `app_state.py` / Flask extension **[M]**;
2. zameniti `import app as museum_app` sa `current_app.extensions[...]` ili DI **[L]**;
3. ujednačiti registraciju blueprintova na jedan poziv **[S]**;
4. postepeno gasiti alias sloj prepravkom `url_for` u šablonima **[M]**.

Support sloj (`app_*_support.py`, 23 modula) je, suprotno očekivanju, **prava
dekompozicija**: moduli primaju zavisnosti kao parametre (DI, npr.
`app.py:917-926`) i međusobno se skoro ne uvoze — nema ciklusa. Zamerka je
prekomerna isečenost: `app_data_support.load_vehicles_data` (`:75-82`) samo
prosleđuje na `vehicle_data_support.load_vehicles` — četiri fajla za jedan
`SELECT`.

### 1.2 Dva izvora istine — inventar (traženo: ima li ih još; ima)

Ponavljajući antipattern: **čitanje ide „PG-prvo pa JSON fallback", a pisanje u
samo JEDAN izvor.** Kad se raziđu, čitanje tiho servira pogrešan izvor.

| # | Oblast | Izvori | Stanje |
|---|--------|--------|--------|
| 1 | Dozvole modula | PG `shared_settings` + `data/module_access.json` | **DOBRO rešeno** — write-through u OBA (`module_access_support.py:129-155`); referentni obrazac. Ostaje problem tihog fallback-a pri DB grešci (v. §4.2) |
| 2 | Vozila i rezervacije | PG `vehicles` + `data/museum_vehicles.json` | **NAJGORI slučaj** — čitanje pada tiho na JSON (`vehicle_data_support.py:17-31`), `save_vehicles` piše SAMO JSON (`:34-42`), PG upis na drugom mestu bez fallback-a (`vehicle_depot_views.py:134-171`); INSERT puni 9 od 17 kolona šeme (`db/schema_vehicles.sql:5-25`) |
| 3 | Inventarska knjiga | SQLite `data/inventory_book.db` (`config.py:74`) + git-trackovan `data/inventory_book.json` + PG | TRI izvora; `inventory_reconciliation.py:31` ih miri ručno u kodu |
| 4 | Minerali / RRUFF | `mineral_database.py` (SQLite) vs `mineral_database_pg.py` (SQLAlchemy) — bira se na startu (`app.py:37-42`) | dve kompletne paralelne implementacije istog API-ja |
| 5 | Timesheet | SQLAlchemy `NullPool` za čitanje (`timesheet_repository.py:43-50`) vs psycopg pool za upise (`timesheet_employee_views.py:109-121`) | nije JSON-vs-PG nego dva DB drajvera nad istom bazom |

**Sistemski rizik:** `git ls-files` pokazuje da su commitovani
`data/module_access.json`, `data/museum_vehicles.json`, `data/library_database.json`,
`data/exhibitions.json`, `data/news.json`, `data/employee_directory.json`,
`data/dashboard_preferences.json`, `data/inventory_book.json`,
`data/image_database.json`. Svaki deploy može da vrati **zastarelu kopiju** koja
onda maskira PG kad god baza zakuca. `.db` fajlovi su ispravno ignorisani
(`.gitignore:129`) — JSON fallback fajlovi treba da dobiju isti tretman.

### 1.3 Konzistentnost modula — isti problem, četiri rešenja

Pristup bazi: fototeka koristi zreo context-manager sa auto commit/rollback
(`fototeka_views.py:524`, semantika u `postgres_service.py:112-124`); timesheet
dva stack-a (SQLAlchemy + psycopg); **vozila su jedini modul** koji vozi ručni
`cursor/commit/close` kroz `phase3a_databases.get_db_connection()`
(`vehicle_depot_views.py:136-159`) — i to **bez rollback-a na izuzetak**, pa se u
pool može vratiti konekcija u prekinutoj transakciji.

Auth provere su, nasuprot tome, **uzorno dosledne**: `@login_required` (189×),
`@admin_required` (62×), `@module_access_required` (59×) iz `security_utils` na
svim blueprintovima, bez ad-hoc `session.get` provera. Fototeka ima opravdan
row-level auth podsistem (`fototeka_views.py:109-160`) — jedini paralelni.

---

## 2. BEZBEDNOST

**Ukupna ocena: iznenađujuće zrela. Nema visokih nalaza sa web površine.**
Kontekst: interni LAN sistem — ali provere ispod važe i za kompromitovan nalog.

### 2.1 Potvrđeno dobro (bez potrebne akcije)

- **Lozinke:** bcrypt cost 12 (`security_utils.py:101,119`) sa auto-migracijom
  legacy SHA-512 hešova pri sledećem loginu (`security_utils.py:144-191`).
- **Sesije:** `SESSION_COOKIE_SECURE/HTTPONLY/SAMESITE=Lax` (`config.py:36-38`),
  `session.clear()` pri loginu protiv session fixation (`core_app_views.py:231-246`),
  Redis sesije u produkciji, Talisman + HSTS (`app.py:573-597`).
- **Fail-closed produkcija:** `ProductionConfig.init_app` diže `RuntimeError` ako
  nema `SECRET_KEY`, ako je fallback auth uključen, ako sesije nisu Redis
  (`config.py:206-237`). Retko viđena disciplina.
- **`fallback_auth_support.py` NIJE backdoor:** aktivan samo uz
  `ENABLE_FALLBACK_AUTH` (u produkciji hard-zabranjen, `config.py:213-214`),
  poziva se samo kad primarni auth nije dostupan (`core_app_views.py:200-210`),
  `secrets.compare_digest`, blokira poznatu bootstrap lozinku.
- **CSRF:** `CSRFProtect(app)` globalno (`app.py:358`), exempt lista
  centralizovana i mala (`app_blueprint_support.py:237-243`), AJAX pokriven
  `X-CSRFToken` headerom iz `base.html:9` meta taga.
- **SQL injection: nema ranjivih tačaka.** Sve dinamičke konstrukcije interpolišu
  isključivo imena tabela/kolona iz belih listi (`bilja_collections_db.py:253,257`,
  `fototeka_views.py:1226`), vrednosti idu kroz `%s` parametre. Provereno i
  `mineral_search_utils.py` (LIKE vrednost je parametar, ne konkatenacija).
- **Upload:** fototeka proverava ekstenziju + limit 200MB + PIL `verify()` magic
  bytes + poseban potpis kontejnera za RAW (`fototeka_views.py:698-717`), path
  containment `.resolve()` pre `send_file` (`~:1332-1410`), write-once `O_EXCL`.
  Dokumenti: whitelist + 25MB + `secure_filename` (`document_library_views.py:52-57,182-186`).
- **Rate limiting dvoslojno:** login 5/min po IP-u (`app_blueprint_support.py:248-249`)
  + lockout po nalogu 5 pokušaja → 30 min, Redis-deljen (`security_utils.py:194-339`).
- **Tajne:** `.env` van gita, `.env.example` samo placeholder-i; nema hardkodovanih
  tajni u web kodu.

### 2.2 Nalazi

- **SREDNJE — CSP `'unsafe-inline'` + `'unsafe-eval'` u `script-src`**
  (`app.py:506-517`; nonce namerno isključen `app.py:587-589` jer 89 šablona nosi
  inline skripte). Ovo XSS zaštitu svodi na escaping u šablonima. Realan uticaj
  ublažen LAN kontekstom, ali je defense-in-depth rupa; rešenje je vezano za UX
  dug (izmeštanje inline JS-a, §5).
- **NISKO** — `edit_bilja_item` bez `@login_required`, zaštićen posredno kroz
  module-access konfiguraciju (`blueprints/collections.py:276`, `:18-32`);
  funkcionalno zatvoreno, ali dodati dekorator radi doslednosti.
- **NISKO** — CSRF-exempt `image_api.upload_image` oslonjen samo na `SameSite=Lax`
  (`app_blueprint_support.py:238`).
- **NISKO** — desktop admin alat: predvidljiva privremena lozinka `"Muzej2024!"`
  (`museum_control_center.py:2676`) i dinamički `set_clause` u SQL-u (`:353`) —
  van web površine, ali srediti.

---

## 3. PERFORMANSE

Ključni kontekst: `gunicorn.conf.py:16-17` — `worker_class='sync'`, `WORKERS=4`
iz `.env`. **Najviše 4 istovremena HTTP zahteva; peti čeka.** `preload_app=True`,
`timeout=120`.

### 3.1 Top rizici kad 38 korisnika bude aktivno (rangirano)

1. **Serviranje slika kroz sinhrone workere — prvo će zaboleti.**
   `fototeka_views.py:1356-1379` `serve_derivat`: svaki thumbnail je zaseban HTTP
   zahtev kroz Flask `send_file`, sa svojim DB upitom (`_fetch_photo` +
   `can_view_photo`). Galerija sa `GALLERY_PAGE_SIZE=60` (`fototeka_views.py:77`)
   = do 60 zahteva koji drže worker tokom celog transfera. Isto važi za thumbnaile
   u tabelama zbirki (`collection_management_views.py:731-749`). Nekoliko
   istovremenih korisnika u fototeci zasićuje sva 4 slota → ceo sajt „visi".
   Rešenje: nginx `X-Accel-Redirect` za fajlove + `gthread` worker klasa.
2. **Spori zahtevi × 4 slota:** ZIP export (`fototeka_views.py:1434`, svesno
   limitiran na 300 fajlova/2GB — pohvala — ali gradi se sinhrono u zahtevu),
   veliki upload sa sha256, inventarska knjiga (dole) — svaki drži 1/4 kapaciteta
   do 120 s.
3. **Iscrpljenje DB konekcija u špicu:** dva nezavisna pool-a po workeru
   (`postgres_service.py:50-74` max 10 + `timesheet_postgres.py:49-65` max 10)
   × 4 workera = do 80, plus `NullPool` tranzijenti mineral/RRUFF
   (`mineral_database_pg.py:26`, `rruff_database_pg.py:26` — **nova TCP konekcija
   po upitu**). PG default `max_connections=100`. Uskladiti brojke; razmotriti
   PgBouncer ili jedan pool.
4. **Inventarska knjiga u RAM po zahtevu:**
   `collection_management_views.py:1085-1100` učitava CELU knjigu, sortira u
   Pythonu, pa seče `items[start:end]` — paginacija koja skalira sa veličinom
   knjige, ne stranice. `InventoryReconciliation()` se instancira po zahtevu.
5. **N+1 upisi:** `timesheet_admin_views.py:1241-1259, 1289-1308` — INSERT
   notifikacije u petlji po izveštaju (laka zamena `executemany`). Plus
   funkcionalni `LOWER(email)` JOIN-ovi bez indeksa na izrazu
   (`timesheet_postgres.py:914`) — sada nebitno (38 redova), proveriti `EXPLAIN`.

### 3.2 Šta je dobro rešeno (pohvale su zaslužene)

- **Lazy startup regresiono zaštićen** (`test_startup_lazy_loading.py`): auth,
  timesheet repo, module-access, biblioteka — sve lazy. Veliki JSON (25MB
  `yugoslav_localities_data.json`) i FastSAM modeli se NE učitavaju u web proces.
- **Obrada slika izmeštena:** derivati/fixity u zasebnom systemd worker-u
  (`fototeka_worker.py`, `deploy/mis-fototeka-worker.service`); background poslovi
  zaštićeni env + fajl-lock (`app.py:1503-1509`).
- **Poolovi su lazy → bezbedni uz `preload_app` + fork** (`postgres_service.py:58`).
- **Indeksna pokrivenost hot tabela je dobra** (`migration/019_fototeka.sql:134-139`,
  `002:30-33`, `005:15-16`); glavne liste su batchovane sa `ANY(%s)`
  (`timesheet_admin_views.py:394-405`, `fototeka_views.py:2282-2318`), ne N+1.
- **Promišljena HTTP cache zaglavlja za slike** (`fototeka_views.py:1382-1392`:
  javne `private, max-age=3600`, privatne `no-store`, `Vary: Cookie`).

Kandidati za indekse kad fototeka poraste: parcijalni `WHERE obrisana=FALSE` +
kompozit sa `datum_snimanja` (`fototeka_views.py:479,532`); `pg_trgm` GIN za
ILIKE pretragu (`:482`).

---

## 4. KVALITET

### 4.1 Testovi — brojka zavarava, disciplina je ipak stvarna

155 `test_*.py` fajlova, ~1470 test funkcija. Od toga 78 fajlova su regresioni
po tri runde bug-fix-eva (fix/fixb/fixc) — **ta disciplina je stvarna i retka**,
svaka oblast je prošla kroz tri talasa imenovane regresije.

Ali: **51 od 155 fajlova gradi ručni `FakeCursor`/`FakeConnection`**
(`test_zahtevi_approval_framework.py:64-92`) koji poredi substring SQL-a i vraća
skriptovane redove — pogrešno ime kolone, tip ili JOIN **ne bi oborili test**.
Pravi Postgres dodiruje manjina testova. `TestingConfig` gasi CSRF i rate-limit
(`config.py:186-193`). Nema centralnog `conftest.py` ni `pytest.ini` — env se
postavlja ad hoc na vrhu svakog fajla.

**Kritično a tanko pokriveno:** `postgres_auth.py` (bez direktnih testova),
`deploy/run_migrations.py` (nepokriven runner koji nosi šemu produkcije),
finansije (`travel_finance_views.py` samo kroz FakeConnection — sume se ne
verifikuju nad pravim numeric tipovima). Upload je, nasuprot tome, dobro pokriven
(`test_media_hardening.py`, `test_image_api_security.py`, 7 faza fototeke).

### 4.2 Error handling — gde greške umiru tiho

~614 `except Exception` u ne-test kodu, 18 bare `except:`. Najgori po posledici:

- **`module_access_support.py:64-67` → `:110-126`** — na DB grešku
  `_load_db_json_setting` vrati `None` uz samo `warning`, pa se dozvole modula
  **tiho vrate na default** (`deepcopy(default_value)`); `_db_setting_failure_cache`
  (`:43-45`) to stanje još i produžava. DB blip = pogrešne dozvole bez ijednog
  ERROR loga i bez traga. **Ovo je pojedinačno najopasnije tiho gutanje u sistemu.**
- **`collection_access_support.py:310-312, 479-481, 608-610`** — tri
  `except Exception → return []`: kustos na DB grešku vidi „nemam nijednu zbirku"
  umesto poruke o kvaru.
- Bare `except:` u `mineral_database.py:208`, `crystal_structure_databases.py:186,223,525`,
  `museum_control_center.py:1168,1207,1287` (hvataju i `KeyboardInterrupt`).
- `mail_client.py` — većina `except: pass` je legitiman IMAP cleanup; problematični
  su tihi `return ''/None/False` pri parsiranju (`:862,893,1314`), posledica kozmetička.

**Uzor kako treba:** `fototeka_worker.py:42-70` — `logger.exception` + backoff,
`logger.critical` + `sys.exit(1)` kad libvips nedostaje.

### 4.3 Logovanje i audit trag

Setup je solidan: `RotatingFileHandler` 10MB×5 + stream u journald
(`app.py:203-214`), opcioni Sentry sa PII sanitizacijom (`observability.py:24-72`),
opcioni OpenTelemetry. `print()` umesto logger-a nije sistemski problem (samo
CLI blokovi).

**Ozbiljna praznina: audit trag postoji samo za timesheet**
(`migration/004_timesheet_audit_log.sql` — uzorno dizajniran: akcija, ko, kada,
old/new vrednosti, IP). Za brisanja u zbirkama, promene dozvola, izmene
korisnika, finansijske zapise — **ne može se rekonstruisati ko je šta uradio**.
Promena dozvola kroz tihi fallback iz §4.2 ne ostavlja nikakav trag. Pred širi
rollout ovo prelazi iz „lepo bi bilo" u „potrebno".

### 4.4 Migracije

Runner `deploy/run_migrations.py` je dobar: `schema_migrations` tabela,
transakcija + rollback + stop na grešci, `status/baseline/mark` komande; SQL
migracije pisane defanzivno (`IF NOT EXISTS`). Zamerke: **duplirani numerički
prefiksi** (`002_exhibition_planner` vs `002_timesheet_schema_fixes`; `005` tri
puta) — redosled zavisi od abecede sufiksa; nema down/rollback putanje;
`db/schema_*.sql` se ručno dopunjuju mimo migracija (`db/schema_vehicles.sql`
sadrži kolone iz `migration/014`, a `migration/016` postoji baš da pomiri legacy
constraint) plus one-off zakrpe u `db/` van numerisanog sistema
(`fix_meteorite_schema.sql`, `promote_from_staging.sql`).

### 4.5 Zavisnosti i higijena

- Poznati dug „fale psutil/xlrd/openpyxl" je **polurešen**: svi su u
  `requirements.lock` (pinovan, 105 linija), ali `requirements.txt` i dalje ne
  navodi `openpyxl` ni `xlrd` — instalacija iz `txt` puca na Excel funkcijama.
  Dva fajla su međusobno nesaglasna (opet dva izvora istine).
- **`app.py:235-239` radi `sys.path.insert` za `localSQLtesting/` i
  `PrirodnjackiMuzej/`** (drugi projekat sa sopstvenim venv-om!) — strani
  direktorijumi utiču na runtime import resolution; rizik senčenja modula.
- Git repo je relativno čist (`.env`, `.db`, `venv/` ispravno van gita); **radni
  direktorijum nije** — `.xlsx`/`.doc` dokumenti, dva FastSAM modela po ~24MB,
  ~20 `.sh` skripti u korenu, zaostali fajl `[200~`.

---

## 5. UX DOSLEDNOST

Najjači deo frontenda: **token sistem tema u `static/css/main.css` je izuzetno
temeljan** — kompletan `:root` skup, puni override za dark/contrast, tri stilske
varijante × 4 akcenta, pre-render skript protiv FOUC-a (`base.html:22-104`),
rešen `<option>` kontrast u tamnoj temi (`main.css:198-207`). Centralizovani
flash sloj, `secureFetch` CSRF omotač i `escapeHtml` u `base.html` — dobra
zajednička infrastruktura. `fototeka` je jedini modul sa čisto izdvojenim JS-om
(`static/js/fototeka*.js`) — uzor za ostale.

Problem je što slój sadržaja tu infrastrukturu zaobilazi:

- **Potvrda brisanja na TRI načina:** nativni `confirm()` (39 poziva u 27
  fajlova), custom modal (`exhibition_planner.html:997-1004`), i — najgore —
  **bez ikakve potvrde: masovno brisanje pošte**
  (`admin_mail_client.html:1590` `deleteMultiSelected()` briše odmah).
- **Povratne poruke na ČETIRI načina:** flash (ispravno), `alert()` (149 poziva),
  dve **nekompatibilne** `showToast` implementacije sa obrnutim potpisom
  (`employee_timesheet.html:798` `showToast(type, message)` vs
  `admin_manage_access.html:293` `showToast(message, type)`), plus
  `exhibition_planner.html:1920` poziva `showToast` koji u tom fajlu **nije ni
  definisan** (tihi no-op).
- **Boja submit dugmeta:** `btn-success` vs `btn-primary` vs `btn-info`
  (`admin_add_book.html:245`) — heritage-shell mapira prva dva na isti gradijent,
  ali `btn-info` ostaje vidno drugačiji.
- **Hardkodovane boje: ~2540 heks vrednosti u 87 šablona sa inline `<style>`**
  (najteži: `admin_maps.html` 451, `employee_timesheet.html` 134) — zaobilaze
  tokene, pa dark/contrast teme ne mogu da ih pokriju.
- **Mixed-script greške (4):** najozbiljnija
  `admin_add_heritage_item.html:299` — `<option value="заштićено">` (ćirilica +
  latinica u `value` atributu → potencijalno funkcionalni bag pri poređenju na
  serveru); zatim `admin_exhibitions_database.html:216,471`,
  `museum_terminology.html:436,677`. Transliterator ove reči ne može ispravno
  konvertovati.
- **Pristupačnost:** 11 `<img>` bez `alt` (`fototeka_fotografija.html:37`,
  `admin_qr_labels.html:63`…), 27 `onclick` na div/span bez keyboard pristupa
  (`_image_upload_modal.html:175`), ~289 `<label>` bez `for=`, `outline:none`
  u 8 šablona. Breadcrumb u samo 7 od ~100 šablona.
- **Mrtav kod:** `notificationBell()`/`mailNotifier()` definisani dvaput u
  `base.html` (`:110-187` i `:1766-1844`); `escapeHtml` redefinisan u 4 šablona
  iako postoji globalni.

---

## TOP 10 PRIORITIZOVANIH PREDLOGA

Trud: S = do dana, M = do nedelje, L = više nedelja. Rizik = šta se rizikuje ako
se NE uradi pre/tokom šireg rollout-a.

| # | Šta | Zašto | Trud | Rizik |
|---|-----|-------|------|-------|
| 1 | **Slike kroz nginx, ne kroz Flask**: `X-Accel-Redirect` za `serve_derivat`/`serve_raw` (`fototeka_views.py:1356-1410`) + prelaz na `gthread` workere | 60 thumbnail zahteva po galeriji × 4 sync workera = ceo sajt „visi" čim nekoliko ljudi otvori fototeku; ovo je prvo što će 38 korisnika osetiti | M | **visok** |
| 2 | **Ukinuti tihi fallback dozvola**: `module_access_support.py:64-67,110-126` — na DB grešku dizati/ERROR-logovati i služiti poslednju poznatu vrednost, nikad tiho default | DB blip trenutno menja dozvole svih korisnika bez traga; bezbednosno-operativna bomba sa odloženim paljenjem | S | **visok** |
| 3 | **Vozila na write-through obrazac** (kao `module_access_support.py:129-155`) + **`data/*.json` fallback fajlove u `.gitignore`** | Jedini modul gde deploy može tiho vratiti stare podatke a kvar baze se maskira JSON-om; usput ispraviti INSERT koji puni 9/17 kolona i dodati rollback (`vehicle_depot_views.py:136-171`) | M | **visok** |
| 4 | **Globalni audit trag** po uzoru na `timesheet_audit_log` (`migration/004`): brisanja u zbirkama, promene dozvola, izmene korisnika, finansije | Sa 38 korisnika „ko je ovo obrisao?" postaje nedeljno pitanje; trenutno je odgovor nemoguć | M | srednji–visok |
| 5 | **Ujednačiti destruktivne akcije i poruke**: potvrda na bulk-delete pošte (`admin_mail_client.html:1590`), jedan `showToast` sa fiksnim potpisom u `base.html`, ispraviti 4 mixed-script greške (posebno `value="заштićено"`, `admin_add_heritage_item.html:299`) | Nepovratno brisanje bez pitanja + nekonzistentne poruke = izgubljeni podaci i pozivi podršci od prvog dana rollout-a | S | srednji |
| 6 | **Uskladiti DB konekcije**: `POSTGRES_POOL_MAX_SIZE`×workers×2 pool-a vs PG `max_connections`; mineral/RRUFF sa `NullPool` (`mineral_database_pg.py:26`) prevesti na zajednički pool | U špicu do 80+ konekcija uz limit 100; NullPool plaća TCP connect po upitu | S | srednji |
| 7 | **`requirements.txt` uskladiti sa `requirements.lock`** (dodati `openpyxl`, `xlrd==1.2.*` uz komentar zašto pin) — i zvanično zatvoriti stavku 2 poznatog tehničkog duga | Instalacija iz `txt` daje sistem koji puca na Excel import/export; dva nesaglasna izvora istine za zavisnosti | S | srednji |
| 8 | **Očistiti runtime putanje**: ukloniti `sys.path.insert` za `localSQLtesting/` i `PrirodnjackiMuzej/` (`app.py:235-239`) i mrtve top-level importe (`app.py:90-142`) | Strani projekat sa sopstvenim venv-om u import putanji produkcije = rizik senčenja modula koji se debaguje danima | S | srednji |
| 9 | **Faza 1 razbijanja god-objecta**: izdvojiti deljeno stanje iz `app.py` u `app_state.py`, pa postepeno gasiti `import app as museum_app` (127 pojava) | Svaka buduća izmena plaća porez cirkularne zavisnosti; bez ovoga se dugovi 1–8 krpe ali ne rešavaju | L | srednji |
| 10 | **Inventarska knjiga na SQL paginaciju** (`collection_management_views.py:1085-1100`) + `executemany` za notifikacije (`timesheet_admin_views.py:1241-1259`) | RAM/CPU po zahtevu raste sa veličinom knjige, ne stranice; drži worker slot | M | nizak–srednji |

**Van liste, ali za plan:** CSP bez `unsafe-inline` (vezano za izmeštanje inline
JS-a iz 89 šablona — prirodno se radi uz stavku 5, modul po modul, po uzoru na
fototeku); konsolidacija mineral/RRUFF SQLite-vs-PG dvokoloseka [L]; migracije —
uvesti trocifrene jedinstvene prefikse i test za `run_migrations.py` [S];
postepeno uvođenje integracionog test sloja nad pravim Postgresom umesto `FakeCursor`.

---

*Revizija: Claude (Fable 5), spoljni pregled koda, jul 2026. Bez izmena koda;
sve reference proverljive na commit-u `4369612`.*
