from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from app.handlers.user import router as user_router
from app.handlers.admin import router as admin_router
from app.handlers.yt_handlers import router as yt_router
from app.middleware.rate_limit import RateLimiter
from app.utils.logger import bot_logger
from config import TOKEN
import asyncio
import os
import sys

# Ensure database directory exists
os.makedirs("app/database", exist_ok=True)

async def main():
    try:
        bot_logger.info("Starting bot initialization...")
        bot = Bot(token=TOKEN,
                default=DefaultBotProperties(parse_mode=ParseMode.HTML))
        dp = Dispatcher()
        
        # Add rate limiter middleware
        bot_logger.info("Setting up rate limiter middleware...")
        dp.message.middleware(RateLimiter(rate_limit=5))  # 5 requests per minute
        dp.callback_query.middleware(RateLimiter(rate_limit=10))  # 10 button clicks per minute
        
        # Include routers
        bot_logger.info("Registering handlers...")
        dp.include_routers(admin_router, user_router, yt_router)
        
        # Register startup and shutdown handlers
        dp.startup.register(startup)
        dp.shutdown.register(shutdown)
        
        bot_logger.info("Bot initialization completed. Starting polling...")
        await dp.start_polling(bot)
        
    except Exception as e:
        bot_logger.error(f"Failed to start bot: {str(e)}", exc_info=True)
        sys.exit(1)

async def startup(dispatcher: Dispatcher):
    """Startup handler"""
    try:
        bot_logger.info("Executing startup actions...")
        # Add any startup actions here
        bot_logger.info("Bot started successfully!")
    except Exception as e:
        bot_logger.error(f"Error during startup: {str(e)}", exc_info=True)
        raise

async def shutdown(dispatcher: Dispatcher):
    """Shutdown handler"""
    try:
        bot_logger.info("Executing shutdown actions...")
        # Add any cleanup actions here
        bot_logger.info("Bot shutdown completed.")
    except Exception as e:
        bot_logger.error(f"Error during shutdown: {str(e)}", exc_info=True)
        raise

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        bot_logger.info("Bot stopped by user (KeyboardInterrupt)")
    except Exception as e:
        bot_logger.critical(f"Unexpected error: {str(e)}", exc_info=True)