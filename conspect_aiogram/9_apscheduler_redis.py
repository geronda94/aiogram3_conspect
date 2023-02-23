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
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.redis import RedisStorage
from apscheduler.jobstores.redis import RedisJobStore
from apscheduler_di import ContextSchedulerDecorator



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
    def __init__(self, scheduler: ContextSchedulerDecorator):
        self.scheduler = scheduler

    async def __call__(self,
                       handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
                       event: TelegramObject,
                       data: Dict[str, Any]
    ) -> Any:
        data['apscheduler'] = self.scheduler
        return await handler(event, data)

#Пишем новую функцию для планировщика которую нужно импортировать в файл FSM для запуска шедулера в конце опросника
async def send_message_scheduler(bot: Bot, chat_id: int):
    await bot.send_message(chat_id, f'Сообщение которое отправлчяется через планировщик после прохождения ОПРОСА!')


###########################БЛОК ОПРОСНИКА
class StepsForm(StatesGroup):
    GET_NAME = State()
    GET_LASTNAME = State()
    GET_OLD = State()

async def get_form(message: Message, state: FSMContext):
    await message.answer(f'{message.from_user.first_name}, начинаем заполнять анкету. Введите свое имя')
    await state.set_state(StepsForm.GET_NAME)


async def get_name(message: Message, state: FSMContext):
    await message.answer(f'Твоё имя: \r\n {message.text}\r\n\nТеперь введите фамилию')
    await state.update_data(name=message.text)     #Заносим данные в машину состояний
    await state.set_state(StepsForm.GET_LASTNAME)  #Переходим к следующему шагу

async def get_lastname(message: Message, state: FSMContext):
    await message.answer(f'Твоя фамилия: \r\n {message.text}\r\n\nТеперь введите возраст')
    await state.update_data(last_name=message.text) #Заносим данные в машину состояний
    await state.set_state(StepsForm.GET_OLD)        #Переходим к следующему шагу

async def get_old(message: Message, bot: Bot, state: FSMContext, apscheduler: AsyncIOScheduler):
    await state.update_data(age=message.text)
    context_data = await state.get_data() # Заносим данные из машины состояний в переменную
    await message.answer(f'Вот ваши данные:\n'\
                         f'Возраст: {context_data["age"]}\n'\
                         f'Имя: {context_data["name"]}\n'\
                         f'Имя: {context_data["last_name"]}\n')
    await state.clear() # Очищаем машину состояний
    apscheduler.add_job(send_message_scheduler, trigger='date', run_date=datetime.now()+ timedelta(seconds=2),
                        kwargs={'chat_id':message.from_user.id})
###################################################


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

    storage = RedisStorage.from_url('redis://127.0.0.1:6379/0') #Создаем хранилище редис для добавлния в диспетчер
    dp = Dispatcher(storage=storage)
    jobstores = { #Прописываем параметры хранилища
        'default': RedisJobStore(jobs_key='dispathed_trips_jobs',
                                run_times_key='dispatched_trips_running',
                                host='127.0.0.1',
                                db=2,
                                port=6379
                                )
    }
    #########
    #Устанавливаем объект шедулер с временной зонной
    scheduler = ContextSchedulerDecorator(AsyncIOScheduler(timezone="Europe/Kiev", jobstores=jobstores))
    scheduler.ctx.add_instance(bot, declared_class=Bot)
    #Регистрируем в шеделере функцию которая отправляет сообщение через 10 минут после старта
    scheduler.add_job(send_message_time, trigger='date', run_date=datetime.now()+timedelta(seconds=10,))
    #Регистрируем шедулер который отправляет сообщение каждый день в определенное время
    scheduler.add_job(send_message_cron, trigger='cron', hour=datetime.now().hour, minute=datetime.now().minute+1,
                      start_date= datetime.now())
    #Регистрируем шедулер который отправляет сообщение каждые 10 секунд
    scheduler.add_job(send_message_interval, trigger='interval', seconds=60)
    scheduler.start() #чтобы все прописанные выше задания выполнились, шедулер нужно запустить
    #############
    #Middleware планировщик
    dp.update.middleware.register(SchedulerMiddleware(scheduler))


    dp.startup.register(start_bot) #Регистрируем хэндлер срабатывающий при запуске
    dp.shutdown.register(stop_bot)

    # Блок формы FSM
    dp.message.register(get_form, Command(commands=['form']))  # Запускаем машину состояний в виде опросника
    dp.message.register(get_name, StepsForm.GET_NAME)  # После введении имени переходим в функцию которая
    dp.message.register(get_lastname, StepsForm.GET_LASTNAME)  # Исполняет дальнейший код и сохраняет данные
    dp.message.register(get_old, StepsForm.GET_OLD)  # В машину состояний
    #Регистрация хэндлера на команду старт
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
