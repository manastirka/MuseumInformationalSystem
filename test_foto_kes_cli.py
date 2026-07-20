"""Регресија: фотографија везана САМО за К-Р досије не сме да важи као „без
икакве везе".

Индекс повезаности (`bez_ijedne_veze_sql`, из кога се изводи пријемни ред и
галеријски филтер) набрајао је само 4 везне табеле и НИЈЕ знао за
`foto_veza_kr_dosije`. Зато су слике унете кроз `uvezi-kr-dosije` (или везане
кроз К-Р модул) погрешно испадале као „сирочад" у пријемном реду, иако су у
бази биле уредно везане за досије. Ово није кеш — то је жив, али НЕПОТПУН упит.

Тестови раде у трансакцији коју на крају ВРАЋАЈУ (rollback), па база остаје
нетакнута.
"""

import os
import uuid
import pytest

os.environ.setdefault('DATABASE_URL', 'postgresql://localhost/museum_system')

import fototeka_views
import kr_dosije_views

try:
    from postgres_service import get_postgres_connection
    _DB_OK = True
    _DB_ERR = None
except Exception as exc:  # pragma: no cover
    _DB_OK = False
    _DB_ERR = exc

_DB_SKIP = pytest.mark.skipif(not _DB_OK, reason=f'нема базе ({_DB_ERR})')


# --- статичка провера предиката (без базе) ---
def test_predikat_zna_za_kr_dosije():
    sql = fototeka_views.bez_ijedne_veze_sql('f')
    assert 'foto_veza_kr_dosije' in sql, \
        'индекс повезаности не набраја foto_veza_kr_dosije'
    # све везне табеле морају бити покривене
    for tabela in ('foto_veza_predmet', 'foto_veza_teren',
                   'foto_veza_projekat', 'foto_veza_izlozba',
                   'foto_veza_kr_dosije'):
        assert tabela in sql


def _insert_temp_photo(cur):
    sha = uuid.uuid4().hex + uuid.uuid4().hex[:0]  # 32 hex
    sha = (sha + '0' * 64)[:64]
    cur.execute(
        """
        INSERT INTO fotografije
            (sha256, raw_putanja, original_ime, ekstenzija, velicina_bajtova,
             autor_email, status, poreklo)
        VALUES (%s, %s, %s, %s, %s, %s, 'primljena', 'import')
        RETURNING id
        """,
        (sha, f'test/{sha}.jpg', 'test.jpg', '.jpg', 123,
         'test@nhmbeo.rs'),
    )
    return cur.fetchone()[0]


@_DB_SKIP
def test_kr_slika_nije_sirotan_u_prijemnom_redu():
    """CLI упис: слика везана само за К-Р досије → ОДМАХ важи као повезана
    (није у пријемном реду), без иједне UI радње."""
    conn = get_postgres_connection()
    try:
        cur = conn.cursor()
        # 1) направи досије + слику + К-Р везу (као што ради CLI увоз)
        cur.execute(
            """
            INSERT INTO kr_dosije (evidencioni_broj, odeljenje, naziv_predmeta, izvor)
            VALUES (%s, 'geo', 'Тест предмет (kes)', 'uvoz') RETURNING id
            """,
            (f'КР-ГЕО-2098-{uuid.uuid4().hex[:6]}',),
        )
        dosije_id = cur.fetchone()[0]
        foto_id = _insert_temp_photo(cur)
        cur.execute(
            """
            INSERT INTO foto_veza_kr_dosije (fotografija_id, dosije_id, faza)
            VALUES (%s, %s, 'pre')
            """,
            (foto_id, dosije_id),
        )

        # 2) индекс повезаности НЕ сме да је третира као сироче
        cur.execute(
            f"""
            SELECT 1 FROM fotografije f
            WHERE f.id = %s AND f.obrisana = FALSE AND f.sklonjena_sa_reda = FALSE
              AND {fototeka_views.bez_ijedne_veze_sql('f')}
            """,
            (foto_id,),
        )
        assert cur.fetchone() is None, \
            'К-Р везана слика погрешно важи као „без икакве везе" (сироче)'

        # 3) К-Р детаљ је ОДМАХ приказује (жив упит, без кеша/UI радње)
        f = kr_dosije_views._fetch_fotografije(cur, dosije_id)
        assert len(f['pre']) == 1 and f['pre'][0]['foto_id'] == foto_id
    finally:
        conn.rollback()
        conn.close()
