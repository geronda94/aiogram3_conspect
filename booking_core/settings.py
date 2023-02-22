from environs import Env #моудль для работы с локальными переменными
from dataclasses import dataclass #модуль с оберткой классов для быстрой инициализации

@dataclass
class Bots:
    bot_token: str
    admin_id: str

@dataclass
class DB:
    user: str
    host: str
    port: str
    password: str
    db: str

@dataclass
class Settings:
    bots: Bots
    db: DB


def get_settings(path: str):
    env = Env()
    env.read_env(path=path)

    return Settings(
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

settings = get_settings('.env')


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