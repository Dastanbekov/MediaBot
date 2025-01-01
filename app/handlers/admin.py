from aiogram.types import Message,CallbackQuery
from aiogram.filters import Command
from aiogram import Router,F

from ..keyboards.admin_kb import main

admin = Router()

ADMIN_ID = 68073708833
@admin.message(Command('admin'))
async def admin_cmd(message:Message):
    if ADMIN_ID == message.from_user.id:
        await message.answer(text='You entered into admin panel.',reply_markup=main)

@admin.callback_query(F.data == 'statistics')
async def chikibambonito(callback:CallbackQuery):
    await callback.message.edit_text(text='function to get stats; 1.amount of people registered 2. how much usages was in youtube downloader')


