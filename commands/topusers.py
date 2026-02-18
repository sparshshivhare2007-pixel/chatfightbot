from pyrogram import filters
from pyrogram.handlers import MessageHandler
from pyrogram.enums import ParseMode
import database as db


async def topusers_cmd(client, message):

    data = db.get_global_leaderboard("overall")

    if not data:
        await message.reply("📊 No data found.")
        return

    text = "🌍 <b>GLOBAL LEADERBOARD</b>\n\n"

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
        parse_mode=ParseMode.HTML
    )


topusers_handler = MessageHandler(
    topusers_cmd,
    filters.command("topusers")
)
