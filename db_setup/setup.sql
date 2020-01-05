DROP TABLE Station, Zone, Municipality, Area, Readings;

CREATE TABLE Zone (
    name VARCHAR(255) PRIMARY KEY
);
CREATE TABLE Municipality (
    name VARCHAR(255) PRIMARY KEY
);
CREATE TABLE Area (
    name VARCHAR(255) PRIMARY KEY
);

CREATE TABLE Station (
    id SERIAL PRIMARY KEY,
    eoi VARCHAR(7) NOT NULL,
    latitude FLOAT(10),
    longitude FLOAT(10),
    zone_name VARCHAR(255) REFERENCES Zone(name),
    zone_municipality VARCHAR(255) REFERENCES Municipality(name),
    zone_area VARCHAR(255) REFERENCES Area(name),
    UNIQUE(eoi)
);

CREATE TABLE Readings(
    id SERIAL PRIMARY KEY,
    eoi VARCHAR(7) NOT NULL REFERENCES Station(eoi),
    time_from TIME NOT NULL,
    time_to TIME NOT NULL,
    value FLOAT(12) NOT NULL,
    index INTEGER,
    unit VARCHAR(50),
    component VARCHAR(255) NOT NULL
);