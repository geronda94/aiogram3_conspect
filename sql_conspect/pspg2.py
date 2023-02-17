import psycopg2
from config import db_name, host,port,user,password

try:
    connection = psycopg2.connect(
        host=host,
        database=db_name,
        user=user,
        password=password)

    cursor = connection.cursor()



except Exception as ex:
    print(ex)
finally:
    pass

