# Museum Information System - Schema Diagram Prompt
## For AI Image Generation (System Architecture Visualization)

---

## PROMPT FOR IMAGE GENERATION:

Create a detailed system architecture diagram for the **Natural History Museum Information System (Природњачки музej у Београду)** with the following technical structure:

### **MAIN SYSTEM ARCHITECTURE** (Top Level)

**Central Hub: Flask Web Application**
- Technology: Python 3.11, Flask 2.3+, Gunicorn WSGI Server
- Deployment: systemd service on Fedora Linux
- Web Server: Nginx reverse proxy (Port 80/443 → 5555)
- Session Management: Flask-Session with server-side storage
- Security: CSRF Protection, Rate Limiting, Password Hashing (SHA-256 + salt)

---

## **LAYER 1: DATABASE TIER** (Bottom Foundation)

### PostgreSQL Database (museum_system)
**Primary database server on localhost:5432**

#### Database Schemas:

**1. Authentication & Users Schema**
```
┌─────────────────────┐
│ users               │ (45 users)
├─────────────────────┤
│ id (PK)            │
│ email              │
│ full_name          │
│ password_hash      │
│ salt               │
│ department         │
│ position           │
│ role               │
│ is_active          │
│ created_at         │
└─────────────────────┘
```

**2. Timesheet Schema** (Working Hours Management)
```
┌──────────────────────────┐      ┌──────────────────────────┐
│ timesheet_reports        │──┬──→│ timesheet_report_days    │
├──────────────────────────┤  │   ├──────────────────────────┤
│ id (PK)                 │  │   │ id (PK)                 │
│ employee_name            │  │   │ report_id (FK)          │
│ month, year              │  │   │ day (1-31)              │
│ organization_unit        │  │   │ work_in_museum          │
│ position                 │  │   │ work_outside            │
│ extraordinary_tasks      │  │   │ vacation                │
│ duties_summary           │  │   │ public_holiday          │
│ employee_signature       │  │   │ paid_leave              │
│ approver                 │  │   │ other_leave             │
│ manager_signature        │  │   │ sick_leave_lt30         │
│ director_signature       │  │   │ sick_leave_gte30        │
│ created_at               │  │   └──────────────────────────┘
└──────────────────────────┘  │
                              │   ┌──────────────────────────┐
                              └──→│ timesheet_entries        │ (normalized)
                                  ├──────────────────────────┤
                                  │ id (PK)                 │
                                  │ report_id (FK)          │
                                  │ category (8 types)      │
                                  │ hours                   │
                                  └──────────────────────────┘
                                  (Auto-synced via trigger)
```

**3. Mineral Collection Schema** (5,997 specimens)
```
┌────────────────────────┐      ┌────────────────────────┐
│ minerals               │──┬──→│ mineral_images         │
├────────────────────────┤  │   ├────────────────────────┤
│ id (PK)               │  │   │ id (PK)               │
│ inventory_number       │  │   │ mineral_id (FK)       │
│ mineral_name_latin     │  │   │ image_path            │
│ mineral_name_serbian   │  │   │ thumbnail_path        │
│ formula                │  │   │ uploaded_at           │
│ crystal_system         │  │   └────────────────────────┘
│ locality               │  │
│ country                │  │   ┌────────────────────────┐
│ discovery_year         │  └──→│ rruff_minerals         │
│ description            │      ├────────────────────────┤
│ box_number             │      │ id (PK)               │
│ created_at             │      │ rruff_id              │
└────────────────────────┘      │ mineral_name          │
                                │ chemistry             │
                                │ crystallography       │
                                │ raman_data            │
                                └────────────────────────┘
                                (External RRUFF database integration)
```

**4. Museum Collections Schema** (Curator Collections)
```
┌────────────────────────┐
│ Collection Tables:     │
├────────────────────────┤
│ • botany_collection    │ (4 specimens)
│ • entomology_collection│ (6 specimens)
│ • herpetology_collection│ (6 specimens)
│ • ichthyology_collection│ (3 specimens)
│ • mycology_collection   │ (5 specimens)
│ • ornithology_collection│ (5 specimens)
│ • paleobotany_collection│ (4 specimens)
│ • paleozoology_collection│ (6 specimens)
│ • petrology_collection  │ (4 specimens)
├────────────────────────┤
│ Common Structure:      │
│ • id (PK)             │
│ • inventory_number     │
│ • scientific_name      │
│ • common_name          │
│ • location             │
│ • date_collected       │
│ • collector            │
│ • description          │
│ • condition            │
│ • curator_notes        │
└────────────────────────┘
```

