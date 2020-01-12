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

## Inserting with new data and data from other table

``` sql

INSERT INTO table1 ( column1, column2, someInt, someVarChar )
SELECT  table2.column1, table2.column2, 8, 'some string etc.'
FROM    table2
WHERE   table2.ID = 7;

```

url: https://stackoverflow.com/questions/25969/insert-into-values-select-from
