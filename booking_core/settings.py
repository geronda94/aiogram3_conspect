from environs import Env #моудль для работы с локальными переменными
from dataclasses import dataclass #модуль с оберткой классов для быстрой инициализации

#СОздаем класс который хранит настройки бота
@dataclass
class Bots:
    bot_token: str
    admin_id: str


#Создаем класс который хранит настрйки БД
@dataclass
class DB:
    user: str
    host: str
    port: str
    password: str
    db: str


#Создаем класс который хранит в себе данный двух предыдущих классов
@dataclass
class Settings:
    bots: Bots #Иницилизация класса с настройками бота
    db: DB     #Инициализация класса с настройками БД


#Создаем функцию которая возращает настройки из классов
def get_settings(path: str):
    env = Env()
    env.read_env(path=path) #Указываем путь до файла с локальными переменными

    return Settings( #Возвращаем класс прописаный выше, инициаизируя через него настройки бота и БД
    bots=Bots(
        bot_token=env.str('TOKEN'),
        admin_id=env.str('ADMIN_ID')
    ),
    db=DB(
        user=env.str('DB_USER'),
        host=env.str('DB_HOST'),
        port=env.str('DB_PORT'),
        password=env.str('DB_PASSWORD'),
        db=env.str('DB_DATABASE')
    ))

settings = get_settings('config.py') #Устанавливаем настройки в переменную

TOKEN = settings.bots.bot_token
ADMIN = settings.bots.admin_id

DB_USER = settings.db.user
DB_PASSWORD = settings.db.password
DB_NAME = settings.db.db
DB_PORT = settings.db.port
DB_HOST = settings.db.host

#from booking_core.settings import TOKEN, ADMIN, DB_HOST, DB_PORT,DB_NAME, DB_USER,DB_PASSWORD





#Делает аналогичное коду выше
# env = Env()
# env.read_env('.env')
# TOKEN = env.str('TOKEN')
# ADMIN = env.int('ADMIN_ID')
# DB_USER = env.str('DB_USER ')
# DB_PASSWORD = env.str('DB_PASSWORD')
# DB_HOST = env.str('DB_HOST')
# DB_PORT = env.str('DB_PORT')
# DB_DATABASE = env.str('DB_DATABASE')