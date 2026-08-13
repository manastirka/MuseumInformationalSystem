-- Migration: Planer prostora u PostgreSQL (revizija 2026-08, batch 6, stavka 10)
-- Date: 2026-08-11
-- Purpose: operativno stanje planera prostora (admin/projekti/space-planner)
--   živelo je isključivo u data/project_space_planner.json — kršenje pravila
--   da je PostgreSQL jedini izvor istine za operativne podatke. Singleton red
--   (id = 1) sa celim stanjem kao JSONB; postojeći JSON se uvozi jednokratno
--   pri prvom čitanju (project_views.load_project_space_planner_state), posle
--   čega se fajl više ne piše.

CREATE TABLE IF NOT EXISTS project_space_planner_state (
    id         SMALLINT PRIMARY KEY DEFAULT 1 CHECK (id = 1),
    state      JSONB NOT NULL,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_by TEXT
);

COMMENT ON TABLE project_space_planner_state IS
    'Singleton stanje planera prostora (ranije data/project_space_planner.json)';
