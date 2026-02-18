from pyrogram import filters
from pyrogram.handlers import MessageHandler
from services.counter_service import increment_counter

async def count_messages(client, message):
    if message.chat.type in ["group", "supergroup"] and not message.from_user.is_bot:
        await increment_counter(message.chat.id, message.from_user.id)

message_counter = MessageHandler(
    count_messages,
    filters.group & filters.text
)
