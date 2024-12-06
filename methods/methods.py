import psycopg2
from config import host, new_db_name, password, port, user

# try:
#     # connect to exist DB

#     connection = psycopg2.connect(
#         host=host, user=user, password=password, dbname=db_name, port=port
#     )
#     connection.autocommit = True

#     # the cursor for performing databse operations

#     # cursor = connection.cursor()

#     with connection.cursor() as cursor:
#         cursor.execute(
#             """
#             CREATE TABLE BOOK(
#             id serial PRIMARY KEY,
#             first_name varchar(50) NOT NULL,
#             nick_name varchar(50) NOT NULL);
# """
#         )
#         print("[INFO] Table created successfully")

# except Exception as _ex:
#     print("[INFO] Error while working with PostgreSQL", _ex)
# finally:
#     if connection:
#         connection.close()
#         print("[INFO] PoasgreSQL connection closed")


def CreateDB():
    try:
        conn = psycopg2.connect(host=host, port=port, user=user, password=password)

        # Создание курсора для выполнения запросов
        cur = conn.cursor()

        # Запрос на создание новой базы данных
        db_name = new_db_name
        create_db_query = f"CREATE DATABASE {db_name};"

        # Выполнение запроса
        cur.execute(create_db_query)
        print(f"База данных '{db_name}' успешно создана.")
    except Exception as e:
        print(f"Произошла ошибка при создании базы данных: {e}")
    finally:
        # Закрытие соединения и курсора
        cur.close()
        conn.commit()  # Применяем изменения
        conn.close()


def CreateTables():
    try:
        pass
    except Exception as e:
        print(f"Произошла ошибка при создании таблиц: {e}")
    finally:
        pass


def DeleteDB():
    try:
        conn = psycopg2.connect(host=host, port=port, user=user, password=password)

        # Создание курсора для выполнения запросов
        cur = conn.cursor()

        # Запрос на создание новой базы данных
        db_name = new_db_name
        delete_db_query = f"DROP DATABASE {db_name};"

        # Выполнение запроса
        cur.execute(delete_db_query)
        print(f"База данных '{db_name}' успешно удалена.")
    except Exception as e:
        print(f"Произошла ошибка при удалении базы данных: {e}")
    finally:
        # Закрытие соединения и курсора
        cur.close()
        conn.commit()  # Применяем изменения
        conn.close()
