-- User: "AirFlowAnalyzer"
-- DROP USER "AirFlowAnalyzer";
CREATE USER "AirFlowAnalyzer" WITH
  LOGIN
  SUPERUSER
  INHERIT
  CREATEDB
  CREATEROLE
  NOREPLICATION;

COMMENT ON ROLE "AirFlowAnalyzer" IS 'AirFlowAnalyzer';

-- Database: AirFlowAnalyzer
-- DROP DATABASE "AirFlowAnalyzer";
CREATE DATABASE "AirFlowAnalyzer"
    WITH 
    OWNER = "AirFlowAnalyzer"
    ENCODING = 'UTF8'
    LC_COLLATE = 'en_GB.UTF-8'
    LC_CTYPE = 'en_GB.UTF-8'
    TABLESPACE = pg_default
    CONNECTION LIMIT = -1;

-- Table: public.session
-- DROP TABLE public.session;
CREATE TABLE public.session
(
    id integer NOT NULL DEFAULT nextval('session_id_seq'::regclass),
    start_session timestamp without time zone NOT NULL,
    stop_session timestamp without time zone NOT NULL,
    name character varying(50) COLLATE pg_catalog."default" NOT NULL,
    comment character varying(100) COLLATE pg_catalog."default",
    CONSTRAINT session_pk PRIMARY KEY (id)
)
WITH (OIDS = TRUE)
TABLESPACE pg_default;

ALTER TABLE public.session OWNER to postgres;

-- Table: public.device
-- DROP TABLE public.device;
CREATE TABLE public.device
(
    id integer NOT NULL DEFAULT nextval('device_id_seq'::regclass),
    name character varying(30) COLLATE pg_catalog."default" NOT NULL,
    address character varying(30) COLLATE pg_catalog."default" NOT NULL,
    serial character varying(30) COLLATE pg_catalog."default" NOT NULL,
    status character varying(30) COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT device_pk PRIMARY KEY (id)
)
WITH (OIDS = TRUE)
TABLESPACE pg_default;

ALTER TABLE public.device OWNER to postgres;

-- Table: public.measurement_dimension
-- DROP TABLE public.measurement_dimension;
CREATE TABLE public.measurement_dimension
(
    id integer NOT NULL DEFAULT nextval('measurement_dimension_id_seq'::regclass),
    name character varying(30) COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT measurement_dimension_pk PRIMARY KEY (id)
)
WITH (OIDS = TRUE)
TABLESPACE pg_default;

ALTER TABLE public.measurement_dimension 

-- Table: public.measurement_variable
-- DROP TABLE public.measurement_variable;
CREATE TABLE public.measurement_variable
(
    id integer NOT NULL DEFAULT nextval('measurement_variable_id_seq'::regclass),
    name character varying(30) COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT measurement_variable_pk PRIMARY KEY (id)
)
WITH (OIDS = TRUE)
TABLESPACE pg_default;

ALTER TABLE public.measurement_variable OWNER to postgres;OWNER to postgres;

-- Table: public.measurement
-- DROP TABLE public.measurement;
CREATE TABLE public.measurement
(
    id integer NOT NULL DEFAULT nextval('measurement_id_seq'::regclass),
    value double precision NOT NULL,
    device_id integer NOT NULL,
    session_id integer NOT NULL,
    measurement_variable_id integer NOT NULL,
    measurement_dimension_id integer NOT NULL,
    "timestamp" timestamp without time zone NOT NULL,
    CONSTRAINT measurement_pk PRIMARY KEY (id),
    CONSTRAINT measurement_dimension_id FOREIGN KEY (measurement_dimension_id)
        REFERENCES public.measurement_dimension (id) MATCH SIMPLE
        ON UPDATE RESTRICT
        ON DELETE RESTRICT,
    CONSTRAINT measurement_variable_id FOREIGN KEY (measurement_variable_id)
        REFERENCES public.measurement_variable (id) MATCH SIMPLE
        ON UPDATE RESTRICT
        ON DELETE RESTRICT,
    CONSTRAINT session_id FOREIGN KEY (session_id)
        REFERENCES public.session (id) MATCH SIMPLE
        ON UPDATE RESTRICT
        ON DELETE RESTRICT
)
WITH (OIDS = TRUE)
TABLESPACE pg_default;

ALTER TABLE public.measurement OWNER to postgres;
