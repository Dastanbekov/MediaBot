from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                           InlineKeyboardMarkup, InlineKeyboardButton)

main = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Chikibambonito!', callback_data='chikibambonito')],
    [InlineKeyboardButton(text='Statistics',callback_data='statistics')]
])