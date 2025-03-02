import os
from aiogram.types import Message, FSInputFile
import yt_dlp

async def download_media(message: Message, media_type: str, url: str):
    """Downloads media from YouTube URL and sends it to the user.
    
    Args:
        message (Message): Telegram message object
        media_type (str): Type of media to download ('mp3' or 'mp4')
        url (str): YouTube URL
    """
    base_filename = f'{message.chat.id}'
    
    if media_type == 'mp3':
        opts = {
            'format': 'bestaudio/best',
            'outtmpl': base_filename,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '320',  # Highest quality
            }],
            'source_address': '0.0.0.0',
            'quiet': True,
            'no_warnings': True,
        }
    else:  # mp4
        opts = {
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
            'outtmpl': base_filename,
            'merge_output_format': 'mp4',
            'source_address': '0.0.0.0',
            'quiet': True,
            'no_warnings': True,
        }

    try:
        status_message = await message.reply("⏳ Downloading media, please wait...")
        
        with yt_dlp.YoutubeDL(opts) as ytdl:
            info = ytdl.extract_info(url, download=True)
            title = info.get('title', 'video')
        
        if media_type == 'mp3':
            final_file = FSInputFile(
                path=f'{base_filename}.mp3',
                filename=f'{title}.mp3'
            )
            await status_message.delete()
            await message.answer_audio(
                audio=final_file,
                title=title,
                performer=info.get('uploader', 'Unknown')
            )
            os.remove(f'{base_filename}.mp3')
        else:
            final_file = FSInputFile(
                path=f'{base_filename}.mp4',
                filename=f'{title}.mp4'
            )
            await status_message.delete()
            await message.answer_video(
                video=final_file,
                caption=f"📹 {title}"
            )
            os.remove(f'{base_filename}.mp4')
            
    except yt_dlp.utils.DownloadError as e:
        await message.reply(f"❌ Download failed: {str(e)}")
    except Exception as e:
        await message.reply(f"❌ An error occurred: {str(e)}")
    finally:
        # Cleanup any remaining files
        for ext in ['.mp3', '.mp4', '.webm', '.m4a', '.part']:
            if os.path.exists(f'{base_filename}{ext}'):
                try:
                    os.remove(f'{base_filename}{ext}')
                except:
                    pass