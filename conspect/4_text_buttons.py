from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, ContentType
from aiogram.filters import Filter, Command, Text
import asyncio
from environs import Env
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton,KeyboardButtonPollType


#Блок инициализации#############################
env = Env()
env.read_env('.env')
TOKEN = env.str('TOKEN')
ADMIN = env.int('ADMIN_ID')
################################################

#Блок с примитивными текстовыми кнопками#######
reply_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='ряд 1, кнопка 1'),
            KeyboardButton(text='ряд 1, кнопка 2'),
            KeyboardButton(text='ряд 1, кнопка 3'),
            KeyboardButton(text='ряд 1, кнопка 4')
        ],[
            KeyboardButton(text='ряд 2, кнопка 1'),
            KeyboardButton(text='ряд 2, кнопка 2'),
            KeyboardButton(text='ряд 2, кнопка 3')
        ],[
            KeyboardButton(text='ряд 3, кнопка 1'),
            KeyboardButton(text='ряд 3, кнопка 2')
        ]
    ], resize_keyboard=True, #Делает кнопки меньше
       one_time_keyboard=True #Скрывает клавиатуру после нажатия
)
################################################

#Блок стартовых функций#########################
async def start_bot(bot: Bot): #функция срабатывает когда запускается сервер с ботом
    await bot.send_message(ADMIN, text='Бот запущен!')

async def get_start(message: Message, bot: Bot): #Функция срабатывает когда юзер дает команду /start
    await message.answer('Давай начнем!',
                         reply_markup=reply_keyboard) #Отправляет текстовые кнопки прописанные выше
###############################################

#Тело бота#####################################
async def start():
    bot = Bot(token=TOKEN, parse_mode="HTML")
    dp = Dispatcher()
    dp.startup.register(start_bot) #Регистрируем хэндлер срабатывающий при запуске




    dp.message.register(get_start, Command(commands=['start'])) #Регистрируем хэндлер на команду /start





    try:
        #Начало сессии
        await dp.start_polling(bot)
    finally:
        #Закрываем сессию
        await bot.session.close()
###############################################


#Запускаем Бота################################
if __name__ =="__main__":
    asyncio.run(start())


