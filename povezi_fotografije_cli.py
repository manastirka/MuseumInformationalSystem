"""`flask povezi-fotografije` — retroaktivno vezivanje uvezenih fotografija.

Uvoz pre popravke (run 71 na produkciji) je pravio vezu na inventarni broj
prepisan iz imena datoteke ('M 028' -> '028'), a u bazi predmeta stoji '28' —
veza je pokazivala na predmet koji ne postoji, pa nijedna od 125 fotografija
nije zaista bila vezana. Ova komanda prolazi kroz fotografije BEZ ijedne veze
(ili sa vezom koja ne pokazuje ni na jedan predmet), ponovo mapira inventarni
broj po novom, fleksibilnom algoritmu (`fototeka_views.normalizuj_inv_broj` +
`nadji_predmet`) i pravi ispravnu vezu.

  flask povezi-fotografije                # DRY-RUN: sta bi povezao, bez izmena
  flask povezi-fotografije --execute      # trazi kucanje imena baze

NE dira datoteke, RAW arhivu ni derivate — samo redove veza (`foto_veza_predmet`)
i zastavicu prijemnog reda. Idempotentna: drugo pokretanje prijavi 0 novih veza.
"""

from urllib.parse import urlsplit

import click

from postgres_service import get_database_url, get_postgres_connection


def _database_name():
    return urlsplit(get_database_url()).path.lstrip('/') or '?'


def fotografije_bez_veze(cur):
    """Fotografije koje nemaju NIJEDNU upotrebljivu vezu.

    Racuna se i fotografija cija veza pokazuje na inventarni broj koji NE postoji
    doslovno u zbirci ('001' dok predmet stoji kao '1') — aplikacija (galerija,
    thumbnail u tabeli) poredi TACAN string, pa je takva veza prazna ljuska i
    fotografija je i dalje nepovezana. Zato je poredjenje ovde doslovno, ne
    normalizovano.
    """
    cur.execute(
        """
        SELECT f.id, f.original_ime
        FROM fotografije f
        WHERE f.obrisana = FALSE
          AND NOT EXISTS (SELECT 1 FROM foto_veza_teren t WHERE t.fotografija_id = f.id)
          AND NOT EXISTS (SELECT 1 FROM foto_veza_projekat p WHERE p.fotografija_id = f.id)
          AND NOT EXISTS (SELECT 1 FROM foto_veza_izlozba i WHERE i.fotografija_id = f.id)
          -- K-R vezana slika NIJE sirotan: ne diraj je (inace bi je ovaj alat
          -- pokusao da preveze na mineral). Isti razlog kao bez_ijedne_veze_sql.
          AND NOT EXISTS (SELECT 1 FROM foto_veza_kr_dosije k WHERE k.fotografija_id = f.id)
          AND NOT EXISTS (
                SELECT 1
                FROM foto_veza_predmet v
                JOIN minerals m
                  ON btrim(m.inventory_number) = btrim(v.inventarni_broj)
                WHERE v.fotografija_id = f.id
              )
        ORDER BY f.id
        """
    )
    redovi = cur.fetchall()
    return [
        (red['id'], red['original_ime']) if isinstance(red, dict) else (red[0], red[1])
        for red in redovi
    ]


def predlozi_veze(cur, kandidati, zbirka):
    """[(foto_id, ime, inv_broj_iz_baze)] za fotografije koje umemo da vezemo."""
    import fototeka_views

    predlozi = []
    for foto_id, ime in kandidati:
        klasifikacija = fototeka_views.classify_import_filename(
            fototeka_views._strip_institution_prefix(ime or ''), zbirka)
        if klasifikacija['klasa'] != 'predmet':
            continue
        trazeni = klasifikacija['veza_meta']['inventarni_broj']
        nadjen, status = fototeka_views.nadji_predmet(cur, zbirka, trazeni)
        if status == 'ok':
            predlozi.append((foto_id, ime, nadjen))
    return predlozi


def primeni_veze(cur, predlozi, zbirka):
    """Upisi ispravne veze i skini fotografije sa prijemnog reda.

    Usput brise PRAZNE LJUSKE — veze te fotografije koje ne pokazuju ni na jedan
    postojeci predmet (npr. stari '001' dok predmet stoji kao '1'). Brisu se
    iskljucivo takve veze; datoteke, RAW arhiva i derivati se ne diraju.
    Vraca (broj_novih_veza, broj_obrisanih_praznih_veza).
    """
    povezano = 0
    ociscenih = 0
    for foto_id, _ime, inv_broj in predlozi:
        cur.execute(
            """
            DELETE FROM foto_veza_predmet v
            WHERE v.fotografija_id = %s
              AND NOT EXISTS (
                    SELECT 1 FROM minerals m
                    WHERE btrim(m.inventory_number) = btrim(v.inventarni_broj)
                  )
            """,
            (foto_id,),
        )
        ociscenih += cur.rowcount if cur.rowcount and cur.rowcount > 0 else 0
        cur.execute(
            """
            INSERT INTO foto_veza_predmet (fotografija_id, database_name, inventarni_broj)
            VALUES (%s, %s, %s)
            ON CONFLICT DO NOTHING
            RETURNING fotografija_id
            """,
            (foto_id, zbirka, inv_broj),
        )
        if cur.fetchone():
            povezano += 1
        cur.execute(
            'UPDATE fotografije SET u_prijemnom_redu = FALSE WHERE id = %s',
            (foto_id,),
        )
    return povezano, ociscenih


def register_cli(app):
    @app.cli.command('povezi-fotografije')
    @click.option('--zbirka', default='mineral',
                  help='Zbirka za mapiranje inventarnih brojeva (podrazumevano mineral).')
    @click.option('--execute', is_flag=True,
                  help='Stvarno upisi veze (podrazumevano dry-run).')
    def povezi_fotografije(zbirka, execute):
        """Retroaktivno vezi uvezene fotografije za predmete (bez diranja datoteka)."""
        mode = 'EXECUTE' if execute else 'DRY-RUN (bez izmena)'
        click.echo(f'=== povezi-fotografije — {mode} — baza: {_database_name()} ===')

        with get_postgres_connection() as conn:
            with conn.cursor() as cur:
                kandidati = fotografije_bez_veze(cur)
                predlozi = predlozi_veze(cur, kandidati, zbirka)

        bez_predloga = len(kandidati) - len(predlozi)
        click.echo(f'Фотографија без иједне везе: {len(kandidati)}')
        click.echo(f'  -> може да се повеже: {len(predlozi)}')
        click.echo(f'  -> остаје БЕЗ ВЕЗЕ (име не носи постојећи инв. број): {bez_predloga}')
        for foto_id, ime, inv in predlozi[:15]:
            click.echo(f'  + {ime} -> предмет {inv} (фото {foto_id})')
        if len(predlozi) > 15:
            click.echo(f'  ... и још {len(predlozi) - 15}')

        if not predlozi:
            click.echo('Нема шта да се повеже.')
            return

        if not execute:
            click.echo(f'Dry-run: ништа није измењено. За упис {len(predlozi)} веза: --execute')
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
                povezano, ociscenih = primeni_veze(cur, predlozi, zbirka)
            conn.commit()

        click.echo(f'Уписано нових веза: {povezano}')
        if ociscenih:
            click.echo(f'Обрисано празних веза (показивале на непостојећи предмет): {ociscenih}')
        click.echo('Датотеке, RAW архива и деривати нису дирани.')
