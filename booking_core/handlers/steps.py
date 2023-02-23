from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from booking_core.other.db_request import Request
from booking_core.other.state_user import States

async def get_name(message: Message, state: FSMContext, request:Request):
    await message.answer('Привет, я помощник салона красоты. Как я могу к тебе обращаться?')
    await state.set_state(States.state_name)
