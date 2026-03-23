-- Promote data from staging tables into production tables.
-- Run after staging tables are filled (per dataset).

BEGIN;

-- Set datestyle to handle DD/MM/YYYY format
SET datestyle = 'DMY';

-- Helper function to safely parse dates
CREATE OR REPLACE FUNCTION safe_parse_date(text_date TEXT) RETURNS DATE AS $$
BEGIN
    IF text_date IS NULL OR text_date = '' THEN
        RETURN NULL;
    END IF;
    IF text_date ~ '(^|/)0+(/|$)' THEN
        RETURN NULL;
    END IF;
    RETURN TRIM(TRAILING '/' FROM REPLACE(REPLACE(text_date, ' ', '/'), '.', '/'))::DATE;
EXCEPTION WHEN OTHERS THEN
    RETURN NULL;
END;
$$ LANGUAGE plpgsql;

-- Helper function to safely parse times
CREATE OR REPLACE FUNCTION safe_parse_time(text_time TEXT) RETURNS TIME AS $$
BEGIN
    IF text_time IS NULL OR text_time = '' THEN
        RETURN NULL;
    END IF;
    -- Handle decimal hour format (0.5 = 12:00, 0.25 = 06:00)
    IF text_time ~ '^0\.[0-9]+$' THEN
        RETURN make_time(
            FLOOR(text_time::NUMERIC * 24)::INTEGER,
            FLOOR((text_time::NUMERIC * 24 - FLOOR(text_time::NUMERIC * 24)) * 60)::INTEGER,
            0
        );
    END IF;
    -- Handle "HH.MM" format (16.45 = 16:45:00)
    IF text_time ~ '^[0-9]{1,2}\.[0-9]{2}$' THEN
        RETURN (REPLACE(text_time, '.', ':') || ':00')::TIME;
    END IF;
    -- Handle valid time formats
    IF text_time ~ '^[0-9]{1,2}:[0-9]{2}' THEN
        RETURN text_time::TIME;
    END IF;
    RETURN NULL;
EXCEPTION WHEN OTHERS THEN
    RETURN NULL;
END;
$$ LANGUAGE plpgsql;

/* ----------------------------- Bird Ringing ----------------------------- */
INSERT INTO bird_species (species_name)
SELECT DISTINCT species_name
FROM staging_bird_ringing
WHERE species_name IS NOT NULL
ON CONFLICT (species_name) DO NOTHING;

INSERT INTO bird_ringing_records (
    ring_number,
    color_ring,
    species_id,
    age,
    sex,
    location,
    coordinates,
    coordinate_accuracy,
    event_date,
    event_time,
    metal_ring_position,
    plastic_ring,
    catching_method,
    bait,
    manipulation,
    status,
    clutch_size,
    pullus_age,
    wing_length,
    third_primary_feather,
    mass,
    molting,
    back_claw,
    bill_length,
    bill_measurement_method,
    head_length,
    tarsus,
    tarsus_measurement_method,
    tail_length,
    fat_deposits,
    pectoral_muscle,
    incubation_patch,
    alula,
    carpal_feathers,
    sex_determination,
    protected_areas,
    ringer,
    notes,
    raw_json
)
SELECT
    NULLIF(s.ring_number, ''),
    NULLIF(s.color_ring, ''),
    bs.id AS species_id,
    NULLIF(s.age, ''),
    NULLIF(s.sex, ''),
    NULLIF(s.location, ''),
    CASE
        WHEN s.coordinates_wkt IS NULL OR s.coordinates_wkt = '' THEN NULL
        ELSE ST_GeomFromEWKT(s.coordinates_wkt)::GEOGRAPHY
    END,
    NULLIF(s.coordinate_accuracy, ''),
    safe_parse_date(s.event_date),
    safe_parse_time(s.event_time),
    CASE
        WHEN s.metal_ring_position ~ '^[0-9]+$' THEN s.metal_ring_position::INTEGER
        ELSE NULL
    END,
    NULLIF(s.plastic_ring, ''),
    NULLIF(s.catching_method, ''),
    NULLIF(s.bait, ''),
    NULLIF(s.manipulation, ''),
    NULLIF(s.status, ''),
    NULLIF(s.clutch_size, ''),
    NULLIF(s.pullus_age, ''),
    NULLIF(s.wing_length, ''),
    NULLIF(s.third_primary_feather, ''),
    NULLIF(s.mass, ''),
    NULLIF(s.molting, ''),
    NULLIF(s.back_claw, ''),
    NULLIF(s.bill_length, ''),
    NULLIF(s.bill_measurement_method, ''),
    NULLIF(s.head_length, ''),
    NULLIF(s.tarsus, ''),
    NULLIF(s.tarsus_measurement_method, ''),
    NULLIF(s.tail_length, ''),
    NULLIF(s.fat_deposits, ''),
    NULLIF(s.pectoral_muscle, ''),
    NULLIF(s.incubation_patch, ''),
    NULLIF(s.alula, ''),
    NULLIF(s.carpal_feathers, ''),
    NULLIF(s.sex_determination, ''),
    NULLIF(s.protected_areas, ''),
    NULLIF(s.ringer, ''),
    NULLIF(s.notes, ''),
    s.raw_json
