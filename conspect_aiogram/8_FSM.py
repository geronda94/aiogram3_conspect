from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, ContentType
from aiogram.filters import Filter, Command, Text
import asyncio
from environs import Env
import logging #импортируем библиотеку логирования
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

#Блок инициализации#############################
env = Env()                                    #
env.read_env('.env')                           #
TOKEN = env.str('TOKEN')                       #
ADMIN = env.int('ADMIN_ID')                    #
################################################

class StepsForm(StatesGroup):
    GET_NAME = State()
    GET_LASTNAME = State()
    GET_OLD = State()

async def get_form(message: Message, state: FSMContext):
    await message.answer(f'{message.from_user.first_name}, начинаем заполнять анкету. Введите свое имя')
    await state.set_state(StepsForm.GET_NAME)


async def get_name(message: Message, state: FSMContext):
    await message.answer(f'Твоё имя: \r\n {message.text}\r\n\nТеперь введите фамилию')
    await state.update_data(name=message.text)
    await state.set_state(StepsForm.GET_LASTNAME)

async def get_lastname(message: Message, state: FSMContext):
    await message.answer(f'Твоя фамилия: \r\n {message.text}\r\n\nТеперь введите возраст')
    await state.update_data(last_name=message.text)
    await state.set_state(StepsForm.GET_OLD)

async def get_old(message: Message, state: FSMContext):
    await message.answer(f'Вам {message.text}')
    await state.update_data(age=message.text)






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
    dp.startup.register(start_bot) #Регистрируем хэндлер срабатывающий при запуске
    dp.shutdown.register(stop_bot)

    #Блок формы FSM
    dp.message.register(get_form, Command(commands=['form']))
    dp.message.register(get_name, StepsForm.GET_NAME)
    dp.message.register(get_lastname, StepsForm.GET_LASTNAME)
    dp.message.register(get_old, StepsForm.GET_OLD)



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


