"""`flask populate-lokaliteti` / `flask export-lokaliteti` — sifarnik lokaliteta.

Alat "Локалитети" je do sada bio runtime-agregat nad `minerals.card_locality`;
migracija 027 uvodi samostalnu tabelu `localities` (lokalitet moze da postoji
i bez ijednog predmeta — teren, buduci nalaz, poznato mesto).

`populate-lokaliteti` puni taj sifarnik:
  - izvor su podrazumevano DISTINCT vrednosti `minerals.card_locality`
    (`--izvor zbirka`), ili CSV sa jednom kolonom naziva (`--izvor csv`) —
    CSV je put za PRODUKCIJU, gde je `card_locality` prazan (0/3421), pa se
    spisak izvozi sa dev-a komandom `export-lokaliteti`;
  - trim i preskakanje praznih; NIKAKVO spajanje slicnih naziva (naucni
    nazivi se ne diraju bez coveka) — 'Trepča' i 'Stari Trg, Trepča, Srbija'
    ostaju dva zapisa;
  - podrazumevano DRY-RUN (spisak novih + broj postojecih, bez ijednog upisa);
  - `--execute` trazi kucanje imena baze pa radi jedan transakcioni INSERT;
  - IDEMPOTENTNA: `ON CONFLICT (name) DO NOTHING` — drugo pokretanje prijavi
    0 novih i ne dira postojece redove (ni `source`, ni rucno dopisane).

Per-item `minerals.card_locality` na produkciji je odvojen podatak-gap i NIJE
predmet ove komande.
"""

import csv
from pathlib import Path
from urllib.parse import urlsplit

import click

from postgres_service import get_database_url, get_postgres_connection


def _database_name():
    return urlsplit(get_database_url()).path.lstrip('/') or '?'


def nazivi_iz_zbirke(cur):
    """DISTINCT lokaliteti iz mineraloske zbirke (trimovani, bez praznih)."""
    cur.execute(
        """
        SELECT DISTINCT btrim(card_locality) AS name
        FROM minerals
        WHERE card_locality IS NOT NULL
          AND btrim(card_locality) <> ''
        ORDER BY 1
        """
    )
    return [row[0] for row in cur.fetchall()]


def nazivi_iz_csv(putanja):
    """Nazivi iz fajla: JEDAN naziv po liniji.

    Nazivi lokaliteta redovno sadrze zareze ('Stari Trg, Trepča, Srbija'), pa
    slepo CSV-parsiranje po zarezu tiho odseca naziv na 'Stari Trg'. Zato:
    liniju u navodnicima (kako je pise `export-lokaliteti` preko csv.writer)
    raspakujemo CSV citacem, a golu liniju uzimamo celu, doslovno.
    """
    nazivi = []
    with open(putanja, newline='', encoding='utf-8') as handle:
        for linija in handle:
            linija = linija.strip()
            if not linija:
                continue
            if linija.startswith('"'):
                red = next(csv.reader([linija]), [])
                naziv = (red[0] if red else '').strip()
            else:
                naziv = linija
            if not naziv or naziv.lower() in {'name', 'naziv'}:
                continue
            nazivi.append(naziv)
    # zadrzi redosled, ukloni ponovljene (isti tekst dva puta u fajlu)
    vidjeni, jedinstveni = set(), []
    for naziv in nazivi:
        if naziv not in vidjeni:
            vidjeni.add(naziv)
            jedinstveni.append(naziv)
    return jedinstveni


def postojeci_nazivi(cur):
    cur.execute('SELECT name FROM localities')
    return {row[0] for row in cur.fetchall()}


def upisi_nove(cur, nazivi, pokrenuo_email):
    """Idempotentan upis: postojeci nazivi se preskacu (ON CONFLICT DO NOTHING).
    Vraca broj stvarno ubacenih redova."""
    ubaceno = 0
    for naziv in nazivi:
        cur.execute(
            """
            INSERT INTO localities (name, source, created_by_email)
            VALUES (%s, 'seed', %s)
            ON CONFLICT (name) DO NOTHING
            RETURNING id
            """,
            (naziv, pokrenuo_email),
        )
        if cur.fetchone():
            ubaceno += 1
    return ubaceno


