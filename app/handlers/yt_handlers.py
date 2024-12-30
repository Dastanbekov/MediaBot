from aiogram import F,Router
from aiogram.types import Message,CallbackQuery
from aiogram.fsm.context import FSMContext

from ..keyboards.user_kb import youtube_kb
from ..states.states import DownloadState
from ..functions.youtube_func import download_mp3
router = Router()

@router.callback_query(F.data == 'youtube')
async def ythandler(callback:CallbackQuery):
    await callback.message.answer(text='What you gonna do?',reply_markup=youtube_kb)

@router.callback_query(F.data == 'yt_mp3')
async def yt_mp3(callback:CallbackQuery, state:FSMContext):
    await callback.message.answer(text='Send link to video.')
    await state.set_state(DownloadState.waiting_for_url) 


@router.callback_query(F.data == 'yt_mp4')
async def yt_mp4(callback:CallbackQuery):
    await callback.message.answer(text='This will be download mp4')


# реализация логики для установки мп3
@router.message(DownloadState.waiting_for_url)
async def process_url(message: Message, state: FSMContext, bot):
    url = message.text.strip()
    if "youtube.com" in url or "youtu.be" in url:
        await message.answer(f"Начинаю загрузку видео по URL: {url}...")
        await download_mp3(message, bot) 
        await state.clear()
    else:
        await message.answer("Это не похоже на ссылку YouTube. Попробуйте ещё раз.")