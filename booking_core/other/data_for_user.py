from aiogram.fsm.context import FSMContext


async def get_data_state(state: FSMContext):
    data = await state.get_data()
    date_needed = data['data']
    time_needed = data['time']
    service = data['service']
    price = data['price']

    text_user = f"Выбранная дата: <b>{date_needed}</b>\r\nВыбранное время: <b>{time_needed}</b>\r\n" \
                f"Ваша стрижка: <b>{service}</b> <b>{price}</b>$\r\n"
    total_price = int(price)

    if 'add_serv' in data:
        dict_data = data['add_serv']

        text_user += f'\r\nСопутствующие услуги: '

        for el_data in dict_data:
            for key, value in el_data.items():
                text_user += f'\r\n<b>{key} {value} $</b>'
                total_price += int(value)

        text_user += f"\r\n\r\nСумма к оплате: <b>{total_price}$</b>"

    return text_user




