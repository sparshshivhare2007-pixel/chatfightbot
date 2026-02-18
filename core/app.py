from pyrogram import Client
from config import API_ID, API_HASH, BOT_TOKEN
from core.router import register_handlers
from core.scheduler import start_scheduler

def create_app():
    app = Client(
        "chatfight-pro",
        api_id=API_ID,
        api_hash=API_HASH,
        bot_token=BOT_TOKEN,
        workers=50
    )

    register_handlers(app)
    start_scheduler()

    return app
