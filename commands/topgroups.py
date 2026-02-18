from pyrogram import filters
from pyrogram.handlers import MessageHandler
from pyrogram.enums import ParseMode
from services.leaderboard_service import get_top_groups
from ui.keyboards import ranking_keyboard


async def topgroups_cmd(client, message):

    data = await get_top_groups(client, "overall")

    if not data:
        await message.reply("📊 No data found.")
        return

    text = "🏆 <b>TOP GROUPS</b>\n\n"

    for i, (group_name, total) in enumerate(data, start=1):
        medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else f"{i}."
        text += f"{medal} {group_name} • {total}\n"

    await message.reply(
        text,
        reply_markup=ranking_keyboard("overall", "groups", 0),
        parse_mode=ParseMode.HTML
    )


topgroups_handler = MessageHandler(
    topgroups_cmd,
    filters.command("topgroups")
)
