from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

admin_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="📢 Broadcast Message", callback_data="broadcast")],
    [InlineKeyboardButton(text="📊 User Statistics", callback_data="user_stats")],
    [InlineKeyboardButton(text="🔙 Back to Menu", callback_data="menu")]
])

broadcast_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="📝 Send Text Message", callback_data="broadcast_text")],
    [InlineKeyboardButton(text="🔙 Back to Admin Panel", callback_data="admin_panel")]
])