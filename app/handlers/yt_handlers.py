from aiogram import F,Router
from aiogram.types import Message,CallbackQuery
from aiogram.fsm.context import FSMContext

from ..keyboards.user_kb import youtube_kb
from ..states.states import DownloadState,DownloadStateVideoYT
from ..functions.youtube_func import download_mp3

router = Router()

@router.callback_query(F.data == 'youtube')
async def ythandler(callback:CallbackQuery):
    await callback.message.edit_text(text='What you gonna do?',reply_markup=youtube_kb)

@router.callback_query(F.data == 'yt_mp3')
async def yt_mp3(callback:CallbackQuery, state:FSMContext):
    await callback.message.answer(text='Send link to video.')
    await state.set_state(DownloadState.waiting_for_url) 

@router.callback_query(F.data == 'yt_mp4')
async def yt_mp4(callback:CallbackQuery,state:FSMContext):
    await callback.message.answer(text='Send link to video.')
    await state.set_state(DownloadStateVideoYT.waiting_for_url)

# реализация логики для установки мп3
@router.message(DownloadState.waiting_for_url)
async def process_url(message: Message, state: FSMContext):
    url = message.text.strip()
    if "youtube.com" in url or "youtu.be" in url:
        await download_mp3(message,type='mp3',url=url) 
        await state.clear()
    else:
        await message.answer("It is not YouTube link. Try again and send the youtube link.")

@router.message(DownloadStateVideoYT.waiting_for_url)
async def process_url_webm(message: Message, state: FSMContext):
    url = message.text.strip()
    if "youtube.com" in url or "youtu.be" in url:
        await download_mp3(message,type='mp4',url=url) 
        await state.clear()
    else:
        await message.answer("It is not YouTube link. Try again and send the youtube link.")