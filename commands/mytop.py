from pyrogram import filters
from pyrogram.handlers import MessageHandler
from services.leaderboard_service import get_user_groups
from services.formatting_service import format_leaderboard

async def mytop_cmd(client, message):

    data = await get_user_groups(message.from_user.id)
    text = await format_leaderboard(data, "YOUR TOP GROUPS")

    await message.reply(text)

mytop_handler = MessageHandler(mytop_cmd, filters.command("mytop"))
