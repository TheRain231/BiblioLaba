import psycopg2
from methods.config import host, new_db_name, password, port, user


def CreateDB():
    try:
        conn = psycopg2.connect(host=host, port=port, user=user, password=password)
        conn.autocommit = True
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
        conn.close()


def CreateTables():
    try:
        conn = psycopg2.connect(
            host=host, port=port, user=user, password=password, dbname=new_db_name
        )

        conn.autocommit = True
        cur = conn.cursor()
        clinetTable = """
        CREATE TABLE IF NOT EXISTS Client (
    client_id SERIAL PRIMARY KEY,
    login VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL
);
        """
        genreTable = """
            CREATE TABLE IF NOT EXISTS Genre (
    genre_id SERIAL PRIMARY KEY,
    genre VARCHAR(255) UNIQUE NOT NULL
);
        """

        authorTable = """
        CREATE TABLE IF NOT EXISTS Author (
    author_id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    surname VARCHAR(255) NOT NULL
);
        """

        publishingHouseTable = """
        CREATE TABLE IF NOT EXISTS PublishingHouse (
    publishing_house_id SERIAL PRIMARY KEY,
    label VARCHAR(255) UNIQUE NOT NULL
);
        """

        bookTable = """
        CREATE TABLE IF NOT EXISTS Book (
    book_id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    image VARCHAR(255),
    description TEXT,
    author_id INT REFERENCES Author(author_id),
    genre_id INT REFERENCES Genre(genre_id),
    publishing_house_id INT REFERENCES PublishingHouse(publishing_house_id),
    client_id INT REFERENCES Client(client_id),
    count INT
);
        """
        queries = [
            clinetTable,
            authorTable,
            genreTable,
            publishingHouseTable,
            bookTable
        ]
        for query in queries:
            try:
                cur.execute(query)
                print(cur.fe)
            except Exception as e:
                print(f"Произошла ошибка при создании таблицы: {e}")
    except Exception as e:
        print(f"Произошла ошибка при создании таблиц: {e}")
    finally:
        cur.close()
        conn.close()


