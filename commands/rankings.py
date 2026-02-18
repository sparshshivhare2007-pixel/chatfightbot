from pyrogram import filters
from pyrogram.handlers import MessageHandler
from pyrogram.enums import ChatType, ParseMode
import database as db
from ui.keyboards import ranking_keyboard


async def rankings_cmd(client, message):

    if message.chat.type not in [ChatType.GROUP, ChatType.SUPERGROUP]:
        await message.reply("❌ This command works only in groups.")
        return

    group_id = message.chat.id

    data = db.get_leaderboard(group_id, "overall")

    if not data:
        await message.reply("📊 No ranking data found.")
        return

    text = "🏆 <b>GROUP LEADERBOARD</b>\n\n"

    for i, (user_id, total) in enumerate(data, start=1):

        user_info = db.get_user_info(user_id)

        if user_info:
            username = user_info.get("username")
            display = f"@{username}" if username else user_info.get("full_name", "User")
        else:
            display = "User"

        medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else f"{i}."

        text += f"{medal} <a href='tg://user?id={user_id}'>{display}</a> • {total}\n"

    await message.reply(
        text,
        reply_markup=ranking_keyboard("overall", "group", group_id),
        parse_mode=ParseMode.HTML
    )


rankings_handler = MessageHandler(
    rankings_cmd,
    filters.command("rankings")
)
