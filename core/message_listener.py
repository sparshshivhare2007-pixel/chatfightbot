from pyrogram import filters
from pyrogram.handlers import MessageHandler
from pyrogram.enums import ChatType
from database import increment_message


async def count_messages(client, message):

    if message.chat.type not in [ChatType.GROUP, ChatType.SUPERGROUP]:
        return

    if not message.from_user or message.from_user.is_bot:
        return

    # Mongo counter use karo
    increment_message(message.from_user, message.chat)


message_counter = MessageHandler(
    count_messages,
    filters.group & ~filters.service
)
