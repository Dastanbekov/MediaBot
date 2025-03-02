from aiogram import F,Router
from aiogram.types import Message,CallbackQuery
from aiogram.fsm.context import FSMContext

from ..keyboards.user_kb import youtube_kb
from ..states.states import DownloadState,DownloadStateVideoYT
from ..functions.youtube_func import download_media

router = Router()

@router.callback_query(F.data == 'youtube')
async def ythandler(callback:CallbackQuery):
    await callback.message.edit_text(text='What would you like to download?', reply_markup=youtube_kb)

@router.callback_query(F.data == 'yt_mp3')
async def yt_mp3(callback:CallbackQuery, state:FSMContext):
    await callback.message.answer(text='Please send the YouTube video link.')
    await state.set_state(DownloadState.waiting_for_url) 

@router.callback_query(F.data == 'yt_mp4')
async def yt_mp4(callback:CallbackQuery,state:FSMContext):
    await callback.message.answer(text='Please send the YouTube video link.')
    await state.set_state(DownloadStateVideoYT.waiting_for_url)

@router.message(DownloadState.waiting_for_url)
async def process_url(message: Message, state: FSMContext):
    url = message.text.strip()
    if "youtube.com" in url or "youtu.be" in url:
        await download_media(message, media_type='mp3', url=url)
        await state.clear()
    else:
        await message.answer("This is not a valid YouTube link. Please send a valid YouTube URL.")

@router.message(DownloadStateVideoYT.waiting_for_url)
async def process_url_video(message: Message, state: FSMContext):
    url = message.text.strip()
    if "youtube.com" in url or "youtu.be" in url:
        await download_media(message, media_type='mp4', url=url)
        await state.clear()
    else:
        await message.answer("This is not a valid YouTube link. Please send a valid YouTube URL.")