FROM staging_bird_ringing s
LEFT JOIN bird_species bs ON bs.species_name = s.species_name
ON CONFLICT DO NOTHING;

TRUNCATE TABLE staging_bird_ringing;

/* -------------------------------- Minerals ----------------------------- */
INSERT INTO minerals (
    inventory_number,
    item_name,
    acquisition_method,
    acquisition_date,
    input_date,
    input_by,
    donor,
    identifier,
    comments,
    description,
    storage_location,
    card_locality,
    bibliography_flag,
    quantity,
    created_at,
    updated_at
)
SELECT
    NULLIF(inventory_number, ''),
    NULLIF(item_name, ''),
    NULLIF(acquisition_method, ''),
    safe_parse_date(acquisition_date),
    NULLIF(input_date, '')::TIMESTAMPTZ,
    NULLIF(input_by, ''),
    NULLIF(donor, ''),
    NULLIF(identifier, ''),
    NULLIF(comments, ''),
    NULLIF(description, ''),
    NULLIF(storage_location, ''),
    NULLIF(card_locality, ''),
    CASE WHEN lower(bibliography_flag) IN ('1','true','да') THEN TRUE ELSE FALSE END,
    NULLIF(quantity, '')::INTEGER,
    now(),
    now()
FROM staging_minerals
ON CONFLICT (inventory_number) DO NOTHING;

TRUNCATE TABLE staging_minerals;

/* ------------------------------- Inventory ------------------------------ */
INSERT INTO inventory_entries (
    inventory_number,
    inventory_number_raw,
    name,
    locality,
    quantity,
    acquisition_info,
    collector,
    notes,
    sheet,
    row_number,
    category,
    revisited,
    physical_location,
    revision_date,
    created_at
)
SELECT
    NULLIF(inventory_number, ''),
    NULLIF(inventory_number_raw, ''),
    NULLIF(name, ''),
    NULLIF(locality, ''),
    NULLIF(quantity, ''),
    NULLIF(acquisition_info, ''),
    NULLIF(collector, ''),
    NULLIF(notes, ''),
    NULLIF(sheet, ''),
    NULLIF(row_number, '')::INTEGER,
    NULLIF(category, ''),
    CASE WHEN revisited IN ('1', 'True', 'true') THEN TRUE ELSE FALSE END,
    NULLIF(physical_location, ''),
    safe_parse_date(revision_date),
    now()
FROM staging_inventory
ON CONFLICT (inventory_number) DO NOTHING;

TRUNCATE TABLE staging_inventory;

/* -------------------------------- Timesheets ----------------------------- */
INSERT INTO timesheet_reports (
    legacy_radna_lista_id,
    employee_name,
    month,
    year,
    organization_unit,
    position,
    special_scope,
    extraordinary_tasks,
    employee_signature,
    approver,
    manager_signature,
    director_signature,
    salary_adjustment,
    duties_summary,
    created_at
)
SELECT
    str.radna_lista_id,
    COALESCE(NULLIF(str.ime_prezime, ''), 'Непознато'),
    COALESCE(str.mesec, 1),
    COALESCE(str.godina, date_part('year', now())::INTEGER),
    NULLIF(str.organizaciona_jedinica, ''),
    NULLIF(str.radno_mesto, ''),
    NULLIF(str.poseban_obim_posla, ''),
    NULLIF(str.vanredni_poslovi, ''),
    NULLIF(str.potpis_zaposlenog, ''),
    NULLIF(str.nalogodavac, ''),
    NULLIF(str.potpis_sefa, ''),
    NULLIF(str.potpis_direktora, ''),
    NULLIF(str.povecanje_umanjenje_zarade, ''),
    NULLIF(str.o_posao, ''),
    safe_parse_date(str.created_at)::TIMESTAMPTZ
