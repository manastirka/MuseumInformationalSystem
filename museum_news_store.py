"""Citanje muzejskih vesti iz baze (izvor istine je news_articles).

Do sada je strana citala museum_app.NEWS_DATABASE — LazyLoadedDict koji se
puni jednom po procesu. Pod gunicorn-om sa vise radnika to znaci da radnik 2
ne vidi vest koju je radnik 1 upravo sacuvao, a posle uvoza sa sajta strana
ostaje na starom sadrzaju dok se proces ne restartuje. Zato ovaj modul cita
bazu pri svakom zahtevu; tabela je mala (stotine redova) i indeksirana po
start_date, pa je cena zanemarljiva u odnosu na zastarele podatke.
"""

import logging

from psycopg.rows import dict_row

logger = logging.getLogger(__name__)

POLJA = """
    id, izvor, spoljni_id, title, description, sadrzaj_tekst, type, status,
    category, start_date, end_date, location, curator, autor, keywords,
    source_link, slika_url, spoljni_izmenjen, uvezeno_at, created_at, updated_at
"""


def _get_postgres_connection(**kwargs):
    from postgres_service import get_postgres_connection
    return get_postgres_connection(**kwargs)


def _uslovi(*, upit=None, tip=None, izvor=None, godina=None):
    """Zajednicki WHERE za listu i za brojanje — jedan izvor logike filtera."""
    delovi = []
    parametri = []

    if upit:
        # ILIKE umesto tsquery: tabela je mala, a kustos trazi delove reci
        # ("минерал", "Трепч") gde bi plainto_tsquery promasio.
        delovi.append('(title ILIKE %s OR description ILIKE %s '
                      'OR sadrzaj_tekst ILIKE %s OR keywords ILIKE %s)')
        obrazac = '%%%s%%' % upit.strip()
        parametri.extend([obrazac] * 4)

    if tip:
        delovi.append('type = %s')
        parametri.append(tip)

    if izvor:
        delovi.append('izvor = %s')
        parametri.append(izvor)

    if godina:
        delovi.append('EXTRACT(YEAR FROM start_date) = %s')
        parametri.append(int(godina))

    return (' AND '.join(delovi) if delovi else 'TRUE'), parametri


def dohvati_vesti(*, upit=None, tip=None, izvor=None, godina=None,
                  limit=12, pomak=0):
    """Stranica vesti + ukupan broj koji odgovara filterima."""
    where, parametri = _uslovi(upit=upit, tip=tip, izvor=izvor, godina=godina)

    with _get_postgres_connection(row_factory=dict_row) as conn:
        with conn.cursor() as cur:
            cur.execute(
                'SELECT count(*) AS ukupno FROM news_articles WHERE ' + where,
                parametri,
            )
            ukupno = cur.fetchone()['ukupno']

            cur.execute(
                'SELECT ' + POLJA + ' FROM news_articles WHERE ' + where +
                ' ORDER BY start_date DESC NULLS LAST, id DESC '
                'LIMIT %s OFFSET %s',
                parametri + [int(limit), int(pomak)],
            )
            vesti = cur.fetchall()

    return vesti, ukupno


def dohvati_vest(vest_id):
    """Jedna vest po id ili None."""
    with _get_postgres_connection(row_factory=dict_row) as conn:
        with conn.cursor() as cur:
            cur.execute(
                'SELECT ' + POLJA + ' FROM news_articles WHERE id = %s',
                (int(vest_id),),
            )
            return cur.fetchone()


def susedne_vesti(vest):
    """Prethodna i sledeca vest po datumu — za navigaciju na strani citanja."""
    if not vest:
        return None, None
    datum = vest.get('start_date')
    with _get_postgres_connection(row_factory=dict_row) as conn:
        with conn.cursor() as cur:
            cur.execute(
                'SELECT id, title FROM news_articles '
                'WHERE (start_date, id) > (%s, %s) '
                'ORDER BY start_date ASC NULLS LAST, id ASC LIMIT 1',
                (datum, vest['id']),
            )
            novija = cur.fetchone()
            cur.execute(
                'SELECT id, title FROM news_articles '
                'WHERE (start_date, id) < (%s, %s) '
                'ORDER BY start_date DESC NULLS LAST, id DESC LIMIT 1',
                (datum, vest['id']),
            )
            starija = cur.fetchone()
    return novija, starija


def pregled():
    """Podaci za zaglavlje strane: brojevi, tipovi, godine, poslednji uvoz."""
    with _get_postgres_connection(row_factory=dict_row) as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT count(*) AS ukupno,
                       count(*) FILTER (WHERE izvor = 'nhmbeo') AS sa_sajta,
                       count(*) FILTER (WHERE izvor = 'rucni')  AS rucnih,
                       count(*) FILTER (
                           WHERE start_date >= CURRENT_DATE - INTERVAL '90 days'
                       ) AS skorasnjih,
                       max(start_date) AS najnovija
                FROM news_articles
                """
            )
            brojevi = cur.fetchone()

            cur.execute(
                'SELECT type, count(*) AS broj FROM news_articles '
                'WHERE type IS NOT NULL AND type <> %s '
                'GROUP BY type ORDER BY broj DESC, type', ('',),
            )
            tipovi = cur.fetchall()

            cur.execute(
                'SELECT DISTINCT EXTRACT(YEAR FROM start_date)::int AS godina '
                'FROM news_articles WHERE start_date IS NOT NULL '
                'ORDER BY godina DESC'
            )
            godine = [red['godina'] for red in cur.fetchall()]

            cur.execute(
                'SELECT status, pokrenuto_at, zavrseno_at, novih, azuriranih, '
                'pregledano, poruka, pokrenuo FROM news_import_log '
                "WHERE izvor = 'nhmbeo' ORDER BY pokrenuto_at DESC LIMIT 1"
            )
            poslednji_uvoz = cur.fetchone()

    return {
        'brojevi': brojevi,
        'tipovi': tipovi,
        'godine': godine,
        'poslednji_uvoz': poslednji_uvoz,
    }


def obrisi_vest(vest_id):
    """Brisanje rucne vesti. Vraca (obrisano, poruka).

    Uvezene vesti se ne brisu odavde — sledeci uvoz bi ih vratio, pa bi
    brisanje izgledalo kao da nije radilo.
    """
    with _get_postgres_connection(row_factory=dict_row) as conn:
        with conn.cursor() as cur:
            cur.execute('SELECT izvor FROM news_articles WHERE id = %s',
                        (int(vest_id),))
            red = cur.fetchone()
            if red is None:
                return False, 'Вест не постоји'
            if red['izvor'] != 'rucni':
                return False, ('Вест је преузета са сајта музеја и не може се '
                               'брисати овде — уклоните је на сајту.')
            cur.execute('DELETE FROM news_articles WHERE id = %s',
                        (int(vest_id),))
            obrisano = cur.rowcount > 0
        conn.commit()
    return obrisano, ('Вест је обрисана' if obrisano
                      else 'Вест није обрисана — покушајте поново')
