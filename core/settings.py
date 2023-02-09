from environs import Env #моудль для работы с локальными переменными
from dataclasses import dataclass #модуль с оберткой классов для быстрой инициализации


@dataclass
class Bots:
    TOKEN : str
    ADMIN : int

@dataclass
class Settings:
    bots: Bots

def get_settings(path: str): #Задаем функцию по выгрузке переменных
    env = Env()
    env.read_env(path)
    return Settings(
        bots = Bots(TOKEN=env.str('TOKEN'),
                    ADMIN=env.int('ADMIN_ID'))
    )

settings = get_settings('.env')  #Создаем набор переменных из окружения .env

TOKEN = settings.bots.TOKEN
ADMIN = settings.bots.ADMIN



# Делает аналогичное коду выше
# env = Env()
# env.read_env('.env')
# TOKEN = env.str('TOKEN')
# ADMIN = env.int('ADMIN_ID')