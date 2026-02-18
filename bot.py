import asyncio
import signal
import sys
import uvloop
from pyrogram import Client
from config import API_ID, API_HASH, BOT_TOKEN
from core.router import register_handlers
from core.scheduler import start_scheduler
from database.indexes import create_indexes
from utils.logger import logger


# Use ultra fast event loop
asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


class ChatFightBot:

    def __init__(self):
        self.app = Client(
            "chatfight-pro",
            api_id=API_ID,
            api_hash=API_HASH,
            bot_token=BOT_TOKEN,
            workers=100,               # high concurrency
            sleep_threshold=30
        )

    async def start(self):
        logger.info("Starting ChatFight Pro...")

        # Register command + callback handlers
        register_handlers(self.app)

        # Create Mongo indexes (background safe)
        await create_indexes()

        # Start scheduler (daily/weekly reset)
        start_scheduler()

        # Start Pyrogram
        await self.app.start()

        me = await self.app.get_me()
        logger.info(f"Bot started as @{me.username}")

    async def stop(self):
        logger.info("Stopping ChatFight Pro...")
        await self.app.stop()
        logger.info("Bot stopped successfully.")

    async def run(self):
        await self.start()

        # Graceful shutdown handling
        loop = asyncio.get_running_loop()

        stop_event = asyncio.Event()

        def _signal_handler():
            logger.info("Shutdown signal received.")
            stop_event.set()

        for sig in (signal.SIGINT, signal.SIGTERM):
            loop.add_signal_handler(sig, _signal_handler)

        await stop_event.wait()
        await self.stop()


# Entry Point
if __name__ == "__main__":
    bot = ChatFightBot()

    try:
        asyncio.run(bot.run())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Bot exited manually.")
        sys.exit(0)
