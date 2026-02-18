from pyrogram import filters
from pyrogram.handlers import MessageHandler
from services.leaderboard_service import get_user_groups


async def mytop_cmd(client, message):

    data = await get_user_groups(message.from_user.id)

    if not data:
        await message.reply("📊 No activity data found.")
        return

    text = "🏆 YOUR TOP GROUPS\n\n"

    for i, (group_name, total) in enumerate(data, start=1):
        text += f"{i}. {group_name} • {total}\n"

    await message.reply(text)


mytop_handler = MessageHandler(mytop_cmd, filters.command("mytop"))
