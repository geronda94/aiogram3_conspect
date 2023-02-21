from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, ContentType
from aiogram.filters import Filter, Command, Text
import asyncio
from environs import Env
import logging #импортируем библиотеку логирования
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime,timedelta
from typing import Dict, Any, Callable, Awaitable
from aiogram import BaseMiddleware
from aiogram.types.base import TelegramObject


#Блок инициализации#############################
env = Env()                                    #
env.read_env('.env')                           #
TOKEN = env.str('TOKEN')                       #
ADMIN = env.int('ADMIN_ID')                    #
################################################

#Устанавливаем функции на выполнение по расписанию обычным способом
async def send_message_time(bot: Bot):
    await bot.send_message(ADMIN, f'Cсообщение которое отправляется через пару секунд после статра бота')

async def send_message_cron(bot: Bot):
    await bot.send_message(ADMIN, f'Собщение которое отправляется еждневно в одно и то же время')

async def send_message_interval(bot: Bot):
    await bot.send_message(ADMIN, f'Сообщение которое отправляется каждую минуту')
#######################################################################
#Устанавливаем функции на выполнение по расписанию через middleware
class SchedulerMiddleware(BaseMiddleware):
    def __init__(self, scheduler: AsyncIOScheduler):
        self.scheduler = scheduler














#Блок стартовых функций#########################
async def start_bot(bot: Bot): #функция срабатывает когда запускается сервер с ботом
    await bot.send_message(ADMIN, text='Бот запущен!')
async def stop_bot(bot: Bot):
    await bot.send_message(ADMIN, text='<s>Бот остановлен</s>')
async def get_start(message: Message, bot: Bot): #Функция срабатывает когда юзер дает команду /start
    await message.answer('Давай начнем!')
###############################################


#Тело бота#####################################
async def start():
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - [%(levelname)s] - %(name)s -(%(filename)s).%(funcName)s(%(lineno)d) - %(message)s")

    bot = Bot(token=TOKEN, parse_mode="HTML")
    dp = Dispatcher()

    #########
    #Устанавливаем объект шедулер с временной зонной
    scheduler = AsyncIOScheduler(timezone="Europe/Kiev")
    #Регистрируем в шеделере функцию которая отправляет сообщение через 10 минут после старта
    scheduler.add_job(send_message_time, trigger='date', run_date=datetime.now()+timedelta(seconds=10,), kwargs={'bot': bot})
    #Регистрируем шедулер который отправляет сообщение каждый день в определенное время
    scheduler.add_job(send_message_cron, trigger='cron', hour=datetime.now().hour, minute=datetime.now().minute+1,
                      start_date= datetime.now(), kwargs={'bot': bot})
    #Регистрируем шедулер который отправляет сообщение каждые 10 секунд
    scheduler.add_job(send_message_interval, trigger='interval', seconds=60, kwargs={'bot': bot})
    scheduler.start() #чтобы все прописанные выше задания выполнились, шедулер нужно запустить
    #############

    dp.startup.register(start_bot) #Регистрируем хэндлер срабатывающий при запуске
    dp.shutdown.register(stop_bot)



    dp.message.register(get_start, Command(commands=['start'])) #Регистрируем хэндлер на команду /start





    try:
        #Начало сессии
        await dp.start_polling(bot)
    finally:
        #Закрываем сессию
        await bot.session.close()
###############################################


#Запускаем функцию Бота########################
if __name__ =="__main__":
    asyncio.run(start())


