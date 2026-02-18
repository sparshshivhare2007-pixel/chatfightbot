from pyrogram import filters
from pyrogram.handlers import MessageHandler
from pyrogram.enums import ParseMode
from database.connection import get_top_groups, get_group_info
from ui.keyboards import ranking_keyboard


async def topgroups_cmd(client, message):

    data = get_top_groups("overall")

    if not data:
        await message.reply("📊 No data found.")
        return

    text = "🏆 <b>TOP GROUPS</b>\n\n"

    for i, (group_id, total) in enumerate(data, start=1):

        group_info = get_group_info(group_id)

        if group_info:
            title = group_info.get("title", "Group")
        else:
            title = "Group"

        medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else f"{i}."

        text += f"{medal} {title} • {total}\n"

    await message.reply(
        text,
        reply_markup=ranking_keyboard("overall", "groups", 0),
        parse_mode=ParseMode.HTML
    )


topgroups_handler = MessageHandler(
    topgroups_cmd,
    filters.command("topgroups")
)
