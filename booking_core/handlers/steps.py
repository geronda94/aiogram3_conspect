from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from booking_core.keyboards.edit_keyboards import delete_button
from booking_core.keyboards.service_button import kb_get_services, kb_get_add_services
from booking_core.keyboards.text_button import get_button_name
from booking_core.keyboards.user_buttons import kb_get_date, kb_get_time
from booking_core.other.data_for_user import get_data_state
from booking_core.other.db_request import Request
from booking_core.other.state_user import States


async def handle_add_services(call: CallbackQuery, state: FSMContext):
    add = []
    data = await state.get_data()

    if 'add_serv' in data:
        add = data['add_serv']

    add_service = call.data.split('=')[1].split('|')[0]
    add_service_price = call.data.split('=')[1].split('|')[1]

    add.append({add_service: add_service_price})
    await state.update_data(add_serv=add)
    keyboard = await delete_button(call.message.reply_markup, call.data)
    await call.message.edit_text(await get_data_state(state), reply_markup=keyboard)


async def get_add_service(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    date_needed = data['date']
    time_needed = data['time']
    service = call.data.split('=')[-1].split('|')[0]
    price = call.data.split('=')[-1].split('|')[1]
    await state.update_data(service=service, price=price)
    await state.set_state(States.state_add_service)

    await call.message.edit_text(f"Выбранная дата: <b>{date_needed}</b>\r\n"
                                 f"Выбранное время: <b>{time_needed}</b>\r\n"
                                 f"Ваша стрижка: <b>{service}  {price}</b>\r\n"
                                 f"Я могу вам предложить одну из наших сопутствующих услуг:",
                                 reply_markup=await kb_get_add_services())


async def get_service(call: CallbackQuery, state: FSMContext, request: Request):
    data = await state.get_data()
    date_needed = data['date']
    time_needed = call.data.split('=')[1]
    await state.update_data(time=time_needed)
    await state.set_state(States.state_service)
    await call.message.edit_text(f"Выбранная дата <b>{date_needed}</b> \r\nВыбранное время: <b>{time_needed}</b>"
                                 f"\r\nТеперь выберите стрижку:",
                                 reply_markup=await kb_get_services())
    await request.db_change_statuse('process', date_needed, time_needed)


async def get_time(call: CallbackQuery, state: FSMContext, request: Request):
    data_needed = call.data.split('=')[1]
    await call.message.edit_text(f'Выбранная дата <b>{data_needed}</b>,\r\n'
                                 f'Теперь выберите желаемое время:  ',
                                 reply_markup=await kb_get_time(request, data_needed))
    await state.set_state(States.state_time)
    await state.update_data(date=data_needed)


async def get_data(message: Message, state: FSMContext, request: Request):
    await message.answer(f'Приятно познакомиться {message.text}, выберите время:  ',
                         reply_markup=await kb_get_date(request))
    await state.update_data(name=message.text)
    await state.set_state(States.state_date)


async def get_name(message: Message, state: FSMContext, request: Request):
    await message.answer('Привет, я помощник салона красоты. Как я могу к тебе обращаться?',
                         reply_markup=await get_button_name(message.from_user.first_name))
    await state.set_state(States.state_name)
    await request.get_user(id_user=message.from_user.id, username=message.from_user.username,
                           first_name=message.from_user.first_name, last_name=message.from_user.last_name)
