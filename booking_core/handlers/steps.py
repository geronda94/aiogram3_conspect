from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from booking_core.keyboards.text_button import get_button_name
from booking_core.other.db_request import Request
from booking_core.other.state_user import States


async def get_data(message: Message, state: FSMContext, request: Request):
    await message.answer(f'Приятно познакомиться {message.text}, выберите время:  ')
    await state.update_data(name=message.text)
    await state.set_state(States.state_date)

    print(await state.get_data())



async def get_name(message: Message, state: FSMContext, request:Request):
    await message.answer('Привет, я помощник салона красоты. Как я могу к тебе обращаться?', reply_markup=await get_button_name(message.from_user.first_name))
    await state.set_state(States.state_name)