**5. Library Schema** (22,000+ titles)
```
┌────────────────────────┐
│ library_books          │
├────────────────────────┤
│ id (PK)               │
│ inventory_number       │
│ title                  │
│ author                 │
│ publisher              │
│ year                   │
│ isbn                   │
│ category               │
│ location               │
│ status                 │
│ borrower               │
│ due_date               │
│ notes                  │
└────────────────────────┘
```

**6. Exhibitions & News Schema**
```
┌────────────────────────┐      ┌────────────────────────┐
│ exhibitions            │      │ news                   │
├────────────────────────┤      ├────────────────────────┤
│ id (PK)               │      │ id (PK)               │
│ title                  │      │ title                  │
│ description            │      │ content                │
│ start_date             │      │ author                 │
│ end_date               │      │ published_date         │
│ location               │      │ category               │
│ curator                │      │ is_published           │
│ visitor_count          │      │ views                  │
│ status                 │      │ created_at             │
│ created_at             │      └────────────────────────┘
└────────────────────────┘
```

**7. Cultural Heritage Schema**
```
┌────────────────────────┐
│ cultural_heritage      │
├────────────────────────┤
│ id (PK)               │
│ registry_number        │
│ item_name              │
│ category               │
│ protection_level       │
│ registration_date      │
│ description            │
│ location               │
│ condition              │
│ guardian               │
│ documentation          │
└────────────────────────┘
```

**8. Employee Profiles Schema**
```
┌────────────────────────┐
│ employee_profiles      │
├────────────────────────┤
│ id (PK)               │
│ user_id (FK)          │
│ biography_sr           │ (Serbian)
│ biography_en           │ (English)
│ education              │
│ research_interests     │
│ publications           │
│ projects               │
│ photo_url              │
│ cv_url                 │
│ updated_at             │
└────────────────────────┘
```

**9. Bird Ringing Database** (157,115 records)
```
┌────────────────────────┐
│ bird_ringing_records   │
├────────────────────────┤
│ id (PK)               │
│ ring_number            │
│ species                │
│ scientific_name        │
│ ringing_date           │
│ ringing_location       │
│ coordinates            │
│ age                    │
│ sex                    │
│ weight                 │
│ wing_length            │
│ ringer_name            │
│ recovery_date          │
│ recovery_location      │
│ recovery_coordinates   │
│ notes                  │
└────────────────────────┘
```

**10. Vehicle Management Schema**
```
┌────────────────────────┐      ┌────────────────────────┐
│ vehicles               │──┬──→│ vehicle_reservations   │
├────────────────────────┤  │   ├────────────────────────┤
│ id (PK)               │  │   │ id (PK)               │
│ name                   │  │   │ vehicle_id (FK)       │
│ license_plate          │  │   │ user_id (FK)          │
│ type                   │  │   │ start_date            │
│ capacity               │  │   │ end_date              │
│ status                 │  │   │ purpose               │
│ last_service           │  │   │ destination           │
│ notes                  │  │   │ status                │
└────────────────────────┘  │   │ created_at            │
                            │   └────────────────────────┘
                            │
                            │   ┌────────────────────────┐
                            └──→│ vehicle_maintenance    │
                                ├────────────────────────┤
                                │ id (PK)               │
                                │ vehicle_id (FK)       │
                                │ service_date          │
                                │ service_type          │
                                │ cost                  │
                                │ notes                 │
                                └────────────────────────┘
```

**11. Meteorite Collection Schema**
```
┌────────────────────────┐
│ meteorites             │
├────────────────────────┤
│ id (PK)               │
│ inventory_number       │
│ meteorite_name         │
│ classification         │
│ fall_date              │
│ fall_location          │
│ coordinates            │
│ mass_grams             │
│ description            │
│ composition            │
│ shock_stage            │
│ weathering_grade       │
│ acquisition_info       │
└────────────────────────┘
```

---

## **LAYER 2: APPLICATION TIER** (Middle Business Logic)

### Flask Application Modules (app.py - 4,900+ lines)

**Module Structure:**

