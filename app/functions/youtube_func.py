import os
from aiogram import F
from aiogram.types import Message, FSInputFile
from aiogram.fsm.context import FSMContext
import yt_dlp

async def download_mp3(message: Message, type):
    """Скачивает MP3 по URL из сообщения и отправляет пользователю."""
    url = message.text.strip()
    base_filename = f'{message.chat.id}'
    if type == 'mp3':
        opts = {
            'format': 'bestaudio/best',
            'outtmpl': base_filename, 
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }
    else:
        opts ={
            'outtmpl':base_filename,
        }
        
    try:
        await message.reply("⏳ Wait a second...")
        with yt_dlp.YoutubeDL(opts) as ytdl:
            ytdl.download([url])
    except Exception:
        await message.reply(text='Incorrect link,try again')
        print(f'Something goes wrong...')
    if type == 'mp3':
        final_audio = FSInputFile(path=f'{base_filename}.mp3')
        await message.answer_audio(audio=final_audio)
        os.remove(f'{base_filename}.mp3')
    else:
        final_video = FSInputFile(path=f'{base_filename}.webm')
        await message.answer_video(video=final_video)
        os.remove(f'{base_filename}.webm')