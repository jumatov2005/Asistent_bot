import asyncio
import logging
import sys
import os
from aiogram import Bot, Dispatcher, types
from config import BOT_TOKEN
from database.db import db
from handlers import start, user, admin, super_admin
import middlewares

# Logs papkasi
if not os.path.exists("logs"):
    os.makedirs("logs")

async def main():
    """
    Botni ishga tushirish (Final Production Version with PostgreSQL)
    """
    # Logging Configuration
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
        handlers=[
            logging.FileHandler("logs/bot_errors.log", encoding='utf-8'),
            logging.StreamHandler(sys.stdout)
        ]
    )
    
    logger = logging.getLogger(__name__)
    logger.info("Bot starting up...")

    # DB Connection (AsyncPG Pool)
    try:
        await db.create()
        logger.info("Database connection pool established.")
    except Exception as e:
        logger.critical(f"Database Initialization Failed: {e}")
        return

    # Bot Setup
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()
    
    # Middleware Setup
    middlewares.setup(dp)
    logger.info("Middlewares configured.")

    # Routers Setup
    dp.include_router(start.router)
    dp.include_router(user.router)
    dp.include_router(admin.router)
    dp.include_router(super_admin.router)
    logger.info("Routers included.")

    # Global Error Handler
    @dp.error()
    async def global_error_handler(event: types.ErrorEvent):
        logger.error(f"Critical Error in Update {event.update}: {event.exception}", exc_info=True)

    # Webhook Cleanup
    await bot.delete_webhook(drop_pending_updates=True)
    logger.info("Webhook cleaned updates dropped.")
    
    logger.info("Bot polling started!")
    try:
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    except Exception as e:
        logger.critical(f"Polling crashed: {e}")
    finally:
        await db.close()
        await bot.session.close()
        logger.info("Bot session and DB pool closed.")

if __name__ == "__main__":
    try:
        if sys.platform == 'win32':
            asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