```
┌──────────────────────────────────────────┐
│          CORE APPLICATION                │
│          (app.py)                        │
├──────────────────────────────────────────┤
│                                          │
│  ┌────────────────────────────────┐    │
│  │ Authentication Module          │    │
│  ├────────────────────────────────┤    │
│  │ • Login/Logout                 │    │
│  │ • Password Management          │    │
│  │ • Session Handling             │    │
│  │ • Role-Based Access Control    │    │
│  │ • PostgreSQL Auth Integration  │    │
│  └────────────────────────────────┘    │
│                                          │
│  ┌────────────────────────────────┐    │
│  │ Timesheet Module               │    │
│  ├────────────────────────────────┤    │
│  │ • /timesheet/entry             │    │
│  │ • /api/timesheet/load          │    │
│  │ • /api/timesheet/save          │    │
│  │ • Serbian Holiday Integration  │    │
│  │ • Calendar Generation          │    │
│  │ • Auto-calculation Engine      │    │
│  │ • Edit Restrictions (1-7 rule) │    │
│  └────────────────────────────────┘    │
│                                          │
│  ┌────────────────────────────────┐    │
│  │ Mineral Database Module        │    │
│  ├────────────────────────────────┤    │
│  │ • /mineral_database            │    │
│  │ • Search & Filter              │    │
│  │ • QR Code Generation           │    │
│  │ • Image Gallery                │    │
│  │ • RRUFF Integration            │    │
│  │ • Box Management               │    │
│  └────────────────────────────────┘    │
│                                          │
│  ┌────────────────────────────────┐    │
│  │ Museum Databases Module        │    │
│  ├────────────────────────────────┤    │
│  │ • /museum_databases            │    │
│  │ • 13 Curator Collections       │    │
│  │ • Search Across Collections    │    │
│  │ • Specimen Management          │    │
│  │ • Export Functions             │    │
│  └────────────────────────────────┘    │
│                                          │
│  ┌────────────────────────────────┐    │
│  │ Library Module                 │    │
│  ├────────────────────────────────┤    │
│  │ • /library_database            │    │
│  │ • Book Catalog (22K+ titles)   │    │
│  │ • Search & Filter              │    │
│  │ • Borrowing System             │    │
│  │ • Category Management          │    │
│  └────────────────────────────────┘    │
│                                          │
│  ┌────────────────────────────────┐    │
│  │ Admin Panel Module             │    │
│  ├────────────────────────────────┤    │
│  │ • /admin/panel                 │    │
│  │ • User Management              │    │
│  │ • Access Control               │    │
│  │ • System Statistics            │    │
│  │ • Reports & Analytics          │    │
│  │ • Timesheet Approval           │    │
│  └────────────────────────────────┘    │
│                                          │
│  ┌────────────────────────────────┐    │
│  │ Exhibitions & News Module      │    │
│  ├────────────────────────────────┤    │
│  │ • /exhibitions                 │    │
│  │ • /news                        │    │
│  │ • Content Management           │    │
│  │ • Publishing System            │    │
│  └────────────────────────────────┘    │
│                                          │
│  ┌────────────────────────────────┐    │
│  │ Bird Ringing Module            │    │
│  ├────────────────────────────────┤    │
│  │ • /bird_ringing                │    │
│  │ • 157K+ Records                │    │
│  │ • Advanced Search              │    │
│  │ • Coordinate Conversion        │    │
│  │ • Recovery Tracking            │    │
│  └────────────────────────────────┘    │
│                                          │
│  ┌────────────────────────────────┐    │
│  │ AI Assistant Module            │    │
│  ├────────────────────────────────┤    │
│  │ • /ai_assistant                │    │
│  │ • Multi-provider Support:      │    │
│  │   - OpenAI (GPT-4, GPT-4o)    │    │
│  │   - Claude (Sonnet, Opus)     │    │
│  │   - Ollama (Local models)     │    │
│  │ • Database Search Integration  │    │
│  │ • Context-aware Responses      │    │
│  └────────────────────────────────┘    │
│                                          │
│  ┌────────────────────────────────┐    │
│  │ Export & Reporting Module      │    │
│  ├────────────────────────────────┤    │
│  │ • PDF Generation               │    │
│  │ • Word Document Export         │    │
│  │ • Excel Export                 │    │
│  │ • QR Labels                    │    │
│  │ • Certificates                 │    │
│  └────────────────────────────────┘    │
│                                          │
└──────────────────────────────────────────┘
```

---

