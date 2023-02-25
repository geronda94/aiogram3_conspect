from typing import List
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from booking_core.other.db_request import Request

async def kb_get_time(request: Request, data_needed):
    lst_date = await request.db_get_time(data_needed)
    time_list: List[InlineKeyboardButton] = []

    buttons: List = []


    for el_time in lst_date:
        if len(time_list) == 3:
            buttons.append(time_list)
            time_list = []

        button = InlineKeyboardButton(text=el_time, callback_data=f'reserve_time={el_time}')
        time_list.append(button)

    buttons.append(time_list)
    return InlineKeyboardMarkup(inline_keyboard=buttons)


async def kb_get_date(request: Request):
    list_date = await request.db_get_date()
    time_list: List[InlineKeyboardButton] = []

    buttons = []

    for el_date in list_date:
        if len(time_list) == 3:
            buttons.append(time_list)
            time_list = []

        button = InlineKeyboardButton(text=el_date, callback_data =f'reverse_date={el_date}')
        time_list.append(button)

    buttons.append(time_list)

    return InlineKeyboardMarkup(inline_keyboard=buttons)

