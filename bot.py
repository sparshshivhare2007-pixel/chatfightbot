import asyncio
import signal
import sys

from pyrogram import Client
from pyrogram.enums import ParseMode

from config import API_ID, API_HASH, BOT_TOKEN
from core.router import register_handlers
from core.scheduler import start_scheduler
from utils.logger import logger


class ChatFightBot:

    def __init__(self):
        self.app: Client | None = None

    async def start(self):
        logger.info("Starting ChatFight Pro...")

        # Create Pyrogram Client (No SQLite session file)
        self.app = Client(
            name="chatfight_session",
            api_id=API_ID,
            api_hash=API_HASH,
            bot_token=BOT_TOKEN,
            workers=20,
            parse_mode=ParseMode.HTML,
            in_memory=True  # Prevent session DB lock
        )

        # Register all handlers
        register_handlers(self.app)

        # Start bot
        await self.app.start()

        # Start scheduler AFTER bot is running
        start_scheduler()

        me = await self.app.get_me()
        logger.info(f"Bot started successfully as @{me.username}")

    async def stop(self):
        logger.info("Stopping ChatFight Pro...")

        if self.app:
            await self.app.stop()

        logger.info("Bot stopped cleanly.")

    async def run(self):
        await self.start()

        stop_event = asyncio.Event()

        def shutdown():
            logger.info("Shutdown signal received.")
            stop_event.set()

        loop = asyncio.get_running_loop()

        # Graceful shutdown signals (Linux)
        try:
            loop.add_signal_handler(signal.SIGINT, shutdown)
            loop.add_signal_handler(signal.SIGTERM, shutdown)
        except NotImplementedError:
            # Windows fallback
            pass

        await stop_event.wait()
        await self.stop()


if __name__ == "__main__":
    try:
        asyncio.run(ChatFightBot().run())
    except (KeyboardInterrupt, SystemExit):
        sys.exit(0)
