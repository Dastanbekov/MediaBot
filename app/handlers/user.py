from aiogram.types import Message,CallbackQuery
from aiogram import Router,F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from ..keyboards.user_kb import main,main_keyboard,go_back,youtube_kb
from ..database.db import Database

router = Router()
db = Database()

@router.message(Command("start"))
async def cmd_start(message: Message):
    # Add user to database
    await db.add_user(
        user_id=message.from_user.id,
        username=message.from_user.username,
        first_name=message.from_user.first_name,
        last_name=message.from_user.last_name
    )
    
    await message.answer(
        text=(
            f"👋 Welcome, {message.from_user.first_name}!\n\n"
            "I'm a Media Download Bot that can help you download content from various platforms.\n"
            "Choose an option from the menu below:"
        ),
        reply_markup=main
    )

@router.message(Command("help"))
async def cmd_help(message: Message):
    await message.answer(
        text=(
            "🤖 Bot Commands:\n\n"
            "/start - Start the bot\n"
            "/help - Show this help message\n"
            "/menu - Show main menu\n\n"
            "📝 How to use:\n"
            "1. Choose a platform (YouTube, etc.)\n"
            "2. Select the format you want to download\n"
            "3. Send the link to the content\n"
            "4. Wait for the download to complete"
        ),
        reply_markup=main
    )

@router.message(Command("menu"))
async def cmd_menu(message: Message):
    await message.answer(
        text="Choose an option from the menu:",
        reply_markup=main
    )

@router.callback_query(F.data == "menu")
async def menu(callback: CallbackQuery):
    await callback.message.edit_text(
        text="Choose an option from the menu:",
        reply_markup=main
    )

@router.callback_query(F.data == "about")
async def about(callback: CallbackQuery):
    await callback.message.edit_text(
        text=(
            "ℹ️ About this bot:\n\n"
            "This is a media download bot that helps you download content from various platforms.\n\n"
            "🔥 Features:\n"
            "• Download YouTube videos as MP3/MP4\n"
            "• High-quality downloads\n"
            "• Fast processing\n\n"
        ),
        reply_markup=main
    )

@router.message(F.text == "🧠How to use?")
async def message_about(message: Message):
    await message.answer(
        text=(
            "📝 How to use this bot:\n\n"
            "1. Choose a platform (YouTube, etc.)\n"
            "2. Select the format you want to download\n"
            "3. Send the link to the content\n"
            "4. Wait for the download to complete\n\n"
            "For more help, use the /help command."
        ),
        reply_markup=go_back
    )

@router.message(F.text == "🎈Youtube")
async def ythandler_text(message: Message):
    await message.answer(
        text="What would you like to download?",
        reply_markup=youtube_kb
    )