## **LAYER 3: SUPPORTING SERVICES** (Side Components)

### Python Helper Modules:

**1. postgres_auth.py** - PostgreSQL Authentication
```
PostgresAuth Class
├── Connection pooling
├── User validation
├── Password verification (SHA-256 + salt)
├── Session management
└── Role retrieval
```

**2. timesheet_repository.py** - Timesheet Data Access
```
TimesheetRepository Class
├── get_month_summary()
├── get_overall_summary()
├── list_reports(pagination)
├── get_report(report_id)
└── Category aggregation
```

**3. serbian_holidays.py** - Holiday Calculator
```
SerbianHolidays Class
├── Orthodox Easter calculation
├── National holidays:
│   • New Year (Jan 1-2)
│   • Orthodox Christmas (Jan 7)
│   • Statehood Day (Feb 15)
│   • Good Friday (variable)
│   • Easter Monday (variable)
│   • Labor Day (May 1-2)
│   • Armistice Day (Nov 11)
├── is_holiday() checker
└── get_holidays_in_range()
```

**4. phase3a_databases.py** - Database Managers
```
Database Manager Classes:
├── LibraryDatabase
├── ExhibitionsDatabase
├── CulturalHeritageDatabase
├── MeteoriteDatabase
├── VehicleManager
└── ReservationManager
```

**5. image_storage_engine.py** - File Management
```
ImageStorage Class
├── Upload handling
├── Thumbnail generation
├── Path management
├── Batch processing
└── Cleanup functions
```

**6. pdf_export.py** - PDF Generation
```
PDFExporter Class
├── Specimen certificates
├── Collection reports
├── Visitor reports
├── Research project docs
└── Custom templates
```

**7. security_utils.py** - Security Functions
```
Security Module:
├── PasswordValidator
├── PasswordHasher
├── login_required decorator
├── admin_required decorator
├── CSRF protection
└── Rate limiting
```

**8. museum_llm_assistant.py** - AI Integration
```
MuseumLLMAssistant Class
├── Multi-provider support
├── Database context injection
├── Response streaming
├── Error handling
└── API key management
```

---

## **LAYER 4: USER INTERFACE** (Top Presentation)

### Frontend Stack:

**Templates (Jinja2):**
```
templates/
├── base.html (Master template)
│   ├── Bootstrap 5.3
│   ├── Bootstrap Icons
│   ├── Custom CSS (museum theme)
│   └── JavaScript modules
│
├── Authentication:
│   ├── login.html
│   ├── change_password.html
│   └── error.html
│
├── Dashboard:
│   ├── dashboard.html
│   ├── customize_dashboard.html
│   └── index.html (landing)
│
├── Timesheet (999 lines):
│   ├── employee_timesheet.html
│   ├── timesheet_integration.html
│   ├── admin_timesheet_reports.html
│   └── admin_timesheet_report_detail.html
│
├── Minerals:
│   ├── admin_mineral_collection.html
│   ├── admin_mineral_detail.html
│   ├── admin_rruff_minerals.html
│   ├── admin_rruff_detail.html
│   ├── admin_qr_labels.html
│   └── admin_batch_image_upload.html
│
├── Collections:
│   ├── admin_museum_databases.html
│   ├── admin_collection_database.html
│   └── [9 collection-specific templates]
│
├── Library:
│   └── admin_library_database.html
│
├── Admin:
│   ├── admin_panel.html
│   ├── admin_manage_access.html
│   ├── admin_statistics.html
│   └── admin_reports.html
│
├── Exhibitions & News:
│   ├── admin_exhibitions_database.html
│   └── admin_news.html
│
└── Misc:
    ├── vehicle_management.html
    ├── admin_ai_assistant.html
    └── museum_terminology.html
```

**Static Assets:**
```
static/
├── css/
│   └── custom-museum.css
├── js/
│   ├── timesheet-calendar.js
│   ├── mineral-search.js
│   ├── collection-filters.js
│   └── ai-assistant.js
├── images/
│   ├── museum-logo.png
│   ├── mineral-photos/
│   └── placeholders/
└── icons/
    └── museum-icon.ico
```

---

## **LAYER 5: EXTERNAL INTEGRATIONS** (External Systems)

