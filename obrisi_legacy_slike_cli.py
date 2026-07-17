"""`flask obrisi-legacy-slike` — brisanje starog `images` skladista slika.

Fototeka je jedini sistem za slike predmeta (uvoz + veze + derivati). Stari
batch upload i legacy fallback su uklonjeni iz koda, pa `images` tabelu i
`ImagesDatabase/` niko vise ne cita — ova komanda ih uklanja.

  flask obrisi-legacy-slike              # DRY-RUN: ispis sta bi obrisao
  flask obrisi-legacy-slike --execute    # trazi kucanje imena baze

Pre brisanja ispisuje POKRIVENOST: koliko predmeta koji danas imaju legacy
sliku ima i fotografiju u Fototeci. Predmeti bez fototeka fotografije posle
brisanja ostaju na placeholderu — zato dry-run to broji unapred.

Brise: redove `images` + datoteke na koje pokazuju (original + thumbnailovi).
Ne dira: Fototeku (RAW arhiva, derivati, `fotografije`, `foto_veza_*`).
Idempotentna: drugo pokretanje prijavi 0 za brisanje.
"""

import os
from pathlib import Path
from urllib.parse import urlsplit

import click

from postgres_service import get_database_url, get_postgres_connection

# Zbirke koje Fototeka danas pokriva za predmete (isto kao u fototeka_views).
FOTOTEKA_ZBIRKA = 'mineral'

# Legacy database_name vrednosti koje pokazuju na mineralosku zbirku.
MINERAL_DATABASE_NAMES = ('mineral', 'minerals')


def _database_name():
    return urlsplit(get_database_url()).path.lstrip('/') or '?'


def _storage_root():
    """Koren legacy skladista — isti izvor kao stari image_storage_engine."""
    return Path(os.environ.get('IMAGE_STORAGE_PATH', './ImagesDatabase'))


def popis_legacy_slika(cur):
    """Svi redovi `images` sa putanjama datoteka koje drze."""
    cur.execute(
        """
        SELECT image_id, database_name, entity_type, entity_id,
               file_path, thumbnail_small, thumbnail_medium, thumbnail_large,
               COALESCE(file_size, 0) AS file_size
        FROM images
        ORDER BY database_name, entity_type, image_id
        """
    )
    redovi = cur.fetchall()
    return [red if isinstance(red, dict) else {
        'image_id': red[0], 'database_name': red[1], 'entity_type': red[2],
        'entity_id': red[3], 'file_path': red[4], 'thumbnail_small': red[5],
        'thumbnail_medium': red[6], 'thumbnail_large': red[7], 'file_size': red[8],
    } for red in redovi]


def _tabela_postoji(cur, ime):
    cur.execute("SELECT to_regclass(%s) IS NOT NULL AS postoji", (f'public.{ime}',))
    red = cur.fetchone()
    return bool(red['postoji'] if isinstance(red, dict) else red[0])


def pokrivenost_fototekom(cur, redovi):
    """(pokriveni, nepokriveni) inventarni brojevi predmeta sa legacy slikom.

    Legacy slike se vezuju za `minerals.id`, a Fototeka za `inventory_number` —
    zato ide preko spajanja na predmet. Racunaju se samo spremne, neobrisane
    fotografije, isto kao prikaz u tabeli.
    """
    mineral_ids = sorted({
        str(r['entity_id']).strip() for r in redovi
        if str(r['database_name']).lower() in MINERAL_DATABASE_NAMES
        and str(r['entity_id'] or '').strip().isdigit()
    }, key=int)
    if not mineral_ids:
        return [], []

    cur.execute(
        """
        SELECT m.inventory_number,
               EXISTS (
                   SELECT 1
                   FROM foto_veza_predmet v
                   JOIN fotografije f ON f.id = v.fotografija_id
                   WHERE v.database_name = %s
                     AND v.inventarni_broj = m.inventory_number
                     AND f.obrisana = FALSE
                     AND f.status = 'spremna'
               ) AS ima_fototeku
        FROM minerals m
        WHERE m.id = ANY(%s)
        ORDER BY m.inventory_number
        """,
        (FOTOTEKA_ZBIRKA, [int(i) for i in mineral_ids]),
    )
    pokriveni, nepokriveni = [], []
    for red in cur.fetchall():
        broj = red['inventory_number'] if isinstance(red, dict) else red[0]
        ima = red['ima_fototeku'] if isinstance(red, dict) else red[1]
        (pokriveni if ima else nepokriveni).append(str(broj))
    return pokriveni, nepokriveni


