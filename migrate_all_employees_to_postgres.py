#!/usr/bin/env python3
"""
Migrate all employees to PostgreSQL authentication
- Activate aca.lukovic@nhmbeo.rs
- Add all employees with default password 'user'
- Set admin privileges for slavko.spasic, biljan.mitrovic, verica.stojanovic
"""

import os
import sys

# Set DATABASE_URL
os.environ['DATABASE_URL'] = 'postgresql+psycopg://aleksandarlukovic@localhost:5432/museum_system'

from postgres_auth import get_postgres_auth

# Admin emails (in addition to 'admin')
ADMIN_EMAILS = [
    'slavko.spasic@nhmbeo.rs',      # Director
    'biljana.mitrovic@nhmbeo.rs',   # Head of Geology Department
    'verica.stojanovic@nhmbeo.rs'   # Curator
]

# All employees from listazaposlenih.txt
EMPLOYEES = [
    # ДИРЕКТОР
    {'email': 'slavko.spasic@nhmbeo.rs', 'name': 'Славко Спасић', 'position': 'виши кустос', 'department': 'Директор'},

    # ОДСЕК ОПШТИХ И ПРАВНИХ ПОСЛОВА
    {'email': 'ana.zivanovic@nhmbeo.rs', 'name': 'Ана Живановић', 'position': 'секретар', 'department': 'Одсек општих и правних послова'},
    {'email': 'ana.kovacevic@nhmbeo.rs', 'name': 'Ана Ковачевић', 'position': 'технички секретар', 'department': 'Одсек општих и правних послова'},
    {'email': 'bora.m@nhmbeo.rs', 'name': 'Бора Милићевић', 'position': 'препаратор – ликовни техничар', 'department': 'Одсек општих и правних послова'},
    {'email': 'pedja@nhmbeo.rs', 'name': 'Предраг Илић', 'position': 'препаратор – техничар графичке припреме', 'department': 'Одсек општих и правних послова'},
    {'email': 'biblioteka@nhmbeo.rs', 'name': 'Оливера Аломеровић', 'position': 'дипл. библиотекар', 'department': 'Одсек општих и правних послова'},

    # ГРУПА ЗА ФИНАНСИЈСКО-РАЧУНОВОДСТВЕНЕ ПОСЛОВЕ
    {'email': 'dusica.ivic@nhmbeo.rs', 'name': 'Душица Ивић', 'position': 'помоћник директора-руководилац одељења финансија', 'department': 'Група за финансијско-рачуноводствене послове'},
    {'email': 'milenar@nhmbeo.rs', 'name': 'Милена Радочај', 'position': 'финансијско-рачуноводствени референт', 'department': 'Група за финансијско-рачуноводствене послове'},
    {'email': 'milica@nhmbeo.rs', 'name': 'Милица Томић', 'position': 'финансијско-рачуноводствени сарадник', 'department': 'Група за финансијско-рачуноводствене послове'},

    # ГРУПА ЗА ЕДУКАЦИЈУ, КОМУНИКАЦИЈУ И МАРКЕТИНГ
    {'email': 'draganav@nhmbeo.rs', 'name': 'Драгана Вучићевић', 'position': 'виши кустос', 'department': 'Група за едукацију, комуникацију и маркетинг'},
    {'email': 'simka.vukojevic@nhmbeo.rs', 'name': 'Симка Вукојевић', 'position': 'музејски педагог', 'department': 'Група за едукацију, комуникацију и маркетинг'},

    # ГРУПА ЗА ИЗЛОЖБЕНЕ ПОСЛОВЕ – ГАЛЕРИЈА
    {'email': 'milica.rakic@nhmbeo.rs', 'name': 'Милица Ракић', 'position': 'организаторка туристичке и услужне делатности', 'department': 'Група за изложбене послове'},
    {'email': 'galerija@nhmbeo.rs', 'name': 'Снежана Јовановић', 'position': 'водич', 'department': 'Група за изложбене послове'},

    # БИОЛОШКО ОДЕЉЕЊЕ
    {'email': 'mniketic@nhmbeo.rs', 'name': 'Марјан Никетић', 'position': 'руководилац Биолошког одељења, музејски саветник ботаничар', 'department': 'Биолошко одељење'},
    {'email': 'dubravka.vucic@nhmbeo.rs', 'name': 'Дубравка Вучић', 'position': 'музејски саветник ихтиолог', 'department': 'Биолошко одељење'},
    {'email': 'milos.jovic@nhmbeo.rs', 'name': 'Милош Јовић', 'position': 'музејски саветник ентомолог', 'department': 'Биолошко одељење'},
    {'email': 'boris@nhmbeo.rs', 'name': 'Борис Иванчевић', 'position': 'музејски саветник миколог', 'department': 'Биолошко одељење'},
    {'email': 'ana.paunovic@nhmbeo.rs', 'name': 'Ана Пауновић', 'position': 'музејски саветник херпетолог', 'department': 'Биолошко одељење'},
    {'email': 'aleksandar@nhmbeo.rs', 'name': 'Александар Стојановић', 'position': 'конзерватор ентомолог', 'department': 'Биолошко одељење'},
    {'email': 'aleksandra.savic@nhmbeo.rs', 'name': 'Александра Савић', 'position': 'музејски саветник ботаничар / етноботаничар', 'department': 'Биолошко одељење'},
    {'email': 'verica.stojanovic@nhmbeo.rs', 'name': 'Верица Стојановић', 'position': 'кустос приправник', 'department': 'Биолошко одељење'},
    {'email': 'gorana.petkovski@nhmbeo.rs', 'name': 'Горана Петковски', 'position': 'конзерватор', 'department': 'Биолошко одељење'},
    {'email': 'marko.nestorovic@nhmbeo.rs', 'name': 'Марко Несторовић', 'position': 'музејски саветник ботаничар / херболог', 'department': 'Биолошко одељење'},
    {'email': 'zorana.markovic@nhmbeo.rs', 'name': 'Зорана Марковић', 'position': 'кустос', 'department': 'Биолошко одељење'},
    {'email': 'vuk.popic@nhmbeo.rs', 'name': 'Вук Попић', 'position': 'кустос приправник', 'department': 'Биолошко одељење'},
    {'email': 'milos.mrvaljevic@nhmbeo.rs', 'name': 'Милош Мрваљевић', 'position': 'препаратор приправник', 'department': 'Биолошко одељење'},
    {'email': 'jovan.kokotovic@nhmbeo.rs', 'name': 'Јован Кокотовић', 'position': 'кустос приправник', 'department': 'Биолошко одељење'},

    # ГЕОЛОШКО ОДЕЉЕЊЕ
    {'email': 'biljana.mitrovic@nhmbeo.rs', 'name': 'Биљана Митровић', 'position': 'начелник Геолошког одељења, музејски саветник палеозоолог', 'department': 'Геолошко одељење'},
    {'email': 'zoran.markovic@nhmbeo.rs', 'name': 'Зоран Марковић', 'position': 'музејски саветник палеозоолог', 'department': 'Геолошко одељење'},
    {'email': 'sanja.pavic@nhmbeo.rs', 'name': 'Сања Алабурић', 'position': 'музејски саветник палеозоолог', 'department': 'Геолошко одељење'},
    {'email': 'amaran@nhmbeo.rs', 'name': 'Александра Маран Стевановић', 'position': 'музејски саветник палеозоолог', 'department': 'Геолошко одељење'},
    {'email': 'desadjm@nhmbeo.rs', 'name': 'Деса Ђорђевић-Милутиновић', 'position': 'музејски саветник, палеоботаничар', 'department': 'Геолошко одељење'},
    {'email': 'aca.lukovic@nhmbeo.rs', 'name': 'Александар Луковић', 'position': 'кустос минералог', 'department': 'Геолошко одељење'},
    {'email': 'dragana.djuric@nhmbeo.rs', 'name': 'Драгана Ђурић', 'position': 'музејски саветник палеозоолог', 'department': 'Геолошко одељење'},
    {'email': 'tatjana.milicbabic@nhmbeo.rs', 'name': 'Татјана Милић Бабић', 'position': 'виши кустос петролог', 'department': 'Геолошко одељење'},
    {'email': 'pejovic.ranko@nhmbeo.rs', 'name': 'Ранко Пејовић', 'position': 'кустос палеозоолог', 'department': 'Геолошко одељење'},
    {'email': 'milos.milivojevic@nhmbeo.rs', 'name': 'Милош Миливојевић', 'position': 'виши препаратор за геолошке збирке', 'department': 'Геолошко одељење'},
    {'email': 'branko.radulovic@nhmbeo.rs', 'name': 'Бранко Радуловић', 'position': 'кустос за геолошке збирке', 'department': 'Геолошко одељење'},
    {'email': 'nenad.mladenovic@nhmbeo.rs', 'name': 'Ненад Младеновић', 'position': 'конзерватор приправник', 'department': 'Геолошко одељење'},
]

