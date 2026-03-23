-- Museum Vehicles and Reservations Schema
-- Phase 3D: Vehicle management system migration to PostgreSQL

-- Vehicles Table
CREATE TABLE IF NOT EXISTS vehicles (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    registration TEXT UNIQUE NOT NULL,
    type TEXT,  -- 'Комби', 'Теренац', 'Путнички'
    capacity TEXT,
    status TEXT DEFAULT 'Активно',  -- 'Активно', 'У сервису', 'Неактивно'
    year TEXT,
    make_model TEXT,
    notes TEXT,
    image_ids TEXT[],  -- Array of image IDs
    created_at TIMESTAMPTZ DEFAULT now(),
    updated_at TIMESTAMPTZ DEFAULT now()
);

-- Vehicle Reservations Table
CREATE TABLE IF NOT EXISTS vehicle_reservations (
    id SERIAL PRIMARY KEY,
    vehicle_id INTEGER REFERENCES vehicles(id) ON DELETE CASCADE,
    reserved_by TEXT NOT NULL,  -- Employee name or email
    purpose TEXT NOT NULL,  -- Purpose of reservation
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    start_time TIME,
    end_time TIME,
    destination TEXT,
    estimated_km INTEGER,
    driver_name TEXT,
    driver_license TEXT,
    passengers INTEGER,
    notes TEXT,
    status TEXT DEFAULT 'Активна',  -- 'Активна', 'Завршена', 'Отказана'
    approved_by TEXT,
    approved_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT now(),
    updated_at TIMESTAMPTZ DEFAULT now(),

    -- Constraints
    CONSTRAINT valid_date_range CHECK (end_date >= start_date),
    CONSTRAINT positive_passengers CHECK (passengers IS NULL OR passengers >= 0),
    CONSTRAINT positive_km CHECK (estimated_km IS NULL OR estimated_km >= 0)
);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_vehicles_status ON vehicles(status);
CREATE INDEX IF NOT EXISTS idx_vehicles_type ON vehicles(type);
CREATE INDEX IF NOT EXISTS idx_vehicles_registration ON vehicles(registration);

CREATE INDEX IF NOT EXISTS idx_reservations_vehicle ON vehicle_reservations(vehicle_id);
CREATE INDEX IF NOT EXISTS idx_reservations_dates ON vehicle_reservations(start_date, end_date);
CREATE INDEX IF NOT EXISTS idx_reservations_status ON vehicle_reservations(status);
CREATE INDEX IF NOT EXISTS idx_reservations_reserved_by ON vehicle_reservations(reserved_by);

-- View for active reservations
CREATE OR REPLACE VIEW active_vehicle_reservations AS
SELECT
    vr.*,
    v.name as vehicle_name,
    v.registration as vehicle_registration,
    v.type as vehicle_type
FROM vehicle_reservations vr
JOIN vehicles v ON vr.vehicle_id = v.id
WHERE vr.status = 'Активна'
    AND vr.end_date >= CURRENT_DATE
ORDER BY vr.start_date, vr.start_time;

-- View for vehicle availability
CREATE OR REPLACE VIEW vehicle_availability AS
SELECT
    v.id,
    v.name,
    v.registration,
    v.type,
    v.status,
    COUNT(vr.id) FILTER (WHERE vr.status = 'Активна' AND vr.end_date >= CURRENT_DATE) as active_reservations,
    MAX(vr.end_date) FILTER (WHERE vr.status = 'Активна') as next_available_date
FROM vehicles v
LEFT JOIN vehicle_reservations vr ON v.id = vr.vehicle_id
GROUP BY v.id, v.name, v.registration, v.type, v.status;

-- View for vehicle usage statistics
CREATE OR REPLACE VIEW vehicle_usage_stats AS
SELECT
    v.id,
    v.name,
    v.registration,
    COUNT(vr.id) as total_reservations,
    COUNT(vr.id) FILTER (WHERE vr.status = 'Завршена') as completed_reservations,
    COUNT(vr.id) FILTER (WHERE vr.status = 'Активна') as active_reservations,
    COUNT(vr.id) FILTER (WHERE vr.status = 'Отказана') as cancelled_reservations,
    SUM(vr.estimated_km) FILTER (WHERE vr.status = 'Завршена') as total_km,
    MIN(vr.start_date) as first_reservation,
    MAX(vr.end_date) as last_reservation
FROM vehicles v
LEFT JOIN vehicle_reservations vr ON v.id = vr.vehicle_id
GROUP BY v.id, v.name, v.registration;

COMMENT ON TABLE vehicles IS 'Museum vehicles inventory';
COMMENT ON TABLE vehicle_reservations IS 'Vehicle reservation and booking system';
COMMENT ON VIEW active_vehicle_reservations IS 'Currently active vehicle reservations';
COMMENT ON VIEW vehicle_availability IS 'Real-time vehicle availability status';
COMMENT ON VIEW vehicle_usage_stats IS 'Vehicle usage statistics and metrics';
