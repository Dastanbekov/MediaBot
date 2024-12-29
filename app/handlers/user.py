from aiogram.types import Message,CallbackQuery
from aiogram import Router,F
from aiogram.filters import Command,CommandStart

from ..keyboards.user_kb import main
user = Router()

@user.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(f'Hello User!', reply_markup=main)

@user.callback_query(F.data == 'menu')
async def callback_main(callback: CallbackQuery):
    await callback.message.answer(text='Choose the option:', reply_markup=main) 
    