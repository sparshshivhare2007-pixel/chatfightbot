from pyrogram import filters
from pyrogram.handlers import MessageHandler
from services.leaderboard_service import get_global_top
from ui.keyboards import ranking_keyboard


async def topusers_cmd(client, message):

    data = await get_global_top(client, "overall")

    if not data:
        await message.reply("📊 No data found.")
        return

    text = "🌍 <b>GLOBAL LEADERBOARD</b>\n\n"

    for i, (username, total) in enumerate(data, start=1):
        medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else f"{i}."
        text += f"{medal} {username} • {total}\n"

    await message.reply(
        text,
        reply_markup=ranking_keyboard("overall", "global", 0),
        parse_mode="HTML"
    )


topusers_handler = MessageHandler(
    topusers_cmd,
    filters.command("topusers")
)