def datoteke_reda(red, koren):
    """Postojece datoteke koje red drzi (original + svi thumbnailovi).

    `file_path` je upisivan repo-relativno ('ImagesDatabase/originals/x.jpg'),
    ali i kao gola putanja — zato se proba oba, isto kao stari resolver.
    """
    putanje = []
    for kljuc in ('file_path', 'thumbnail_small', 'thumbnail_medium', 'thumbnail_large'):
        vrednost = (red.get(kljuc) or '').strip()
        if not vrednost:
            continue
        kandidati = [Path(vrednost)]
        ime = Path(vrednost).name
        kandidati.append(koren / 'originals' / ime)
        for velicina in ('small', 'medium', 'large'):
            kandidati.append(koren / 'thumbnails' / velicina / ime)
        for kandidat in kandidati:
            if kandidat.is_file():
                putanje.append(kandidat)
                break
    return putanje


def _ispisi_popis(redovi, koren):
    """Ispis po zbirci + ukupno; vraca (sve_datoteke, ukupno_bajtova)."""
    po_zbirci = {}
    for red in redovi:
        kljuc = (red['database_name'], red['entity_type'])
        po_zbirci.setdefault(kljuc, []).append(red)

    sve_datoteke, ukupno_bajtova = [], 0
    click.echo('Легаци слике у бази:')
    for (baza, tip), grupa in sorted(po_zbirci.items()):
        predmeta = len({str(r['entity_id']) for r in grupa})
        datoteke = [p for r in grupa for p in datoteke_reda(r, koren)]
        bajtova = sum(p.stat().st_size for p in datoteke)
        sve_datoteke.extend(datoteke)
        ukupno_bajtova += bajtova
        click.echo(
            f'  {baza}/{tip}: {len(grupa)} слика, {predmeta} предмета, '
            f'{len(datoteke)} датотека, {bajtova / 1024 / 1024:.1f} MB'
        )
    return sve_datoteke, ukupno_bajtova


def _ispisi_ostatak(koren, datoteke):
    """Datoteke pod korenom skladista koje NIJEDAN red ne pominje.

    Stara rezerva (`ImagesDatabase/backups`) je paralelna kopija bez reda u bazi,
    pa je brisanje po redovima ne dodiruje. Ne brise se automatski — samo se
    prijavi, da operater zna sta ostaje i moze da ukloni ceo direktorijum rucno.
    """
    if not koren.is_dir():
        return
    poznate = {p.resolve() for p in datoteke}
    ostale = [p for p in koren.rglob('*') if p.is_file() and p.resolve() not in poznate]
    if not ostale:
        return
    bajtova = sum(p.stat().st_size for p in ostale)
    click.echo('')
    click.echo(f'Ван базе (ниједан ред их не помиње): {len(ostale)} датотека, '
               f'{bajtova / 1024 / 1024:.1f} MB')
    click.echo(f'  Ова команда их НЕ дира. Кад потврдиш да је све у реду, цео '
               f'{koren}/ се уклања ручно.')


def _ispisi_jos_u_upotrebi(redovi):
    """Redovi koje neki zivi ekran jos cita — Fototeka ih ne pokriva.

    Terenski podaci (`geo_field`) i dalje prikazuju slike kroz `/api/images/<id>`;
    Fototeka za teren ima svoju vezu, ali prikaz jos nije prevezan. Brisanje takvih
    redova ostavlja teren bez slika, pa mora da se vidi u dry-run-u.
    """
    ostali = sorted({
        (r['database_name'], r['entity_type']) for r in redovi
        if str(r['database_name']).lower() not in MINERAL_DATABASE_NAMES
    })
    if not ostali:
        return True
    click.echo('')
    click.echo('УПОЗОРЕЊЕ: ови редови нису минерали — Фототека их не покрива:')
    for baza, tip in ostali:
        broj = len([r for r in redovi if (r['database_name'], r['entity_type']) == (baza, tip)])
        click.echo(f'  {baza}/{tip}: {broj} слика — брисање их оставља без слике.')
    return False


