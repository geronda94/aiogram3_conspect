from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from booking_core.keyboards.text_button import get_button_name
from booking_core.keyboards.user_buttons import kb_get_date, kb_get_time
from booking_core.other.db_request import Request
from booking_core.other.state_user import States



async def get_time(call: CallbackQuery, state: FSMContext, request: Request):
    data_needed = call.data.split('=')[1]
    await call.message.edit_text(f'Выбранная дата <b>{data_needed}</b>,\r\n'
                                 f'Теперь выберите желаемое время:  ',
                                   reply_markup= await kb_get_time(request, data_needed))
    await state.set_state(States.state_time)
    await state.update_data(date=data_needed)


async def get_data(message: Message, state: FSMContext, request: Request):
    await message.answer(f'Приятно познакомиться {message.text}, выберите время:  ',
                         reply_markup= await kb_get_date(request))
    await state.update_data(name=message.text)
    await state.set_state(States.state_date)




async def get_name(message: Message, state: FSMContext, request:Request):
    await message.answer('Привет, я помощник салона красоты. Как я могу к тебе обращаться?',
                         reply_markup=await get_button_name(message.from_user.first_name))
    await state.set_state(States.state_name)
    await request.get_user(id_user=message.from_user.id, username=message.from_user.username,
                           first_name=message.from_user.first_name, last_name=message.from_user.last_name)
