--
-- PostgreSQL database dump
--

\restrict mqMbdJFOmifNmMWhDlREhkEZunehGu7NsC71I0vQy3HARwU8vZnjf5WvRu6Z5Jw

-- Dumped from database version 16.11
-- Dumped by pg_dump version 16.11

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: btree_gist; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS btree_gist WITH SCHEMA public;


--
-- Name: EXTENSION btree_gist; Type: COMMENT; Schema: -; Owner: -
--

COMMENT ON EXTENSION btree_gist IS 'support for indexing common datatypes in GiST';


--
-- Name: citext; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS citext WITH SCHEMA public;


--
-- Name: EXTENSION citext; Type: COMMENT; Schema: -; Owner: -
--

COMMENT ON EXTENSION citext IS 'data type for case-insensitive character strings';


--
-- Name: pgcrypto; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS pgcrypto WITH SCHEMA public;


--
-- Name: EXTENSION pgcrypto; Type: COMMENT; Schema: -; Owner: -
--

COMMENT ON EXTENSION pgcrypto IS 'cryptographic functions';


--
-- Name: postgis; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS postgis WITH SCHEMA public;


--
-- Name: EXTENSION postgis; Type: COMMENT; Schema: -; Owner: -
--

COMMENT ON EXTENSION postgis IS 'PostGIS geometry and geography spatial types and functions';


--
-- Name: uuid-ossp; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS "uuid-ossp" WITH SCHEMA public;


--
-- Name: EXTENSION "uuid-ossp"; Type: COMMENT; Schema: -; Owner: -
--

COMMENT ON EXTENSION "uuid-ossp" IS 'generate universally unique identifiers (UUIDs)';


--
-- Name: safe_parse_date(text); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.safe_parse_date(text_date text) RETURNS date
    LANGUAGE plpgsql
    AS $_$
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
$_$;


--
-- Name: safe_parse_time(text); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.safe_parse_time(text_time text) RETURNS time without time zone
    LANGUAGE plpgsql
    AS $_$
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
$_$;


--
-- Name: sync_timesheet_entries(integer); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.sync_timesheet_entries(p_report_id integer) RETURNS void
    LANGUAGE plpgsql
    AS $$
BEGIN
    -- Check if report still exists (important for CASCADE deletes)
    IF NOT EXISTS (SELECT 1 FROM timesheet_reports WHERE id = p_report_id) THEN
        -- Report was deleted, just clean up any orphaned entries
        DELETE FROM timesheet_entries WHERE report_id = p_report_id;
        RETURN;
    END IF;

    -- Delete existing entries for this report
    DELETE FROM timesheet_entries WHERE report_id = p_report_id;

    -- Insert aggregated categories from daily data
    INSERT INTO timesheet_entries (report_id, category, hours)
    SELECT
        p_report_id,
        'rad_na_mestu',
        COALESCE(SUM(work_in_museum), 0)
    FROM timesheet_report_days
    WHERE report_id = p_report_id
    HAVING SUM(work_in_museum) > 0;

    INSERT INTO timesheet_entries (report_id, category, hours)
    SELECT
        p_report_id,
        'van_muzeja',
        COALESCE(SUM(work_outside), 0)
    FROM timesheet_report_days
    WHERE report_id = p_report_id
    HAVING SUM(work_outside) > 0;

    INSERT INTO timesheet_entries (report_id, category, hours)
    SELECT
        p_report_id,
        'godisnji_odmor',
        COALESCE(SUM(vacation), 0)
    FROM timesheet_report_days
    WHERE report_id = p_report_id
    HAVING SUM(vacation) > 0;

    INSERT INTO timesheet_entries (report_id, category, hours)
    SELECT
        p_report_id,
        'drzavni_praznik',
        COALESCE(SUM(public_holiday), 0)
    FROM timesheet_report_days
    WHERE report_id = p_report_id
    HAVING SUM(public_holiday) > 0;

    INSERT INTO timesheet_entries (report_id, category, hours)
    SELECT
        p_report_id,
        'placeno_odsustvo',
        COALESCE(SUM(paid_leave), 0)
    FROM timesheet_report_days
    WHERE report_id = p_report_id
    HAVING SUM(paid_leave) > 0;

    INSERT INTO timesheet_entries (report_id, category, hours)
    SELECT
        p_report_id,
        'ostalo_odsustvo',
        COALESCE(SUM(other_leave), 0)
    FROM timesheet_report_days
    WHERE report_id = p_report_id
    HAVING SUM(other_leave) > 0;

    INSERT INTO timesheet_entries (report_id, category, hours)
    SELECT
        p_report_id,
        'bolovanje_manje_30',
        COALESCE(SUM(sick_leave_lt30), 0)
    FROM timesheet_report_days
    WHERE report_id = p_report_id
    HAVING SUM(sick_leave_lt30) > 0;

    INSERT INTO timesheet_entries (report_id, category, hours)
    SELECT
        p_report_id,
        'bolovanje_vece_30',
        COALESCE(SUM(sick_leave_gte30), 0)
    FROM timesheet_report_days
    WHERE report_id = p_report_id
    HAVING SUM(sick_leave_gte30) > 0;
END;
$$;


--
-- Name: FUNCTION sync_timesheet_entries(p_report_id integer); Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON FUNCTION public.sync_timesheet_entries(p_report_id integer) IS 'Synchronizes timesheet_entries from daily data for a specific report';


--
-- Name: sync_timesheet_entries_batch(integer[]); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.sync_timesheet_entries_batch(report_ids integer[]) RETURNS void
    LANGUAGE plpgsql
    AS $$
DECLARE
    rid INTEGER;
BEGIN
    FOREACH rid IN ARRAY report_ids
    LOOP
        -- Skip if report doesn't exist (cascade delete scenario)
        IF NOT EXISTS (SELECT 1 FROM timesheet_reports WHERE id = rid) THEN
            DELETE FROM timesheet_entries WHERE report_id = rid;
            CONTINUE;
        END IF;

        -- Delete existing entries for this report
        DELETE FROM timesheet_entries WHERE report_id = rid;

        -- Insert aggregated categories in a single statement
        INSERT INTO timesheet_entries (report_id, category, hours)
        SELECT
            rid,
            category,
            total_hours
        FROM (
            SELECT 'rad_na_mestu'::TEXT as category, COALESCE(SUM(work_in_museum), 0) as total_hours
            FROM timesheet_report_days WHERE report_id = rid
            UNION ALL
            SELECT 'van_muzeja', COALESCE(SUM(work_outside), 0)
            FROM timesheet_report_days WHERE report_id = rid
            UNION ALL
            SELECT 'godisnji_odmor', COALESCE(SUM(vacation), 0)
            FROM timesheet_report_days WHERE report_id = rid
            UNION ALL
            SELECT 'drzavni_praznik', COALESCE(SUM(public_holiday), 0)
            FROM timesheet_report_days WHERE report_id = rid
            UNION ALL
            SELECT 'placeno_odsustvo', COALESCE(SUM(paid_leave), 0)
            FROM timesheet_report_days WHERE report_id = rid
            UNION ALL
            SELECT 'ostalo_odsustvo', COALESCE(SUM(other_leave), 0)
            FROM timesheet_report_days WHERE report_id = rid
            UNION ALL
            SELECT 'bolovanje_manje_30', COALESCE(SUM(sick_leave_lt30), 0)
            FROM timesheet_report_days WHERE report_id = rid
            UNION ALL
            SELECT 'bolovanje_vece_30', COALESCE(SUM(sick_leave_gte30), 0)
            FROM timesheet_report_days WHERE report_id = rid
        ) AS categories
        WHERE total_hours > 0;
    END LOOP;
END;
$$;


--
-- Name: timesheet_audit_trigger(); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.timesheet_audit_trigger() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
DECLARE
    audit_action VARCHAR(20);
    old_json JSONB := NULL;
    new_json JSONB := NULL;
    summary TEXT;
BEGIN
    -- Determine action and prepare data
    IF TG_OP = 'INSERT' THEN
        audit_action := 'INSERT';
        new_json := to_jsonb(NEW);
        summary := format('Created timesheet for %s (%s/%s)',
                         NEW.employee_name,
                         NEW.month,
                         NEW.year);

    ELSIF TG_OP = 'UPDATE' THEN
        -- Detect specific action types
        IF OLD.is_verified = FALSE AND NEW.is_verified = TRUE THEN
            audit_action := 'VERIFY';
            summary := format('Verified by %s', COALESCE(NEW.verified_by, 'unknown'));
        ELSIF OLD.is_locked = FALSE AND NEW.is_locked = TRUE THEN
            audit_action := 'LOCK';
            summary := 'Locked for editing';
        ELSIF OLD.is_locked = TRUE AND NEW.is_locked = FALSE THEN
            audit_action := 'UNLOCK';
            summary := 'Unlocked for editing';
        ELSE
            audit_action := 'UPDATE';
            summary := format('Updated timesheet (version %s -> %s)',
                            COALESCE(OLD.version, 1),
                            COALESCE(NEW.version, 1));
        END IF;

        old_json := to_jsonb(OLD);
        new_json := to_jsonb(NEW);

    ELSIF TG_OP = 'DELETE' THEN
        audit_action := 'DELETE';
        old_json := to_jsonb(OLD);
        summary := format('Deleted timesheet for %s (%s/%s)',
                         OLD.employee_name,
                         OLD.month,
                         OLD.year);
    END IF;

    -- Insert audit record
    INSERT INTO timesheet_audit_log (
        report_id,
        action,
        changed_by,
        old_values,
        new_values,
        change_summary
    ) VALUES (
        COALESCE(NEW.id, OLD.id),
        audit_action,
        COALESCE(NEW.verified_by, NEW.employee_email, OLD.employee_email, 'system'),
        old_json,
        new_json,
        summary
    );

    -- Return appropriate value
    IF TG_OP = 'DELETE' THEN
        RETURN OLD;
    ELSE
        RETURN NEW;
    END IF;
END;
$$;


--
-- Name: timesheet_reports_version_trigger(); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.timesheet_reports_version_trigger() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
    -- Only increment if version wasn't explicitly set in the UPDATE
    IF NEW.version = OLD.version THEN
        NEW.version := OLD.version + 1;
    END IF;
    NEW.updated_at := now();
    RETURN NEW;
END;
$$;


--
-- Name: trigger_sync_timesheet_entries(); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.trigger_sync_timesheet_entries() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
    -- For DELETE operations, check if the report still exists
    -- CASCADE delete on timesheet_reports will clean up entries automatically
    IF TG_OP = 'DELETE' THEN
        -- Only sync if report still exists (not a cascade delete)
        IF EXISTS (SELECT 1 FROM timesheet_reports WHERE id = OLD.report_id) THEN
            PERFORM sync_timesheet_entries(OLD.report_id);
        END IF;
        RETURN OLD;
    ELSE
        PERFORM sync_timesheet_entries(NEW.report_id);
        RETURN NEW;
    END IF;
END;
$$;


--
-- Name: FUNCTION trigger_sync_timesheet_entries(); Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON FUNCTION public.trigger_sync_timesheet_entries() IS 'Trigger function to auto-sync entries when daily data changes';


--
-- Name: trigger_sync_timesheet_entries_statement(); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.trigger_sync_timesheet_entries_statement() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
DECLARE
    affected_ids INTEGER[];
BEGIN
    -- Collect unique report_ids from transition tables
    IF TG_OP = 'INSERT' OR TG_OP = 'UPDATE' THEN
        SELECT ARRAY_AGG(DISTINCT report_id) INTO affected_ids
        FROM new_table;
    END IF;

    IF TG_OP = 'DELETE' OR TG_OP = 'UPDATE' THEN
        IF affected_ids IS NULL THEN
            SELECT ARRAY_AGG(DISTINCT report_id) INTO affected_ids
            FROM old_table;
        ELSE
            -- Merge with old_table report_ids for UPDATE
            SELECT ARRAY_AGG(DISTINCT rid) INTO affected_ids
            FROM (
                SELECT UNNEST(affected_ids) AS rid
                UNION
                SELECT report_id FROM old_table
            ) AS combined;
        END IF;
    END IF;

    -- Process all affected reports in batch
    IF affected_ids IS NOT NULL AND array_length(affected_ids, 1) > 0 THEN
        PERFORM sync_timesheet_entries_batch(affected_ids);
    END IF;

    RETURN NULL;  -- Statement-level triggers return NULL
END;
$$;


SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: vehicle_reservations; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.vehicle_reservations (
    id integer NOT NULL,
    vehicle_id integer,
    reserved_by text,
    purpose text NOT NULL,
    start_date date NOT NULL,
    end_date date NOT NULL,
    start_time time without time zone,
    end_time time without time zone,
    destination text,
    estimated_km integer,
    driver_name text,
    driver_license text,
    passengers integer,
    notes text,
    status text DEFAULT 'Активна'::text,
    approved_by text,
    approved_at timestamp with time zone,
    created_at timestamp with time zone DEFAULT now(),
    updated_at timestamp with time zone DEFAULT now(),
    requester_email text,
    requester_name text,
    starts_at timestamp with time zone DEFAULT now(),
    ends_at timestamp with time zone DEFAULT (now() + '01:00:00'::interval),
    rejected_by text,
    rejected_at timestamp with time zone,
    rejection_note text,
    reservation_date timestamp with time zone,
    return_date timestamp with time zone,
    CONSTRAINT positive_km CHECK (((estimated_km IS NULL) OR (estimated_km >= 0))),
    CONSTRAINT positive_passengers CHECK (((passengers IS NULL) OR (passengers >= 0))),
    CONSTRAINT valid_date_range CHECK ((end_date >= start_date))
);


--
-- Name: TABLE vehicle_reservations; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TABLE public.vehicle_reservations IS 'Vehicle reservation and booking system';


--
-- Name: vehicles; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.vehicles (
    id integer NOT NULL,
    name text NOT NULL,
    registration text NOT NULL,
    type text,
    capacity text,
    status text DEFAULT 'Активно'::text,
    year text,
    make_model text,
    notes text,
    image_ids text[],
    created_at timestamp with time zone DEFAULT now(),
    updated_at timestamp with time zone DEFAULT now(),
    vin text,
    model_variant text,
    max_mass_kg integer,
    curb_mass_kg integer,
    engine_displacement_cc integer,
    engine_power_kw integer,
    fuel_type text,
    fuel_consumption real
);


--
-- Name: TABLE vehicles; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TABLE public.vehicles IS 'Museum vehicles inventory';


--
-- Name: active_vehicle_reservations; Type: VIEW; Schema: public; Owner: -
--

CREATE VIEW public.active_vehicle_reservations AS
 SELECT vr.id,
    vr.vehicle_id,
    vr.reserved_by,
    vr.purpose,
    vr.start_date,
    vr.end_date,
    vr.start_time,
    vr.end_time,
    vr.destination,
    vr.estimated_km,
    vr.driver_name,
    vr.driver_license,
    vr.passengers,
    vr.notes,
    vr.status,
    vr.approved_by,
    vr.approved_at,
    vr.created_at,
    vr.updated_at,
    v.name AS vehicle_name,
    v.registration AS vehicle_registration,
    v.type AS vehicle_type
   FROM (public.vehicle_reservations vr
     JOIN public.vehicles v ON ((vr.vehicle_id = v.id)))
  WHERE ((vr.status = 'Активна'::text) AND (vr.end_date >= CURRENT_DATE))
  ORDER BY vr.start_date, vr.start_time;


--
-- Name: VIEW active_vehicle_reservations; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON VIEW public.active_vehicle_reservations IS 'Currently active vehicle reservations';


--
-- Name: app_shared_settings; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.app_shared_settings (
    setting_key text NOT NULL,
    setting_value jsonb NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL
);


--
-- Name: approval_signatures; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.approval_signatures (
    id integer NOT NULL,
    request_id integer,
    approver_role character varying(100) NOT NULL,
    approver_email character varying(255),
    approver_name character varying(255),
    decision character varying(20) DEFAULT 'pending'::character varying,
    comments text,
    signed_at timestamp without time zone,
    signature_order integer NOT NULL
);


--
-- Name: TABLE approval_signatures; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TABLE public.approval_signatures IS 'Tracks approval decisions by each approver in the chain';


--
-- Name: approval_signatures_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.approval_signatures_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: approval_signatures_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.approval_signatures_id_seq OWNED BY public.approval_signatures.id;


--
-- Name: archive_requests; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.archive_requests (
    id integer NOT NULL,
    request_type character varying(50) NOT NULL,
    subtype character varying(100),
    title character varying(500) NOT NULL,
    description text,
    request_data jsonb DEFAULT '{}'::jsonb,
    status character varying(50) DEFAULT 'pending'::character varying,
    priority character varying(20) DEFAULT 'normal'::character varying,
    created_by_email character varying(255) NOT NULL,
    created_by_name character varying(255),
    created_by_department character varying(255),
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    attachments jsonb DEFAULT '[]'::jsonb,
    approval_chain jsonb DEFAULT '[]'::jsonb,
    current_approval_step integer DEFAULT 0,
    final_decision character varying(50),
    final_decision_by_email character varying(255),
    final_decision_by_name character varying(255),
    final_decision_at timestamp without time zone,
    final_notes text,
    archived_at timestamp without time zone,
    archive_reference character varying(100),
    archive_year integer
);


--
-- Name: TABLE archive_requests; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TABLE public.archive_requests IS 'Main table for all archive requests (zahtevi, finansije, terenska aktivnost)';


--
-- Name: COLUMN archive_requests.request_type; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.archive_requests.request_type IS 'Type: zahtev, finansije, terenska_aktivnost';


--
-- Name: COLUMN archive_requests.request_data; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.archive_requests.request_data IS 'Type-specific data stored as JSON';


--
-- Name: COLUMN archive_requests.approval_chain; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.archive_requests.approval_chain IS 'JSON array: [{role, order, required}]';


--
-- Name: archive_requests_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.archive_requests_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: archive_requests_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.archive_requests_id_seq OWNED BY public.archive_requests.id;


--
-- Name: audit_log; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.audit_log (
    id bigint NOT NULL,
    table_name text NOT NULL,
    record_id bigint,
    action text NOT NULL,
    old_values jsonb,
    new_values jsonb,
    performed_by integer,
    performed_at timestamp with time zone DEFAULT now(),
    ip_address inet,
    changed_by text,
    change_summary text,
    user_agent text,
    record_ref text
);


--
-- Name: TABLE audit_log; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TABLE public.audit_log IS 'Globalni audit trag osetljivih akcija (piše aplikacija, best-effort)';


--
-- Name: COLUMN audit_log.table_name; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.audit_log.table_name IS 'Tip/tabela entiteta (mineral, user, module_access, nabavka, fotografije, ...)';


--
-- Name: COLUMN audit_log.record_id; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.audit_log.record_id IS 'Numerički id pogođenog zapisa (NULL kad id nije broj)';


--
-- Name: COLUMN audit_log.changed_by; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.audit_log.changed_by IS 'Email aktera (app-level upisi); za starije upise koristi performed_by → users.id';


--
-- Name: COLUMN audit_log.change_summary; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.audit_log.change_summary IS 'Čitljiv opis akcije';


--
-- Name: COLUMN audit_log.record_ref; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.audit_log.record_ref IS 'Tekstualni id pogođenog zapisa (email, registracija, module_key)';


--
-- Name: audit_log_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.audit_log_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: audit_log_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.audit_log_id_seq OWNED BY public.audit_log.id;


--
-- Name: audit_outbox; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.audit_outbox (
    id bigint NOT NULL,
    table_name text NOT NULL,
    record_id bigint,
    record_ref text,
    action text NOT NULL,
    changed_by text NOT NULL,
    old_values jsonb,
    new_values jsonb,
    change_summary text,
    ip_address inet,
    user_agent text,
    status text DEFAULT 'PENDING'::text NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    flushed_at timestamp with time zone,
    CONSTRAINT audit_outbox_status_check CHECK ((status = ANY (ARRAY['PENDING'::text, 'CONFIRMED'::text, 'ABORTED'::text])))
);


--
-- Name: TABLE audit_outbox; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TABLE public.audit_outbox IS 'Outbox za audit fajlskih radnji: namera pre radnje, potvrda posle, flush u audit_log';


--
-- Name: audit_outbox_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.audit_outbox_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: audit_outbox_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.audit_outbox_id_seq OWNED BY public.audit_outbox.id;


--
-- Name: bilja_hydrobioidea_radoman; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.bilja_hydrobioidea_radoman (
    id integer NOT NULL,
    redni_broj integer,
    inventarski_broj text,
    klasa text,
    red text,
    familija text,
    rod text,
    vrsta text,
    tipska_vrsta text,
    sinonim text,
    lokalitet text,
    rasprostranjenost text,
    datum_nalaska text,
    broj_primeraka text,
    holotip text,
    paratip text,
    lektotip text,
    paralektotip text,
    dimenzije_ljusture text,
    ekoloske_osobine text,
    legator text,
    odredba text,
    zbirka_orman_kutija text,
    ugrozenost text,
    napomena text,
    literatura text,
    source_file text,
    created_at timestamp with time zone DEFAULT now(),
    updated_at timestamp with time zone DEFAULT now()
);


--
-- Name: TABLE bilja_hydrobioidea_radoman; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TABLE public.bilja_hydrobioidea_radoman IS 'Hydrobioidea zbirka Pavla Radomana — recentni gastropodi, tipski primerci. Kategorija: biologija.';


--
-- Name: bilja_hydrobioidea_radoman_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.bilja_hydrobioidea_radoman_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: bilja_hydrobioidea_radoman_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.bilja_hydrobioidea_radoman_id_seq OWNED BY public.bilja_hydrobioidea_radoman.id;


--
-- Name: bilja_kenozojske_invertebrate; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.bilja_kenozojske_invertebrate (
    id integer NOT NULL,
    redni_broj integer,
    inventarski_broj text,
    klasa text,
    red text,
    familija text,
    rod text,
    vrsta text,
    sinonim text,
    lokalitet text,
    stratigrafski_nivo text,
    datum_nalaska text,
    nalazac text,
    odredba text,
    napomena text,
    dimenzije text,
    broj_primeraka text,
    source_file text,
    created_at timestamp with time zone DEFAULT now(),
    updated_at timestamp with time zone DEFAULT now()
);


--
-- Name: TABLE bilja_kenozojske_invertebrate; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TABLE public.bilja_kenozojske_invertebrate IS 'Kenozojske invertebrate inventarska knjiga — fosilni invertebrati (kvartar/diluvium). Kategorija: paleozoologija.';


--
-- Name: bilja_kenozojske_invertebrate_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.bilja_kenozojske_invertebrate_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: bilja_kenozojske_invertebrate_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.bilja_kenozojske_invertebrate_id_seq OWNED BY public.bilja_kenozojske_invertebrate.id;


--
-- Name: bilja_opsta_zbirka_mollusca; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.bilja_opsta_zbirka_mollusca (
    id integer NOT NULL,
    redni_broj integer,
    inventarski_broj text,
    klasa text,
    red text,
    familija text,
    rod text,
    vrsta text,
    sinonim text,
    lokalitet text,
    rasprostranjenost text,
    datum_nalaska text,
    broj_primeraka text,
    dimenzije_ljusture text,
    ekoloske_osobine text,
    ps_pavlovic text,
    odredba text,
    zbirka_orman_kutija text,
    ugrozenost text,
    napomena text,
    literatura text,
    source_file text,
    created_at timestamp with time zone DEFAULT now(),
    updated_at timestamp with time zone DEFAULT now()
);


--
-- Name: TABLE bilja_opsta_zbirka_mollusca; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TABLE public.bilja_opsta_zbirka_mollusca IS 'Opšta zbirka mekušaca (Bivalvia/Gastropoda, razni sakupljači). Kategorija: biologija.';


--
-- Name: bilja_opsta_zbirka_mollusca_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.bilja_opsta_zbirka_mollusca_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: bilja_opsta_zbirka_mollusca_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.bilja_opsta_zbirka_mollusca_id_seq OWNED BY public.bilja_opsta_zbirka_mollusca.id;


--
-- Name: bilja_recentni_morski_mekusci; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.bilja_recentni_morski_mekusci (
    id integer NOT NULL,
    redni_broj integer,
    inventarski_broj text,
    klasa text,
    red text,
    familija text,
    rod text,
    vrsta text,
    sinonim text,
    lokalitet text,
    rasprostranjenost text,
    datum_nalaska text,
    broj_primeraka text,
    izbrojan_broj_primeraka text,
    dimenzije_ljusture text,
    ekoloske_osobine text,
    ps_pavlovic text,
    odredba text,
    zbirka_orman_kutija text,
    ugrozenost text,
    napomena text,
    literatura text,
    source_file text,
    created_at timestamp with time zone DEFAULT now(),
    updated_at timestamp with time zone DEFAULT now()
);


