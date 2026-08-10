-- Migration 016: drop the legacy status CHECK on `vehicle_reservations`
-- and migrate leftover English status values to the Serbian ones the
-- application uses.
--
-- Context:
--   The deployed vehicle_reservations table predates the current schema
--   and still carries vehicle_reservations_status_check, which only
--   allows ('PENDING','APPROVED','REJECTED','CANCELLED'). The application
--   (vehicle_depot_views.handle_add_vehicle_reservation) inserts the
--   status 'Активна', so every reservation INSERT fails with
--   CheckViolation. The canonical db/schema_vehicles.sql declares no
--   status CHECK at all. Current app statuses are 'Активна' / 'Завршена'
--   / 'Отказана'; legacy English rows are invisible to the calendar,
--   the reservation views and the delete-vehicle guard, so they are
--   mapped onto the Serbian equivalents.
--
-- Safe to run repeatedly (DROP ... IF EXISTS; the UPDATEs match only
-- legacy English values, so re-runs are no-ops).

ALTER TABLE vehicle_reservations
    DROP CONSTRAINT IF EXISTS vehicle_reservations_status_check;

UPDATE vehicle_reservations
    SET status = 'Активна'
    WHERE status IN ('PENDING', 'APPROVED');

UPDATE vehicle_reservations
    SET status = 'Отказана'
    WHERE status IN ('REJECTED', 'CANCELLED');

-- Rollback (only if you must revert):
--   ALTER TABLE vehicle_reservations
--       ADD CONSTRAINT vehicle_reservations_status_check
--       CHECK (status IN ('PENDING','APPROVED','REJECTED','CANCELLED'));
--   (Status values cannot be restored automatically: the mapping
--   'Активна' -> PENDING/APPROVED and 'Отказана' -> REJECTED/CANCELLED
--   is lossy.)
