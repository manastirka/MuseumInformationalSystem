#!/usr/bin/env python3
"""Jednokratna popravka nasledjenih redova u news_articles.

Dve greske su usle prilikom starog uvoza vesti (scripts/migrate_news_to_postgres.py)
i vide se na strani „Muzejske vesti" cim je dobila novi prikaz:

1. ``location`` svih rucnih redova drzi tekst dugmeta sa starog sajta
   ("Погледај веб страницу") umesto mesta dogadjaja. To nije podatak nego
   ostatak HTML-a, pa se brise (NULL), a ne prepisuje necim izmisljenim.

2. Naslovi i opisi nekih redova nose HTML entitete (``&#8211;``, ``&#8220;``)
   jer su bili escape-ovani dva puta. Jinja ih ispisuje doslovno, pa kustos
   vidi „Пут на Месец&#8220;". Entiteti se razrešavaju u prave znakove.

Podrazumevano je DRY RUN — ispis sta bi se promenilo, nula izmena. Prava
izmena trazi --execute I --database <ime> koje mora da se poklopi sa
current_database(), isti obrazac kao deploy/run_migrations.py.

    python scripts/migration/popravi_stare_vesti.py
    python scripts/migration/popravi_stare_vesti.py --execute --database mis_db
"""

import argparse
import html
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(REPO))

LAZNO_MESTO = 'Погледај веб страницу'
ENTITET = re.compile(r'&#?\w+;')


def _veza():
    from postgres_service import get_postgres_connection
    from psycopg.rows import dict_row
    return get_postgres_connection(row_factory=dict_row)


def _razresi(vrednost):
    """Razresi HTML entitete; vrati None kad nema promene."""
    if not vrednost or not ENTITET.search(vrednost):
        return None
    razreseno = html.unescape(vrednost)
    return razreseno if razreseno != vrednost else None


def main(argv=None):
    from dotenv import load_dotenv
    load_dotenv()

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--execute', action='store_true',
                        help='stvarno upisi izmene (bez ovoga je dry run)')
    parser.add_argument('--database',
                        help='ime baze — mora da se poklopi sa current_database()')
    a = parser.parse_args(argv)

    if a.execute and not a.database:
        print('GRESKA: --execute trazi i --database <ime>.', file=sys.stderr)
        return 2

    with _veza() as conn:
        with conn.cursor() as cur:
            cur.execute('SELECT current_database() AS ime')
            baza = cur.fetchone()['ime']
            if a.execute and baza != a.database:
                print('GRESKA: povezan sam na „%s", a --database kaze „%s".'
                      % (baza, a.database), file=sys.stderr)
                return 2
            print('Baza: %s%s' % (baza, '' if a.execute else '  (DRY RUN)'))

            cur.execute(
                'SELECT count(*) AS broj FROM news_articles WHERE location = %s',
                (LAZNO_MESTO,))
            lazna_mesta = cur.fetchone()['broj']

            cur.execute(
                "SELECT id, title, description FROM news_articles "
                "WHERE title ~ '&#?\\w+;' OR description ~ '&#?\\w+;'")
            kandidati = cur.fetchall()

            popravke = []
            for red in kandidati:
                novi_naslov = _razresi(red['title'])
                novi_opis = _razresi(red['description'])
                if novi_naslov or novi_opis:
                    popravke.append((red['id'],
                                     novi_naslov or red['title'],
                                     novi_opis if novi_opis is not None
                                     else red['description']))

            print('1) location = „%s" -> NULL: %d red(ova)'
                  % (LAZNO_MESTO, lazna_mesta))
            print('2) HTML entiteti u naslovu/opisu: %d red(ova)'
                  % len(popravke))
            for vest_id, naslov, _ in popravke[:5]:
                print('   #%s  %s' % (vest_id, naslov[:70]))
            if len(popravke) > 5:
                print('   … i još %d' % (len(popravke) - 5))

            if not a.execute:
                print('\nNista nije promenjeno. Za izmenu: '
                      '--execute --database %s' % baza)
                return 0

            cur.execute(
                'UPDATE news_articles SET location = NULL, updated_at = now() '
                'WHERE location = %s', (LAZNO_MESTO,))
            promenjeno_mesta = cur.rowcount

            promenjeno_teksta = 0
            for vest_id, naslov, opis in popravke:
                cur.execute(
                    'UPDATE news_articles SET title = %s, description = %s, '
                    'updated_at = now() WHERE id = %s',
                    (naslov, opis, vest_id))
                promenjeno_teksta += cur.rowcount

        conn.commit()

    print('\nUpisano: %d mesta ocisceno, %d naslova/opisa razreseno.'
          % (promenjeno_mesta, promenjeno_teksta))
    if promenjeno_mesta != lazna_mesta or promenjeno_teksta != len(popravke):
        print('UPOZORENJE: broj izmenjenih redova se ne poklapa sa planom.',
              file=sys.stderr)
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
