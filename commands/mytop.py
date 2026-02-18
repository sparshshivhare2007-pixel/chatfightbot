from pyrogram import filters
from pyrogram.handlers import MessageHandler
from pyrogram.enums import ParseMode
from services.leaderboard_service import get_user_groups


async def mytop_cmd(client, message):

    data = await get_user_groups(client, message.from_user.id)

    if not data:
        await message.reply("📊 No activity data found.")
        return

    text = "🏆 <b>YOUR TOP GROUPS</b>\n\n"

    for i, (group_name, total) in enumerate(data, start=1):
        text += f"{i}. {group_name} • {total}\n"

    await message.reply(
        text,
        parse_mode=ParseMode.HTML
    )


mytop_handler = MessageHandler(
    mytop_cmd,
    filters.command("mytop")
)