--
-- Name: TABLE bilja_recentni_morski_mekusci; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TABLE public.bilja_recentni_morski_mekusci IS 'Recentni morski mekušci (Bivalvia + Gastropoda). Kategorija: biologija.';


--
-- Name: bilja_recentni_morski_mekusci_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.bilja_recentni_morski_mekusci_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: bilja_recentni_morski_mekusci_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.bilja_recentni_morski_mekusci_id_seq OWNED BY public.bilja_recentni_morski_mekusci.id;


--
-- Name: bilja_skoljke_tadic; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.bilja_skoljke_tadic (
    id integer NOT NULL,
    redni_broj integer,
    inventarski_broj text,
    klasa text,
    red text,
    familija text,
    rod text,
    vrsta text,
    podvrsta text,
    sinonim text,
    lokalitet text,
    datum_nalaska text,
    broj_primeraka text,
    broj_levih_kapaka text,
    broj_desnih_kapaka text,
    boja_ljusture_forel_ule text,
    dimenzije_kapka text,
    tip_brave text,
    ekoloske_osobine text,
    sakupljac text,
    odredba text,
    zbirka_orman_kutija text,
    napomena text,
    literatura text,
    source_file text,
    created_at timestamp with time zone DEFAULT now(),
    updated_at timestamp with time zone DEFAULT now()
);


--
-- Name: TABLE bilja_skoljke_tadic; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TABLE public.bilja_skoljke_tadic IS 'Zbirka školjki Ante Tadića — recentni slatkovodni bivalvi (Unio i dr.). Kategorija: biologija.';


--
-- Name: bilja_skoljke_tadic_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.bilja_skoljke_tadic_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: bilja_skoljke_tadic_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.bilja_skoljke_tadic_id_seq OWNED BY public.bilja_skoljke_tadic.id;


--
-- Name: bilja_suvozemni_puzevi_pavlovic; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.bilja_suvozemni_puzevi_pavlovic (
    id integer NOT NULL,
    redni_broj integer,
    inventarski_broj text,
    klasa text,
    red text,
    familija text,
    rod text,
    vrsta text,
    sinonim text,
    lokalitet text,
    rasprostranjenost text,
    datum_nalaska text,
    broj_primeraka text,
    dimenzije_ljusture text,
    ekoloske_osobine text,
    ps_pavlovic text,
    odredba text,
    zbirka_orman_kutija text,
    ugrozenost text,
    napomena text,
    literatura text,
    source_file text,
    created_at timestamp with time zone DEFAULT now(),
    updated_at timestamp with time zone DEFAULT now()
);


--
-- Name: TABLE bilja_suvozemni_puzevi_pavlovic; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TABLE public.bilja_suvozemni_puzevi_pavlovic IS 'Zbirka suvozemnih puževa P. S. Pavlovića — recentni gastropodi. Kategorija: biologija.';


--
-- Name: bilja_suvozemni_puzevi_pavlovic_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.bilja_suvozemni_puzevi_pavlovic_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: bilja_suvozemni_puzevi_pavlovic_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.bilja_suvozemni_puzevi_pavlovic_id_seq OWNED BY public.bilja_suvozemni_puzevi_pavlovic.id;


--
-- Name: bird_ringing_records; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.bird_ringing_records (
    id bigint NOT NULL,
    ring_number text,
    species_id integer,
    age text,
    sex text,
    location text,
    coordinates public.geography(Point,4326),
    coordinate_accuracy text,
    event_date date,
    event_time time without time zone,
    metal_ring_position integer,
    plastic_ring text,
    catching_method text,
    bait text,
    manipulation text,
    status text,
    clutch_size text,
    pullus_age text,
    wing_length text,
    third_primary_feather text,
    mass text,
    molting text,
    back_claw text,
    bill_length text,
    bill_measurement_method text,
    head_length text,
    tarsus text,
    tarsus_measurement_method text,
    tail_length text,
    fat_deposits text,
    pectoral_muscle text,
    incubation_patch text,
    alula text,
    carpal_feathers text,
    sex_determination text,
    protected_areas text,
    ringer text,
    notes text,
    raw_json jsonb,
    created_at timestamp with time zone DEFAULT now(),
    color_ring text
);


--
-- Name: bird_ringing_records_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.bird_ringing_records_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: bird_ringing_records_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.bird_ringing_records_id_seq OWNED BY public.bird_ringing_records.id;


--
-- Name: bird_species; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.bird_species (
    id integer NOT NULL,
    species_name text NOT NULL
);


--
-- Name: bird_species_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.bird_species_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: bird_species_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.bird_species_id_seq OWNED BY public.bird_species.id;


--
-- Name: chat_messages; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.chat_messages (
    id bigint NOT NULL,
    user_id integer NOT NULL,
    user_name text NOT NULL,
    user_email public.citext NOT NULL,
    user_department text DEFAULT ''::text,
    channel text DEFAULT 'general'::text NOT NULL,
    message text DEFAULT ''::text NOT NULL,
    file_name text,
    file_path text,
    file_size bigint,
    file_type text,
    "timestamp" text NOT NULL,
    ts_epoch double precision NOT NULL
);


--
-- Name: chat_messages_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.chat_messages_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: chat_messages_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.chat_messages_id_seq OWNED BY public.chat_messages.id;


--
-- Name: chat_presence; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.chat_presence (
    user_id integer NOT NULL,
    user_name text NOT NULL,
    user_email public.citext NOT NULL,
    user_department text DEFAULT ''::text,
    status text DEFAULT 'online'::text NOT NULL,
    last_seen double precision NOT NULL
);


--
-- Name: chat_unread_cursors; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.chat_unread_cursors (
    user_id integer NOT NULL,
    channel text NOT NULL,
    last_read_epoch double precision DEFAULT 0 NOT NULL
);


--
-- Name: collection_specimens; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.collection_specimens (
    id integer NOT NULL,
    catalog_number text NOT NULL,
    collection_type text NOT NULL,
    scientific_name text NOT NULL,
    common_name_sr text,
    common_name_en text,
    family text,
    order_name text,
    class_name text,
    phylum text,
    kingdom text,
    location_found text,
    locality_details text,
    habitat text,
    altitude text,
    coordinates public.geography(Point,4326),
    date_collected date,
    collector text,
    collection_method text,
    age text,
    sex text,
    condition text,
    preparation_type text,
    measurements jsonb,
    endemic_status text,
    conservation_status text,
    iucn_status text,
    storage_location text,
    herbarium_number text,
    accession_number text,
    curator text,
    description text,
    notes text,
    images text[],
    status text DEFAULT 'active'::text,
    created_at timestamp with time zone DEFAULT now(),
    updated_at timestamp with time zone DEFAULT now()
);


--
-- Name: TABLE collection_specimens; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TABLE public.collection_specimens IS 'Phase 3C: Unified biological collection specimens';


--
-- Name: collection_specimens_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.collection_specimens_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: collection_specimens_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.collection_specimens_id_seq OWNED BY public.collection_specimens.id;


--
-- Name: collection_types; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.collection_types (
    id integer NOT NULL,
    code text NOT NULL,
    name_sr text NOT NULL,
    name_en text,
    icon text,
    description_sr text,
    description_en text,
    created_at timestamp with time zone DEFAULT now()
);


--
-- Name: TABLE collection_types; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TABLE public.collection_types IS 'Collection type definitions for biological collections';


--
-- Name: collection_statistics; Type: VIEW; Schema: public; Owner: -
--

CREATE VIEW public.collection_statistics AS
 SELECT ct.code,
    ct.name_sr,
    count(cs.id) AS total_specimens,
    count(cs.id) FILTER (WHERE ((cs.endemic_status IS NOT NULL) AND (cs.endemic_status <> ''::text))) AS endemic_species,
    count(cs.id) FILTER (WHERE ((cs.conservation_status ~~ '%угрожен%'::text) OR (cs.conservation_status ~~ '%endangered%'::text))) AS threatened_species,
    count(cs.id) FILTER (WHERE (cs.status = 'on_display'::text)) AS on_display,
    count(DISTINCT cs.family) AS families_count,
    min(cs.date_collected) AS earliest_specimen,
    max(cs.date_collected) AS latest_specimen
   FROM (public.collection_types ct
     LEFT JOIN public.collection_specimens cs ON ((ct.code = cs.collection_type)))
  GROUP BY ct.code, ct.name_sr;


--
-- Name: VIEW collection_statistics; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON VIEW public.collection_statistics IS 'Real-time statistics for each collection type';


--
-- Name: collection_types_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.collection_types_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: collection_types_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.collection_types_id_seq OWNED BY public.collection_types.id;


--
-- Name: departments; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.departments (
    id integer NOT NULL,
    name text NOT NULL,
    created_at timestamp with time zone DEFAULT now()
);


--
-- Name: departments_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.departments_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: departments_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.departments_id_seq OWNED BY public.departments.id;


--
-- Name: digitized_profiles; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.digitized_profiles (
    id text NOT NULL,
    digitized_by text,
    profile jsonb NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL
);


--
-- Name: document_audit_log; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.document_audit_log (
    id integer NOT NULL,
    document_id integer NOT NULL,
    version_id integer,
    action text NOT NULL,
    actor_email text NOT NULL,
    note text,
    created_at timestamp with time zone DEFAULT now() NOT NULL
);


--
-- Name: TABLE document_audit_log; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TABLE public.document_audit_log IS 'Who did what and when across the document approval workflow';


--
-- Name: document_audit_log_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.document_audit_log_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: document_audit_log_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.document_audit_log_id_seq OWNED BY public.document_audit_log.id;


--
-- Name: document_signatures; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.document_signatures (
    id integer NOT NULL,
    document_type character varying(100) NOT NULL,
    document_id integer,
    document_title character varying(500) NOT NULL,
    document_pdf_path character varying(500),
    requester_email character varying(255) NOT NULL,
    requester_name character varying(255),
    requester_department character varying(255),
    status character varying(50) DEFAULT 'pending_signature'::character varying,
    requester_signed_at timestamp without time zone,
    requester_signature_valid boolean DEFAULT false,
    requester_certificate_info jsonb DEFAULT '{}'::jsonb,
    legal_verified_at timestamp without time zone,
    legal_verified_by_email character varying(255),
    legal_verified_by_name character varying(255),
    legal_verification_notes text,
    legal_certificate_info jsonb DEFAULT '{}'::jsonb,
    approver_signed_at timestamp without time zone,
    approver_email character varying(255),
    approver_name character varying(255),
    approver_certificate_info jsonb DEFAULT '{}'::jsonb,
    registration_number character varying(100),
    registered_at timestamp without time zone,
    registered_by_email character varying(255),
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    notes text,
    document_hash character varying(256),
    signed_document_path character varying(500)
);


--
-- Name: TABLE document_signatures; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TABLE public.document_signatures IS 'Tracks digital signatures on official documents per Serbian KEP requirements';


--
-- Name: COLUMN document_signatures.registration_number; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.document_signatures.registration_number IS 'Official registration number (delovodni broj)';


--
-- Name: COLUMN document_signatures.document_hash; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.document_signatures.document_hash IS 'SHA-256 hash of original document for integrity verification';


--
-- Name: document_signatures_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.document_signatures_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: document_signatures_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.document_signatures_id_seq OWNED BY public.document_signatures.id;


--
-- Name: document_versions; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.document_versions (
    id integer NOT NULL,
    document_id integer NOT NULL,
    version_no integer NOT NULL,
    file_path text NOT NULL,
    original_filename text NOT NULL,
    mime_type text,
    file_size bigint,
    sha256 character(64),
    status text DEFAULT 'nacrt'::text NOT NULL,
    uploaded_by_email text NOT NULL,
    uploaded_at timestamp with time zone DEFAULT now() NOT NULL,
    submitted_at timestamp with time zone,
    reviewed_by_email text,
    reviewed_at timestamp with time zone,
    review_comment text,
    CONSTRAINT document_versions_status_check CHECK ((status = ANY (ARRAY['nacrt'::text, 'na_odobrenju'::text, 'odobreno'::text, 'arhivirano'::text])))
);


--
-- Name: TABLE document_versions; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TABLE public.document_versions IS 'One row per uploaded file version; file_path is relative to DOCUMENTS_STORAGE_PATH';


--
-- Name: document_versions_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.document_versions_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: document_versions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.document_versions_id_seq OWNED BY public.document_versions.id;


--
-- Name: documents; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.documents (
    id integer NOT NULL,
    title text NOT NULL,
    description text,
    category text NOT NULL,
    department text,
    created_by_email text NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    is_active boolean DEFAULT true NOT NULL,
    CONSTRAINT documents_category_check CHECK ((category = ANY (ARRAY['obrasci_zahtevi'::text, 'uputstva'::text, 'pravilnici'::text, 'finansije'::text, 'izvestaji'::text, 'organizacija'::text, 'ostalo'::text])))
);


--
-- Name: TABLE documents; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TABLE public.documents IS 'Logical museum documents; the actual files are per-version rows in document_versions';


--
-- Name: documents_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.documents_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: documents_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.documents_id_seq OWNED BY public.documents.id;


--
-- Name: employee_profiles; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.employee_profiles (
    id integer NOT NULL,
    user_id integer,
    employee_id character varying(50),
    full_name text NOT NULL,
    name_cyrillic text,
    date_of_birth date,
    place_of_birth text,
    nationality character varying(100),
    email public.citext NOT NULL,
    phone character varying(50),
    mobile character varying(50),
    emergency_contact text,
    emergency_phone character varying(50),
    "position" text NOT NULL,
    department character varying(100),
    division character varying(100),
    employment_type character varying(50),
    employment_status character varying(50) DEFAULT 'активан'::character varying,
    hire_date date,
    termination_date date,
    contract_type character varying(50),
    academic_title character varying(100),
    academic_degree character varying(100),
    education_level character varying(100),
    specialization text,
    university text,
    graduation_year integer,
    expertise_areas text[],
    research_interests text[],
    languages_spoken text[],
    certifications text[],
    memberships text[],
    publications_count integer DEFAULT 0,
    research_projects text[],
    awards text[],
    biography text,
    biography_short text,
    professional_experience text,
    office_location text,
    office_phone character varying(50),
    office_hours text,
    photo_url text,
    cv_url text,
    notes text,
    metadata jsonb,
    created_at timestamp with time zone DEFAULT now(),
    updated_at timestamp with time zone DEFAULT now(),
    is_department_head boolean DEFAULT false NOT NULL
);


--
-- Name: TABLE employee_profiles; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TABLE public.employee_profiles IS 'Phase 3A: Employee database - Enhanced from employee_directory.json';


--
-- Name: employee_profiles_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.employee_profiles_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: employee_profiles_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.employee_profiles_id_seq OWNED BY public.employee_profiles.id;


--
-- Name: employee_publications; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.employee_publications (
    id integer NOT NULL,
    employee_id integer,
    publication_type character varying(100),
    title text NOT NULL,
    authors text[],
    publication_year integer,
    journal text,
    publisher text,
    doi text,
    isbn text,
    url text,
    citation text,
    abstract text,
    keywords text[],
    created_at timestamp with time zone DEFAULT now()
);


--
-- Name: employee_publications_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.employee_publications_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: employee_publications_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.employee_publications_id_seq OWNED BY public.employee_publications.id;


--
-- Name: employee_statistics; Type: VIEW; Schema: public; Owner: -
--

CREATE VIEW public.employee_statistics AS
 SELECT count(*) AS total_employees,
    count(*) FILTER (WHERE ((employment_status)::text = 'активан'::text)) AS active_employees,
    count(DISTINCT department) AS total_departments,
    count(DISTINCT academic_degree) AS degree_types
   FROM public.employee_profiles;


--
-- Name: exhibition_events; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.exhibition_events (
    id integer NOT NULL,
    exhibition_id integer,
    event_type character varying(100),
    event_title text NOT NULL,
    event_date date,
    event_time time without time zone,
    speaker text,
    description text,
    attendees integer,
    created_at timestamp with time zone DEFAULT now()
);


--
-- Name: exhibition_events_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.exhibition_events_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: exhibition_events_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.exhibition_events_id_seq OWNED BY public.exhibition_events.id;


--
-- Name: exhibition_items; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.exhibition_items (
    id integer NOT NULL,
    exhibition_id integer,
    item_type character varying(100),
    item_name text,
    item_description text,
    catalog_number character varying(100),
    collection_source character varying(100),
    display_location text,
    display_order integer,
    notes text,
    created_at timestamp with time zone DEFAULT now()
);


--
-- Name: exhibition_items_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.exhibition_items_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: exhibition_items_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.exhibition_items_id_seq OWNED BY public.exhibition_items.id;


--
-- Name: exhibitions; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.exhibitions (
    id integer NOT NULL,
    title text NOT NULL,
    subtitle text,
    description text,
    exhibition_type character varying(100),
    location text,
    venue text,
    start_date date,
    end_date date,
    opening_date date,
    curator text,
    co_curators text[],
    organizer text,
    sponsors text[],
    status character varying(50) DEFAULT 'планирана'::character varying,
    visitor_count integer DEFAULT 0,
    catalog_published boolean DEFAULT false,
    catalog_path text,
    poster_path text,
    budget numeric(12,2),
    notes text,
    created_at timestamp with time zone DEFAULT now(),
    updated_at timestamp with time zone DEFAULT now(),
    progress integer DEFAULT 0,
    planning_phase character varying(50) DEFAULT 'conceptual'::character varying,
    checklist_data jsonb DEFAULT '{}'::jsonb,
    team_members jsonb DEFAULT '[]'::jsonb,
    created_by_email character varying(255),
    created_by_name character varying(255)
);


--
-- Name: TABLE exhibitions; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TABLE public.exhibitions IS 'Phase 3A: Exhibitions database - Migrated from exhibitions.json';


--
-- Name: COLUMN exhibitions.status; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.exhibitions.status IS 'Status: planning, preparation, active, completed, cancelled';


--
-- Name: COLUMN exhibitions.progress; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.exhibitions.progress IS 'Completion progress percentage (0-100)';


--
-- Name: COLUMN exhibitions.planning_phase; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.exhibitions.planning_phase IS 'Current planning phase: conceptual, design, technical, digital, team';


--
-- Name: COLUMN exhibitions.checklist_data; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.exhibitions.checklist_data IS 'JSON object storing checklist completion state';


--
-- Name: COLUMN exhibitions.team_members; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.exhibitions.team_members IS 'JSON array of team member assignments';


--
-- Name: COLUMN exhibitions.created_by_email; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.exhibitions.created_by_email IS 'Email of user who created the exhibition';


--
-- Name: COLUMN exhibitions.created_by_name; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.exhibitions.created_by_name IS 'Full name of user who created the exhibition';


--
-- Name: exhibition_statistics; Type: VIEW; Schema: public; Owner: -
--

CREATE VIEW public.exhibition_statistics AS
 SELECT count(*) AS total_exhibitions,
    count(*) FILTER (WHERE ((status)::text = 'активна'::text)) AS active_exhibitions,
    count(*) FILTER (WHERE ((status)::text = 'завршена'::text)) AS completed_exhibitions,
    count(*) FILTER (WHERE ((status)::text = 'планирана'::text)) AS planned_exhibitions,
    sum(visitor_count) AS total_visitors
   FROM public.exhibitions;


--
-- Name: exhibitions_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.exhibitions_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: exhibitions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.exhibitions_id_seq OWNED BY public.exhibitions.id;


