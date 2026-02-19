from pyrogram import filters
from pyrogram.handlers import MessageHandler
from pyrogram.enums import ChatType
from database import increment_message


async def count_messages(client, message):

    # Only count group messages
    if message.chat.type not in [ChatType.GROUP, ChatType.SUPERGROUP]:
        return

    # Ignore service messages
    if not message.from_user:
        return

    # Ignore bots
    if message.from_user.is_bot:
        return

    group_id = message.chat.id
    user_id = message.from_user.id

    # Increment counter
    await increment_counter(group_id, user_id)


# Count ALL normal messages (not only text)
message_counter = MessageHandler(
    count_messages,
    filters.group & ~filters.service
)