**1. RRUFF Database Integration**
```
┌─────────────────────────┐
│ RRUFF Mineral Database  │
│ (rruff.info)            │
├─────────────────────────┤
│ • Mineral data import   │
│ • Crystal structures    │
│ • Raman spectra         │
│ • X-ray diffraction     │
│ • Chemistry data        │
└─────────────────────────┘
         ↕ HTTP API
┌─────────────────────────┐
│ rruff_database_pg.py    │
└─────────────────────────┘
```

**2. AI Providers**
```
┌─────────────────┐
│ OpenAI API      │
│ (GPT-4, 4o, o1) │
└─────────────────┘
         ↕
┌─────────────────┐       ┌─────────────────┐
│ Claude API      │←─────→│ AI Assistant    │
│ (Sonnet, Opus)  │       │ Module          │
└─────────────────┘       └─────────────────┘
         ↕
┌─────────────────┐
│ Ollama Local    │
│ (llama3, phi)   │
└─────────────────┘
```

---

## **DEPLOYMENT ARCHITECTURE**

```
┌─────────────────────────────────────────────────────┐
│              FEDORA LINUX SERVER                    │
├─────────────────────────────────────────────────────┤
│                                                     │
│  ┌─────────────────────────────────────────────┐  │
│  │  Nginx (Port 80/443)                        │  │
│  │  - Reverse proxy                            │  │
│  │  - SSL/TLS termination                      │  │
│  │  - Static file serving                      │  │
│  │  - Load balancing                           │  │
│  └──────────────┬──────────────────────────────┘  │
│                 ↓                                   │
│  ┌─────────────────────────────────────────────┐  │
│  │  Gunicorn WSGI (Port 5555)                  │  │
│  │  - 50 worker processes                      │  │
│  │  - Async workers                            │  │
│  │  - Auto-restart on failure                  │  │
│  └──────────────┬──────────────────────────────┘  │
│                 ↓                                   │
│  ┌─────────────────────────────────────────────┐  │
│  │  Flask Application                          │  │
│  │  - Main app (app.py)                        │  │
│  │  - All modules loaded                       │  │
│  │  - Session management                       │  │
│  └──────────────┬──────────────────────────────┘  │
│                 ↓                                   │
│  ┌─────────────────────────────────────────────┐  │
│  │  PostgreSQL (Port 5432)                     │  │
│  │  - Database: museum_system                  │  │
│  │  - 45 tables                                │  │
│  │  - Auto-backup enabled                      │  │
│  └─────────────────────────────────────────────┘  │
│                                                     │
│  ┌─────────────────────────────────────────────┐  │
│  │  systemd Services                           │  │
│  │  - museum-system.service (main app)         │  │
│  │  - postgresql.service (database)            │  │
│  │  - nginx.service (web server)               │  │
│  └─────────────────────────────────────────────┘  │
│                                                     │
└─────────────────────────────────────────────────────┘
```

---

## **USER ROLES & ACCESS CONTROL**

```
┌──────────────────────────────────────────────────┐
│              USER HIERARCHY                       │
├──────────────────────────────────────────────────┤
│                                                   │
│  SUPER ADMIN (System Administrator)              │
│  ├── All permissions                             │
│  ├── User management                             │
│  ├── System configuration                        │
│  └── Database admin                              │
│                                                   │
│  ADMIN (Museum Directors)                        │
│  ├── All databases access                        │
│  ├── Timesheet approval                          │
│  ├── Report generation                           │
│  └── Content management                          │
│                                                   │
│  DEPARTMENT HEAD                                 │
│  ├── Department collections                      │
│  ├── Team timesheet review                       │
│  └── Department reports                          │
│                                                   │
│  CURATOR                                         │
│  ├── Assigned collections                        │
│  ├── Specimen management                         │
│  ├── Research database                           │
│  └── Exhibition planning                         │
│                                                   │
│  EMPLOYEE (Regular Staff)                        │
│  ├── Own timesheet                               │
│  ├── Read-only collections                       │
│  ├── News/exhibitions view                       │
│  └── Basic search                                │
│                                                   │
└──────────────────────────────────────────────────┘
```

---

## **DATA FLOW DIAGRAM**

```
USER BROWSER
     ↓ HTTPS Request
[Nginx Reverse Proxy]
     ↓ HTTP Forward
[Gunicorn WSGI Server]
     ↓ WSGI Protocol
[Flask Application]
     ↓ Query
[PostgreSQL Database]
     ↑ Result
[Flask Application]
     ↑ Render
[Jinja2 Template Engine]
     ↑ HTML Response
[Nginx]
     ↑ HTTPS Response
USER BROWSER
```

