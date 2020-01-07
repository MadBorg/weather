DROP TABLE Station, Reading, Component;

CREATE TABLE Station (
    id SERIAL PRIMARY KEY,
    eoi VARCHAR(7) NOT NULL,
    latitude FLOAT(10),
    longitude FLOAT(10),
    zone_name VARCHAR(255),
    zone_municipality VARCHAR(255),
    zone_area VARCHAR(255),
    UNIQUE (eoi)
);

CREATE TABLE Component (
    id SERIAL PRIMARY KEY,
    component VARCHAR(255) NOT NULL,
    unit VARCHAR(255)
);

CREATE TABLE Reading(
    id SERIAL PRIMARY KEY,
    eoi VARCHAR(7) NOT NULL REFERENCES Station(eoi),
    time_from TIME NOT NULL,
    time_to TIME NOT NULL,
    value FLOAT(12) NOT NULL,
    index INTEGER,
    id_component INTEGER REFERENCES Component(id),

    UNIQUE (eoi, time_from, time_to, id_component)
);

