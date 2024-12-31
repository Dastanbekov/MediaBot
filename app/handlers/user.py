from aiogram.types import Message,CallbackQuery
from aiogram import Router,F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext

from ..keyboards.user_kb import main,main_keyboard
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
    
# @user.message()
# async def fallback_message(message:Message):
#     await message.answer("Sorry i can't understand you. Use /start command.")\