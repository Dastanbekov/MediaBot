from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from ..keyboards.admin_kb import admin_kb, broadcast_kb
from ..states.states import BroadcastState
from ..database.db import Database
from config import ADMIN_ID

router = Router()
db = Database()

@router.message(Command("admin"))
async def admin_panel(message: Message):
    if message.from_user.id != ADMIN_ID:
        return
    
    stats = await db.get_user_stats()
    text = (
        "👨‍💼 Admin Panel\n\n"
        f"📊 Statistics:\n"
        f"Total users: {stats['total_users']}\n"
        f"Active users: {stats['active_users']}\n"
        f"Inactive users: {stats['inactive_users']}\n"
    )
    await message.answer(text, reply_markup=admin_kb)

@router.callback_query(F.data == "broadcast")
async def broadcast_menu(callback: CallbackQuery):
    if callback.from_user.id != ADMIN_ID:
        return
    
    await callback.message.edit_text(
        "📢 Broadcast Menu\n\n"
        "Choose the type of broadcast message:",
        reply_markup=broadcast_kb
    )

@router.callback_query(F.data == "admin_panel")
async def back_to_admin(callback: CallbackQuery):
    if callback.from_user.id != ADMIN_ID:
        return
    
    stats = await db.get_user_stats()
    text = (
        "👨‍💼 Admin Panel\n\n"
        f"📊 Statistics:\n"
        f"Total users: {stats['total_users']}\n"
        f"Active users: {stats['active_users']}\n"
        f"Inactive users: {stats['inactive_users']}\n"
    )
    await callback.message.edit_text(text, reply_markup=admin_kb)

@router.callback_query(F.data == "broadcast_text")
async def start_broadcast(callback: CallbackQuery, state: FSMContext):
    if callback.from_user.id != ADMIN_ID:
        return
    
    await callback.message.answer(
        "📝 Send me the message you want to broadcast to all users.\n"
        "You can use HTML formatting."
    )
    await state.set_state(BroadcastState.waiting_for_message)

@router.message(BroadcastState.waiting_for_message)
async def process_broadcast(message: Message, state: FSMContext):
    if message.from_user.id != ADMIN_ID:
        return
    
    await state.clear()
    status_msg = await message.answer("📤 Broadcasting message...")
    
    users = await db.get_all_users()
    success_count = 0
    fail_count = 0
    
    for user_id in users:
        try:
            await message.bot.send_message(
                chat_id=user_id,
                text=message.html_text or message.text,
                parse_mode="HTML"
            )
            success_count += 1
        except Exception as e:
            print(f"Failed to send message to {user_id}: {e}")
            await db.deactivate_user(user_id)
            fail_count += 1
    
    # Log the broadcast
    await db.log_broadcast(
        message=message.text,
        sent_by=message.from_user.id,
        success_count=success_count,
        fail_count=fail_count
    )
    
    await status_msg.edit_text(
        f"✅ Broadcast completed!\n\n"
        f"📊 Statistics:\n"
        f"✓ Successfully sent: {success_count}\n"
        f"✗ Failed: {fail_count}\n"
        f"📱 Total reached: {success_count + fail_count}"
    )

@router.callback_query(F.data == "user_stats")
async def show_stats(callback: CallbackQuery):
    if callback.from_user.id != ADMIN_ID:
        return
    
    stats = await db.get_user_stats()
    await callback.message.edit_text(
        f"📊 User Statistics\n\n"
        f"👥 Total users: {stats['total_users']}\n"
        f"✅ Active users: {stats['active_users']}\n"
        f"❌ Inactive users: {stats['inactive_users']}",
        reply_markup=admin_kb
    )


