from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, ContentType, BotCommand, BotCommandScopeDefault
from aiogram.types import FSInputFile, InputMediaPhoto, InputMediaVideo
from aiogram.filters import Filter, Command, Text
import asyncio
from environs import Env
import logging #импортируем библиотеку логирования

#Блок инициализации#############################
env = Env()                                    #
env.read_env('.env')                           #
TOKEN = env.str('TOKEN')                       #
ADMIN = env.int('ADMIN_ID')                    #
################################################
#Блок с хэндлерами на отправку медиафайлов
async def send_audio(message: Message, bot: Bot):
    audio = FSInputFile(path=f'media_files/audio.m4a', filename='Какой-то звук')
    await message.answer_audio(audio=audio)

async def send_document(message: Message, bot: Bot):
    document = FSInputFile(path=f'media_files/document.pdf')
    await message.answer_document(document=document, caption='It`s document')

async def send_mediagroup(message: Message, bot: Bot):
    photo1 = InputMediaPhoto(type='photo', media=FSInputFile(path='media_files/photo_1.jpg'), caption='MEDIAGROUP_photo1')
    photo2 = InputMediaPhoto(type='photo', media=FSInputFile(path='media_files/photo_2.PNG'), caption='MEDIAGROUP_photo2')
    video = InputMediaVideo(type='video', media=FSInputFile(path='media_files/video.mp4'), caption='MEDIAGROUP_video')
    media = [photo1, photo2, video]
    await message.answer_media_group( media)

async def send_photo(message: Message, bot: Bot):
    photo = FSInputFile(path='media_files/photo_1.jpg')
    await message.answer_photo(photo, caption='It`s Photo')

async def send_video(message: Message, bot:Bot):





#Блок стартовых функций#########################
#Установка команд в меню при старте
async def set_commands(bot: Bot):
    commands = [
        BotCommand(command='start', description='👻 Начало'),
        BotCommand(command='help', description='Описание Бота'),
        BotCommand(command='inline', description='Карточки товаров'),
        BotCommand(command='form', description='Заполнить анкету'),
        BotCommand(command='end_block', description='----------------'),

        #Блок команд на отправку медиа файлов
            BotCommand(command='send_photo', description='Отправить фото'),
        BotCommand(command='send_video', description='Отправить видео'),
        BotCommand(command='send_audio', description='Отправить аудио'),
        BotCommand(command='send_document', description='Отправить документ'),
        BotCommand(command='send_mediagroup', description='Отправить несколько медиафайлов'),
        BotCommand(command='send_sticker', description='Отправить стикер'),
        BotCommand(command='send_videonote', description='Отправить видеосообщение'),
        BotCommand(command='send_voice', description='Отправить голосового сообщение'),
        #######################################
    ]

    await bot.set_my_commands(commands, BotCommandScopeDefault()) #Скоп по умолчанию|ПОказывает команды всем

async def start_bot(bot: Bot): #функция срабатывает когда запускается сервер с ботом
    await bot.send_message(ADMIN, text='Бот запущен!')
    await set_commands(bot)

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


    #Регистрация хэндлеров на отправку медиафайлов
    dp.message.register(get_start, Command(commands=['start'])) #Регистрируем хэндлер на команду /start
    dp.message.register(send_audio, Command(commands=['send_audio'])) #Регистрируем хэндлер на команду /start
    dp.message.register(send_document, Command(commands=['send_document'])) #Регистрируем хэндлер на команду /start
    dp.message.register(send_mediagroup, Command(commands=['send_mediagroup'])) #Регистрируем хэндлер на команду /start
    dp.message.register(send_photo, Command(commands=['send_photo'])) #Регистрируем хэндлер на команду /start





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