---

## **SECURITY LAYERS**

```
┌────────────────────────────────────┐
│   1. NGINX LAYER                   │
│   - HTTPS/SSL                      │
│   - Rate limiting                  │
│   - DDoS protection                │
└────────────┬───────────────────────┘
             ↓
┌────────────────────────────────────┐
│   2. APPLICATION LAYER             │
│   - CSRF tokens                    │
│   - Session validation             │
│   - Input sanitization             │
│   - XSS prevention                 │
└────────────┬───────────────────────┘
             ↓
┌────────────────────────────────────┐
│   3. AUTHENTICATION LAYER          │
│   - Password hashing (SHA-256)     │
│   - Salt generation                │
│   - Session encryption             │
│   - Role-based access              │
└────────────┬───────────────────────┘
             ↓
┌────────────────────────────────────┐
│   4. DATABASE LAYER                │
│   - Parameterized queries          │
│   - Connection pooling             │
│   - Transaction isolation          │
│   - Audit logging                  │
└────────────────────────────────────┘
```

---

## **TECHNOLOGY STACK SUMMARY**

**Backend:**
- Python 3.11
- Flask 2.3+
- Gunicorn (WSGI)
- psycopg 3.x (PostgreSQL driver)
- SQLAlchemy (ORM, partial)

**Database:**
- PostgreSQL 15+
- 45 tables
- ~180,000 total records
- Indexes optimized

**Frontend:**
- Jinja2 templates
- Bootstrap 5.3
- Bootstrap Icons
- Vanilla JavaScript
- jQuery (minimal)

**Server:**
- Fedora Linux (Kernel 6.16)
- systemd process management
- Nginx web server
- Python venv

**Security:**
- Flask-Session
- Flask-CSRF
- Flask-Limiter
- Custom password hashing

**External:**
- OpenAI API
- Claude API
- Ollama (local AI)
- RRUFF Database API

---

## **PERFORMANCE METRICS**

- **Application size:** 4,900+ lines (app.py)
- **Total codebase:** ~15,000 lines Python
- **Templates:** 50+ HTML files
- **Database size:** ~2.5 GB
- **Worker processes:** 50 (Gunicorn)
- **Response time:** < 200ms average
- **Concurrent users:** 100+ supported
- **Uptime:** 99.9% (systemd auto-restart)

---

## **MODULE INTERCONNECTIONS**

```
         [Authentication]
                ↓
         [Dashboard] ←───────────┐
                ↓                │
    ┌───────────┴───────────┐   │
    ↓           ↓           ↓   │
[Timesheet] [Minerals] [Collections]
    ↓           ↓           ↓   │
    └───→ [Database] ←──────┘   │
                ↓                │
         [AI Assistant]          │
                ↓                │
         [Export/PDF] ───────────┘
```

---

## **VISUAL STYLE RECOMMENDATIONS FOR DIAGRAM:**

**Colors:**
- Database tier: Dark Blue (#1a365d)
- Application tier: Medium Blue (#2c5d84)
- UI tier: Light Blue (#4a90c2)
- External services: Green (#2d7a3e)
- Security layers: Orange (#d97706)
- User roles: Purple (#7c3aed)

**Icons:**
- Database: Cylinder icon
- Web app: Server icon
- Users: Person icons
- API: Cloud icons
- Security: Shield icons
- Files: Document icons

**Layout:**
- Bottom-up architecture (database → app → UI)
- Left-to-right data flow
- Grouped modules in boxes
- Clear arrows showing relationships
- Color-coded by function

---

## **DIAGRAM SECTIONS TO INCLUDE:**

1. **Title:** "Natural History Museum Information System Architecture"
2. **Subtitle:** "Природњачки музеј у Београду - Sistema arhitektura"
3. **Layer 1:** PostgreSQL Database (bottom)
4. **Layer 2:** Flask Application Modules (middle)
5. **Layer 3:** Supporting Services (sides)
6. **Layer 4:** User Interface (top)
7. **Layer 5:** External Integrations (clouds)
8. **Side panel:** User Roles & Permissions
9. **Legend:** Technology stack icons
10. **Footer:** Version, date, tech stack summary

---

**END OF SCHEMA PROMPT**

This comprehensive description includes all technical branches, components, databases, modules, integrations, security layers, and data flows of the complete museum information system.
