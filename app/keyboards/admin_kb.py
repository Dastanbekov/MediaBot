from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                           InlineKeyboardMarkup, InlineKeyboardButton)

main = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Statistics',callback_data='statistics')]
])