--
-- Name: financial_plans; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.financial_plans (
    id integer NOT NULL,
    odeljenje character varying(100),
    odeljenje_text character varying(200),
    kustos character varying(200),
    datum_izrade date,
    plan_data jsonb,
    total_2026 numeric(15,2),
    total_2027 numeric(15,2),
    total_2028 numeric(15,2),
    grand_total numeric(15,2),
    user_email character varying(200),
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


--
-- Name: financial_plans_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.financial_plans_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: financial_plans_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.financial_plans_id_seq OWNED BY public.financial_plans.id;


--
-- Name: foto_poslovi; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.foto_poslovi (
    id integer NOT NULL,
    fotografija_id integer NOT NULL,
    tip text NOT NULL,
    status text DEFAULT 'ceka'::text NOT NULL,
    pokusaji integer DEFAULT 0 NOT NULL,
    sledeci_pokusaj_at timestamp with time zone,
    zakljucan_at timestamp with time zone,
    zakljucao text,
    poslednja_greska text,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL,
    CONSTRAINT foto_poslovi_status_check CHECK ((status = ANY (ARRAY['ceka'::text, 'radi'::text, 'uspeh'::text, 'greska'::text]))),
    CONSTRAINT foto_poslovi_tip_check CHECK ((tip = ANY (ARRAY['derivati'::text, 'fixity'::text])))
);


--
-- Name: TABLE foto_poslovi; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TABLE public.foto_poslovi IS 'DB-backed job queue; a stuck ''radi'' row older than the reclaim window is returned to ''ceka'' by the worker';


--
-- Name: foto_poslovi_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.foto_poslovi_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: foto_poslovi_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.foto_poslovi_id_seq OWNED BY public.foto_poslovi.id;


--
-- Name: foto_veza_izlozba; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.foto_veza_izlozba (
    id integer NOT NULL,
    fotografija_id integer NOT NULL,
    exhibition_id integer NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL
);


--
-- Name: foto_veza_izlozba_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.foto_veza_izlozba_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: foto_veza_izlozba_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.foto_veza_izlozba_id_seq OWNED BY public.foto_veza_izlozba.id;


--
-- Name: foto_veza_kr_dosije; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.foto_veza_kr_dosije (
    id integer NOT NULL,
    fotografija_id integer NOT NULL,
    dosije_id integer NOT NULL,
    faza text NOT NULL,
    redosled integer DEFAULT 0 NOT NULL,
    created_by_email character varying(255),
    created_at timestamp without time zone DEFAULT now() NOT NULL,
    CONSTRAINT foto_veza_kr_dosije_faza_check CHECK ((faza = ANY (ARRAY['pre'::text, 'tokom'::text, 'posle'::text])))
);


--
-- Name: TABLE foto_veza_kr_dosije; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TABLE public.foto_veza_kr_dosije IS 'Веза К-Р досијеа и фотографије из Фототеке; faza = pre/tokom/posle (сл. а/б/в)';


--
-- Name: foto_veza_kr_dosije_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.foto_veza_kr_dosije_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: foto_veza_kr_dosije_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.foto_veza_kr_dosije_id_seq OWNED BY public.foto_veza_kr_dosije.id;


--
-- Name: foto_veza_predmet; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.foto_veza_predmet (
    id integer NOT NULL,
    fotografija_id integer NOT NULL,
    database_name text NOT NULL,
    inventarni_broj text NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    mineral_id integer
);


--
-- Name: COLUMN foto_veza_predmet.mineral_id; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.foto_veza_predmet.mineral_id IS 'FK ka minerals za database_name=''mineral'' (ON UPDATE/DELETE CASCADE); NULL za druge zbirke i neuparene zapise';


--
-- Name: foto_veza_predmet_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.foto_veza_predmet_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: foto_veza_predmet_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.foto_veza_predmet_id_seq OWNED BY public.foto_veza_predmet.id;


--
-- Name: foto_veza_projekat; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.foto_veza_projekat (
    id integer NOT NULL,
    fotografija_id integer NOT NULL,
    projekat_id integer NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL
);


--
-- Name: foto_veza_projekat_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.foto_veza_projekat_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: foto_veza_projekat_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.foto_veza_projekat_id_seq OWNED BY public.foto_veza_projekat.id;


--
-- Name: foto_veza_teren; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.foto_veza_teren (
    id integer NOT NULL,
    fotografija_id integer NOT NULL,
    teren_id integer NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL
);


--
-- Name: foto_veza_teren_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.foto_veza_teren_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: foto_veza_teren_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.foto_veza_teren_id_seq OWNED BY public.foto_veza_teren.id;


--
-- Name: fotografija_tagovi; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.fotografija_tagovi (
    id integer NOT NULL,
    fotografija_id integer NOT NULL,
    tag text NOT NULL
);


--
-- Name: TABLE fotografija_tagovi; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TABLE public.fotografija_tagovi IS 'Free-form tags; no separate tag dictionary — autocomplete works off SELECT DISTINCT';


--
-- Name: fotografija_tagovi_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.fotografija_tagovi_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: fotografija_tagovi_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.fotografija_tagovi_id_seq OWNED BY public.fotografija_tagovi.id;


--
-- Name: fotografije; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.fotografije (
    id integer NOT NULL,
    sha256 character(64) NOT NULL,
    raw_putanja text NOT NULL,
    original_ime text NOT NULL,
    ekstenzija text,
    velicina_bajtova bigint,
    width integer,
    height integer,
    autor_email text NOT NULL,
    datum_snimanja date,
    exif jsonb,
    opis text,
    poreklo text NOT NULL,
    status text DEFAULT 'primljena'::text NOT NULL,
    u_prijemnom_redu boolean DEFAULT false NOT NULL,
    obrisana boolean DEFAULT false NOT NULL,
    fixity_proveren_at timestamp with time zone,
    fixity_ok boolean,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL,
    vidljivost text DEFAULT 'javno'::text NOT NULL,
    sklonjena_sa_reda boolean DEFAULT false NOT NULL,
    CONSTRAINT fotografije_poreklo_check CHECK ((poreklo = ANY (ARRAY['upload'::text, 'import'::text]))),
    CONSTRAINT fotografije_status_check CHECK ((status = ANY (ARRAY['primljena'::text, 'obrada'::text, 'spremna'::text, 'greska'::text, 'bez_derivata'::text]))),
    CONSTRAINT fotografije_vidljivost_check CHECK ((vidljivost = ANY (ARRAY['javno'::text, 'privatno'::text])))
);


--
-- Name: TABLE fotografije; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TABLE public.fotografije IS 'Photo registry; raw_putanja is relative to FOTOTEKA_ARHIVA_PATH and is written once at intake — later linking never moves the RAW file';


--
-- Name: COLUMN fotografije.u_prijemnom_redu; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.fotografije.u_prijemnom_redu IS 'LEGACY flag — no longer used to build the queue (it could lie); kept for history';


--
-- Name: COLUMN fotografije.sklonjena_sa_reda; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.fotografije.sklonjena_sa_reda IS 'Curator explicitly took this photo off the reception queue without linking it';


--
-- Name: fotografije_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.fotografije_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: fotografije_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.fotografije_id_seq OWNED BY public.fotografije.id;


--
-- Name: fototeka_intake_pending; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.fototeka_intake_pending (
    id bigint NOT NULL,
    sha256 text NOT NULL,
    raw_putanja text NOT NULL,
    original_ime text,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    claim_token text
);


--
-- Name: TABLE fototeka_intake_pending; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TABLE public.fototeka_intake_pending IS 'Namera intake-a RAW fajla pre postavljanja; red bez fotografije = siroče propalog commit-a';


--
-- Name: COLUMN fototeka_intake_pending.claim_token; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.fototeka_intake_pending.claim_token IS 'Vlasnik namere (uuid procesa unosa); čišćenje sme da obriše RAW samo uz poklapanje tokena';


--
-- Name: fototeka_intake_pending_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.fototeka_intake_pending_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: fototeka_intake_pending_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.fototeka_intake_pending_id_seq OWNED BY public.fototeka_intake_pending.id;


--
-- Name: fototeka_projekti; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.fototeka_projekti (
    id integer NOT NULL,
    naziv text NOT NULL,
    created_by_email text,
    created_at timestamp with time zone DEFAULT now() NOT NULL
);


--
-- Name: TABLE fototeka_projekti; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TABLE public.fototeka_projekti IS 'Lightweight project registry until a real project module exists in the DB';


--
-- Name: fototeka_projekti_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.fototeka_projekti_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: fototeka_projekti_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.fototeka_projekti_id_seq OWNED BY public.fototeka_projekti.id;


--
-- Name: fototeka_tereni; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.fototeka_tereni (
    id integer NOT NULL,
    godina smallint NOT NULL,
    naziv text NOT NULL,
    created_by_email text,
    created_at timestamp with time zone DEFAULT now() NOT NULL
);


--
-- Name: TABLE fototeka_tereni; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TABLE public.fototeka_tereni IS 'Field-trip registry mirroring the RAW layout teren/<godina>/<akcija>/';


--
-- Name: fototeka_tereni_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.fototeka_tereni_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: fototeka_tereni_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.fototeka_tereni_id_seq OWNED BY public.fototeka_tereni.id;


--
-- Name: fototeka_uvoz_run; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.fototeka_uvoz_run (
    id integer NOT NULL,
    pokrenut_at timestamp without time zone DEFAULT now() NOT NULL,
    zavrsen_at timestamp without time zone,
    izvor text NOT NULL,
    pokrenuo_email character varying(255),
    ukupno integer DEFAULT 0 NOT NULL,
    uvezeno integer DEFAULT 0 NOT NULL,
    duplikata integer DEFAULT 0 NOT NULL,
    neuspesno integer DEFAULT 0 NOT NULL,
    u_prijemni_red integer DEFAULT 0 NOT NULL,
    vezano_predmet integer DEFAULT 0 NOT NULL,
    vezano_teren integer DEFAULT 0 NOT NULL,
    bez_veze integer DEFAULT 0 NOT NULL,
    CONSTRAINT fototeka_uvoz_run_izvor_check CHECK ((izvor = ANY (ARRAY['ui'::text, 'timer'::text, 'cli'::text])))
);


--
-- Name: TABLE fototeka_uvoz_run; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TABLE public.fototeka_uvoz_run IS 'Batch import runs from the shared intake folder (Samba)';


--
-- Name: COLUMN fototeka_uvoz_run.vezano_predmet; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.fototeka_uvoz_run.vezano_predmet IS 'Photos linked to an existing specimen (the number was found in the collection)';


--
-- Name: COLUMN fototeka_uvoz_run.bez_veze; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.fototeka_uvoz_run.bez_veze IS 'Photos with no link — unrecognized name, or a number that does not exist';


--
-- Name: fototeka_uvoz_run_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.fototeka_uvoz_run_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: fototeka_uvoz_run_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.fototeka_uvoz_run_id_seq OWNED BY public.fototeka_uvoz_run.id;


--
-- Name: fototeka_uvoz_stavka; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.fototeka_uvoz_stavka (
    id integer NOT NULL,
    run_id integer NOT NULL,
    datoteka text NOT NULL,
    korisnicki_folder text,
    ishod text NOT NULL,
    klasa text,
    fotografija_id integer,
    poruka text,
    CONSTRAINT fototeka_uvoz_stavka_ishod_check CHECK ((ishod = ANY (ARRAY['uvezeno'::text, 'duplikat'::text, 'neuspesno'::text]))),
    CONSTRAINT fototeka_uvoz_stavka_klasa_check CHECK ((klasa = ANY (ARRAY['predmet'::text, 'teren'::text, 'prijemni_red'::text])))
);


--
-- Name: TABLE fototeka_uvoz_stavka; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TABLE public.fototeka_uvoz_stavka IS 'Per-file outcome of a batch import run';


--
-- Name: fototeka_uvoz_stavka_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.fototeka_uvoz_stavka_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: fototeka_uvoz_stavka_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.fototeka_uvoz_stavka_id_seq OWNED BY public.fototeka_uvoz_stavka.id;


--
-- Name: geo_field_data; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.geo_field_data (
    id integer NOT NULL,
    title character varying(255) NOT NULL,
    description text,
    latitude double precision NOT NULL,
    longitude double precision NOT NULL,
    category character varying(50) DEFAULT 'other'::character varying,
    rock_mineral_type character varying(255),
    geological_period character varying(255),
    formation_name character varying(255),
    field_notes text,
    created_by character varying(255) NOT NULL,
    created_at timestamp without time zone DEFAULT now(),
    updated_at timestamp without time zone DEFAULT now()
);


--
-- Name: geo_field_data_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.geo_field_data_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: geo_field_data_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.geo_field_data_id_seq OWNED BY public.geo_field_data.id;


--
-- Name: heritage_categories; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.heritage_categories (
    id integer NOT NULL,
    category_name character varying(100) NOT NULL,
    heritage_type character varying(100),
    description text
);


--
-- Name: heritage_categories_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.heritage_categories_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: heritage_categories_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.heritage_categories_id_seq OWNED BY public.heritage_categories.id;


--
-- Name: heritage_items; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.heritage_items (
    id integer NOT NULL,
    registry_number character varying(100),
    item_name text NOT NULL,
    alternative_names text[],
    heritage_type character varying(100),
    category character varying(100),
    subcategory character varying(100),
    significance_level character varying(100),
    description text,
    detailed_description text,
    dimensions_height numeric(10,2),
    dimensions_width numeric(10,2),
    dimensions_depth numeric(10,2),
    dimensions_diameter numeric(10,2),
    dimensions_unit character varying(10) DEFAULT 'cm'::character varying,
    weight numeric(10,2),
    weight_unit character varying(10) DEFAULT 'g'::character varying,
    material text,
    technique text,
    color text,
    date_of_origin text,
    century character varying(50),
    cultural_period text,
    creator text,
    creator_nationality text,
    provenance text,
    historical_context text,
    current_location text,
    storage_location text,
    display_status character varying(50),
    protection_status character varying(100),
    protection_level character varying(50),
    legal_basis text,
    inscription_date date,
    condition character varying(50),
    condition_notes text,
    conservation_history text,
    conservation_needs text,
    bibliography text,
    related_items text[],
    keywords text[],
    notes text,
    images jsonb,
    created_at timestamp with time zone DEFAULT now(),
    updated_at timestamp with time zone DEFAULT now()
);


--
-- Name: TABLE heritage_items; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TABLE public.heritage_items IS 'Phase 3A: Cultural heritage database - Migrated from CULTURAL_HERITAGE_DATABASE dict';


--
-- Name: heritage_items_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.heritage_items_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: heritage_items_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.heritage_items_id_seq OWNED BY public.heritage_items.id;


--
-- Name: heritage_statistics; Type: VIEW; Schema: public; Owner: -
--

CREATE VIEW public.heritage_statistics AS
 SELECT count(*) AS total_items,
    count(DISTINCT heritage_type) AS total_types,
    count(DISTINCT category) AS total_categories,
    count(*) FILTER (WHERE (protection_status IS NOT NULL)) AS protected_items
   FROM public.heritage_items;


--
-- Name: heritage_types; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.heritage_types (
    id integer NOT NULL,
    type_name character varying(100) NOT NULL,
    description text
);


--
-- Name: heritage_types_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.heritage_types_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: heritage_types_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.heritage_types_id_seq OWNED BY public.heritage_types.id;


--
-- Name: images; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.images (
    id integer NOT NULL,
    image_id character varying(255) NOT NULL,
    database_name character varying(100) NOT NULL,
    entity_type character varying(100) NOT NULL,
    entity_id character varying(255) NOT NULL,
    original_filename character varying(500),
    file_extension character varying(10) NOT NULL,
    file_path character varying(1000) NOT NULL,
    thumbnail_small character varying(1000),
    thumbnail_medium character varying(1000),
    thumbnail_large character varying(1000),
    description text DEFAULT ''::text,
    file_size bigint DEFAULT 0,
    file_hash character varying(64),
    width integer,
    height integer,
    custom_metadata jsonb DEFAULT '{}'::jsonb,
    backed_up boolean DEFAULT false,
    backup_date timestamp with time zone,
    created_at timestamp with time zone DEFAULT now(),
    updated_at timestamp with time zone DEFAULT now()
);


--
-- Name: images_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.images_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: images_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.images_id_seq OWNED BY public.images.id;


--
-- Name: inventory_entries; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.inventory_entries (
    id integer NOT NULL,
    inventory_number text,
    inventory_number_raw text,
    name text,
    locality text,
    quantity text,
    acquisition_info text,
    collector text,
    notes text,
    sheet text,
    row_number integer,
    category text,
    revisited boolean DEFAULT false,
    physical_location text,
    revision_date date,
    created_at timestamp with time zone DEFAULT now(),
    in_printed_book boolean DEFAULT false NOT NULL
);


--
-- Name: inventory_entries_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.inventory_entries_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: inventory_entries_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.inventory_entries_id_seq OWNED BY public.inventory_entries.id;


--
-- Name: kr_dosije; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.kr_dosije (
    id integer NOT NULL,
    evidencioni_broj text NOT NULL,
    odeljenje text NOT NULL,
    predmet_tip text DEFAULT 'zbirka'::text NOT NULL,
    database_name text,
    inventarni_broj text,
    kolektorski_broj text,
    naziv_predmeta text NOT NULL,
    narucilac text,
    opis_pre text,
    opis_postupak text,
    opis_posle text,
    period_od date,
    period_do date,
    period_tekst text,
    napomena text,
    izvor text DEFAULT 'rucno'::text NOT NULL,
    izvorni_evidencioni_broj text,
    created_by_email character varying(255),
    created_at timestamp without time zone DEFAULT now() NOT NULL,
    updated_at timestamp without time zone DEFAULT now() NOT NULL,
    CONSTRAINT kr_dosije_izvor_check CHECK ((izvor = ANY (ARRAY['rucno'::text, 'uvoz'::text]))),
    CONSTRAINT kr_dosije_odeljenje_check CHECK ((odeljenje = ANY (ARRAY['geo'::text, 'bio'::text]))),
    CONSTRAINT kr_dosije_predmet_tip_check CHECK ((predmet_tip = ANY (ARRAY['zbirka'::text, 'slobodan'::text])))
);


--
-- Name: TABLE kr_dosije; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TABLE public.kr_dosije IS 'Конзерваторско-рестаураторски досије — један ред по захвату на предмету';


--
-- Name: COLUMN kr_dosije.evidencioni_broj; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.kr_dosije.evidencioni_broj IS 'Аутоматски, по одељењу и години: КР-ГЕО-2026-001 / КР-БИО-2026-001';


--
-- Name: COLUMN kr_dosije.kolektorski_broj; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.kr_dosije.kolektorski_broj IS 'Колекторски број (Col.XXX) — слике из Фототеке се вежу по овом броју';


--
-- Name: kr_dosije_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.kr_dosije_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: kr_dosije_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.kr_dosije_id_seq OWNED BY public.kr_dosije.id;


--
-- Name: kr_dosije_izvrsilac; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.kr_dosije_izvrsilac (
    id integer NOT NULL,
    dosije_id integer NOT NULL,
    user_email character varying(255),
    ime_tekst text NOT NULL,
    redosled integer DEFAULT 0 NOT NULL,
    created_at timestamp without time zone DEFAULT now() NOT NULL
);


--
-- Name: TABLE kr_dosije_izvrsilac; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TABLE public.kr_dosije_izvrsilac IS 'Лица која су вршила радове на досијеу (веза на users кад постоји налог)';


--
-- Name: kr_dosije_izvrsilac_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.kr_dosije_izvrsilac_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: kr_dosije_izvrsilac_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.kr_dosije_izvrsilac_id_seq OWNED BY public.kr_dosije_izvrsilac.id;


--
-- Name: kr_predlozak; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.kr_predlozak (
    id integer NOT NULL,
    odeljenje text,
    vrsta text NOT NULL,
    naziv text NOT NULL,
    sadrzaj text NOT NULL,
    created_by_email character varying(255),
    created_at timestamp without time zone DEFAULT now() NOT NULL,
    updated_at timestamp without time zone DEFAULT now() NOT NULL,
    CONSTRAINT kr_predlozak_odeljenje_check CHECK (((odeljenje IS NULL) OR (odeljenje = ANY (ARRAY['geo'::text, 'bio'::text])))),
    CONSTRAINT kr_predlozak_vrsta_check CHECK ((vrsta = ANY (ARRAY['pre'::text, 'postupak'::text, 'posle'::text])))
);


--
-- Name: TABLE kr_predlozak; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TABLE public.kr_predlozak IS 'Предлошци описа/поступка за К-Р досије — бирају се па дорађују (CRUD за конзераторе)';


--
-- Name: COLUMN kr_predlozak.vrsta; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.kr_predlozak.vrsta IS 'Које поље описа попуњава: pre / postupak / posle';


--
-- Name: kr_predlozak_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.kr_predlozak_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: kr_predlozak_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.kr_predlozak_id_seq OWNED BY public.kr_predlozak.id;


--
-- Name: library_books; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.library_books (
    id integer NOT NULL,
    title text NOT NULL,
    author text,
    isbn character varying(20),
    publisher text,
    publication_year integer,
    category character varying(100),
    subcategory character varying(100),
    language character varying(50) DEFAULT 'српски'::character varying,
    pages integer,
    format character varying(50),
    location text,
    shelf_number character varying(50),
    status character varying(50) DEFAULT 'доступна'::character varying,
    acquisition_date date,
    acquisition_method character varying(100),
    price numeric(10,2),
    condition character varying(50),
    description text,
    notes text,
    keywords text[],
    created_at timestamp with time zone DEFAULT now(),
    updated_at timestamp with time zone DEFAULT now()
);


--
-- Name: TABLE library_books; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TABLE public.library_books IS 'Phase 3A: Library database - Migrated from library_database.json';


--
-- Name: library_books_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.library_books_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: library_books_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.library_books_id_seq OWNED BY public.library_books.id;


--
-- Name: library_categories; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.library_categories (
    id integer NOT NULL,
    name character varying(100) NOT NULL,
    description text,
    parent_category character varying(100),
    created_at timestamp with time zone DEFAULT now()
);


--
-- Name: library_categories_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.library_categories_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: library_categories_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.library_categories_id_seq OWNED BY public.library_categories.id;


--
-- Name: library_loans; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.library_loans (
    id integer NOT NULL,
    book_id integer,
    borrower_name text NOT NULL,
    borrower_email text,
    loan_date date DEFAULT CURRENT_DATE NOT NULL,
    due_date date NOT NULL,
    return_date date,
    status character varying(50) DEFAULT 'активна'::character varying,
    notes text,
    created_at timestamp with time zone DEFAULT now()
);


--
-- Name: library_loans_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.library_loans_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: library_loans_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.library_loans_id_seq OWNED BY public.library_loans.id;


--
-- Name: library_statistics; Type: VIEW; Schema: public; Owner: -
--

CREATE VIEW public.library_statistics AS
 SELECT count(*) AS total_books,
    count(*) FILTER (WHERE ((status)::text = 'доступна'::text)) AS available_books,
    count(*) FILTER (WHERE ((status)::text = 'позајмљена'::text)) AS borrowed_books,
    count(DISTINCT category) AS total_categories,
    count(DISTINCT author) AS total_authors
   FROM public.library_books;


--
-- Name: localities; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.localities (
    id integer NOT NULL,
    name text NOT NULL,
    country text,
    note text,
    source text DEFAULT 'rucno'::text NOT NULL,
    created_by_email character varying(255),
    created_at timestamp without time zone DEFAULT now() NOT NULL,
    updated_at timestamp without time zone DEFAULT now() NOT NULL,
    CONSTRAINT localities_source_check CHECK ((source = ANY (ARRAY['rucno'::text, 'seed'::text])))
);


--
-- Name: TABLE localities; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TABLE public.localities IS 'Standalone locality registry — independent of specimens (field sites, future finds)';


--
-- Name: COLUMN localities.source; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.localities.source IS 'rucno = added by a curator; seed = imported from the collection''s distinct values';


--
-- Name: localities_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.localities_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: localities_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.localities_id_seq OWNED BY public.localities.id;


--
-- Name: mail_cache_folders; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.mail_cache_folders (
    user_email public.citext NOT NULL,
    name text NOT NULL,
    uidvalidity bigint DEFAULT 0,
    highest_uid bigint DEFAULT 0,
    unseen integer DEFAULT 0,
    last_synced_at double precision DEFAULT 0,
    message_count integer DEFAULT 0
);


--
-- Name: mail_cache_messages; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.mail_cache_messages (
    user_email public.citext NOT NULL,
    folder text NOT NULL,
    uid bigint NOT NULL,
    from_name text DEFAULT ''::text,
    from_address text DEFAULT ''::text,
    reply_to_name text DEFAULT ''::text,
    reply_to_address text DEFAULT ''::text,
    subject text DEFAULT ''::text,
    date_iso text DEFAULT ''::text,
    is_read boolean DEFAULT false,
    has_body boolean DEFAULT false,
    text_body text DEFAULT ''::text,
    html_body text DEFAULT ''::text,
    to_json text DEFAULT '[]'::text,
    cc_json text DEFAULT '[]'::text,
    attachments_json text DEFAULT '[]'::text,
    links_json text DEFAULT '[]'::text,
    received_iso text DEFAULT ''::text,
    sort_date_iso text DEFAULT ''::text
);


--
-- Name: mail_cache_meta; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.mail_cache_meta (
    user_email public.citext NOT NULL,
    key text NOT NULL,
    value text
);


--
-- Name: mail_cache_pending_reads; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.mail_cache_pending_reads (
    user_email public.citext NOT NULL,
    folder text NOT NULL,
    uid bigint NOT NULL
);


--
-- Name: mail_user_settings; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.mail_user_settings (
    user_email public.citext NOT NULL,
    settings_json jsonb DEFAULT '{}'::jsonb NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL
);


--
-- Name: meteorite_specimens; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.meteorite_specimens (
    id integer NOT NULL,
    catalog_number character varying(100) NOT NULL,
    specimen_name text NOT NULL,
    alternative_names text[],
    meteorite_class character varying(100),
    meteorite_group character varying(100),
    meteorite_type character varying(100),
    classification_scheme text,
    mass numeric(10,3),
    mass_unit character varying(10) DEFAULT 'g'::character varying,
    dimensions text,
    shape text,
    color text,
    surface_features text,
    main_minerals text[],
    minor_minerals text[],
    chemical_composition text,
    metal_content numeric(5,2),
    silicate_content numeric(5,2),
    fall_date date,
    fall_location text,
    fall_country character varying(100),
    fall_coordinates public.geography(Point,4326),
    fall_witnessed boolean DEFAULT false,
    fall_description text,
    discovery_date date,
    discovery_location text,
    discoverer text,
    collection_date date,
    collector text,
    collection_method text,
    acquisition_date date,
    acquisition_method character varying(100),
    acquisition_source text,
    acquisition_value numeric(12,2),
    shock_stage character varying(50),
    weathering_grade character varying(50),
    texture text,
    petrographic_notes text,
    geochemical_data text,
    isotopic_data jsonb,
    age_estimation text,
    parent_body text,
    storage_location text,
    storage_conditions text,
    condition character varying(50),
    condition_notes text,
    description text,
    scientific_significance text,
    publications text[],
    bibliography_references text,
    keywords text[],
    notes text,
    images jsonb,
    status character varying(50) DEFAULT 'у збирци'::character varying,
    display_status character varying(50),
    created_at timestamp with time zone DEFAULT now(),
    updated_at timestamp with time zone DEFAULT now(),
    fall_type text,
    total_mass numeric(10,3),
    total_mass_unit character varying(10) DEFAULT 'kg'::character varying,
    quantity integer DEFAULT 1,
    meteorite_bulletin_number character varying(50),
    mineralogy text,
    cosmic_ray_exposure text,
    widmanstatten_pattern text,
    fusion_crust text,
    serbian_meteorite boolean DEFAULT false,
    fall_date_text text,
    acquisition_date_text text
);


--
-- Name: TABLE meteorite_specimens; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TABLE public.meteorite_specimens IS 'Phase 3A: Meteorite collection - Migrated from METEORITE_COLLECTION_DATABASE dict';


--
-- Name: COLUMN meteorite_specimens.fall_type; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.meteorite_specimens.fall_type IS 'Serbian: Тип пада (Пад посматран, Налаз, итд.)';


--
-- Name: COLUMN meteorite_specimens.total_mass; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.meteorite_specimens.total_mass IS 'Total mass of all specimens found (not just this one)';


--
-- Name: COLUMN meteorite_specimens.quantity; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.meteorite_specimens.quantity IS 'Number of specimens in collection';


--
-- Name: COLUMN meteorite_specimens.meteorite_bulletin_number; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.meteorite_specimens.meteorite_bulletin_number IS 'Meteoritical Bulletin catalog number';


--
-- Name: COLUMN meteorite_specimens.serbian_meteorite; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.meteorite_specimens.serbian_meteorite IS 'Serbian: Српски метеорит';


--
-- Name: COLUMN meteorite_specimens.fall_date_text; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.meteorite_specimens.fall_date_text IS 'Fall date in original Serbian format (e.g. 13. октобар 1877.)';


--
-- Name: COLUMN meteorite_specimens.acquisition_date_text; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.meteorite_specimens.acquisition_date_text IS 'Acquisition date in original format';


--
-- Name: meteorite_specimens_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.meteorite_specimens_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: meteorite_specimens_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.meteorite_specimens_id_seq OWNED BY public.meteorite_specimens.id;


--
-- Name: meteorite_statistics; Type: VIEW; Schema: public; Owner: -
--

CREATE VIEW public.meteorite_statistics AS
 SELECT count(*) AS total_specimens,
    count(DISTINCT meteorite_class) AS total_classes,
    sum(mass) AS total_mass_grams,
    count(*) FILTER (WHERE (fall_witnessed = true)) AS witnessed_falls,
    count(*) FILTER (WHERE (fall_witnessed = false)) AS finds
   FROM public.meteorite_specimens;


--
-- Name: mineral_references; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.mineral_references (
    id integer NOT NULL,
    mineral_name text NOT NULL,
    mineral_name_alt text,
    mineral_species text,
    chemical_formula text,
    crystal_system text,
    hardness text,
    specific_gravity text,
    color text,
    streak text,
    luster text,
    transparency text,
    fracture text,
    cleavage text,
    occurrence text,
    locality text,
    created_at timestamp with time zone DEFAULT now(),
    updated_at timestamp with time zone DEFAULT now()
);


--
-- Name: mineral_references_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.mineral_references_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: mineral_references_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.mineral_references_id_seq OWNED BY public.mineral_references.id;


--
-- Name: mineral_rruff_matches; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.mineral_rruff_matches (
    id integer NOT NULL,
    mineral_id integer NOT NULL,
    rruff_id character varying(20) NOT NULL,
    match_confidence double precision DEFAULT 1.0,
    matched_by character varying(50),
    matched_at timestamp with time zone DEFAULT now()
);


--
-- Name: mineral_rruff_matches_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.mineral_rruff_matches_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: mineral_rruff_matches_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.mineral_rruff_matches_id_seq OWNED BY public.mineral_rruff_matches.id;


--
-- Name: minerals; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.minerals (
    id integer NOT NULL,
    inventory_number character varying(50),
    item_name text,
    acquisition_method text,
    acquisition_date date,
    input_date timestamp with time zone,
    input_by text,
    donor text,
    identifier text,
    comments text,
    description text,
    storage_location text,
    card_locality text,
    bibliography_flag boolean,
    quantity integer,
    created_at timestamp with time zone DEFAULT now(),
    updated_at timestamp with time zone DEFAULT now(),
    physical_presence_confirmed boolean DEFAULT true NOT NULL,
    source text
);


--
-- Name: minerals_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.minerals_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: minerals_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.minerals_id_seq OWNED BY public.minerals.id;


--
-- Name: news_articles; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.news_articles (
    id integer NOT NULL,
    original_id integer,
    title text NOT NULL,
    title_en text,
    type text,
    status text,
    category text,
    start_date date,
    end_date date,
    location text,
    curator text,
    co_curator text,
    specimens_count integer DEFAULT 0,
    species_count integer DEFAULT 0,
    boxes_count integer DEFAULT 0,
    illustrations_count integer DEFAULT 0,
    visitor_count integer DEFAULT 0,
    description text,
    description_en text,
    target_audience text,
    educational_programs text,
    guided_tours text,
    catalog_available text,
    keywords text,
    source_link text,
    created_at timestamp with time zone DEFAULT now(),
    updated_at timestamp with time zone DEFAULT now()
);


--
-- Name: TABLE news_articles; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TABLE public.news_articles IS 'Phase 3B: News and exhibition articles - Migrated from news.json';


--
-- Name: news_articles_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.news_articles_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: news_articles_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.news_articles_id_seq OWNED BY public.news_articles.id;


--
-- Name: paper_feature_links; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.paper_feature_links (
    id bigint NOT NULL,
    paper_id bigint NOT NULL,
    feature_type text NOT NULL,
    feature_name text NOT NULL,
    feature_id text,
    link_type text DEFAULT 'search'::text,
    relevance_rank integer DEFAULT 0,
    search_query text
);


--
-- Name: paper_feature_links_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.paper_feature_links_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: paper_feature_links_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.paper_feature_links_id_seq OWNED BY public.paper_feature_links.id;


--
-- Name: paper_locality_links; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.paper_locality_links (
    id bigint NOT NULL,
    paper_id bigint NOT NULL,
    locality_name text NOT NULL,
    ogk_code text,
    link_type text DEFAULT 'search'::text,
    relevance_rank integer DEFAULT 0,
    search_query text
);


--
-- Name: paper_locality_links_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.paper_locality_links_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: paper_locality_links_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.paper_locality_links_id_seq OWNED BY public.paper_locality_links.id;


--
-- Name: procurement_requests; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.procurement_requests (
    id integer NOT NULL,
    datum date NOT NULL,
    podnosilac character varying(255) NOT NULL,
    items jsonb NOT NULL,
    total_estimated numeric(12,2) DEFAULT 0,
    total_realized numeric(12,2) DEFAULT 0,
    teret_aktivnosti character varying(100),
    teret_aktivnosti_opis text,
    saglasan_rukovodilac character varying(255),
    sef_racunovodstva character varying(255),
    direktor character varying(255),
    status character varying(50) DEFAULT 'pending'::character varying,
    user_email character varying(255),
    created_at timestamp without time zone DEFAULT now(),
    updated_at timestamp without time zone DEFAULT now(),
    archive_request_id integer
);


--
-- Name: procurement_requests_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.procurement_requests_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: procurement_requests_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.procurement_requests_id_seq OWNED BY public.procurement_requests.id;


--
-- Name: project_space_planner_state; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.project_space_planner_state (
    id smallint DEFAULT 1 NOT NULL,
    state jsonb NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_by text,
    CONSTRAINT project_space_planner_state_id_check CHECK ((id = 1))
);


--
-- Name: TABLE project_space_planner_state; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TABLE public.project_space_planner_state IS 'Singleton stanje planera prostora (ranije data/project_space_planner.json)';


--
-- Name: request_comments; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.request_comments (
    id integer NOT NULL,
    request_id integer,
    author_email character varying(255) NOT NULL,
    author_name character varying(255),
    comment text NOT NULL,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


--
-- Name: TABLE request_comments; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TABLE public.request_comments IS 'Discussion comments on requests';


--
-- Name: request_comments_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.request_comments_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: request_comments_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.request_comments_id_seq OWNED BY public.request_comments.id;


--
-- Name: request_history; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.request_history (
    id integer NOT NULL,
    request_id integer,
    action character varying(100) NOT NULL,
    action_by_email character varying(255) NOT NULL,
    action_by_name character varying(255),
    old_values jsonb,
    new_values jsonb,
    notes text,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


--
-- Name: TABLE request_history; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TABLE public.request_history IS 'Audit trail for all request changes';


--
-- Name: request_history_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.request_history_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: request_history_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.request_history_id_seq OWNED BY public.request_history.id;


--
-- Name: research_projects; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.research_projects (
    id integer NOT NULL,
    title text NOT NULL,
    project_code text,
    principal_investigator text,
    department text,
    research_area text,
    start_date date,
    end_date date,
    funding_source text,
    budget text,
    status text,
    description text,
    publications text,
    collaborators text,
    keywords text,
    created_at timestamp with time zone DEFAULT now() NOT NULL
);


--
-- Name: research_projects_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.research_projects_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: research_projects_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.research_projects_id_seq OWNED BY public.research_projects.id;


--
-- Name: roles; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.roles (
    id integer NOT NULL,
    name text NOT NULL,
    description text,
    CONSTRAINT roles_name_check CHECK ((name = ANY (ARRAY['admin'::text, 'employee'::text, 'curator'::text, 'viewer'::text, 'direktor'::text, 'sef_odeljenja'::text, 'sef_racunovodstva'::text, 'sef_pravne_sluzbe'::text])))
);


--
-- Name: roles_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.roles_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: roles_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.roles_id_seq OWNED BY public.roles.id;


--
-- Name: rruff_chemistry; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.rruff_chemistry (
    id integer NOT NULL,
    rruff_id character varying(20) NOT NULL,
    oxide character varying(20) NOT NULL,
    weight_percent double precision
);


--
-- Name: rruff_chemistry_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.rruff_chemistry_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: rruff_chemistry_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.rruff_chemistry_id_seq OWNED BY public.rruff_chemistry.id;


--
-- Name: rruff_localities; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.rruff_localities (
    id integer NOT NULL,
    rruff_id character varying(20) NOT NULL,
    locality text,
    country character varying(100),
    latitude double precision,
    longitude double precision
);


--
-- Name: rruff_localities_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.rruff_localities_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: rruff_localities_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.rruff_localities_id_seq OWNED BY public.rruff_localities.id;


--
-- Name: rruff_minerals; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.rruff_minerals (
    id integer NOT NULL,
    rruff_id character varying(20) NOT NULL,
    name text NOT NULL,
    name_plain text,
    formula_rruff text,
    formula_ima text,
    formula_concise text,
    formula_html text,
    ideal_chemistry text,
    chemistry_elements text,
    valence_elements text,
    ima_number text,
    ima_status text,
    ima_mineral character varying(1),
    ima_mineral_symbol character varying(20),
    year_first_published integer,
    structural_groupname text,
    fleischers_groupname text,
    fleischers_glossary character varying(1),
    crystal_system text,
    crystal_systems text,
    space_group text,
    space_groups text,
    country_type_locality text,
    crystal_morphology text,
    oldest_known_age_ma double precision,
    paragenetic_modes text,
    status_notes text,
    rruff_ids text,
    database_id integer,
    created_at timestamp with time zone DEFAULT now()
);


--
-- Name: rruff_minerals_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.rruff_minerals_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: rruff_minerals_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.rruff_minerals_id_seq OWNED BY public.rruff_minerals.id;


--
-- Name: rruff_references; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.rruff_references (
    id integer NOT NULL,
    rruff_id character varying(20) NOT NULL,
    reference_text text,
    authors text,
    title text,
    journal character varying(200),
    year integer,
    doi character varying(100)
);


--
-- Name: rruff_references_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.rruff_references_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: rruff_references_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.rruff_references_id_seq OWNED BY public.rruff_references.id;


--
-- Name: sanja_paleogene_neogene_mammals; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.sanja_paleogene_neogene_mammals (
    id integer NOT NULL,
    source_row integer,
    specimen jsonb NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL
);


--
-- Name: schema_migrations; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.schema_migrations (
    filename text NOT NULL,
    applied_at timestamp with time zone DEFAULT now() NOT NULL
);


--
-- Name: science_news; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.science_news (
    id text NOT NULL,
    datum text DEFAULT ''::text NOT NULL,
    auto_fetched boolean DEFAULT false NOT NULL,
    item jsonb NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL
);


--
-- Name: TABLE science_news; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TABLE public.science_news IS 'Kurirane naučne vesti (ručne + RSS); item nosi ceo JSON zapis, datum/auto_fetched su radi sortiranja i orezivanja';


--
-- Name: scientific_papers; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.scientific_papers (
    id bigint NOT NULL,
    openalex_id text,
    doi text,
    title text NOT NULL,
    abstract text,
    publication_year integer,
    cited_by_count integer DEFAULT 0,
    journal_name text,
    volume text,
    issue text,
    authors_json text,
    keywords_json text,
    concepts_json text,
    is_open_access boolean DEFAULT false,
    oa_url text,
    pdf_url text,
    language text,
    source_api text DEFAULT 'openalex'::text,
    search_query text,
    fetch_date text,
    created_at timestamp with time zone DEFAULT now()
);


--
-- Name: scientific_papers_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.scientific_papers_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: scientific_papers_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.scientific_papers_id_seq OWNED BY public.scientific_papers.id;


--
-- Name: signature_audit_log; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.signature_audit_log (
    id integer NOT NULL,
    document_signature_id integer,
    action character varying(100) NOT NULL,
    action_by_email character varying(255) NOT NULL,
    action_by_name character varying(255),
    action_details jsonb DEFAULT '{}'::jsonb,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


--
-- Name: TABLE signature_audit_log; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TABLE public.signature_audit_log IS 'Audit trail for all signature-related actions';


--
-- Name: signature_audit_log_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.signature_audit_log_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: signature_audit_log_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.signature_audit_log_id_seq OWNED BY public.signature_audit_log.id;


--
-- Name: signature_templates; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.signature_templates (
    id integer NOT NULL,
    document_type character varying(100) NOT NULL,
    document_type_label character varying(255) NOT NULL,
    requires_requester_signature boolean DEFAULT true,
    requires_legal_verification boolean DEFAULT true,
    requires_approver_signature boolean DEFAULT false,
    approver_roles jsonb DEFAULT '[]'::jsonb,
    template_path character varying(500),
    instructions text,
    is_active boolean DEFAULT true,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


--
-- Name: TABLE signature_templates; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TABLE public.signature_templates IS 'Configuration for different document types requiring signatures';


--
-- Name: signature_templates_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.signature_templates_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: signature_templates_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.signature_templates_id_seq OWNED BY public.signature_templates.id;


--
-- Name: staging_bird_ringing; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.staging_bird_ringing (
    ring_number text,
    species_name text,
    age text,
    sex text,
    location text,
    coordinates_wkt text,
    coordinate_accuracy text,
    event_date text,
    event_time text,
    status text,
    ringer text,
    notes text,
    raw_json jsonb
);


--
-- Name: staging_inventory; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.staging_inventory (
    inventory_number text,
    inventory_number_raw text,
    name text,
    locality text,
    quantity text,
    acquisition_info text,
    collector text,
    notes text,
    sheet text,
    row_number text,
    category text,
    revisited text,
    physical_location text,
    revision_date text
);


--
-- Name: staging_minerals; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.staging_minerals (
    inventory_number text,
    item_name text,
    acquisition_method text,
    acquisition_date text,
    input_date text,
    input_by text,
    donor text,
    identifier text,
    comments text,
    description text,
    storage_location text,
    card_locality text,
    bibliography_flag text,
    quantity text
);


--
-- Name: staging_timesheet_days; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.staging_timesheet_days (
    radna_lista_id integer,
    dan integer,
    rad_na_mestu numeric,
    van_muzeja numeric,
    godisnji_odmor numeric,
    drzavni_praznik numeric,
    placeno_odsustvo numeric,
    ostalo_odsustvo numeric,
    bolovanje_manje_30 numeric,
    bolovanje_vece_30 numeric
);


--
-- Name: staging_timesheet_reports; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.staging_timesheet_reports (
    radna_lista_id integer,
    ime_prezime text,
    mesec integer,
    godina integer,
    organizaciona_jedinica text,
    radno_mesto text,
    poseban_obim_posla text,
    vanredni_poslovi text,
    potpis_zaposlenog text,
    nalogodavac text,
    potpis_sefa text,
    potpis_direktora text,
    povecanje_umanjenje_zarade text,
    o_posao text,
    created_at text
);


--
-- Name: timesheet_audit_log; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.timesheet_audit_log (
    id integer NOT NULL,
    report_id integer,
    action character varying(20) NOT NULL,
    changed_by character varying(255),
    changed_at timestamp with time zone DEFAULT now(),
    old_values jsonb,
    new_values jsonb,
    change_summary text,
    ip_address character varying(45),
    user_agent text,
    CONSTRAINT timesheet_audit_log_action_check CHECK (((action)::text = ANY (ARRAY[('INSERT'::character varying)::text, ('UPDATE'::character varying)::text, ('DELETE'::character varying)::text, ('VERIFY'::character varying)::text, ('LOCK'::character varying)::text, ('UNLOCK'::character varying)::text])))
);


--
-- Name: TABLE timesheet_audit_log; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TABLE public.timesheet_audit_log IS 'Audit trail for all timesheet changes';


--
-- Name: COLUMN timesheet_audit_log.action; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.timesheet_audit_log.action IS 'Type of action: INSERT, UPDATE, DELETE, VERIFY, LOCK, UNLOCK';


--
-- Name: COLUMN timesheet_audit_log.old_values; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.timesheet_audit_log.old_values IS 'Previous state as JSON (for UPDATE/DELETE)';


--
-- Name: COLUMN timesheet_audit_log.new_values; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.timesheet_audit_log.new_values IS 'New state as JSON (for INSERT/UPDATE)';


--
-- Name: timesheet_audit_log_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.timesheet_audit_log_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: timesheet_audit_log_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.timesheet_audit_log_id_seq OWNED BY public.timesheet_audit_log.id;


--
-- Name: timesheet_reports; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.timesheet_reports (
    id integer NOT NULL,
    legacy_radna_lista_id integer,
    employee_name text NOT NULL,
    month integer NOT NULL,
    year integer NOT NULL,
    organization_unit text,
    "position" text,
    special_scope text,
    extraordinary_tasks text,
    employee_signature text,
    approver text,
    manager_signature text,
    director_signature text,
    salary_adjustment text,
    duties_summary text,
    created_at timestamp with time zone DEFAULT now(),
    is_verified boolean DEFAULT false,
    verified_by character varying(255),
    verified_at timestamp without time zone,
    is_locked boolean DEFAULT false,
    supervisor_signature character varying(255),
    employee_email character varying(255) NOT NULL,
    updated_at timestamp with time zone DEFAULT now(),
    special_tasks text,
    version integer DEFAULT 1,
    status character varying(20) DEFAULT 'DRAFT'::character varying,
    submitted_at timestamp with time zone,
    reviewed_at timestamp with time zone,
    reviewed_by_email character varying(255),
    rejection_note text,
    verified_role character varying(64),
    editable_until timestamp with time zone,
    head_verified_by character varying(255),
    head_verified_at timestamp with time zone,
    director_verified_by character varying(255),
    director_verified_at timestamp with time zone,
    admin_approved_by character varying(255),
    admin_approved_at timestamp with time zone,
    imported_from character varying(20),
    imported_at timestamp with time zone,
    CONSTRAINT timesheet_reports_imported_from_check CHECK (((imported_from IS NULL) OR ((imported_from)::text = ANY ((ARRAY['word-tekuca'::character varying, 'word-arhiva'::character varying])::text[])))),
    CONSTRAINT timesheet_reports_month_check CHECK (((month >= 1) AND (month <= 12))),
    CONSTRAINT timesheet_reports_status_check CHECK (((status)::text = ANY ((ARRAY['DRAFT'::character varying, 'SUBMITTED'::character varying, 'APPROVED'::character varying, 'REJECTED'::character varying, 'ARHIVA'::character varying])::text[])))
);


--
-- Name: TABLE timesheet_reports; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TABLE public.timesheet_reports IS 'Employee monthly work reports (Radna Lista)';


--
-- Name: COLUMN timesheet_reports.is_verified; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.timesheet_reports.is_verified IS 'Whether the report has been verified/approved by admin';


--
-- Name: COLUMN timesheet_reports.verified_by; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.timesheet_reports.verified_by IS 'Email of admin who verified the report';


--
-- Name: COLUMN timesheet_reports.verified_at; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.timesheet_reports.verified_at IS 'Timestamp when report was verified';


--
-- Name: COLUMN timesheet_reports.is_locked; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.timesheet_reports.is_locked IS 'Whether the report is locked for editing';


--
-- Name: COLUMN timesheet_reports.employee_email; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.timesheet_reports.employee_email IS 'Обавезан канонски идентитет запосленог (NOT NULL од миграције 036). Идентификација листе иде ИСКЉУЧИВО по email-у; поклапање по имену је укинуто јер више не постоји ред са NULL email-ом.';


--
-- Name: COLUMN timesheet_reports.updated_at; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.timesheet_reports.updated_at IS 'Last modification timestamp';


--
-- Name: COLUMN timesheet_reports.special_tasks; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.timesheet_reports.special_tasks IS 'Special tasks description (alias for extraordinary_tasks)';


--
-- Name: COLUMN timesheet_reports.version; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.timesheet_reports.version IS 'Optimistic locking version - increments on each update';


--
-- Name: COLUMN timesheet_reports.head_verified_by; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.timesheet_reports.head_verified_by IS 'Email шефа одељења који је потврдио листу (први потпис); NULL = још није';


--
-- Name: COLUMN timesheet_reports.director_verified_by; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.timesheet_reports.director_verified_by IS 'Email директора који је потврдио листу (други потпис); NULL = још није';


--
-- Name: COLUMN timesheet_reports.admin_approved_by; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.timesheet_reports.admin_approved_by IS 'Email администратора/директора који је листу одобрио АДМИНИСТРАТИВНО (ван редовног двостепеног ланца); NULL = редовно одобрење или није одобрено';


--
-- Name: COLUMN timesheet_reports.admin_approved_at; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.timesheet_reports.admin_approved_at IS 'Тренутак административног одобрења; NULL ако листа није административно одобрена';


--
-- Name: COLUMN timesheet_reports.imported_from; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.timesheet_reports.imported_from IS 'Порекло увоза: word-tekuca (у ланац одобравања) или word-arhiva (одобрена архива); NULL = ручни унос';


--
-- Name: timesheet_audit_summary; Type: VIEW; Schema: public; Owner: -
--

CREATE VIEW public.timesheet_audit_summary AS
 SELECT tal.id,
    tal.report_id,
    tal.action,
    tal.changed_by,
    tal.changed_at,
    tal.change_summary,
    tr.employee_name,
    tr.month,
    tr.year
   FROM (public.timesheet_audit_log tal
     LEFT JOIN public.timesheet_reports tr ON ((tr.id = tal.report_id)))
  ORDER BY tal.changed_at DESC;


--
-- Name: VIEW timesheet_audit_summary; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON VIEW public.timesheet_audit_summary IS 'Human-readable audit log with employee details';


--
-- Name: timesheet_entries; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.timesheet_entries (
    id integer NOT NULL,
    report_id integer NOT NULL,
    category text NOT NULL,
    hours numeric(6,2) DEFAULT 0 NOT NULL,
    created_at timestamp with time zone DEFAULT now(),
    CONSTRAINT timesheet_entries_category_check CHECK ((category = ANY (ARRAY['rad_na_mestu'::text, 'van_muzeja'::text, 'godisnji_odmor'::text, 'drzavni_praznik'::text, 'placeno_odsustvo'::text, 'ostalo_odsustvo'::text, 'bolovanje_manje_30'::text, 'bolovanje_vece_30'::text])))
);


--
-- Name: TABLE timesheet_entries; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TABLE public.timesheet_entries IS 'Aggregated hours by category for efficient querying';


--
-- Name: timesheet_category_totals; Type: VIEW; Schema: public; Owner: -
--

CREATE VIEW public.timesheet_category_totals AS
 SELECT category,
    count(DISTINCT report_id) AS report_count,
    sum(hours) AS total_hours,
    avg(hours) AS avg_hours_per_report,
    min(hours) AS min_hours,
    max(hours) AS max_hours
   FROM public.timesheet_entries
  GROUP BY category
  ORDER BY (sum(hours)) DESC;


--
-- Name: VIEW timesheet_category_totals; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON VIEW public.timesheet_category_totals IS 'Overall statistics by work category';


--
-- Name: timesheet_edit_requests; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.timesheet_edit_requests (
    id integer NOT NULL,
    report_id integer NOT NULL,
    requester_email character varying(255) NOT NULL,
    reason text NOT NULL,
    status character varying(20) DEFAULT 'pending'::character varying,
    requested_at timestamp without time zone DEFAULT now(),
    processed_at timestamp without time zone,
    processed_by character varying(255),
    notes text,
    CONSTRAINT valid_status CHECK (((status)::text = ANY (ARRAY[('pending'::character varying)::text, ('approved'::character varying)::text, ('rejected'::character varying)::text])))
);


--
-- Name: TABLE timesheet_edit_requests; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TABLE public.timesheet_edit_requests IS 'Tracks edit requests for locked/verified timesheets';


--
-- Name: COLUMN timesheet_edit_requests.status; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.timesheet_edit_requests.status IS 'Request status: pending, approved, or rejected';


--
-- Name: timesheet_edit_requests_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.timesheet_edit_requests_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: timesheet_edit_requests_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.timesheet_edit_requests_id_seq OWNED BY public.timesheet_edit_requests.id;


--
-- Name: timesheet_employee_summary; Type: VIEW; Schema: public; Owner: -
--

CREATE VIEW public.timesheet_employee_summary AS
 SELECT tr.employee_name,
    tr.year,
    tr.month,
    tr.organization_unit,
    tr."position",
    sum(
        CASE
            WHEN (te.category = 'rad_na_mestu'::text) THEN te.hours
            ELSE (0)::numeric
        END) AS work_in_museum,
    sum(
        CASE
            WHEN (te.category = 'van_muzeja'::text) THEN te.hours
            ELSE (0)::numeric
        END) AS work_outside,
    sum(
        CASE
            WHEN (te.category = 'godisnji_odmor'::text) THEN te.hours
            ELSE (0)::numeric
        END) AS vacation,
    sum(
        CASE
            WHEN (te.category = 'drzavni_praznik'::text) THEN te.hours
            ELSE (0)::numeric
        END) AS public_holiday,
    sum(
        CASE
            WHEN (te.category = 'placeno_odsustvo'::text) THEN te.hours
            ELSE (0)::numeric
        END) AS paid_leave,
    sum(
        CASE
            WHEN (te.category = 'ostalo_odsustvo'::text) THEN te.hours
            ELSE (0)::numeric
        END) AS other_leave,
    sum(
        CASE
            WHEN (te.category = 'bolovanje_manje_30'::text) THEN te.hours
            ELSE (0)::numeric
        END) AS sick_lt30,
    sum(
        CASE
            WHEN (te.category = 'bolovanje_vece_30'::text) THEN te.hours
            ELSE (0)::numeric
        END) AS sick_gte30,
    sum(te.hours) AS total_hours
   FROM (public.timesheet_reports tr
     LEFT JOIN public.timesheet_entries te ON ((te.report_id = tr.id)))
  GROUP BY tr.employee_name, tr.year, tr.month, tr.organization_unit, tr."position"
  ORDER BY tr.year DESC, tr.month DESC, tr.employee_name;


--
-- Name: VIEW timesheet_employee_summary; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON VIEW public.timesheet_employee_summary IS 'Employee-level monthly summaries';


--
-- Name: timesheet_entries_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.timesheet_entries_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: timesheet_entries_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.timesheet_entries_id_seq OWNED BY public.timesheet_entries.id;


--
-- Name: timesheet_monthly_summary; Type: VIEW; Schema: public; Owner: -
--

CREATE VIEW public.timesheet_monthly_summary AS
 SELECT tr.year,
    tr.month,
    count(DISTINCT tr.id) AS report_count,
    count(DISTINCT tr.employee_name) AS employee_count,
    sum(
        CASE
            WHEN (te.category = 'rad_na_mestu'::text) THEN te.hours
            ELSE (0)::numeric
        END) AS total_work_in_museum,
    sum(
        CASE
            WHEN (te.category = 'van_muzeja'::text) THEN te.hours
            ELSE (0)::numeric
        END) AS total_work_outside,
    sum(
        CASE
            WHEN (te.category = 'godisnji_odmor'::text) THEN te.hours
            ELSE (0)::numeric
        END) AS total_vacation,
    sum(
        CASE
            WHEN (te.category = 'drzavni_praznik'::text) THEN te.hours
            ELSE (0)::numeric
        END) AS total_public_holiday,
    sum(
        CASE
            WHEN (te.category = 'placeno_odsustvo'::text) THEN te.hours
            ELSE (0)::numeric
        END) AS total_paid_leave,
    sum(
        CASE
            WHEN (te.category = 'ostalo_odsustvo'::text) THEN te.hours
            ELSE (0)::numeric
        END) AS total_other_leave,
    sum(
        CASE
            WHEN (te.category = 'bolovanje_manje_30'::text) THEN te.hours
            ELSE (0)::numeric
        END) AS total_sick_lt30,
    sum(
        CASE
            WHEN (te.category = 'bolovanje_vece_30'::text) THEN te.hours
            ELSE (0)::numeric
        END) AS total_sick_gte30,
    sum(te.hours) AS total_hours
   FROM (public.timesheet_reports tr
     LEFT JOIN public.timesheet_entries te ON ((te.report_id = tr.id)))
  GROUP BY tr.year, tr.month
  ORDER BY tr.year DESC, tr.month DESC;


--
-- Name: VIEW timesheet_monthly_summary; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON VIEW public.timesheet_monthly_summary IS 'Monthly aggregated statistics across all employees';


--
-- Name: timesheet_report_days; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.timesheet_report_days (
    id integer NOT NULL,
    report_id integer NOT NULL,
    day integer NOT NULL,
    work_in_museum numeric(4,2) DEFAULT 0,
    work_outside numeric(4,2) DEFAULT 0,
    vacation numeric(4,2) DEFAULT 0,
    public_holiday numeric(4,2) DEFAULT 0,
    paid_leave numeric(4,2) DEFAULT 0,
    other_leave numeric(4,2) DEFAULT 0,
    sick_leave_lt30 numeric(4,2) DEFAULT 0,
    sick_leave_gte30 numeric(4,2) DEFAULT 0,
    CONSTRAINT timesheet_report_days_day_check CHECK (((day >= 1) AND (day <= 31)))
);


--
-- Name: TABLE timesheet_report_days; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TABLE public.timesheet_report_days IS 'Daily breakdown of hours by category for each report';


--
-- Name: timesheet_report_days_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.timesheet_report_days_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: timesheet_report_days_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.timesheet_report_days_id_seq OWNED BY public.timesheet_report_days.id;


--
-- Name: timesheet_reports_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.timesheet_reports_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: timesheet_reports_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.timesheet_reports_id_seq OWNED BY public.timesheet_reports.id;


--
-- Name: timesheet_status_history; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.timesheet_status_history (
    id integer NOT NULL,
    report_id integer,
    old_status character varying(20),
    new_status character varying(20) NOT NULL,
    changed_by character varying(255) NOT NULL,
    changed_at timestamp with time zone DEFAULT now(),
    note text
);


--
-- Name: timesheet_status_history_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.timesheet_status_history_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: timesheet_status_history_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.timesheet_status_history_id_seq OWNED BY public.timesheet_status_history.id;


--
-- Name: user_activity_log; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.user_activity_log (
    id bigint NOT NULL,
    user_id integer,
    action text NOT NULL,
    metadata jsonb,
    created_at timestamp with time zone DEFAULT now()
);


--
-- Name: user_activity_log_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.user_activity_log_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: user_activity_log_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.user_activity_log_id_seq OWNED BY public.user_activity_log.id;


--
-- Name: user_custom_themes; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.user_custom_themes (
    id integer NOT NULL,
    user_email character varying(255) NOT NULL,
    name character varying(80) NOT NULL,
    definition jsonb NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL
);


--
-- Name: TABLE user_custom_themes; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TABLE public.user_custom_themes IS 'Phase 3 per-user custom themes. Private to the owner (user_email); shared only by explicit JSON export/import. definition = validated colours + shadow + radius, mapped to --pal-* tokens at render time.';


--
-- Name: user_custom_themes_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.user_custom_themes_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: user_custom_themes_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.user_custom_themes_id_seq OWNED BY public.user_custom_themes.id;


--
-- Name: user_dashboard_config; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.user_dashboard_config (
    user_email character varying(255) NOT NULL,
    enabled_elements jsonb DEFAULT '[]'::jsonb NOT NULL,
    updated_at timestamp without time zone DEFAULT now() NOT NULL
);


--
-- Name: TABLE user_dashboard_config; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TABLE public.user_dashboard_config IS 'Per-user selection of dashboard elements (sections + module cards)';


--
-- Name: user_module_permissions; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.user_module_permissions (
    user_id bigint NOT NULL,
    module_key text NOT NULL,
    allowed boolean DEFAULT false NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL
);


--
-- Name: user_notifications; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.user_notifications (
    id integer NOT NULL,
    user_email character varying(255) NOT NULL,
    title text NOT NULL,
    message text NOT NULL,
    icon character varying(50) DEFAULT 'bi-bell'::character varying,
    type character varying(20) DEFAULT 'info'::character varying,
    is_read boolean DEFAULT false,
    created_at timestamp with time zone DEFAULT now()
);


--
-- Name: user_notifications_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.user_notifications_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: user_notifications_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.user_notifications_id_seq OWNED BY public.user_notifications.id;


--
-- Name: user_sessions; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.user_sessions (
    id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    user_id integer,
    session_key text NOT NULL,
    issued_at timestamp with time zone DEFAULT now() NOT NULL,
    expires_at timestamp with time zone NOT NULL,
    ip_address inet,
    user_agent text
);


--
-- Name: users; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.users (
    id integer NOT NULL,
    email public.citext NOT NULL,
    password_hash text NOT NULL,
    salt text NOT NULL,
    full_name text NOT NULL,
    role_id integer,
    department_id integer,
    "position" text,
    is_active boolean DEFAULT true NOT NULL,
    last_login_at timestamp with time zone,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL,
    is_first_login boolean DEFAULT true NOT NULL,
    theme_palette character varying(24) DEFAULT 'plava-klasicna'::character varying NOT NULL,
    theme_mode character varying(16) DEFAULT 'system'::character varying NOT NULL,
    theme_accent character varying(16) DEFAULT 'podrazumevano'::character varying NOT NULL,
    theme_style character varying(20) DEFAULT 'institucionalna'::character varying NOT NULL,
    theme_density character varying(16) DEFAULT 'komforno'::character varying NOT NULL,
    active_custom_theme_id integer,
    auth_version integer DEFAULT 1 NOT NULL,
    CONSTRAINT users_theme_accent_check CHECK (((theme_accent)::text = ANY ((ARRAY['podrazumevano'::character varying, 'zelena'::character varying, 'bordo'::character varying, 'oker'::character varying, 'petrolej'::character varying, 'klasicna-plava'::character varying, 'svetloplava'::character varying, 'tamnoplava'::character varying, 'tirkizna'::character varying, 'ljubicasta'::character varying, 'narandzasta'::character varying, 'grafitnosiva'::character varying])::text[]))),
    CONSTRAINT users_theme_density_check CHECK (((theme_density)::text = ANY ((ARRAY['komforno'::character varying, 'kompakt'::character varying])::text[]))),
    CONSTRAINT users_theme_mode_check CHECK (((theme_mode)::text = ANY ((ARRAY['light'::character varying, 'dark'::character varying, 'system'::character varying, 'contrast'::character varying])::text[]))),
    CONSTRAINT users_theme_palette_check CHECK (((theme_palette)::text = ANY ((ARRAY['heritage'::character varying, 'plava-klasicna'::character varying, 'plava-windows'::character varying, 'plava-tamna'::character varying, 'plava-ledena'::character varying, 'plava-muzejska'::character varying, 'siva-poslovna'::character varying, 'zelena-institucionalna'::character varying, 'bordo-muzejska'::character varying, 'crno-bela'::character varying, 'custom'::character varying])::text[]))),
    CONSTRAINT users_theme_style_check CHECK (((theme_style)::text = ANY ((ARRAY['institucionalna'::character varying, 'moderna'::character varying, 'arhivska'::character varying, 'terenska'::character varying])::text[])))
);


--
-- Name: COLUMN users.theme_palette; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.users.theme_palette IS 'Named theme palette: heritage (classic museum look) | plava-* (phase 1) | siva-poslovna | zelena-institucionalna | bordo-muzejska | crno-bela (phase 2 flat palettes) | custom (phase 3, render active_custom_theme_id)';


--
-- Name: COLUMN users.theme_mode; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.users.theme_mode IS 'UI theme mode: light | dark | system (prefers-color-scheme) | contrast (accessibility)';


--
-- Name: COLUMN users.theme_accent; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.users.theme_accent IS 'Accent axis: podrazumevano (family default) | zelena | bordo | oker | petrolej (heritage) | klasicna-plava | svetloplava | tamnoplava | tirkizna | ljubicasta | narandzasta | grafitnosiva (phase 2, applies to flat palettes)';


--
-- Name: COLUMN users.theme_style; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.users.theme_style IS 'Visual style character: institucionalna (default) | moderna | arhivska | terenska';


--
-- Name: COLUMN users.theme_density; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.users.theme_density IS 'UI density: komforno (default) | kompakt';


--
-- Name: COLUMN users.active_custom_theme_id; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.users.active_custom_theme_id IS 'Which user_custom_themes.id is applied when theme_palette = custom. Soft pointer (no FK): a dangling value falls back to the default palette.';


--
-- Name: COLUMN users.auth_version; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.users.auth_version IS 'Verzija prava naloga; bump pri deaktivaciji/promeni uloge/lozinke ruši postojeće sesije';


--
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;


--
-- Name: vehicle_availability; Type: VIEW; Schema: public; Owner: -
--

CREATE VIEW public.vehicle_availability AS
 SELECT v.id,
    v.name,
    v.registration,
    v.type,
    v.status,
    count(vr.id) FILTER (WHERE ((vr.status = 'Активна'::text) AND (vr.end_date >= CURRENT_DATE))) AS active_reservations,
    max(vr.end_date) FILTER (WHERE (vr.status = 'Активна'::text)) AS next_available_date
   FROM (public.vehicles v
     LEFT JOIN public.vehicle_reservations vr ON ((v.id = vr.vehicle_id)))
  GROUP BY v.id, v.name, v.registration, v.type, v.status;


--
-- Name: VIEW vehicle_availability; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON VIEW public.vehicle_availability IS 'Real-time vehicle availability status';


--
-- Name: vehicle_reservations_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.vehicle_reservations_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: vehicle_reservations_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.vehicle_reservations_id_seq OWNED BY public.vehicle_reservations.id;


--
-- Name: vehicle_usage_stats; Type: VIEW; Schema: public; Owner: -
--

CREATE VIEW public.vehicle_usage_stats AS
 SELECT v.id,
    v.name,
    v.registration,
    count(vr.id) AS total_reservations,
    count(vr.id) FILTER (WHERE (vr.status = 'Завршена'::text)) AS completed_reservations,
    count(vr.id) FILTER (WHERE (vr.status = 'Активна'::text)) AS active_reservations,
    count(vr.id) FILTER (WHERE (vr.status = 'Отказана'::text)) AS cancelled_reservations,
    sum(vr.estimated_km) FILTER (WHERE (vr.status = 'Завршена'::text)) AS total_km,
    min(vr.start_date) AS first_reservation,
    max(vr.end_date) AS last_reservation
   FROM (public.vehicles v
     LEFT JOIN public.vehicle_reservations vr ON ((v.id = vr.vehicle_id)))
  GROUP BY v.id, v.name, v.registration;


--
-- Name: VIEW vehicle_usage_stats; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON VIEW public.vehicle_usage_stats IS 'Vehicle usage statistics and metrics';


--
-- Name: vehicles_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.vehicles_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: vehicles_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.vehicles_id_seq OWNED BY public.vehicles.id;


--
-- Name: visitor_records; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.visitor_records (
    id integer NOT NULL,
    visit_date date,
    visitor_type text,
    group_size integer DEFAULT 1 NOT NULL,
    age_category text,
    nationality text,
    ticket_type text,
    guided_tour boolean DEFAULT false NOT NULL,
    exhibition text,
    feedback_rating text,
    notes text,
    created_at timestamp with time zone DEFAULT now() NOT NULL
);


--
-- Name: visitor_records_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.visitor_records_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: visitor_records_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.visitor_records_id_seq OWNED BY public.visitor_records.id;


--
-- Name: approval_signatures id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.approval_signatures ALTER COLUMN id SET DEFAULT nextval('public.approval_signatures_id_seq'::regclass);


--
-- Name: archive_requests id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.archive_requests ALTER COLUMN id SET DEFAULT nextval('public.archive_requests_id_seq'::regclass);


--
-- Name: audit_log id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.audit_log ALTER COLUMN id SET DEFAULT nextval('public.audit_log_id_seq'::regclass);


--
-- Name: audit_outbox id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.audit_outbox ALTER COLUMN id SET DEFAULT nextval('public.audit_outbox_id_seq'::regclass);


--
-- Name: bilja_hydrobioidea_radoman id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.bilja_hydrobioidea_radoman ALTER COLUMN id SET DEFAULT nextval('public.bilja_hydrobioidea_radoman_id_seq'::regclass);


--
-- Name: bilja_kenozojske_invertebrate id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.bilja_kenozojske_invertebrate ALTER COLUMN id SET DEFAULT nextval('public.bilja_kenozojske_invertebrate_id_seq'::regclass);


--
-- Name: bilja_opsta_zbirka_mollusca id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.bilja_opsta_zbirka_mollusca ALTER COLUMN id SET DEFAULT nextval('public.bilja_opsta_zbirka_mollusca_id_seq'::regclass);


--
-- Name: bilja_recentni_morski_mekusci id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.bilja_recentni_morski_mekusci ALTER COLUMN id SET DEFAULT nextval('public.bilja_recentni_morski_mekusci_id_seq'::regclass);


--
-- Name: bilja_skoljke_tadic id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.bilja_skoljke_tadic ALTER COLUMN id SET DEFAULT nextval('public.bilja_skoljke_tadic_id_seq'::regclass);


--
-- Name: bilja_suvozemni_puzevi_pavlovic id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.bilja_suvozemni_puzevi_pavlovic ALTER COLUMN id SET DEFAULT nextval('public.bilja_suvozemni_puzevi_pavlovic_id_seq'::regclass);


--
-- Name: bird_ringing_records id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.bird_ringing_records ALTER COLUMN id SET DEFAULT nextval('public.bird_ringing_records_id_seq'::regclass);


--
-- Name: bird_species id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.bird_species ALTER COLUMN id SET DEFAULT nextval('public.bird_species_id_seq'::regclass);


--
-- Name: chat_messages id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.chat_messages ALTER COLUMN id SET DEFAULT nextval('public.chat_messages_id_seq'::regclass);


--
-- Name: collection_specimens id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.collection_specimens ALTER COLUMN id SET DEFAULT nextval('public.collection_specimens_id_seq'::regclass);


--
-- Name: collection_types id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.collection_types ALTER COLUMN id SET DEFAULT nextval('public.collection_types_id_seq'::regclass);


--
-- Name: departments id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.departments ALTER COLUMN id SET DEFAULT nextval('public.departments_id_seq'::regclass);


--
-- Name: document_audit_log id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.document_audit_log ALTER COLUMN id SET DEFAULT nextval('public.document_audit_log_id_seq'::regclass);


--
-- Name: document_signatures id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.document_signatures ALTER COLUMN id SET DEFAULT nextval('public.document_signatures_id_seq'::regclass);


--
-- Name: document_versions id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.document_versions ALTER COLUMN id SET DEFAULT nextval('public.document_versions_id_seq'::regclass);


--
-- Name: documents id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.documents ALTER COLUMN id SET DEFAULT nextval('public.documents_id_seq'::regclass);


--
-- Name: employee_profiles id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.employee_profiles ALTER COLUMN id SET DEFAULT nextval('public.employee_profiles_id_seq'::regclass);


--
-- Name: employee_publications id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.employee_publications ALTER COLUMN id SET DEFAULT nextval('public.employee_publications_id_seq'::regclass);


--
-- Name: exhibition_events id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.exhibition_events ALTER COLUMN id SET DEFAULT nextval('public.exhibition_events_id_seq'::regclass);


--
-- Name: exhibition_items id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.exhibition_items ALTER COLUMN id SET DEFAULT nextval('public.exhibition_items_id_seq'::regclass);


--
-- Name: exhibitions id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.exhibitions ALTER COLUMN id SET DEFAULT nextval('public.exhibitions_id_seq'::regclass);


--
-- Name: financial_plans id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.financial_plans ALTER COLUMN id SET DEFAULT nextval('public.financial_plans_id_seq'::regclass);


--
-- Name: foto_poslovi id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.foto_poslovi ALTER COLUMN id SET DEFAULT nextval('public.foto_poslovi_id_seq'::regclass);


--
-- Name: foto_veza_izlozba id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.foto_veza_izlozba ALTER COLUMN id SET DEFAULT nextval('public.foto_veza_izlozba_id_seq'::regclass);


--
-- Name: foto_veza_kr_dosije id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.foto_veza_kr_dosije ALTER COLUMN id SET DEFAULT nextval('public.foto_veza_kr_dosije_id_seq'::regclass);


--
-- Name: foto_veza_predmet id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.foto_veza_predmet ALTER COLUMN id SET DEFAULT nextval('public.foto_veza_predmet_id_seq'::regclass);


--
-- Name: foto_veza_projekat id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.foto_veza_projekat ALTER COLUMN id SET DEFAULT nextval('public.foto_veza_projekat_id_seq'::regclass);


--
-- Name: foto_veza_teren id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.foto_veza_teren ALTER COLUMN id SET DEFAULT nextval('public.foto_veza_teren_id_seq'::regclass);


--
-- Name: fotografija_tagovi id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.fotografija_tagovi ALTER COLUMN id SET DEFAULT nextval('public.fotografija_tagovi_id_seq'::regclass);


--
-- Name: fotografije id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.fotografije ALTER COLUMN id SET DEFAULT nextval('public.fotografije_id_seq'::regclass);


--
-- Name: fototeka_intake_pending id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.fototeka_intake_pending ALTER COLUMN id SET DEFAULT nextval('public.fototeka_intake_pending_id_seq'::regclass);


--
-- Name: fototeka_projekti id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.fototeka_projekti ALTER COLUMN id SET DEFAULT nextval('public.fototeka_projekti_id_seq'::regclass);


--
-- Name: fototeka_tereni id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.fototeka_tereni ALTER COLUMN id SET DEFAULT nextval('public.fototeka_tereni_id_seq'::regclass);


--
-- Name: fototeka_uvoz_run id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.fototeka_uvoz_run ALTER COLUMN id SET DEFAULT nextval('public.fototeka_uvoz_run_id_seq'::regclass);


--
-- Name: fototeka_uvoz_stavka id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.fototeka_uvoz_stavka ALTER COLUMN id SET DEFAULT nextval('public.fototeka_uvoz_stavka_id_seq'::regclass);


--
-- Name: geo_field_data id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.geo_field_data ALTER COLUMN id SET DEFAULT nextval('public.geo_field_data_id_seq'::regclass);


--
-- Name: heritage_categories id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.heritage_categories ALTER COLUMN id SET DEFAULT nextval('public.heritage_categories_id_seq'::regclass);


--
-- Name: heritage_items id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.heritage_items ALTER COLUMN id SET DEFAULT nextval('public.heritage_items_id_seq'::regclass);


--
-- Name: heritage_types id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.heritage_types ALTER COLUMN id SET DEFAULT nextval('public.heritage_types_id_seq'::regclass);


--
-- Name: images id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.images ALTER COLUMN id SET DEFAULT nextval('public.images_id_seq'::regclass);


--
-- Name: inventory_entries id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.inventory_entries ALTER COLUMN id SET DEFAULT nextval('public.inventory_entries_id_seq'::regclass);


--
-- Name: kr_dosije id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.kr_dosije ALTER COLUMN id SET DEFAULT nextval('public.kr_dosije_id_seq'::regclass);


--
-- Name: kr_dosije_izvrsilac id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.kr_dosije_izvrsilac ALTER COLUMN id SET DEFAULT nextval('public.kr_dosije_izvrsilac_id_seq'::regclass);


--
-- Name: kr_predlozak id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.kr_predlozak ALTER COLUMN id SET DEFAULT nextval('public.kr_predlozak_id_seq'::regclass);


--
-- Name: library_books id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.library_books ALTER COLUMN id SET DEFAULT nextval('public.library_books_id_seq'::regclass);


--
-- Name: library_categories id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.library_categories ALTER COLUMN id SET DEFAULT nextval('public.library_categories_id_seq'::regclass);


--
-- Name: library_loans id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.library_loans ALTER COLUMN id SET DEFAULT nextval('public.library_loans_id_seq'::regclass);


--
-- Name: localities id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.localities ALTER COLUMN id SET DEFAULT nextval('public.localities_id_seq'::regclass);


--
-- Name: meteorite_specimens id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.meteorite_specimens ALTER COLUMN id SET DEFAULT nextval('public.meteorite_specimens_id_seq'::regclass);


--
-- Name: mineral_references id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.mineral_references ALTER COLUMN id SET DEFAULT nextval('public.mineral_references_id_seq'::regclass);


--
-- Name: mineral_rruff_matches id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.mineral_rruff_matches ALTER COLUMN id SET DEFAULT nextval('public.mineral_rruff_matches_id_seq'::regclass);


--
-- Name: minerals id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.minerals ALTER COLUMN id SET DEFAULT nextval('public.minerals_id_seq'::regclass);


--
-- Name: news_articles id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.news_articles ALTER COLUMN id SET DEFAULT nextval('public.news_articles_id_seq'::regclass);


--
-- Name: paper_feature_links id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.paper_feature_links ALTER COLUMN id SET DEFAULT nextval('public.paper_feature_links_id_seq'::regclass);


--
-- Name: paper_locality_links id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.paper_locality_links ALTER COLUMN id SET DEFAULT nextval('public.paper_locality_links_id_seq'::regclass);


--
-- Name: procurement_requests id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.procurement_requests ALTER COLUMN id SET DEFAULT nextval('public.procurement_requests_id_seq'::regclass);


--
-- Name: request_comments id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.request_comments ALTER COLUMN id SET DEFAULT nextval('public.request_comments_id_seq'::regclass);


--
-- Name: request_history id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.request_history ALTER COLUMN id SET DEFAULT nextval('public.request_history_id_seq'::regclass);


--
-- Name: research_projects id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.research_projects ALTER COLUMN id SET DEFAULT nextval('public.research_projects_id_seq'::regclass);


--
-- Name: roles id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.roles ALTER COLUMN id SET DEFAULT nextval('public.roles_id_seq'::regclass);


--
-- Name: rruff_chemistry id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.rruff_chemistry ALTER COLUMN id SET DEFAULT nextval('public.rruff_chemistry_id_seq'::regclass);


--
-- Name: rruff_localities id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.rruff_localities ALTER COLUMN id SET DEFAULT nextval('public.rruff_localities_id_seq'::regclass);


--
-- Name: rruff_minerals id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.rruff_minerals ALTER COLUMN id SET DEFAULT nextval('public.rruff_minerals_id_seq'::regclass);


--
-- Name: rruff_references id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.rruff_references ALTER COLUMN id SET DEFAULT nextval('public.rruff_references_id_seq'::regclass);


--
-- Name: scientific_papers id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.scientific_papers ALTER COLUMN id SET DEFAULT nextval('public.scientific_papers_id_seq'::regclass);


--
-- Name: signature_audit_log id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.signature_audit_log ALTER COLUMN id SET DEFAULT nextval('public.signature_audit_log_id_seq'::regclass);


--
-- Name: signature_templates id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.signature_templates ALTER COLUMN id SET DEFAULT nextval('public.signature_templates_id_seq'::regclass);


--
-- Name: timesheet_audit_log id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.timesheet_audit_log ALTER COLUMN id SET DEFAULT nextval('public.timesheet_audit_log_id_seq'::regclass);


--
-- Name: timesheet_edit_requests id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.timesheet_edit_requests ALTER COLUMN id SET DEFAULT nextval('public.timesheet_edit_requests_id_seq'::regclass);


--
-- Name: timesheet_entries id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.timesheet_entries ALTER COLUMN id SET DEFAULT nextval('public.timesheet_entries_id_seq'::regclass);


--
-- Name: timesheet_report_days id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.timesheet_report_days ALTER COLUMN id SET DEFAULT nextval('public.timesheet_report_days_id_seq'::regclass);


--
-- Name: timesheet_reports id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.timesheet_reports ALTER COLUMN id SET DEFAULT nextval('public.timesheet_reports_id_seq'::regclass);


--
-- Name: timesheet_status_history id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.timesheet_status_history ALTER COLUMN id SET DEFAULT nextval('public.timesheet_status_history_id_seq'::regclass);


--
-- Name: user_activity_log id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.user_activity_log ALTER COLUMN id SET DEFAULT nextval('public.user_activity_log_id_seq'::regclass);


--
-- Name: user_custom_themes id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.user_custom_themes ALTER COLUMN id SET DEFAULT nextval('public.user_custom_themes_id_seq'::regclass);


--
-- Name: user_notifications id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.user_notifications ALTER COLUMN id SET DEFAULT nextval('public.user_notifications_id_seq'::regclass);


--
-- Name: users id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);


--
-- Name: vehicle_reservations id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.vehicle_reservations ALTER COLUMN id SET DEFAULT nextval('public.vehicle_reservations_id_seq'::regclass);


--
-- Name: vehicles id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.vehicles ALTER COLUMN id SET DEFAULT nextval('public.vehicles_id_seq'::regclass);


--
-- Name: visitor_records id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.visitor_records ALTER COLUMN id SET DEFAULT nextval('public.visitor_records_id_seq'::regclass);


--
-- Name: app_shared_settings app_shared_settings_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.app_shared_settings
    ADD CONSTRAINT app_shared_settings_pkey PRIMARY KEY (setting_key);


--
-- Name: approval_signatures approval_signatures_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.approval_signatures
    ADD CONSTRAINT approval_signatures_pkey PRIMARY KEY (id);


--
-- Name: approval_signatures approval_signatures_request_id_approver_role_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.approval_signatures
    ADD CONSTRAINT approval_signatures_request_id_approver_role_key UNIQUE (request_id, approver_role);


--
-- Name: archive_requests archive_requests_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.archive_requests
    ADD CONSTRAINT archive_requests_pkey PRIMARY KEY (id);


--
-- Name: audit_log audit_log_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.audit_log
    ADD CONSTRAINT audit_log_pkey PRIMARY KEY (id);


--
-- Name: audit_outbox audit_outbox_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.audit_outbox
    ADD CONSTRAINT audit_outbox_pkey PRIMARY KEY (id);


--
-- Name: bilja_hydrobioidea_radoman bilja_hydrobioidea_radoman_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.bilja_hydrobioidea_radoman
    ADD CONSTRAINT bilja_hydrobioidea_radoman_pkey PRIMARY KEY (id);


--
-- Name: bilja_kenozojske_invertebrate bilja_kenozojske_invertebrate_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.bilja_kenozojske_invertebrate
    ADD CONSTRAINT bilja_kenozojske_invertebrate_pkey PRIMARY KEY (id);


--
-- Name: bilja_opsta_zbirka_mollusca bilja_opsta_zbirka_mollusca_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.bilja_opsta_zbirka_mollusca
    ADD CONSTRAINT bilja_opsta_zbirka_mollusca_pkey PRIMARY KEY (id);


--
-- Name: bilja_recentni_morski_mekusci bilja_recentni_morski_mekusci_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.bilja_recentni_morski_mekusci
    ADD CONSTRAINT bilja_recentni_morski_mekusci_pkey PRIMARY KEY (id);


--
-- Name: bilja_skoljke_tadic bilja_skoljke_tadic_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.bilja_skoljke_tadic
    ADD CONSTRAINT bilja_skoljke_tadic_pkey PRIMARY KEY (id);


--
-- Name: bilja_suvozemni_puzevi_pavlovic bilja_suvozemni_puzevi_pavlovic_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.bilja_suvozemni_puzevi_pavlovic
    ADD CONSTRAINT bilja_suvozemni_puzevi_pavlovic_pkey PRIMARY KEY (id);


--
-- Name: bird_ringing_records bird_ringing_records_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.bird_ringing_records
    ADD CONSTRAINT bird_ringing_records_pkey PRIMARY KEY (id);


--
-- Name: bird_species bird_species_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.bird_species
    ADD CONSTRAINT bird_species_pkey PRIMARY KEY (id);


--
-- Name: bird_species bird_species_species_name_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.bird_species
    ADD CONSTRAINT bird_species_species_name_key UNIQUE (species_name);


--
-- Name: chat_messages chat_messages_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.chat_messages
    ADD CONSTRAINT chat_messages_pkey PRIMARY KEY (id);


--
-- Name: chat_presence chat_presence_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.chat_presence
    ADD CONSTRAINT chat_presence_pkey PRIMARY KEY (user_id);


--
-- Name: chat_unread_cursors chat_unread_cursors_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.chat_unread_cursors
    ADD CONSTRAINT chat_unread_cursors_pkey PRIMARY KEY (user_id, channel);


--
-- Name: timesheet_report_days chk_report_days_hours_range; Type: CHECK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE public.timesheet_report_days
    ADD CONSTRAINT chk_report_days_hours_range CHECK (((work_in_museum >= (0)::numeric) AND (work_in_museum <= (24)::numeric) AND (work_outside >= (0)::numeric) AND (work_outside <= (24)::numeric) AND (vacation >= (0)::numeric) AND (vacation <= (24)::numeric) AND (public_holiday >= (0)::numeric) AND (public_holiday <= (24)::numeric) AND (paid_leave >= (0)::numeric) AND (paid_leave <= (24)::numeric) AND (other_leave >= (0)::numeric) AND (other_leave <= (24)::numeric) AND (sick_leave_lt30 >= (0)::numeric) AND (sick_leave_lt30 <= (24)::numeric) AND (sick_leave_gte30 >= (0)::numeric) AND (sick_leave_gte30 <= (24)::numeric))) NOT VALID;


--
-- Name: collection_specimens collection_specimens_catalog_number_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.collection_specimens
    ADD CONSTRAINT collection_specimens_catalog_number_key UNIQUE (catalog_number);


--
-- Name: collection_specimens collection_specimens_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.collection_specimens
    ADD CONSTRAINT collection_specimens_pkey PRIMARY KEY (id);


--
-- Name: collection_types collection_types_code_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.collection_types
    ADD CONSTRAINT collection_types_code_key UNIQUE (code);


--
-- Name: collection_types collection_types_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.collection_types
    ADD CONSTRAINT collection_types_pkey PRIMARY KEY (id);


--
-- Name: departments departments_name_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.departments
    ADD CONSTRAINT departments_name_key UNIQUE (name);


--
-- Name: departments departments_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.departments
    ADD CONSTRAINT departments_pkey PRIMARY KEY (id);


--
-- Name: digitized_profiles digitized_profiles_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.digitized_profiles
    ADD CONSTRAINT digitized_profiles_pkey PRIMARY KEY (id);


--
-- Name: document_audit_log document_audit_log_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.document_audit_log
    ADD CONSTRAINT document_audit_log_pkey PRIMARY KEY (id);


--
-- Name: document_signatures document_signatures_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.document_signatures
    ADD CONSTRAINT document_signatures_pkey PRIMARY KEY (id);


--
-- Name: document_versions document_versions_document_id_version_no_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.document_versions
    ADD CONSTRAINT document_versions_document_id_version_no_key UNIQUE (document_id, version_no);


--
-- Name: document_versions document_versions_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.document_versions
    ADD CONSTRAINT document_versions_pkey PRIMARY KEY (id);


--
-- Name: documents documents_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.documents
    ADD CONSTRAINT documents_pkey PRIMARY KEY (id);


--
-- Name: employee_profiles employee_profiles_email_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.employee_profiles
    ADD CONSTRAINT employee_profiles_email_key UNIQUE (email);


--
-- Name: employee_profiles employee_profiles_employee_id_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.employee_profiles
    ADD CONSTRAINT employee_profiles_employee_id_key UNIQUE (employee_id);


--
-- Name: employee_profiles employee_profiles_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.employee_profiles
    ADD CONSTRAINT employee_profiles_pkey PRIMARY KEY (id);


--
-- Name: employee_publications employee_publications_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.employee_publications
    ADD CONSTRAINT employee_publications_pkey PRIMARY KEY (id);


--
-- Name: vehicle_reservations excl_vehicle_rezervacije_preklapanje; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.vehicle_reservations
    ADD CONSTRAINT excl_vehicle_rezervacije_preklapanje EXCLUDE USING gist (vehicle_id WITH =, daterange(start_date, end_date, '[]'::text) WITH &&) WHERE ((status = 'Активна'::text));


--
-- Name: CONSTRAINT excl_vehicle_rezervacije_preklapanje ON vehicle_reservations; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON CONSTRAINT excl_vehicle_rezervacije_preklapanje ON public.vehicle_reservations IS 'Aktivne rezervacije istog vozila ne smeju da se preklapaju po datumu (btree_gist)';


--
-- Name: exhibition_events exhibition_events_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.exhibition_events
    ADD CONSTRAINT exhibition_events_pkey PRIMARY KEY (id);


--
-- Name: exhibition_items exhibition_items_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.exhibition_items
    ADD CONSTRAINT exhibition_items_pkey PRIMARY KEY (id);


--
-- Name: exhibitions exhibitions_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.exhibitions
    ADD CONSTRAINT exhibitions_pkey PRIMARY KEY (id);


--
-- Name: financial_plans financial_plans_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.financial_plans
    ADD CONSTRAINT financial_plans_pkey PRIMARY KEY (id);


--
-- Name: foto_poslovi foto_poslovi_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.foto_poslovi
    ADD CONSTRAINT foto_poslovi_pkey PRIMARY KEY (id);


--
-- Name: foto_veza_izlozba foto_veza_izlozba_fotografija_id_exhibition_id_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.foto_veza_izlozba
    ADD CONSTRAINT foto_veza_izlozba_fotografija_id_exhibition_id_key UNIQUE (fotografija_id, exhibition_id);


--
-- Name: foto_veza_izlozba foto_veza_izlozba_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.foto_veza_izlozba
    ADD CONSTRAINT foto_veza_izlozba_pkey PRIMARY KEY (id);


--
-- Name: foto_veza_kr_dosije foto_veza_kr_dosije_fotografija_id_dosije_id_faza_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.foto_veza_kr_dosije
    ADD CONSTRAINT foto_veza_kr_dosije_fotografija_id_dosije_id_faza_key UNIQUE (fotografija_id, dosije_id, faza);


--
-- Name: foto_veza_kr_dosije foto_veza_kr_dosije_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.foto_veza_kr_dosije
    ADD CONSTRAINT foto_veza_kr_dosije_pkey PRIMARY KEY (id);


--
-- Name: foto_veza_predmet foto_veza_predmet_fotografija_id_database_name_inventarni_b_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.foto_veza_predmet
    ADD CONSTRAINT foto_veza_predmet_fotografija_id_database_name_inventarni_b_key UNIQUE (fotografija_id, database_name, inventarni_broj);


--
-- Name: foto_veza_predmet foto_veza_predmet_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.foto_veza_predmet
    ADD CONSTRAINT foto_veza_predmet_pkey PRIMARY KEY (id);


--
-- Name: foto_veza_projekat foto_veza_projekat_fotografija_id_projekat_id_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.foto_veza_projekat
    ADD CONSTRAINT foto_veza_projekat_fotografija_id_projekat_id_key UNIQUE (fotografija_id, projekat_id);


--
-- Name: foto_veza_projekat foto_veza_projekat_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.foto_veza_projekat
    ADD CONSTRAINT foto_veza_projekat_pkey PRIMARY KEY (id);


--
-- Name: foto_veza_teren foto_veza_teren_fotografija_id_teren_id_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.foto_veza_teren
    ADD CONSTRAINT foto_veza_teren_fotografija_id_teren_id_key UNIQUE (fotografija_id, teren_id);


--
-- Name: foto_veza_teren foto_veza_teren_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.foto_veza_teren
    ADD CONSTRAINT foto_veza_teren_pkey PRIMARY KEY (id);


--
-- Name: fotografija_tagovi fotografija_tagovi_fotografija_id_tag_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.fotografija_tagovi
    ADD CONSTRAINT fotografija_tagovi_fotografija_id_tag_key UNIQUE (fotografija_id, tag);


--
-- Name: fotografija_tagovi fotografija_tagovi_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.fotografija_tagovi
    ADD CONSTRAINT fotografija_tagovi_pkey PRIMARY KEY (id);


--
-- Name: fotografije fotografije_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.fotografije
    ADD CONSTRAINT fotografije_pkey PRIMARY KEY (id);


--
-- Name: fotografije fotografije_raw_putanja_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.fotografije
    ADD CONSTRAINT fotografije_raw_putanja_key UNIQUE (raw_putanja);


--
-- Name: fotografije fotografije_sha256_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.fotografije
    ADD CONSTRAINT fotografije_sha256_key UNIQUE (sha256);


--
-- Name: fototeka_intake_pending fototeka_intake_pending_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.fototeka_intake_pending
    ADD CONSTRAINT fototeka_intake_pending_pkey PRIMARY KEY (id);


--
-- Name: fototeka_projekti fototeka_projekti_naziv_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.fototeka_projekti
    ADD CONSTRAINT fototeka_projekti_naziv_key UNIQUE (naziv);


--
-- Name: fototeka_projekti fototeka_projekti_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.fototeka_projekti
    ADD CONSTRAINT fototeka_projekti_pkey PRIMARY KEY (id);


--
-- Name: fototeka_tereni fototeka_tereni_godina_naziv_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.fototeka_tereni
    ADD CONSTRAINT fototeka_tereni_godina_naziv_key UNIQUE (godina, naziv);


--
-- Name: fototeka_tereni fototeka_tereni_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.fototeka_tereni
    ADD CONSTRAINT fototeka_tereni_pkey PRIMARY KEY (id);


--
-- Name: fototeka_uvoz_run fototeka_uvoz_run_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.fototeka_uvoz_run
    ADD CONSTRAINT fototeka_uvoz_run_pkey PRIMARY KEY (id);


--
-- Name: fototeka_uvoz_stavka fototeka_uvoz_stavka_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.fototeka_uvoz_stavka
    ADD CONSTRAINT fototeka_uvoz_stavka_pkey PRIMARY KEY (id);


--
-- Name: geo_field_data geo_field_data_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.geo_field_data
    ADD CONSTRAINT geo_field_data_pkey PRIMARY KEY (id);


--
-- Name: heritage_categories heritage_categories_category_name_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.heritage_categories
    ADD CONSTRAINT heritage_categories_category_name_key UNIQUE (category_name);


--
-- Name: heritage_categories heritage_categories_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.heritage_categories
    ADD CONSTRAINT heritage_categories_pkey PRIMARY KEY (id);


--
-- Name: heritage_items heritage_items_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.heritage_items
    ADD CONSTRAINT heritage_items_pkey PRIMARY KEY (id);


--
-- Name: heritage_items heritage_items_registry_number_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.heritage_items
    ADD CONSTRAINT heritage_items_registry_number_key UNIQUE (registry_number);


--
-- Name: heritage_types heritage_types_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.heritage_types
    ADD CONSTRAINT heritage_types_pkey PRIMARY KEY (id);


--
-- Name: heritage_types heritage_types_type_name_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.heritage_types
    ADD CONSTRAINT heritage_types_type_name_key UNIQUE (type_name);


--
-- Name: images images_image_id_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.images
    ADD CONSTRAINT images_image_id_key UNIQUE (image_id);


--
-- Name: images images_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.images
    ADD CONSTRAINT images_pkey PRIMARY KEY (id);


--
-- Name: inventory_entries inventory_entries_inventory_number_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.inventory_entries
    ADD CONSTRAINT inventory_entries_inventory_number_key UNIQUE (inventory_number);


--
-- Name: inventory_entries inventory_entries_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.inventory_entries
    ADD CONSTRAINT inventory_entries_pkey PRIMARY KEY (id);


--
-- Name: kr_dosije kr_dosije_evidencioni_broj_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.kr_dosije
    ADD CONSTRAINT kr_dosije_evidencioni_broj_key UNIQUE (evidencioni_broj);


--
-- Name: kr_dosije_izvrsilac kr_dosije_izvrsilac_dosije_id_ime_tekst_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.kr_dosije_izvrsilac
    ADD CONSTRAINT kr_dosije_izvrsilac_dosije_id_ime_tekst_key UNIQUE (dosije_id, ime_tekst);


--
-- Name: kr_dosije_izvrsilac kr_dosije_izvrsilac_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.kr_dosije_izvrsilac
    ADD CONSTRAINT kr_dosije_izvrsilac_pkey PRIMARY KEY (id);


--
-- Name: kr_dosije kr_dosije_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.kr_dosije
    ADD CONSTRAINT kr_dosije_pkey PRIMARY KEY (id);


--
-- Name: kr_predlozak kr_predlozak_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.kr_predlozak
    ADD CONSTRAINT kr_predlozak_pkey PRIMARY KEY (id);


--
-- Name: library_books library_books_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.library_books
    ADD CONSTRAINT library_books_pkey PRIMARY KEY (id);


--
-- Name: library_categories library_categories_name_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.library_categories
    ADD CONSTRAINT library_categories_name_key UNIQUE (name);


--
-- Name: library_categories library_categories_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.library_categories
    ADD CONSTRAINT library_categories_pkey PRIMARY KEY (id);


--
-- Name: library_loans library_loans_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.library_loans
    ADD CONSTRAINT library_loans_pkey PRIMARY KEY (id);


--
-- Name: localities localities_name_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.localities
    ADD CONSTRAINT localities_name_key UNIQUE (name);


--
-- Name: localities localities_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.localities
    ADD CONSTRAINT localities_pkey PRIMARY KEY (id);


--
-- Name: mail_cache_folders mail_cache_folders_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.mail_cache_folders
    ADD CONSTRAINT mail_cache_folders_pkey PRIMARY KEY (user_email, name);


--
-- Name: mail_cache_messages mail_cache_messages_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.mail_cache_messages
    ADD CONSTRAINT mail_cache_messages_pkey PRIMARY KEY (user_email, folder, uid);


--
-- Name: mail_cache_meta mail_cache_meta_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.mail_cache_meta
    ADD CONSTRAINT mail_cache_meta_pkey PRIMARY KEY (user_email, key);


--
-- Name: mail_cache_pending_reads mail_cache_pending_reads_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.mail_cache_pending_reads
    ADD CONSTRAINT mail_cache_pending_reads_pkey PRIMARY KEY (user_email, folder, uid);


--
-- Name: mail_user_settings mail_user_settings_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.mail_user_settings
    ADD CONSTRAINT mail_user_settings_pkey PRIMARY KEY (user_email);


--
-- Name: meteorite_specimens meteorite_specimens_catalog_number_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.meteorite_specimens
    ADD CONSTRAINT meteorite_specimens_catalog_number_key UNIQUE (catalog_number);


--
-- Name: meteorite_specimens meteorite_specimens_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.meteorite_specimens
    ADD CONSTRAINT meteorite_specimens_pkey PRIMARY KEY (id);


--
-- Name: mineral_references mineral_references_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.mineral_references
    ADD CONSTRAINT mineral_references_pkey PRIMARY KEY (id);


--
-- Name: mineral_rruff_matches mineral_rruff_matches_mineral_id_rruff_id_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.mineral_rruff_matches
    ADD CONSTRAINT mineral_rruff_matches_mineral_id_rruff_id_key UNIQUE (mineral_id, rruff_id);


--
-- Name: mineral_rruff_matches mineral_rruff_matches_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.mineral_rruff_matches
    ADD CONSTRAINT mineral_rruff_matches_pkey PRIMARY KEY (id);


--
-- Name: minerals minerals_inventory_number_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.minerals
    ADD CONSTRAINT minerals_inventory_number_key UNIQUE (inventory_number);


--
-- Name: minerals minerals_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.minerals
    ADD CONSTRAINT minerals_pkey PRIMARY KEY (id);


--
-- Name: news_articles news_articles_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.news_articles
    ADD CONSTRAINT news_articles_pkey PRIMARY KEY (id);


--
-- Name: paper_feature_links paper_feature_links_paper_id_feature_type_feature_name_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.paper_feature_links
    ADD CONSTRAINT paper_feature_links_paper_id_feature_type_feature_name_key UNIQUE (paper_id, feature_type, feature_name);


--
-- Name: paper_feature_links paper_feature_links_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.paper_feature_links
    ADD CONSTRAINT paper_feature_links_pkey PRIMARY KEY (id);


--
-- Name: paper_locality_links paper_locality_links_paper_id_locality_name_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.paper_locality_links
    ADD CONSTRAINT paper_locality_links_paper_id_locality_name_key UNIQUE (paper_id, locality_name);


--
-- Name: paper_locality_links paper_locality_links_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.paper_locality_links
    ADD CONSTRAINT paper_locality_links_pkey PRIMARY KEY (id);


--
-- Name: procurement_requests procurement_requests_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.procurement_requests
    ADD CONSTRAINT procurement_requests_pkey PRIMARY KEY (id);


--
-- Name: project_space_planner_state project_space_planner_state_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.project_space_planner_state
    ADD CONSTRAINT project_space_planner_state_pkey PRIMARY KEY (id);


--
-- Name: request_comments request_comments_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.request_comments
    ADD CONSTRAINT request_comments_pkey PRIMARY KEY (id);


--
-- Name: request_history request_history_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.request_history
    ADD CONSTRAINT request_history_pkey PRIMARY KEY (id);


--
-- Name: research_projects research_projects_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.research_projects
    ADD CONSTRAINT research_projects_pkey PRIMARY KEY (id);


--
-- Name: roles roles_name_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.roles
    ADD CONSTRAINT roles_name_key UNIQUE (name);


--
-- Name: roles roles_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.roles
    ADD CONSTRAINT roles_pkey PRIMARY KEY (id);


--
-- Name: rruff_chemistry rruff_chemistry_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.rruff_chemistry
    ADD CONSTRAINT rruff_chemistry_pkey PRIMARY KEY (id);


--
-- Name: rruff_localities rruff_localities_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.rruff_localities
    ADD CONSTRAINT rruff_localities_pkey PRIMARY KEY (id);


--
-- Name: rruff_minerals rruff_minerals_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.rruff_minerals
    ADD CONSTRAINT rruff_minerals_pkey PRIMARY KEY (id);


--
-- Name: rruff_minerals rruff_minerals_rruff_id_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.rruff_minerals
    ADD CONSTRAINT rruff_minerals_rruff_id_key UNIQUE (rruff_id);


--
-- Name: rruff_references rruff_references_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.rruff_references
    ADD CONSTRAINT rruff_references_pkey PRIMARY KEY (id);


--
-- Name: sanja_paleogene_neogene_mammals sanja_paleogene_neogene_mammals_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.sanja_paleogene_neogene_mammals
    ADD CONSTRAINT sanja_paleogene_neogene_mammals_pkey PRIMARY KEY (id);


--
-- Name: schema_migrations schema_migrations_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.schema_migrations
    ADD CONSTRAINT schema_migrations_pkey PRIMARY KEY (filename);


--
-- Name: science_news science_news_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.science_news
    ADD CONSTRAINT science_news_pkey PRIMARY KEY (id);


--
-- Name: scientific_papers scientific_papers_openalex_id_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.scientific_papers
    ADD CONSTRAINT scientific_papers_openalex_id_key UNIQUE (openalex_id);


--
-- Name: scientific_papers scientific_papers_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.scientific_papers
    ADD CONSTRAINT scientific_papers_pkey PRIMARY KEY (id);


--
-- Name: signature_audit_log signature_audit_log_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.signature_audit_log
    ADD CONSTRAINT signature_audit_log_pkey PRIMARY KEY (id);


--
-- Name: signature_templates signature_templates_document_type_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.signature_templates
    ADD CONSTRAINT signature_templates_document_type_key UNIQUE (document_type);


--
-- Name: signature_templates signature_templates_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.signature_templates
    ADD CONSTRAINT signature_templates_pkey PRIMARY KEY (id);


--
-- Name: timesheet_audit_log timesheet_audit_log_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.timesheet_audit_log
    ADD CONSTRAINT timesheet_audit_log_pkey PRIMARY KEY (id);


--
-- Name: timesheet_edit_requests timesheet_edit_requests_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.timesheet_edit_requests
    ADD CONSTRAINT timesheet_edit_requests_pkey PRIMARY KEY (id);


--
-- Name: timesheet_entries timesheet_entries_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.timesheet_entries
    ADD CONSTRAINT timesheet_entries_pkey PRIMARY KEY (id);


--
-- Name: timesheet_entries timesheet_entries_report_id_category_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.timesheet_entries
    ADD CONSTRAINT timesheet_entries_report_id_category_key UNIQUE (report_id, category);


--
-- Name: timesheet_report_days timesheet_report_days_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.timesheet_report_days
    ADD CONSTRAINT timesheet_report_days_pkey PRIMARY KEY (id);


--
-- Name: timesheet_report_days timesheet_report_days_report_id_day_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.timesheet_report_days
    ADD CONSTRAINT timesheet_report_days_report_id_day_key UNIQUE (report_id, day);


--
-- Name: timesheet_reports timesheet_reports_legacy_radna_lista_id_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.timesheet_reports
    ADD CONSTRAINT timesheet_reports_legacy_radna_lista_id_key UNIQUE (legacy_radna_lista_id);


--
-- Name: timesheet_reports timesheet_reports_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.timesheet_reports
    ADD CONSTRAINT timesheet_reports_pkey PRIMARY KEY (id);


--
-- Name: timesheet_status_history timesheet_status_history_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.timesheet_status_history
    ADD CONSTRAINT timesheet_status_history_pkey PRIMARY KEY (id);


--
-- Name: timesheet_reports unique_employee_month_year; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.timesheet_reports
    ADD CONSTRAINT unique_employee_month_year UNIQUE (employee_email, month, year);


--
-- Name: user_activity_log user_activity_log_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.user_activity_log
    ADD CONSTRAINT user_activity_log_pkey PRIMARY KEY (id);


--
-- Name: user_custom_themes user_custom_themes_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.user_custom_themes
    ADD CONSTRAINT user_custom_themes_pkey PRIMARY KEY (id);


--
-- Name: user_dashboard_config user_dashboard_config_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.user_dashboard_config
    ADD CONSTRAINT user_dashboard_config_pkey PRIMARY KEY (user_email);


--
-- Name: user_module_permissions user_module_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.user_module_permissions
    ADD CONSTRAINT user_module_permissions_pkey PRIMARY KEY (user_id, module_key);


--
-- Name: user_notifications user_notifications_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.user_notifications
    ADD CONSTRAINT user_notifications_pkey PRIMARY KEY (id);


--
-- Name: user_sessions user_sessions_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.user_sessions
    ADD CONSTRAINT user_sessions_pkey PRIMARY KEY (id);


--
-- Name: user_sessions user_sessions_session_key_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.user_sessions
    ADD CONSTRAINT user_sessions_session_key_key UNIQUE (session_key);


--
-- Name: users users_email_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_email_key UNIQUE (email);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: vehicle_reservations vehicle_reservations_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.vehicle_reservations
    ADD CONSTRAINT vehicle_reservations_pkey PRIMARY KEY (id);


--
-- Name: vehicle_reservations vehicle_reservations_time_check; Type: CHECK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE public.vehicle_reservations
    ADD CONSTRAINT vehicle_reservations_time_check CHECK ((ends_at > starts_at)) NOT VALID;


--
-- Name: vehicles vehicles_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.vehicles
    ADD CONSTRAINT vehicles_pkey PRIMARY KEY (id);


--
-- Name: vehicles vehicles_registration_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.vehicles
    ADD CONSTRAINT vehicles_registration_key UNIQUE (registration);


--
-- Name: visitor_records visitor_records_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.visitor_records
    ADD CONSTRAINT visitor_records_pkey PRIMARY KEY (id);


--
-- Name: audit_table_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX audit_table_idx ON public.audit_log USING btree (table_name, record_id);


--
-- Name: bird_ringing_date_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX bird_ringing_date_idx ON public.bird_ringing_records USING btree (event_date);


--
-- Name: bird_ringing_geo_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX bird_ringing_geo_idx ON public.bird_ringing_records USING gist (coordinates);


--
-- Name: bird_ringing_species_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX bird_ringing_species_idx ON public.bird_ringing_records USING btree (species_id);


--
-- Name: chat_messages_channel_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX chat_messages_channel_idx ON public.chat_messages USING btree (channel, ts_epoch DESC);


--
-- Name: chat_messages_user_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX chat_messages_user_idx ON public.chat_messages USING btree (user_id, channel, ts_epoch DESC);


--
-- Name: employee_profiles_department_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX employee_profiles_department_idx ON public.employee_profiles USING btree (department);


--
-- Name: employee_profiles_email_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX employee_profiles_email_idx ON public.employee_profiles USING btree (email);


--
-- Name: employee_profiles_status_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX employee_profiles_status_idx ON public.employee_profiles USING btree (employment_status);


--
-- Name: employee_profiles_user_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX employee_profiles_user_idx ON public.employee_profiles USING btree (user_id);


--
-- Name: employee_publications_employee_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX employee_publications_employee_idx ON public.employee_publications USING btree (employee_id);


--
-- Name: exhibition_events_exhibition_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX exhibition_events_exhibition_idx ON public.exhibition_events USING btree (exhibition_id);


--
-- Name: exhibition_items_exhibition_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX exhibition_items_exhibition_idx ON public.exhibition_items USING btree (exhibition_id);


--
-- Name: exhibitions_dates_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX exhibitions_dates_idx ON public.exhibitions USING btree (start_date, end_date);


--
-- Name: exhibitions_status_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX exhibitions_status_idx ON public.exhibitions USING btree (status);


--
-- Name: exhibitions_type_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX exhibitions_type_idx ON public.exhibitions USING btree (exhibition_type);


--
-- Name: heritage_category_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX heritage_category_idx ON public.heritage_items USING btree (category);


--
-- Name: heritage_name_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX heritage_name_idx ON public.heritage_items USING btree (item_name);


--
-- Name: heritage_protection_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX heritage_protection_idx ON public.heritage_items USING btree (protection_status);


--
-- Name: heritage_registry_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX heritage_registry_idx ON public.heritage_items USING btree (registry_number);


--
-- Name: heritage_significance_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX heritage_significance_idx ON public.heritage_items USING btree (significance_level);


--
-- Name: heritage_type_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX heritage_type_idx ON public.heritage_items USING btree (heritage_type);


--
-- Name: idx_approval_signatures_approver; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_approval_signatures_approver ON public.approval_signatures USING btree (approver_email);


--
-- Name: idx_approval_signatures_decision; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_approval_signatures_decision ON public.approval_signatures USING btree (decision);


--
-- Name: idx_approval_signatures_request; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_approval_signatures_request ON public.approval_signatures USING btree (request_id);


--
-- Name: idx_archive_requests_archive_year; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_archive_requests_archive_year ON public.archive_requests USING btree (archive_year);


--
-- Name: idx_archive_requests_created_at; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_archive_requests_created_at ON public.archive_requests USING btree (created_at);


--
-- Name: idx_archive_requests_created_by; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_archive_requests_created_by ON public.archive_requests USING btree (created_by_email);


--
-- Name: idx_archive_requests_created_by_department; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_archive_requests_created_by_department ON public.archive_requests USING btree (created_by_department);


--
-- Name: idx_archive_requests_created_by_email; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_archive_requests_created_by_email ON public.archive_requests USING btree (created_by_email);


--
-- Name: idx_archive_requests_status; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_archive_requests_status ON public.archive_requests USING btree (status);


--
-- Name: idx_archive_requests_subtype; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_archive_requests_subtype ON public.archive_requests USING btree (subtype);


--
-- Name: idx_archive_requests_type; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_archive_requests_type ON public.archive_requests USING btree (request_type);


--
-- Name: idx_archive_requests_type_status; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_archive_requests_type_status ON public.archive_requests USING btree (request_type, status);


--
-- Name: idx_audit_log_action; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_audit_log_action ON public.timesheet_audit_log USING btree (action);


--
-- Name: idx_audit_log_changed_at; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_audit_log_changed_at ON public.timesheet_audit_log USING btree (changed_at DESC);


--
-- Name: idx_audit_log_changed_by; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_audit_log_changed_by ON public.timesheet_audit_log USING btree (changed_by);


--
-- Name: idx_audit_log_performed_at; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_audit_log_performed_at ON public.audit_log USING btree (performed_at DESC);


--
-- Name: idx_audit_log_report; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_audit_log_report ON public.timesheet_audit_log USING btree (report_id);


--
-- Name: idx_audit_log_report_time; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_audit_log_report_time ON public.timesheet_audit_log USING btree (report_id, changed_at DESC);


--
-- Name: idx_audit_log_table_record; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_audit_log_table_record ON public.audit_log USING btree (table_name, record_id);


--
-- Name: idx_audit_outbox_unflushed; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_audit_outbox_unflushed ON public.audit_outbox USING btree (id) WHERE (flushed_at IS NULL);


--
-- Name: idx_doc_signatures_created; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_doc_signatures_created ON public.document_signatures USING btree (created_at);


--
-- Name: idx_doc_signatures_requester; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_doc_signatures_requester ON public.document_signatures USING btree (requester_email);


--
-- Name: idx_doc_signatures_status; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_doc_signatures_status ON public.document_signatures USING btree (status);


--
-- Name: idx_doc_signatures_type; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_doc_signatures_type ON public.document_signatures USING btree (document_type);


--
-- Name: idx_document_audit_log_document_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_document_audit_log_document_id ON public.document_audit_log USING btree (document_id);


--
-- Name: idx_document_versions_document_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_document_versions_document_id ON public.document_versions USING btree (document_id);


--
-- Name: idx_document_versions_status; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_document_versions_status ON public.document_versions USING btree (status);


--
-- Name: idx_documents_category; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_documents_category ON public.documents USING btree (category);


--
-- Name: idx_edit_requests_report; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_edit_requests_report ON public.timesheet_edit_requests USING btree (report_id);


--
-- Name: idx_edit_requests_requester; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_edit_requests_requester ON public.timesheet_edit_requests USING btree (requester_email);


--
-- Name: idx_edit_requests_status; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_edit_requests_status ON public.timesheet_edit_requests USING btree (status);


--
-- Name: idx_exhibitions_created_by; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_exhibitions_created_by ON public.exhibitions USING btree (created_by_email);


--
-- Name: idx_foto_poslovi_red; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_foto_poslovi_red ON public.foto_poslovi USING btree (status, sledeci_pokusaj_at);


--
-- Name: idx_foto_veza_izlozba_exhibition_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_foto_veza_izlozba_exhibition_id ON public.foto_veza_izlozba USING btree (exhibition_id);


--
-- Name: idx_foto_veza_kr_dosije; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_foto_veza_kr_dosije ON public.foto_veza_kr_dosije USING btree (dosije_id);


--
-- Name: idx_foto_veza_kr_foto; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_foto_veza_kr_foto ON public.foto_veza_kr_dosije USING btree (fotografija_id);


--
-- Name: idx_foto_veza_predmet_meta; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_foto_veza_predmet_meta ON public.foto_veza_predmet USING btree (database_name, inventarni_broj);


--
-- Name: idx_foto_veza_predmet_mineral_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_foto_veza_predmet_mineral_id ON public.foto_veza_predmet USING btree (mineral_id) WHERE (mineral_id IS NOT NULL);


--
-- Name: idx_foto_veza_projekat_projekat_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_foto_veza_projekat_projekat_id ON public.foto_veza_projekat USING btree (projekat_id);


--
-- Name: idx_foto_veza_teren_teren_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_foto_veza_teren_teren_id ON public.foto_veza_teren USING btree (teren_id);


--
-- Name: idx_fotografija_tagovi_tag; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_fotografija_tagovi_tag ON public.fotografija_tagovi USING btree (lower(tag));


--
-- Name: idx_fotografije_autor_email; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_fotografije_autor_email ON public.fotografije USING btree (autor_email);


--
-- Name: idx_fotografije_datum_snimanja; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_fotografije_datum_snimanja ON public.fotografije USING btree (datum_snimanja);


--
-- Name: idx_fotografije_prijemni_red; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_fotografije_prijemni_red ON public.fotografije USING btree (u_prijemnom_redu) WHERE u_prijemnom_redu;


--
-- Name: idx_fotografije_sklonjena_sa_reda; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_fotografije_sklonjena_sa_reda ON public.fotografije USING btree (sklonjena_sa_reda) WHERE (sklonjena_sa_reda = false);


--
-- Name: idx_fotografije_status; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_fotografije_status ON public.fotografije USING btree (status);


--
-- Name: idx_fotografije_vidljivost; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_fotografije_vidljivost ON public.fotografije USING btree (vidljivost);


--
-- Name: idx_fototeka_uvoz_stavka_run; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_fototeka_uvoz_stavka_run ON public.fototeka_uvoz_stavka USING btree (run_id);


--
-- Name: idx_geo_field_data_coords; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_geo_field_data_coords ON public.geo_field_data USING btree (latitude, longitude);


--
-- Name: idx_geo_field_data_user; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_geo_field_data_user ON public.geo_field_data USING btree (created_by);


--
-- Name: idx_images_created_at; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_images_created_at ON public.images USING btree (created_at);


--
-- Name: idx_images_database_entity; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_images_database_entity ON public.images USING btree (database_name, entity_type, entity_id);


--
-- Name: idx_images_database_name; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_images_database_name ON public.images USING btree (database_name);


--
-- Name: idx_images_entity_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_images_entity_id ON public.images USING btree (entity_id);


--
-- Name: idx_inventory_entries_in_printed_book; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_inventory_entries_in_printed_book ON public.inventory_entries USING btree (in_printed_book);


--
-- Name: idx_kenozojske_inv_familija; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_kenozojske_inv_familija ON public.bilja_kenozojske_invertebrate USING btree (familija);


--
-- Name: idx_kenozojske_inv_inv_broj; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_kenozojske_inv_inv_broj ON public.bilja_kenozojske_invertebrate USING btree (inventarski_broj);


--
-- Name: idx_kenozojske_inv_klasa; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_kenozojske_inv_klasa ON public.bilja_kenozojske_invertebrate USING btree (klasa);


--
-- Name: idx_kenozojske_inv_lokalitet; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_kenozojske_inv_lokalitet ON public.bilja_kenozojske_invertebrate USING btree (lokalitet);


--
-- Name: idx_kenozojske_inv_stratigrafija; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_kenozojske_inv_stratigrafija ON public.bilja_kenozojske_invertebrate USING btree (stratigrafski_nivo);


--
-- Name: idx_kenozojske_inv_vrsta_search; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_kenozojske_inv_vrsta_search ON public.bilja_kenozojske_invertebrate USING gin (to_tsvector('simple'::regconfig, COALESCE(vrsta, ''::text)));


--
-- Name: idx_kr_dosije_kolektorski; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_kr_dosije_kolektorski ON public.kr_dosije USING btree (kolektorski_broj);


--
-- Name: idx_kr_dosije_odeljenje; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_kr_dosije_odeljenje ON public.kr_dosije USING btree (odeljenje);


--
-- Name: idx_kr_dosije_predmet; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_kr_dosije_predmet ON public.kr_dosije USING btree (database_name, inventarni_broj);


--
-- Name: idx_kr_izvrsilac_dosije; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_kr_izvrsilac_dosije ON public.kr_dosije_izvrsilac USING btree (dosije_id);


--
-- Name: idx_kr_izvrsilac_email; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_kr_izvrsilac_email ON public.kr_dosije_izvrsilac USING btree (user_email);


--
-- Name: idx_kr_predlozak_izbor; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_kr_predlozak_izbor ON public.kr_predlozak USING btree (odeljenje, vrsta);


--
-- Name: idx_localities_name; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_localities_name ON public.localities USING btree (name);


--
-- Name: idx_mineral_rruff_matches_mineral_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_mineral_rruff_matches_mineral_id ON public.mineral_rruff_matches USING btree (mineral_id);


--
-- Name: idx_mineral_rruff_matches_rruff_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_mineral_rruff_matches_rruff_id ON public.mineral_rruff_matches USING btree (rruff_id);


--
-- Name: idx_minerals_physical_presence_confirmed; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_minerals_physical_presence_confirmed ON public.minerals USING btree (physical_presence_confirmed);


--
-- Name: idx_morski_familija; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_morski_familija ON public.bilja_recentni_morski_mekusci USING btree (familija);


--
-- Name: idx_morski_inv_broj; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_morski_inv_broj ON public.bilja_recentni_morski_mekusci USING btree (inventarski_broj);


--
-- Name: idx_morski_klasa; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_morski_klasa ON public.bilja_recentni_morski_mekusci USING btree (klasa);


--
-- Name: idx_morski_lokalitet; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_morski_lokalitet ON public.bilja_recentni_morski_mekusci USING btree (lokalitet);


--
-- Name: idx_news_category; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_news_category ON public.news_articles USING btree (category);


--
-- Name: idx_news_curator; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_news_curator ON public.news_articles USING btree (curator);


--
-- Name: idx_news_description_search; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_news_description_search ON public.news_articles USING gin (to_tsvector('simple'::regconfig, description));


--
-- Name: idx_news_start_date; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_news_start_date ON public.news_articles USING btree (start_date);


--
-- Name: idx_news_status; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_news_status ON public.news_articles USING btree (status);


--
-- Name: idx_news_title_search; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_news_title_search ON public.news_articles USING gin (to_tsvector('simple'::regconfig, title));


--
-- Name: idx_news_type; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_news_type ON public.news_articles USING btree (type);


--
-- Name: idx_notifications_unread; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_notifications_unread ON public.user_notifications USING btree (user_email, is_read) WHERE (is_read = false);


--
-- Name: idx_notifications_user_email; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_notifications_user_email ON public.user_notifications USING btree (user_email);


--
-- Name: idx_opsta_moll_familija; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_opsta_moll_familija ON public.bilja_opsta_zbirka_mollusca USING btree (familija);


--
-- Name: idx_opsta_moll_inv_broj; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_opsta_moll_inv_broj ON public.bilja_opsta_zbirka_mollusca USING btree (inventarski_broj);


--
-- Name: idx_opsta_moll_klasa; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_opsta_moll_klasa ON public.bilja_opsta_zbirka_mollusca USING btree (klasa);


--
-- Name: idx_opsta_moll_lokalitet; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_opsta_moll_lokalitet ON public.bilja_opsta_zbirka_mollusca USING btree (lokalitet);


--
-- Name: idx_pavlovic_familija; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_pavlovic_familija ON public.bilja_suvozemni_puzevi_pavlovic USING btree (familija);


--
-- Name: idx_pavlovic_inv_broj; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_pavlovic_inv_broj ON public.bilja_suvozemni_puzevi_pavlovic USING btree (inventarski_broj);


--
-- Name: idx_pavlovic_lokalitet; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_pavlovic_lokalitet ON public.bilja_suvozemni_puzevi_pavlovic USING btree (lokalitet);


--
-- Name: idx_pavlovic_rod; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_pavlovic_rod ON public.bilja_suvozemni_puzevi_pavlovic USING btree (rod);


--
-- Name: idx_pavlovic_vrsta_search; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_pavlovic_vrsta_search ON public.bilja_suvozemni_puzevi_pavlovic USING gin (to_tsvector('simple'::regconfig, COALESCE(vrsta, ''::text)));


--
-- Name: idx_procurement_requests_archive_request_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_procurement_requests_archive_request_id ON public.procurement_requests USING btree (archive_request_id);


--
-- Name: idx_radoman_familija; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_radoman_familija ON public.bilja_hydrobioidea_radoman USING btree (familija);


--
-- Name: idx_radoman_holotip; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_radoman_holotip ON public.bilja_hydrobioidea_radoman USING btree (holotip) WHERE (holotip IS NOT NULL);


--
-- Name: idx_radoman_inv_broj; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_radoman_inv_broj ON public.bilja_hydrobioidea_radoman USING btree (inventarski_broj);


--
-- Name: idx_radoman_lokalitet; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_radoman_lokalitet ON public.bilja_hydrobioidea_radoman USING btree (lokalitet);


--
-- Name: idx_radoman_rod; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_radoman_rod ON public.bilja_hydrobioidea_radoman USING btree (rod);


--
-- Name: idx_request_comments_request; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_request_comments_request ON public.request_comments USING btree (request_id);


--
-- Name: idx_request_history_request; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_request_history_request ON public.request_history USING btree (request_id);


--
-- Name: idx_research_projects_start_date; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_research_projects_start_date ON public.research_projects USING btree (start_date);


--
-- Name: idx_reservations_dates; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_reservations_dates ON public.vehicle_reservations USING btree (start_date, end_date);


--
-- Name: idx_reservations_reserved_by; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_reservations_reserved_by ON public.vehicle_reservations USING btree (reserved_by);


--
-- Name: idx_reservations_status; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_reservations_status ON public.vehicle_reservations USING btree (status);


--
-- Name: idx_reservations_vehicle; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_reservations_vehicle ON public.vehicle_reservations USING btree (vehicle_id);


--
-- Name: idx_rruff_chemistry_rruff_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_rruff_chemistry_rruff_id ON public.rruff_chemistry USING btree (rruff_id);


--
-- Name: idx_rruff_localities_rruff_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_rruff_localities_rruff_id ON public.rruff_localities USING btree (rruff_id);


--
-- Name: idx_rruff_minerals_crystal_system; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_rruff_minerals_crystal_system ON public.rruff_minerals USING btree (crystal_system);


--
-- Name: idx_rruff_minerals_ima_status; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_rruff_minerals_ima_status ON public.rruff_minerals USING btree (ima_status);


--
-- Name: idx_rruff_minerals_name; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_rruff_minerals_name ON public.rruff_minerals USING btree (name);


--
-- Name: idx_rruff_minerals_name_fts; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_rruff_minerals_name_fts ON public.rruff_minerals USING gin (to_tsvector('english'::regconfig, ((name || ' '::text) || COALESCE(name_plain, ''::text))));


--
-- Name: idx_rruff_minerals_name_plain; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_rruff_minerals_name_plain ON public.rruff_minerals USING btree (name_plain);


--
-- Name: idx_rruff_references_rruff_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_rruff_references_rruff_id ON public.rruff_references USING btree (rruff_id);


--
-- Name: idx_signature_audit_doc; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_signature_audit_doc ON public.signature_audit_log USING btree (document_signature_id);


--
-- Name: idx_specimens_catalog_number; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_specimens_catalog_number ON public.collection_specimens USING btree (catalog_number);


--
-- Name: idx_specimens_collection_type; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_specimens_collection_type ON public.collection_specimens USING btree (collection_type);


--
-- Name: idx_specimens_collector; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_specimens_collector ON public.collection_specimens USING btree (collector);


--
-- Name: idx_specimens_common_search; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_specimens_common_search ON public.collection_specimens USING gin (to_tsvector('simple'::regconfig, common_name_sr));


--
-- Name: idx_specimens_coordinates; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_specimens_coordinates ON public.collection_specimens USING gist (coordinates);


--
-- Name: idx_specimens_description_search; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_specimens_description_search ON public.collection_specimens USING gin (to_tsvector('simple'::regconfig, description));


--
-- Name: idx_specimens_family; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_specimens_family ON public.collection_specimens USING btree (family);


--
-- Name: idx_specimens_scientific_name; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_specimens_scientific_name ON public.collection_specimens USING btree (scientific_name);


--
-- Name: idx_specimens_scientific_search; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_specimens_scientific_search ON public.collection_specimens USING gin (to_tsvector('simple'::regconfig, scientific_name));


--
-- Name: idx_specimens_status; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_specimens_status ON public.collection_specimens USING btree (status);


--
-- Name: idx_tadic_familija; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_tadic_familija ON public.bilja_skoljke_tadic USING btree (familija);


--
-- Name: idx_tadic_inv_broj; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_tadic_inv_broj ON public.bilja_skoljke_tadic USING btree (inventarski_broj);


--
-- Name: idx_tadic_lokalitet; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_tadic_lokalitet ON public.bilja_skoljke_tadic USING btree (lokalitet);


--
-- Name: idx_tadic_vrsta; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_tadic_vrsta ON public.bilja_skoljke_tadic USING btree (vrsta);


--
-- Name: idx_timesheet_entries_category; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_timesheet_entries_category ON public.timesheet_entries USING btree (category);


--
-- Name: idx_timesheet_entries_report; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_timesheet_entries_report ON public.timesheet_entries USING btree (report_id);


--
-- Name: idx_timesheet_entries_report_category; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_timesheet_entries_report_category ON public.timesheet_entries USING btree (report_id, category);


--
-- Name: idx_timesheet_report_days_day; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_timesheet_report_days_day ON public.timesheet_report_days USING btree (report_id, day);


--
-- Name: idx_timesheet_report_days_report; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_timesheet_report_days_report ON public.timesheet_report_days USING btree (report_id);


--
-- Name: idx_timesheet_reports_email; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_timesheet_reports_email ON public.timesheet_reports USING btree (employee_email);


--
-- Name: idx_timesheet_reports_employee; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_timesheet_reports_employee ON public.timesheet_reports USING btree (employee_name);


--
-- Name: idx_timesheet_reports_employee_period; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_timesheet_reports_employee_period ON public.timesheet_reports USING btree (employee_email, year, month);


--
-- Name: idx_timesheet_reports_legacy; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_timesheet_reports_legacy ON public.timesheet_reports USING btree (legacy_radna_lista_id);


--
-- Name: idx_timesheet_reports_locked; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_timesheet_reports_locked ON public.timesheet_reports USING btree (is_locked);


--
-- Name: idx_timesheet_reports_period; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_timesheet_reports_period ON public.timesheet_reports USING btree (year, month);


--
-- Name: idx_timesheet_reports_period_desc; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_timesheet_reports_period_desc ON public.timesheet_reports USING btree (year DESC, month DESC);


--
-- Name: idx_timesheet_reports_status; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_timesheet_reports_status ON public.timesheet_reports USING btree (status);


--
-- Name: idx_timesheet_reports_verified; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_timesheet_reports_verified ON public.timesheet_reports USING btree (is_verified);


--
-- Name: idx_timesheet_reports_verified_by; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_timesheet_reports_verified_by ON public.timesheet_reports USING btree (verified_by);


--
-- Name: idx_timesheet_status_history_report_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_timesheet_status_history_report_id ON public.timesheet_status_history USING btree (report_id);


--
-- Name: idx_vehicle_reservations_requester; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_vehicle_reservations_requester ON public.vehicle_reservations USING btree (lower(requester_email), starts_at);


--
-- Name: idx_vehicle_reservations_vehicle_time; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_vehicle_reservations_vehicle_time ON public.vehicle_reservations USING btree (vehicle_id, starts_at, ends_at);


--
-- Name: idx_vehicles_registration; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_vehicles_registration ON public.vehicles USING btree (registration);


--
-- Name: idx_vehicles_status; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_vehicles_status ON public.vehicles USING btree (status);


--
-- Name: idx_vehicles_type; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_vehicles_type ON public.vehicles USING btree (type);


--
-- Name: idx_visitor_records_visit_date; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_visitor_records_visit_date ON public.visitor_records USING btree (visit_date);


--
-- Name: ix_digitized_profiles_digitized_by; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_digitized_profiles_digitized_by ON public.digitized_profiles USING btree (digitized_by);


--
-- Name: ix_sanja_location_found; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_sanja_location_found ON public.sanja_paleogene_neogene_mammals USING btree (((specimen ->> 'location_found'::text)));


--
-- Name: ix_sanja_specimen_name; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_sanja_specimen_name ON public.sanja_paleogene_neogene_mammals USING btree (((specimen ->> 'specimen_name'::text)));


--
-- Name: ix_science_news_datum; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_science_news_datum ON public.science_news USING btree (datum DESC);


--
-- Name: ix_user_custom_themes_email; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_user_custom_themes_email ON public.user_custom_themes USING btree (lower((user_email)::text));


--
-- Name: library_books_author_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX library_books_author_idx ON public.library_books USING btree (author);


--
-- Name: library_books_category_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX library_books_category_idx ON public.library_books USING btree (category);


--
-- Name: library_books_isbn_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX library_books_isbn_idx ON public.library_books USING btree (isbn);


--
-- Name: library_books_status_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX library_books_status_idx ON public.library_books USING btree (status);


--
-- Name: library_books_title_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX library_books_title_idx ON public.library_books USING btree (title);


--
-- Name: library_loans_book_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX library_loans_book_idx ON public.library_loans USING btree (book_id);


--
-- Name: library_loans_status_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX library_loans_status_idx ON public.library_loans USING btree (status);


--
-- Name: mail_cache_messages_date_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX mail_cache_messages_date_idx ON public.mail_cache_messages USING btree (user_email, folder, date_iso DESC, uid DESC);


--
-- Name: mail_cache_messages_folder_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX mail_cache_messages_folder_idx ON public.mail_cache_messages USING btree (user_email, folder, uid DESC);


--
-- Name: mail_cache_messages_read_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX mail_cache_messages_read_idx ON public.mail_cache_messages USING btree (user_email, folder, is_read, uid DESC);


--
-- Name: mail_cache_messages_sender_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX mail_cache_messages_sender_idx ON public.mail_cache_messages USING btree (user_email, folder, lower(from_name), uid DESC);


--
-- Name: mail_cache_messages_sort_date_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX mail_cache_messages_sort_date_idx ON public.mail_cache_messages USING btree (user_email, folder, sort_date_iso DESC, uid DESC);


--
-- Name: mail_cache_messages_subject_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX mail_cache_messages_subject_idx ON public.mail_cache_messages USING btree (user_email, folder, lower(subject), uid DESC);


--
-- Name: meteorite_bulletin_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX meteorite_bulletin_idx ON public.meteorite_specimens USING btree (meteorite_bulletin_number);


--
-- Name: meteorite_catalog_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX meteorite_catalog_idx ON public.meteorite_specimens USING btree (catalog_number);


--
-- Name: meteorite_class_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX meteorite_class_idx ON public.meteorite_specimens USING btree (meteorite_class);


--
-- Name: meteorite_coords_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX meteorite_coords_idx ON public.meteorite_specimens USING gist (fall_coordinates);


--
-- Name: meteorite_name_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX meteorite_name_idx ON public.meteorite_specimens USING btree (specimen_name);


--
-- Name: meteorite_serbian_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX meteorite_serbian_idx ON public.meteorite_specimens USING btree (serbian_meteorite) WHERE (serbian_meteorite = true);


--
-- Name: paper_feature_links_paper_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX paper_feature_links_paper_idx ON public.paper_feature_links USING btree (paper_id);


--
-- Name: paper_feature_links_type_name_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX paper_feature_links_type_name_idx ON public.paper_feature_links USING btree (feature_type, feature_name);


--
-- Name: paper_locality_links_locality_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX paper_locality_links_locality_idx ON public.paper_locality_links USING btree (locality_name);


--
-- Name: paper_locality_links_ogk_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX paper_locality_links_ogk_idx ON public.paper_locality_links USING btree (ogk_code);


--
-- Name: paper_locality_links_paper_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX paper_locality_links_paper_idx ON public.paper_locality_links USING btree (paper_id);


--
-- Name: scientific_papers_citations_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX scientific_papers_citations_idx ON public.scientific_papers USING btree (cited_by_count DESC);


--
-- Name: scientific_papers_doi_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX scientific_papers_doi_idx ON public.scientific_papers USING btree (doi);


--
-- Name: scientific_papers_journal_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX scientific_papers_journal_idx ON public.scientific_papers USING btree (journal_name);


--
-- Name: scientific_papers_language_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX scientific_papers_language_idx ON public.scientific_papers USING btree (language);


--
-- Name: scientific_papers_oa_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX scientific_papers_oa_idx ON public.scientific_papers USING btree (is_open_access);


--
-- Name: scientific_papers_search_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX scientific_papers_search_idx ON public.scientific_papers USING gin (to_tsvector('simple'::regconfig, ((((((COALESCE(title, ''::text) || ' '::text) || COALESCE(abstract, ''::text)) || ' '::text) || COALESCE(authors_json, ''::text)) || ' '::text) || COALESCE(keywords_json, ''::text))));


--
-- Name: scientific_papers_year_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX scientific_papers_year_idx ON public.scientific_papers USING btree (publication_year);


--
-- Name: timesheet_report_days_report_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX timesheet_report_days_report_idx ON public.timesheet_report_days USING btree (report_id);


--
-- Name: timesheet_reports_employee_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX timesheet_reports_employee_idx ON public.timesheet_reports USING btree (employee_name);


--
-- Name: timesheet_reports_legacy_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX timesheet_reports_legacy_idx ON public.timesheet_reports USING btree (legacy_radna_lista_id);


--
-- Name: timesheet_reports_period_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX timesheet_reports_period_idx ON public.timesheet_reports USING btree (year, month);


--
-- Name: uq_fototeka_intake_pending_raw; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX uq_fototeka_intake_pending_raw ON public.fototeka_intake_pending USING btree (raw_putanja);


--
-- Name: uq_timesheet_reports_email_month_year; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX uq_timesheet_reports_email_month_year ON public.timesheet_reports USING btree (lower((employee_email)::text), month, year) WHERE (employee_email IS NOT NULL);


--
-- Name: uq_timesheet_reports_name_month_year; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX uq_timesheet_reports_name_month_year ON public.timesheet_reports USING btree (employee_name, month, year) WHERE (employee_email IS NULL);


--
-- Name: timesheet_report_days timesheet_report_days_sync_delete; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER timesheet_report_days_sync_delete AFTER DELETE ON public.timesheet_report_days REFERENCING OLD TABLE AS old_table FOR EACH STATEMENT EXECUTE FUNCTION public.trigger_sync_timesheet_entries_statement();


--
-- Name: timesheet_report_days timesheet_report_days_sync_insert; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER timesheet_report_days_sync_insert AFTER INSERT ON public.timesheet_report_days REFERENCING NEW TABLE AS new_table FOR EACH STATEMENT EXECUTE FUNCTION public.trigger_sync_timesheet_entries_statement();


--
-- Name: timesheet_report_days timesheet_report_days_sync_update; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER timesheet_report_days_sync_update AFTER UPDATE ON public.timesheet_report_days REFERENCING OLD TABLE AS old_table NEW TABLE AS new_table FOR EACH STATEMENT EXECUTE FUNCTION public.trigger_sync_timesheet_entries_statement();


--
-- Name: timesheet_reports timesheet_reports_audit; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER timesheet_reports_audit AFTER INSERT OR DELETE OR UPDATE ON public.timesheet_reports FOR EACH ROW EXECUTE FUNCTION public.timesheet_audit_trigger();


--
-- Name: timesheet_reports timesheet_reports_version_update; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER timesheet_reports_version_update BEFORE UPDATE ON public.timesheet_reports FOR EACH ROW EXECUTE FUNCTION public.timesheet_reports_version_trigger();


--
-- Name: approval_signatures approval_signatures_request_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.approval_signatures
    ADD CONSTRAINT approval_signatures_request_id_fkey FOREIGN KEY (request_id) REFERENCES public.archive_requests(id) ON DELETE CASCADE;


--
-- Name: audit_log audit_log_performed_by_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.audit_log
    ADD CONSTRAINT audit_log_performed_by_fkey FOREIGN KEY (performed_by) REFERENCES public.users(id);


--
-- Name: bird_ringing_records bird_ringing_records_species_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.bird_ringing_records
    ADD CONSTRAINT bird_ringing_records_species_id_fkey FOREIGN KEY (species_id) REFERENCES public.bird_species(id);


--
-- Name: collection_specimens collection_specimens_collection_type_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.collection_specimens
    ADD CONSTRAINT collection_specimens_collection_type_fkey FOREIGN KEY (collection_type) REFERENCES public.collection_types(code);


--
-- Name: document_audit_log document_audit_log_document_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.document_audit_log
    ADD CONSTRAINT document_audit_log_document_id_fkey FOREIGN KEY (document_id) REFERENCES public.documents(id) ON DELETE CASCADE;


--
-- Name: document_audit_log document_audit_log_version_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.document_audit_log
    ADD CONSTRAINT document_audit_log_version_id_fkey FOREIGN KEY (version_id) REFERENCES public.document_versions(id) ON DELETE SET NULL;


--
-- Name: document_versions document_versions_document_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.document_versions
    ADD CONSTRAINT document_versions_document_id_fkey FOREIGN KEY (document_id) REFERENCES public.documents(id) ON DELETE CASCADE;


--
-- Name: employee_profiles employee_profiles_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.employee_profiles
    ADD CONSTRAINT employee_profiles_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- Name: employee_publications employee_publications_employee_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.employee_publications
    ADD CONSTRAINT employee_publications_employee_id_fkey FOREIGN KEY (employee_id) REFERENCES public.employee_profiles(id) ON DELETE CASCADE;


--
-- Name: exhibition_events exhibition_events_exhibition_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.exhibition_events
    ADD CONSTRAINT exhibition_events_exhibition_id_fkey FOREIGN KEY (exhibition_id) REFERENCES public.exhibitions(id) ON DELETE CASCADE;


--
-- Name: exhibition_items exhibition_items_exhibition_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.exhibition_items
    ADD CONSTRAINT exhibition_items_exhibition_id_fkey FOREIGN KEY (exhibition_id) REFERENCES public.exhibitions(id) ON DELETE CASCADE;


--
-- Name: foto_veza_predmet fk_foto_veza_predmet_mineral; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.foto_veza_predmet
    ADD CONSTRAINT fk_foto_veza_predmet_mineral FOREIGN KEY (mineral_id) REFERENCES public.minerals(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: foto_poslovi foto_poslovi_fotografija_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.foto_poslovi
    ADD CONSTRAINT foto_poslovi_fotografija_id_fkey FOREIGN KEY (fotografija_id) REFERENCES public.fotografije(id) ON DELETE CASCADE;


--
-- Name: foto_veza_izlozba foto_veza_izlozba_exhibition_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.foto_veza_izlozba
    ADD CONSTRAINT foto_veza_izlozba_exhibition_id_fkey FOREIGN KEY (exhibition_id) REFERENCES public.exhibitions(id) ON DELETE CASCADE;


--
-- Name: foto_veza_izlozba foto_veza_izlozba_fotografija_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.foto_veza_izlozba
    ADD CONSTRAINT foto_veza_izlozba_fotografija_id_fkey FOREIGN KEY (fotografija_id) REFERENCES public.fotografije(id) ON DELETE CASCADE;


--
-- Name: foto_veza_kr_dosije foto_veza_kr_dosije_dosije_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.foto_veza_kr_dosije
    ADD CONSTRAINT foto_veza_kr_dosije_dosije_id_fkey FOREIGN KEY (dosije_id) REFERENCES public.kr_dosije(id) ON DELETE CASCADE;


--
-- Name: foto_veza_kr_dosije foto_veza_kr_dosije_fotografija_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.foto_veza_kr_dosije
    ADD CONSTRAINT foto_veza_kr_dosije_fotografija_id_fkey FOREIGN KEY (fotografija_id) REFERENCES public.fotografije(id) ON DELETE CASCADE;


--
-- Name: foto_veza_predmet foto_veza_predmet_fotografija_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.foto_veza_predmet
    ADD CONSTRAINT foto_veza_predmet_fotografija_id_fkey FOREIGN KEY (fotografija_id) REFERENCES public.fotografije(id) ON DELETE CASCADE;


--
-- Name: foto_veza_projekat foto_veza_projekat_fotografija_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.foto_veza_projekat
    ADD CONSTRAINT foto_veza_projekat_fotografija_id_fkey FOREIGN KEY (fotografija_id) REFERENCES public.fotografije(id) ON DELETE CASCADE;


--
-- Name: foto_veza_projekat foto_veza_projekat_projekat_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.foto_veza_projekat
    ADD CONSTRAINT foto_veza_projekat_projekat_id_fkey FOREIGN KEY (projekat_id) REFERENCES public.fototeka_projekti(id) ON DELETE CASCADE;


--
-- Name: foto_veza_teren foto_veza_teren_fotografija_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.foto_veza_teren
    ADD CONSTRAINT foto_veza_teren_fotografija_id_fkey FOREIGN KEY (fotografija_id) REFERENCES public.fotografije(id) ON DELETE CASCADE;


--
-- Name: foto_veza_teren foto_veza_teren_teren_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.foto_veza_teren
    ADD CONSTRAINT foto_veza_teren_teren_id_fkey FOREIGN KEY (teren_id) REFERENCES public.fototeka_tereni(id) ON DELETE CASCADE;


--
-- Name: fotografija_tagovi fotografija_tagovi_fotografija_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.fotografija_tagovi
    ADD CONSTRAINT fotografija_tagovi_fotografija_id_fkey FOREIGN KEY (fotografija_id) REFERENCES public.fotografije(id) ON DELETE CASCADE;


--
-- Name: fototeka_uvoz_stavka fototeka_uvoz_stavka_fotografija_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.fototeka_uvoz_stavka
    ADD CONSTRAINT fototeka_uvoz_stavka_fotografija_id_fkey FOREIGN KEY (fotografija_id) REFERENCES public.fotografije(id) ON DELETE SET NULL;


--
-- Name: fototeka_uvoz_stavka fototeka_uvoz_stavka_run_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.fototeka_uvoz_stavka
    ADD CONSTRAINT fototeka_uvoz_stavka_run_id_fkey FOREIGN KEY (run_id) REFERENCES public.fototeka_uvoz_run(id) ON DELETE CASCADE;


--
-- Name: kr_dosije_izvrsilac kr_dosije_izvrsilac_dosije_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.kr_dosije_izvrsilac
    ADD CONSTRAINT kr_dosije_izvrsilac_dosije_id_fkey FOREIGN KEY (dosije_id) REFERENCES public.kr_dosije(id) ON DELETE CASCADE;


--
-- Name: library_loans library_loans_book_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.library_loans
    ADD CONSTRAINT library_loans_book_id_fkey FOREIGN KEY (book_id) REFERENCES public.library_books(id) ON DELETE CASCADE;


--
-- Name: mineral_rruff_matches mineral_rruff_matches_mineral_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.mineral_rruff_matches
    ADD CONSTRAINT mineral_rruff_matches_mineral_id_fkey FOREIGN KEY (mineral_id) REFERENCES public.minerals(id) ON DELETE CASCADE;


--
-- Name: mineral_rruff_matches mineral_rruff_matches_rruff_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.mineral_rruff_matches
    ADD CONSTRAINT mineral_rruff_matches_rruff_id_fkey FOREIGN KEY (rruff_id) REFERENCES public.rruff_minerals(rruff_id) ON DELETE CASCADE;


--
-- Name: paper_feature_links paper_feature_links_paper_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.paper_feature_links
    ADD CONSTRAINT paper_feature_links_paper_id_fkey FOREIGN KEY (paper_id) REFERENCES public.scientific_papers(id) ON DELETE CASCADE;


--
-- Name: paper_locality_links paper_locality_links_paper_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.paper_locality_links
    ADD CONSTRAINT paper_locality_links_paper_id_fkey FOREIGN KEY (paper_id) REFERENCES public.scientific_papers(id) ON DELETE CASCADE;


--
-- Name: procurement_requests procurement_requests_archive_request_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.procurement_requests
    ADD CONSTRAINT procurement_requests_archive_request_id_fkey FOREIGN KEY (archive_request_id) REFERENCES public.archive_requests(id);


--
-- Name: request_comments request_comments_request_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.request_comments
    ADD CONSTRAINT request_comments_request_id_fkey FOREIGN KEY (request_id) REFERENCES public.archive_requests(id) ON DELETE CASCADE;


--
-- Name: request_history request_history_request_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.request_history
    ADD CONSTRAINT request_history_request_id_fkey FOREIGN KEY (request_id) REFERENCES public.archive_requests(id) ON DELETE CASCADE;


--
-- Name: rruff_chemistry rruff_chemistry_rruff_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.rruff_chemistry
    ADD CONSTRAINT rruff_chemistry_rruff_id_fkey FOREIGN KEY (rruff_id) REFERENCES public.rruff_minerals(rruff_id) ON DELETE CASCADE;


--
-- Name: rruff_localities rruff_localities_rruff_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.rruff_localities
    ADD CONSTRAINT rruff_localities_rruff_id_fkey FOREIGN KEY (rruff_id) REFERENCES public.rruff_minerals(rruff_id) ON DELETE CASCADE;


--
-- Name: rruff_references rruff_references_rruff_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.rruff_references
    ADD CONSTRAINT rruff_references_rruff_id_fkey FOREIGN KEY (rruff_id) REFERENCES public.rruff_minerals(rruff_id) ON DELETE CASCADE;


--
-- Name: signature_audit_log signature_audit_log_document_signature_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.signature_audit_log
    ADD CONSTRAINT signature_audit_log_document_signature_id_fkey FOREIGN KEY (document_signature_id) REFERENCES public.document_signatures(id) ON DELETE CASCADE;


--
-- Name: timesheet_edit_requests timesheet_edit_requests_report_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.timesheet_edit_requests
    ADD CONSTRAINT timesheet_edit_requests_report_id_fkey FOREIGN KEY (report_id) REFERENCES public.timesheet_reports(id) ON DELETE CASCADE;


--
-- Name: timesheet_entries timesheet_entries_report_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.timesheet_entries
    ADD CONSTRAINT timesheet_entries_report_id_fkey FOREIGN KEY (report_id) REFERENCES public.timesheet_reports(id) ON DELETE CASCADE;


--
-- Name: timesheet_report_days timesheet_report_days_report_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.timesheet_report_days
    ADD CONSTRAINT timesheet_report_days_report_id_fkey FOREIGN KEY (report_id) REFERENCES public.timesheet_reports(id) ON DELETE CASCADE;


--
-- Name: timesheet_status_history timesheet_status_history_report_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.timesheet_status_history
    ADD CONSTRAINT timesheet_status_history_report_id_fkey FOREIGN KEY (report_id) REFERENCES public.timesheet_reports(id) ON DELETE CASCADE;


--
-- Name: user_activity_log user_activity_log_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.user_activity_log
    ADD CONSTRAINT user_activity_log_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- Name: user_module_permissions user_module_permissions_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.user_module_permissions
    ADD CONSTRAINT user_module_permissions_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- Name: user_sessions user_sessions_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.user_sessions
    ADD CONSTRAINT user_sessions_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- Name: users users_department_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_department_id_fkey FOREIGN KEY (department_id) REFERENCES public.departments(id);


--
-- Name: users users_role_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_role_id_fkey FOREIGN KEY (role_id) REFERENCES public.roles(id);


--
-- Name: vehicle_reservations vehicle_reservations_vehicle_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.vehicle_reservations
    ADD CONSTRAINT vehicle_reservations_vehicle_id_fkey FOREIGN KEY (vehicle_id) REFERENCES public.vehicles(id) ON DELETE CASCADE;


--
-- PostgreSQL database dump complete
--

\unrestrict mqMbdJFOmifNmMWhDlREhkEZunehGu7NsC71I0vQy3HARwU8vZnjf5WvRu6Z5Jw

