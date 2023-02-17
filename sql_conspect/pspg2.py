import psycopg2
from config import db_name, host,port,user,password

try:
    connection = psycopg2.connect(
        host=host,
        port=port,
        database=db_name,
        user=user,
        password=password)

    connection.autocommit = True

    # with connection.cursor() as cursor:
    #     cursor.execute(
    #         """
    #         CREATE TABLE users(
    #         id serial PRIMARY KEY,
    #         name varchar(15) NOT NULL,
    #         nick_name varchar(25) NOT NULL
    #         );
    #         """)
    #     print(f'Таблица users создана!')

    # with connection.cursor() as cursor:
    #     cursor.execute(
    #         """
    #         INSERT INTO users (name, nick_name) VALUES ('igor', 'harry94');
    #         """
    #     )
    #     print('Данные добавлены')

    # with connection.cursor() as cursor:
    #         cursor.execute(
    #             """
    #             SELECT * FROM users;
    #             """
    #         )
    #         data = cursor.fetchall()

    with connection.cursor() as cursor:
        cursor.execute('DROP TABLE users;')

except Exception as ex:
    print(ex)
finally:
    if connection:
        connection.close()

