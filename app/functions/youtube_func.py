import os
from aiogram.types import Message, FSInputFile
import yt_dlp

async def download_mp3(message: Message, bot):
    """Скачивает MP3 по URL из сообщения и отправляет пользователю."""
    url = message.text.strip()
    base_filename = f'{message.chat.id}_audio'

    opts = {
        'format': 'bestaudio/best',
        'outtmpl': base_filename, 
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    try:
        await message.reply("⏳ Начинаю загрузку и конвертацию MP3. Подождите...")
        with yt_dlp.YoutubeDL(opts) as ytdl:
            ytdl.download([url])
    except Exception as e:
        print(f'exception{e}')
    
    finall_audio = FSInputFile(path=f'{base_filename}.mp3')
    await message.answer_audio(audio=finall_audio)
    os.remove(f'{base_filename}.mp3')
