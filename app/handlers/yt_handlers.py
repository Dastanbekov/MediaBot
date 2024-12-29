from aiogram import F,Router
from aiogram.types import Message,CallbackQuery

from ..keyboards.user_kb import youtube_kb

router = Router()

@router.callback_query(F.data == 'youtube')
async def ythandler(callback:CallbackQuery):
    await callback.message.answer(text='What you gonna do?',reply_markup=youtube_kb)

@router.callback_query(F.data == 'yt_mp3')
async def yt_mp3(callback:CallbackQuery):
    await callback.message.answer(text='This will be download mp3')

@router.callback_query(F.data == 'yt_mp4')
async def yt_mp4(callback:CallbackQuery):
    await callback.message.answer(text='This will be download mp4')
