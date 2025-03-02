from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from app.handlers.user import router as user_router
from app.handlers.admin import router as admin_router
from app.handlers.yt_handlers import router as yt_router
from config import TOKEN
import asyncio
import os

# Ensure database directory exists
os.makedirs("app/database", exist_ok=True)

async def main():
    bot = Bot(token=TOKEN,
              default=DefaultBotProperties(parse_mode=ParseMode.HTML)) #parse mode for use html tags like <b>  and e.t.c
    dp = Dispatcher()
    # dp.include_router(....) later
    dp.include_routers(admin_router, user_router, yt_router)
    dp.startup.register(startup)
    dp.shutdown.register(shutdown)
    await dp.start_polling(bot)

async def startup(dispatcher: Dispatcher):
    print('Starting')

async def shutdown(dispatcher: Dispatcher):
    print('Shutting Down...')


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass