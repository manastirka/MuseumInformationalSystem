#!/bin/bash
# ============================================================================
# Phase 3A Migration Runner
# Migrates 5 high-priority databases to PostgreSQL
# ============================================================================

echo "============================================================================"
echo "              PHASE 3A: HIGH-PRIORITY DATABASE MIGRATION"
echo "============================================================================"
echo ""
echo "This will migrate the following databases to PostgreSQL:"
echo "  1. Library Database (598 books)"
echo "  2. Exhibitions Database (~20 exhibitions)"
echo "  3. Cultural Heritage (~30 items)"
echo "  4. Meteorite Collection (~15 specimens)"
echo "  5. Employees Database (7 employees)"
echo ""
echo "============================================================================"
echo ""

# Check if PostgreSQL is running
echo "🔍 Checking PostgreSQL status..."
if systemctl is-active --quiet postgresql; then
    echo "   ✓ PostgreSQL is running"
else
    echo "   ❌ PostgreSQL is NOT running"
    echo ""
    echo "   Please start PostgreSQL first:"
    echo "   sudo systemctl start postgresql"
    echo ""
    exit 1
fi

# Check if DATABASE_URL is set
if [ -z "$DATABASE_URL" ]; then
    echo "❌ DATABASE_URL environment variable is not set"
    echo ""
    echo "   Please set DATABASE_URL in .env file or export it:"
    echo "   export DATABASE_URL=postgresql+psycopg://aleksandarlukovic@localhost:5432/museum_system"
    echo ""
    exit 1
fi

echo "   ✓ DATABASE_URL is set"
echo ""

# Ask for confirmation
read -p "Continue with migration? (yes/no): " confirm
if [ "$confirm" != "yes" ]; then
    echo "Migration cancelled."
    exit 0
fi

echo ""
echo "============================================================================"
echo "STEP 1: Apply PostgreSQL Schema"
echo "============================================================================"
echo ""

# Apply schema
psql $DATABASE_URL -f db/schema_phase3a.sql

if [ $? -ne 0 ]; then
    echo ""
    echo "❌ Schema application failed!"
    echo "   Please check the error above and fix it."
    exit 1
fi

echo ""
echo "✓ Schema applied successfully"
echo ""

echo "============================================================================"
echo "STEP 2: Migrate All 5 Databases"
echo "============================================================================"
echo ""

# Run the migration script
python3 scripts/migrate_phase3a_all.py

if [ $? -ne 0 ]; then
    echo ""
    echo "❌ Migration failed!"
    echo "   Please check the error above."
    exit 1
fi

echo ""
echo "============================================================================"
echo "STEP 3: Restart Museum System"
echo "============================================================================"
echo ""

read -p "Restart museum system now? (yes/no): " restart
if [ "$restart" == "yes" ]; then
    echo "Restarting museum-system service..."
    sudo systemctl restart museum-system

    if [ $? -eq 0 ]; then
        echo "✓ Museum system restarted"
        echo ""
        echo "   Check status: systemctl status museum-system"
        echo "   View logs: journalctl -u museum-system -f"
    else
        echo "❌ Failed to restart museum system"
    fi
fi

echo ""
echo "============================================================================"
echo "✅ PHASE 3A MIGRATION COMPLETE"
echo "============================================================================"
echo ""
echo "Next steps:"
echo "  1. Test the library database: http://localhost/admin/library_database"
echo "  2. Test exhibitions: http://localhost/admin/exhibitions_database"
echo "  3. Test cultural heritage: http://localhost/admin/cultural_heritage_database"
echo "  4. Test meteorites: http://localhost/admin/meteorite_collection"
echo "  5. Test employees: http://localhost/admin/employees_database"
echo ""
echo "If everything works, you can proceed with Phase 3B migration."
echo ""
