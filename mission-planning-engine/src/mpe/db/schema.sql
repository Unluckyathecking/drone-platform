-- C2 Engine database schema (PostgreSQL + PostGIS)
-- Reference SQL for manual table creation without SQLAlchemy.

CREATE EXTENSION IF NOT EXISTS postgis;

-- Track updates: every position report from any sensor source
CREATE TABLE IF NOT EXISTS track_updates (
    id              SERIAL PRIMARY KEY,
    entity_id       VARCHAR(64) NOT NULL,
    source          VARCHAR(32) NOT NULL,
    "timestamp"     TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    position        geometry(Point, 4326),
    latitude        DOUBLE PRECISION,
    longitude       DOUBLE PRECISION,
    altitude_m      DOUBLE PRECISION DEFAULT 0.0,
    heading         DOUBLE PRECISION DEFAULT 0.0,
    speed_mps       DOUBLE PRECISION DEFAULT 0.0,
    vertical_rate_mps DOUBLE PRECISION DEFAULT 0.0,
    raw_data        JSONB DEFAULT '{}'::jsonb
);

CREATE INDEX IF NOT EXISTS ix_track_updates_entity_id ON track_updates (entity_id);
CREATE INDEX IF NOT EXISTS ix_track_updates_entity_time ON track_updates (entity_id, "timestamp");
CREATE INDEX IF NOT EXISTS ix_track_updates_time ON track_updates ("timestamp");
CREATE INDEX IF NOT EXISTS ix_track_updates_position ON track_updates USING GIST (position);

-- Entities: resolved fused identities
CREATE TABLE IF NOT EXISTS entities (
    id              VARCHAR(64) PRIMARY KEY,
    domain          VARCHAR(16) NOT NULL,
    entity_type     VARCHAR(32) DEFAULT 'unknown',
    name            VARCHAR(128) DEFAULT '',
    callsign        VARCHAR(64) DEFAULT '',
    mmsi            INTEGER,
    icao_hex        VARCHAR(8),
    mavlink_sysid   INTEGER,
    affiliation     VARCHAR(16) DEFAULT 'unknown',
    threat_level    INTEGER DEFAULT 0,
    threat_category VARCHAR(16) DEFAULT 'none',
    confidence      DOUBLE PRECISION DEFAULT 0.5,
    last_position   geometry(Point, 4326),
    last_latitude   DOUBLE PRECISION DEFAULT 0.0,
    last_longitude  DOUBLE PRECISION DEFAULT 0.0,
    last_altitude_m DOUBLE PRECISION DEFAULT 0.0,
    last_heading    DOUBLE PRECISION DEFAULT 0.0,
    last_speed_mps  DOUBLE PRECISION DEFAULT 0.0,
    last_seen       TIMESTAMPTZ,
    first_seen      TIMESTAMPTZ,
    created_at      TIMESTAMPTZ DEFAULT NOW(),
    updated_at      TIMESTAMPTZ DEFAULT NOW(),
    metadata        JSONB DEFAULT '{}'::jsonb
);

CREATE INDEX IF NOT EXISTS ix_entities_mmsi ON entities (mmsi);
CREATE INDEX IF NOT EXISTS ix_entities_icao_hex ON entities (icao_hex);
CREATE INDEX IF NOT EXISTS ix_entities_last_position ON entities USING GIST (last_position);

-- Classifications: every classification decision
CREATE TABLE IF NOT EXISTS classifications (
    id              SERIAL PRIMARY KEY,
    entity_id       VARCHAR(64) NOT NULL REFERENCES entities(id),
    "timestamp"     TIMESTAMPTZ DEFAULT NOW(),
    affiliation     VARCHAR(16),
    threat_level    INTEGER,
    threat_category VARCHAR(16),
    confidence      DOUBLE PRECISION,
    reasoning       JSONB DEFAULT '[]'::jsonb,
    anomalies       JSONB DEFAULT '[]'::jsonb
);

CREATE INDEX IF NOT EXISTS ix_classifications_entity_id ON classifications (entity_id);
CREATE INDEX IF NOT EXISTS ix_classifications_entity_time ON classifications (entity_id, "timestamp");

-- Alerts
CREATE TABLE IF NOT EXISTS alerts (
    id              SERIAL PRIMARY KEY,
    entity_id       VARCHAR(64) REFERENCES entities(id),
    alert_type      VARCHAR(32) NOT NULL,
    severity        INTEGER DEFAULT 5,
    title           VARCHAR(256) NOT NULL,
    description     TEXT DEFAULT '',
    acknowledged    BOOLEAN DEFAULT FALSE,
    acknowledged_by VARCHAR(64),
    acknowledged_at TIMESTAMPTZ,
    created_at      TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS ix_alerts_type_sev ON alerts (alert_type, severity);
CREATE INDEX IF NOT EXISTS ix_alerts_created ON alerts (created_at);

-- Audit log: immutable trail of significant actions
CREATE TABLE IF NOT EXISTS audit_log (
    id              SERIAL PRIMARY KEY,
    "timestamp"     TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    actor           VARCHAR(64) DEFAULT 'system',
    action          VARCHAR(64) NOT NULL,
    target_type     VARCHAR(32),
    target_id       VARCHAR(64),
    details         JSONB DEFAULT '{}'::jsonb
);

CREATE INDEX IF NOT EXISTS ix_audit_time ON audit_log ("timestamp");
CREATE INDEX IF NOT EXISTS ix_audit_actor ON audit_log (actor);