def CreateFuncs():
    try:
        conn = psycopg2.connect(
            host=host, port=port, user=user, password=password, dbname=new_db_name
        )
        cur = conn.cursor()
        conn.autocommit = True
        insertFunc = """
        CREATE OR REPLACE FUNCTION check_and_update_count()
RETURNS TRIGGER AS

$$
DECLARE
    existing_record RECORD;
BEGIN
    SELECT * INTO existing_record
    FROM Book
    WHERE author_id = NEW.author_id
      AND publishing_house_id = NEW.publishing_house_id
      AND title = NEW.title;
      
    IF FOUND THEN
        UPDATE Book
        SET count = count + NEW.count
        WHERE book_id = existing_record.book_id;
        
        RETURN NULL; 
    ELSE
        RETURN NEW; 
    END IF;
END;

$$ LANGUAGE plpgsql;
        """
        decreaseCountFunc = """
        CREATE OR REPLACE FUNCTION decrease_count(book_id INTEGER)
RETURNS VOID AS

$$
BEGIN
    UPDATE Book
    SET count = CASE WHEN count > 0 THEN count - 1 ELSE 0 END
    WHERE book_id = decrease_count.book_id;
END;

$$ LANGUAGE plpgsql;"""

        getAuthorId = """
        CREATE OR REPLACE FUNCTION get_author_id(name1 VARCHAR, surname1 VARCHAR)
RETURNS INT AS

$$
DECLARE
    v_author_id INT;
BEGIN
    SELECT a.author_id INTO v_author_id
    FROM Author a
    WHERE a.name = name1
      AND a.surname = surname1;

    IF FOUND THEN
        RETURN v_author_id;
    ELSE
        RETURN -1;
    END IF;
END;

$$ LANGUAGE plpgsql;
        """

        getPublishingHouseId = """
        CREATE OR REPLACE FUNCTION get_publishing_house_id(label1 VARCHAR)
RETURNS INT AS

$$
DECLARE
    v_publishing_house_id INT;
BEGIN
    SELECT p.publishing_house_id INTO v_publishing_house_id
    FROM PublishingHouse p
    WHERE p.label = label1;

    IF FOUND THEN
        RETURN v_publishing_house_id;
    ELSE
        RETURN -1;
    END IF;
END;

$$ LANGUAGE plpgsql;
        """

        getGenreId = """
        CREATE OR REPLACE FUNCTION get_genre_id(genre1 VARCHAR)
RETURNS INT AS

$$
DECLARE
    v_genre_id INT;
BEGIN
    SELECT g.genre_id INTO v_genre_id
    FROM Genre g
    WHERE g.genre = genre1;

    IF FOUND THEN
        RETURN v_genre_id;
    ELSE
        RETURN -1;
    END IF;
END;

$$ LANGUAGE plpgsql;
        """

        getClientId = """
        CREATE OR REPLACE FUNCTION get_client_id(login1 VARCHAR)
RETURNS INT AS

$$
DECLARE
    v_client_id INT;
BEGIN
    SELECT c.client_id INTO v_client_id
    FROM Client c
    WHERE c.login = login1;

    IF FOUND THEN
        RETURN v_client_id;
    ELSE
        RETURN -1;
    END IF;
END;

$$ LANGUAGE plpgsql;
        """

        queries = [
            insertFunc,
            decreaseCountFunc,
            getAuthorId,
            getPublishingHouseId,
            getGenreId,
            getClientId
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
        conn.close()



def CreateTriggers():
    try:
        conn = psycopg2.connect(
            host=host, port=port, user=user, password=password, dbname=new_db_name
        )
        cur = conn.cursor()
        conn.autocommit = True
        insertTrigger = """
        CREATE TRIGGER before_insert_book
BEFORE INSERT ON Book
FOR EACH ROW
EXECUTE FUNCTION check_and_update_count();
        """

        queries = [
            insertTrigger
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
        conn.close()



def DeleteDB():
    try:
        conn = psycopg2.connect(host=host, port=port, user=user, password=password)

        # Создание курсора для выполнения запросов
        cur = conn.cursor()
        conn.autocommit = True
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
        conn.close()




def InsertNewBook(title: str, authorName: str, authorSurName: str, image: str, description: str, genre: str, publishngHouseLabel: str, clientLogin:str, clientPassword:str, count: int = 1):
    try:
        conn = psycopg2.connect(host=host, port=port, user=user, password=password, dbname=new_db_name)

        cur = conn.cursor()
        conn.autocommit = True
        #todo: Переписать в разные функции, которые будут возвращать id каждого

        authorId = f"""
        SELECT get_author_id('{authorName}', '{authorSurName}');
"""
        cur.execute(authorId)
        author_id = cur.fetchall()[0][0]
        if (author_id == -1):
            newAuthorId = f"""
            INSERT INTO author(name, surname)
            VALUES('{authorName}', '{authorSurName}');
"""
            cur.execute(newAuthorId)
            cur.execute(authorId)
            author_id = cur.fetchall()[0][0]




        genreId = f"""
        SELECT get_genre_id('{genre}');
        
"""
        cur.execute(genreId)
        genre_id = cur.fetchall()[0][0]

        if (genre_id == -1):
            newGenreId = f"""
                    INSERT INTO Genre(genre)
                    VALUES('{genre}');
        """
            cur.execute(newGenreId)
            cur.execute(genreId)
            genre_id = cur.fetchall()[0][0]

        publishngHouseId = f"""
        SELECT get_publishing_house_id('{publishngHouseLabel}');
"""
        cur.execute(publishngHouseId)
        publishngHouse_id = cur.fetchall()[0][0]

        clientId = f"""
        SELECT get_client_id('{clientLogin}');
"""

        cur.execute(clientId)
        client_id = cur.fetchall()[0][0]
        print(author_id, genre_id, publishngHouse_id, client_id)
        GeneralQuery = f"""
        INSERT INTO Book (title, image, description, author_id, genre_id, publishing_house_id, client_id, count)
        VALUES (
    '{title}',
    '{image}',
    '{description}',
    '{author_id}',
    '{genre_id}',
    '{publishngHouse_id}',
    '{client_id}',
    '{count}'
);

"""
    except Exception as e:
        print(f"Произошла ошибка при Добавлении элеента: {e}")

    finally:
        cur.close()

        conn.close()



def DecreaseCount(title:str, authorName:str, authorSurName:str):
    try:
        conn = psycopg2.connect(host=host, port=port, user=user, password=password, dbname=new_db_name)
        conn.autocommit = True
        cur = conn.cursor()
        #todo: Запрос на уменьшение книги(функция)
        query = f""""""
        cur.execute(query)
    except Exception as e:
        print(f"Произошла ошибка при Добавлении элеента: {e}")

    finally:
        cur.close()
        conn.close()