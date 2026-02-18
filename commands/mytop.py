from pyrogram import filters
from pyrogram.handlers import MessageHandler
from pyrogram.enums import ParseMode
import database as db


async def mytop_cmd(client, message):

    user_id = message.from_user.id

    data = db.get_user_groups_stats(user_id, "overall")

    if not data:
        await message.reply("📊 No activity data found.")
        return

    text = "🏆 <b>YOUR TOP GROUPS</b>\n\n"

    for i, (group_id, total) in enumerate(data, start=1):

        group_info = db.get_group_info(group_id)

        if group_info:
            title = group_info.get("title", "Group")
        else:
            title = "Group"

        text += f"{i}. {title} • {total}\n"

    await message.reply(
        text,
        parse_mode=ParseMode.HTML
    )


mytop_handler = MessageHandler(
    mytop_cmd,
    filters.command("mytop")
)