def main():
    auth = get_postgres_auth()

    if not auth.available:
        print("✗ PostgreSQL authentication not available!")
        sys.exit(1)

    print("=" * 70)
    print("MIGRATING ALL EMPLOYEES TO POSTGRESQL")
    print("=" * 70)

    # Step 1: Activate aca.lukovic@nhmbeo.rs if exists
    print("\n1. Activating aca.lukovic@nhmbeo.rs...")
    try:
        import psycopg
        pg_url = os.environ['DATABASE_URL'].replace('postgresql+psycopg://', 'postgresql://')

        with psycopg.connect(pg_url) as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    UPDATE users
                    SET is_active = TRUE
                    WHERE email = 'aca.lukovic@nhmbeo.rs'
                """)
                if cur.rowcount > 0:
                    print("   ✓ Activated existing user: aca.lukovic@nhmbeo.rs")
                else:
                    print("   ℹ User aca.lukovic@nhmbeo.rs not found, will be created")
                conn.commit()
    except Exception as e:
        print(f"   ⚠ Error: {e}")

    # Step 2: Add all employees
    print(f"\n2. Adding {len(EMPLOYEES)} employees to PostgreSQL...")
    added_count = 0
    updated_count = 0
    error_count = 0

    for emp in EMPLOYEES:
        email = emp['email']
        name = emp['name']
        position = emp['position']
        department = emp['department']

        # Determine role
        role = 'admin' if email in ADMIN_EMAILS else 'employee'

        try:
            # Check if user exists
            existing_user = auth.get_user_by_email(email)

            if existing_user:
                # Update existing user
                import psycopg
                pg_url = os.environ['DATABASE_URL'].replace('postgresql+psycopg://', 'postgresql://')

                with psycopg.connect(pg_url) as conn:
                    with conn.cursor() as cur:
                        cur.execute("""
                            UPDATE users
                            SET is_active = TRUE,
                                full_name = %s,
                                position = %s,
                                department_id = (SELECT id FROM departments WHERE name = %s),
                                role_id = (SELECT id FROM roles WHERE name = %s)
                            WHERE LOWER(email) = LOWER(%s)
                        """, (name, position, department, role, email))
                        conn.commit()
                        updated_count += 1
                        print(f"   ✓ Updated: {email} ({name}) - Role: {role}")
            else:
                # Create new user
                user_id = auth.create_user(
                    email=email,
                    password='user',  # Default password
                    full_name=name,
                    role=role,
                    position=position
                )

                if user_id:
                    # Update department
                    import psycopg
                    pg_url = os.environ['DATABASE_URL'].replace('postgresql+psycopg://', 'postgresql://')

                    with psycopg.connect(pg_url) as conn:
                        with conn.cursor() as cur:
                            cur.execute("""
                                UPDATE users
                                SET department_id = (SELECT id FROM departments WHERE name = %s)
                                WHERE id = %s
                            """, (department, user_id))
                            conn.commit()

                    added_count += 1
                    print(f"   ✓ Added: {email} ({name}) - Role: {role}")
                else:
                    error_count += 1
                    print(f"   ✗ Failed: {email}")

        except Exception as e:
            error_count += 1
            print(f"   ✗ Error adding {email}: {e}")

    # Summary
    print("\n" + "=" * 70)
    print("MIGRATION SUMMARY")
    print("=" * 70)
    print(f"Total employees: {len(EMPLOYEES)}")
    print(f"Added: {added_count}")
    print(f"Updated: {updated_count}")
    print(f"Errors: {error_count}")

    # List admin users
    print(f"\n👤 ADMIN USERS:")
    print(f"   • admin (System Administrator)")
    for email in ADMIN_EMAILS:
        emp = next((e for e in EMPLOYEES if e['email'] == email), None)
        if emp:
            print(f"   • {email} ({emp['name']})")

    print(f"\n🔑 DEFAULT PASSWORD FOR ALL USERS: 'user'")
    print(f"   (Users will be prompted to change on first login)")

    # Verify total user count
    print("\n3. Verifying user count in PostgreSQL...")
    try:
        import psycopg
        from psycopg.rows import dict_row
        pg_url = os.environ['DATABASE_URL'].replace('postgresql+psycopg://', 'postgresql://')

        with psycopg.connect(pg_url, row_factory=dict_row) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT COUNT(*) as count FROM users WHERE is_active = TRUE")
                result = cur.fetchone()
                total_active = result['count']

                cur.execute("""
                    SELECT COUNT(*) as count
                    FROM users u
                    JOIN roles r ON u.role_id = r.id
                    WHERE u.is_active = TRUE AND r.name = 'admin'
                """)
                result = cur.fetchone()
                total_admins = result['count']

                cur.execute("""
                    SELECT COUNT(*) as count
                    FROM users u
                    JOIN roles r ON u.role_id = r.id
                    WHERE u.is_active = TRUE AND r.name = 'employee'
                """)
                result = cur.fetchone()
                total_employees = result['count']

                print(f"   ✓ Total active users: {total_active}")
                print(f"   ✓ Admins: {total_admins}")
                print(f"   ✓ Employees: {total_employees}")
    except Exception as e:
        print(f"   ✗ Error verifying: {e}")

    print("\n✅ MIGRATION COMPLETE!")
    print("=" * 70)

if __name__ == "__main__":
    main()
