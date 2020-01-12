import IPython as IP
import psycopg2 as psql
import numpy as np
import lorem
# j


def test_connection():
    user = "db_air"
    pwd = "password"
    db = "weather"
    port = "5432"
    host = "localhost"
    connection = \
    f"dbname='" + db + "' " + \
    f"user='{user}' " + \
    f"port='{port}' " + \
    f"host='{host}' " + \
    f"password='{pwd}' "
    conn = psql.connect(connection)
    cur = conn.cursor()
    n = 2
    # test_text = (
    #     [lorem.paragraph() for _ in range(n)],
    #     [lorem.paragraph() for _ in range(n)],
    #     [lorem.paragraph() for _ in range(n)],
    # )
    test_text = (
        [lorem.sentence() for _ in range(n)],
        [lorem.sentence() for _ in range(n)],
        [lorem.sentence() for _ in range(n)],
    )
    test_int = (
        [np.random.randint(100_000) for _ in range(n)],
        [np.random.randint(100_000) for _ in range(n)],
        [np.random.randint(100_000) for _ in range(n)],
    )

    # Setting up the tables
    q = ""
    with open("test/test_db_create_table.sql", "r") as file:
        q += file.read()
    cur.execute(q)
    conn.commit()

    #inserting data
    for j in range(3):
        for i in zip(test_text[j], test_int[j]):
            cur.execute(f"INSERT INTO test{j+1}(test_text, test_int) VALUES (%s, %s)", (i))
    conn.commit()

    # Reading the data
    read_data = []
    for j in range(3):
        cur.execute(f"SELECT * FROM test{j+1}")
        rows = cur.fetchall()
        read_data.append(rows)
    # print(f"\n\n read data is: \n{read_data} \n")

    # Asserting data
    for i in range(len(read_data)):
        for j in range(n):
            assert read_data[i][j][1] == test_text[i][j], f"""
                read_data: (text)
                {read_data[i][j][1]}
                    !=
                test_data (text)
                {test_text[i][j]}
                """
            assert read_data[i][j][2] == test_int[i][j], f"""
                read_data: (int)
                {read_data[i][j][2]}
                    !=
                test_data (int)
                {test_int[i][j]}
                test_connection():Asserting data"""

    # cleaning up
    q = "DROP TABLE test1, test2, test3;"
    
    cur.execute(q)
    conn.commit()
    cur.close()
    conn.close()


if __name__ == "__main__":
    test_connection()

