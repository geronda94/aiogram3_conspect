import asyncio
import asyncpg
from aiohttp import web
from config import user, password, host, port

db_name = 'booking_bot'

dsn = f'postgresql://{user}:{password}@{host}:{port}/{db_name}'


###############################################################
#Самый простой но не очень удобный пример подключения к бд
async def print_db():
    async def con_db():

        pool = await asyncpg.create_pool(dsn)
        async with pool.acquire() as connection:
            result = await connection.fetch("SELECT * FROM test")

        await pool.close()

        return [x for x in result]

    lst = await con_db()


    for i in lst:
        print(*i)
##############################################################
#Прописываем все действия с базой в классы, удобно но медлено
class Database:
    def __init__(self, user, password, host, port, db_name):
        self.pool = None
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.db_name = db_name
        self.dsn = f'postgresql://{user}:{password}@{host}:{port}/{db_name}'

    #При формировании запроса к бд сначала нужно будет открыть подключение этой функцией
    async def connect(self):
        self.pool = await asyncpg.create_pool(user=self.user, password=self.password, host=self.host,
                                              port=self.port, database=self.db_name)
        #self.pool = await asyncpg.create_pool(self.dsn)

    #а после всех действий закрыть этой
    async def disconnect(self):
        await self.pool.close()

    #Функция на извлечение данных из бд
    async def fetch(self, query):
        async with self.pool.acquire() as connection:
            return await connection.fetch(query)

    # Функция на добавление данных в бд
    async def execute(self, query):
        async with self.pool.acquire() as connection:
            return await connection.execute(query)

#Пример подключения через классы
async def main():
    db = Database(user, password, host, port, db_name) # инициализируем подключение
    await db.connect() # подключаемся к бд
    result = await db.fetch("SELECT * FROM booking;") #Извлекаем данные в переменную
    for i in result:
        print(*i)
    #await db.execute(f"INSERT INTO users (name, dob) VALUES ('Albert','1999-05-06');" )#Добавляем данные в бд
    await db.disconnect()# закрываем подключени


async def db_write(query: str): #В query прописываем обращение к бд
    db = Database(user, password, host, port, db_name)
    await db.connect()
    await db.execute(query)#f"INSERT INTO users (name, dob) VALUES ('Albert','1999-05-06');"   - ПРимер запроса к бд
    await db.disconnect()


async def db_read(query: str):
    db = Database(user, password, host, port, db_name)
    await db.connect()
    result = await db.fetch(query) #"SELECT * FROM users"   - Пример запроса к бд
    await db.disconnect()
    return result #возвращаем данные извлеченные из базы


########################################################################################
#Еще один пример как можно вызывать пул хапрос к бд, самый быстрый
async def pool_connect():
    return await asyncpg.create_pool(user='DB_USER', password='DB_PASSWORD', host='DB_HOST',
                                     port='DB_PORT', database='DB_NAME')



async def database_entry():
    pool = await pool_connect() #Передаем соединение с бд через пул в переменную

    async with pool.acquire() as connection: #Покдючаемся к бд через контестный менеджер
        await connection.fetch(f'INSERT ....')  #Добавляем в базу значения
        ret = await connection.execute(f'SELECT ....')  #Извлекаем из базы значения и помещаем их в переменную

#############################################################################################

if __name__ == "__main__":
    asyncio.run(main())





