DROP TABLE IF EXISTS test1, test2, test3;

CREATE TABLE test1 (
    id SERIAL PRIMARY KEY,
    test_text text,
    test_int INTEGER
);
CREATE TABLE test2 (
    id SERIAL PRIMARY KEY,
    test_text text,
    test_int INTEGER,
    test_reff INTEGER REFERENCES test1(id)
);
CREATE TABLE test3 (
    id SERIAL PRIMARY KEY,
    test_text text,
    test_int INTEGER,
    test_reff INTEGER REFERENCES test2(id) 
);