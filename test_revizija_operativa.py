"""Ревизија 2026-08, батч 4 — оператива, деплој и опоравак.

Чувари за оперативне поправке:
  1. deploy.sh има PREV + trap rollback и smoke test на /healthz;
  2. /healthz СТВАРНО пада (503) кад је база недоступна — то је поента
     smoke testa, "/" враћа 200 и уз мртав PostgreSQL;
  3. run_migrations.py без --execute не мења базу; погрешан --database
     се одбија;
  4. requirements.txt и requirements.lock садрже pyvips и xlrd;
  5. nginx client_max_body_size >= MAX_CONTENT_LENGTH (иначе 413 пре Flask-а);
  6. systemd јединице у deploy/ не помињу имена која не постоје на
     продукцији (nhmb-srv01).
"""

import os
import re
import subprocess
import sys
from pathlib import Path

os.environ.setdefault('FLASK_ENV', 'testing')
os.environ.setdefault('SECRET_KEY', 'test-secret')
os.environ.setdefault('REDIS_URL', '')
os.environ.setdefault('SESSION_TYPE', 'filesystem')
os.environ.setdefault('SESSION_FILE_DIR', '/tmp/museum-test-operativa')

REPO = Path(__file__).resolve().parent
DEPLOY_SH = REPO / 'deploy.sh'


# --- 1. deploy.sh: rollback + pravi smoke test --------------------------------

def test_deploy_sh_sintaksno_ispravan():
    result = subprocess.run(['bash', '-n', str(DEPLOY_SH)],
                            capture_output=True, text=True)
    assert result.returncode == 0, result.stderr


def test_deploy_sh_ima_prev_trap_i_rollback():
    text = DEPLOY_SH.read_text(encoding='utf-8')
    assert re.search(r'^PREV=', text, re.M), 'nema PREV= snimka pre pull-a'
    assert re.search(r'trap\s+rollback\s+ERR', text), 'nema trap ... ERR'
    assert 'reset --hard "$PREV"' in text, 'rollback ne vraća kod na PREV'
    assert 'systemctl restart mis' in text, 'rollback ne restartuje servis'


def test_deploy_sh_smoke_ide_na_healthz_sa_retry_petljom():
    text = DEPLOY_SH.read_text(encoding='utf-8')
    assert '/healthz' in text, 'smoke test ne gađa /healthz'
    assert not re.search(r'curl[^\n]*127\.0\.0\.1:8000\s*$', text, re.M), \
        'smoke i dalje gađa goli gunicorn / umesto /healthz kroz nginx'
    assert re.search(r'for\s+_?\w*\s+in\s+\$\(seq', text), \
        'nema retry petlje (fiksni sleep nije smoke test)'


def test_deploy_sh_instalira_lock_i_sistemske_fajlove():
    text = DEPLOY_SH.read_text(encoding='utf-8')
    assert 'requirements.lock' in text, 'prod i dalje instalira nepinovan requirements.txt'
    assert 'daemon-reload' in text
    assert 'nginx -t' in text, 'nema nginx -t pre reload-a'
    assert 'logrotate' in text


def test_deploy_sh_ne_prepisuje_prod_autoritativne_fajlove():
    """Batč 7: repo kopije backup/restore skripti i nginx konfiga su
    rekonstrukcije po opisu — deploy sme samo da upozori na razliku,
    nikako da ih instalira preko prod primerka."""
    text = DEPLOY_SH.read_text(encoding='utf-8')
    for fajl in ('backup-nhmb.sh', 'restore-proba.sh', 'nginx_museum_prod.conf'):
        assert not re.search(rf'^\s*install\s[^\n]*{re.escape(fajl)}', text, re.M), \
            f'deploy.sh i dalje instalira {fajl} preko prod primerka'
    assert 'warn_if_differs' in text, \
        'deploy.sh ne poredi (diff) repo kopije sa živim fajlovima'
    assert re.search(r'diff -q "\$repo" "\$live"', text), \
        'deploy.sh ne radi diff repo naspram živog fajla'


def test_deploy_sh_rollback_vraca_nginx_konfig():
    text = DEPLOY_SH.read_text(encoding='utf-8')
    assert 'NGINX_PRE' in text, 'nema snimka nginx konfiga pre deploja'
    rollback_telo = text.split('rollback() {', 1)[1].split('\n}', 1)[0]
    assert 'NGINX_PRE' in rollback_telo and '$NGINX_CONF' in rollback_telo, \
        'rollback ne vraća nginx konfig na stanje pre deploja'


