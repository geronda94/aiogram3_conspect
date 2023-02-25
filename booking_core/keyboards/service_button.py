from typing import List

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


async def kb_get_services():
    dict_services = {"Пикси":100, "Боб":200,"Милитари":120, "Гарсон":180, "Гранж":220,
        "Аврова":250, "Голливуд":300,"Итальянка":270,"Ассиметрия":260,
        "Лесенка":240,"Шегги":315,"Волчица":330 }

    time_list: List[InlineKeyboardButton] = []
    buttons: List = []


    for k, v in dict_services.items():
        if len(time_list) == 3:
            buttons.append(time_list)
            time_list =[]

        button = InlineKeyboardButton(text=f'{k}--{v}$', callback_data=f"services={k}|{v}")
        time_list.append(button)

    buttons.append(time_list)
    return InlineKeyboardMarkup(inline_keyboard=buttons)












