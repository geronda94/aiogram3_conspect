from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, ContentType
from aiogram.filters import Filter, Command, Text
import asyncio
from environs import Env
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton,KeyboardButtonPollType
from aiogram.utils.keyboard import ReplyKeyboardBuilder

#Блок инициализации#############################
env = Env()
env.read_env('.env')
TOKEN = env.str('TOKEN')
ADMIN = env.int('ADMIN_ID')
################################################

#Блок с примитивными текстовыми кнопками#######
reply_keyboard = ReplyKeyboardMarkup(
    keyboard=[[ #from aiogram.types import ReplyKeyboardMarkup, KeyboardButton,KeyboardButtonPollType
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
        ]],
    resize_keyboard=True, #Делает кнопки меньше
    one_time_keyboard=True, #Скрывает клавиатуру после нажатия
    input_field_placeholder='Выбери кнопку', #Подсказка в виде надписи в поле ввода
    selective=True #Показывает клавиатуру только тому кто ее вызвал(актуально в группах)
    )
################################################

#Блок с кнопками телефона и геолокацией и викториной
loc_tel_poll_keyboard = ReplyKeyboardMarkup(keyboard =[
    [   #from aiogram.types import ReplyKeyboardMarkup, KeyboardButton,KeyboardButtonPollType
        KeyboardButton(text='Отправить геолокацию', request_location=True),
        KeyboardButton(text='Отправить телефон', request_contact=True)
    ],[
        KeyboardButton(text='Создать викторину', request_poll=KeyboardButtonPollType()) #по умолчанию опрос любого типа
    ]],                                           #Если передать type='quiz' -викторина, type='regular' создает опрос
    resize_keyboard=True,
    one_time_keyboard = True,
    input_field_placeholder ='ТЕСТИРУЮ КНОПКИ',

)
#######################################
#Формируем кнопки через билдер from aiogram.utils.keyboard import ReplyKeyboardBuilder
def get_reply_keyboard_builder():
    keyboard_builder = ReplyKeyboardBuilder()#Создаем объект билдера кнопок
    keyboard_builder.button(text='Кнопка 1') #далее создаем кнопки
    keyboard_builder.button(text='Кнопка 2')
    keyboard_builder.button(text='Кнопка 3')
    keyboard_builder.button(text='Отправить локацию', request_location=True)
    keyboard_builder.button(text='Отправить контакт', request_contact=True)
    keyboard_builder.button(text='Создать викторину', request_poll=KeyboardButtonPollType())
    # для викторин нужен такой импорт from aiogram.types import ReplyKeyboardMarkup, KeyboardButton,KeyboardButtonPollType
    keyboard_builder.adjust(3,2,1) #Указывает в каком ряду сколько кнопок должно быть
    return keyboard_builder.as_markup(resize_keyboard=True, #Указываем настройки клавиатуры
                               one_time_leyboard=True,
                               input_field_placeholder='Показываю кнопки')

########################################

#Хэндлер который будет запускаться при отправке локации
async def get_location(message: Message, bot: Bot):
    await message.answer(f'Ты отправил локацию\n'
                         f'{message.location.latitude}\n'
                         f'{message.location.longitude}')
#Хэндлер на отправку контактов
async def get_contact(message: Message, bot: Bot):
    if message.contact.user_id == message.from_user.id:
        await bot.send_message(ADMIN,text=f'Пользователь {message.from_user.id} отправил телефон '
                               f'\n {message.contact.phone_number}, он под ним зарегистрирован в ТГ')
    else:
        await bot.send_message(ADMIN, text=f'Пользователь {message.from_user.id} отправил телефон '
                                f'\n {message.contact.phone_number}, но это не тот номер к которому привязан аккаунт!')
#Блок стартовых функций#########################
async def start_bot(bot: Bot): #функция срабатывает когда запускается сервер с ботом
    await bot.send_message(ADMIN, text='Бот запущен!')

async def get_start(message: Message, bot: Bot): #Функция срабатывает когда юзер дает команду /start
    await message.answer('Давай начнем!',
                         reply_markup=get_reply_keyboard_builder()) #Отправляет текстовые кнопки прописанные выше
###############################################

#Тело бота#####################################
async def start():
    bot = Bot(token=TOKEN, parse_mode="HTML")
    dp = Dispatcher()
    dp.startup.register(start_bot) #Регистрируем хэндлер срабатывающий при запуске




    dp.message.register(get_start, Command(commands=['start'])) #Регистрируем хэндлер на команду /start
    dp.message.register(get_location, F.content_type == ContentType.LOCATION)
    dp.message.register(get_contact, F.content_type == ContentType.CONTACT)



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