def register_cli(app):
    @app.cli.command('export-lokaliteti')
    @click.option('--izlaz', default='data/lokaliteti_export.csv',
                  help='Putanja CSV fajla (podrazumevano data/lokaliteti_export.csv).')
    def export_lokaliteti(izlaz):
        """Izvezi DISTINCT lokalitete iz zbirke u CSV (za prenos na produkciju)."""
        with get_postgres_connection() as conn:
            with conn.cursor() as cur:
                nazivi = nazivi_iz_zbirke(cur)

        putanja = Path(izlaz)
        putanja.parent.mkdir(parents=True, exist_ok=True)
        with open(putanja, 'w', newline='', encoding='utf-8') as handle:
            pisac = csv.writer(handle)
            pisac.writerow(['name'])
            for naziv in nazivi:
                pisac.writerow([naziv])

        click.echo(f'=== export-lokaliteti — baza: {_database_name()} ===')
        click.echo(f'Izvezeno naziva: {len(nazivi)} -> {putanja}')
        click.echo('Fajl se NE commituje — prenesi ga scp-om na produkciju.')

    @app.cli.command('populate-lokaliteti')
    @click.option('--izvor', type=click.Choice(['zbirka', 'csv']), default='zbirka',
                  help='zbirka = DISTINCT card_locality (dev); csv = spisak iz fajla (prod).')
    @click.option('--csv-putanja', default='data/lokaliteti_export.csv',
                  help='CSV kad je --izvor csv.')
    @click.option('--execute', is_flag=True,
                  help='Stvarno upisi u sifarnik (podrazumevano dry-run).')
    @click.option('--email', default='cli@nhmbeo.rs',
                  help='Email koji se belezi kao created_by_email.')
    def populate_lokaliteti(izvor, csv_putanja, execute, email):
        """Popuni samostalan sifarnik lokaliteta (idempotentno, bez spajanja naziva)."""
        mode = 'EXECUTE' if execute else 'DRY-RUN (bez izmena)'
        click.echo(f'=== populate-lokaliteti — {mode} — baza: {_database_name()} ===')

        with get_postgres_connection() as conn:
            with conn.cursor() as cur:
                if izvor == 'csv':
                    if not Path(csv_putanja).is_file():
                        raise click.ClickException(f'CSV ne postoji: {csv_putanja}')
                    nazivi = nazivi_iz_csv(csv_putanja)
                    click.echo(f'Izvor: CSV {csv_putanja} — naziva u fajlu: {len(nazivi)}')
                else:
                    nazivi = nazivi_iz_zbirke(cur)
                    click.echo(f'Izvor: DISTINCT minerals.card_locality — naziva: {len(nazivi)}')

                postojeci = postojeci_nazivi(cur)

        novi = [naziv for naziv in nazivi if naziv not in postojeci]
        vec_ima = len(nazivi) - len(novi)

        click.echo(f'U sifarniku vec: {len(postojeci)} | poklapa se sa izvorom: {vec_ima}')
        click.echo(f'Novih za upis: {len(novi)}')
        for naziv in novi[:15]:
            click.echo(f'  + {naziv}')
        if len(novi) > 15:
            click.echo(f'  ... i jos {len(novi) - 15}')

        if not novi:
            click.echo('Nema novih naziva — sifarnik je vec usaglasen (idempotentno).')
            return

        if not execute:
            click.echo(f'Dry-run: nista nije upisano. Za upis {len(novi)} naziva: --execute')
            return

        db_name = _database_name()
        odgovor = click.prompt(
            f'POTVRDA: za upis otkucaj tacno ime baze ({db_name!r})',
            default='', show_default=False,
        )
        if odgovor != db_name:
            raise click.ClickException('Ime baze se ne poklapa — prekid, bez izmena.')

        with get_postgres_connection() as conn:
            with conn.cursor() as cur:
                ubaceno = upisi_nove(cur, novi, email)
            conn.commit()

        click.echo(f'Upisano novih lokaliteta: {ubaceno}')
        click.echo('Alat „Локалитети" ih vidi odmah (cita bazu u letu, bez restarta).')
