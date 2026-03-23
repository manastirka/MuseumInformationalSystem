# PostgreSQL Migration Complete
## Date: 2026-01-05

## Summary
Successfully migrated all museum employees to PostgreSQL authentication system. The system now uses **only PostgreSQL** for user management.

---

## User Statistics

| Category | Count |
|----------|-------|
| **Total Active Users** | 40 |
| **Admin Users** | 4 |
| **Employee Users** | 36 |

---

## Admin Users (4)

| Email | Name | Position |
|-------|------|----------|
| `admin` | System Administrator | System Admin |
| `slavko.spasic@nhmbeo.rs` | Славко Спасић | Директор (Director) |
| `biljana.mitrovic@nhmbeo.rs` | Биљана Митровић | Начелник Геолошког одељења |
| `verica.stojanovic@nhmbeo.rs` | Верица Стојановић | Кустос приправник |

---

## Login Credentials

### System Administrator
- **Username:** `admin`
- **Password:** `admin123`
- **Role:** Full system administrator

### All Museum Employees (39 users)
- **Username:** Their email address (e.g., `aca.lukovic@nhmbeo.rs`)
- **Default Password:** `user`
- **Role:** Employee (except 3 admins listed above)

---

## Employee List (Alphabetical)

### Биолошко одељење (Biology Department) - 14 employees
1. aleksandar@nhmbeo.rs - Александар Стојановић
2. aleksandra.savic@nhmbeo.rs - Александра Савић
3. ana.paunovic@nhmbeo.rs - Ана Пауновић
4. boris@nhmbeo.rs - Борис Иванчевић
5. dubravka.vucic@nhmbeo.rs - Дубравка Вучић
6. gorana.petkovski@nhmbeo.rs - Горана Петковски
7. jovan.kokotovic@nhmbeo.rs - Јован Кокотовић
8. marko.nestorovic@nhmbeo.rs - Марко Несторовић
9. milos.jovic@nhmbeo.rs - Милош Јовић
10. milos.mrvaljevic@nhmbeo.rs - Милош Мрваљевић
11. mniketic@nhmbeo.rs - Марјан Никетић
12. **verica.stojanovic@nhmbeo.rs - Верица Стојановић (ADMIN)**
13. vuk.popic@nhmbeo.rs - Вук Попић
14. zorana.markovic@nhmbeo.rs - Зорана Марковић

### Геолошко одељење (Geology Department) - 12 employees
1. aca.lukovic@nhmbeo.rs - Александар Луковић
2. amaran@nhmbeo.rs - Александра Маран Стевановић
3. **biljana.mitrovic@nhmbeo.rs - Биљана Митровић (ADMIN)**
4. branko.radulovic@nhmbeo.rs - Бранко Радуловић
5. desadjm@nhmbeo.rs - Деса Ђорђевић-Милутиновић
6. dragana.djuric@nhmbeo.rs - Драгана Ђурић
7. milos.milivojevic@nhmbeo.rs - Милош Миливојевић
8. nenad.mladenovic@nhmbeo.rs - Ненад Младеновић
9. pejovic.ranko@nhmbeo.rs - Ранко Пејовић
10. sanja.pavic@nhmbeo.rs - Сања Алабурић
11. tatjana.milicbabic@nhmbeo.rs - Татјана Милић Бабић
12. zoran.markovic@nhmbeo.rs - Зоран Марковић

### Одсек општих и правних послова (General & Legal Affairs) - 6 employees
1. ana.kovacevic@nhmbeo.rs - Ана Ковачевић
2. ana.zivanovic@nhmbeo.rs - Ана Живановић
3. biblioteka@nhmbeo.rs - Оливера Аломеровић
4. bora.m@nhmbeo.rs - Бора Милићевић
5. pedja@nhmbeo.rs - Предраг Илић

### Група за финансијско-рачуноводствене послове (Finance) - 3 employees
1. dusica.ivic@nhmbeo.rs - Душица Ивић
2. milica@nhmbeo.rs - Милица Томић
3. milenar@nhmbeo.rs - Милена Радочај

### Група за едукацију, комуникацију и маркетинг (Education & Marketing) - 2 employees
1. draganav@nhmbeo.rs - Драгана Вучићевић
2. simka.vukojevic@nhmbeo.rs - Симка Вукојевић

### Група за изложбене послове (Exhibition Gallery) - 2 employees
1. galerija@nhmbeo.rs - Снежана Јовановић
2. milica.rakic@nhmbeo.rs - Милица Ракић

### Директор (Director) - 1 employee
1. **slavko.spasic@nhmbeo.rs - Славко Спасић (ADMIN)**

---

## Password Policy

### Default Password
- All users have the default password: `user`
- Users will be prompted to change their password on first login

### Admin Account
- The system administrator account (`admin`) uses password: `admin123`
- This should be kept secure and not shared with regular employees

---

## Key Changes

### ✅ Completed
1. ✓ Activated `aca.lukovic@nhmbeo.rs` in PostgreSQL
2. ✓ Added all 39 museum employees to PostgreSQL
3. ✓ Set default password `user` for all employees
4. ✓ Granted admin privileges to:
   - slavko.spasic@nhmbeo.rs (Director)
   - biljana.mitrovic@nhmbeo.rs (Head of Geology Department)
   - verica.stojanovic@nhmbeo.rs (Curator)
5. ✓ All employees use their email addresses as usernames
6. ✓ System now uses **only PostgreSQL** for authentication

### ⚠️ Important Notes
- **SQLite databases are no longer used for authentication**
- **All future authentication uses PostgreSQL**
- Users must change their default password on first login
- Admin users have full system access
- Employee users have standard access rights

---

## Testing Results

All login tests passed successfully:
- ✓ System admin login (admin/admin123)
- ✓ Employee logins with default password (email/user)
- ✓ Admin user logins (email/user)
- ✓ Password reset functionality working

---

## Database Configuration

The system uses PostgreSQL with the following configuration:
- **Database:** `museum_system`
- **Host:** `localhost:5432`
- **User:** `aleksandarlukovic`

Authentication tables:
- `users` - User accounts
- `roles` - User roles (admin, employee, curator, viewer)
- `departments` - Department assignments

---

## Next Steps for Users

### First Login
1. Go to: `http://localhost:5555/login`
2. Enter your email address as username
3. Enter default password: `user`
4. You will be prompted to change your password
5. Set a secure new password

### Admin Users
Admin users have access to:
- All museum databases
- User management
- System configuration
- Reports and analytics
- Timesheet system

### Employee Users
Employee users have access to:
- Their assigned collections/databases
- Timesheet system
- Basic reports
- Public exhibition information

---

## Technical Details

### Migration Script
- Location: `/home/aleksandarlukovic/MuseumInfoSystem/migrate_all_employees_to_postgres.py`
- Successfully processed: 39 employees
- Added: 38 new users
- Updated: 1 existing user (aca.lukovic@nhmbeo.rs)
- Errors: 0

### Authentication Module
- Module: `postgres_auth.py`
- Uses: `psycopg` for PostgreSQL connection
- Password hashing: SHA-512 with salt
- Session management: Flask sessions with PostgreSQL backend

---

## Support

For issues or questions:
1. Contact system administrator
2. Check `/home/aleksandarlukovic/MuseumInfoSystem/logs/` for error logs
3. Refer to this document for user credentials

---

**Migration completed successfully on 2026-01-05**
