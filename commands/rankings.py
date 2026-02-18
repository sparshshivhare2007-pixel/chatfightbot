from pyrogram import filters
from pyrogram.handlers import MessageHandler
from pyrogram.enums import ParseMode
from services.leaderboard_service import get_group_top
from ui.keyboards import ranking_keyboard


async def rankings_cmd(client, message):

    # group check
    if message.chat.type not in ["group", "supergroup"]:
        await message.reply("❌ This command works only in groups.")
        return

    group_id = int(message.chat.id)

    data = await get_group_top(client, group_id, "overall")

    if not data:
        await message.reply("📊 No ranking data found.")
        return

    text = "🏆 <b>GROUP LEADERBOARD</b>\n\n"

    for i, (username, total) in enumerate(data, start=1):

        if i == 1:
            medal = "🥇"
        elif i == 2:
            medal = "🥈"
        elif i == 3:
            medal = "🥉"
        else:
            medal = f"{i}."

        text += f"{medal} {username} • {total}\n"

    await message.reply(
        text,
        reply_markup=ranking_keyboard("overall", "group", group_id),
        parse_mode=ParseMode.HTML
    )


rankings_handler = MessageHandler(
    rankings_cmd,
    filters.command("rankings") & filters.group
)