# --- 2. /healthz pada kad baza ne radi ----------------------------------------

def test_healthz_pada_kad_je_baza_nedostupna(monkeypatch):
    import app as museum_app
    import postgres_service

    def _baza_mrtva():
        raise RuntimeError('PostgreSQL nedostupan (simulacija pada)')

    monkeypatch.setattr(postgres_service, 'get_postgres_connection', _baza_mrtva)
    client = museum_app.app.test_client()
    resp = client.get('/healthz', base_url='https://localhost')
    assert resp.status_code == 503
    data = resp.get_json()
    assert data['status'] == 'degraded'
    assert data['db'] == 'error'


def test_healthz_zelen_kad_baza_radi():
    import app as museum_app

    client = museum_app.app.test_client()
    resp = client.get('/healthz', base_url='https://localhost')
    assert resp.status_code == 200
    assert resp.get_json()['db'] == 'ok'


# --- 3. run_migrations.py: dry-run podrazumevano ------------------------------

def _snimak_evidencije():
    """Sadržaj schema_migrations (None ako tabela ne postoji)."""
    import postgres_service
    conn = postgres_service.get_postgres_connection()
    try:
        cur = conn.cursor()
        cur.execute("SELECT to_regclass('public.schema_migrations') IS NOT NULL")
        if not cur.fetchone()[0]:
            return None
        cur.execute(
            "SELECT filename, applied_at FROM schema_migrations ORDER BY filename")
        return cur.fetchall()
    finally:
        conn.close()


def _run_migracije(*args):
    return subprocess.run(
        [sys.executable, 'deploy/run_migrations.py', *args],
        capture_output=True, text=True, cwd=REPO, env=os.environ.copy())


def _db_name():
    return os.environ['DATABASE_URL'].rsplit('/', 1)[-1].split('?')[0]


def test_run_migrations_bez_execute_sa_pending_vraca_nenulti_exit():
    """apply bez --execute uz bar jednu pending migraciju NE SME da vrati 0.

    Produkcijski deploy.sh (stara verzija, bez root pristupa da se menja)
    zove baš 'apply' bez --execute — nulti exit kod bi značio da je deploy
    uspeo dok nijedna migracija nije primenjena (tihi neuspeh).
    """
    import postgres_service
    pre = _snimak_evidencije()
    applied = {row[0] for row in (pre or [])}
    removed = None
    conn = postgres_service.get_postgres_connection()
    try:
        if not applied:
            # baza je već potpuno pending (uobičajeno za museum_system_test);
            # ništa dodatno ne treba forsirati.
            pass
        else:
            removed = sorted(applied)[0]
            cur = conn.cursor()
            cur.execute("DELETE FROM schema_migrations WHERE filename = %s", (removed,))
            conn.commit()

        pre_run = _snimak_evidencije()
        result = _run_migracije('apply')
        assert result.returncode != 0, \
            'apply bez --execute uz pending migracije mora da vrati nenulti exit'
        assert 'DRY RUN' in result.stdout
        assert _snimak_evidencije() == pre_run, \
            'apply bez --execute je promenio tabelu evidencije'
    finally:
        if removed is not None:
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO schema_migrations(filename) VALUES (%s) "
                "ON CONFLICT DO NOTHING", (removed,))
            conn.commit()
        conn.close()
    # Poredimo imena, ne vremena: povratni INSERT u finally bloku dobija novi
    # applied_at, pa bi poredjenje celih redova palo cim evidencija nije
    # prazna (a jeste cim neko pusti apply --execute nad test bazom).
    assert [red[0] for red in (_snimak_evidencije() or [])] == \
           [red[0] for red in (pre or [])]


