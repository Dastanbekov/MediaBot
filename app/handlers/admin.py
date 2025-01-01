from aiogram.types import Message,CallbackQuery
from aiogram.filters import Command
from aiogram import Router,F

from ..keyboards.admin_kb import main

admin = Router()

ADMIN_ID = 6807370883
@admin.message(Command('admin'))
async def admin_cmd(message:Message):
    if ADMIN_ID == message.from_user.id:
        await message.answer(text='You entered into admin panel.',reply_markup=main)

@admin.callback_query(F.data == 'chikibambonito')
async def chikibambonito(callback:CallbackQuery):
    await callback.message.edit_text(text='Chikibambonito!')
