# CLAUDE.md — Museum Information System (MIS)

## Projekat

Flask + PostgreSQL aplikacija Prirodnjačkog muzeja u Beogradu (zbirke,
geoprostorni podaci/Leaflet, QR etikete, evidencija rada, finansije,
izložbe). U produkciji radi iza gunicorn + nginx na Fedora Serveru.

## Okruženja — gde se šta sme

| Uloga | Mašina | Napomena |
|---|---|---|
| **DEV** | stari server (`192.168.144.48`) | ovde se piše kod |
| **PROD** | `nhmb-srv01` (`192.168.144.194`) | aplikacija: `/opt/mis/app`, venv: `/opt/mis/venv`, servis: `mis.service`, podaci: `/data/mis`, noćni backup 02:30 |
| **GitHub** | `manastirka/MuseumInformationalSystem` | izvor istine |

**Kod putuje isključivo kroz git** (dev → GitHub → prod). Podaci putuju
rsync-om. Tajne (`.env`) ne putuju nikako — svako okruženje ima svoj.

**Grane (konsolidovano 2026-07-10):** `main` je JEDINA radna grana — i DEV
i PROD je prate; feature rad ide kratkoživućim granama koje se brišu posle
merge-a. `sol/rad` je radna grana codex worktree-a. Stare grane
(`fix/bug-audit-2026-05-29`, `feat/*`) su ugašene; istorija je sačuvana u
tagovima `arhiva/*` i snimku `~/grane-pre-konsolidacije.txt`.

## Pravila za Claude Code sesije

**Na DEV mašini** — puna sloboda: pisanje koda, refaktorisanje,
eksperimenti. Obavezno pri tom:
- `pytest test_*.py` mora biti zelen pre svakog commita (suite ima
  ~1040 testova; puna kolekcija bez argumenata hvata i 2 pokvarena
  skripta u `PrirodnjackiMuzej/` — ne koristiti);
- izmene šeme baze isključivo kroz migracije, nikad ručni `ALTER`;
- nove zavisnosti odmah u `requirements.txt`, sa verzijom;
- konfiguracija (putanje, kredencijali, SECRET_KEY) samo kroz `.env` /
  config — nikad hardkodovano u kodu;
- `.env`, `__pycache__`, lokalni podaci se ne commituju.

**Na PROD serveru** — isključivo uloga operatera:
- DOZVOLJENO: `deploy.sh`, čitanje logova (`journalctl -u mis`),
  `systemctl status/restart mis`, dijagnostika (uključujući čitanje koda).
- ZABRANJENO: menjanje koda direktno, pisanje u bazu mimo aplikacije,
  instaliranje paketa mimo `requirements.txt`, menjanje configa bez
  znanja korisnika.
- Ako `git pull --ff-only` odbije — STANI i prijavi korisniku: znači da
  je neko menjao kod na produkciji mimo procedure.

## Deploy procedura

1. Na DEV: `pytest` zelen → commit → push.
2. Označi verziju: `git tag prod-YYYY-MM-DD && git push --tags`
3. Na PROD: `sudo /usr/local/bin/deploy.sh`
   (skripta: backup → pull --ff-only → pip install → restart → smoke test)

**Rollback:** na PROD
`sudo -u mis git -C /opt/mis/app checkout <prethodni-tag>` +
`sudo systemctl restart mis`.

## Frontend i18n (језици)

Апликација је **само српска: ћирилица + латиница**. Енглески је *меко
уклоњен* (2026-07-08) — механизам је ту, али угашен.

**Механизам је client-side у `static/js/translator.js`, НЕ Flask-Babel.**
(Babel је иницијализован у `app.py`, али нема `translations/`/`.po`.)

- **Извор = ћирилица**, писана директно у Jinja шаблонима.
- **Латиница = аутоматска транслитерација** (`cyrToLat`). Нема речника —
  латиница стиже сама.
- **Додавање/измена текста:** упиши исправну ћирилицу у шаблон; латиница
  долази бесплатно. За српски **нема кључева** — не дира се `translator.js`.
  Пази на mixed-script словне грешке типа `изnad` (виде се на обе варијанте).
- **Динамички садржај (AJAX табеле, JS-рендер календар):** почетни прелаз је
  једнократан, али `MutationObserver` у `translator.js` наставља да примењује
  активни језик на накнадно убачене чворове. Нова JS-грађена компонента се
  покрива сама (осим ако је под `data-no-translate`).

**Енглески (дормантан, за евентуални повратак):**
- `enTranslations` + `translateToEnglish` остају у `translator.js`, неактивни.
- Укључени језици су на **два места**: `ENABLED_LANGS` (`translator.js`) и
  `UI_LANGUAGES` (`core_app_views.py`). Повратак EN = додај `'en'` у оба +
  врати `<li>` у `templates/base.html`.
- Сачувани `museum_lang=en` **чисто пада на ћирилицу** (нормализација на
  клијенту и серверу); `translateToEnglish` поклапа на **граници речи**, па
  нови EN кључеви морају бити пуне речи/фразе.

## Статички асети

`.gitignore`: `static/*` + `!static/css/` + `!static/js/`.

- **Изворни CSS/JS** (`static/css/`, `static/js/`) **иду кроз git** → стижу на
  прод обичним `deploy.sh` (`git pull`).
- **Бинарни/генерисани медиј** (`static/img/`, `static/images/`,
  `static/map_tiles/` ~1.9 GB) **НЕ иду у git** → путују rsync/data путем.
- Правило: нов **текстуални извор** → у `static/css`/`static/js` (git); нов
  **бинарни асет** → ван гита (rsync). `deploy.sh` нема rsync за `static/`.

## Poznati tehnički dug (popisano 2026-07-03)

Prvi zadaci za DEV sesije — na produkciji trenutno pokriveno
improvizacijama koje treba da postanu nepotrebne:

1. **Hardkodovane putanje** (`/home/aleksandarlukovic/...`) u kodu —
   prebaciti na config/env vrednosti. (Na prod pokriveno symlinkom.)
2. **requirements.txt nepotpun** — fale `psutil`, `xlrd`, `openpyxl`
   (na prod instalirani ručno; uskladiti fajl sa stvarnim uvozima).
3. **gunicorn.conf.py** hardkoduje korisnika — parametrizovati ili
   ukloniti (produkcija gunicorn parametre drži u systemd unitu).

Posle svake od ovih popravki: pytest, pa normalan deploy ciklus.
