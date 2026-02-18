from pyrogram import filters
from pyrogram.handlers import MessageHandler
from services.leaderboard_service import get_group_top
from ui.keyboards import ranking_keyboard


async def rankings_cmd(client, message):

    if message.chat.type not in ["group", "supergroup"]:
        await message.reply("❌ This command works only in groups.")
        return

    group_id = message.chat.id  # Important: int

    data = await get_group_top(group_id, "overall")

    if not data:
        await message.reply("📊 No ranking data found.")
        return

    text = "🏆 GROUP LEADERBOARD\n\n"

    for i, (username, total) in enumerate(data, start=1):
        text += f"{i}. {username} • {total}\n"

    await message.reply(
        text,
        reply_markup=ranking_keyboard("overall", "group", group_id)
    )


rankings_handler = MessageHandler(
    rankings_cmd,
    filters.command("rankings") & filters.group
)