def test_run_migrations_bez_execute_bez_pending_vraca_0():
    """Kad NEMA nijedne pending migracije, apply bez --execute vraća 0 —
    nema šta da padne."""
    import postgres_service
    pre = _snimak_evidencije()
    mark = _run_migracije('mark', '*.sql', '--execute', '--database', _db_name())
    assert mark.returncode == 0, mark.stdout + mark.stderr
    try:
        result = _run_migracije('apply')
        assert result.returncode == 0, result.stdout + result.stderr
        assert 'Nothing to apply' in result.stdout
    finally:
        conn = postgres_service.get_postgres_connection()
        try:
            cur = conn.cursor()
            pre_files = {row[0] for row in (pre or [])}
            cur.execute("SELECT filename FROM schema_migrations")
            for (f,) in cur.fetchall():
                if f not in pre_files:
                    cur.execute("DELETE FROM schema_migrations WHERE filename = %s", (f,))
            conn.commit()
        finally:
            conn.close()
    assert _snimak_evidencije() == pre


def test_run_migrations_pogresna_baza_se_odbija():
    pre = _snimak_evidencije()
    result = _run_migracije('apply', '--execute', '--database', 'mis_db')
    assert result.returncode != 0, \
        'apply --execute sa pogrešnim imenom baze mora da bude odbijen'
    assert 'ODBIJENO' in result.stdout
    assert _snimak_evidencije() == pre


def test_run_migrations_execute_bez_database_se_odbija():
    result = _run_migracije('apply', '--execute')
    assert result.returncode != 0
    assert 'ODBIJENO' in result.stdout



# --- 3b. run_migrations.py: sve ili ništa -------------------------------------
#
# Nalaz broj 1 u sva tri kruga avgustovske revizije: runner je commit-ovao
# svaki fajl posebno, pa je pad druge migracije ostavljao prvu u bazi dok se
# kod vraćao na stari SHA. Ovi testovi rade nad PRAVOM bazom (museum_system_test)
# sa privremenim MIGRATION_DIR-om, da se vidi šta je stvarno ostalo u šemi.

_ATOM_PRVA = '900_atomicnost_prva.sql'
_ATOM_DRUGA = '901_atomicnost_druga.sql'
_ATOM_TABELE = ('zz_atomicnost_prva', 'zz_atomicnost_druga')


def _ucitaj_runner():
    import importlib.util
    putanja = os.path.join(REPO, 'deploy', 'run_migrations.py')
    spec = importlib.util.spec_from_file_location('run_migrations_pod_testom', putanja)
    modul = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modul)
    return modul


def _tabela_postoji(ime):
    import postgres_service
    conn = postgres_service.get_postgres_connection()
    try:
        cur = conn.cursor()
        cur.execute("SELECT to_regclass(%s) IS NOT NULL", (f'public.{ime}',))
        return bool(cur.fetchone()[0])
    finally:
        conn.close()


def _ocisti_atomicnost():
    import postgres_service
    conn = postgres_service.get_postgres_connection()
    try:
        cur = conn.cursor()
        for t in _ATOM_TABELE:
            cur.execute(f"DROP TABLE IF EXISTS {t}")
        cur.execute("SELECT to_regclass('public.schema_migrations') IS NOT NULL")
        if cur.fetchone()[0]:
            cur.execute(
                "DELETE FROM schema_migrations WHERE filename IN (%s, %s)",
                (_ATOM_PRVA, _ATOM_DRUGA))
        conn.commit()
    finally:
        conn.close()


def _privremene_migracije(tmp_path, druga_sql):
    d = tmp_path / 'migration'
    d.mkdir()
    (d / _ATOM_PRVA).write_text(
        "CREATE TABLE zz_atomicnost_prva (id integer PRIMARY KEY);\n",
        encoding='utf-8')
    (d / _ATOM_DRUGA).write_text(druga_sql, encoding='utf-8')
    return d


def _evidencija_imena():
    return {red[0] for red in (_snimak_evidencije() or [])}


