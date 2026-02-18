from pyrogram import filters
from pyrogram.handlers import MessageHandler
from pyrogram.enums import ChatType, ParseMode
from database.connection import get_leaderboard, get_user_info
from ui.keyboards import ranking_keyboard


async def rankings_cmd(client, message):

    if message.chat.type not in [ChatType.GROUP, ChatType.SUPERGROUP]:
        await message.reply("❌ This command works only in groups.")
        return

    group_id = message.chat.id

    data = get_leaderboard(group_id, "overall")

    if not data:
        await message.reply("📊 No ranking data found.")
        return

    text = "🏆 <b>GROUP LEADERBOARD</b>\n\n"

    for i, (user_id, total) in enumerate(data, start=1):

        user_info = get_user_info(user_id)

        if user_info:
            name = user_info.get("username")
            if name:
                display = f"@{name}"
            else:
                display = user_info.get("full_name", "User")
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