FROM staging_timesheet_reports str
ON CONFLICT (legacy_radna_lista_id) DO UPDATE
SET
    employee_name = EXCLUDED.employee_name,
    month = EXCLUDED.month,
    year = EXCLUDED.year,
    organization_unit = EXCLUDED.organization_unit,
    position = EXCLUDED.position,
    special_scope = EXCLUDED.special_scope,
    extraordinary_tasks = EXCLUDED.extraordinary_tasks,
    employee_signature = EXCLUDED.employee_signature,
    approver = EXCLUDED.approver,
    manager_signature = EXCLUDED.manager_signature,
    director_signature = EXCLUDED.director_signature,
    salary_adjustment = EXCLUDED.salary_adjustment,
    duties_summary = EXCLUDED.duties_summary,
    created_at = COALESCE(EXCLUDED.created_at, timesheet_reports.created_at);

DELETE FROM timesheet_report_days
WHERE report_id IN (
    SELECT id FROM timesheet_reports
    WHERE legacy_radna_lista_id IN (SELECT radna_lista_id FROM staging_timesheet_reports)
);

INSERT INTO timesheet_report_days (
    report_id,
    day,
    work_in_museum,
    work_outside,
    vacation,
    public_holiday,
    paid_leave,
    other_leave,
    sick_leave_lt30,
    sick_leave_gte30
)
SELECT
    tr.id,
    std.dan,
    COALESCE(std.rad_na_mestu, 0),
    COALESCE(std.van_muzeja, 0),
    COALESCE(std.godisnji_odmor, 0),
    COALESCE(std.drzavni_praznik, 0),
    COALESCE(std.placeno_odsustvo, 0),
    COALESCE(std.ostalo_odsustvo, 0),
    COALESCE(std.bolovanje_manje_30, 0),
    COALESCE(std.bolovanje_vece_30, 0)
FROM staging_timesheet_days std
JOIN timesheet_reports tr ON tr.legacy_radna_lista_id = std.radna_lista_id;

DELETE FROM timesheet_entries
WHERE report_id IN (
    SELECT id FROM timesheet_reports
    WHERE legacy_radna_lista_id IN (SELECT radna_lista_id FROM staging_timesheet_reports)
);

INSERT INTO timesheet_entries (
    user_id,
    report_id,
    employee_name,
    work_date,
    category,
    hours,
    notes
)
SELECT
    NULL,
    tr.id,
    tr.employee_name,
    CASE
        WHEN tr.month BETWEEN 1 AND 12 AND td.day BETWEEN 1 AND 31
            THEN make_date(tr.year, tr.month, td.day)
        ELSE NULL
    END AS work_date,
    metric.category,
    metric.hours,
    tr.organization_unit
FROM timesheet_report_days td
JOIN timesheet_reports tr ON tr.id = td.report_id
JOIN LATERAL (
    VALUES
        ('rad_na_mestu', NULLIF(td.work_in_museum, 0)),
        ('van_muzeja', NULLIF(td.work_outside, 0)),
        ('godisnji_odmor', NULLIF(td.vacation, 0)),
        ('drzavni_praznik', NULLIF(td.public_holiday, 0)),
        ('placeno_odsustvo', NULLIF(td.paid_leave, 0)),
        ('ostalo_odsustvo', NULLIF(td.other_leave, 0)),
        ('bolovanje_manje_30', NULLIF(td.sick_leave_lt30, 0)),
        ('bolovanje_vece_30', NULLIF(td.sick_leave_gte30, 0))
) AS metric(category, hours) ON TRUE
WHERE metric.hours IS NOT NULL
  AND (CASE
           WHEN tr.month BETWEEN 1 AND 12 AND td.day BETWEEN 1 AND 31
               THEN make_date(tr.year, tr.month, td.day)
           ELSE NULL
       END) IS NOT NULL
  AND tr.legacy_radna_lista_id IN (SELECT radna_lista_id FROM staging_timesheet_reports);

TRUNCATE TABLE staging_timesheet_days;
TRUNCATE TABLE staging_timesheet_reports;

COMMIT;
