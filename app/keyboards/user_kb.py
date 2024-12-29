from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                           InlineKeyboardMarkup, InlineKeyboardButton)
from aiogram.utils.keyboard import InlineKeyboardBuilder

main = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Youtube', callback_data='youtube')],
    [InlineKeyboardButton(text='About Application',callback_data='about')],
])

youtube_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Download Mp3',callback_data='yt_mp3')],
    [InlineKeyboardButton(text='Download Mp4', callback_data='yt_mp4')],
    [InlineKeyboardButton(text='Menu',callback_data='menu')]
])

