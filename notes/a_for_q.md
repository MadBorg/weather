## Postgres: INSERT if does not exist already

``` sql

INSERT ... ON CONFLICT DO NOTHING/UPDATE

```

## Creating user and giving all priveliges

``` sql

CREATE DATABASE yourdbname;
CREATE USER youruser WITH ENCRYPTED PASSWORD 'yourpass';
GRANT ALL PRIVILEGES ON DATABASE yourdbname TO youruser;

```