def test_run_migrations_druga_pada_prva_se_vraca(tmp_path, monkeypatch, capsys):
    """Pad druge migracije NE SME da ostavi prvu u bazi ni u evidenciji,
    a --applied-log mora da ostane prazan (deploy.sh po njemu odlučuje da li
    je šema ispred koda)."""
    rm = _ucitaj_runner()
    d = _privremene_migracije(
        tmp_path,
        "CREATE TABLE zz_atomicnost_druga (id integer PRIMARY KEY);\n"
        "SELECT * FROM tabela_koja_ne_postoji_zz_atomicnost;\n")
    monkeypatch.setattr(rm, 'MIGRATION_DIR', d)
    dnevnik = tmp_path / 'primenjeno.log'
    _ocisti_atomicnost()
    try:
        kod = rm.cmd_apply(True, _db_name(), applied_log=str(dnevnik))
        izlaz = capsys.readouterr().out
        assert kod == 1, izlaz
        assert not _tabela_postoji('zz_atomicnost_prva'), \
            'prva migracija je OSTALA u bazi iako je druga pala'
        assert not _tabela_postoji('zz_atomicnost_druga')
        assert not (_evidencija_imena() & {_ATOM_PRVA, _ATOM_DRUGA}), \
            'evidencija tvrdi da je nešto primenjeno, a šema je vraćena'
        assert not dnevnik.exists() or dnevnik.read_text(encoding='utf-8') == '', \
            '--applied-log sme da sadrži samo ono što je stvarno commit-ovano'
        # poruke tek posle stanja baze: stanje je dokaz, poruka je objašnjenje
        assert f'FAILED on {_ATOM_DRUGA}' in izlaz
        assert 'NIJE primenjena' in izlaz
        assert 'ROLLBACK: vraćeno' in izlaz, 'poruka mora da kaže da je i prva vraćena'
        assert _ATOM_PRVA in izlaz.split('ROLLBACK: vraćeno', 1)[1]
    finally:
        _ocisti_atomicnost()


def test_run_migrations_obe_prolaze_u_jednoj_transakciji(tmp_path, monkeypatch, capsys):
    rm = _ucitaj_runner()
    d = _privremene_migracije(
        tmp_path, "CREATE TABLE zz_atomicnost_druga (id integer PRIMARY KEY);\n")
    monkeypatch.setattr(rm, 'MIGRATION_DIR', d)
    dnevnik = tmp_path / 'primenjeno.log'
    _ocisti_atomicnost()
    try:
        kod = rm.cmd_apply(True, _db_name(), applied_log=str(dnevnik))
        izlaz = capsys.readouterr().out
        assert kod == 0, izlaz
        assert 'in one transaction' in izlaz
        assert _tabela_postoji('zz_atomicnost_prva')
        assert _tabela_postoji('zz_atomicnost_druga')
        assert {_ATOM_PRVA, _ATOM_DRUGA} <= _evidencija_imena()
        assert dnevnik.read_text(encoding='utf-8').split() == [_ATOM_PRVA, _ATOM_DRUGA]
    finally:
        _ocisti_atomicnost()


def test_run_migrations_odbija_fajl_sa_sopstvenim_commit_vec_u_dry_runu(
        tmp_path, monkeypatch, capsys):
    """COMMIT unutar fajla bi presekao zajedničku transakciju — runner to
    mora da odbije bez --execute, da svita i probni deploj to uhvate."""
    rm = _ucitaj_runner()
    d = _privremene_migracije(
        tmp_path,
        "BEGIN;\nCREATE TABLE zz_atomicnost_druga (id integer PRIMARY KEY);\nCOMMIT;\n")
    monkeypatch.setattr(rm, 'MIGRATION_DIR', d)
    _ocisti_atomicnost()
    try:
        kod = rm.cmd_apply(False, None)
        izlaz = capsys.readouterr().out
        assert kod == 1, izlaz
        assert 'ODBIJENO' in izlaz
        assert f'{_ATOM_DRUGA}:1: BEGIN;' in izlaz
        assert f'{_ATOM_DRUGA}:3: COMMIT;' in izlaz
        assert not _tabela_postoji('zz_atomicnost_prva')
        assert not _tabela_postoji('zz_atomicnost_druga')
    finally:
        _ocisti_atomicnost()


def test_problemi_za_transakciju_prepoznaje_samo_stvarne_naredbe():
    rm = _ucitaj_runner()
    assert rm.problemi_za_transakciju(
        "-- BEGIN;\nDO $$\nBEGIN\n  PERFORM 1;\nEND;\n$$;\n"
        "-- ne sme CREATE INDEX CONCURRENTLY\n") == []
    assert rm.problemi_za_transakciju("BEGIN;\nSELECT 1;\nCOMMIT;\n") == \
        [(1, 'BEGIN;'), (3, 'COMMIT;')]
    assert rm.problemi_za_transakciju(
        "CREATE INDEX CONCURRENTLY ix ON t (a);\n") == \
        [(1, 'CREATE INDEX CONCURRENTLY')]
    assert rm.problemi_za_transakciju("  start transaction ;\n") == \
        [(1, 'start transaction ;')]


