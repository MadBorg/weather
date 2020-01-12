DROP TABLE IF EXISTS Station, Reading, Component;

CREATE TABLE Station (
    id INTEGER PRIMARY KEY,
    eoi VARCHAR(10) UNIQUE,
    name VARCHAR(255) UNIQUE,
    latitude FLOAT(10),
    longitude FLOAT(10),
    zone VARCHAR(255),
    municipality VARCHAR(255),
    area VARCHAR(255),
    description text,
    components text,
    status text
);

CREATE TABLE Component (
    id SERIAL PRIMARY KEY,
    component VARCHAR(255) NOT NULL
    -- unit VARCHAR(255)
);

CREATE TABLE Reading(
    id SERIAL PRIMARY KEY,
    eoi VARCHAR(10) NOT NULL REFERENCES Station(eoi),
    time_from TIMESTAMP WITH TIME ZONE NOT NULL,
    time_to TIMESTAMP WITH TIME ZONE NOT NULL,
    value FLOAT(12) NOT NULL,
    -- index INTEGER,
    id_component INTEGER REFERENCES Component(id),

    UNIQUE (eoi, time_from, time_to, id_component)
);

