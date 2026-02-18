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


class ChatFightBot:

    def __init__(self):
        self.app = None

    async def start(self):
        logger.info("Starting ChatFight Pro...")

        # Create client INSIDE running loop
        self.app = Client(
            "chatfight-pro",
            api_id=API_ID,
            api_hash=API_HASH,
            bot_token=BOT_TOKEN,
            workers=100,
        )

        register_handlers(self.app)
        await create_indexes()
        start_scheduler()

        await self.app.start()

        me = await self.app.get_me()
        logger.info(f"Bot started as @{me.username}")

    async def stop(self):
        logger.info("Stopping ChatFight Pro...")
        if self.app:
            await self.app.stop()
        logger.info("Bot stopped successfully.")

    async def run(self):
        await self.start()

        stop_event = asyncio.Event()

        def shutdown():
            logger.info("Shutdown signal received.")
            stop_event.set()

        loop = asyncio.get_running_loop()
        loop.add_signal_handler(signal.SIGINT, shutdown)
        loop.add_signal_handler(signal.SIGTERM, shutdown)

        await stop_event.wait()
        await self.stop()


if __name__ == "__main__":
    uvloop.install()

    try:
        asyncio.run(ChatFightBot().run())
    except (KeyboardInterrupt, SystemExit):
        sys.exit(0)