def test_sve_migracije_u_repou_mogu_u_jednu_transakciju():
    """Nijedan fajl u migration/ ne sme da nosi sopstveni BEGIN/COMMIT niti
    naredbu koju PostgreSQL odbija u transakcionom bloku."""
    rm = _ucitaj_runner()
    losi = []
    for ime in rm.discover_migrations():
        sql = (rm.MIGRATION_DIR / ime).read_text(encoding='utf-8')
        for linija, naredba in rm.problemi_za_transakciju(sql):
            losi.append(f'{ime}:{linija}: {naredba}')
    assert losi == [], '\n'.join(losi)


# --- 4. zavisnosti: pyvips i xlrd u OBA fajla ---------------------------------

def test_requirements_sadrze_pyvips_i_xlrd():
    txt = (REPO / 'requirements.txt').read_text(encoding='utf-8')
    lock = (REPO / 'requirements.lock').read_text(encoding='utf-8')
    for naziv, sadrzaj in (('requirements.txt', txt), ('requirements.lock', lock)):
        assert re.search(r'^pyvips', sadrzaj, re.M), \
            f'{naziv} nema pyvips (fototeka worker ne bi startovao)'
        assert re.search(r'^xlrd', sadrzaj, re.M), \
            f'{naziv} nema xlrd (mineral_science_views -> local_rruff_data)'


# --- 5. nginx limit >= MAX_CONTENT_LENGTH -------------------------------------

def _nginx_body_limit_bytes(conf):
    match = re.search(r'client_max_body_size\s+(\d+)([kKmMgG]?)\s*;',
                      conf.read_text(encoding='utf-8'))
    assert match, f'{conf} nema client_max_body_size'
    mult = {'': 1, 'k': 1024, 'm': 1024 ** 2, 'g': 1024 ** 3}
    return int(match.group(1)) * mult[match.group(2).lower()]


def test_nginx_limit_pokriva_max_content_length():
    from config import Config
    flask_limit = int(Config.MAX_CONTENT_LENGTH)
    for conf in (REPO / 'nginx_museum.conf',
                 REPO / 'deploy' / 'nginx_museum_prod.conf'):
        nginx_limit = _nginx_body_limit_bytes(conf)
        assert nginx_limit >= flask_limit, (
            f'{conf.name}: client_max_body_size {nginx_limit} < '
            f'MAX_CONTENT_LENGTH {flask_limit} — nginx bi vraćao 413 pre Flask-a')


# --- 6. systemd jedinice = stvarna imena sa produkcije ------------------------

# Provereno na nhmb-srv01 2026-08-10 (systemctl list-units/list-timers).
PROD_JEDINICE = {
    'backup-nhmb.service', 'backup-nhmb.timer',
    'restore-proba.service', 'restore-proba.timer',
    'fototeka-import.service', 'fototeka-import.timer',
    'fototeka-fixity.service', 'fototeka-fixity.timer',
    'mis.service', 'mis-fototeka-worker.service',
}
SISTEMSKE = {'postgresql.service'}


def test_deploy_jedinice_ne_pominju_nepostojeca_imena():
    deploy_dir = REPO / 'deploy'
    fajlovi = sorted(deploy_dir.glob('*.service')) + sorted(deploy_dir.glob('*.timer'))
    assert fajlovi, 'deploy/ nema systemd jedinica?'
    isporucene = {f.name for f in fajlovi}
    dozvoljena = PROD_JEDINICE | SISTEMSKE | isporucene
    pominjanje = re.compile(r'[\w@%.-]+\.(?:service|timer)\b')
    losa = []
    for fajl in fajlovi:
        for line in fajl.read_text(encoding='utf-8').splitlines():
            line = line.strip()
            if not line or line.startswith(('#', ';')):
                continue
            for ime in pominjanje.findall(line):
                # instanca šablona (mis-alarm@%n.service) -> šablon (mis-alarm@.service)
                normalizovano = re.sub(r'@[^.]+\.', '@.', ime)
                if normalizovano not in dozvoljena:
                    losa.append(f'{fajl.name}: {ime}')
    assert not losa, (
        'systemd jedinice pominju imena koja ne postoje na produkciji:\n  '
        + '\n  '.join(losa))
