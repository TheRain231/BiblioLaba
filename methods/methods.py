import psycopg2
from config import host, new_db_name, password, port, user


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
        conn = psycopg2.connect(
            host=host, port=port, user=user, password=password, dbname=new_db_name
        )
        cur = conn.cursor()
        create_table_book = """
        CREATE TABLE IF NOT EXISTS BOOK (
    book_id SERIAL PRIMARY KEY,
    title VARCHAR(255),
    price DECIMAL(10, 2),
    amount INT,
    author_id INT REFERENCES AUTHOR(author_id),
    genre_id INT REFERENCES GENRE(genre_id),
    publishing_house_id INT REFERENCES PUBLISHING_HOUSE(publishing_house_id),
    description_id INT REFERENCES DESCRIPTION(description_id)
);
"""
        create_table_author = """
    CREATE TABLE IF NOT EXISTS AUTHOR (
        author_id SERIAL PRIMARY KEY,
        author_first_name VARCHAR(100),
        author_last_name VARCHAR(100)
    );
    """
        create_table_genre = """
    CREATE TABLE IF NOT EXISTS GENRE (
        genre_id SERIAL PRIMARY KEY,
        genre VARCHAR(50)
    );
    """
        create_table_publishing_house = """
        CREATE TABLE IF NOT EXISTS PUBLISHING_HOUSE (
        publishing_house_id SERIAL PRIMARY KEY,
        publishing_house_name VARCHAR(200),
        city VARCHAR(100),
        country VARCHAR(100),
        count_of_books INT
    );
    """
        create_table_description = """
    CREATE TABLE IF NOT EXISTS DESCRIPTION (
        description_id SERIAL PRIMARY KEY,
        description TEXT);
    """
        queries = [
            create_table_book,
            create_table_author,
            create_table_genre,
            create_table_description,
            create_table_publishing_house,
        ]
        for query in queries:
            try:
                cur.execute(query)
                print("Table was created successfully")
            except Exception as e:
                print(f"Произошла ошибка при создании таблицы: {e}")

    except Exception as e:
        print(f"Произошла ошибка при создании таблиц: {e}")
    finally:
        cur.close()
        conn.commit()  # Применяем изменения
        conn.close()


def CreateFuncs():
    try:
        conn = psycopg2.connect(
            host=host, port=port, user=user, password=password, dbname=new_db_name
        )
        cur = conn.cursor()
        create_func_author = """
CREATE OR REPLACE FUNCTION check_author_exists(author_id INT)
RETURNS BOOLEAN AS

$$
BEGIN
    RETURN EXISTS (SELECT 1 FROM BOOK WHERE author_id = $1);
END;

$$ LANGUAGE plpgsql;
"""
        create_func_genre = """
    CREATE OR REPLACE FUNCTION check_genre_exists(genre_id INT)
    RETURNS BOOLEAN AS

    $$
    BEGIN
        RETURN EXISTS (SELECT 1 FROM BOOK WHERE genre_id = $1);
    END;

    $$ LANGUAGE plpgsql;

    """
        create_func_publishing_house = """
CREATE OR REPLACE FUNCTION check_publishing_house_exists(publishing_house_id INT)
RETURNS BOOLEAN AS

$$
BEGIN
    RETURN EXISTS (SELECT 1 FROM BOOK WHERE publishing_house_id = $1);
END;

$$ LANGUAGE plpgsql;
"""
        queries = [
            create_func_author,
            create_func_genre,
            create_func_publishing_house,
        ]
        for query in queries:
            try:
                cur.execute(query)
                print("Functions was created successfully")
            except Exception as e:
                print(f"Произошла ошибка при создании таблицы: {e}")

    except Exception as e:
        print(f"Произошла ошибка при создании функций: {e}")
    finally:
        cur.close()
        conn.commit()  # Применяем изменения
        conn.close()


def CreateProcedures():
    try:
        conn = psycopg2.connect(
            host=host, port=port, user=user, password=password, dbname=new_db_name
        )
        cur = conn.cursor()

        delete_author = """
    CREATE OR REPLACE PROCEDURE delete_author_if_not_used(author_id INT)
LANGUAGE plpgsql
AS

$$
BEGIN
    IF NOT check_author_exists(author_id) THEN
        DELETE FROM AUTHOR WHERE author_id = $1;
    END IF;
END;

$$;
"""
        delete_genre = """
CREATE OR REPLACE PROCEDURE delete_genre_if_not_used(genre_id INT)
LANGUAGE plpgsql
AS

$$
BEGIN
    IF NOT check_genre_exists(genre_id) THEN
        DELETE FROM GENRE WHERE genre_id = $1;
    END IF;
END;

$$;
"""
        delete_publishing_house = """
    CREATE OR REPLACE PROCEDURE delete_publishing_house_if_not_used(publishing_house_id INT)
LANGUAGE plpgsql
AS

$$
BEGIN
    IF NOT check_publishing_house_exists(publishing_house_id) THEN
        DELETE FROM PUBLISHING_HOUSE WHERE publishing_house_id = $1;
    END IF;
END;

$$;
"""
        queries = [delete_author, delete_genre, delete_publishing_house]
        for query in queries:
            try:
                cur.execute(query)
                print("Functions was created successfully")
            except Exception as e:
                print(f"Произошла ошибка при удалении строки в таблицах: {e}")

    except Exception as e:
        print(f"Произошла ошибка при создании процедур: {e}")
    finally:
        cur.close()
        conn.commit()  # Применяем изменения
        conn.close()


def CreateTriggers():
    try:
        conn = psycopg2.connect(
            host=host, port=port, user=user, password=password, dbname=new_db_name
        )
        cur = conn.cursor()

        trigger_delete_author = """
CREATE OR REPLACE TRIGGER trigger_delete_book
AFTER DELETE ON BOOK
FOR EACH ROW
EXECUTE FUNCTION delete_author_if_not_used(OLD.author_id);
"""
        trigger_delete_genre = """
    CREATE OR REPLACE TRIGGER trigger_delete_book_genre
AFTER DELETE ON BOOK
FOR EACH ROW
EXECUTE FUNCTION delete_genre_if_not_used(OLD.genre_id);
"""
        trigger_delete_publishing_house = """
CREATE OR REPLACE TRIGGER trigger_delete_book_publishing_house
AFTER DELETE ON BOOK
FOR EACH ROW
EXECUTE FUNCTION delete_publishing_house_if_not_used(OLD.publishing_house_id);
"""
        queries = [
            trigger_delete_author,
            trigger_delete_genre,
            trigger_delete_publishing_house,
        ]
        for query in queries:
            try:
                cur.execute(query)
                print("Triggers was created successfully")
            except Exception as e:
                print(f"Произошла ошибка при добавлении триггеров в DB: {e}")

    except Exception as e:
        print(f"Произошла ошибка при создании триггеров: {e}")
    finally:
        cur.close()
        conn.commit()  # Применяем изменения
        conn.close()



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