def _ispisi_pokrivenost(cur, redovi):
    """Vraca True ako je bezbedno nastaviti bez dodatnog upozorenja."""
    if not _tabela_postoji(cur, 'foto_veza_predmet'):
        click.echo('УПОЗОРЕЊЕ: табела `foto_veza_predmet` не постоји — Фототека није '
                   'мигрирана на овом окружењу. Брисање би оставило све предмете без слике.')
        return False

    pokriveni, nepokriveni = pokrivenost_fototekom(cur, redovi)
    ukupno = len(pokriveni) + len(nepokriveni)
    if not ukupno:
        return True

    click.echo('')
    click.echo('Покривеност Фототеком (предмети који данас имају легаци слику):')
    click.echo(f'  има фотографију у Фототеци: {len(pokriveni)}/{ukupno}')
    click.echo(f'  остаје на плацехолдеру:      {len(nepokriveni)}/{ukupno}')
    if nepokriveni:
        prikaz = ', '.join(nepokriveni[:20])
        if len(nepokriveni) > 20:
            prikaz += f' ... и још {len(nepokriveni) - 20}'
        click.echo(f'  -> инв. бројеви без Фототеке: {prikaz}')
        click.echo('  Ако ово није намерно: прво `migrate_images_to_fototeka.py --commit`, '
                   'па `flask povezi-fotografije --execute`.')
    return not nepokriveni


def obrisi(cur, redovi, koren):
    """Brise datoteke pa redove. Vraca (obrisano_datoteka, obrisano_redova)."""
    obrisano_datoteka = 0
    for red in redovi:
        for putanja in datoteke_reda(red, koren):
            try:
                putanja.unlink()
                obrisano_datoteka += 1
            except OSError as greska:
                click.echo(f'  ! не могу да обришем {putanja}: {greska}')
    cur.execute("DELETE FROM images")
    return obrisano_datoteka, cur.rowcount


def register_cli(app):
    @app.cli.command('obrisi-legacy-slike')
    @click.option('--execute', is_flag=True, default=False,
                  help='Стварно обриши (подразумевано је dry-run).')
    def obrisi_legacy_slike(execute):
        """Обриши старо `images` складиште — Фототека је једини систем за слике."""
        koren = _storage_root()

        with get_postgres_connection() as conn:
            with conn.cursor() as cur:
                if not _tabela_postoji(cur, 'images'):
                    click.echo('Табела `images` не постоји — нема шта да се брише.')
                    return

                redovi = popis_legacy_slika(cur)
                if not redovi:
                    click.echo('Табела `images` је празна — нема шта да се брише.')
                    return

                datoteke, bajtova = _ispisi_popis(redovi, koren)
                click.echo(
                    f'УКУПНО: {len(redovi)} редова, {len(datoteke)} датотека, '
                    f'{bajtova / 1024 / 1024:.1f} MB (корен: {koren})'
                )
                _ispisi_ostatak(koren, datoteke)
                cisto = _ispisi_pokrivenost(cur, redovi)
                cisto = _ispisi_jos_u_upotrebi(redovi) and cisto

                if not execute:
                    click.echo('')
                    click.echo('Dry-run: ништа није измењено. За брисање: --execute')
                    return

                click.echo('')
                if not cisto:
                    click.echo('ПАЖЊА: брисање ће оставити предмете без иједне слике (види горе).')
                db_name = _database_name()
                odgovor = click.prompt(
                    f'POTVRDA: za brisanje otkucaj tacno ime baze ({db_name!r})',
                    default='', show_default=False,
                )
                if odgovor != db_name:
                    raise click.ClickException('Ime baze se ne poklapa — prekid, bez izmena.')

                obrisano_datoteka, obrisano_redova = obrisi(cur, redovi, koren)
            conn.commit()

        click.echo(f'Обрисано редова: {obrisano_redova}')
        click.echo(f'Обрисано датотека: {obrisano_datoteka}')
        click.echo('Фототека (RAW архива, деривати, везе) није дирана.')
