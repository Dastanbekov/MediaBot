from aiogram.types import Message,CallbackQuery
from aiogram import Router,F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext

from ..keyboards.user_kb import main
user = Router()

@user.message(CommandStart())
async def cmd_start(message: Message,state:FSMContext):
    await state.clear()
    await message.answer(f'Hello User!', reply_markup=main)

@user.callback_query(F.data == 'menu')
async def callback_main(callback: CallbackQuery,state:FSMContext):
    await state.clear()
    await callback.message.edit_text(text='Choose the option:', reply_markup=main) 
    