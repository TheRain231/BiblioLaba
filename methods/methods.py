import psycopg2
from config import db_name, host, password, port, user

try:
    # connect to exist DB

    connection = psycopg2.connect(
        host=host, user=user, password=password, dbname=db_name, port=port
    )
    connection.autocommit = True

    # the cursor for performing databse operations

    # cursor = connection.cursor()

    with connection.cursor() as cursor:
        cursor.execute(
            """
            CREATE TABLE BOOK(
            id serial PRIMARY KEY,
            first_name varchar(50) NOT NULL,
            nick_name varchar(50) NOT NULL);
"""
        )
        print("[INFO] Table created successfully")

except Exception as _ex:
    print("[INFO] Error while working with PostgreSQL", _ex)
finally:
    if connection:
        connection.close()
        print("[INFO] PoasgreSQL connection closed")
