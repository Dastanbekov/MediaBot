from aiogram.types import Message,CallbackQuery
from aiogram import Router,F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext

from ..keyboards.user_kb import main,main_keyboard,go_back,youtube_kb
user = Router()

@user.message(CommandStart())
async def cmd_start(message: Message,state:FSMContext):
    await state.clear()
    await message.answer('Hello User!', reply_markup=main_keyboard)
    await message.answer('Choose the option:',reply_markup=main)

@user.callback_query(F.data == 'menu')
async def callback_main(callback: CallbackQuery,state:FSMContext):
    await state.clear()
    await callback.message.edit_text(text='Choose the option:', reply_markup=main)

#help function(later i will care about dry principle)
@user.callback_query(F.data == 'about') 
async def callback_about(callback:CallbackQuery):
    await callback.message.edit_text(text='It is example of about us text.There i will describe this app', reply_markup=go_back)
    
@user.message(F.text == '🧠How to use?')
async def message_about(message:Message):
    await message.answer(text='It is example of about us text.There i will describe this app', reply_markup=go_back)

@user.message(F.text == '🎈Youtube')
async def ythandler_text(message:Message):
    await message.answer(text='What you gonna do?',reply_markup=youtube_kb)

